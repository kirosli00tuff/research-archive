"""Section 6: the registered cost bands, and the venue that carries none."""

from __future__ import annotations

import pytest

from etf.costs import hyperliquid_band, ibkr_band, kraken_spot_round_trip_bp


def test_the_hyperliquid_band_is_three_nine_eighteen_bp() -> None:
    band = hyperliquid_band()
    assert (band.low_bp, band.central_bp, band.high_bp) == (3.0, 9.0, 18.0)


def test_the_central_case_is_taker_both_legs_not_the_optimistic_end() -> None:
    """9 bp = 4.5 bp taker per side. The 3 bp end is maker both legs."""
    band = hyperliquid_band()
    assert band.central_bp == 2 * 4.5
    assert band.low_bp == 2 * 1.5
    assert band.central_bp > band.low_bp


def test_the_band_converts_to_fractions_of_notional() -> None:
    assert hyperliquid_band().as_fractions() == pytest.approx((0.0003, 0.0009, 0.0018))


def test_kraken_spot_is_fifty_and_eighty_bp_round_trip() -> None:
    assert kraken_spot_round_trip_bp() == (50.0, 80.0)


def test_ibkr_carries_no_band_at_all() -> None:
    """Error 10243 closes the venue. A band would imply an implementation."""
    assert ibkr_band() is None
