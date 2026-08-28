"""A.2 Task 3: seal the outcome substrate across the whole servable hourly window.

**Why this runs now rather than after Section 0 fires.** A.1 Task 1 measured the
venue serving a rolling 5,001-candle window: hourly candles reach back about 208
days and the boundary slides forward one hour per hour. Every day of delay
permanently destroys one day of retro coverage, and there is no archive for it.

**Why the window sealed is wider than the registered hold.** The Section 3
anchor amendment can only move the anchor *later*. A hold window pinned to the
provisional 08:00 UTC anchor would have to be refetched if the measured 95th
percentile moves it — by which time part of it may have slid out of the servable
window. So this seals, per trading day D, the whole span [D+1 00:00Z, D+3
00:00Z): 48 hours, which contains the anchor-plus-24-hours window for **any**
anchor hour the amendment rule could choose. Sealing wide is anchor-agnostic;
it is not a second look, because nothing here reads a value.

Sealed as raw response bytes. Coverage is counted through the blindness readers,
which see timestamps and row counts and cannot return a close.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, date, datetime, timedelta

from etf.absence import Absent
from etf.blindness import candle_times, funding_rows
from etf.clock import MS_PER_HOUR, iso_z, now_utc, utc_ms
from etf.config import CONFIG
from etf.http import PacedClient
from etf.ledger.requests import RequestLedger
from etf.paths import DATA, FUNDING_DIR, OUTCOMES_DIR, REPORTS
from etf.seal import seal_bytes
from etf.snapshot import parse_flow_table

REPORT = REPORTS / "stage_a2" / "substrate_coverage.json"
CANDLE_PAGE_ROWS = 5000
FUNDING_PAGE_ROWS = 500


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    client = PacedClient(RequestLedger())
    now = now_utc()

    days = parse_flow_table((DATA / "access" / "farside-btc-all.html").read_text(errors="replace"))
    oos_start = date.fromisoformat(CONFIG.oos_start_date)
    universe = [
        d.trade_date
        for d in days
        if d.trade_date >= oos_start and not isinstance(d.signal_usd, Absent)
    ]

    # One request establishes where the rolling window actually starts today.
    probe = client.post_json(
        CONFIG.hyperliquid_info_url,
        {
            "type": "candleSnapshot",
            "req": {
                "coin": CONFIG.perp_coin,
                "interval": "1h",
                "startTime": utc_ms(now - timedelta(days=400)),
                "endTime": utc_ms(now),
            },
        },
        source="venue",
        endpoint="venue.candleSnapshot",
    )
    times = candle_times(probe.body)
    if not times.open_ms:
        print("the venue served no hourly candles at all; recording the absence and stopping")
        return 1
    window_start_ms = times.open_ms[0]
    written = seal_bytes(OUTCOMES_DIR / "btc-1h-servable-window.json", probe.body)
    print(
        f"hourly window: {datetime.fromtimestamp(window_start_ms / 1000, UTC).isoformat()} "
        f"-> now, rows={times.row_count}, sha256={written.sha256[:12]}"
    )

    hours_present = set(times.open_ms)

    # Funding, paged at the measured 500 rows per page, over the same span.
    funding_hours: set[int] = set()
    cursor = window_start_ms
    pages = 0
    while cursor < utc_ms(now):
        response = client.post_json(
            CONFIG.hyperliquid_info_url,
            {"type": "fundingHistory", "coin": CONFIG.perp_coin, "startTime": cursor},
            source="venue",
            endpoint="venue.fundingHistory",
        )
        if response.status != 200:
            print(f"funding page at {cursor} returned HTTP {response.status}; recorded, stopping")
            break
        rows = funding_rows(response.body)
        if not rows:
            break
        seal_bytes(FUNDING_DIR / f"btc-funding-{cursor}.json", response.body)
        pages += 1
        for row in rows:
            funding_hours.add(row.time_ms - (row.time_ms % MS_PER_HOUR))
        last = rows[-1].time_ms
        if len(rows) < FUNDING_PAGE_ROWS or last <= cursor:
            break
        cursor = last + 1
    print(f"funding pages sealed: {pages}, distinct hours: {len(funding_hours)}")

    # Per trading day, coverage of the wide 48-hour span. Counts only.
    per_day: list[dict[str, object]] = []
    for day in universe:
        span_start = datetime.combine(day + timedelta(days=1), datetime.min.time(), tzinfo=UTC)
        span_end = span_start + timedelta(hours=48)
        expected = [utc_ms(span_start) + h * MS_PER_HOUR for h in range(48)]
        candles = sum(1 for ms in expected if ms in hours_present)
        funding = sum(1 for ms in expected if ms in funding_hours)
        per_day.append(
            {
                "trade_date": day.isoformat(),
                "span_start": iso_z(span_start),
                "span_end": iso_z(span_end),
                "expected_hours": 48,
                "candle_hours": candles,
                "funding_hours": funding,
                "candle_coverage": candles / 48,
                "funding_coverage": funding / 48,
                "covered": (candles / 48) >= CONFIG.min_outcome_coverage_candles
                and (funding / 48) >= CONFIG.min_outcome_coverage_funding,
            }
        )

    covered = [d for d in per_day if d["covered"]]
    out = {
        "measured_at": iso_z(now),
        "hourly_window_start": datetime.fromtimestamp(window_start_ms / 1000, UTC).isoformat(),
        "hourly_rows_sealed": times.row_count,
        "funding_pages_sealed": pages,
        "funding_hours_sealed": len(funding_hours),
        "oos_trading_days": len(universe),
        "days_covered_at_registered_bars": len(covered),
        "min_outcome_coverage_candles": CONFIG.min_outcome_coverage_candles,
        "min_outcome_coverage_funding": CONFIG.min_outcome_coverage_funding,
        "per_day": per_day,
    }
    REPORT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(
        f"out-of-sample trading days n = {len(universe)}; "
        f"days covered at the registered 0.95/0.95 bars n = {len(covered)}"
    )
    if covered:
        print(f"first covered {covered[0]['trade_date']}, last covered {covered[-1]['trade_date']}")
    print(f"\nwrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
