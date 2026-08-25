"""The experiment's own store. Nothing outside npd.data writes here.

Absence is recorded, never synthesized. Every table that can hold a missing
observation carries an `absent_reason` column beside the value column, and the
value column is NULL exactly when a reason is present. `tests/test_absence.py`
fails when a row carries both or neither.
"""

from __future__ import annotations

import datetime as dt
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from npd.paths import STORE_DB, ensure_dirs

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS session (
    date TEXT PRIMARY KEY,
    idx  INTEGER NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS bar (
    symbol TEXT NOT NULL,
    date   TEXT NOT NULL,
    close  REAL NOT NULL,
    volume REAL NOT NULL,
    PRIMARY KEY (symbol, date)
) WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS idx_bar_date ON bar(date);

CREATE TABLE IF NOT EXISTS formation (
    formation_date       TEXT NOT NULL,
    symbol               TEXT NOT NULL,
    rank                 INTEGER NOT NULL,
    median_dollar_volume REAL NOT NULL,
    median_close         REAL NOT NULL,
    window_bars          INTEGER NOT NULL,
    PRIMARY KEY (formation_date, symbol)
);

CREATE TABLE IF NOT EXISTS panel (
    date    TEXT NOT NULL,
    symbol  TEXT NOT NULL,
    stratum INTEGER NOT NULL,
    formation_date TEXT NOT NULL,
    PRIMARY KEY (date, symbol)
);

CREATE TABLE IF NOT EXISTS feature (
    date          TEXT NOT NULL,
    symbol        TEXT NOT NULL,
    name          TEXT NOT NULL,
    raw           REAL,
    z             REAL,
    absent_reason TEXT,
    PRIMARY KEY (date, symbol, name),
    CHECK ((raw IS NULL) = (absent_reason IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS anonymization (
    date   TEXT NOT NULL,
    label  TEXT NOT NULL,
    symbol TEXT NOT NULL,
    nonce  TEXT NOT NULL,
    PRIMARY KEY (date, label)
);

CREATE TABLE IF NOT EXISTS baseline_ranking (
    date     TEXT NOT NULL,
    baseline TEXT NOT NULL,
    symbol   TEXT NOT NULL,
    rank     INTEGER NOT NULL,
    PRIMARY KEY (date, baseline, symbol)
);

CREATE TABLE IF NOT EXISTS model_ranking (
    date   TEXT NOT NULL,
    rank   INTEGER NOT NULL,
    label  TEXT NOT NULL,
    symbol TEXT NOT NULL,
    PRIMARY KEY (date, rank)
);

CREATE TABLE IF NOT EXISTS day_status (
    date       TEXT PRIMARY KEY,
    state      TEXT NOT NULL,
    detail     TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS logistic_coefficient (
    name TEXT PRIMARY KEY,
    coef REAL NOT NULL
);
"""


@contextmanager
def open_store(path: Path = STORE_DB) -> Iterator[sqlite3.Connection]:
    """Open the experiment's own store, creating the schema when absent."""
    ensure_dirs()
    con = sqlite3.connect(path, timeout=60.0)
    con.execute("PRAGMA foreign_keys=ON")
    try:
        con.executescript(SCHEMA)
        yield con
        con.commit()
    finally:
        con.close()


def set_meta(con: sqlite3.Connection, key: str, value: str) -> None:
    con.execute(
        "INSERT INTO meta(key, value) VALUES(?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value),
    )


def get_meta(con: sqlite3.Connection, key: str) -> str | None:
    row = con.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return None if row is None else str(row[0])


def sessions(con: sqlite3.Connection) -> list[str]:
    return [r[0] for r in con.execute("SELECT date FROM session ORDER BY idx")]


def session_index(con: sqlite3.Connection) -> dict[str, int]:
    return {r[0]: int(r[1]) for r in con.execute("SELECT date, idx FROM session")}


def record_day_state(con: sqlite3.Connection, date: str, state: str, detail: str = "") -> None:
    con.execute(
        "INSERT INTO day_status(date, state, detail, updated_at) VALUES(?,?,?,?) "
        "ON CONFLICT(date) DO UPDATE SET state=excluded.state, detail=excluded.detail, "
        "updated_at=excluded.updated_at",
        (date, state, detail, dt.datetime.now(dt.UTC).isoformat()),
    )


def day_states(con: sqlite3.Connection) -> dict[str, str]:
    return {r[0]: r[1] for r in con.execute("SELECT date, state FROM day_status")}


# Row clearing lives here and nowhere else, so a rebuild of one day cannot be
# written twice in two different ways. Every statement is scoped to a single
# date, so rebuilding one session never touches another.
_DAY_TABLES = ("panel", "feature", "anonymization", "baseline_ranking", "model_ranking")


def clear_day(con: sqlite3.Connection, date: str) -> None:
    """Remove every derived row for one session. Bars and formations survive."""
    for table in _DAY_TABLES:
        con.execute(f"DELETE FROM {table} WHERE date = ?", (date,))


def clear_derived(con: sqlite3.Connection) -> None:
    """Remove every derived row for every session. Used by a full rebuild."""
    for table in _DAY_TABLES:
        con.execute(f"DELETE FROM {table}")
    con.execute("DELETE FROM day_status")


def forget_rows(con: sqlite3.Connection, table: str, dates: list[str]) -> int:
    """Remove rows for the given dates from one derived table.

    Used by the B.0b scenarios to stage a source fault and a lost commit against
    a scratch store. Refuses any table outside the derived set, so it cannot
    reach bars, formations, or the session calendar.
    """
    if table not in _DAY_TABLES:
        raise ValueError(f"{table} is not a derived table")
    cur = con.executemany(f"DELETE FROM {table} WHERE date = ?", [(d,) for d in dates])
    return cur.rowcount if cur.rowcount is not None else 0
