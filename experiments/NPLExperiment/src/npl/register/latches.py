"""Per-hypothesis read latches. One sealed read per surviving registration.

The H1 latch machinery is quarantined with the rest of the spent read
surface, so the register carries its own: one latch file per surviving
hypothesis, written exactly once (O_EXCL, fsynced) before that
hypothesis's registered Stage B read runs, so a crash after the latch
spends the read. Only survivors have latch paths — a BLOCKED hypothesis
has no Stage B to latch, and asking for its latch is a loud refusal.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from npl.clock import iso_z, now_utc
from npl.paths import STATE_DIR

# Survivors of the 2026-08-28 cull (registrations/H2 Amendment H2-1).
SURVIVOR_LATCHES: dict[str, Path] = {
    "H2": STATE_DIR / "h2_read_latch.json",
}


class NoLatchForHypothesis(ValueError):
    """A latch was asked for a hypothesis with no registered Stage B."""


class RegisterReadAlreadySpent(RuntimeError):
    """The latch exists: that hypothesis's single read is spent."""


def latch_path(hypothesis: str) -> Path:
    path = SURVIVOR_LATCHES.get(hypothesis)
    if path is None:
        raise NoLatchForHypothesis(
            f"{hypothesis!r} has no latch: only the cull's survivors "
            f"({sorted(SURVIVOR_LATCHES)}) have a registered Stage B."
        )
    return path


def require_unspent(hypothesis: str, path: Path | None = None) -> None:
    """Refuses loudly when the hypothesis's single read is already spent."""
    target = path if path is not None else latch_path(hypothesis)
    if target.exists():
        raise RegisterReadAlreadySpent(
            f"the latch {target} exists: {hypothesis}'s single registered read is "
            f"spent; recovery works from partial artifacts under an amendment, "
            f"never a silent re-run."
        )


def write_latch(hypothesis: str, module_hashes: dict[str, str], path: Path | None = None) -> Path:
    """Write-once, fsynced. Existence alone spends the read."""
    target = path if path is not None else latch_path(hypothesis)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "hypothesis": hypothesis,
        "read_at": iso_z(now_utc()),
        "module_hashes": module_hashes,
    }
    with target.open("x", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    return target
