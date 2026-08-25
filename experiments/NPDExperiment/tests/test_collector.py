"""The collector resumes, retries by taxonomy, and refuses before it spends."""

from __future__ import annotations

import dataclasses
import json
import sqlite3
from pathlib import Path

import pytest

from npd.callstate import CallState
from npd.collect.adapter import UnparseableResponse, parse_ranking
from npd.collect.collector import collect, load_day, reconcile
from npd.collect.mock import MockAdapter
from npd.collect.prompt import build as build_prompt
from npd.config import CONFIG
from npd.data.anonymize import build as build_mapping
from npd.data.anonymize import new_nonce
from npd.data.store import SCHEMA, open_store
from npd.ledger.evidence import EvidenceLedger
from npd.ledger.spend import SpendLedger

DATES = ["2025-03-03", "2025-03-04", "2025-03-05"]
SYMBOLS = [f"S{i:02d}" for i in range(CONFIG.panel_size)]


def _store(tmp_path: Path, dates: list[str] = DATES) -> Path:
    path = tmp_path / "s.db"
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    for i, d in enumerate(dates):
        con.execute("INSERT OR REPLACE INTO session(date, idx) VALUES(?,?)", (d, i))
        nonce = new_nonce()
        anon = build_mapping(list(SYMBOLS), nonce)
        con.executemany(
            "INSERT INTO anonymization(date, label, symbol, nonce) VALUES(?,?,?,?)",
            [(d, lab, sym, nonce) for lab, sym in anon.label_to_symbol.items()],
        )
        con.executemany(
            "INSERT INTO feature(date, symbol, name, raw, z, absent_reason) VALUES(?,?,?,?,?,NULL)",
            [
                (d, sym, name, 0.1 * j, (j - 15) / 10.0)
                for j, sym in enumerate(SYMBOLS)
                for name in CONFIG.feature_names
            ],
        )
    con.commit()
    con.close()
    return path


def _ledgers(tmp_path: Path) -> tuple[SpendLedger, EvidenceLedger]:
    return SpendLedger(path=tmp_path / "spend.jsonl"), EvidenceLedger(path=tmp_path / "ev.jsonl")


def _no_sleep(_s: float) -> None:
    return None


# --- parsing ---------------------------------------------------------------


def test_parse_accepts_a_clean_ranking() -> None:
    labels = ("AB", "CD", "EF")
    raw = json.dumps({"ranking": ["CD", "AB", "EF"]})
    assert parse_ranking(raw, labels) == ("CD", "AB", "EF")


def test_parse_accepts_a_fenced_block() -> None:
    labels = ("AB", "CD")
    raw = '```json\n{"ranking": ["AB", "CD"]}\n```'
    assert parse_ranking(raw, labels) == ("AB", "CD")


@pytest.mark.parametrize(
    "raw",
    [
        "not json at all",
        json.dumps({"order": ["AB", "CD"]}),
        json.dumps({"ranking": "AB,CD"}),
        json.dumps({"ranking": ["AB"]}),
        json.dumps({"ranking": ["AB", "AB"]}),
        json.dumps({"ranking": ["AB", "ZZ"]}),
    ],
)
def test_parse_refuses_anything_unusable(raw: str) -> None:
    with pytest.raises(UnparseableResponse):
        parse_ranking(raw, ("AB", "CD"))


def test_a_partial_ranking_is_not_patched() -> None:
    """A ranking missing a label is unusable, not a thing to complete."""
    with pytest.raises(UnparseableResponse, match="2 entries, expected 3"):
        parse_ranking(json.dumps({"ranking": ["AB", "CD"]}), ("AB", "CD", "EF"))
    with pytest.raises(UnparseableResponse, match="label mismatch"):
        parse_ranking(json.dumps({"ranking": ["AB", "CD", "ZZ"]}), ("AB", "CD", "EF"))


# --- day loading -----------------------------------------------------------


def test_load_day_serves_a_complete_panel(tmp_path: Path) -> None:
    path = _store(tmp_path)
    with open_store(path) as con:
        payload = load_day(con, DATES[0])
    assert payload is not None
    assert len(payload.labels) == CONFIG.panel_size
    assert set(payload.label_to_symbol.values()) == set(SYMBOLS)


