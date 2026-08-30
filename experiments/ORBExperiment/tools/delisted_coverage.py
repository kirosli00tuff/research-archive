"""A.1 TASK 6 — delisted-name coverage, measured.

**A reference row costs nothing. A served bar is the thing the experiment
needs.** A universe missing its delisted names is survivor-only, and every
downstream figure computed on it is inflated beyond recovery — which is why
Section 0 fires **BLOCKED-3** at zero delisted names with intraday history, at
any power.

**Two questions, asked separately because they have different answers.**

1. **Enumeration.** How many US common stocks carry a delisting date inside
   2016-01-04 to 2026-06-30, and how are they spread across the years?
2. **Intraday service.** For a sample of those names, are **one-minute bars
   actually served** for sessions before the delisting, or is the name merely a
   row in a listing table?

**The sample is drawn before any bar is requested, by a rule fixed in this
file**: sort by delisting date then ticker, and take a **systematic sample at a
fixed stride**. It is deterministic, reproducible, and blind to every priced
value — nothing about which names are drawn depends on what the bars contain.

The probe session is **five sessions before the delisting date**, because a name
frequently serves nothing on its own final day and a last-day miss would be read
as an absent history.

**Readable fields only:** ticker, delisting date, status code and bar count.
"""

from __future__ import annotations

import collections
import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import send, wire, write_report

from orb.calendar import sessions
from orb.comparator import count_bars
from orb.config import CONFIG
from orb.integrity import IntegrityVerdict
from orb.redact import say
from orb.vendors import (
    alpaca_minute_bars,
    consolidated_feed,
    massive_delisted,
    massive_minute_bars,
)

ALPACA_SAMPLE = 120
"""Enough to reach the registered PASS bar of 100 by measurement rather than by
extrapolation. A rate measured on 20 names and multiplied up is a synthesized
count, and standing rule 5 forbids one."""

MASSIVE_SAMPLE = 20
"""The prompt's sample size. Massive's measured reach starts 2024-08-29, so most
delisted names in the window are out of reach **by construction** — the sample
exists to confirm the reach finding applies to delisted names too, not to reach
a threshold it structurally cannot reach."""

SESSIONS_BEFORE_DELISTING = 5
MAX_ENUMERATION_PAGES = 40


def session_before(day: date, back: int) -> date | None:
    """The n-th registered regular session strictly before ``day``."""
    window = [
        s.day for s in sessions(day - timedelta(days=45), day - timedelta(days=1))
    ]
    if len(window) < back:
        return None
    return window[-back]


