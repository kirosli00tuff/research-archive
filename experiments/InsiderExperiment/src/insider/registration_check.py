"""The operator prior gate.

NPDExperiment's prior was adopted rather than formed. A calibration ledger
needs an independently formed number to be worth anything, so the slot is
reserved and empty and it blocks Stage B while empty. The assistant's own prior
sits beside it and never substitutes for it.
"""

from __future__ import annotations

import re
from pathlib import Path

from insider.config import CONFIG, Config
from insider.paths import REGISTRATION

EMPTY_MARKER = "[ EMPTY."
_PRIOR_RE = re.compile(
    r"^>\s*Operator prior[^\n]*?:\s*([01](?:\.\d+)?)\s*$", re.IGNORECASE | re.MULTILINE
)
_SECTION_RE = re.compile(r"^##\s*Section 12\..*?$(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)


class OperatorPriorMissing(RuntimeError):
    """Stage B asked to run while the operator prior slot is empty."""


def _section_text(registration: Path | None = None) -> str:
    path = registration or REGISTRATION
    if not path.exists():
        raise FileNotFoundError(f"registration missing: {path}")
    match = _SECTION_RE.search(path.read_text(encoding="utf-8"))
    return match.group(1) if match else ""


def operator_prior(registration: Path | None = None) -> float | None:
    """The recorded operator prior, or None when the slot is empty.

    Absence of the empty marker is not presence of a prior. A number must be
    present and parseable or this returns None.
    """
    text = _section_text(registration)
    if EMPTY_MARKER in text:
        return None
    match = _PRIOR_RE.search(text)
    if match is None:
        return None
    value = float(match.group(1))
    return value if 0.0 <= value <= 1.0 else None


def operator_prior_filled(registration: Path | None = None) -> bool:
    return operator_prior(registration) is not None


def require_operator_prior(registration: Path | None = None) -> float:
    """Refuse, rather than warn, when the slot is empty."""
    value = operator_prior(registration)
    if value is None:
        raise OperatorPriorMissing(
            "the operator prior slot in REGISTRATION.md Section 12 is empty. "
            "Stage B stays blocked until the operator writes a number there himself."
        )
    return value


def assistant_prior(cfg: Config = CONFIG) -> float:
    """The assistant's prior. Recorded beside the empty slot, never inside it."""
    return cfg.assistant_prior
