"""The clock guard. A naive datetime is refused, never assumed.

Ported by copying from VRPExperiment's ``tzguard`` module.

Every timestamp in this repository is timezone-aware and in UTC. A naive
datetime is refused at the boundary rather than silently interpreted as local
time, because "silently interpreted as local time" is how a British Columbia
machine turns a UTC exchange stamp into a figure seven or eight hours wrong
depending on the month. The operator's own Gateway records
``TimeZone=America/Vancouver``, so the two clocks genuinely differ here.

Two clocks are recorded on every observation and never conflated. The **venue**
timestamp is what the exchange stamped on the tick. The **local** timestamp is
when this process received it. Their difference is the staleness that the census
refuses on, and a single merged clock cannot express it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import final

#: A tick whose venue stamp trails the local capture instant by more than this
#: is stale. Registered in REGISTRATION.md Section 3.4 before any quote existed.
STALE_AFTER = timedelta(seconds=5)


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
    return require_utc(value, context).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse_utc(text: str, context: str = "parse_utc") -> datetime:
    """Parse an ISO-8601 string, refusing anything that lacks an offset."""
    candidate = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return require_utc(candidate, f"{context}: {text!r}")


@final
@dataclass(frozen=True, slots=True)
class ObservationClock:
    """The two clocks of one observation, recorded separately.

    ``venue`` is the instant the exchange stamped on the tick. ``local`` is the
    instant this process received it. Ordering across processes is done on the
    recorded clock and never on append order, because append order across
    processes is not a clock.
    """

    venue: datetime
    local: datetime

    def __post_init__(self) -> None:
        require_utc(self.venue, "ObservationClock.venue")
        require_utc(self.local, "ObservationClock.local")

    @property
    def lag(self) -> timedelta:
        """How far the venue stamp trails local capture. May be negative."""
        return self.local - self.venue

    @property
    def is_stale(self) -> bool:
        """True when the venue stamp trails local capture beyond STALE_AFTER."""
        return self.lag > STALE_AFTER

    def as_row(self) -> dict[str, str | float]:
        return {
            "venue_ts": iso_utc(self.venue, "ObservationClock.venue"),
            "local_ts": iso_utc(self.local, "ObservationClock.local"),
            "lag_seconds": self.lag.total_seconds(),
        }
