"""Frozen experiment configuration.

Six Level 1 keys in AiTrader were parsed, validated, printed at startup, and
enforced nowhere. Every field declared here must be referenced by at least one
module under src/insider outside this file. tests/test_guards.py fails when a
field has no enforcement site, so a key cannot be added as decoration.

Values here are registered in REGISTRATION.md and frozen before Task 4 computes
anything. Changing one after the corpus is built requires a numbered amendment.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final


@dataclass(frozen=True, slots=True)
class Config:
    """Registered parameters. Frozen at A.1, amended only by numbered amendment."""

    # --- span --------------------------------------------------------------
    universe_id: str
    benchmark_id: str
    bars_start: str
    bars_end: str
    event_span_start: str
    event_span_end: str
    lookback_start: str

    # --- SEC access --------------------------------------------------------
    sec_user_agent_env: str
    sec_requests_per_second: float
    sec_request_timeout_seconds: float
    sec_max_retries: int
    sec_backoff_base_seconds: float
    sec_backoff_max_seconds: float
    sec_retry_status_codes: tuple[int, ...]
    dera_first_quarter: str
    dera_last_quarter: str

    # --- ex-ante classification rule, frozen at Task 3 ---------------------
    allowed_transaction_codes: tuple[str, ...]
    lookback_trade_codes: tuple[str, ...]
    allowed_roles: tuple[str, ...]
    excluded_roles: tuple[str, ...]
    min_transaction_usd: float
    exclude_10b5_1: bool
    routine_consecutive_years: int
    min_history_years: int
    cluster_min_filers: int
    cluster_window_days: int
    johnsen_same_date_price_fraction: float

    # --- portfolio ---------------------------------------------------------
    primary_hold_sessions: int
    secondary_hold_sessions: tuple[int, ...]
    entry_lag_sessions: int
    primary_weighting: str
    secondary_weighting: str
    sessions_per_month: int

    # --- cost band, measured by the operator -------------------------------
    spread_bp_low: float
    spread_bp_high: float
    round_trip_bp_low: float
    round_trip_bp_high: float

    # --- Section 0 bars, registered before Task 4 --------------------------
    mde_go_ceiling_bp: float
    mde_degraded_ceiling_bp: float
    corpus_event_floor: int
    corpus_coverage_floor: float

    # --- inference ---------------------------------------------------------
    t_critical: float
    newey_west_lags: int
    newey_west_lag_grid: tuple[int, ...]
    decayed_gross_band_bp: tuple[float, float]

    # --- priors ------------------------------------------------------------
    assistant_prior: float

    def field_names(self) -> tuple[str, ...]:
        return tuple(f.name for f in fields(self))


CONFIG: Final = Config(
    universe_id="U-LIQ-500-stk-w60-m40-p5",
    benchmark_id="U-LIQ-500-VW",
    # The first formation date the source universe carries, and the last daily
    # bar in the source store. Both read from analysis_bars.db at A.1 and fixed.
    bars_start="2016-04-01",
    bars_end="2026-08-25",
    # Events are admitted through the last complete DERA quarter. Their holds
    # run past that date and are truncated at the bar end, which shortens a
    # book but cannot bias a second moment.
    event_span_start="2016-04-01",
    event_span_end="2026-03-31",
    # Three calendar years before the first event, so the Cohen-Malloy-Pomorski
    # rule has its full look-back on day one of the event span.
    lookback_start="2013-01-01",
    sec_user_agent_env="SEC_USER_AGENT",
    # The SEC states a ceiling of ten requests per second. Eight leaves headroom
    # for clock skew and for any other process on this machine.
    sec_requests_per_second=8.0,
    sec_request_timeout_seconds=120.0,
    sec_max_retries=5,
    sec_backoff_base_seconds=2.0,
    sec_backoff_max_seconds=60.0,
    sec_retry_status_codes=(403, 429, 500, 502, 503, 504),
    dera_first_quarter="2013q1",
    dera_last_quarter="2026q1",
    # Purchases only. Sales carry diversification and liquidity motives and no
    # study finds signal in them. P is the open-market purchase code. A grants,
    # M option exercises and F tax withholding are not discretionary purchases.
    allowed_transaction_codes=("P",),
    # The routine rule reads discretionary open-market trades only. Including A
    # grants would make almost every insider routine, because grants land in the
    # same calendar month every year by design.
    lookback_trade_codes=("P", "S"),
    allowed_roles=("officer", "director"),
    excluded_roles=("tenpercentowner",),
    min_transaction_usd=10_000.0,
    exclude_10b5_1=True,
    routine_consecutive_years=3,
    min_history_years=3,
    cluster_min_filers=3,
    cluster_window_days=5,
    johnsen_same_date_price_fraction=0.80,
    # Six months. It amortizes the round trip across the holding period and is
    # the short-swing horizon.
    primary_hold_sessions=126,
    secondary_hold_sessions=(21, 63),
    # A public filer reads the filing after it posts, so entry is the close of
    # the first session strictly after the filing date.
    entry_lag_sessions=1,
    primary_weighting="value_weighted",
    secondary_weighting="equal_weighted",
    sessions_per_month=21,
    spread_bp_low=15.8,
    spread_bp_high=50.0,
    round_trip_bp_low=32.0,
    round_trip_bp_high=100.0,
    mde_go_ceiling_bp=20.0,
    mde_degraded_ceiling_bp=40.0,
    corpus_event_floor=1_000,
    corpus_coverage_floor=0.80,
    t_critical=2.0,
    # One trading month. Membership persists for the hold, so the standard
    # automatic bandwidth is too short here. The grid is reported beside it.
    newey_west_lags=21,
    newey_west_lag_grid=(5, 21, 63, 126),
    decayed_gross_band_bp=(30.0, 40.0),
    assistant_prior=0.12,
)
