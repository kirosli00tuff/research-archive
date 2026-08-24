"""Deferred parameters refuse as values, and the hurdle pins to the data."""
import json
import statistics as st
from pathlib import Path

import pytest

from hfexperiment.costmodel import Regime, daily_cost_hurdle_bp, round_trip
from hfexperiment.registered import (
    CHURN_NAMES_PER_MONTH,
    DEFERRED_PARAMETERS,
    PER_NAME_NOTIONAL_USD,
    THRESHOLDS,
    DeferredParameter,
    DeferredParameterError,
    resolve,
)

ROOT = Path(__file__).resolve().parent.parent
REGISTRATION = ROOT / "REGISTRATION.md"
SPREADS_JSON = ROOT / "reports/stage_a2/book_spreads.json"
WIDTH5_NAMES = ("WOLF", "AXTI", "SNDK", "BE", "LITE")


def test_deferred_parameters_are_not_numbers() -> None:
    for param in DEFERRED_PARAMETERS:
        assert isinstance(param, DeferredParameter)
        assert not isinstance(param, int | float)


def test_resolve_refuses_a_deferred_parameter_by_name() -> None:
    with pytest.raises(DeferredParameterError) as exc:
        resolve(PER_NAME_NOTIONAL_USD)
    assert "per_name_notional_usd" in str(exc.value)
    assert "Amendment 1" in str(exc.value)


def test_resolve_passes_a_real_value_through() -> None:
    assert resolve(45.0) == 45.0


def test_every_deferred_parameter_is_marked_in_the_registration() -> None:
    text = REGISTRATION.read_text()
    for param in DEFERRED_PARAMETERS:
        assert param.name in text, (
            f"{param.name} is deferred in code but absent from "
            f"REGISTRATION.md"
        )
    assert "DEFERRED" in text


def test_registered_hurdle_re_derives_from_the_measured_spreads() -> None:
    """The same derivation scripts/cost_table_a2.py prints."""
    per_name = json.loads(SPREADS_JSON.read_text())["per_name"]
    w5 = [per_name[s] for s in WIDTH5_NAMES]
    w5_spread = st.median(v["median_bp"] for v in w5)
    w5_mid = st.median(v["median_mid"] for v in w5)
    rt = round_trip(
        Regime.FRACTIONAL, 900.0 / THRESHOLDS.primary_width, w5_mid,
        w5_spread,
    )
    hurdle = daily_cost_hurdle_bp(
        THRESHOLDS.primary_width,
        CHURN_NAMES_PER_MONTH[THRESHOLDS.primary_width],
        rt.total_rt_bp,
    )
    assert THRESHOLDS.cost_hurdle_bp_per_day == pytest.approx(
        hurdle, abs=0.005
    )


def test_widths_agree_between_thresholds_and_churn_table() -> None:
    assert THRESHOLDS.primary_width in CHURN_NAMES_PER_MONTH
    assert THRESHOLDS.traded_width in CHURN_NAMES_PER_MONTH
    assert THRESHOLDS.traded_width in THRESHOLDS.secondary_widths
