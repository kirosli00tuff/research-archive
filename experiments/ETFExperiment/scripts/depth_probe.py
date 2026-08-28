"""A.1 Task 1: the served depth of each outcome substrate, measured.

Counts rows and reads timestamps. No price field is parsed on this path.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime, timedelta

from etf.blindness import candle_times, funding_rows
from etf.clock import now_utc, utc_ms
from etf.config import CONFIG
from etf.http import PacedClient
from etf.ledger.requests import RequestLedger
from etf.paths import REPORTS

REPORT = REPORTS / "stage_a1" / "depth.json"


def iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, UTC).isoformat()


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    client = PacedClient(RequestLedger())
    now = now_utc()
    out: list[dict[str, object]] = []

    # Does one candleSnapshot call cap at 5,000 rows?
    for interval, days in (("1h", 400), ("1d", 3000)):
        start = now - timedelta(days=days)
        r = client.post_json(
            CONFIG.hyperliquid_info_url,
            {
                "type": "candleSnapshot",
                "req": {
                    "coin": CONFIG.perp_coin,
                    "interval": interval,
                    "startTime": utc_ms(start),
                    "endTime": utc_ms(now),
                },
            },
            source="venue",
            endpoint="venue.candleSnapshot",
        )
        t = candle_times(r.body)
        entry = {
            "probe": f"candle_cap_{interval}",
            "requested_days": days,
            "row_count": t.row_count,
            "first_open_utc": iso(t.open_ms[0]) if t.open_ms else None,
            "last_close_utc": iso(t.close_ms[-1]) if t.close_ms else None,
        }
        out.append(entry)
        print(json.dumps(entry))

    # How far back does fundingHistory reach, and what is one page worth?
    for label, start_ms in (
        ("funding_2024_01", utc_ms(datetime(2024, 1, 1, tzinfo=UTC))),
        ("funding_2023_05", utc_ms(datetime(2023, 5, 13, tzinfo=UTC))),
        ("funding_2025_05_page", utc_ms(datetime(2025, 5, 1, tzinfo=UTC))),
    ):
        r = client.post_json(
            CONFIG.hyperliquid_info_url,
            {"type": "fundingHistory", "coin": CONFIG.perp_coin, "startTime": start_ms},
            source="venue",
            endpoint="venue.fundingHistory",
        )
        rows = funding_rows(r.body)
        entry = {
            "probe": label,
            "http_status": r.status,
            "row_count": len(rows),
            "gated_rows": sum(1 for x in rows if not isinstance(x.rate, float)),
            "first_time_utc": iso(rows[0].time_ms) if rows else None,
            "last_time_utc": iso(rows[-1].time_ms) if rows else None,
        }
        out.append(entry)
        print(json.dumps(entry))

    REPORT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
