"""Reproduce the source's own stored membership with the ported rule.

A copied rule that is never re-derived is a rule nobody checked. This module
rebuilds membership for one formation date straight from the source bars and
sets it beside the membership the source stored, so the port is proved faithful
rather than assumed faithful.
"""

from __future__ import annotations

from dataclasses import dataclass

from insider.market import source
from insider.market.universe import (
    RuleParams,
    classify_fund,
    has_segment_break_in,
    rank_members,
    segment_series,
    summarize_window,
    window_bounds,
)

PARAMS = RuleParams()

# Bars are pulled from this many sessions before the window so a listing gap
# that ends inside the window is visible. It exceeds SEGMENT_BREAK_SESSIONS,
# which is what makes any break landing in the window detectable in the slice.
SEGMENT_PAD_SESSIONS = 25


@dataclass(frozen=True, slots=True)
class PortResult:
    formation_date: str
    n_stored: int
    n_reproduced: int
    first_difference: str | None

    @property
    def ok(self) -> bool:
        return self.first_difference is None and self.n_stored == self.n_reproduced


def reproduce(formation_date: str, rule_id: str) -> PortResult:
    """Rebuild one formation from the source bars and compare rank by rank."""
    with source.read_only_bars() as con:
        sessions = source.sessions(con, "1900-01-01", "2100-01-01")
        start, end = window_bounds(sessions, formation_date, PARAMS.window_sessions)
        pad_index = max(sessions.index(start) - SEGMENT_PAD_SESSIONS, 0)
        pad_start = sessions[pad_index]
        session_index = {d: i for i, d in enumerate(sessions)}

        meta = {sym: (name, exch) for sym, name, exch in source.asset_metadata(con)}

        dates: dict[str, list[str]] = {}
        closes: dict[str, list[float]] = {}
        volumes: dict[str, list[float]] = {}
        for symbol, date, close, volume in source.window_bars_all_symbols(con, pad_start, end):
            dates.setdefault(symbol, []).append(date)
            if start <= date <= end:
                closes.setdefault(symbol, []).append(close)
                volumes.setdefault(symbol, []).append(volume)

        stored = source.stored_membership(con, rule_id, formation_date)

    candidates = []
    for symbol, symbol_closes in closes.items():
        name, exchange = meta.get(symbol, ("", ""))
        ordered = sorted(dates.get(symbol, []))
        segments = segment_series(ordered, session_index)
        candidate = summarize_window(
            symbol,
            symbol_closes,
            volumes[symbol],
            is_fund=classify_fund(name, exchange),
            segment_break_in_window=has_segment_break_in(segments, start, end),
        )
        if candidate is not None:
            candidates.append(candidate)

    members, _ = rank_members(candidates, PARAMS)
    difference: str | None = None
    for (stored_symbol, stored_rank, _dv, _mc, _wb), member in zip(stored, members, strict=False):
        if stored_symbol != member.candidate.symbol or stored_rank != member.rank:
            difference = (
                f"rank {stored_rank} is {stored_symbol} in the source and "
                f"{member.candidate.symbol} at rank {member.rank} in the port"
            )
            break
    if difference is None and len(stored) != len(members):
        difference = f"the source stored {len(stored)} members and the port built {len(members)}"

    return PortResult(
        formation_date=formation_date,
        n_stored=len(stored),
        n_reproduced=len(members),
        first_difference=difference,
    )
