"""Amendment H5-2: the three-field listing rule, on its registered boundary."""

from __future__ import annotations

import pytest

from npl.absence import NOT_SERVED
from npl.h5.listing import (
    LISTING_STATUSES,
    STATUS_CONFLICTING,
    STATUS_DELISTED,
    STATUS_LIVE,
    is_live,
    listing_status,
)


def test_the_three_statuses_are_pinned_by_equality() -> None:
    assert LISTING_STATUSES == ("live", "excluded_delisted", "conflicting")


def test_all_three_fields_must_agree_for_a_delisted_exclusion() -> None:
    """Measured 2026-08-28: 57 of 57 delisted instruments carried exactly zero
    open interest and exactly zero day volume, and 0 of 94 live ones did."""
    assert listing_status(True, 0.0, 0.0) == STATUS_DELISTED
    assert listing_status(False, 12.5, 9_000.0) == STATUS_LIVE


@pytest.mark.parametrize(
    ("delisted", "oi", "vol"),
    [
        (True, 12.5, 0.0),  # flagged, but open interest is live
        (True, 0.0, 9_000.0),  # flagged, but it traded today
        (False, 0.0, 0.0),  # not flagged, but dead on both counts
        (False, 0.0, 9_000.0),
        (True, 12.5, 9_000.0),
    ],
)
def test_any_disagreement_is_reported_and_never_resolved_here(
    delisted: bool, oi: float, vol: float
) -> None:
    assert listing_status(delisted, oi, vol) == STATUS_CONFLICTING


def test_an_absent_field_is_never_read_as_a_zero() -> None:
    """The exclusion needs a served, exact zero. An absence is not one."""
    assert listing_status(True, NOT_SERVED, 0.0) == STATUS_CONFLICTING
    assert listing_status(True, 0.0, NOT_SERVED) == STATUS_CONFLICTING
    assert listing_status(True, None, None) == STATUS_CONFLICTING


def test_a_tiny_nonzero_open_interest_is_not_zero() -> None:
    """The boundary is exact: 1e-12 of open interest is not a dead market."""
    assert listing_status(True, 1e-12, 0.0) == STATUS_CONFLICTING


def test_is_live_admits_only_the_live_status() -> None:
    assert is_live(STATUS_LIVE)
    assert not is_live(STATUS_DELISTED)
    assert not is_live(STATUS_CONFLICTING)
