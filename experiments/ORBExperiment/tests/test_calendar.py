"""The session calendar, and the internal cross-checks that stand in for a
second source until one is reachable.

The registered window is 2016-01-04 to 2026-06-30. Every session carries a
DST-aware Eastern anchor, and the tests below check the anchor moves across
both transitions rather than trusting that it does.
"""

from __future__ import annotations

from datetime import date, timedelta

from orb.calendar import (
    JUNETEENTH_FIRST_OBSERVED_YEAR,
    UNSCHEDULED_CLOSURES,
    SessionKind,
    early_closes,
    full_day_holidays,
    session_counts,
    sessions,
)

WINDOW_START = date(2016, 1, 4)
WINDOW_END = date(2026, 6, 30)


def _weekdays(year: int) -> int:
    day, count = date(year, 1, 1), 0
    while day.year == year:
        if day.weekday() < 5:
            count += 1
        day += timedelta(days=1)
    return count


# --- Internal cross-check: two independent derivations must agree ---------


def test_session_count_equals_weekdays_minus_weekday_closures() -> None:
    """A second derivation of the same number, from different arithmetic."""
    counts = session_counts(date(2016, 1, 1), date(2025, 12, 31))
    for year in range(2016, 2026):
        holidays = full_day_holidays(year)
        weekday_closures = sum(1 for d in holidays if d.weekday() < 5)
        derived = _weekdays(year) - weekday_closures
        assert counts[year][0] == derived, (year, counts[year][0], derived)


def test_no_session_falls_on_a_weekend_or_a_closure() -> None:
    for session in sessions(WINDOW_START, WINDOW_END):
        assert session.day.weekday() < 5, session.day
        assert session.day not in full_day_holidays(session.day.year), session.day


def test_every_half_session_is_also_a_session() -> None:
    by_day = {s.day: s for s in sessions(WINDOW_START, WINDOW_END)}
    for year in range(2016, 2027):
        for day in early_closes(year):
            if WINDOW_START <= day <= WINDOW_END and day.weekday() < 5:
                assert day in by_day, day
                assert by_day[day].kind is SessionKind.HALF, day


# --- The registered window ------------------------------------------------


def test_the_in_sample_window_holds_1762_sessions() -> None:
    """Computed. The registration's ~1,760 is an approximation; this is the count."""
    n = sum(1 for _ in sessions(date(2016, 1, 4), date(2022, 12, 30)))
    assert n == 1762, n


def test_the_holdout_window_holds_875_sessions() -> None:
    """Computed 875 against the registration's stated ~880. Recorded, not reconciled."""
    n = sum(1 for _ in sessions(date(2023, 1, 3), date(2026, 6, 30)))
    assert n == 875, n


def test_the_full_window_totals_2637_sessions_with_21_half_sessions() -> None:
    counts = session_counts(WINDOW_START, WINDOW_END)
    total = sum(c for c, _ in counts.values())
    half = sum(h for _, h in counts.values())
    assert total == 2637, total
    assert half == 21, half


# --- Named rules, pinned on the dates that exercise them ------------------


def test_juneteenth_is_a_holiday_from_2022_and_not_before() -> None:
    assert date(2021, 6, 18) not in full_day_holidays(2021)
    assert date(2021, 6, 21) not in full_day_holidays(2021)
    observed = full_day_holidays(JUNETEENTH_FIRST_OBSERVED_YEAR)
    assert date(2022, 6, 20) in observed  # 19 June 2022 was a Sunday
    assert observed[date(2022, 6, 20)].startswith("Juneteenth")


def test_a_saturday_holiday_is_observed_on_the_friday_before() -> None:
    """4 July 2020 was a Saturday; the NYSE closed Friday 3 July."""
    holidays = full_day_holidays(2020)
    assert date(2020, 7, 3) in holidays
    assert date(2020, 7, 6) not in holidays


def test_a_sunday_holiday_is_observed_on_the_monday_after() -> None:
    """1 January 2023 was a Sunday; the NYSE closed Monday 2 January."""
    assert date(2023, 1, 2) in full_day_holidays(2023)


