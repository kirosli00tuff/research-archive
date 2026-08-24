"""The A.2 cost model. Three billing regimes, commission and spread apart.

The three regimes are whole-share Tiered, whole-share Fixed, and
fractional. They never blend. A mixed integer-plus-fraction order's regime
is a DEFERRED parameter until a paper fill measures it, and this module
refuses to guess: callers name a regime or they get no number.

COMMISSION IS NOT A MEASUREMENT CONTAMINANT. It is deterministic, known
before submission, and subtracts exactly, so it is a P&L drag and nothing
more. The measured quantity of the live series is fill price against
arrival mid, and commission never enters it. The wrong version of this
statement would argue a later session into larger positions for no
measurement benefit: position size buys commission relief, not measurement
accuracy, and the verdict never reads live P&L.

The spread term is the price of immediacy and IS part of what the live
series measures. It comes from measured quoted spreads on the real book
(scripts/measure_book_spreads.py, Alpaca historical consolidated tape)
where measured, and from the inherited band's UPPER bound where not,
because the book's names sit at the wide end of that band and a band
middle would flatter them.

Tick-multiple fallback ported from AiTrader backtest/fees.py and its
config fees block, read 2026-08-23, copied in rather than imported. Tiers
3 and 4 were measured 2026-07-29 from historical consolidated SIP quotes.
The other tiers are unmeasured 1.0 floors, stated rather than guessed.
The Amihud impact term is not ported: at 45 to 180 USD order size it is
below 0.1 bp and carrying it would imply a precision this model lacks.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from hfexperiment.commission import (
    FIXED,
    TIERED,
    CommissionResult,
    commission,
    fractional_commission,
    sell_leg_regulatory,
)

# Inherited spread band from AiTrader's 2026-07-29 tape measurement, bp of
# mid. The upper bound is the UNMEASURED carry, never the middle.
INHERITED_BAND_BP = (15.8, 50.0)
UNMEASURED_SPREAD_BP = INHERITED_BAND_BP[1]

# Ported per-tier tick multiples. Index 0 is tier 1. Source: AiTrader
# config fees block, tiers 3 and 4 measured 2026-07-29, others 1.0 floors.
SPREAD_TICK_USD = 0.01
TIER_ADV_FLOORS_USD = (277e6, 65.3e6, 13.3e6, 2.07e6, 235e3)
TIER_SPREAD_TICK_MULTIPLES = (1.0, 1.0, 8.0, 9.0, 1.0, 1.0)


class Regime(Enum):
    """One billing regime. Orders bill under exactly one."""

    WHOLE_TIERED = "whole_tiered"
    WHOLE_FIXED = "whole_fixed"
    FRACTIONAL = "fractional"


def regime_commission(
    regime: Regime, shares: float, trade_value_usd: float
) -> CommissionResult:
    """Commission for one order under exactly one regime, never a blend.

    The fractional regime is flat at the greater of 1 percent of value or
    one cent, with no cap relief at any notional. Collapsing it into the
    Tiered branch must fail tests/test_costmodel.py.
    """
    if regime is Regime.WHOLE_TIERED:
        return commission(TIERED, shares, trade_value_usd)
    if regime is Regime.WHOLE_FIXED:
        return commission(FIXED, shares, trade_value_usd)
    amount = fractional_commission(trade_value_usd)
    return CommissionResult(amount_usd=amount, binding="fractional_1pct")


def liquidity_tier(adv_usd: float) -> int:
    """1..6 by median daily dollar volume, 6 thinnest. Ported."""
    for tier, floor in enumerate(TIER_ADV_FLOORS_USD, start=1):
        if adv_usd >= floor:
            return tier
    return 6


def tick_multiple_spread_bp(price_usd: float, adv_usd: float) -> float:
    """Full quoted spread in bp from the ported tick-multiple model.

    Fallback only. A measured per-name spread beats it wherever one
    exists, and an unknown name carries UNMEASURED_SPREAD_BP instead.
    """
    if price_usd <= 0 or adv_usd <= 0:
        return UNMEASURED_SPREAD_BP
    multiple = TIER_SPREAD_TICK_MULTIPLES[liquidity_tier(adv_usd) - 1]
    return SPREAD_TICK_USD * multiple / price_usd * 1e4


@dataclass(frozen=True)
class RoundTrip:
    """One round trip with every term apart. Nothing pre-summed hides."""

    regime: Regime
    notional_usd: float
    commission_per_side_usd: float
    commission_binding: str
    regulatory_sell_usd: float
    spread_bp: float
    spread_measured: bool

    @property
    def commission_rt_usd(self) -> float:
        return 2.0 * self.commission_per_side_usd

    @property
    def commission_rt_bp(self) -> float:
        return self.commission_rt_usd / self.notional_usd * 1e4

    @property
    def regulatory_bp(self) -> float:
        return self.regulatory_sell_usd / self.notional_usd * 1e4

    @property
    def spread_rt_bp(self) -> float:
        """Half the quoted spread paid each side, one full spread total."""
        return self.spread_bp

    @property
    def total_rt_bp(self) -> float:
        return self.commission_rt_bp + self.regulatory_bp + self.spread_rt_bp


def round_trip(
    regime: Regime,
    notional_usd: float,
    share_price_usd: float,
    spread_bp: float | None,
) -> RoundTrip:
    """One name bought and later sold at one notional under one regime.

    spread_bp None means unmeasured, and the inherited band's upper bound
    is carried, flagged as such.
    """
    if notional_usd <= 0 or share_price_usd <= 0:
        raise ValueError("notional and share price must be positive")
    shares = notional_usd / share_price_usd
    c = regime_commission(regime, shares, notional_usd)
    reg = sell_leg_regulatory(shares, notional_usd)
    measured = spread_bp is not None
    return RoundTrip(
        regime=regime,
        notional_usd=notional_usd,
        commission_per_side_usd=c.amount_usd,
        commission_binding=c.binding,
        regulatory_sell_usd=reg.total_usd,
        spread_bp=spread_bp if spread_bp is not None else UNMEASURED_SPREAD_BP,
        spread_measured=measured,
    )


@dataclass(frozen=True)
class AnnualDrag:
    """Commission and regulatory drag for one year at a measured fill rate."""

    regime: Regime
    width: int
    fills_per_month: float
    commission_usd: float
    regulatory_usd: float

    @property
    def total_usd(self) -> float:
        return self.commission_usd + self.regulatory_usd


def annual_commission_drag(
    regime: Regime,
    width: int,
    churn_names_per_month: float,
    deployed_usd: float,
    share_price_usd: float,
) -> AnnualDrag:
    """Yearly deterministic drag at the measured churn.

    One churned name is two fills, a sell and a buy, each at the width's
    per-name notional. Regulatory fees ride the sell leg only. The spread
    term is excluded on purpose: it belongs to the measurement, not to the
    deterministic drag this figure exists to project.
    """
    if width <= 0 or churn_names_per_month < 0:
        raise ValueError("width must be positive, churn non-negative")
    notional = deployed_usd / width
    shares = notional / share_price_usd
    per_fill = regime_commission(regime, shares, notional).amount_usd
    fills_per_month = 2.0 * churn_names_per_month
    sells_per_year = churn_names_per_month * 12.0
    reg = sell_leg_regulatory(shares, notional).total_usd
    return AnnualDrag(
        regime=regime,
        width=width,
        fills_per_month=fills_per_month,
        commission_usd=fills_per_month * 12.0 * per_fill,
        regulatory_usd=sells_per_year * reg,
    )


def daily_cost_hurdle_bp(
    width: int,
    churn_names_per_month: float,
    round_trip_bp: float,
    trading_days_per_month: float = 21.0,
) -> float:
    """The shadow-series success hurdle in bp per day at one width.

    A month round-trips churn/width of the book at round_trip_bp each, and
    the monthly drag spreads over the month's trading days.
    """
    if width <= 0 or trading_days_per_month <= 0:
        raise ValueError("width and trading days must be positive")
    monthly_bp = churn_names_per_month / width * round_trip_bp
    return monthly_bp / trading_days_per_month
