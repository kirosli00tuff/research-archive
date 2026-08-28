"""The source builds fresh-adjustment queries and fails loudly."""
import json

import pytest

from hfexperiment.alpaca_source import AlpacaSource, SourceError


class FakeTransport:
    def __init__(self, responses: list[tuple[int, object]]) -> None:
        self.responses = responses
        self.urls: list[str] = []

    def __call__(
        self, url: str, headers: dict[str, str]
    ) -> tuple[int, bytes]:
        self.urls.append(url)
        status, payload = self.responses.pop(0)
        return status, json.dumps(payload).encode()


def _source(transport: FakeTransport) -> AlpacaSource:
    return AlpacaSource("key", "secret", transport, sleep=lambda _s: None)


def test_daily_bars_carry_adjustment_all_and_paginate() -> None:
    page_one = {
        "bars": {
            "AAA": [
                {"t": "2026-09-01T04:00:00Z", "o": 1, "h": 2, "l": 1,
                 "c": 1.5, "v": 10}
            ]
        },
        "next_page_token": "tok",
    }
    page_two = {
        "bars": {
            "AAA": [
                {"t": "2026-09-02T04:00:00Z", "o": 1, "h": 2, "l": 1,
                 "c": 1.6, "v": 11}
            ]
        },
        "next_page_token": None,
    }
    transport = FakeTransport([(200, page_one), (200, page_two)])
    bars = _source(transport).daily_bars(["AAA"], "2026-09-01", "2026-09-02")
    assert "adjustment=all" in transport.urls[0]
    assert "feed=sip" in transport.urls[0]
    assert "page_token=tok" in transport.urls[1]
    assert [row[0] for row in bars["AAA"]] == ["2026-09-01", "2026-09-02"]
    assert bars["AAA"][1][4] == 1.6


def test_http_error_raises_source_error_not_a_fabricated_payload() -> None:
    transport = FakeTransport([(500, {"message": "boom"})])
    with pytest.raises(SourceError, match="HTTP 500"):
        _source(transport).calendar("2026-09-01", "2026-09-02")


def test_rate_limit_retries_once_then_succeeds() -> None:
    transport = FakeTransport(
        [(429, {}), (200, [{"date": "2026-09-01", "open": "09:30",
                            "close": "16:00"}])]
    )
    sessions = _source(transport).calendar("2026-09-01", "2026-09-01")
    assert sessions == [("2026-09-01", "09:30", "16:00")]
    assert len(transport.urls) == 2
