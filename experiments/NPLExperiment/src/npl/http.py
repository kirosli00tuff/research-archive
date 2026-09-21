"""Paced keyless HTTP client, ledger-gated. The only module that opens a socket.

Every request charges the ledger first, then paces per endpoint, then sends.
An HTTP error status is returned to the caller, who maps it to a recorded
call state; a transport failure settles source_failed and raises loudly. No
key, token, or credential exists anywhere on this path.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass

from npl.config import CONFIG
from npl.ledger.requests import RequestLedger


class TransportFailure(RuntimeError):
    """The request never produced an HTTP status. Settled as source_failed."""


@dataclass(frozen=True, slots=True)
class InfoResponse:
    status: int
    body: bytes
    elapsed_s: float


class InfoClient:
    """POSTs to the venue info endpoint under the ledger, paced per endpoint."""

    def __init__(
        self,
        ledger: RequestLedger,
        url: str = CONFIG.info_url,
        pacing_s: dict[str, float] | None = None,
        sleeper: Callable[[float], None] = time.sleep,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self._ledger = ledger
        self._url = url
        self._pacing = dict(pacing_s or {})
        self._sleep = sleeper
        self._monotonic = monotonic
        self._last_sent: dict[str, float] = {}

    def _pace(self, endpoint: str) -> None:
        interval = self._pacing.get(endpoint, 0.0)
        if interval <= 0.0:
            return
        last = self._last_sent.get(endpoint)
        if last is not None:
            wait = interval - (self._monotonic() - last)
            if wait > 0:
                self._sleep(wait)

    def post(self, body: dict[str, object], endpoint: str) -> InfoResponse:
        """Charge, pace, send. Returns every HTTP status; raises on transport failure."""
        self._ledger.charge(endpoint)
        self._pace(endpoint)
        payload = json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            self._url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        started = self._monotonic()
        self._last_sent[endpoint] = started
        try:
            with urllib.request.urlopen(
                request, timeout=CONFIG.request_timeout_seconds
            ) as response:
                status = int(response.status)
                content = response.read()
        except urllib.error.HTTPError as exc:
            status = int(exc.code)
            content = exc.read()
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            self._ledger.settle(endpoint, "source_failed", None)
            raise TransportFailure(f"{endpoint}: no HTTP status came back: {exc}") from exc
        elapsed = self._monotonic() - started
        self._ledger.settle(endpoint, "http", status)
        return InfoResponse(status=status, body=content, elapsed_s=elapsed)
