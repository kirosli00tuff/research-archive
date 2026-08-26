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

from insider.market import store as market_store
from insider.paths import DISPERSION_DB, SEALED_DB, ensure_dirs
from insider.portfolio.membership import MembershipSeries

SEALED_SCHEMA = """
CREATE TABLE IF NOT EXISTS raw_excess (
    hold_sessions INTEGER NOT NULL,
    weighting TEXT NOT NULL,
    date TEXT NOT NULL,
    excess REAL NOT NULL,
    PRIMARY KEY (hold_sessions, weighting, date)
);
"""

DISPERSION_SCHEMA = """
CREATE TABLE IF NOT EXISTS centered_excess (
    hold_sessions INTEGER NOT NULL,
    weighting TEXT NOT NULL,
    date TEXT NOT NULL,
    centered REAL NOT NULL,
    book_width INTEGER NOT NULL,
    PRIMARY KEY (hold_sessions, weighting, date)
);
CREATE TABLE IF NOT EXISTS dropped (
    hold_sessions INTEGER NOT NULL,
    weighting TEXT NOT NULL,
    reason TEXT NOT NULL,
    n INTEGER NOT NULL,
    PRIMARY KEY (hold_sessions, weighting, reason)
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


def _share(weights: np.ndarray, top: int) -> float:
    """Weight share held by the heaviest `top` names. A concentration measure."""
    total = weights.sum()
    if total <= 0:
        return 0.0
    ordered = np.sort(weights)[::-1]
    return float(ordered[:top].sum() / total)


def _effective_names(weights: np.ndarray) -> float:
    """Inverse Herfindahl. How many equally weighted names the book behaves like."""
    total = weights.sum()
    if total <= 0:
        return 0.0
    p = weights / total
    return float(1.0 / np.square(p).sum())


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
    weighting: str
    dates: tuple[str, ...]
    raw_excess: tuple[float, ...]
    book_width: tuple[int, ...]
    dropped: dict[str, int]
    # Second moments and weight shares only. No first moment of any return
    # series is computed here or anywhere else outside insider.eval.evaluator.
    diagnostics: dict[str, float]


def build_series(
    con: sqlite3.Connection,
    panel: Panel,
    rets: np.ndarray,
    series: MembershipSeries,
    weighting: str,
) -> SeriesBuild:
    """One portfolio excess return per session with a non-empty book."""
    row_of = panel.index_of()
    formations = market_store.formation_dates(con)
    members_at = {f: market_store.members_at(con, f) for f in formations}

    dates: list[str] = []
    excess: list[float] = []
    widths: list[int] = []
    dropped = {"empty_book": 0, "no_finite_member_return": 0, "no_benchmark": 0, "not_priced": 0}
    port_track: list[float] = []
    bench_track: list[float] = []
    top1: list[float] = []
    top5: list[float] = []
    btop1: list[float] = []
    btop5: list[float] = []
    eff_n: list[float] = []

    governing_index = 0
    for j, date in enumerate(series.sessions):
        while governing_index + 1 < len(formations) and formations[governing_index + 1] <= date:
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
        port_track.append(port)
        bench_track.append(bench)
        top1.append(_share(w, 1))
        top5.append(_share(w, 5))
        btop1.append(_share(bw, 1))
        btop5.append(_share(bw, 5))
        eff_n.append(_effective_names(w))

    port_arr = np.asarray(port_track, dtype=np.float64)
    bench_arr = np.asarray(bench_track, dtype=np.float64)
    diagnostics: dict[str, float] = {
        "sd_portfolio_daily": float(port_arr.std(ddof=1)) if port_arr.size > 1 else 0.0,
        "sd_benchmark_daily": float(bench_arr.std(ddof=1)) if bench_arr.size > 1 else 0.0,
        "corr_portfolio_benchmark": (
            float(np.corrcoef(port_arr, bench_arr)[0, 1]) if port_arr.size > 1 else 0.0
        ),
        "book_weight_top1_share": float(np.mean(top1)) if top1 else 0.0,
        "book_weight_top5_share": float(np.mean(top5)) if top5 else 0.0,
        "bench_weight_top1_share": float(np.mean(btop1)) if btop1 else 0.0,
        "bench_weight_top5_share": float(np.mean(btop5)) if btop5 else 0.0,
        "book_effective_names": float(np.mean(eff_n)) if eff_n else 0.0,
    }

    return SeriesBuild(
        hold_sessions=series.hold_sessions,
        weighting=weighting,
        dates=tuple(dates),
        raw_excess=tuple(excess),
        book_width=tuple(widths),
        dropped=dropped,
        diagnostics=diagnostics,
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
            key = (build.hold_sessions, build.weighting)
            sealed.execute("DELETE FROM raw_excess WHERE hold_sessions = ? AND weighting = ?", key)
            sealed.executemany(
                "INSERT INTO raw_excess(hold_sessions, weighting, date, excess) VALUES (?,?,?,?)",
                [(*key, d, v) for d, v in zip(build.dates, build.raw_excess, strict=True)],
            )

    with _dispersion() as disp:
        for build in builds:
            key = (build.hold_sessions, build.weighting)
            disp.execute(
                "DELETE FROM centered_excess WHERE hold_sessions = ? AND weighting = ?", key
            )
            disp.execute("DELETE FROM dropped WHERE hold_sessions = ? AND weighting = ?", key)
            values = np.asarray(build.raw_excess, dtype=np.float64)
            centered = values - values.mean() if values.size else values
            disp.executemany(
                "INSERT INTO centered_excess"
                "(hold_sessions, weighting, date, centered, book_width) VALUES (?,?,?,?,?)",
                [
                    (*key, d, float(c), int(w))
                    for d, c, w in zip(build.dates, centered, build.book_width, strict=True)
                ],
            )
            disp.executemany(
                "INSERT INTO dropped(hold_sessions, weighting, reason, n) VALUES (?,?,?,?)",
                [(*key, k, v) for k, v in sorted(build.dropped.items())],
            )
