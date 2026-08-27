"""Exact binomial power for the three co-primaries. Reads no outcome value.

Every function here is arithmetic over counts and registered probabilities.
Nothing imports a data path, a ledger, or a payload reader; the guard tests
pin that this module stays that way. Log-space pmf keeps n in the thousands
exact enough (absolute tail error well under 1e-12 against an exact-fraction
reference, pinned by test).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, lgamma, log

from npl.config import CONFIG, Config


def _log_pmf(n: int, k: int, p: float) -> float:
    if not 0.0 < p < 1.0:
        raise ValueError(f"p must be inside (0, 1), got {p}")
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) + k * log(p) + (n - k) * log(1.0 - p)


def upper_tail(n: int, k: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n, p), exactly summed in log space."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return min(1.0, sum(exp(_log_pmf(n, i, p)) for i in range(k, n + 1)))


def critical_k(n: int, p0: float, alpha: float) -> int | None:
    """Smallest k with P(X >= k | p0) <= alpha, or None when even k = n misses."""
    if upper_tail(n, n, p0) > alpha:
        return None
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if upper_tail(n, mid, p0) <= alpha:
            hi = mid
        else:
            lo = mid + 1
    return lo


def exact_power(n: int, p0: float, p_true: float, alpha: float) -> float:
    """Power of the one-sided exact test of p0 against greater, at p_true."""
    k_star = critical_k(n, p0, alpha)
    if k_star is None:
        return 0.0
    return upper_tail(n, k_star, p_true)


def min_n_for_power(
    p0: float, p_true: float, alpha: float, target: float, n_max: int = 5000
) -> int | None:
    """Smallest n from which exact power stays at or above target, or None.

    Exact binomial power is not monotone in n (it saw-tooths as the critical
    k steps), so this scans and returns the first n from which power never
    drops below target again within the horizon checked.
    """
    good_from: int | None = None
    for n in range(1, n_max + 1):
        if exact_power(n, p0, p_true, alpha) >= target:
            if good_from is None:
                good_from = n
        else:
            good_from = None
    return good_from


@dataclass(frozen=True, slots=True)
class CoPrimaryPowerReport:
    """The three co-primary powers at one sample-size scenario."""

    scenario: str
    n_events: int
    n_pairs: int
    p1_power: float
    p2_power: float
    p3_power: float


def co_primary_powers(
    scenario: str, n_events: int, n_pairs: int, cfg: Config = CONFIG
) -> CoPrimaryPowerReport:
    """Powers of P1, P2, P3 at the registered assumptions and alpha_adj.

    P1: exact test of p0 = p1_bar against greater, true share p1_true_share.
    P2: exact sign test of p0 = 1/2, true share p2_true_share.
    P3: exact sign test of p0 = 1/2 on n_pairs, true share p3_true_share.
    """
    if n_events < 0 or n_pairs < 0 or n_pairs > n_events:
        raise ValueError(f"impossible counts: n_events={n_events}, n_pairs={n_pairs}")
    return CoPrimaryPowerReport(
        scenario=scenario,
        n_events=n_events,
        n_pairs=n_pairs,
        p1_power=exact_power(n_events, cfg.p1_bar, cfg.p1_true_share, cfg.alpha_adj),
        p2_power=exact_power(n_events, 0.5, cfg.p2_true_share, cfg.alpha_adj),
        p3_power=exact_power(n_pairs, 0.5, cfg.p3_true_share, cfg.alpha_adj),
    )
