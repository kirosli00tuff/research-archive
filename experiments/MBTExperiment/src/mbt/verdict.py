"""The stage verdict, computed from recorded artifacts rather than asserted.

REGISTRATION.md Section 0.1 registers **HARNESS-READY** as requiring four things
at once. This module reads each from the artifact that demonstrates it and
reports which held. A verdict written by hand can drift from the evidence under
it; one computed from the artifacts cannot, and it is re-runnable, so the
operator sees the verdict change the moment a condition is met.

**This stage can reach neither HARVESTABLE-CONFIRMED nor VENUE_BLOCKED**, and
those are not represented here. Both need the MARGIN gate, and the MARGIN gate
needs a U-prefixed session the paper-only clause forecloses.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum, unique
from pathlib import Path
from typing import final

from mbt.clock import iso_utc, utc_now
from mbt.registry import MIN_OBSERVATION_WINDOWS

REPO = Path(__file__).resolve().parents[2]
REPORTS = REPO / "reports"


@unique
class StageVerdict(StrEnum):
    """The two terminal states this stage can reach. There is no third."""

    HARNESS_READY = "HARNESS-READY"
    HARNESS_BLOCKED = "HARNESS-BLOCKED"


@final
@dataclass(frozen=True, slots=True)
class Condition:
    """One registered HARNESS-READY condition and the artifact that decides it."""

    name: str
    held: bool
    evidence: str
    detail: str

    def as_row(self) -> dict[str, object]:
        return {
            "condition": self.name,
            "held": self.held,
            "evidence": self.evidence,
            "detail": self.detail,
        }


def _load(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return loaded if isinstance(loaded, dict) else None


def condition_harness_builds() -> Condition:
    """The no-transmit scan is the build gate, so its artifact decides this."""
    scan = _load(REPORTS / "guards" / "no_transmit_scan.json")
    if scan is None:
        return Condition(
            "the harness builds",
            False,
            "reports/guards/no_transmit_scan.json",
            "the no-transmit scan artifact is absent, so the build is not demonstrated",
        )
    clean = scan.get("verdict") == "CLEAN"
    return Condition(
        "the harness builds",
        clean,
        "reports/guards/no_transmit_scan.json",
        f"no-transmit scan verdict {scan.get('verdict')!r} over "
        f"{scan.get('package_files_scanned')} package files, "
        f"{scan.get('finding_count')} findings",
    )


def condition_guards_fire_under_mutation() -> Condition:
    """Every registered mutation must be caught and every restore must go green."""
    mutations = _load(REPORTS / "mutations" / "mutations.json")
    if mutations is None:
        return Condition(
            "all five guards fire under mutation",
            False,
            "reports/mutations/mutations.json",
            "the mutation artifact is absent, so no guard has been shown to fail",
        )
    failures = mutations.get("failures")
    results = mutations.get("results")
    count = len(results) if isinstance(results, list) else 0
    return Condition(
        "all five guards fire under mutation",
        failures == 0 and count == 5,
        "reports/mutations/mutations.json",
        f"{count} mutations applied to real source, {failures} did not behave as registered",
    )


def condition_known_answer_reproduced() -> Condition:
    """The what-if reader must reproduce an independently checkable margin first."""
    check = _load(REPORTS / "task4" / "known_answer.json")
    if check is None:
        return Condition(
            "the known-answer test reproduces an independently checkable margin",
            False,
            "reports/task4/known_answer.json",
            "no known-answer artifact: the check did not run, so the code path has "
            "not been checked against a known answer and its MBT output is not trusted",
        )
    agrees = check.get("agrees") is True
    return Condition(
        "the known-answer test reproduces an independently checkable margin",
        agrees,
        "reports/task4/known_answer.json",
        str(check.get("detail", "")),
    )


def condition_census_armed() -> Condition:
    """Armed means the projection exists, not that windows have been collected."""
    projection = _load(REPORTS / "task5" / "projection_if_started_today.json")
    status = _load(REPORTS / "task5" / "census_status.json")
    if projection is None:
        return Condition(
            "the census is armed with its projected completion date",
            False,
            "reports/task5/projection_if_started_today.json",
            "no projection artifact, so the census carries no completion date",
        )
    accepted = 0
    if status is not None:
        census = status.get("census")
        if isinstance(census, dict):
            accepted = int(census.get("n_accepted", 0) or 0)
    return Condition(
        "the census is armed with its projected completion date",
        True,
        "reports/task5/projection_if_started_today.json",
        f"armed: {projection.get('collection_days_required')} collection days required, "
        f"{accepted} of {MIN_OBSERVATION_WINDOWS} windows collected. Armed is not "
        "collected, and this condition asks only that the projection exists.",
    )


@final
@dataclass(frozen=True, slots=True)
class VerdictResult:
    verdict: StageVerdict
    conditions: list[Condition]
    blocking: list[str]
    decided_at: str

    def as_row(self) -> dict[str, object]:
        return {
            "verdict": str(self.verdict),
            "decided_at": self.decided_at,
            "conditions": [c.as_row() for c in self.conditions],
            "conditions_held": sum(1 for c in self.conditions if c.held),
            "conditions_total": len(self.conditions),
            "blocking": self.blocking,
            "unreachable_here": [
                "HARVESTABLE-CONFIRMED",
                "VENUE_BLOCKED",
            ],
            "why_unreachable": (
                "Both need the MARGIN gate, which needs a U-prefixed session. The "
                "paper-only clause forecloses one, so neither is registered as "
                "available to this stage."
            ),
        }


def decide() -> VerdictResult:
    """Read every condition's artifact and return the registered verdict."""
    conditions = [
        condition_harness_builds(),
        condition_guards_fire_under_mutation(),
        condition_known_answer_reproduced(),
        condition_census_armed(),
    ]
    blocking = [c.name for c in conditions if not c.held]
    return VerdictResult(
        verdict=StageVerdict.HARNESS_READY if not blocking else StageVerdict.HARNESS_BLOCKED,
        conditions=conditions,
        blocking=blocking,
        decided_at=iso_utc(utc_now(), "verdict.decide"),
    )
