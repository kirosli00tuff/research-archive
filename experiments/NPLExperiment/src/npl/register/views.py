"""Per-hypothesis eligibility views over the one substrate.

One census, one watcher, one funding recorder, one checkpoint scheduler —
and these views on top. A view is a pure function from fresh events (plus
registered pre-entry inputs) to an eligibility decision per event, with
exclusion reasons counted. Every view refuses the generating sample first:
the 312 H1 retro events cannot enter any successor statistic, and the
refusal is produced by test. Nothing here reads an outcome value; the only
funding input is the pre-entry trailing mean of standing rule 13.
"""

from __future__ import annotations

from dataclasses import dataclass

from npl.absence import Absent
from npl.config import CONFIG, Config
from npl.register.conditioning import cell_clears, threshold_cells
from npl.register.generating_sample import refuse_generating_sample

MAIN_DEX = ""


@dataclass(frozen=True, slots=True)
class FreshEvent:
    """One fresh-cohort event: identity, timestamps, and tag. No outcome."""

    coin: str
    dex: str
    event_type: str
    listing_open_ms: int
    entry_ms: int

    def event_id(self) -> str:
        return f"{self.coin}|{self.dex}|{self.listing_open_ms}"


@dataclass(frozen=True, slots=True)
class ViewRow:
    """One event's decision under one view. reason is empty iff eligible."""

    event: FreshEvent
    eligible: bool
    reason: str


@dataclass(frozen=True, slots=True)
class ViewResult:
    """One hypothesis view over the fresh cohort, reasons counted."""

    hypothesis: str
    rows: tuple[ViewRow, ...]

    def eligible_events(self) -> tuple[FreshEvent, ...]:
        return tuple(row.event for row in self.rows if row.eligible)

    def excluded_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for row in self.rows:
            if not row.eligible:
                counts[row.reason] = counts.get(row.reason, 0) + 1
        return counts


def _require_fresh(events: tuple[FreshEvent, ...], sample: frozenset[str]) -> None:
    refuse_generating_sample((event.event_id() for event in events), sample)


def h2_pairable_view(
    events: tuple[FreshEvent, ...],
    candidate_counts: dict[str, int],
    sample: frozenset[str],
) -> ViewResult:
    """H2: fresh events with at least one Section 6 candidate on their dex.

    candidate_counts is keyed by event_id and comes from the census by
    listing dates (the A.2 feasibility count). A missing count is a
    recorded measurement gap, never a zero.
    """
    _require_fresh(events, sample)
    rows: list[ViewRow] = []
    for event in events:
        count = candidate_counts.get(event.event_id())
        if count is None:
            rows.append(ViewRow(event, False, "candidate_count_unmeasured"))
        elif count <= 0:
            rows.append(ViewRow(event, False, "no_control_candidate"))
        else:
            rows.append(ViewRow(event, True, ""))
    return ViewResult(hypothesis="H2", rows=tuple(rows))


def h3_main_dex_view(events: tuple[FreshEvent, ...], sample: frozenset[str]) -> ViewResult:
    """H3: the mechanical instrument-class rule. Reads the dex field only."""
    _require_fresh(events, sample)
    rows = tuple(
        ViewRow(event, True, "")
        if event.dex == MAIN_DEX
        else ViewRow(event, False, "hip3_builder_dex")
        for event in events
    )
    return ViewResult(hypothesis="H3", rows=rows)


def h4_conditioned_view(
    events: tuple[FreshEvent, ...],
    trailing_means: dict[str, float | Absent],
    sample: frozenset[str],
    cfg: Config = CONFIG,
) -> dict[str, ViewResult]:
    """H4: one view per registered threshold cell, keyed by cell label.

    trailing_means is keyed by event_id: the signed trailing 168h mean
    hourly funding at entry (pre-entry feature, rule 13). An Absent mean is
    a recorded absence and excludes the event from every cell, counted.
    """
    _require_fresh(events, sample)
    out: dict[str, ViewResult] = {}
    for cell in threshold_cells(cfg):
        rows: list[ViewRow] = []
        for event in events:
            mean = trailing_means.get(event.event_id())
            if mean is None:
                rows.append(ViewRow(event, False, "trailing_funding_unmeasured"))
            elif isinstance(mean, Absent):
                rows.append(ViewRow(event, False, f"trailing_funding_absent_{mean.reason.value}"))
            elif cell_clears(mean, cell):
                rows.append(ViewRow(event, True, ""))
            else:
                rows.append(ViewRow(event, False, "above_threshold"))
        out[cell.label] = ViewResult(hypothesis=f"H4:{cell.label}", rows=tuple(rows))
    return out
