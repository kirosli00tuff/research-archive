"""The whole verdict pipeline, proved end to end on synthetic data.

Fake returns only. This test exercises every line B.2 will run without touching
one real outcome, which is what lets the sealed store stay sealed until the
operator writes Amendment 0.
"""

from __future__ import annotations

import dataclasses
import random

import pytest

from npd.config import CONFIG
from npd.eval.evaluator import (
    LeakageDetected,
    assert_control_collapsed,
    block_bootstrap_interval,
    daily_ic,
    evaluate,
    spearman,
)

FAST = dataclasses.replace(CONFIG, bootstrap_resamples=400, permutation_resamples=60)
SYMBOLS = [f"S{i:02d}" for i in range(30)]


def _returns(rng: random.Random) -> dict[str, float]:
    return {s: rng.gauss(0.0, 0.02) for s in SYMBOLS}


def _true_order(returns: dict[str, float]) -> list[str]:
    return sorted(SYMBOLS, key=lambda s: (-returns[s], s))


def _noisy_order(returns: dict[str, float], rng: random.Random, skill: float) -> list[str]:
    """A ranking that carries `skill` of the truth and the rest noise."""
    scored = {s: skill * returns[s] + (1 - skill) * rng.gauss(0.0, 0.02) for s in SYMBOLS}
    return sorted(SYMBOLS, key=lambda s: (-scored[s], s))


def _world(
    days: int, skill: float, seed: int
) -> tuple[dict[str, list[str]], dict[str, dict[str, list[str]]], dict[str, dict[str, float]]]:
    rng = random.Random(seed)
    dates = [f"2025-{1 + d // 20:02d}-{1 + d % 20:02d}" for d in range(days)]
    returns_by_day: dict[str, dict[str, float]] = {}
    model_orders: dict[str, list[str]] = {}
    baseline_orders: dict[str, dict[str, list[str]]] = {
        name: {} for name in ("sign_last", "mom_12_1", "logistic")
    }
    for d in dates:
        r = _returns(rng)
        returns_by_day[d] = r
        model_orders[d] = _noisy_order(r, rng, skill)
        for name in baseline_orders:
            shuffled = list(SYMBOLS)
            rng.shuffle(shuffled)
            baseline_orders[name][d] = shuffled
    return model_orders, baseline_orders, returns_by_day


def test_a_perfect_ranking_scores_plus_one() -> None:
    """The sign convention. Rank 1 is best in both vectors, so perfect is +1."""
    rng = random.Random(1)
    r = _returns(rng)
    assert daily_ic(_true_order(r), r) == pytest.approx(1.0)


def test_a_reversed_ranking_scores_minus_one() -> None:
    rng = random.Random(2)
    r = _returns(rng)
    assert daily_ic(list(reversed(_true_order(r))), r) == pytest.approx(-1.0)


def test_spearman_needs_spread_and_pairs() -> None:
    with pytest.raises(ValueError):
        spearman([1.0, 2.0], [1.0, 2.0])
    with pytest.raises(ValueError):
        spearman([1.0, 1.0, 1.0], [1.0, 2.0, 3.0])


def test_the_block_bootstrap_brackets_the_point_estimate() -> None:
    values = [0.05] * 100
    iv = block_bootstrap_interval(values, resamples=200, block_length=10, t_critical=2.0, seed=1)
    assert iv.point == pytest.approx(0.05)
    assert iv.low <= iv.point <= iv.high


def test_a_signal_free_model_scores_near_zero() -> None:
    """A model with no skill produces a mean rank IC near zero on every seed.

    The assertion is on the magnitude, not on the verdict. A single seed can
    throw a two-sigma fluke and calling that a failure would be the same mistake
    the predecessor made when it read a pooling artifact as a result. The false
    positive RATE is checked separately, below.
    """
    for seed in (11, 21, 31):
        model, baselines, returns = _world(200, skill=0.0, seed=seed)
        v = evaluate(model, baselines, returns, FAST)
        assert abs(v.model_mean_ic) < 0.05, f"seed {seed} produced {v.model_mean_ic}"
        assert not v.beats_best_baseline


def test_the_bootstrap_is_not_under_dispersed() -> None:
    """An under-dispersed interval would manufacture significance.

    The daily rank IC of an unskilled ranking over 30 names has standard
    deviation 1/sqrt(29). The bootstrap standard error of a mean over n such days
    must land near that divided by sqrt(n). A bootstrap that read tighter would
    turn noise into findings, which is exactly what this repository exists to
    stop.
    """
    import math
    import statistics

    rng = random.Random(404)
    n = 200
    theory = (1.0 / math.sqrt(len(SYMBOLS) - 1)) / math.sqrt(n)
    widths = []
    excluded = 0
    for trial in range(25):
        series = []
        for _ in range(n):
            r = _returns(rng)
            order = list(SYMBOLS)
            rng.shuffle(order)
            series.append(daily_ic(order, r))
        iv = block_bootstrap_interval(
            series, resamples=300, block_length=10, t_critical=2.0, seed=trial
        )
        widths.append((iv.high - iv.point) / 2.0)
        excluded += int(iv.excludes_zero())
    measured = statistics.mean(widths)
    assert measured == pytest.approx(theory, rel=0.25), (
        f"bootstrap standard error {measured:.5f} against theory {theory:.5f}"
    )
    assert excluded <= 6, f"{excluded} of 25 iid series were called significant"


def test_a_model_with_real_skill_beats_coin_and_the_baselines() -> None:
    model, baselines, returns = _world(220, skill=0.55, seed=12)
    v = evaluate(model, baselines, returns, FAST)
    assert v.model_mean_ic > 0.1
    assert v.beats_coin
    assert v.beats_best_baseline
    assert "C.1 authorized" in v.outcome
    assert v.permutation_p < 0.05


def test_the_negative_control_collapses_toward_zero() -> None:
    model, baselines, returns = _world(220, skill=0.55, seed=13)
    v = evaluate(model, baselines, returns, FAST)
    assert abs(v.negative_control_mean_ic) < 0.02
    assert_control_collapsed(v)


def test_leakage_stops_everything() -> None:
    model, baselines, returns = _world(60, skill=0.0, seed=14)
    v = evaluate(model, baselines, returns, FAST)
    v.negative_control_mean_ic = 0.25
    with pytest.raises(LeakageDetected, match="Everything stops"):
        assert_control_collapsed(v)


def test_the_best_baseline_is_the_one_the_contrast_uses() -> None:
    model, baselines, returns = _world(120, skill=0.4, seed=15)
    v = evaluate(model, baselines, returns, FAST)
    assert v.best_baseline in v.baseline_mean_ic
    assert v.baseline_mean_ic[v.best_baseline] == max(v.baseline_mean_ic.values())


def test_no_evaluable_days_raises_rather_than_returning_a_verdict() -> None:
    with pytest.raises(ValueError, match="no evaluable days"):
        evaluate({}, {}, {}, FAST)
