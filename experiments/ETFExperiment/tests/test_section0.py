"""Section 0, with every boundary fixture sitting exactly on the registered boundary."""

from __future__ import annotations

import pytest

from etf.config import CONFIG
from etf.observability import Observability
from etf.section0 import (
    BLOCKED_SCOPE,
    DEGRADED_SCOPE,
    GO_SCOPE,
    CoPrimaryPowers,
    Section0Verdict,
    fire_section0,
)

GO_FLOOR = CONFIG.power_go_floor
BLOCKED_FLOOR = CONFIG.power_blocked_floor


def fire(
    *,
    e1_reg: float = 0.9,
    e2_reg: float = 0.9,
    e1_pub: float = 0.99,
    e2_pub: float = 0.99,
    observability: Observability = Observability.PASS,
    unstable: float = 0.0,
):  # type: ignore[no-untyped-def]
    return fire_section0(
        powers_registered=CoPrimaryPowers(e1=e1_reg, e2=e2_reg),
        powers_published=CoPrimaryPowers(e1=e1_pub, e2=e2_pub),
        observability=observability,
        unstable_asprinted_share=unstable,
    )


def test_go_requires_both_co_primaries_and_a_full_observability_pass() -> None:
    gate = fire(e1_reg=GO_FLOOR, e2_reg=GO_FLOOR)
    assert gate.verdict is Section0Verdict.GO
    assert gate.collectors_armed
    assert gate.verdict_scope == GO_SCOPE


def test_one_co_primary_one_notch_under_the_go_floor_is_not_a_go() -> None:
    """The fixture sits exactly on the boundary; E2 alone is a hair below it."""
    gate = fire(e1_reg=GO_FLOOR, e2_reg=GO_FLOOR - 1e-12)
    assert gate.verdict is Section0Verdict.DEGRADED
    assert gate.verdict_scope == DEGRADED_SCOPE


def test_the_registered_expectation_shape_fires_degraded() -> None:
    """E1 clears 0.80 at the published magnitude but not at the registered half.

    This is the outcome the registration states in advance that it expects.
    """
    gate = fire(e1_reg=0.31, e2_reg=0.22, e1_pub=0.86, e2_pub=0.71)
    assert gate.verdict is Section0Verdict.DEGRADED
    assert gate.collectors_armed
    assert "not present at its published magnitude" in gate.verdict_scope
    assert "cannot distinguish a decayed effect from no effect" in gate.verdict_scope


def test_a_partial_observability_fires_degraded_even_at_full_power() -> None:
    gate = fire(observability=Observability.PARTIAL)
    assert gate.verdict is Section0Verdict.DEGRADED
    assert "demoting the retro cohort to descriptive" in gate.rationale


def test_an_observability_fail_fires_blocked_and_arms_nothing() -> None:
    gate = fire(observability=Observability.FAIL)
    assert gate.verdict is Section0Verdict.BLOCKED
    assert not gate.collectors_armed
    assert gate.verdict_scope == BLOCKED_SCOPE


def test_e1_exactly_on_the_blocked_floor_at_published_magnitude_is_not_blocked() -> None:
    """Strictly under 0.50 blocks; 0.50 itself does not. Fixture on the boundary."""
    assert fire(e1_reg=0.2, e1_pub=BLOCKED_FLOOR).verdict is Section0Verdict.DEGRADED
    assert fire(e1_reg=0.2, e1_pub=BLOCKED_FLOOR - 1e-12).verdict is Section0Verdict.BLOCKED


def test_the_residual_band_is_registered_as_degraded_not_left_as_a_gap() -> None:
    """E1 published power between the two floors: collection proceeds, narrowed."""
    gate = fire(e1_reg=0.20, e2_reg=0.15, e1_pub=0.62, e2_pub=0.40)
    assert gate.verdict is Section0Verdict.DEGRADED
    assert "residual band" in gate.rationale


def test_an_unstable_majority_fires_blocked_and_the_fixture_sits_on_one_half() -> None:
    """Strictly more than half blocks; exactly half does not."""
    assert fire(unstable=0.5).verdict is not Section0Verdict.BLOCKED
    blocked = fire(unstable=0.5 + 1e-12)
    assert blocked.verdict is Section0Verdict.BLOCKED
    assert "no stable as-printed value" in blocked.rationale


def test_blocked_triggers_are_checked_before_go_even_at_perfect_power() -> None:
    assert fire(unstable=0.9, e1_reg=1.0, e2_reg=1.0).verdict is Section0Verdict.BLOCKED
    assert fire(observability=Observability.FAIL, e1_reg=1.0).verdict is Section0Verdict.BLOCKED


@pytest.mark.parametrize("bad", [-0.01, 1.01, float("nan")])
def test_a_power_outside_zero_one_is_refused_rather_than_clamped(bad: float) -> None:
    with pytest.raises(ValueError, match="probability in"):
        fire(e1_reg=bad)


@pytest.mark.parametrize("bad", [-0.01, 1.01, float("nan")])
def test_an_unstable_share_outside_zero_one_is_refused(bad: float) -> None:
    with pytest.raises(ValueError, match="share in"):
        fire(unstable=bad)


def test_every_verdict_carries_its_scope_in_plain_words() -> None:
    for gate in (
        fire(),
        fire(e1_reg=0.1, e1_pub=0.9),
        fire(observability=Observability.FAIL),
    ):
        assert gate.verdict_scope
        assert gate.rationale.endswith(".")
