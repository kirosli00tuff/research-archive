"""Request-body builders for the venue info endpoint. Pure, no network.

Each builder returns the JSON body for one documented request type. Keeping
them pure keeps every collector testable without a socket and keeps the
endpoint names (the ledger's accounting unit) in one place.
"""

from __future__ import annotations

EP_META = "info:meta"
EP_META_AND_CTXS = "info:metaAndAssetCtxs"
EP_PERP_DEXS = "info:perpDexs"
EP_CANDLE_SNAPSHOT = "info:candleSnapshot"
EP_FUNDING_HISTORY = "info:fundingHistory"
EP_L2_BOOK = "info:l2Book"

ALL_ENDPOINTS: tuple[str, ...] = (
    EP_META,
    EP_META_AND_CTXS,
    EP_PERP_DEXS,
    EP_CANDLE_SNAPSHOT,
    EP_FUNDING_HISTORY,
    EP_L2_BOOK,
)


def meta_body(dex: str | None = None) -> dict[str, object]:
    """Perp universe for the main dex (dex=None) or a named HIP-3 builder dex."""
    if dex is None:
        return {"type": "meta"}
    return {"type": "meta", "dex": dex}


def meta_and_asset_ctxs_body() -> dict[str, object]:
    return {"type": "metaAndAssetCtxs"}


def perp_dexs_body() -> dict[str, object]:
    return {"type": "perpDexs"}


def candle_snapshot_body(coin: str, interval: str, start_ms: int, end_ms: int) -> dict[str, object]:
    if interval not in ("1h", "1d"):
        raise ValueError(f"unregistered candle interval {interval!r}; the study uses 1h and 1d")
    return {
        "type": "candleSnapshot",
        "req": {"coin": coin, "interval": interval, "startTime": start_ms, "endTime": end_ms},
    }


def funding_history_body(coin: str, start_ms: int, end_ms: int | None = None) -> dict[str, object]:
    body: dict[str, object] = {"type": "fundingHistory", "coin": coin, "startTime": start_ms}
    if end_ms is not None:
        body["endTime"] = end_ms
    return body


def l2_book_body(coin: str) -> dict[str, object]:
    return {"type": "l2Book", "coin": coin}
