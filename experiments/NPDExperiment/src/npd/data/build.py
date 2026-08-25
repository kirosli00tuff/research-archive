"""Stage B.0. Build the whole data layer into the repository own store.

Runs in one command and is idempotent. Order matters and is fixed here.

    1. extract bars and the session calendar from the read-only source
    2. reproduce every formation the pipeline needs, and verify each one
       against the source own stored membership
    3. draw panels, compute feature blocks, build anonymization mappings
    4. compute forward returns and route them to the fit store or the sealed
       store by date
    5. fit the logistic baseline once on the fit period, then freeze it
    6. compute all three baseline rankings for every window day

Nothing here reads a window forward return. The sealed store is written and
never queried.
"""

from __future__ import annotations

import datetime as dt
import sys
from dataclasses import dataclass, field

from npd.absence import Maybe
from npd.baselines import logistic as logistic_baseline
from npd.baselines.logistic import FIT_END, FIT_START, LOGISTIC, FittedLogistic
from npd.baselines.mom_12_1 import (
    LOOKBACK_SESSIONS,
    MOM_12_1,
    SKIP_SESSIONS,
    momentum_12_1,
    rank_mom_12_1,
)
from npd.baselines.sign_last import SIGN_LAST, rank_sign_last
from npd.callstate import CallState
from npd.config import CONFIG
from npd.data import anonymize, extract, forward_returns, panel, series
from npd.data.features import MAX_LOOKBACK, cross_sectional_z, is_complete, raw_block
from npd.data.formations import PARAMS, build_formation, governing_formation, verify_against_source
from npd.data.store import clear_derived, open_store, record_day_state, session_index, set_meta
from npd.data.universe import formation_dates
from npd.window import derive_window

HORIZONS = (CONFIG.secondary_horizon_sessions, CONFIG.primary_horizon_sessions)


@dataclass(slots=True)
class BuildReport:
    extract: extract.ExtractReport | None = None
    formations_built: int = 0
    formations_verified: int = 0
    formation_failures: list[str] = field(default_factory=list)
    panels_by_month: dict[str, int] = field(default_factory=dict)
    fit_days: int = 0
    window_days: int = 0
    window_panels: int = 0
    window_no_data: int = 0
    baseline_days: dict[str, int] = field(default_factory=dict)
    forward_fit_rows: int = 0
    forward_sealed_rows: int = 0
    forward_absent_rows: int = 0
    logistic_digest: str = ""
    seconds: float = 0.0


def _has_span(store: series.SeriesStore, symbol: str, lo: int, hi: int) -> bool:
    """Whether the symbol traded every session in [lo, hi]."""
    import numpy as np

    positions = store.idx.get(symbol)
    if positions is None or lo < 0:
        return False
    a = int(np.searchsorted(positions, lo, side="left"))
    b = int(np.searchsorted(positions, hi, side="right"))
    return (b - a) == (hi - lo + 1)


def _has_session(store: series.SeriesStore, symbol: str, i: int) -> bool:
    import numpy as np

    positions = store.idx.get(symbol)
    if positions is None or i < 0:
        return False
    a = int(np.searchsorted(positions, i, side="left"))
    return a < len(positions) and int(positions[a]) == i


def eligible_members(
    store: series.SeriesStore, members: list[tuple[str, int]], t_i: int
) -> list[tuple[str, int]]:
    """Members whose data supports every feature and every baseline on this day.

    Eligibility is decided by data availability alone. It never consults an
    outcome, and it is checked before the draw so the panel is always exactly
    the registered size or the day is recorded as no_data.

    Three spans are required. The feature block needs every session from
    t minus 60 through t. The 12-1 momentum baseline needs the sessions at
    t minus 21 and t minus 252. Requiring all three keeps the model and all
    three baselines on identical names, which is what the registration means by
    identical feature block and identical days.
    """
    out: list[tuple[str, int]] = []
    for sym, rank in members:
        if not _has_span(store, sym, t_i - MAX_LOOKBACK, t_i):
            continue
        if t_i - LOOKBACK_SESSIONS < 0:
            continue
        if not _has_session(store, sym, t_i - SKIP_SESSIONS):
            continue
        if not _has_session(store, sym, t_i - LOOKBACK_SESSIONS):
            continue
        out.append((sym, rank))
    return out


