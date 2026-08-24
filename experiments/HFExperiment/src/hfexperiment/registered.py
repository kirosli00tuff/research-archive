"""The registered thresholds and the deferred parameters, as code.

Every numeric threshold REGISTRATION.md registers lives here as a field,
and tests/test_structural_guard.py fails if any field lacks a consumption
site outside this file. A registered number nothing enforces is
decoration, and decoration drifts.

A deferred parameter is not a placeholder value. It is a DeferredParameter
instance, and any attempt to use it as a number raises. A later stage
cannot read 45.0 where the registration says DEFERRED, because there is no
45.0 to read.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeferredParameter:
    """A registered parameter whose value waits on a named amendment.

    Machine-detectable on purpose. resolve() raises on it, so code that
    needs the value refuses until the amendment lands.
    """

    name: str
    amendment: str
    reason: str


class DeferredParameterError(RuntimeError):
    """A deferred parameter was used where a value is required."""


def resolve(value: float | DeferredParameter) -> float:
    """The numeric value, or a refusal naming the pending amendment."""
    if isinstance(value, DeferredParameter):
        raise DeferredParameterError(
            f"{value.name} is DEFERRED to {value.amendment}: {value.reason}"
        )
    return value


@dataclass(frozen=True)
class RegisteredThresholds:
    """Registration sections 4, 8, 9 and 11 as enforceable numbers.

    restart_floor_usd is a RESTART bar, not a termination. Breach halts
    the sleeve and waits for an explicit operator decision. Fill history
    survives. kill.py enforces the distinction.
    """

    # Section 9. Total account equity in USD. 500 is 1.31 sigma of the
    # width-20 annual tracking error on 900 deployed, driftless touch
    # probability near 19 percent in year one before beta inflation.
    restart_floor_usd: float = 500.0
    # Section 8. Cumulative commission plus regulatory spend per rolling
    # 365 days. About 1.75x the worst-case fractional-regime projection.
    spend_cap_usd_per_year: float = 100.0
    # Section 4. Verdict width and traded width, chosen for different
    # objectives on the already-spent holdout.
    primary_width: int = 5
    traded_width: int = 20
    secondary_widths: tuple[int, ...] = (20, 50)
    # Section 11. One-sided level for the primary, Bonferroni within the
    # secondary family.
    alpha_one_sided: float = 0.05
    secondary_alpha_one_sided: float = 0.025
    crossing_target_days: int = 1600
    futility_bp_per_day: float = 10.0
    # Section 11. The success hurdle in bp per day on the shadow series at
    # the primary width, computed at registration from the measured cost
    # model under the worst-case fractional regime: width 5, churn 2.0
    # names per month, 180 USD per name, round trip 213.84 bp with the
    # measured 13.08 bp width-5 spread. Derivation in
    # reports/stage_a2/cost_table.md and scripts/cost_table_a2.py, pinned
    # by tests/test_registered.py.
    cost_hurdle_bp_per_day: float = 4.07


THRESHOLDS = RegisteredThresholds()

# Measured churn, A.1 Task 4, names per month over the last 6 formations.
# Two legs per churned name gives the fill rate the drag arithmetic uses.
CHURN_NAMES_PER_MONTH: dict[int, float] = {5: 2.0, 20: 5.2}

# Deferred parameters. Amendment 1 must land before the first live order.
PER_NAME_NOTIONAL_USD = DeferredParameter(
    name="per_name_notional_usd",
    amendment="Amendment 1",
    reason="the billing regime of a mixed integer-plus-fraction order "
           "decides it and only a paper fill measures that",
)
BROKER_MIN_NOTIONAL_USD = DeferredParameter(
    name="broker_min_notional_usd",
    amendment="Amendment 1",
    reason="MinSize and SizeIncrement come from reqContractDetails on a "
           "live-permissioned account that does not exist yet",
)
MIXED_ORDER_BILLING_REGIME = DeferredParameter(
    name="mixed_order_billing_regime",
    amendment="Amendment 1",
    reason="whether a mixed integer-plus-fraction order bills whole on "
           "the fractional schedule is not determinable from IBKR's page",
)

DEFERRED_PARAMETERS: tuple[DeferredParameter, ...] = (
    PER_NAME_NOTIONAL_USD,
    BROKER_MIN_NOTIONAL_USD,
    MIXED_ORDER_BILLING_REGIME,
)
