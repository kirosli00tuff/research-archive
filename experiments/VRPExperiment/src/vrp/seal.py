"""Guard 5, part two — the seal. Sealed writers store bytes and parse nothing.

A sealed writer takes raw response bytes, hashes them, writes them, and records
the hash in the append-only ledger. **It never parses a field.** No caller ever
receives an implied volatility, a realized volatility, an option price or a
premium from anything in this module.

The one code path that reads a blind field outside a sealed module does not
exist. ``tests/test_guards.py`` walks the parse tree of every module under
``src/vrp`` and fails if one appears.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import final

from vrp.fields import BLIND_FIELDS, READABLE_FIELDS, SEALED_MODULES
from vrp.ledger import AppendOnlyLedger
from vrp.redact import redact_data
from vrp.tzguard import iso_utc, utc_now


class SealViolationError(PermissionError):
    """Raised when a caller asks a sealed writer for a blind value."""


__all__ = [
    "BLIND_FIELDS",
    "READABLE_FIELDS",
    "SEALED_MODULES",
    "SealRecord",
    "SealViolationError",
    "SealedWriter",
]


@final
@dataclass(frozen=True, slots=True)
class SealRecord:
    """What a sealed write returns. Counts and hashes only, never a value."""

    path: Path
    sha256: str
    byte_count: int
    line_count: int
    retrieved_at: str

    def as_row(self) -> dict[str, object]:
        return {
            "kind": "seal",
            "path": str(self.path),
            "sha256": self.sha256,
            "byte_count": self.byte_count,
            "line_count": self.line_count,
            "retrieved_at": self.retrieved_at,
        }


@final
class SealedWriter:
    """Writes raw bytes. Parses nothing. Returns no blind value, ever."""

    __slots__ = ("_ledger", "_root")

    def __init__(self, root: Path, ledger: AppendOnlyLedger) -> None:
        self._root = root
        self._ledger = ledger
        self._root.mkdir(parents=True, exist_ok=True)

    def write(self, relative: str, payload: bytes) -> SealRecord:
        """Store ``payload`` verbatim under ``relative`` and seal it."""
        if not isinstance(payload, bytes):
            raise SealViolationError(
                "a sealed writer stores bytes: it refuses a parsed object, "
                "because parsing is exactly what it exists not to do."
            )
        target = self._root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        record = SealRecord(
            path=target,
            sha256=hashlib.sha256(payload).hexdigest(),
            byte_count=len(payload),
            line_count=payload.count(b"\n"),
            retrieved_at=iso_utc(utc_now(), "SealedWriter.write"),
        )
        self._ledger.append(record.as_row())
        return record

    def describe(self, relative: str) -> dict[str, object]:
        """Metadata about a sealed file. Never its content."""
        target = self._root / relative
        if not target.exists():
            return {"kind": "seal_missing", "path": str(target)}
        raw = target.read_bytes()
        described = redact_data(
            {
                "kind": "seal_describe",
                "path": str(target),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "byte_count": len(raw),
                "line_count": raw.count(b"\n"),
            }
        )
        if not isinstance(described, dict):  # pragma: no cover
            raise SealViolationError("describe must return a mapping")
        return described

    def refuse_value(self, field: str) -> None:
        """Explicitly refuse a caller asking for a blind field by name."""
        if field in BLIND_FIELDS:
            raise SealViolationError(
                f"a sealed writer never serves {field!r}: it is a blind field. "
                "Open the TASK 6 latch and use the sealed reader, once."
            )
        raise SealViolationError(
            f"a sealed writer serves no field values at all, {field!r} included."
        )
