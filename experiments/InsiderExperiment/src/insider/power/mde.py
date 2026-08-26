"""The minimum detectable effect, derived from a dispersion and a sample size.

Nothing here takes a realized return. The inputs are a standard deviation, an
effective period count, and the registered critical value, and the output is the
smallest monthly alpha the design could call significant. That number exists
before any alpha is computed, which is the whole reason Stage A.1 exists.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from insider.config import CONFIG, Config
from insider.power.dispersion import DispersionStats


@dataclass(frozen=True, slots=True)
class MdeResult:
    """One minimum detectable effect and the three numbers that produced it.

    tests/test_guards.py asserts this exact field tuple, for the same reason it
    asserts DispersionStats.
    """

    hold_sessions: int
    weighting: str
    n_sessions: int
    effective_periods: float
    sd_daily_excess: float
    annualized_tracking_error: float
    newey_west_lags: int
    variance_inflation: float
    standard_error_monthly_bp: float
    mde_bp_per_month: float


def standard_error_monthly(
    sd_daily: float, effective_periods: float, cfg: Config = CONFIG
) -> float:
    """Standard error of the monthly alpha, in return units.

    A monthly alpha is the daily alpha times the registered sessions per month,
    so its standard error scales the same way.
    """
    if effective_periods <= 0:
        raise ValueError("effective periods must be positive")
    if sd_daily <= 0:
        raise ValueError("a standard deviation must be positive")
    return cfg.sessions_per_month * sd_daily / math.sqrt(effective_periods)


def mde_from(stats: DispersionStats, cfg: Config = CONFIG) -> MdeResult:
    """The smallest monthly alpha the test could call significant at t critical."""
    se = standard_error_monthly(stats.sd_daily_excess, stats.effective_periods, cfg)
    return MdeResult(
        hold_sessions=stats.hold_sessions,
        weighting=stats.weighting,
        n_sessions=stats.n_sessions,
        effective_periods=stats.effective_periods,
        sd_daily_excess=stats.sd_daily_excess,
        annualized_tracking_error=stats.annualized_tracking_error,
        newey_west_lags=stats.newey_west_lags,
        variance_inflation=stats.variance_inflation,
        standard_error_monthly_bp=se * 10_000.0,
        mde_bp_per_month=cfg.t_critical * se * 10_000.0,
    )


def band_position(mde_bp: float, cfg: Config = CONFIG) -> str:
    """Where a minimum detectable effect sits against the decayed gross band."""
    low, high = cfg.decayed_gross_band_bp
    if mde_bp <= low:
        return f"below the decayed gross band {low:g} to {high:g} bp, so the whole band resolves"
    if mde_bp <= high:
        return (
            f"inside the decayed gross band {low:g} to {high:g} bp, so only effects above "
            f"{mde_bp:.2f} bp resolve"
        )
    return (
        f"above the decayed gross band {low:g} to {high:g} bp, so no effect the literature "
        f"reports would resolve"
    )
