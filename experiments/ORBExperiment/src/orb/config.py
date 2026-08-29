"""The registered configuration. Every field is enforced by Guard 2.

Guard 2 walks the parse tree of every module and requires that each field of
:class:`Config` is read by a module **outside** ``config.py``, or else sits on
``PENDING_ENFORCEMENT`` in ``tests/test_guards.py`` with the task that will
enforce it named. A config key nobody reads is a registered intention nobody
implemented.

Nothing here is a measured figure. Measured figures live in ``reports/`` and in
``REGISTRATION.md`` amendments, and every one travels with its n.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, final


@final
@dataclass(frozen=True, slots=True)
class Config:
    """Registered constants. Frozen at registration; moved only by amendment."""

    # --- Windows, Section 7 -------------------------------------------
    pre_period_end_ms: int
    """2016-01-04T14:30:00.000Z, exclusive. The pre-period carve-out boundary."""

    in_sample_start: str
    """2016-01-04. First session of the in-sample window."""

    in_sample_end: str
    """2022-12-30. Last session of the in-sample window."""

    holdout_start: str
    """2023-01-03. First session of the holdout. Pinned."""

    holdout_end: str
    """2026-06-30. Last session of the holdout. Pinned."""

    # --- Universe and event rule, Section 2 ---------------------------
    opening_range_minutes: int
    """5. The registered range length. 15/30/60 are named secondaries."""

    selection_width: int
    """20. Top-N by opening relative volume. 10 and 40 are named secondaries."""

    relvol_lookback_sessions: int
    """14. Trailing sessions for the median first-5-minute volume denominator."""

    min_session_open_usd: float
    """5.00. Section 2 price filter."""

    min_avg_volume_shares: int
    """1,000,000. Section 2 14-session average volume filter."""

    min_atr_usd: float
    """0.50. Section 2 14-session ATR filter."""

    max_borrow_rate_annual: float
    """0.25. Above this, or with no locate, the name is excluded on the short side."""

    # --- Entry and exit, Section 3 ------------------------------------
    entry_offset_fraction: float
    """0.0005. Marketable limit at the range boundary plus 5 bp of price."""

    # --- Sizing, Section 4 --------------------------------------------
    risk_fraction_per_trade: float
    """0.0025. Equal risk, 0.25 percent of equity, entry-to-stop distance."""

    max_concurrent_positions: int
    """20."""

    max_gross_notional_multiple: float
    """1.0. No leverage, no compounding, constant equity base."""

    # --- Costs, Section 6 ---------------------------------------------
    commission_per_share_usd: float
    """0.0035, carried from IBKR. Re-verified live at A.2 TASK 2."""

    commission_order_minimum_usd: float
    """0.35, carried. Re-verified live at A.2 TASK 2."""

    finra_taf_per_share_sold_usd: float
    """0.000166, carried. Re-verified live at A.2 TASK 2."""

    entry_slippage_usd: tuple[float, float, float]
    """(0.010, 0.020, 0.040) — optimistic, central, pessimistic, per share."""

    stop_slippage_usd: tuple[float, float, float]
    """(0.020, 0.040, 0.080). Wider: a stop is marketable and gap-prone."""

    close_slippage_usd: tuple[float, float, float]
    """(0.005, 0.010, 0.020)."""

    # --- Inference, Section 8 -----------------------------------------
    n_co_primaries: int
    """2. alpha_adj = 1 - 0.95 ** (1 / n_co_primaries)."""

    trial_count: int
    """8. Four range lengths crossed with two entry rules, for the DSR."""

    deflated_sharpe_bar: float
    """1.00. E1 bar."""

    holdout_per_trade_t_gate: float
    """2.50. Registered openly against the 2.62 the holdout yields."""

    max_single_year_pnl_share: float
    """0.50. Concentration gate; the replication's 2022 share was 0.76."""

    min_positive_holdout_years: int
    """3 of 4 holdout calendar years."""

    # --- Power, Section 9 ---------------------------------------------
    registered_sharpe_assumption: float
    """1.40 annualized net, half the published 2.81."""

    published_sharpe_assumption: float
    """2.81, the source study's reported figure."""

    quartered_sharpe_assumption: float
    """0.70."""

    trading_days_per_year: int
    """252."""

    target_power: float
    """0.80."""

    blocked_power_floor: float
    """0.50."""

    # --- Integrity verdicts, A.1 TASK 3 and TASK 4 --------------------
    revision_pass_max_share: float
    """0.005. At or below is PASS."""

    revision_partial_max_share: float
    """0.020. Above is FAIL and fires BLOCKED."""

    agreement_pass_min_share: float
    """0.95 of session-ticker pairs agreeing on the first-5-minute high or low."""

    agreement_partial_min_share: float
    """0.85. Below is FAIL and fires BLOCKED."""

    delisted_pass_min_count: int
    """100 delisted names served with intraday history."""

    delisted_partial_min_count: int
    """20. Below is FAIL and fires BLOCKED."""

    revision_repull_wait_days: int
    """14 calendar days. This is why Stage A cannot finish in one session."""

    probe_sessions: int
    """60 consecutive regular sessions."""

    probe_tickers: int
    """40 alphabetically-first symbols meeting the sealed liquidity screen."""

    probe_min_age_days: int
    """30. The probe slice ends at least this far before today."""

    # --- Sizing constraint carried from HFExperiment ------------------
    integer_shares_only: bool
    """True. IBKR refuses fractional API orders, error 10243."""


CONFIG: Final[Config] = Config(
    pre_period_end_ms=1_451_917_800_000,
    in_sample_start="2016-01-04",
    in_sample_end="2022-12-30",
    holdout_start="2023-01-03",
    holdout_end="2026-06-30",
    opening_range_minutes=5,
    selection_width=20,
    relvol_lookback_sessions=14,
    min_session_open_usd=5.00,
    min_avg_volume_shares=1_000_000,
    min_atr_usd=0.50,
    max_borrow_rate_annual=0.25,
    entry_offset_fraction=0.0005,
    risk_fraction_per_trade=0.0025,
    max_concurrent_positions=20,
    max_gross_notional_multiple=1.0,
    commission_per_share_usd=0.0035,
    commission_order_minimum_usd=0.35,
    finra_taf_per_share_sold_usd=0.000166,
    entry_slippage_usd=(0.010, 0.020, 0.040),
    stop_slippage_usd=(0.020, 0.040, 0.080),
    close_slippage_usd=(0.005, 0.010, 0.020),
    n_co_primaries=2,
    trial_count=8,
    deflated_sharpe_bar=1.00,
    holdout_per_trade_t_gate=2.50,
    max_single_year_pnl_share=0.50,
    min_positive_holdout_years=3,
    registered_sharpe_assumption=1.40,
    published_sharpe_assumption=2.81,
    quartered_sharpe_assumption=0.70,
    trading_days_per_year=252,
    target_power=0.80,
    blocked_power_floor=0.50,
    revision_pass_max_share=0.005,
    revision_partial_max_share=0.020,
    agreement_pass_min_share=0.95,
    agreement_partial_min_share=0.85,
    delisted_pass_min_count=100,
    delisted_partial_min_count=20,
    revision_repull_wait_days=14,
    probe_sessions=60,
    probe_tickers=40,
    probe_min_age_days=30,
    integer_shares_only=True,
)
