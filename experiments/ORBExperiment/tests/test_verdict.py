"""Section 8, built dark. Includes the planted-signal canary that must fire.

A verdict machine that has never been shown to fire on a planted edge, and
never been shown to stay silent on noise, is an assertion about nothing.
"""

from __future__ import annotations

import math
import random

import pytest

from orb.absence import AbsenceReason, Absent
from orb.config import CONFIG
from orb.verdict import (
    alpha_adj,
    annualize,
    concentration_gate,
    daily_from_annual,
    deflated_sharpe_probability,
    deflated_sharpe_statistic,
    expected_max_sharpe,
    fire_verdict,
    kurtosis,
    permutation_lower_bound,
    persistence_gate,
    sharpe,
    skewness,
)

# --- The registered arithmetic of Section 9, reproduced in code -----------


def test_alpha_adj_is_the_registered_figure() -> None:
    """1 - 0.95 ** (1/2) = 0.02532057..., applied to each co-primary."""
    assert alpha_adj(2) == pytest.approx(0.02532057, abs=1e-8)
    assert 1 - (1 - alpha_adj(2)) ** 2 == pytest.approx(0.05, abs=1e-12)


def test_the_registered_daily_sharpe_reproduces() -> None:
    """1.40 / sqrt(252) = 0.0882. The registration's own figure."""
    assert daily_from_annual(1.40) == pytest.approx(0.0882, abs=1e-4)


def test_the_registered_minimum_n_figures_reproduce() -> None:
    """514 sessions clears t = 2.0; 1,157 clears t = 3.0. Both stated in Section 9."""
    d = daily_from_annual(CONFIG.registered_sharpe_assumption)
    assert d * math.sqrt(514) == pytest.approx(2.0, abs=0.001)
    assert d * math.sqrt(1157) == pytest.approx(3.0, abs=0.001)


def test_the_holdout_t_is_below_the_factor_zoo_hurdle() -> None:
    """The openly registered shortfall (ADR-005), at the computed n = 875."""
    d = daily_from_annual(CONFIG.registered_sharpe_assumption)
    t_computed = d * math.sqrt(875)
    t_stated = d * math.sqrt(880)
    assert t_computed == pytest.approx(2.609, abs=0.001)
    assert t_stated == pytest.approx(2.616, abs=0.001)
    assert t_computed < 3.0
    assert t_computed > CONFIG.holdout_per_trade_t_gate


# --- Sharpe and its moments ----------------------------------------------


def test_sharpe_is_mean_over_standard_deviation() -> None:
    """Hand-computed: [1,2,3,4,5] has mean 3 and sample sd sqrt(2.5)."""
    assert sharpe([1, 2, 3, 4, 5]) == pytest.approx(3 / math.sqrt(2.5))


def test_annualize_multiplies_by_root_252() -> None:
    assert annualize(0.0882) == pytest.approx(0.0882 * math.sqrt(252))
    assert annualize(daily_from_annual(1.40)) == pytest.approx(1.40)


def test_a_degenerate_series_is_refused_not_reported_as_infinite() -> None:
    with pytest.raises(ValueError, match="zero dispersion"):
        sharpe([2.0] * 10)
    with pytest.raises(ValueError, match="at least two"):
        sharpe([1.0])


def test_kurtosis_of_a_normal_series_is_near_three() -> None:
    rng = random.Random(11)
    series = [rng.gauss(0.0, 1.0) for _ in range(20_000)]
    assert kurtosis(series) == pytest.approx(3.0, abs=0.15)
    assert skewness(series) == pytest.approx(0.0, abs=0.06)


def test_skewness_detects_a_deliberately_skewed_series() -> None:
    """The DSR is registered to take skew from the realized series, so it must move."""
    series = [0.0] * 99 + [50.0]
    assert skewness(series) > 5.0


# --- Deflation ------------------------------------------------------------


