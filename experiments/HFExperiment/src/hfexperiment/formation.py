"""The 12-1 cross-sectional momentum formation.

Rank universe members by trailing 12-month return skipping the most recent
month. Formation happens on the first trading session of each calendar month.

Anchor convention, fixed here and pinned by tests/test_formation.py:

  far anchor    the session strictly before the formation date 12 months back
                in the formation-date sequence
  near anchor   the session strictly before the formation date 1 month back

The momentum return is close(near) / close(far) - 1. Both closes come from
bars dated at or before their anchor session. A bar more than
MAX_ANCHOR_GAP_SESSIONS before its anchor disqualifies the symbol, because a
stale price is not a price. Both bars must sit inside the same listing
segment, because two listings are never one price series.

Everything is deterministic. Ties break on symbol ascending.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

# A bar this stale relative to its anchor session disqualifies the symbol.
# Matches SEGMENT_BREAK_SESSIONS in universe.py: a gap that would end a
# listing segment is also too long to carry a price across.
MAX_ANCHOR_GAP_SESSIONS = 20

# The registered lookback. Twelve formation dates back, skip the most
# recent month by ending one formation date back.
LOOKBACK_FORMATIONS = 12
SKIP_FORMATIONS = 1


@dataclass(frozen=True)
class AnchorBar:
    """The bar that supplies one anchor close."""
    date: str
    close: float


@dataclass(frozen=True)
class MomentumEntry:
    """One symbol's momentum measurement at a formation date."""
    symbol: str
    momentum: float
    far_bar: AnchorBar
    near_bar: AnchorBar


def anchor_sessions(
    all_formation_dates: Sequence[str],
    formation_date: str,
    sessions: Sequence[str],
) -> tuple[str, str]:
    """The (far, near) anchor sessions for a formation date.

    Raises ValueError when the formation-date sequence is too short to reach
    back LOOKBACK_FORMATIONS months. The caller skips such dates rather than
    shortening the lookback, because a shortened lookback is a different
    hypothesis.
    """
    idx = all_formation_dates.index(formation_date)
    if idx < LOOKBACK_FORMATIONS:
        raise ValueError(
            f"{formation_date} lacks {LOOKBACK_FORMATIONS} months of history"
        )
    far_formation = all_formation_dates[idx - LOOKBACK_FORMATIONS]
    near_formation = all_formation_dates[idx - SKIP_FORMATIONS]
    far = sessions[sessions.index(far_formation) - 1]
    near = sessions[sessions.index(near_formation) - 1]
    return far, near


def bar_at_or_before(
    bars: Sequence[tuple[str, float]],
    anchor: str,
    session_index: Mapping[str, int],
) -> AnchorBar | None:
    """The last bar dated at or before the anchor session, or None.

    None when no such bar exists or when the bar is more than
    MAX_ANCHOR_GAP_SESSIONS sessions before the anchor. `bars` is
    (date, close) ascending by date.
    """
    chosen: tuple[str, float] | None = None
    for date, close in bars:
        if date > anchor:
            break
        chosen = (date, close)
    if chosen is None:
        return None
    gap = session_index[anchor] - session_index[chosen[0]]
    if gap > MAX_ANCHOR_GAP_SESSIONS:
        return None
    return AnchorBar(date=chosen[0], close=chosen[1])


def momentum_for_symbol(
    symbol: str,
    bars: Sequence[tuple[str, float]],
    far_anchor: str,
    near_anchor: str,
    session_index: Mapping[str, int],
    segments: Sequence[tuple[str, str]] | None = None,
) -> MomentumEntry | str:
    """One symbol's momentum, or the string reason it cannot be measured.

    `segments` is (start_date, end_date) listing segments ascending. When
    given, both anchor bars must land in the same segment.
    """
    far_bar = bar_at_or_before(bars, far_anchor, session_index)
    if far_bar is None:
        return "no_far_anchor_bar"
    near_bar = bar_at_or_before(bars, near_anchor, session_index)
    if near_bar is None:
        return "no_near_anchor_bar"
    if far_bar.close <= 0:
        return "nonpositive_far_close"
    if segments is not None:
        far_seg = _segment_of(segments, far_bar.date)
        near_seg = _segment_of(segments, near_bar.date)
        if far_seg is None or near_seg is None or far_seg != near_seg:
            return "anchors_span_segments"
    return MomentumEntry(
        symbol=symbol,
        momentum=near_bar.close / far_bar.close - 1.0,
        far_bar=far_bar,
        near_bar=near_bar,
    )


def _segment_of(segments: Sequence[tuple[str, str]], date: str) -> int | None:
    for i, (start, end) in enumerate(segments):
        if start <= date <= end:
            return i
    return None


def form_book(
    entries: Sequence[MomentumEntry], width: int
) -> list[MomentumEntry]:
    """The top `width` entries by momentum descending, symbol ascending on ties.

    Pure and deterministic. The same entries always produce the same book.
    """
    ordered = sorted(entries, key=lambda e: (-e.momentum, e.symbol))
    return list(ordered[:width])
