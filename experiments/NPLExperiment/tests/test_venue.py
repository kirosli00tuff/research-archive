"""The venue layer maps statuses to call states and parses metadata only."""

from __future__ import annotations

import json
from dataclasses import dataclass

import pytest

from npl.callstate import CallState
from npl.http import InfoResponse, TransportFailure
from npl.venue import Venue, parse_meta, parse_perp_dexs

META = json.dumps(
    {
        "universe": [
            {"szDecimals": 5, "name": "BTC", "maxLeverage": 40, "marginTableId": 56},
            {
                "szDecimals": 1,
                "name": "MATIC",
                "maxLeverage": 20,
                "marginTableId": 20,
                "isDelisted": True,
            },
        ]
    }
).encode()

PERP_DEXS = json.dumps([None, {"name": "xyz", "fullName": "XYZ", "deployer": "0x88"}]).encode()


@dataclass
class _FakeClient:
    status: int = 200
    body: bytes = b"[]"
    fail: bool = False

    def post(self, body: dict[str, object], endpoint: str) -> InfoResponse:
        if self.fail:
            raise TransportFailure("down")
        return InfoResponse(status=self.status, body=self.body, elapsed_s=0.01)


def test_a_200_is_stored_with_its_body() -> None:
    venue = Venue(_FakeClient(status=200, body=META))  # type: ignore[arg-type]
    out = venue.meta()
    assert out.state is CallState.STORED
    assert out.body == META


def test_a_429_is_rate_limited_never_source_failed() -> None:
    venue = Venue(_FakeClient(status=429, body=b"slow down"))  # type: ignore[arg-type]
    out = venue.meta()
    assert out.state is CallState.RATE_LIMITED
    assert out.http_status == 429


def test_a_5xx_is_source_failed() -> None:
    venue = Venue(_FakeClient(status=503, body=b""))  # type: ignore[arg-type]
    assert venue.perp_dexs().state is CallState.SOURCE_FAILED


def test_a_transport_failure_is_source_failed_with_no_status() -> None:
    venue = Venue(_FakeClient(fail=True))  # type: ignore[arg-type]
    out = venue.funding("BTC", 0)
    assert out.state is CallState.SOURCE_FAILED
    assert out.http_status is None
    assert out.body is None


def test_parse_meta_reads_the_delisted_flag_and_defaults_it_false() -> None:
    perps = parse_meta(META)
    assert [p.name for p in perps] == ["BTC", "MATIC"]
    assert perps[0].is_delisted is False
    assert perps[1].is_delisted is True
    assert perps[0].sz_decimals == 5
    assert perps[0].max_leverage == 40


def test_parse_meta_refuses_a_shape_without_a_universe() -> None:
    with pytest.raises(ValueError, match="refusing to guess"):
        parse_meta(b'{"error": "nope"}')


def test_parse_perp_dexs_skips_the_null_main_dex_entry() -> None:
    dexs = parse_perp_dexs(PERP_DEXS)
    assert len(dexs) == 1
    assert dexs[0].name == "xyz"


def test_parse_perp_dexs_refuses_a_non_list() -> None:
    with pytest.raises(ValueError, match="refusing to guess"):
        parse_perp_dexs(b"{}")
