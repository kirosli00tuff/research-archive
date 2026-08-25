"""Baseline one. Sign of the last one-session return.

The cheapest thing that could work. Ranks the panel by yesterday's return,
best first. If the model cannot beat this it has not earned its price.
"""

from __future__ import annotations

SIGN_LAST = "sign_last"


def rank_sign_last(ret_1_by_symbol: dict[str, float]) -> list[str]:
    """Symbols best to worst by last one-session return.

    Ties break on symbol ascending, so the ranking is deterministic.
    """
    return [s for s, _ in sorted(ret_1_by_symbol.items(), key=lambda kv: (-kv[1], kv[0]))]
