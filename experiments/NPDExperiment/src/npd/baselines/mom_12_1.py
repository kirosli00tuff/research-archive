"""Baseline two. 12-1 momentum.

Trailing twelve-month return excluding the most recent month. The exclusion is
the whole point of the factor: the last month reverses, the eleven before it
persist. Computed from the same bar series and with the same absence discipline
as the features, so a name missing a bar in the span produces a recorded
absence rather than a filled number.
"""

from __future__ import annotations

import math

from npd.absence import NO_BAR, ZERO_DENOMINATOR, Absent, Maybe
from npd.data.features import Series

MOM_12_1 = "mom_12_1"

# Sessions, not calendar months. Twenty-one sessions is about one month and 252
# is about twelve.
SKIP_SESSIONS = 21
LOOKBACK_SESSIONS = 252


def momentum_12_1(s: Series, t: int) -> Maybe[float]:
    """close[t - 21] / close[t - 252] - 1."""
    end = t - SKIP_SESSIONS
    start = t - LOOKBACK_SESSIONS
    if start < 0:
        from npd.absence import INSUFFICIENT_HISTORY

        return INSUFFICIENT_HISTORY
    base = s.close[start]
    tip = s.close[end]
    if base is None or tip is None:
        return NO_BAR
    if base <= 0.0:
        return ZERO_DENOMINATOR
    value = tip / base - 1.0
    if not math.isfinite(value):
        from npd.absence import NON_FINITE

        return NON_FINITE
    return value


def rank_mom_12_1(momentum_by_symbol: dict[str, Maybe[float]]) -> list[str]:
    """Symbols best to worst by 12-1 momentum.

    An absent value cannot be ranked, so it raises. Panel eligibility already
    requires a complete 12-1 span, which is what keeps this branch unreachable
    in the built pipeline and loud if that ever changes.
    """
    present: dict[str, float] = {}
    for sym, value in momentum_by_symbol.items():
        if isinstance(value, Absent):
            raise ValueError(f"{sym} has absent 12-1 momentum ({value.reason.value})")
        present[sym] = value
    return [s for s, _ in sorted(present.items(), key=lambda kv: (-kv[1], kv[0]))]
