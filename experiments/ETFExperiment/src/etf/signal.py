"""Section 4: the signal and the position rule. It reads no return.

The signal is the admissible as-printed aggregate net flow in USD. The primary
position rule is symmetric: long one unit of BTC perp when the signal exceeds
+T, short one unit when it falls below -T, flat otherwise, entered at the
anchor and exited at the same clock time 24 hours later. T is registered at
100 million USD, matching the source study's unit.

Constant notional, no compounding, no leverage beyond one, no liquidation
modelling — each a named Stage-scope simplification (Section 4).
"""

from __future__ import annotations

from enum import IntEnum

from etf.absence import Absent
from etf.config import CONFIG


class Position(IntEnum):
    """One unit long, one unit short, or flat. Nothing else exists."""

    SHORT = -1
    FLAT = 0
    LONG = 1


def position(
    signal_usd: float | Absent, threshold_usd: float = CONFIG.signal_threshold_usd
) -> Position:
    """The Section 4 rule. An absent signal is FLAT and is counted, never guessed."""
    if isinstance(signal_usd, Absent):
        return Position.FLAT
    if signal_usd > threshold_usd:
        return Position.LONG
    if signal_usd < -threshold_usd:
        return Position.SHORT
    return Position.FLAT


def registered_universe() -> tuple[str, ...]:
    """The five largest US spot Bitcoin ETFs, named in Section 2 by ticker."""
    return CONFIG.flow_universe_tickers
