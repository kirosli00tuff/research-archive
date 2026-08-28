#!/usr/bin/env python
"""Fetch the real 2026-08-03 formation into C.1's own store.

The B.1 bar store records formations only from the 2026-09-01 series
start, so the 2026-08-03 formation cannot come from it. This script
computes it fresh through the registered rule with HFExperiment's own
Alpaca keys, into data/c1_formation.db, a store this stage owns. The
B.1 store, ledgers, and timer are not touched.

Evidence lands in reports/stage_c1/formation_2026-08-03.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import hfexperiment.alpaca_source as alpaca_source  # noqa: E402
from hfexperiment.accrual import WIDTHS  # noqa: E402
from hfexperiment.alpaca_source import AlpacaSource, SourceError  # noqa: E402

# The keys in .env are paper keys, and Alpaca serves trading-API
# endpoints for paper keys from paper-api.alpaca.markets. B.1 pinned
# the live base and this stage may not touch B.1 source, so the
# override is confined to this script. The B.1 defect is recorded in
# progress.md for a session authorized to fix it before 2026-09-01.
alpaca_source.TRADE_BASE = "https://paper-api.alpaca.markets"
from hfexperiment.barstore import BarStore  # noqa: E402
from hfexperiment.envfile import load_credentials  # noqa: E402
from hfexperiment.formationrun import FormationError, run_formation  # noqa: E402

FORMATION_DATE = "2026-08-03"
CAL_START = "2025-04-01"
CAL_END = "2026-08-10"
STORE_PATH = ROOT / "data" / "c1_formation.db"
OUT_PATH = ROOT / "reports" / "stage_c1" / "formation_2026-08-03.json"


def main() -> int:
    creds = load_credentials(ROOT / ".env")
    source = AlpacaSource(creds["ALPACA_KEY_ID"], creds["ALPACA_SECRET_KEY"])
    store = BarStore(STORE_PATH)
    run_utc = "fetch-c1"
    try:
        calendar = source.calendar(CAL_START, CAL_END)
    except SourceError as err:
        print(f"CALENDAR FAILED: {err}", file=sys.stderr)
        return 1
    store.append_sessions(calendar, run_utc)
    sessions = store.session_dates(CAL_START, CAL_END)
    print(f"calendar: {len(sessions)} sessions "
          f"{sessions[0]}..{sessions[-1]}")
    try:
        result = run_formation(
            store, source, sessions, FORMATION_DATE, list(WIDTHS), run_utc
        )
    except (FormationError, SourceError) as err:
        print(f"FORMATION FAILED: {err}", file=sys.stderr)
        return 1
    entry_closes = {
        sym: store.last_close_at_or_before(sym, FORMATION_DATE)
        for sym in result.books[20]
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(
            {
                "formation_date": FORMATION_DATE,
                "rule": "U-LIQ-500-stk-w60-m40-p5, momentum 12-1 skip 1",
                "n_members": result.n_candidates,
                "n_measurable": result.n_measurable,
                "books": result.books,
                "width20_entry_closes": entry_closes,
                "source": "fresh Alpaca query, adjustment=all, C.1 store",
            },
            indent=1,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"width 20 book: {result.books[20]}")
    print(f"wrote {OUT_PATH}")
    store.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
