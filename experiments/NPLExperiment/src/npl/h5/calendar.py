"""The registered US equity-market calendar and session tagger (H5 Section 5).

**Written before any snapshot was collected.** Every H5 observation carries
exactly one of four session tags, computed from the observation's UTC
timestamp against this calendar in `America/New_York`:

- ``regular``        — a trading day, 09:30 up to the day's close
                       (16:00, or 13:00 on a registered early-close day)
- ``extended``       — a trading day, 04:00 to 09:30 and close to 20:00
                       (close to 17:00 on an early-close day)
- ``closed_weekday`` — Monday to Friday outside those windows, and the whole
                       of a registered full holiday
- ``weekend``        — Saturday or Sunday in New York

The holiday and early-close tables are the NYSE calendar for 2024 through
2027, written out by date rather than derived, so a rule change in a later
year is an amendment and not a silent recomputation. A timestamp in a year
this table does not cover is a **loud refusal**, never a default to "open".
"""

from __future__ import annotations

from datetime import date, datetime, time
from typing import Final
from zoneinfo import ZoneInfo

EXCHANGE_TZ: Final = ZoneInfo("America/New_York")

TAG_REGULAR: Final = "regular"
TAG_EXTENDED: Final = "extended"
TAG_CLOSED_WEEKDAY: Final = "closed_weekday"
TAG_WEEKEND: Final = "weekend"

SESSION_TAGS: Final[tuple[str, ...]] = (
    TAG_REGULAR,
    TAG_EXTENDED,
    TAG_CLOSED_WEEKDAY,
    TAG_WEEKEND,
)

PREMARKET_OPEN: Final = time(4, 0)
REGULAR_OPEN: Final = time(9, 30)
REGULAR_CLOSE: Final = time(16, 0)
EARLY_CLOSE: Final = time(13, 0)
POSTMARKET_CLOSE: Final = time(20, 0)
EARLY_POSTMARKET_CLOSE: Final = time(17, 0)

# NYSE full closures. Written out; not derived.
HOLIDAYS: Final[frozenset[date]] = frozenset(
    {
        # 2024
        date(2024, 1, 1),
        date(2024, 1, 15),
        date(2024, 2, 19),
        date(2024, 3, 29),
        date(2024, 5, 27),
        date(2024, 6, 19),
        date(2024, 7, 4),
        date(2024, 9, 2),
        date(2024, 11, 28),
        date(2024, 12, 25),
        # 2025
        date(2025, 1, 1),
        date(2025, 1, 9),
        date(2025, 1, 20),
        date(2025, 2, 17),
        date(2025, 4, 18),
        date(2025, 5, 26),
        date(2025, 6, 19),
        date(2025, 7, 4),
        date(2025, 9, 1),
        date(2025, 11, 27),
        date(2025, 12, 25),
        # 2026
        date(2026, 1, 1),
        date(2026, 1, 19),
        date(2026, 2, 16),
        date(2026, 4, 3),
        date(2026, 5, 25),
        date(2026, 6, 19),
        date(2026, 7, 3),
        date(2026, 9, 7),
        date(2026, 11, 26),
        date(2026, 12, 25),
        # 2027
        date(2027, 1, 1),
        date(2027, 1, 18),
        date(2027, 2, 15),
        date(2027, 3, 26),
        date(2027, 5, 31),
        date(2027, 6, 18),
        date(2027, 7, 5),
        date(2027, 9, 6),
        date(2027, 11, 25),
        date(2027, 12, 24),
    }
)

# 13:00 ET closes.
EARLY_CLOSES: Final[frozenset[date]] = frozenset(
    {
        date(2024, 7, 3),
        date(2024, 11, 29),
        date(2024, 12, 24),
        date(2025, 7, 3),
        date(2025, 11, 28),
        date(2025, 12, 24),
        date(2026, 11, 27),
        date(2026, 12, 24),
        date(2027, 11, 26),
    }
)

COVERED_YEARS: Final[frozenset[int]] = frozenset({2024, 2025, 2026, 2027})

SATURDAY: Final = 5


class CalendarOutOfRange(RuntimeError):
    """A timestamp fell outside the registered calendar years. Loud, never open."""


def _local(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        raise ValueError("refusing a naive datetime; every H5 timestamp is UTC-aware")
    return moment.astimezone(EXCHANGE_TZ)


def is_holiday(day: date) -> bool:
    return day in HOLIDAYS


def is_early_close(day: date) -> bool:
    return day in EARLY_CLOSES


def is_weekend(day: date) -> bool:
    """Saturday and Sunday. The boundary is `>= SATURDAY`, and it is pinned."""
    return day.weekday() >= SATURDAY


def is_trading_day(day: date) -> bool:
    return not is_weekend(day) and not is_holiday(day)


def close_time(day: date) -> time:
    return EARLY_CLOSE if is_early_close(day) else REGULAR_CLOSE


def post_close_time(day: date) -> time:
    return EARLY_POSTMARKET_CLOSE if is_early_close(day) else POSTMARKET_CLOSE


def session_tag(moment: datetime) -> str:
    """The registered session tag for one UTC-aware instant."""
    local = _local(moment)
    if local.year not in COVERED_YEARS:
        raise CalendarOutOfRange(
            f"{local.date()} lies outside the registered calendar years "
            f"{sorted(COVERED_YEARS)}. The tagger refuses rather than assuming a "
            f"session; extend the table by amendment."
        )
    day = local.date()
    if is_weekend(day):
        return TAG_WEEKEND
    if is_holiday(day):
        return TAG_CLOSED_WEEKDAY
    clock = local.time()
    if REGULAR_OPEN <= clock < close_time(day):
        return TAG_REGULAR
    if PREMARKET_OPEN <= clock < REGULAR_OPEN:
        return TAG_EXTENDED
    if close_time(day) <= clock < post_close_time(day):
        return TAG_EXTENDED
    return TAG_CLOSED_WEEKDAY


def session_tag_of_ms(ms: int) -> str:
    """The session tag for a millisecond UTC epoch stamp."""
    from npl.clock import ms_to_utc

    return session_tag(ms_to_utc(ms))
