"""A.1 TASK 3 — credentialed access verification.

Establishes that each credential **authenticates**, before anything is measured
about the data it serves. Status code, latency, body size and a **redacted**
body fragment are recorded per probe; raw bytes are sealed with a SHA-256 in the
append-only ledger.

Every bar request sits **inside the pre-period carve-out**, strictly before
2016-01-04T14:30:00.000Z. Nothing here parses a priced field: the probes read a
status code and a byte count, both on the readable field list.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import probe_row, send, wire, write_report  # noqa: E402
from orb.redact import say  # noqa: E402
from orb.vendors import (  # noqa: E402
    alpaca_account,
    alpaca_assets,
    alpaca_minute_bars,
    massive_minute_bars,
    massive_reference,
)

CARVE_OUT_SESSION = "2015-06-01"
CARVE_OUT_START_ISO = "2015-06-01T13:30:00Z"
CARVE_OUT_END_ISO = "2015-06-01T20:00:00Z"


def main() -> int:
    store, client, seal = wire()

    say("credential presence, name and character length only:")
    for presence in store.presence():
        say(
            f"  {presence.name:24s} present={presence.is_present} "
            f"len={presence.character_length}"
        )

    probes = [
        ("massive_reference", massive_reference(store, limit=1)),
        (
            "massive_aggs_carveout",
            massive_minute_bars(store, "AAPL", CARVE_OUT_SESSION, CARVE_OUT_SESSION),
        ),
        (
            "alpaca_bars_carveout_sip",
            alpaca_minute_bars(
                store, "AAPL", CARVE_OUT_START_ISO, CARVE_OUT_END_ISO, feed="sip"
            ),
        ),
        (
            "alpaca_bars_carveout_iex",
            alpaca_minute_bars(
                store, "AAPL", CARVE_OUT_START_ISO, CARVE_OUT_END_ISO, feed="iex"
            ),
        ),
        ("alpaca_account_live", alpaca_account(store, paper=False)),
        ("alpaca_account_paper", alpaca_account(store, paper=True)),
        ("alpaca_assets_inactive", alpaca_assets(store, status="inactive")),
    ]

    findings: list[dict[str, object]] = []
    for label, request in probes:
        response = send(client, request)
        record = seal.store(f"task3_{label}.raw", response.body)
        findings.append(probe_row(label, request, response, record.sha256))
        say(
            f"{label:28s} http={response.status_code:<4d} "
            f"bytes={response.byte_count:<8d} {response.elapsed_s:.2f}s"
        )

    write_report("task3_auth.json", findings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
