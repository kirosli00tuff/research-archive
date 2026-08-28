"""The daily pass, fired by etf-daily.timer at 12:20 UTC.

Order matters and is registered (solattn ADR-019 part 2): the seal runs first,
so it lands within a minute of the timer fire rather than after a multi-hour
fetch, and a failed attestation stops the pass loudly before anything else
runs.

1. Seal yesterday, now closed and final. Never the open day.
2. Refresh the full-history page and record a revision row for any closed day
   whose value moved since the last capture, with both values and both capture
   timestamps.
3. Record and seal the outcome substrate for each day whose hold window has
   completed and is not yet sealed.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, date, timedelta

from etf.absence import Absent
from etf.clock import iso_z, now_utc
from etf.config import CONFIG
from etf.guard import require_no_active_unit
from etf.http import PacedClient
from etf.ledger.append_only import AppendOnlyLedger
from etf.ledger.requests import RequestLedger
from etf.manifest import seal_day
from etf.paths import OUTCOMES_DIR, RETRO_DIR, SNAPSHOT_LEDGER
from etf.recorder import record_day
from etf.snapshot import capture

UNIT = "etf-daily.service"
REVISION_LEDGER = RETRO_DIR / "revisions.jsonl"


def main(argv: list[str]) -> int:
    scheduled = "--scheduled" in argv
    if not scheduled:
        require_no_active_unit(UNIT)
    now = now_utc()
    yesterday = now.astimezone(UTC).date() - timedelta(days=1)

    # 1. Seal first, loudly.
    snap_ledger = AppendOnlyLedger(SNAPSHOT_LEDGER)
    rows = snap_ledger.require_intact()
    captures = [r for r in rows if str(r.get("captured_at", "")).startswith(yesterday.isoformat())]
    manifest = seal_day(yesterday, captures, now=now)
    print(
        f"sealed {manifest.day} captures={manifest.capture_count} "
        f"digest={manifest.capture_digest[:12]}"
    )

    client = PacedClient(RequestLedger())

    # 2. Full history, and a revision row for any closed day whose value moved.
    previous: dict[str, float] = {}
    for row in rows:
        if str(row.get("url")) != CONFIG.flow_all_data_url:
            continue
        for day in row.get("days", []):
            value = day.get("signal_usd")
            if isinstance(value, int | float):
                previous[str(day["date"])] = float(value)

    snapshot = capture(client, now=now, url=CONFIG.flow_all_data_url)
    revisions = AppendOnlyLedger(REVISION_LEDGER)
    moved = 0
    open_day = now.astimezone(UTC).date()
    for day in snapshot.days:
        if day.trade_date >= open_day:
            continue  # never seal or diff the open day
        if isinstance(day.signal_usd, Absent):
            continue
        before = previous.get(day.trade_date.isoformat())
        if before is not None and before != day.signal_usd:
            revisions.append(
                {
                    "trade_date": day.trade_date.isoformat(),
                    "previous_usd": before,
                    "current_usd": day.signal_usd,
                    "delta_usd": day.signal_usd - before,
                    "observed_at": iso_z(now),
                }
            )
            moved += 1
    print(f"full history rows={len(snapshot.days)} revisions_appended={moved}")

    # 3. Seal completed hold windows not yet on disk.
    sealed = 0
    for day in snapshot.days:
        if isinstance(day.signal_usd, Absent):
            continue
        if day.trade_date < date.fromisoformat(CONFIG.oos_start_date):
            continue
        if (OUTCOMES_DIR / f"btc-1h-{day.trade_date.isoformat()}.json").exists():
            continue
        anchor_end = day.trade_date + timedelta(days=2)
        if anchor_end >= open_day:
            continue  # the hold window has not completed
        coverage = record_day(client, day.trade_date)
        if coverage.candle_rows or coverage.funding_rows:
            sealed += 1
            print(
                json.dumps(
                    {
                        "day": coverage.trade_date.isoformat(),
                        "candles": coverage.candle_rows,
                        "funding": coverage.funding_rows,
                        "expected": coverage.candle_expected,
                        "covered": coverage.covered,
                    }
                )
            )
    print(f"sealed hold windows this pass: {sealed}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
