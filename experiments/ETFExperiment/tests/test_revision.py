"""A.1 Task 4's forward leg: the sign-flip and threshold-cross rates decide it."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from etf.config import CONFIG
from etf.revision import ValueAt, build_report, compare_day

D = date(2025, 6, 2)
T0 = datetime(2025, 6, 3, 2, tzinfo=UTC)
T = CONFIG.signal_threshold_usd


def v(hours: float, value: float) -> ValueAt:
    return ValueAt(captured_at=T0 + timedelta(hours=hours), signal_usd=value)


def test_a_single_capture_yields_no_comparison() -> None:
    assert compare_day(D, [v(0, 150e6)]) is None


def test_an_unrevised_day_is_intact_and_carries_a_zero_delta() -> None:
    rev = compare_day(D, [v(0, 150e6), v(24, 150e6)])
    assert rev is not None
    assert not rev.revised
    assert rev.delta_usd == 0.0
    assert rev.intact


def test_a_revision_that_keeps_sign_and_side_is_revised_but_intact() -> None:
    rev = compare_day(D, [v(0, 150e6), v(24, 180e6)])
    assert rev is not None
    assert rev.revised
    assert not rev.sign_flipped
    assert not rev.threshold_crossed
    assert rev.intact
    assert rev.delta_usd == 30e6
    assert rev.delta_share == 0.2


def test_a_sign_flip_is_caught_even_when_neither_side_clears_the_threshold() -> None:
    """E1 is a rank correlation, so a sign flip corrupts it whatever the threshold does."""
    rev = compare_day(D, [v(0, 20e6), v(24, -20e6)])
    assert rev is not None
    assert rev.sign_flipped
    assert not rev.intact


def test_a_threshold_cross_is_caught_when_the_sign_is_unchanged() -> None:
    """E2 trades the position, so a move across T corrupts it with no sign change."""
    rev = compare_day(D, [v(0, 150e6), v(24, 50e6)])
    assert rev is not None
    assert not rev.sign_flipped
    assert rev.threshold_crossed
    assert not rev.intact


def test_the_threshold_boundary_fixture_sits_exactly_on_T() -> None:
    """Exactly +T is FLAT, so moving from T to T+1 is a cross."""
    rev = compare_day(D, [v(0, T), v(24, T + 1.0)])
    assert rev is not None
    assert rev.threshold_crossed


def test_the_settled_value_is_the_one_standing_at_the_registered_horizon() -> None:
    """48 hours after the first capture, and the fixture sits exactly on it."""
    assert CONFIG.revision_settle_hours == 48
    rev = compare_day(
        D,
        [v(0, 150e6), v(CONFIG.revision_settle_hours, 200e6), v(72, 900e6)],
    )
    assert rev is not None
    assert rev.settled_value_usd == 200e6, "a value past the horizon does not settle the day"


def test_the_report_reports_every_share_with_its_n() -> None:
    per_day = {
        date(2025, 6, 2): [v(0, 150e6), v(24, 150e6)],
        date(2025, 6, 3): [v(0, 150e6), v(24, 50e6)],
        date(2025, 6, 4): [v(0, 20e6), v(24, -20e6)],
        date(2025, 6, 5): [v(0, 150e6)],
    }
    report = build_report(per_day)
    assert report.n_days == 3
    assert report.revised_days == 2
    assert report.sign_flip_days == 1
    assert report.threshold_cross_days == 1, "a sign flip wholly inside the band is not a cross"
    assert report.intact_days == 1
    assert report.intact_share is not None
    assert abs(report.intact_share - 1 / 3) < 1e-12


def test_an_empty_input_reports_absences_not_zeros() -> None:
    report = build_report({})
    assert report.n_days == 0
    assert report.revised_share is None
    assert report.intact_share is None
    assert report.median_abs_delta_usd is None
