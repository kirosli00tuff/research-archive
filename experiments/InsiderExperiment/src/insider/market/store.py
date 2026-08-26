"""The experiment's own copy of the market data it needs.

Copied once from the neighbouring repository, then never read across the
boundary again. Everything downstream reads this file, so a run cannot silently
depend on the source repository still being there or still being the same.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable, Iterator
from contextlib import contextmanager

from insider.paths import MARKET_DB, ensure_dirs

SCHEMA = """
CREATE TABLE IF NOT EXISTS session (
    date TEXT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS membership (
    formation_date TEXT NOT NULL,
    symbol TEXT NOT NULL,
    rank INTEGER NOT NULL,
    median_dollar_volume REAL NOT NULL,
    median_close REAL NOT NULL,
    window_bars INTEGER NOT NULL,
    PRIMARY KEY (formation_date, symbol)
);
CREATE TABLE IF NOT EXISTS bar (
    symbol TEXT NOT NULL,
    date TEXT NOT NULL,
    close REAL NOT NULL,
    volume REAL NOT NULL,
    PRIMARY KEY (symbol, date)
);
CREATE INDEX IF NOT EXISTS idx_bar_date ON bar(date);
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    ensure_dirs()
    con = sqlite3.connect(MARKET_DB)
    try:
        con.executescript(SCHEMA)
        yield con
        con.commit()
    finally:
        con.close()


def write_sessions(con: sqlite3.Connection, dates: Iterable[str]) -> int:
    rows = [(d,) for d in dates]
    con.executemany("INSERT OR REPLACE INTO session(date) VALUES (?)", rows)
    return len(rows)


def write_membership(
    con: sqlite3.Connection, formation_date: str, rows: Iterable[tuple[str, int, float, float, int]]
) -> int:
    payload = [(formation_date, *r) for r in rows]
    con.executemany(
        "INSERT OR REPLACE INTO membership"
        "(formation_date, symbol, rank, median_dollar_volume, median_close, window_bars) "
        "VALUES (?,?,?,?,?,?)",
        payload,
    )
    return len(payload)


def write_bars(con: sqlite3.Connection, rows: Iterable[tuple[str, str, float, float]]) -> int:
    batch = list(rows)
    con.executemany("INSERT OR REPLACE INTO bar(symbol, date, close, volume) VALUES (?,?,?,?)", batch)
    return len(batch)


def set_meta(con: sqlite3.Connection, key: str, value: str) -> None:
    con.execute("INSERT OR REPLACE INTO meta(key, value) VALUES (?,?)", (key, value))


def get_meta(con: sqlite3.Connection, key: str) -> str | None:
    row = con.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else None


def sessions(con: sqlite3.Connection) -> list[str]:
    return [r[0] for r in con.execute("SELECT date FROM session ORDER BY date")]


def formation_dates(con: sqlite3.Connection) -> list[str]:
    return [
        r[0] for r in con.execute("SELECT DISTINCT formation_date FROM membership ORDER BY 1")
    ]


def members_at(con: sqlite3.Connection, formation_date: str) -> dict[str, float]:
    """Symbol to point-in-time median dollar volume for one formation."""
    return {
        r[0]: float(r[1])
        for r in con.execute(
            "SELECT symbol, median_dollar_volume FROM membership WHERE formation_date = ?",
            (formation_date,),
        )
    }


def distinct_member_symbols(con: sqlite3.Connection) -> list[str]:
    return [r[0] for r in con.execute("SELECT DISTINCT symbol FROM membership ORDER BY 1")]


def iter_bars(con: sqlite3.Connection) -> Iterator[tuple[str, str, float, float]]:
    cursor = con.execute("SELECT symbol, date, close, volume FROM bar ORDER BY symbol, date")
    while True:
        rows = cursor.fetchmany(200_000)
        if not rows:
            return
        yield from rows
