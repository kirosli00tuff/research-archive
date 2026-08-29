"""A.1 TASK 1 — live access probes, paced and ledger-charged.

Sends one probe per endpoint against the vendors whose recorded terms permit
it, stores the raw bytes sealed, and records **only** the status code, the byte
count, the elapsed time and the verbatim refusal fragment. **No response body
is parsed for a priced field.**
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from orb.http import PacedClient  # noqa: E402
from orb.ledger import AppendOnlyLedger, RequestLedger  # noqa: E402
from orb.seal import SealedWriter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "access"

# Vendor -> (pace_key, url). One probe each. Keyless by design: Stage A holds
# no credential and .env.example is empty.
PROBES: dict[str, list[tuple[str, str]]] = {
    "polygon": [
        (
            "polygon:aggs",
            "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/minute/2015-06-01/2015-06-01",
        ),
        ("polygon:tickers", "https://api.polygon.io/v3/reference/tickers?limit=1"),
    ],
    "alpaca": [
        (
            "alpaca:bars",
            "https://data.alpaca.markets/v2/stocks/AAPL/bars?timeframe=1Min&start=2015-06-01&end=2015-06-02",
        ),
    ],
    "databento": [
        ("databento:timeseries", "https://hist.databento.com/v0/metadata.list_datasets"),
    ],
    "tiingo": [
        ("tiingo:iex", "https://api.tiingo.com/iex/AAPL/prices?resampleFreq=1min"),
    ],
    "alphavantage": [
        (
            "alphavantage:intraday",
            "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min&outputsize=compact&apikey=demo",
        ),
        (
            "alphavantage:listing",
            "https://www.alphavantage.co/query?function=LISTING_STATUS&state=delisted&apikey=demo",
        ),
    ],
}

DAILY_CAPS: dict[str, int] = {v: 40 for v in PROBES}
SPACING: dict[str, float] = {}


def main() -> int:
    ledger = RequestLedger(DATA / "requests.jsonl", DAILY_CAPS)
    seal = SealedWriter(DATA / "sealed", AppendOnlyLedger(DATA / "seals.jsonl"))
    client = PacedClient(ledger, SPACING)

    findings: list[dict[str, object]] = []
    for vendor, probes in PROBES.items():
        for pace_key, url in probes:
            response = client.get(url, vendor=vendor, pace_key=pace_key)
            record = seal.store(
                f"{pace_key.replace(':', '_')}.raw", response.body
            )
            finding = {
                "vendor": vendor,
                "pace_key": pace_key,
                "url": url,
                "status_code": response.status_code,
                "byte_count": response.byte_count,
                "elapsed_s": round(response.elapsed_s, 3),
                "health": response.health.value,
                "sha256": record.sha256,
                "sent_at": response.sent_at,
                "refusal_fragment": response.refusal_fragment(600),
            }
            findings.append(finding)
            print(
                f"{vendor:14s} {pace_key:26s} http={response.status_code:<4d} "
                f"bytes={response.byte_count:<7d} {response.elapsed_s:.2f}s"
            )

    out = DATA / "probe_findings.json"
    out.write_text(json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwrote {out} ({len(findings)} probes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
