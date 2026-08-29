"""Section 6 — the cost model. Built here, frozen and hashed at A.2 TASK 2.

**The cost band is not a robustness check in this design; it is the
experiment's second axis.** The independent replication measured the sibling
index strategy's net PnL crossing zero at roughly **0.022 USD per share of
entry slippage**, against a QQQ spread near **0.010 USD** (carried, C-6). The
registered central entry assumption of **0.020 USD per share** sits **0.002 USD
below that measured break-even**.

Every component is a pure function of counts and prices, unit-tested against a
hand-computed example. **Nothing here reads a bar**: the caller supplies a fill
price and a share count, and both arrive from a sealed path after the Stage C
latch, never before.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from datetime import date
from enum import StrEnum, unique
from typing import final

from orb.absence import AbsenceReason, Absent, Maybe


@unique
class Leg(StrEnum):
    """The three fills a registered trade can have."""

    ENTRY = "entry"
    STOP_EXIT = "stop_exit"
    CLOSE_EXIT = "close_exit"


@unique
class Band(StrEnum):
    """Three-point slippage bands. OPTIMISTIC is an upper bound of optimism."""

    OPTIMISTIC = "optimistic"
    CENTRAL = "central"
    PESSIMISTIC = "pessimistic"


@unique
class Side(StrEnum):
    LONG = "long"
    SHORT = "short"


@final
@dataclass(frozen=True, slots=True)
class SecFeeSchedule:
    """The SEC Section 31 fee, **recorded per date, never a single constant**.

    Section 6 requires the rate *in force on the session date*. A schedule with
    a hole therefore returns :class:`Absent` rather than the nearest rate: a
    fee silently taken from the wrong year is a cost model that cannot be
    defended, and it would bias every net figure in one direction.
    """

    effective_dates: tuple[date, ...]
    rates_per_dollar: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.effective_dates) != len(self.rates_per_dollar):
            raise ValueError("effective_dates and rates_per_dollar differ in length")
        if list(self.effective_dates) != sorted(self.effective_dates):
            raise ValueError("effective_dates must be sorted ascending")

    def rate_on(self, session: date) -> Maybe[float]:
        """The rate in force on ``session``, or a recorded absence."""
        if not self.effective_dates or session < self.effective_dates[0]:
            return Absent(
                AbsenceReason.NOT_YET_MEASURED,
                f"no SEC Section 31 rate recorded in force on {session.isoformat()}",
            )
        index = bisect_right(self.effective_dates, session) - 1
        return self.rates_per_dollar[index]


@final
@dataclass(frozen=True, slots=True)
class CostModel:
    """Section 6, implemented exactly. Frozen and hashed once verified."""

    commission_per_share: float
    commission_order_minimum: float
    commission_max_fraction_of_trade_value: float
    finra_taf_per_share_sold: float
    finra_cat_per_share: float
    clearing_per_share: float
    sec_fees: SecFeeSchedule
    entry_slippage: tuple[float, float, float]
    stop_slippage: tuple[float, float, float]
    close_slippage: tuple[float, float, float]

    # --- Components, each unit-tested against a hand-computed example ---

    def commission(self, shares: int, fill_price: float) -> float:
        """Per-share, floored at the order minimum, capped at 1% of trade value.

        The cap is **measured**, not carried: IBKR publishes *Maximum per order
        1% of Trade Value* alongside the per-share rate, and the registration as
        first written did not model it. On a small, cheap order the cap binds
        **below** the 0.35 minimum, and the minimum does not survive it.
        """
        if shares <= 0:
            raise ValueError(f"share count must be positive, got {shares}")
        raw = shares * self.commission_per_share
        floored = max(raw, self.commission_order_minimum)
        cap = self.commission_max_fraction_of_trade_value * shares * fill_price
        return min(floored, cap)

    def finra_taf(self, shares_sold: int) -> float:
        """Charged on the **sell** leg only, per share."""
        return max(0, shares_sold) * self.finra_taf_per_share_sold

    def finra_cat(self, shares: int) -> float:
        """Consolidated Audit Trail, charged per share on **every** leg."""
        return max(0, shares) * self.finra_cat_per_share

    def clearing(self, shares: int) -> float:
        """NSCC/DTC pass-through, per share on **every** leg."""
        return max(0, shares) * self.clearing_per_share

    def sec_fee(self, shares_sold: int, price: float, session: date) -> Maybe[float]:
        """Charged on sells, on notional, at the rate in force on ``session``."""
        rate = self.sec_fees.rate_on(session)
        if isinstance(rate, Absent):
            return rate
        return max(0, shares_sold) * price * rate

    def slippage_per_share(self, leg: Leg, band: Band) -> float:
        """The registered per-leg figure. The stop band is widest by design."""
        table = {
            Leg.ENTRY: self.entry_slippage,
            Leg.STOP_EXIT: self.stop_slippage,
            Leg.CLOSE_EXIT: self.close_slippage,
        }[leg]
        return table[[Band.OPTIMISTIC, Band.CENTRAL, Band.PESSIMISTIC].index(band)]

    def slippage_shift_per_share(
        self, exit_leg: Leg, *, band_from: Band, band_to: Band
    ) -> float:
        """The per-share cost of moving both legs from one band to another.

        **Registered by Amendment 19**, which made the pessimistic end of the
        Section 6 band the null of E2. The shift is an **absolute dollar
        quantity per share**, charged on the **entry** leg and on **whichever
        exit leg the trade actually took** — so it depends on the realized
        stop-versus-close mix, which is a **measurement** (A.1 TASK 3 of the
        inference-repair pass) and not an assumption.

        At the registered bands, moving central to pessimistic costs
        **0.030 USD/share on a close exit** and **0.060 on a stop exit**:
        entry 0.020 to 0.040 is +0.020 on both, and the exit is 0.010 to 0.020
        on a close and 0.040 to 0.080 on a stop.
        """
        if exit_leg is Leg.ENTRY:
            raise ValueError("exit_leg must be a stop exit or a close exit")
        entry = self.slippage_per_share(Leg.ENTRY, band_to) - self.slippage_per_share(
            Leg.ENTRY, band_from
        )
        exit_ = self.slippage_per_share(exit_leg, band_to) - self.slippage_per_share(
            exit_leg, band_from
        )
        return entry + exit_

    def mean_slippage_shift_per_share(
        self, stop_exit_share: float, *, band_from: Band, band_to: Band
    ) -> float:
        """The shift averaged over a **measured** stop-versus-close exit mix.

        ``stop_exit_share`` is the share of triggered trades that exited on the
        stop. It is a measured figure and this method refuses a value outside
        ``[0, 1]`` rather than clamping one: a share above 1 is an arithmetic
        fault upstream, and clamping it would hide the fault inside a cost.
        """
        if not 0.0 <= stop_exit_share <= 1.0:
            raise ValueError(
                f"stop_exit_share must lie in [0, 1], got {stop_exit_share}"
            )
        stop = self.slippage_shift_per_share(
            Leg.STOP_EXIT, band_from=band_from, band_to=band_to
        )
        close = self.slippage_shift_per_share(
            Leg.CLOSE_EXIT, band_from=band_from, band_to=band_to
        )
        return stop_exit_share * stop + (1.0 - stop_exit_share) * close

    # --- The whole round trip -----------------------------------------

    def round_trip_cost(
        self,
        shares: int,
        entry_price: float,
        exit_price: float,
        exit_leg: Leg,
        side: Side,
        session: date,
        band: Band = Band.CENTRAL,
    ) -> Maybe[float]:
        """Total modeled cost of one registered trade, in USD.

        Slippage is charged **against** the trader on both legs regardless of
        side: a marketable order pays the spread going in and coming out.
        """
        if exit_leg is Leg.ENTRY:
            raise ValueError("exit_leg must be a stop exit or a close exit")

        sell_price = exit_price if side is Side.LONG else entry_price
        sec = self.sec_fee(shares, sell_price, session)
        if isinstance(sec, Absent):
            return sec

        commissions = self.commission(shares, entry_price) + self.commission(
            shares, exit_price
        )
        regulatory = self.finra_taf(shares) + sec + 2 * self.finra_cat(shares)
        clearing = 2 * self.clearing(shares)
        slippage = shares * (
            self.slippage_per_share(Leg.ENTRY, band)
            + self.slippage_per_share(exit_leg, band)
        )
        return commissions + regulatory + clearing + slippage

    def net_pnl(
        self,
        shares: int,
        entry_fill: float,
        exit_fill: float,
        exit_leg: Leg,
        side: Side,
        session: date,
        band: Band = Band.CENTRAL,
    ) -> Maybe[float]:
        """Section 5. **A positive number is a gain in both directions.**"""
        gross = (
            (exit_fill - entry_fill) if side is Side.LONG else (entry_fill - exit_fill)
        ) * shares
        cost = self.round_trip_cost(
            shares, entry_fill, exit_fill, exit_leg, side, session, band
        )
        if isinstance(cost, Absent):
            return cost
        return gross - cost
