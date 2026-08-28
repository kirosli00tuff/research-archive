"""The verdict boundary. A studentized asymptotic confidence sequence.

Section 11 of the registration. The sequence is time-uniform, so peeking
at any day inflates nothing. That property is the whole reason for the
construction: the operator may look daily for years without spending
alpha.

The radius follows the asymptotic confidence sequence form

    radius(t) = sigma_t * sqrt( 2(t rho^2 + 1) / (t^2 rho^2)
                                * ln( sqrt(t rho^2 + 1) / alpha ) )

with sigma_t the running sample standard deviation of daily shadow excess
return. The tuning parameter rho is set by numerical minimization of the
radius at the registered crossing target, 1,600 trading days, and is
frozen at registration. Stage B.1 consumes these functions unchanged.
"""
from __future__ import annotations

import math
from enum import Enum

from hfexperiment.registered import THRESHOLDS, RegisteredThresholds


def acs_radius(t: int, sigma: float, rho: float, alpha: float) -> float:
    """The one-sided confidence sequence radius after t daily observations."""
    if t <= 0 or sigma <= 0 or rho <= 0 or not 0 < alpha < 1:
        raise ValueError("t, sigma, rho positive and alpha in (0, 1)")
    trho2 = t * rho * rho
    return sigma * math.sqrt(
        2.0 * (trho2 + 1.0) / (t * trho2)
        * math.log(math.sqrt(trho2 + 1.0) / alpha)
    )


def tuned_rho(
    t_star: int | None = None, alpha: float | None = None
) -> float:
    """The rho minimizing the radius at the registered crossing target.

    Golden-section search on log10(rho). Deterministic, no closed form
    trusted from memory. tests/test_verdict.py pins the minimizing
    property against a grid.
    """
    t = t_star if t_star is not None else THRESHOLDS.crossing_target_days
    a = alpha if alpha is not None else THRESHOLDS.alpha_one_sided

    def radius_at(log_rho: float) -> float:
        return acs_radius(t, 1.0, math.pow(10.0, log_rho), a)

    lo, hi = -4.0, 0.0
    invphi = (math.sqrt(5.0) - 1.0) / 2.0
    x1 = hi - invphi * (hi - lo)
    x2 = lo + invphi * (hi - lo)
    f1, f2 = radius_at(x1), radius_at(x2)
    for _ in range(200):
        if f1 < f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - invphi * (hi - lo)
            f1 = radius_at(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + invphi * (hi - lo)
            f2 = radius_at(x2)
    return math.pow(10.0, (lo + hi) / 2.0)


def confidence_bounds(
    mean_bp: float, sigma_bp: float, t: int, rho: float,
    alpha: float | None = None,
) -> tuple[float, float]:
    """(lower, upper) for the daily excess mean after t observations.

    Each side holds at level alpha one-sided, which is how both the
    success rule (lower bound) and the futility rule (upper bound) read
    it.
    """
    a = alpha if alpha is not None else THRESHOLDS.alpha_one_sided
    r = acs_radius(t, sigma_bp, rho, a)
    return mean_bp - r, mean_bp + r


class VerdictState(Enum):
    """What the monitor may declare on any day."""

    SUCCESS = "success"
    FUTILITY = "futility"
    CONTINUE = "continue"


def classify_verdict(
    lower_bp: float, upper_bp: float,
    thresholds: RegisteredThresholds = THRESHOLDS,
) -> VerdictState:
    """Success clears the cost hurdle. Futility falls below 10 bp per day."""
    if lower_bp > thresholds.cost_hurdle_bp_per_day:
        return VerdictState.SUCCESS
    if upper_bp < thresholds.futility_bp_per_day:
        return VerdictState.FUTILITY
    return VerdictState.CONTINUE


def alpha_for_width(
    width: int, thresholds: RegisteredThresholds = THRESHOLDS
) -> float:
    """The registered one-sided level for a width. Unregistered widths raise.

    The primary spends alpha 0.05. The secondaries split 0.05 between
    them, Bonferroni, so the family never spends more than the primary.
    """
    if width == thresholds.primary_width:
        return thresholds.alpha_one_sided
    if width in thresholds.secondary_widths:
        return thresholds.secondary_alpha_one_sided
    raise ValueError(f"width {width} is not registered for any verdict")


def first_crossing_day(
    mean_bp: float, sigma_bp: float, rho: float, hurdle_bp: float,
    alpha: float | None = None, max_days: int = 20_000,
) -> int | None:
    """The first day the lower bound clears a hurdle if the mean holds.

    Planning arithmetic only. It assumes the sample mean sits at mean_bp
    forever, which no sample does. The registration reports it as the
    honest expectation, not as a promise.
    """
    a = alpha if alpha is not None else THRESHOLDS.alpha_one_sided
    for t in range(1, max_days + 1):
        if mean_bp - acs_radius(t, sigma_bp, rho, a) > hurdle_bp:
            return t
    return None
