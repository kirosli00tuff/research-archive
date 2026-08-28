"""HFExperiment's own bar store. Append-only SQLite, no mutation ever.

Built against the stale-adjustment trap Task 0 of Stage B.1 checked
for: every query's result is appended with its query timestamp, reads
take the latest row per key, and nothing is ever updated or deleted in
place. An adjustment landing between runs re-enters the store as newer
rows rather than aging out of it. tests/test_barstore.py asserts this
module's source contains no update and no delete statement.

This store belongs to HFExperiment alone. It never touches AiTrader's
database, its credentials, or its rate window.
"""
from __future__ import annotations

import sqlite3
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS bars (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    session TEXT NOT NULL,
    open REAL, high REAL, low REAL,
    close REAL NOT NULL,
    volume REAL,
    adjustment TEXT NOT NULL,
    queried_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS bars_key ON bars (symbol, session, queried_utc);
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    open_local TEXT NOT NULL,
    close_local TEXT NOT NULL,
    queried_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_key ON sessions (date, queried_utc);
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    status TEXT NOT NULL,
    tradable INTEGER NOT NULL,
    queried_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS assets_key ON assets (symbol, queried_utc);
CREATE TABLE IF NOT EXISTS universe (
    id INTEGER PRIMARY KEY,
    formation_date TEXT NOT NULL,
    symbol TEXT NOT NULL,
    recorded_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS formations (
    id INTEGER PRIMARY KEY,
    formation_date TEXT NOT NULL,
    width INTEGER NOT NULL,
    rank INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    recorded_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS fetch_log (
    id INTEGER PRIMARY KEY,
    run_utc TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    ok INTEGER NOT NULL,
    detail TEXT NOT NULL
);
"""

BarRow = tuple[
    str, str, float | None, float | None, float | None, float, float | None
]
SessionRow = tuple[str, str, str]
AssetRow = tuple[str, str, str, str, int]


@dataclass(frozen=True)
class AssetInfo:
    """The latest snapshot of one asset."""

    name: str
    exchange: str
    active: bool


class BarStore:
    """One SQLite file, INSERT and SELECT only."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self._path)
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    # -- bars ---------------------------------------------------------

    def append_bars(
        self, rows: Iterable[BarRow], adjustment: str, queried_utc: str
    ) -> int:
        data = [
            (sym, ses, o, h, lo, c, v, adjustment, queried_utc)
            for sym, ses, o, h, lo, c, v in rows
        ]
        self._conn.executemany(
            "INSERT INTO bars (symbol, session, open, high, low, close,"
            " volume, adjustment, queried_utc) VALUES (?,?,?,?,?,?,?,?,?)",
            data,
        )
        self._conn.commit()
        return len(data)

    def latest_closes(
        self, symbols: Sequence[str], start: str, end: str
    ) -> dict[tuple[str, str], float]:
        """Latest close per (symbol, session) in [start, end] inclusive."""
        out: dict[tuple[str, str], float] = {}
        marks = ",".join("?" for _ in symbols)
        cur = self._conn.execute(
            f"SELECT symbol, session, close FROM bars WHERE symbol IN"
            f" ({marks}) AND session >= ? AND session <= ?"
            " ORDER BY queried_utc ASC, id ASC",
            (*symbols, start, end),
        )
        for sym, ses, close in cur:
            out[(sym, ses)] = close
        return out

    def last_close_at_or_before(
        self, symbol: str, session: str
    ) -> float | None:
        """The latest-queried close of the last bar at or before session."""
        row = self._conn.execute(
            "SELECT close FROM bars WHERE symbol = ? AND session <= ?"
            " ORDER BY session DESC, queried_utc DESC, id DESC LIMIT 1",
            (symbol, session),
        ).fetchone()
        return None if row is None else float(row[0])

    def bar_sessions(self, symbol: str, start: str, end: str) -> list[str]:
        """Distinct sessions with any bar for the symbol, ascending."""
        cur = self._conn.execute(
            "SELECT DISTINCT session FROM bars WHERE symbol = ? AND"
            " session >= ? AND session <= ? ORDER BY session ASC",
            (symbol, start, end),
        )
        return [row[0] for row in cur]

    # -- trading calendar ---------------------------------------------

    def append_sessions(
        self, rows: Iterable[SessionRow], queried_utc: str
    ) -> int:
        data = [(d, o, c, queried_utc) for d, o, c in rows]
        self._conn.executemany(
            "INSERT INTO sessions (date, open_local, close_local,"
            " queried_utc) VALUES (?,?,?,?)",
            data,
        )
        self._conn.commit()
        return len(data)

    def session_dates(self, start: str, end: str) -> list[str]:
        cur = self._conn.execute(
            "SELECT DISTINCT date FROM sessions WHERE date >= ? AND"
            " date <= ? ORDER BY date ASC",
            (start, end),
        )
        return [row[0] for row in cur]

    # -- assets -------------------------------------------------------

    def append_assets(self, rows: Iterable[AssetRow], queried_utc: str) -> int:
        data = [(s, n, e, st, t, queried_utc) for s, n, e, st, t in rows]
        self._conn.executemany(
            "INSERT INTO assets (symbol, name, exchange, status, tradable,"
            " queried_utc) VALUES (?,?,?,?,?,?)",
            data,
        )
        self._conn.commit()
        return len(data)

    def latest_assets(self) -> dict[str, AssetInfo]:
        cur = self._conn.execute(
            "SELECT symbol, name, exchange, status FROM assets"
            " ORDER BY queried_utc ASC, id ASC"
        )
        out: dict[str, AssetInfo] = {}
        for sym, name, exchange, status in cur:
            out[sym] = AssetInfo(
                name=name, exchange=exchange, active=status == "active"
            )
        return out

    # -- universe and formations --------------------------------------

    def append_universe(
        self, formation_date: str, symbols: Sequence[str], recorded_utc: str
    ) -> None:
        self._conn.executemany(
            "INSERT INTO universe (formation_date, symbol, recorded_utc)"
            " VALUES (?,?,?)",
            [(formation_date, s, recorded_utc) for s in symbols],
        )
        self._conn.commit()

    def universe_members(self, formation_date: str) -> list[str]:
        cur = self._conn.execute(
            "SELECT DISTINCT symbol FROM universe WHERE formation_date = ?"
            " ORDER BY symbol ASC",
            (formation_date,),
        )
        return [row[0] for row in cur]

    def append_formation(
        self,
        formation_date: str,
        width: int,
        ranked_symbols: Sequence[str],
        recorded_utc: str,
    ) -> None:
        self._conn.executemany(
            "INSERT INTO formations (formation_date, width, rank, symbol,"
            " recorded_utc) VALUES (?,?,?,?,?)",
            [
                (formation_date, width, i + 1, s, recorded_utc)
                for i, s in enumerate(ranked_symbols)
            ],
        )
        self._conn.commit()

    def formation_books(self, formation_date: str) -> dict[int, list[str]]:
        cur = self._conn.execute(
            "SELECT width, rank, symbol FROM formations WHERE"
            " formation_date = ? ORDER BY width ASC, rank ASC, id ASC",
            (formation_date,),
        )
        out: dict[int, dict[int, str]] = {}
        for width, rank, symbol in cur:
            out.setdefault(width, {})[rank] = symbol
        return {
            w: [ranked[r] for r in sorted(ranked)] for w, ranked in out.items()
        }

    def recorded_formation_dates(self) -> list[str]:
        cur = self._conn.execute(
            "SELECT DISTINCT formation_date FROM formations"
            " ORDER BY formation_date ASC"
        )
        return [row[0] for row in cur]

    # -- fetch log ----------------------------------------------------

    def append_fetch(
        self, run_utc: str, endpoint: str, ok: bool, detail: str
    ) -> None:
        self._conn.execute(
            "INSERT INTO fetch_log (run_utc, endpoint, ok, detail)"
            " VALUES (?,?,?,?)",
            (run_utc, endpoint, 1 if ok else 0, detail),
        )
        self._conn.commit()

    def recent_fetches(
        self, limit: int = 20
    ) -> list[tuple[str, str, bool, str]]:
        cur = self._conn.execute(
            "SELECT run_utc, endpoint, ok, detail FROM fetch_log"
            " ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return [(r, e, bool(ok), d) for r, e, ok, d in cur]