def test_good_friday_is_computed_not_listed() -> None:
    for year, expected in (
        (2016, date(2016, 3, 25)),
        (2018, date(2018, 3, 30)),
        (2024, date(2024, 3, 29)),
        (2026, date(2026, 4, 3)),
    ):
        assert expected in full_day_holidays(year), (year, expected)


def test_both_unscheduled_closures_are_recorded_with_reasons() -> None:
    """A rule cannot predict a state funeral, so these are data, dated and reasoned."""
    assert len(UNSCHEDULED_CLOSURES) == 2
    assert date(2018, 12, 5) in UNSCHEDULED_CLOSURES
    assert date(2025, 1, 9) in UNSCHEDULED_CLOSURES
    for reason in UNSCHEDULED_CLOSURES.values():
        assert "mourning" in reason


def test_the_2018_closure_removes_exactly_one_session() -> None:
    """2018: 261 weekdays, 10 weekday closures, 251 sessions. Hand-computed."""
    assert _weekdays(2018) == 261
    holidays = full_day_holidays(2018)
    assert sum(1 for d in holidays if d.weekday() < 5) == 10
    assert session_counts(date(2018, 1, 1), date(2018, 12, 31))[2018][0] == 251


def test_christmas_eve_is_a_half_session_only_on_a_weekday() -> None:
    assert date(2021, 12, 24) not in early_closes(2021)  # observed Christmas Day
    assert date(2024, 12, 24) in early_closes(2024)  # a Tuesday
    assert date(2022, 12, 24) not in early_closes(2022)  # a Saturday


def test_the_day_after_thanksgiving_is_always_a_half_session() -> None:
    for year in range(2016, 2027):
        assert any("Thanksgiving" in r for r in early_closes(year).values()), year


# --- The DST-aware anchor -------------------------------------------------


def test_the_eastern_offset_moves_across_both_transitions() -> None:
    """The whole point of Guard 7, exercised on real sessions."""
    by_day = {s.day: s for s in sessions(WINDOW_START, WINDOW_END)}
    assert by_day[date(2016, 3, 10)].utc_offset_minutes() == -300
    assert by_day[date(2016, 3, 14)].utc_offset_minutes() == -240
    assert by_day[date(2016, 11, 4)].utc_offset_minutes() == -240
    assert by_day[date(2016, 11, 7)].utc_offset_minutes() == -300


def test_the_opening_range_is_five_minutes_wide_in_both_dst_regimes() -> None:
    by_day = {s.day: s for s in sessions(WINDOW_START, WINDOW_END)}
    for day in (date(2016, 1, 4), date(2016, 7, 5)):
        start, end = by_day[day].opening_range_utc()
        assert end - start == 5 * 60 * 1000, day
        assert by_day[day].evaluation_ms() == end, day


def test_a_full_and_a_half_session_differ_by_three_hours_at_the_exit() -> None:
    """Compared on the **same** date, so the 24-hour day gap cannot confound it."""
    from orb.sessionclock import close_exit_window_utc

    by_day = {s.day: s for s in sessions(WINDOW_START, WINDOW_END)}
    assert by_day[date(2024, 12, 23)].kind is SessionKind.FULL
    assert by_day[date(2024, 12, 24)].kind is SessionKind.HALF

    day = date(2024, 12, 24)
    full_start, _ = close_exit_window_utc(day, half_session=False)
    half_start, _ = close_exit_window_utc(day, half_session=True)
    assert (full_start - half_start).total_seconds() == 3 * 60 * 60

    # And the half session this calendar actually generates uses the shifted window.
    assert by_day[day].close_exit_utc()[0] == int(half_start.timestamp() * 1000)


def test_the_first_in_sample_session_anchors_to_the_carve_out_boundary() -> None:
    """The registered boundary is 09:30 Eastern on the first in-sample session."""
    from orb.config import CONFIG

    first = next(iter(sessions(date(2016, 1, 4), date(2016, 1, 4))))
    assert first.opening_range_utc()[0] == CONFIG.pre_period_end_ms
