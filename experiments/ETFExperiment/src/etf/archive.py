"""A.1 Task 4, retro leg: archive capture density, measured from the timemap.

A retro day is admissible only if an archive capture strictly before the entry
anchor serves a flow value for that day (Section 3.3). The qualifying window is
bounded below by the registered snapshot peak-window start — 20:00 UTC on day
D, which is when the US close the print follows has happened — and above by the
entry anchor. Both bounds come from registered constants; neither is a new
number invented here.

Nothing in this module reads a price. It reads capture timestamps.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from email.utils import parsedate_to_datetime

from etf.anchor import entry_anchor
from etf.config import CONFIG

_LINK = re.compile(
    r'<(?P<url>[^>]+)>\s*;\s*rel="(?P<rel>[^"]+)"(?:[^,]*?datetime="(?P<dt>[^"]+)")?'
)


class TimemapShape(RuntimeError):
    """The timemap did not parse as RFC 7089 link-format."""


@dataclass(frozen=True, slots=True)
class Memento:
    captured_at: datetime
    url: str


@dataclass(frozen=True, slots=True)
class DayArchive:
    trade_date: date
    window_start: datetime
    window_end: datetime
    qualifying: tuple[Memento, ...]

    @property
    def admissible(self) -> bool:
        return bool(self.qualifying)

    @property
    def reason(self) -> str | None:
        """Why the day is inadmissible. The two reasons never merge."""
        if self.qualifying:
            return None
        return "no_capture"


@dataclass(frozen=True, slots=True)
class DensityReport:
    days: tuple[DayArchive, ...]
    n_trading_days: int
    admissible_days: int
    admissible_share: float | None
    no_capture_days: int
    capture_too_late_days: int
    total_mementos: int
    first_memento: datetime | None
    last_memento: datetime | None


def parse_timemap(payload: bytes | str) -> tuple[Memento, ...]:
    """Every memento in an RFC 7089 link-format timemap, ordered by clock."""
    text = payload.decode("utf-8", "replace") if isinstance(payload, bytes) else payload
    mementos: list[Memento] = []
    for match in _LINK.finditer(text):
        rel = match.group("rel")
        stamp = match.group("dt")
        if "memento" not in rel.split() or stamp is None:
            continue
        try:
            moment = parsedate_to_datetime(stamp)
        except (TypeError, ValueError) as exc:
            raise TimemapShape(f"unparseable memento datetime {stamp!r}: {exc}") from exc
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=UTC)
        mementos.append(Memento(captured_at=moment.astimezone(UTC), url=match.group("url")))
    return tuple(sorted(mementos, key=lambda m: m.captured_at))


def qualifying_window(trade_day: date) -> tuple[datetime, datetime]:
    """[D at the peak-window start, the entry anchor on D+1). Both registered."""
    start = datetime.combine(trade_day, datetime.min.time(), tzinfo=UTC).replace(
        hour=CONFIG.snapshot_peak_start_hour_utc
    )
    return start, entry_anchor(trade_day)


def density(trading_days: Sequence[date], mementos: Iterable[Memento]) -> DensityReport:
    """Per trading day, whether a capture lands strictly inside the qualifying window."""
    ordered = sorted(mementos, key=lambda m: m.captured_at)
    days: list[DayArchive] = []
    too_late = 0
    for trade_day in trading_days:
        start, end = qualifying_window(trade_day)
        inside = tuple(m for m in ordered if start <= m.captured_at < end)
        # A capture that exists for the day but lands at or after the anchor is
        # a different fact from no capture at all, and the two never merge.
        after = any(end <= m.captured_at < end + timedelta(days=1) for m in ordered)
        if not inside and after:
            too_late += 1
        days.append(
            DayArchive(trade_date=trade_day, window_start=start, window_end=end, qualifying=inside)
        )
    admissible = sum(1 for d in days if d.admissible)
    n = len(days)
    no_capture = n - admissible - too_late
    return DensityReport(
        days=tuple(days),
        n_trading_days=n,
        admissible_days=admissible,
        admissible_share=(admissible / n) if n else None,
        no_capture_days=no_capture,
        capture_too_late_days=too_late,
        total_mementos=len(ordered),
        first_memento=ordered[0].captured_at if ordered else None,
        last_memento=ordered[-1].captured_at if ordered else None,
    )
