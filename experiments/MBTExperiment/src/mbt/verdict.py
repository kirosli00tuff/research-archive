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


def _duration_days(projection: dict[str, object]) -> object:
    """The registered collection-day count, or absent. Never a default number."""
    block = projection.get("duration_once_it_can_begin")
    return block.get("collection_days_required") if isinstance(block, dict) else "an absent"


def condition_census_armed() -> Condition:
    """The census must carry a projected completion date, not merely a duration.

    **The projection runs from the first window ACTUALLY collected**, not from a
    hypothetical start. Stage B could only compute a hypothetical one, because no
    session existed and no window could be attempted, and it recorded the
    condition as held on that basis. A session now exists and windows have been
    attempted, so the hypothetical projection is superseded by a real one, and a
    real one requires a real first window.

    **Reading the superseded artifact would be the drift a computed verdict
    exists to prevent**: the stale file would keep reporting a completion date
    for a census that cannot begin. See ADR-011.
    """
    projection = _load(REPORTS / "task5" / "projection_from_first_window.json")
    status = _load(REPORTS / "task5" / "census_status.json")
    accepted = 0
    if status is not None:
        census = status.get("census")
        if isinstance(census, dict):
            accepted = int(census.get("n_accepted", 0) or 0)
    if projection is None:
        return Condition(
            "the census is armed with its projected completion date",
            False,
            "reports/task5/projection_from_first_window.json",
            "no projection artifact, so the census carries no completion date",
        )
    projected = projection.get("projected_completion_utc")
    has_date = isinstance(projected, str) and projected.strip() != ""
    return Condition(
        "the census is armed with its projected completion date",
        has_date,
        "reports/task5/projection_from_first_window.json",
        (
            f"projected completion {projected}, from the first window actually "
            f"collected, with {accepted} of {MIN_OBSERVATION_WINDOWS} windows accepted"
        )
        if has_date
        else (
            f"the projected completion date is ABSENT: {accepted} of "
            f"{MIN_OBSERVATION_WINDOWS} windows are accepted and "
            f"{projection.get('windows_refused')} were refused, so there is no first "
            f"window to project from. The registered duration of "
            f"{_duration_days(projection)} collection days is a property of the rule "
            "and is not a completion date, because there is no start to add it to."
        ),
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
