"""Union time intervals before summing. A standing rule, defect-earned.

Three separate parent-project defects came from summing a list of windows
without merging first: a list, a sum(), no union. It never raises; it silently
returns a number too large. Every interval computation in this repository goes
through merge_windows, and any new interval arithmetic carries a test with at
least one overlapping pair.
"""

from __future__ import annotations


def merge_windows(windows: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Union half-open [start, end) millisecond windows. Inverted windows raise."""
    for start, end in windows:
        if end < start:
            raise ValueError(f"inverted window [{start}, {end}): refusing to drop it silently")
    ordered = sorted(w for w in windows if w[1] > w[0])
    merged: list[tuple[int, int]] = []
    for start, end in ordered:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def total_covered_ms(windows: list[tuple[int, int]]) -> int:
    """Total covered milliseconds, unioned before summing."""
    return sum(end - start for start, end in merge_windows(windows))
