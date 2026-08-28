"""Flow is signal: every field readable. A dash is an absence, never a zero."""

from __future__ import annotations

import pytest

from etf.absence import DASH_IN_CELL, NOT_SERVED, Absent
from etf.flow import FlowCell, aggregate, parse_cell


def test_a_plain_number_parses_to_usd_from_the_published_millions() -> None:
    assert parse_cell("123.4") == 123_400_000.0


def test_a_thousands_separated_number_parses() -> None:
    assert parse_cell("1,234.5") == 1_234_500_000.0


def test_a_parenthesised_number_is_negative_the_table_convention() -> None:
    assert parse_cell("(45.6)") == -45_600_000.0


def test_a_leading_minus_is_negative() -> None:
    assert parse_cell("-45.6") == -45_600_000.0


@pytest.mark.parametrize("token", ["-", "–", "—", "", "   "])
def test_every_dash_rendering_is_a_recorded_absence_never_zero(token: str) -> None:
    result = parse_cell(token)
    assert result == DASH_IN_CELL
    assert result != 0.0
    with pytest.raises(TypeError, match="refusing to coerce"):
        float(result)


def test_an_unreadable_cell_is_not_served_which_is_a_different_absence() -> None:
    """A dash and an unreadable string are different facts and never merge."""
    assert parse_cell("pending") == NOT_SERVED
    assert parse_cell("pending") != DASH_IN_CELL


def test_the_aggregate_of_five_present_cells_is_their_sum() -> None:
    cells = tuple(FlowCell(ticker=t, value_usd=10_000_000.0) for t in "ABCDE")
    assert aggregate(cells) == 50_000_000.0


def test_one_absent_fund_makes_the_whole_aggregate_absent() -> None:
    """The mutation this pins: substituting zero for a fund that reported late.

    On a day the largest fund is missing, a zero substitution fabricates the
    sign of the aggregate, which is the quantity the Section 4 rule trades on.
    """
    cells = (
        FlowCell(ticker="IBIT", value_usd=DASH_IN_CELL),
        FlowCell(ticker="FBTC", value_usd=-30_000_000.0),
    )
    result = aggregate(cells)
    assert isinstance(result, Absent)
    assert result == DASH_IN_CELL
