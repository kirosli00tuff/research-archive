"""Opening a Gateway session, and refusing to record when it is not what it claims.

The connection sequence is fixed and its order matters:

1. connect on the configured host and port;
2. **read the account list back from the broker**;
3. build :class:`SessionProvenance` from the account that came back, which raises
   if the measured environment differs from the declared one;
4. only then may anything be recorded.

Step 3 raising before step 4 is what makes "a session declaring live that
connects to a D-prefixed account refuses and writes nothing" structural. The
recorder is never handed an object, so there is nothing for it to write.

An unreachable Gateway is a typed absence carrying its errno, not an exception
that stops the stage. The rest of the harness is built and tested against a stub
implementing :class:`Session`, so the code path is exercised without a broker.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, final

from mbt.absence import AbsenceReason, Absent, Maybe
from mbt.clock import iso_utc, utc_now
from mbt.config import GatewayConfig
from mbt.figures import TickDelayStatus, status_from_market_data_type
from mbt.provenance import SessionProvenance


class Session(Protocol):
    """The narrow broker slice this package uses. No transmitting method appears.

    Return types are widened to ``object`` where ``ib_async`` returns something
    this package does not read. ``IB.disconnect`` returns ``str | None``, which is
    not a subtype of ``None``, so declaring ``None`` here would make the real
    client fail to satisfy the protocol it is meant to describe.
    """

    def connect(self, host: str, port: int, clientId: int, timeout: float) -> object: ...
    def managedAccounts(self) -> list[str]: ...
    def reqMarketDataType(self, marketDataType: int) -> object: ...
    def disconnect(self) -> object: ...


@final
@dataclass(frozen=True, slots=True)
class ProbeResult:
    """What one probe learned. Every unanswerable field is a typed absence."""

    reachable: bool
    provenance: Maybe[SessionProvenance]
    accounts_returned: int
    handshake_seconds: Maybe[float]
    tick_delay: TickDelayStatus
    detail: str
    probed_at: str

    def as_row(self) -> dict[str, object]:
        handshake = (
            self.handshake_seconds.as_row()
            if isinstance(self.handshake_seconds, Absent)
            else self.handshake_seconds
        )
        return {
            "reachable": self.reachable,
            "provenance": self.provenance.as_row(),
            "accounts_returned": self.accounts_returned,
            "handshake_seconds": handshake,
            "tick_delay": str(self.tick_delay),
            "detail": self.detail,
            "probed_at": self.probed_at,
        }


def unreachable(detail: str) -> ProbeResult:
    """The result recorded when no Gateway answers. Never a retry loop."""
    return ProbeResult(
        reachable=False,
        provenance=Absent(AbsenceReason.GATEWAY_UNREACHABLE, detail),
        accounts_returned=0,
        handshake_seconds=Absent(AbsenceReason.GATEWAY_UNREACHABLE, detail),
        tick_delay=TickDelayStatus.UNKNOWN,
        detail=detail,
        probed_at=iso_utc(utc_now(), "session.unreachable"),
    )


def probe(session: Session, config: GatewayConfig, *, timeout: float = 10.0) -> ProbeResult:
    """Connect, read the account back, and build measured provenance.

    Raises :class:`EnvironmentMismatchError` from
    :meth:`SessionProvenance.from_connection` when the declared environment and
    the connected account disagree. The raise propagates rather than being caught
    and recorded, because a mismatched session must write nothing at all.
    """
    started = utc_now()
    try:
        session.connect(config.host, config.port, clientId=config.client_id, timeout=timeout)
    except OSError as exc:
        return unreachable(f"{type(exc).__name__}: {exc}")

    try:
        accounts = list(session.managedAccounts())
        elapsed = (utc_now() - started).total_seconds()
        if not accounts:
            return ProbeResult(
                reachable=True,
                provenance=Absent(
                    AbsenceReason.NOT_SERVED,
                    "the session connected and returned no managed account. An "
                    "environment tag derives from the account the session actually "
                    "connected to, so no account means no environment tag.",
                ),
                accounts_returned=0,
                handshake_seconds=elapsed,
                tick_delay=TickDelayStatus.UNKNOWN,
                detail="connected, zero managed accounts returned",
                probed_at=iso_utc(utc_now(), "session.probe"),
            )
        provenance = SessionProvenance.from_connection(
            declared=config.declared,
            connected_account=accounts[0],
            client_id=config.client_id,
            host=config.host,
            port=config.port,
        )
        return ProbeResult(
            reachable=True,
            provenance=provenance,
            accounts_returned=len(accounts),
            handshake_seconds=elapsed,
            tick_delay=TickDelayStatus.UNKNOWN,
            detail=f"connected; environment measured from the account prefix {provenance.account_prefix!r}",
            probed_at=iso_utc(utc_now(), "session.probe"),
        )
    finally:
        session.disconnect()


def request_realtime(session: Session) -> None:
    """Ask for live streaming ticks. Type 1 is the only admissible feed.

    Requesting it does not guarantee receiving it: IBKR downgrades to delayed
    when no subscription covers the instrument. The status is therefore recorded
    per observation from what actually arrived, never from what was requested.
    """
    session.reqMarketDataType(1)


def observed_tick_status(ticker: Any) -> TickDelayStatus:
    """Read the delay status off a ticker, defaulting to UNKNOWN, never to live."""
    return status_from_market_data_type(getattr(ticker, "marketDataType", None))
