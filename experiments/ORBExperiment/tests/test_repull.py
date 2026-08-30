"""The revision clock, with fixtures ON the registered 14-day boundary."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from orb.config import CONFIG
from orb.repull import (
    RepullNotDueError,
    days_waited,
    earliest_eligible,
    is_due,
    registered_wait_days,
    require_due,
)

PULLED = date(2026, 8, 29)


def test_the_registered_wait_is_fourteen_calendar_days() -> None:
    assert registered_wait_days() == 14
    assert CONFIG.revision_repull_wait_days == 14


def test_the_earliest_eligible_date_is_the_pull_plus_the_wait() -> None:
    assert earliest_eligible(PULLED) == date(2026, 9, 12)


def test_one_day_before_the_boundary_refuses() -> None:
    """The fixture sits ON the boundary minus one day, not comfortably inside."""
    day_thirteen = PULLED + timedelta(days=13)
    assert is_due(PULLED, day_thirteen) is False
    with pytest.raises(RepullNotDueError, match="not due"):
        require_due(PULLED, day_thirteen)


def test_the_boundary_day_itself_is_due() -> None:
    day_fourteen = PULLED + timedelta(days=14)
    assert is_due(PULLED, day_fourteen) is True
    assert require_due(PULLED, day_fourteen) == 14


def test_a_day_after_the_boundary_is_due() -> None:
    assert require_due(PULLED, PULLED + timedelta(days=15)) == 15


def test_the_day_of_the_pull_refuses() -> None:
    with pytest.raises(RepullNotDueError):
        require_due(PULLED, PULLED)


def test_a_date_before_the_pull_refuses_and_reports_a_negative_wait() -> None:
    earlier = PULLED - timedelta(days=3)
    assert days_waited(PULLED, earlier) == -3
    with pytest.raises(RepullNotDueError, match="-3 calendar days"):
        require_due(PULLED, earlier)


def test_the_refusal_names_the_earliest_eligible_date() -> None:
    """A refusal that does not say when to come back is a refusal twice."""
    with pytest.raises(RepullNotDueError, match="2026-09-12"):
        require_due(PULLED, PULLED + timedelta(days=1))


def test_the_refusal_states_why_an_early_repull_is_wrong_not_merely_weak() -> None:
    with pytest.raises(RepullNotDueError, match="biased toward zero"):
        require_due(PULLED, PULLED)
