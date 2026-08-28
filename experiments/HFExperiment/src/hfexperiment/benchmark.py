"""The benchmark. The equal-weighted mean daily return of the formation
universe membership.

Source of the definition, cited per the B.1 stage prompt. REGISTRATION.md
Section 1 registers the hypothesis against "the equal-weighted
universe", the benchmark the recorded cross-sectional round of
2026-07-26 ran and the one that produced the recorded 27.99 bp per day
at width 5 (Section 4 table, row width 5). The construction: membership
is fixed at each formation by rule U-LIQ-500-stk-w60-m40-p5 (Section
3), and each session's benchmark return is the arithmetic mean of the
members' close-to-close returns. The mean weights every member
identically every session, which is what equal-weighted means here:
daily rebalanced by construction, not drifting.

Member states follow Section 3 exactly as book names do. A halted or
delisted member marks at its last available close, contributes zero
return, and leaves at the next formation. A member with a missing bar
or failed source excludes the day for every width, because a mean over
a silently shrunken membership is a different benchmark. The exclusion
is recorded and retried, shadow.py enforces the refusal.
"""
from __future__ import annotations

from collections.abc import Mapping


def benchmark_daily_return(member_returns: Mapping[str, float]) -> float:
    """The arithmetic mean over the full fixed membership.

    The input is the complete membership's returns for one session, as
    produced by shadow.advance_panel: computed members carry real
    returns, marked members carry exactly zero. An empty membership is
    a construction error, not a zero.
    """
    if not member_returns:
        raise ValueError("benchmark over an empty membership")
    return sum(member_returns.values()) / len(member_returns)
