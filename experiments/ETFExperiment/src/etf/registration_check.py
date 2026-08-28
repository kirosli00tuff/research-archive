"""The registration's structural preconditions. The empty prior slot blocks Stage B.

Section 13 reserves an operator prior slot and leaves it empty. This module is
the enforcement site: it parses the registration text, and until the slot holds
a probability in [0, 1] followed by `(independent)` or `(adopted)`, Stage B
cannot open.

The assistant prior is recorded beside it and is deliberately NOT accepted as a
fill. The NPDExperiment Amendment 0 lesson: an adopted prior corrupts the
calibration ledger, because a number copied from the assistant measures the
assistant twice and the operator not at all.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from etf.config import CONFIG
from etf.paths import REGISTRATION_MD

SLOT_LABEL = "Operator prior on the Stage B bars clearing:"
_FILL = re.compile(
    rf"{re.escape(SLOT_LABEL)}\s*\**\s*(?P<value>0?\.\d+|0|1|1\.0+)\s*\((?P<label>independent|adopted)\)"
)


class OperatorPriorMissing(RuntimeError):
    """Section 13's slot is empty. Stage B is blocked structurally."""


class OperatorPriorMalformed(RuntimeError):
    """Something stands in the slot that the registered format does not accept."""


@dataclass(frozen=True, slots=True)
class OperatorPrior:
    value: float
    label: str


def assistant_prior() -> float:
    """The assistant's recorded prior. Context, never the operator's number."""
    return CONFIG.assistant_prior_edge


def read_operator_prior(path: Path = REGISTRATION_MD) -> OperatorPrior:
    """Parse the Section 13 slot, or raise. Nothing here fills it."""
    text = path.read_text(encoding="utf-8")
    if SLOT_LABEL not in text:
        raise OperatorPriorMalformed(
            f"{path}: the Section 13 slot label is absent. The registration is append-only; "
            f"the slot is not removable."
        )
    match = _FILL.search(text)
    if match is None:
        raise OperatorPriorMissing(
            f"{path}: the Section 13 operator prior slot is empty. The accepted format is a "
            f"probability in [0, 1] followed by (independent) or (adopted). Stage B is blocked "
            f"structurally until the operator fills it; the assistant prior of "
            f"{assistant_prior()} is not that number and may not be copied into the slot."
        )
    value = float(match.group("value"))
    if not 0.0 <= value <= 1.0:
        raise OperatorPriorMalformed(f"{path}: operator prior {value} is outside [0, 1]")
    return OperatorPrior(value=value, label=match.group("label"))


def require_operator_prior(path: Path = REGISTRATION_MD) -> OperatorPrior:
    """Stage B's structural precondition. Raises unless the slot is filled and labelled."""
    return read_operator_prior(path)


def operator_prior_is_filled(path: Path = REGISTRATION_MD) -> bool:
    """True only when the slot parses. Used to report the open operator item."""
    try:
        read_operator_prior(path)
    except (OperatorPriorMissing, OperatorPriorMalformed):
        return False
    return True
