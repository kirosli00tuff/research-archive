"""The power module: known answers, boundary behaviour, and no outcome read."""

from __future__ import annotations

import math
import random

import pytest

from etf.config import CONFIG
from etf.power import (
    _inverse_normal_cdf,
    _two_sided_cut,
    e1_critical_value,
    e1_power,
    pearson_for_spearman,
    spearman,
    spearman_from_ranks,
)


def test_spearman_of_the_identity_permutation_is_one() -> None:
    assert spearman_from_ranks(list(range(50))) == 1.0


def test_spearman_of_the_reversed_permutation_is_minus_one() -> None:
    assert spearman_from_ranks(list(reversed(range(50)))) == -1.0


def test_spearman_is_monotone_invariant() -> None:
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [10.0, 20.0, 30.0, 40.0, 50.0]
    assert spearman(x, y) == 1.0
    assert spearman(x, [math.exp(v) for v in y]) == 1.0


def test_spearman_needs_paired_samples() -> None:
    with pytest.raises(ValueError, match="paired samples"):
        spearman([1.0, 2.0], [1.0])


def test_a_rank_correlation_on_two_points_is_an_absence() -> None:
    with pytest.raises(ValueError, match="an absence, not a number"):
        spearman_from_ranks([0, 1])


def test_the_copula_inversion_round_trips_at_the_registered_assumptions() -> None:
    """rho_s = (6/pi) arcsin(rho_p / 2), inverted."""
    for rho_s in (CONFIG.rho_registered, CONFIG.rho_undecayed, CONFIG.rho_quartered):
        rho_p = pearson_for_spearman(rho_s)
        assert (6.0 / math.pi) * math.asin(rho_p / 2.0) == pytest.approx(rho_s, abs=1e-12)


def test_a_rank_correlation_outside_minus_one_to_one_is_refused() -> None:
    with pytest.raises(ValueError, match=r"\[-1, 1\]"):
        pearson_for_spearman(1.5)


def test_the_permutation_critical_value_tracks_the_known_null_sd() -> None:
    """Under H0 the permutation rho has sd 1/sqrt(n-1); the simulated cut must agree."""
    n = 200
    rng = random.Random(7)
    cut = e1_critical_value(n, 0.05, 4000, rng)
    expected = 1.6449 / math.sqrt(n - 1)
    assert abs(cut - expected) < 0.02, f"cut {cut} against the asymptotic {expected}"


def test_a_tighter_alpha_demands_a_higher_critical_value() -> None:
    rng = random.Random(11)
    loose = e1_critical_value(200, 0.10, 4000, rng)
    tight = e1_critical_value(200, 0.01, 4000, rng)
    assert tight > loose


def test_power_at_a_zero_true_effect_sits_at_alpha_the_calibration_check() -> None:
    """A test whose size is not alpha under the null is not the registered test."""
    power = e1_power(120, 0.0, alpha=0.05, draws=4000, simulations=800, seed=3)
    assert 0.02 < power < 0.09, f"size {power} is not near the nominal 0.05"


def test_power_rises_with_the_true_effect_and_with_n() -> None:
    small = e1_power(120, 0.05, draws=3000, simulations=400, seed=5)
    large = e1_power(120, 0.30, draws=3000, simulations=400, seed=5)
    assert large > small
    thin = e1_power(60, 0.20, draws=3000, simulations=400, seed=5)
    thick = e1_power(600, 0.20, draws=3000, simulations=400, seed=5)
    assert thick > thin


def test_a_huge_effect_on_a_large_sample_is_near_certain() -> None:
    assert e1_power(400, 0.60, draws=2000, simulations=200, seed=9) > 0.99


def test_the_inverse_normal_cdf_matches_known_quantiles() -> None:
    assert _inverse_normal_cdf(0.5) == pytest.approx(0.0, abs=1e-9)
    assert _inverse_normal_cdf(0.975) == pytest.approx(1.959964, abs=1e-5)
    assert _inverse_normal_cdf(0.99) == pytest.approx(2.326348, abs=1e-5)
    assert _inverse_normal_cdf(0.01) == pytest.approx(-2.326348, abs=1e-5)


def test_the_trade_share_cut_reproduces_the_share_it_was_given() -> None:
    assert _two_sided_cut(1.0) == pytest.approx(0.0, abs=1e-9)
    assert _two_sided_cut(0.05) == pytest.approx(1.959964, abs=1e-5)
    with pytest.raises(ValueError, match=r"\(0, 1\]"):
        _two_sided_cut(0.0)


def test_the_module_reads_no_outcome_and_imports_no_network() -> None:
    import ast
    import pathlib

    source = pathlib.Path("src/etf/power.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
        elif isinstance(node, ast.Import):
            modules |= {a.name for a in node.names}
    assert not (modules & {"etf.http", "etf.seal", "urllib", "urllib.request"})
    assert "etf.preperiod_prices" not in modules, (
        "power takes its pre-period inputs as arguments; it does not fetch them itself"
    )
