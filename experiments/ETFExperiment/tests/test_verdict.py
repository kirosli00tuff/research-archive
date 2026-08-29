"""The verdict machinery, dark: synthetic fixtures with known answers, and a canary."""

from __future__ import annotations

import ast
import pathlib
import random
from datetime import date, timedelta

import pytest

from etf.config import CONFIG
from etf.signal import Position
from etf.verdict import (
    SEALED_MARKERS,
    Day,
    SealedDataRefused,
    net_return,
    refuse_sealed_path,
    reversal_profile,
    run_e1,
    run_e2,
    run_secondaries,
)

T = CONFIG.signal_threshold_usd
COST = CONFIG.hyperliquid_round_trip_bp[1]


def noise_days(n: int, seed: int = 4) -> list[Day]:
    """A fixture with NO relationship. The primaries must not fire on it."""
    rng = random.Random(seed)
    start = date(2025, 5, 1)
    return [
        Day(
            trade_date=start + timedelta(days=i),
            signal_usd=rng.gauss(0.0, 250e6),
            forward_return=rng.gauss(0.0, 0.027),
            funding_sum=0.0005,
            revised=False,
            same_day_return=rng.gauss(0.0, 0.027),
        )
        for i in range(n)
    ]


def planted_days(n: int, seed: int = 5, strength: float = 0.9) -> list[Day]:
    """The planted-signal canary: the signal IS the return, up to a little noise."""
    rng = random.Random(seed)
    start = date(2025, 5, 1)
    days: list[Day] = []
    for i in range(n):
        z = rng.gauss(0.0, 1.0)
        days.append(
            Day(
                trade_date=start + timedelta(days=i),
                signal_usd=z * 250e6,
                forward_return=(strength * z + (1 - strength) * rng.gauss(0.0, 1.0)) * 0.027,
                funding_sum=0.0,
                revised=(i % 5 == 0),
                same_day_return=z * 0.027,
            )
        )
    return days


# --- the dark pin --------------------------------------------------------


@pytest.mark.parametrize("marker", SEALED_MARKERS)
def test_a_sealed_store_path_is_refused(marker: str) -> None:
    with pytest.raises(SealedDataRefused, match="synthetic fixtures"):
        refuse_sealed_path(f"/home/u/repo/{marker}/btc-1h-2026-08-01.json")


def test_a_fixture_path_is_permitted() -> None:
    assert refuse_sealed_path("tests/fixtures/planted.json").endswith("planted.json")


