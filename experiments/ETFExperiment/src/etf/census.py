"""A.2 Task 1: the admissible-day census.

Every US trading day from the registered out-of-sample start to the census
date, with its admissibility under Section 3, the source of the as-printed
value, the capture timestamp, the revised flag, and the exclusion reason where
inadmissible.

**Flow fields and timestamps only. No price field is touched, and no module
imported here can read one.** The trading-day universe is the flow source's own
date rows, which is what Section 2 defines an event day as, measured rather
than assumed from a hardcoded holiday calendar.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date, datetime

from etf.absence import Absent
from etf.archive import Memento
from etf.callstate import CallState
from etf.snapshot import DayRow


class AdmissibilitySource:
    """How an admissible day's as-printed value was obtained."""

    RETRO_ARCHIVE = "retro_archive"
    FORWARD_CAPTURE = "forward_capture"


@dataclass(frozen=True, slots=True)
class CensusRow:
    trade_date: date
    admissible: bool
    state: CallState
    source: str | None
    capture_timestamp: datetime | None
    revised: bool
    exclusion_reason: str | None
    printed_signal_present: bool

    def as_ledger_dict(self) -> dict[str, object]:
        return {
            "trade_date": self.trade_date.isoformat(),
            "admissible": self.admissible,
            "state": self.state.value,
            "source": self.source,
            "capture_timestamp": (
                self.capture_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
                if self.capture_timestamp
                else None
            ),
            "revised": self.revised,
            "exclusion_reason": self.exclusion_reason,
            "printed_signal_present": self.printed_signal_present,
        }


def build_census(
    day_rows: Sequence[DayRow],
    *,
    oos_start: date,
    census_date: date,
    archive_windows: dict[date, tuple[datetime, datetime]],
    mementos: Iterable[Memento],
    forward_captures: dict[date, datetime],
    revised_days: frozenset[date],
) -> tuple[CensusRow, ...]:
    """One row per date the flow source serves inside the window. Nothing is imputed."""
    ordered = sorted(mementos, key=lambda m: m.captured_at)
    rows: list[CensusRow] = []
    for day in day_rows:
        if not (oos_start <= day.trade_date <= census_date):
            continue
        printed = not isinstance(day.signal_usd, Absent)
        if not printed:
            rows.append(
                CensusRow(
                    trade_date=day.trade_date,
                    admissible=False,
                    state=CallState.EXCLUDED_INELIGIBLE,
                    source=None,
                    capture_timestamp=None,
                    revised=False,
                    exclusion_reason="no_printed_value",
                    printed_signal_present=False,
                )
            )
            continue

        forward = forward_captures.get(day.trade_date)
        if forward is not None:
            rows.append(
                CensusRow(
                    trade_date=day.trade_date,
                    admissible=True,
                    state=CallState.STORED,
                    source=AdmissibilitySource.FORWARD_CAPTURE,
                    capture_timestamp=forward,
                    revised=day.trade_date in revised_days,
                    exclusion_reason=None,
                    printed_signal_present=True,
                )
            )
            continue

        window = archive_windows.get(day.trade_date)
        qualifying = (
            [m for m in ordered if window[0] <= m.captured_at < window[1]] if window else []
        )
        if qualifying:
            rows.append(
                CensusRow(
                    trade_date=day.trade_date,
                    admissible=True,
                    state=CallState.STORED,
                    source=AdmissibilitySource.RETRO_ARCHIVE,
                    # The value the registered rule would have read is the LAST
                    # capture strictly before the anchor, not the first.
                    capture_timestamp=qualifying[-1].captured_at,
                    revised=day.trade_date in revised_days,
                    exclusion_reason=None,
                    printed_signal_present=True,
                )
            )
            continue

        later = window is not None and any(m.captured_at >= window[1] for m in ordered)
        rows.append(
            CensusRow(
                trade_date=day.trade_date,
                admissible=False,
                state=CallState.EXCLUDED_INELIGIBLE,
                source=None,
                capture_timestamp=None,
                revised=False,
                exclusion_reason="capture_too_late" if later else "no_capture",
                printed_signal_present=True,
            )
        )
    return tuple(rows)
