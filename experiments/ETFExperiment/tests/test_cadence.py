"""The registered snapshot cadence, including the midnight wrap."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from etf.cadence import in_peak_window, interval_seconds
from etf.config import CONFIG


def _at(hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 8, 28, hour, minute, tzinfo=UTC)


def test_the_peak_window_wraps_midnight() -> None:
    assert in_peak_window(_at(20))
    assert in_peak_window(_at(23))
    assert in_peak_window(_at(0))
    assert in_peak_window(_at(13))


def test_the_window_edges_sit_exactly_on_the_registered_hours() -> None:
    assert in_peak_window(_at(CONFIG.snapshot_peak_start_hour_utc))
    assert not in_peak_window(_at(CONFIG.snapshot_peak_start_hour_utc - 1))
    assert not in_peak_window(_at(CONFIG.snapshot_peak_end_hour_utc))
    assert in_peak_window(_at(CONFIG.snapshot_peak_end_hour_utc - 1, 59))


def test_the_intervals_are_the_registered_twenty_minutes_and_two_hours() -> None:
    assert interval_seconds(_at(2)) == 20 * 60
    assert interval_seconds(_at(16)) == 2 * 3600


def test_a_naive_datetime_is_refused() -> None:
    with pytest.raises(ValueError, match="naive"):
        in_peak_window(datetime(2026, 8, 28, 2, 0))
