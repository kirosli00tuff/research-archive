"""The empty operator prior slot blocks Stage B structurally."""

from __future__ import annotations

from pathlib import Path

import pytest

from etf.paths import REGISTRATION_MD
from etf.registration_check import (
    SLOT_LABEL,
    OperatorPriorMalformed,
    OperatorPriorMissing,
    assistant_prior,
    operator_prior_is_filled,
    read_operator_prior,
    require_operator_prior,
)


def test_the_live_registration_slot_is_empty_and_blocks_stage_b() -> None:
    assert not operator_prior_is_filled()
    with pytest.raises(OperatorPriorMissing, match="blocked"):
        require_operator_prior()


def test_the_refusal_names_the_assistant_prior_as_not_the_operator_number() -> None:
    with pytest.raises(OperatorPriorMissing) as exc:
        require_operator_prior()
    assert "may not be copied into the slot" in str(exc.value)
    assert str(assistant_prior()) in str(exc.value)


def test_the_assistant_prior_is_the_registered_zero_point_one_zero() -> None:
    assert assistant_prior() == 0.10


def test_a_filled_and_labelled_slot_parses(tmp_path: Path) -> None:
    path = tmp_path / "REGISTRATION.md"
    path.write_text(f"> **{SLOT_LABEL}** 0.35 (independent)\n", encoding="utf-8")
    prior = read_operator_prior(path)
    assert prior.value == 0.35
    assert prior.label == "independent"


def test_an_adopted_label_parses_and_is_recorded_as_adopted(tmp_path: Path) -> None:
    path = tmp_path / "REGISTRATION.md"
    path.write_text(f"{SLOT_LABEL} 0.4 (adopted)\n", encoding="utf-8")
    assert read_operator_prior(path).label == "adopted"


def test_a_number_without_a_label_does_not_parse(tmp_path: Path) -> None:
    """Nothing else parses. An unlabelled number is not a fill."""
    path = tmp_path / "REGISTRATION.md"
    path.write_text(f"{SLOT_LABEL} 0.4\n", encoding="utf-8")
    with pytest.raises(OperatorPriorMissing):
        read_operator_prior(path)


def test_a_removed_slot_label_is_malformed_not_merely_missing(tmp_path: Path) -> None:
    path = tmp_path / "REGISTRATION.md"
    path.write_text("no slot here\n", encoding="utf-8")
    with pytest.raises(OperatorPriorMalformed, match="not removable"):
        read_operator_prior(path)


def test_the_registration_file_the_check_reads_is_the_repo_registration() -> None:
    assert REGISTRATION_MD.name == "REGISTRATION.md"
    assert SLOT_LABEL in REGISTRATION_MD.read_text(encoding="utf-8")
