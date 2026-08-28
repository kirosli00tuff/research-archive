"""Measure quoted spreads for the 2026-07-01 width-20 book from the tape.

Stage A.2 Task 2. The route is the one AiTrader already owns and used to
measure its per-tier tick multiples on 2026-07-29: Alpaca's HISTORICAL
consolidated quotes endpoint, feed=sip, which serves any window older than
about 15 minutes. Methodology copied from that measurement so the numbers
are comparable: three most recent complete sessions from trading_calendar,
three windows per session (after the open, mid, near the close), five
minute spans, up to 50 quotes per cell, and the same per-quote discard
taxonomy (crossed, locked, zero, no_size).

The names are the point. A.1 inherited a 15.8 to 50 bp band measured on a
stratified sample. This measures the actual book, which sits at the wide
end. No proxy substitutes: the entitlement probe uses AAPL to test
reachability only and its numbers never enter the output.

Run with AiTrader's interpreter so its credential resolver loads:

  ~/Documents/GitHub/AiTrader/.venv/bin/python \
      scripts/measure_book_spreads.py reports/stage_a2/book_spreads.json

Read-only everywhere. Reads the trading calendar through SQLite ro mode,
reads credentials through AiTrader's resolver, GETs historical quotes.
Writes one JSON file inside this repository and nothing else.
"""
from __future__ import annotations

import datetime
import json
import sqlite3
import statistics as st
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

AITRADER = Path.home() / "Documents/GitHub/AiTrader"
sys.path.insert(0, str(AITRADER))
from account_manager import credentials as cr  # noqa: E402

DB = AITRADER / "analysis_bars.db"
ET = ZoneInfo("America/New_York")

# The 2026-07-01 width-20 book, from reports/stage_a1/formations.md,
# reproduced against the recorded round in Stage A.1.
BOOK = (
    "WOLF", "AXTI", "SNDK", "BE", "LITE", "PL", "WDC", "MU", "CIEN",
    "ONDS", "HUT", "MXL", "AAOI", "STX", "TSEM", "WULF", "DOCN", "INTC",
    "CIFR", "VIAV",
)

N_SESSIONS = 3
WINDOWS = ((14, 0), (16, 30), (19, 30))  # UTC
WINDOW_SPAN_S = 300
QUOTES_PER_CELL = 50
TICK = 0.01
SLEEP_S = 0.35  # gentler than the 200 req/min limit needs, on purpose


def _hdr() -> dict[str, str]:
    return {
        "APCA-API-KEY-ID": cr.get_credential("alpaca_paper_key"),
        "APCA-API-SECRET-KEY": cr.get_credential("alpaca_paper_secret"),
    }


def complete_sessions(n: int) -> list[dict]:
    """The n most recent complete sessions with UTC open and close."""
    today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = conn.execute(
        "SELECT date, open, close FROM trading_calendar WHERE date < ? "
        "ORDER BY date DESC LIMIT ?", (today, n)).fetchall()
    conn.close()
    out = []
    for date, o, c in rows:
        y, m, d = (int(x) for x in date.split("-"))
        oh, om = (int(x) for x in o.split(":"))
        ch, cm = (int(x) for x in c.split(":"))
        out.append({
            "date": date,
            "open_utc": datetime.datetime(y, m, d, oh, om, tzinfo=ET)
            .astimezone(datetime.UTC),
            "close_utc": datetime.datetime(y, m, d, ch, cm, tzinfo=ET)
            .astimezone(datetime.UTC),
        })
    return sorted(out, key=lambda s: s["date"])


def fetch_quotes(sym: str, start: datetime.datetime,
                 end: datetime.datetime) -> list[dict] | None:
    """Up to QUOTES_PER_CELL sip quotes in [start, end). None on failure."""
    url = (f"https://data.alpaca.markets/v2/stocks/{sym}/quotes"
           f"?start={start:%Y-%m-%dT%H:%M:%SZ}&end={end:%Y-%m-%dT%H:%M:%SZ}"
           f"&limit={QUOTES_PER_CELL}&feed=sip")
    for attempt in (1, 2):
        try:
            req = urllib.request.Request(url, headers=_hdr())
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode()).get("quotes") or []
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:
                time.sleep(20)
                continue
            return None
        except Exception:
            return None
    return None


def cell_median(quotes: list[dict], disc: dict) -> dict | None:
    """Median spread over one cell's usable quotes, or None."""
    ticks, bps, mids = [], [], []
    for q in quotes:
        bid, ask = q.get("bp"), q.get("ap")
        bs, as_ = q.get("bs", 0), q.get("as", 0)
        if not bid or not ask or bid <= 0 or ask <= 0:
            disc["zero"] += 1
            continue
        if ask < bid:
            disc["crossed"] += 1
            continue
        if ask == bid:
            disc["locked"] += 1
            continue
        if not bs or not as_:
            disc["no_size"] += 1
            continue
        mid = (bid + ask) / 2.0
        ticks.append((ask - bid) / TICK)
        bps.append((ask - bid) / mid * 1e4)
        mids.append(mid)
    if not ticks:
        return None
    return {"ticks": st.median(ticks), "bp": st.median(bps),
            "mid": st.median(mids), "n_quotes": len(ticks)}


