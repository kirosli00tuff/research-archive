"""A.1 Task 3's figures, with the anchor boundary fixture sitting exactly on 08:00Z."""

from __future__ import annotations

from datetime import UTC, date, datetime

from etf.config import CONFIG
from etf.lag import CaptureObservation, build_report, day_lags

D = date(2025, 6, 2)
FIVE = frozenset(CONFIG.flow_universe_tickers)


def obs(
    hour: int,
    minute: int = 0,
    *,
    present: bool,
    day: date = D,
    absent: frozenset[str] = frozenset(),
) -> CaptureObservation:
    return CaptureObservation(
        captured_at=datetime(2025, 6, 3, hour, minute, tzinfo=UTC),
        trade_date=day,
        signal_present=present,
        present_tickers=FIVE - absent if present or absent else frozenset(),
        absent_tickers=absent if present or absent else FIVE,
    )


def test_the_first_print_is_the_earliest_capture_in_which_the_value_stood() -> None:
    lags = day_lags(
        [obs(6, present=False), obs(3, present=False), obs(5, present=True), obs(7, present=True)]
    )
    assert len(lags) == 1
    assert lags[0].first_present_at == datetime(2025, 6, 3, 5, tzinfo=UTC)
    assert lags[0].hours_past_midnight_next_day == 5.0
    assert lags[0].captures == 4


def test_captures_are_ordered_by_clock_not_by_file_position() -> None:
    """Standing rule 9. The out-of-order input above already exercises it."""
    late_first = [obs(9, present=True), obs(2, present=True)]
    assert day_lags(late_first)[0].hours_past_midnight_next_day == 2.0


def test_a_first_print_one_minute_before_the_anchor_counts_as_before_it() -> None:
    assert day_lags([obs(7, 59, present=True)])[0].before_provisional_anchor


def test_a_first_print_exactly_on_the_anchor_does_not_count_as_before_it() -> None:
    """Strictly before, and the fixture sits exactly on 08:00:00Z."""
    assert not day_lags([obs(8, 0, present=True)])[0].before_provisional_anchor


def test_a_day_that_never_printed_carries_no_hours_and_is_counted() -> None:
    lag = day_lags([obs(2, present=False), obs(9, present=False)])[0]
    assert lag.first_present_at is None
    assert lag.hours_past_midnight_next_day is None
    assert not lag.before_provisional_anchor


def test_the_largest_fund_reporting_late_is_measured_on_the_first_registered_ticker() -> None:
    largest = CONFIG.flow_universe_tickers[0]
    report = build_report([obs(2, present=True, absent=frozenset({largest})), obs(4, present=True)])
    assert report.largest_fund_late_days == 1
    assert report.largest_fund_late_share == 1.0


def test_a_dash_that_a_later_capture_fills_with_a_number_is_counted() -> None:
    largest = CONFIG.flow_universe_tickers[0]
    report = build_report([obs(2, present=True, absent=frozenset({largest})), obs(4, present=True)])
    assert report.dash_then_number_days == 1


def test_a_day_never_dashed_is_not_counted_as_a_dash_then_number() -> None:
    report = build_report([obs(2, present=True), obs(4, present=True)])
    assert report.dash_then_number_days == 0


def test_the_registered_minimum_of_fifteen_trading_days_gates_the_report() -> None:
    assert CONFIG.lag_min_trading_days == 15
    few = build_report([obs(2, present=True, day=date(2025, 6, d)) for d in range(1, 5)])
    assert not few.meets_registered_minimum
    many = build_report([obs(2, present=True, day=date(2025, 6, d)) for d in range(1, 16)])
    assert many.n_days == 15
    assert many.meets_registered_minimum


def test_the_percentiles_carry_the_cadence_floor_that_bounds_them() -> None:
    report = build_report([obs(h, present=True, day=date(2025, 6, h)) for h in range(1, 21)])
    assert report.p50_hours is not None and report.p95_hours is not None
    assert report.p95_hours >= report.p90_hours >= report.p50_hours  # type: ignore[operator]
    assert report.cadence_floor_minutes == CONFIG.snapshot_peak_interval_minutes
