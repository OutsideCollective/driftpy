from dataclasses import dataclass
from driftpy.types import OracleSource
from solders.pubkey import Pubkey  # type: ignore


@dataclass
class PerpMarketConfig:
    symbol: str
    base_asset_symbol: str
    market_index: int
    oracle: Pubkey
    oracle_source: OracleSource


devnet_perp_market_configs: list[PerpMarketConfig] = [
    PerpMarketConfig(
        symbol="SOL-PERP",
        base_asset_symbol="SOL",
        market_index=0,
        oracle=Pubkey.from_string("BAtFj4kQttZRVep3UZS2aZRDixkGYgWsbqTBVDbnSsPF"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="BTC-PERP",
        base_asset_symbol="BTC",
        market_index=1,
        oracle=Pubkey.from_string("486kr3pmFPfTsS4aZgcsQ7kS4i9rjMsYYZup6HQNSTT4"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="ETH-PERP",
        base_asset_symbol="ETH",
        market_index=2,
        oracle=Pubkey.from_string("6bEp2MiyoiiiDxcVqE8rUHQWwHirXUXtKfAEATTVqNzT"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="APT-PERP",
        base_asset_symbol="APT",
        market_index=3,
        oracle=Pubkey.from_string("79EWaCYU9jiQN8SbvVzGFAhAncUZYp3PjNg7KxmN5cLE"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="1MBONK-PERP",
        base_asset_symbol="1MBONK",
        market_index=4,
        oracle=Pubkey.from_string("GojbSnJuPdKDT1ZuHuAM5t9oz6bxTo1xhUKpTua2F72p"),
        oracle_source=OracleSource.Pyth1MPull(),
    ),
    PerpMarketConfig(
        symbol="MATIC-PERP",
        base_asset_symbol="MATIC",
        market_index=5,
        oracle=Pubkey.from_string("BrzyDgwELy4jjjsqLQpBeUxzrsueYyMhuWpYBaUYcXvi"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="ARB-PERP",
        base_asset_symbol="ARB",
        market_index=6,
        oracle=Pubkey.from_string("8ocfAdqVRnzvfdubQaTxar4Kz5HJhNbPNmkLxswqiHUD"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="DOGE-PERP",
        base_asset_symbol="DOGE",
        market_index=7,
        oracle=Pubkey.from_string("23y63pHVwKfYSCDFdiGRaGbTYWoyr8UzhUE7zukyf6gK"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="BNB-PERP",
        base_asset_symbol="BNB",
        market_index=8,
        oracle=Pubkey.from_string("Dk8eWjuQHMbxJAwB9Sg7pXQPH4kgbg8qZGcUrWcD9gTm"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="SUI-PERP",
        base_asset_symbol="SUI",
        market_index=9,
        oracle=Pubkey.from_string("HBordkz5YxjzNURmKUY4vfEYFG9fZyZNeNF1VDLMoemT"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="1MPEPE-PERP",
        base_asset_symbol="1MPEPE",
        market_index=10,
        oracle=Pubkey.from_string("CLxofhtzvLiErpn25wvUzpZXEqBhuZ6WMEckEraxyuGt"),
        oracle_source=OracleSource.Pyth1MPull(),
    ),
    PerpMarketConfig(
        symbol="OP-PERP",
        base_asset_symbol="OP",
        market_index=11,
        oracle=Pubkey.from_string("C9Zi2Y3Mt6Zt6pcFvobN3N29HcrzKujPAPBDDTDRcUa2"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="RNDR-PERP",
        base_asset_symbol="RNDR",
        market_index=12,
        oracle=Pubkey.from_string("8TQztfGcNjHGRusX4ejQQtPZs3Ypczt9jWF6pkgQMqUX"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="XRP-PERP",
        base_asset_symbol="XRP",
        market_index=13,
        oracle=Pubkey.from_string("9757epAjXWCWQH98kyK9vzgehd1XDVEf7joNHUaKk3iV"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="HNT-PERP",
        base_asset_symbol="HNT",
        market_index=14,
        oracle=Pubkey.from_string("9b1rcK9RUPK2vAqwNYCYEG34gUVpS2WGs2YCZZy2X5Tb"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="INJ-PERP",
        base_asset_symbol="INJ",
        market_index=15,
        oracle=Pubkey.from_string("BfXcyDWJmYADa5eZD7gySSDd6giqgjvm7xsAhQ239SUD"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="LINK-PERP",
        base_asset_symbol="LINK",
        market_index=16,
        oracle=Pubkey.from_string("Gwvob7yoLMgQRVWjScCRyQFMsgpRKrSAYisYEyjDJwEp"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="RLB-PERP",
        base_asset_symbol="RLB",
        market_index=17,
        oracle=Pubkey.from_string("4CyhPqyVK3UQHFWhEpk91Aw4WbBsN3JtyosXH6zjoRqG"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="PYTH-PERP",
        base_asset_symbol="PYTH",
        market_index=18,
        oracle=Pubkey.from_string("GqkCu7CbsPVz1H6W6AAHuReqbJckYG59TXz7Y5HDV7hr"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="TIA-PERP",
        base_asset_symbol="TIA",
        market_index=19,
        oracle=Pubkey.from_string("C6LHPUrgjrgo5eNUitC8raNEdEttfoRhmqdJ3BHVBJhi"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="JTO-PERP",
        base_asset_symbol="JTO",
        market_index=20,
        oracle=Pubkey.from_string("Ffq6ACJ17NAgaxC6ocfMzVXL3K61qxB2xHg6WUawWPfP"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="SEI-PERP",
        base_asset_symbol="SEI",
        market_index=21,
        oracle=Pubkey.from_string("EVyoxFo5jWpv1vV7p6KVjDWwVqtTqvrZ4JMFkieVkVsD"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="AVAX-PERP",
        base_asset_symbol="AVAX",
        market_index=22,
        oracle=Pubkey.from_string("FgBGHNex4urrBmNbSj8ntNQDGqeHcWewKtkvL6JE6dEX"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="W-PERP",
        base_asset_symbol="W",
        market_index=23,
        oracle=Pubkey.from_string("4iCi4DvXrubHQne8jzbMaWL3pd7v1Fip8iTe4H9vHNXB"),
        oracle_source=OracleSource.SwitchboardOnDemand(),
    ),
    PerpMarketConfig(
        symbol="KMNO-PERP",
        base_asset_symbol="KMNO",
        market_index=24,
        oracle=Pubkey.from_string("7aqj2wH1BH8XT3QQ3MWtvt3My7RAGf5Stm3vx5fiysJz"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="1KWEN-PERP",
        base_asset_symbol="1KWEN",
        market_index=25,
        oracle=Pubkey.from_string("F47c7aJgYkfKXQ9gzrJaEpsNwUKHprysregTWXrtYLFp"),
        oracle_source=OracleSource.Pyth1KPull(),
    ),
    PerpMarketConfig(
        symbol="TRUMP-WIN-2024-PREDICT",
        base_asset_symbol="TRUMP-WIN-2024",
        market_index=26,
        oracle=Pubkey.from_string("3TVuLmEGBRfVgrmFRtYTheczXaaoRBwcHw1yibZHSeNA"),
        oracle_source=OracleSource.Prelaunch(),
    ),
    PerpMarketConfig(
        symbol="KAMALA-POPULAR-VOTE-2024-PREDICT",
        base_asset_symbol="KAMALA-POPULAR-VOTE",
        market_index=27,
        oracle=Pubkey.from_string("GU6CA7a2KCyhpfqZNb36UAfc9uzKBM8jHjGdt245QhYX"),
        oracle_source=OracleSource.Prelaunch(),
    ),
]

mainnet_perp_market_configs: list[PerpMarketConfig] = [
    PerpMarketConfig(
        symbol="SOL-PERP",
        base_asset_symbol="SOL",
        market_index=0,
        oracle=Pubkey.from_string("BAtFj4kQttZRVep3UZS2aZRDixkGYgWsbqTBVDbnSsPF"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="BTC-PERP",
        base_asset_symbol="BTC",
        market_index=1,
        oracle=Pubkey.from_string("486kr3pmFPfTsS4aZgcsQ7kS4i9rjMsYYZup6HQNSTT4"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="ETH-PERP",
        base_asset_symbol="ETH",
        market_index=2,
        oracle=Pubkey.from_string("6bEp2MiyoiiiDxcVqE8rUHQWwHirXUXtKfAEATTVqNzT"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="APT-PERP",
        base_asset_symbol="APT",
        market_index=3,
        oracle=Pubkey.from_string("79EWaCYU9jiQN8SbvVzGFAhAncUZYp3PjNg7KxmN5cLE"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="1MBONK-PERP",
        base_asset_symbol="1MBONK",
        market_index=4,
        oracle=Pubkey.from_string("GojbSnJuPdKDT1ZuHuAM5t9oz6bxTo1xhUKpTua2F72p"),
        oracle_source=OracleSource.Pyth1MPull(),
    ),
    PerpMarketConfig(
        symbol="MATIC-PERP",
        base_asset_symbol="MATIC",
        market_index=5,
        oracle=Pubkey.from_string("BrzyDgwELy4jjjsqLQpBeUxzrsueYyMhuWpYBaUYcXvi"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="ARB-PERP",
        base_asset_symbol="ARB",
        market_index=6,
        oracle=Pubkey.from_string("8ocfAdqVRnzvfdubQaTxar4Kz5HJhNbPNmkLxswqiHUD"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="DOGE-PERP",
        base_asset_symbol="DOGE",
        market_index=7,
        oracle=Pubkey.from_string("23y63pHVwKfYSCDFdiGRaGbTYWoyr8UzhUE7zukyf6gK"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="BNB-PERP",
        base_asset_symbol="BNB",
        market_index=8,
        oracle=Pubkey.from_string("Dk8eWjuQHMbxJAwB9Sg7pXQPH4kgbg8qZGcUrWcD9gTm"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="SUI-PERP",
        base_asset_symbol="SUI",
        market_index=9,
        oracle=Pubkey.from_string("HBordkz5YxjzNURmKUY4vfEYFG9fZyZNeNF1VDLMoemT"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="1MPEPE-PERP",
        base_asset_symbol="1MPEPE",
        market_index=10,
        oracle=Pubkey.from_string("CLxofhtzvLiErpn25wvUzpZXEqBhuZ6WMEckEraxyuGt"),
        oracle_source=OracleSource.Pyth1MPull(),
    ),
    PerpMarketConfig(
        symbol="OP-PERP",
        base_asset_symbol="OP",
        market_index=11,
        oracle=Pubkey.from_string("C9Zi2Y3Mt6Zt6pcFvobN3N29HcrzKujPAPBDDTDRcUa2"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="RNDR-PERP",
        base_asset_symbol="RNDR",
        market_index=12,
        oracle=Pubkey.from_string("8TQztfGcNjHGRusX4ejQQtPZs3Ypczt9jWF6pkgQMqUX"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="XRP-PERP",
        base_asset_symbol="XRP",
        market_index=13,
        oracle=Pubkey.from_string("9757epAjXWCWQH98kyK9vzgehd1XDVEf7joNHUaKk3iV"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="HNT-PERP",
        base_asset_symbol="HNT",
        market_index=14,
        oracle=Pubkey.from_string("9b1rcK9RUPK2vAqwNYCYEG34gUVpS2WGs2YCZZy2X5Tb"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="INJ-PERP",
        base_asset_symbol="INJ",
        market_index=15,
        oracle=Pubkey.from_string("BfXcyDWJmYADa5eZD7gySSDd6giqgjvm7xsAhQ239SUD"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="LINK-PERP",
        base_asset_symbol="LINK",
        market_index=16,
        oracle=Pubkey.from_string("Gwvob7yoLMgQRVWjScCRyQFMsgpRKrSAYisYEyjDJwEp"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="RLB-PERP",
        base_asset_symbol="RLB",
        market_index=17,
        oracle=Pubkey.from_string("4CyhPqyVK3UQHFWhEpk91Aw4WbBsN3JtyosXH6zjoRqG"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="PYTH-PERP",
        base_asset_symbol="PYTH",
        market_index=18,
        oracle=Pubkey.from_string("GqkCu7CbsPVz1H6W6AAHuReqbJckYG59TXz7Y5HDV7hr"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="TIA-PERP",
        base_asset_symbol="TIA",
        market_index=19,
        oracle=Pubkey.from_string("C6LHPUrgjrgo5eNUitC8raNEdEttfoRhmqdJ3BHVBJhi"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="JTO-PERP",
        base_asset_symbol="JTO",
        market_index=20,
        oracle=Pubkey.from_string("Ffq6ACJ17NAgaxC6ocfMzVXL3K61qxB2xHg6WUawWPfP"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="SEI-PERP",
        base_asset_symbol="SEI",
        market_index=21,
        oracle=Pubkey.from_string("EVyoxFo5jWpv1vV7p6KVjDWwVqtTqvrZ4JMFkieVkVsD"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="AVAX-PERP",
        base_asset_symbol="AVAX",
        market_index=22,
        oracle=Pubkey.from_string("FgBGHNex4urrBmNbSj8ntNQDGqeHcWewKtkvL6JE6dEX"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="WIF-PERP",
        base_asset_symbol="WIF",
        market_index=23,
        oracle=Pubkey.from_string("6x6KfE7nY2xoLCRSMPT1u83wQ5fpGXoKNBqFjrCwzsCQ"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="JUP-PERP",
        base_asset_symbol="JUP",
        market_index=24,
        oracle=Pubkey.from_string("AwqRpfJ36jnSZQykyL1jYY35mhMteeEAjh7o8LveRQin"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="DYM-PERP",
        base_asset_symbol="DYM",
        market_index=25,
        oracle=Pubkey.from_string("hnefGsC8hJi8MBajpRSkUY97wJmLoBQYXaHkz3nmw1z"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="TAO-PERP",
        base_asset_symbol="TAO",
        market_index=26,
        oracle=Pubkey.from_string("5ZPtwR9QpBLcZQVMnVURuYBmZMu1qQrBcA9Gutc5eKN3"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="W-PERP",
        base_asset_symbol="W",
        market_index=27,
        oracle=Pubkey.from_string("4HbitGsdcFbtFotmYscikQFAAKJ3nYx4t7sV7fTvsk8U"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="KMNO-PERP",
        base_asset_symbol="KMNO",
        market_index=28,
        oracle=Pubkey.from_string("7aqj2wH1BH8XT3QQ3MWtvt3My7RAGf5Stm3vx5fiysJz"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="TNSR-PERP",
        base_asset_symbol="TNSR",
        market_index=29,
        oracle=Pubkey.from_string("13jpjpVyU5hGpjsZ4HzCcmBo85wze4N8Au7U6cC3GMip"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="DRIFT-PERP",
        base_asset_symbol="DRIFT",
        market_index=30,
        oracle=Pubkey.from_string("23KmX7SNikmUr2axSCy6Zer7XPBnvmVcASALnDGqBVRR"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="CLOUD-PERP",
        base_asset_symbol="CLOUD",
        market_index=31,
        oracle=Pubkey.from_string("4FG7UyPkszGvcSVCCKaLSZsArGjyxitwhJeQhYu2bFTS"),
        oracle_source=OracleSource.Switchboard(),
    ),
    PerpMarketConfig(
        symbol="IO-PERP",
        base_asset_symbol="IO",
        market_index=32,
        oracle=Pubkey.from_string("HxM66CFwGwrvfTFFkvvA8N3CnKX6m2obzameYWDaSSdA"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="ZEX-PERP",
        base_asset_symbol="ZEX",
        market_index=33,
        oracle=Pubkey.from_string("HVwBCaR4GEB1fHrp7xCTzbYoZXL3V8b1aek2swPrmGx3"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="POPCAT-PERP",
        base_asset_symbol="POPCAT",
        market_index=34,
        oracle=Pubkey.from_string("H3pn43tkNvsG5z3qzmERguSvKoyHZvvY6VPmNrJqiW5X"),
        oracle_source=OracleSource.PythPull(),
    ),
    PerpMarketConfig(
        symbol="1KWEN-PERP",
        base_asset_symbol="1KWEN",
        market_index=35,
        oracle=Pubkey.from_string("F47c7aJgYkfKXQ9gzrJaEpsNwUKHprysregTWXrtYLFp"),
        oracle_source=OracleSource.Pyth1KPull(),
    ),
    PerpMarketConfig(
        symbol="TRUMP-WIN-2024-BET",
        base_asset_symbol="TRUMP-WIN-2024",
        market_index=36,
        oracle=Pubkey.from_string("7YrQUxmxGdbk8pvns9KcL5ojbZSL2eHj62hxRqggtEUR"),
        oracle_source=OracleSource.Prelaunch(),
    ),
    PerpMarketConfig(
        symbol="KAMALA-POPULAR-VOTE-2024-BET",
        base_asset_symbol="KAMALA-POPULAR-VOTE-2024",
        market_index=37,
        oracle=Pubkey.from_string("AowFw1dCVjS8kngvTCoT3oshiUyL69k7P1uxqXwteWH4"),
        oracle_source=OracleSource.Prelaunch(),
    ),
    PerpMarketConfig(
        symbol="FED-CUT-50-SEPT-2024-BET",
        base_asset_symbol="FED-CUT-50-SEPT-2024",
        market_index=38,
        oracle=Pubkey.from_string("5QzgqAbEhJ1cPnLX4tSZEXezmW7sz7PPVVg2VanGi8QQ"),
        oracle_source=OracleSource.Prelaunch(),
    ),
    PerpMarketConfig(
        symbol="FED-CUT-50-SEPT-2024-BET",
        base_asset_symbol="FED-CUT-50-SEPT-2024",
        market_index=38,
        oracle=Pubkey.from_string("5QzgqAbEhJ1cPnLX4tSZEXezmW7sz7PPVVg2VanGi8QQ"),
        oracle_source=OracleSource.Prelaunch(),
    ),
    PerpMarketConfig(
        symbol="REPUBLICAN-POPULAR-AND-WIN-BET",
        base_asset_symbol="REPUBLICAN-POPULAR-AND-WIN",
        market_index=39,
        oracle=Pubkey.from_string("BtUUSUc9rZSzBmmKhQq4no65zHQTzMFeVYss7xcMRD53"),
        oracle_source=OracleSource.Prelaunch(),
    ),
    PerpMarketConfig(
        symbol="BREAKPOINT-IGGYERIC-BET",
        base_asset_symbol="BREAKPOINT-IGGYERIC",
        market_index=40,
        oracle=Pubkey.from_string("2ftYxoSupperd4ULxy9xyS2Az38wfAe7Lm8FCAPwjjVV"),
        oracle_source=OracleSource.Prelaunch(),
    ),
    PerpMarketConfig(
        symbol="DEMOCRATS-WIN-MICHIGAN-BET",
        base_asset_symbol="DEMOCRATS-WIN-MICHIGAN",
        market_index=41,
        oracle=Pubkey.from_string("8HTDLjhb2esGU5mu11v3pq3eWeFqmvKPkQNCnTTwKAyB"),
        oracle_source=OracleSource.Prelaunch(),
    ),
    PerpMarketConfig(
        symbol="TON-PERP",
        base_asset_symbol="TON",
        market_index=42,
        oracle=Pubkey.from_string("BNjCXrpEqjdBnuRy2SAUgm5Pq8B73wGFwsf6RYFJiLPY"),
        oracle_source=OracleSource.PythPull(),
    ),
]
