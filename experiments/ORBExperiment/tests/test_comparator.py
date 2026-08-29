"""The sealed comparator, against synthetic fixtures with known answers."""

from __future__ import annotations

import json

from orb.comparator import SealedComparator
from orb.integrity import IntegrityVerdict


def bar(
    t: int, o: float, h: float, low: float, c: float, v: int = 1000
) -> dict[str, object]:
    return {"t": t, "o": o, "h": h, "l": low, "c": c, "v": v}


def raw(bars: list[dict[str, object]]) -> bytes:
    return json.dumps(bars, sort_keys=True).encode("utf-8")


MS = 60_000
BASE = 1_451_917_800_000  # 2016-01-04T14:30:00.000Z, the pre-period boundary


def five_minute_slice(offset: float = 0.0) -> list[dict[str, object]]:
    return [
        bar(
            BASE + i * MS, 10.00 + offset, 10.50 + offset, 9.50 + offset, 10.25 + offset
        )
        for i in range(5)
    ]


# --- A.1 TASK 3, bar revision ---------------------------------------------


def test_an_unchanged_re_pull_measures_zero_revision() -> None:
    bars = {"AAPL/2016-01-04": five_minute_slice()}
    payload = {k: raw(v) for k, v in bars.items()}
    finding = SealedComparator().compare_pulls(
        payload, payload, bars, bars, frozenset(), 14
    )
    assert finding.changed_bar_share == 0.0
    assert finding.bars_compared == 5
    assert finding.changed_bar_count == 0
    assert finding.verdict() is IntegrityVerdict.PASS
    assert finding.wait_satisfied()


def test_one_revised_bar_in_five_measures_exactly_one_fifth() -> None:
    """A known answer, hand-computed: 1 of 5 bars changed is 0.20."""
    first = {"AAPL/2016-01-04": five_minute_slice()}
    second_bars = five_minute_slice()
    second_bars[2] = bar(BASE + 2 * MS, 10.00, 10.51, 9.50, 10.25)  # high +1 cent
    second = {"AAPL/2016-01-04": second_bars}

    finding = SealedComparator().compare_pulls(
        {k: raw(v) for k, v in first.items()},
        {k: raw(v) for k, v in second.items()},
        first,
        second,
        frozenset(),
        14,
    )
    assert finding.changed_bar_count == 1
    assert finding.bars_compared == 5
    assert finding.changed_bar_share == 0.2
    assert finding.verdict() is IntegrityVerdict.FAIL


def test_a_dropped_bar_is_counted_as_a_bar_count_change() -> None:
    first = {"AAPL/2016-01-04": five_minute_slice()}
    second = {"AAPL/2016-01-04": five_minute_slice()[:4]}
    finding = SealedComparator().compare_pulls(
        {k: raw(v) for k, v in first.items()},
        {k: raw(v) for k, v in second.items()},
        first,
        second,
        frozenset(),
        14,
    )
    assert finding.pairs_with_changed_bar_count == 1
    assert finding.pairs_with_timestamp_change == 1


def test_a_revision_on_a_corporate_action_ticker_is_attributed() -> None:
    """The split is the event most likely to trigger a silent vendor rewrite."""
    key = "AAPL/2016-01-04"
    first = {key: five_minute_slice()}
    second = {key: five_minute_slice(offset=0.01)}
    finding = SealedComparator().compare_pulls(
        {k: raw(v) for k, v in first.items()},
        {k: raw(v) for k, v in second.items()},
        first,
        second,
        frozenset({key}),
        14,
    )
    assert finding.changes_coinciding_with_corporate_action == 1


def test_a_re_pull_taken_before_the_registered_wait_is_not_evidence() -> None:
    bars = {"AAPL/2016-01-04": five_minute_slice()}
    payload = {k: raw(v) for k, v in bars.items()}
    early = SealedComparator().compare_pulls(
        payload, payload, bars, bars, frozenset(), 13
    )
    assert early.changed_bar_share == 0.0
    assert not early.wait_satisfied()


