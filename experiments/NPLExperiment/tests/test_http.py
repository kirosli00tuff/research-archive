"""The HTTP client charges before sending, paces per endpoint, settles loudly."""

from __future__ import annotations

import email.message
import io
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import pytest

from npl.http import InfoClient, TransportFailure
from npl.ledger.append_only import AppendOnlyLedger
from npl.ledger.requests import CapExceeded, RequestLedger


class FakeClock:
    def __init__(self) -> None:
        self.t = 0.0
        self.slept: list[float] = []

    def monotonic(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.t += seconds


def _ledger(tmp_path: Path, cap: int = 10) -> RequestLedger:
    return RequestLedger(tmp_path / "req.jsonl", cap_per_day=cap)


def test_the_charge_lands_before_the_socket_opens(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[str] = []

    def refuse(*args: Any, **kwargs: Any) -> Any:
        calls.append("network")
        raise AssertionError("the socket must not open when the ledger refuses")

    monkeypatch.setattr(urllib.request, "urlopen", refuse)
    ledger = _ledger(tmp_path, cap=0)
    client = InfoClient(ledger)
    with pytest.raises(CapExceeded):
        client.post({"type": "meta"}, "info:meta")
    assert calls == []


class _Resp:
    status = 200

    def read(self) -> bytes:
        return b"[]"

    def __enter__(self) -> _Resp:
        return self

    def __exit__(self, *args: object) -> None:
        return None


def test_pacing_holds_between_same_endpoint_sends(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    clock = FakeClock()
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: _Resp())
    client = InfoClient(
        _ledger(tmp_path),
        pacing_s={"info:meta": 5.0},
        sleeper=clock.sleep,
        monotonic=clock.monotonic,
    )
    client.post({"type": "meta"}, "info:meta")
    client.post({"type": "meta"}, "info:meta")
    assert clock.slept
    assert clock.slept[0] == pytest.approx(5.0)
    # A different endpoint is not held by this endpoint's pace.
    client.post({"type": "perpDexs"}, "info:perpDexs")
    assert len(clock.slept) == 1


def test_an_http_error_status_is_returned_not_raised(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_429(*args: Any, **kwargs: Any) -> Any:
        raise urllib.error.HTTPError(
            "https://api.hyperliquid.xyz/info",
            429,
            "Too Many Requests",
            email.message.Message(),
            io.BytesIO(b"slow"),
        )

    monkeypatch.setattr(urllib.request, "urlopen", raise_429)
    client = InfoClient(_ledger(tmp_path))
    response = client.post({"type": "meta"}, "info:meta")
    assert response.status == 429
    assert response.body == b"slow"


def test_a_transport_failure_settles_source_failed_and_raises(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def unreachable(*args: Any, **kwargs: Any) -> Any:
        raise urllib.error.URLError("dns down")

    monkeypatch.setattr(urllib.request, "urlopen", unreachable)
    path = tmp_path / "req.jsonl"
    ledger = RequestLedger(path, cap_per_day=10)
    client = InfoClient(ledger)
    with pytest.raises(TransportFailure, match="no HTTP status"):
        client.post({"type": "meta"}, "info:meta")
    rows = AppendOnlyLedger(path).read().rows
    settles = [r for r in rows if r["kind"] == "settle"]
    assert settles
    assert settles[-1]["status"] == "source_failed"
    assert settles[-1]["http_status"] is None
