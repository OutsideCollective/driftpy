from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from anchorpy.program.context import Context
from anchorpy.program.core import Program
from anchorpy.provider import Provider, Wallet
from anchorpy_core.idl import Idl
from construct import Int32sl, Int64ul
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solders.instruction import Instruction
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.system_program import CreateAccountParams, create_account
from spl.token._layouts import ACCOUNT_LAYOUT, MINT_LAYOUT
from spl.token.async_client import AsyncToken
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import (
    InitializeAccountParams,
    InitializeMintParams,
    MintToParams,
    initialize_account,
    initialize_mint,
    mint_to,
)

from driftpy.account_subscription_config import AccountSubscriptionConfig
from driftpy.accounts.bulk_account_loader import BulkAccountLoader
from driftpy.accounts.polling.drift_client import PollingDriftClientAccountSubscriber
from driftpy.admin import Admin
from driftpy.constants.numeric_constants import (
    QUOTE_PRECISION,
    SPOT_MARKET_WEIGHT_PRECISION,
    SPOT_RATE_PRECISION,
)
from driftpy.drift_client import DriftClient
from driftpy.math.amm import calculate_amm_reserves_after_swap, calculate_price
from driftpy.types import (
    AssetType,
    OracleInfo,
    OracleSource,
    PerpMarketAccount,
    PositionDirection,
    SwapDirection,
)

NATIVE_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112")
LAMPORTS_PER_SOL = 1_000_000_000


async def adjust_oracle_pretrade(
    baa: int,
    position_direction: PositionDirection,
    market: PerpMarketAccount,
    oracle_program: Program,
):
    price = calculate_price(
        market.amm.base_asset_reserve,
        market.amm.quote_asset_reserve,
        market.amm.peg_multiplier,
    )
    swap_direction = (
        SwapDirection.Add
        if position_direction == PositionDirection.Short()  # type: ignore
        else SwapDirection.Remove
    )
    new_qar, new_bar = calculate_amm_reserves_after_swap(
        market.amm,
        AssetType.BASE(),  # type: ignore
        abs(baa),
        swap_direction,  # type: ignore
    )
    newprice = calculate_price(new_bar, new_qar, market.amm.peg_multiplier)
    await set_price_feed(oracle_program, market.amm.oracle, newprice)
    print(f"oracle: {price} -> {newprice}")

    return newprice


async def _airdrop_user(
    provider: Provider, user: Optional[Keypair] = None
) -> tuple[Keypair, Signature]:
    if user is None:
        user = Keypair()
    resp = await provider.connection.request_airdrop(user.pubkey(), 100_0 * 1000000000)
    tx_sig = resp.value
    return user, tx_sig


async def _create_mint(provider: Provider) -> Keypair:
    fake_create_mint = Keypair()
    params = CreateAccountParams(
        from_pubkey=provider.wallet.public_key,
        to_pubkey=fake_create_mint.pubkey(),
        lamports=await AsyncToken.get_min_balance_rent_for_exempt_for_mint(
            provider.connection
        ),
        space=MINT_LAYOUT.sizeof(),
        owner=TOKEN_PROGRAM_ID,
    )
    create_create_mint_account_ix = create_account(params)
    init_collateral_mint_ix = initialize_mint(
        InitializeMintParams(
            decimals=6,
            program_id=TOKEN_PROGRAM_ID,
            mint=fake_create_mint.pubkey(),
            mint_authority=provider.wallet.public_key,
            freeze_authority=None,
        )
    )

    fake_tx = Transaction(
        instructions=[create_create_mint_account_ix, init_collateral_mint_ix],
        recent_blockhash=(
            await provider.connection.get_latest_blockhash()
        ).value.blockhash,
        fee_payer=provider.wallet.public_key,
    )

    fake_tx.sign_partial(fake_create_mint)
    provider.wallet.sign_transaction(fake_tx)
    await provider.send(fake_tx)
    return fake_create_mint


async def _create_user_ata_tx(
    account: Keypair, provider: Provider, mint: Keypair, owner: Pubkey
) -> Transaction:
    fake_tx = Transaction()

    create_token_account_ix = create_account(
        CreateAccountParams(
            from_pubkey=provider.wallet.public_key,
            to_pubkey=account.pubkey(),
            lamports=await AsyncToken.get_min_balance_rent_for_exempt_for_account(
                provider.connection
            ),
            space=ACCOUNT_LAYOUT.sizeof(),
            owner=TOKEN_PROGRAM_ID,
        )
    )
    fake_tx.add(create_token_account_ix)

    init_token_account_ix = initialize_account(
        InitializeAccountParams(
            program_id=TOKEN_PROGRAM_ID,
            account=account.pubkey(),
            mint=mint.pubkey(),
            owner=owner,
        )
    )
    fake_tx.add(init_token_account_ix)

    return fake_tx


