"""Calendar-time portfolio membership.

One book per session, holding every name currently inside its post-filing
window. This is the structure that absorbs day-clustering: when many insiders
buy on the same day, the calendar-time portfolio counts that day once.

Nothing here reads a return.
"""

from __future__ import annotations

import bisect
from collections import defaultdict
from dataclasses import dataclass

from insider.config import CONFIG, Config


@dataclass(frozen=True, slots=True)
class Event:
    """One qualifying event, reduced to what membership needs."""

    symbol: str
    entry_session: str


@dataclass(frozen=True, slots=True)
class MembershipSeries:
    """Which names are in the book on each session, at one hold."""

    hold_sessions: int
    sessions: tuple[str, ...]
    book: tuple[frozenset[str], ...]

    @property
    def widths(self) -> tuple[int, ...]:
        return tuple(len(b) for b in self.book)

    @property
    def non_empty_sessions(self) -> int:
        return sum(1 for b in self.book if b)

    def coverage(self) -> float:
        return self.non_empty_sessions / len(self.sessions) if self.sessions else 0.0

    def mean_width(self) -> float:
        """Average book width over sessions that carry a book.

        Averaged over non-empty sessions on purpose. Averaging over every
        session in the span would fold coverage into width and hide a book that
        is wide when it exists and absent half the time.
        """
        widths = [w for w in self.widths if w]
        return sum(widths) / len(widths) if widths else 0.0


def entry_session_for(sessions: list[str], filing_date: str, cfg: Config = CONFIG) -> str | None:
    """The close a public filer can first reach.

    The first session strictly after the filing date, shifted by the registered
    entry lag. Returns None when the filing lands past the end of the bars,
    which is a recorded absence and never a substituted date.
    """
    index = bisect.bisect_right(sessions, filing_date) + cfg.entry_lag_sessions - 1
    return sessions[index] if 0 <= index < len(sessions) else None


def build(events: list[Event], sessions: list[str], hold_sessions: int) -> MembershipSeries:
    """Expand each event into its holding window and union by session.

    A name held through two overlapping events counts once. The book is a set,
    so a second purchase in a name already held widens nothing, which is the
    correct treatment: the portfolio holds one position per name.
    """
    index_of = {s: i for i, s in enumerate(sessions)}
    holders: dict[int, set[str]] = defaultdict(set)
    for event in events:
        start = index_of.get(event.entry_session)
        if start is None:
            continue
        stop = min(start + hold_sessions, len(sessions))
        for i in range(start, stop):
            holders[i].add(event.symbol)
    return MembershipSeries(
        hold_sessions=hold_sessions,
        sessions=tuple(sessions),
        book=tuple(frozenset(holders.get(i, ())) for i in range(len(sessions))),
    )
