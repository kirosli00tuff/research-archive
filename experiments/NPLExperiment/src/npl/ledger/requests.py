"""The request ledger. Charges before sending, refuses past the daily cap.

Zero dollars and keyless endpoints do not remove the need for a gate: a gate
that never fires is still a gate, and the cap is the registered protection
against a runaway collector. The charge lands (fsynced) before any socket
opens, so a crash between charge and response leaves an over-count, never an
under-count. Settle rows record what came back and never move the cap.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from npl.clock import iso_z, now_utc
from npl.config import CONFIG
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import REQUEST_LEDGER


class CapExceeded(RuntimeError):
    """The daily request cap would be exceeded. Refused loudly, nothing sent."""


class RequestLedger:
    """Append-only, restart-proof daily request accounting."""

    def __init__(
        self,
        path: Path = REQUEST_LEDGER,
        cap_per_day: int = CONFIG.request_cap_per_day,
        clock: Callable[[], datetime] = now_utc,
    ) -> None:
        self._ledger = AppendOnlyLedger(path)
        self._cap = cap_per_day
        self._clock = clock
        # A truncated final line is reported at startup, never appended past.
        self._ledger.require_intact()

    def spent_on(self, day: str) -> int:
        """Charge rows for a UTC day. Reads the file, so restarts cannot reset it."""
        rows = self._ledger.read().rows
        return sum(1 for r in rows if r.get("day") == day and r.get("kind") == "charge")

    def charge(self, endpoint: str) -> None:
        """Charge one request before it is sent. Refuses past the cap, naming arithmetic."""
        now = self._clock()
        day = now.date().isoformat()
        spent = self.spent_on(day)
        if spent + 1 > self._cap:
            raise CapExceeded(
                f"daily request cap: {spent} charged on {day} and one more would exceed "
                f"the registered cap of {self._cap}. Nothing was sent."
            )
        self._ledger.append({"day": day, "endpoint": endpoint, "kind": "charge", "ts": iso_z(now)})

    def settle(self, endpoint: str, status: str, http_status: int | None) -> None:
        """Record what came back. A settle row never moves the cap."""
        now = self._clock()
        self._ledger.append(
            {
                "day": now.date().isoformat(),
                "endpoint": endpoint,
                "http_status": http_status,
                "kind": "settle",
                "status": status,
                "ts": iso_z(now),
            }
        )
