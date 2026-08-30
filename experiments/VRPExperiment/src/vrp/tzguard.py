"""Guard 2 — the timezone guard. A naive datetime is refused, never assumed.

Every timestamp in this repository is timezone-aware and in UTC. A naive
datetime is refused at the boundary rather than silently interpreted as local
time, because "silently interpreted as local time" is how a British Columbia
machine turns a UTC exchange settlement stamp into a figure seven or eight
hours wrong depending on the month.

Option expiries carry their **exchange settlement time**, which is a distinct
object from a bare date: Deribit settles at 08:00 UTC, CME at a
contract-specific time in a named exchange timezone. :class:`ExchangeExpiry`
refuses to exist without both.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import final


class NaiveDatetimeError(ValueError):
    """Raised when a datetime without a timezone reaches a boundary."""


class NonUtcDatetimeError(ValueError):
    """Raised when an aware datetime is not normalised to UTC."""


def require_aware(value: datetime, context: str) -> datetime:
    """Return ``value`` if it is timezone-aware; refuse loudly if it is not."""
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        raise NaiveDatetimeError(
            f"{context}: refusing naive datetime {value!r}. Every timestamp in "
            "this repository is timezone-aware. A naive stamp is never assumed "
            "to be UTC and never assumed to be local."
        )
    return value


def require_utc(value: datetime, context: str) -> datetime:
    """Return ``value`` if it is aware **and** exactly UTC. Never converts."""
    aware = require_aware(value, context)
    offset = aware.utcoffset()
    if offset is None or offset != timedelta(0):
        raise NonUtcDatetimeError(
            f"{context}: refusing non-UTC datetime {value!r} at offset {offset}. "
            "Convert explicitly at the boundary; this guard never converts for "
            "you, because a silent conversion hides which side was wrong."
        )
    return aware


def utc_now() -> datetime:
    """The only sanctioned clock read. Always aware, always UTC."""
    return datetime.now(tz=UTC)


def iso_utc(value: datetime, context: str = "iso_utc") -> str:
    """Serialise an aware UTC datetime to ``...Z`` form, refusing naive input."""
    return (
        require_utc(value, context)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def parse_utc(text: str, context: str = "parse_utc") -> datetime:
    """Parse an ISO-8601 string, refusing anything that lacks an offset."""
    candidate = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return require_utc(candidate, f"{context}: {text!r}")


@final
@dataclass(frozen=True, slots=True)
class ExchangeExpiry:
    """An option expiry with its exchange settlement time attached.

    A bare expiry date is not enough to place a realized-volatility window
    against an implied one. The settlement instant decides which returns fall
    inside the tenor, and it differs by venue.
    """

    settlement: datetime
    """The settlement instant, timezone-aware and UTC."""

    exchange: str
    """The exchange whose settlement calendar defines the instant."""

    settlement_rule: str
    """The published rule, recorded verbatim, e.g. '08:00 UTC daily'."""

    def __post_init__(self) -> None:
        require_utc(
            self.settlement,
            f"ExchangeExpiry({self.exchange}) settlement",
        )
        if not self.exchange.strip():
            raise ValueError(
                "ExchangeExpiry refuses an empty exchange: an expiry without "
                "a named settlement calendar is not an expiry."
            )
        if not self.settlement_rule.strip():
            raise ValueError(
                "ExchangeExpiry refuses an empty settlement_rule: the rule is "
                "recorded verbatim so a later reader can check the instant."
            )

    def as_row(self) -> dict[str, str]:
        return {
            "settlement": iso_utc(self.settlement, "ExchangeExpiry.as_row"),
            "exchange": self.exchange,
            "settlement_rule": self.settlement_rule,
        }
