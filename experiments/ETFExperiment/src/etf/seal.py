"""The sealed writers. They write raw response bytes and parse nothing.

A sealed store holds the outcome substrate: Hyperliquid BTC perp hourly candles
and hourly funding covering each admissible day's anchor and hold window. The
writer here never decodes a field. Coverage is accounted from the blind readers
in `etf.blindness`, which see timestamps and row counts only.

The solattn ADR-019 shape governs the manifest: the daily pass seals the day
that closed, never the open day, and a reader refuses an unattested closed day.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SealedWrite:
    path: Path
    sha256: str
    byte_count: int


def seal_bytes(path: Path, payload: bytes) -> SealedWrite:
    """Write raw bytes and fsync. Nothing here parses the payload."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    digest = hashlib.sha256(payload).hexdigest()
    return SealedWrite(path=path, sha256=digest, byte_count=len(payload))


def digest_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest(path: Path, rows: list[dict[str, object]]) -> SealedWrite:
    """Write a manifest of sealed writes. Counts, paths and hashes only."""
    payload = json.dumps(rows, sort_keys=True, indent=2).encode("utf-8")
    return seal_bytes(path, payload)
