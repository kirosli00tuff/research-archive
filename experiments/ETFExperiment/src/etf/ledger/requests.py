"""The request ledger. Charges before sending, refuses past the daily cap.

Zero dollars and keyless endpoints do not remove the need for a gate: a gate
that never fires is still a gate, and the cap is the registered protection
against a runaway collector. The charge lands (fsynced) before any socket
opens, so a crash between charge and response leaves an over-count, never an
under-count. Settle rows record what came back and never move the cap.

Caps are per source (Section 12), because a flow source and a venue API are
different budgets and one exhausting the other is exactly the failure a single
shared cap invites.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from etf.clock import iso_z, now_utc
from etf.config import CONFIG
from etf.ledger.append_only import AppendOnlyLedger
from etf.paths import REQUEST_LEDGER


def registered_caps_per_day() -> dict[str, int]:
    """Per-source daily caps. Section 12: one budget must not exhaust another.

    A flow source and a venue API are different budgets; one exhausting the
    other is exactly the failure a single shared cap invites.
    """
    return {
        "flow": CONFIG.request_cap_flow_per_day,
        "archive": CONFIG.request_cap_archive_per_day,
        "venue": CONFIG.request_cap_venue_per_day,
    }


class CapExceeded(RuntimeError):
    """The daily request cap would be exceeded. Refused loudly, nothing sent."""


class RequestLedger:
    """Append-only, restart-proof daily request accounting, keyed per source."""

    def __init__(
        self,
        path: Path = REQUEST_LEDGER,
        caps_per_day: dict[str, int] | None = None,
        default_cap_per_day: int = CONFIG.request_cap_per_day_default,
        clock: Callable[[], datetime] = now_utc,
    ) -> None:
        self._ledger = AppendOnlyLedger(path)
        self._caps = dict(caps_per_day or registered_caps_per_day())
        self._default_cap = default_cap_per_day
        self._clock = clock
        # A truncated final line is reported at startup, never appended past.
        self._ledger.require_intact()

    def cap_for(self, source: str) -> int:
        return self._caps.get(source, self._default_cap)

    def spent_on(self, day: str, source: str) -> int:
        """Charge rows for a UTC day and source. Reads the file, so restarts cannot reset it."""
        rows = self._ledger.read().rows
        return sum(
            1
            for r in rows
            if r.get("day") == day and r.get("kind") == "charge" and r.get("source") == source
        )

    def charge(self, source: str, endpoint: str) -> None:
        """Charge one request before it is sent. Refuses past the cap, naming arithmetic."""
        now = self._clock()
        day = now.date().isoformat()
        cap = self.cap_for(source)
        spent = self.spent_on(day, source)
        if spent + 1 > cap:
            raise CapExceeded(
                f"daily request cap for source {source!r}: {spent} charged on {day} and one "
                f"more would exceed the registered cap of {cap}. Nothing was sent."
            )
        self._ledger.append(
            {
                "day": day,
                "endpoint": endpoint,
                "kind": "charge",
                "source": source,
                "ts": iso_z(now),
            }
        )

    def settle(self, source: str, endpoint: str, status: str, http_status: int | None) -> None:
        """Record what came back. A settle row never moves the cap."""
        now = self._clock()
        self._ledger.append(
            {
                "day": now.date().isoformat(),
                "endpoint": endpoint,
                "http_status": http_status,
                "kind": "settle",
                "source": source,
                "status": status,
                "ts": iso_z(now),
            }
        )
