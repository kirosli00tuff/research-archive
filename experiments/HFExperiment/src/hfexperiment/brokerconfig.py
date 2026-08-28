"""Broker configuration and the account pin.

The operator declined the scoped IBKR username and runs the Gateway
from the full-access main login, so the session can see and trade
accounts holding money that is not this project's. The pin here is the
software standing in for the scoped username, ADR-018. Three facts
must cohere before anything faces a socket: the declared mode, the
port for that mode, and the account prefix for that mode.

The TWS API treats an empty account field as a request for the default
account, which on this login is the operator's main account. Empty
therefore refuses exactly as absent does.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hfexperiment.envfile import parse_env
from hfexperiment.gate import Refusal

# Paper until D.1 arms live by amendment. Nothing else changes this.
DECLARED_MODE = "paper"

MODE_PORTS = {"paper": 4002, "live": 4001}
MODE_PREFIXES = {"paper": "DU", "live": "U"}

REQUIRED_VARS = (
    "IBKR_GATEWAY_HOST",
    "IBKR_GATEWAY_PORT",
    "IBKR_CLIENT_ID",
    "IBKR_ACCOUNT_ID",
)


class BrokerEnvError(RuntimeError):
    """.env lacks a Gateway variable. Refuse loudly, name the gap."""


@dataclass(frozen=True)
class BrokerEnv:
    """The Gateway connection facts from .env. Values, never defaults."""

    host: str
    port: int
    client_id: int
    account_id: str


def load_broker_env(env_path: str | Path) -> BrokerEnv:
    """The four Gateway variables, or a refusal naming what is absent."""
    path = Path(env_path)
    if not path.exists():
        raise BrokerEnvError(f"{path} does not exist")
    values = parse_env(path.read_text(encoding="utf-8"))
    missing = [v for v in REQUIRED_VARS if not values.get(v)]
    if missing:
        raise BrokerEnvError(f"{path} lacks {missing}")
    return BrokerEnv(
        host=values["IBKR_GATEWAY_HOST"],
        port=int(values["IBKR_GATEWAY_PORT"]),
        client_id=int(values["IBKR_CLIENT_ID"]),
        account_id=values["IBKR_ACCOUNT_ID"],
    )


def pin_account(
    intent_account: str | None, pinned: str, mode: str
) -> Refusal | None:
    """Refusal 8. The account pin, first-class, checked before anything.

    The intent's account must be present, must exactly equal the pinned
    IBKR_ACCOUNT_ID, and the account must carry the declared mode's
    prefix. Absent, empty, mismatched, and mode-inconsistent each
    refuse with the arithmetic named. This is the software standing in
    for the scoped username the operator declined.
    """
    if mode not in MODE_PREFIXES:
        raise ValueError(f"undeclared mode: {mode}")
    if intent_account is None:
        return Refusal(
            reason="account_not_pinned",
            arithmetic="intent.account is absent. The TWS API would "
                       "route an accountless order to the default "
                       "account on the full-access login. Refused "
                       "before any socket.",
        )
    if intent_account == "":
        return Refusal(
            reason="account_not_pinned",
            arithmetic="intent.account is empty. The TWS API treats an "
                       "empty account field as the default account, "
                       "the operator's main account. Refused.",
        )
    if intent_account != pinned:
        return Refusal(
            reason="account_not_pinned",
            arithmetic=f"intent.account {intent_account} != pinned "
                       f"IBKR_ACCOUNT_ID {pinned}",
        )
    prefix = MODE_PREFIXES[mode]
    if not intent_account.startswith(prefix):
        return Refusal(
            reason="account_mode_mismatch",
            arithmetic=f"account {intent_account} lacks the {mode} "
                       f"prefix {prefix}: right account under the "
                       f"wrong declared mode refuses",
        )
    return None
