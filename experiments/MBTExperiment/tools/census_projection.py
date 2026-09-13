#!/usr/bin/env python3
"""Project the census completion date from the registered distinctness rule.

The census is **clock-bound, not effort-bound**. The rule registered in
REGISTRATION.md Section 3.5 caps windows at 4 per UTC calendar day and requires
60 minutes between them, so 20 windows need 5 collection days and no amount of
effort compresses that.

CME crypto futures and options trade Sunday 17:00 CT to Friday 16:00 CT with a
daily halt, so a **UTC** collection day is Monday through Friday. Saturday and
Sunday UTC are not collection days: Sunday's CT open falls on Monday UTC.

This computes the completion date from a start date rather than hard-coding one,
because the start is not known while the Gateway is down and a hard-coded date
would silently go stale.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

MIN_OBSERVATION_WINDOWS = 20
MAX_WINDOWS_PER_UTC_DAY = 4
MIN_MINUTES_BETWEEN_WINDOWS = 60

#: Monday is 0. Saturday and Sunday are not CME crypto collection days in UTC.
_WEEKEND = {5, 6}


def is_collection_day(day: date) -> bool:
    return day.weekday() not in _WEEKEND


def collection_days(start: date, count: int) -> list[date]:
    """The first ``count`` CME crypto collection days on or after ``start``."""
    days: list[date] = []
    cursor = start
    while len(days) < count:
        if is_collection_day(cursor):
            days.append(cursor)
        cursor += timedelta(days=1)
    return days


def project(start: date) -> dict[str, object]:
    needed = -(-MIN_OBSERVATION_WINDOWS // MAX_WINDOWS_PER_UTC_DAY)  # ceiling division
    days = collection_days(start, needed)
    return {
        "windows_required": MIN_OBSERVATION_WINDOWS,
        "max_windows_per_utc_day": MAX_WINDOWS_PER_UTC_DAY,
        "min_minutes_between_windows": MIN_MINUTES_BETWEEN_WINDOWS,
        "collection_days_required": needed,
        "first_collection_day": days[0].isoformat(),
        "collection_days": [f"{d.isoformat()} {d.strftime('%A')}" for d in days],
        "projected_completion_utc": days[-1].isoformat(),
        "elapsed_calendar_days": (days[-1] - days[0]).days + 1,
        "note": (
            "Clock-bound and not compressible. The rule fixes the DURATION at "
            f"{needed} collection days; it does not fix the start. The start is "
            "the first day a Gateway session exists."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default="", help="first collection day, YYYY-MM-DD, UTC")
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    start = date.fromisoformat(args.start) if args.start else datetime.now(tz=UTC).date()
    payload = project(start)
    payload["start_requested"] = start.isoformat()
    payload["start_was_a_collection_day"] = is_collection_day(start)

    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.out:
        out = REPO / args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
