"""Cluster buys and the Johnsen programmatic-event filter."""

from __future__ import annotations

import datetime as dt

from insider.config import CONFIG
from insider.corpus.cluster import Buy, find_clusters, modal_date_price_fraction


def buy(i: int, cik: int, day: int, price: float = 10.0, symbol: str = "AAA") -> Buy:
    return Buy(
        index=i,
        symbol=symbol,
        filer_cik=cik,
        transaction_date=dt.date(2020, 5, day),
        price_per_share=price,
    )


def test_three_distinct_filers_in_five_days_make_a_cluster() -> None:
    report = find_clusters([buy(0, 1, 1, 10.0), buy(1, 2, 3, 11.0), buy(2, 3, 5, 12.0)])
    assert len(report.clusters) == 1
    assert report.clusters[0].distinct_filers == 3
    assert report.in_surviving_cluster == {0, 1, 2}


def test_two_filers_are_not_a_cluster() -> None:
    report = find_clusters([buy(0, 1, 1, 10.0), buy(1, 2, 3, 11.0)])
    assert report.clusters == ()
    assert not report.in_surviving_cluster


def test_one_filer_buying_three_times_is_not_a_cluster() -> None:
    """A cluster needs three judgements, not three tickets."""
    report = find_clusters([buy(0, 1, 1, 10.0), buy(1, 1, 2, 11.0), buy(2, 1, 3, 12.0)])
    assert report.clusters == ()


def test_a_sixth_day_falls_outside_the_five_day_window() -> None:
    report = find_clusters([buy(0, 1, 1, 10.0), buy(1, 2, 3, 11.0), buy(2, 3, 6, 12.0)])
    assert report.clusters == ()


def test_the_johnsen_filter_rejects_one_price_on_one_day() -> None:
    report = find_clusters([buy(0, 1, 1, 58.5), buy(1, 2, 1, 58.5), buy(2, 3, 1, 58.5)])
    assert len(report.clusters) == 1
    assert report.clusters[0].rejected
    assert report.clusters[0].modal_date_price_fraction == 1.0
    assert not report.in_surviving_cluster
    assert report.johnsen_rejected_only == {0, 1, 2}


def test_a_cluster_at_the_threshold_is_rejected() -> None:
    """Eighty percent or more, so the boundary itself is a rejection."""
    buys = [buy(i, i + 1, 1, 58.5) for i in range(4)] + [buy(4, 5, 2, 61.0)]
    report = find_clusters(buys)
    rejected = [c for c in report.clusters if c.size == 5]
    assert rejected and rejected[0].modal_date_price_fraction == 0.8
    assert rejected[0].rejected


def test_independent_prices_survive_the_filter() -> None:
    buys = [buy(0, 1, 1, 58.5), buy(1, 2, 2, 60.1), buy(2, 3, 3, 61.7)]
    report = find_clusters(buys)
    assert not report.clusters[0].rejected
    assert report.in_surviving_cluster == {0, 1, 2}


def test_clusters_do_not_cross_issuers() -> None:
    buys = [buy(0, 1, 1, symbol="AAA"), buy(1, 2, 1, symbol="BBB"), buy(2, 3, 1, symbol="CCC")]
    assert find_clusters(buys).clusters == ()


def test_the_modal_fraction_is_over_date_and_price_together() -> None:
    same_day_two_prices = [buy(0, 1, 1, 10.0), buy(1, 2, 1, 11.0)]
    assert modal_date_price_fraction(same_day_two_prices) == 0.5


def test_the_registered_thresholds_are_the_ones_in_force() -> None:
    assert CONFIG.cluster_min_filers == 3
    assert CONFIG.cluster_window_days == 5
    assert CONFIG.johnsen_same_date_price_fraction == 0.80
