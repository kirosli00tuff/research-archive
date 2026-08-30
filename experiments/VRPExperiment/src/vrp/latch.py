"""The TASK 6 latch — the real-data read happens exactly once.

Outcome blindness applies to the premium. The extraction and estimation
machinery is built and verified against synthetic fixtures with known answers,
and pointed at real public data **exactly once**, behind this latch.

A latch is written **before** the read and records the SHA-256 of every module
that participates. If the modules change after a read, the recorded hashes no
longer match and the discrepancy is visible rather than silent. A second read
of the same window voids the hypothesis and raises
:class:`LatchAlreadySpentError`.

The fixture latch is a separate, freely re-openable object: fixtures may be run
any number of times, which is the point of having them.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum, unique
from pathlib import Path
from typing import final

from vrp.tzguard import iso_utc, utc_now


@unique
class ReadKind(StrEnum):
    """What is being read. Fixtures are unlatched; real data is latched once."""

    FIXTURE = "fixture"
    """Synthetic data with a known answer. Re-openable without limit."""

    REAL = "real"
    """Public real data. **One read. Ever.**"""


class LatchError(PermissionError):
    """Base class for every refusal the latch machinery can raise."""


class LatchAlreadySpentError(LatchError):
    """A second read of the real window. **This voids the hypothesis.**"""


class LatchNotWrittenError(LatchError):
    """A real read was attempted with no latch record on disk."""


class LatchModuleDriftError(LatchError):
    """A participating module changed between latch write and read."""


class BlindnessViolationError(LatchError):
    """A blind value was requested while the real latch was unspent."""


@final
@dataclass(frozen=True, slots=True)
class LatchRecord:
    """One latch. Records what was about to be read, and by which code."""

    kind: ReadKind
    written_at: str
    module_hashes: dict[str, str]
    note: str

    def as_row(self) -> dict[str, object]:
        return {
            "kind": f"latch:{self.kind.value}",
            "written_at": self.written_at,
            "module_hashes": dict(self.module_hashes),
            "note": self.note,
        }


def hash_modules(paths: list[Path]) -> dict[str, str]:
    """SHA-256 of each participating module, keyed by path, sorted."""
    hashes: dict[str, str] = {}
    for path in sorted(paths):
        hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


@final
class Latch:
    """The real-data latch. Written once, spent once, never rewritten."""

    __slots__ = ("_path",)

    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return self._path

    def is_spent(self) -> bool:
        return self._path.exists()

    def write(self, modules: list[Path], note: str) -> LatchRecord:
        """Write the latch. Refuses if one already exists."""
        if self._path.exists():
            raise LatchAlreadySpentError(
                f"the real-data latch at {self._path} is already spent. "
                "A second read of the real window voids the hypothesis. "
                "The recorded result stands; it is not re-run."
            )
        record = LatchRecord(
            kind=ReadKind.REAL,
            written_at=iso_utc(utc_now(), "Latch.write"),
            module_hashes=hash_modules(modules),
            note=note,
        )
        self._path.write_text(
            json.dumps(record.as_row(), sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        return record

    def read_record(self) -> LatchRecord:
        if not self._path.exists():
            raise LatchNotWrittenError(
                f"no latch at {self._path}: a real read requires a latch "
                "written before it, not after."
            )
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        return LatchRecord(
            kind=ReadKind.REAL,
            written_at=str(raw["written_at"]),
            module_hashes={str(k): str(v) for k, v in raw["module_hashes"].items()},
            note=str(raw["note"]),
        )

    def verify_modules(self, modules: list[Path]) -> dict[str, tuple[str, str]]:
        """Return every module whose hash drifted since the latch was written."""
        recorded = self.read_record().module_hashes
        current = hash_modules(modules)
        drift: dict[str, tuple[str, str]] = {}
        for name, digest in recorded.items():
            now = current.get(name, "<absent>")
            if now != digest:
                drift[name] = (digest, now)
        return drift

    def require_unspent(self) -> None:
        """Guard for callers that must not run after the latch is spent."""
        if self.is_spent():
            raise LatchAlreadySpentError(
                f"the real-data latch at {self._path} is spent: this code path "
                "may not run a second time."
            )


def require_blindness(latch: Latch, context: str) -> None:
    """Refuse a blind read while the real latch is unspent."""
    if not latch.is_spent():
        raise BlindnessViolationError(
            f"{context}: blindness holds. The real-data latch at {latch.path} "
            "has not been written, so no premium value may be read. Build "
            "against fixtures."
        )
