"""The append-only primitive both ledgers share.

Rows land as one JSON object per line, opened in append mode, flushed and
fsynced before the call returns. A process killed after the write keeps the
row. A process killed during the write leaves a partial final line, which
`read_rows` reports rather than repairs, because a truncated record is an
absence and absence is never synthesized.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator


class LedgerCorruption(RuntimeError):
    """A ledger line did not parse. Reported, never silently dropped."""


@dataclass(frozen=True, slots=True)
class ReadResult:
    rows: list[dict[str, Any]]
    trailing_partial_line: str | None


class AppendOnlyLedger:
    """A JSON-lines file that only ever grows."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, row: dict[str, Any]) -> None:
        line = json.dumps(row, sort_keys=True, separators=(",", ":"), default=str)
        if "\n" in line:
            raise ValueError("ledger row must serialize to one line")
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()
            os.fsync(fh.fileno())

    def read(self) -> ReadResult:
        if not self.path.exists():
            return ReadResult(rows=[], trailing_partial_line=None)
        raw = self.path.read_text(encoding="utf-8")
        lines = raw.split("\n")
        trailing = None
        if lines and lines[-1] != "":
            trailing = lines[-1]
        complete = lines[:-1] if lines else []
        rows: list[dict[str, Any]] = []
        for i, line in enumerate(complete, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise LedgerCorruption(f"{self.path}:{i} did not parse: {exc}") from exc
        return ReadResult(rows=rows, trailing_partial_line=trailing)

    def iter_rows(self) -> Iterator[dict[str, Any]]:
        yield from self.read().rows
