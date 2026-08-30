"""A.1 TASK 3, second round — disambiguating two refusals.

Round one left two questions that a status code alone cannot answer.

1. **Massive returned 403 `NOT_AUTHORIZED` on a 2015 aggregate.** That is
   consistent with *"this tier serves no aggregates at all"* and with *"this
   tier serves aggregates but not that far back"*, and the two have completely
   different consequences. A recent aggregate separates them.
2. **Alpaca returned 401 on the live trading host** while the paper host
   answered 200. That is consistent with *"the credential is broken"* and with
   *"the credential is a paper-account credential"*. The paper asset endpoint
   separates them.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import probe_row, send, wire, write_report

from orb.redact import say
from orb.vendors import (
    ALPACA,
    ALPACA_PAPER_HOST,
    MEASURED_SINGLE_VENUE_FEED,
    VendorRequest,
    alpaca_headers,
    alpaca_minute_bars,
    alpaca_minute_bars_on_feed,
    consolidated_feed,
    massive_minute_bars,
)

RECENT_SESSION = "2026-07-15"
RECENT_START_ISO = "2026-07-15T13:30:00Z"
RECENT_END_ISO = "2026-07-15T13:40:00Z"


def main() -> int:
    store, client, seal = wire()

    probes = [
        (
            "massive_aggs_recent",
            massive_minute_bars(store, "AAPL", RECENT_SESSION, RECENT_SESSION),
        ),
        (
            "alpaca_bars_recent_sip",
            alpaca_minute_bars(
                store,
                "AAPL",
                RECENT_START_ISO,
                RECENT_END_ISO,
                feed=consolidated_feed(),
            ),
        ),
        (
            "alpaca_bars_recent_iex",
            alpaca_minute_bars_on_feed(
                store,
                "AAPL",
                RECENT_START_ISO,
                RECENT_END_ISO,
                feed=MEASURED_SINGLE_VENUE_FEED,
                tape_control_reason=(
                    "A.1 TASK 2 tape control: the single-venue feed is "
                    "requested on purpose, beside the consolidated one, so "
                    "that the two can be compared. Amendment 7 registered "
                    "the branch."
                ),
            ),
        ),
        (
            "alpaca_assets_paper_inactive",
            VendorRequest(
                vendor=ALPACA,
                pace_key="alpaca:assets",
                url=f"{ALPACA_PAPER_HOST}/v2/assets?status=inactive&asset_class=us_equity",
                headers=alpaca_headers(store),
            ),
        ),
    ]

    findings: list[dict[str, object]] = []
    for label, request in probes:
        response = send(client, request)
        record = seal.store(f"task3b_{label}.raw", response.body)
        findings.append(probe_row(label, request, response, record.sha256))
        say(
            f"{label:30s} http={response.status_code:<4d} "
            f"bytes={response.byte_count:<8d} {response.elapsed_s:.2f}s"
        )

    write_report("task3b_auth.json", findings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
