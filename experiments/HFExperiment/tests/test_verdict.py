"""The verdict boundary behaves as registered."""
import pytest

from hfexperiment.registered import THRESHOLDS
from hfexperiment.verdict import (
    VerdictState,
    acs_radius,
    alpha_for_width,
    classify_verdict,
    confidence_bounds,
    first_crossing_day,
    tuned_rho,
)


def test_tuned_rho_minimizes_the_boundary_at_the_crossing_target() -> None:
    rho = tuned_rho()
    at_target = acs_radius(
        THRESHOLDS.crossing_target_days, 1.0, rho, THRESHOLDS.alpha_one_sided
    )
    for factor in (0.25, 0.5, 0.8, 1.25, 2.0, 4.0):
        other = acs_radius(
            THRESHOLDS.crossing_target_days, 1.0, rho * factor,
            THRESHOLDS.alpha_one_sided,
        )
        assert at_target <= other + 1e-12


def test_radius_shrinks_with_time() -> None:
    rho = tuned_rho()
    r400 = acs_radius(400, 418.0, rho, 0.05)
    r1600 = acs_radius(1600, 418.0, rho, 0.05)
    r3000 = acs_radius(3000, 418.0, rho, 0.05)
    assert r400 > r1600 > r3000


def test_radius_scales_linearly_in_sigma() -> None:
    rho = tuned_rho()
    assert acs_radius(1600, 2.0, rho, 0.05) == pytest.approx(
        2.0 * acs_radius(1600, 1.0, rho, 0.05)
    )


def test_bounds_are_symmetric_about_the_mean() -> None:
    rho = tuned_rho()
    lower, upper = confidence_bounds(27.99, 418.0, 1600, rho)
    assert upper - 27.99 == pytest.approx(27.99 - lower)


def test_classification_reads_the_registered_thresholds() -> None:
    hurdle = THRESHOLDS.cost_hurdle_bp_per_day
    futility = THRESHOLDS.futility_bp_per_day
    assert classify_verdict(hurdle + 0.1, 60.0) is VerdictState.SUCCESS
    assert classify_verdict(-5.0, futility - 0.1) is VerdictState.FUTILITY
    assert classify_verdict(hurdle - 0.1, futility + 0.1) is (
        VerdictState.CONTINUE
    )


def test_alpha_spends_on_the_registered_widths_only() -> None:
    assert alpha_for_width(THRESHOLDS.primary_width) == 0.05
    for width in THRESHOLDS.secondary_widths:
        assert alpha_for_width(width) == 0.025
    with pytest.raises(ValueError):
        alpha_for_width(7)


def test_honest_arithmetic_matches_the_registration() -> None:
    """The registered expectation: clears zero near day 2061, hurdle 2852."""
    rho = tuned_rho()
    assert first_crossing_day(27.99, 418.0, rho, 0.0) == 2061
    assert first_crossing_day(
        27.99, 418.0, rho, THRESHOLDS.cost_hurdle_bp_per_day
    ) == 2852


def test_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        acs_radius(0, 1.0, 0.1, 0.05)
    with pytest.raises(ValueError):
        acs_radius(10, 1.0, 0.1, 1.5)
