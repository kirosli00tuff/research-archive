"""A.1 Task 2: rate ceilings measured per endpoint, never per host.

The solattn ADR-021 lesson: ceilings are per endpoint, measured never assumed,
and a measurement of one endpoint is not evidence about another even on the
same host. Each endpoint below gets its own escalation ladder.

Protocol, fixed before running:

1. Descend a ladder of spacings, `BURST` requests at each rung.
2. Record every status code and the verbatim first 300 bytes of any non-200.
3. **Stop the ladder at the first non-200** — the refusal is the measurement,
   and continuing past it is abuse rather than science.
4. The ladder bottoms out at `ABSOLUTE_MIN_SPACING_S` (1.0 s), the repository's
   own floor. A ceiling below a pace this project will never use is not
   actionable, so where no refusal appears the finding recorded is **"no
   ceiling found at or above the floor"** and the operating pace is set at half
   the highest verified-clean rate — the NPLExperiment pattern for an endpoint
   whose ceiling was not found.

Nothing here parses a payload beyond its status and its first bytes.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field

from etf.clock import iso_z, now_utc
from etf.config import CONFIG
from etf.http import PacedClient, TransportFailure
from etf.ledger.requests import RequestLedger
from etf.pacing import ABSOLUTE_MIN_SPACING_S
from etf.paths import REPORTS

REPORT = REPORTS / "stage_a1" / "rate_ceilings.json"
BURST = 6


@dataclass(frozen=True, slots=True)
class Target:
    endpoint: str
    source: str
    method: str
    url: str
    body: dict[str, object] = field(default_factory=dict)
    ladder: tuple[float, ...] = (5.0, 2.0, 1.0)


TARGETS: tuple[Target, ...] = (
    Target(
        "flow.table",
        "flow",
        "GET",
        "https://farside.co.uk/btc/",
        ladder=(20.0, 10.0, 5.0),
    ),
    Target(
        "archive.availability",
        "archive",
        "GET",
        f"{CONFIG.wayback_availability_url}"
        "?url=farside.co.uk/bitcoin-etf-flow-all-data/&timestamp=20250601",
    ),
    Target(
        "archive.timemap",
        "archive",
        "GET",
        f"{CONFIG.wayback_timemap_url}/https://farside.co.uk/bitcoin-etf-flow-all-data/",
    ),
    Target(
        "venue.candleSnapshot",
        "venue",
        "POST",
        CONFIG.hyperliquid_info_url,
        body={
            "type": "candleSnapshot",
            "req": {
                "coin": CONFIG.perp_coin,
                "interval": "1h",
                "startTime": 1_772_000_000_000,
                "endTime": 1_772_086_400_000,
            },
        },
        ladder=(2.0, 1.0),
    ),
    Target(
        "venue.fundingHistory",
        "venue",
        "POST",
        CONFIG.hyperliquid_info_url,
        body={
            "type": "fundingHistory",
            "coin": CONFIG.perp_coin,
            "startTime": 1_772_000_000_000,
            "endTime": 1_772_086_400_000,
        },
        ladder=(2.0, 1.0),
    ),
    Target(
        "kraken.ohlc",
        "venue",
        "GET",
        f"{CONFIG.kraken_ohlc_url}?pair=XBTUSD&interval=1440",
        ladder=(3.0, 1.5, 1.0),
    ),
)


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    ledger = RequestLedger()
    results: list[dict[str, object]] = []

    for target in TARGETS:
        rungs: list[dict[str, object]] = []
        refused = False
        clean_rate_per_min = 0.0
        for spacing in target.ladder:
            if refused:
                break
            # The ceiling probe overrides the registered pace deliberately;
            # measuring a ceiling is the one job that needs to.
            client = PacedClient(ledger, pacing_overrides={target.endpoint: spacing})
            statuses: list[int] = []
            first_refusal: str | None = None
            started = time.monotonic()
            for _ in range(BURST):
                try:
                    if target.method == "GET":
                        response = client.get(
                            target.url, source=target.source, endpoint=target.endpoint
                        )
                    else:
                        response = client.post_json(
                            target.url,
                            target.body,
                            source=target.source,
                            endpoint=target.endpoint,
                        )
                except TransportFailure as exc:
                    statuses.append(-1)
                    first_refusal = f"TransportFailure: {exc}"
                    refused = True
                    break
                statuses.append(response.status)
                if response.status != 200:
                    first_refusal = response.body[:300].decode("utf-8", "replace")
                    refused = True
                    break
            elapsed = time.monotonic() - started
            observed = (len(statuses) / elapsed * 60.0) if elapsed > 0 else 0.0
            rung = {
                "spacing_s": spacing,
                "requests": len(statuses),
                "statuses": statuses,
                "elapsed_s": round(elapsed, 2),
                "observed_rate_per_min": round(observed, 2),
                "all_200": all(s == 200 for s in statuses),
                "first_refusal_verbatim": first_refusal,
            }
            rungs.append(rung)
            if rung["all_200"]:
                clean_rate_per_min = max(clean_rate_per_min, observed)
            print(f"{target.endpoint:24s} spacing={spacing:5.1f}s statuses={statuses}")

        if refused:
            finding = "ceiling_found"
            operating = target.ladder[max(0, len(rungs) - 1)] * 2.0
        else:
            finding = "no_ceiling_found_at_or_above_floor"
            operating = max(target.ladder[-1] * 2.0, ABSOLUTE_MIN_SPACING_S)
        results.append(
            {
                "endpoint": target.endpoint,
                "source": target.source,
                "measured_at": iso_z(now_utc()),
                "burst_per_rung": BURST,
                "ladder": list(target.ladder),
                "rungs": rungs,
                "finding": finding,
                "highest_verified_clean_rate_per_min": round(clean_rate_per_min, 2),
                "operating_min_spacing_s": operating,
            }
        )

    REPORT.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
