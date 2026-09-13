"""Section 6 control assignment. Trailing-only reads, append-only pairs.

The matcher consumes FundingRow sequences that must end at or before the
event entry: a row stamped after the entry raises PostEntryRead loudly —
the pin the mutation exercise targets. The trailing mean reads only present
rates (the blindness gate already made post-entry rates Absent), and a
candidate under the coverage bar is skipped and counted, never guessed.

Amendment H2-3 Change 1 adds the fallback control: where the same-dex
candidate set is empty — nothing on the event's dex meets both the 180-day
age condition and the coverage condition — the main-dex candidate set is
consulted under the identical distance, tie-break, and replacement rules.
Every assignment carries `pair_type` (`same_dex` | `cross_dex`) and the
control's own dex. The tag never filters anything; it names a stratum.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol

from npl.absence import NO_CONTROL_CANDIDATE, AbsenceReason, Absent
from npl.blindness import FundingRow
from npl.clock import MS_PER_HOUR, iso_z, now_utc
from npl.config import CONFIG, Config
from npl.ledger.append_only import AppendOnlyLedger
from npl.pairtype import PAIR_TYPE_CROSS_DEX, PAIR_TYPE_SAME_DEX, REGISTERED_PAIR_TYPES
from npl.paths import PAIRS_LEDGER


class PostEntryRead(RuntimeError):
    """A funding row stamped after the event entry reached the matcher."""


# Amendment H2-3 Change 1: the registered pair types live in npl.pairtype so
# the dark reader can name a stratum without importing a path-owning module.
MAIN_DEX = ""


class CandidateLike(Protocol):
    """What the registered selection reads off a candidate, and nothing more.

    Structural, so the tiered selector of Amendment H2-5 runs the identical
    distance, tie-break, and coverage rules over its own richer record without
    either module reaching into the other's privates.
    """

    @property
    def coin(self) -> str: ...

    @property
    def listing_open_ms(self) -> int: ...

    @property
    def rows(self) -> tuple[FundingRow, ...]: ...


@dataclass(frozen=True, slots=True)
class Candidate:
    coin: str
    listing_open_ms: int
    rows: tuple[FundingRow, ...]


@dataclass(frozen=True, slots=True)
class ControlAssignment:
    event_coin: str
    control_coin: str
    dex: str
    entry_ms: int
    event_trailing_mean: float
    control_trailing_mean: float
    candidates_considered: int
    candidates_skipped_low_coverage: int
    assigned_at: str
    control_dex: str = MAIN_DEX
    pair_type: str = PAIR_TYPE_SAME_DEX


def trailing_mean(
    rows: tuple[FundingRow, ...], entry_ms: int, cfg: Config = CONFIG
) -> float | Absent:
    """Mean hourly funding over (entry - 168h, entry]. Trailing only, by pin."""
    for row in rows:
        if row.time_ms > entry_ms:
            raise PostEntryRead(
                f"a funding row stamped {row.time_ms} reached the matcher for an entry at "
                f"{entry_ms}. Matching reads no row stamped after the event entry."
            )
    window_start = entry_ms - cfg.control_trailing_window_hours * MS_PER_HOUR
    values: list[float] = []
    hours: set[int] = set()
    for row in rows:
        if window_start < row.time_ms <= entry_ms and not isinstance(row.rate, Absent):
            values.append(row.rate)
            hours.add(row.time_ms // MS_PER_HOUR)
    coverage = len(hours) / cfg.control_trailing_window_hours
    if coverage < cfg.funding_coverage_bar:
        return Absent(AbsenceReason.NO_FUNDING_ROWS)
    return sum(values) / len(values)


def event_trailing_mean(
    event_rows: tuple[FundingRow, ...], entry_ms: int, cfg: Config
) -> float | Absent:
    """The event's own trailing mean over its short life; partial by design."""
    for row in event_rows:
        if row.time_ms > entry_ms:
            raise PostEntryRead(
                f"the event's own funding rows extend past its entry ({row.time_ms} > {entry_ms})"
            )
    window_start = entry_ms - cfg.control_trailing_window_hours * MS_PER_HOUR
    values = [
        row.rate
        for row in event_rows
        if window_start < row.time_ms <= entry_ms and not isinstance(row.rate, Absent)
    ]
    if not values:
        return Absent(AbsenceReason.NO_FUNDING_ROWS)
    return sum(values) / len(values)


@dataclass(frozen=True, slots=True)
class Selection:
    """The registered selection's result: the winner and who was examined.

    `considered` and `skipped` carry **coin names, not counts**, because the
    tiered rule of Amendment H2-5 examines nested pools and a bare counter
    would report the same candidate two or three times. Callers take `len()`
    of a set where they want a count.
    """

    best: tuple[float, int, str, float] | None  # (distance, listing, name, mean)
    considered: tuple[str, ...]
    skipped: tuple[str, ...]


