"""IBKR Pro commission arithmetic for US equities, both plans.

Figures verified against IBKR's published schedules on 2026-08-23. Sources
and retrieval dates live in docs/ACCESS.md. The rule that matters at this
account size, in IBKR's own words: when the calculated maximum per order is
less than the minimum per order, the maximum is assessed.

Regulatory fees ride the sell leg only: SEC Section 31 on sale proceeds and
FINRA TAF per share with a one cent per-trade minimum.
"""
from __future__ import annotations

from dataclasses import dataclass

# Regulatory rates, verified 2026-08-23. Sources in docs/ACCESS.md.
# SEC Section 31: per dollar of covered sale proceeds. USD 20.60 per million
# effective 2026-04-04.
SEC_SECTION_31_RATE = 0.0000206
# FINRA TAF: per share sold, effective 2026-01-01. Capped at 9.79 per trade,
# far above any order this book sends.
FINRA_TAF_PER_SHARE = 0.000195
FINRA_TAF_MAX_USD = 9.79
# Conservative bound. FINRA's own schedule carries no per-trade minimum and
# IBKR's pages state none for TAF. Billing granularity on a sub-cent fee is
# unmeasured until a real fill, so the model holds the worst case. A stage C
# fill statement replaces this with the observed behaviour.
FINRA_TAF_MIN_USD = 0.01
# IBKR fractional-order schedule, from the .ca commissions page footnote:
# the greater of 1 percent of trade value or USD 0.01, both plans.
FRACTIONAL_PCT_OF_VALUE = 0.01
FRACTIONAL_MIN_USD = 0.01


@dataclass(frozen=True)
class Plan:
    """One IBKR Pro pricing plan."""
    name: str
    per_share_usd: float
    min_per_order_usd: float
    cap_pct_of_value: float


TIERED = Plan(
    name="tiered",
    per_share_usd=0.0035,
    min_per_order_usd=0.35,
    cap_pct_of_value=0.005,
)
FIXED = Plan(
    name="fixed",
    per_share_usd=0.005,
    min_per_order_usd=1.00,
    cap_pct_of_value=0.01,
)


@dataclass(frozen=True)
class CommissionResult:
    """Commission for one order with the branch that produced it."""
    amount_usd: float
    binding: str  # per_share | minimum | cap


def commission(plan: Plan, shares: float, trade_value_usd: float) -> CommissionResult:
    """Commission for one order under one plan.

    The cap-below-minimum branch is the load-bearing one: below the
    crossover notional the cap is less than the minimum and the cap is
    assessed. Removing that branch must fail tests/test_commission.py.
    """
    if shares <= 0 or trade_value_usd <= 0:
        raise ValueError("shares and trade value must be positive")
    calculated = shares * plan.per_share_usd
    cap = trade_value_usd * plan.cap_pct_of_value
    if cap < plan.min_per_order_usd:
        return CommissionResult(amount_usd=cap, binding="cap")
    if calculated < plan.min_per_order_usd:
        return CommissionResult(amount_usd=plan.min_per_order_usd, binding="minimum")
    return CommissionResult(amount_usd=calculated, binding="per_share")


@dataclass(frozen=True)
class SellLegFees:
    """Regulatory drag on the sell leg."""
    sec_usd: float
    taf_usd: float

    @property
    def total_usd(self) -> float:
        return self.sec_usd + self.taf_usd


def sell_leg_regulatory(shares: float, trade_value_usd: float) -> SellLegFees:
    """SEC Section 31 plus FINRA TAF for one sell, worst-case TAF floor."""
    if shares <= 0 or trade_value_usd <= 0:
        raise ValueError("shares and trade value must be positive")
    sec = trade_value_usd * SEC_SECTION_31_RATE
    taf = min(max(shares * FINRA_TAF_PER_SHARE, FINRA_TAF_MIN_USD),
              FINRA_TAF_MAX_USD)
    return SellLegFees(sec_usd=sec, taf_usd=taf)


def fractional_commission(trade_value_usd: float) -> float:
    """Commission for an order with a fractional share quantity.

    IBKR bills these outside the whole-share schedule: the greater of 1
    percent of trade value or one cent, on either plan. Whether a mixed
    integer-plus-fraction order is billed whole on this schedule or split
    is unmeasured until a paper fill. The model holds the worst case.
    """
    if trade_value_usd <= 0:
        raise ValueError("trade value must be positive")
    return max(trade_value_usd * FRACTIONAL_PCT_OF_VALUE, FRACTIONAL_MIN_USD)


def crossover_notional_usd(plan: Plan) -> float:
    """The notional where the cap equals the minimum.

    Below this every order pays the cap. Tiered: 70. Fixed: 100.
    """
    return plan.min_per_order_usd / plan.cap_pct_of_value
