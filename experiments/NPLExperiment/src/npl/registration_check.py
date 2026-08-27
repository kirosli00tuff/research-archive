"""The operator prior gate. The empty slot blocks Stage B structurally.

Section 13 of REGISTRATION.md reserves a slot for the operator's own prior,
labelled independent or adopted. The assistant priors recorded there are not
the operator's number. Stage B requires the slot filled; this module is the
enforcement site, and the refusal is produced, never asserted.
"""

from __future__ import annotations

import re
from pathlib import Path

from npl.config import CONFIG, Config
from npl.paths import REGISTRATION_MD


class OperatorPriorMissing(RuntimeError):
    """Stage B was asked for while the operator prior slot is empty."""


_PRIOR_RE = re.compile(
    r"Operator prior[^:\n]*:\s*(0(?:\.\d+)?|1(?:\.0+)?)\s*\((independent|adopted)\)"
)


def operator_prior(path: Path = REGISTRATION_MD) -> tuple[float, str] | None:
    """The operator's recorded prior and its label, or None while the slot is empty."""
    if not path.exists():
        return None
    match = _PRIOR_RE.search(path.read_text(encoding="utf-8"))
    if match is None:
        return None
    return float(match.group(1)), match.group(2)


def operator_prior_filled(path: Path = REGISTRATION_MD) -> bool:
    return operator_prior(path) is not None


def require_operator_prior(path: Path = REGISTRATION_MD) -> tuple[float, str]:
    found = operator_prior(path)
    if found is None:
        raise OperatorPriorMissing(
            "the operator prior slot in REGISTRATION.md Section 13 is empty. Stage B is "
            "structurally blocked until the operator records a prior labelled independent "
            "or adopted. The assistant priors are not the operator's number."
        )
    return found


def assistant_priors(cfg: Config = CONFIG) -> tuple[float, float]:
    """The assistant priors recorded 2026-08-26: (edge overall, Stage B bars clearing)."""
    return cfg.assistant_prior_edge, cfg.assistant_prior_stage_b
