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


def test_the_real_registration_slot_is_still_empty_and_blocks_stage_b() -> None:
    assert operator_prior() is None, "the operator prior must be written by the operator"
    assert not operator_prior_filled()
    with pytest.raises(OperatorPriorMissing, match="structurally blocked"):
        require_operator_prior()


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