def test_expected_max_sharpe_grows_with_the_trial_count() -> None:
    """More trials, a higher bar to clear by chance. This is the whole point."""
    two = expected_max_sharpe(2, 0.05)
    eight = expected_max_sharpe(CONFIG.trial_count, 0.05)
    fifty = expected_max_sharpe(50, 0.05)
    assert isinstance(two, float) and isinstance(eight, float)
    assert isinstance(fifty, float)
    assert two < eight < fifty


def test_expected_max_sharpe_scales_with_trial_dispersion() -> None:
    a = expected_max_sharpe(8, 0.05)
    b = expected_max_sharpe(8, 0.10)
    assert isinstance(a, float) and isinstance(b, float)
    assert b == pytest.approx(2 * a)


def test_an_unmeasured_trial_dispersion_returns_a_recorded_absence() -> None:
    """A deflation benchmark from an invented dispersion deflates by an invented
    amount. The repository refuses rather than assumes."""
    missing = Absent(AbsenceReason.NOT_YET_MEASURED, "no trial dispersion measured")
    assert isinstance(expected_max_sharpe(8, missing), Absent)
    assert isinstance(deflated_sharpe_statistic([0.1, 0.2, 0.3], missing), Absent)


def test_the_absence_propagates_through_the_whole_verdict() -> None:
    missing = Absent(AbsenceReason.NOT_YET_MEASURED, "no trial dispersion measured")
    result = fire_verdict(
        [0.01, -0.02, 0.03] * 20,
        {"2023-01-03": [1.0, 2.0]},
        {2023: 5.0, 2024: 5.0, 2025: 5.0, 2026: 5.0},
        missing,
    )
    assert isinstance(result, Absent)
    assert "E1 cannot be computed" in result.detail


def test_the_dsr_probability_falls_as_the_benchmark_rises() -> None:
    rng = random.Random(7)
    series = [rng.gauss(0.05, 1.0) for _ in range(1000)]
    low = deflated_sharpe_probability(series, 0.0)
    high = deflated_sharpe_probability(series, 0.05)
    assert 0.0 <= high <= low <= 1.0


# --- The planted-signal canary -------------------------------------------


def test_the_canary_fires_on_a_planted_edge() -> None:
    """A series built with a known, large edge MUST clear both co-primaries.

    Planted: daily returns with an annualized Sharpe near 3.0, and per-trade PnL
    with a strong positive mean spread across many sessions. If this does not
    fire, the verdict machinery is broken and no negative result from it means
    anything.
    """
    rng = random.Random(2026)
    daily_sr = daily_from_annual(3.0)
    returns = [rng.gauss(daily_sr, 1.0) for _ in range(875)]

    pnl_by_session = {
        f"s{i:04d}": [rng.gauss(6.0, 4.0) for _ in range(20)] for i in range(300)
    }
    pnl_by_year = {2023: 100.0, 2024: 110.0, 2025: 95.0, 2026: 105.0}

    result = fire_verdict(returns, pnl_by_session, pnl_by_year, 0.01, iterations=2000)
    assert not isinstance(result, Absent)
    assert result.e1_statistic is not None and result.e1_statistic > 1.0
    assert result.e1_passes, result.e1_statistic
    assert result.e2_p_value < alpha_adj(), result.e2_p_value
    assert result.e2_passes
    assert result.concentration_passes
    assert result.persistence_passes
    assert result.passes


def test_the_canary_stays_silent_on_pure_noise() -> None:
    """A zero-mean series must NOT clear the bars. The converse of the canary."""
    rng = random.Random(99)
    returns = [rng.gauss(0.0, 1.0) for _ in range(875)]
    pnl_by_session = {
        f"s{i:04d}": [rng.gauss(0.0, 4.0) for _ in range(20)] for i in range(300)
    }
    pnl_by_year = {2023: 1.0, 2024: -1.0, 2025: 0.5, 2026: -0.4}

    result = fire_verdict(returns, pnl_by_session, pnl_by_year, 0.01, iterations=2000)
    assert not isinstance(result, Absent)
    assert not result.e1_passes
    assert not result.passes


# --- E2, the clustered permutation ---------------------------------------


