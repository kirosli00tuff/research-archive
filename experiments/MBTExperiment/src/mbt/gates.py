"""Guard three — paper figures are never verdict-bearing.

A gate is the only place a measurement becomes a verdict, so it is the only place
worth putting the admissibility check. Any attempt to fire a gate from a figure
whose environment does not admit it **raises**. It does not warn, does not
degrade to a qualified pass, and does not record a softened result.

**Admissibility is a function of the provenance KIND, not of the environment
alone**, because the three kinds are not equally blocked:

- a **margin** is a property of the ACCOUNT, so paper is inadmissible outright;
- a **commission report** is a property of the FILL, and paper fills are
  simulated, so paper is inadmissible outright;
- a **quote** is a property of the MARKET DATA FEED, which IBKR routes by
  subscription rather than by account type, so paper **is** admissible when the
  tick is real-time and inadmissible when it is not.

That third rule rests on a **documented claim, not a measurement**, and every
result it admits says so. See REGISTRATION.md Section 0.5.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, unique
from typing import final

from mbt.absence import Absent, Maybe
from mbt.clock import iso_utc, utc_now
from mbt.figures import Figure, TickDelayStatus
from mbt.provenance import Environment, ProvenanceKind


@unique
class GateName(StrEnum):
    """The two registered gates. This stage fires at most one of them."""

    MARGIN = "margin"
    """Initial margin on a short MBT option, against 12.80% of notional."""

    COST = "cost"
    """The absent cost legs at p90, against the registered ceiling."""


@unique
class GateOutcome(StrEnum):
    """What a gate did. ABSENT is a recorded state, never an omission."""

    PASS = "pass"
    FAIL = "fail"
    ABSENT = "absent"


class InadmissibleFigureError(PermissionError):
    """Base class for a figure a gate refuses to read."""


class PaperFigureInadmissibleError(InadmissibleFigureError):
    """A paper-tagged figure reached a gate. **Pinned by test.**

    A paper margin read is development evidence. Promoting one into a verdict is
    the single failure this repository's paper-only clause exists to prevent.
    """


class DelayedQuoteInadmissibleError(InadmissibleFigureError):
    """A quote that was not real-time reached a gate.

    A delayed tick carries a stale and artificially wide spread. Admitting one
    would measure the delay rather than the venue, and widening it into a cost
    band would bake the delay into a verdict.
    """


@final
@dataclass(frozen=True, slots=True)
class GateResult:
    """What a gate decided, and on what. Carries its own reason either way."""

    gate: GateName
    outcome: GateOutcome
    ceiling: float
    unit: str
    measured: float | None
    reason: str
    fired_at: str
    figure_name: str = ""
    environment: str = ""
    admissibility_note: str = ""

    def as_row(self) -> dict[str, object]:
        return {
            "gate": str(self.gate),
            "outcome": str(self.outcome),
            "ceiling": self.ceiling,
            "unit": self.unit,
            "measured": self.measured,
            "reason": self.reason,
            "fired_at": self.fired_at,
            "figure_name": self.figure_name,
            "environment": self.environment,
            "admissibility_note": self.admissibility_note,
        }


#: Kinds whose environment must be LIVE. A margin belongs to the account and a
#: commission report belongs to the fill; paper simulates both.
_LIVE_ONLY_KINDS = frozenset({ProvenanceKind.MARGIN, ProvenanceKind.COMMISSION_REPORT})

_PAPER_QUOTE_ADMISSIBILITY_NOTE = (
    "DOCUMENTED, NOT MEASURED: this quote was taken on a paper session and is "
    "admitted because IBKR routes market data by subscription rather than by "
    "account type. That is a claim resting on IBKR's published routing, not a "
    "measurement made here, and it is re-verified against a live session "
    "whenever one becomes available. Measured beats documented, and this one is "
    "currently documented."
)


def require_admissible(figure: Figure, gate: GateName) -> str:
    """Refuse a figure whose provenance does not admit it. Returns any caveat.

    Raises rather than returning a flag, because a caller that can ignore a flag
    will eventually ignore it.
    """
    if figure.kind in _LIVE_ONLY_KINDS and figure.environment is Environment.PAPER:
        raise PaperFigureInadmissibleError(
            f"REFUSED: figure {figure.name!r} of kind {figure.kind.value!r} is "
            f"tagged environment {figure.environment.value!r} and reached the "
            f"{gate.value!r} gate. A {figure.kind.value} is a property of the "
            "account or the fill, both of which paper simulates, so a paper one "
            "is development evidence and is never verdict-bearing."
        )
    if figure.kind is ProvenanceKind.QUOTE:
        if figure.tick_delay is not TickDelayStatus.REALTIME:
            raise DelayedQuoteInadmissibleError(
                f"REFUSED: quote {figure.name!r} carries tick delay status "
                f"{figure.tick_delay.value!r} and reached the {gate.value!r} "
                "gate. Only a real-time tick is admissible. A delayed quote's "
                "spread is stale and artificially wide, and is never widened "
                "into a cost band."
            )
        if figure.environment is Environment.PAPER:
            return _PAPER_QUOTE_ADMISSIBILITY_NOTE
    return ""


def fire_lower_bound(
    gate: GateName,
    lower_bound: float,
    *,
    ceiling: float,
    unit: str,
    absent_legs: list[str],
) -> GateResult:
    """Fire a gate against a STRICT LOWER BOUND on the cost. Never returns PASS.

    When one cost leg is a recorded absence, the all-in cost is absent too, and
    `Absent` refuses the arithmetic that would sum it. But the legs that ARE
    measured still form a strict lower bound, because every absent leg is
    non-negative, and **a lower bound is a real constraint even though it is not
    the cost**.

    The constraint is one-sided, and that asymmetry is the whole point:

    - if the lower bound **exceeds** the ceiling, the true cost exceeds it too,
      and **FAIL is sound**;
    - if the lower bound sits **at or below** the ceiling, nothing follows, since
      the absent legs could carry the total anywhere above it, and the result is
      **ABSENT rather than PASS**.

    So a gate with an absent leg **can close a question negatively and can never
    close it positively.** VRPExperiment used its commission-only bound exactly
    this way: a lower bound is used as a constraint and never reported as the
    cost.
    """
    fired_at = iso_utc(utc_now(), "gates.fire_lower_bound")
    legs = ", ".join(absent_legs) if absent_legs else "none"
    if lower_bound > ceiling:
        return GateResult(
            gate=gate,
            outcome=GateOutcome.FAIL,
            ceiling=ceiling,
            unit=unit,
            measured=lower_bound,
            reason=(
                f"the measured legs alone reach {lower_bound} {unit}, above the "
                f"registered ceiling of {ceiling} {unit}. Every absent leg is "
                f"non-negative, so the true cost is at least this and FAIL is "
                f"sound on a lower bound. Absent legs: {legs}."
            ),
            fired_at=fired_at,
            admissibility_note="fired on a strict lower bound, which can FAIL but never PASS",
        )
    return GateResult(
        gate=gate,
        outcome=GateOutcome.ABSENT,
        ceiling=ceiling,
        unit=unit,
        measured=None,
        reason=(
            f"the measured legs reach {lower_bound} {unit}, at or below the "
            f"registered ceiling of {ceiling} {unit}, and nothing follows from "
            f"that. The absent legs are non-negative and unbounded above by any "
            f"evidence here, so they could carry the total past the ceiling. A "
            f"PASS cannot be concluded from a lower bound. Absent legs: {legs}."
        ),
        fired_at=fired_at,
        admissibility_note="fired on a strict lower bound, which can FAIL but never PASS",
    )


def fire(
    gate: GateName,
    figure: Maybe[Figure],
    *,
    ceiling: float,
    unit: str,
) -> GateResult:
    """Fire one gate against one figure, or record why it could not fire.

    A gate handed an :class:`Absent` records ABSENT with the absence's reason. It
    never treats the absence as zero, and it never quietly omits the gate from a
    verdict table.
    """
    fired_at = iso_utc(utc_now(), "gates.fire")
    if isinstance(figure, Absent):
        return GateResult(
            gate=gate,
            outcome=GateOutcome.ABSENT,
            ceiling=ceiling,
            unit=unit,
            measured=None,
            reason=(
                f"Absent({figure.reason}): {figure.detail}. An absent gate is a "
                "recorded state carrying its reason. It is never an unfired gate "
                "omitted from a verdict table, and never a paper figure promoted "
                "to stand in for a live one."
            ),
            fired_at=fired_at,
        )

    caveat = require_admissible(figure, gate)
    passed = figure.value <= ceiling
    return GateResult(
        gate=gate,
        outcome=GateOutcome.PASS if passed else GateOutcome.FAIL,
        ceiling=ceiling,
        unit=unit,
        measured=figure.value,
        reason=(
            f"measured {figure.value} {unit} against a registered ceiling of "
            f"{ceiling} {unit}: {'at or below' if passed else 'above'} the ceiling"
        ),
        fired_at=fired_at,
        figure_name=figure.name,
        environment=str(figure.environment),
        admissibility_note=caveat,
    )
