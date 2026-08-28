"""Frozen experiment configuration.

Every field declared here must be referenced by at least one module under
src/npl outside this file. tests/test_guards.py fails when a field has no
enforcement site, so a key cannot be added as decoration. Fields whose
consumer lands in a later Stage A task sit on the PENDING_ENFORCEMENT list in
that test, which must shrink to empty by Stage A.3.

Values here are registered in REGISTRATION.md and frozen at Stage A.0, before
any network call. Changing one requires a numbered amendment.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

# alpha_adj = 1 - 0.95 ** (1/3): three co-primaries, family-wise 0.05, Sidak.
ALPHA_ADJ: Final = 1.0 - 0.95 ** (1.0 / 3.0)


@dataclass(frozen=True, slots=True)
class Config:
    """Registered parameters. Frozen at A.0, amended only by numbered amendment."""

    # --- access -------------------------------------------------------------
    info_url: str
    request_cap_per_day: int
    request_timeout_seconds: float

    # --- inference (Section 8) ---------------------------------------------
    alpha_adj: float
    p1_bar: float
    p1_true_share: float
    p2_net_threshold: float
    p2_true_share: float
    p3_true_share: float

    # --- Section 0 bars ------------------------------------------------------
    power_go_floor: float
    power_blocked_floor: float

    # --- horizons and anchors (Sections 3, 7) -------------------------------
    horizon_primary_days: int
    horizon_secondary_days: int
    entry_anchor_offset_days: int
    listing_tolerance_days: int

    # --- costs, round trip in bp (Section 5): (low, central, high) ----------
    vanilla_round_trip_bp: tuple[float, float, float]
    hip3_round_trip_bp: tuple[float, float, float]

    # --- matched control (Section 6) ----------------------------------------
    control_min_age_days: int
    control_trailing_window_hours: int

    # --- eligibility (A.2 Task 2) -------------------------------------------
    funding_coverage_bar: float
    retro_history_required_days: int
    interim_deadline: str
    projection_deadline: str
    # Amendment 1: the venue funding archive epoch, measured 2026-08-27.
    # First funding rows at or before this instant are archive-start
    # censoring, not listings; candles before it are index backfill.
    funding_archive_epoch_ms: int

    # --- collectors (Stage A.3) ---------------------------------------------
    watcher_poll_minutes: int
    checkpoint_offsets_days: tuple[int, int, int]
    catch_up_window_days: int
    min_outcome_coverage_candles: float
    min_outcome_coverage_funding: float
    spread_snapshot_window_minutes: int
    backfill_candle_start_offset_days: int
    backfill_candle_end_offset_days: int
    backfill_funding_start_offset_hours: int
    backfill_funding_end_offset_days: int

    # --- priors (Section 13) -------------------------------------------------
    assistant_prior_edge: float
    assistant_prior_stage_b: float

    # --- the register (Amendment 4): familywise budget -----------------------
    # alpha_h = 1 - family_confidence ** (1/k), k fixed by the A.2 cull.
    family_confidence: float

    # --- H2, the age-contrast pair (registrations/H2) ------------------------
    # Generating-sample-derived true shares: P3 pair share 114/175 = 0.651.
    h2_e1_true_share: float
    h2_e2_true_share: float
    # E2's economic floor: pair net at or above this multiple of the pair's
    # registered central cost.
    h2_cost_floor_multiple: float

    # --- H3, the population-corrected naive short (registrations/H3) ---------
    # Main-dex share positive, generating-sample-derived (107/158 = 0.677).
    h3_share_positive_true: float
    # The magnitude leg's honest range: the H1 registered assumption and the
    # H1 measured overall share (111/312 = 0.356); the generating figure
    # governs the cull, the registered figure is reported beside it.
    h3_magnitude_true_h1_registered: float
    h3_magnitude_true_generating: float

    # --- H4, the funding-conditioned short (registrations/H4) ----------------
    # The pre-registered threshold grid, percent per year, signed; the
    # conditioning feature is the trailing 168h mean hourly funding at entry.
    h4_funding_thresholds_annualized: tuple[float, float, float]
    # The honest range for the conditional share positive: the H1 registered
    # P1 assumption and the generating-sample overall (197/312 = 0.631); the
    # generating figure governs the cull.
    h4_true_share_h1_registered: float
    h4_true_share_generating: float

    # --- register priors (one Section 13 analog per hypothesis) --------------
    h2_assistant_prior_edge: float
    h2_assistant_prior_bars: float
    h3_assistant_prior_bars: float
    h4_assistant_prior_bars: float

    def field_names(self) -> tuple[str, ...]:
        return tuple(f.name for f in fields(self))


CONFIG: Final = Config(
    info_url="https://api.hyperliquid.xyz/info",
    # Zero dollars. Keyless public endpoints only. The ledger charges before
    # sending and refuses past this cap, naming the arithmetic.
    request_cap_per_day=20_000,
    request_timeout_seconds=30.0,
    alpha_adj=ALPHA_ADJ,
    # P1: exact binomial lower confidence bound on the share of events with a
    # positive 30-day net short return, bar at or above 0.60; power at 0.85.
    p1_bar=0.60,
    p1_true_share=0.85,
    # P2: exact sign test on the share of events at or below -15 percent net.
    p2_net_threshold=-0.15,
    p2_true_share=0.65,
    # P3: exact sign test on paired young-minus-control differentials, negative.
    p3_true_share=0.70,
    power_go_floor=0.80,
    power_blocked_floor=0.50,
    horizon_primary_days=30,
    horizon_secondary_days=90,
    # Entry is the second daily close: the close of listing day plus one.
    entry_anchor_offset_days=1,
    listing_tolerance_days=1,
    # Round trip, bp: (low, central, high). Vanilla from the venue's 1.5 maker
    # / 4.5 taker per side; HIP-3 builder markets default to double fees.
    vanilla_round_trip_bp=(3.0, 9.0, 18.0),
    hip3_round_trip_bp=(6.0, 18.0, 36.0),
    control_min_age_days=180,
    control_trailing_window_hours=168,
    funding_coverage_bar=0.95,
    retro_history_required_days=90,
    interim_deadline="2026-12-31",
    projection_deadline="2027-03-31",
    # 2023-05-12T00:00:00Z, measured on 5 of 5 venue-launch-era instruments.
    funding_archive_epoch_ms=1_683_849_600_000,
    watcher_poll_minutes=60,
    checkpoint_offsets_days=(2, 32, 92),
    catch_up_window_days=5,
    min_outcome_coverage_candles=0.90,
    min_outcome_coverage_funding=0.95,
    spread_snapshot_window_minutes=30,
    backfill_candle_start_offset_days=-1,
    backfill_candle_end_offset_days=91,
    backfill_funding_start_offset_hours=-168,
    backfill_funding_end_offset_days=91,
    # Assistant priors, recorded 2026-08-26 in chat. The NPD Amendment 0
    # lesson: an adopted prior corrupts the calibration ledger. The operator
    # slot in REGISTRATION.md Section 13 stays empty until the operator fills
    # it, and the empty slot blocks Stage B structurally.
    assistant_prior_edge=0.20,
    assistant_prior_stage_b=0.40,
    # The register familywise budget: 0.05 across the survivors of the cull.
    family_confidence=0.95,
    # H2 assumptions, generating-sample-derived and labelled so in the
    # registration: E1 from the P3 pair share 114/175 = 0.651, E2 one notch
    # under it for the economic floor.
    h2_e1_true_share=0.65,
    h2_e2_true_share=0.60,
    h2_cost_floor_multiple=2.0,
    # H3 assumptions: main-dex share positive 107/158 (generating sample);
    # the magnitude leg's honest range (H1 registered / H1 measured overall).
    h3_share_positive_true=0.677,
    h3_magnitude_true_h1_registered=0.65,
    h3_magnitude_true_generating=0.356,
    # H4: the registered threshold grid, signed percent per year, and the
    # conditional-share honest range (H1 registered / generating overall).
    h4_funding_thresholds_annualized=(-0.10, -0.20, -0.40),
    h4_true_share_h1_registered=0.85,
    h4_true_share_generating=0.631,
    # Register assistant priors, recorded 2026-08-28 in chat. The adoption
    # warning carries over verbatim; the three operator slots stay empty.
    h2_assistant_prior_edge=0.25,
    h2_assistant_prior_bars=0.35,
    h3_assistant_prior_bars=0.10,
    h4_assistant_prior_bars=0.05,
)
