"""The readable-pair projection (Amendment H2-5 / `npl.register.projection`).

Boundary fixtures ON the registered boundary: a pair becomes readable on the
day its candle window seals, not the day after, and the seal day is ADR-019's
entry + 92 days exactly.
"""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path

import pytest

from npl.clock import MS_PER_DAY
from npl.register import projection
from npl.register.projection import (
    DAYS_PER_MONTH,
    FORWARD_READABLE_LAG_DAYS,
    READABLE_LAG_DAYS,
    day_ms,
    first_date_reaching,
    month_ends,
    projected_pairs,
    readable_days,
)

TODAY = date(2026, 9, 13)
DEADLINE = date(2027, 3, 31)
ACCRUAL = 18.57


def _entry(day: date) -> int:
    return day_ms(day)


def test_a_pair_is_readable_exactly_92_days_after_its_entry() -> None:
    """ON the boundary: the seal day counts, the day before does not."""
    entry = _entry(date(2026, 6, 1))
    assert readable_days([entry]) == [entry + READABLE_LAG_DAYS * MS_PER_DAY]
    seal_day = date(2026, 9, 1)  # 2026-06-01 + 92 days
    readable = readable_days([entry])
    assert projected_pairs(readable, seal_day, TODAY, 0.0, 1.0)[0] == 1
    day_before = date(2026, 8, 31)
    assert projected_pairs(readable, day_before, TODAY, 0.0, 1.0)[0] == 0


def test_forward_pairs_are_the_accrual_times_the_match_rate() -> None:
    """Under a rule that excludes some events, events and pairs differ."""
    horizon = date(2027, 3, 31)
    days = (horizon - TODAY).days - FORWARD_READABLE_LAG_DAYS
    at_full = int(ACCRUAL * 1.0 * days / DAYS_PER_MONTH)
    at_partial = int(ACCRUAL * 0.873 * days / DAYS_PER_MONTH)
    assert projected_pairs([], horizon, TODAY, ACCRUAL, 1.0)[1] == at_full
    assert projected_pairs([], horizon, TODAY, ACCRUAL, 0.873)[1] == at_partial
    assert at_partial < at_full


def test_a_forward_birth_needs_94_days_not_92() -> None:
    """Entry is listing + 2, so the pair is readable at listing + 94."""
    just_short = TODAY.toordinal() + FORWARD_READABLE_LAG_DAYS - 1
    assert projected_pairs([], date.fromordinal(just_short), TODAY, ACCRUAL, 1.0)[1] == 0


def test_a_match_rate_outside_a_share_is_a_loud_refusal() -> None:
    for bad in (-0.1, 1.1):
        with pytest.raises(ValueError, match="must be a share"):
            projected_pairs([], TODAY, TODAY, ACCRUAL, bad)


def test_first_date_reaching_returns_the_earliest_day_not_a_later_one() -> None:
    entries = [_entry(date(2026, 6, 1)), _entry(date(2026, 6, 2))]
    readable = readable_days(entries)
    assert first_date_reaching(readable, 1, TODAY, DEADLINE, 0.0, 1.0) == TODAY.isoformat()
    assert first_date_reaching(readable, 2, TODAY, DEADLINE, 0.0, 1.0) == TODAY.isoformat()


def test_first_date_reaching_returns_none_when_the_target_is_out_of_reach() -> None:
    assert first_date_reaching([], 10_000, TODAY, DEADLINE, ACCRUAL, 1.0) is None


def test_month_ends_runs_from_this_month_to_the_deadline_inclusive() -> None:
    ends = month_ends(TODAY, DEADLINE)
    assert ends[0] == date(2026, 9, 30)
    assert ends[-1] == DEADLINE
    assert date(2026, 12, 31) in ends
    assert date(2027, 2, 28) in ends  # 2027 is not a leap year


def test_month_ends_crosses_the_year_boundary_without_a_gap() -> None:
    ends = month_ends(date(2026, 11, 15), date(2027, 1, 31))
    assert ends == [date(2026, 11, 30), date(2026, 12, 31), date(2027, 1, 31)]


def test_the_projection_reads_no_outcome_value_and_owns_no_path() -> None:
    tree = ast.parse(Path(projection.__file__).read_text(encoding="utf-8"))
    imports = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert imports == {"__future__", "datetime", "typing", "npl.clock"}