def mint_ix(
    usdc_mint: Pubkey,
    mint_auth: Pubkey,
    usdc_amount: int,
    ata_account: Pubkey,
) -> Instruction:
    mint_to_user_account_tx = mint_to(
        MintToParams(
            program_id=TOKEN_PROGRAM_ID,
            mint=usdc_mint,
            dest=ata_account,
            mint_authority=mint_auth,
            signers=[],
            amount=usdc_amount,
        )
    )
    return mint_to_user_account_tx


def _mint_usdc_tx(
    usdc_mint: Keypair,
    provider: Provider,
    usdc_amount: int,
    ata_account: Pubkey,
) -> Transaction:
    fake_usdc_tx = Transaction()

    mint_to_user_account_tx = mint_to(
        MintToParams(
            program_id=TOKEN_PROGRAM_ID,
            mint=usdc_mint.pubkey(),
            dest=ata_account,
            mint_authority=provider.wallet.public_key,
            signers=[],
            amount=usdc_amount,
        )
    )
    fake_usdc_tx.add(mint_to_user_account_tx)

    return fake_usdc_tx


async def _create_and_mint_user_usdc(
    usdc_mint: Keypair, provider: Provider, usdc_amount: int, owner: Pubkey
) -> Keypair:
    usdc_account = Keypair()

    ata_tx: Transaction = await _create_user_ata_tx(
        usdc_account,
        provider,
        usdc_mint,
        owner,
    )
    mint_tx: Transaction = _mint_usdc_tx(
        usdc_mint, provider, usdc_amount, usdc_account.pubkey()
    )

    for ix in mint_tx.instructions:
        ata_tx.add(ix)

    ata_tx.recent_blockhash = (
        await provider.connection.get_latest_blockhash()
    ).value.blockhash
    ata_tx.fee_payer = provider.wallet.payer.pubkey()

    ata_tx.sign_partial(usdc_account)
    ata_tx.sign(provider.wallet.payer)

    await provider.send(ata_tx)

    return usdc_account


async def create_user_with_usdc_account(
    provider: Provider,
    usdc_mint: Keypair,
    usdc_amount: int,
    market_indexes: list[int],
    bank_indexes: list[int],
    oracle_infos: list[OracleInfo] = [],
    account_loader: BulkAccountLoader | None = None,
) -> tuple[DriftClient, Pubkey, Keypair]:
    user_keypair = await create_funded_keypair(provider)
    usdc_account = await create_usdc_account_for_user(
        provider, user_keypair, usdc_mint, usdc_amount
    )
    drift_client = await initialize_and_subscribe_drift_client(
        provider.connection,
        user_keypair,
        market_indexes,
        bank_indexes,
        oracle_infos,
        account_loader,
    )

    return drift_client, usdc_account, user_keypair


async def create_funded_keypair(provider: Provider) -> Keypair:
    keypair = Keypair()
    await provider.connection.request_airdrop(keypair.pubkey(), 100 * LAMPORTS_PER_SOL)
    return keypair


async def create_usdc_account_for_user(
    provider: Provider,
    user_keypair: Keypair,
    usdc_mint: Keypair,
    usdc_amount: int,
) -> Pubkey:
    user_usdc_account = await _create_and_mint_user_usdc(
        usdc_mint, provider, usdc_amount, user_keypair.pubkey()
    )
    return user_usdc_account.pubkey()


async def initialize_and_subscribe_drift_client(
    connection: AsyncClient,
    user_keypair: Keypair,
    market_indexes: list[int],
    bank_indexes: list[int],
    oracle_infos: list[OracleInfo] = [],
    account_loader: BulkAccountLoader | None = None,
) -> DriftClient:
    account_subscription = AccountSubscriptionConfig("websocket")
    if account_loader is not None:
        account_subscription = AccountSubscriptionConfig(
            "polling", bulk_account_loader=account_loader
        )

    drift_client = DriftClient(
        connection=connection,
        wallet=Wallet(user_keypair),
        perp_market_indexes=market_indexes,
        spot_market_indexes=bank_indexes,
        oracle_infos=oracle_infos,
        account_subscription=account_subscription,
    )
    await drift_client.subscribe()
    await drift_client.initialize_user()
    return drift_client


async def set_price_feed(
    oracle_program: Program,
    oracle_public_key: Pubkey,
    price: float,
):
    data = await get_feed_data(oracle_program, oracle_public_key)
    int_price = int(price * 10**-data.exponent)
    return await oracle_program.rpc["set_price"](
        int_price, ctx=Context(accounts={"price": oracle_public_key})
    )


