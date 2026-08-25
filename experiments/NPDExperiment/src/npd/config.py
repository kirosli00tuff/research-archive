"""Frozen experiment configuration.

Six configuration keys in the predecessor system were enforced nowhere. Every
field declared here must be referenced by at least one module under src/npd
outside this file. tests/test_guards.py fails when a field has no enforcement
site, so a key cannot be added as decoration.

Values here are registered. Changing one after B.1 starts requires a numbered
amendment in REGISTRATION.md.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, fields
from typing import Final


@dataclass(frozen=True, slots=True)
class Config:
    """Registered parameters. Frozen at A.2, amended only by numbered amendment."""

    # --- gate model, verified at A.2.0 -------------------------------------
    gate_model: str
    knowledge_cutoff: dt.date
    cutoff_source_url: str
    cutoff_retrieved_on: dt.date
    guard_band_months: int
    window_end: dt.date
    min_trading_days: int

    # --- task --------------------------------------------------------------
    universe_id: str
    panel_size: int
    panel_seed: int
    strata_count: int
    primary_horizon_sessions: int
    secondary_horizon_sessions: int
    feature_names: tuple[str, ...]

    # --- model call --------------------------------------------------------
    temperature: float
    max_output_tokens: int
    reasoning_effort: str
    request_timeout_seconds: float
    max_retries: int
    backoff_base_seconds: float
    backoff_max_seconds: float

    # --- spend -------------------------------------------------------------
    spend_cap_usd: float
    batch_size: int
    price_input_per_mtok_usd: float
    price_cached_input_per_mtok_usd: float
    price_output_per_mtok_usd: float

    # --- Section 0 coverage bars ------------------------------------------
    coverage_go_floor: float
    coverage_degraded_floor: float

    # --- inference, used only by the B.2 evaluator -------------------------
    bootstrap_resamples: int
    permutation_resamples: int
    t_critical: float
    realistic_effect_band: tuple[float, float]

    def field_names(self) -> tuple[str, ...]:
        return tuple(f.name for f in fields(self))


CONFIG: Final = Config(
    gate_model="gpt-5-2025-08-07",
    knowledge_cutoff=dt.date(2024, 9, 30),
    cutoff_source_url="https://developers.openai.com/api/docs/models/gpt-5",
    cutoff_retrieved_on=dt.date(2026, 8, 25),
    guard_band_months=1,
    window_end=dt.date(2026, 7, 24),
    min_trading_days=200,
    universe_id="U-LIQ-500-stk-w60-m40-p5",
    panel_size=30,
    panel_seed=20260825,
    strata_count=5,
    primary_horizon_sessions=5,
    secondary_horizon_sessions=1,
    feature_names=(
        "ret_1",
        "ret_5",
        "ret_10",
        "ret_20",
        "ret_60",
        "rvol_20",
        "rvol_60",
        "dvol_z_60",
        "vtrend_5_60",
    ),
    temperature=0.0,
    max_output_tokens=4096,
    reasoning_effort="low",
    request_timeout_seconds=180.0,
    max_retries=5,
    backoff_base_seconds=2.0,
    backoff_max_seconds=60.0,
    spend_cap_usd=10.0,
    batch_size=50,
    price_input_per_mtok_usd=1.25,
    price_cached_input_per_mtok_usd=0.125,
    price_output_per_mtok_usd=10.0,
    coverage_go_floor=0.90,
    coverage_degraded_floor=0.70,
    bootstrap_resamples=10_000,
    permutation_resamples=10_000,
    t_critical=2.0,
    realistic_effect_band=(0.01, 0.05),
)
