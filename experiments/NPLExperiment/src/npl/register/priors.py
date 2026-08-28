"""Per-hypothesis operator prior slots. Each empty slot blocks its own Stage B.

Every successor registration carries a Section 13 analog: the assistant
priors recorded 2026-08-28 (context, never the operator's number — the NPD
Amendment 0 adoption warning carries over verbatim), and one reserved empty
operator slot. The slot parses only as a probability in [0, 1] followed by
`(independent)` or `(adopted)`; anything else is empty. An empty slot blocks
that hypothesis's Stage B structurally, and the refusal is produced by test,
never asserted. The assistant never fills any slot.
"""

from __future__ import annotations

import re
from pathlib import Path

from npl.config import CONFIG, Config
from npl.paths import H2_REGISTRATION_MD, H3_REGISTRATION_MD, H4_REGISTRATION_MD

_REGISTRATION_PATHS: dict[str, Path] = {
    "H2": H2_REGISTRATION_MD,
    "H3": H3_REGISTRATION_MD,
    "H4": H4_REGISTRATION_MD,
}

_PRIOR_RE = re.compile(
    r"Operator prior[^:\n]*:\s*(0(?:\.\d+)?|1(?:\.0+)?)\s*\((independent|adopted)\)"
)

_SLOT_MARKER = "Operator prior"


class RegisterOperatorPriorMissing(RuntimeError):
    """A successor Stage B was asked for while its operator slot is empty."""


class UnknownHypothesis(ValueError):
    """A hypothesis name outside the register was asked for. Refused."""


def registration_path(hypothesis: str) -> Path:
    path = _REGISTRATION_PATHS.get(hypothesis)
    if path is None:
        raise UnknownHypothesis(
            f"{hypothesis!r} is not a register entry; the register holds "
            f"{sorted(_REGISTRATION_PATHS)}"
        )
    return path


def slot_reserved(hypothesis: str, path: Path | None = None) -> bool:
    """The registration carries the reserved slot marker at all."""
    target = path if path is not None else registration_path(hypothesis)
    if not target.exists():
        return False
    return _SLOT_MARKER in target.read_text(encoding="utf-8")


def operator_prior(hypothesis: str, path: Path | None = None) -> tuple[float, str] | None:
    """The operator's recorded prior and label, or None while the slot is empty."""
    target = path if path is not None else registration_path(hypothesis)
    if not target.exists():
        return None
    match = _PRIOR_RE.search(target.read_text(encoding="utf-8"))
    if match is None:
        return None
    return float(match.group(1)), match.group(2)


def require_operator_prior(hypothesis: str, path: Path | None = None) -> tuple[float, str]:
    """The structural block: an empty slot refuses that hypothesis's Stage B."""
    found = operator_prior(hypothesis, path)
    if found is None:
        raise RegisterOperatorPriorMissing(
            f"the operator prior slot in {registration_path(hypothesis)} is empty. "
            f"{hypothesis}'s Stage B is structurally blocked until the operator records "
            f"a prior labelled independent or adopted. The assistant priors are not the "
            f"operator's number."
        )
    return found


def assistant_priors(hypothesis: str, cfg: Config = CONFIG) -> dict[str, float]:
    """The assistant priors recorded 2026-08-28 in chat, per register entry."""
    by_hypothesis: dict[str, dict[str, float]] = {
        "H2": {
            "edge_overall": cfg.h2_assistant_prior_edge,
            "bars_clearing": cfg.h2_assistant_prior_bars,
        },
        "H3": {"bars_clearing": cfg.h3_assistant_prior_bars},
        "H4": {"bars_clearing": cfg.h4_assistant_prior_bars},
    }
    priors = by_hypothesis.get(hypothesis)
    if priors is None:
        raise UnknownHypothesis(
            f"{hypothesis!r} is not a register entry; the register holds {sorted(by_hypothesis)}"
        )
    return priors
