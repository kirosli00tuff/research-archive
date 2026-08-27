"""Section 6 control assignment. Trailing-only reads, append-only pairs.

The matcher consumes FundingRow sequences that must end at or before the
event entry: a row stamped after the entry raises PostEntryRead loudly —
the pin the mutation exercise targets. The trailing mean reads only present
rates (the blindness gate already made post-entry rates Absent), and a
candidate under the coverage bar is skipped and counted, never guessed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from npl.absence import NO_CONTROL_CANDIDATE, AbsenceReason, Absent
from npl.blindness import FundingRow
from npl.clock import MS_PER_HOUR, iso_z, now_utc
from npl.config import CONFIG, Config
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import PAIRS_LEDGER


class PostEntryRead(RuntimeError):
    """A funding row stamped after the event entry reached the matcher."""


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


def _event_trailing_mean(
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


def assign_control(
    event_coin: str,
    dex: str,
    entry_ms: int,
    event_rows: tuple[FundingRow, ...],
    candidates: list[Candidate],
    cfg: Config = CONFIG,
    pairs_path: Path = PAIRS_LEDGER,
) -> ControlAssignment | Absent:
    """The registered rule: same dex, aged 180d+, coverage, nearest signed
    trailing mean, with replacement; ties to the older listing, then name."""
    event_mean = _event_trailing_mean(event_rows, entry_ms, cfg)
    if isinstance(event_mean, Absent):
        return event_mean

    considered = 0
    skipped = 0
    best: tuple[float, int, str, float] | None = None  # (distance, listing, name, mean)
    for candidate in candidates:
        considered += 1
        mean = trailing_mean(candidate.rows, entry_ms, cfg)
        if isinstance(mean, Absent):
            skipped += 1
            continue
        key = (abs(mean - event_mean), candidate.listing_open_ms, candidate.coin, mean)
        if best is None or key < best:
            best = key
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
    )
    AppendOnlyLedger(pairs_path).append(asdict(assignment))
    return assignment
