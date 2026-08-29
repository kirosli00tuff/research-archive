"""A manual run is refused while the scheduled unit is active."""

from __future__ import annotations

import pytest

from etf.guard import OVERRIDE_ENV, UnitActive, require_no_active_unit


def test_the_override_variable_is_the_registered_name() -> None:
    assert OVERRIDE_ENV == "ETF_ALLOW_MANUAL_RUN"


def test_an_inactive_unit_permits_a_manual_run() -> None:
    require_no_active_unit("etf-a-unit-that-does-not-exist.service", env={})


def test_an_active_unit_refuses_and_names_the_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("etf.guard.unit_is_active", lambda unit: True)
    with pytest.raises(UnitActive, match=OVERRIDE_ENV):
        require_no_active_unit("etf-snap.service", env={})


def test_the_override_permits_it_deliberately(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("etf.guard.unit_is_active", lambda unit: True)
    require_no_active_unit("etf-snap.service", env={OVERRIDE_ENV: "1"})


def test_any_value_other_than_one_does_not_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("etf.guard.unit_is_active", lambda unit: True)
    with pytest.raises(UnitActive):
        require_no_active_unit("etf-snap.service", env={OVERRIDE_ENV: "yes"})
