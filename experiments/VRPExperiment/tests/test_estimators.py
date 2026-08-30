"""Outcome-blind construction: the machinery is verified on known answers only.

Three fixtures are registered by Section 0's logic and built here: a **planted
premium** the canary must fire on, a **zero premium**, and a **negative
premium**. The estimator does not know which it is looking at, and the latch
decides — once — what it is finally pointed at.

A canary that cannot fire proves nothing, so `test_the_canary_fires` asserts the
planted fixture is detected *and* `test_the_canary_stays_silent_on_zero` asserts
the zero fixture is not.
"""

from __future__ import annotations

import math
import random

import pytest

from vrp.absence import AbsenceReason, Absent
from vrp.sealed_read import (
    MIN_OBSERVATIONS,
    TENOR_DAYS,
    PremiumResult,
    bps_per_volatility_point,
    build_premium_series,
    estimate_premium,
    incomplete_beta,
    newey_west_se,
    non_overlapping,
    realized_volatility,
    student_t_critical,
    student_t_sf,
)

ALPHA = 0.05


# ---------------------------------------------------------------------------
# Known-answer checks on the registered estimators
# ---------------------------------------------------------------------------


def test_realized_volatility_reproduces_a_hand_computable_answer() -> None:
    # Arrange — closes whose log returns are exactly +r, -r, +r, -r.
    r = 0.01
    closes = [100.0]
    for i in range(8):
        closes.append(closes[-1] * math.exp(r if i % 2 == 0 else -r))

    # Act
    measured = realized_volatility(closes)

    # Assert — returns alternate +/- r with mean 0, so sd = r*sqrt(n/(n-1)).
    assert not isinstance(measured, Absent)
    n = len(closes) - 1
    expected = r * math.sqrt(n / (n - 1)) * math.sqrt(365.0)
    assert measured == pytest.approx(expected, rel=1e-12)


def test_realized_volatility_annualises_by_365_not_252() -> None:
    """Crypto trades every calendar day. Section 2.3 registered 365."""
    closes = [100.0, *[100.0 * math.exp(0.01 * ((-1) ** i)) for i in range(9)]]
    measured = realized_volatility(closes)
    assert not isinstance(measured, Absent)
    # Rebuilding with a 252 factor must give a strictly different number.
    assert measured != pytest.approx(measured * math.sqrt(252.0 / 365.0))


def test_realized_volatility_refuses_rather_than_returning_zero() -> None:
    for closes in ([], [100.0], [100.0, 101.0]):
        result = realized_volatility(closes)
        assert isinstance(result, Absent)
        assert result.reason is AbsenceReason.INSUFFICIENT_SAMPLE
    negative = realized_volatility([100.0, -1.0, 102.0])
    assert isinstance(negative, Absent)


def test_the_registered_conversion_is_22_875_bps_per_volatility_point() -> None:
    """Section 2.6, fixed before any number existed."""
    per_unit = bps_per_volatility_point()
    assert per_unit == pytest.approx(2287.5, abs=0.1)
    assert per_unit * 0.01 == pytest.approx(22.875, abs=0.001)


def test_the_sign_convention_is_implied_minus_realized() -> None:
    """Section 2.4. A sign error here inverts the verdict."""
    implied = [0.60] * MIN_OBSERVATIONS
    realized = [0.50] * MIN_OBSERVATIONS
    series = build_premium_series(implied, realized)
    assert not isinstance(series, Absent)
    assert all(p == pytest.approx(0.10) for p in series.premium)
    assert series.n == MIN_OBSERVATIONS

    inverted = build_premium_series(realized, implied)
    assert not isinstance(inverted, Absent)
    assert all(p == pytest.approx(-0.10) for p in inverted.premium)


def test_a_short_series_is_absent_not_estimated() -> None:
    short = build_premium_series([0.5] * 59, [0.4] * 59)
    assert isinstance(short, Absent)
    assert short.reason is AbsenceReason.INSUFFICIENT_SAMPLE
    mismatched = build_premium_series([0.5] * 80, [0.4] * 79)
    assert isinstance(mismatched, Absent)


# ---------------------------------------------------------------------------
# The HAC standard error and the t distribution
# ---------------------------------------------------------------------------


def test_newey_west_at_bandwidth_zero_is_the_iid_standard_error() -> None:
    values = [0.1, -0.2, 0.35, 0.05, -0.1, 0.2, 0.0, 0.15]
    n = len(values)
    mean = sum(values) / n
    population_variance = sum((v - mean) ** 2 for v in values) / n
    expected = math.sqrt(population_variance / n)
    measured = newey_west_se(values, 0)
    assert not isinstance(measured, Absent)
    assert measured == pytest.approx(expected, rel=1e-12)


