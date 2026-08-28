"""Section 4: the symmetric position rule, with fixtures ON the 100M threshold."""

from __future__ import annotations

from etf.absence import DASH_IN_CELL
from etf.config import CONFIG
from etf.signal import Position, position, registered_universe

T = CONFIG.signal_threshold_usd


def test_the_registered_threshold_is_one_hundred_million_usd() -> None:
    assert T == 100_000_000.0


def test_a_signal_exactly_on_the_positive_threshold_is_flat() -> None:
    """Strictly greater than +T, and the fixture sits exactly on it."""
    assert position(T) is Position.FLAT
    assert position(T + 1.0) is Position.LONG


def test_a_signal_exactly_on_the_negative_threshold_is_flat() -> None:
    assert position(-T) is Position.FLAT
    assert position(-T - 1.0) is Position.SHORT


def test_an_absent_signal_is_flat_and_is_never_guessed() -> None:
    assert position(DASH_IN_CELL) is Position.FLAT


def test_the_universe_is_the_five_named_tickers() -> None:
    universe = registered_universe()
    assert len(universe) == 5
    assert universe == ("IBIT", "FBTC", "GBTC", "ARKB", "BITB")
