"""A.3 Task 5: the verdict machinery, built dark.

Computes E1, E2 and every named secondary of Section 8. **It is never pointed at
real sealed data in Stage A**: `refuse_sealed_path` raises on any path under the
sealed stores, and `tests/test_verdict.py` pins that refusal and pins the module
against a synthetic fixture set with known answers, including a planted-signal
fixture the canary must fire on.

Stage B calls this exactly once, behind a latch written first.

A statistic not named in Section 8 is a second look and does not exist here.
"""

from __future__ import annotations

import random
import statistics
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from etf.config import CONFIG
from etf.power import spearman
from etf.signal import Position, position

BP = 1e-4


class SealedDataRefused(RuntimeError):
    """The dark verdict machinery was pointed at a real sealed store."""


SEALED_MARKERS: tuple[str, ...] = ("data/outcomes", "data/funding", "data/retro", "data/census")


def refuse_sealed_path(path: str) -> str:
    """Refuse any path inside a sealed store. The Stage A pin, enforced in code."""
    normalised = path.replace("\\", "/")
    for marker in SEALED_MARKERS:
        if marker in normalised:
            raise SealedDataRefused(
                f"refusing to read {path!r}: it lies under the sealed store {marker!r}. "
                "verdict.py runs against synthetic fixtures until the registered Stage B read."
            )
    return path


@dataclass(frozen=True, slots=True)
class Day:
    """One admissible day. `funding_sum` is the signed hourly sum over the hold."""

    trade_date: date
    signal_usd: float
    forward_return: float
    funding_sum: float
    revised: bool
    same_day_return: float | None = None


@dataclass(frozen=True, slots=True)
class E1Result:
    n: int
    rho: float
    p_value: float
    passes: bool


@dataclass(frozen=True, slots=True)
class E2Result:
    n_days: int
    n_trades: int
    mean_net: float
    p_value: float
    passes: bool
    cost_bp: float


def net_return(day: Day, pos: Position, cost_bp: float) -> float:
    """Section 5. A positive funding rate pays the short, so a long pays `F`."""
    if pos is Position.FLAT:
        return 0.0
    return pos * (day.forward_return - day.funding_sum) - cost_bp * BP


def run_e1(
    days: Sequence[Day], *, alpha: float = CONFIG.alpha_adj, draws: int | None = None, seed: int = 1
) -> E1Result:
    """Exact permutation test on the rank correlation, one-sided positive, no threshold."""
    if len(days) < 3:
        raise ValueError("E1 on fewer than 3 admissible days is an absence, not a result")
    signals = [d.signal_usd for d in days]
    returns = [d.forward_return for d in days]
    observed = spearman(signals, returns)
    rng = random.Random(seed)
    shuffled = list(returns)
    n_draws = draws if draws is not None else CONFIG.permutation_draws
    exceed = 0
    for _ in range(n_draws):
        rng.shuffle(shuffled)
        if spearman(signals, shuffled) >= observed:
            exceed += 1
    p = (exceed + 1) / (n_draws + 1)
    return E1Result(n=len(days), rho=observed, p_value=p, passes=p <= alpha)


def run_e2(
    days: Sequence[Day],
    *,
    cost_bp: float | None = None,
    threshold_usd: float = CONFIG.signal_threshold_usd,
    alpha: float = CONFIG.alpha_adj,
    draws: int | None = None,
    seed: int = 1,
) -> E2Result:
    """Mean net return per trade, exact one-sided permutation test above zero."""
    cost = cost_bp if cost_bp is not None else CONFIG.hyperliquid_round_trip_bp[1]
    positions = [position(d.signal_usd, threshold_usd) for d in days]
    traded = sum(1 for p in positions if p is not Position.FLAT)
    if traded == 0:
        raise ValueError("E2 with zero trades is an absence, not a mean of zero")
    edges = [
        p * (d.forward_return - d.funding_sum)
        for p, d in zip(positions, days, strict=True)
        if p is not Position.FLAT
    ]
    observed = statistics.fmean(edges) - cost * BP
    rng = random.Random(seed)
    shuffled = list(positions)
    n_draws = draws if draws is not None else CONFIG.permutation_draws
    exceed = 0
    for _ in range(n_draws):
        rng.shuffle(shuffled)
        perm = [
            p * (d.forward_return - d.funding_sum)
            for p, d in zip(shuffled, days, strict=True)
            if p is not Position.FLAT
        ]
        if perm and statistics.fmean(perm) - cost * BP >= observed:
            exceed += 1
    p = (exceed + 1) / (n_draws + 1)
    return E2Result(
        n_days=len(days),
        n_trades=traded,
        mean_net=observed,
        p_value=p,
        passes=p <= alpha,
        cost_bp=cost,
    )


