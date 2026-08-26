"""Stage B. The only permitted reader of the sealed store.

Nothing in Stage A.1 calls anything here. The module exists now so the seal has
exactly one named reader from the first commit, and so the refusal that blocks
Stage B is a real object rather than a plan.

`read_sealed_returns` is defined here and nowhere else. tests/test_guards.py
fails when any other module names `SEALED_DB`, names `insider_sealed`, or calls
`read_sealed_returns`.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from insider.config import CONFIG, Config
from insider.paths import SEALED_DB
from insider.registration_check import require_operator_prior


@dataclass(frozen=True, slots=True)
class SealedSeries:
    """The raw calendar-time excess return series. Its mean is the realized alpha."""

    hold_sessions: int
    weighting: str
    dates: tuple[str, ...]
    excess: tuple[float, ...]


def read_sealed_returns(
    hold_sessions: int, weighting: str, registration: Path | None = None, cfg: Config = CONFIG
) -> SealedSeries:
    """Open the seal. Refuses while the operator prior slot is empty.

    The refusal comes first, before the file is touched, so a run with an empty
    slot cannot read one row and then stop.
    """
    require_operator_prior(registration)
    if not SEALED_DB.exists():
        raise FileNotFoundError(f"sealed store missing: {SEALED_DB}")
    con = sqlite3.connect(f"file:{SEALED_DB}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT date, excess FROM raw_excess WHERE hold_sessions = ? AND weighting = ? "
            "ORDER BY date",
            (hold_sessions or cfg.primary_hold_sessions, weighting or cfg.primary_weighting),
        ).fetchall()
    finally:
        con.close()
    return SealedSeries(
        hold_sessions=hold_sessions,
        weighting=weighting,
        dates=tuple(r[0] for r in rows),
        excess=tuple(float(r[1]) for r in rows),
    )
