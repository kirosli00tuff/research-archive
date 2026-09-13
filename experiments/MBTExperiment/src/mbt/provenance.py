"""Guard two — environment provenance is measured, never declared.

Configuration states an **intent**. The connection states a **fact**. The fact
wins, and there is no code path in this package where the intent is written down
as though it were the fact.

The environment tag on every recorded figure derives from the account number the
session actually connected to, read back from the broker. A ``D`` prefix is
paper, a ``U`` prefix is live. A session declaring ``live`` that connects to a
D-prefixed account **refuses and writes nothing**: :class:`SessionProvenance`
raises during construction, so the recorder never receives an object to write.
Refusing at construction rather than at write time is what makes "writes nothing"
structural instead of a discipline someone has to remember.

Account numbers never enter an artifact. Only the prefix, the length and a mask
do, which is everything the guard needs and everything a reader needs to check
the shape.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, unique
from typing import final

from mbt.clock import iso_utc, utc_now


@unique
class Environment(StrEnum):
    """Which broker environment a figure was measured in."""

    PAPER = "paper"
    """A D-prefixed account. Simulated fills, simulated commission reports."""

    LIVE = "live"
    """A U-prefixed account. The only environment a margin figure may come from."""


@unique
class ProvenanceKind(StrEnum):
    """What kind of thing a figure is. The three kinds are not equally blocked.

    Registered separately in REGISTRATION.md Section 0.4 because merging them is
    exactly how a paper margin gets promoted into a live verdict.
    """

    MARGIN = "margin"
    """A property of the ACCOUNT. Carries the account prefix read back from the
    session. Needs a U-prefixed session."""

    QUOTE = "quote"
    """A property of the MARKET DATA FEED. Carries the subscription state and the
    tick delay status. Collectible on paper when real-time."""

    COMMISSION_REPORT = "commission_report"
    """A property of the FILL. Synthetic under paper, so unavailable there in
    either direction."""


class ProvenanceError(PermissionError):
    """Base class for every refusal the provenance machinery can raise."""


class EnvironmentMismatchError(ProvenanceError):
    """A session declared one environment and connected to the other.

    Raised during :class:`SessionProvenance` construction, before any recorder
    holds an object, so a mismatched session writes nothing.
    """


class UnknownAccountPrefixError(ProvenanceError):
    """An account number carried neither a D nor a U prefix.

    Never defaulted to paper. An unrecognised prefix means the assumption that
    IBKR encodes the environment in the prefix has broken, and a guard resting on
    a broken assumption must fail rather than guess the safer-looking side.
    """


#: IBKR encodes the environment in the account prefix. Paper accounts carry D
#: (DU, DUR, DF); live accounts carry U. Measured on this operator's own paper
#: account, which is 9 characters beginning with D.
_PREFIX_TO_ENVIRONMENT = {"D": Environment.PAPER, "U": Environment.LIVE}


def environment_from_account(account: str) -> Environment:
    """Derive the environment from an account number read back from the broker.

    This is the only function in the package that decides an environment, and it
    reads the account rather than the configuration.
    """
    cleaned = account.strip()
    if not cleaned:
        raise UnknownAccountPrefixError(
            "refusing an empty account number: the environment tag on every "
            "recorded figure derives from the account the session actually "
            "connected to, so an empty account has no environment."
        )
    prefix = cleaned[0].upper()
    environment = _PREFIX_TO_ENVIRONMENT.get(prefix)
    if environment is None:
        raise UnknownAccountPrefixError(
            f"refusing account prefix {prefix!r}: expected D for paper or U for "
            "live. An unrecognised prefix means the prefix assumption has "
            "broken, and this guard fails rather than defaulting to either side."
        )
    return environment


def mask_account(account: str) -> str:
    """Mask an account number for an artifact: first character, last character."""
    cleaned = account.strip()
    if len(cleaned) <= 2:
        return "*" * len(cleaned)
    return f"{cleaned[0]}{'*' * (len(cleaned) - 2)}{cleaned[-1]}"


@final
@dataclass(frozen=True, slots=True)
class SessionProvenance:
    """What a session turned out to be, as opposed to what it was asked to be.

    Constructed only through :meth:`from_connection`, which reads the account
    back from the broker. There is no constructor that accepts a declared
    environment as fact.
    """

    declared: Environment
    measured: Environment
    account_prefix: str
    account_masked: str
    account_length: int
    client_id: int
    host: str
    port: int
    connected_at: str

    @classmethod
    def from_connection(
        cls,
        *,
        declared: Environment,
        connected_account: str,
        client_id: int,
        host: str,
        port: int,
    ) -> SessionProvenance:
        """Build provenance from the account the broker actually reported.

        Raises :class:`EnvironmentMismatchError` when the declared environment
        and the measured one differ. The raise happens here, before any caller
        holds an object to record, which is why a mismatched session writes
        nothing rather than writing something tagged wrong.
        """
        measured = environment_from_account(connected_account)
        if measured is not declared:
            raise EnvironmentMismatchError(
                f"REFUSED and wrote nothing: session declared {declared.value!r} "
                f"and connected to a {connected_account.strip()[0].upper()}-prefixed "
                f"account, which is {measured.value!r}. Config states an intent, "
                "the connection states a fact, and the fact wins."
            )
        return cls(
            declared=declared,
            measured=measured,
            account_prefix=connected_account.strip()[0].upper(),
            account_masked=mask_account(connected_account),
            account_length=len(connected_account.strip()),
            client_id=client_id,
            host=host,
            port=port,
            connected_at=iso_utc(utc_now(), "SessionProvenance.connected_at"),
        )

    def as_row(self) -> dict[str, str | int]:
        """The artifact form. Carries the prefix and the mask, never the number."""
        return {
            "declared": str(self.declared),
            "measured": str(self.measured),
            "account_prefix": self.account_prefix,
            "account_masked": self.account_masked,
            "account_length": self.account_length,
            "client_id": self.client_id,
            "host": self.host,
            "port": self.port,
            "connected_at": self.connected_at,
        }
