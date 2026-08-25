"""Stage B.2. The only module permitted to read the sealed forward returns.

Nothing else in this repository may name var/npd_sealed.db, query its
forward_return table, or call read_sealed_returns. tests/test_guards.py walks
every source file and fails the moment another module does.

The evaluator refuses to run while Amendment 0 is empty. That refusal is the
mechanism, not a reminder: the operator writes his prior down before he can see
a number.
"""

from __future__ import annotations

import math
import random
import re
import sqlite3
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from npd.baselines import BASELINE_NAMES
from npd.config import CONFIG, Config
from npd.paths import REPO_ROOT, SEALED_DB

AMENDMENT_0_EMPTY_MARKER = "[ EMPTY."
REGISTRATION = REPO_ROOT / "REGISTRATION.md"


class AmendmentZeroMissing(RuntimeError):
    """The operator prior is not recorded. B.2 refuses to run."""


class LeakageDetected(RuntimeError):
    """The negative control did not collapse. Everything stops."""


def amendment_zero_filled(path: Path = REGISTRATION) -> bool:
    """Whether the operator has written his prior into Section 13."""
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    match = re.search(r"## Section 13\.(.*?)(?=\n## Section 14\.)", text, re.S)
    if match is None:
        return False
    return AMENDMENT_0_EMPTY_MARKER not in match.group(1)


def require_amendment_zero(path: Path = REGISTRATION) -> None:
    if not amendment_zero_filled(path):
        raise AmendmentZeroMissing(
            "Amendment 0 is empty. The operator writes his registered prior into "
            "REGISTRATION.md Section 13 before B.2 runs. Refusing."
        )


def read_sealed_returns(horizon: int, path: Path = SEALED_DB) -> dict[tuple[str, str], float]:
    """The sealed forward returns. This function has exactly one caller."""
    if not path.exists():
        raise FileNotFoundError(f"sealed store missing: {path}")
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT date, symbol, ret FROM forward_return WHERE horizon = ? AND ret IS NOT NULL",
            (horizon,),
        ).fetchall()
    finally:
        con.close()
    return {(r[0], r[1]): float(r[2]) for r in rows}


def spearman(ranks_a: Sequence[float], ranks_b: Sequence[float]) -> float:
    """Pearson correlation of two rank vectors."""
    n = len(ranks_a)
    if n != len(ranks_b) or n < 3:
        raise ValueError("need at least three paired ranks")
    ma = sum(ranks_a) / n
    mb = sum(ranks_b) / n
    num = sum((a - ma) * (b - mb) for a, b in zip(ranks_a, ranks_b, strict=True))
    da = math.sqrt(sum((a - ma) ** 2 for a in ranks_a))
    db = math.sqrt(sum((b - mb) ** 2 for b in ranks_b))
    if da <= 0 or db <= 0:
        raise ValueError("a rank vector has zero spread")
    return num / (da * db)


def _ranks_from_order(order: Sequence[str]) -> dict[str, float]:
    return {sym: float(i + 1) for i, sym in enumerate(order)}


def _outcome_ranks(symbols: Sequence[str], returns: dict[str, float]) -> dict[str, float]:
    ordered = sorted(symbols, key=lambda s: (-returns[s], s))
    return _ranks_from_order(ordered)


def daily_ic(order: Sequence[str], returns: dict[str, float]) -> float:
    """Rank IC for one day. Predicted order against realized order.

    Both vectors rank best first, so a positive value means the ranking put the
    winners near the top.
    """
    symbols = [s for s in order if s in returns]
    if len(symbols) < 3:
        raise ValueError("too few symbols with a realized return")
    pred = _ranks_from_order([s for s in order if s in returns])
    real = _outcome_ranks(symbols, returns)
    # Rank 1 is best in both vectors, so a perfect ranking correlates at plus
    # one. No negation. tests/test_evaluator_synthetic.py pins the convention.
    return spearman([pred[s] for s in symbols], [real[s] for s in symbols])


@dataclass(frozen=True, slots=True)
class Interval:
    point: float
    low: float
    high: float

    def excludes_zero(self) -> bool:
        return self.low > 0.0 or self.high < 0.0


@dataclass(slots=True)
class Verdict:
    n_days: int
    model_mean_ic: float
    baseline_mean_ic: dict[str, float] = field(default_factory=dict)
    best_baseline: str = ""
    contrast: Interval | None = None
    permutation_p: float = 1.0
    negative_control_mean_ic: float = 0.0
    beats_coin: bool = False
    beats_best_baseline: bool = False
    outcome: str = ""


