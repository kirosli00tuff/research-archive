"""The census admits, excludes and counts. It never imputes."""

from __future__ import annotations

from datetime import UTC, date, datetime

from etf.absence import DASH_IN_CELL
from etf.archive import Memento, qualifying_window
from etf.callstate import (
    OPERATIONAL_HEALTH_STATES,
    SAMPLE_COMPOSITION_STATES,
    CallState,
)
from etf.census import AdmissibilitySource, build_census
from etf.flow import FlowCell
from etf.snapshot import DayRow

OOS = date(2025, 5, 1)
CENSUS = date(2025, 5, 10)
D = date(2025, 5, 5)


def day(d: date, signal: float | None) -> DayRow:
    return DayRow(
        trade_date=d,
        per_fund=(
            FlowCell(ticker="IBIT", value_usd=signal if signal is not None else DASH_IN_CELL),
        ),
        signal_usd=signal if signal is not None else DASH_IN_CELL,
        total_printed_usd=DASH_IN_CELL,
    )


def windows(*days: date) -> dict[date, tuple[datetime, datetime]]:
    return {d: qualifying_window(d) for d in days}


def test_an_archive_capture_inside_the_window_admits_the_day() -> None:
    rows = build_census(
        [day(D, 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[Memento(datetime(2025, 5, 5, 23, tzinfo=UTC), "u")],
        forward_captures={},
        revised_days=frozenset(),
    )
    assert rows[0].admissible
    assert rows[0].source == AdmissibilitySource.RETRO_ARCHIVE
    assert rows[0].state is CallState.STORED


def test_the_capture_taken_is_the_last_before_the_anchor_not_the_first() -> None:
    """The registered rule reads the value standing at the anchor."""
    rows = build_census(
        [day(D, 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[
            Memento(datetime(2025, 5, 5, 21, tzinfo=UTC), "early"),
            Memento(datetime(2025, 5, 6, 7, tzinfo=UTC), "late"),
        ],
        forward_captures={},
        revised_days=frozenset(),
    )
    assert rows[0].capture_timestamp == datetime(2025, 5, 6, 7, tzinfo=UTC)


def test_a_capture_at_or_after_the_anchor_excludes_as_capture_too_late() -> None:
    rows = build_census(
        [day(D, 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[Memento(datetime(2025, 5, 6, 8, tzinfo=UTC), "u")],
        forward_captures={},
        revised_days=frozenset(),
    )
    assert not rows[0].admissible
    assert rows[0].exclusion_reason == "capture_too_late"
    assert rows[0].state is CallState.EXCLUDED_INELIGIBLE


def test_no_capture_at_all_excludes_as_no_capture_and_the_two_never_merge() -> None:
    rows = build_census(
        [day(D, 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[],
        forward_captures={},
        revised_days=frozenset(),
    )
    assert rows[0].exclusion_reason == "no_capture"


def test_a_day_with_no_printed_value_is_excluded_before_any_capture_test() -> None:
    rows = build_census(
        [day(D, None)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[Memento(datetime(2025, 5, 5, 23, tzinfo=UTC), "u")],
        forward_captures={},
        revised_days=frozenset(),
    )
    assert not rows[0].admissible
    assert rows[0].exclusion_reason == "no_printed_value"
    assert not rows[0].printed_signal_present


def test_a_forward_capture_wins_over_an_archive_one() -> None:
    rows = build_census(
        [day(D, 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[Memento(datetime(2025, 5, 5, 23, tzinfo=UTC), "u")],
        forward_captures={D: datetime(2025, 5, 5, 22, tzinfo=UTC)},
        revised_days=frozenset(),
    )
    assert rows[0].source == AdmissibilitySource.FORWARD_CAPTURE


def test_the_revised_flag_is_carried_and_never_corrects_the_value() -> None:
    rows = build_census(
        [day(D, 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[Memento(datetime(2025, 5, 5, 23, tzinfo=UTC), "u")],
        forward_captures={},
        revised_days=frozenset({D}),
    )
    assert rows[0].revised


def test_days_outside_the_registered_window_are_not_censused() -> None:
    rows = build_census(
        [day(date(2025, 4, 30), 1.0), day(D, 1.0), day(date(2025, 6, 1), 1.0)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[],
        forward_captures={},
        revised_days=frozenset(),
    )
    assert [r.trade_date for r in rows] == [D]


def test_the_ledger_dict_carries_every_recorded_field() -> None:
    rows = build_census(
        [day(D, 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[Memento(datetime(2025, 5, 5, 23, tzinfo=UTC), "u")],
        forward_captures={},
        revised_days=frozenset(),
    )
    payload = rows[0].as_ledger_dict()
    assert set(payload) == {
        "trade_date",
        "admissible",
        "state",
        "source",
        "capture_timestamp",
        "revised",
        "exclusion_reason",
        "printed_signal_present",
    }
    assert payload["capture_timestamp"] == "2025-05-05T23:00:00Z"


def test_an_admissible_day_always_carries_the_capture_that_admitted_it() -> None:
    """The invariant that forbids substituting a live value for a missing capture.

    A day admitted with no capture timestamp is a day whose as-printed value
    can only have come from the source's current page, which Section 3 forbids
    absolutely: "a later value for the same day, however authoritative, is never
    substituted".
    """
    rows = build_census(
        [day(D, 150e6), day(date(2025, 5, 6), 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D, date(2025, 5, 6)),
        mementos=[Memento(datetime(2025, 5, 5, 23, tzinfo=UTC), "u")],
        forward_captures={},
        revised_days=frozenset(),
    )
    for row in rows:
        if row.admissible:
            assert row.capture_timestamp is not None, (
                f"{row.trade_date} was admitted with no capture; its value could only "
                "come from the live page, which Section 3 forbids"
            )
            assert row.source in {"retro_archive", "forward_capture"}
        else:
            assert row.capture_timestamp is None
            assert row.exclusion_reason is not None


def test_a_capture_that_served_no_value_is_excluded_with_its_own_reason() -> None:
    """Section 3 needs a capture that SERVES A VALUE, not merely a capture.

    Measured at A.1 Task 4: 23 of 34 parseable pre-anchor archive captures
    showed the day still dashed. A dash is not a value.
    """
    rows = build_census(
        [day(D, 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[Memento(datetime(2025, 5, 5, 23, tzinfo=UTC), "u")],
        forward_captures={},
        revised_days=frozenset(),
        archive_served_values=frozenset(),
    )
    assert not rows[0].admissible
    assert rows[0].exclusion_reason == "capture_served_no_value"
    assert rows[0].state is CallState.EXCLUDED_INELIGIBLE


def test_a_failed_archive_fetch_is_operational_and_never_an_exclusion() -> None:
    """A fetch fault must not masquerade as a narrowed cohort."""
    rows = build_census(
        [day(D, 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[Memento(datetime(2025, 5, 5, 23, tzinfo=UTC), "u")],
        forward_captures={},
        revised_days=frozenset(),
        archive_served_values=frozenset(),
        archive_fetch_failed=frozenset({D}),
    )
    assert rows[0].state is CallState.SOURCE_FAILED
    assert rows[0].state in OPERATIONAL_HEALTH_STATES
    assert rows[0].state not in SAMPLE_COMPOSITION_STATES
    assert rows[0].exclusion_reason == "archive_fetch_failed"


def test_the_capture_too_late_test_is_bounded_to_the_day_after_the_anchor() -> None:
    """An unbounded test would call every day too-late once one later memento existed."""
    rows = build_census(
        [day(D, 150e6)],
        oos_start=OOS,
        census_date=CENSUS,
        archive_windows=windows(D),
        mementos=[Memento(datetime(2026, 8, 1, 12, tzinfo=UTC), "much later")],
        forward_captures={},
        revised_days=frozenset(),
    )
    assert rows[0].exclusion_reason == "no_capture"
