"""The bid-ask census: distinct observation windows, and the refusals between.

**All three legs are sampled, never the options alone.** The hedge leg is the MBT
front future, and the registered hedging rule trades it a median of 11 and a p90
of 16 times over the tenor (n = 1,955 paths, VRPExperiment). Measuring a spread on
the two option legs and omitting the future would understate the cost by the
larger part of it, since the hedge leg is traded an order of magnitude more often
than the straddle.

**What makes two windows distinct, in clock terms.** Registered in
REGISTRATION.md Section 3.5 before any window was appended:

    Two observation windows are distinct if and only if their local capture
    instants differ by at least 60 minutes, and at most 4 windows are drawn from
    any one UTC calendar day.

The mechanism behind both halves. An option book's touch persists over minutes,
so two samples inside an hour re-measure one book state and inflate ``n`` without
adding information. The per-day cap forces the sample across at least five
sessions, so the 90th percentile reflects variation between sessions rather than
within one afternoon. Together they fix the census at **five collection days
minimum for 20 windows**, which is why it is clock-bound and cannot be
compressed.

**A refused window is recorded, never dropped.** Dropping refusals to reach 20
would turn the count into a selection, and the selection would be on exactly the
book states the refusal conditions identify as unusual.

**A missed window is a gap, never a backfill.** The machine's internal fans are
not functioning, so the census runs as discrete sampling with the session closed
between windows rather than as a resident collector.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import final

from mbt.absence import AbsenceReason, Absent, Maybe
from mbt.clock import iso_utc, parse_utc
from mbt.provenance import Environment
from mbt.quotes import Quote, half_spread_bps, screen
from mbt.registry import (
    MAX_WINDOWS_PER_UTC_DAY,
    MIN_MINUTES_BETWEEN_WINDOWS,
    MIN_OBSERVATION_WINDOWS,
)

#: The three legs every window must carry. A window missing one is refused.
REQUIRED_LEGS = ("option_call", "option_put", "future_hedge")


class CensusDistinctnessError(ValueError):
    """A window failed the registered distinctness rule and was not appended."""


@final
@dataclass(frozen=True, slots=True)
class CensusWindow:
    """One accepted observation window across all three legs."""

    sequence: int
    local_ts: str
    environment: Environment
    legs: dict[str, Quote]
    half_spreads_bps: dict[str, float]
    straddle_round_trip_bps: float
    note: str = ""

    def as_row(self) -> dict[str, object]:
        return {
            "kind": "window",
            "sequence": self.sequence,
            "local_ts": self.local_ts,
            "environment": str(self.environment),
            "legs": {name: quote.as_row() for name, quote in self.legs.items()},
            "half_spreads_bps": dict(self.half_spreads_bps),
            "straddle_round_trip_bps": self.straddle_round_trip_bps,
            "note": self.note,
        }


@final
@dataclass(frozen=True, slots=True)
class RefusedWindow:
    """One window that failed a refusal condition. Recorded with its reason."""

    local_ts: str
    environment: Environment
    reason: str
    detail: str
    leg: str

    def as_row(self) -> dict[str, object]:
        return {
            "kind": "refusal",
            "local_ts": self.local_ts,
            "environment": str(self.environment),
            "reason": self.reason,
            "detail": self.detail,
            "leg": self.leg,
        }


def straddle_round_trip_bps(half_spreads: dict[str, float]) -> float:
    """Entry and exit on both option legs.

    A short straddle pays the call half-spread and the put half-spread on entry
    and again on exit, so the round trip is twice their sum. The hedge leg is
    reported separately because it is paid per rebalance, not per round trip, and
    adding it here would silently assume a rebalance count.
    """
    return 2.0 * (half_spreads["option_call"] + half_spreads["option_put"])


def check_distinct(candidate_local: datetime, accepted: list[CensusWindow]) -> None:
    """Apply the registered distinctness rule. Raises rather than silently skipping."""
    spacing = timedelta(minutes=MIN_MINUTES_BETWEEN_WINDOWS)
    same_day = 0
    for window in accepted:
        previous = parse_utc(window.local_ts, "check_distinct")
        if abs(candidate_local - previous) < spacing:
            raise CensusDistinctnessError(
                f"REFUSED: candidate window at {candidate_local.isoformat()} sits "
                f"{abs(candidate_local - previous).total_seconds() / 60:.1f} minutes "
                f"from the window at {window.local_ts}, inside the registered "
                f"{MIN_MINUTES_BETWEEN_WINDOWS}-minute spacing. An option book's "
                "touch persists over minutes, so a closer sample re-measures one "
                "book state and inflates n without adding information."
            )
        if previous.date() == candidate_local.date():
            same_day += 1
    if same_day >= MAX_WINDOWS_PER_UTC_DAY:
        raise CensusDistinctnessError(
            f"REFUSED: {same_day} windows are already recorded for UTC "
            f"{candidate_local.date().isoformat()}, at the registered cap of "
            f"{MAX_WINDOWS_PER_UTC_DAY} per day. The cap forces the sample across "
            "sessions so the 90th percentile reflects variation between them."
        )


def build_window(
    sequence: int,
    legs: dict[str, Quote],
    *,
    environment: Environment,
    notional: float,
    local_ts: datetime,
    note: str = "",
) -> CensusWindow | RefusedWindow:
    """Screen all three legs and build a window, or record the refusal.

    Every leg is screened before any is accepted, so a window is never half
    recorded. The first refusal decides, and its leg is named.
    """
    stamp = iso_utc(local_ts, "build_window")
    missing = [leg for leg in REQUIRED_LEGS if leg not in legs]
    if missing:
        return RefusedWindow(
            local_ts=stamp,
            environment=environment,
            reason=str(AbsenceReason.UNQUOTED_LEG),
            detail=(
                f"window is missing required leg(s) {missing}. A spread measured on "
                "options alone understates the hedge leg, which the registered rule "
                "trades a median of 11 and a p90 of 16 times over the tenor."
            ),
            leg=",".join(missing),
        )

    half_spreads: dict[str, float] = {}
    for leg in REQUIRED_LEGS:
        screened = screen(legs[leg])
        if isinstance(screened, Absent):
            return RefusedWindow(
                local_ts=stamp,
                environment=environment,
                reason=str(screened.reason),
                detail=screened.detail,
                leg=leg,
            )
        half_spreads[leg] = half_spread_bps(screened, notional)

    return CensusWindow(
        sequence=sequence,
        local_ts=stamp,
        environment=environment,
        legs=dict(legs),
        half_spreads_bps=half_spreads,
        straddle_round_trip_bps=straddle_round_trip_bps(half_spreads),
        note=note,
    )


@final
class CensusLedger:
    """Append-only census storage, ordered by the recorded clock on read.

    **Append order across processes is not a clock.** The census runs as discrete
    sampling with the session closed between windows, so rows are written by
    different processes at different times and the file order reflects whichever
    process flushed first. Every read sorts on the recorded local timestamp.
    """

    __slots__ = ("_path",)

    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return self._path

    def append(self, row: CensusWindow | RefusedWindow) -> None:
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row.as_row(), sort_keys=True) + "\n")

    def read_rows(self) -> list[dict[str, object]]:
        """Every row, ordered by the recorded clock rather than by append order."""
        if not self._path.exists():
            return []
        rows: list[dict[str, object]] = []
        for line in self._path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return sorted(rows, key=lambda row: str(row.get("local_ts", "")))

    def accepted(self) -> list[dict[str, object]]:
        return [row for row in self.read_rows() if row.get("kind") == "window"]

    def refusals(self) -> list[dict[str, object]]:
        return [row for row in self.read_rows() if row.get("kind") == "refusal"]


def percentile(values: list[float], fraction: float) -> Maybe[float]:
    """Linear-interpolated percentile. Refuses an empty sample rather than nan."""
    if not values:
        return Absent(
            AbsenceReason.INSUFFICIENT_SAMPLE,
            f"no observations, so the {fraction:.0%} percentile is absent and is "
            "never reported as zero or as nan.",
        )
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = fraction * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


@final
@dataclass(frozen=True, slots=True)
class CensusSummary:
    """What the census says so far, with its n in the same object as its numbers."""

    n_accepted: int
    n_refused: int
    n_required: int
    meets_minimum: bool
    median_bps: Maybe[float]
    p90_bps: Maybe[float]
    refusal_reasons: dict[str, int]

    def as_row(self) -> dict[str, object]:
        return {
            "n_accepted": self.n_accepted,
            "n_refused": self.n_refused,
            "n_required": self.n_required,
            "meets_minimum": self.meets_minimum,
            "median_bps": _maybe_row(self.median_bps),
            "p90_bps": _maybe_row(self.p90_bps),
            "refusal_reasons": dict(self.refusal_reasons),
        }


def _maybe_row(value: Maybe[float]) -> object:
    return value.as_row() if isinstance(value, Absent) else value


def summarise(ledger: CensusLedger) -> CensusSummary:
    """Summarise the census as it stands, refusals counted rather than dropped."""
    accepted = ledger.accepted()
    refusals = ledger.refusals()
    values = [float(row["straddle_round_trip_bps"]) for row in accepted]  # type: ignore[arg-type]
    reasons: dict[str, int] = {}
    for row in refusals:
        key = str(row.get("reason", "unknown"))
        reasons[key] = reasons.get(key, 0) + 1
    return CensusSummary(
        n_accepted=len(accepted),
        n_refused=len(refusals),
        n_required=MIN_OBSERVATION_WINDOWS,
        meets_minimum=len(accepted) >= MIN_OBSERVATION_WINDOWS,
        median_bps=percentile(values, 0.50),
        p90_bps=percentile(values, 0.90),
        refusal_reasons=reasons,
    )


def window_stub_from_row(row: dict[str, object]) -> CensusWindow:
    """Rebuild only what the distinctness rule reads: the recorded local clock.

    The legs and the half-spreads are deliberately left empty. Rehydrating them
    would mean reconstructing a Quote from its artifact form, and a
    reconstruction that is never compared against the original is a second
    representation of the same fact with nothing keeping the two in step.
    :func:`check_distinct` reads ``local_ts`` and nothing else.
    """
    raw_sequence = row.get("sequence", 0)
    sequence = int(raw_sequence) if isinstance(raw_sequence, (int, float, str)) else 0
    raw_bps = row.get("straddle_round_trip_bps", 0.0)
    bps = float(raw_bps) if isinstance(raw_bps, (int, float, str)) else 0.0
    return CensusWindow(
        sequence=sequence,
        local_ts=str(row.get("local_ts", "")),
        environment=Environment(str(row.get("environment", "paper"))),
        legs={},
        half_spreads_bps={},
        straddle_round_trip_bps=bps,
    )
