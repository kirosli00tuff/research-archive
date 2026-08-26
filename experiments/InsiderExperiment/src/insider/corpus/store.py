"""The corpus store. Qualifying events and the attrition that produced them."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable, Iterator
from contextlib import contextmanager

from insider.paths import CORPUS_DB, ensure_dirs

SCHEMA = """
CREATE TABLE IF NOT EXISTS event (
    accession TEXT NOT NULL,
    filer_cik INTEGER NOT NULL,
    issuer_cik INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    filing_date TEXT NOT NULL,
    entry_session TEXT NOT NULL,
    value_usd REAL NOT NULL,
    routine_class TEXT NOT NULL,
    in_surviving_cluster INTEGER NOT NULL,
    flag_reported INTEGER NOT NULL,
    PRIMARY KEY (accession, filer_cik, transaction_date, value_usd)
);
CREATE INDEX IF NOT EXISTS idx_event_entry ON event(entry_session);
CREATE TABLE IF NOT EXISTS attrition (
    state TEXT NOT NULL,
    reason TEXT NOT NULL,
    n INTEGER NOT NULL,
    PRIMARY KEY (state, reason)
);
CREATE TABLE IF NOT EXISTS lag (
    days INTEGER PRIMARY KEY,
    n INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS cluster (
    cluster_id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    window_start TEXT NOT NULL,
    window_end TEXT NOT NULL,
    size INTEGER NOT NULL,
    distinct_filers INTEGER NOT NULL,
    modal_date_price_fraction REAL NOT NULL,
    rejected INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS refusal (
    kind TEXT NOT NULL,
    ordinal INTEGER NOT NULL,
    detail TEXT NOT NULL,
    PRIMARY KEY (kind, ordinal)
);
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    ensure_dirs()
    con = sqlite3.connect(CORPUS_DB)
    try:
        con.executescript(SCHEMA)
        yield con
        con.commit()
    finally:
        con.close()


def reset(con: sqlite3.Connection) -> None:
    """Clear every table. The corpus is rebuilt whole or not at all."""
    con.execute("DELETE FROM event")
    con.execute("DELETE FROM cluster")
    con.execute("DELETE FROM refusal")
    con.execute("DELETE FROM attrition")
    con.execute("DELETE FROM lag")
    con.execute("DELETE FROM meta")


def write_events(con: sqlite3.Connection, rows: Iterable[tuple[object, ...]]) -> int:
    batch = list(rows)
    con.executemany(
        "INSERT OR REPLACE INTO event(accession, filer_cik, issuer_cik, symbol, "
        "transaction_date, filing_date, entry_session, value_usd, routine_class, "
        "in_surviving_cluster, flag_reported) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        batch,
    )
    return len(batch)


def write_attrition(con: sqlite3.Connection, counts: dict[tuple[str, str], int]) -> None:
    con.executemany(
        "INSERT OR REPLACE INTO attrition(state, reason, n) VALUES (?,?,?)",
        [(state, reason, n) for (state, reason), n in sorted(counts.items())],
    )


def write_lags(con: sqlite3.Connection, counts: dict[int, int]) -> None:
    con.executemany("INSERT OR REPLACE INTO lag(days, n) VALUES (?,?)", sorted(counts.items()))


def write_clusters(con: sqlite3.Connection, rows: Iterable[tuple[object, ...]]) -> int:
    batch = list(rows)
    con.executemany(
        "INSERT OR REPLACE INTO cluster(cluster_id, symbol, window_start, window_end, size, "
        "distinct_filers, modal_date_price_fraction, rejected) VALUES (?,?,?,?,?,?,?,?)",
        batch,
    )
    return len(batch)


def write_refusal(con: sqlite3.Connection, kind: str, ordinal: int, detail: str) -> None:
    """A refusal is recorded because it was produced, never because it was asserted."""
    con.execute(
        "INSERT OR REPLACE INTO refusal(kind, ordinal, detail) VALUES (?,?,?)",
        (kind, ordinal, detail),
    )


def refusals(con: sqlite3.Connection, kind: str) -> list[str]:
    return [
        r[0]
        for r in con.execute(
            "SELECT detail FROM refusal WHERE kind = ? ORDER BY ordinal", (kind,)
        )
    ]


def set_meta(con: sqlite3.Connection, key: str, value: str) -> None:
    con.execute("INSERT OR REPLACE INTO meta(key, value) VALUES (?,?)", (key, value))


def events(con: sqlite3.Connection) -> list[tuple[str, str]]:
    """(symbol, entry_session) for every qualifying event, the shape membership needs."""
    return [(r[0], r[1]) for r in con.execute("SELECT symbol, entry_session FROM event")]


def event_count(con: sqlite3.Connection) -> int:
    row = con.execute("SELECT COUNT(*) FROM event").fetchone()
    return int(row[0]) if row else 0


def events_per_year(con: sqlite3.Connection) -> dict[str, int]:
    return {
        r[0]: int(r[1])
        for r in con.execute(
            "SELECT substr(entry_session,1,4), COUNT(*) FROM event GROUP BY 1 ORDER BY 1"
        )
    }
