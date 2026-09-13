"""The H2 asset-class taxonomy (Amendment H2-5 section 1). Strings only.

A pure module: no path, no ledger, no venue, no payload reader. The dark H2
pair reader names a tier stratum and a class pair through this module, so it
must stay importable without touching anything that owns a path — the same
constraint `npl.pairtype` carries, and the guard tests pin it.

Assignment is mechanical and happens in two steps:

1. **The dex rule.** Every instrument on the main dex (``dex == ""``) and on
   the hyna dex is ``crypto``.
2. **The builder-dex ticker table.** Every other instrument takes its class
   from an exact-string lookup. The classes available on a builder dex are
   ``fx``, ``rates``, ``vol``, ``commodity``, ``index``, ``etf``, ``equity``;
   ``crypto`` is deliberately not among them, because step 1 is a dex rule.

A ticker in neither step is ``excluded_unclassifiable`` with its reason
recorded and counted. **It is never guessed and never takes a default.**

This table asks *what kind of thing the string names*, not *which specific
instrument it prices*. `npl.h5.resolution` asks the second question, because
H5 measures a basis against an external reference price and needs the
instrument itself; H2 needs only the factor the leg is exposed to. The two
tables are different by design and are never merged — neither imports the
other, and `tests/test_assetclass.py` pins that they stay separate.
"""

from __future__ import annotations

from typing import Final

# --- the eight registered classes -------------------------------------------
CLASS_CRYPTO: Final = "crypto"
CLASS_EQUITY: Final = "equity"
CLASS_ETF: Final = "etf"
CLASS_INDEX: Final = "index"
CLASS_COMMODITY: Final = "commodity"
CLASS_FX: Final = "fx"
CLASS_RATES: Final = "rates"
CLASS_VOL: Final = "vol"

REGISTERED_CLASSES: Final[frozenset[str]] = frozenset(
    {
        CLASS_CRYPTO,
        CLASS_EQUITY,
        CLASS_ETF,
        CLASS_INDEX,
        CLASS_COMMODITY,
        CLASS_FX,
        CLASS_RATES,
        CLASS_VOL,
    }
)

# The equity complex: equity, etf, and index together, and nothing else.
EQUITY_COMPLEX: Final[frozenset[str]] = frozenset({CLASS_EQUITY, CLASS_ETF, CLASS_INDEX})

# Step 1 is a dex rule, not a ticker rule.
CRYPTO_DEXS: Final[frozenset[str]] = frozenset({"", "hyna"})

# --- the registered exclusion reasons ---------------------------------------
REASON_AMBIGUOUS: Final = "ambiguous_ticker"
REASON_HOUSE_INDEX: Final = "venue_house_index_mixed_complex"
REASON_CRYPTO_ON_BUILDER: Final = "crypto_reference_on_builder_dex"
REASON_NOT_IN_MAPPING: Final = "not_in_registered_mapping"

# --- table 1: equity — one identified issuer, public or private -------------
_EQUITY: Final[tuple[str, ...]] = (
    "AAOI", "AAPL", "AMAT", "AMD", "AMZN", "ANTH", "ANTHROPIC", "ARM", "ASML", "AVGO",
    "BABA", "BB", "BE", "BMNR", "BX", "CAMBRICON", "CAR", "CIEN", "COHR", "COIN",
    "COST", "CRCL", "CRDO", "CRWD", "CRWV", "CXMT", "DELL", "DKNG", "EBAY", "GEV",
    "GIGADEV", "GLW", "GME", "GOOGL", "HIMS", "HOOD", "HYUNDAI", "IBIDEN", "IBM",
    "INNOLIGHT", "INTC", "IONQ", "IREN", "KIOXIA", "LITE", "LLY", "LRCX", "MELI",
    "META", "MINIMAX", "MRNA", "MRVL", "MSFT", "MSTR", "MU", "NAVER", "NBIS", "NET",
    "NFLX", "NOK", "NOW", "NVDA", "OAI", "OPENAI", "ORCL", "PLTR", "QCOM", "RDDT",
    "RIVN", "RKLB", "RTX", "SHEIN", "SKHX", "SKHY", "SMCI", "SMSN", "SNDK", "SOFTBANK",
    "SPACEX", "SPCX", "STRC", "STX", "TENCENT", "TER", "TSLA", "TSM", "UNITREE",
    "USAR", "VST", "WDC", "XIAOMI", "ZHIPU", "ZM",
)  # fmt: skip

# --- table 2: etf — one named exchange-traded fund --------------------------
_ETF: Final[tuple[str, ...]] = (
    "EWJ", "EWT", "EWY", "EWZ", "KORU", "KSTR", "KWEB", "MAGS", "SMH", "SOXL",
    "URNM", "XBI", "XLE",
)  # fmt: skip

# --- table 3: index — a named equity index, or an industry/company basket ---
# The last eight are thematic baskets admitted under the industry-or-company-
# group clause: GLDMINE names gold *miners*, which are companies, not bullion.
_INDEX: Final[tuple[str, ...]] = (
    "IBOV", "JP225", "JPN225", "KR200", "NIFTY", "SMALL2000", "SP500", "US500",
    "USA100", "USA500", "USTECH",
    "BIOTECH", "DEFENSE", "GLDMINE", "INFOTECH", "MAG7", "ROBOT", "SEMI", "SEMIS",
)  # fmt: skip

# --- table 4: commodity — one named physical or industrial commodity --------
# DRAM and H100 are industrial commodity prices, not claims on an issuer —
# the same ground on which the H5 registered mapping admitted them.
_COMMODITY: Final[tuple[str, ...]] = (
    "ALUMINIUM", "BRENTOIL", "COPPER", "CORN", "DRAM", "GAS", "GOLD", "GOLDJM",
    "H100", "NATGAS", "OIL", "PALLADIUM", "PLATINUM", "SILVER", "SILVERJM", "SOY",
    "TTF", "URANIUM", "USOIL", "WHEAT", "WTI",
)  # fmt: skip

