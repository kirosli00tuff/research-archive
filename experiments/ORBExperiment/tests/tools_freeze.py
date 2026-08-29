"""Test helper: recompute the frozen cost-model hash the same way the tool does."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from freeze_costs import canonical  # type: ignore[import-not-found]

from orb.costs_registered import REGISTERED_COST_MODEL


def canonical_for_test() -> str:
    payload: str = canonical(REGISTERED_COST_MODEL)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