def test_the_module_imports_no_network_and_no_sealed_writer() -> None:
    tree = ast.parse(pathlib.Path("src/etf/verdict.py").read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
        elif isinstance(node, ast.Import):
            modules |= {a.name for a in node.names}
    assert not (modules & {"etf.http", "etf.seal", "etf.recorder", "urllib", "urllib.request"})


def test_no_stage_a_module_imports_the_verdict_machinery() -> None:
    """It is built dark. Nothing in the collection path may call it."""
    src = pathlib.Path("src/etf")
    importers = [
        p.name
        for p in src.rglob("*.py")
        if p.name != "verdict.py" and "etf.verdict" in p.read_text(encoding="utf-8")
    ]
    assert not importers, f"verdict.py is imported by {importers}"


# --- known answers -------------------------------------------------------


def test_the_canary_fires_on_a_planted_signal() -> None:
    """A verdict engine that cannot detect a planted effect proves nothing about a null."""
    days = planted_days(200)
    e1 = run_e1(days, draws=2000)
    assert e1.rho > 0.7
    assert e1.p_value <= CONFIG.alpha_adj
    assert e1.passes
    e2 = run_e2(days, draws=2000)
    assert e2.mean_net > 0
    assert e2.passes


def test_neither_primary_fires_on_pure_noise() -> None:
    days = noise_days(200)
    assert not run_e1(days, draws=2000).passes
    assert not run_e2(days, draws=2000).passes


def test_a_planted_negative_relationship_does_not_fire_a_one_sided_positive_test() -> None:
    days = [
        Day(
            trade_date=d.trade_date,
            signal_usd=d.signal_usd,
            forward_return=-d.forward_return,
            funding_sum=0.0,
            revised=False,
        )
        for d in planted_days(200)
    ]
    assert not run_e1(days, draws=2000).passes


def test_the_net_return_pays_funding_from_the_long_and_to_the_short() -> None:
    """Section 5's sign convention, stated and pinned."""
    day = Day(
        trade_date=date(2025, 5, 1),
        signal_usd=200e6,
        forward_return=0.01,
        funding_sum=0.001,
        revised=False,
    )
    long = net_return(day, Position.LONG, 0.0)
    short = net_return(day, Position.SHORT, 0.0)
    assert long == pytest.approx(0.01 - 0.001)
    assert short == pytest.approx(-0.01 + 0.001)
    assert net_return(day, Position.FLAT, 9.0) == 0.0


def test_the_cost_is_charged_once_per_trade_and_only_on_a_trade() -> None:
    day = Day(
        trade_date=date(2025, 5, 1),
        signal_usd=200e6,
        forward_return=0.0,
        funding_sum=0.0,
        revised=False,
    )
    assert net_return(day, Position.LONG, 9.0) == pytest.approx(-0.0009)
    assert net_return(day, Position.FLAT, 9.0) == 0.0


def test_e1_on_fewer_than_three_days_is_an_absence() -> None:
    with pytest.raises(ValueError, match="an absence, not a result"):
        run_e1(planted_days(2), draws=10)


def test_e2_with_no_trades_is_an_absence_not_a_mean_of_zero() -> None:
    flat = [
        Day(
            trade_date=date(2025, 5, 1) + timedelta(days=i),
            signal_usd=0.0,
            forward_return=0.01,
            funding_sum=0.0,
            revised=False,
        )
        for i in range(20)
    ]
    with pytest.raises(ValueError, match="an absence, not a mean of zero"):
        run_e2(flat, draws=10)


def test_a_higher_cost_band_never_improves_the_mean_net() -> None:
    days = planted_days(150)
    low = run_e2(days, cost_bp=3.0, draws=500).mean_net
    central = run_e2(days, cost_bp=9.0, draws=500).mean_net
    high = run_e2(days, cost_bp=18.0, draws=500).mean_net
    assert low > central > high


def test_the_p_value_is_never_zero_because_the_observed_draw_counts() -> None:
    result = run_e1(planted_days(120), draws=200)
    assert result.p_value >= 1 / 201


# --- the named secondaries, and nothing else -----------------------------


def test_the_secondaries_carry_the_registered_grid_with_a_sidak_correction() -> None:
    sec = run_secondaries(planted_days(200), draws=300)
    assert set(sec.threshold_grid) <= set(CONFIG.threshold_grid_usd)
    expected = 1.0 - (1.0 - CONFIG.alpha_adj) ** (1.0 / len(CONFIG.threshold_grid_usd))
    assert sec.sidak_alpha == pytest.approx(expected)
    assert sec.sidak_alpha < CONFIG.alpha_adj


def test_the_secondaries_split_the_sample_into_halves_and_carry_both_n() -> None:
    sec = run_secondaries(planted_days(200), draws=300)
    assert set(sec.halves) == {"first_half", "second_half"}
    assert sec.halves["first_half"]["n"] + sec.halves["second_half"]["n"] == 200


def test_the_revised_and_unrevised_subsets_are_reported_separately_with_their_n() -> None:
    sec = run_secondaries(planted_days(200), draws=300)
    assert sec.revised_n > 0
    assert sec.unrevised_n > 0
    assert sec.revised_n + sec.unrevised_n <= 200


def test_the_same_day_coefficient_is_computed_only_where_it_was_supplied() -> None:
    days = [
        Day(
            trade_date=d.trade_date,
            signal_usd=d.signal_usd,
            forward_return=d.forward_return,
            funding_sum=0.0,
            revised=False,
        )
        for d in planted_days(50)
    ]
    sec = run_secondaries(days, draws=100)
    assert sec.same_day_n == 0
    assert sec.same_day_rho is None


def test_the_reversal_profile_covers_the_registered_horizons_and_no_others() -> None:
    positions = [Position.LONG] * 10
    profile = reversal_profile({h: [0.01 * h] * 10 for h in range(1, 40)}, positions)
    assert max(profile) == CONFIG.reversal_horizon_max_days
    assert min(profile) == 1


def test_the_cost_band_reports_all_three_registered_costs() -> None:
    sec = run_secondaries(planted_days(150), draws=300)
    assert set(sec.cost_band) == set(CONFIG.hyperliquid_round_trip_bp)