async def set_price_feed_detailed(
    oracle_program: Program,
    oracle_public_key: Pubkey,
    price: float,
    conf: float,
    slot: int,
):
    data = await get_feed_data(oracle_program, oracle_public_key)
    int_price = int(price * 10**-data.exponent)
    int_conf = int(abs(conf) * 10**-data.exponent)
    print("setting oracle price", int_price, "+/-", int_conf, "@ slot=", slot)
    return await oracle_program.rpc["set_price_info"](
        int_price, int_conf, slot, ctx=Context(accounts={"price": oracle_public_key})
    )


async def get_set_price_feed_detailed_ix(
    oracle_program: Program,
    oracle_public_key: Pubkey,
    price: float,
    conf: float,
    slot: int,
):
    data = await get_feed_data(oracle_program, oracle_public_key)
    int_price = int(price * 10**-data.exponent)
    int_conf = int(abs(conf) * 10**-data.exponent)
    print("setting oracle price", int_price, "+/-", int_conf, "@ slot=", slot)
    return oracle_program.instruction["set_price_info"](
        int_price, int_conf, slot, ctx=Context(accounts={"price": oracle_public_key})
    )


async def create_price_feed(
    *,  # enforce keyword arguments
    oracle_program: Program,
    init_price: int,
    confidence: Optional[int] = None,
    expo: int = -4,
) -> Pubkey:
    conf = int((init_price / 10) * 10**-expo) if confidence is None else confidence
    collateral_token_feed = Keypair()
    space = 3312
    lamports = (
        await oracle_program.provider.connection.get_minimum_balance_for_rent_exemption(
            space
        )
    ).value

    tx_sig = await oracle_program.rpc["initialize"](
        int(init_price * 10**-expo),
        expo,
        conf,
        ctx=Context(
            accounts={"price": collateral_token_feed.pubkey()},
            signers=[collateral_token_feed],
            pre_instructions=[
                create_account(
                    CreateAccountParams(
                        from_pubkey=oracle_program.provider.wallet.public_key,
                        to_pubkey=collateral_token_feed.pubkey(),
                        space=space,
                        lamports=lamports,
                        owner=oracle_program.program_id,
                    )
                ),
            ],
        ),
    )
    print(tx_sig)
    return collateral_token_feed.pubkey()


@dataclass
class PriceData:
    exponent: int
    price: int


def parse_price_data(data: bytes) -> PriceData:
    exponent = Int32sl.parse(data[20:24])
    raw_price = Int64ul.parse(data[208:216])
    price = raw_price * 10**exponent
    return PriceData(exponent, price)


async def get_feed_data(oracle_program: Program, price_feed: Pubkey) -> PriceData:
    info_resp = await oracle_program.provider.connection.get_account_info(price_feed)
    if info_resp.value is None:
        raise ValueError("Account info is None")
    return parse_price_data(info_resp.value.data)


async def get_oracle_data(
    connection: AsyncClient,
    oracle_addr: Pubkey,
):
    info_resp = await connection.get_account_info(oracle_addr)
    if info_resp.value is None:
        raise ValueError("Account info is None")
    return parse_price_data(info_resp.value.data)


async def mock_oracle(
    pyth_program: Program,
    price: int = int(50 * 10e7),
    expo: int = -7,
    confidence: Optional[int] = None,
) -> Pubkey:
    price_feed_address = await create_price_feed(
        oracle_program=pyth_program, init_price=price, expo=expo, confidence=confidence
    )

    feed_data = await get_feed_data(pyth_program, price_feed_address)

    if feed_data.price != price:
        print(f"mockOracle precision error: {feed_data.price} != {price}")

    assert abs(feed_data.price - price) < 1e-10, f"{feed_data.price} {price}"
    return price_feed_address


async def initialize_sol_spot_market(
    admin: Admin,
    sol_oracle: Pubkey,
    sol_mint: Pubkey = NATIVE_MINT,
    oracle_source: OracleSource = OracleSource.Pyth(),  # type: ignore
):
    optimal_utilization = SPOT_RATE_PRECISION // 2
    optimal_rate = SPOT_RATE_PRECISION * 20
    max_rate = SPOT_RATE_PRECISION * 50
    initial_asset_weight = (SPOT_MARKET_WEIGHT_PRECISION * 8) // 10
    maintenance_asset_weight = (SPOT_MARKET_WEIGHT_PRECISION * 9) // 10
    initial_liability_weight = (SPOT_MARKET_WEIGHT_PRECISION * 12) // 10
    maintenance_liability_weight = (SPOT_MARKET_WEIGHT_PRECISION * 11) // 10

    market_index = admin.get_state_account().number_of_markets  # type: ignore

    sig = await admin.initialize_spot_market(
        sol_mint,
        optimal_utilization,
        optimal_rate,
        max_rate,
        sol_oracle,
        oracle_source,
        initial_asset_weight,
        maintenance_asset_weight,
        initial_liability_weight,
        maintenance_liability_weight,
    )

    await admin.update_withdraw_guard_threshold(
        market_index, (10**10) * QUOTE_PRECISION
    )

    return sig