def block_bootstrap_interval(
    values: Sequence[float],
    *,
    resamples: int,
    block_length: int,
    t_critical: float,
    seed: int,
) -> Interval:
    """Moving-block bootstrap on a day-ordered series.

    Blocks are used rather than independent days because a multi-session horizon
    makes consecutive days share most of their forward window. The block length
    is registered at twice the primary horizon.
    """
    n = len(values)
    if n < block_length:
        raise ValueError("series shorter than one block")
    rng = random.Random(seed)
    point = sum(values) / n
    n_blocks = math.ceil(n / block_length)
    means: list[float] = []
    for _ in range(resamples):
        drawn: list[float] = []
        for _ in range(n_blocks):
            start = rng.randrange(0, n - block_length + 1)
            drawn.extend(values[start : start + block_length])
        drawn = drawn[:n]
        means.append(sum(drawn) / n)
    means.sort()
    sd = math.sqrt(sum((m - point) ** 2 for m in means) / (len(means) - 1))
    return Interval(point=point, low=point - t_critical * sd, high=point + t_critical * sd)


def within_day_permutation_p(
    orders: dict[str, list[str]],
    returns_by_day: dict[str, dict[str, float]],
    observed: float,
    *,
    resamples: int,
    seed: int,
) -> float:
    """Two-sided p under a null that shuffles each ranking inside its own day."""
    rng = random.Random(seed)
    days = sorted(orders)
    count = 0
    for _ in range(resamples):
        total = 0.0
        for d in days:
            shuffled = list(orders[d])
            rng.shuffle(shuffled)
            total += daily_ic(shuffled, returns_by_day[d])
        if abs(total / len(days)) >= abs(observed):
            count += 1
    return (count + 1) / (resamples + 1)


def evaluate(
    model_orders: dict[str, list[str]],
    baseline_orders: dict[str, dict[str, list[str]]],
    returns_by_day: dict[str, dict[str, float]],
    cfg: Config = CONFIG,
    *,
    seed: int = 20260825,
) -> Verdict:
    """Run the registered inference. Primary contrast, permutation null, control."""
    days = sorted(d for d in model_orders if returns_by_day.get(d))
    if not days:
        raise ValueError("no evaluable days")

    model_ics = [daily_ic(model_orders[d], returns_by_day[d]) for d in days]
    verdict = Verdict(n_days=len(days), model_mean_ic=sum(model_ics) / len(days))

    for name in BASELINE_NAMES:
        orders = baseline_orders.get(name, {})
        ics = [daily_ic(orders[d], returns_by_day[d]) for d in days if d in orders]
        verdict.baseline_mean_ic[name] = sum(ics) / len(ics) if ics else 0.0

    verdict.best_baseline = max(verdict.baseline_mean_ic, key=lambda k: verdict.baseline_mean_ic[k])
    best_orders = baseline_orders[verdict.best_baseline]
    contrast_series = [
        daily_ic(model_orders[d], returns_by_day[d]) - daily_ic(best_orders[d], returns_by_day[d])
        for d in days
    ]

    block = 2 * cfg.primary_horizon_sessions
    verdict.contrast = block_bootstrap_interval(
        contrast_series,
        resamples=cfg.bootstrap_resamples,
        block_length=block,
        t_critical=cfg.t_critical,
        seed=seed,
    )

    coin_interval = block_bootstrap_interval(
        model_ics,
        resamples=cfg.bootstrap_resamples,
        block_length=block,
        t_critical=cfg.t_critical,
        seed=seed + 1,
    )
    verdict.beats_coin = coin_interval.low > 0.0
    verdict.beats_best_baseline = verdict.contrast.low > 0.0

    verdict.permutation_p = within_day_permutation_p(
        {d: model_orders[d] for d in days},
        returns_by_day,
        verdict.model_mean_ic,
        resamples=min(cfg.permutation_resamples, 1000),
        seed=seed + 2,
    )

    control_rng = random.Random(seed + 3)
    control_ics = []
    for d in days:
        shuffled = list(model_orders[d])
        control_rng.shuffle(shuffled)
        control_ics.append(daily_ic(shuffled, returns_by_day[d]))
    verdict.negative_control_mean_ic = sum(control_ics) / len(control_ics)

    if verdict.beats_coin and verdict.beats_best_baseline:
        verdict.outcome = "conditional phase C.1 authorized, labelled a large-effect screen"
    elif verdict.beats_coin:
        verdict.outcome = "an expensive wrapper for a subtraction. No phase. Finding recorded."
    else:
        verdict.outcome = (
            "the replication confirms the council negative under frontier capability "
            "and sane formulation. Closed."
        )
    return verdict


def assert_control_collapsed(verdict: Verdict, tolerance: float = 0.02) -> None:
    """The negative control must collapse toward zero. Non-zero stops everything."""
    if abs(verdict.negative_control_mean_ic) > tolerance:
        raise LeakageDetected(
            f"the within-day shuffle control read {verdict.negative_control_mean_ic:+.4f}, "
            f"outside the {tolerance} tolerance. Everything stops."
        )
