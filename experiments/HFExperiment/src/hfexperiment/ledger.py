"""Append-only on-disk ledger.

Every record is one JSON line, flushed and fsynced before append returns, so
the ledger survives a restart and a crash mid-session loses at most the
record being written. There is no update and no delete. A correction is a
new record that names the one it corrects.

Stage C.1 builds the priced-before-sending order gate on top of this
primitive. Nothing in stage A touches an order.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class Ledger:
    """One append-only JSONL file."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return self._path

    def append(self, record: dict[str, Any]) -> None:
        """Append one record durably."""
        line = json.dumps(record, sort_keys=True, separators=(",", ":"))
        if "\n" in line:
            raise ValueError("record serialised with a newline")
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())

    def read_all(self) -> list[dict[str, Any]]:
        """Every record in append order. Empty list when the file is absent."""
        if not self._path.exists():
            return []
        records: list[dict[str, Any]] = []
        with open(self._path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records
