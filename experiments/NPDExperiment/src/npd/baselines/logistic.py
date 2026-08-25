"""Baseline three. Logistic regression on the identical nine features.

Fit once on panel days strictly before the window start, then frozen. The
coefficients are written to the store and hashed, and the fitted flag is checked
before any window day is ranked. A refit inside the window fails
tests/test_guards.py.

The fit reads forward returns from var/npd_fit.db, which holds only dates before
the window start. It cannot reach the sealed store, and the guard test proves it
does not name that path. load_fit_targets refuses any date after the guard band
end, so the refusal holds even if the two stores were ever pointed at one file.
"""

from __future__ import annotations

import hashlib
import json
import math
import sqlite3
from collections.abc import Sequence
from dataclasses import dataclass

from npd.config import CONFIG, Config
from npd.paths import FIT_RETURNS_DB

LOGISTIC = "logistic"

# Panel days used to fit. Strictly before the window start of 2024-10-31.
FIT_START = "2022-01-03"
FIT_END = "2024-10-30"


@dataclass(frozen=True, slots=True)
class FittedLogistic:
    intercept: float
    coefficients: tuple[tuple[str, float], ...]
    n_rows: int
    n_days: int
    fit_start: str
    fit_end: str

    @property
    def digest(self) -> str:
        payload = json.dumps(
            {
                "intercept": round(self.intercept, 12),
                "coefficients": [[n, round(c, 12)] for n, c in self.coefficients],
                "fit_start": self.fit_start,
                "fit_end": self.fit_end,
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()

    def score(self, features: dict[str, float]) -> float:
        z = self.intercept + sum(c * features[n] for n, c in self.coefficients)
        return 1.0 / (1.0 + math.exp(-z)) if z > -700 else 0.0


def load_fit_targets(dates: Sequence[str], horizon: int) -> dict[tuple[str, str], float]:
    """Forward returns for the fit period only.

    Refuses any date on or after the window start. The refusal is here rather
    than at the call site because a baseline that could reach a window outcome
    would be the whole experiment leaking through its cheapest component.
    """
    last_allowed = _last_pre_window_date()
    bad = [d for d in dates if d > last_allowed]
    if bad:
        raise PermissionError(
            f"the logistic fit asked for {len(bad)} dates after {last_allowed}, which is "
            f"the last date strictly before the window start. Refused. First was {bad[0]}."
        )
    if not FIT_RETURNS_DB.exists():
        raise FileNotFoundError(f"fit returns store missing: {FIT_RETURNS_DB}")
    con = sqlite3.connect(f"file:{FIT_RETURNS_DB}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT date, symbol, ret FROM forward_return WHERE horizon = ? AND ret IS NOT NULL",
            (horizon,),
        ).fetchall()
    finally:
        con.close()
    wanted = set(dates)
    return {(r[0], r[1]): float(r[2]) for r in rows if r[0] in wanted}


def _last_pre_window_date() -> str:
    """The latest date the fit may use.

    The window starts at the first session strictly after the guard band, so the
    guard band end is the last calendar date that is unambiguously outside the
    window. Expressed without the session calendar on purpose, so this refusal
    holds even when the calendar is unavailable.
    """
    from npd.window import guard_band_end

    return guard_band_end(CONFIG.knowledge_cutoff, CONFIG.guard_band_months).isoformat()


def fit_logistic(
    rows: Sequence[tuple[str, dict[str, float], int]],
    cfg: Config = CONFIG,
    *,
    max_iter: int = 500,
) -> FittedLogistic:
    """Fit on (date, feature block, label) rows. Label is 1 above the day median.

    Uses scikit-learn's LBFGS solver with the default L2 penalty. The solver is
    named here because a baseline whose optimizer is unstated cannot be
    replicated.
    """
    import numpy as np
    from sklearn.linear_model import LogisticRegression

    names = list(cfg.feature_names)
    x = np.array([[block[n] for n in names] for _d, block, _y in rows], dtype=float)
    y = np.array([label for _d, _b, label in rows], dtype=int)
    if len(set(y.tolist())) < 2:
        raise ValueError("the fit sample has only one class")

    model = LogisticRegression(max_iter=max_iter, solver="lbfgs")
    model.fit(x, y)
    dates = sorted({d for d, _b, _y in rows})
    return FittedLogistic(
        intercept=float(model.intercept_[0]),
        coefficients=tuple(zip(names, (float(c) for c in model.coef_[0]), strict=True)),
        n_rows=len(rows),
        n_days=len(dates),
        fit_start=dates[0],
        fit_end=dates[-1],
    )


def rank_logistic(fitted: FittedLogistic, blocks: dict[str, dict[str, float]]) -> list[str]:
    """Symbols best to worst by fitted probability of an above-median return."""
    scored = {sym: fitted.score(block) for sym, block in blocks.items()}
    return [s for s, _ in sorted(scored.items(), key=lambda kv: (-kv[1], kv[0]))]


def save(con: sqlite3.Connection, fitted: FittedLogistic) -> None:
    con.execute("DELETE FROM logistic_coefficient")
    con.executemany(
        "INSERT INTO logistic_coefficient(name, coef) VALUES(?,?)",
        [("__intercept__", fitted.intercept), *fitted.coefficients],
    )
    from npd.data.store import set_meta

    set_meta(con, "logistic.digest", fitted.digest)
    set_meta(con, "logistic.n_rows", str(fitted.n_rows))
    set_meta(con, "logistic.n_days", str(fitted.n_days))
    set_meta(con, "logistic.fit_start", fitted.fit_start)
    set_meta(con, "logistic.fit_end", fitted.fit_end)


def load(con: sqlite3.Connection, cfg: Config = CONFIG) -> FittedLogistic:
    rows = {r[0]: float(r[1]) for r in con.execute("SELECT name, coef FROM logistic_coefficient")}
    if not rows:
        raise RuntimeError("the logistic baseline has not been fitted")
    from npd.data.store import get_meta

    return FittedLogistic(
        intercept=rows.pop("__intercept__"),
        coefficients=tuple((n, rows[n]) for n in cfg.feature_names),
        n_rows=int(get_meta(con, "logistic.n_rows") or 0),
        n_days=int(get_meta(con, "logistic.n_days") or 0),
        fit_start=get_meta(con, "logistic.fit_start") or "",
        fit_end=get_meta(con, "logistic.fit_end") or "",
    )
