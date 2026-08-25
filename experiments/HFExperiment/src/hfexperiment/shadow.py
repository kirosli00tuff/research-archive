"""The shadow book and benchmark panel accrual arithmetic. Pure functions.

The shadow series is the signal instrument, REGISTRATION.md Section 2.
Three books at widths 5, 20 and 50 from the registered rule at each
formation, equal weights at formation, weights drifting between
formations. First accrual day is the 2026-09-01 formation, ADR-015.

The state rules, from Section 3 and the B.1 registration:

  computed          the name's return is close over last close minus 1.
  halted, delisted  the name marks at its last available close, exactly
                    zero return, until it redeploys at the next
                    formation. The mark persists intra-month even if
                    bars resume.
  missing_bar,      the day cannot accrue. These functions REFUSE, the
  source_failed     caller records the exclusion and retries next run.
                    No branch synthesizes a price.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from hfexperiment.states import AccrualState, excludes_day, marks_at_last_close


@dataclass(frozen=True)
class BookState:
    """One width's book between formations. Immutable, replaced daily.

    values drift multiplicatively from the equal 1/width start.
    last_closes carry each name's last available close, the marking
    price of Section 3. marked maps a name to the state value that
    froze it, and stays until the next formation.
    """

    formation_date: str
    asof: str
    width: int
    names: tuple[str, ...]
    values: Mapping[str, float]
    last_closes: Mapping[str, float]
    marked: Mapping[str, str]


@dataclass(frozen=True)
class MemberPanel:
    """The benchmark membership between formations. Daily-rebalanced, so
    it carries no drifting values, only marking state per member."""

    formation_date: str
    asof: str
    names: tuple[str, ...]
    last_closes: Mapping[str, float]
    marked: Mapping[str, str]


def initial_book(
    formation_date: str,
    width: int,
    names: Sequence[str],
    entry_closes: Mapping[str, float],
) -> BookState:
    """Equal weights at formation, valued at the formation-day close.

    Every name needs an entry close. A name without one cannot enter a
    book honestly, and the formation that produced it must be reported,
    not patched.
    """
    if len(names) != width:
        raise ValueError(f"{len(names)} names for width {width}")
    missing = [n for n in names if n not in entry_closes]
    if missing:
        raise ValueError(f"no entry close for {missing}")
    return BookState(
        formation_date=formation_date,
        asof=formation_date,
        width=width,
        names=tuple(names),
        values={n: 1.0 / width for n in names},
        last_closes={n: entry_closes[n] for n in names},
        marked={},
    )


def initial_panel(
    formation_date: str,
    names: Sequence[str],
    entry_closes: Mapping[str, float],
) -> MemberPanel:
    """The benchmark membership at formation, per-member entry closes."""
    missing = [n for n in names if n not in entry_closes]
    if missing:
        raise ValueError(f"no entry close for {missing}")
    return MemberPanel(
        formation_date=formation_date,
        asof=formation_date,
        names=tuple(sorted(names)),
        last_closes={n: entry_closes[n] for n in names},
        marked={},
    )


def day_exclusion(states: Mapping[str, AccrualState]) -> list[str]:
    """The names whose state excludes the day, empty when none does."""
    return sorted(n for n, s in states.items() if excludes_day(s))


def _name_return(
    name: str,
    state: AccrualState,
    closes: Mapping[str, float],
    last_closes: Mapping[str, float],
) -> float:
    """One name's daily return under its state. Refuses excluding states.

    The refusal is the enforcement site for the absence rule: a missing
    bar or failed source has no return, carried-forward or otherwise.
    """
    if excludes_day(state):
        raise ValueError(
            f"{name} is {state.value}: the day must be excluded and "
            "retried, never accrued from a synthesized price"
        )
    if marks_at_last_close(state):
        return 0.0
    close = closes.get(name)
    prev = last_closes.get(name)
    if close is None or prev is None or prev <= 0:
        raise ValueError(f"{name} computed without a usable close pair")
    return close / prev - 1.0


@dataclass(frozen=True)
class BookDay:
    """One accrued session for one book."""

    session: str
    book_return: float
    name_returns: Mapping[str, float]
    state: BookState


def accrue_book_day(
    book: BookState,
    session: str,
    states: Mapping[str, AccrualState],
    closes: Mapping[str, float],
) -> BookDay:
    """One session's book return with drifting weights.

    Marked names contribute zero at their marked close and keep their
    drifted value frozen. The caller must already have checked
    day_exclusion: an excluding state here raises.
    """
    values = dict(book.values)
    last_closes = dict(book.last_closes)
    marked = dict(book.marked)
    returns: dict[str, float] = {}
    for name in book.names:
        state = states[name]
        r = _name_return(name, state, closes, book.last_closes)
        if state is AccrualState.COMPUTED:
            last_closes[name] = closes[name]
        elif name not in marked:
            marked[name] = state.value
        returns[name] = r
        values[name] = book.values[name] * (1.0 + r)
    total_before = sum(book.values.values())
    total_after = sum(values.values())
    if total_before <= 0:
        raise ValueError("book value is not positive")
    return BookDay(
        session=session,
        book_return=total_after / total_before - 1.0,
        name_returns=returns,
        state=BookState(
            formation_date=book.formation_date,
            asof=session,
            width=book.width,
            names=book.names,
            values=values,
            last_closes=last_closes,
            marked=marked,
        ),
    )


@dataclass(frozen=True)
class PanelDay:
    """One advanced session for the benchmark panel."""

    session: str
    member_returns: Mapping[str, float]
    panel: MemberPanel


def advance_panel(
    panel: MemberPanel,
    session: str,
    states: Mapping[str, AccrualState],
    closes: Mapping[str, float],
) -> PanelDay:
    """One session's member returns. Same state rules as the book."""
    last_closes = dict(panel.last_closes)
    marked = dict(panel.marked)
    returns: dict[str, float] = {}
    for name in panel.names:
        state = states[name]
        r = _name_return(name, state, closes, panel.last_closes)
        if state is AccrualState.COMPUTED:
            last_closes[name] = closes[name]
        elif name not in marked:
            marked[name] = state.value
        returns[name] = r
    return PanelDay(
        session=session,
        member_returns=returns,
        panel=MemberPanel(
            formation_date=panel.formation_date,
            asof=session,
            names=panel.names,
            last_closes=last_closes,
            marked=marked,
        ),
    )
