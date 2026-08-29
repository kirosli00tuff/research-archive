"""The table reader returns cell text and repairs nothing."""

from __future__ import annotations

import pytest

from etf.table import largest_table, read_tables

SIMPLE = """
<table><tr><th>Date</th><th>IBIT</th></tr>
<tr><td>01 May 2025</td><td>(53.6)</td></tr></table>
"""


def test_rows_and_cells_come_back_as_text() -> None:
    tables = read_tables(SIMPLE)
    assert len(tables) == 1
    assert tables[0] == [["Date", "IBIT"], ["01 May 2025", "(53.6)"]]


def test_entities_are_decoded_and_whitespace_normalised() -> None:
    rows = read_tables("<table><tr><td>  a&nbsp;&mdash;\n b </td></tr></table>")[0]
    assert rows[0][0] == "a — b"


def test_markup_inside_a_cell_is_stripped_but_its_text_is_kept() -> None:
    rows = read_tables("<table><tr><td><span>12</span>.<b>3</b></td></tr></table>")[0]
    assert rows[0][0] == "12.3"


def test_script_and_style_content_never_becomes_cell_text() -> None:
    rows = read_tables(
        "<table><tr><td><script>var x=99;</script>7.5<style>td{}</style></td></tr></table>"
    )[0]
    assert rows[0][0] == "7.5"


def test_a_ragged_row_is_returned_as_it_stands_not_padded() -> None:
    """The reader repairs nothing; a shape the caller did not expect is the caller's absence."""
    rows = read_tables("<table><tr><td>a</td><td>b</td></tr><tr><td>c</td></tr></table>")[0]
    assert rows == [["a", "b"], ["c"]]


def test_the_largest_table_is_selected_by_cell_count() -> None:
    markup = "<table><tr><td>x</td></tr></table>" + SIMPLE
    assert largest_table(markup)[0] == ["Date", "IBIT"]


def test_a_document_with_no_table_raises_rather_than_returning_empty() -> None:
    with pytest.raises(ValueError, match="refusing to guess"):
        largest_table("<p>nothing here</p>")


def test_an_unclosed_table_still_yields_its_rows() -> None:
    rows = read_tables("<table><tr><td>a</td></tr>")[0]
    assert rows == [["a"]]
