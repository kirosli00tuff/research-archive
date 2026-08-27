"""Section 0. The outcome map judges collection feasibility, never returns.

The fire function reads powers, the delisting-observability verdict, and two
census facts. It reads no outcome value: every input is a count-derived power
or an operational verdict. Committed with the registration, before any
network call, so the map cannot be fitted to what the census finds.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from npl.config import CONFIG, Config


class Section0Verdict(StrEnum):
    GO = "GO"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


class DelistingObservability(StrEnum):
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    FAIL = "FAIL"


@dataclass(frozen=True, slots=True)
class CoPrimaryPowers:
    """Power of each co-primary at the achievable event count by the deadline."""

    p1: float
    p2: float
    p3: float

    def minimum(self) -> float:
        return min(self.p1, self.p2, self.p3)


@dataclass(frozen=True, slots=True)
class Section0Gate:
    verdict: Section0Verdict
    cohort_basis: str
    rationale: str
    collectors_armed: bool


def _validate(powers: CoPrimaryPowers, label: str) -> None:
    for name, value in (("p1", powers.p1), ("p2", powers.p2), ("p3", powers.p3)):
        if not (value == value) or not 0.0 <= value <= 1.0:
            raise ValueError(f"{label}.{name} must be a probability in [0, 1], got {value!r}")


def fire_section0(
    *,
    powers_full: CoPrimaryPowers,
    powers_forward_only: CoPrimaryPowers,
    delisting: DelistingObservability,
    listing_dates_inferable: bool,
    funding_retention_ok: bool,
    cfg: Config = CONFIG,
) -> Section0Gate:
    """Fire the registered Section 0 verdict.

    GO: all three co-primaries at or above the 0.80 power floor at the
    achievable count by the projection deadline, and delisting observability
    passes in full.
    DEGRADED: any power in [0.50, 0.80), or delisting passes partially or
    fails, demoting the retrospective cohort to descriptive with the forward
    cohort carrying the verdict alone. Collection proceeds.
    BLOCKED: any co-primary under 0.50 power on the verdict-bearing cohort, or
    listing timestamps not inferable to plus or minus one day, or funding
    retention below the per-event coverage bar. Nothing armed beyond the
    census.
    """
    _validate(powers_full, "powers_full")
    _validate(powers_forward_only, "powers_forward_only")

    if not listing_dates_inferable:
        return Section0Gate(
            verdict=Section0Verdict.BLOCKED,
            cohort_basis="none",
            rationale=(
                "listing timestamps are not inferable to plus or minus one day. The event rule "
                "cannot anchor entries. Nothing is armed beyond the census."
            ),
            collectors_armed=False,
        )
    if not funding_retention_ok:
        return Section0Gate(
            verdict=Section0Verdict.BLOCKED,
            cohort_basis="none",
            rationale=(
                "funding retention is below the per-event coverage bar, so the funding leg of "
                "the outcome cannot be measured. Nothing is armed beyond the census."
            ),
            collectors_armed=False,
        )

    if delisting is DelistingObservability.PASS:
        powers = powers_full
        basis = "retro_plus_forward"
    else:
        powers = powers_forward_only
        basis = "forward_only"

    pmin = powers.minimum()
    if pmin < cfg.power_blocked_floor:
        return Section0Gate(
            verdict=Section0Verdict.BLOCKED,
            cohort_basis=basis,
            rationale=(
                f"the weakest co-primary reaches {pmin:.3f} power on the {basis} cohort at the "
                f"achievable count by {cfg.projection_deadline}, under the "
                f"{cfg.power_blocked_floor:.2f} floor. Nothing is armed beyond the census."
            ),
            collectors_armed=False,
        )
    if delisting is DelistingObservability.PASS and pmin >= cfg.power_go_floor:
        return Section0Gate(
            verdict=Section0Verdict.GO,
            cohort_basis=basis,
            rationale=(
                f"all three co-primaries reach at least {pmin:.3f} power at the achievable count "
                f"by {cfg.projection_deadline}, at or above the {cfg.power_go_floor:.2f} floor, "
                f"and delisting observability passes in full. Collectors are armed."
            ),
            collectors_armed=True,
        )
    if delisting is DelistingObservability.PASS:
        reason = (
            f"the weakest co-primary reaches {pmin:.3f} power, between the "
            f"{cfg.power_blocked_floor:.2f} and {cfg.power_go_floor:.2f} floors."
        )
    else:
        reason = (
            f"delisting observability is {delisting.value}, demoting the retrospective cohort "
            f"to descriptive. The forward cohort carries the verdict alone at {pmin:.3f} "
            f"minimum power."
        )
    return Section0Gate(
        verdict=Section0Verdict.DEGRADED,
        cohort_basis=basis,
        rationale=(
            f"{reason} Collection proceeds; recomputed power is stated beside the registered "
            f"{cfg.power_go_floor:.2f} target."
        ),
        collectors_armed=True,
    )
