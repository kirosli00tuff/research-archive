"""Readable-pair projection: when a pair becomes readable, and how many by when.

Pure arithmetic over entry timestamps, dates, and a measured accrual rate.
Nothing here opens a sealed store, parses a payload, or reads an outcome
value — it counts pairs and compares dates, and the guard tests pin that it
stays that way.

The one registered fact it encodes (ADR-019): a backfill pair's candle
window seals once, at **entry + 92 days**, so that is the day its 30-day
primary becomes readable. A forward birth's entry is its listing + 2 days,
so its pair is readable at **listing + 94 days**.

Extracted from `scripts/ktable_amended.py` at Amendment H2-5 so the tiered
projection and the amended one cannot drift apart in the arithmetic. The
Amendment H2-4 figures themselves are **quoted from the recorded artifact**
`reports/stage_a_h2/ktable_amended.json`, never recomputed — a recomputed
"superseded" number would not be the one the amendment recorded.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Final

from npl.clock import MS_PER_DAY

# ADR-019: the seal happens once, at entry + 92 days.
READABLE_LAG_DAYS: Final = 92
FORWARD_READABLE_LAG_DAYS: Final = 94
DAYS_PER_MONTH: Final = 30.44


def day_ms(day: date) -> int:
    """Midnight UTC of a calendar day, in milliseconds."""
    return int(datetime(day.year, day.month, day.day, tzinfo=UTC).timestamp() * 1000)


def readable_days(entry_ms_values: list[int]) -> list[int]:
    """The day each backfill pair becomes readable, ascending. Counts only."""
    return sorted(ms + READABLE_LAG_DAYS * MS_PER_DAY for ms in entry_ms_values)


def projected_pairs(
    readable: list[int], at: date, today: date, accrual_per_month: float, match_rate: float
) -> tuple[int, int, int]:
    """(backfill readable, forward readable, total) at a date. Counts only.

    Forward pairs are the measured accrual over the window that has had time
    to become readable, **times the measured match rate** — under a rule that
    excludes some events, events and pairs are not the same number.
    """
    if not 0.0 <= match_rate <= 1.0:
        raise ValueError(f"match_rate must be a share, got {match_rate}")
    cut = day_ms(at)
    backfill = sum(1 for ms in readable if ms <= cut)
    horizon_days = (at - today).days - FORWARD_READABLE_LAG_DAYS
    forward = max(0, int(accrual_per_month * match_rate * horizon_days / DAYS_PER_MONTH))
    return backfill, forward, backfill + forward


def first_date_reaching(
    readable: list[int],
    target: int,
    today: date,
    limit: date,
    accrual_per_month: float,
    match_rate: float,
) -> str | None:
    """The earliest day total readable pairs reaches the target, or None by `limit`."""
    day = today
    while day <= limit:
        if projected_pairs(readable, day, today, accrual_per_month, match_rate)[2] >= target:
            return day.isoformat()
        day += timedelta(days=1)
    return None


def month_ends(today: date, deadline: date) -> list[date]:
    """Each month end from this month through the deadline, inclusive."""
    out: list[date] = []
    cursor = date(today.year, today.month, 1)
    while cursor <= deadline:
        nxt = date(cursor.year + (cursor.month == 12), (cursor.month % 12) + 1, 1)
        out.append(min(nxt - timedelta(days=1), deadline))
        cursor = nxt
    return out
