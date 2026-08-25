"""The nine registered features and the cross-sectional z-score.

Nothing here carries a value forward. A symbol missing any bar in a feature's
trailing span produces a recorded absence, not an interpolated number. That is
the standing rule from npd.absence, and tests/test_absence.py fails the moment
a synthesized value appears.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import pairwise

from npd.absence import (
    INSUFFICIENT_HISTORY,
    NO_BAR,
    NON_FINITE,
    ZERO_DENOMINATOR,
    Absent,
    Maybe,
)
from npd.config import CONFIG

RETURN_LOOKBACKS = (1, 5, 10, 20, 60)
RVOL_LOOKBACKS = (20, 60)
DVOL_LOOKBACK = 60
VTREND_SHORT = 5
VTREND_LONG = 60

# The longest trailing span any feature needs. A symbol without this many
# consecutive sessions of bars cannot produce a full block.
MAX_LOOKBACK = 60


@dataclass(frozen=True, slots=True)
class Series:
    """One symbol's close and volume aligned to the session calendar.

    `close[i]` and `volume[i]` are None when the symbol had no bar on
    `sessions[i]`. None is an absence, and every function here treats it as one.
    """

    symbol: str
    close: tuple[float | None, ...]
    volume: tuple[float | None, ...]


def _span(values: Sequence[float | None], t: int, n: int) -> list[float] | Absent:
    """The n values ending at index t, or a recorded absence.

    Requires every session in the span to carry a bar. A hole is not filled.
    """
    start = t - n + 1
    if start < 0:
        return INSUFFICIENT_HISTORY
    out: list[float] = []
    for i in range(start, t + 1):
        v = values[i]
        if v is None:
            return NO_BAR
        if not math.isfinite(v):
            return NON_FINITE
        out.append(v)
    return out


def trailing_return(s: Series, t: int, k: int) -> Maybe[float]:
    """close[t] / close[t-k] - 1."""
    span = _span(s.close, t, k + 1)
    if isinstance(span, Absent):
        return span
    base = span[0]
    if base <= 0.0:
        return ZERO_DENOMINATOR
    value = span[-1] / base - 1.0
    return value if math.isfinite(value) else NON_FINITE


def realized_vol(s: Series, t: int, n: int) -> Maybe[float]:
    """Sample standard deviation of the last n close-to-close log returns."""
    span = _span(s.close, t, n + 1)
    if isinstance(span, Absent):
        return span
    rets: list[float] = []
    for prev, cur in pairwise(span):
        if prev <= 0.0 or cur <= 0.0:
            return ZERO_DENOMINATOR
        rets.append(math.log(cur / prev))
    mean = sum(rets) / len(rets)
    var = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
    value = math.sqrt(var)
    return value if math.isfinite(value) else NON_FINITE


def dollar_volume_z(s: Series, t: int, n: int = DVOL_LOOKBACK) -> Maybe[float]:
    """Today's dollar volume as a z-score inside the symbol's own trailing n."""
    closes = _span(s.close, t, n)
    if isinstance(closes, Absent):
        return closes
    volumes = _span(s.volume, t, n)
    if isinstance(volumes, Absent):
        return volumes
    dv = [c * v for c, v in zip(closes, volumes, strict=True)]
    mean = sum(dv) / len(dv)
    var = sum((x - mean) ** 2 for x in dv) / (len(dv) - 1)
    sd = math.sqrt(var)
    if sd <= 0.0:
        return ZERO_DENOMINATOR
    value = (dv[-1] - mean) / sd
    return value if math.isfinite(value) else NON_FINITE


def volume_trend(
    s: Series, t: int, short: int = VTREND_SHORT, long: int = VTREND_LONG
) -> Maybe[float]:
    """Mean volume over the short span divided by mean volume over the long span."""
    volumes = _span(s.volume, t, long)
    if isinstance(volumes, Absent):
        return volumes
    long_mean = sum(volumes) / len(volumes)
    if long_mean <= 0.0:
        return ZERO_DENOMINATOR
    short_mean = sum(volumes[-short:]) / short
    value = short_mean / long_mean
    return value if math.isfinite(value) else NON_FINITE


def raw_block(s: Series, t: int) -> dict[str, Maybe[float]]:
    """Every registered feature for one symbol on one session."""
    out: dict[str, Maybe[float]] = {}
    for k in RETURN_LOOKBACKS:
        out[f"ret_{k}"] = trailing_return(s, t, k)
    for n in RVOL_LOOKBACKS:
        out[f"rvol_{n}"] = realized_vol(s, t, n)
    out["dvol_z_60"] = dollar_volume_z(s, t)
    out["vtrend_5_60"] = volume_trend(s, t)
    missing = set(CONFIG.feature_names) - set(out)
    if missing:
        raise RuntimeError(f"registered features not computed: {sorted(missing)}")
    extra = set(out) - set(CONFIG.feature_names)
    if extra:
        raise RuntimeError(f"unregistered features computed: {sorted(extra)}")
    return out


def is_complete(block: dict[str, Maybe[float]]) -> bool:
    """True when every registered feature is present. Eligibility, not quality."""
    return all(not isinstance(block[name], Absent) for name in CONFIG.feature_names)


def cross_sectional_z(
    blocks: dict[str, dict[str, float]], feature_names: Sequence[str]
) -> dict[str, dict[str, float]]:
    """Z-score each feature across the symbols presented on one day.

    The panel handed to the model is the population, so the mean and standard
    deviation are taken across exactly the rows the model sees. A feature with
    zero cross-sectional spread would divide by zero, so it raises rather than
    returning a fabricated zero.
    """
    symbols = sorted(blocks)
    out: dict[str, dict[str, float]] = {s: {} for s in symbols}
    for name in feature_names:
        values = [blocks[s][name] for s in symbols]
        mean = sum(values) / len(values)
        var = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
        sd = math.sqrt(var)
        if sd <= 0.0:
            raise ValueError(f"feature {name} has zero cross-sectional spread")
        for s, v in zip(symbols, values, strict=True):
            out[s][name] = (v - mean) / sd
    return out
