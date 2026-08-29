"""The registered cost model instance — only measured figures, frozen and hashed.

**Every parameter here was verified live on 2026-08-29 against the vendor's own
published schedule**, under standing rule 4 and the MLCryptoEngine ADR-055
pattern: a carried fee is a **dated measurement**, never a constant, and the
measured figure wins.

One parameter is deliberately **incomplete and refuses rather than guesses**.
The SEC Section 31 rate is required *per session date* by Section 6. One rate
was measured; **its effective date was not**, and `sec.gov` returned HTTP 403
*"Request Rate Threshold Exceeded"* on two attempts. The schedule therefore
holds no entry covering the registered window, and
:meth:`orb.costs.SecFeeSchedule.rate_on` returns `Absent` for every session in
it. **The model refuses to price a trade rather than take a fee from the wrong
year.**
"""

from __future__ import annotations

from datetime import date
from typing import Final

from orb.costs import CostModel, SecFeeSchedule

MEASURED_ON: Final[date] = date(2026, 8, 29)
"""The date every figure below was re-verified live."""

SEC_RATE_MEASURED: Final[float] = 0.0000206
"""USD per dollar of aggregate sales. Measured; **effective date unmeasured**."""

SEC_FEE_SCHEDULE: Final[SecFeeSchedule] = SecFeeSchedule(
    effective_dates=(),
    rates_per_dollar=(),
)
"""Empty **on purpose**. See the module docstring.

The one measured rate is recorded in :data:`SEC_RATE_MEASURED` and is **not**
placed in the schedule, because placing it would require inventing an effective
date and would silently apply a 2026 rate to a 2016 session. An empty schedule
makes every session in the registered window return a recorded absence, which is
the true state.
"""

REGISTERED_COST_MODEL: Final[CostModel] = CostModel(
    commission_per_share=0.0035,
    commission_order_minimum=0.35,
    commission_max_fraction_of_trade_value=0.01,
    finra_taf_per_share_sold=0.000195,
    finra_cat_per_share=0.000003,
    clearing_per_share=0.00020,
    sec_fees=SEC_FEE_SCHEDULE,
    entry_slippage=(0.010, 0.020, 0.040),
    stop_slippage=(0.020, 0.040, 0.080),
    close_slippage=(0.005, 0.010, 0.020),
)

MEASURED_AGAINST_CARRIED: Final[dict[str, tuple[float | None, float, str]]] = {
    # name: (carried, measured, verdict)
    "commission_per_share": (0.0035, 0.0035, "agrees"),
    "commission_order_minimum": (0.35, 0.35, "agrees"),
    "finra_taf_per_share_sold": (0.000166, 0.000195, "CARRIED FIGURE IS STALE"),
    "commission_max_fraction_of_trade_value": (None, 0.01, "NOT PREVIOUSLY MODELED"),
    "finra_cat_per_share": (None, 0.000003, "NOT PREVIOUSLY MODELED"),
    "clearing_per_share": (None, 0.00020, "NOT PREVIOUSLY MODELED"),
    "sec_rate": (None, SEC_RATE_MEASURED, "measured, effective date unmeasured"),
}
"""Measured against carried, in one place, for the amendment and the report."""
