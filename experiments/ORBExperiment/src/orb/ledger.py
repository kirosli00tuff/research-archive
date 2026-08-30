"""Guard 3 — append-only, fsynced ledgers. A truncated line is reported.

Every line is one JSON object plus a newline, written with ``O_APPEND`` and
followed by ``fsync``. Reading is strict: a line that does not parse is
surfaced as :class:`TruncatedLedgerLine` in the returned sequence and is
**never repaired, never skipped and never inferred**. A ledger that quietly
drops its own damaged lines cannot be used as evidence about anything.

The request ledger charges its per-vendor daily cap **before** the request is
sent, so an exhausted budget refuses rather than overspends.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, final

from orb.absence import AbsenceReason, Absent
from orb.redact import redact_row


class LedgerError(Exception):
    """Base class for ledger faults."""


class LedgerAppendError(LedgerError):
    """Raised when a line cannot be appended durably."""


class RequestCapExceededError(LedgerError):
    """Raised when a vendor's registered daily cap is already spent."""


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


def _utc_now_iso() -> str:
    return (
        datetime.now(tz=UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    )


@final
class AppendOnlyLedger:
    """An append-only JSONL ledger. Every append is fsynced before returning."""

    __slots__ = ("path",)

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, row: LedgerRow) -> None:
        """Append one row durably, redacted. The row is stamped if it is not already.

        Guard 8: a ledger row is a **recorded string**, so every credential
        value in it becomes a placeholder naming its variable before the line
        is serialised. Redaction is deterministic, so a ledger stays comparable
        line for line across runs.
        """
        payload: dict[str, Any] = dict(redact_row(row))
        payload.setdefault("recorded_at", _utc_now_iso())
        line = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
        flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
        try:
            fd = os.open(self.path, flags, 0o644)
        except OSError as exc:
            raise LedgerAppendError(f"cannot open {self.path}: {exc}") from exc
        try:
            written = os.write(fd, line.encode("utf-8"))
            if written != len(line.encode("utf-8")):
                raise LedgerAppendError(
                    f"short write to {self.path}: {written} of "
                    f"{len(line.encode('utf-8'))} bytes"
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
        # ``read_text`` rather than ``Path.open``: Guard 5 forbids the
        # attribute name ``open`` outside a sealed writer, and the guard is
        # right to. It caught this line on its first run against a real
        # module, which is the evidence that it binds on more than fixtures.
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

    def damaged_lines(self) -> list[TruncatedLedgerLine]:
        """Every line that did not parse. Reported, never repaired."""
        return [e for e in self.iter_rows() if isinstance(e, TruncatedLedgerLine)]


@final
class RequestLedger:
    """A per-vendor daily request cap that charges before the request is sent."""

    __slots__ = ("_caps", "_ledger")

    def __init__(self, path: Path, caps: Mapping[str, int]) -> None:
        self._ledger = AppendOnlyLedger(path)
        self._caps = dict(caps)

    def cap(self, vendor: str) -> int:
        if vendor not in self._caps:
            raise RequestCapExceededError(
                f"vendor {vendor!r} has no registered daily cap; an unmeasured "
                "endpoint is not a licence to send."
            )
        return self._caps[vendor]

    def spent_today(self, vendor: str, day: str) -> int:
        total = 0
        for entry in self._ledger.iter_rows():
            if isinstance(entry, TruncatedLedgerLine):
                raise LedgerError(
                    f"request ledger line {entry.line_number} did not parse; "
                    "the cap cannot be computed over a damaged ledger."
                )
            if entry.get("vendor") == vendor and entry.get("day") == day:
                total += 1
        return total

    def charge(self, vendor: str, day: str, endpoint: str) -> None:
        """Charge one request. Raises **before** the caller sends anything."""
        cap = self.cap(vendor)
        spent = self.spent_today(vendor, day)
        if spent >= cap:
            raise RequestCapExceededError(
                f"{vendor} daily cap {cap} already spent ({spent}) on {day}; "
                "refusing to send."
            )
        self._ledger.append(
            {"vendor": vendor, "day": day, "endpoint": endpoint, "kind": "charge"}
        )
