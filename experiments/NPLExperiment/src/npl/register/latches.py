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

# Amendment H2-3 Change 3: H2's sealed outcomes open exactly twice, once per
# registered look, each behind its own write-once latch. Look 2 cannot run
# before look 1's latch exists — the order is pinned, not assumed.
REGISTERED_LOOKS: tuple[int, ...] = (1, 2)
LOOK_LATCHES: dict[tuple[str, int], Path] = {
    ("H2", 1): STATE_DIR / "h2_look1_latch.json",
    ("H2", 2): STATE_DIR / "h2_look2_latch.json",
}


class NoLatchForHypothesis(ValueError):
    """A latch was asked for a hypothesis with no registered Stage B."""


class LookOutOfOrder(RuntimeError):
    """Look 2 was asked for before look 1 was spent."""


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
    return _write(target, {"hypothesis": hypothesis, "module_hashes": module_hashes})


def _write(target: Path, payload: dict[str, object]) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    body = dict(payload)
    body["read_at"] = iso_z(now_utc())
    with target.open("x", encoding="utf-8") as fh:
        json.dump(body, fh, indent=2, sort_keys=True)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    return target


def look_latch_path(hypothesis: str, look: int) -> Path:
    """The per-look latch path, or a loud refusal for an unregistered look."""
    path = LOOK_LATCHES.get((hypothesis, look))
    if path is None:
        raise NoLatchForHypothesis(
            f"{hypothesis!r} look {look!r} has no registered latch: the registered looks are "
            f"{sorted(look for h, look in LOOK_LATCHES if h == hypothesis)}"
        )
    return path


def require_look_unspent(
    hypothesis: str,
    look: int,
    path: Path | None = None,
    previous_path: Path | None = None,
) -> None:
    """Refuses when this look is spent, or when look 2 precedes look 1.

    The ordering pin is structural: look 2's read cannot run until look 1's
    latch exists on disk, so a look-2 boundary can never be computed without
    the look-1 counts it needs.
    """
    target = path if path is not None else look_latch_path(hypothesis, look)
    if target.exists():
        raise RegisterReadAlreadySpent(
            f"the latch {target} exists: {hypothesis} look {look} is spent; recovery works "
            f"from partial artifacts under an amendment, never a silent re-run."
        )
    if look == 1:
        return
    previous = previous_path if previous_path is not None else look_latch_path(hypothesis, look - 1)
    if not previous.exists():
        raise LookOutOfOrder(
            f"{hypothesis} look {look} was asked for before look {look - 1} was spent "
            f"({previous} is absent). The registered looks run in order."
        )


def write_look_latch(
    hypothesis: str, look: int, module_hashes: dict[str, str], path: Path | None = None
) -> Path:
    """Write-once, fsynced. Existence alone spends that look."""
    target = path if path is not None else look_latch_path(hypothesis, look)
    return _write(target, {"hypothesis": hypothesis, "look": look, "module_hashes": module_hashes})