# --- A.1 TASK 4, cross-vendor agreement -----------------------------------

WINDOW = {"AAPL/2016-01-04": (BASE, BASE + 5 * MS)}


def test_two_identical_vendors_agree_on_every_pair() -> None:
    slice_ = {"AAPL/2016-01-04": five_minute_slice()}
    finding = SealedComparator().compare_vendors(slice_, slice_, WINDOW, 250, 250)
    assert finding.first5_high_low_agreement_share == 1.0
    assert finding.session_ticker_pairs_compared == 1
    assert finding.bars_present_in_both == 5
    assert finding.bars_agreeing_to_the_cent == 5
    assert finding.verdict() is IntegrityVerdict.PASS


def test_a_one_cent_disagreement_inside_the_range_breaks_the_pair() -> None:
    """The only disagreement that changes an entry price."""
    primary = {"AAPL/2016-01-04": five_minute_slice()}
    secondary_bars = five_minute_slice()
    secondary_bars[1] = bar(BASE + MS, 10.00, 10.51, 9.50, 10.25)
    secondary = {"AAPL/2016-01-04": secondary_bars}

    finding = SealedComparator().compare_vendors(primary, secondary, WINDOW, 250, 250)
    assert finding.first5_high_low_agreement_share == 0.0
    assert finding.bars_agreeing_to_the_cent == 4


def test_a_disagreement_outside_the_opening_range_does_not_break_the_pair() -> None:
    """Only the first five minutes decide an entry price. The rest is noise here."""
    primary_bars = [*five_minute_slice(), bar(BASE + 90 * MS, 11.0, 11.5, 10.5, 11.2)]
    secondary_bars = [*five_minute_slice(), bar(BASE + 90 * MS, 11.0, 99.9, 10.5, 11.2)]
    finding = SealedComparator().compare_vendors(
        {"AAPL/2016-01-04": primary_bars},
        {"AAPL/2016-01-04": secondary_bars},
        WINDOW,
        250,
        250,
    )
    assert finding.first5_high_low_agreement_share == 1.0
    assert finding.bars_agreeing_to_the_cent == 5
    assert finding.bars_present_in_both == 6


def test_the_window_boundary_is_half_open() -> None:
    """A bar stamped exactly at 09:35:00.000 is outside the opening range."""
    inside = five_minute_slice()
    at_boundary = bar(BASE + 5 * MS, 10.0, 99.9, 9.5, 10.25)
    finding = SealedComparator().compare_vendors(
        {"AAPL/2016-01-04": [*inside, at_boundary]},
        {"AAPL/2016-01-04": [*inside, bar(BASE + 5 * MS, 10.0, 10.5, 9.5, 10.25)]},
        WINDOW,
        250,
        250,
    )
    assert finding.first5_high_low_agreement_share == 1.0


def test_delisted_coverage_is_carried_through_untouched() -> None:
    slice_ = {"AAPL/2016-01-04": five_minute_slice()}
    finding = SealedComparator().compare_vendors(slice_, slice_, WINDOW, 300, 19)
    assert finding.delisted_names_served == 300
    assert finding.delisted_names_with_intraday_history == 19
    assert finding.delisted_verdict() is IntegrityVerdict.FAIL
    assert finding.verdict() is IntegrityVerdict.FAIL


def test_the_comparator_returns_no_bar_value_at_runtime() -> None:
    """Not just by annotation: the returned objects hold no price, in any field."""
    import dataclasses

    slice_ = {"AAPL/2016-01-04": five_minute_slice()}
    finding = SealedComparator().compare_vendors(slice_, slice_, WINDOW, 250, 250)
    values = [getattr(finding, f.name) for f in dataclasses.fields(finding)]
    assert all(isinstance(v, int | float) for v in values)
    # 10.50 is the fixture's opening-range high. It must appear nowhere.
    assert 10.50 not in values
    assert 1050 not in values
