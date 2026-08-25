"""The broker env loader and the account pin, four ways and passing."""
from pathlib import Path

import pytest

from hfexperiment.brokerconfig import (
    DECLARED_MODE,
    MODE_PORTS,
    MODE_PREFIXES,
    BrokerEnvError,
    load_broker_env,
    pin_account,
)

PINNED = "[paper account ID removed]"


def test_declared_mode_is_paper_with_coherent_maps() -> None:
    assert DECLARED_MODE == "paper"
    assert MODE_PORTS == {"paper": 4002, "live": 4001}
    assert MODE_PREFIXES == {"paper": "DU", "live": "U"}


def test_load_refuses_missing_file_and_missing_vars(tmp_path: Path) -> None:
    with pytest.raises(BrokerEnvError, match="does not exist"):
        load_broker_env(tmp_path / ".env")
    env = tmp_path / ".env"
    env.write_text("IBKR_GATEWAY_HOST=127.0.0.1\n")
    with pytest.raises(BrokerEnvError, match="IBKR_GATEWAY_PORT"):
        load_broker_env(env)


def test_load_reads_all_four_variables(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text(
        "IBKR_GATEWAY_HOST=127.0.0.1\nIBKR_GATEWAY_PORT=4002\n"
        "IBKR_CLIENT_ID=1\nIBKR_ACCOUNT_ID=[paper account ID removed]\n"
    )
    loaded = load_broker_env(env)
    assert loaded.host == "127.0.0.1"
    assert loaded.port == 4002
    assert loaded.client_id == 1
    assert loaded.account_id == PINNED


def test_pin_refuses_absent_account() -> None:
    refusal = pin_account(None, PINNED, "paper")
    assert refusal is not None
    assert refusal.reason == "account_not_pinned"
    assert "absent" in refusal.arithmetic


def test_pin_refuses_empty_account_the_tws_default_trap() -> None:
    refusal = pin_account("", PINNED, "paper")
    assert refusal is not None
    assert refusal.reason == "account_not_pinned"
    assert "default account" in refusal.arithmetic


def test_pin_refuses_wrong_account() -> None:
    refusal = pin_account("DU9999999", PINNED, "paper")
    assert refusal is not None
    assert refusal.reason == "account_not_pinned"
    assert "DU9999999" in refusal.arithmetic
    assert PINNED in refusal.arithmetic


def test_pin_refuses_right_account_under_wrong_mode() -> None:
    refusal = pin_account(PINNED, PINNED, "live")
    assert refusal is not None
    assert refusal.reason == "account_mode_mismatch"
    assert "prefix U" in refusal.arithmetic


def test_pin_passes_the_pinned_account_in_the_declared_mode() -> None:
    assert pin_account(PINNED, PINNED, "paper") is None
    assert pin_account("U1234567", "U1234567", "live") is None


def test_pin_refuses_undeclared_mode_loudly() -> None:
    with pytest.raises(ValueError, match="undeclared mode"):
        pin_account(PINNED, PINNED, "demo")