def entitlement_probe(session: dict) -> tuple[bool, str]:
    """Historical sip reachable on this key. AAPL tests reachability only."""
    y, m, d = (int(x) for x in session["date"].split("-"))
    w0 = datetime.datetime(y, m, d, 14, 0, tzinfo=datetime.UTC)
    quotes = fetch_quotes("AAPL", w0, w0 + datetime.timedelta(minutes=5))
    if quotes is None:
        return False, "historical sip request failed"
    if not quotes:
        return False, "historical sip served zero probe quotes"
    return True, f"sip ok, {len(quotes)} probe quotes at {session['date']}"


def pctile(sorted_vals: list[float], p: float) -> float:
    return sorted_vals[int(p * (len(sorted_vals) - 1))]


def main() -> None:
    out_path = Path(sys.argv[1])
    sessions = complete_sessions(N_SESSIONS)
    if len(sessions) < N_SESSIONS:
        print(f"REFUSING: only {len(sessions)} complete sessions")
        sys.exit(2)
    ok, detail = entitlement_probe(sessions[-1])
    if not ok:
        print(f"REFUSING: {detail}. Record spreads UNMEASURED and carry "
              f"the inherited band's upper bound.")
        sys.exit(3)
    print(f"entitlement: {detail}")
    print(f"sessions: {[s['date'] for s in sessions]}")

    now = datetime.datetime.now(datetime.UTC)
    disc = {"crossed": 0, "locked": 0, "zero": 0, "no_size": 0,
            "http": 0, "no_quotes": 0, "all_filtered": 0}
    cells: dict[str, list[dict]] = {sym: [] for sym in BOOK}
    for sess in sessions:
        for h, m in WINDOWS:
            y, mo, d = (int(x) for x in sess["date"].split("-"))
            w0 = datetime.datetime(y, mo, d, h, m,
                                   tzinfo=datetime.UTC)
            w1 = w0 + datetime.timedelta(seconds=WINDOW_SPAN_S)
            if w0 < sess["open_utc"] or w1 > sess["close_utc"]:
                continue
            if (now - w1).total_seconds() < 16 * 60:
                continue
            for sym in BOOK:
                quotes = fetch_quotes(sym, w0, w1)
                time.sleep(SLEEP_S)
                if quotes is None:
                    disc["http"] += 1
                    continue
                if not quotes:
                    disc["no_quotes"] += 1
                    continue
                cell = cell_median(quotes, disc)
                if cell is None:
                    disc["all_filtered"] += 1
                    continue
                cell.update(session=sess["date"], window=f"{h:02d}:{m:02d}Z")
                cells[sym].append(cell)

    per_name = {}
    unmeasured = []
    for sym in BOOK:
        rows = cells[sym]
        if not rows:
            unmeasured.append(sym)
            continue
        per_name[sym] = {
            "n_cells": len(rows),
            "median_bp": st.median(r["bp"] for r in rows),
            "median_ticks": st.median(r["ticks"] for r in rows),
            "median_mid": st.median(r["mid"] for r in rows),
        }

    med_bps = sorted(v["median_bp"] for v in per_name.values())
    dist = {
        "n_names_measured": len(med_bps),
        "min_bp": med_bps[0], "p25_bp": pctile(med_bps, 0.25),
        "median_bp": st.median(med_bps), "p75_bp": pctile(med_bps, 0.75),
        "p90_bp": pctile(med_bps, 0.90), "max_bp": med_bps[-1],
    } if med_bps else {}

    print(f"\n{'symbol':<7}{'cells':>6}{'mid':>9}{'ticks':>8}{'bp':>8}")
    for sym in BOOK:
        if sym in per_name:
            v = per_name[sym]
            print(f"{sym:<7}{v['n_cells']:>6}{v['median_mid']:>9.2f}"
                  f"{v['median_ticks']:>8.2f}{v['median_bp']:>8.2f}")
        else:
            print(f"{sym:<7}{'UNMEASURED':>30}")
    if dist:
        print(f"\ndistribution of per-name median spread bp: "
              f"min {dist['min_bp']:.1f}  p25 {dist['p25_bp']:.1f}  "
              f"med {dist['median_bp']:.1f}  p75 {dist['p75_bp']:.1f}  "
              f"p90 {dist['p90_bp']:.1f}  max {dist['max_bp']:.1f}")
    print(f"discards: {disc}")
    if unmeasured:
        print(f"UNMEASURED names: {unmeasured}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({
            "measured_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "feed": "sip",
            "endpoint": "/v2/stocks/{symbol}/quotes (historical)",
            "book_formation": "2026-07-01 width 20",
            "sessions": [s["date"] for s in sessions],
            "windows": [f"{h:02d}:{m:02d}Z" for h, m in WINDOWS],
            "per_name": per_name,
            "unmeasured": unmeasured,
            "distribution": dist,
            "discarded": disc,
        }, f, indent=1)
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