def test_load_day_returns_none_when_the_panel_is_short(tmp_path: Path) -> None:
    path = _store(tmp_path)
    con = sqlite3.connect(path)
    con.execute(
        "DELETE FROM anonymization WHERE date = ? AND rowid IN "
        "(SELECT rowid FROM anonymization WHERE date = ? LIMIT 1)",
        (DATES[0], DATES[0]),
    )
    con.commit()
    con.close()
    with open_store(path) as con:
        assert load_day(con, DATES[0]) is None


def test_the_prompt_built_from_a_day_carries_no_symbol(tmp_path: Path) -> None:
    path = _store(tmp_path)
    with open_store(path) as con:
        payload = load_day(con, DATES[0])
    assert payload is not None
    prompt = build_prompt(payload.labels, payload.z_by_label)
    for sym in payload.label_to_symbol.values():
        assert sym not in prompt.user


# --- resume ----------------------------------------------------------------


def test_a_second_run_calls_nothing(tmp_path: Path) -> None:
    path = _store(tmp_path)
    spend, evidence = _ledgers(tmp_path)
    first = MockAdapter()
    collect(
        DATES,
        first,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )
    assert len(first.calls) == len(DATES)

    second = MockAdapter(seed=5)
    result = collect(
        DATES,
        second,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )
    assert second.calls == []
    assert result.counts[CallState.STORED] == len(DATES)


def test_a_lost_commit_is_rebuilt_from_the_ledger_not_recalled(tmp_path: Path) -> None:
    path = _store(tmp_path)
    spend, evidence = _ledgers(tmp_path)
    collect(
        DATES,
        MockAdapter(),
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )

    con = sqlite3.connect(path)
    con.execute("DELETE FROM model_ranking WHERE date = ?", (DATES[1],))
    con.commit()
    con.close()

    with open_store(path) as con:
        repaired = reconcile(con, evidence, DATES)
        assert repaired == 1
        n = con.execute(
            "SELECT COUNT(*) FROM model_ranking WHERE date = ?", (DATES[1],)
        ).fetchone()[0]
    assert n == CONFIG.panel_size
    spent_before = spend.total_usd()

    again = MockAdapter(seed=9)
    collect(
        DATES,
        again,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )
    assert again.calls == []
    assert spend.total_usd() == spent_before


def test_a_source_fault_sends_no_call_and_keeps_its_own_state(tmp_path: Path) -> None:
    path = _store(tmp_path)
    con = sqlite3.connect(path)
    con.execute("DELETE FROM anonymization WHERE date = ?", (DATES[1],))
    con.commit()
    con.close()

    spend, evidence = _ledgers(tmp_path)
    adapter = MockAdapter()
    result = collect(
        DATES,
        adapter,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )
    assert result.counts[CallState.SOURCE_FAILED] == 1
    assert result.counts.get(CallState.MODEL_FAILED, 0) == 0
    assert DATES[1] not in adapter.calls


def test_a_model_fault_exhausts_retries_then_lands_in_model_failed(tmp_path: Path) -> None:
    path = _store(tmp_path)
    spend, evidence = _ledgers(tmp_path)
    adapter = MockAdapter(fail_dates=frozenset({DATES[1]}))
    result = collect(
        DATES,
        adapter,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )
    assert result.counts[CallState.MODEL_FAILED] == 1
    assert result.counts.get(CallState.SOURCE_FAILED, 0) == 0
    attempts = [r for r in evidence.rows() if r["date"] == DATES[1]]
    assert len(attempts) == CONFIG.max_retries


def test_a_refused_batch_sends_nothing(tmp_path: Path) -> None:
    path = _store(tmp_path)
    tiny = dataclasses.replace(CONFIG, spend_cap_usd=0.0001)
    spend = SpendLedger(path=tmp_path / "spend.jsonl", cfg=tiny)
    evidence = EvidenceLedger(path=tmp_path / "ev.jsonl")
    adapter = MockAdapter()
    result = collect(
        DATES,
        adapter,
        cfg=tiny,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )
    assert adapter.calls == []
    assert result.stopped_early.startswith("spend_refused")
    assert spend.total_usd() == 0.0


