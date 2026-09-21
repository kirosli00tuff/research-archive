"""Section 4 arithmetic. Pure functions over named values.

No payload, no path, no parser: the Stage B sealed reader (which does not
exist in Stage A) will hand this module plain numbers, and the A.3 synthetic
fixtures do the same. The sign convention is registered: a positive funding
rate pays the short.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from npl.census import EVENT_HIP3
from npl.config import CONFIG, Config


@dataclass(frozen=True, slots=True)
class NetDecomposition:
    """The H8 decomposition: every net splits into its price and funding terms."""

    price_term: float
    funding_term: float
    cost_term: float

    def net(self) -> float:
        return self.price_term + self.funding_term - self.cost_term


def cost_round_trip_bp(event_type: str, cfg: Config = CONFIG, band: str = "central") -> float:
    """The registered round-trip cost for an event class (Section 5)."""
    low, central, high = (
        cfg.hip3_round_trip_bp if event_type == EVENT_HIP3 else cfg.vanilla_round_trip_bp
    )
    by_band = {"low": low, "central": central, "high": high}
    if band not in by_band:
        raise ValueError(f"unregistered cost band {band!r}")
    return by_band[band]


def net_short_decomposition(
    entry_close: float,
    exit_close: float,
    hourly_funding_rates: Iterable[float],
    round_trip_bp: float,
) -> NetDecomposition:
    """net_short(H) = -price_return + sum(funding) - cost, constant notional.

    Constant notional, no compounding, no liquidation modelling — the three
    registered Stage-scope simplifications.
    """
    if entry_close <= 0.0 or exit_close < 0.0:
        raise ValueError(
            f"prices must be positive (entry {entry_close!r}, exit {exit_close!r}); "
            f"a dead instrument is truncated at its last served close, never zero-priced"
        )
    price_return = exit_close / entry_close - 1.0
    funding_sum = float(sum(hourly_funding_rates))
    return NetDecomposition(
        price_term=-price_return,
        funding_term=funding_sum,
        cost_term=round_trip_bp / 1e4,
    )


def net_short_return(
    entry_close: float,
    exit_close: float,
    hourly_funding_rates: Iterable[float],
    round_trip_bp: float,
) -> float:
    return net_short_decomposition(
        entry_close, exit_close, hourly_funding_rates, round_trip_bp
    ).net()