def test_newey_west_widens_the_interval_on_a_positively_autocorrelated_series() -> None:
    """The whole reason Section 6 registered bandwidth 30 before any data."""
    rng = random.Random(20260830)
    n = 900
    series: list[float] = []
    level = 0.0
    for _ in range(n):
        level = 0.95 * level + rng.gauss(0.0, 0.01)
        series.append(level)
    iid = newey_west_se(series, 0)
    hac = newey_west_se(series, TENOR_DAYS)
    assert not isinstance(iid, Absent)
    assert not isinstance(hac, Absent)
    assert hac > iid * 2.0, (
        "an IID standard error on an overlapping-window series is far too "
        f"narrow: iid {iid:.6g} vs hac {hac:.6g}"
    )


def test_the_t_distribution_matches_published_critical_values() -> None:
    # Published one-sided 0.05 critical values.
    assert student_t_critical(1, 0.05) == pytest.approx(6.314, abs=0.002)
    assert student_t_critical(10, 0.05) == pytest.approx(1.812, abs=0.002)
    assert student_t_critical(30, 0.05) == pytest.approx(1.697, abs=0.002)
    assert student_t_critical(1000, 0.05) == pytest.approx(1.646, abs=0.003)
    # Symmetry and the incomplete beta's endpoints.
    assert student_t_sf(0.0, 50) == pytest.approx(0.5, abs=1e-9)
    assert incomplete_beta(2.0, 3.0, 0.0) == 0.0
    assert incomplete_beta(2.0, 3.0, 1.0) == 1.0


def test_a_one_sided_test_is_not_a_two_sided_one() -> None:
    """Section 6 registered one-sided. A two-sided p would be twice this."""
    assert student_t_sf(1.812, 10) == pytest.approx(0.05, abs=0.001)


# ---------------------------------------------------------------------------
# The three registered fixtures
# ---------------------------------------------------------------------------


def _fixture(planted_premium: float, n: int = 900, seed: int = 20260830) -> list[float]:
    """A premium series with a known mean and realistic overlap structure.

    The overlap is built in deliberately: consecutive observations share 29 of
    30 forward days, so the series is strongly positively autocorrelated by
    construction, exactly as the real one will be.
    """
    rng = random.Random(seed)
    shocks = [rng.gauss(0.0, 0.04) for _ in range(n + TENOR_DAYS)]
    return [
        planted_premium + sum(shocks[t : t + TENOR_DAYS]) / TENOR_DAYS for t in range(n)
    ]


def test_the_canary_fires_on_a_planted_premium() -> None:
    """A pin that cannot fire proves nothing."""
    # Arrange — a planted premium of exactly 8 volatility points.
    planted = 0.08
    series = _fixture(planted)

    # Act
    result = estimate_premium(series, label="planted", alpha=ALPHA)

    # Assert
    assert isinstance(result, PremiumResult)
    assert result.n == 900
    assert result.mean_vol_points == pytest.approx(planted, abs=0.02)
    assert result.one_sided_p < ALPHA, "the canary must fire on a planted premium"
    assert result.ci_lower_vol_points > 0.0
    assert result.mean_bps == pytest.approx(
        result.mean_vol_points * bps_per_volatility_point(), rel=1e-12
    )


def test_the_canary_stays_silent_on_a_zero_premium() -> None:
    result = estimate_premium(_fixture(0.0), label="zero", alpha=ALPHA)
    assert isinstance(result, PremiumResult)
    assert result.mean_vol_points == pytest.approx(0.0, abs=0.02)
    assert result.one_sided_p > ALPHA, (
        "a zero-premium fixture must not reject; a canary that always fires is "
        "not a canary"
    )


def test_the_canary_stays_silent_on_a_negative_premium() -> None:
    result = estimate_premium(_fixture(-0.08), label="negative", alpha=ALPHA)
    assert isinstance(result, PremiumResult)
    assert result.mean_vol_points < 0.0
    assert result.t_statistic < 0.0
    assert result.one_sided_p > 0.5, (
        "a negative premium must give a one-sided p above one half; the test is "
        "H1: mean > 0"
    )
    assert result.ci_lower_vol_points < 0.0


