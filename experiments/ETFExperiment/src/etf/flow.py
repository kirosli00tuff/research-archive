"""The flow payload reader. Flow is signal, not outcome: every field is readable.

Standing rule, stated in CLAUDE.md: flow payload fields readable outside the
sealed writers are *every* field, including the flow values themselves, plus
the capture timestamp this repository stamps on the capture. The blindness
boundary does not touch flow.

What this module refuses is the other failure: a dash where a number will later
stand. A dash is not zero net flow. `parse_cell` returns a recorded absence for
it, and the absence refuses coercion to a float, so a fabricated flat day
cannot enter the threshold band and quietly change the trade count.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from etf.absence import DASH_IN_CELL, NOT_SERVED, Absent

# Every rendering of "no value here" this repository has seen or expects. A
# string outside this set that also fails numeric parsing is NOT_SERVED, which
# is a different recorded absence: the source served something unreadable.
DASH_TOKENS: frozenset[str] = frozenset({"-", "‐", "‑", "‒", "–", "—", "―", ""})

_NUMERIC = re.compile(r"^\(?-?[\d,]*\.?\d+\)?$")


@dataclass(frozen=True, slots=True)
class FlowCell:
    """One fund's value on one trading day, as printed."""

    ticker: str
    value_usd: float | Absent


@dataclass(frozen=True, slots=True)
class FlowRow:
    """One trading day's row of the flow table, as printed in one capture."""

    trade_date: str
    per_fund: tuple[FlowCell, ...]
    total_usd: float | Absent


def parse_cell(raw: str) -> float | Absent:
    """Parse one printed cell into USD, or a recorded absence. Never a zero."""
    text = raw.strip().replace(" ", " ").strip()
    if text in DASH_TOKENS:
        return DASH_IN_CELL
    negative = text.startswith("(") and text.endswith(")")
    body = text[1:-1] if negative else text
    body = body.replace(",", "").replace("$", "").strip()
    if not _NUMERIC.match(body if not negative else f"({body})") and not _NUMERIC.match(body):
        return NOT_SERVED
    try:
        value = float(body)
    except ValueError:
        return NOT_SERVED
    # The published table is denominated in millions of USD.
    value_usd = value * 1_000_000.0
    return -value_usd if negative else value_usd


def aggregate(cells: tuple[FlowCell, ...]) -> float | Absent:
    """Sum the five registered funds. Any absent cell makes the aggregate absent.

    Deliberately strict: substituting zero for one missing fund is exactly the
    synthesized value the standing rule forbids, and on a day the largest fund
    reports late it would fabricate the sign of the aggregate.
    """
    total = 0.0
    for cell in cells:
        if isinstance(cell.value_usd, Absent):
            return cell.value_usd
        total += cell.value_usd
    return total
