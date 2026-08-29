"""Archive capture density, with the window boundaries sitting exactly on the anchors."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from etf.archive import Memento, TimemapShape, density, parse_timemap, qualifying_window

D = date(2025, 6, 2)

TIMEMAP = (
    '<https://farside.co.uk/btc/>; rel="original",\n'
    '<https://web.archive.org/web/timemap/link/https://farside.co.uk/btc/>; rel="self"; '
    'type="application/link-format"; from="Sun, 11 Aug 2024 04:19:54 GMT",\n'
    '<https://web.archive.org/web/https://farside.co.uk/btc/>; rel="timegate",\n'
    "<https://web.archive.org/web/20250602230003/https://farside.co.uk/btc/>; "
    'rel="first memento"; datetime="Mon, 02 Jun 2025 23:00:03 GMT",\n'
    "<https://web.archive.org/web/20250603120000/https://farside.co.uk/btc/>; "
    'rel="memento"; datetime="Tue, 03 Jun 2025 12:00:00 GMT"\n'
)


def test_only_mementos_are_parsed_not_the_self_or_timegate_links() -> None:
    mementos = parse_timemap(TIMEMAP)
    assert len(mementos) == 2
    assert mementos[0].captured_at == datetime(2025, 6, 2, 23, 0, 3, tzinfo=UTC)
    assert all("web.archive.org/web/2" in m.url for m in mementos)


def test_first_memento_counts_as_a_memento() -> None:
    assert any(m.captured_at.day == 2 for m in parse_timemap(TIMEMAP))


def test_mementos_come_back_ordered_by_clock() -> None:
    reversed_map = "\n".join(reversed(TIMEMAP.strip().split("\n")))
    stamps = [m.captured_at for m in parse_timemap(reversed_map)]
    assert stamps == sorted(stamps)


def test_an_unparseable_datetime_is_refused_rather_than_dropped() -> None:
    bad = '<https://web.archive.org/web/x/u>; rel="memento"; datetime="not a date"'
    with pytest.raises(TimemapShape, match="unparseable memento datetime"):
        parse_timemap(bad)


def test_the_window_runs_from_the_registered_peak_start_to_the_anchor() -> None:
    start, end = qualifying_window(D)
    assert start == datetime(2025, 6, 2, 20, tzinfo=UTC)
    assert end == datetime(2025, 6, 3, 8, tzinfo=UTC)


def test_a_capture_exactly_on_the_window_start_qualifies() -> None:
    report = density([D], [Memento(datetime(2025, 6, 2, 20, 0, 0, tzinfo=UTC), "u")])
    assert report.admissible_days == 1


def test_a_capture_exactly_on_the_anchor_does_not_qualify() -> None:
    """Strictly before the anchor, and the fixture sits exactly on 08:00:00Z."""
    report = density([D], [Memento(datetime(2025, 6, 3, 8, 0, 0, tzinfo=UTC), "u")])
    assert report.admissible_days == 0
    assert report.capture_too_late_days == 1
    assert report.no_capture_days == 0


def test_no_capture_and_capture_too_late_never_merge() -> None:
    """Operational health and sample composition never share a representation."""
    report = density([D, date(2025, 6, 3)], [Memento(datetime(2025, 6, 3, 9, tzinfo=UTC), "u")])
    assert report.capture_too_late_days == 1
    assert report.no_capture_days == 1
    assert report.admissible_days == 0


def test_a_capture_one_second_before_the_window_start_does_not_qualify() -> None:
    report = density([D], [Memento(datetime(2025, 6, 2, 19, 59, 59, tzinfo=UTC), "u")])
    assert report.admissible_days == 0


def test_the_share_carries_its_n_and_an_empty_universe_is_an_absence() -> None:
    report = density([], [])
    assert report.n_trading_days == 0
    assert report.admissible_share is None
    full = density([D], [Memento(datetime(2025, 6, 2, 23, tzinfo=UTC), "u")])
    assert full.admissible_share == 1.0
    assert full.n_trading_days == 1
