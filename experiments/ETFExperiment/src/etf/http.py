"""Paced keyless HTTP client, ledger-gated. The only module that opens a socket.

Every request charges the ledger first, then paces per endpoint, then sends. An
HTTP error status is returned to the caller, who maps it to a recorded call
state; a transport failure settles source_failed and raises loudly. No key,
token, or credential exists anywhere on this path, and none is needed.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass

from etf.config import CONFIG
from etf.ledger.requests import RequestLedger
from etf.pacing import min_spacing_s


class TransportFailure(RuntimeError):
    """The request never produced an HTTP status. Settled as source_failed."""


@dataclass(frozen=True, slots=True)
class Response:
    status: int
    body: bytes
    elapsed_s: float
    headers: dict[str, str]


class PacedClient:
    """Charges, paces, sends. Returns every HTTP status; raises on transport failure."""

    def __init__(
        self,
        ledger: RequestLedger,
        pacing_overrides: dict[str, float] | None = None,
        sleeper: Callable[[float], None] = time.sleep,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self._ledger = ledger
        self._overrides = dict(pacing_overrides or {})
        self._sleep = sleeper
        self._monotonic = monotonic
        self._last_sent: dict[str, float] = {}

    def _pace(self, endpoint: str) -> None:
        interval = min_spacing_s(endpoint, self._overrides)
        last = self._last_sent.get(endpoint)
        if last is not None:
            wait = interval - (self._monotonic() - last)
            if wait > 0:
                self._sleep(wait)

    def _send(self, request: urllib.request.Request, source: str, endpoint: str) -> Response:
        self._ledger.charge(source, endpoint)
        self._pace(endpoint)
        started = self._monotonic()
        self._last_sent[endpoint] = started
        try:
            with urllib.request.urlopen(
                request, timeout=CONFIG.request_timeout_seconds
            ) as response:
                status = int(response.status)
                content = bytes(response.read())
                headers = {k.lower(): v for k, v in response.headers.items()}
        except urllib.error.HTTPError as exc:
            status = int(exc.code)
            content = bytes(exc.read())
            headers = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            self._ledger.settle(source, endpoint, "source_failed", None)
            raise TransportFailure(f"{endpoint}: no HTTP status came back: {exc}") from exc
        elapsed = self._monotonic() - started
        self._ledger.settle(source, endpoint, "http", status)
        return Response(status=status, body=content, elapsed_s=elapsed, headers=headers)

    def get(self, url: str, *, source: str, endpoint: str) -> Response:
        request = urllib.request.Request(
            url, headers={"User-Agent": CONFIG.user_agent}, method="GET"
        )
        return self._send(request, source, endpoint)

    def post_json(
        self, url: str, body: dict[str, object], *, source: str, endpoint: str
    ) -> Response:
        request = urllib.request.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": CONFIG.user_agent},
            method="POST",
        )
        return self._send(request, source, endpoint)
