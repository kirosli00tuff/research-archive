"""Guard 5 — the seal. Sealed writers store bytes and parse nothing.

A sealed writer takes raw response bytes, hashes them, writes them, and records
the hash in the append-only ledger. **It never parses a field.** No caller ever
receives a bar value from anything in this module.

The one code path in this repository that reads a priced bar field outside a
sealed writer does not exist. ``tests/test_guards.py`` walks the parse tree of
every module and fails if one appears.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from orb.ledger import AppendOnlyLedger

PRICED_BAR_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "open",
        "high",
        "low",
        "close",
        "volume",
        "vwap",
        "trade_count",
        "tradecount",
        "trades",
        "bid",
        "ask",
        "o",
        "h",
        "l",
        "c",
        "v",
        "vw",
        "n",
        "bp",
        "ap",
        "bidprice",
        "askprice",
        "bid_price",
        "ask_price",
        "adjclose",
        "adj_close",
        "openinterest",
    }
)
"""Every spelling of a priced bar field, in every vendor dialect probed.

Guard 5 refuses a read of any of these outside a sealed writer. The list is
deliberately wider than any single vendor's schema: a field this repository
never sees costs nothing to forbid, and a field it forbids too late costs the
whole experiment.
"""

READABLE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "ticker",
        "symbol",
        "exchange",
        "primary_exchange",
        "listing_date",
        "delisting_date",
        "delisted_utc",
        "timestamp",
        "t",
        "session_date",
        "bar_count",
        "status_code",
        "status",
    }
)
"""The readable field list of the blindness section, stated exactly."""


class SealViolationError(PermissionError):
    """Raised when a caller asks a sealed writer for a bar value."""


@final
@dataclass(frozen=True, slots=True)
class SealRecord:
    """What a sealed write returns. Counts and hashes only, never a value."""

    path: Path
    sha256: str
    byte_count: int
    line_count: int

    def as_row(self) -> dict[str, object]:
        return {
            "kind": "seal",
            "path": str(self.path),
            "sha256": self.sha256,
            "byte_count": self.byte_count,
            "line_count": self.line_count,
        }


@final
class SealedWriter:
    """Writes raw vendor bytes. Parses nothing. Returns no bar value, ever."""

    __slots__ = ("_ledger", "root")

    def __init__(self, root: Path, ledger: AppendOnlyLedger) -> None:
        self.root = root
        self._ledger = ledger
        self.root.mkdir(parents=True, exist_ok=True)

    def store(self, relative_path: str, payload: bytes) -> SealRecord:
        """Store ``payload`` verbatim and record its hash. No parse occurs."""
        target = self.root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        record = SealRecord(
            path=target,
            sha256=hashlib.sha256(payload).hexdigest(),
            byte_count=len(payload),
            line_count=payload.count(b"\n"),
        )
        self._ledger.append(record.as_row())
        return record

    def value(self, *_args: object, **_kwargs: object) -> None:
        """Structurally unavailable. A sealed writer returns no bar value."""
        raise SealViolationError(
            "a sealed writer returns no bar value to any caller; it returns "
            "counts, hashes and timestamps only."
        )
