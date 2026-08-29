"""A.2 Task 4 inputs: pre-period volatility and funding, under the Section 9 carve-out.

**Every read here is stamped strictly before 2025-05-01.** That window sits
inside the source study's own sample (January 2024 through April 2025) and
outside this test sample, so reading it cannot leak an observation the Stage B
verdict is computed on. The reader refuses the boundary instant itself, and it
refuses the whole series rather than truncating it if one row crosses.

These are the only price and funding values this repository reads before the
registered Stage B read, and this is the only script that reads them.
"""

from __future__ import annotations

import json
import statistics
import sys
from datetime import UTC, datetime

from etf.blindness import funding_rows
from etf.clock import iso_z, now_utc, utc_ms
from etf.config import CONFIG
from etf.http import PacedClient
from etf.ledger.requests import RequestLedger
from etf.paths import REPORTS
from etf.preperiod import is_pre_period
from etf.preperiod_prices import daily_volatility, pre_period_closes

REPORT = REPORTS / "stage_a2" / "preperiod_inputs.json"

# The source study's own sample start, and one millisecond inside the boundary.
STUDY_START = datetime(2024, 1, 11, tzinfo=UTC)
BOUNDARY_MS = CONFIG.pre_period_end_ms


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    client = PacedClient(RequestLedger())

    response = client.post_json(
        CONFIG.hyperliquid_info_url,
        {
            "type": "candleSnapshot",
            "req": {
                "coin": CONFIG.perp_coin,
                "interval": "1d",
                "startTime": utc_ms(STUDY_START),
                # The last fully-closed pre-period daily candle. Its close
                # stamp is 2025-04-30T23:59:59.999Z, one millisecond inside.
                "endTime": BOUNDARY_MS - 1,
            },
        },
        source="venue",
        endpoint="venue.candleSnapshot",
    )
    closes = pre_period_closes(response.body)
    vol = daily_volatility(closes)
    print(
        f"pre-period daily volatility: sd = {vol.daily_sd:.6f} on n = {vol.n_returns} returns, "
        f"{datetime.fromtimestamp(vol.first_close_ms / 1000, UTC).date()} to "
        f"{datetime.fromtimestamp(vol.last_close_ms / 1000, UTC).date()}"
    )

    rates: list[float] = []
    cursor = utc_ms(STUDY_START)
    pages = 0
    while cursor < BOUNDARY_MS:
        page = client.post_json(
            CONFIG.hyperliquid_info_url,
            {
                "type": "fundingHistory",
                "coin": CONFIG.perp_coin,
                "startTime": cursor,
                "endTime": BOUNDARY_MS - 1,
            },
            source="venue",
            endpoint="venue.fundingHistory",
        )
        if page.status != 200:
            print(f"funding page at {cursor} returned HTTP {page.status}; recorded, stopping")
            break
        rows = funding_rows(page.body)
        if not rows:
            break
        pages += 1
        for row in rows:
            # Belt and braces: the reader already gated these, and the pin is
            # asserted again here so a widened gate cannot pass unnoticed.
            if not is_pre_period(row.time_ms):
                raise RuntimeError(
                    f"a funding row stamped {row.time_ms} reached the pre-period sum; "
                    "the carve-out gate did not hold"
                )
            if isinstance(row.rate, float):
                rates.append(row.rate)
        last = rows[-1].time_ms
        if len(rows) < 500 or last <= cursor:
            break
        cursor = last + 1

    if len(rates) < 24:
        print(f"only {len(rates)} pre-period funding hours served; recording the absence")
        return 1
    mean_hourly = statistics.fmean(rates)
    daily_sum = mean_hourly * 24
    print(
        f"pre-period funding: mean hourly rate {mean_hourly:.8f} on n = {len(rates)} hours "
        f"across {pages} pages; 24-hour hold sum {daily_sum:.6f}"
    )

    out = {
        "measured_at": iso_z(now_utc()),
        "carve_out_boundary_ms": BOUNDARY_MS,
        "carve_out_boundary": CONFIG.pre_period_end_date,
        "window_start": iso_z(STUDY_START),
        "daily_sd": vol.daily_sd,
        "n_volatility_returns": vol.n_returns,
        "first_close_ms": vol.first_close_ms,
        "last_close_ms": vol.last_close_ms,
        "mean_hourly_funding_rate": mean_hourly,
        "daily_funding_sum": daily_sum,
        "n_funding_hours": len(rates),
        "funding_pages": pages,
        "annualized_funding_pct": mean_hourly * 24 * 365 * 100,
    }
    REPORT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