# --- Amendment 3, the reasoning effort ladder ------------------------------


def test_the_ladder_starts_at_the_registered_effort_and_climbs_once() -> None:
    from npd.collect.collector import effort_for_attempt

    assert effort_for_attempt(1, CONFIG) == "minimal"
    assert effort_for_attempt(2, CONFIG) == "low"
    assert effort_for_attempt(3, CONFIG) == "low"
    assert effort_for_attempt(CONFIG.max_retries, CONFIG) == "low"


def test_the_ladder_is_identical_for_every_day() -> None:
    """The procedure is uniform even though the realized effort is not."""
    from npd.collect.collector import effort_for_attempt

    ladders = {
        tuple(effort_for_attempt(a, CONFIG) for a in range(1, CONFIG.max_retries + 1))
        for _ in range(5)
    }
    assert len(ladders) == 1


def test_a_config_without_a_ladder_falls_back_to_the_registered_effort() -> None:
    from npd.collect.collector import effort_for_attempt

    bare = dataclasses.replace(CONFIG, reasoning_effort_ladder=())
    assert effort_for_attempt(1, bare) == CONFIG.reasoning_effort
    assert effort_for_attempt(4, bare) == CONFIG.reasoning_effort


def test_the_evidence_ledger_records_the_effort_each_attempt_used(tmp_path: Path) -> None:
    path = _store(tmp_path)
    spend, evidence = _ledgers(tmp_path)
    adapter = MockAdapter(fail_dates=frozenset({DATES[1]}))
    collect(
        DATES,
        adapter,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )
    rows = [r for r in evidence.rows() if r["date"] == DATES[1]]
    efforts = [r["reasoning_effort"] for r in rows]
    assert efforts[0] == "minimal"
    assert set(efforts[1:]) == {"low"}


def test_retry_failed_reopens_days_that_failed_under_a_superseded_procedure(tmp_path: Path) -> None:
    path = _store(tmp_path)
    spend, evidence = _ledgers(tmp_path)
    doomed = frozenset({DATES[1]})
    collect(
        DATES,
        MockAdapter(fail_dates=doomed),
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )

    # Without the flag a failed day stays closed.
    quiet = MockAdapter(seed=3)
    collect(
        DATES,
        quiet,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )
    assert quiet.calls == []

    # With it, and only it, the day is attempted once more.
    reopened = MockAdapter(seed=4)
    result = collect(
        DATES,
        reopened,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
        retry_failed=True,
    )
    assert reopened.calls == [DATES[1]]
    assert result.counts[CallState.STORED] == len(DATES)


def test_a_day_stored_under_a_superseded_procedure_is_recollected(tmp_path: Path) -> None:
    """Amendment 3 changed the retry procedure, so its predecessors do not count.

    A row written before the ladder existed carries no reasoning_effort. The
    resume logic treats that day as not yet collected, so every day in the final
    sample came from one identical procedure. The superseded rows stay in the
    ledger, because a ledger is history.
    """
    path = _store(tmp_path)
    spend, evidence = _ledgers(tmp_path)

    # A row shaped like the pre-Amendment-3 ledger: stored, no effort recorded.
    evidence._ledger.append(
        {
            "ts": "2026-08-25T17:12:52+00:00",
            "date": DATES[0],
            "state": "stored",
            "model": CONFIG.gate_model,
            "attempt": 1,
            "input_tokens": 1753,
            "cached_input_tokens": 0,
            "output_tokens": 106,
            "reasoning_tokens": 0,
            "cost_usd": 0.003251,
            "latency_s": 2.3,
            "raw_response": "{}",
            "detail": "",
        }
    )
    adapter = MockAdapter()
    collect(
        DATES,
        adapter,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )
    assert DATES[0] in adapter.calls, "a superseded day was not recollected"

    # And a day stored under the current procedure is not called again.
    second = MockAdapter(seed=8)
    collect(
        DATES,
        second,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=path,
    )
    assert second.calls == []
