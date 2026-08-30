"""The US equity regular-session calendar, built from a recorded rule source.

The rules encoded here are the **NYSE published holiday and early-closing
schedule**. They are recorded as rules rather than as a downloaded list so that
the calendar is reproducible without a vendor, and so that every session in the
registered window carries a **DST-aware Eastern anchor** rather than a date.

**Half sessions are excluded from the sample and counted** (Section 2). They are
generated here anyway, because a session that is excluded still has to be
well-formed to be excluded correctly.

This module reads **no price**. It is a symbol-free, value-free date substrate.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import date, timedelta
from enum import StrEnum, unique
from typing import Final, final

from orb.sessionclock import (
    close_exit_window_utc,
    evaluation_instant_utc,
    opening_range_window_utc,
    utc_offset_minutes,
)


@unique
class SessionKind(StrEnum):
    FULL = "full"
    HALF = "half"


@final
@dataclass(frozen=True, slots=True)
class Session:
    """One regular session, anchored to a DST-aware Eastern clock."""

    day: date
    kind: SessionKind

    @property
    def is_half(self) -> bool:
        return self.kind is SessionKind.HALF

    def opening_range_utc(self) -> tuple[int, int]:
        """The half-open ``[09:30, 09:35)`` Eastern window, in epoch ms."""
        start, end = opening_range_window_utc(self.day)
        return int(start.timestamp() * 1000), int(end.timestamp() * 1000)

    def evaluation_ms(self) -> int:
        """09:35:00 Eastern, in epoch ms."""
        return int(evaluation_instant_utc(self.day).timestamp() * 1000)

    def close_exit_utc(self) -> tuple[int, int]:
        start, end = close_exit_window_utc(self.day, half_session=self.is_half)
        return int(start.timestamp() * 1000), int(end.timestamp() * 1000)

    def utc_offset_minutes(self) -> int:
        return utc_offset_minutes(self.day)


# --- The recorded rule source ---------------------------------------------

UNSCHEDULED_CLOSURES: Final[dict[date, str]] = {
    date(2018, 12, 5): "national day of mourning, George H. W. Bush",
    date(2025, 1, 9): "national day of mourning, Jimmy Carter",
}
"""Unscheduled full-day closures inside 2016-01-04 to 2026-06-30, with reasons.

Recorded as data because they are events, not rules; a rule cannot predict a
state funeral. Each is dated and reasoned so a later disagreement with a second
source is auditable rather than mysterious.
"""

JUNETEENTH_FIRST_OBSERVED_YEAR: Final[int] = 2022
"""Juneteenth became an NYSE holiday in 2022. Before that it was a full session."""


def _easter(year: int) -> date:
    """Gregorian Easter Sunday, by the anonymous algorithm."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    lam = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * lam) // 451
    month, day = divmod(h + lam - 7 * m + 114, 31)
    return date(year, month, day + 1)


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    """The ``n``-th ``weekday`` of a month. Monday is 0."""
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return first + timedelta(days=offset + 7 * (n - 1))


def _last_weekday(year: int, month: int, weekday: int) -> date:
    """The last ``weekday`` of a month."""
    last_day = (
        (date(year, month + 1, 1) - timedelta(days=1))
        if month < 12
        else date(year, 12, 31)
    )
    offset = (last_day.weekday() - weekday) % 7
    return last_day - timedelta(days=offset)


def _observed(day: date) -> date | None:
    """NYSE observation rule: Saturday shifts back, Sunday shifts forward.

    A holiday observed on the Saturday of a weekend is taken on the preceding
    Friday; on a Sunday, the following Monday. Returns None where the shift
    would land outside the holiday's own year, which cannot happen for any
    holiday in this set but is refused rather than assumed.
    """
    if day.weekday() == 5:
        return day - timedelta(days=1)
    if day.weekday() == 6:
        return day + timedelta(days=1)
    return day


def full_day_holidays(year: int) -> dict[date, str]:
    """Every scheduled NYSE full-day closure in ``year``, with its name."""
    out: dict[date, str] = {}

    def add(day: date | None, name: str) -> None:
        if day is not None and day.year == year:
            out[day] = name

    add(_observed(date(year, 1, 1)), "New Year's Day")
    add(_nth_weekday(year, 1, 0, 3), "Martin Luther King Jr. Day")
    add(_nth_weekday(year, 2, 0, 3), "Washington's Birthday")
    add(_easter(year) - timedelta(days=2), "Good Friday")
    add(_last_weekday(year, 5, 0), "Memorial Day")
    if year >= JUNETEENTH_FIRST_OBSERVED_YEAR:
        add(_observed(date(year, 6, 19)), "Juneteenth National Independence Day")
    add(_observed(date(year, 7, 4)), "Independence Day")
    add(_nth_weekday(year, 9, 0, 1), "Labor Day")
    add(_nth_weekday(year, 11, 3, 4), "Thanksgiving Day")
    add(_observed(date(year, 12, 25)), "Christmas Day")

    for day, reason in UNSCHEDULED_CLOSURES.items():
        if day.year == year:
            out[day] = reason
    return out


def early_closes(year: int) -> dict[date, str]:
    """Every scheduled NYSE 13:00 Eastern early close in ``year``.

    Three rules, as published: the day after Thanksgiving; Christmas Eve when it
    falls on a weekday and is not itself a closure; and 3 July when it falls on
    a weekday and 4 July is a full weekday session.
    """
    out: dict[date, str] = {}
    holidays = full_day_holidays(year)

    friday_after_thanksgiving = _nth_weekday(year, 11, 3, 4) + timedelta(days=1)
    if friday_after_thanksgiving not in holidays:
        out[friday_after_thanksgiving] = "day after Thanksgiving"

    christmas_eve = date(year, 12, 24)
    if christmas_eve.weekday() < 5 and christmas_eve not in holidays:
        out[christmas_eve] = "Christmas Eve"

    july_third = date(year, 7, 3)
    if july_third.weekday() < 5 and july_third not in holidays:
        out[july_third] = "3 July"

    return out


def sessions(start: date, end: date) -> Iterator[Session]:
    """Every regular session in ``[start, end]`` inclusive, in date order."""
    holidays: dict[int, dict[date, str]] = {}
    earlies: dict[int, dict[date, str]] = {}
    day = start
    while day <= end:
        if day.year not in holidays:
            holidays[day.year] = full_day_holidays(day.year)
            earlies[day.year] = early_closes(day.year)
        if day.weekday() < 5 and day not in holidays[day.year]:
            kind = SessionKind.HALF if day in earlies[day.year] else SessionKind.FULL
            yield Session(day, kind)
        day += timedelta(days=1)


def session_counts(start: date, end: date) -> dict[int, tuple[int, int]]:
    """Per calendar year: (total sessions, half sessions)."""
    counts: dict[int, tuple[int, int]] = {}
    for session in sessions(start, end):
        total, half = counts.get(session.day.year, (0, 0))
        counts[session.day.year] = (total + 1, half + (1 if session.is_half else 0))
    return counts