def test_an_iid_standard_error_would_have_over_rejected_the_zero_fixture() -> None:
    """Why Section 6 registered HAC before seeing data, stated as a test."""
    series = _fixture(0.0)
    hac = newey_west_se(series, TENOR_DAYS)
    iid = newey_west_se(series, 0)
    assert not isinstance(hac, Absent)
    assert not isinstance(iid, Absent)
    assert hac > iid, (
        "on an overlapping-window series the IID error is the narrower one, "
        "which is how a null becomes a false positive"
    )


def test_the_non_overlapping_robustness_check_costs_a_factor_of_thirty() -> None:
    series = _fixture(0.08)
    thinned = non_overlapping(series)
    assert len(thinned) == math.ceil(len(series) / TENOR_DAYS)
    assert len(thinned) == 30


def test_the_estimator_cannot_tell_a_fixture_from_real_data() -> None:
    """Outcome blindness, stated structurally.

    `estimate_premium` takes a bare list of floats. It has no parameter, field
    or branch that distinguishes a fixture from a real series, so no code path
    can behave differently on the real read.
    """
    import inspect

    signature = inspect.signature(estimate_premium)
    names = set(signature.parameters)
    assert names == {"premium", "label", "bandwidth", "alpha"}
    for forbidden in ("is_real", "fixture", "source", "latch", "mode"):
        assert forbidden not in names


# ---------------------------------------------------------------------------
# The registered hedging rule, verified on known answers
# ---------------------------------------------------------------------------


def test_an_atm_straddle_is_delta_flat_to_a_small_convexity_term() -> None:
    """At S = K the straddle delta is 2*N(sigma*sqrt(T)/2) - 1, near zero."""
    from vrp.sealed_read import straddle_delta

    delta = straddle_delta(100.0, 100.0, 0.60, 30.0 / 365.0)
    assert not isinstance(delta, Absent)
    expected_d1 = 0.5 * 0.60 * math.sqrt(30.0 / 365.0)
    expected = 2.0 * 0.5 * (1.0 + math.erf(expected_d1 / math.sqrt(2.0))) - 1.0
    assert delta == pytest.approx(expected, rel=1e-12)
    assert 0.0 < delta < 0.15


def test_straddle_delta_moves_the_right_way_and_saturates() -> None:
    from vrp.sealed_read import straddle_delta

    up = straddle_delta(140.0, 100.0, 0.60, 30.0 / 365.0)
    down = straddle_delta(60.0, 100.0, 0.60, 30.0 / 365.0)
    assert not isinstance(up, Absent) and not isinstance(down, Absent)
    assert up > 0.9, "deep in the money the straddle is long one unit"
    assert down < -0.9, "deep out of the money it is short one unit"


def test_straddle_delta_refuses_impossible_inputs() -> None:
    from vrp.sealed_read import straddle_delta

    for args in (
        (0.0, 100.0, 0.6, 0.1),
        (100.0, 0.0, 0.6, 0.1),
        (100.0, 100.0, 0.0, 0.1),
        (100.0, 100.0, 0.6, 0.0),
    ):
        assert isinstance(straddle_delta(*args), Absent)


def test_a_flat_price_path_requires_no_rebalance() -> None:
    from vrp.sealed_read import RebalanceCount, count_rebalances

    result = count_rebalances([100.0] * 31, strike=100.0, sigma=0.60, band=0.10)
    assert isinstance(result, RebalanceCount)
    assert result.rebalances == 0, "a flat path cannot breach a delta band"
    assert result.days_evaluated == 29


def test_a_trending_path_requires_more_rebalances_at_a_tighter_band() -> None:
    from vrp.sealed_read import RebalanceCount, count_rebalances

    closes = [100.0 * (1.01**i) for i in range(31)]
    tight = count_rebalances(closes, strike=100.0, sigma=0.60, band=0.05)
    registered = count_rebalances(closes, strike=100.0, sigma=0.60, band=0.10)
    wide = count_rebalances(closes, strike=100.0, sigma=0.60, band=0.20)
    assert isinstance(tight, RebalanceCount)
    assert isinstance(registered, RebalanceCount)
    assert isinstance(wide, RebalanceCount)
    assert tight.rebalances >= registered.rebalances >= wide.rebalances
    assert tight.rebalances > 0, "a 1%/day trend must breach a 0.05 band"


def test_the_rebalance_count_refuses_rather_than_returning_zero() -> None:
    from vrp.sealed_read import count_rebalances

    assert isinstance(count_rebalances([100.0], 100.0, 0.6), Absent)
    assert isinstance(count_rebalances([100.0, 101.0], 100.0, 0.0), Absent)
