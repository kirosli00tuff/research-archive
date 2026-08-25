"""Report Stage B.1. Per-state counts, spend against cap, coverage, Section 0.

Coverage decides the Section 0 verdict and nothing else does. This script reads
no forward return, joins no output to any outcome, and computes no statistic
relating the two. It counts days and dollars.
"""

from __future__ import annotations

import collections
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from npd.callstate import ALL_STATES, CallState  # noqa: E402
from npd.collect.prompt import template_digest  # noqa: E402
from npd.config import CONFIG  # noqa: E402
from npd.data.store import open_store  # noqa: E402
from npd.ledger.evidence import EvidenceLedger  # noqa: E402
from npd.ledger.spend import SpendLedger  # noqa: E402
from npd.section0 import fire  # noqa: E402
from npd.window import derive_window  # noqa: E402


def main() -> int:
    with open_store() as con:
        sess = [r[0] for r in con.execute("SELECT date FROM session ORDER BY idx")]
        window = derive_window([dt.date.fromisoformat(d) for d in sess])
        dates = [d.isoformat() for d in window.sessions]
        states = dict(con.execute("SELECT date, state FROM day_status"))
        ranked = {
            r[0]: r[1]
            for r in con.execute("SELECT date, COUNT(*) FROM model_ranking GROUP BY date")
        }

    counts = dict.fromkeys(ALL_STATES, 0)
    for d in dates:
        s = states.get(d)
        if s is not None:
            counts[CallState(s)] += 1

    spend = SpendLedger()
    evidence = EvidenceLedger()
    rows = evidence.rows()
    all_gate_rows = [r for r in rows if r["date"] != "calibration"]
    current = template_digest()
    gate_rows = [r for r in all_gate_rows if str(r.get("prompt_digest", "")) == current]
    superseded_rows = [r for r in all_gate_rows if str(r.get("prompt_digest", "")) != current]
    attempts = collections.Counter(r["date"] for r in gate_rows)
    retried = {d: n for d, n in attempts.items() if n > 1}
    tokens_in = sum(int(r["input_tokens"]) for r in gate_rows)
    tokens_out = sum(int(r["output_tokens"]) for r in gate_rows)
    reasoning = sum(int(r["reasoning_tokens"]) for r in gate_rows)
    calib = [r for r in rows if r["date"] == "calibration"]
    last_by_date: dict[str, dict[str, object]] = {}
    for r in gate_rows:
        last_by_date[str(r["date"])] = r
    escalated = sum(
        1
        for r in last_by_date.values()
        if r.get("state") == "stored" and str(r.get("reasoning_effort") or "") == "low"
    )

    # Structural integrity of what was stored. Ranks, labels, and symbols only.
    # No forward return is read and no output is joined to any outcome.
    integrity: dict[str, int] = collections.Counter()
    with open_store() as con:
        for d in dates:
            ranking_rows = con.execute(
                "SELECT rank, label, symbol FROM model_ranking WHERE date = ? ORDER BY rank", (d,)
            ).fetchall()
            if not ranking_rows:
                continue
            mapping = dict(
                con.execute("SELECT label, symbol FROM anonymization WHERE date = ?", (d,))
            )
            panel_symbols = {
                r[0] for r in con.execute("SELECT symbol FROM panel WHERE date = ?", (d,))
            }
            integrity["days_with_a_ranking"] += 1
            if [r[0] for r in ranking_rows] == list(range(1, CONFIG.panel_size + 1)):
                integrity["ranks_are_1_to_30"] += 1
            if {r[1] for r in ranking_rows} == set(mapping):
                integrity["labels_match_the_mapping"] += 1
            if {r[2] for r in ranking_rows} == panel_symbols:
                integrity["symbols_match_the_panel"] += 1
            if all(mapping.get(r[1]) == r[2] for r in ranking_rows):
                integrity["label_to_symbol_is_consistent"] += 1

    report = fire(counts, window_clears_power_floor=window.clears_power_floor)
    full_rankings = sum(1 for d in dates if ranked.get(d) == CONFIG.panel_size)
    short = {d: n for d, n in ranked.items() if d in set(dates) and n != CONFIG.panel_size}

    payload = {
        "window": {"start": str(window.start), "end": str(window.end), "days": window.n_days},
        "counts": {k.value: v for k, v in counts.items()},
        "coverage": round(report.coverage, 4),
        "verdict": report.verdict.value,
        "spend_usd": round(spend.total_usd(), 4),
        "cap_usd": CONFIG.spend_cap_usd,
        "full_rankings_stored": full_rankings,
        "escalated_days": escalated,
        "integrity": dict(integrity),
    }

    lines = [
        "# Stage B.1. The live gate collection",
        "",
        f"Completed {dt.datetime.now(dt.UTC).isoformat()}.",
        "",
        f"Gate model `{CONFIG.gate_model}`, reasoning effort `{CONFIG.reasoning_effort}`, "
        f"temperature not sent (Amendment 1).",
        "",
        f"Prompt template digest `{template_digest()}`.",
        "",
        "## Window",
        "",
        f"- {window.start} through {window.end}",
        f"- **{window.n_days} trading days**, derived from the verified cutoff "
        f"{CONFIG.knowledge_cutoff} plus a one month guard band",
        f"- clears the registered {CONFIG.min_trading_days} day floor: "
        f"**{window.clears_power_floor}**",
        "",
        "## Per-state counts",
        "",
        "The five states are never merged.",
        "",
        "| state | days | class |",
        "|---|---|---|",
    ]
    classes = {
        CallState.STORED: "sample",
        CallState.NO_DATA: "sample composition",
        CallState.MODEL_FAILED: "**operational health**",
        CallState.EXCLUDED_PRE_CUTOFF: "**sample composition**",
        CallState.SOURCE_FAILED: "operational health",
    }
    for st in ALL_STATES:
        lines.append(f"| `{st.value}` | {counts[st]} | {classes[st]} |")
    lines += [
        f"| **total** | **{sum(counts.values())}** | |",
        "",
        "## Coverage against the Section 0 bars",
        "",
        f"- eligible days, `excluded_pre_cutoff` removed from the denominator: "
        f"**{report.eligible_days}**",
        f"- days carrying a stored, parseable ranking: **{report.stored_days}**",
        f"- days carrying a full {CONFIG.panel_size} name ranking in the store: "
        f"**{full_rankings}**",
        f"- coverage: **{report.coverage:.1%}**",
        "",
        "| bar | threshold | met |",
        "|---|---|---|",
        f"| GO | at least {CONFIG.coverage_go_floor:.0%} | "
        f"{'yes' if report.coverage >= CONFIG.coverage_go_floor else 'no'} |",
        f"| DEGRADED | {CONFIG.coverage_degraded_floor:.0%} to {CONFIG.coverage_go_floor:.0%} | "
        f"{'yes' if CONFIG.coverage_degraded_floor <= report.coverage < CONFIG.coverage_go_floor else 'no'} |",
        f"| BLOCKED | under {CONFIG.coverage_degraded_floor:.0%}, or the window under the power floor | "
        f"{'yes' if report.verdict.value == 'BLOCKED' else 'no'} |",
        "",
        f"## Section 0 verdict: **{report.verdict.value}**",
        "",
        report.rationale,
        "",
        "## Spend",
        "",
        f"- gate calls billed: **{spend.n_calls('gate')}**",
        f"- calibration calls, excluded from the sample: **{spend.n_calls('calibration')}**",
        f"- total spent: **{spend.total_usd():.4f} USD** of a {CONFIG.spend_cap_usd:.2f} USD cap",
        f"- remaining: **{spend.remaining_usd():.4f} USD**",
        f"- measured cost per gate call: **{(spend.mean_cost_per_call('gate') or 0.0):.6f} USD**",
        f"- input tokens: {tokens_in:,}",
        f"- output tokens: {tokens_out:,}, of which reasoning {reasoning:,}",
        "",
        "## Stored ranking integrity",
        "",
        "Structural only. No forward return was read and no output was joined to any",
        "outcome.",
        "",
        "| check | days |",
        "|---|---|",
        f"| days with a ranking in the store | {integrity['days_with_a_ranking']} |",
        f"| ranks are exactly 1 to {CONFIG.panel_size} | {integrity['ranks_are_1_to_30']} |",
        f"| labels match that day mapping | {integrity['labels_match_the_mapping']} |",
        f"| symbols match that day panel | {integrity['symbols_match_the_panel']} |",
        f"| label to symbol is consistent | {integrity['label_to_symbol_is_consistent']} |",
        "",
        "## Operational health",
        "",
        f"- attempts under the current procedure: **{len(gate_rows)}**, "
        f"across {len(attempts)} days, {len(gate_rows) / max(1, len(attempts)):.2f} per day",
        f"- days needing more than one attempt: **{len(retried)}**",
        f"- attempts by reasoning effort: "
        f"**{dict(collections.Counter(str(r.get('reasoning_effort')) for r in gate_rows))}**",
        f"- superseded attempts, kept in the ledger and excluded from these counts: "
        f"**{len(superseded_rows)}**",
        f"- calibration calls, excluded from the sample: **{len(calib)}**",
        f"- days whose stored answer came from `low` after an escalation: **{escalated}**",
    ]
    if retried:
        lines += ["", "| date | attempts |", "|---|---|"]
        for d, n in sorted(retried.items())[:20]:
            lines.append(f"| {d} | {n} |")
    if short:
        lines += ["", f"Days with a partial ranking in the store: {sorted(short)}"]

    lines += [
        "",
        "## What this stage did not do",
        "",
        "It computed no rank IC, read no outcome against any output, and fired no",
        "hypothesis verdict. The Section 0 verdict above is fired on coverage alone.",
        "B.2 runs once, later, and only after the operator writes his registered prior",
        "into REGISTRATION.md Section 13.",
        "",
    ]

    out = ROOT / "reports" / "stage_b1"
    out.mkdir(parents=True, exist_ok=True)
    (out / "collection.md").write_text("\n".join(lines), encoding="utf-8")
    (out / "collection.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
