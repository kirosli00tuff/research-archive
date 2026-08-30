"""The sealed reader — the one module permitted to name a blind field.

Everything here operates on implied volatility, realized volatility and the
premium. Guard 5 exempts this module by name (``vrp/fields.py``,
``vrp/seal.py``, ``vrp/sealed_read.py``) and pins every other module in
``src/vrp`` against naming any of them.

Nothing in this module knows whether its input is a fixture or real data. That
is the point: the machinery is built and verified against synthetic fixtures
with known answers, and the latch decides — once — what it is pointed at.

Estimators are exactly those registered in Section 2 and are not parameterised
away from the registration:

* implied leg — the exchange-published 30-day model-free index, taken as given
* realized leg — close-to-close, ``ddof=1``, annualised by ``sqrt(365)``,
  over the 30 days **following** each implied observation
* sign — ``VRP_t = IV_t - RV_{t->t+30}``, positive meaning the option market
  charged more than the underlying delivered
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import final

from vrp.absence import AbsenceReason, Absent, Maybe

TRADING_DAYS_PER_YEAR = 365.0
"""Crypto trades every calendar day. Registered in Section 2.3, not 252."""

TENOR_DAYS = 30
"""Registered in Section 2.1. One tenor, both assets, no sweep."""

MIN_OBSERVATIONS = 60
"""Registered in Section 2.5. Below this, Absent(insufficient_sample)."""

SQRT_TWO_OVER_PI = math.sqrt(2.0 / math.pi)
"""0.797885. The ATM straddle price coefficient of Section 2.6."""


def bps_per_volatility_point(tenor_days: int = TENOR_DAYS) -> float:
    """Section 2.6, registered before any number existed.

    ``edge_bps = sqrt(2/pi) * sqrt(T) * (IV - RV) * 10_000`` per unit of
    decimal volatility. At the registered 30-day tenor this is 2287.5 bps per
    unit, i.e. **22.875 bps per volatility point**.
    """
    tenor_years = tenor_days / TRADING_DAYS_PER_YEAR
    return SQRT_TWO_OVER_PI * math.sqrt(tenor_years) * 10_000.0


def realized_volatility(closes: list[float]) -> Maybe[float]:
    """Close-to-close annualised realized volatility, ``ddof=1``, x sqrt(365).

    ``closes`` must be the closes bounding the window, so ``n`` closes give
    ``n - 1`` log returns. Two closes give one return and no dispersion, so the
    estimator refuses rather than returning zero.
    """
    if len(closes) < 3:
        return Absent(
            AbsenceReason.INSUFFICIENT_SAMPLE,
            f"realized volatility needs at least 3 closes, got {len(closes)}",
        )
    if any(c <= 0 for c in closes):
        return Absent(
            AbsenceReason.NOT_SERVED,
            "a non-positive close cannot produce a log return",
        )
    returns = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    return math.sqrt(variance) * math.sqrt(TRADING_DAYS_PER_YEAR)


@final
@dataclass(frozen=True, slots=True)
class PremiumSeries:
    """The paired legs and their difference. Every field carries its own n."""

    implied: list[float]
    realized: list[float]
    premium: list[float]

    @property
    def n(self) -> int:
        return len(self.premium)


def build_premium_series(
    implied: list[float], realized: list[float]
) -> Maybe[PremiumSeries]:
    """``VRP_t = IV_t - RV_{t->t+30}``. Section 2.4's sign, applied once."""
    if len(implied) != len(realized):
        return Absent(
            AbsenceReason.NOT_SERVED,
            f"leg lengths differ: implied {len(implied)}, realized {len(realized)}",
        )
    if len(implied) < MIN_OBSERVATIONS:
        return Absent(
            AbsenceReason.INSUFFICIENT_SAMPLE,
            f"{len(implied)} observations is below the registered floor of "
            f"{MIN_OBSERVATIONS}",
        )
    return PremiumSeries(
        implied=list(implied),
        realized=list(realized),
        premium=[i - r for i, r in zip(implied, realized, strict=True)],
    )


