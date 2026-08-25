"""Compute forward returns and route them to the correct store. Write only.

This module has no reader. It cannot answer what a forward return was, only
record it. Two stores exist and the split is the seal.

    var/npd_fit.db      dates strictly before the window start. Read by the
                        logistic baseline to fit once and freeze. Holds no
                        window outcome, so reading it leaks nothing.

    var/npd_sealed.db   dates inside the window. Read by npd.eval.evaluator and
                        by nothing else, ever. tests/test_guards.py walks every
                        source file and fails when another module names it.

Absence is recorded. A day whose forward window runs past the end of the store
has no forward return, and that fact is written down rather than filled.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from npd.absence import INSUFFICIENT_HISTORY, NO_BAR, ZERO_DENOMINATOR, Absent, Maybe
from npd.paths import FIT_RETURNS_DB, SEALED_DB, ensure_dirs

RETURNS_SCHEMA = """
CREATE TABLE IF NOT EXISTS forward_return (
    date          TEXT NOT NULL,
    symbol        TEXT NOT NULL,
    horizon       INTEGER NOT NULL,
    ret           REAL,
    absent_reason TEXT,
    PRIMARY KEY (date, symbol, horizon),
    CHECK ((ret IS NULL) = (absent_reason IS NOT NULL))
);
"""


@dataclass(frozen=True, slots=True)
class WriteReport:
    fit_rows: int
    sealed_rows: int
    absent_rows: int


@contextmanager
def _open_writer(path: Path) -> Iterator[sqlite3.Connection]:
    ensure_dirs()
    con = sqlite3.connect(path, timeout=60.0)
    try:
        con.executescript(RETURNS_SCHEMA)
        yield con
        con.commit()
    finally:
        con.close()


def compute(closes: Sequence[float | None], t: int, horizon: int) -> Maybe[float]:
    """close[t + horizon] / close[t] - 1, or a recorded absence."""
    target = t + horizon
    if target >= len(closes):
        return INSUFFICIENT_HISTORY
    base = closes[t]
    tip = closes[target]
    if base is None or tip is None:
        return NO_BAR
    if base <= 0.0:
        return ZERO_DENOMINATOR
    return tip / base - 1.0


def write(rows: Sequence[tuple[str, str, int, Maybe[float]]], *, window_start: str) -> WriteReport:
    """Route each (date, symbol, horizon, value) row to its store.

    The routing is by date alone and it is the only place the two stores are
    named together. A date on or after the window start can only reach the
    sealed store.
    """
    fit_rows: list[tuple[str, str, int, float | None, str | None]] = []
    sealed_rows: list[tuple[str, str, int, float | None, str | None]] = []
    absent = 0
    for date, symbol, horizon, value in rows:
        packed: tuple[str, str, int, float | None, str | None]
        if isinstance(value, Absent):
            packed = (date, symbol, horizon, None, value.reason.value)
            absent += 1
        else:
            packed = (date, symbol, horizon, float(value), None)
        (fit_rows if date < window_start else sealed_rows).append(packed)

    stmt = (
        "INSERT OR REPLACE INTO forward_return(date, symbol, horizon, ret, absent_reason) "
        "VALUES(?,?,?,?,?)"
    )
    if fit_rows:
        with _open_writer(FIT_RETURNS_DB) as con:
            con.executemany(stmt, fit_rows)
    if sealed_rows:
        with _open_writer(SEALED_DB) as con:
            con.executemany(stmt, sealed_rows)

    return WriteReport(fit_rows=len(fit_rows), sealed_rows=len(sealed_rows), absent_rows=absent)
