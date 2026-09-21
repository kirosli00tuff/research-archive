"""H5's Section 9 prior slot. The empty slot blocks the successor draft.

H5 has no Stage B and no capital, so an empty operator slot cannot block a
read. What it blocks is the *consequence* of a VIABLE row: drafting the
successor hypothesis for a fresh repo. The slot parses only as a probability
in [0, 1] followed by `(independent)` or `(adopted)`; the assistant never
fills it. The shared parser in `npl.register.priors` is reused with an
explicit path, so nothing in the H2/H3/H4 prior machinery changes.
"""

from __future__ import annotations

from pathlib import Path

from npl.config import CONFIG, Config
from npl.paths import H5_REGISTRATION_MD
from npl.register.priors import operator_prior as _shared_operator_prior

HYPOTHESIS = "H5"


class H5OperatorPriorMissing(RuntimeError):
    """A successor draft was asked for while H5's operator slot is empty."""


def operator_prior(path: Path = H5_REGISTRATION_MD) -> tuple[float, str] | None:
    """H5's recorded operator prior and label, or None while the slot is empty."""
    return _shared_operator_prior(HYPOTHESIS, path=path)


def require_operator_prior_for_successor(path: Path = H5_REGISTRATION_MD) -> tuple[float, str]:
    """The structural block on the VIABLE consequence, not on any read."""
    found = operator_prior(path)
    if found is None:
        raise H5OperatorPriorMissing(
            "the operator prior slot in registrations/H5/REGISTRATION.md Section 9 is "
            "empty. A VIABLE row may be recorded, but drafting the successor hypothesis "
            "is structurally blocked until the operator records a prior labelled "
            "independent or adopted. The assistant prior is not the operator's number."
        )
    return found


def assistant_prior(cfg: Config = CONFIG) -> float:
    """0.05, recorded 2026-08-28 in chat, that a real capturable edge exists here."""
    return cfg.h5_assistant_prior_edge
