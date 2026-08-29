"""A.1 Task 4's verdict, with fixtures ON the 0.60 and 0.90 bars."""

from __future__ import annotations

import pytest

from etf.config import CONFIG
from etf.observability import Observability, fire_observability

DENSITY_BAR = CONFIG.archive_density_pass_share
INTACT_BAR = CONFIG.revision_intact_pass_share


def test_the_registered_bars_are_sixty_and_ninety_percent() -> None:
    assert DENSITY_BAR == 0.60
    assert INTACT_BAR == 0.90


def test_both_legs_exactly_on_their_bars_pass() -> None:
    verdict = fire_observability(
        archive_admissible_days=60,
        archive_trading_days=100,
        revision_intact_days=90,
        revision_days=100,
    )
    assert verdict.verdict is Observability.PASS
    assert not verdict.retro_cohort_is_descriptive_only()
    assert "n = 100" in verdict.rationale


def test_one_day_under_the_density_bar_is_partial_and_demotes_the_retro_cohort() -> None:
    verdict = fire_observability(
        archive_admissible_days=59,
        archive_trading_days=100,
        revision_intact_days=95,
        revision_days=100,
    )
    assert verdict.verdict is Observability.PARTIAL
    assert verdict.retro_cohort_is_descriptive_only()
    assert "archive capture density" in verdict.rationale
    assert "forward cohort carries the verdict alone" in verdict.rationale


def test_one_day_under_the_revision_bar_is_partial_and_names_the_failing_leg() -> None:
    verdict = fire_observability(
        archive_admissible_days=80,
        archive_trading_days=100,
        revision_intact_days=89,
        revision_days=100,
    )
    assert verdict.verdict is Observability.PARTIAL
    assert "forward revision integrity" in verdict.rationale


def test_both_legs_under_their_bars_fail() -> None:
    verdict = fire_observability(
        archive_admissible_days=59,
        archive_trading_days=100,
        revision_intact_days=89,
        revision_days=100,
    )
    assert verdict.verdict is Observability.FAIL
    assert "No admissible as-printed cohort exists" in verdict.rationale


def test_a_share_over_zero_days_is_an_absence_not_a_number() -> None:
    with pytest.raises(ValueError, match="absence, not a number"):
        fire_observability(
            archive_admissible_days=0,
            archive_trading_days=0,
            revision_intact_days=1,
            revision_days=1,
        )
