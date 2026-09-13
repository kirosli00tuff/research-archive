"""Task 1 of Stage B.1 — measure what Stage B could not, and record the reversal.

Stage B recorded five things ``Absent(gateway_unreachable)`` because no listener
answered. A listener now answers, so each becomes measurable, and this module
measures them rather than assuming the reversal is total. **A TCP connect proves
a listener, not a session; a session proves a handshake, not a subscription; and
a subscription request proves neither.** Each is measured separately here
because each failed separately.

**The what-if wait is bounded.** Measured on 2026-09-03, IBKR answers a what-if
it refuses to validate with error 321 and then never resolves the request, so an
unbounded wait hangs the command rather than recording a refusal. A bounded wait
turns that into a typed absence carrying the elapsed time, which is a
measurement. Waiting forever is not.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any, final

from mbt.absence import AbsenceReason, Absent, Maybe
from mbt.broker import MarginPreview, build_short_option_order, what_if_order
from mbt.clock import iso_utc, utc_now
from mbt.figures import TickDelayStatus
from mbt.marketdata import TickerReader
from mbt.quotes import Quote, screen

#: How long a what-if preview is given to answer before its absence is recorded.
#: IBKR answered every VALIDATED what-if in 0.24 to 0.26 s over n = 7 previews on
#: 2026-09-03, so a request still silent after this long is not slow, it is one
#: the venue declined to process.
WHAT_IF_TIMEOUT_SECONDS = 20.0

#: How long a market-data subscription is given to deliver a touch. Delayed ticks
#: arrived within 2 s over n = 3 legs on 2026-09-03.
MARKET_DATA_TIMEOUT_SECONDS = 8.0


@final
class BoundedWhatIfBroker:
    """Adapts an ``IB`` client to :class:`mbt.broker.WhatIfBroker` with a timeout.

    The package's own preview path is exercised through this, unchanged, so the
    thing being measured is the code path that would read MBT and not a
    reimplementation of it that happens to work.
    """

    __slots__ = ("_ib", "_timeout", "last_elapsed", "last_timed_out")

    def __init__(self, ib: Any, timeout: float = WHAT_IF_TIMEOUT_SECONDS) -> None:
        self._ib = ib
        self._timeout = timeout
        self.last_elapsed = 0.0
        self.last_timed_out = False

    def whatIfOrder(self, contract: Any, order: Any) -> Any:
        started = time.perf_counter()
        self.last_timed_out = False
        try:
            state = self._ib.run(
                asyncio.wait_for(self._ib.whatIfOrderAsync(contract, order), self._timeout)
            )
        except TimeoutError:
            self.last_elapsed = time.perf_counter() - started
            self.last_timed_out = True
            return _EmptyOrderState()
        self.last_elapsed = time.perf_counter() - started
        return state if not isinstance(state, list) else _EmptyOrderState()


@final
class _EmptyOrderState:
    """What a declined what-if yields: every field absent, none invented."""


@final
@dataclass(frozen=True, slots=True)
class PermissionProbe:
    """Whether the account may price a short MBT option, measured by preview."""

    permitted: Maybe[bool]
    preview: MarginPreview | None
    elapsed_seconds: float
    timed_out: bool
    broker_errors: list[str]
    detail: str

    def as_row(self) -> dict[str, object]:
        return {
            "permitted": self.permitted.as_row()
            if isinstance(self.permitted, Absent)
            else self.permitted,
            "preview": self.preview.as_row() if self.preview is not None else None,
            "elapsed_seconds": round(self.elapsed_seconds, 4),
            "timed_out": self.timed_out,
            "broker_errors": self.broker_errors,
            "detail": self.detail,
        }


def probe_permission(
    broker: BoundedWhatIfBroker, contract: Any, errors: list[str]
) -> PermissionProbe:
    """Price a short MBT option through the package's own preview path.

    A returned margin proves the account may price the instrument. A declined
    request proves nothing about permission on its own, which is why the
    distinction between ``Absent(permission_unknown)`` and a measured absence of
    permission is kept rather than collapsed.
    """
    before = len(errors)
    order = build_short_option_order(quantity=1)
    preview = what_if_order(broker, contract, order, whatIf=True)
    raised = errors[before:]

    if broker.last_timed_out or not preview.init_margin_change.strip():
        return PermissionProbe(
            permitted=Absent(
                AbsenceReason.PERMISSION_UNKNOWN,
                "the venue returned no OrderState for a what-if built by this "
                "package, so nothing was learned about permission. An unanswered "
                "request is not a refused one, and the two are never merged: one "
                "says the account may not, the other says nobody asked.",
            ),
            preview=None,
            elapsed_seconds=broker.last_elapsed,
            timed_out=broker.last_timed_out,
            broker_errors=raised,
            detail=(
                f"no OrderState after {broker.last_elapsed:.2f} s. Broker errors "
                f"raised during the request: {raised or 'none'}"
            ),
        )
    return PermissionProbe(
        permitted=True,
        preview=preview,
        elapsed_seconds=broker.last_elapsed,
        timed_out=False,
        broker_errors=raised,
        detail=(
            "the venue returned an initial margin for a short MBT option, so the "
            "account may price the instrument. This measures PERMISSION only; the "
            "margin itself is a paper figure and is inadmissible to the MARGIN gate."
        ),
    )


def sample_leg(
    ib: Any,
    contract: Any,
    leg: str,
    *,
    subscription_note: str,
    timeout: float = MARKET_DATA_TIMEOUT_SECONDS,
) -> tuple[Maybe[Quote], Maybe[Quote]]:
    """Subscribe, wait for a touch, and return the raw quote and its screening.

    Returns both so the artifact can show what arrived alongside what the
    registered refusal conditions did with it. Recording only the verdict would
    hide whether a leg was refused because nothing arrived or because what
    arrived was inadmissible, and those are different facts about the venue.
    """
    ticker = ib.reqMktData(contract, "", False, False)
    deadline = time.perf_counter() + timeout
    try:
        while time.perf_counter() < deadline:
            ib.sleep(0.25)
            bid, ask = getattr(ticker, "bid", None), getattr(ticker, "ask", None)
            if bid == bid and ask == ask and bid is not None and ask is not None:
                break
        raw = TickerReader(leg, subscription_note).read(ticker, utc_now())
    finally:
        ib.cancelMktData(contract)
    if isinstance(raw, Absent):
        return raw, raw
    return raw, screen(raw)


def requested_status(code: int) -> TickDelayStatus:
    """What a market-data type code was ASKED for. Never what was served."""
    from mbt.figures import status_from_market_data_type

    return status_from_market_data_type(code)


def stamp() -> str:
    """One sanctioned clock read for an artifact."""
    return iso_utc(utc_now(), "probe.stamp")


@final
@dataclass(frozen=True, slots=True)
class FeedObservation:
    """What one leg's feed served under one requested market-data type."""

    leg: str
    requested: str
    served: str
    raw: Maybe[Quote]
    screened: Maybe[Quote]

    def as_row(self) -> dict[str, object]:
        return {
            "leg": self.leg,
            "requested_market_data_type": self.requested,
            "served_tick_delay_status": self.served,
            "raw": self.raw.as_row(),
            "admissible": not isinstance(self.screened, Absent),
            "screening": self.screened.as_row()
            if isinstance(self.screened, Absent)
            else "ACCEPTED by every registered refusal condition",
        }


def observe_feed(ib: Any, legs: dict[str, Any], market_data_type: int) -> list[FeedObservation]:
    """Ask for one market-data type and record what each leg actually served.

    Both the request and the answer are recorded. Requesting real-time does not
    grant it, and the gap between the two is the fact worth having.
    """
    ib.reqMarketDataType(market_data_type)
    note = (
        f"reqMarketDataType({market_data_type}) was REQUESTED. The status recorded "
        "per leg is what the feed served, which is not the same thing."
    )
    observations: list[FeedObservation] = []
    for leg, contract in legs.items():
        raw, screened = sample_leg(ib, contract, leg, subscription_note=note)
        served = (
            str(raw.tick_delay) if not isinstance(raw, Absent) else str(TickDelayStatus.UNKNOWN)
        )
        observations.append(
            FeedObservation(
                leg=leg,
                requested=str(requested_status(market_data_type)),
                served=served,
                raw=raw,
                screened=screened,
            )
        )
    return observations
