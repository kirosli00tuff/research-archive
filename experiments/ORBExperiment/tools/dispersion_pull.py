"""A.1 TASK 5, phase 1 — the post-holdout pull, under the amended carve-out.

**This is the one task in this pass that points live machinery at real bars.**
Amendment 11 made the carve-out two-sided, and this pull reads the second half:
sessions **strictly after** ``CONFIG.holdout_end`` = 2026-06-30, enforced at
``CONFIG.post_holdout_start_ms`` = 2026-07-01T04:00:00.000Z, which is
2026-07-01T00:00:00.000 US Eastern (EDT, UTC-04:00).

**The boundary is enforced, not asserted.** Every requested window is passed
through ``orb.preperiod.require_pre_period`` — the two-sided check — before the
request is built, so a window that strayed into the sealed region would raise
rather than send.

**The last session pulled is the last CLOSED session.** ADR-016: the seal target
is the closed session, never the open one.

**The universe is a systematic sample, and it is price-blind.** The registered
universe is US common stock; the reference vendor's active-CS listing is walked
in full by cursor and **every k-th ticker** is taken, so the sample spreads
across the whole alphabet instead of collecting the first two hundred names
beginning with A. `bar_count per session` is the only served field consulted, and
it is on the readable field list.

**The session list actually pulled is recorded in the append-only ledger at the
time of the pull**, per Amendment 11, rather than fixed in advance anywhere.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import DATA, send, wire, write_report

from orb.calendar import sessions
from orb.comparator import count_bars
from orb.config import CONFIG
from orb.ledger import AppendOnlyLedger
from orb.preperiod import post_holdout_start_ms, require_pre_period
from orb.redact import say
from orb.vendors import (
    alpaca_minute_bars,
    consolidated_feed,
    massive_active_common,
)

FIRST_SESSION = date(2026, 7, 1)
LAST_CLOSED_SESSION = date(2026, 8, 28)
"""The last **closed** session. Today is 2026-08-29; ADR-016 forbids the open one."""

UNIVERSE_TARGET = 200
"""A systematic sample. Bounded by the registered daily cap, not by preference."""

REFERENCE_PAGE = 1000
MAX_REFERENCE_PAGES = 10
MAX_PAGES_PER_TICKER = 4


def main() -> int:
    boundary = post_holdout_start_ms()
    slice_sessions = list(sessions(FIRST_SESSION, LAST_CLOSED_SESSION))
    say(
        f"post-holdout slice: n = {len(slice_sessions)} sessions, "
        f"{slice_sessions[0].day} .. {slice_sessions[-1].day}; "
        f"carve-out boundary {boundary} (2026-07-01T04:00:00.000Z)"
    )

    # The boundary is enforced on every session before anything is requested.
    for session in slice_sessions:
        open_ms, _ = session.opening_range_utc()
        require_pre_period(open_ms, f"post-holdout pull, session {session.day}")

    # The request window opens exactly at the registered boundary instant, so
    # the vendor is never asked for a bar the carve-out does not permit.
    start_iso = (
        datetime.fromtimestamp(boundary / 1000, tz=UTC)
        .isoformat()
        .replace("+00:00", "Z")
    )
    end_iso = f"{LAST_CLOSED_SESSION.isoformat()}T23:59:59Z"

    store, client, seal = wire()

    # --- the price-blind systematic universe sample ----------------------
    pool: list[str] = []
    cursor: str | None = None
    pages = 0
    while pages < MAX_REFERENCE_PAGES:
        response = send(
            client,
            massive_active_common(store, limit=REFERENCE_PAGE, cursor_url=cursor),
        )
        seal.store(f"task5b_reference_page{pages:02d}.raw", response.body)
        pages += 1
        if not (200 <= response.status_code < 300):
            say(f"  reference page {pages} refused at {response.status_code}; stopping")
            break
        envelope = json.loads(response.body)
        for row in envelope.get("results", []):
            ticker = row.get("ticker")
            if isinstance(ticker, str) and row.get("type") == "CS":
                pool.append(ticker)
        cursor = envelope.get("next_url")
        if not isinstance(cursor, str):
            break
    pool = sorted(set(pool))
    say(
        f"reference listing walked: n = {len(pool)} active US common "
        f"stocks, {pages} pages"
    )

    if len(pool) <= UNIVERSE_TARGET:
        chosen = pool
        stride = 1
    else:
        stride = len(pool) // UNIVERSE_TARGET
        chosen = pool[::stride][:UNIVERSE_TARGET]
    say(
        f"systematic sample: every {stride}th ticker, "
        f"n = {len(chosen)} ({chosen[0]} .. {chosen[-1]})"
    )

    # --- the sealed pull --------------------------------------------------
    manifest: list[dict[str, object]] = []
    total_bars = 0
    served_tickers = 0
    for index, ticker in enumerate(chosen, start=1):
        token: str | None = None
        page = 0
        ticker_bars = 0
        while page < MAX_PAGES_PER_TICKER:
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
            name = f"task5b_{ticker}_page{page:02d}.raw"
            record = seal.store(name, response.body)
            counted = count_bars(response.body)
            ticker_bars += counted
            total_bars += counted
            token = None
            if 200 <= response.status_code < 300:
                envelope = json.loads(response.body)
                if isinstance(envelope, dict):
                    raw = envelope.get("next_page_token")
                    token = raw if isinstance(raw, str) else None
            manifest.append(
                {
                    "ticker": ticker,
                    "feed": request.feed,
                    "page": page,
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
        if ticker_bars > 0:
            served_tickers += 1
        if index % 25 == 0:
            say(f"  pulled {index}/{len(chosen)} tickers, {total_bars} bars so far")

    session_list = [s.day.isoformat() for s in slice_sessions]
    findings = {
        "kind": "post_holdout_carve_out_pull",
        "pulled_at": date.today().isoformat(),
        "primary_vendor": "alpaca",
        "feed": consolidated_feed(),
        "carve_out_boundary_ms": boundary,
        "carve_out_half": "post_holdout",
        "first_session": slice_sessions[0].day.isoformat(),
        "last_closed_session": slice_sessions[-1].day.isoformat(),
        "session_count": len(slice_sessions),
        "sessions": session_list,
        "half_sessions": [s.day.isoformat() for s in slice_sessions if s.is_half],
        "reference_pool_size": len(pool),
        "reference_pages": pages,
        "universe_stride": stride,
        "tickers": chosen,
        "ticker_count": len(chosen),
        "tickers_serving_at_least_one_bar": served_tickers,
        "files_stored": len(manifest),
        "bars_stored": total_bars,
        "relvol_lookback_sessions": CONFIG.relvol_lookback_sessions,
        "evaluable_sessions": len(slice_sessions) - CONFIG.relvol_lookback_sessions,
        "manifest": manifest,
    }
    write_report("task5b_post_holdout_pull.json", findings)

    # Amendment 11: the sessions used are recorded in the ledger at the time of
    # the computation, never fixed in advance.
    AppendOnlyLedger(DATA / "carve_out_reads.jsonl").append(
        {
            "kind": "carve_out_session_list",
            "half": "post_holdout",
            "boundary_ms": boundary,
            "sessions": session_list,
            "session_count": len(session_list),
            "tickers": len(chosen),
            "bars_stored": total_bars,
            "feed": consolidated_feed(),
        }
    )
    say(
        f"stored n = {len(manifest)} sealed files, {total_bars} bars, "
        f"{served_tickers} of {len(chosen)} tickers served at least one bar, "
        f"over n = {len(slice_sessions)} post-holdout sessions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
