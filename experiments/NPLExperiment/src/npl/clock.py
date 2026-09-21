"""The only source of wall-clock time. UTC, injectable for tests."""

from __future__ import annotations

from datetime import UTC, date, datetime

MS_PER_HOUR = 3_600_000
MS_PER_DAY = 86_400_000


def now_utc() -> datetime:
    return datetime.now(UTC)


def utc_ms(moment: datetime) -> int:
    if moment.tzinfo is None:
        raise ValueError("refusing a naive datetime; every timestamp here is UTC-aware")
    return int(moment.timestamp() * 1000)


def ms_to_utc(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000, tz=UTC)


def utc_date_of_ms(ms: int) -> date:
    return ms_to_utc(ms).date()


def iso_z(moment: datetime) -> str:
    if moment.tzinfo is None:
        raise ValueError("refusing a naive datetime; every timestamp here is UTC-aware")
    return moment.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
