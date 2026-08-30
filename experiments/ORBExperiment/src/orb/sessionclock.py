"""Guard 7 — the session clock. DST-aware Eastern, never a fixed UTC offset.

The opening range is anchored to 09:30:00 America/New_York. That instant is
13:30 UTC under daylight time and 14:30 UTC under standard time. A fixed UTC
offset therefore mis-slices roughly a third of any multi-year sample — every
session between the March and November transitions under a winter offset, and
every session outside them under a summer offset — and it does so **silently**,
producing a range taken from the wrong five minutes rather than an error.

Every function here refuses a naive datetime. There is no code path in this
repository that produces an Eastern wall-clock time without going through
:data:`EASTERN`.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from typing import Final
from zoneinfo import ZoneInfo

EASTERN: Final[ZoneInfo] = ZoneInfo("America/New_York")
"""The one Eastern zone in this repository. DST-aware by construction."""

REGULAR_OPEN: Final[time] = time(9, 30, 0)
"""09:30:00 Eastern. The first instant of the regular session."""

OPENING_RANGE_END: Final[time] = time(9, 34, 59, 999_000)
"""09:34:59.999 Eastern. The last instant inside the 5-minute opening range."""

EVALUATION_TIME: Final[time] = time(9, 35, 0)
"""09:35:00 Eastern. Selection is evaluated here, per Section 2."""

REGULAR_CLOSE: Final[time] = time(16, 0, 0)
"""16:00:00 Eastern on a full session."""

HALF_SESSION_CLOSE: Final[time] = time(13, 0, 0)
"""13:00:00 Eastern on a half session. Half sessions are excluded and counted."""

CLOSE_EXIT_START: Final[time] = time(15, 55, 0)
"""15:55:00 Eastern. The exit window opens, per Section 3."""

CLOSE_EXIT_END: Final[time] = time(15, 59, 0)
"""15:59:00 Eastern. The exit window closes, per Section 3."""


class NaiveDatetimeError(ValueError):
    """Raised whenever a datetime without a tzinfo reaches the session clock."""


class FixedOffsetEasternError(ValueError):
    """Raised when an Eastern instant is built on a fixed offset rather than a zone."""


def require_aware(moment: datetime, context: str) -> datetime:
    """Refuse a naive datetime, loudly, at the boundary."""
    if moment.tzinfo is None or moment.tzinfo.utcoffset(moment) is None:
        raise NaiveDatetimeError(
            f"{context}: refusing a naive datetime {moment!r}. Every timestamp "
            "in this repository carries a zone; a naive one silently adopts "
            "whatever the host clock is set to."
        )
    return moment


def require_dst_aware_eastern(moment: datetime, context: str) -> datetime:
    """Refuse an Eastern instant that was built on a fixed offset."""
    require_aware(moment, context)
    if not isinstance(moment.tzinfo, ZoneInfo):
        raise FixedOffsetEasternError(
            f"{context}: refusing tzinfo {moment.tzinfo!r}. An Eastern instant "
            "must carry a DST-aware ZoneInfo; a fixed offset mis-slices the "
            "opening range on roughly a third of the sample, silently."
        )
    if str(moment.tzinfo) != "America/New_York":
        raise FixedOffsetEasternError(
            f"{context}: refusing zone {moment.tzinfo!r}; expected America/New_York."
        )
    return moment


def eastern_instant(session: date, wall: time) -> datetime:
    """Build the UTC-resolvable instant for an Eastern wall-clock time."""
    return datetime.combine(session, wall, tzinfo=EASTERN)


def to_utc(moment: datetime, context: str = "to_utc") -> datetime:
    """Convert an aware instant to UTC. A naive instant is refused."""
    return require_aware(moment, context).astimezone(UTC)


def session_open_utc(session: date) -> datetime:
    """09:30:00 Eastern on ``session``, in UTC."""
    return to_utc(eastern_instant(session, REGULAR_OPEN), "session_open_utc")


def opening_range_window_utc(session: date) -> tuple[datetime, datetime]:
    """The half-open UTC window ``[09:30:00.000, 09:35:00.000)`` Eastern."""
    start = eastern_instant(session, REGULAR_OPEN)
    end = eastern_instant(session, EVALUATION_TIME)
    return to_utc(start, "opening_range_start"), to_utc(end, "opening_range_end")


def evaluation_instant_utc(session: date) -> datetime:
    """09:35:00 Eastern on ``session``, in UTC. Selection is evaluated here."""
    return to_utc(eastern_instant(session, EVALUATION_TIME), "evaluation_instant_utc")


def close_exit_window_utc(
    session: date, *, half_session: bool = False
) -> tuple[datetime, datetime]:
    """The registered close-exit window, shifted three hours on a half session."""
    if half_session:
        shift = timedelta(hours=3)
        start = eastern_instant(session, CLOSE_EXIT_START) - shift
        end = eastern_instant(session, CLOSE_EXIT_END) - shift
    else:
        start = eastern_instant(session, CLOSE_EXIT_START)
        end = eastern_instant(session, CLOSE_EXIT_END)
    return to_utc(start, "close_exit_start"), to_utc(end, "close_exit_end")


def utc_offset_minutes(session: date) -> int:
    """The Eastern UTC offset in minutes. -240 in summer, -300 in winter."""
    offset = eastern_instant(session, REGULAR_OPEN).utcoffset()
    if offset is None:  # pragma: no cover - ZoneInfo always supplies one
        raise FixedOffsetEasternError(f"no UTC offset resolvable for {session}")
    return int(offset.total_seconds() // 60)


def is_daylight_time(session: date) -> bool:
    """True when ``session`` falls inside US Eastern daylight time."""
    return utc_offset_minutes(session) == -240
