"""A.3 TASK 4 — the Stage C and Stage D latches, and the quarantine.

**Stage C opens the sealed in-sample read exactly once. Stage D opens the
holdout exactly once, behind its own latch, and cannot run before Stage C's
latch exists. A second read of either window voids the hypothesis.**

A latch is written **first**, before the read, and records the SHA-256 of every
module that participates. If the modules change after a read, the recorded
hashes no longer match and the discrepancy is visible rather than silent.

The **quarantine** is the other half: every value inside a spent read is
unreachable from any successor code path, pinned by AST walk and by test. A
successor hypothesis runs on fresh data or it does not run.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum, unique
from pathlib import Path
from typing import final


@unique
class Stage(StrEnum):
    C = "stage_c"
    """The in-sample read, 2016-01-04 to 2022-12-30."""

    D = "stage_d"
    """The holdout read, 2023-01-03 to 2026-06-30."""


class LatchError(PermissionError):
    """Base class for every refusal the latch machinery can raise."""


class LatchAlreadySpentError(LatchError):
    """A second read of a window. **This voids the hypothesis.**"""


class LatchPrerequisiteError(LatchError):
    """Stage D was attempted before Stage C's latch existed."""


class OperatorGateError(LatchError):
    """The operator prior slot is empty, or no operator instruction was given."""


@final
@dataclass(frozen=True, slots=True)
class LatchRecord:
    stage: Stage
    written_at: str
    module_hashes: dict[str, str]
    operator_prior_label: str

    def as_json(self) -> str:
        return json.dumps(
            {
                "stage": self.stage.value,
                "written_at": self.written_at,
                "module_hashes": self.module_hashes,
                "operator_prior_label": self.operator_prior_label,
            },
            indent=2,
            sort_keys=True,
        )


def module_hashes(source_root: Path) -> dict[str, str]:
    """SHA-256 of every module in the package, at the moment of the read."""
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(source_root.rglob("*.py"))
    }


def latch_path(state_root: Path, stage: Stage) -> Path:
    return state_root / f"{stage.value}_read.json"


def write_latch(
    state_root: Path,
    source_root: Path,
    stage: Stage,
    *,
    operator_prior_label: str,
    operator_instruction: bool,
) -> LatchRecord:
    """Write the latch **before** the read. Refuses every registered way.

    Section 10's three conditions are enforced here, not documented here: the
    operator prior slot must be filled and labelled, an explicit operator
    instruction must be present, and the window must be unspent.
    """
    if not operator_instruction:
        raise OperatorGateError(
            f"{stage.value}: refusing without an explicit operator instruction."
        )
    if operator_prior_label not in {"independent", "adopted"}:
        raise OperatorGateError(
            f"{stage.value}: the operator prior slot is empty or unlabelled "
            f"(got {operator_prior_label!r}). Section 13 reserves it for the "
            "operator, and the empty slot blocks this latch structurally."
        )

    target = latch_path(state_root, stage)
    if target.exists():
        raise LatchAlreadySpentError(
            f"{stage.value} has already been read, at "
            f"{json.loads(target.read_text())['written_at']}. **A second read "
            "of this window voids the hypothesis.** The latch is not removable "
            "by this code path."
        )
    if stage is Stage.D and not latch_path(state_root, Stage.C).exists():
        raise LatchPrerequisiteError(
            "stage_d cannot run before stage_c's latch exists."
        )

    record = LatchRecord(
        stage=stage,
        written_at=datetime.now(tz=UTC).isoformat(timespec="seconds"),
        module_hashes=module_hashes(source_root),
        operator_prior_label=operator_prior_label,
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(record.as_json(), encoding="utf-8")
    return record


def is_spent(state_root: Path, stage: Stage) -> bool:
    return latch_path(state_root, stage).exists()


def require_unspent(state_root: Path, stage: Stage) -> None:
    """Refuse loudly at the top of any read path."""
    if is_spent(state_root, stage):
        raise LatchAlreadySpentError(
            f"{stage.value} is spent. A second read voids the hypothesis."
        )
