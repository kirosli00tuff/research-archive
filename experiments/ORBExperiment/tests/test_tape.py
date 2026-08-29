"""A.1 TASK 4 — tape identification, with fixtures ON the registered boundaries.

The InsiderExperiment lesson governs this file: a fixture comfortably inside its
boundary lets a moved threshold pass unnoticed. Every threshold here is
exercised **at** the registered value and **one ULP across it**.
"""

from __future__ import annotations

import math

from orb.comparator import SealedComparator
from orb.config import CONFIG
from orb.integrity import TapeFinding, TapeVerdict


def _finding(median: float, *, below_share: float = 0.0, n: int = 100) -> TapeFinding:
    """A finding carrying one median. Every other field is a plausible count."""
    return TapeFinding(
        median_ratio=median,
        iqr_low_ratio=median,
        iqr_high_ratio=median,
        min_ratio=median,
        max_ratio=median,
        share_below_single_venue_threshold=below_share,
        session_ticker_pairs_compared=n,
        pairs_with_volume_in_both=n,
        pairs_with_volume_in_primary_only=0,
        pairs_with_volume_in_secondary_only=0,
        pairs_with_volume_in_neither=0,
    )


# --- the three verdicts, at their boundaries ------------------------------


def test_a_median_exactly_on_the_lower_same_tape_bar_is_same_tape() -> None:
    assert _finding(CONFIG.tape_same_min_ratio).verdict() is TapeVerdict.SAME_TAPE


def test_one_ulp_below_the_lower_same_tape_bar_is_ambiguous() -> None:
    just_below = math.nextafter(CONFIG.tape_same_min_ratio, 0.0)
    assert _finding(just_below).verdict() is TapeVerdict.AMBIGUOUS


def test_a_median_exactly_on_the_upper_same_tape_bar_is_same_tape() -> None:
    assert _finding(CONFIG.tape_same_max_ratio).verdict() is TapeVerdict.SAME_TAPE


def test_one_ulp_above_the_upper_same_tape_bar_is_ambiguous() -> None:
    just_above = math.nextafter(CONFIG.tape_same_max_ratio, 2.0)
    assert _finding(just_above).verdict() is TapeVerdict.AMBIGUOUS


def test_a_median_exactly_on_the_different_tape_bar_is_ambiguous_not_different() -> (
    None
):
    """The clause is *strictly* below 0.50. The boundary itself is not it."""
    assert _finding(CONFIG.tape_different_max_ratio).verdict() is TapeVerdict.AMBIGUOUS


def test_one_ulp_below_the_different_tape_bar_is_different_tape() -> None:
    just_below = math.nextafter(CONFIG.tape_different_max_ratio, 0.0)
    assert _finding(just_below).verdict() is TapeVerdict.DIFFERENT_TAPE


def test_only_same_tape_licenses_the_registered_agreement_thresholds() -> None:
    """A DIFFERENT_TAPE verdict must not let the 0.95 / 0.85 bars fire."""
    assert _finding(1.00).agreement_thresholds_apply() is True
    assert _finding(0.02).agreement_thresholds_apply() is False
    assert _finding(0.70).agreement_thresholds_apply() is False


def test_the_single_venue_share_reads_as_a_majority_not_a_presence() -> None:
    assert _finding(0.02, below_share=0.51).looks_like_a_single_venue_subset() is True
    assert _finding(0.02, below_share=0.50).looks_like_a_single_venue_subset() is False


# --- the comparator, against synthetic bars with known answers ------------

WINDOW = (1_000_000, 1_300_000)
"""A five-minute window in epoch milliseconds, half-open."""


def _bars(*rows: tuple[int, float]) -> list[dict[str, object]]:
    """Bars carrying a timestamp and a volume. Priced fields are irrelevant here."""
    return [{"t": stamp, "v": volume} for stamp, volume in rows]


def test_two_identical_feeds_measure_a_ratio_of_exactly_one() -> None:
    # Arrange
    primary = {"AAPL:1": _bars((1_000_000, 500.0), (1_060_000, 500.0))}
    secondary = {"AAPL:1": _bars((1_000_000, 500.0), (1_060_000, 500.0))}
    # Act
    finding = SealedComparator().compare_tapes(primary, secondary, {"AAPL:1": WINDOW})
    # Assert
    assert finding.median_ratio == 1.0
    assert finding.verdict() is TapeVerdict.SAME_TAPE
    assert finding.pairs_with_volume_in_both == 1


def test_a_single_venue_subset_measures_a_small_systematic_fraction() -> None:
    # Arrange — the secondary carries 1.5 percent of the primary's volume.
    primary = {f"T{i}:1": _bars((1_000_000, 100_000.0)) for i in range(20)}
    secondary = {f"T{i}:1": _bars((1_000_000, 1_500.0)) for i in range(20)}
    windows = {f"T{i}:1": WINDOW for i in range(20)}
    # Act
    finding = SealedComparator().compare_tapes(primary, secondary, windows)
    # Assert
    assert finding.median_ratio == 0.015
    assert finding.verdict() is TapeVerdict.DIFFERENT_TAPE
    assert finding.agreement_thresholds_apply() is False
    assert finding.share_below_single_venue_threshold == 1.0
    assert finding.looks_like_a_single_venue_subset() is True


