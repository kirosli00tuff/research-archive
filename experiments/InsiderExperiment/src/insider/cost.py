"""The operator's measured cost band, and what it does to a monthly gross edge.

P26 is the standing reference point. 19,648 trades at minus 1.97 bp per trade,
exactly the fee, gross edge precisely zero. A cost model that is not applied to
the gross number produces exactly that outcome one layer up.
"""

from __future__ import annotations

from dataclasses import dataclass

from insider.config import CONFIG, Config


@dataclass(frozen=True, slots=True)
class CostDrag:
    """Round-trip cost expressed as a monthly drag over one holding period."""

    hold_sessions: int
    hold_months: float
    optimistic_bp_per_month: float
    pessimistic_bp_per_month: float


def hold_months(hold_sessions: int, cfg: Config = CONFIG) -> float:
    """A hold in trading months at the registered sessions-per-month constant."""
    return hold_sessions / cfg.sessions_per_month


def monthly_cost_drag(hold_sessions: int, cfg: Config = CONFIG) -> CostDrag:
    """Amortize one round trip across the holding period.

    A position pays the round trip once, so a longer hold spreads the same
    charge over more months. That is the entire cost argument for six months
    and it is stated here rather than asserted in prose.
    """
    months = hold_months(hold_sessions, cfg)
    if months <= 0:
        raise ValueError("hold must be positive")
    return CostDrag(
        hold_sessions=hold_sessions,
        hold_months=months,
        optimistic_bp_per_month=cfg.round_trip_bp_low / months,
        pessimistic_bp_per_month=cfg.round_trip_bp_high / months,
    )


def net_band_bp_per_month(hold_sessions: int, cfg: Config = CONFIG) -> tuple[float, float]:
    """The decayed gross band after the round trip, at one hold.

    Low end pairs the weakest gross with the heaviest cost. High end pairs the
    strongest gross with the lightest. The pessimistic 100 bp round trip is the
    primary bar, so the low end is the number a verdict is read against.
    """
    drag = monthly_cost_drag(hold_sessions, cfg)
    gross_low, gross_high = cfg.decayed_gross_band_bp
    return (gross_low - drag.pessimistic_bp_per_month, gross_high - drag.optimistic_bp_per_month)


def spread_band_bp(cfg: Config = CONFIG) -> tuple[float, float]:
    """The measured one-way spread band. Two crossings make the round trip."""
    return (cfg.spread_bp_low, cfg.spread_bp_high)
