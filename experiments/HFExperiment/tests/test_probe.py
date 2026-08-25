"""The probe: mode-port assertion, read-only encoder, recorded states."""
import socket
from pathlib import Path

import pytest

import hfexperiment.ibkrprobe as probe_module
from hfexperiment.brokerconfig import BrokerEnv
from hfexperiment.ibkrprobe import (
    OUTBOUND_MESSAGE_IDS,
    ProbeProtocolError,
    assert_mode_port,
    encode_message,
    probe,
)


def test_mode_port_assertion_refuses_before_any_connection() -> None:
    refusal = assert_mode_port("paper", 4001)
    assert refusal is not None
    assert refusal.reason == "mode_port_mismatch"
    assert "4002" in refusal.arithmetic
    refusal = assert_mode_port("live", 4002)
    assert refusal is not None
    assert assert_mode_port("paper", 4002) is None
    assert assert_mode_port("live", 4001) is None
    with pytest.raises(ValueError, match="undeclared mode"):
        assert_mode_port("demo", 4002)


def test_probe_refuses_mode_port_mismatch_without_touching_network(
) -> None:
    env = BrokerEnv(
        host="host.invalid", port=4001, client_id=1,
        account_id="[paper account ID removed]",
    )
    result = probe(env)
    assert result.state == "mode_port_mismatch"


def test_encoder_is_structurally_read_only() -> None:
    # The only messages this module can send: START_API (71) and
    # REQ_CURRENT_TIME (49). placeOrder is message id 3 and the
    # encoder must refuse it and every other id.
    assert sorted(OUTBOUND_MESSAGE_IDS) == [49, 71]
    for other_id in (3, 4, 1, 61, 0):
        with pytest.raises(ProbeProtocolError, match="read-only"):
            encode_message(other_id, 1)


def test_no_order_vocabulary_in_the_probe_source() -> None:
    src = Path(probe_module.__file__).read_text()
    for token in ("placeOrder", "PLACE_ORDER", "cancelOrder",
                  "CANCEL_ORDER"):
        assert token not in src


def test_encoded_frame_is_length_prefixed_nul_separated() -> None:
    frame = encode_message(49, 1)
    assert frame[:4] == b"\x00\x00\x00\x05"
    assert frame[4:] == b"49\x001\x00"


def test_unreachable_is_a_recorded_state_not_an_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Grab a verifiably free port, close it, and align the mode map to
    # it so the assertion passes and the connection itself refuses.
    placeholder = socket.socket()
    placeholder.bind(("127.0.0.1", 0))
    free_port = placeholder.getsockname()[1]
    placeholder.close()
    monkeypatch.setitem(probe_module.MODE_PORTS, "paper", free_port)
    env = BrokerEnv(
        host="127.0.0.1", port=free_port, client_id=1,
        account_id="[paper account ID removed]",
    )
    result = probe(env)
    assert result.state == "unreachable"
    assert "Recorded, not raised" in result.detail
