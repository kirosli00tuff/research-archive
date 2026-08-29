"""A.1 TASK 2 — rate-ceiling escalation, per endpoint.

The solattn ADR-021 lesson: **ceilings are per endpoint, never per host, and
measured never assumed.** This probe runs a short escalation against the
endpoints whose terms permit it and records the refusal shape verbatim, the
sustained admitted rate, and the status distribution.

**What this can and cannot measure is recorded with the result.** With no
credential, the only reachable path on every permitted vendor is the
*unauthenticated refusal* path. A ceiling measured on a 401 path is **not
evidence about the authenticated data endpoint** — that is ADR-021's own
corollary, applied to this repository's own measurement.
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from orb.http import PacedClient  # noqa: E402
from orb.ledger import RequestLedger  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "access"

# (vendor, pace_key, url, spacing_s, n) — a short escalation, deliberately
# modest: the goal is the refusal shape, not a denial-of-service census.
ESCALATION: list[tuple[str, str, str, float, int]] = [
    ("polygon", "polygon:aggs", "https://api.polygon.io/v3/reference/tickers?limit=1", 2.0, 5),
    ("polygon", "polygon:aggs", "https://api.polygon.io/v3/reference/tickers?limit=1", 0.5, 8),
    ("alphavantage", "alphavantage:intraday",
     "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min&apikey=demo",
     2.0, 5),
]

CAPS: dict[str, int] = {"polygon": 60, "alphavantage": 40}


def main() -> int:
    ledger = RequestLedger(DATA / "requests.jsonl", CAPS)
    results: list[dict[str, object]] = []

    for vendor, pace_key, url, spacing, n in ESCALATION:
        client = PacedClient(ledger, {pace_key: spacing})
        codes: Counter[int] = Counter()
        fragments: set[str] = set()
        started = time.monotonic()
        for _ in range(n):
            response = client.get(url, vendor=vendor, pace_key=pace_key)
            codes[response.status_code] += 1
            fragments.add(response.refusal_fragment(200))
        elapsed = time.monotonic() - started
        row = {
            "vendor": vendor,
            "pace_key": pace_key,
            "requested_spacing_s": spacing,
            "n": n,
            "elapsed_s": round(elapsed, 2),
            "achieved_rate_per_min": round(n / elapsed * 60, 2) if elapsed else None,
            "status_distribution": dict(codes),
            "refused_429": codes.get(429, 0),
            "distinct_payloads": sorted(fragments),
        }
        results.append(row)
        print(
            f"{vendor:14s} {pace_key:24s} spacing={spacing}s n={n} "
            f"rate={row['achieved_rate_per_min']}/min codes={dict(codes)} "
            f"429s={codes.get(429, 0)}"
        )

    out = DATA / "ceiling_findings.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
