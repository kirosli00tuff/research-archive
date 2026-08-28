"""Frozen experiment configuration.

Every field declared here must be referenced by at least one module under
src/etf outside this file. tests/test_guards.py fails when a field has no
enforcement site, so a key cannot be added as decoration. Fields whose consumer
lands in a later Stage A task sit on the PENDING_ENFORCEMENT list in that test,
with the task named, and that list must be empty by the end of Stage A.3.

Values here are registered in REGISTRATION.md and frozen at Stage A.0, before
any network call. Changing one requires a numbered amendment.

The guard walks the parse tree rather than the text. A config key left behind
in a comment while the code that read it was replaced by a literal is the exact
shape of the defect this guard exists for, and a text search calls that
enforcement (InsiderExperiment mutation lesson, ADR-012 there).
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import UTC, datetime
from typing import Final

# alpha_adj = 1 - 0.95 ** (1/2): two co-primaries, family-wise 0.05, Sidak.
ALPHA_ADJ: Final = 1.0 - 0.95 ** (1.0 / 2.0)

# The pre-period carve-out boundary. Strictly before this instant, BTC price and
# funding are readable for power inputs; at or after it they are sealed.
# 2025-05-01T00:00:00Z.
PRE_PERIOD_END_MS: Final = int(datetime(2025, 5, 1, tzinfo=UTC).timestamp() * 1000)


@dataclass(frozen=True, slots=True)
class Config:
    """Registered parameters. Frozen at A.0, amended only by numbered amendment."""

    # --- access (Section 12) ------------------------------------------------
    hyperliquid_info_url: str
    kraken_ohlc_url: str
    wayback_availability_url: str
    wayback_timemap_url: str
    request_timeout_seconds: float
    user_agent: str
    request_cap_per_day_default: int
    request_cap_flow_per_day: int
    request_cap_archive_per_day: int
    request_cap_venue_per_day: int

    # --- universe (Section 2) -----------------------------------------------
    flow_universe_tickers: tuple[str, str, str, str, str]
    perp_coin: str

    # --- the print, the anchor, admissibility (Section 3) -------------------
    entry_anchor_hour_utc: int
    anchor_amendment_trigger_hour_utc: int
    anchor_amendment_percentile: float
    oos_start_date: str

    # --- signal and position (Section 4) ------------------------------------
    signal_threshold_usd: float

    # --- costs (Section 6), round trip in bp --------------------------------
    hyperliquid_round_trip_bp: tuple[float, float, float]
    kraken_spot_round_trip_bp: tuple[float, float]

    # --- horizons (Section 7) -----------------------------------------------
    horizon_primary_days: int
    reversal_horizon_max_days: int

    # --- inference (Section 8) ----------------------------------------------
    alpha_adj: float
    threshold_grid_usd: tuple[float, float, float, float]
    permutation_draws: int

    # --- power (Section 9) --------------------------------------------------
    rho_registered: float
    rho_undecayed: float
    rho_quartered: float
    power_go_floor: float
    power_blocked_floor: float
    power_simulations: int
    pre_period_end_date: str
    pre_period_end_ms: int
    interim_deadline: str
    projection_deadline: str

    # --- A.1 Task 3, the lag measurement ------------------------------------
    snapshot_peak_interval_minutes: int
    snapshot_offpeak_interval_hours: int
    snapshot_peak_start_hour_utc: int
    snapshot_peak_end_hour_utc: int
    lag_min_trading_days: int

    # --- A.1 Task 4, as-printed observability -------------------------------
    archive_density_pass_share: float
    revision_intact_pass_share: float
    retro_revision_sample_min: int
    revision_settle_hours: int

    # --- A.2 Task 3, sealed coverage ----------------------------------------
    min_outcome_coverage_candles: float
    min_outcome_coverage_funding: float

    # --- priors (Section 13) ------------------------------------------------
    assistant_prior_edge: float

    def field_names(self) -> tuple[str, ...]:
        return tuple(f.name for f in fields(self))


CONFIG: Final = Config(
    hyperliquid_info_url="https://api.hyperliquid.xyz/info",
    kraken_ohlc_url="https://api.kraken.com/0/public/OHLC",
    wayback_availability_url="https://archive.org/wayback/available",
    wayback_timemap_url="https://web.archive.org/web/timemap/link",
    request_timeout_seconds=30.0,
    # Identifies the collector honestly. A source that wishes to refuse this
    # project can do so by name; a disguised agent would make the recorded
    # terms of service unenforceable in the one direction that matters.
    user_agent="ETFExperiment/0.1 (measurement-only research; contact via repo)",
    # Zero dollars. Keyless public endpoints only. Provisional caps, registered
    # at A.0 and amended from the A.1 Task 2 measurement (Section 12).
    request_cap_per_day_default=2_000,
    request_cap_flow_per_day=200,
    request_cap_archive_per_day=2_000,
    request_cap_venue_per_day=5_000,
    # Section 2: the five largest US spot Bitcoin ETFs by assets, named
    # explicitly so the universe cannot drift with an AUM table.
    flow_universe_tickers=("IBIT", "FBTC", "GBTC", "ARKB", "BITB"),
    perp_coin="BTC",
    # Section 3: the provisional anchor. A.1 Task 3 may move it, once, by
    # amendment, from the measured 95th percentile first-print time.
    entry_anchor_hour_utc=8,
    anchor_amendment_trigger_hour_utc=7,
    anchor_amendment_percentile=0.95,
    oos_start_date="2025-05-01",
    # Section 4: T, matching the source study's 100M USD unit.
    signal_threshold_usd=100_000_000.0,
    # Section 6: (low, central, high). Central is taker both legs at the venue's
    # 4.5 bp taker per side. The 3 bp low end is maker both legs and is an
    # upper-bound-of-optimism, never the central case.
    hyperliquid_round_trip_bp=(3.0, 9.0, 18.0),
    # Kraken Pro base tier 0.25 maker / 0.40 taker per side (ADR-055, verified
    # live 2026-08-08): 50 bp maker round trip, 80 bp taker round trip.
    kraken_spot_round_trip_bp=(50.0, 80.0),
    horizon_primary_days=1,
    reversal_horizon_max_days=20,
    alpha_adj=ALPHA_ADJ,
    threshold_grid_usd=(0.0, 50_000_000.0, 100_000_000.0, 200_000_000.0),
    permutation_draws=20_000,
    # Section 9: the registered assumption is half the published next-day
    # effect. The published Newey-West t 3.12 over 313 days implies a rank
    # correlation near 0.18; the registered assumption is 0.09, and the
    # undecayed 0.18 and quartered 0.045 are reported beside it.
    rho_registered=0.09,
    rho_undecayed=0.18,
    rho_quartered=0.045,
    power_go_floor=0.80,
    power_blocked_floor=0.50,
    power_simulations=2_000,
    pre_period_end_date="2025-05-01",
    pre_period_end_ms=PRE_PERIOD_END_MS,
    interim_deadline="2026-12-31",
    projection_deadline="2027-03-31",
    # A.1 Task 3: every 20 minutes across the 20:00-14:00 UTC window that
    # brackets the print and revision window, every 2 hours otherwise.
    snapshot_peak_interval_minutes=20,
    snapshot_offpeak_interval_hours=2,
    snapshot_peak_start_hour_utc=20,
    snapshot_peak_end_hour_utc=14,
    lag_min_trading_days=15,
    # A.1 Task 4 verdict bars.
    archive_density_pass_share=0.60,
    revision_intact_pass_share=0.90,
    retro_revision_sample_min=30,
    revision_settle_hours=48,
    min_outcome_coverage_candles=0.95,
    min_outcome_coverage_funding=0.95,
    # Assistant prior, recorded 2026-08-27 in chat. The NPD Amendment 0 lesson:
    # an adopted prior corrupts the calibration ledger. The operator slot in
    # REGISTRATION.md Section 13 stays empty until the operator fills it, and
    # the empty slot blocks Stage B structurally.
    assistant_prior_edge=0.10,
)
