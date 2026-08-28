"""A.1 Task 1 step 1: robots.txt and published terms, before the first repeated fetch.

Standing rule 11: terms of service bind. This script fetches nothing but
`robots.txt` and the published terms page of each candidate source, records the
status code and the verbatim body, and stops. It touches no data surface.

Every request goes through the ledger, which charges before sending.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from etf.clock import iso_z, now_utc
from etf.http import PacedClient, TransportFailure
from etf.ledger.requests import RequestLedger
from etf.paths import DATA, REPORTS

OUT_DIR = DATA / "access"
REPORT = REPORTS / "stage_a1" / "robots_and_terms.json"

# (source bucket, host label, url, endpoint pacing key)
TARGETS: tuple[tuple[str, str, str, str], ...] = (
    ("flow", "farside", "https://farside.co.uk/robots.txt", "meta.robots"),
    ("flow", "sosovalue", "https://sosovalue.com/robots.txt", "meta.robots"),
    ("flow", "theblock", "https://www.theblock.co/robots.txt", "meta.robots"),
    ("flow", "glassnode", "https://glassnode.com/robots.txt", "meta.robots"),
    ("archive", "web.archive.org", "https://web.archive.org/robots.txt", "meta.robots"),
    ("archive", "archive.org", "https://archive.org/robots.txt", "meta.robots"),
    ("venue", "api.hyperliquid.xyz", "https://api.hyperliquid.xyz/robots.txt", "meta.robots"),
    ("venue", "api.kraken.com", "https://api.kraken.com/robots.txt", "meta.robots"),
    ("flow", "farside-terms", "https://farside.co.uk/terms-of-use/", "meta.terms"),
)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    ledger = RequestLedger()
    client = PacedClient(ledger)
    rows: list[dict[str, object]] = []
    for source, label, url, endpoint in TARGETS:
        started = iso_z(now_utc())
        try:
            response = client.get(url, source=source, endpoint=endpoint)
        except TransportFailure as exc:
            rows.append(
                {
                    "source": source,
                    "label": label,
                    "url": url,
                    "requested_at": started,
                    "state": "source_failed",
                    "detail": str(exc),
                }
            )
            print(f"{label:22s} TRANSPORT FAILURE {exc}")
            continue
        body_path = OUT_DIR / f"{label}.robots.txt"
        body_path.write_bytes(response.body)
        rows.append(
            {
                "source": source,
                "label": label,
                "url": url,
                "requested_at": started,
                "state": "stored" if response.status == 200 else "source_failed",
                "http_status": response.status,
                "byte_count": len(response.body),
                "content_type": response.headers.get("content-type", ""),
                "body_path": str(body_path.relative_to(Path.cwd())),
            }
        )
        print(f"{label:22s} HTTP {response.status}  {len(response.body)} bytes")
    REPORT.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
