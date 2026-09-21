"""Eligibility rules, boundary fixtures on the registered boundaries."""

from __future__ import annotations

from npl.census import CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR
from npl.config import CONFIG
from npl.eligibility import (
    Eligibility,
    assess_retro,
    control_candidates_exist,
    deadline_ms,
    entry_anchor_ms,
    expected_funding_hours,
    funding_window,
    matured_by,
    project_cohort,
    resolve_event,
)

L0 = 1700000000000 - (1700000000000 % MS_PER_DAY)  # a midnight-aligned listing open


def _row(
    coin: str = "NEW",
    dex: str = "",
    first: int | None = L0,
    last_offset_days: int | None = 400,
    delisted: bool = False,
    rows: int = 400,
    funding_first: int | None = None,
) -> CensusRow:
    last = (
        None
        if first is None or last_offset_days is None
        else first + last_offset_days * MS_PER_DAY - 1
    )
    return CensusRow(
        coin=coin,
        dex=dex,
        event_type="vanilla",
        hyperp_source="",
        is_delisted=delisted,
        sz_decimals=2,
        max_leverage=10,
        state="stored",
        first_1d_open_ms=first,
        last_1d_close_ms=last,
        candle_rows=rows if first is not None else 0,
        funding_state="stored" if first is not None else "no_data",
        first_funding_time_ms=funding_first
        if funding_first is not None
        else (first + 3 * MS_PER_HOUR if first is not None else None),
        funding_page_rows=500 if first is not None else 0,
        recorded_at="t",
    )


NOW = L0 + 500 * MS_PER_DAY
FULL_HOURS = CONFIG.horizon_primary_days * 24  # 720


def test_the_entry_anchor_is_the_second_daily_close() -> None:
    # Listing day opens at L0; the second daily close is 00:00Z of day + 2.
    assert entry_anchor_ms(L0) == L0 + 2 * MS_PER_DAY


def test_a_full_coverage_old_event_is_retro_eligible() -> None:
    verdict = assess_retro(_row(), NOW, funding_hours_present=FULL_HOURS)
    assert verdict.verdict is Eligibility.RETRO_ELIGIBLE
    assert verdict.reasons == ()
    assert verdict.funding_hours_expected == FULL_HOURS


def test_funding_coverage_exactly_at_the_bar_is_eligible() -> None:
    # The bar is >= 0.95: exactly 0.95 of 720 hours (= 684) passes.
    at_bar = int(FULL_HOURS * CONFIG.funding_coverage_bar)
    assert at_bar / FULL_HOURS == CONFIG.funding_coverage_bar
    verdict = assess_retro(_row(), NOW, funding_hours_present=at_bar)
    assert verdict.verdict is Eligibility.RETRO_ELIGIBLE


def test_funding_coverage_one_hour_below_the_bar_is_excluded() -> None:
    below = int(FULL_HOURS * CONFIG.funding_coverage_bar) - 1
    verdict = assess_retro(_row(), NOW, funding_hours_present=below)
    assert verdict.verdict is Eligibility.EXCLUDED_INELIGIBLE
    assert "funding_coverage_below_bar" in verdict.reasons


def test_unmeasured_funding_coverage_never_passes_silently() -> None:
    verdict = assess_retro(_row(), NOW, funding_hours_present=None)
    assert verdict.verdict is Eligibility.EXCLUDED_INELIGIBLE
    assert "funding_coverage_unmeasured" in verdict.reasons


def test_an_uninferable_listing_date_is_excluded_with_its_reason() -> None:
    verdict = assess_retro(_row(first=None, last_offset_days=None), NOW, None)
    assert verdict.verdict is Eligibility.EXCLUDED_INELIGIBLE
    assert verdict.reasons == ("listing_date_uninferable", "no_candles")


def test_a_perp_delisted_before_entry_is_excluded() -> None:
    verdict = assess_retro(_row(delisted=True, last_offset_days=1, rows=1), NOW, None)
    assert verdict.verdict is Eligibility.EXCLUDED_INELIGIBLE
    assert verdict.reasons == ("died_before_entry",)


def test_a_delisting_inside_the_window_is_retro_eligible_and_truncated() -> None:
    # Delisted 10 days after listing: entry exists, horizon truncates at death.
    verdict = assess_retro(_row(delisted=True, last_offset_days=10, rows=10), NOW, 8 * 24)
    assert verdict.verdict is Eligibility.RETRO_ELIGIBLE
    assert verdict.truncated_by_delisting
    # Expected hours run entry -> last close, not the full 720.
    expected = verdict.funding_hours_expected
    assert expected is not None
    assert expected < FULL_HOURS


def test_an_event_younger_than_the_horizon_is_pending_never_partial() -> None:
    # Listing such that entry+90d lands exactly one day past now: pending.
    young = NOW - (2 + CONFIG.retro_history_required_days) * MS_PER_DAY + MS_PER_DAY
    verdict = assess_retro(_row(first=young, last_offset_days=None), NOW, None)
    assert verdict.verdict is Eligibility.PENDING
    assert verdict.reasons == ("younger_than_horizon",)


