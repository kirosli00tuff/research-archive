"""The registered ticker-to-underlying mapping (H5 Section 2).

**Written before any price was read**, and mechanical: a ticker resolves iff
its exact string appears in one of the three tables below. Nothing here
fuzzy-matches, and nothing guesses. A ticker absent from all three tables is
``excluded_unresolvable`` with reason ``not_in_registered_mapping``, counted
and reported, never silently dropped and never assigned an underlying.

Three registered outcomes, counted separately and reported both separately
and as a union (the prompt's ``excluded_unresolvable`` is the union of the
two exclusion states):

- ``resolved`` — the ticker names an identifiable **equity, ETF, or index**
  underlying. Only these enter the H5 universe.
- ``excluded_non_equity`` — the ticker resolves confidently to something
  that is not an equity-style underlying: crypto, a crypto index, a
  commodity, an FX pair, or a rate instrument.
- ``excluded_unresolvable`` — the string does not resolve to an identifiable
  underlying at all: a private or pre-IPO issuer with no public price, an
  ambiguous ticker, an unnamed thematic basket, or a venue house index.

The registered admission criterion, stated once so it can be checked: an
entry is registered as ``resolved`` only where the ticker string is **(a) an
exact listed ticker symbol on a major exchange**, or **(b) an unambiguous
name or standard abbreviation of exactly one listed issuer or one named
public index**. Everything that fails both tests is excluded, including
several tickers whose likely meaning is obvious to a reader — a likely
meaning is a guess, and a guess is what this table exists to refuse.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

STATE_RESOLVED: Final = "resolved"
STATE_NON_EQUITY: Final = "excluded_non_equity"
STATE_UNRESOLVABLE: Final = "excluded_unresolvable"

KIND_EQUITY: Final = "equity"
KIND_ETF: Final = "etf"
KIND_INDEX: Final = "index"

FAMILY_SINGLE: Final = "equity_single"
FAMILY_ETF: Final = "equity_etf"
FAMILY_INDEX: Final = "equity_index"
FAMILY_VOL: Final = "volatility_index"


@dataclass(frozen=True, slots=True)
class Underlying:
    """One identifiable underlying. Descriptive metadata only, no price."""

    symbol: str
    kind: str
    family: str
    name: str


def _eq(symbol: str, name: str) -> Underlying:
    return Underlying(symbol=symbol, kind=KIND_EQUITY, family=FAMILY_SINGLE, name=name)


def _etf(symbol: str, name: str) -> Underlying:
    return Underlying(symbol=symbol, kind=KIND_ETF, family=FAMILY_ETF, name=name)


def _idx(symbol: str, name: str, family: str = FAMILY_INDEX) -> Underlying:
    return Underlying(symbol=symbol, kind=KIND_INDEX, family=family, name=name)


# --- table 1: resolved underlyings ------------------------------------------
RESOLVED: Final[dict[str, Underlying]] = {
    # US single equities, exact listed tickers
    "AAOI": _eq("AAOI", "Applied Optoelectronics"),
    "AAPL": _eq("AAPL", "Apple"),
    "AMAT": _eq("AMAT", "Applied Materials"),
    "AMD": _eq("AMD", "Advanced Micro Devices"),
    "AMZN": _eq("AMZN", "Amazon.com"),
    "ARM": _eq("ARM", "Arm Holdings ADR"),
    "ASML": _eq("ASML", "ASML Holding ADR"),
    "AVGO": _eq("AVGO", "Broadcom"),
    "BABA": _eq("BABA", "Alibaba Group ADR"),
    "BB": _eq("BB", "BlackBerry"),
    "BE": _eq("BE", "Bloom Energy"),
    "BMNR": _eq("BMNR", "Bitmine Immersion Technologies"),
    "BX": _eq("BX", "Blackstone"),
    "CAR": _eq("CAR", "Avis Budget Group"),
    "CIEN": _eq("CIEN", "Ciena"),
    "COHR": _eq("COHR", "Coherent"),
    "COIN": _eq("COIN", "Coinbase Global"),
    "COST": _eq("COST", "Costco Wholesale"),
    "CRCL": _eq("CRCL", "Circle Internet Group"),
    "CRDO": _eq("CRDO", "Credo Technology Group"),
    "CRWD": _eq("CRWD", "CrowdStrike Holdings"),
    "CRWV": _eq("CRWV", "CoreWeave"),
    "DELL": _eq("DELL", "Dell Technologies"),
    "DKNG": _eq("DKNG", "DraftKings"),
    "EBAY": _eq("EBAY", "eBay"),
    "GEV": _eq("GEV", "GE Vernova"),
    "GLW": _eq("GLW", "Corning"),
    "GME": _eq("GME", "GameStop"),
    "GOOGL": _eq("GOOGL", "Alphabet class A"),
    "HIMS": _eq("HIMS", "Hims & Hers Health"),
    "HOOD": _eq("HOOD", "Robinhood Markets"),
    "IBM": _eq("IBM", "International Business Machines"),
    "INTC": _eq("INTC", "Intel"),
    "IONQ": _eq("IONQ", "IonQ"),
    "IREN": _eq("IREN", "IREN Limited"),
    "LITE": _eq("LITE", "Lumentum Holdings"),
    "LLY": _eq("LLY", "Eli Lilly"),
    "LRCX": _eq("LRCX", "Lam Research"),
    "MELI": _eq("MELI", "MercadoLibre"),
    "META": _eq("META", "Meta Platforms"),
    "MRNA": _eq("MRNA", "Moderna"),
    "MRVL": _eq("MRVL", "Marvell Technology"),
    "MSFT": _eq("MSFT", "Microsoft"),
    "MSTR": _eq("MSTR", "Strategy (MicroStrategy)"),
    "MU": _eq("MU", "Micron Technology"),
    "NBIS": _eq("NBIS", "Nebius Group"),
    "NET": _eq("NET", "Cloudflare"),
    "NFLX": _eq("NFLX", "Netflix"),
    "NOK": _eq("NOK", "Nokia ADR"),
    "NOW": _eq("NOW", "ServiceNow"),
    "NVDA": _eq("NVDA", "NVIDIA"),
    "ORCL": _eq("ORCL", "Oracle"),
    "PLTR": _eq("PLTR", "Palantir Technologies"),
    "QCOM": _eq("QCOM", "Qualcomm"),
    "RDDT": _eq("RDDT", "Reddit"),
    "RIVN": _eq("RIVN", "Rivian Automotive"),
    "RKLB": _eq("RKLB", "Rocket Lab"),
    "RTX": _eq("RTX", "RTX Corporation"),
    "SMCI": _eq("SMCI", "Super Micro Computer"),
    "SNDK": _eq("SNDK", "SanDisk"),
    "STX": _eq("STX", "Seagate Technology"),
    "TER": _eq("TER", "Teradyne"),
    "TSLA": _eq("TSLA", "Tesla"),
    "TSM": _eq("TSM", "Taiwan Semiconductor ADR"),
    "USAR": _eq("USAR", "USA Rare Earth"),
    "VST": _eq("VST", "Vistra"),
    "WDC": _eq("WDC", "Western Digital"),
    "ZM": _eq("ZM", "Zoom Communications"),
    # Non-US single equities, unambiguous issuer names or exact tickers
    "CAMBRICON": _eq("SSE:688256", "Cambricon Technologies"),
    "GIGADEV": _eq("SSE:603986", "GigaDevice Semiconductor"),
    "HYUNDAI": _eq("KRX:005380", "Hyundai Motor Company"),
    "IBIDEN": _eq("TSE:4062", "Ibiden Co"),
    "INNOLIGHT": _eq("SZSE:300308", "Innolight Technology"),
    "KIOXIA": _eq("TSE:285A", "Kioxia Holdings"),
    "NAVER": _eq("KRX:035420", "NAVER Corporation"),
    "SMSN": _eq("SMSN", "Samsung Electronics GDR"),
    "SOFTBANK": _eq("TSE:9984", "SoftBank Group"),
    "TENCENT": _eq("HKEX:0700", "Tencent Holdings"),
    "XIAOMI": _eq("HKEX:1810", "Xiaomi Corporation"),
    # ETFs, exact listed tickers
    "EWJ": _etf("EWJ", "iShares MSCI Japan ETF"),
    "EWT": _etf("EWT", "iShares MSCI Taiwan ETF"),
    "EWY": _etf("EWY", "iShares MSCI South Korea ETF"),
    "EWZ": _etf("EWZ", "iShares MSCI Brazil ETF"),
    "KORU": _etf("KORU", "Direxion Daily South Korea Bull 3X"),
    "KSTR": _etf("KSTR", "KraneShares SSE STAR Market 50 ETF"),
    "KWEB": _etf("KWEB", "KraneShares CSI China Internet ETF"),
    "MAGS": _etf("MAGS", "Roundhill Magnificent Seven ETF"),
    "SMH": _etf("SMH", "VanEck Semiconductor ETF"),
    "SOXL": _etf("SOXL", "Direxion Daily Semiconductor Bull 3X"),
    "URNM": _etf("URNM", "Sprott Uranium Miners ETF"),
    "XBI": _etf("XBI", "SPDR S&P Biotech ETF"),
    "XLE": _etf("XLE", "Energy Select Sector SPDR"),
    # Named public equity indices
    "IBOV": _idx("IBOV", "Ibovespa"),
    "JP225": _idx("NI225", "Nikkei 225"),
    "JPN225": _idx("NI225", "Nikkei 225"),
    "KR200": _idx("KOSPI200", "KOSPI 200"),
    "NIFTY": _idx("NIFTY50", "Nifty 50"),
    "SMALL2000": _idx("RUT", "Russell 2000"),
    "SP500": _idx("SPX", "S&P 500"),
    "US500": _idx("SPX", "S&P 500"),
    "USA100": _idx("NDX", "Nasdaq-100"),
    "USA500": _idx("SPX", "S&P 500"),
    "USTECH": _idx("NDX", "Nasdaq-100"),
    "VIX": _idx("VIX", "CBOE Volatility Index", FAMILY_VOL),
}

# --- table 2: resolved, but not an equity-style underlying -------------------
CLASS_CRYPTO: Final = "crypto"
CLASS_CRYPTO_INDEX: Final = "crypto_index"
CLASS_COMMODITY: Final = "commodity"
CLASS_FX: Final = "fx"
CLASS_RATE: Final = "rate"

NON_EQUITY: Final[dict[str, str]] = {
    "1000PEPE": CLASS_CRYPTO,
    "ADA": CLASS_CRYPTO,
    "BASED": CLASS_CRYPTO,
    "BCH": CLASS_CRYPTO,
    "BNB": CLASS_CRYPTO,
    "BTC": CLASS_CRYPTO,
    "DOGE": CLASS_CRYPTO,
    "ENA": CLASS_CRYPTO,
    "ETH": CLASS_CRYPTO,
    "FARTCOIN": CLASS_CRYPTO,
    "HYPE": CLASS_CRYPTO,
    "IP": CLASS_CRYPTO,
    "LIGHTER": CLASS_CRYPTO,
    "LINK": CLASS_CRYPTO,
    # LIT appears on the wholly-crypto hyna dex only, where it is Litentry;
    # the Global X Lithium ETF shares the string and appears on no HIP-3 dex.
    "LIT": CLASS_CRYPTO,
    "LTC": CLASS_CRYPTO,
    "PUMP": CLASS_CRYPTO,
    "SOL": CLASS_CRYPTO,
    "SUI": CLASS_CRYPTO,
    "USDE": CLASS_CRYPTO,
    "XMR": CLASS_CRYPTO,
    "XPL": CLASS_CRYPTO,
    "XRP": CLASS_CRYPTO,
    "ZEC": CLASS_CRYPTO,
    "BTCD": CLASS_CRYPTO_INDEX,
    "OTHERS": CLASS_CRYPTO_INDEX,
    "TOTAL2": CLASS_CRYPTO_INDEX,
    "ALUMINIUM": CLASS_COMMODITY,
    "BRENTOIL": CLASS_COMMODITY,
    "COPPER": CLASS_COMMODITY,
    "CORN": CLASS_COMMODITY,
    "DRAM": CLASS_COMMODITY,
    "GAS": CLASS_COMMODITY,
    "GOLD": CLASS_COMMODITY,
    "GOLDJM": CLASS_COMMODITY,
    "H100": CLASS_COMMODITY,
    "NATGAS": CLASS_COMMODITY,
    "OIL": CLASS_COMMODITY,
    "PALLADIUM": CLASS_COMMODITY,
    "PLATINUM": CLASS_COMMODITY,
    "SILVER": CLASS_COMMODITY,
    "SILVERJM": CLASS_COMMODITY,
    "SOY": CLASS_COMMODITY,
    "TTF": CLASS_COMMODITY,
    "URANIUM": CLASS_COMMODITY,
    "USOIL": CLASS_COMMODITY,
    "WHEAT": CLASS_COMMODITY,
    "WTI": CLASS_COMMODITY,
    "DXY": CLASS_FX,
    "EUR": CLASS_FX,
    "GBP": CLASS_FX,
    "JPY": CLASS_FX,
    "KRW": CLASS_FX,
    "10Y": CLASS_RATE,
    "2Y": CLASS_RATE,
    "30Y": CLASS_RATE,
    "USBOND": CLASS_RATE,
}

# --- table 3: registered as unresolvable, with the reason -------------------
REASON_PRIVATE: Final = "private_no_public_underlying"
REASON_AMBIGUOUS: Final = "ambiguous_ticker"
REASON_BASKET: Final = "basket_no_named_reference"
REASON_HOUSE_INDEX: Final = "venue_house_index"
REASON_NOT_IN_MAPPING: Final = "not_in_registered_mapping"

UNRESOLVABLE: Final[dict[str, str]] = {
    "ANSEM": REASON_AMBIGUOUS,
    "ANTH": REASON_PRIVATE,
    "ANTHROPIC": REASON_PRIVATE,
    "BIOTECH": REASON_BASKET,
    "BIRD": REASON_AMBIGUOUS,
    "BOT": REASON_AMBIGUOUS,
    "CBRS": REASON_AMBIGUOUS,
    "CL": REASON_AMBIGUOUS,
    "CXMT": REASON_PRIVATE,
    "DEFENSE": REASON_BASKET,
    "ENERGY": REASON_BASKET,
    "GLDMINE": REASON_BASKET,
    "INFOTECH": REASON_BASKET,
    "LYTE": REASON_AMBIGUOUS,
    "MAG7": REASON_BASKET,
    "MINIMAX": REASON_PRIVATE,
    "NCLD": REASON_AMBIGUOUS,
    "NUCLEAR": REASON_BASKET,
    "OAI": REASON_PRIVATE,
    "OPENAI": REASON_PRIVATE,
    "PURRDAT": REASON_AMBIGUOUS,
    "QNT": REASON_AMBIGUOUS,
    "ROBOT": REASON_BASKET,
    "SEMI": REASON_BASKET,
    "SEMIS": REASON_BASKET,
    "SHAZ": REASON_AMBIGUOUS,
    "SHEIN": REASON_PRIVATE,
    "SKHX": REASON_AMBIGUOUS,
    "SKHY": REASON_AMBIGUOUS,
    "SPACEX": REASON_PRIVATE,
    "SPCX": REASON_AMBIGUOUS,
    "STRC": REASON_AMBIGUOUS,
    "UNITREE": REASON_PRIVATE,
    "USENERGY": REASON_BASKET,
    "VOL": REASON_AMBIGUOUS,
    "XYZ100": REASON_HOUSE_INDEX,
    "ZHIPU": REASON_PRIVATE,
}


class MappingConflict(RuntimeError):
    """A ticker appears in more than one registered table. Refused loudly."""


def _check_tables() -> None:
    """The three tables are disjoint. A collision is a defect, not a default."""
    names: tuple[tuple[str, frozenset[str]], ...] = (
        ("RESOLVED", frozenset(RESOLVED)),
        ("NON_EQUITY", frozenset(NON_EQUITY)),
        ("UNRESOLVABLE", frozenset(UNRESOLVABLE)),
    )
    for i, (a_name, a) in enumerate(names):
        for b_name, b in names[i + 1 :]:
            overlap = sorted(a & b)
            if overlap:
                raise MappingConflict(
                    f"{a_name} and {b_name} both claim {overlap}; the registered mapping "
                    f"must be a partition, and nothing here picks a winner"
                )


_check_tables()


@dataclass(frozen=True, slots=True)
class Resolution:
    """One instrument's registered resolution. No price, no venue field."""

    coin: str
    dex: str
    ticker: str
    state: str
    reason: str
    underlying: Underlying | None

    @property
    def is_resolved(self) -> bool:
        return self.state == STATE_RESOLVED


def bare_ticker(coin: str) -> str:
    """The ticker after the dex prefix. `xyz:AAPL` -> `AAPL`; no prefix -> as-is."""
    return coin.split(":", 1)[1] if ":" in coin else coin


def resolve(coin: str, dex: str) -> Resolution:
    """Apply the registered mapping. Exact string lookup, no fuzzy matching."""
    ticker = bare_ticker(coin)
    underlying = RESOLVED.get(ticker)
    if underlying is not None:
        return Resolution(
            coin=coin,
            dex=dex,
            ticker=ticker,
            state=STATE_RESOLVED,
            reason=underlying.kind,
            underlying=underlying,
        )
    non_equity = NON_EQUITY.get(ticker)
    if non_equity is not None:
        return Resolution(
            coin=coin,
            dex=dex,
            ticker=ticker,
            state=STATE_NON_EQUITY,
            reason=non_equity,
            underlying=None,
        )
    return Resolution(
        coin=coin,
        dex=dex,
        ticker=ticker,
        state=STATE_UNRESOLVABLE,
        reason=UNRESOLVABLE.get(ticker, REASON_NOT_IN_MAPPING),
        underlying=None,
    )
