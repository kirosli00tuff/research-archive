"""Frozen rho, the registered projection, and the append discipline."""
import statistics
from pathlib import Path

import pytest

from hfexperiment.accrual import Ledgers, open_ledgers
from hfexperiment.registered import (
    PROJECTION_CLEAR_HURDLE_DAY,
    PROJECTION_CLEAR_ZERO_DAY,
    PROJECTION_MEAN_BP,
    PROJECTION_SIGMA_BP,
    RHO_FROZEN,
    THRESHOLDS,
)
from hfexperiment.verdict import (
    confidence_bounds,
    first_crossing_day,
    tuned_rho,
)
from hfexperiment.verdictengine import recompute_and_append, width_verdict


def test_frozen_rho_matches_the_registered_value_to_full_precision() -> None:
    assert RHO_FROZEN == 0.071641
    assert round(tuned_rho(), 6) == RHO_FROZEN


def test_registered_projection_reproduces_from_the_frozen_rho() -> None:
    zero_day = first_crossing_day(
        PROJECTION_MEAN_BP, PROJECTION_SIGMA_BP, RHO_FROZEN, 0.0
    )
    hurdle_day = first_crossing_day(
        PROJECTION_MEAN_BP,
        PROJECTION_SIGMA_BP,
        RHO_FROZEN,
        THRESHOLDS.cost_hurdle_bp_per_day,
    )
    assert zero_day == PROJECTION_CLEAR_ZERO_DAY == 2061
    assert hurdle_day == PROJECTION_CLEAR_HURDLE_DAY == 2852


def _seed(ledgers: Ledgers, width: int, values: list[float],
          offset: int = 2) -> None:
    for i, bp in enumerate(values):
        ledgers.accrual.append(
            {
                "kind": "accrual",
                "status": "computed",
                "session": f"2026-09-{i + offset:02d}",
                "width": width,
                "formation_date": "2026-09-01",
                "excess_bp": bp,
                "run_utc": "seed",
            }
        )


def test_engine_appends_only_on_new_information(tmp_path: Path) -> None:
    ledgers = open_ledgers(tmp_path)
    # Pre-start: nothing to recompute, the verdict ledger stays empty.
    assert recompute_and_append(ledgers, "r0") == []
    assert ledgers.verdict.read_all() == []
    _seed(ledgers, 5, [30.0, -10.0])
    appended = recompute_and_append(ledgers, "r1")
    assert len(appended) == 1
    record = appended[0]
    assert record["width"] == 5
    assert record["t"] == 2
    assert record["rho"] == RHO_FROZEN
    mean = statistics.fmean([30.0, -10.0])
    sigma = statistics.stdev([30.0, -10.0])
    lower, upper = confidence_bounds(mean, sigma, 2, RHO_FROZEN, 0.05)
    assert record["mean_bp"] == pytest.approx(mean)
    assert record["lower_bp"] == pytest.approx(lower)
    assert record["upper_bp"] == pytest.approx(upper)
    assert record["state"] == "continue"
    assert record["projection"]["clear_zero_day"] == 2061
    assert record["projection"]["clear_hurdle_day"] == 2852
    # Idempotent: same information appends nothing.
    assert recompute_and_append(ledgers, "r2") == []
    # New information appends again, history untouched.
    _seed(ledgers, 5, [5.0], offset=4)
    again = recompute_and_append(ledgers, "r3")
    assert len(again) == 1
    assert again[0]["t"] == 3
    assert len(ledgers.verdict.read_all()) == 2


def test_secondary_widths_spend_their_registered_alpha() -> None:
    record = width_verdict(
        20, [("2026-09-02", 1.0), ("2026-09-03", 2.0)], "r"
    )
    assert record["alpha"] == THRESHOLDS.secondary_alpha_one_sided == 0.025
    primary = width_verdict(
        5, [("2026-09-02", 1.0), ("2026-09-03", 2.0)], "r"
    )
    assert primary["alpha"] == THRESHOLDS.alpha_one_sided == 0.05


def test_one_observation_has_no_bounds_and_continues() -> None:
    record = width_verdict(5, [("2026-09-02", 30.0)], "r")
    assert record["t"] == 1
    assert record["lower_bp"] is None
    assert record["upper_bp"] is None
    assert record["state"] == "continue"
