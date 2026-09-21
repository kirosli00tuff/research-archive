"""H5 Task 3: the retrospective deviation reader, its gate, and its absences."""

from __future__ import annotations

import json

import pytest

from npl.absence import Absent, is_absent
from npl.blindness import DEVIATION_FIELD, deviation_rows
from npl.callstate import CallState
from npl.config import CONFIG
from npl.h5 import retro as h5retro
from npl.h5.calendar import TAG_REGULAR, TAG_WEEKEND
from npl.h5.gate import Cohorts, H5RetrospectiveGated
from npl.venue import FetchOutcome

HOUR_MS = 3_600_000


def _row(time_ms: int, premium: str | None) -> dict[str, object]:
    row: dict[str, object] = {"coin": "xyz:GOOGL", "fundingRate": "0.0000125", "time": time_ms}
    if premium is not None:
        row[DEVIATION_FIELD] = premium
    return row


def test_the_deviation_reader_takes_time_and_premium_and_nothing_else() -> None:
    payload = json.dumps([_row(1_780_000_000_000, "-0.0003482613")])
    rows = deviation_rows(payload)
    assert len(rows) == 1
    assert rows[0].time_ms == 1_780_000_000_000
    assert rows[0].premium == pytest.approx(-0.0003482613)


def test_an_unserved_premium_is_a_recorded_absence() -> None:
    rows = deviation_rows(json.dumps([_row(1_780_000_000_000, None)]))
    assert isinstance(rows[0].premium, Absent)
    with pytest.raises(TypeError):
        float(rows[0].premium)


class _FakeVenue:
    """Serves pages of deviation rows. Records every coin it was asked for."""

    def __init__(self, pages: list[list[dict[str, object]]]) -> None:
        self._pages = pages
        self.asked: list[str] = []

    def request(self, body: dict[str, object], endpoint: str) -> FetchOutcome:
        self.asked.append(str(body["coin"]))
        page = self._pages.pop(0) if self._pages else []
        return FetchOutcome(state=CallState.STORED, http_status=200, body=json.dumps(page).encode())


def _cohorts() -> Cohorts:
    return Cohorts(
        generating_sample=frozenset({"xyz:AAPL"}),
        fresh_plan=frozenset(),
        h2_pairs=frozenset({"xyz:AVGO"}),
    )


def test_a_gated_coin_never_reaches_the_network() -> None:
    """The gate runs before the first request: a quarantined coin costs nothing."""
    venue = _FakeVenue([[_row(1, "0.001")]])
    with pytest.raises(H5RetrospectiveGated):
        h5retro.fetch_series(venue, "xyz:AAPL", _cohorts(), 0, HOUR_MS)  # type: ignore[arg-type]
    assert venue.asked == []


def test_an_ungated_coin_pages_until_a_short_page() -> None:
    start = 1_780_000_000_000
    full = [_row(start + i * HOUR_MS, "0.0001") for i in range(h5retro.PAGE_ROWS)]
    short = [_row(start + h5retro.PAGE_ROWS * HOUR_MS, "0.0002")]
    venue = _FakeVenue([full, short])
    series = h5retro.fetch_series(
        venue,  # type: ignore[arg-type]
        "xyz:GOOGL",
        _cohorts(),
        start,
        start + 10_000 * HOUR_MS,
    )
    assert series.pages_fetched == 2
    assert len(series.observations) == h5retro.PAGE_ROWS + 1
    assert series.n == h5retro.PAGE_ROWS + 1
    assert series.first_time_ms == start
    assert series.state == CallState.STORED.value


def test_paging_stops_at_the_registered_page_budget() -> None:
    start = 1_780_000_000_000
    pages = [
        [_row(start + (p * h5retro.PAGE_ROWS + i) * HOUR_MS, "0.0001") for i in range(500)]
        for p in range(CONFIG.h5_retro_page_budget + 5)
    ]
    venue = _FakeVenue(pages)
    series = h5retro.fetch_series(
        venue,  # type: ignore[arg-type]
        "xyz:GOOGL",
        _cohorts(),
        start,
        start + 10**7 * HOUR_MS,
    )
    assert series.pages_fetched == CONFIG.h5_retro_page_budget


def test_premium_is_converted_to_bp_and_absences_survive() -> None:
    start = 1_780_000_000_000
    venue = _FakeVenue([[_row(start, "0.0001"), _row(start + HOUR_MS, None)]])
    series = h5retro.fetch_series(
        venue,  # type: ignore[arg-type]
        "xyz:GOOGL",
        _cohorts(),
        start,
        start + 10 * HOUR_MS,
    )
    assert series.observations[0].deviation_bp == pytest.approx(1.0)
    assert is_absent(series.observations[1].deviation_bp)
    assert series.n == 1


def test_every_observation_carries_a_session_tag() -> None:
    # 2026-08-28T14:00Z is Friday 10:00 ET; 2026-08-29T14:00Z is a Saturday.
    friday = 1_787_925_600_000
    saturday = friday + 24 * HOUR_MS
    venue = _FakeVenue([[_row(friday, "0.0001"), _row(saturday, "0.0002")]])
    series = h5retro.fetch_series(
        venue,  # type: ignore[arg-type]
        "xyz:GOOGL",
        _cohorts(),
        friday,
        saturday + HOUR_MS,
    )
    tags = [o.session_tag for o in series.observations]
    assert tags == [TAG_REGULAR, TAG_WEEKEND]
    pooled = h5retro.by_session_tag([series])
    assert sorted(pooled) == [TAG_REGULAR, TAG_WEEKEND]
    assert len(pooled[TAG_REGULAR]) == 1


def test_covered_days_counts_distinct_days_with_a_served_observation() -> None:
    start = 1_780_000_000_000
    rows = [_row(start + i * HOUR_MS, "0.0001") for i in range(49)]
    venue = _FakeVenue([rows])
    series = h5retro.fetch_series(
        venue,  # type: ignore[arg-type]
        "xyz:GOOGL",
        _cohorts(),
        start,
        start + 100 * HOUR_MS,
    )
    assert series.covered_days == 3
