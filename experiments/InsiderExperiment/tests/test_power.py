"""The power arithmetic, checked against hand-computed values."""

from __future__ import annotations

import math
import random

import pytest

from insider.config import CONFIG
from insider.power.dispersion import (
    CenteredSeries,
    CenteringBroken,
    DispersionStats,
    autocorrelation,
    sample_sd,
    summarize,
    variance_inflation,
)
from insider.power.mde import band_position, mde_from, standard_error_monthly


def centered(values: list[float], hold: int = 126) -> CenteredSeries:
    mean = sum(values) / len(values)
    shifted = [v - mean for v in values]
    return CenteredSeries(
        hold_sessions=hold,
        weighting="value_weighted",
        dates=tuple(f"d{i}" for i in range(len(values))),
        centered=tuple(shifted),
        book_width=tuple(50 for _ in values),
    )


def test_a_series_that_was_not_centered_is_refused() -> None:
    with pytest.raises(CenteringBroken, match="carries a first moment"):
        CenteredSeries(
            hold_sessions=126,
            weighting="value_weighted",
            dates=("a", "b", "c"),
            centered=(1.0, 1.0, 1.0),
            book_width=(5, 5, 5),
        )


def test_a_centered_series_is_accepted() -> None:
    series = centered([0.01, -0.02, 0.005, 0.001])
    assert abs(math.fsum(series.centered)) < 1e-12


def test_the_sample_sd_uses_n_minus_one() -> None:
    series = centered([1.0, 2.0, 3.0, 4.0])
    assert sample_sd(series.centered) == pytest.approx(math.sqrt(5.0 / 3.0))


def white_noise(n: int, seed: int = 20260825) -> list[float]:
    """Deterministic draws with no serial structure. A sinusoid is not one."""
    rng = random.Random(seed)
    return [rng.gauss(0.0, 1.0) for _ in range(n)]


def test_an_independent_series_has_a_variance_inflation_near_one() -> None:
    series = centered(white_noise(4000))
    assert variance_inflation(series.centered, 5) == pytest.approx(1.0, abs=0.25)


def test_a_positively_autocorrelated_series_inflates_the_variance() -> None:
    shocks = white_noise(4000, seed=11)
    values = [shocks[0]]
    for shock in shocks[1:]:
        values.append(0.8 * values[-1] + shock)
    series = centered(values)
    assert autocorrelation(series.centered, 1) > 0.5
    assert variance_inflation(series.centered, 21) > 2.0


def test_a_negatively_autocorrelated_series_deflates_it_and_that_is_reported() -> None:
    """A variance inflation below one is a real measurement, not an error."""
    shocks = white_noise(4000, seed=13)
    values = [shocks[0]]
    for shock in shocks[1:]:
        values.append(-0.6 * values[-1] + shock)
    series = centered(values)
    assert autocorrelation(series.centered, 1) < 0
    assert variance_inflation(series.centered, 21) < 1.0


def test_the_monthly_standard_error_scales_by_sessions_per_month() -> None:
    se = standard_error_monthly(0.006295, 2869.9)
    assert se == pytest.approx(CONFIG.sessions_per_month * 0.006295 / math.sqrt(2869.9))
    assert se * 10_000 == pytest.approx(24.68, abs=0.05)


def test_the_mde_is_the_critical_value_times_the_standard_error() -> None:
    stats = DispersionStats(
        hold_sessions=126,
        weighting="value_weighted",
        n_sessions=2581,
        sd_daily_excess=0.006295,
        annualized_tracking_error=0.09993,
        newey_west_lags=21,
        variance_inflation=0.899,
        effective_periods=2869.9,
        autocorr_lag_1=-0.01,
        autocorr_lag_5=0.0,
        autocorr_lag_21=0.0,
        book_width_mean=71.9,
        book_width_min=1,
        book_width_p10=46,
        book_width_p50=72,
        book_width_p90=89,
        book_width_max=120,
    )
    result = mde_from(stats)
    assert result.mde_bp_per_month == pytest.approx(49.35, abs=0.1)
    assert result.mde_bp_per_month == pytest.approx(
        CONFIG.t_critical * result.standard_error_monthly_bp
    )


def test_a_lower_tracking_error_lowers_the_mde() -> None:
    """The whole corpus-floor argument, checked rather than asserted."""
    noise = white_noise(2000)
    narrow = mde_from(summarize(centered([v * 0.02 for v in noise]), lags=5))
    wide = mde_from(summarize(centered([v * 0.005 for v in noise]), lags=5))
    assert wide.mde_bp_per_month < narrow.mde_bp_per_month
    assert wide.mde_bp_per_month == pytest.approx(narrow.mde_bp_per_month / 4.0, rel=1e-6)


def test_more_periods_lower_the_mde_by_the_square_root() -> None:
    noise = white_noise(8000, seed=5)
    short = mde_from(summarize(centered(noise[:500]), lags=5))
    long = mde_from(summarize(centered(noise[:8000]), lags=5))
    assert long.mde_bp_per_month < short.mde_bp_per_month
    assert long.mde_bp_per_month == pytest.approx(short.mde_bp_per_month / 4.0, rel=0.25)


def test_band_position_reports_where_the_mde_lands() -> None:
    assert "below" in band_position(10.0)
    assert "inside" in band_position(35.0)
    assert "above" in band_position(49.35)


def test_a_series_too_short_to_measure_raises_rather_than_guessing() -> None:
    with pytest.raises(ValueError):
        sample_sd((0.0,))
    with pytest.raises(ValueError):
        summarize(centered([0.01, -0.01]), lags=5).sd_daily_excess  # noqa: B018