def run(*, rebuild_extract: bool = True) -> BuildReport:
    t0 = dt.datetime.now(dt.UTC)
    report = BuildReport()

    with open_store() as con:
        if rebuild_extract:
            print("B.0 step 1: extract", flush=True)
            report.extract = extract.run(con)
            print(
                f"   {report.extract.bars_written} bars, {report.extract.symbols} symbols",
                flush=True,
            )

        sess = [r[0] for r in con.execute("SELECT date FROM session ORDER BY idx")]
        idx_of = session_index(con)
        window = derive_window([dt.date.fromisoformat(d) for d in sess])
        window_dates = [d.isoformat() for d in window.sessions]
        window_start = window.start.isoformat()
        set_meta(con, "window.start", window_start)
        set_meta(con, "window.end", window.end.isoformat())
        set_meta(con, "window.n_days", str(window.n_days))

        print("B.0 step 2: load series", flush=True)
        store = series.load(con, sess)
        print(f"   {len(store.idx)} symbols in memory", flush=True)

        assets = extract.asset_lookup(con)

        print("B.0 step 3: formations", flush=True)
        first_needed = min(FIT_START, window_start)
        all_formations = formation_dates(sess, PARAMS)
        # Every formation that governs a day the pipeline uses, plus the one
        # immediately before the first such day.
        needed = [f for f in all_formations if f <= window.end.isoformat()]
        needed = [f for f in needed if f >= _preceding(all_formations, first_needed)]
        clear_derived(con)
        for f in needed:
            n = build_formation(con, f, sess, store, assets)
            report.formations_built += 1
            v = verify_against_source(con, f)
            if v.ok:
                report.formations_verified += 1
            else:
                report.formation_failures.append(
                    f"{f}: reproduced {v.n_reproduced} stored {v.n_stored} "
                    f"set_match={v.symbol_set_matches} rank_match={v.rank_sequence_matches} "
                    f"{v.first_difference}"
                )
            print(f"   {f}: {n} members, verified={v.ok}", flush=True)
        con.commit()

        fit_dates = [d for d in sess if FIT_START <= d <= FIT_END]
        report.fit_days = len(fit_dates)
        report.window_days = len(window_dates)

        print("B.0 step 4: panels, features, forward returns", flush=True)
        fit_rows: list[tuple[str, str, dict[str, float]]] = []
        pending_returns: list[tuple[str, str, int, Maybe[float]]] = []
        current_month = ""

        for date in fit_dates + window_dates:
            month = date[:7]
            if month != current_month:
                store.drop_dense_cache()
                current_month = month
                print(f"   {month}", flush=True)

            t_i = idx_of[date]
            f_date = governing_formation(needed, date)
            members = [
                (r[0], int(r[1]))
                for r in con.execute(
                    "SELECT symbol, rank FROM formation WHERE formation_date = ?", (f_date,)
                )
            ]
            eligible = eligible_members(store, members, t_i)
            drawn = panel.draw(date, f_date, eligible)
            if drawn is None:
                if date >= window_start:
                    record_day_state(
                        con,
                        date,
                        CallState.NO_DATA.value,
                        f"eligible pool {len(eligible)} under panel size {CONFIG.panel_size}",
                    )
                    report.window_no_data += 1
                continue

            blocks_raw = {}
            incomplete = False
            for sym in drawn.symbols:
                block = raw_block(store.dense(sym), t_i)
                if not is_complete(block):
                    incomplete = True
                    break
                blocks_raw[sym] = {k: float(v) for k, v in block.items()}
            if incomplete:
                if date >= window_start:
                    record_day_state(con, date, CallState.NO_DATA.value, "incomplete feature block")
                    report.window_no_data += 1
                continue

            blocks_z = cross_sectional_z(blocks_raw, CONFIG.feature_names)

            con.executemany(
                "INSERT OR REPLACE INTO panel(date, symbol, stratum, formation_date) VALUES(?,?,?,?)",
                [
                    (date, sym, panel.stratum_of(rank, 500, CONFIG.strata_count), f_date)
                    for sym, rank in drawn.picks
                ],
            )
            con.executemany(
                "INSERT OR REPLACE INTO feature(date, symbol, name, raw, z, absent_reason) "
                "VALUES(?,?,?,?,?,NULL)",
                [
                    (date, sym, name, blocks_raw[sym][name], blocks_z[sym][name])
                    for sym in drawn.symbols
                    for name in CONFIG.feature_names
                ],
            )

            for sym in drawn.symbols:
                closes = store.dense(sym).close
                for h in HORIZONS:
                    pending_returns.append((date, sym, h, forward_returns.compute(closes, t_i, h)))

            if date >= window_start:
                report.window_panels += 1
                nonce = anonymize.new_nonce()
                anon = anonymize.build(list(drawn.symbols), nonce)
                con.executemany(
                    "INSERT OR REPLACE INTO anonymization(date, label, symbol, nonce) VALUES(?,?,?,?)",
                    [(date, lab, sym, nonce) for lab, sym in anon.label_to_symbol.items()],
                )
                ranked = rank_sign_last({s: blocks_z[s]["ret_1"] for s in drawn.symbols})
                con.executemany(
                    "INSERT OR REPLACE INTO baseline_ranking(date, baseline, symbol, rank) VALUES(?,?,?,?)",
                    [(date, SIGN_LAST, s, i + 1) for i, s in enumerate(ranked)],
                )
                mom = {s: momentum_12_1(store.dense(s), t_i) for s in drawn.symbols}
                ranked_mom = rank_mom_12_1(mom)
                con.executemany(
                    "INSERT OR REPLACE INTO baseline_ranking(date, baseline, symbol, rank) VALUES(?,?,?,?)",
                    [(date, MOM_12_1, s, i + 1) for i, s in enumerate(ranked_mom)],
                )
            else:
                for sym in drawn.symbols:
                    fit_rows.append((date, sym, blocks_z[sym]))

            report.panels_by_month[month] = report.panels_by_month.get(month, 0) + 1
        con.commit()

        print("B.0 step 5: forward returns", flush=True)
        wr = forward_returns.write(pending_returns, window_start=window_start)
        report.forward_fit_rows = wr.fit_rows
        report.forward_sealed_rows = wr.sealed_rows
        report.forward_absent_rows = wr.absent_rows
        print(f"   fit {wr.fit_rows}, sealed {wr.sealed_rows}, absent {wr.absent_rows}", flush=True)

        print("B.0 step 6: fit the logistic baseline", flush=True)
        fitted = _fit(fit_rows)
        logistic_baseline.save(con, fitted)
        report.logistic_digest = fitted.digest
        print(
            f"   {fitted.n_rows} rows over {fitted.n_days} days, digest {fitted.digest[:16]}",
            flush=True,
        )

        print("B.0 step 7: logistic rankings for window days", flush=True)
        n_log = 0
        for date in window_dates:
            rows = con.execute(
                "SELECT symbol, name, z FROM feature WHERE date = ?", (date,)
            ).fetchall()
            if not rows:
                continue
            blocks: dict[str, dict[str, float]] = {}
            for sym, name, z in rows:
                blocks.setdefault(sym, {})[name] = float(z)
            ranked = logistic_baseline.rank_logistic(fitted, blocks)
            con.executemany(
                "INSERT OR REPLACE INTO baseline_ranking(date, baseline, symbol, rank) VALUES(?,?,?,?)",
                [(date, LOGISTIC, s, i + 1) for i, s in enumerate(ranked)],
            )
            n_log += 1
        con.commit()

        for name in (SIGN_LAST, MOM_12_1, LOGISTIC):
            report.baseline_days[name] = int(
                con.execute(
                    "SELECT COUNT(DISTINCT date) FROM baseline_ranking WHERE baseline = ?", (name,)
                ).fetchone()[0]
            )

    report.seconds = (dt.datetime.now(dt.UTC) - t0).total_seconds()
    return report


