"""Calendar-time membership. One book per session, one position per name."""

from __future__ import annotations

from insider.config import CONFIG
from insider.portfolio.membership import Event, build, entry_session_for

SESSIONS = [f"2020-01-{d:02d}" for d in range(1, 21)]


def test_entry_is_the_first_session_strictly_after_the_filing() -> None:
    assert entry_session_for(SESSIONS, "2020-01-05") == "2020-01-06"
    assert entry_session_for(SESSIONS, "2020-01-04") == "2020-01-05"


def test_a_filing_past_the_last_session_has_no_entry_rather_than_a_substituted_one() -> None:
    assert entry_session_for(SESSIONS, "2020-01-20") is None
    assert entry_session_for(SESSIONS, "2021-06-01") is None


def test_the_registered_entry_lag_is_one_session() -> None:
    assert CONFIG.entry_lag_sessions == 1


def test_a_name_is_held_for_exactly_the_hold() -> None:
    series = build([Event("AAA", "2020-01-05")], SESSIONS, 3)
    held = [d for d, b in zip(series.sessions, series.book, strict=True) if b]
    assert held == ["2020-01-05", "2020-01-06", "2020-01-07"]


def test_two_events_in_one_name_are_one_position() -> None:
    series = build([Event("AAA", "2020-01-05"), Event("AAA", "2020-01-06")], SESSIONS, 3)
    assert max(series.widths) == 1, "the portfolio holds one position per name"


def test_two_events_in_two_names_widen_the_book() -> None:
    series = build([Event("AAA", "2020-01-05"), Event("BBB", "2020-01-05")], SESSIONS, 3)
    assert max(series.widths) == 2


def test_a_hold_running_past_the_last_session_is_truncated_not_extended() -> None:
    series = build([Event("AAA", "2020-01-19")], SESSIONS, 100)
    assert series.non_empty_sessions == 2


def test_coverage_and_width_are_separate_facts() -> None:
    series = build([Event("AAA", "2020-01-05"), Event("BBB", "2020-01-05")], SESSIONS, 2)
    assert series.non_empty_sessions == 2
    assert series.coverage() == 2 / len(SESSIONS)
    assert series.mean_width() == 2.0, "width averages over sessions that carry a book"


def test_an_event_whose_entry_is_not_a_session_is_dropped_not_shifted() -> None:
    series = build([Event("AAA", "1999-01-01")], SESSIONS, 3)
    assert series.non_empty_sessions == 0