def test_the_permutation_clusters_on_session_date() -> None:
    """One strong session must not masquerade as many independent observations.

    The same 40 trades are presented twice: once as 40 separate sessions, and
    once as 2 sessions of 20. The clustered arrangement carries far less
    evidence, and the p-value must reflect that.
    """
    trades = [3.0] * 20 + [1.0] * 20
    spread = {f"s{i:02d}": [t] for i, t in enumerate(trades)}
    clustered = {"s00": trades[:20], "s01": trades[20:]}

    p_spread, mean_spread = permutation_lower_bound(spread, iterations=4000, seed=5)
    p_clustered, mean_clustered = permutation_lower_bound(
        clustered, iterations=4000, seed=5
    )

    assert mean_spread == pytest.approx(mean_clustered)
    assert p_spread < p_clustered, (p_spread, p_clustered)


def test_the_permutation_p_value_is_bounded_and_never_zero() -> None:
    """(k+1)/(iterations+1) — a permutation p-value of exactly zero is a lie."""
    strong = {f"s{i:03d}": [50.0] for i in range(100)}
    p, mean = permutation_lower_bound(strong, iterations=1000, seed=3)
    assert mean == 50.0
    assert p > 0.0
    assert p == pytest.approx(1 / 1001, abs=1e-9)


def test_an_empty_input_is_refused() -> None:
    with pytest.raises(ValueError, match="no sessions"):
        permutation_lower_bound({}, iterations=10)
    with pytest.raises(ValueError, match="no trades"):
        permutation_lower_bound({"s0": []}, iterations=10)


# --- The two structural gates --------------------------------------------


def test_the_concentration_gate_sits_exactly_on_fifty_percent() -> None:
    """50 percent exactly passes; a hair above fails. The 2022 share was 0.76."""
    assert concentration_gate({2023: 50.0, 2024: 50.0})
    assert not concentration_gate({2023: 50.01, 2024: 49.99})


def test_the_concentration_gate_fails_the_replications_own_profile() -> None:
    """76 percent from one year (carried, C-8) is exactly what this gate stops."""
    assert not concentration_gate({2022: 76.0, 2021: 8.0, 2020: 8.0, 2019: 8.0})


def test_a_non_positive_total_fails_the_concentration_gate() -> None:
    """A losing strategy cannot pass a concentration gate by shrinking its own base."""
    assert not concentration_gate({2023: -10.0, 2024: 5.0})
    assert not concentration_gate({2023: 0.0, 2024: 0.0})


def test_the_persistence_gate_needs_three_of_four_positive_years() -> None:
    assert persistence_gate({2023: 1.0, 2024: 1.0, 2025: 1.0, 2026: -5.0})
    assert not persistence_gate({2023: 1.0, 2024: 1.0, 2025: -1.0, 2026: -5.0})


def test_a_zero_year_is_not_a_positive_year() -> None:
    """The boundary sits on zero, and zero is not positive."""
    assert persistence_gate({2023: 1.0, 2024: 1.0, 2025: 0.0, 2026: 1.0}) is not False
    assert persistence_gate({2023: 1.0, 2024: 1.0, 2025: 0.0, 2026: 1.0})
    assert not persistence_gate({2023: 1.0, 2024: 0.0, 2025: 0.0, 2026: 1.0})


def test_all_four_conditions_are_required() -> None:
    """Three of four is a failure. Pinned so no gate can quietly become advisory."""
    rng = random.Random(4)
    returns = [rng.gauss(daily_from_annual(3.0), 1.0) for _ in range(875)]
    sessions = {
        f"s{i:04d}": [rng.gauss(6.0, 4.0) for _ in range(20)] for i in range(300)
    }
    concentrated = {2023: 90.0, 2024: 4.0, 2025: 3.0, 2026: 3.0}

    result = fire_verdict(returns, sessions, concentrated, 0.01, iterations=1000)
    assert not isinstance(result, Absent)
    assert result.e1_passes
    assert result.e2_passes
    assert result.persistence_passes
    assert not result.concentration_passes
    assert not result.passes
