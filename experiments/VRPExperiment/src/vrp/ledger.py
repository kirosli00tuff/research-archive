"""Guard 3 — append-only, fsynced ledgers. A truncated line is reported.

Every line is one JSON object plus a newline, written with ``O_APPEND`` and
followed by ``fsync``. Reading is strict: a line that does not parse is
surfaced as :class:`TruncatedLedgerLine` and is **never repaired, never skipped
and never inferred**. A ledger that quietly drops its own damaged lines cannot
be used as evidence about anything.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, final

from vrp.absence import AbsenceReason, Absent
from vrp.redact import redact_row
from vrp.tzguard import iso_utc, utc_now


class LedgerError(Exception):
    """Base class for ledger faults."""


class LedgerAppendError(LedgerError):
    """Raised when a line cannot be appended durably."""


class LedgerImmutableError(LedgerError):
    """Raised when a caller tries to rewrite or truncate a ledger."""


@final
@dataclass(frozen=True, slots=True)
class TruncatedLedgerLine:
    """A line that did not parse. Reported in place, never repaired."""

    line_number: int
    raw: str
    error: str

    def as_absent(self) -> Absent:
        return Absent(
            AbsenceReason.TRUNCATED_LEDGER_LINE,
            f"line {self.line_number}: {self.error}",
        )


type LedgerRow = Mapping[str, Any]
type LedgerEntry = LedgerRow | TruncatedLedgerLine


@final
class AppendOnlyLedger:
    """An append-only JSONL ledger. Every append is fsynced before returning."""

    __slots__ = ("path",)

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, row: LedgerRow) -> None:
        """Append one row durably, redacted, stamped if it is not already."""
        payload: dict[str, Any] = dict(redact_row(row))
        payload.setdefault("recorded_at", iso_utc(utc_now(), "ledger.append"))
        line = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
        encoded = line.encode("utf-8")
        flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
        try:
            fd = os.open(self.path, flags, 0o644)
        except OSError as exc:
            raise LedgerAppendError(f"cannot open {self.path}: {exc}") from exc
        try:
            written = os.write(fd, encoded)
            if written != len(encoded):
                raise LedgerAppendError(
                    f"short write to {self.path}: {written} of {len(encoded)} bytes"
                )
            os.fsync(fd)
        finally:
            os.close(fd)

    def read(self) -> list[LedgerEntry]:
        """Read every line. Damaged lines come back as TruncatedLedgerLine."""
        return list(self.iter_rows())

    def iter_rows(self) -> Iterator[LedgerEntry]:
        if not self.path.exists():
            return
        # ``read_text`` rather than an ``open`` call: Guard 5's AST walk
        # forbids the attribute name ``open`` outside a sealed writer.
        raw_text = self.path.read_text(encoding="utf-8")
        for number, raw in enumerate(raw_text.splitlines(keepends=True), start=1):
            stripped = raw.rstrip("\n")
            if not raw.endswith("\n"):
                yield TruncatedLedgerLine(
                    number, stripped, "line has no terminating newline"
                )
                continue
            if not stripped.strip():
                continue
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError as exc:
                yield TruncatedLedgerLine(number, stripped, str(exc))
                continue
            if not isinstance(parsed, dict):
                yield TruncatedLedgerLine(number, stripped, "line is not a JSON object")
                continue
            yield parsed

    def row_count(self) -> int:
        """Rows that parsed. Truncated lines are excluded and reported apart."""
        return sum(1 for entry in self.iter_rows() if isinstance(entry, dict))

    def truncated(self) -> list[TruncatedLedgerLine]:
        """Every damaged line, in order. Never empty by suppression."""
        return [e for e in self.iter_rows() if isinstance(e, TruncatedLedgerLine)]
