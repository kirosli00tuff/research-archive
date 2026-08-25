"""The five B.0b mock scenarios. Every one must pass before B.1 sends a call.

Each scenario runs against its own scratch copy of the derived tables and its
own pair of ledgers, so nothing here touches the real store or the real spend
record. The mock adapter never reaches the network.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import shutil
import sqlite3
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from npd.callstate import ALL_STATES, CallState
from npd.collect import mock
from npd.collect.collector import collect
from npd.collect.prompt import template_digest
from npd.config import CONFIG
from npd.data.store import SCHEMA, forget_rows, open_store
from npd.ledger.evidence import EvidenceLedger
from npd.ledger.spend import SpendLedger
from npd.paths import REPORTS, STORE_DB
from npd.window import derive_window

COPIED_TABLES = ("session", "anonymization", "feature", "panel", "baseline_ranking")


def _no_sleep(_seconds: float) -> None:
    return None


def window_dates() -> list[str]:
    with open_store() as con:
        sess = [r[0] for r in con.execute("SELECT date FROM session ORDER BY idx")]
    w = derive_window([dt.date.fromisoformat(d) for d in sess])
    return [d.isoformat() for d in w.sessions]


def _scratch_store(root: Path, dates: list[str]) -> Path:
    """A scratch store holding only what the collector reads for these dates."""
    path = root / "scratch.db"
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    src = sqlite3.connect(f"file:{STORE_DB}?mode=ro", uri=True)
    placeholders = ",".join("?" * len(dates))
    try:
        for row in src.execute("SELECT date, idx FROM session"):
            con.execute("INSERT OR REPLACE INTO session(date, idx) VALUES(?,?)", row)
        for table in ("anonymization", "feature", "panel", "baseline_ranking"):
            cols = [r[1] for r in src.execute(f"PRAGMA table_info({table})")]
            rows = src.execute(
                f"SELECT {','.join(cols)} FROM {table} WHERE date IN ({placeholders})",
                tuple(dates),
            ).fetchall()
            con.executemany(
                f"INSERT OR REPLACE INTO {table}({','.join(cols)}) "
                f"VALUES({','.join('?' * len(cols))})",
                rows,
            )
        con.commit()
    finally:
        src.close()
        con.close()
    return path


def _counts(result: Any) -> dict[str, int]:
    return {st.value: result.counts.get(st, 0) for st in ALL_STATES}


def _run(name: str, body: Callable[[Path, list[str]], dict[str, Any]]) -> dict[str, Any]:
    dates = window_dates()
    root = Path(tempfile.mkdtemp(prefix=f"npd-b0b-{name}-"))
    try:
        out = body(root, dates)
        out["scenario"] = name
        return out
    finally:
        shutil.rmtree(root, ignore_errors=True)


def scenario_clean(root: Path, dates: list[str]) -> dict[str, Any]:
    """A clean full pass. Every eligible day stores a parseable ranking."""
    store = _scratch_store(root, dates)
    spend = SpendLedger(path=root / "spend.jsonl")
    evidence = EvidenceLedger(path=root / "evidence.jsonl")
    adapter = mock.MockAdapter()
    result = collect(
        dates,
        adapter,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=store,
    )
    servable = _servable(store, dates)
    passed = (
        result.counts.get(CallState.STORED, 0) == servable
        and result.counts.get(CallState.MODEL_FAILED, 0) == 0
        and len(adapter.calls) == servable
        and _ranked_days(store) == servable
    )
    return {
        "passed": passed,
        "counts": _counts(result),
        "calls_sent": len(adapter.calls),
        "servable_days": servable,
        "ranked_days": _ranked_days(store),
        "spend_usd": round(spend.total_usd(), 4),
    }


def scenario_kill_resume(root: Path, dates: list[str]) -> dict[str, Any]:
    """A mid-run kill, then a resume. No date is ever called twice."""
    store = _scratch_store(root, dates)
    spend = SpendLedger(path=root / "spend.jsonl")
    evidence = EvidenceLedger(path=root / "evidence.jsonl")

    kill_after = 137
    first = mock.MockAdapter(kill_after=kill_after)
    killed = False
    try:
        collect(
            dates,
            first,
            spend=spend,
            evidence=evidence,
            sleeper=_no_sleep,
            pass_date_to_adapter=True,
            store_path=store,
        )
    except mock.KilledMidRun:
        killed = True

    # Stage the harder half of the race. A process killed between the ledger
    # append and the store commit leaves a paid-for call whose ranking never
    # landed. Resume must rebuild it from the ledger, not buy it again.
    lost = [d for d in first.calls if d][:3]
    con = sqlite3.connect(store)
    try:
        forget_rows(con, "model_ranking", lost)
        con.commit()
    finally:
        con.close()

    second = mock.MockAdapter(seed=99)
    result = collect(
        dates,
        second,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=store,
    )

    first_dates = [d for d in first.calls if d]
    second_dates = [d for d in second.calls if d]
    overlap = sorted(set(first_dates[:-1]) & set(second_dates))
    servable = _servable(store, dates)
    passed = (
        killed
        and not overlap
        and result.reconciled == len(lost)
        and not (set(lost) & set(second_dates))
        and result.counts.get(CallState.STORED, 0) == servable
        and _ranked_days(store) == servable
    )
    return {
        "passed": passed,
        "killed_after_calls": kill_after,
        "calls_before_kill": len(first_dates),
        "calls_after_resume": len(second_dates),
        "double_called_dates": overlap,
        "lost_commit_dates": lost,
        "lost_dates_recalled": sorted(set(lost) & set(second_dates)),
        "reconciled_from_ledger": result.reconciled,
        "counts": _counts(result),
        "ranked_days": _ranked_days(store),
        "spend_usd": round(spend.total_usd(), 4),
    }


def scenario_model_failed(root: Path, dates: list[str]) -> dict[str, Any]:
    """A forced model fault. The day lands in model_failed, never in no_data."""
    store = _scratch_store(root, dates)
    spend = SpendLedger(path=root / "spend.jsonl")
    evidence = EvidenceLedger(path=root / "evidence.jsonl")
    doomed = frozenset(dates[10:14])
    adapter = mock.MockAdapter(fail_dates=doomed)
    result = collect(
        dates,
        adapter,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=store,
    )

    rows = evidence.rows()
    attempts = {d: sum(1 for r in rows if r["date"] == d) for d in doomed}
    final = {d: [r["state"] for r in rows if r["date"] == d][-1] for d in doomed}
    passed = (
        result.counts.get(CallState.MODEL_FAILED, 0) == len(doomed)
        and result.counts.get(CallState.NO_DATA, 0) == 0
        and result.counts.get(CallState.SOURCE_FAILED, 0) == 0
        and all(n == CONFIG.max_retries for n in attempts.values())
        and all(s == CallState.MODEL_FAILED.value for s in final.values())
    )
    return {
        "passed": passed,
        "forced_dates": sorted(doomed),
        "attempts_per_forced_date": attempts,
        "final_state_per_forced_date": final,
        "counts": _counts(result),
    }


def scenario_source_failed(root: Path, dates: list[str]) -> dict[str, Any]:
    """A forced source fault. No call is sent and the state stays distinct."""
    store = _scratch_store(root, dates)
    broken = dates[20:23]
    con = sqlite3.connect(store)
    try:
        forget_rows(con, "anonymization", broken)
        con.commit()
    finally:
        con.close()

    spend = SpendLedger(path=root / "spend.jsonl")
    evidence = EvidenceLedger(path=root / "evidence.jsonl")
    adapter = mock.MockAdapter()
    result = collect(
        dates,
        adapter,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=store,
    )

    called = {d for d in adapter.calls if d}
    passed = (
        result.counts.get(CallState.SOURCE_FAILED, 0) == len(broken)
        and result.counts.get(CallState.MODEL_FAILED, 0) == 0
        and not (called & set(broken))
    )
    return {
        "passed": passed,
        "broken_dates": broken,
        "calls_sent_for_broken_dates": sorted(called & set(broken)),
        "counts": _counts(result),
    }


def scenario_spend_refused(root: Path, dates: list[str]) -> dict[str, Any]:
    """A lowered cap. The batch is refused before it is sent, not after."""
    store = _scratch_store(root, dates)
    cheap_cap = dataclasses.replace(CONFIG, spend_cap_usd=0.20)
    spend = SpendLedger(path=root / "spend.jsonl", cfg=cheap_cap)
    evidence = EvidenceLedger(path=root / "evidence.jsonl")
    adapter = mock.MockAdapter()
    result = collect(
        dates,
        adapter,
        cfg=cheap_cap,
        spend=spend,
        evidence=evidence,
        sleeper=_no_sleep,
        pass_date_to_adapter=True,
        store_path=store,
    )

    per_call = mock.MOCK_INPUT_TOKENS / 1e6 * cheap_cap.price_input_per_mtok_usd + (
        (mock.MOCK_OUTPUT_TOKENS + mock.MOCK_REASONING_TOKENS)
        / 1e6
        * cheap_cap.price_output_per_mtok_usd
    )
    passed = (
        result.stopped_early.startswith("spend_refused")
        and spend.total_usd() <= cheap_cap.spend_cap_usd
        and len(adapter.calls) < len(dates)
    )
    return {
        "passed": passed,
        "cap_usd": cheap_cap.spend_cap_usd,
        "measured_cost_per_call_usd": round(per_call, 6),
        "calls_sent_before_refusal": len(adapter.calls),
        "spend_at_stop_usd": round(spend.total_usd(), 4),
        "stopped_early": result.stopped_early,
        "counts": _counts(result),
    }


SCENARIOS: dict[str, Callable[[Path, list[str]], dict[str, Any]]] = {
    mock.SCENARIO_CLEAN: scenario_clean,
    mock.SCENARIO_KILL_RESUME: scenario_kill_resume,
    mock.SCENARIO_MODEL_FAILED: scenario_model_failed,
    mock.SCENARIO_SOURCE_FAILED: scenario_source_failed,
    mock.SCENARIO_SPEND_REFUSED: scenario_spend_refused,
}


def _servable(store: Path, dates: list[str]) -> int:
    con = sqlite3.connect(f"file:{store}?mode=ro", uri=True)
    try:
        rows = con.execute("SELECT date, COUNT(*) FROM anonymization GROUP BY date").fetchall()
    finally:
        con.close()
    wanted = set(dates)
    return sum(1 for d, n in rows if d in wanted and n == CONFIG.panel_size)


def _ranked_days(store: Path) -> int:
    con = sqlite3.connect(f"file:{store}?mode=ro", uri=True)
    try:
        return int(con.execute("SELECT COUNT(DISTINCT date) FROM model_ranking").fetchone()[0])
    finally:
        con.close()


def run_one(name: str) -> dict[str, Any]:
    if name not in SCENARIOS:
        raise KeyError(f"unknown scenario {name}. known: {sorted(SCENARIOS)}")
    out = _run(name, SCENARIOS[name])
    out["all_passed"] = bool(out.get("passed"))
    return out


def run_all() -> dict[str, Any]:
    results = [_run(name, fn) for name, fn in SCENARIOS.items()]
    every = all(r.get("passed") for r in results)
    payload = {
        "prompt_template_digest": template_digest(),
        "gate_model": CONFIG.gate_model,
        "scenarios": results,
        "all_passed": every,
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
    }
    write_report(payload)
    return payload


def write_report(payload: dict[str, Any]) -> Path:
    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / "stage_b0b" / "mock_run.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Stage B.0b. Mock run evidence",
        "",
        f"Generated {payload['generated_at']}.",
        "",
        f"Gate model `{payload['gate_model']}`.",
        "",
        "**Prompt template digest, frozen here and used by every B.3 replay:**",
        "",
        f"    {payload['prompt_template_digest']}",
        "",
        "All five scenarios must pass before Stage B.1 sends a single real call.",
        "",
        "| scenario | result |",
        "|---|---|",
    ]
    for r in payload["scenarios"]:
        lines.append(f"| `{r['scenario']}` | {'PASS' if r.get('passed') else 'FAIL'} |")
    lines += ["", f"**Overall: {'PASS' if payload['all_passed'] else 'FAIL'}**", ""]
    for r in payload["scenarios"]:
        lines += [f"## {r['scenario']}", ""]
        for k, v in r.items():
            if k in ("scenario", "passed"):
                continue
            lines.append(f"- `{k}`: {v}")
        lines += ["", f"Result: **{'PASS' if r.get('passed') else 'FAIL'}**", ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
