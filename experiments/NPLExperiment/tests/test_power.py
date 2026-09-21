"""Exact binomial power, checked against an exact-fraction reference."""

from __future__ import annotations

from fractions import Fraction
from math import comb

import pytest

from npl.config import CONFIG
from npl.power import (
    co_primary_powers,
    critical_k,
    exact_power,
    min_n_for_power,
    upper_tail,
)


def _tail_exact(n: int, k: int, p: Fraction) -> Fraction:
    total = Fraction(0)
    for i in range(k, n + 1):
        total += Fraction(comb(n, i)) * p**i * (1 - p) ** (n - i)
    return total


def test_upper_tail_matches_the_exact_fraction_reference() -> None:
    cases = [(10, 9, Fraction(1, 2)), (50, 30, Fraction(6, 10)), (200, 130, Fraction(1, 2))]
    for n, k, p in cases:
        got = upper_tail(n, k, float(p))
        want = float(_tail_exact(n, k, p))
        assert got == pytest.approx(want, abs=1e-12)


def test_critical_k_known_answer_n10_alpha_05() -> None:
    # P(X>=9 | n=10, p=1/2) = 11/1024 = 0.0107 <= 0.05; P(X>=8) = 56/1024 > 0.05.
    assert critical_k(10, 0.5, 0.05) == 9


def test_the_boundary_alpha_is_inclusive() -> None:
    # P(X>=4 | n=4, p=1/2) = 1/16 = 0.0625 exactly. At alpha = 0.0625 the
    # rule "<= alpha" admits k=4. The fixture sits ON the registered boundary.
    assert critical_k(4, 0.5, 0.0625) == 4
    assert critical_k(4, 0.5, 0.0624) is None


def test_power_is_zero_when_no_rejection_region_exists() -> None:
    assert exact_power(3, 0.5, 0.9, 0.01) == 0.0


def test_power_known_answer() -> None:
    # n=10, p0=0.5, alpha=0.05 -> k*=9; power at 0.9 = P(X>=9 | 0.9)
    want = float(_tail_exact(10, 9, Fraction(9, 10)))
    assert exact_power(10, 0.5, 0.9, 0.05) == pytest.approx(want, abs=1e-12)


def test_min_n_returns_a_stable_threshold() -> None:
    n_star = min_n_for_power(0.5, 0.7, CONFIG.alpha_adj, 0.80, n_max=400)
    assert n_star is not None
    # From the stable threshold onward, power stays at or above target.
    for n in range(n_star, n_star + 25):
        assert exact_power(n, 0.5, 0.7, CONFIG.alpha_adj) >= 0.80
    # And the point just below it does not clear the bar.
    assert exact_power(n_star - 1, 0.5, 0.7, CONFIG.alpha_adj) < 0.80


def test_the_registered_alpha_is_the_sidak_third() -> None:
    assert CONFIG.alpha_adj == pytest.approx(1.0 - 0.95 ** (1.0 / 3.0))
    assert CONFIG.alpha_adj == pytest.approx(0.0170, abs=5e-5)


def test_co_primary_powers_reads_the_registered_assumptions() -> None:
    report = co_primary_powers("unit", n_events=100, n_pairs=80)
    assert report.p1_power == pytest.approx(
        exact_power(100, CONFIG.p1_bar, CONFIG.p1_true_share, CONFIG.alpha_adj)
    )
    assert report.p2_power == pytest.approx(
        exact_power(100, 0.5, CONFIG.p2_true_share, CONFIG.alpha_adj)
    )
    assert report.p3_power == pytest.approx(
        exact_power(80, 0.5, CONFIG.p3_true_share, CONFIG.alpha_adj)
    )


def test_impossible_counts_raise() -> None:
    with pytest.raises(ValueError, match="impossible"):
        co_primary_powers("unit", n_events=10, n_pairs=11)