async def initialize_quote_spot_market(
    admin: Admin,
    usdc_mint: Pubkey,
):
    optimal_utilization = SPOT_RATE_PRECISION // 2  # 50% utilization
    optimal_rate = SPOT_RATE_PRECISION
    max_rate = SPOT_RATE_PRECISION
    initial_asset_weight = SPOT_MARKET_WEIGHT_PRECISION
    maintenance_asset_weight = SPOT_MARKET_WEIGHT_PRECISION
    initial_liability_weight = SPOT_MARKET_WEIGHT_PRECISION
    maintenance_liability_weight = SPOT_MARKET_WEIGHT_PRECISION
    imf_factor = 0

    state_account = admin.get_state_account()
    if state_account is None:
        raise ValueError("State account is None")
    market_index = state_account.number_of_spot_markets

    sig = await admin.initialize_spot_market(
        mint=usdc_mint,
        optimal_utilization=optimal_utilization,
        optimal_rate=optimal_rate,
        max_rate=max_rate,
        oracle=Pubkey.default(),
        oracle_source=OracleSource.QuoteAsset(),  # type: ignore
        initial_asset_weight=initial_asset_weight,
        maintenance_asset_weight=maintenance_asset_weight,
        initial_liability_weight=initial_liability_weight,
        maintenance_liability_weight=maintenance_liability_weight,
        imf_factor=imf_factor,
    )

    if isinstance(admin.account_subscriber, PollingDriftClientAccountSubscriber):
        admin.account_subscriber.spot_oracle_map[0] = Pubkey.default()

    await admin.update_withdraw_guard_threshold(
        market_index, (10**10) * QUOTE_PRECISION
    )

    return sig


async def mock_oracle_no_program(
    connection: AsyncClient,
    wallet: Wallet,
    price: int = int(50 * 10e7),
    expo: int = -7,
    confidence: Optional[int] = None,
) -> Pubkey:
    pyth_idl = (
        Path(__file__).parent.parent.parent.parent
        / "protocol-v2"
        / "target"
        / "idl"
        / "pyth.json"
    )
    idl = Idl.from_json(pyth_idl.read_text())
    provider = Provider(connection, wallet)
    program = Program(
        idl=idl,
        program_id=Pubkey.from_string("FsJ3A3u2vn5cTVofAjvy6y5kwABJAqYWpe4975bi2epH"),
        provider=provider,
    )

    price_feed_address = await create_price_feed_no_program(
        connection,
        wallet,
        price,
        program,
        confidence,
        expo,
    )

    feed_data = await get_oracle_data(connection, price_feed_address)

    if feed_data.price != price:
        print(f"mockOracle precision error: {feed_data.price} != {price}")

    assert abs(feed_data.price - price) < 1e-10, f"{feed_data.price} {price}"

    return price_feed_address


async def create_price_feed_no_program(
    connection: AsyncClient,
    wallet: Wallet,
    init_price: int,
    program: Program,
    confidence: Optional[int] = None,
    expo: int = -4,
) -> Pubkey:
    conf = confidence if confidence is not None else int((init_price / 10) * 10**-expo)

    collateral_token_feed = Keypair()
    create_account_ix = create_account(
        CreateAccountParams(
            from_pubkey=wallet.payer.pubkey(),
            to_pubkey=collateral_token_feed.pubkey(),
            space=3312,
            lamports=int(LAMPORTS_PER_SOL / 20),  # hardcoded based on mainnet
            owner=program.program_id,
        )
    )

    init_ix = program.instruction["initialize"](
        int(init_price * 10**-expo),
        expo,
        conf,
        ctx=Context(accounts={"price": collateral_token_feed.pubkey()}),
    )

    tx = Transaction()
    tx.add(create_account_ix)
    tx.add(init_ix)
    tx.recent_blockhash = (await connection.get_latest_blockhash()).value.blockhash
    tx.fee_payer = wallet.payer.pubkey()
    tx.sign(*[wallet.payer, collateral_token_feed])

    provider = Provider(connection, wallet)
    await provider.send(tx)

    return collateral_token_feed.pubkey()
