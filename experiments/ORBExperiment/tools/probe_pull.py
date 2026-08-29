"""A.1 TASK 9 — the registered probe slice, sealed, and the revision clock started.

**This is the pull whose identical repetition, at least 14 calendar days later,
measures the bar revision rate.** That measurement is the one this repository
turns on: MLCryptoEngine H11 died on a **measured 75-day publication lag** in a
source with whole-file regeneration that revised past rows, and the lag was
**discovered rather than registered**. Here it is registered first.

**Preconditions, all three measured before this runs:** A.1 TASK 5 reach covers
the registered windows (**Alpaca, 2016-01-04, 1,762/1,762 and 875/875**), A.1
TASK 6 delisted coverage is **`PASS` at 203 names, n = 229**, and the A.1 TASK 4
tape verdict is **`SAME_TAPE`**, which is not blocking.

**Nothing is parsed outside the readable field list.** The pull stores raw bytes
through the sealed writer, records a SHA-256 per file in the append-only ledger,
and reads only **bar count** and **page token presence** from each response — the
first is readable, the second is an envelope fact and not a bar.

**Selection reads no price.** The 40 tickers are the alphabetically-first
**active US common stocks** from the reference vendor that **serve at least one
bar** on a fixed reference session. `bar_count per session` is on the readable
field list, so a bar-count screen is price-blind by construction.

**Request shape, and why it is not one file per session-ticker pair.** The
registered granularity is the session-ticker pair, and 40 × 60 = **2,400**
single-session requests would exceed the registered daily cap and take 40
minutes. Each ticker is instead pulled in **12 chunks of 5 consecutive
sessions**, whose boundaries are **session dates rather than page tokens** — a
token-paginated boundary moves when bars are added or removed, so a re-pull
would differ from the original for a reason that is not a revision. The
**bar-level** comparison at re-pull time re-keys to session-ticker pairs from
the readable timestamp, so the registered `session_ticker_pairs_compared = 2,400`
is preserved.
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import send, wire, write_report

from orb.calendar import sessions
from orb.comparator import count_bars
from orb.config import CONFIG
from orb.redact import say
from orb.vendors import (
    alpaca_minute_bars,
    consolidated_feed,
    massive_active_common,
)

CHUNK_SESSIONS = 5
CANDIDATE_POOL = 1000
MAX_PAGES_PER_CHUNK = 6


def slice_sessions(today: date) -> list[date]:
    """The registered probe slice: 60 consecutive regular sessions ending at
    least ``probe_min_age_days`` calendar days before today."""
    latest = today - timedelta(days=CONFIG.probe_min_age_days)
    days = [s.day for s in sessions(latest - timedelta(days=200), latest)]
    return days[-CONFIG.probe_sessions :]


def main() -> int:
    store, client, seal = wire()
    today = date.today()
    slice_days = slice_sessions(today)
    say(
        f"probe slice: n = {len(slice_days)} sessions, "
        f"{slice_days[0]} .. {slice_days[-1]} (today {today}, "
        f"min age {CONFIG.probe_min_age_days} days)"
    )

    # --- 1. the candidate pool, from the reference vendor, price-blind ---
    reference = send(
        client,
        massive_active_common(store, limit=CANDIDATE_POOL),
    )
    seal.store("task9_reference_pool.raw", reference.body)
    pool: list[str] = []
    if 200 <= reference.status_code < 300:
        envelope = json.loads(reference.body)
        for row in envelope.get("results", []):
            ticker = row.get("ticker")
            kind = row.get("type")
            if isinstance(ticker, str) and kind == "CS":
                pool.append(ticker)
    pool.sort()
    say(f"candidate pool from the reference vendor: n = {len(pool)}")

    # --- 2. the bar-count screen: readable, price-blind ------------------
    reference_session = slice_days[-1].isoformat()
    chosen: list[str] = []
    screen: list[dict[str, object]] = []
    for ticker in pool:
        if len(chosen) >= CONFIG.probe_tickers:
            break
        response = send(
            client,
            alpaca_minute_bars(
                store,
                ticker,
                f"{reference_session}T00:00:00Z",
                f"{reference_session}T23:59:59Z",
                feed=consolidated_feed(),
                limit=10000,
            ),
        )
        counted = count_bars(response.body)
        screen.append(
            {
                "ticker": ticker,
                "reference_session": reference_session,
                "status_code": response.status_code,
                "bar_count": counted,
                "admitted": counted > 0,
            }
        )
        if 200 <= response.status_code < 300 and counted > 0:
            chosen.append(ticker)
    say(
        f"bar-count screen: n = {len(screen)} candidates examined, "
        f"{len(chosen)} admitted"
    )
    if len(chosen) < CONFIG.probe_tickers:
        say(
            f"REFUSING: the screen admitted {len(chosen)} of the registered "
            f"{CONFIG.probe_tickers} tickers. A short slice is a recorded "
            "absence, never a quietly smaller probe."
        )
        return 78

    # --- 3. the sealed pull ---------------------------------------------
    chunks = [
        slice_days[i : i + CHUNK_SESSIONS]
        for i in range(0, len(slice_days), CHUNK_SESSIONS)
    ]
    manifest: list[dict[str, object]] = []
    total_bars = 0
    truncated_chunks = 0
    for ticker in chosen:
        for index, chunk in enumerate(chunks):
            start_iso = f"{chunk[0].isoformat()}T00:00:00Z"
            end_iso = f"{chunk[-1].isoformat()}T23:59:59Z"
            token: str | None = None
            page = 0
            while page < MAX_PAGES_PER_CHUNK:
                request = alpaca_minute_bars(
                    store,
                    ticker,
                    start_iso,
                    end_iso,
                    feed=consolidated_feed(),
                    limit=10000,
                    page_token=token,
                )
                response = send(client, request)
                name = f"task9_{ticker}_chunk{index:02d}_page{page:02d}.raw"
                record = seal.store(name, response.body)
                counted = count_bars(response.body)
                total_bars += counted
                token = None
                if 200 <= response.status_code < 300:
                    envelope = json.loads(response.body)
                    if isinstance(envelope, dict):
                        raw_token = envelope.get("next_page_token")
                        token = raw_token if isinstance(raw_token, str) else None
                manifest.append(
                    {
                        "ticker": ticker,
                        "feed": request.feed,
                        "chunk_index": index,
                        "page": page,
                        "sessions": [d.isoformat() for d in chunk],
                        "start_iso": start_iso,
                        "end_iso": end_iso,
                        "stored_file": name,
                        "sha256": record.sha256,
                        "byte_count": record.byte_count,
                        "bar_count": counted,
                        "status_code": response.status_code,
                        "continued": token is not None,
                    }
                )
                page += 1
                if token is None:
                    break
            if page > 1:
                truncated_chunks += 1
        say(f"  pulled {ticker}: {len(chunks)} chunks")

    earliest_repull = today + timedelta(days=CONFIG.revision_repull_wait_days)
    findings = {
        "pulled_at": today.isoformat(),
        "primary_vendor": "alpaca",
        "feed": consolidated_feed(),
        "sessions": [d.isoformat() for d in slice_days],
        "session_count": len(slice_days),
        "tickers": chosen,
        "ticker_count": len(chosen),
        "session_ticker_pairs": len(slice_days) * len(chosen),
        "chunk_sessions": CHUNK_SESSIONS,
        "chunks_per_ticker": len(chunks),
        "files_stored": len(manifest),
        "bars_stored": total_bars,
        "chunks_needing_more_than_one_page": truncated_chunks,
        "registered_wait_days": CONFIG.revision_repull_wait_days,
        "earliest_eligible_repull": earliest_repull.isoformat(),
        "screen": screen,
        "manifest": manifest,
    }
    write_report("task9_probe_manifest.json", findings)
    say(
        f"stored n = {len(manifest)} sealed files, {total_bars} bars, "
        f"{len(chosen)} tickers x {len(slice_days)} sessions = "
        f"{len(slice_days) * len(chosen)} session-ticker pairs"
    )
    say(f"EARLIEST ELIGIBLE RE-PULL: {earliest_repull.isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
