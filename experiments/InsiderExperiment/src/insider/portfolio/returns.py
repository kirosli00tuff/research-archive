"""Daily calendar-time portfolio returns, and the two stores they split into.

This module is the only place raw portfolio excess returns exist. It writes
them twice and reads neither back.

    var/insider_sealed.db       the raw series. Its mean is the realized alpha.
                                insider.eval.evaluator is its only reader.
    var/insider_dispersion.db   the same series with its own mean subtracted.
                                The mean is never written, so it cannot be read
                                back out. insider.power is its only reader.

A name with no finite return on a session is dropped from that session's
average and counted. Absence is a recorded state, never a synthesized value, so
no missing return is carried forward or filled with a zero.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

import numpy as np

from insider.config import CONFIG, Config
from insider.market import store as market_store
from insider.paths import DISPERSION_DB, SEALED_DB, ensure_dirs
from insider.portfolio.membership import MembershipSeries

SEALED_SCHEMA = """
CREATE TABLE IF NOT EXISTS raw_excess (
    hold_sessions INTEGER NOT NULL,
    date TEXT NOT NULL,
    excess REAL NOT NULL,
    PRIMARY KEY (hold_sessions, date)
);
"""

DISPERSION_SCHEMA = """
CREATE TABLE IF NOT EXISTS centered_excess (
    hold_sessions INTEGER NOT NULL,
    date TEXT NOT NULL,
    centered REAL NOT NULL,
    book_width INTEGER NOT NULL,
    PRIMARY KEY (hold_sessions, date)
);
CREATE TABLE IF NOT EXISTS dropped (
    hold_sessions INTEGER NOT NULL,
    reason TEXT NOT NULL,
    n INTEGER NOT NULL,
    PRIMARY KEY (hold_sessions, reason)
);
"""


@dataclass(frozen=True, slots=True)
class Panel:
    """Aligned closes for every symbol that is ever a universe member."""

    symbols: tuple[str, ...]
    dates: tuple[str, ...]
    close: np.ndarray

    def index_of(self) -> dict[str, int]:
        return {s: i for i, s in enumerate(self.symbols)}


def load_panel(con: sqlite3.Connection) -> Panel:
    symbols = market_store.distinct_member_symbols(con)
    dates = market_store.sessions(con)
    row_of = {s: i for i, s in enumerate(symbols)}
    col_of = {d: i for i, d in enumerate(dates)}
    close = np.full((len(symbols), len(dates)), np.nan, dtype=np.float64)
    for symbol, date, value, _volume in market_store.iter_bars(con):
        r = row_of.get(symbol)
        c = col_of.get(date)
        if r is not None and c is not None:
            close[r, c] = value
    return Panel(symbols=tuple(symbols), dates=tuple(dates), close=close)


def simple_returns(panel: Panel) -> np.ndarray:
    """Close-to-close returns. Column 0 is absent by construction and stays NaN."""
    out = np.full_like(panel.close, np.nan)
    prev = panel.close[:, :-1]
    cur = panel.close[:, 1:]
    with np.errstate(invalid="ignore", divide="ignore"):
        out[:, 1:] = np.where(prev > 0, cur / prev - 1.0, np.nan)
    return out


def _weights(
    weighting: str, members: dict[str, float], names: list[str], row_of: dict[str, int]
) -> tuple[np.ndarray, np.ndarray]:
    """Row indexes and weights for one book on one session."""
    rows = np.array([row_of[n] for n in names], dtype=np.int64)
    if weighting == "equal_weighted":
        raw = np.ones(len(names), dtype=np.float64)
    elif weighting == "value_weighted":
        raw = np.array([max(members.get(n, 0.0), 0.0) for n in names], dtype=np.float64)
    else:
        raise ValueError(f"unregistered weighting {weighting!r}")
    return rows, raw


def _weighted(values: np.ndarray, weights: np.ndarray) -> float | None:
    finite = np.isfinite(values) & (weights > 0)
    if not finite.any():
        return None
    w = weights[finite]
    total = w.sum()
    if total <= 0:
        return None
    return float((values[finite] * w).sum() / total)


@dataclass(frozen=True, slots=True)
class SeriesBuild:
    hold_sessions: int
    dates: tuple[str, ...]
    raw_excess: tuple[float, ...]
    book_width: tuple[int, ...]
    dropped: dict[str, int]


def build_series(
    con: sqlite3.Connection,
    panel: Panel,
    rets: np.ndarray,
    series: MembershipSeries,
    weighting: str,
    cfg: Config = CONFIG,
) -> SeriesBuild:
    """One portfolio excess return per session with a non-empty book."""
    row_of = panel.index_of()
    formations = market_store.formation_dates(con)
    members_at = {f: market_store.members_at(con, f) for f in formations}

    dates: list[str] = []
    excess: list[float] = []
    widths: list[int] = []
    dropped = {"empty_book": 0, "no_finite_member_return": 0, "no_benchmark": 0, "not_priced": 0}

    governing_index = 0
    for j, date in enumerate(series.sessions):
        while (
            governing_index + 1 < len(formations) and formations[governing_index + 1] <= date
        ):
            governing_index += 1
        formation = formations[governing_index]
        if formation > date:
            continue
        members = members_at[formation]

        book = [n for n in series.book[j] if n in row_of]
        if not book:
            dropped["empty_book"] += 1
            continue

        priced = [n for n in book if n in members]
        dropped["not_priced"] += len(book) - len(priced)
        if not priced:
            dropped["no_finite_member_return"] += 1
            continue

        rows, w = _weights(weighting, members, priced, row_of)
        port = _weighted(rets[rows, j], w)
        if port is None:
            dropped["no_finite_member_return"] += 1
            continue

        bench_names = [n for n in members if n in row_of]
        brows, bw = _weights(weighting, members, bench_names, row_of)
        bench = _weighted(rets[brows, j], bw)
        if bench is None:
            dropped["no_benchmark"] += 1
            continue

        dates.append(date)
        excess.append(port - bench)
        widths.append(len(priced))

    return SeriesBuild(
        hold_sessions=series.hold_sessions,
        dates=tuple(dates),
        raw_excess=tuple(excess),
        book_width=tuple(widths),
        dropped=dropped,
    )


@contextmanager
def _sealed() -> Iterator[sqlite3.Connection]:
    ensure_dirs()
    con = sqlite3.connect(SEALED_DB)
    try:
        con.executescript(SEALED_SCHEMA)
        yield con
        con.commit()
    finally:
        con.close()


@contextmanager
def _dispersion() -> Iterator[sqlite3.Connection]:
    ensure_dirs()
    con = sqlite3.connect(DISPERSION_DB)
    try:
        con.executescript(DISPERSION_SCHEMA)
        yield con
        con.commit()
    finally:
        con.close()


def write(builds: list[SeriesBuild]) -> None:
    """Write the raw series to the seal and the centered series to dispersion.

    Centering happens here and the mean is a local that is never returned,
    never stored, and never logged. What lands in the dispersion store sums to
    zero by construction, so the first moment cannot be recovered from it.
    """
    with _sealed() as sealed:
        for build in builds:
            sealed.execute("DELETE FROM raw_excess WHERE hold_sessions = ?", (build.hold_sessions,))
            sealed.executemany(
                "INSERT INTO raw_excess(hold_sessions, date, excess) VALUES (?,?,?)",
                [(build.hold_sessions, d, v) for d, v in zip(build.dates, build.raw_excess, strict=True)],
            )

    with _dispersion() as disp:
        for build in builds:
            disp.execute(
                "DELETE FROM centered_excess WHERE hold_sessions = ?", (build.hold_sessions,)
            )
            disp.execute("DELETE FROM dropped WHERE hold_sessions = ?", (build.hold_sessions,))
            values = np.asarray(build.raw_excess, dtype=np.float64)
            centered = values - values.mean() if values.size else values
            disp.executemany(
                "INSERT INTO centered_excess(hold_sessions, date, centered, book_width) "
                "VALUES (?,?,?,?)",
                [
                    (build.hold_sessions, d, float(c), int(w))
                    for d, c, w in zip(build.dates, centered, build.book_width, strict=True)
                ],
            )
            disp.executemany(
                "INSERT INTO dropped(hold_sessions, reason, n) VALUES (?,?,?)",
                [(build.hold_sessions, k, v) for k, v in sorted(build.dropped.items())],
            )
