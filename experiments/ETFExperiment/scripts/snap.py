"""A.1 Task 3: one flow capture, cadence-gated. Fired by etf-snap.timer.

The timer fires every 20 minutes. This script decides whether the registered
cadence asks for a capture now — every 20 minutes inside the 20:00 to 14:00 UTC
print-and-revision window, every 2 hours outside it — and records a skip as a
skip rather than as a failure.

A non-200 writes a loud marker to the ledger and is never read as end-of-print.
"""

from __future__ import annotations

import sys

from etf.cadence import interval_seconds
from etf.clock import iso_z, now_utc
from etf.guard import require_no_active_unit
from etf.http import PacedClient
from etf.ledger.append_only import AppendOnlyLedger
from etf.ledger.requests import RequestLedger
from etf.paths import SNAPSHOT_LEDGER
from etf.snapshot import capture

UNIT = "etf-snap.service"


def last_capture_epoch() -> float | None:
    from datetime import UTC, datetime

    rows = AppendOnlyLedger(SNAPSHOT_LEDGER).read().rows
    stamps: list[str] = [stamp for r in rows if isinstance(stamp := r.get("captured_at"), str)]
    if not stamps:
        return None
    latest = max(stamps)
    return datetime.strptime(latest, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).timestamp()


def main(argv: list[str]) -> int:
    scheduled = "--scheduled" in argv
    if not scheduled:
        require_no_active_unit(UNIT)
    now = now_utc()
    due = interval_seconds(now)
    last = last_capture_epoch()
    if last is not None and (now.timestamp() - last) < due - 60:
        waited = int(now.timestamp() - last)
        print(f"skip: {waited}s since the last capture, registered cadence asks {due}s")
        return 0
    snapshot = capture(PacedClient(RequestLedger()), now=now)
    open_day = snapshot.days[-1] if snapshot.days else None
    print(
        f"captured {iso_z(now)} http={snapshot.http_status} rows={len(snapshot.days)} "
        f"bytes={snapshot.byte_count} "
        f"open_day={open_day.trade_date if open_day else None} "
        f"open_signal={open_day.signal_usd if open_day else None}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