@dataclass(frozen=True, slots=True)
class Secondaries:
    """Descriptive, never verdict-bearing. Nothing outside Section 8's list."""

    same_day_rho: float | None
    same_day_n: int
    threshold_grid: dict[float, dict[str, float]]
    sidak_alpha: float
    halves: dict[str, dict[str, float]]
    long_only_mean_net: float | None
    long_only_n: int
    revised_mean_net: float | None
    revised_n: int
    unrevised_mean_net: float | None
    unrevised_n: int
    cost_band: dict[float, float]


def run_secondaries(days: Sequence[Day], *, seed: int = 1, draws: int = 2000) -> Secondaries:
    """Every named secondary of Section 8, and nothing else."""
    same_day = [(d.signal_usd, d.same_day_return) for d in days if d.same_day_return is not None]
    same_day_rho = (
        spearman([s for s, _ in same_day], [r for _, r in same_day if r is not None])
        if len(same_day) >= 3
        else None
    )

    grid_size = len(CONFIG.threshold_grid_usd)
    sidak = 1.0 - (1.0 - CONFIG.alpha_adj) ** (1.0 / grid_size)
    grid: dict[float, dict[str, float]] = {}
    for t in CONFIG.threshold_grid_usd:
        try:
            result = run_e2(days, threshold_usd=t, alpha=sidak, draws=draws, seed=seed)
        except ValueError:
            continue
        grid[t] = {
            "mean_net": result.mean_net,
            "p_value": result.p_value,
            "n_trades": float(result.n_trades),
        }

    ordered = sorted(days, key=lambda d: d.trade_date)
    cut = len(ordered) // 2
    halves: dict[str, dict[str, float]] = {}
    for label, chunk in (("first_half", ordered[:cut]), ("second_half", ordered[cut:])):
        if len(chunk) >= 3:
            e1 = run_e1(chunk, draws=draws, seed=seed)
            halves[label] = {"n": float(e1.n), "rho": e1.rho, "p_value": e1.p_value}

    longs = [
        net_return(d, Position.LONG, CONFIG.hyperliquid_round_trip_bp[1])
        for d in days
        if position(d.signal_usd) is Position.LONG
    ]
    revised = [
        net_return(d, position(d.signal_usd), CONFIG.hyperliquid_round_trip_bp[1])
        for d in days
        if d.revised and position(d.signal_usd) is not Position.FLAT
    ]
    unrevised = [
        net_return(d, position(d.signal_usd), CONFIG.hyperliquid_round_trip_bp[1])
        for d in days
        if not d.revised and position(d.signal_usd) is not Position.FLAT
    ]

    band: dict[float, float] = {}
    for cost in CONFIG.hyperliquid_round_trip_bp:
        try:
            band[cost] = run_e2(days, cost_bp=cost, draws=draws, seed=seed).mean_net
        except ValueError:
            continue

    return Secondaries(
        same_day_rho=same_day_rho,
        same_day_n=len(same_day),
        threshold_grid=grid,
        sidak_alpha=sidak,
        halves=halves,
        long_only_mean_net=statistics.fmean(longs) if longs else None,
        long_only_n=len(longs),
        revised_mean_net=statistics.fmean(revised) if revised else None,
        revised_n=len(revised),
        unrevised_mean_net=statistics.fmean(unrevised) if unrevised else None,
        unrevised_n=len(unrevised),
        cost_band=band,
    )


def reversal_profile(
    returns_by_horizon: dict[int, Sequence[float]], positions: Sequence[Position]
) -> dict[int, float]:
    """The 1-to-20-day reversal profile, a named secondary. Descriptive only."""
    out: dict[int, float] = {}
    for horizon in range(1, CONFIG.reversal_horizon_max_days + 1):
        series = returns_by_horizon.get(horizon)
        if series is None or len(series) != len(positions):
            continue
        signed = [p * r for p, r in zip(positions, series, strict=True) if p is not Position.FLAT]
        if signed:
            out[horizon] = statistics.fmean(signed)
    return out
