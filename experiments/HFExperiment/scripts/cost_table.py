"""Emit the docs/ACCESS.md cost arithmetic from the commission module.

One source of truth. The table in ACCESS.md is pasted from this output and
tests/test_commission.py pins the branch behaviour the table relies on.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from hfexperiment.commission import (
    FIXED,
    TIERED,
    commission,
    crossover_notional_usd,
    fractional_commission,
    sell_leg_regulatory,
)
from hfexperiment.config import CONFIG

NOTIONALS = (30.0, 45.0, 70.0, 100.0, 180.0)
# A representative share price for the share-count inputs. TAF and per-share
# rates barely move with it. The measured median book price replaces it in
# the A.2 cost model.
ASSUMED_SHARE_PRICE = 45.0


def bp(amount: float, value: float) -> float:
    return amount / value * 10_000


def main() -> None:
    print("| notional | plan | commission/side | binds | reg drag sell side "
          "| round trip |")
    print("|---|---|---|---|---|---|")
    for value in NOTIONALS:
        shares = value / ASSUMED_SHARE_PRICE
        for plan in (TIERED, FIXED):
            c = commission(plan, shares, value)
            reg = sell_leg_regulatory(shares, value)
            round_trip = 2 * c.amount_usd + reg.total_usd
            print(
                f"| {value:.0f} | {plan.name} "
                f"| {c.amount_usd:.4f} ({bp(c.amount_usd, value):.1f} bp) "
                f"| {c.binding} "
                f"| {reg.total_usd:.4f} ({bp(reg.total_usd, value):.2f} bp) "
                f"| {round_trip:.4f} ({bp(round_trip, value):.1f} bp) |"
            )
        frac = fractional_commission(value)
        reg = sell_leg_regulatory(value / ASSUMED_SHARE_PRICE, value)
        round_trip = 2 * frac + reg.total_usd
        print(
            f"| {value:.0f} | fractional "
            f"| {frac:.4f} ({bp(frac, value):.1f} bp) | 1pct floor "
            f"| {reg.total_usd:.4f} ({bp(reg.total_usd, value):.2f} bp) "
            f"| {round_trip:.4f} ({bp(round_trip, value):.1f} bp) |"
        )
    print()
    print(f"Tiered crossover: {crossover_notional_usd(TIERED):.0f} USD")
    print(f"Fixed crossover: {crossover_notional_usd(FIXED):.0f} USD")
    print()
    settled_configuration()


def settled_configuration() -> None:
    """The settled book, priced both ways for one full-turnover month."""
    value = CONFIG.per_name_notional_usd
    plan = TIERED if CONFIG.plan_name == "tiered" else FIXED
    shares = value / ASSUMED_SHARE_PRICE
    whole = commission(plan, shares, value).amount_usd
    frac = fractional_commission(value)
    reg = sell_leg_regulatory(shares, value).total_usd
    n = CONFIG.book_width
    print(f"Settled book: {n} names at {value:.0f} USD "
          f"({CONFIG.deployed_usd:.0f} deployed, {CONFIG.buffer_usd:.0f} "
          f"buffer, {CONFIG.total_usd:.0f} total), plan {plan.name}.")
    print(f"Full-turnover month, whole-share billing: "
          f"{n * (2 * whole + reg):.2f} USD")
    print(f"Full-turnover month, fractional billing: "
          f"{n * (2 * frac + reg):.2f} USD")


if __name__ == "__main__":
    main()
