"""Sequential daily accrual over the append-only ledgers.

The orchestration rules, from the B.1 registration:

  Sessions accrue strictly in order within a formation lineage. A day
  whose state excludes (missing_bar, source_failed) is recorded as an
  exclusion and blocks its lineage until a retry computes it, because
  the next day's arithmetic needs this day's state. Bars backfill, so
  blocks heal on later runs. Nothing edits history: a healed day is a
  new computed record appended after its exclusion records.

  A formation ends its lineage. The session return INTO a formation
  date belongs to the old membership, the new books and panel enter at
  the formation close, and the new lineage accrues from the next
  session. First accrual day of the whole series is the 2026-09-01
  formation, ADR-015.

  The benchmark chain gates every width: a member with a missing bar
  or failed source excludes the day for all widths, per benchmark.py's
  cited definition. Book exclusions block only their own width.

Ledger record kinds: panel_init and book_init (formation.jsonl),
benchmark (benchmark.jsonl), accrual (accrual.jsonl). The verdict
engine appends to verdict.jsonl over these.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from hfexperiment.benchmark import benchmark_daily_return
from hfexperiment.ledger import Ledger
from hfexperiment.registered import THRESHOLDS
from hfexperiment.shadow import (
    BookState,
    MemberPanel,
    accrue_book_day,
    advance_panel,
    day_exclusion,
    initial_book,
    initial_panel,
)
from hfexperiment.states import AccrualState, classify_name_day

# The registered widths, primary first. Section 4.
WIDTHS: tuple[int, ...] = (
    THRESHOLDS.primary_width,
    *(
        w
        for w in THRESHOLDS.secondary_widths
        if w != THRESHOLDS.primary_width
    ),
)


class BarView(Protocol):
    """One run's view of the data, enough to classify every name-day."""

    def close(self, symbol: str, session: str) -> float | None: ...

    def asset_active(self, symbol: str) -> bool: ...

    def bar_exists_later(self, symbol: str, session: str) -> bool: ...

    def absent_streak(self, symbol: str, session: str) -> int: ...


@dataclass(frozen=True)
class Ledgers:
    """The four append-only files of the shadow series."""

    formation: Ledger
    benchmark: Ledger
    accrual: Ledger
    verdict: Ledger


def open_ledgers(directory: str | Path) -> Ledgers:
    base = Path(directory)
    return Ledgers(
        formation=Ledger(base / "formation.jsonl"),
        benchmark=Ledger(base / "benchmark.jsonl"),
        accrual=Ledger(base / "accrual.jsonl"),
        verdict=Ledger(base / "verdict.jsonl"),
    )


def classify_names(
    view: BarView,
    names: Sequence[str],
    session: str,
    fetch_ok: bool,
    marked: Mapping[str, str],
) -> dict[str, AccrualState]:
    """Every name's state for one session through the single classifier."""
    out: dict[str, AccrualState] = {}
    for name in names:
        already = AccrualState(marked[name]) if name in marked else None
        out[name] = classify_name_day(
            fetch_ok=fetch_ok,
            has_bar=view.close(name, session) is not None,
            asset_active=view.asset_active(name),
            bar_exists_later=view.bar_exists_later(name, session),
            absent_streak=view.absent_streak(name, session),
            already_marked=already,
        )
    return out


def _closes(
    view: BarView, names: Sequence[str], session: str
) -> dict[str, float]:
    out: dict[str, float] = {}
    for name in names:
        close = view.close(name, session)
        if close is not None:
            out[name] = close
    return out


