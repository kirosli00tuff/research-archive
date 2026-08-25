"""The formation run. Fresh full-window queries, never stored history.

The stale-adjustment trap Task 0 checked for is designed away here:
each formation re-queries the entire trailing window with
adjustment=all rather than trusting bars stored by earlier runs. An
adjustment landing between formations re-enters the store as newer
rows. The rule logic itself is the registered one: universe.py copied
verbatim from the recorded round, formation.py's anchor conventions
fixed by ADR-006. Nothing here reinterprets either.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from hfexperiment import formation, universe
from hfexperiment.alpaca_source import DailyBar
from hfexperiment.barstore import BarRow, BarStore


class MarketSource(Protocol):
    """What a formation needs from the data source. AlpacaSource
    satisfies this structurally, and tests inject deterministic fakes."""

    def active_assets(self) -> list[tuple[str, str, str, str, int]]: ...

    def daily_bars(
        self, symbols: Sequence[str], start: str, end: str
    ) -> dict[str, list[DailyBar]]: ...

# Calendar depth the runs fetch: 13 months of momentum anchors plus the
# 60-session universe window plus slack for holidays.
CALENDAR_LOOKBACK_DAYS = 560


class FormationError(RuntimeError):
    """The formation could not be produced honestly. Report, never patch."""


@dataclass(frozen=True)
class FormationResult:
    """What one formation produced, for the record and the health view."""

    formation_date: str
    members: tuple[str, ...]
    books: dict[int, list[str]]
    n_candidates: int
    n_measurable: int


def _bar_rows(bars: dict[str, list[DailyBar]]) -> list[BarRow]:
    return [
        (sym, ses, o, h, lo, c, v)
        for sym, rows in bars.items()
        for ses, o, h, lo, c, v in rows
    ]


def _dated_closes(
    rows: Sequence[DailyBar], session_index: dict[str, int]
) -> list[tuple[str, float, float]]:
    """(session, close, volume) ascending, calendar sessions only."""
    usable = [
        (ses, c, v if v is not None else 0.0)
        for ses, _o, _h, _lo, c, v in rows
        if ses in session_index
    ]
    return sorted(usable)


def run_formation(
    store: BarStore,
    source: MarketSource,
    sessions: Sequence[str],
    formation_date: str,
    widths: Sequence[int],
    run_utc: str,
    params: universe.RuleParams | None = None,
) -> FormationResult:
    """One formation from fresh queries. Appends everything it derives.

    `sessions` is the trading calendar ascending, already fetched by the
    caller this run, deep enough for CALENDAR_LOOKBACK_DAYS. `params`
    defaults to the registered rule and is overridable only so tests
    can prove determinism on a small fixture pool.
    """
    if formation_date not in sessions:
        raise FormationError(f"{formation_date} is not a trading session")
    session_index = {d: i for i, d in enumerate(sessions)}
    if params is None:
        params = universe.RuleParams()

    members = _form_universe(
        store, source, sessions, session_index, formation_date, params, run_utc
    )
    entries = _measure_momentum(
        store, source, sessions, session_index, formation_date, members,
        params, run_utc,
    )
    if len(entries) < max(widths):
        raise FormationError(
            f"{formation_date}: only {len(entries)} measurable members "
            f"for width {max(widths)}"
        )
    books: dict[int, list[str]] = {}
    for width in widths:
        book = formation.form_book(entries, width)
        names = [e.symbol for e in book]
        store.append_formation(formation_date, width, names, run_utc)
        books[width] = names
    return FormationResult(
        formation_date=formation_date,
        members=tuple(members),
        books=books,
        n_candidates=len(members),
        n_measurable=len(entries),
    )


def _form_universe(
    store: BarStore,
    source: MarketSource,
    sessions: Sequence[str],
    session_index: dict[str, int],
    formation_date: str,
    params: universe.RuleParams,
    run_utc: str,
) -> list[str]:
    """U-LIQ-500 membership from a fresh full-pool window query."""
    win_start, win_end = universe.window_bounds(
        sessions, formation_date, params.window_sessions
    )
    assets = source.active_assets()
    store.append_assets(assets, run_utc)
    symbols = sorted(a[0] for a in assets)
    asset_meta = {a[0]: (a[1], a[2]) for a in assets}
    bars = source.daily_bars(symbols, win_start, win_end)
    store.append_bars(_bar_rows(bars), "all", run_utc)

    candidates: list[universe.Candidate] = []
    for sym in symbols:
        dated = _dated_closes(bars.get(sym) or [], session_index)
        if not dated:
            continue
        name, exchange = asset_meta[sym]
        segments = universe.segment_series(
            [d for d, _c, _v in dated], session_index
        )
        cand = universe.summarize_window(
            sym,
            [c for _d, c, _v in dated],
            [v for _d, _c, v in dated],
            is_fund=universe.classify_fund(name, exchange),
            segment_break_in_window=universe.has_segment_break_in(
                segments, win_start, win_end
            ),
        )
        if cand is not None:
            candidates.append(cand)
    ranked, _rejected = universe.rank_members(candidates, params)
    members = [m.candidate.symbol for m in ranked]
    if len(members) < params.top_n:
        raise FormationError(
            f"{formation_date}: universe has {len(members)} members, "
            f"rule requires {params.top_n}"
        )
    store.append_universe(formation_date, members, run_utc)
    return members


def _measure_momentum(
    store: BarStore,
    source: MarketSource,
    sessions: Sequence[str],
    session_index: dict[str, int],
    formation_date: str,
    members: Sequence[str],
    params: universe.RuleParams,
    run_utc: str,
) -> list[formation.MomentumEntry]:
    """12-1 momentum for members from a fresh full-span query."""
    all_fdates = universe.formation_dates(sessions, params)
    if formation_date not in all_fdates:
        raise FormationError(
            f"{formation_date} lacks a full trailing window in the "
            "fetched calendar"
        )
    far, near = formation.anchor_sessions(all_fdates, formation_date, sessions)
    hist_start_idx = max(
        0, session_index[far] - formation.MAX_ANCHOR_GAP_SESSIONS - 1
    )
    hist_start = sessions[hist_start_idx]
    hist_end = sessions[session_index[formation_date] - 1]
    hist = source.daily_bars(list(members), hist_start, hist_end)
    store.append_bars(_bar_rows(hist), "all", run_utc)

    entries: list[formation.MomentumEntry] = []
    for sym in members:
        dated = _dated_closes(hist.get(sym) or [], session_index)
        bars_dc = [(d, c) for d, c, _v in dated]
        segments = universe.segment_series(
            [d for d, _c in bars_dc], session_index
        )
        spans = [(s.start_date, s.end_date) for s in segments]
        result = formation.momentum_for_symbol(
            sym, bars_dc, far, near, session_index, spans
        )
        if isinstance(result, formation.MomentumEntry):
            entries.append(result)
    return entries
