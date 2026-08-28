"""The Alpaca data source. Thin, injected transport, loud failures.

Every bar query carries adjustment=all and feed=sip, per the B.1
fresh-adjustment design: the daily run re-queries the session fresh and
the formation run re-queries the full trailing window fresh, so an
adjustment landing between runs re-enters the store rather than aging
out of it.

Credentials come from HFExperiment's own .env through envfile.py, never
from AiTrader. The timer is staggered to 23:30 UTC against AiTrader's
22:30 so two collectors never share a rate window, and requests here
sleep between calls well under the documented 200 per minute.

A failure raises SourceError. The caller records source_failed and the
day excludes and retries. Nothing here ever fabricates a payload.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from typing import Any

DATA_BASE = "https://data.alpaca.markets"
TRADE_BASE = "https://api.alpaca.markets"
BARS_PAGE_LIMIT = 10_000
SYMBOL_CHUNK = 200
RATE_SLEEP_S = 0.35
RETRY_AFTER_429_S = 20.0
TIMEOUT_S = 30

Transport = Callable[[str, Mapping[str, str]], tuple[int, bytes]]
DailyBar = tuple[
    str, float | None, float | None, float | None, float, float | None
]


class SourceError(RuntimeError):
    """The source could not serve the request. The day is source_failed."""

    def __init__(self, endpoint: str, detail: str) -> None:
        super().__init__(f"{endpoint}: {detail}")
        self.endpoint = endpoint
        self.detail = detail


def urllib_transport(url: str, headers: Mapping[str, str]) -> tuple[int, bytes]:
    """GET the URL. Returns (status, body). Network errors raise SourceError."""
    request = urllib.request.Request(url, headers=dict(headers))
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as err:
        return err.code, err.read()
    except Exception as err:  # noqa: BLE001 - every network failure is one case
        raise SourceError(url.split("?")[0], repr(err)) from err


class AlpacaSource:
    """Calendar, assets, and daily bars against the Alpaca HTTP API."""

    def __init__(
        self,
        key_id: str,
        secret_key: str,
        transport: Transport = urllib_transport,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._headers = {
            "APCA-API-KEY-ID": key_id,
            "APCA-API-SECRET-KEY": secret_key,
        }
        self._transport = transport
        self._sleep = sleep

    def _get_json(self, url: str) -> Any:
        endpoint = url.split("?")[0]
        for attempt in (1, 2):
            status, body = self._transport(url, self._headers)
            if status == 429 and attempt == 1:
                self._sleep(RETRY_AFTER_429_S)
                continue
            if status != 200:
                raise SourceError(endpoint, f"HTTP {status}")
            try:
                return json.loads(body.decode())
            except ValueError as err:
                raise SourceError(endpoint, f"bad JSON: {err}") from err
        raise SourceError(endpoint, "unreachable retry state")

    def calendar(self, start: str, end: str) -> list[tuple[str, str, str]]:
        """Trading sessions as (date, open_local, close_local)."""
        url = f"{TRADE_BASE}/v2/calendar?start={start}&end={end}"
        payload = self._get_json(url)
        if not isinstance(payload, list):
            raise SourceError(url.split("?")[0], "calendar payload not a list")
        return [(d["date"], d["open"], d["close"]) for d in payload]

    def active_assets(self) -> list[tuple[str, str, str, str, int]]:
        """Active US equities as (symbol, name, exchange, status, tradable)."""
        url = f"{TRADE_BASE}/v2/assets?status=active&asset_class=us_equity"
        payload = self._get_json(url)
        if not isinstance(payload, list):
            raise SourceError(url.split("?")[0], "assets payload not a list")
        return [
            (
                a["symbol"],
                a.get("name") or "",
                a.get("exchange") or "",
                a.get("status") or "",
                1 if a.get("tradable") else 0,
            )
            for a in payload
        ]

    def daily_bars(
        self, symbols: Sequence[str], start: str, end: str
    ) -> dict[str, list[DailyBar]]:
        """Daily bars, adjustment=all, feed=sip, for [start, end] inclusive.

        Chunks symbols and follows pagination. A symbol the source
        returns nothing for is simply absent from the result: absence
        is the caller's signal, never patched here.
        """
        out: dict[str, list[DailyBar]] = {}
        for i in range(0, len(symbols), SYMBOL_CHUNK):
            chunk = symbols[i : i + SYMBOL_CHUNK]
            self._collect_chunk(chunk, start, end, out)
        return out

    def _collect_chunk(
        self,
        chunk: Sequence[str],
        start: str,
        end: str,
        out: dict[str, list[DailyBar]],
    ) -> None:
        base = (
            f"{DATA_BASE}/v2/stocks/bars?symbols={','.join(chunk)}"
            f"&timeframe=1Day&adjustment=all&feed=sip"
            f"&start={start}&end={end}&limit={BARS_PAGE_LIMIT}"
        )
        token: str | None = None
        while True:
            url = base + (f"&page_token={token}" if token else "")
            payload = self._get_json(url)
            bars = payload.get("bars") or {}
            for symbol, rows in bars.items():
                for row in rows:
                    out.setdefault(symbol, []).append(
                        (
                            str(row["t"])[:10],
                            row.get("o"),
                            row.get("h"),
                            row.get("l"),
                            float(row["c"]),
                            row.get("v"),
                        )
                    )
            token = payload.get("next_page_token")
            self._sleep(RATE_SLEEP_S)
            if not token:
                return