def test_the_horizon_boundary_event_is_retro_not_pending() -> None:
    # entry+90d == now exactly: the history requirement is satisfiable.
    boundary = NOW - (2 + CONFIG.retro_history_required_days) * MS_PER_DAY
    row = _row(first=boundary, last_offset_days=2 + CONFIG.retro_history_required_days)
    verdict = assess_retro(row, NOW, funding_hours_present=FULL_HOURS)
    assert verdict.verdict is Eligibility.RETRO_ELIGIBLE


def test_an_alive_event_with_a_serving_gap_is_excluded_not_guessed() -> None:
    row = _row(last_offset_days=30, rows=30)  # alive, but candles stop at day 30
    verdict = assess_retro(row, NOW, funding_hours_present=FULL_HOURS)
    assert verdict.verdict is Eligibility.EXCLUDED_INELIGIBLE
    assert "history_not_servable_to_horizon" in verdict.reasons


def test_control_candidates_age_boundary_sits_at_180_days() -> None:
    event = assess_retro(_row(), NOW, FULL_HOURS)
    assert event.entry_ms is not None
    exactly = _row(
        coin="OLD",
        first=event.entry_ms - CONFIG.control_min_age_days * MS_PER_DAY,
        last_offset_days=600,
    )
    too_young = _row(
        coin="YOUNG",
        first=event.entry_ms - CONFIG.control_min_age_days * MS_PER_DAY + 1,
        last_offset_days=600,
    )
    assert control_candidates_exist(event, [exactly, too_young]) == 1


def test_control_candidates_must_share_the_dex() -> None:
    event = assess_retro(_row(dex="xyz"), NOW, FULL_HOURS)
    main_dex_old = _row(coin="OLD", dex="", first=L0 - 400 * MS_PER_DAY)
    same_dex_old = _row(coin="OLD2", dex="xyz", first=L0 - 400 * MS_PER_DAY)
    assert control_candidates_exist(event, [main_dex_old, same_dex_old]) == 1


def test_funding_window_truncates_at_death() -> None:
    start, end = funding_window(1000, truncation_ms=1000 + 5 * MS_PER_DAY)
    assert end == 1000 + 5 * MS_PER_DAY
    assert expected_funding_hours(start, end) == 5 * 24


def test_maturity_counts_events_whose_primary_matures_by_the_deadline() -> None:
    deadline = L0 + 200 * MS_PER_DAY
    on_time = deadline - (2 + CONFIG.horizon_primary_days) * MS_PER_DAY
    assert matured_by(on_time, deadline)
    assert not matured_by(on_time + MS_PER_DAY, deadline)


def test_project_cohort_combines_retro_pending_and_rate() -> None:
    now = deadline_ms("2026-09-01")
    projection = project_cohort(
        achieved_retro_n=100,
        pending_listings_ms=[now - 10 * MS_PER_DAY],
        monthly_rate=10.0,
        now_ms=now,
    )
    assert projection.achieved_retro_n == 100
    assert projection.pending_n == 1
    assert projection.combined_by_deadline >= projection.combined_by_interim
    assert projection.combined_by_interim > 100


# ------------------------------------------------- Amendment 1 resolution ---


def test_same_day_funding_cross_check_confirms_a_vanilla_listing() -> None:
    resolved = resolve_event(_row())
    assert resolved.event_type == "vanilla"
    assert resolved.event_listing_ms == L0
    assert resolved.censoring == ""


def test_funding_exactly_one_day_later_is_inside_the_tolerance() -> None:
    resolved = resolve_event(_row(funding_first=L0 + MS_PER_DAY))
    assert resolved.event_type == "vanilla"
    assert resolved.event_listing_ms == L0


def test_funding_two_days_later_tags_a_mechanical_hyperp_conversion() -> None:
    resolved = resolve_event(_row(funding_first=L0 + 2 * MS_PER_DAY + MS_PER_HOUR))
    assert resolved.event_type == "hyperp_conversion"
    assert resolved.event_listing_ms == L0 + 2 * MS_PER_DAY
    assert resolved.pre_vanilla_days == 2


def test_first_funding_at_the_archive_epoch_is_censored() -> None:
    epoch = CONFIG.funding_archive_epoch_ms
    resolved = resolve_event(_row(first=epoch, funding_first=epoch))
    assert resolved.event_listing_ms is None
    assert resolved.censoring == "epoch_censored"


def test_candles_predating_the_epoch_are_censored() -> None:
    epoch = CONFIG.funding_archive_epoch_ms
    resolved = resolve_event(_row(first=epoch - MS_PER_DAY, funding_first=epoch + MS_PER_HOUR))
    assert resolved.censoring == "epoch_censored"


def test_one_ms_past_the_epoch_is_not_censored() -> None:
    epoch = CONFIG.funding_archive_epoch_ms
    aligned = epoch  # the epoch itself is midnight-aligned
    resolved = resolve_event(_row(first=aligned, funding_first=epoch + 1))
    assert resolved.censoring == ""
    assert resolved.event_listing_ms == aligned


def test_missing_funding_rows_refuse_resolution() -> None:
    from dataclasses import replace

    row = replace(_row(), first_funding_time_ms=None)
    resolved = resolve_event(row)
    assert resolved.event_listing_ms is None
    assert resolved.censoring == "no_funding_rows"
