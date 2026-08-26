"""The fetch ledger. One row per SEC request, whether served from cache or wire.

The throttle is only meaningful if it can be audited after the fact, so every
request records its URL, its outcome, and the seconds the throttle made it wait.
"""

from __future__ import annotations

import datetime as dt

from insider.ledger.append_only import AppendOnlyLedger
from insider.paths import FETCH_LEDGER


def record_fetch(
    url: str, *, status: int | None, served_from: str, waited_seconds: float, bytes_read: int
) -> None:
    AppendOnlyLedger(FETCH_LEDGER).append(
        {
            "recorded_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
            "url": url,
            "status": status,
            "served_from": served_from,
            "waited_seconds": round(waited_seconds, 4),
            "bytes_read": bytes_read,
        }
    )


def wire_request_count() -> int:
    return sum(
        1 for r in AppendOnlyLedger(FETCH_LEDGER).iter_rows() if r.get("served_from") == "wire"
    )
