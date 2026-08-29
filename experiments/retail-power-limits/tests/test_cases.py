"""The extracted evidence is checked for the properties the note depends on."""

from __future__ import annotations

import pytest

from rplimits.cases import CONTRAST_CASES, HEADLINES, POWER_CASES, ContrastCase, Figure, PowerCase
from rplimits.sources import SOURCES

ALL_CASES: list[PowerCase | ContrastCase] = [*POWER_CASES, *CONTRAST_CASES]


def test_a_figure_cannot_cite_an_unknown_source() -> None:
    with pytest.raises(KeyError):
        Figure("a value", "no-such-source")


def test_a_figure_cannot_be_empty() -> None:
    with pytest.raises(ValueError, match="not a figure"):
        Figure("   ", "npd-registration")


@pytest.mark.parametrize("case", ALL_CASES, ids=lambda c: c.key)
def test_every_figure_resolves_to_a_source(case: PowerCase | ContrastCase) -> None:
    """The note is a secondary source; an unsourced figure has no business in it."""
    for figure in case.figures:
        assert figure.source in SOURCES, f"{case.key}: {figure.source!r} does not resolve"


def test_there_are_exactly_four_power_cases() -> None:
    """Four cases are four cases. A fifth would change the claim, not extend it."""
    assert len(POWER_CASES) == 4
    assert [case.repo for case in POWER_CASES] == [
        "NPDExperiment",
        "InsiderExperiment",
        "ETFExperiment",
        "HFExperiment",
    ]


@pytest.mark.parametrize("case", POWER_CASES, ids=lambda c: c.key)
def test_every_power_case_records_its_scope_or_correction(case: PowerCase) -> None:
    """Each of the four carries a caveat; three of them carry a correction."""
    assert len(case.caveat) > 80, f"{case.key}: caveat is too thin to be doing any work"


@pytest.mark.parametrize("case", CONTRAST_CASES, ids=lambda c: c.key)
def test_every_contrast_case_says_why_it_is_not_a_power_closure(case: ContrastCase) -> None:
    assert len(case.why_not_power) > 80, f"{case.key}: no stated reason it contrasts"


def test_headlines_and_power_cases_correspond_exactly() -> None:
    """No orphaned headline, and no case missing from the summary table."""
    assert [h.case for h in HEADLINES] == [case.repo for case in POWER_CASES]


def test_cases_are_immutable() -> None:
    """Frozen: a later session cannot edit a quoted figure in place."""
    with pytest.raises(AttributeError):
        POWER_CASES[0].caveat = "edited"  # type: ignore[misc]
