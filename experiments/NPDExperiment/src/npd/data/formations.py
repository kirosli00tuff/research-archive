"""Reproduce U-LIQ-500 formations from the local extract, then verify the port.

The source store already holds its own membership for this rule. That table is
not copied and used. It is used to CHECK a reproduction built here from bars,
which is what proves the ported rule is faithful rather than merely similar.
A single differing symbol fails the check.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from npd.config import CONFIG
from npd.data import source
from npd.data.universe import (
    SEGMENT_BREAK_SESSIONS,
    RuleParams,
    classify_fund,
    rank_members,
    summarize_window,
    window_bounds,
)

if TYPE_CHECKING:
    import numpy as np
    import numpy.typing as npt

    from npd.data.series import SeriesStore

PARAMS = RuleParams()

# The ported rule must produce the registered rule id. A port that quietly
# changed a threshold would produce a different id and a different universe, and
# every downstream panel would be drawn from the wrong pool.
if PARAMS.rule_id != CONFIG.universe_id:
    raise RuntimeError(
        f"the ported rule builds {PARAMS.rule_id}, the registration names {CONFIG.universe_id}"
    )


@dataclass(frozen=True, slots=True)
class VerifyResult:
    formation_date: str
    n_reproduced: int
    n_stored: int
    symbol_set_matches: bool
    rank_sequence_matches: bool
    first_difference: str | None

    @property
    def ok(self) -> bool:
        return self.symbol_set_matches and self.rank_sequence_matches


def segment_break_in_window(
    positions: npt.NDArray[np.int32], wstart_i: int, wend_i: int, max_gap: int = 20
) -> bool:
    """Whether a listing segment after the first begins inside the window.

    Same rule as the ported segment_series, expressed on session indices so it
    runs without materializing a date list. A gap wider than max_gap sessions
    ends a segment, and a ticker reused by a second listing must never have its
    two runs joined into one price series.
    """
    if len(positions) == 0:
        return False
    for j in range(1, len(positions)):
        gap = int(positions[j]) - int(positions[j - 1]) - 1
        if gap > max_gap and wstart_i <= int(positions[j]) <= wend_i:
            return True
    return False


def build_formation(
    con: sqlite3.Connection,
    formation_date: str,
    sessions: Sequence[str],
    store: SeriesStore,
    assets: dict[str, tuple[str, str]],
) -> int:
    """Compute and store one formation's membership from the local extract."""
    wstart, wend = window_bounds(sessions, formation_date, PARAMS.window_sessions)
    wstart_i = store.index_of[wstart]
    wend_i = store.index_of[wend]

    candidates = []
    for sym in store.idx:
        closes, vols = store.window(sym, wstart_i, wend_i)
        if closes.size == 0:
            continue
        name, exch = assets.get(sym, ("", ""))
        cand = summarize_window(
            sym,
            [float(x) for x in closes],
            [float(x) for x in vols],
            is_fund=classify_fund(name, exch),
            segment_break_in_window=segment_break_in_window(
                store.idx[sym], wstart_i, wend_i, SEGMENT_BREAK_SESSIONS
            ),
        )
        if cand is not None:
            candidates.append(cand)

    members, _rejected = rank_members(candidates, PARAMS)
    con.execute("DELETE FROM formation WHERE formation_date = ?", (formation_date,))
    con.executemany(
        "INSERT INTO formation(formation_date, symbol, rank, median_dollar_volume, "
        "median_close, window_bars) VALUES(?,?,?,?,?,?)",
        [
            (
                formation_date,
                m.candidate.symbol,
                m.rank,
                m.candidate.median_dollar_volume,
                m.candidate.median_close,
                m.candidate.window_bars,
            )
            for m in members
        ],
    )
    return len(members)


def verify_against_source(con: sqlite3.Connection, formation_date: str) -> VerifyResult:
    """Compare the local reproduction to the source's own stored membership."""
    local = [
        (r[0], int(r[1]))
        for r in con.execute(
            "SELECT symbol, rank FROM formation WHERE formation_date = ? ORDER BY rank",
            (formation_date,),
        )
    ]
    with source.read_only_bars() as src:
        stored = source.stored_membership(src, PARAMS.rule_id, formation_date)

    local_syms = {s for s, _ in local}
    stored_syms = {s for s, _ in stored}
    set_matches = local_syms == stored_syms
    seq_matches = local == stored

    first_diff: str | None = None
    if not set_matches:
        only_local = sorted(local_syms - stored_syms)[:8]
        only_stored = sorted(stored_syms - local_syms)[:8]
        first_diff = f"only_local={only_local} only_stored={only_stored}"
    elif not seq_matches:
        for (ls, lr), (ss, sr) in zip(local, stored, strict=False):
            if ls != ss or lr != sr:
                first_diff = f"rank {lr}: local {ls}, stored {ss} at rank {sr}"
                break

    return VerifyResult(
        formation_date=formation_date,
        n_reproduced=len(local),
        n_stored=len(stored),
        symbol_set_matches=set_matches,
        rank_sequence_matches=seq_matches,
        first_difference=first_diff,
    )


def governing_formation(formation_dates_asc: Sequence[str], date: str) -> str:
    """The most recent formation on or before the given date.

    A formation decided at f governs every session from f until the next
    formation. A session before the first formation has no governing formation
    and raises, because guessing one would be a synthesized value.
    """
    chosen: str | None = None
    for f in formation_dates_asc:
        if f <= date:
            chosen = f
        else:
            break
    if chosen is None:
        raise ValueError(f"no formation governs {date}")
    return chosen
