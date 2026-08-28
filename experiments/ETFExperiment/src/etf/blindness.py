"""The blindness boundary. The only price and funding parsers outside seals.

Price payload fields readable outside the sealed writers: `t`, `T`, and the row
count. Never `o`, `h`, `l`, `c`, `v`, under any spelling, in any module, until
the registered Stage B read.

Funding fields readable: `time` always; `fundingRate` only where `time` is
strictly before the registered pre-period boundary of 2025-05-01, under the
Section 9 carve-out enforced in `etf.preperiod`. A row stamped at or after that
instant carries a recorded absence, which refuses numeric coercion.

Flow is signal, not outcome, and is parsed in `etf.flow` with every field
readable. Nothing in this module touches flow.

tests/test_blindness.py and tests/test_guards.py pin these absences against the
parse tree of every module under src/etf.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from etf.absence import Absent
from etf.preperiod import gate_pre_period

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
    """Parse a candleSnapshot response reading only `t`, `T`, and the row count."""
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
        for field in ALLOWED_CANDLE_FIELDS:
            if field not in row:
                raise BlindnessViolation(
                    f"candleSnapshot row lacks {field!r}; refusing to guess a timestamp"
                )
        opens.append(int(row[ALLOWED_CANDLE_FIELDS[0]]))
        closes.append(int(row[ALLOWED_CANDLE_FIELDS[1]]))
    return CandleTimes(open_ms=tuple(opens), close_ms=tuple(closes), row_count=len(parsed))


@dataclass(frozen=True, slots=True)
class FundingRow:
    """One fundingHistory row. The rate is gated by the pre-period carve-out."""

    time_ms: int
    rate: float | Absent


def funding_rows(payload: bytes | str) -> tuple[FundingRow, ...]:
    """Parse a fundingHistory response under the pre-period gate.

    `time` is read always. `fundingRate` is read only where `time` is strictly
    before the registered 2025-05-01 boundary; a row stamped at or after it
    carries `Absent(pre_period_gated)`, which refuses numeric coercion.
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
        rows.append(
            FundingRow(time_ms=time_ms, rate=gate_pre_period(time_ms, float(row["fundingRate"])))
        )
    return tuple(rows)
