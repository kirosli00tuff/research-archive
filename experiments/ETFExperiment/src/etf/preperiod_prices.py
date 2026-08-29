"""The pre-period carve-out's price reader. The ONLY module that reads a close.

Registered in REGISTRATION.md Section 9 and stated in CLAUDE.md: **power inputs
may read BTC price and funding data stamped strictly before 2025-05-01**, which
sits inside the source study's own sample (January 2024 through April 2025) and
outside this test sample (which begins 2025-05-01). Reading it cannot leak a
single observation the Stage B verdict will be computed on.

Every other price read in this repository is sealed. This module exists so the
carve-out has exactly one address, and `tests/test_guards.py` pins it there:

- it is the only file on `PRE_PERIOD_PRICE_ALLOWED_FILES`;
- it must call `require_pre_period` on the parse tree, so an inlined comparison
  fails the guard;
- it must not import the network layer, so it cannot decide its own window.

**The refusal is loud and total.** A payload carrying one row stamped at or
after the boundary raises; nothing is dropped quietly and no partial series is
returned, because a silently truncated volatility series is a synthesized one.
"""

from __future__ import annotations

import itertools
import json
import math
import statistics
from dataclasses import dataclass

from etf.preperiod import require_pre_period

# The three fields this module may read, and the only place `c` is named in the
# repository outside the sealed writers, which parse nothing at all.
ALLOWED_PRE_PERIOD_FIELDS: tuple[str, ...] = ("t", "T", "c")


class PrePeriodPayloadShape(RuntimeError):
    """The candle payload is not the shape the pre-period reader was registered against."""


@dataclass(frozen=True, slots=True)
class PrePeriodClose:
    open_ms: int
    close_ms: int
    close: float


def pre_period_closes(payload: bytes | str) -> tuple[PrePeriodClose, ...]:
    """Parse closes from a candle payload wholly inside the carve-out.

    Raises `PrePeriodViolation` on the first row stamped at or after the
    registered boundary. It does not skip such a row: a caller that hands this
    reader a window straddling the boundary has made an error the registration
    cannot absorb, and a half-served series would hide it.
    """
    parsed = json.loads(payload)
    if not isinstance(parsed, list):
        raise PrePeriodPayloadShape(
            f"candle payload is not a list: {type(parsed).__name__}. Refusing to guess."
        )
    rows: list[PrePeriodClose] = []
    for row in parsed:
        if not isinstance(row, dict):
            raise PrePeriodPayloadShape("candle row is not an object; refusing to guess")
        close_ms = int(row["T"])
        require_pre_period(close_ms, "pre-period price reader (Section 9 carve-out)")
        rows.append(PrePeriodClose(open_ms=int(row["t"]), close_ms=close_ms, close=float(row["c"])))
    if not rows:
        raise PrePeriodPayloadShape(
            "the payload carried no candle rows; an empty volatility input is an absence"
        )
    return tuple(rows)


@dataclass(frozen=True, slots=True)
class PrePeriodVolatility:
    n_returns: int
    daily_sd: float
    first_close_ms: int
    last_close_ms: int


def daily_volatility(closes: tuple[PrePeriodClose, ...]) -> PrePeriodVolatility:
    """Sample standard deviation of consecutive log returns. Every figure carries its n."""
    if len(closes) < 3:
        raise PrePeriodPayloadShape(
            f"a volatility needs at least 3 closes; {len(closes)} were served. "
            "Report the absence rather than a number computed on two points."
        )
    ordered = sorted(closes, key=lambda c: c.close_ms)
    returns = [
        math.log(b.close / a.close)
        for a, b in itertools.pairwise(ordered)
        if a.close > 0 and b.close > 0
    ]
    if len(returns) < 2:
        raise PrePeriodPayloadShape("fewer than two usable returns; refusing to report a sd")
    return PrePeriodVolatility(
        n_returns=len(returns),
        daily_sd=statistics.stdev(returns),
        first_close_ms=ordered[0].close_ms,
        last_close_ms=ordered[-1].close_ms,
    )
