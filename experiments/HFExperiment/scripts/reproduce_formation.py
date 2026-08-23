"""Stage A.1 Task 4: reproduce the universe and the 12-1 formation.

Reads exactly two things from AiTrader, both read-only: analysis_bars.db
and the already copied universe rule. Verifies the database hash is
unchanged afterward from the shell, not here.

Outputs land in reports/stage_a1/:
  universe_check.json   reproduced top-500 vs recorded universe_membership
  formations.json       books at widths 5, 20, 50 for the last 7 formations
  formations.md         the same, readable, with churn and median price

Reports no return of any kind. Membership, churn, and share price are
inputs. A return is an outcome.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from hfexperiment import formation as fm
from hfexperiment import universe as uv
from hfexperiment.dbaccess import open_readonly

REPORT_DIR = Path(__file__).resolve().parent.parent / "reports/stage_a1"
RULE = uv.RuleParams()
WIDTHS = (5, 20, 50)
# The last 7 formations. Books for all 7, churn for the last 6.
RECENT_FORMATIONS = 7
# Universe reproduction is checked at the recent formations plus these
# historical spot checks across the recorded range.
SPOT_CHECKS = ("2016-04-01", "2020-03-02", "2024-01-02")


def load_calendar(con) -> list[str]:
    rows = con.execute("SELECT date FROM trading_calendar ORDER BY date").fetchall()
    return [r[0] for r in rows]


def load_assets(con) -> dict[str, tuple[str, str]]:
    """symbol -> (name, exchange) for fund classification."""
    rows = con.execute(
        "SELECT symbol, COALESCE(name,''), COALESCE(exchange,'') FROM universe_asset"
    ).fetchall()
    return {r[0]: (r[1], r[2]) for r in rows}


def compute_segments(con, session_index: dict[str, int],
                     pool: set[str]) -> dict[str, list[tuple[str, str]]]:
    """Listing segments per symbol from the full daily bar history."""
    segments: dict[str, list[tuple[str, str]]] = {}
    cur = con.execute(
        "SELECT symbol, substr(timestamp,1,10) FROM bars "
        "WHERE timeframe='1day' ORDER BY symbol, timestamp"
    )
    current_symbol: str | None = None
    dates: list[str] = []

    def flush() -> None:
        if current_symbol is None or current_symbol not in pool or not dates:
            return
        segs = uv.segment_series(dates, session_index)
        segments[current_symbol] = [(s.start_date, s.end_date) for s in segs]

    for symbol, date in cur:
        if symbol != current_symbol:
            flush()
            current_symbol = symbol
            dates = []
        dates.append(date)
    flush()
    return segments


def window_summaries(con, start: str, end: str, pool: set[str],
                     assets: dict[str, tuple[str, str]],
                     segments: dict[str, list[tuple[str, str]]]
                     ) -> list[uv.Candidate]:
    rows = con.execute(
        "SELECT symbol, substr(timestamp,1,10), close, volume FROM bars "
        "WHERE timeframe='1day' AND timestamp >= ? AND timestamp <= ? "
        "ORDER BY symbol, timestamp",
        (start, end + "T23:59:59Z"),
    ).fetchall()
    by_symbol: dict[str, tuple[list[float], list[float]]] = defaultdict(
        lambda: ([], [])
    )
    for symbol, _date, close, volume in rows:
        if symbol in pool:
            closes, volumes = by_symbol[symbol]
            closes.append(close)
            volumes.append(volume)
    candidates: list[uv.Candidate] = []
    for symbol, (closes, volumes) in by_symbol.items():
        name, exchange = assets.get(symbol, ("", ""))
        segs = segments.get(symbol, [])
        seg_break = any(
            i > 0 and start <= seg_start <= end
            for i, (seg_start, _seg_end) in enumerate(segs)
        )
        cand = uv.summarize_window(
            symbol, closes, volumes,
            is_fund=uv.classify_fund(name, exchange),
            segment_break_in_window=seg_break,
        )
        if cand is not None:
            candidates.append(cand)
    return candidates


def check_universe(con, members: list[uv.Member], formation_date: str) -> dict:
    recorded = con.execute(
        "SELECT symbol, rank, median_dollar_volume, median_close, window_bars "
        "FROM universe_membership WHERE rule=? AND formation_date=? "
        "ORDER BY rank",
        (RULE.rule_id, formation_date),
    ).fetchall()
    rec_by_symbol = {r[0]: r for r in recorded}
    mine_by_symbol = {m.candidate.symbol: m for m in members}
    missing = sorted(set(rec_by_symbol) - set(mine_by_symbol))
    extra = sorted(set(mine_by_symbol) - set(rec_by_symbol))
    value_mismatches = []
    rank_mismatches = []
    for sym, m in mine_by_symbol.items():
        rec = rec_by_symbol.get(sym)
        if rec is None:
            continue
        if m.rank != rec[1]:
            rank_mismatches.append((sym, m.rank, rec[1]))
        c = m.candidate
        if (abs(c.median_dollar_volume - rec[2]) > 1e-6 * max(1.0, abs(rec[2]))
                or abs(c.median_close - rec[3]) > 1e-9 * max(1.0, abs(rec[3]))
                or c.window_bars != rec[4]):
            value_mismatches.append(
                (sym, c.median_dollar_volume, rec[2], c.median_close, rec[3],
                 c.window_bars, rec[4])
            )
    return {
        "formation_date": formation_date,
        "recorded_rows": len(recorded),
        "reproduced_rows": len(members),
        "missing_from_reproduction": missing,
        "extra_in_reproduction": extra,
        "rank_mismatches": rank_mismatches[:20],
        "value_mismatches": value_mismatches[:20],
        "exact_match": (not missing and not extra and not rank_mismatches
                        and not value_mismatches),
    }


def closes_for_symbols(con, symbols: set[str], start: str, end: str
                       ) -> dict[str, list[tuple[str, float]]]:
    rows = con.execute(
        "SELECT symbol, substr(timestamp,1,10), close FROM bars "
        "WHERE timeframe='1day' AND timestamp >= ? AND timestamp <= ? "
        "ORDER BY symbol, timestamp",
        (start, end + "T23:59:59Z"),
    ).fetchall()
    out: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for symbol, date, close in rows:
        if symbol in symbols:
            out[symbol].append((date, close))
    return out


def median(values: list[float]) -> float:
    return uv.median(values)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    con = open_readonly()
    sessions = load_calendar(con)
    session_index = {d: i for i, d in enumerate(sessions)}
    assets = load_assets(con)

    # The horizon is the recorded round's own pull end, not the newest bar.
    # 1,535 symbols carry refreshed bars past the pull (the news-drift set),
    # and a universe computed on that partial pool would be garbage.
    pull_end = con.execute(
        "SELECT substr(value,1,10) FROM analysis_meta "
        "WHERE key='universe_pull_end'"
    ).fetchone()[0]
    usable_sessions = [d for d in sessions if d <= pull_end]
    all_formations = uv.formation_dates(usable_sessions, RULE)

    recorded_formations = [r[0] for r in con.execute(
        "SELECT DISTINCT formation_date FROM universe_membership WHERE rule=? "
        "ORDER BY formation_date", (RULE.rule_id,)).fetchall()]
    print(f"formation dates: reproduced {len(all_formations)}, "
          f"recorded {len(recorded_formations)}, "
          f"identical={all_formations == recorded_formations}")

    pool = {r[0] for r in con.execute("SELECT symbol FROM universe_asset")}
    print("computing listing segments from full bar history")
    segments = compute_segments(con, session_index, pool)
    print(f"segments computed for {len(segments)} symbols")

    recent = all_formations[-RECENT_FORMATIONS:]
    check_dates = list(SPOT_CHECKS) + recent
    universe_checks = []
    books: dict[str, dict[int, list[dict]]] = {}
    median_price: dict[str, dict[int, float]] = {}

    for f_date in check_dates:
        start, end = uv.window_bounds(usable_sessions, f_date,
                                      RULE.window_sessions)
        candidates = window_summaries(con, start, end, pool, assets, segments)
        members, _rejections = uv.rank_members(candidates, RULE)
        chk = check_universe(con, members, f_date)
        universe_checks.append(chk)
        print(f"universe {f_date}: exact_match={chk['exact_match']}")

        if f_date not in recent:
            continue

        far_anchor, near_anchor = fm.anchor_sessions(
            all_formations, f_date, usable_sessions)
        member_symbols = {m.candidate.symbol for m in members}
        fetch_start = sessions[max(0, session_index[far_anchor]
                                   - fm.MAX_ANCHOR_GAP_SESSIONS)]
        price_end = usable_sessions[usable_sessions.index(f_date) - 1]
        series = closes_for_symbols(con, member_symbols, fetch_start, price_end)

        entries: list[fm.MomentumEntry] = []
        exclusions: dict[str, int] = defaultdict(int)
        for sym in sorted(member_symbols):
            result = fm.momentum_for_symbol(
                sym, series.get(sym, []), far_anchor, near_anchor,
                session_index, segments=segments.get(sym))
            if isinstance(result, str):
                exclusions[result] += 1
            else:
                entries.append(result)

        last_close: dict[str, float] = {}
        for sym, bars in series.items():
            usable = [(d, c) for d, c in bars if d <= price_end]
            if usable:
                last_close[sym] = usable[-1][1]

        books[f_date] = {}
        median_price[f_date] = {}
        for width in WIDTHS:
            book = fm.form_book(entries, width)
            books[f_date][width] = [
                {"rank": i + 1, "symbol": e.symbol,
                 "momentum": round(e.momentum, 6),
                 "last_close": last_close.get(e.symbol)}
                for i, e in enumerate(book)
            ]
            prices = [last_close[e.symbol] for e in book
                      if e.symbol in last_close]
            median_price[f_date][width] = round(median(prices), 2)
        print(f"formation {f_date}: {len(entries)} ranked, "
              f"exclusions={dict(exclusions)}")

    churn: dict[int, dict[str, int]] = {w: {} for w in WIDTHS}
    for prev_date, cur_date in zip(recent, recent[1:], strict=False):
        for width in WIDTHS:
            prev_set = {e["symbol"] for e in books[prev_date][width]}
            cur_set = {e["symbol"] for e in books[cur_date][width]}
            churn[width][cur_date] = len(cur_set - prev_set)

    (REPORT_DIR / "universe_check.json").write_text(
        json.dumps(universe_checks, indent=1))
    (REPORT_DIR / "formations.json").write_text(json.dumps(
        {"rule": RULE.rule_id, "widths": list(WIDTHS),
         "formations": books, "churn": churn,
         "median_price": median_price}, indent=1))

    lines = ["# Stage A.1 formations, reproduced", "",
             f"Rule {RULE.rule_id}. Momentum 12-1 with skip month.",
             "Prices are adjusted closes as stored (adjustment=all as of the",
             "2026-07-24 pull), so recent closes sit near actual prints.", ""]
    lines.append("## Churn per month (names entering the book)")
    lines.append("")
    lines.append("| formation | width 5 | width 20 | width 50 |")
    lines.append("|---|---|---|---|")
    for cur_date in recent[1:]:
        lines.append(f"| {cur_date} | {churn[5][cur_date]} "
                     f"| {churn[20][cur_date]} | {churn[50][cur_date]} |")
    lines.append("")
    lines.append("## Median share price of the book at formation")
    lines.append("")
    lines.append("| formation | width 5 | width 20 | width 50 |")
    lines.append("|---|---|---|---|")
    for f_date in recent:
        mp = median_price[f_date]
        lines.append(f"| {f_date} | {mp[5]} | {mp[20]} | {mp[50]} |")
    lines.append("")
    for f_date in recent:
        lines.append(f"## {f_date}")
        lines.append("")
        for width in WIDTHS:
            symbols = ", ".join(e["symbol"] for e in books[f_date][width])
            lines.append(f"- width {width}: {symbols}")
        lines.append("")
    (REPORT_DIR / "formations.md").write_text("\n".join(lines))

    all_exact = all(c["exact_match"] for c in universe_checks)
    print(f"ALL UNIVERSE CHECKS EXACT: {all_exact}")
    con.close()


if __name__ == "__main__":
    main()
