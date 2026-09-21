"""Typed wrappers over the info endpoint.

Meta and perpDexs responses are instrument metadata and are fully parseable.
Candle and funding payloads are handed to npl.blindness and are never parsed
here. Every HTTP status maps to a recorded call state; nothing is retried
silently and nothing empty is synthesized into a value.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from npl.api import (
    EP_CANDLE_SNAPSHOT,
    EP_FUNDING_HISTORY,
    EP_META,
    EP_PERP_DEXS,
    candle_snapshot_body,
    funding_history_body,
    meta_body,
    perp_dexs_body,
)
from npl.callstate import CallState
from npl.http import InfoClient, TransportFailure


@dataclass(frozen=True, slots=True)
class FetchOutcome:
    """One request's terminal state, with the raw body where one was served."""

    state: CallState
    http_status: int | None
    body: bytes | None


@dataclass(frozen=True, slots=True)
class PerpInfo:
    """One instrument row from a meta universe. Metadata only, no prices."""

    name: str
    sz_decimals: int
    max_leverage: int
    is_delisted: bool


@dataclass(frozen=True, slots=True)
class PerpDex:
    """One HIP-3 builder dex row from perpDexs."""

    name: str
    full_name: str


def _state_of(status: int) -> CallState:
    if status == 200:
        return CallState.STORED
    if status == 429:
        return CallState.RATE_LIMITED
    return CallState.SOURCE_FAILED


class Venue:
    """The one place requests are made and statuses become call states."""

    def __init__(self, client: InfoClient) -> None:
        self._client = client

    def request(self, body: dict[str, object], endpoint: str) -> FetchOutcome:
        try:
            response = self._client.post(body, endpoint)
        except TransportFailure:
            return FetchOutcome(state=CallState.SOURCE_FAILED, http_status=None, body=None)
        return FetchOutcome(
            state=_state_of(response.status),
            http_status=response.status,
            body=response.body,
        )

    def meta(self, dex: str | None = None) -> FetchOutcome:
        return self.request(meta_body(dex), EP_META)

    def perp_dexs(self) -> FetchOutcome:
        return self.request(perp_dexs_body(), EP_PERP_DEXS)

    def candles(self, coin: str, interval: str, start_ms: int, end_ms: int) -> FetchOutcome:
        return self.request(
            candle_snapshot_body(coin, interval, start_ms, end_ms), EP_CANDLE_SNAPSHOT
        )

    def funding(self, coin: str, start_ms: int, end_ms: int | None = None) -> FetchOutcome:
        return self.request(funding_history_body(coin, start_ms, end_ms), EP_FUNDING_HISTORY)


def parse_meta(body: bytes) -> tuple[PerpInfo, ...]:
    """Parse a meta universe. Refuses shapes it does not recognize."""
    parsed = json.loads(body)
    if not isinstance(parsed, dict) or "universe" not in parsed:
        raise ValueError("meta response carries no universe; refusing to guess")
    rows: list[PerpInfo] = []
    for row in parsed["universe"]:
        if not isinstance(row, dict):
            raise ValueError("meta universe row is not an object; refusing to guess")
        rows.append(
            PerpInfo(
                name=str(row["name"]),
                sz_decimals=int(row["szDecimals"]),
                max_leverage=int(row["maxLeverage"]),
                is_delisted=bool(row.get("isDelisted", False)),
            )
        )
    return tuple(rows)


def parse_perp_dexs(body: bytes) -> tuple[PerpDex, ...]:
    """Parse perpDexs. The first entry is null (the main dex) and is skipped."""
    parsed = json.loads(body)
    if not isinstance(parsed, list):
        raise ValueError("perpDexs response is not a list; refusing to guess")
    dexs: list[PerpDex] = []
    for row in parsed:
        if row is None:
            continue
        if not isinstance(row, dict):
            raise ValueError("perpDexs row is neither null nor an object; refusing to guess")
        dexs.append(PerpDex(name=str(row["name"]), full_name=str(row.get("full_name", ""))))
    return tuple(dexs)