# --- table 5: fx — one currency pair or currency index ----------------------
_FX: Final[tuple[str, ...]] = ("DXY", "EUR", "GBP", "JPY", "KRW")

# --- table 6: rates — one government-rate instrument ------------------------
_RATES: Final[tuple[str, ...]] = ("10Y", "2Y", "30Y", "USBOND")

# --- table 7: vol — one volatility index ------------------------------------
# Exactly one member, so no admissible elder can ever exist for a `vol` leg.
# Recorded rather than hidden: a future `vol` birth is excluded_no_class_elder
# until a second volatility instrument lists and ages 180 days.
_VOL: Final[tuple[str, ...]] = ("VIX",)

TICKER_CLASS: Final[dict[str, str]] = {
    **dict.fromkeys(_EQUITY, CLASS_EQUITY),
    **dict.fromkeys(_ETF, CLASS_ETF),
    **dict.fromkeys(_INDEX, CLASS_INDEX),
    **dict.fromkeys(_COMMODITY, CLASS_COMMODITY),
    **dict.fromkeys(_FX, CLASS_FX),
    **dict.fromkeys(_RATES, CLASS_RATES),
    **dict.fromkeys(_VOL, CLASS_VOL),
}

# --- table 8: excluded_unclassifiable, with reasons -------------------------
# A reader will find one or two of the ambiguous entries obvious. A likely
# meaning is a guess, and refusing guesses is what this table is for; the cost
# of each refusal is counted in Amendment H2-5 section 4 rather than absorbed.
UNCLASSIFIABLE: Final[dict[str, str]] = {
    "ANSEM": REASON_AMBIGUOUS,
    "BIRD": REASON_AMBIGUOUS,
    "BOT": REASON_AMBIGUOUS,
    "CBRS": REASON_AMBIGUOUS,
    "CL": REASON_AMBIGUOUS,
    "ENERGY": REASON_AMBIGUOUS,
    "LYTE": REASON_AMBIGUOUS,
    "NCLD": REASON_AMBIGUOUS,
    "NUCLEAR": REASON_AMBIGUOUS,
    "PURRDAT": REASON_AMBIGUOUS,
    "QNT": REASON_AMBIGUOUS,
    "SHAZ": REASON_AMBIGUOUS,
    "USENERGY": REASON_AMBIGUOUS,
    "VOL": REASON_AMBIGUOUS,
    "XYZ100": REASON_HOUSE_INDEX,
    # Crypto-referenced, but on a dex the step-1 rule does not assign to
    # crypto, and the builder-dex class list contains no crypto class.
    "BTC": REASON_CRYPTO_ON_BUILDER,
    "ETH": REASON_CRYPTO_ON_BUILDER,
    "XMR": REASON_CRYPTO_ON_BUILDER,
    "USDE": REASON_CRYPTO_ON_BUILDER,
    "BTCD": REASON_CRYPTO_ON_BUILDER,
    "OTHERS": REASON_CRYPTO_ON_BUILDER,
    "TOTAL2": REASON_CRYPTO_ON_BUILDER,
}


class TaxonomyConflict(RuntimeError):
    """A ticker claims two registered classes, or a class and an exclusion."""


def _check_tables() -> None:
    """The tables partition. A collision is a defect, never a silent winner."""
    seen: dict[str, str] = {}
    for names, label in (
        (_EQUITY, CLASS_EQUITY),
        (_ETF, CLASS_ETF),
        (_INDEX, CLASS_INDEX),
        (_COMMODITY, CLASS_COMMODITY),
        (_FX, CLASS_FX),
        (_RATES, CLASS_RATES),
        (_VOL, CLASS_VOL),
    ):
        for ticker in names:
            if ticker in seen:
                raise TaxonomyConflict(
                    f"{ticker!r} is claimed by both {seen[ticker]!r} and {label!r}; "
                    f"the registered taxonomy must be a partition and nothing picks a winner"
                )
            seen[ticker] = label
    overlap = sorted(set(seen) & set(UNCLASSIFIABLE))
    if overlap:
        raise TaxonomyConflict(
            f"{overlap} are classified and excluded at once; the registered taxonomy "
            f"must be a partition and nothing picks a winner"
        )


_check_tables()


def bare_ticker(coin: str) -> str:
    """The ticker after the dex prefix. `xyz:AAPL` -> `AAPL`; no prefix -> as-is."""
    return coin.split(":", 1)[1] if ":" in coin else coin


def asset_class(coin: str, dex: str) -> str | None:
    """The registered class, or None where the ticker resolves to no class.

    Step 1 is the dex rule; step 2 is the exact-string table. Nothing here
    fuzzy-matches and nothing falls through to a default.
    """
    if dex in CRYPTO_DEXS:
        return CLASS_CRYPTO
    return TICKER_CLASS.get(bare_ticker(coin))


def unclassifiable_reason(coin: str, dex: str) -> str:
    """Why a coin takes no class. Only meaningful where `asset_class` is None."""
    if asset_class(coin, dex) is not None:
        raise ValueError(f"{coin!r} on dex {dex!r} is classified; it has no exclusion reason")
    return UNCLASSIFIABLE.get(bare_ticker(coin), REASON_NOT_IN_MAPPING)


def in_equity_complex(asset_cls: str | None) -> bool:
    """Whether a class is one of equity, etf, index — and nothing else."""
    return asset_cls in EQUITY_COMPLEX


def class_pair(event_class: str, control_class: str) -> str:
    """The stratum label written on every pair row, e.g. `equity->etf`."""
    return f"{event_class}->{control_class}"