def test_volume_outside_the_opening_range_window_is_not_counted() -> None:
    """The window is half-open: the end instant belongs to the next window."""
    # Arrange
    primary = {
        "AAPL:1": _bars((999_999, 9_999.0), (1_000_000, 100.0), (1_300_000, 9_999.0))
    }
    secondary = {"AAPL:1": _bars((1_000_000, 50.0), (1_300_000, 9_999.0))}
    # Act
    finding = SealedComparator().compare_tapes(primary, secondary, {"AAPL:1": WINDOW})
    # Assert — 50 / 100, with every out-of-window bar ignored on both sides.
    assert finding.median_ratio == 0.5
    assert finding.verdict() is TapeVerdict.AMBIGUOUS


def test_an_rfc3339_timestamp_is_normalised_to_epoch_milliseconds() -> None:
    """Massive serves epoch ms; Alpaca serves RFC 3339. Both must land."""
    # Arrange
    primary = {"AAPL:1": [{"t": 1_752_579_000_000, "v": 1_000.0}]}
    secondary = {"AAPL:1": [{"t": "2025-07-15T11:30:00Z", "v": 250.0}]}
    window = (1_752_579_000_000, 1_752_579_300_000)
    # Act
    finding = SealedComparator().compare_tapes(primary, secondary, {"AAPL:1": window})
    # Assert
    assert finding.pairs_with_volume_in_both == 1
    assert finding.median_ratio == 0.25


def test_a_naive_timestamp_is_refused_rather_than_assumed_utc() -> None:
    """Standing rule 14: never store a naive timestamp, never infer a zone."""
    # Arrange
    primary = {"AAPL:1": [{"t": 1_752_579_000_000, "v": 1_000.0}]}
    secondary = {"AAPL:1": [{"t": "2025-07-15T11:30:00", "v": 250.0}]}
    window = (1_752_579_000_000, 1_752_579_300_000)
    # Act
    finding = SealedComparator().compare_tapes(primary, secondary, {"AAPL:1": window})
    # Assert — the naive bar contributes nothing, so only the primary has volume.
    assert finding.pairs_with_volume_in_both == 0
    assert finding.pairs_with_volume_in_primary_only == 1


def test_a_pair_absent_from_both_feeds_is_counted_and_never_a_ratio() -> None:
    # Arrange
    finding = SealedComparator().compare_tapes(
        {"AAPL:1": _bars((1_000_000, 0.0))},
        {"AAPL:1": _bars((1_000_000, 0.0))},
        {"AAPL:1": WINDOW},
    )
    # Assert
    assert finding.pairs_with_volume_in_neither == 1
    assert finding.pairs_with_volume_in_both == 0
    assert finding.median_ratio == 0.0


def test_a_pair_with_no_registered_window_is_skipped_entirely() -> None:
    """A key with no opening-range window is not a zero-volume observation."""
    finding = SealedComparator().compare_tapes(
        {"AAPL:1": _bars((1_000_000, 5.0))},
        {"AAPL:1": _bars((1_000_000, 5.0))},
        {},
    )
    assert finding.session_ticker_pairs_compared == 1
    assert finding.pairs_with_volume_in_both == 0
    assert finding.pairs_with_volume_in_neither == 0


def test_the_interquartile_range_is_reported_with_its_n() -> None:
    # Arrange — ratios 0.1 … 1.0 in ten steps.
    primary = {f"T{i}:1": _bars((1_000_000, 100.0)) for i in range(10)}
    secondary = {f"T{i}:1": _bars((1_000_000, 10.0 * (i + 1))) for i in range(10)}
    windows = {f"T{i}:1": WINDOW for i in range(10)}
    # Act
    finding = SealedComparator().compare_tapes(primary, secondary, windows)
    # Assert
    assert finding.pairs_with_volume_in_both == 10
    assert math.isclose(finding.median_ratio, 0.55)
    assert math.isclose(finding.iqr_low_ratio, 0.325)
    assert math.isclose(finding.iqr_high_ratio, 0.775)
    assert math.isclose(finding.min_ratio, 0.1)
    assert math.isclose(finding.max_ratio, 1.0)


def test_an_empty_comparison_reports_zero_beside_an_n_of_zero() -> None:
    """A 0.0 median at n = 0 is legible as an absence, never as a measurement."""
    finding = SealedComparator().compare_tapes({}, {}, {})
    assert finding.session_ticker_pairs_compared == 0
    assert finding.pairs_with_volume_in_both == 0
    assert finding.median_ratio == 0.0
