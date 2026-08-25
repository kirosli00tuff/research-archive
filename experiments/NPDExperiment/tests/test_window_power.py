"""The window is derived, never assumed. The power number comes from it."""

from __future__ import annotations

import datetime as dt

import pytest

from npd.config import CONFIG
from npd.power import (
    band_coverage,
    contrast_grid,
    detection_mde,
    effective_days,
    null_ic_sd,
    overlap_vif,
    registered_floor_mde,
)
from npd.window import derive_window, guard_band_end


def _calendar(start: dt.date, days: int) -> list[dt.date]:
    out: list[dt.date] = []
    d = start
    while len(out) < days:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def test_the_guard_band_is_one_calendar_month_past_the_cutoff() -> None:
    assert guard_band_end(dt.date(2024, 9, 30), 1) == dt.date(2024, 10, 30)


def test_the_window_starts_strictly_after_the_guard_band() -> None:
    cal = _calendar(dt.date(2024, 1, 1), 900)
    cal = [d for d in cal if d <= CONFIG.window_end]
    w = derive_window(cal)
    assert w.start > w.guard_band_end
    assert w.end <= CONFIG.window_end
    assert all(d > w.guard_band_end for d in w.sessions)


def test_a_calendar_that_misses_the_window_raises_rather_than_guessing() -> None:
    cal = _calendar(dt.date(2020, 1, 1), 50)
    with pytest.raises(ValueError, match="does not cover"):
        derive_window(cal)


def test_sessions_must_be_ascending_and_unique() -> None:
    cal = _calendar(dt.date(2025, 1, 1), 10)
    with pytest.raises(ValueError):
        derive_window(list(reversed(cal)))


def test_evaluable_days_drop_the_tail_the_horizon_cannot_reach() -> None:
    cal = _calendar(dt.date(2024, 11, 1), 300)
    cal = [d for d in cal if d <= CONFIG.window_end]
    w = derive_window(cal)
    assert w.evaluable_days(5) == w.n_days - 5
    assert w.evaluable_days(1) == w.n_days - 1


def test_null_ic_sd_at_the_registered_panel_size() -> None:
    assert null_ic_sd(30) == pytest.approx(0.185695, abs=1e-6)
    with pytest.raises(ValueError):
        null_ic_sd(2)


def test_a_one_session_horizon_overlaps_nothing() -> None:
    assert overlap_vif(1) == 1.0
    assert effective_days(400, 1) == 400.0


def test_a_five_session_horizon_inflates_variance_by_the_registered_factor() -> None:
    assert overlap_vif(5) == pytest.approx(3.4, abs=1e-9)
    assert effective_days(427, 5) == pytest.approx(125.588, abs=1e-3)


def test_the_registered_floor_is_met_by_the_derived_window() -> None:
    mde = registered_floor_mde(432, CONFIG.panel_size, CONFIG.t_critical)
    assert mde == pytest.approx(0.01787, abs=1e-5)
    assert mde <= 0.025, "the window no longer clears the registered power floor"


def test_the_contrast_grid_spans_the_registered_correlations() -> None:
    grid = contrast_grid(427, CONFIG.panel_size, 5, CONFIG.t_critical)
    assert [c.corr_model_baseline for c in grid] == [0.0, 0.3, 0.5, 0.7]
    assert grid[0].detect > grid[-1].detect, "a higher correlation must detect more"
    assert all(c.powered_80 > c.detect for c in grid)


def test_band_coverage_states_where_the_design_sits() -> None:
    low, high = CONFIG.realistic_effect_band
    assert "whole registered band" in band_coverage(low / 2)
    assert "upper part" in band_coverage((low + high) / 2)
    assert "Large effects only" in band_coverage(high * 2)


def test_detection_needs_a_positive_effective_sample() -> None:
    with pytest.raises(ValueError):
        detection_mde(0.2, 0.0, 2.0)
