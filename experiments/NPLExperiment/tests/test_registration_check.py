"""The operator prior gate. The refusal is produced, never asserted."""

from __future__ import annotations

from pathlib import Path

import pytest

from npl.registration_check import (
    OperatorPriorMissing,
    assistant_priors,
    operator_prior,
    operator_prior_filled,
    require_operator_prior,
)


def test_the_real_registration_slot_is_filled_0_40_adopted() -> None:
    """The operator instructed the fill on 2026-08-27; the pin now holds the filled state."""
    found = operator_prior()
    assert found is not None, "the slot was filled by operator instruction on 2026-08-27"
    assert found[0] == pytest.approx(0.40)
    assert found[1] == "adopted"
    assert operator_prior_filled()
    assert require_operator_prior() == found


def test_an_empty_slot_still_produces_the_structural_refusal(tmp_path: Path) -> None:
    empty = tmp_path / "REGISTRATION.md"
    empty.write_text(
        "> Operator prior on the Stage B bars clearing: _reserved — empty. The\n"
        "> operator fills this line by replacing everything after the colon with a\n"
        "> probability and a label._\n",
        encoding="utf-8",
    )
    assert operator_prior(empty) is None
    assert not operator_prior_filled(empty)
    with pytest.raises(OperatorPriorMissing, match="structurally blocked"):
        require_operator_prior(empty)


def test_a_section_that_claims_a_prior_without_recording_one_is_blank(tmp_path: Path) -> None:
    hollow = tmp_path / "REGISTRATION.md"
    hollow.write_text("## Section 13\n\nThe operator recorded a prior.\n", encoding="utf-8")
    assert not operator_prior_filled(hollow)


def test_a_prior_without_a_label_does_not_count(tmp_path: Path) -> None:
    unlabelled = tmp_path / "REGISTRATION.md"
    unlabelled.write_text("> Operator prior: 0.25\n", encoding="utf-8")
    assert not operator_prior_filled(unlabelled)


def test_a_recorded_labelled_prior_unblocks(tmp_path: Path) -> None:
    filled = tmp_path / "REGISTRATION.md"
    filled.write_text(
        "> Operator prior on the Stage B bars clearing: 0.35 (independent)\n", encoding="utf-8"
    )
    found = operator_prior(filled)
    assert found is not None
    value, label = found
    assert value == pytest.approx(0.35)
    assert label == "independent"
    assert require_operator_prior(filled) == found


def test_an_adopted_label_is_parsed_and_preserved(tmp_path: Path) -> None:
    filled = tmp_path / "REGISTRATION.md"
    filled.write_text("> Operator prior: 0.40 (adopted)\n", encoding="utf-8")
    found = operator_prior(filled)
    assert found is not None
    assert found[0] == pytest.approx(0.40)
    assert found[1] == "adopted"


def test_the_assistant_priors_are_the_recorded_pair() -> None:
    assert assistant_priors() == (0.20, 0.40)
