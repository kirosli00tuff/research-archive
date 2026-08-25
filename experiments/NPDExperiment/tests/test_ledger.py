"""The ledgers only grow, they survive restart, and the cap is checked before."""

from __future__ import annotations

from pathlib import Path

import pytest

from npd.callstate import CallState
from npd.config import CONFIG
from npd.ledger.append_only import AppendOnlyLedger, LedgerCorruption
from npd.ledger.evidence import EvidenceLedger
from npd.ledger.spend import SpendLedger, SpendRefused, cost_of


def test_rows_survive_a_new_process(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    AppendOnlyLedger(path).append({"a": 1})
    AppendOnlyLedger(path).append({"a": 2})
    assert [r["a"] for r in AppendOnlyLedger(path).iter_rows()] == [1, 2]


def test_a_truncated_final_line_is_reported_not_repaired(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    led = AppendOnlyLedger(path)
    led.append({"a": 1})
    with path.open("a", encoding="utf-8") as fh:
        fh.write('{"a": 2')
    result = led.read()
    assert [r["a"] for r in result.rows] == [1]
    assert result.trailing_partial_line == '{"a": 2'


def test_a_corrupt_line_raises(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    path.write_text("not json\n", encoding="utf-8")
    with pytest.raises(LedgerCorruption):
        AppendOnlyLedger(path).read()


def test_cost_uses_the_registered_rates() -> None:
    assert cost_of(1_000_000, 0, 0) == pytest.approx(CONFIG.price_input_per_mtok_usd)
    assert cost_of(0, 0, 1_000_000) == pytest.approx(CONFIG.price_output_per_mtok_usd)
    assert cost_of(1_000_000, 1_000_000, 0) == pytest.approx(CONFIG.price_cached_input_per_mtok_usd)


def test_the_cap_is_checked_before_the_batch_not_after(tmp_path: Path) -> None:
    ledger = SpendLedger(path=tmp_path / "s.jsonl")
    ledger.refuse_if_projection_crosses_cap(calls_in_batch=50, projected_cost_per_call=0.01)
    with pytest.raises(SpendRefused, match="Refused before sending"):
        ledger.refuse_if_projection_crosses_cap(calls_in_batch=50, projected_cost_per_call=1.0)
    assert ledger.total_usd() == 0.0


def test_measured_cost_replaces_the_estimate_once_calls_have_run(tmp_path: Path) -> None:
    ledger = SpendLedger(path=tmp_path / "s.jsonl")
    assert ledger.mean_cost_per_call("gate") is None
    ledger.record(
        date="2025-01-02", kind="gate", input_tokens=1000, cached_input_tokens=0, output_tokens=1000
    )
    assert ledger.mean_cost_per_call("gate") == pytest.approx(cost_of(1000, 0, 1000))


def test_calibration_calls_are_counted_apart_from_gate_calls(tmp_path: Path) -> None:
    ledger = SpendLedger(path=tmp_path / "s.jsonl")
    ledger.record(
        date="2025-01-02",
        kind="calibration",
        input_tokens=10,
        cached_input_tokens=0,
        output_tokens=10,
    )
    ledger.record(
        date="2025-01-03", kind="gate", input_tokens=10, cached_input_tokens=0, output_tokens=10
    )
    assert ledger.n_calls("calibration") == 1
    assert ledger.n_calls("gate") == 1
    assert ledger.n_calls() == 2


def test_the_evidence_ledger_keeps_the_last_state_per_date(tmp_path: Path) -> None:
    led = EvidenceLedger(path=tmp_path / "e.jsonl")
    led.record(date="2025-01-02", state=CallState.MODEL_FAILED, model="m", attempt=1)
    led.record(
        date="2025-01-02",
        state=CallState.STORED,
        model="m",
        attempt=2,
        raw_response='{"ranking": []}',
    )
    assert led.terminal_state_by_date() == {"2025-01-02": CallState.STORED}


def test_the_raw_response_is_kept_verbatim(tmp_path: Path) -> None:
    led = EvidenceLedger(path=tmp_path / "e.jsonl")
    raw = '{"ranking": ["AB", "CD"]}'
    led.record(date="2025-01-02", state=CallState.STORED, model="m", attempt=1, raw_response=raw)
    assert led.rows()[0]["raw_response"] == raw
