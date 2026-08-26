"""Cluster buys and the Johnsen programmatic-event filter.

A cluster is three or more distinct filer CIKs making P-code purchases at the
same issuer inside a rolling five-day window, counted in calendar days as
[d, d + 4] inclusive.

The Johnsen filter rejects a cluster when a single date-and-price pair accounts
for eighty percent or more of the contributing buys. Insiders who all bought at
one price on one day were filled by one mechanism, not by three independent
judgements, and a cluster is only interesting if the judgements are independent.
"""

from __future__ import annotations

import datetime as dt
from collections import Counter, defaultdict
from dataclasses import dataclass

from insider.config import CONFIG, Config


@dataclass(frozen=True, slots=True)
class Buy:
    """The minimum a buy needs to be clustered. Index ties it back to the corpus."""

    index: int
    symbol: str
    filer_cik: int
    transaction_date: dt.date
    price_per_share: float


@dataclass(frozen=True, slots=True)
class Cluster:
    symbol: str
    window_start: dt.date
    window_end: dt.date
    member_indexes: tuple[int, ...]
    distinct_filers: int
    modal_date_price_fraction: float
    rejected: bool

    @property
    def size(self) -> int:
        return len(self.member_indexes)


@dataclass(frozen=True, slots=True)
class ClusterReport:
    clusters: tuple[Cluster, ...]
    in_surviving_cluster: frozenset[int]
    johnsen_rejected_only: frozenset[int]


def modal_date_price_fraction(buys: list[Buy]) -> float:
    """Share of the cluster held by its most common date-and-price pair."""
    if not buys:
        return 0.0
    counts = Counter((b.transaction_date, round(b.price_per_share, 4)) for b in buys)
    return counts.most_common(1)[0][1] / len(buys)


def find_clusters(buys: list[Buy], cfg: Config = CONFIG) -> ClusterReport:
    """Every cluster in the stream, with its Johnsen fate recorded."""
    by_symbol: dict[str, list[Buy]] = defaultdict(list)
    for buy in buys:
        by_symbol[buy.symbol].append(buy)

    span = dt.timedelta(days=cfg.cluster_window_days - 1)
    clusters: list[Cluster] = []
    surviving: set[int] = set()
    clustered: set[int] = set()

    for symbol, group in by_symbol.items():
        group.sort(key=lambda b: (b.transaction_date, b.filer_cik, b.index))
        for i, anchor in enumerate(group):
            end = anchor.transaction_date + span
            window = [b for b in group[i:] if b.transaction_date <= end]
            filers = {b.filer_cik for b in window}
            if len(filers) < cfg.cluster_min_filers:
                continue
            fraction = modal_date_price_fraction(window)
            rejected = fraction >= cfg.johnsen_same_date_price_fraction
            indexes = tuple(b.index for b in window)
            clusters.append(
                Cluster(
                    symbol=symbol,
                    window_start=anchor.transaction_date,
                    window_end=end,
                    member_indexes=indexes,
                    distinct_filers=len(filers),
                    modal_date_price_fraction=fraction,
                    rejected=rejected,
                )
            )
            clustered.update(indexes)
            if not rejected:
                surviving.update(indexes)

    return ClusterReport(
        clusters=tuple(clusters),
        in_surviving_cluster=frozenset(surviving),
        johnsen_rejected_only=frozenset(clustered - surviving),
    )