def newey_west_se(values: list[float], bandwidth: int) -> Maybe[float]:
    """Newey-West HAC standard error of the mean. Section 6, bandwidth 30.

    Registered before any data, because the realized leg's overlapping 30-day
    forward windows induce serial correlation *by construction*. An IID
    standard error here is the defect ORBExperiment's audit A3 found in its own
    census intervals, where independence made them 2-17x too narrow.
    """
    n = len(values)
    if n < 3:
        return Absent(
            AbsenceReason.INSUFFICIENT_SAMPLE,
            f"a HAC standard error needs at least 3 observations, got {n}",
        )
    if bandwidth < 0 or bandwidth >= n:
        return Absent(
            AbsenceReason.NOT_SERVED,
            f"bandwidth {bandwidth} is not usable at n = {n}",
        )
    mean = sum(values) / n
    deviations = [v - mean for v in values]

    def autocovariance(lag: int) -> float:
        return sum(deviations[t] * deviations[t - lag] for t in range(lag, n)) / n

    long_run = autocovariance(0)
    for lag in range(1, bandwidth + 1):
        weight = 1.0 - lag / (bandwidth + 1.0)
        long_run += 2.0 * weight * autocovariance(lag)
    if long_run <= 0.0:
        return Absent(
            AbsenceReason.NOT_SERVED,
            f"the HAC long-run variance is non-positive ({long_run:.6g}); the "
            "Bartlett kernel guarantees non-negativity only asymptotically, and "
            "this sample did not deliver it",
        )
    return math.sqrt(long_run / n)


