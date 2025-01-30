import asyncio
import base64
import json
import logging
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

import nacl.signing
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from websockets.client import WebSocketClientProtocol, connect
from websockets.exceptions import ConnectionClosed

from driftpy.accounts import get_user_stats_account_public_key
from driftpy.addresses import get_user_account_public_key
from driftpy.constants.perp_markets import (
    devnet_perp_market_configs,
    mainnet_perp_market_configs,
)
from driftpy.decode.swift_order import decode_swift_order_params_message
from driftpy.drift_client import DriftClient
from driftpy.types import MarketType, PostOnlyParams, SwiftOrderParamsMessage
from driftpy.user_map.user_map import UserMap

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class SwiftOrderSubscriberConfig:
    drift_client: DriftClient
    user_map: UserMap
    drift_env: str
    endpoint: Optional[str]
    market_indexes: List[int]
    keypair: Keypair


class SwiftOrderSubscriber:
    def __init__(self, config: SwiftOrderSubscriberConfig):
        print(f"Initializing SwiftOrderSubscriber with config: {config}")
        self.config = config
        self.drift_client = config.drift_client
        self.user_map = config.user_map
        self.ws: Optional[WebSocketClientProtocol] = None
        self.heartbeat_task = None
        self.heartbeat_interval = 60
        self.subscribed = False
        self.on_order = None

    def get_symbol_for_market_index(self, market_index: int) -> str:
        print(f"Getting symbol for market index: {market_index}")
        markets = (
            devnet_perp_market_configs
            if self.config.drift_env == "devnet"
            else mainnet_perp_market_configs
        )
        symbol = markets[market_index].symbol
        print(f"Found symbol: {symbol}")
        return symbol

    def generate_challenge_response(self, nonce: str) -> str:
        print(f"Generating challenge response for nonce: {nonce}")
        message_bytes = nonce.encode("utf-8")
        signing_key = nacl.signing.SigningKey(self.config.keypair.secret())
        signature = signing_key.sign(message_bytes).signature
        response = base64.b64encode(signature).decode("utf-8")
        print("Challenge response generated successfully")
        return response

    async def handle_auth_message(self, message: Dict) -> None:
        print(f"Handling auth message: {message}")
        if self.ws is None:
            logger.warning("WebSocket connection not established")
            return

        if message.get("channel") == "auth" and message.get("nonce"):
            print("Processing auth challenge")
            signature_base64 = self.generate_challenge_response(message["nonce"])
            await self.ws.send(
                json.dumps(
                    {
                        "pubkey": str(self.config.keypair.pubkey()),
                        "signature": signature_base64,
                    }
                )
            )
            print("Auth response sent")

        if (
            message.get("channel") == "auth"
            and isinstance(message.get("message"), str)
            and message["message"].lower() == "authenticated"
        ):
            print("Successfully authenticated")
            self.subscribed = True
            for market_index in self.config.market_indexes:
                print(f"Subscribing to market index: {market_index}")
                await self.ws.send(
                    json.dumps(
                        {
                            "action": "subscribe",
                            "market_type": "perp",
                            "market_name": self.get_symbol_for_market_index(
                                market_index
                            ),
                        }
                    )
                )
                await asyncio.sleep(0.1)

    async def subscribe(
        self, on_order: Callable[[Dict, SwiftOrderParamsMessage], None]
    ) -> None:
        print("Starting subscription process")
        self.on_order = on_order
        endpoint = self.config.endpoint or (
            "wss://master.swift.drift.trade/ws"
            if self.config.drift_env == "devnet"
            else "wss://swift.drift.trade/ws"
        )
        print(f"Using endpoint: {endpoint}")

        while True:
            try:
                print("Attempting WebSocket connection")
                async with connect(
                    f"{endpoint}?pubkey={str(self.config.keypair.pubkey())}",
                    open_timeout=30,  # Increase timeout to 30 seconds
                    ping_interval=20,  # Keep connection alive
                    ping_timeout=20,
                ) as websocket:
                    self.ws = websocket
                    print("Connected to the server")

                    while True:
                        try:
                            raw_message = await websocket.recv()
                            message = json.loads(raw_message)

                            if message.get("channel") == "auth":
                                await self.handle_auth_message(message)

                            if message.get("order"):
                                order = json.loads(message["order"])
                                swift_order_params_buf = bytes.fromhex(
                                    order["order_message"]
                                )
                                swift_order_params_message = (
                                    decode_swift_order_params_message(
                                        swift_order_params_buf
                                    )
                                )

                                if not swift_order_params_message.swift_order_params.price:
                                    logger.warning(
                                        f"Order has no price: {swift_order_params_message.swift_order_params}"
                                    )
                                    continue
                                await on_order(order, swift_order_params_message)

                        except ConnectionClosed:
                            logger.error("WebSocket connection closed")
                            break

            except asyncio.TimeoutError:
                logger.error("Connection timed out, waiting before retry...")
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"WebSocket error: {e}", exc_info=True)
                await asyncio.sleep(5)

            print("Disconnected from server, reconnecting...")
            await asyncio.sleep(1)

    async def get_place_and_make_swift_order_ixs(
        self,
        order_message_raw: Dict,
        swift_order_params_message: SwiftOrderParamsMessage,
        maker_order_params: Dict,
    ):
        swift_order_params_buf = bytes.fromhex(order_message_raw["order_message"])
        taker_authority = Pubkey.from_string(order_message_raw["taker_authority"])
        taker_user_pubkey = get_user_account_public_key(
            self.drift_client.program_id,
            taker_authority,
            swift_order_params_message.sub_account_id,
        )

        taker_user_account = (
            await self.user_map.must_get(str(taker_user_pubkey))
        ).get_user_account()

        maker_order_params.update(
            {
                "post_only": PostOnlyParams.MustPostOnly,
                "immediate_or_cancel": True,
                "market_type": MarketType.Perp,
            }
        )

        ixs = await self.drift_client.get_place_and_make_swift_perp_order_ixs(
            {
                "order_params": swift_order_params_buf,
                "signature": base64.b64decode(order_message_raw["order_signature"]),
                "user_stats": get_user_stats_account_public_key(
                    self.drift_client.program_id, taker_user_account.authority
                ),
            },
            order_message_raw["uuid"].encode("utf-8"),
            {
                "taker": taker_user_pubkey,
                "taker_user_account": taker_user_account,
                "taker_stats": get_user_stats_account_public_key(
                    self.drift_client.program_id, taker_user_account.authority
                ),
            },
            maker_order_params,
        )
        return ixs
