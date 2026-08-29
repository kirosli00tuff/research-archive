"""A.1 Task 1: live verification of the venue and archive endpoints.

Reads nothing but timestamps, row counts and HTTP statuses. The candle probe
goes through `etf.blindness.candle_times`, which sees `t`, `T` and the row
count and cannot see a price. The funding probe goes through
`etf.blindness.funding_rows`, whose rates are gated by the pre-period pin.
"""

from __future__ import annotations

import json
import sys

from etf.blindness import candle_times, funding_rows
from etf.clock import iso_z, now_utc
from etf.config import CONFIG
from etf.http import PacedClient, TransportFailure
from etf.ledger.requests import RequestLedger
from etf.paths import DATA, REPORTS

OUT = DATA / "access"
REPORT = REPORTS / "stage_a1" / "venue_and_archive.json"

# 2025-04-01 and 2025-05-15, so one probe sits inside the pre-period carve-out
# and one sits after it; the funding reader must gate the second and not the
# first, and that is checked here against a live payload.
PRE_PERIOD_START_MS = 1_743_465_600_000
POST_PERIOD_START_MS = 1_747_267_200_000


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    client = PacedClient(RequestLedger())
    rows: list[dict[str, object]] = []

    def record(name: str, **kv: object) -> None:
        rows.append({"probe": name, "at": iso_z(now_utc()), **kv})
        print(name, json.dumps(kv, default=str)[:400])

    probes: list[tuple[str, dict[str, object], str]] = [
        (
            "candle_1h",
            {
                "type": "candleSnapshot",
                "req": {
                    "coin": CONFIG.perp_coin,
                    "interval": "1h",
                    "startTime": POST_PERIOD_START_MS,
                    "endTime": POST_PERIOD_START_MS + 7 * 86_400_000,
                },
            },
            "venue.candleSnapshot",
        ),
        (
            "candle_1d",
            {
                "type": "candleSnapshot",
                "req": {
                    "coin": CONFIG.perp_coin,
                    "interval": "1d",
                    "startTime": POST_PERIOD_START_MS,
                    "endTime": POST_PERIOD_START_MS + 30 * 86_400_000,
                },
            },
            "venue.candleSnapshot",
        ),
        (
            "funding_pre_period",
            {
                "type": "fundingHistory",
                "coin": CONFIG.perp_coin,
                "startTime": PRE_PERIOD_START_MS,
                "endTime": PRE_PERIOD_START_MS + 3 * 86_400_000,
            },
            "venue.fundingHistory",
        ),
        (
            "funding_post_period",
            {
                "type": "fundingHistory",
                "coin": CONFIG.perp_coin,
                "startTime": POST_PERIOD_START_MS,
                "endTime": POST_PERIOD_START_MS + 3 * 86_400_000,
            },
            "venue.fundingHistory",
        ),
        ("meta", {"type": "meta"}, "venue.meta"),
    ]

    for name, body, endpoint in probes:
        try:
            response = client.post_json(
                CONFIG.hyperliquid_info_url, body, source="venue", endpoint=endpoint
            )
        except TransportFailure as exc:
            record(name, state="source_failed", detail=str(exc))
            continue
        (OUT / f"hl-{name}.json").write_bytes(response.body)
        entry: dict[str, object] = {
            "state": "stored" if response.status == 200 else "source_failed",
            "http_status": response.status,
            "byte_count": len(response.body),
            "elapsed_s": round(response.elapsed_s, 3),
            "head": response.body[:140].decode("utf-8", "replace"),
        }
        if response.status == 200 and name.startswith("candle"):
            times = candle_times(response.body)
            entry |= {
                "row_count": times.row_count,
                "first_open_ms": times.open_ms[0] if times.open_ms else None,
                "last_close_ms": times.close_ms[-1] if times.close_ms else None,
            }
        if response.status == 200 and name.startswith("funding"):
            frows = funding_rows(response.body)
            gated = sum(1 for r in frows if not isinstance(r.rate, float))
            entry |= {
                "row_count": len(frows),
                "gated_rows": gated,
                "readable_rows": len(frows) - gated,
                "first_time_ms": frows[0].time_ms if frows else None,
                "last_time_ms": frows[-1].time_ms if frows else None,
            }
        record(name, **entry)

    archive_targets = (
        (
            "wayback_availability",
            f"{CONFIG.wayback_availability_url}"
            "?url=farside.co.uk/bitcoin-etf-flow-all-data/&timestamp=20250601",
            "archive.availability",
        ),
        (
            "wayback_timemap",
            f"{CONFIG.wayback_timemap_url}/https://farside.co.uk/bitcoin-etf-flow-all-data/",
            "archive.timemap",
        ),
        (
            "kraken_ohlc",
            f"{CONFIG.kraken_ohlc_url}?pair=XBTUSD&interval=1440",
            "kraken.ohlc",
        ),
    )
    for name, url, endpoint in archive_targets:
        source = "venue" if name.startswith("kraken") else "archive"
        try:
            response = client.get(url, source=source, endpoint=endpoint)
        except TransportFailure as exc:
            record(name, state="source_failed", detail=str(exc))
            continue
        (OUT / f"{name}.txt").write_bytes(response.body)
        record(
            name,
            state="stored" if response.status == 200 else "source_failed",
            http_status=response.status,
            byte_count=len(response.body),
            elapsed_s=round(response.elapsed_s, 3),
            content_type=response.headers.get("content-type", ""),
            head=response.body[:200].decode("utf-8", "replace"),
        )

    REPORT.write_text(json.dumps(rows, indent=2, sort_keys=True, default=str), encoding="utf-8")
    print(f"\nwrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
