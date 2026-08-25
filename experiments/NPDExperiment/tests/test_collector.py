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
