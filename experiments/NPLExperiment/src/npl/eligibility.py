"""Event eligibility and cohort projection. Counts and timestamps only.

Every input is a census row, a clock, or an integer count of funding hours.
No price, no volume, no funding value reaches this module; the funding
coverage figure arrives as hours-present, counted from row timestamps by the
caller through the blindness reader.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from npl.census import CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR
from npl.config import CONFIG, Config


class Eligibility(StrEnum):
    RETRO_ELIGIBLE = "retro_eligible"
    PENDING = "pending"
    EXCLUDED_INELIGIBLE = "excluded_ineligible"


@dataclass(frozen=True, slots=True)
class ResolvedEvent:
    """Amendment 1: the event date resolved from candle and funding starts."""

    event_type: str
    event_listing_ms: int | None
    censoring: str
    pre_vanilla_days: int | None


def resolve_event(row: CensusRow, cfg: Config = CONFIG) -> ResolvedEvent:
    """The Amendment 1 rule: cross-check, epoch censoring, mechanical hyperp tag."""
    if row.first_1d_open_ms is None or row.candle_rows == 0:
        return ResolvedEvent(row.event_type, None, "no_candles", None)
    if row.first_funding_time_ms is None:
        return ResolvedEvent(row.event_type, None, "no_funding_rows", None)
    epoch = cfg.funding_archive_epoch_ms
    if row.first_1d_open_ms < epoch or row.first_funding_time_ms <= epoch:
        return ResolvedEvent(row.event_type, None, "epoch_censored", None)
    candle_day = row.first_1d_open_ms // MS_PER_DAY
    funding_day = row.first_funding_time_ms // MS_PER_DAY
    delta_days = funding_day - candle_day
    if delta_days < -cfg.listing_tolerance_days:
        # Funding predating candles by more than the tolerance is a shape the
        # measurement never produced; refuse to guess.
        return ResolvedEvent(row.event_type, None, "cross_check_disagreement", None)
    if delta_days <= cfg.listing_tolerance_days:
        return ResolvedEvent(row.event_type, row.first_1d_open_ms, "", None)
    from npl.census import EVENT_HYPERP_CONVERSION

    return ResolvedEvent(EVENT_HYPERP_CONVERSION, funding_day * MS_PER_DAY, "", delta_days)


@dataclass(frozen=True, slots=True)
class EventAssessment:
    coin: str
    dex: str
    event_type: str
    verdict: Eligibility
    reasons: tuple[str, ...]
    listing_open_ms: int | None
    entry_ms: int | None
    truncated_by_delisting: bool
    funding_hours_present: int | None
    funding_hours_expected: int | None


def entry_anchor_ms(listing_open_ms: int, cfg: Config = CONFIG) -> int:
    """The second daily close: 00:00Z of listing day + 2 (Section 3).

    The venue serves 1d candles aligned to the UTC day, so the first candle's
    t is the listing day's 00:00Z and the entry anchor is t + (offset+1) days.
    """
    return listing_open_ms + (cfg.entry_anchor_offset_days + 1) * MS_PER_DAY


def funding_window(
    entry_ms: int, truncation_ms: int | None, cfg: Config = CONFIG
) -> tuple[int, int]:
    """The primary-horizon funding window (entry, entry + 30d], truncated by death."""
    end = entry_ms + cfg.horizon_primary_days * MS_PER_DAY
    if truncation_ms is not None:
        end = min(end, truncation_ms)
    return entry_ms, end


def expected_funding_hours(entry_ms: int, end_ms: int) -> int:
    return max(0, (end_ms - entry_ms) // MS_PER_HOUR)


def assess_retro(
    row: CensusRow,
    now_ms: int,
    funding_hours_present: int | None,
    cfg: Config = CONFIG,
) -> EventAssessment:
    """The registered retro-eligibility rule, applied to one census row."""
    reasons: list[str] = []

    resolved = resolve_event(row, cfg)
    if resolved.event_listing_ms is None:
        return EventAssessment(
            coin=row.coin,
            dex=row.dex,
            event_type=resolved.event_type,
            verdict=Eligibility.EXCLUDED_INELIGIBLE,
            reasons=("listing_date_uninferable", resolved.censoring),
            listing_open_ms=None,
            entry_ms=None,
            truncated_by_delisting=False,
            funding_hours_present=None,
            funding_hours_expected=None,
        )

    listing_ms = resolved.event_listing_ms
    entry = entry_anchor_ms(listing_ms, cfg)
    last_close = row.last_1d_close_ms if row.last_1d_close_ms is not None else listing_ms

    if row.is_delisted and last_close < entry:
        return EventAssessment(
            coin=row.coin,
            dex=row.dex,
            event_type=resolved.event_type,
            verdict=Eligibility.EXCLUDED_INELIGIBLE,
            reasons=("died_before_entry",),
            listing_open_ms=listing_ms,
            entry_ms=entry,
            truncated_by_delisting=True,
            funding_hours_present=None,
            funding_hours_expected=None,
        )

    required_end = entry + cfg.retro_history_required_days * MS_PER_DAY
    truncated = row.is_delisted and last_close < required_end
    if not truncated and required_end > now_ms:
        return EventAssessment(
            coin=row.coin,
            dex=row.dex,
            event_type=resolved.event_type,
            verdict=Eligibility.PENDING,
            reasons=("younger_than_horizon",),
            listing_open_ms=listing_ms,
            entry_ms=entry,
            truncated_by_delisting=False,
            funding_hours_present=funding_hours_present,
            funding_hours_expected=None,
        )
    if not truncated and last_close + MS_PER_DAY < required_end:
        # Alive but the venue stops serving before entry+90d: retention gap.
        reasons.append("history_not_servable_to_horizon")

    truncation = last_close if truncated else None
    start, end = funding_window(entry, truncation, cfg)
    expected = expected_funding_hours(start, end)
    if funding_hours_present is None:
        reasons.append("funding_coverage_unmeasured")
    elif expected > 0 and funding_hours_present / expected < cfg.funding_coverage_bar:
        reasons.append("funding_coverage_below_bar")

    verdict = Eligibility.RETRO_ELIGIBLE if not reasons else Eligibility.EXCLUDED_INELIGIBLE
    return EventAssessment(
        coin=row.coin,
        dex=row.dex,
        event_type=resolved.event_type,
        verdict=verdict,
        reasons=tuple(reasons),
        listing_open_ms=listing_ms,
        entry_ms=entry,
        truncated_by_delisting=truncated,
        funding_hours_present=funding_hours_present,
        funding_hours_expected=expected,
    )


def control_candidates_exist(
    event: EventAssessment, rows: list[CensusRow], cfg: Config = CONFIG
) -> int:
    """Count Section 6 candidates by census dates: same dex, listed >= 180 days earlier.

    Funding coverage of the selected candidate is enforced at assignment time
    (A.3 Task 6); this is the A.2 feasibility count, and it is reported as a
    date-based count, not a coverage-verified one.
    """
    if event.entry_ms is None:
        return 0
    cutoff = event.entry_ms - cfg.control_min_age_days * MS_PER_DAY
    n = 0
    for row in rows:
        if row.dex != event.dex or row.coin == event.coin:
            continue
        if row.first_1d_open_ms is None:
            continue
        if row.first_1d_open_ms <= cutoff:
            # The candidate must also still serve history around the event
            # entry: alive then, or delisted after the trailing window.
            last = row.last_1d_close_ms or row.first_1d_open_ms
            if last >= event.entry_ms - cfg.control_trailing_window_hours * MS_PER_HOUR:
                n += 1
    return n


def deadline_ms(iso_date: str) -> int:
    moment = datetime.fromisoformat(iso_date).replace(tzinfo=UTC)
    return int(moment.timestamp() * 1000)


def matured_by(listing_ms: int, deadline: int, cfg: Config = CONFIG) -> bool:
    """An event counts for a deadline when its 30-day primary matures by it."""
    entry = entry_anchor_ms(listing_ms, cfg)
    return entry + cfg.horizon_primary_days * MS_PER_DAY <= deadline


@dataclass(frozen=True, slots=True)
class CohortProjection:
    achieved_retro_n: int
    pending_n: int
    projected_forward_by_interim: int
    projected_forward_by_deadline: int
    combined_by_interim: int
    combined_by_deadline: int
    monthly_rate: float


def project_cohort(
    achieved_retro_n: int,
    pending_listings_ms: list[int],
    monthly_rate: float,
    now_ms: int,
    cfg: Config = CONFIG,
) -> CohortProjection:
    """Combined N at the interim and final deadlines (Section 9).

    Achievable means the 30-day primary matures by the deadline: pending
    events count where their maturity date clears it, and projected forward
    events accrue at the trailing monthly rate until deadline minus the
    entry-plus-horizon lag.
    """
    interim = deadline_ms(cfg.interim_deadline)
    final = deadline_ms(cfg.projection_deadline)
    lag_ms = (cfg.entry_anchor_offset_days + 1 + cfg.horizon_primary_days) * MS_PER_DAY

    pending_interim = sum(1 for ms in pending_listings_ms if matured_by(ms, interim, cfg))
    pending_final = sum(1 for ms in pending_listings_ms if matured_by(ms, final, cfg))

    months_interim = max(0.0, (interim - lag_ms - now_ms) / (30.44 * MS_PER_DAY))
    months_final = max(0.0, (final - lag_ms - now_ms) / (30.44 * MS_PER_DAY))
    forward_interim = int(monthly_rate * months_interim)
    forward_final = int(monthly_rate * months_final)

    return CohortProjection(
        achieved_retro_n=achieved_retro_n,
        pending_n=len(pending_listings_ms),
        projected_forward_by_interim=forward_interim + pending_interim,
        projected_forward_by_deadline=forward_final + pending_final,
        combined_by_interim=achieved_retro_n + forward_interim + pending_interim,
        combined_by_deadline=achieved_retro_n + forward_final + pending_final,
        monthly_rate=monthly_rate,
    )
