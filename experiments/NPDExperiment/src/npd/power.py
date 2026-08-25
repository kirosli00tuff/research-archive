"""Minimum detectable mean rank IC, computed from the derived window.

The predecessor experiment registered its power against a 50 bp effect and
delivered a sample that could not distinguish no effect from no power. This
module produces the number before a cent is spent, and it produces it from the
derived day count rather than an assumed one.

Two quantities are reported and they answer different questions.

registered_floor_mde
    The floor named in the B.3 replay schedule, detectable IC 0.025 at 30
    names. It is a one-sample test of the model's own daily rank IC against
    zero, at the registered critical value, with no overlap adjustment. It
    decides whether a window is worth collecting at all.

contrast_mde
    The number that governs the primary inference. It is the difference of two
    daily rank IC series, so its standard deviation depends on how correlated
    the model and the baseline are, and its effective sample size depends on
    the overlap induced by a multi-session horizon. It is reported across a
    sensitivity grid because neither input is known before collection.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from npd.config import Config


def null_ic_sd(n_names: int) -> float:
    """Standard deviation of a daily Spearman rank IC under the null.

    For n independent ranks the sampling standard deviation of Spearman's rho
    is 1/sqrt(n-1). At the registered panel size of 30 this is 0.1857.
    """
    if n_names < 3:
        raise ValueError("rank IC needs at least three names")
    return 1.0 / math.sqrt(n_names - 1)


def overlap_vif(horizon_sessions: int) -> float:
    """Variance inflation from overlapping forward windows.

    Consecutive start dates share horizon minus one sessions of the same
    forward return, so the daily IC series is positively autocorrelated with
    triangular decay. Taking the overlap fraction as the autocorrelation,
    rho_k = 1 - k/h, the variance of the mean inflates by
    1 + 2 * sum_{k=1}^{h-1} (1 - k/h)^2.

    A one-session horizon overlaps nothing and returns 1.0.
    """
    if horizon_sessions < 1:
        raise ValueError("horizon must be at least one session")
    return 1.0 + 2.0 * sum((1.0 - k / horizon_sessions) ** 2 for k in range(1, horizon_sessions))


def effective_days(n_days: int, horizon_sessions: int) -> float:
    """Independent-equivalent day count after the overlap penalty."""
    return n_days / overlap_vif(horizon_sessions)


def detection_mde(sd: float, n_eff: float, t_critical: float) -> float:
    """Smallest mean the test can call significant. Detection, not power."""
    if n_eff <= 0:
        raise ValueError("effective days must be positive")
    return t_critical * sd / math.sqrt(n_eff)


def powered_mde(sd: float, n_eff: float, t_critical: float, power: float = 0.80) -> float:
    """Smallest mean the test detects with the stated probability.

    Adds the one-sided normal quantile for the target power to the critical
    value. At 80 percent that quantile is 0.8416.
    """
    z_power = {0.80: 0.8416, 0.90: 1.2816, 0.95: 1.6449}.get(power)
    if z_power is None:
        raise ValueError(f"unsupported power target {power}")
    if n_eff <= 0:
        raise ValueError("effective days must be positive")
    return (t_critical + z_power) * sd / math.sqrt(n_eff)


@dataclass(frozen=True, slots=True)
class ContrastPower:
    """One cell of the sensitivity grid."""

    corr_model_baseline: float
    sd_diff: float
    n_eff: float
    detect: float
    powered_80: float


def contrast_grid(
    n_days: int,
    n_names: int,
    horizon_sessions: int,
    t_critical: float,
    correlations: tuple[float, ...] = (0.0, 0.3, 0.5, 0.7),
) -> tuple[ContrastPower, ...]:
    """Minimum detectable contrast across plausible model-baseline correlations.

    The daily contrast is IC_model minus IC_baseline. Both have the null
    standard deviation for the panel size, so the difference has standard
    deviation sqrt(2 * (1 - corr)) times that value. corr is unknown before
    collection, so the whole grid is registered rather than one guessed cell.
    """
    sd_one = null_ic_sd(n_names)
    n_eff = effective_days(n_days, horizon_sessions)
    out = []
    for corr in correlations:
        sd_diff = math.sqrt(2.0 * (1.0 - corr)) * sd_one
        out.append(
            ContrastPower(
                corr_model_baseline=corr,
                sd_diff=sd_diff,
                n_eff=n_eff,
                detect=detection_mde(sd_diff, n_eff, t_critical),
                powered_80=powered_mde(sd_diff, n_eff, t_critical),
            )
        )
    return tuple(out)


def registered_floor_mde(n_days: int, n_names: int, t_critical: float) -> float:
    """The B.3 power floor. One-sample daily IC against zero, no overlap term."""
    return detection_mde(null_ic_sd(n_names), float(n_days), t_critical)


def band_coverage(mde: float, cfg: Config | None = None) -> str:
    """Where a minimum detectable effect sits against the registered band.

    The band is the range of rank IC the literature reports for real
    cross-sectional signals. A design whose smallest detectable effect sits above
    the band can only find something larger than anything anyone has reported,
    which is a fact to register rather than discover.
    """
    from npd.config import CONFIG as _CFG

    conf = cfg or _CFG
    low, high = conf.realistic_effect_band
    if mde <= low:
        return f"covers the whole registered band {low:g} to {high:g}"
    if mde <= high:
        return f"covers the upper part of the registered band {low:g} to {high:g}, from {mde:.4f}"
    return f"sits above the registered band {low:g} to {high:g}. Large effects only."
