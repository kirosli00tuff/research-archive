"""Section 3: the anchor, strict admissibility, and the single permitted amendment."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from etf.anchor import (
    amended_anchor_hour,
    entry_anchor,
    is_admissible_capture,
    out_of_sample_start,
    percentile,
)
from etf.config import CONFIG

D = date(2025, 6, 2)


def test_the_out_of_sample_window_starts_at_the_registered_date() -> None:
    assert out_of_sample_start() == date(2025, 5, 1)


def test_the_anchor_is_eight_utc_on_the_day_after_the_trading_day() -> None:
    assert entry_anchor(D) == datetime(2025, 6, 3, 8, 0, tzinfo=UTC)


def test_a_capture_one_second_before_the_anchor_qualifies() -> None:
    assert is_admissible_capture(datetime(2025, 6, 3, 7, 59, 59, tzinfo=UTC), D)


def test_a_capture_exactly_on_the_anchor_does_not_qualify() -> None:
    """Strictly before, and the fixture sits exactly on the boundary."""
    assert not is_admissible_capture(datetime(2025, 6, 3, 8, 0, 0, tzinfo=UTC), D)


def test_a_naive_capture_timestamp_is_refused() -> None:
    with pytest.raises(ValueError, match="naive"):
        is_admissible_capture(datetime(2025, 6, 3, 7, 0), D)


def test_the_percentile_is_nearest_rank_and_deterministic() -> None:
    assert percentile([1.0, 2.0, 3.0, 4.0], 0.95) == 4.0
    assert percentile([1.0, 2.0, 3.0, 4.0], 0.5) == 2.0
    with pytest.raises(ValueError, match="empty sample"):
        percentile([], 0.95)


def test_the_anchor_holds_when_the_measured_p95_lands_at_the_trigger_hour() -> None:
    """Exactly on 07:00: the rule says 'later than 07:00', so 07:00 does not move it."""
    hours = [6.0] * 18 + [float(CONFIG.anchor_amendment_trigger_hour_utc)] * 2
    assert percentile(hours, 0.95) == 7.0
    assert amended_anchor_hour(hours) == CONFIG.entry_anchor_hour_utc


def test_the_anchor_moves_to_the_next_whole_hour_after_a_late_p95() -> None:
    hours = [6.0] * 18 + [9.25, 9.25]
    assert amended_anchor_hour(hours) == 10


def test_a_p95_exactly_on_a_whole_hour_moves_to_the_next_one() -> None:
    hours = [6.0] * 18 + [9.0, 9.0]
    assert amended_anchor_hour(hours) == 10
