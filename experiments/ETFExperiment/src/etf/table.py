"""A dependency-free HTML table reader.

The project has zero runtime dependencies and keeps it that way: a flow table
served as server-rendered HTML needs a table reader, not a browser. This one
walks `html.parser` and returns rows of cell text, decoded and whitespace-
normalised, and nothing else.

It deliberately does not "repair" a malformed table. A row whose cell count
differs from the header's is returned as it stands; the caller decides, and the
caller's rule is that a shape it did not expect is a recorded absence.
"""

from __future__ import annotations

from html.parser import HTMLParser
from typing import Final

_CELL_TAGS: Final = frozenset({"td", "th"})
_SKIP_TAGS: Final = frozenset({"script", "style"})


class _TableReader(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._table_stack: list[list[list[str]]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _SKIP_TAGS:
            self._skip_depth += 1
            return
        if tag == "table":
            self._table_stack.append([])
        elif tag == "tr" and self._table_stack:
            self._row = []
        elif tag in _CELL_TAGS and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag: str) -> None:
        if tag in _SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if tag in _CELL_TAGS and self._cell is not None and self._row is not None:
            self._row.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._row is not None and self._table_stack:
            self._table_stack[-1].append(self._row)
            self._row = None
        elif tag == "table" and self._table_stack:
            self.tables.append(self._table_stack.pop())

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0 and self._cell is not None:
            self._cell.append(data)

    def close(self) -> None:
        super().close()
        # An unclosed <table> still yields its rows rather than vanishing.
        while self._table_stack:
            self.tables.append(self._table_stack.pop())


def read_tables(markup: str) -> list[list[list[str]]]:
    """Every table in the document, as rows of cell text, outermost last."""
    reader = _TableReader()
    reader.feed(markup)
    reader.close()
    return reader.tables


def largest_table(markup: str) -> list[list[str]]:
    """The table with the most cells. Raises when the document holds none."""
    tables = read_tables(markup)
    if not tables:
        raise ValueError("no <table> element in the document; refusing to guess a layout")
    return max(tables, key=lambda t: sum(len(r) for r in t))
