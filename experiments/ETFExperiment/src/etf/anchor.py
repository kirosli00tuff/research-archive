"""Section 3: the print, the entry anchor, and admissibility.

This is the section the repository turns on, so its rule lives in one module
with one enforcement site.

The as-printed value for US trading day D is the aggregate net flow for D as
served by the flow source in a capture **strictly before** the entry anchor.
The value taken is the one in that capture. A later value for the same day,
however authoritative, is never substituted; where the two differ the day is
flagged `revised` and the difference recorded.

The entry anchor is registered provisionally at 08:00 UTC on day D+1. A.1 Task
3 measures the distribution of first-print times. If the measured 95th
percentile first-print time falls later than 07:00 UTC, the anchor moves to the
next whole hour after that percentile, by amendment, before any outcome read
and before any admissibility count is final. No other input moves the anchor.
"""

from __future__ import annotations

import math
from datetime import UTC, date, datetime, timedelta

from etf.config import CONFIG


class AnchorAmendmentRefused(RuntimeError):
    """An anchor move was requested by something other than the registered rule."""


def out_of_sample_start() -> date:
    """The first US trading day of the test sample. Everything before it is pre-period."""
    return date.fromisoformat(CONFIG.oos_start_date)


def entry_anchor(trade_day: date, anchor_hour_utc: int = CONFIG.entry_anchor_hour_utc) -> datetime:
    """The anchor for US trading day D: `anchor_hour` UTC on D+1."""
    return datetime.combine(trade_day + timedelta(days=1), datetime.min.time(), tzinfo=UTC).replace(
        hour=anchor_hour_utc
    )


def is_admissible_capture(
    capture_ts: datetime,
    trade_day: date,
    anchor_hour_utc: int = CONFIG.entry_anchor_hour_utc,
) -> bool:
    """A capture qualifies only if it lands **strictly before** the anchor.

    Strict, and the tests sit exactly on the boundary: a capture at
    07:59:59Z on D+1 qualifies and one at 08:00:00Z does not. A fixture
    comfortably inside its boundary lets a moved threshold pass unnoticed.
    """
    if capture_ts.tzinfo is None:
        raise ValueError("refusing a naive capture timestamp; every timestamp here is UTC-aware")
    return capture_ts < entry_anchor(trade_day, anchor_hour_utc)


def percentile(values: list[float], q: float) -> float:
    """Nearest-rank percentile. Deterministic, no interpolation, no numpy."""
    if not values:
        raise ValueError("percentile of an empty sample is an absence, not a number")
    if not 0.0 < q <= 1.0:
        raise ValueError(f"percentile q must be in (0, 1], got {q}")
    ordered = sorted(values)
    rank = max(1, math.ceil(q * len(ordered)))
    return ordered[rank - 1]


def amended_anchor_hour(first_print_hours_utc: list[float]) -> int:
    """The Section 3 anchor amendment rule, and the only permitted anchor movement.

    Takes the measured first-print times of each trading day, expressed as
    fractional hours past midnight UTC on D+1. If the measured 95th percentile
    falls at or before the 07:00 UTC trigger, the provisional 08:00 anchor
    stands. Otherwise the anchor moves to the next whole hour strictly after
    that percentile.
    """
    p = percentile(first_print_hours_utc, CONFIG.anchor_amendment_percentile)
    if p <= CONFIG.anchor_amendment_trigger_hour_utc:
        return CONFIG.entry_anchor_hour_utc
    return math.floor(p) + 1
