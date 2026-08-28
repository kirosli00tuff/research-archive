"""Section 6: the registered cost bands. Fees are dated measurements, not constants.

The ADR-055 pattern from MLCryptoEngine: a fee schedule recorded once is a
dated measurement and is re-verified before any verdict-bearing use, with the
correction recorded and an explicit statement of which closures flip.

Hyperliquid central 9 bp round trip, taker both legs, band 3 / 9 / 18. The 3 bp
end is maker both legs and is reported as an upper-bound-of-optimism, never as
the central case, because a daily signal must fill.

Kraken spot at 50 bp maker and 80 bp taker round trip is reported beside every
economic figure to show the venue dependence, descriptive only. IBKR carries no
band at all because error 10243 — the API refusing fractional-sized orders,
HFExperiment reports/stage_a1b/a1b_report.md line 52 — closes that venue, and a
band would imply an implementation that does not exist.
"""

from __future__ import annotations

from dataclasses import dataclass

from etf.config import CONFIG

BP = 1e-4


@dataclass(frozen=True, slots=True)
class CostBand:
    low_bp: float
    central_bp: float
    high_bp: float

    def as_fractions(self) -> tuple[float, float, float]:
        return (self.low_bp * BP, self.central_bp * BP, self.high_bp * BP)


def hyperliquid_band() -> CostBand:
    low, central, high = CONFIG.hyperliquid_round_trip_bp
    return CostBand(low_bp=low, central_bp=central, high_bp=high)


def kraken_spot_round_trip_bp() -> tuple[float, float]:
    """(maker round trip, taker round trip) in bp. Descriptive, never verdict-bearing."""
    return CONFIG.kraken_spot_round_trip_bp


def ibkr_band() -> CostBand | None:
    """There is no IBKR band. Error 10243 closes the venue; None is the honest value.

    HFExperiment reports/stage_a1b/a1b_report.md line 52: the API refuses
    fractional-sized orders with error 10243, so no equity-side implementation
    exists. A band here would imply one.
    """
    return None
