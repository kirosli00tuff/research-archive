"""Structural guards. Each one fails a specific mutation of real source.

These are not style checks. Each guard exists because the predecessor system
failed in exactly the way the guard forbids.
"""

from __future__ import annotations

import ast
import re
from dataclasses import fields
from pathlib import Path

import pytest

from npd.callstate import (
    ALL_STATES,
    OPERATIONAL_HEALTH_STATES,
    SAMPLE_COMPOSITION_STATES,
    CallState,
)
from npd.config import CONFIG

SRC = Path(__file__).resolve().parents[1] / "src" / "npd"
CONFIG_FILE = SRC / "config.py"

# Files permitted to name the sealed store at all.
SEAL_MENTION_ALLOWED = {
    SRC / "paths.py",  # defines the path
    SRC / "data" / "forward_returns.py",  # writes, never reads
    SRC / "eval" / "evaluator.py",  # the one reader
}
# The single module permitted to read it.
SEAL_READER = SRC / "eval" / "evaluator.py"

SEAL_TOKENS = ("SEALED_DB", "npd_sealed")
READ_PATTERN = re.compile(r"select\s+.*\bfrom\s+forward_return\b", re.IGNORECASE | re.DOTALL)


def source_files() -> list[Path]:
    return sorted(p for p in SRC.rglob("*.py"))


# --------------------------------------------------------------------------
# Guard 1. Every config field has an enforcement site.
# Six config keys in the predecessor were enforced nowhere.
# --------------------------------------------------------------------------


def test_every_config_field_has_an_enforcement_site() -> None:
    names = [f.name for f in fields(CONFIG)]
    assert names, "the config declares no fields"

    bodies = {p: p.read_text(encoding="utf-8") for p in source_files() if p != CONFIG_FILE}
    unenforced = []
    for name in names:
        pattern = re.compile(rf"\b{re.escape(name)}\b")
        sites = [p.name for p, text in bodies.items() if pattern.search(text)]
        if not sites:
            unenforced.append(name)
    assert not unenforced, (
        "config fields with no enforcement site anywhere under src/npd: "
        f"{unenforced}. A key enforced nowhere is decoration."
    )


# --------------------------------------------------------------------------
# Guard 2. The sealed forward returns have exactly one reader.
# --------------------------------------------------------------------------


def test_only_the_evaluator_mentions_the_sealed_store() -> None:
    offenders = []
    for path in source_files():
        if path in SEAL_MENTION_ALLOWED:
            continue
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in SEAL_TOKENS):
            offenders.append(str(path.relative_to(SRC)))
    assert not offenders, f"modules naming the sealed store outside the permitted set: {offenders}"


def test_the_forward_return_table_is_read_only_through_a_guarded_path() -> None:
    """Both stores hold a forward_return table, so the guard is on the PATH.

    var/npd_fit.db holds dates strictly before the window start and the logistic
    baseline reads it. var/npd_sealed.db holds the window outcomes and only the
    evaluator may name it. A module that reads forward returns without naming a
    permitted path is the thing this catches.
    """
    offenders = []
    for path in source_files():
        if path in SEAL_MENTION_ALLOWED or path == SRC / "baselines" / "logistic.py":
            continue
        text = path.read_text(encoding="utf-8")
        if READ_PATTERN.search(text):
            offenders.append(str(path.relative_to(SRC)))
    assert not offenders, (
        f"modules reading a forward_return table outside the permitted set: {offenders}. "
        "Collection is not evaluation."
    )


def test_the_logistic_baseline_refuses_a_window_date() -> None:
    """The one baseline that reads an outcome cannot reach a window outcome."""
    from npd.baselines.logistic import load_fit_targets

    with pytest.raises(PermissionError):
        load_fit_targets(["2022-03-01", "2025-06-02"], 5)


def test_read_sealed_returns_has_one_definition_and_no_outside_callers() -> None:
    definitions = []
    callers = []
    for path in source_files():
        text = path.read_text(encoding="utf-8")
        if "def read_sealed_returns" in text:
            definitions.append(path)
        if path != SEAL_READER and "read_sealed_returns(" in text:
            callers.append(str(path.relative_to(SRC)))
    assert definitions == [SEAL_READER], f"unexpected definitions: {definitions}"
    assert not callers, f"modules calling the sealed reader: {callers}"


# --------------------------------------------------------------------------
# Guard 3. The five call states are never merged.
# --------------------------------------------------------------------------


def test_five_distinct_call_states() -> None:
    assert len(ALL_STATES) == 5, f"expected five states, found {len(ALL_STATES)}"
    values = [s.value for s in ALL_STATES]
    assert len(set(values)) == 5, f"two states share a value: {values}"
    assert set(values) == {
        "stored",
        "no_data",
        "model_failed",
        "excluded_pre_cutoff",
        "source_failed",
    }


def test_model_failed_is_operational_health_not_sample_composition() -> None:
    assert CallState.MODEL_FAILED in OPERATIONAL_HEALTH_STATES
    assert CallState.MODEL_FAILED not in SAMPLE_COMPOSITION_STATES
    assert CallState.EXCLUDED_PRE_CUTOFF in SAMPLE_COMPOSITION_STATES
    assert CallState.EXCLUDED_PRE_CUTOFF not in OPERATIONAL_HEALTH_STATES
    assert not (OPERATIONAL_HEALTH_STATES & SAMPLE_COMPOSITION_STATES)


def test_model_failed_and_source_failed_stay_separate() -> None:
    # mypy calls these comparisons statically decidable. They are kept because
    # the mutation exercise edits the source, and a merged pair must fail here
    # at runtime rather than pass because a type checker was satisfied.
    assert CallState.MODEL_FAILED is not CallState.SOURCE_FAILED  # type: ignore[comparison-overlap]
    assert CallState.MODEL_FAILED.value != CallState.SOURCE_FAILED.value  # type: ignore[comparison-overlap]


# --------------------------------------------------------------------------
# Guard 4. No confidence field exists in version one.
# --------------------------------------------------------------------------


def test_no_confidence_field_anywhere_in_the_pipeline() -> None:
    offenders = []
    for path in source_files():
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        for node in ast.walk(tree):
            is_prose = isinstance(node, ast.Constant) and isinstance(node.value, str)
            if is_prose and re.search(r"\bconfidence\b", node.value, re.IGNORECASE):  # type: ignore[attr-defined]
                # Prose in a docstring that explains the clause is allowed.
                lowered = node.value.lower()  # type: ignore[attr-defined]
                if "council" not in lowered and "decoration" not in lowered:
                    offenders.append(f"{path.name}: {node.value[:60]}")  # type: ignore[attr-defined]
            if isinstance(node, ast.Name) and "confidence" in node.id.lower():
                offenders.append(f"{path.name}: name {node.id}")
    assert not offenders, f"a confidence field reappeared: {offenders}"


# --------------------------------------------------------------------------
# Guard 5. The evaluator refuses to run while Amendment 0 is empty.
# --------------------------------------------------------------------------


def test_amendment_zero_is_empty_and_blocks_b2() -> None:
    from npd.eval.evaluator import (
        AmendmentZeroMissing,
        amendment_zero_filled,
        require_amendment_zero,
    )

    assert not amendment_zero_filled(), (
        "Amendment 0 reads as filled. If the operator has written his prior, "
        "update this test deliberately rather than by accident."
    )
    with pytest.raises(AmendmentZeroMissing):
        require_amendment_zero()
