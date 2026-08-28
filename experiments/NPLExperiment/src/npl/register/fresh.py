"""The fresh cohort: every resolved event that is not the generating sample.

The register's successor hypotheses test on fresh, unread data only. Fresh
means: an event the Amendment 1 resolution recognizes (a listing date
inferable to the registered tolerance) that is NOT one of the 312
generating-sample events and did not die before its entry anchor. On the
sealed H1 census this reproduces exactly the 62 pending-at-closure events;
census refresh rows append forward births to it. Counts and timestamps
only — no outcome value exists on this path.
"""

from __future__ import annotations

from npl.census import CensusRow
from npl.clock import MS_PER_DAY
from npl.config import CONFIG, Config
from npl.eligibility import entry_anchor_ms, resolve_event
from npl.register.generating_sample import event_id
from npl.register.views import FreshEvent

# The registered pending-at-closure count (root REGISTRATION.md, Stage B
# verdict record). The sealed-census reconstruction must reproduce it.
REGISTERED_PENDING_AT_CLOSURE = 62


class FreshCohortMismatch(RuntimeError):
    """The sealed-census fresh cohort does not reproduce the registered count."""


def fresh_backfillable_events(
    census_rows: list[CensusRow],
    sample: frozenset[str],
    cfg: Config = CONFIG,
) -> tuple[FreshEvent, ...]:
    """Every resolved, non-generating event from census rows, birth-ordered.

    Duplicate (coin, dex) rows keep the first record (the sealed census
    pass), matching the Stage B reconstruction rule. An event whose
    instrument died before its entry anchor is excluded (died_before_entry,
    the H1 rule), counted by the caller via the difference in lengths.
    """
    seen: set[tuple[str, str]] = set()
    out: list[FreshEvent] = []
    for row in census_rows:
        key = (row.coin, row.dex)
        if key in seen:
            continue
        seen.add(key)
        resolved = resolve_event(row, cfg)
        if resolved.event_listing_ms is None:
            continue
        listing = resolved.event_listing_ms
        if event_id(row.coin, row.dex, listing) in sample:
            continue
        entry = entry_anchor_ms(listing, cfg)
        last_close = row.last_1d_close_ms if row.last_1d_close_ms is not None else listing
        if row.is_delisted and last_close < entry:
            continue
        out.append(
            FreshEvent(
                coin=row.coin,
                dex=row.dex,
                event_type=resolved.event_type,
                listing_open_ms=listing,
                entry_ms=entry,
            )
        )
    return tuple(sorted(out, key=lambda e: (e.listing_open_ms, e.coin)))


def require_registered_pending_count(
    events: tuple[FreshEvent, ...],
    newest_sealed_listing_ms: int,
    expected: int = REGISTERED_PENDING_AT_CLOSURE,
) -> None:
    """On the sealed census (no refresh rows), the cohort must be exactly 62.

    Refresh rows are newer than the sealed census's newest listing; the
    check counts only events at or before that watermark so it stays valid
    after the census grows.
    """
    sealed = [e for e in events if e.listing_open_ms <= newest_sealed_listing_ms]
    if len(sealed) != expected:
        raise FreshCohortMismatch(
            f"the sealed-census fresh cohort reconstructs to {len(sealed)} events "
            f"against the registered pending-at-closure {expected}; refusing to guess"
        )


def fresh_funding_span(event: FreshEvent, cfg: Config = CONFIG) -> tuple[int, int]:
    """The registered funding window for a fresh event: entry-168h .. entry+91d."""
    return (
        event.entry_ms + cfg.backfill_funding_start_offset_hours * 3_600_000,
        event.entry_ms + cfg.backfill_funding_end_offset_days * MS_PER_DAY,
    )
