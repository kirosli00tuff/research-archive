"""The blindness boundary. The only candle and funding parsers outside seals.

Candle payload fields readable outside the sealed writers: t, T, and row
count. fundingHistory fields readable: time always, fundingRate only where
time is at or before the referencing event entry timestamp. Every other field
of either payload is unreadable here until the registered Stage B read, and
tests/test_blindness.py pins these absences against this file's parse tree.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from npl.absence import BLINDNESS_GATED, Absent

ALLOWED_CANDLE_FIELDS: tuple[str, ...] = ("t", "T")


class BlindnessViolation(RuntimeError):
    """A payload reached the blind reader in a shape it refuses to guess about."""


@dataclass(frozen=True, slots=True)
class CandleTimes:
    """Timestamps and count only. No price or volume field exists here."""

    open_ms: tuple[int, ...]
    close_ms: tuple[int, ...]
    row_count: int


def candle_times(payload: bytes | str) -> CandleTimes:
    """Parse a candleSnapshot response reading only t, T, and the row count."""
    parsed = json.loads(payload)
    if not isinstance(parsed, list):
        raise BlindnessViolation(
            f"candleSnapshot payload is not a list: {type(parsed).__name__}. "
            "Refusing to guess; record the call as source_failed."
        )
    opens: list[int] = []
    closes: list[int] = []
    for row in parsed:
        if not isinstance(row, dict):
            raise BlindnessViolation("candleSnapshot row is not an object; refusing to guess")
        opens.append(int(row["t"]))
        closes.append(int(row["T"]))
    return CandleTimes(open_ms=tuple(opens), close_ms=tuple(closes), row_count=len(parsed))


@dataclass(frozen=True, slots=True)
class FundingRow:
    """One fundingHistory row. The rate is gated by the referencing entry."""

    time_ms: int
    rate: float | Absent


def funding_rows(payload: bytes | str, *, entry_ms: int | None) -> tuple[FundingRow, ...]:
    """Parse a fundingHistory response under the blindness gate.

    time is read always. fundingRate is read only where time is at or before
    entry_ms; a later row carries a recorded absence, and a coverage read
    (entry_ms=None) carries absences throughout.
    """
    parsed = json.loads(payload)
    if not isinstance(parsed, list):
        raise BlindnessViolation(
            f"fundingHistory payload is not a list: {type(parsed).__name__}. "
            "Refusing to guess; record the call as source_failed."
        )
    rows: list[FundingRow] = []
    for row in parsed:
        if not isinstance(row, dict):
            raise BlindnessViolation("fundingHistory row is not an object; refusing to guess")
        time_ms = int(row["time"])
        rate: float | Absent
        if entry_ms is not None and time_ms <= entry_ms:
            rate = float(row["fundingRate"])
        else:
            rate = BLINDNESS_GATED
        rows.append(FundingRow(time_ms=time_ms, rate=rate))
    return tuple(rows)
