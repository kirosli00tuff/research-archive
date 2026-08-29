"""One-shot ledger-charged fetch, for A.1 access verification.

Usage: uv run python scripts/fetch_once.py <source> <endpoint> <url> <out-name>

Records the status, headers and verbatim body under data/access/. Nothing here
parses a payload; the reader decides what the bytes are.
"""

from __future__ import annotations

import json
import sys

from etf.clock import iso_z, now_utc
from etf.http import PacedClient, TransportFailure
from etf.ledger.requests import RequestLedger
from etf.paths import DATA

OUT_DIR = DATA / "access"


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__)
        return 2
    _, source, endpoint, url, name = argv
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = PacedClient(RequestLedger())
    started = iso_z(now_utc())
    try:
        response = client.get(url, source=source, endpoint=endpoint)
    except TransportFailure as exc:
        print(json.dumps({"state": "source_failed", "url": url, "detail": str(exc)}, indent=2))
        return 1
    body_path = OUT_DIR / name
    body_path.write_bytes(response.body)
    meta = {
        "requested_at": started,
        "url": url,
        "http_status": response.status,
        "byte_count": len(response.body),
        "elapsed_s": round(response.elapsed_s, 3),
        "content_type": response.headers.get("content-type", ""),
        "server": response.headers.get("server", ""),
        "body_path": str(body_path),
    }
    (OUT_DIR / f"{name}.meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
