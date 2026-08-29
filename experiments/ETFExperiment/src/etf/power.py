"""A.2 Task 4: exact permutation power by simulation. No number is invented.

Section 9 registers the method: exact permutation power for E1 and E2 at
alpha_adj one-sided, at the registered rank correlation of 0.09, at the
undecayed published 0.18, and at the quartered 0.045, computed from the
measured admissible-day count.

Zero dependencies, deliberately: the arithmetic is a rank correlation, a
shuffle, and a mean, and pulling in a numerical stack to do that would put a
version-dependent RNG between the registration and the verdict.

**Nothing here reads an outcome.** The returns it handles are simulated draws
whose only empirical inputs are the pre-period volatility and funding of the
Section 9 carve-out, strictly before 2025-05-01.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from etf.config import CONFIG


def spearman_from_ranks(perm: list[int]) -> float:
    """Spearman's rho between 0..n-1 and a permutation of it. No ties by construction."""
    n = len(perm)
    if n < 3:
        raise ValueError("a rank correlation on fewer than 3 points is an absence, not a number")
    d2 = sum((i - p) * (i - p) for i, p in enumerate(perm))
    return 1.0 - (6.0 * d2) / (n * (n * n - 1))


def spearman(x: list[float], y: list[float]) -> float:
    """Spearman's rho of two continuous samples, via ranks."""
    if len(x) != len(y):
        raise ValueError("spearman needs paired samples of equal length")
    order_x = sorted(range(len(x)), key=lambda i: x[i])
    order_y = sorted(range(len(y)), key=lambda i: y[i])
    rank_y = [0] * len(y)
    for rank, idx in enumerate(order_y):
        rank_y[idx] = rank
    return spearman_from_ranks([rank_y[i] for i in order_x])


def pearson_for_spearman(rho_s: float) -> float:
    """The Gaussian-copula Pearson correlation giving a target Spearman rho.

    rho_s = (6/pi) arcsin(rho_p / 2), inverted. Exact for a bivariate normal,
    which is the generating model the power simulation registers.
    """
    if not -1.0 <= rho_s <= 1.0:
        raise ValueError(f"a rank correlation must lie in [-1, 1], got {rho_s}")
    return 2.0 * math.sin(math.pi * rho_s / 6.0)


def _bivariate(n: int, rho_p: float, rng: random.Random) -> tuple[list[float], list[float]]:
    xs: list[float] = []
    ys: list[float] = []
    root = math.sqrt(max(0.0, 1.0 - rho_p * rho_p))
    for _ in range(n):
        a = rng.gauss(0.0, 1.0)
        b = rng.gauss(0.0, 1.0)
        xs.append(a)
        ys.append(rho_p * a + root * b)
    return xs, ys


def e1_critical_value(n: int, alpha: float, draws: int, rng: random.Random) -> float:
    """The one-sided upper critical value of Spearman's rho under the permutation null.

    Distribution-free: the null distribution depends on n alone, which is why
    the threshold-free rank test was registered as the directional primary.
    """
    perm = list(range(n))
    stats: list[float] = []
    for _ in range(draws):
        rng.shuffle(perm)
        stats.append(spearman_from_ranks(perm))
    stats.sort()
    index = min(len(stats) - 1, math.ceil((1.0 - alpha) * len(stats)) - 1)
    return stats[max(0, index)]


def e1_power(
    n: int,
    rho_true: float,
    *,
    alpha: float = CONFIG.alpha_adj,
    draws: int = CONFIG.permutation_draws,
    simulations: int = CONFIG.power_simulations,
    seed: int = 20260828,
) -> float:
    """Simulated power of the E1 permutation test at a true rank correlation."""
    rng = random.Random(seed)
    critical = e1_critical_value(n, alpha, draws, rng)
    rho_p = pearson_for_spearman(rho_true)
    hits = 0
    for _ in range(simulations):
        xs, ys = _bivariate(n, rho_p, rng)
        if spearman(xs, ys) > critical:
            hits += 1
    return hits / simulations


