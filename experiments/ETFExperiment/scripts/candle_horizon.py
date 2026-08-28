"""A.1 Task 1: how far back does the venue serve 1h candles for the perp?

Reads `t`, `T` and row counts only. No price field is parsed anywhere on this
path; the blindness reader is structurally incapable of returning one.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime, timedelta

from etf.blindness import candle_times
from etf.clock import iso_z, now_utc, utc_ms
from etf.config import CONFIG
from etf.http import PacedClient
from etf.ledger.requests import RequestLedger
from etf.paths import REPORTS

REPORT = REPORTS / "stage_a1" / "candle_horizon_bisect.json"


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    client = PacedClient(RequestLedger())
    now = now_utc()
    rows: list[dict[str, object]] = []
    probes = [
        ("1h", 250),
        ("1h", 225),
        ("1h", 212),
        ("1h", 206),
        ("1h", 203),
        ("1d", 1200),
        ("1d", 1000),
        ("1h", 201),
    ]
    for interval, days_back in probes:
        start = now - timedelta(days=days_back)
        end = start + timedelta(days=7)
        response = client.post_json(
            CONFIG.hyperliquid_info_url,
            {
                "type": "candleSnapshot",
                "req": {
                    "coin": CONFIG.perp_coin,
                    "interval": interval,
                    "startTime": utc_ms(start),
                    "endTime": utc_ms(end),
                },
            },
            source="venue",
            endpoint="venue.candleSnapshot",
        )
        times = candle_times(response.body) if response.status == 200 else None
        entry = {
            "interval": interval,
            "days_back": days_back,
            "window_start_utc": iso_z(start),
            "http_status": response.status,
            "row_count": times.row_count if times else None,
            "first_open_utc": (
                datetime.fromtimestamp(times.open_ms[0] / 1000, UTC).isoformat()
                if times and times.open_ms
                else None
            ),
        }
        rows.append(entry)
        print(json.dumps(entry))
    REPORT.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