def nearest_by_funding(
    candidates: Sequence[CandidateLike], entry_ms: int, event_mean: float, cfg: Config
) -> Selection:
    """The nearest signed trailing mean under the registered distance and ties.

    The key orders by |distance|, then the earlier listing date, then coin
    name ascending — the registered tie-break, verbatim. A candidate whose
    trailing mean is Absent (under the coverage bar) is skipped and recorded,
    never guessed.
    """
    considered: list[str] = []
    skipped: list[str] = []
    best: tuple[float, int, str, float] | None = None
    for candidate in candidates:
        considered.append(candidate.coin)
        mean = trailing_mean(candidate.rows, entry_ms, cfg)
        if isinstance(mean, Absent):
            skipped.append(candidate.coin)
            continue
        key = (abs(mean - event_mean), candidate.listing_open_ms, candidate.coin, mean)
        if best is None or key < best:
            best = key
    return Selection(best=best, considered=tuple(considered), skipped=tuple(skipped))


def assign_control(
    event_coin: str,
    dex: str,
    entry_ms: int,
    event_rows: tuple[FundingRow, ...],
    candidates: list[Candidate],
    cfg: Config = CONFIG,
    pairs_path: Path = PAIRS_LEDGER,
    fallback_candidates: list[Candidate] | None = None,
) -> ControlAssignment | Absent:
    """The registered rule: same dex, aged 180d+, coverage, nearest signed
    trailing mean, with replacement; ties to the older listing, then name.

    Amendment H2-3 Change 1: `fallback_candidates` are the main-dex elders
    meeting the same conditions. They are consulted **only** where the
    same-dex set yields nothing — a same-dex candidate always wins — and the
    resulting pair is tagged `cross_dex`.
    """
    event_mean = event_trailing_mean(event_rows, entry_ms, cfg)
    if isinstance(event_mean, Absent):
        return event_mean

    selection = nearest_by_funding(candidates, entry_ms, event_mean, cfg)
    best = selection.best
    considered = len(selection.considered)
    skipped = len(selection.skipped)
    pair_type = PAIR_TYPE_SAME_DEX
    control_dex = dex
    if best is None and fallback_candidates:
        fallback = nearest_by_funding(fallback_candidates, entry_ms, event_mean, cfg)
        considered += len(fallback.considered)
        skipped += len(fallback.skipped)
        if fallback.best is not None:
            best = fallback.best
            pair_type = PAIR_TYPE_CROSS_DEX
            control_dex = MAIN_DEX
    if best is None:
        return NO_CONTROL_CANDIDATE
    assignment = ControlAssignment(
        event_coin=event_coin,
        control_coin=best[2],
        dex=dex,
        entry_ms=entry_ms,
        event_trailing_mean=event_mean,
        control_trailing_mean=best[3],
        candidates_considered=considered,
        candidates_skipped_low_coverage=skipped,
        assigned_at=iso_z(now_utc()),
        control_dex=control_dex,
        pair_type=pair_type,
    )
    AppendOnlyLedger(pairs_path).append(asdict(assignment))
    return assignment


def pair_type_of_row(row: dict[str, object]) -> str:
    """The pair type of one ledger row, per Amendment H2-3 Change 1.

    A row written before the amendment carries no `pair_type` field: the
    rule in force when it was written admitted same-dex candidates only, so
    it is `same_dex` **by the registered rule that produced it**, not by
    imputation of a missing value. A row carrying an unregistered tag is a
    loud refusal, never a silent default.
    """
    tag = row.get("pair_type", PAIR_TYPE_SAME_DEX)
    if tag not in REGISTERED_PAIR_TYPES:
        raise ValueError(
            f"unregistered pair_type {tag!r} on pair row {row.get('event_coin')!r}; "
            f"the registered types are {PAIR_TYPE_SAME_DEX!r} and {PAIR_TYPE_CROSS_DEX!r}"
        )
    return str(tag)


def control_dex_of_row(row: dict[str, object]) -> str:
    """The control leg's own dex. Pre-amendment rows are same-dex by rule."""
    if "control_dex" in row:
        return str(row["control_dex"])
    if pair_type_of_row(row) == PAIR_TYPE_CROSS_DEX:
        raise ValueError(
            f"a cross_dex pair row for {row.get('event_coin')!r} carries no control_dex; "
            f"every row written after Amendment H2-3 carries one"
        )
    return str(row.get("dex", MAIN_DEX))
