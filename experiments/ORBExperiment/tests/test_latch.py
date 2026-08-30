"""The Stage C and Stage D latches. A second read voids the hypothesis."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from orb.latch import (
    REGISTERED_PRIOR_LABELS,
    LatchAlreadySpentError,
    LatchPrerequisiteError,
    OperatorGateError,
    Stage,
    is_spent,
    latch_path,
    module_hashes,
    require_unspent,
    write_latch,
)

SRC = Path(__file__).resolve().parent.parent / "src" / "orb"


def _write(tmp_path: Path, stage: Stage, **kw: object) -> object:
    defaults: dict[str, object] = {
        "operator_prior_label": "independent",
        "operator_instruction": True,
    }
    defaults.update(kw)
    return write_latch(tmp_path, SRC, stage, **defaults)  # type: ignore[arg-type]


def test_the_latch_is_written_before_the_read_and_records_module_hashes(
    tmp_path: Path,
) -> None:
    record = _write(tmp_path, Stage.C)
    payload = json.loads(latch_path(tmp_path, Stage.C).read_text())
    assert payload["stage"] == "stage_c"
    assert payload["operator_prior_label"] == "independent"
    assert len(payload["module_hashes"]) >= 20
    assert payload["module_hashes"]["config.py"] == module_hashes(SRC)["config.py"]
    assert record is not None


def test_a_second_read_of_the_same_window_is_refused(tmp_path: Path) -> None:
    """**This voids the hypothesis.** The refusal says so."""
    _write(tmp_path, Stage.C)
    with pytest.raises(LatchAlreadySpentError, match="voids the hypothesis"):
        _write(tmp_path, Stage.C)


def test_require_unspent_refuses_at_the_top_of_a_read_path(tmp_path: Path) -> None:
    require_unspent(tmp_path, Stage.C)
    _write(tmp_path, Stage.C)
    with pytest.raises(LatchAlreadySpentError):
        require_unspent(tmp_path, Stage.C)


def test_stage_d_cannot_run_before_stage_c(tmp_path: Path) -> None:
    with pytest.raises(LatchPrerequisiteError, match="before stage_c"):
        _write(tmp_path, Stage.D)
    _write(tmp_path, Stage.C)
    _write(tmp_path, Stage.D)
    assert is_spent(tmp_path, Stage.D)


def test_an_empty_operator_prior_slot_blocks_the_latch_structurally(
    tmp_path: Path,
) -> None:
    """Section 13's empty slot is a gate, not a reminder."""
    with pytest.raises(OperatorGateError, match="reserves it for the operator"):
        _write(tmp_path, Stage.C, operator_prior_label="")
    with pytest.raises(OperatorGateError):
        _write(tmp_path, Stage.C, operator_prior_label="<EMPTY>")
    assert not latch_path(tmp_path, Stage.C).exists()


def test_the_prior_label_must_be_independent_or_adopted(tmp_path: Path) -> None:
    """The label is part of the datum. NPDExperiment Amendment 0."""
    with pytest.raises(OperatorGateError):
        _write(tmp_path, Stage.C, operator_prior_label="probably_independent")
    _write(tmp_path, Stage.C, operator_prior_label="adopted")
    assert is_spent(tmp_path, Stage.C)


def test_no_operator_instruction_blocks_the_latch(tmp_path: Path) -> None:
    with pytest.raises(OperatorGateError, match="explicit operator instruction"):
        _write(tmp_path, Stage.C, operator_instruction=False)
    assert not latch_path(tmp_path, Stage.C).exists()


def test_a_failed_latch_leaves_no_file_so_a_retry_is_not_a_second_read(
    tmp_path: Path,
) -> None:
    """A refused attempt must not consume the one read the window has."""
    for kwargs in (
        {"operator_instruction": False},
        {"operator_prior_label": ""},
    ):
        with pytest.raises(OperatorGateError):
            _write(tmp_path, Stage.C, **kwargs)
    assert not is_spent(tmp_path, Stage.C)
    _write(tmp_path, Stage.C)
    assert is_spent(tmp_path, Stage.C)


def test_the_two_stages_have_separate_latches(tmp_path: Path) -> None:
    _write(tmp_path, Stage.C)
    assert is_spent(tmp_path, Stage.C)
    assert not is_spent(tmp_path, Stage.D)
    assert latch_path(tmp_path, Stage.C) != latch_path(tmp_path, Stage.D)


def test_the_operator_label_is_accepted_as_the_operator_wrote_it(
    tmp_path: Path,
) -> None:
    """Amendment 5 recorded the label as ``INDEPENDENT``, in capitals.

    A latch that refused a correct answer over letter case would fail exactly
    once, at the most expensive moment, and would look identical to the refusal
    that exists to stop an unlabelled slot.
    """
    # Arrange
    state, source = tmp_path / "state", tmp_path / "src"
    source.mkdir()
    (source / "m.py").write_text("x = 1\n", encoding="utf-8")
    # Act
    record = write_latch(
        state,
        source,
        Stage.C,
        operator_prior_label="  INDEPENDENT  ",
        operator_instruction=True,
    )
    # Assert — stored in the registered lower-case form.
    assert record.operator_prior_label == "independent"


def test_an_unregistered_label_is_still_refused_after_case_folding(
    tmp_path: Path,
) -> None:
    """Case folding is the only normalisation. A wrong label still refuses."""
    # Arrange
    state, source = tmp_path / "state", tmp_path / "src"
    source.mkdir()
    (source / "m.py").write_text("x = 1\n", encoding="utf-8")
    # Act / Assert
    for label in ("INDEPENDENT-ISH", "assumed", "", "   "):
        with pytest.raises(OperatorGateError, match="empty or unlabelled"):
            write_latch(
                state,
                source,
                Stage.C,
                operator_prior_label=label,
                operator_instruction=True,
            )


def test_the_registered_label_set_is_exactly_the_two_section_13_labels() -> None:
    assert sorted(REGISTERED_PRIOR_LABELS) == ["adopted", "independent"]