def _state_counts(states: Mapping[str, AccrualState]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for state in states.values():
        counts[state.value] = counts.get(state.value, 0) + 1
    return counts


def _excluding_detail(
    states: Mapping[str, AccrualState], excluding: Sequence[str]
) -> dict[str, Any]:
    """The exclusion, recorded with its states never merged."""
    return {
        "excluding_state_counts": _state_counts(
            {n: states[n] for n in excluding}
        ),
        "excluding_sample": {n: states[n].value for n in excluding[:10]},
        "n_excluding": len(excluding),
    }


# -- serialization ----------------------------------------------------


def panel_to_json(panel: MemberPanel) -> dict[str, Any]:
    return {
        "formation_date": panel.formation_date,
        "asof": panel.asof,
        "names": list(panel.names),
        "last_closes": dict(panel.last_closes),
        "marked": dict(panel.marked),
    }


def panel_from_json(data: Mapping[str, Any]) -> MemberPanel:
    return MemberPanel(
        formation_date=data["formation_date"],
        asof=data["asof"],
        names=tuple(data["names"]),
        last_closes=dict(data["last_closes"]),
        marked=dict(data["marked"]),
    )


def book_to_json(book: BookState) -> dict[str, Any]:
    return {
        "formation_date": book.formation_date,
        "asof": book.asof,
        "width": book.width,
        "names": list(book.names),
        "values": dict(book.values),
        "last_closes": dict(book.last_closes),
        "marked": dict(book.marked),
    }


def book_from_json(data: Mapping[str, Any]) -> BookState:
    return BookState(
        formation_date=data["formation_date"],
        asof=data["asof"],
        width=data["width"],
        names=tuple(data["names"]),
        values=dict(data["values"]),
        last_closes=dict(data["last_closes"]),
        marked=dict(data["marked"]),
    )


# -- formation entry --------------------------------------------------


def record_formation_states(
    ledgers: Ledgers,
    formation_date: str,
    members: Sequence[str],
    books: Mapping[int, Sequence[str]],
    entry_closes: Mapping[str, float],
    run_utc: str,
) -> None:
    """Append the panel and book initial states for one formation.

    Entry closes are each name's last available close at or before the
    formation date, from the store's fresh rows. Equal weights at
    formation, so no pre-registration price history enters weight
    computation.
    """
    panel = initial_panel(formation_date, list(members), entry_closes)
    ledgers.formation.append(
        {
            "kind": "panel_init",
            "formation_date": formation_date,
            "panel": panel_to_json(panel),
            "run_utc": run_utc,
        }
    )
    for width in sorted(books):
        book = initial_book(
            formation_date, width, list(books[width]), entry_closes
        )
        ledgers.formation.append(
            {
                "kind": "book_init",
                "formation_date": formation_date,
                "width": width,
                "book": book_to_json(book),
                "run_utc": run_utc,
            }
        )


# -- ledger rebuild ---------------------------------------------------


def panel_inits(ledgers: Ledgers) -> list[MemberPanel]:
    records = [
        r
        for r in ledgers.formation.read_all()
        if r["kind"] == "panel_init"
    ]
    ordered = sorted(records, key=lambda r: str(r["formation_date"]))
    return [panel_from_json(r["panel"]) for r in ordered]


def book_inits(ledgers: Ledgers, width: int) -> list[BookState]:
    records = [
        r
        for r in ledgers.formation.read_all()
        if r["kind"] == "book_init" and r["width"] == width
    ]
    ordered = sorted(records, key=lambda r: str(r["formation_date"]))
    return [book_from_json(r["book"]) for r in ordered]


def _latest_panel_state(ledgers: Ledgers, init: MemberPanel) -> MemberPanel:
    best = init
    for r in ledgers.benchmark.read_all():
        if (
            r["status"] == "computed"
            and r["formation_date"] == init.formation_date
            and str(r["session"]) > best.asof
        ):
            best = panel_from_json(r["panel"])
    return best


def _latest_book_state(ledgers: Ledgers, init: BookState) -> BookState:
    best = init
    for r in ledgers.accrual.read_all():
        if (
            r["status"] == "computed"
            and r["width"] == init.width
            and r["formation_date"] == init.formation_date
            and str(r["session"]) > best.asof
        ):
            best = book_from_json(r["book"])
    return best


def benchmark_returns(ledgers: Ledgers) -> dict[str, float]:
    """session -> computed benchmark mean return."""
    out: dict[str, float] = {}
    for r in ledgers.benchmark.read_all():
        if r["status"] == "computed":
            out[str(r["session"])] = float(r["mean_return"])
    return out


def chain_pointers(ledgers: Ledgers) -> dict[str, str]:
    """Each chain's last accrued session, for the health view and the
    daily fetch span. Empty before the first formation."""
    out: dict[str, str] = {}
    panels = panel_inits(ledgers)
    if panels:
        out["benchmark"] = _latest_panel_state(ledgers, panels[-1]).asof
    for width in WIDTHS:
        books = book_inits(ledgers, width)
        if books:
            out[f"width_{width}"] = _latest_book_state(
                ledgers, books[-1]
            ).asof
    return out


def excess_series(ledgers: Ledgers, width: int) -> list[tuple[str, float]]:
    """(session, excess_bp) ascending, computed days only, first record
    per session wins because a computed day is history."""
    seen: dict[str, float] = {}
    for r in ledgers.accrual.read_all():
        if r["status"] == "computed" and r["width"] == width:
            seen.setdefault(str(r["session"]), float(r["excess_bp"]))
    return sorted(seen.items())


# -- processing -------------------------------------------------------


def process_pending(
    ledgers: Ledgers,
    view: BarView,
    sessions: Sequence[str],
    fetch_ok: bool,
    run_utc: str,
) -> dict[str, int]:
    """Accrue every pending session across lineages, in session order.

    `sessions` is the ascending calendar span from the first formation
    through the last complete session. Returns event counts for the
    health view.
    """
    counts = {
        "benchmark_computed": 0,
        "benchmark_excluded": 0,
        "accrual_computed": 0,
        "accrual_excluded": 0,
    }
    _process_benchmark(ledgers, view, sessions, fetch_ok, run_utc, counts)
    bench = benchmark_returns(ledgers)
    for width in WIDTHS:
        _process_book(
            ledgers, view, sessions, width, bench, fetch_ok, run_utc, counts
        )
    return counts


def _lineage_span(
    inits_dates: Sequence[str], k: int, sessions: Sequence[str]
) -> list[str]:
    """The sessions lineage k owns: after its formation, through the
    next formation date inclusive, or open-ended for the last."""
    start = inits_dates[k]
    end = inits_dates[k + 1] if k + 1 < len(inits_dates) else None
    return [
        s
        for s in sessions
        if s > start and (end is None or s <= end)
    ]


def _process_benchmark(
    ledgers: Ledgers,
    view: BarView,
    sessions: Sequence[str],
    fetch_ok: bool,
    run_utc: str,
    counts: dict[str, int],
) -> None:
    inits = panel_inits(ledgers)
    dates = [p.formation_date for p in inits]
    for k, init in enumerate(inits):
        panel = _latest_panel_state(ledgers, init)
        for session in _lineage_span(dates, k, sessions):
            if session <= panel.asof:
                continue
            states = classify_names(
                view, panel.names, session, fetch_ok, panel.marked
            )
            excluding = day_exclusion(states)
            if excluding:
                ledgers.benchmark.append(
                    {
                        "kind": "benchmark",
                        "status": "excluded",
                        "session": session,
                        "formation_date": init.formation_date,
                        **_excluding_detail(states, excluding),
                        "run_utc": run_utc,
                    }
                )
                counts["benchmark_excluded"] += 1
                break
            day = advance_panel(
                panel, session, states, _closes(view, panel.names, session)
            )
            mean = benchmark_daily_return(day.member_returns)
            ledgers.benchmark.append(
                {
                    "kind": "benchmark",
                    "status": "computed",
                    "session": session,
                    "formation_date": init.formation_date,
                    "mean_return": mean,
                    "n_members": len(panel.names),
                    "state_counts": _state_counts(states),
                    "panel": panel_to_json(day.panel),
                    "run_utc": run_utc,
                }
            )
            counts["benchmark_computed"] += 1
            panel = day.panel


def _process_book(
    ledgers: Ledgers,
    view: BarView,
    sessions: Sequence[str],
    width: int,
    bench: Mapping[str, float],
    fetch_ok: bool,
    run_utc: str,
    counts: dict[str, int],
) -> None:
    inits = book_inits(ledgers, width)
    dates = [b.formation_date for b in inits]
    for k, init in enumerate(inits):
        book = _latest_book_state(ledgers, init)
        for session in _lineage_span(dates, k, sessions):
            if session <= book.asof:
                continue
            if session not in bench:
                # The benchmark chain is blocked or excluded here. Its
                # record carries the exclusion. Retry heals both.
                break
            states = classify_names(
                view, book.names, session, fetch_ok, book.marked
            )
            excluding = day_exclusion(states)
            if excluding:
                ledgers.accrual.append(
                    {
                        "kind": "accrual",
                        "status": "excluded",
                        "session": session,
                        "width": width,
                        "formation_date": init.formation_date,
                        **_excluding_detail(states, excluding),
                        "run_utc": run_utc,
                    }
                )
                counts["accrual_excluded"] += 1
                break
            day = accrue_book_day(
                book, session, states, _closes(view, book.names, session)
            )
            excess_bp = (day.book_return - bench[session]) * 1e4
            ledgers.accrual.append(
                {
                    "kind": "accrual",
                    "status": "computed",
                    "session": session,
                    "width": width,
                    "formation_date": init.formation_date,
                    "book_return": day.book_return,
                    "benchmark_return": bench[session],
                    "excess_bp": excess_bp,
                    "name_states": {
                        n: s.value for n, s in states.items()
                    },
                    "book": book_to_json(day.state),
                    "run_utc": run_utc,
                }
            )
            counts["accrual_computed"] += 1
            book = day.state
