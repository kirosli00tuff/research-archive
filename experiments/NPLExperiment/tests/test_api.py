"""Request-body builders are pure and match the documented request shapes."""

from __future__ import annotations

import pytest

from npl.api import (
    ALL_ENDPOINTS,
    candle_snapshot_body,
    funding_history_body,
    l2_book_body,
    meta_and_asset_ctxs_body,
    meta_body,
    perp_dexs_body,
)


def test_meta_bodies() -> None:
    assert meta_body() == {"type": "meta"}
    assert meta_body("builderdex") == {"type": "meta", "dex": "builderdex"}
    assert meta_and_asset_ctxs_body() == {"type": "metaAndAssetCtxs"}
    assert perp_dexs_body() == {"type": "perpDexs"}


def test_candle_snapshot_body_carries_the_req_envelope() -> None:
    body = candle_snapshot_body("BTC", "1d", 1, 2)
    assert body == {
        "type": "candleSnapshot",
        "req": {"coin": "BTC", "interval": "1d", "startTime": 1, "endTime": 2},
    }


def test_an_unregistered_interval_is_refused() -> None:
    with pytest.raises(ValueError, match="unregistered"):
        candle_snapshot_body("BTC", "5m", 1, 2)


def test_funding_history_body_pages_by_start_time() -> None:
    assert funding_history_body("BTC", 10) == {
        "type": "fundingHistory",
        "coin": "BTC",
        "startTime": 10,
    }
    assert funding_history_body("BTC", 10, 20)["endTime"] == 20


def test_l2_book_body() -> None:
    assert l2_book_body("BTC") == {"type": "l2Book", "coin": "BTC"}


def test_the_six_ledger_endpoint_names_are_distinct() -> None:
    assert len(set(ALL_ENDPOINTS)) == 6
