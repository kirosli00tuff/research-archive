"""Enumerating the live MBT chain and sampling one observation window.

This module is the bridge between the broker and the registered rules. It holds
no rule of its own: :mod:`mbt.chain` decides the expiry and the strike,
:mod:`mbt.quotes` decides whether a leg is admissible, and this module only
fetches what those need and hands it over.

**The expiry universe is every LISTED MBT option expiry, across every underlying
futures month.** Registered rule 3.3 says "the listed expiry minimising the
absolute distance from 30 days" and does not restrict the universe to one
underlying. Restricting it to the front future would be a narrowing invented
after seeing the chain, and it would be a consequential one: measured on
2026-09-03, the front future MBTU6 lists six expiries of which the longest is
22 days, so a front-future-only universe contains no expiry near the registered
30-day tenor at all, while the full listed chain contains one at 29 days.

**The settlement instant is read from the contract, never assumed.** Registered
rule 3.3 measures the tenor to the expiry's settlement instant rather than to
midnight, and ``ContractDetails`` carries ``lastTradeTime`` with the
``timeZoneId`` it is stated in. Measured on 2026-09-03: ``10:00:00`` in
``US/Central`` for both a weekly and a monthly MBT option.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, final
from zoneinfo import ZoneInfo

from mbt.absence import AbsenceReason, Absent, Maybe
from mbt.chain import ListedExpiry
from mbt.clock import require_utc

MBT_SYMBOL = "MBT"
MBT_EXCHANGE = "CME"

#: The settlement rule this repository records alongside every expiry it
#: resolves, so a reader can see which instant the tenor was measured to.
SETTLEMENT_RULE = "ContractDetails.lastTradeTime read in ContractDetails.timeZoneId"


@final
@dataclass(frozen=True, slots=True)
class ListedSeries:
    """One listed expiry with the strikes and trading class it was listed under."""

    expiry: ListedExpiry
    trading_class: str
    underlying_local_symbol: str
    strikes: tuple[float, ...]

    def as_row(self) -> dict[str, object]:
        return {
            "expiry": self.expiry.as_row(),
            "trading_class": self.trading_class,
            "underlying": self.underlying_local_symbol,
            "strikes_listed": len(self.strikes),
        }


def settlement_instant(expiry_yyyymmdd: str, last_trade_time: str, tz_id: str) -> Maybe[datetime]:
    """Combine the expiry date, the last trade time and the venue timezone.

    Returns an absence rather than guessing when any part is missing. A tenor
    measured to a guessed instant is a tenor measured to midnight by another
    name, which is the failure registered rule 3.3 exists to prevent.
    """
    if not (expiry_yyyymmdd and last_trade_time and tz_id):
        return Absent(
            AbsenceReason.NOT_SERVED,
            f"the contract served expiry={expiry_yyyymmdd!r} "
            f"last_trade_time={last_trade_time!r} timezone={tz_id!r}. The tenor is "
            "measured to the settlement instant, so an incomplete instant is "
            "recorded absent rather than rounded to midnight.",
        )
    try:
        naive = datetime.strptime(f"{expiry_yyyymmdd} {last_trade_time}", "%Y%m%d %H:%M:%S")
        local = naive.replace(tzinfo=ZoneInfo(tz_id))
    except (ValueError, KeyError) as exc:
        return Absent(
            AbsenceReason.NOT_SERVED,
            f"could not build a settlement instant from {expiry_yyyymmdd!r} "
            f"{last_trade_time!r} {tz_id!r}: {type(exc).__name__}: {exc}",
        )
    from datetime import UTC

    return local.astimezone(UTC)


def front_future(broker: Any) -> Maybe[Any]:
    """The nearest-dated listed MBT future. The registered ATM reference leg."""
    from ib_async import Future

    details = broker.reqContractDetails(Future(symbol=MBT_SYMBOL, exchange=MBT_EXCHANGE))
    if not details:
        return Absent(
            AbsenceReason.NOT_SERVED,
            "the broker listed no MBT future, so there is no front future and no "
            "at-the-money reference. The straddle is refused rather than resolved "
            "against a substitute reference.",
        )
    ordered = sorted(details, key=lambda d: d.contract.lastTradeDateOrContractMonth)
    return ordered[0].contract


def enumerate_series(broker: Any, at: datetime, *, max_underlyings: int = 4) -> list[ListedSeries]:
    """Every listed MBT option series, across underlying futures months.

    ``max_underlyings`` bounds the enumeration rather than selecting within it:
    the registered rule targets a 30-day tenor, and months beyond the first few
    cannot be nearest to 30 days while nearer ones are listed. It is a bound on
    work, not a filter on the rule's candidate set.
    """
    from ib_async import Future, FuturesOption

    require_utc(at, "enumerate_series(at)")
    futures = sorted(
        broker.reqContractDetails(Future(symbol=MBT_SYMBOL, exchange=MBT_EXCHANGE)),
        key=lambda d: d.contract.lastTradeDateOrContractMonth,
    )[:max_underlyings]

    series: list[ListedSeries] = []
    for detail in futures:
        underlying = detail.contract
        for params in broker.reqSecDefOptParams(MBT_SYMBOL, MBT_EXCHANGE, "FUT", underlying.conId):
            for expiry_text in sorted(params.expirations):
                sample = broker.reqContractDetails(
                    FuturesOption(
                        symbol=MBT_SYMBOL,
                        lastTradeDateOrContractMonth=expiry_text,
                        exchange=MBT_EXCHANGE,
                        tradingClass=params.tradingClass,
                    )
                )
                if not sample:
                    continue
                first = sample[0]
                instant = settlement_instant(
                    expiry_text,
                    str(getattr(first, "lastTradeTime", "") or ""),
                    str(getattr(first, "timeZoneId", "") or ""),
                )
                if isinstance(instant, Absent):
                    continue
                series.append(
                    ListedSeries(
                        expiry=ListedExpiry(
                            label=f"{params.tradingClass}:{expiry_text}",
                            settlement=instant,
                            exchange=MBT_EXCHANGE,
                            settlement_rule=SETTLEMENT_RULE,
                        ),
                        trading_class=params.tradingClass,
                        underlying_local_symbol=underlying.localSymbol,
                        strikes=tuple(sorted(params.strikes)),
                    )
                )
    return series
