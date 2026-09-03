"""A recorded figure and the provenance it is inseparable from.

A number without its provenance is not a figure here. :class:`Figure` carries the
environment that was **measured** from the connected account, the provenance kind
that decides whether that environment admits it, and, for a quote, the
subscription state and tick delay status the observation was taken under.

Bundling them is the point. A bare float can be passed to a gate and the gate has
no way to ask where it came from. A :class:`Figure` cannot be built without
answering, and :mod:`mbt.gates` refuses on the answer.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, unique
from typing import final

from mbt.clock import iso_utc, utc_now
from mbt.provenance import Environment, ProvenanceKind


@unique
class TickDelayStatus(StrEnum):
    """What the feed served. Mirrors the IBKR market data type codes.

    Only :attr:`REALTIME` is admissible. A delayed quote carries a stale and
    artificially wide spread, and widening a cost band from one measures the
    delay rather than the venue.
    """

    REALTIME = "realtime"
    """IBKR market data type 1. Live streaming ticks."""

    FROZEN = "frozen"
    """Type 2. The last known snapshot, not a live book."""

    DELAYED = "delayed"
    """Type 3. Delayed by the exchange's published interval."""

    DELAYED_FROZEN = "delayed_frozen"
    """Type 4. Both at once."""

    UNKNOWN = "unknown"
    """The session did not report a type. Never assumed to be realtime."""


#: The IBKR market data type codes, as returned by the API, mapped to the status
#: this repository records. Measured against ib_async 2.1.0 rather than assumed.
MARKET_DATA_TYPE_TO_STATUS = {
    1: TickDelayStatus.REALTIME,
    2: TickDelayStatus.FROZEN,
    3: TickDelayStatus.DELAYED,
    4: TickDelayStatus.DELAYED_FROZEN,
}


def status_from_market_data_type(code: int | None) -> TickDelayStatus:
    """Map an IBKR market data type code, defaulting to UNKNOWN rather than live."""
    if code is None:
        return TickDelayStatus.UNKNOWN
    return MARKET_DATA_TYPE_TO_STATUS.get(code, TickDelayStatus.UNKNOWN)


@final
@dataclass(frozen=True, slots=True)
class Figure:
    """One recorded number, with everything a gate needs to judge admissibility."""

    name: str
    value: float
    unit: str
    kind: ProvenanceKind
    environment: Environment
    recorded_at: str
    detail: str = ""
    tick_delay: TickDelayStatus = TickDelayStatus.UNKNOWN
    subscription_note: str = ""

    @classmethod
    def record(
        cls,
        *,
        name: str,
        value: float,
        unit: str,
        kind: ProvenanceKind,
        environment: Environment,
        detail: str = "",
        tick_delay: TickDelayStatus = TickDelayStatus.UNKNOWN,
        subscription_note: str = "",
    ) -> Figure:
        """Record a figure, stamping it with the sanctioned clock."""
        return cls(
            name=name,
            value=value,
            unit=unit,
            kind=kind,
            environment=environment,
            recorded_at=iso_utc(utc_now(), "Figure.record"),
            detail=detail,
            tick_delay=tick_delay,
            subscription_note=subscription_note,
        )

    def as_row(self) -> dict[str, str | float]:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "kind": str(self.kind),
            "environment": str(self.environment),
            "recorded_at": self.recorded_at,
            "detail": self.detail,
            "tick_delay": str(self.tick_delay),
            "subscription_note": self.subscription_note,
        }
