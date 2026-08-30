"""Guard 7 — the session clock. DST-aware Eastern, never a fixed UTC offset.

The measurement this pins: 09:30 Eastern is 13:30 UTC in summer and 14:30 UTC
in winter. A fixed offset takes the range from the wrong five minutes on
roughly a third of any multi-year sample, and does it silently.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta, timezone

import pytest

from orb.sessionclock import (
    EASTERN,
    FixedOffsetEasternError,
    NaiveDatetimeError,
    close_exit_window_utc,
    evaluation_instant_utc,
    is_daylight_time,
    opening_range_window_utc,
    require_aware,
    require_dst_aware_eastern,
    session_open_utc,
    to_utc,
    utc_offset_minutes,
)

WINTER = date(2016, 1, 4)
SUMMER = date(2016, 7, 5)
DST_START_2016 = date(2016, 3, 13)
DST_END_2016 = date(2016, 11, 6)


def test_winter_open_is_1430z() -> None:
    assert session_open_utc(WINTER) == datetime(2016, 1, 4, 14, 30, tzinfo=UTC)
    assert utc_offset_minutes(WINTER) == -300
    assert not is_daylight_time(WINTER)


def test_summer_open_is_1330z() -> None:
    assert session_open_utc(SUMMER) == datetime(2016, 7, 5, 13, 30, tzinfo=UTC)
    assert utc_offset_minutes(SUMMER) == -240
    assert is_daylight_time(SUMMER)


def test_the_offset_actually_moves_across_the_dst_transitions() -> None:
    """A fixed offset would make these four assertions impossible to satisfy."""
    assert utc_offset_minutes(DST_START_2016 - timedelta(days=1)) == -300
    assert utc_offset_minutes(DST_START_2016) == -240
    assert utc_offset_minutes(DST_END_2016 - timedelta(days=1)) == -240
    assert utc_offset_minutes(DST_END_2016) == -300


def test_the_summer_and_winter_opens_differ_by_exactly_one_hour_of_utc() -> None:
    """The whole guard in one line: same wall clock, different UTC instant."""
    winter = session_open_utc(WINTER).time()
    summer = session_open_utc(SUMMER).time()
    assert winter == time(14, 30)
    assert summer == time(13, 30)


def test_the_opening_range_window_is_half_open_and_five_minutes_wide() -> None:
    start, end = opening_range_window_utc(WINTER)
    assert start == datetime(2016, 1, 4, 14, 30, tzinfo=UTC)
    assert end == datetime(2016, 1, 4, 14, 35, tzinfo=UTC)
    assert end - start == timedelta(minutes=5)


def test_evaluation_sits_exactly_on_0935_eastern() -> None:
    """Section 2 evaluates at 09:35:00 Eastern. The fixture sits on it."""
    assert evaluation_instant_utc(WINTER) == datetime(2016, 1, 4, 14, 35, tzinfo=UTC)
    assert evaluation_instant_utc(SUMMER) == datetime(2016, 7, 5, 13, 35, tzinfo=UTC)
    _, range_end = opening_range_window_utc(SUMMER)
    assert range_end == evaluation_instant_utc(SUMMER)


def test_the_close_exit_window_is_1555_to_1559_eastern() -> None:
    start, end = close_exit_window_utc(WINTER)
    assert start == datetime(2016, 1, 4, 20, 55, tzinfo=UTC)
    assert end == datetime(2016, 1, 4, 20, 59, tzinfo=UTC)


def test_a_half_session_shifts_the_exit_window_three_hours() -> None:
    start, end = close_exit_window_utc(WINTER, half_session=True)
    assert start == datetime(2016, 1, 4, 17, 55, tzinfo=UTC)
    assert end == datetime(2016, 1, 4, 17, 59, tzinfo=UTC)


def test_a_naive_datetime_is_refused() -> None:
    with pytest.raises(NaiveDatetimeError):
        require_aware(datetime(2016, 1, 4, 9, 30), "probe")
    with pytest.raises(NaiveDatetimeError):
        to_utc(datetime(2016, 1, 4, 9, 30))


def test_an_aware_datetime_passes() -> None:
    moment = datetime(2016, 1, 4, 14, 30, tzinfo=UTC)
    assert require_aware(moment, "probe") is moment


def test_a_fixed_offset_eastern_is_refused() -> None:
    """The mutation this exists to catch: -05:00 hardcoded as 'Eastern'."""
    fixed = datetime(2016, 7, 5, 9, 30, tzinfo=timezone(timedelta(hours=-5)))
    with pytest.raises(FixedOffsetEasternError, match="DST-aware"):
        require_dst_aware_eastern(fixed, "probe")


def test_a_different_zone_is_refused() -> None:
    from zoneinfo import ZoneInfo

    chicago = datetime(2016, 7, 5, 8, 30, tzinfo=ZoneInfo("America/Chicago"))
    with pytest.raises(FixedOffsetEasternError, match="America/New_York"):
        require_dst_aware_eastern(chicago, "probe")


def test_a_dst_aware_eastern_instant_passes() -> None:
    moment = datetime(2016, 7, 5, 9, 30, tzinfo=EASTERN)
    assert require_dst_aware_eastern(moment, "probe") is moment


def test_a_fixed_offset_would_mis_slice_a_third_of_the_sample() -> None:
    """The cost of the bug, measured on the registered window rather than asserted.

    Counts the calendar days of 2016-01-04 to 2026-06-30 on which a fixed
    -05:00 offset resolves 09:30 Eastern to the wrong UTC instant.
    """
    start, end = date(2016, 1, 4), date(2026, 6, 30)
    total = (end - start).days + 1
    wrong = sum(
        1 for i in range(total) if utc_offset_minutes(start + timedelta(days=i)) != -300
    )
    share = wrong / total
    assert 0.30 < share < 0.70, f"{wrong} of {total} days = {share:.3f}"
    assert share > 1 / 3, f"n = {total} days, mis-sliced share {share:.3f}"
