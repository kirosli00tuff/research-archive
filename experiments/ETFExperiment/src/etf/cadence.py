"""The registered snapshot cadence (A.1 Task 3, promoted at A.3 Task 1).

Every 20 minutes across 20:00 to 14:00 UTC, the window that brackets the print
and the revision window, and every 2 hours otherwise, subject to the A.1 Task 2
measured pace and the recorded terms of service.

The peak window wraps midnight, so the membership test is a disjunction rather
than a range. Getting that backwards would sample the print window at the
off-peak rate and understate the first-print time by up to two hours, which is
the one figure this repository turns on.
"""

from __future__ import annotations

from datetime import datetime

from etf.config import CONFIG


def in_peak_window(moment: datetime) -> bool:
    """True inside the wrapping 20:00-14:00 UTC print-and-revision window."""
    if moment.tzinfo is None:
        raise ValueError("refusing a naive datetime; every timestamp here is UTC-aware")
    hour = moment.hour
    start = CONFIG.snapshot_peak_start_hour_utc
    end = CONFIG.snapshot_peak_end_hour_utc
    if start <= end:
        return start <= hour < end
    return hour >= start or hour < end


def interval_seconds(moment: datetime) -> int:
    """The registered spacing between captures at this moment."""
    if in_peak_window(moment):
        return CONFIG.snapshot_peak_interval_minutes * 60
    return CONFIG.snapshot_offpeak_interval_hours * 3600