def main() -> int:
    store, client, seal = wire()
    window_start = CONFIG.in_sample_start
    window_end = CONFIG.holdout_end

    # --- 1. enumeration, from Massive's reference endpoint -------------
    rows: list[dict[str, str]] = []
    cursor: str | None = None
    pages = 0
    while pages < MAX_ENUMERATION_PAGES:
        request = (
            massive_delisted(store, cursor_url=cursor)
            if cursor
            else massive_delisted(
                store, delisted_after=window_start, delisted_before=window_end
            )
        )
        response = send(client, request)
        seal.store(f"task6_reference_page{pages:02d}.raw", response.body)
        if not (200 <= response.status_code < 300):
            say(f"enumeration stopped at page {pages}: http={response.status_code}")
            say(f"  refusal: {response.refusal_fragment(300)}")
            break
        envelope = json.loads(response.body)
        page_rows = envelope.get("results", [])
        for row in page_rows:
            ticker = row.get("ticker")
            delisted = row.get("delisted_utc")
            if isinstance(ticker, str) and isinstance(delisted, str):
                rows.append({"ticker": ticker, "delisted_utc": delisted})
        pages += 1
        say(f"  page {pages:02d}: {len(page_rows)} rows, running total {len(rows)}")
        cursor = envelope.get("next_url")
        if not cursor:
            break

    by_year: collections.Counter[int] = collections.Counter()
    for row in rows:
        by_year[int(row["delisted_utc"][:4])] += 1
    say(f"enumerated delisted common stocks, n = {len(rows)}, pages = {pages}")
    say(f"  per year: {dict(sorted(by_year.items()))}")

    # --- 2. the sample, drawn before any bar is requested --------------
    ordered = sorted(rows, key=lambda r: (r["delisted_utc"], r["ticker"]))
    total = len(ordered)

    def systematic(size: int) -> list[dict[str, str]]:
        if total == 0:
            return []
        stride = max(1, total // size)
        picked = ordered[::stride][:size]
        return picked

    alpaca_sample = systematic(ALPACA_SAMPLE)
    massive_pool = [r for r in ordered if r["delisted_utc"][:10] >= "2024-08-29"]
    massive_stride = max(1, len(massive_pool) // MASSIVE_SAMPLE) if massive_pool else 1
    massive_sample = massive_pool[::massive_stride][:MASSIVE_SAMPLE]
    say(
        f"sample drawn: alpaca n = {len(alpaca_sample)}, "
        f"massive n = {len(massive_sample)} (pool inside Massive's measured "
        f"reach: {len(massive_pool)})"
    )

    # --- 3. intraday service, measured per vendor ----------------------
    checks: list[dict[str, object]] = []

    def check(vendor: str, entry: dict[str, str]) -> bool:
        delisted_day = date.fromisoformat(entry["delisted_utc"][:10])
        probe_day = session_before(delisted_day, SESSIONS_BEFORE_DELISTING)
        if probe_day is None:
            return False
        iso = probe_day.isoformat()
        ticker = entry["ticker"]
        if vendor == "massive":
            request = massive_minute_bars(store, ticker, iso, iso)
        else:
            request = alpaca_minute_bars(
                store,
                ticker,
                f"{iso}T00:00:00Z",
                f"{iso}T23:59:59Z",
                feed=consolidated_feed(),
            )
        response = send(client, request)
        record = seal.store(f"task6_{vendor}_{ticker}_{iso}.raw", response.body)
        counted = count_bars(response.body)
        served = 200 <= response.status_code < 300 and counted > 0
        checks.append(
            {
                "vendor": vendor,
                "ticker": ticker,
                "delisted_utc": entry["delisted_utc"],
                "probe_session": iso,
                "status_code": response.status_code,
                "bar_count": counted,
                "served": served,
                "health": response.health.value,
                "sha256": record.sha256,
                "body_redacted": (
                    "<served payload, not recorded: a bar value never leaves the seal>"
                    if 200 <= response.status_code < 300
                    else response.refusal_fragment(300)
                ),
            }
        )
        return served

    say("checking Alpaca …")
    alpaca_served = sum(check("alpaca", e) for e in alpaca_sample)
    say(f"  alpaca: {alpaca_served} of {len(alpaca_sample)} names served intraday bars")

    say("checking Massive …")
    massive_served = sum(check("massive", e) for e in massive_sample)
    say(
        f"  massive: {massive_served} of {len(massive_sample)} names served "
        "intraday bars, inside its measured reach"
    )

    def verdict(count: int) -> str:
        if count >= CONFIG.delisted_pass_min_count:
            return IntegrityVerdict.PASS.value
        if count >= CONFIG.delisted_partial_min_count:
            return IntegrityVerdict.PARTIAL.value
        return IntegrityVerdict.FAIL.value

    findings = {
        "window": [window_start, window_end],
        "enumeration_source": "massive:/v3/reference/tickers?active=false&type=CS",
        "enumerated_delisted_names": len(rows),
        "enumeration_pages": pages,
        "per_year": dict(sorted(by_year.items())),
        "alpaca": {
            "sample_size": len(alpaca_sample),
            "names_with_intraday_history": alpaca_served,
            "served_share": (
                alpaca_served / len(alpaca_sample) if alpaca_sample else 0.0
            ),
            "registered_verdict_on_measured_count": verdict(alpaca_served),
        },
        "massive": {
            "sample_size": len(massive_sample),
            "pool_inside_measured_reach": len(massive_pool),
            "names_with_intraday_history": massive_served,
            "served_share": (
                massive_served / len(massive_sample) if massive_sample else 0.0
            ),
            "registered_verdict_on_measured_count": verdict(massive_served),
        },
        "checks": checks,
        "enumerated_names": ordered,
    }
    write_report("task6_delisted.json", findings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
