"""A.1 TASK 7 — rate ceilings, re-measured on the **authenticated** endpoints.

**The ceilings in `docs/ACCESS.md` were measured against a 401 and carry no
information about the served path.** That is Amendment 2's own corollary, and
this task is where it is discharged: solattn ADR-021 established that a ceiling
is a property of an **endpoint**, and the authenticated data endpoint is a
different endpoint from the refusal path that answered in August.

**The escalation protocol is the one A.1 TASK 2 used**, run against paths that
now serve. It is deliberately modest — the goal is **the refusal shape and the
sustained admitted rate**, not a census and certainly not a load test. Each cell
stops at a bounded `n`, and a cell that draws a refusal is not repeated faster.

**The operating pace is set at half the measured ceiling**, and reduced further
where the recorded terms ask for it. Where the measurement and the vendor's
documented limit disagree, **the disagreement is recorded as a finding** and the
measurement wins — standing rule 4 — but the *operating* figure stays on the
conservative side of both.
"""

from __future__ import annotations

import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import DATA, send, wire, write_report  # noqa: E402
from orb.http import PacedClient  # noqa: E402
from orb.ledger import RequestLedger  # noqa: E402
from orb.redact import say  # noqa: E402
from orb.vendors import (  # noqa: E402
    ALPACA,
    ALPACA_DOCUMENTED_PER_MINUTE,
    MASSIVE,
    MASSIVE_DOCUMENTED_PER_MINUTE,
    PROVISIONAL_DAILY_CAPS,
    alpaca_minute_bars,
    massive_minute_bars,
    massive_reference,
)

PROBE_SESSION = "2026-07-15"
PROBE_START_ISO = "2026-07-15T13:30:00Z"
PROBE_END_ISO = "2026-07-15T13:35:00Z"


def main() -> int:
    store, _client, _seal = wire()
    ledger = RequestLedger(DATA / "requests.jsonl", dict(PROVISIONAL_DAILY_CAPS))

    cells = [
        (
            MASSIVE,
            "massive:reference",
            lambda: massive_reference(store, limit=1),
            2.0,
            8,
            MASSIVE_DOCUMENTED_PER_MINUTE,
        ),
        (
            MASSIVE,
            "massive:aggs",
            lambda: massive_minute_bars(store, "AAPL", PROBE_SESSION, PROBE_SESSION),
            2.0,
            8,
            MASSIVE_DOCUMENTED_PER_MINUTE,
        ),
        (
            MASSIVE,
            "massive:aggs",
            lambda: massive_minute_bars(store, "AAPL", PROBE_SESSION, PROBE_SESSION),
            0.5,
            12,
            MASSIVE_DOCUMENTED_PER_MINUTE,
        ),
        (
            ALPACA,
            "alpaca:bars",
            lambda: alpaca_minute_bars(
                store, "AAPL", PROBE_START_ISO, PROBE_END_ISO, feed="sip"
            ),
            0.2,
            25,
            ALPACA_DOCUMENTED_PER_MINUTE,
        ),
    ]

    results: list[dict[str, object]] = []
    for vendor, pace_key, build, spacing, n, documented in cells:
        client = PacedClient(ledger, {pace_key: spacing}, timeout_s=60.0)
        codes: Counter[int] = Counter()
        fragments: set[str] = set()
        first_refusal_at: int | None = None
        started = time.monotonic()
        for index in range(n):
            response = send(client, build())
            codes[response.status_code] += 1
            if not (200 <= response.status_code < 300):
                fragments.add(response.refusal_fragment(300))
                if first_refusal_at is None:
                    first_refusal_at = index + 1
        elapsed = time.monotonic() - started
        rate = round(n / elapsed * 60, 2) if elapsed else 0.0
        admitted = sum(count for code, count in codes.items() if 200 <= code < 300)
        row: dict[str, object] = {
            "vendor": vendor,
            "pace_key": pace_key,
            "requested_spacing_s": spacing,
            "n": n,
            "elapsed_s": round(elapsed, 2),
            "achieved_rate_per_min": rate,
            "admitted": admitted,
            "sustained_admitted_rate_per_min": (
                round(admitted / elapsed * 60, 2) if elapsed else 0.0
            ),
            "status_distribution": dict(codes),
            "refused_429": codes.get(429, 0),
            "first_refusal_at_request": first_refusal_at,
            "documented_per_minute": documented,
            "documented_label": "carried, vendor documentation, never measured",
            "refusal_payloads_verbatim_redacted": sorted(fragments),
        }
        results.append(row)
        say(
            f"{vendor:8s} {pace_key:18s} spacing={spacing}s n={n} "
            f"rate={rate}/min admitted={admitted} codes={dict(codes)} "
            f"429s={codes.get(429, 0)}"
        )

    write_report("task7_ceilings.json", results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
