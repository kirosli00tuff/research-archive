"""The registration and the code must not drift apart."""

from __future__ import annotations

from pathlib import Path

from npd.config import CONFIG
from npd.registration_check import assert_agrees, check


def test_registration_agrees_with_the_frozen_config() -> None:
    assert_agrees()


def test_the_checker_notices_a_disagreement(tmp_path: Path) -> None:
    fake = tmp_path / "REGISTRATION.md"
    fake.write_text("this registration states nothing at all", encoding="utf-8")
    bad = check(fake, CONFIG)
    assert bad, "the checker passed a registration that states none of the values"
    assert any(d.field == "gate_model" for d in bad)


def test_the_gate_names_the_dated_snapshot_not_the_alias() -> None:
    assert CONFIG.gate_model == "gpt-5-2025-08-07"
    assert CONFIG.gate_model != "gpt-5"
    assert CONFIG.gate_model.count("-") >= 3, "the model id is not a dated snapshot"
