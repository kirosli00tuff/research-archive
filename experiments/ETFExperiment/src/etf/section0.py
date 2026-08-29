"""Section 0. The outcome map judges collection feasibility and detectability, never returns.

The fire function reads powers, the as-printed observability verdict, and one
measured stability share. It reads no outcome value: every input is a
count-derived power or an operational verdict. Committed with the registration,
before any network call, so the map cannot be fitted to what the census finds.

Registered expectation, stated in the registration before any data exists: the
Section 9 arithmetic and the decay evidence point to DEGRADED. A DEGRADED here
narrows a question rather than abandoning it, and a BLOCKED is a documented
answer, not a failure of process.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from etf.config import CONFIG, Config
from etf.observability import Observability

# A measured revision rate high enough that no stable as-printed value exists
# before the entry anchor on a MAJORITY of days fires BLOCKED. "Majority" is
# strictly more than half, and the fixture in tests sits exactly on 0.50.
MAJORITY = 0.50


class Section0Verdict(StrEnum):
    GO = "GO"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class CoPrimaryPowers:
    """Power of each co-primary at one effect assumption and one achievable N."""

    e1: float
    e2: float

    def minimum(self) -> float:
        return min(self.e1, self.e2)


@dataclass(frozen=True, slots=True)
class Section0Gate:
    verdict: Section0Verdict
    rationale: str
    collectors_armed: bool
    verdict_scope: str


# The plain-words narrowing the registration requires under DEGRADED, stated
# before any data exists so it cannot be written to fit a disappointment.
DEGRADED_SCOPE = (
    "Under DEGRADED a Stage B FAIL establishes that the effect is not present at its "
    "published magnitude, and cannot distinguish a decayed effect from no effect at all."
)
GO_SCOPE = (
    "Under GO a Stage B FAIL establishes that the effect is not present at the registered "
    "half-published magnitude on this sample."
)
BLOCKED_SCOPE = (
    "Under BLOCKED nothing is armed beyond the census. The registered design cannot resolve "
    "the effect on the data this repository can obtain, and that is the finding."
)


def _validate(powers: CoPrimaryPowers, label: str) -> None:
    for name, value in (("e1", powers.e1), ("e2", powers.e2)):
        if value != value or not 0.0 <= value <= 1.0:
            raise ValueError(f"{label}.{name} must be a probability in [0, 1], got {value!r}")


def fire_section0(
    *,
    powers_registered: CoPrimaryPowers,
    powers_published: CoPrimaryPowers,
    observability: Observability,
    unstable_asprinted_share: float,
    cfg: Config = CONFIG,
) -> Section0Gate:
    """Fire the registered Section 0 verdict.

    `powers_registered` are the co-primary powers at the registered effect
    assumption (rank correlation 0.09) at the achievable admissible-day count
    by the projection deadline. `powers_published` are the same powers at the
    undecayed published magnitude (0.18). `unstable_asprinted_share` is the
    measured share of days on which no stable as-printed value exists before
    the entry anchor.
    """
    _validate(powers_registered, "powers_registered")
    _validate(powers_published, "powers_published")
    if unstable_asprinted_share != unstable_asprinted_share or not (
        0.0 <= unstable_asprinted_share <= 1.0
    ):
        raise ValueError(
            f"unstable_asprinted_share must be a share in [0, 1], got {unstable_asprinted_share!r}"
        )

    # --- BLOCKED, three independent triggers, checked first -----------------
    if observability is Observability.FAIL:
        return Section0Gate(
            verdict=Section0Verdict.BLOCKED,
            rationale=(
                "as-printed observability fired FAIL: neither the archive capture density nor "
                "the forward revision integrity bar holds, so no admissible as-printed cohort "
                "exists. Nothing is armed beyond the census."
            ),
            collectors_armed=False,
            verdict_scope=BLOCKED_SCOPE,
        )
    if unstable_asprinted_share > MAJORITY:
        return Section0Gate(
            verdict=Section0Verdict.BLOCKED,
            rationale=(
                f"the measured revision rate leaves no stable as-printed value before the entry "
                f"anchor on {unstable_asprinted_share:.4f} of days, a majority. The signal the "
                f"registered rule trades on does not exist at the anchor. Nothing is armed "
                f"beyond the census."
            ),
            collectors_armed=False,
            verdict_scope=BLOCKED_SCOPE,
        )
    if powers_published.e1 < cfg.power_blocked_floor:
        return Section0Gate(
            verdict=Section0Verdict.BLOCKED,
            rationale=(
                f"E1 reaches {powers_published.e1:.4f} power at the undecayed published-magnitude "
                f"assumption at the achievable admissible-day count by {cfg.projection_deadline}, "
                f"under the registered {cfg.power_blocked_floor:.2f} floor. The design cannot "
                f"detect even the effect as published. Nothing is armed beyond the census."
            ),
            collectors_armed=False,
            verdict_scope=BLOCKED_SCOPE,
        )

    # --- GO -----------------------------------------------------------------
    if observability is Observability.PASS and powers_registered.minimum() >= cfg.power_go_floor:
        return Section0Gate(
            verdict=Section0Verdict.GO,
            rationale=(
                f"both co-primaries reach at least {powers_registered.minimum():.4f} power at "
                f"alpha_adj under the registered effect assumption at the achievable admissible-"
                f"day count by {cfg.projection_deadline}, at or above the "
                f"{cfg.power_go_floor:.2f} floor, and as-printed observability passed in full. "
                f"Collectors are armed."
            ),
            collectors_armed=True,
            verdict_scope=GO_SCOPE,
        )

    # --- DEGRADED, including the registered residual-band rule --------------
    if observability is Observability.PARTIAL:
        reason = (
            "as-printed observability passed partially, demoting the retro cohort to descriptive "
            "and leaving the forward cohort to carry the verdict alone"
        )
    elif powers_published.e1 >= cfg.power_go_floor:
        reason = (
            f"E1 reaches {powers_published.e1:.4f} power at the published-magnitude assumption, "
            f"at or above the {cfg.power_go_floor:.2f} floor, but only "
            f"{powers_registered.e1:.4f} at the registered assumption"
        )
    else:
        # The residual band, registered explicitly rather than left as a gap in
        # the map: E1 power at the published magnitude between the 0.50 BLOCKED
        # floor and the 0.80 GO floor. It is above the floor that stops
        # collection, so collection proceeds under the DEGRADED narrowing.
        reason = (
            f"E1 reaches {powers_published.e1:.4f} power at the published-magnitude assumption, "
            f"inside the residual band between the {cfg.power_blocked_floor:.2f} and "
            f"{cfg.power_go_floor:.2f} floors"
        )
    return Section0Gate(
        verdict=Section0Verdict.DEGRADED,
        rationale=(
            f"{reason}. Collection proceeds; recomputed power at the registered assumption is "
            f"E1 {powers_registered.e1:.4f} and E2 {powers_registered.e2:.4f}, stated beside the "
            f"registered {cfg.power_go_floor:.2f} target."
        ),
        collectors_armed=True,
        verdict_scope=DEGRADED_SCOPE,
    )
