"""Coverage accounting. Counts rows and timestamps only — never a value.

Operational health and sample composition never merge: the reasons this
module reports are drawn from the registered set {rate_limited,
source_failed, not_yet_attempted}, plus the loud `expired` record for a
closed catch-up window. An under-covered event reports underpowered, never
a negative.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from npl.blindness import CandleTimes, FundingRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR
from npl.config import CONFIG, Config
from npl.intervals import total_covered_ms
from npl.pairtype import REGISTERED_PAIR_TYPES


class CoverageReason(StrEnum):
    RATE_LIMITED = "rate_limited"
    SOURCE_FAILED = "source_failed"
    NOT_YET_ATTEMPTED = "not_yet_attempted"


@dataclass(frozen=True, slots=True)
class WindowCoverage:
    expected: int
    present: int

    def share(self) -> float:
        if self.expected <= 0:
            return 0.0
        return self.present / self.expected


def candle_day_coverage(times: CandleTimes, start_ms: int, end_ms: int) -> WindowCoverage:
    """Days in [start, end) with a served daily candle, unioned before counting."""
    expected = max(0, (end_ms - start_ms) // MS_PER_DAY)
    windows = [
        (max(open_ms, start_ms), min(open_ms + MS_PER_DAY, end_ms))
        for open_ms in times.open_ms
        if open_ms + MS_PER_DAY > start_ms and open_ms < end_ms
    ]
    covered_days = total_covered_ms(windows) // MS_PER_DAY
    return WindowCoverage(expected=int(expected), present=int(covered_days))


def funding_hour_coverage(
    rows: tuple[FundingRow, ...], start_ms: int, end_ms: int
) -> WindowCoverage:
    """Distinct hours in (start, end] carrying a funding row. Timestamps only."""
    expected = max(0, (end_ms - start_ms) // MS_PER_HOUR)
    hours = {row.time_ms // MS_PER_HOUR for row in rows if start_ms < row.time_ms <= end_ms}
    return WindowCoverage(expected=int(expected), present=len(hours))


@dataclass(frozen=True, slots=True)
class EventCoverage:
    coin: str
    candles: WindowCoverage
    funding: WindowCoverage
    meets_bars: bool
    label: str


def assess_event_coverage(
    coin: str,
    candles: WindowCoverage,
    funding: WindowCoverage,
    cfg: Config = CONFIG,
) -> EventCoverage:
    """MIN_OUTCOME_COVERAGE: 0.90 candles, 0.95 funding hours. Under-covered
    reports `underpowered`, never a negative."""
    ok = (
        candles.share() >= cfg.min_outcome_coverage_candles
        and funding.share() >= cfg.min_outcome_coverage_funding
    )
    return EventCoverage(
        coin=coin,
        candles=candles,
        funding=funding,
        meets_bars=ok,
        label="covered" if ok else "underpowered",
    )


@dataclass(frozen=True, slots=True)
class PairTypeCoverage:
    """Pair counts for one registered pair type. Counts only, never a value."""

    pair_type: str
    pairs: int
    covered: int
    underpowered: int

    def share(self) -> float:
        return (self.covered / self.pairs) if self.pairs else 0.0


def coverage_by_pair_type(
    pairs: Iterable[tuple[str, bool]],
) -> tuple[PairTypeCoverage, ...]:
    """Amendment H2-3 Change 1: coverage reported per pair type.

    Takes (pair_type, both_legs_meet_bars) per pair. Every registered pair
    type appears in the result even at zero pairs — an absent row would read
    as "no such pairs" where the truth is "none yet", and an unregistered
    tag is a loud refusal, never a new bucket.
    """
    counted = {t: [0, 0] for t in REGISTERED_PAIR_TYPES}
    for pair_type, covered in pairs:
        if pair_type not in counted:
            raise ValueError(
                f"unregistered pair_type {pair_type!r} in a coverage view; "
                f"the registered types are {list(REGISTERED_PAIR_TYPES)}"
            )
        counted[pair_type][0] += 1
        counted[pair_type][1] += int(covered)
    return tuple(
        PairTypeCoverage(
            pair_type=pair_type, pairs=total, covered=covered, underpowered=total - covered
        )
        for pair_type, (total, covered) in counted.items()
    )