def _preceding(formations: list[str], date: str) -> str:
    chosen = formations[0]
    for f in formations:
        if f <= date:
            chosen = f
        else:
            break
    return chosen


def _fit(fit_rows: list[tuple[str, str, dict[str, float]]]) -> FittedLogistic:
    """Attach labels from the fit store, then fit once.

    The label is 1 when the forward return beat the median of its own day, so
    the target is cross-sectional and matches the task the model is asked to do.
    A symbol whose forward return is absent is dropped from the fit rather than
    labelled by a guess.
    """
    dates = sorted({d for d, _s, _b in fit_rows})
    targets = logistic_baseline.load_fit_targets(dates, CONFIG.primary_horizon_sessions)

    by_date: dict[str, list[tuple[str, dict[str, float]]]] = {}
    for date, symbol, block in fit_rows:
        by_date.setdefault(date, []).append((symbol, block))

    labelled: list[tuple[str, dict[str, float], int]] = []
    for date, rows in by_date.items():
        present = [(sym, block) for sym, block in rows if (date, sym) in targets]
        if len(present) < 2:
            continue
        rets = sorted(targets[(date, sym)] for sym, _b in present)
        n = len(rets)
        mid = rets[n // 2] if n % 2 else 0.5 * (rets[n // 2 - 1] + rets[n // 2])
        for sym, block in present:
            labelled.append((date, block, 1 if targets[(date, sym)] > mid else 0))
    if not labelled:
        raise RuntimeError("the logistic fit sample is empty")
    return logistic_baseline.fit_logistic(labelled)


if __name__ == "__main__":
    rep = run(rebuild_extract="--skip-extract" not in sys.argv)
    print(rep)
