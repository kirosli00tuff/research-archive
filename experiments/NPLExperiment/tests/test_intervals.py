"""Union before summing, with the mandatory overlapping pair."""

from __future__ import annotations

import pytest

from npl.intervals import merge_windows, total_covered_ms


def test_overlapping_windows_are_unioned_before_summing() -> None:
    # Two 10ms windows overlapping by 5ms cover 15ms, not 20.
    assert total_covered_ms([(0, 10), (5, 15)]) == 15


def test_touching_windows_merge() -> None:
    assert merge_windows([(0, 10), (10, 20)]) == [(0, 20)]


def test_disjoint_windows_stay_apart() -> None:
    assert merge_windows([(20, 30), (0, 10)]) == [(0, 10), (20, 30)]


def test_a_contained_window_adds_nothing() -> None:
    assert total_covered_ms([(0, 100), (10, 20)]) == 100


def test_an_inverted_window_raises_rather_than_vanishing() -> None:
    with pytest.raises(ValueError, match="inverted"):
        merge_windows([(10, 0)])


def test_empty_input_is_zero() -> None:
    assert total_covered_ms([]) == 0
