"""The evidence ledger. Every claim this stage makes gets a row before it is
quoted anywhere else.

A refusal is demonstrated by producing it, never asserted, so a refusal writes
a row here the same as any other event.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from insider.ledger.append_only import AppendOnlyLedger
from insider.paths import EVIDENCE_LEDGER


def record(kind: str, **fields: Any) -> dict[str, Any]:
    """Append one evidence row and return it."""
    row: dict[str, Any] = {
        "recorded_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "kind": kind,
        **fields,
    }
    AppendOnlyLedger(EVIDENCE_LEDGER).append(row)
    return row


def rows_of_kind(kind: str) -> list[dict[str, Any]]:
    return [r for r in AppendOnlyLedger(EVIDENCE_LEDGER).iter_rows() if r.get("kind") == kind]