@dataclass(frozen=True, slots=True)
class EconomicInputs:
    """Pre-period inputs only. Every one is stamped strictly before 2025-05-01."""

    daily_sd: float
    daily_funding_sum: float
    round_trip_cost: float
    trade_share: float
    n_volatility_returns: int
    n_funding_hours: int


def e2_power(
    n: int,
    rho_true: float,
    inputs: EconomicInputs,
    *,
    alpha: float = CONFIG.alpha_adj,
    draws: int = 2_000,
    simulations: int = 400,
    seed: int = 20260828,
) -> float:
    """Simulated power of the E2 permutation test on mean net return per trade.

    Net for a day is `p * (r - F) - cost * |p|`, with `p` in {-1, 0, +1} from the
    Section 4 rule and `F` the funding sum over the hold — a positive funding
    rate pays the short, so a long pays `F` and a short receives it, which is
    the `-p * F` term.

    The permutation shuffles the position vector against the realised returns.
    `|p|` is preserved by a shuffle, so the cost term is constant under the null
    and the test is on the mean of `p * (r - F)`.
    """
    rng = random.Random(seed)
    rho_p = pearson_for_spearman(rho_true)
    # The Section 4 threshold, expressed as the standard-normal quantile that
    # reproduces the MEASURED share of days outside the +/-100M band.
    cut = _two_sided_cut(inputs.trade_share)
    hits = 0
    for _ in range(simulations):
        signals, shocks = _bivariate(n, rho_p, rng)
        returns = [s * inputs.daily_sd for s in shocks]
        positions = [(1 if s > cut else (-1 if s < -cut else 0)) for s in signals]
        traded = sum(1 for p in positions if p)
        if traded == 0:
            continue
        edge = [p * (r - inputs.daily_funding_sum) for p, r in zip(positions, returns, strict=True)]
        observed = sum(edge) / traded - inputs.round_trip_cost
        shuffled = list(positions)
        exceed = 0
        for _ in range(draws):
            rng.shuffle(shuffled)
            perm_edge = sum(
                p * (r - inputs.daily_funding_sum) for p, r in zip(shuffled, returns, strict=True)
            )
            if perm_edge / traded - inputs.round_trip_cost >= observed:
                exceed += 1
        if (exceed + 1) / (draws + 1) <= alpha:
            hits += 1
    return hits / simulations


def _two_sided_cut(trade_share: float) -> float:
    """The |z| cut reproducing a measured two-sided trade share on a standard normal."""
    if not 0.0 < trade_share <= 1.0:
        raise ValueError(f"the measured trade share must lie in (0, 1], got {trade_share}")
    # P(|Z| > c) = trade_share  =>  c = Phi^-1(1 - trade_share/2)
    return _inverse_normal_cdf(1.0 - trade_share / 2.0)


def _inverse_normal_cdf(p: float) -> float:
    """Acklam's inverse normal CDF. Accurate to ~1.15e-9, stdlib only."""
    if not 0.0 < p < 1.0:
        raise ValueError(f"the inverse normal CDF needs p in (0, 1), got {p}")
    a = (
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    )
    b = (
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    )
    c = (
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    )
    d = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00, 3.754408661907416e00)
    low, high = 0.02425, 1 - 0.02425
    if p < low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
        )
    if p > high:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
        )
    q = p - 0.5
    r = q * q
    return (
        (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5])
        * q
        / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    )


def minimum_n(
    rho_true: float,
    target: float,
    *,
    lo: int = 20,
    hi: int = 4000,
    alpha: float = CONFIG.alpha_adj,
    draws: int = 4_000,
    simulations: int = 600,
    seed: int = 20260828,
) -> int | None:
    """The smallest n whose E1 power reaches the target. None when hi does not."""
    if (
        e1_power(hi, rho_true, alpha=alpha, draws=draws, simulations=simulations, seed=seed)
        < target
    ):
        return None
    low, high = lo, hi
    while low < high:
        mid = (low + high) // 2
        power = e1_power(
            mid, rho_true, alpha=alpha, draws=draws, simulations=simulations, seed=seed
        )
        if power >= target:
            high = mid
        else:
            low = mid + 1
    return low