def _log_beta(a: float, b: float) -> float:
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the incomplete beta function (Lentz's method)."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-16:
            break
    return h


def incomplete_beta(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta ``I_x(a, b)``. No third-party dependency."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    front = math.exp(a * math.log(x) + b * math.log(1.0 - x) - _log_beta(a, b))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return (
        1.0
        - math.exp(b * math.log(1.0 - x) + a * math.log(x) - _log_beta(b, a))
        * _betacf(b, a, 1.0 - x)
        / b
    )


def student_t_sf(t: float, degrees_of_freedom: float) -> float:
    """Upper-tail probability ``P(T > t)`` for Student's t. The one-sided p."""
    if degrees_of_freedom <= 0:
        raise ValueError("degrees of freedom must be positive")
    x = degrees_of_freedom / (degrees_of_freedom + t * t)
    tail = 0.5 * incomplete_beta(degrees_of_freedom / 2.0, 0.5, x)
    return tail if t > 0 else 1.0 - tail


def student_t_critical(degrees_of_freedom: float, alpha: float) -> float:
    """One-sided critical value by bisection on the survival function."""
    low, high = 0.0, 100.0
    for _ in range(200):
        mid = (low + high) / 2.0
        if student_t_sf(mid, degrees_of_freedom) > alpha:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


@final
@dataclass(frozen=True, slots=True)
class PremiumResult:
    """The endpoint, with every figure carrying its own n."""

    label: str
    n: int
    mean_vol_points: float
    hac_standard_error: float
    hac_bandwidth: int
    t_statistic: float
    one_sided_p: float
    ci_lower_vol_points: float
    mean_bps: float
    ci_lower_bps: float
    positive_share: float

    def as_row(self) -> dict[str, object]:
        return {
            "label": self.label,
            "n": self.n,
            "mean_vol_points": round(self.mean_vol_points, 6),
            "hac_standard_error": round(self.hac_standard_error, 6),
            "hac_bandwidth": self.hac_bandwidth,
            "t_statistic": round(self.t_statistic, 4),
            "one_sided_p": self.one_sided_p,
            "ci_lower_vol_points": round(self.ci_lower_vol_points, 6),
            "mean_bps": round(self.mean_bps, 4),
            "ci_lower_bps": round(self.ci_lower_bps, 4),
            "positive_share": round(self.positive_share, 6),
        }


def estimate_premium(
    premium: list[float],
    *,
    label: str,
    bandwidth: int = TENOR_DAYS,
    alpha: float = 0.05,
) -> Maybe[PremiumResult]:
    """Section 6's single one-sided test, in volatility points and in bps.

    ``premium`` is in **decimal** volatility (0.05 = five volatility points).
    """
    n = len(premium)
    if n < MIN_OBSERVATIONS:
        return Absent(
            AbsenceReason.INSUFFICIENT_SAMPLE,
            f"{n} observations is below the registered floor of {MIN_OBSERVATIONS}",
        )
    standard_error = newey_west_se(premium, bandwidth)
    if isinstance(standard_error, Absent):
        return standard_error
    mean = sum(premium) / n
    t_statistic = mean / standard_error
    degrees_of_freedom = float(n - 1)
    scale = bps_per_volatility_point()
    critical = student_t_critical(degrees_of_freedom, alpha)
    ci_lower = mean - critical * standard_error
    return PremiumResult(
        label=label,
        n=n,
        mean_vol_points=mean,
        hac_standard_error=standard_error,
        hac_bandwidth=bandwidth,
        t_statistic=t_statistic,
        one_sided_p=student_t_sf(t_statistic, degrees_of_freedom),
        ci_lower_vol_points=ci_lower,
        mean_bps=mean * scale,
        ci_lower_bps=ci_lower * scale,
        positive_share=sum(1 for p in premium if p > 0) / n,
    )


def non_overlapping(premium: list[float], stride: int = TENOR_DAYS) -> list[float]:
    """Section 6's registered robustness: IID by construction, at n/30 cost."""
    return premium[::stride]


# ---------------------------------------------------------------------------
# The registered hedging rule (Section 4.3), which needs a blind field
# ---------------------------------------------------------------------------


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def straddle_delta(
    spot: float, strike: float, sigma: float, tenor_years: float
) -> Maybe[float]:
    """Delta of a long ATM straddle, ``2*N(d1) - 1``, at zero rates.

    Lives in the sealed module because ``d1`` requires ``sigma`` — an implied
    volatility, and therefore a blind field. This is why Section 4.3's rebalance
    **count** could not be computed at TASK 5 while its **price** could.
    """
    if spot <= 0 or strike <= 0 or sigma <= 0 or tenor_years <= 0:
        return Absent(
            AbsenceReason.NOT_SERVED,
            f"straddle delta undefined at spot={spot}, strike={strike}, "
            f"sigma={sigma}, tenor_years={tenor_years}",
        )
    d1 = (math.log(spot / strike) + 0.5 * sigma * sigma * tenor_years) / (
        sigma * math.sqrt(tenor_years)
    )
    return 2.0 * _normal_cdf(d1) - 1.0


@final
@dataclass(frozen=True, slots=True)
class RebalanceCount:
    """How many resizes the registered rule required over one tenor."""

    band: float
    rebalances: int
    days_evaluated: int
    max_abs_drift: float


def count_rebalances(
    closes: list[float],
    strike: float,
    sigma: float,
    band: float = 0.10,
    tenor_days: int = TENOR_DAYS,
) -> Maybe[RebalanceCount]:
    """Section 4.3, applied exactly as registered.

    Delta-hedge a short ATM straddle, resized whenever the **net** position
    delta moves more than ``+/- band`` from flat, evaluated once per calendar
    day over the tenor. A resize returns the net to flat, so the drift is
    measured from the option delta at the last resize, not from inception.
    """
    if len(closes) < 2:
        return Absent(
            AbsenceReason.INSUFFICIENT_SAMPLE,
            f"a rebalance count needs at least 2 closes, got {len(closes)}",
        )
    if sigma <= 0 or strike <= 0 or band <= 0:
        return Absent(
            AbsenceReason.NOT_SERVED,
            f"rebalance count undefined at sigma={sigma}, strike={strike}, band={band}",
        )
    anchor = straddle_delta(
        closes[0], strike, sigma, tenor_days / TRADING_DAYS_PER_YEAR
    )
    if isinstance(anchor, Absent):
        return anchor
    rebalances = 0
    max_drift = 0.0
    evaluated = 0
    for day in range(1, min(len(closes), tenor_days + 1)):
        remaining_days = tenor_days - day
        if remaining_days <= 0:
            break
        current = straddle_delta(
            closes[day],
            strike,
            sigma,
            remaining_days / TRADING_DAYS_PER_YEAR,
        )
        if isinstance(current, Absent):
            continue
        evaluated += 1
        drift = abs(current - anchor)
        max_drift = max(max_drift, drift)
        if drift > band:
            rebalances += 1
            anchor = current
    return RebalanceCount(
        band=band,
        rebalances=rebalances,
        days_evaluated=evaluated,
        max_abs_drift=max_drift,
    )
