"""Hindsight-free universe construction. Ported by copy, never imported.

PROVENANCE. Copied from ~/Documents/GitHub/AiTrader/backtest/universe.py on
2026-08-25. The source file is hashed before and after the port and the pair is
recorded in reports/stage_b0/port.md. The source repository is read-only to
this one and nothing here imports across the boundary.

The port keeps the rule identical. tests/test_universe_port.py reproduces the
source's own stored membership for every formation the window needs and fails
on any difference, which is what proves the copy is faithful rather than
merely similar.

Pure functions only. No network, no database, no clock. Everything here decides
membership from bars dated strictly before the formation date, so a decision
made at date f cannot move when later data arrives.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from itertools import pairwise

WINDOW_SESSIONS = 60
MIN_WINDOW_BARS = 40
MIN_MEDIAN_CLOSE = 5.0
TOP_N = 500
SEGMENT_BREAK_SESSIONS = 20
JUMP_THRESHOLD = 0.50

_STRONG_TOKENS = (
    "etf",
    "etfs",
    "etn",
    "etns",
    "etp",
    "exchange traded",
    "exchange-traded",
    "index fund",
    "mutual fund",
    "closed end",
    "closed-end",
    "fund",
    "funds",
    "unit investment trust",
    "royalty trust",
    "series trust",
    "spdr",
    "ishares",
    "proshares",
    "direxion",
    "wisdomtree",
    "vaneck",
    "etracs",
    "ipath",
    "xtrackers",
    "powershares",
)
_WEAK_TOKENS = (
    "trust",
    "portfolio",
    "portfolios",
    "index",
    "series",
    "shares",
    "beneficial interest",
)

_STRONG_RE = re.compile(r"\b(" + "|".join(_STRONG_TOKENS) + r")\b", re.IGNORECASE)
_WEAK_RE = re.compile(r"\b(" + "|".join(_WEAK_TOKENS) + r")\b", re.IGNORECASE)

FUND_EXCHANGES = frozenset({"ARCA", "BATS"})


def classify_fund(name: str, exchange: str) -> bool | None:
    """Whether the instrument is a pooled vehicle, or None when that cannot be
    established.

    The return is tri-state and None is not False. A symbol carrying no name is
    an absence of evidence, not evidence of an operating company, and
    `rejection_reason` excludes it. Same shape as the standing absence rule in
    npd.absence.
    """
    if (exchange or "").strip().upper() in FUND_EXCHANGES:
        return True
    nm = (name or "").strip()
    if not nm:
        return None
    if _STRONG_RE.search(nm):
        return True
    return len({m.group(0).lower() for m in _WEAK_RE.finditer(nm)}) >= 2


def median(values: Sequence[float]) -> float:
    """Median of a non-empty sequence. Raises on empty rather than guessing."""
    if not values:
        raise ValueError("median of an empty sequence")
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


@dataclass(frozen=True)
class RuleParams:
    """Every knob the membership rule has. Frozen so a caller cannot produce an
    unlabelled hybrid between formation dates."""

    window_sessions: int = WINDOW_SESSIONS
    min_window_bars: int = MIN_WINDOW_BARS
    min_median_close: float = MIN_MEDIAN_CLOSE
    top_n: int = TOP_N
    include_funds: bool = False

    @property
    def rule_id(self) -> str:
        kind = "all" if self.include_funds else "stk"
        return (
            f"U-LIQ-{self.top_n}-{kind}-w{self.window_sessions}"
            f"-m{self.min_window_bars}-p{self.min_median_close:g}"
        )


@dataclass(frozen=True)
class Candidate:
    symbol: str
    window_bars: int
    median_close: float
    median_dollar_volume: float
    is_fund: bool | None
    segment_break_in_window: bool


@dataclass(frozen=True)
class Member:
    rank: int
    candidate: Candidate


def summarize_window(
    symbol: str,
    closes: Sequence[float],
    volumes: Sequence[float],
    *,
    is_fund: bool | None,
    segment_break_in_window: bool,
) -> Candidate | None:
    """Reduce one symbol's window to a Candidate, or None when it has no bars.

    Dollar volume is close times volume per session, then the median over
    sessions. The median, not the mean, so one squeeze day cannot buy
    membership for a name that is otherwise untradeable.
    """
    if not closes or len(closes) != len(volumes):
        return None
    return Candidate(
        symbol=symbol,
        window_bars=len(closes),
        median_close=median(closes),
        median_dollar_volume=median([c * v for c, v in zip(closes, volumes, strict=True)]),
        is_fund=is_fund,
        segment_break_in_window=segment_break_in_window,
    )


def rejection_reason(cand: Candidate, params: RuleParams) -> str | None:
    """Why this candidate cannot be a member, or None when it can be ranked.

    Returned rather than raised so every rejection can be recorded. A filter
    that rejects silently cannot be evaluated.
    """
    if cand.window_bars < params.min_window_bars:
        return f"thin_window:{cand.window_bars}<{params.min_window_bars}"
    if cand.median_close < params.min_median_close:
        return f"below_price_floor:{cand.median_close:.2f}"
    if cand.segment_break_in_window:
        return "listing_segment_break_in_window"
    # Fail closed. Unclassified is not a fund, it is an unknown, so a caller
    # asking for funds does not get it either. This branch sits before the
    # include_funds check on purpose.
    if cand.is_fund is None:
        return "unclassified"
    if cand.is_fund and not params.include_funds:
        return "fund"
    return None


def rank_members(
    candidates: Iterable[Candidate], params: RuleParams
) -> tuple[list[Member], list[tuple[str, str]]]:
    """Rank eligible candidates by median dollar volume and take the top N.

    Ties break on symbol ascending so the same inputs always produce the same
    membership.
    """
    eligible: list[Candidate] = []
    rejected: list[tuple[str, str]] = []
    for cand in candidates:
        reason = rejection_reason(cand, params)
        if reason:
            rejected.append((cand.symbol, reason))
        else:
            eligible.append(cand)
    eligible.sort(key=lambda c: (-c.median_dollar_volume, c.symbol))
    members = [Member(rank=i + 1, candidate=c) for i, c in enumerate(eligible[: params.top_n])]
    for c in eligible[params.top_n :]:
        rejected.append((c.symbol, f"below_rank_{params.top_n}"))
    return members, rejected


def formation_dates(sessions: Sequence[str], params: RuleParams) -> list[str]:
    """First trading session of each month that has a full trailing window.

    `sessions` is the exchange trading calendar as ascending YYYY-MM-DD, not the
    dates one symbol happened to trade. A schedule keyed off a symbol's own bars
    would shift whenever that symbol was quiet.
    """
    out: list[str] = []
    seen_months: set[str] = set()
    for i, day in enumerate(sessions):
        month = day[:7]
        if month in seen_months:
            continue
        seen_months.add(month)
        if i >= params.window_sessions:
            out.append(day)
    return out


def window_bounds(
    sessions: Sequence[str], formation_date: str, window_sessions: int
) -> tuple[str, str]:
    """The trailing window as [start, end] inclusive session dates.

    The window ends on the session before the formation date. A window that
    included the formation date would decide membership using a bar the month it
    governs can trade on.
    """
    idx = sessions.index(formation_date)
    if idx < window_sessions:
        raise ValueError(f"{formation_date} has no full trailing window")
    return sessions[idx - window_sessions], sessions[idx - 1]


@dataclass(frozen=True)
class Segment:
    index: int
    start_date: str
    end_date: str
    n_bars: int
    gap_sessions_before: int


def segment_series(
    bar_dates: Sequence[str],
    session_index: dict[str, int],
    max_gap_sessions: int = SEGMENT_BREAK_SESSIONS,
) -> list[Segment]:
    """Split a ticker's bar dates into listing segments.

    The gap is counted in trading sessions, not calendar days, so a holiday week
    is never mistaken for a delisting. More than one segment means the ticker
    carried more than one listing, and the segments must never be joined into a
    single price series.
    """
    if not bar_dates:
        return []
    segments: list[Segment] = []
    start = bar_dates[0]
    count = 1
    gap_before = 0
    for prev, cur in pairwise(bar_dates):
        gap = session_index[cur] - session_index[prev] - 1
        if gap > max_gap_sessions:
            segments.append(Segment(len(segments), start, prev, count, gap_before))
            start, count, gap_before = cur, 1, gap
        else:
            count += 1
    segments.append(Segment(len(segments), start, bar_dates[-1], count, gap_before))
    return segments


def has_segment_break_in(segments: Sequence[Segment], start: str, end: str) -> bool:
    """Whether any segment begins inside [start, end] after the first one."""
    return any(seg.index > 0 and start <= seg.start_date <= end for seg in segments)
