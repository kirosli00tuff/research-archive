"""Run the collector. One command, three modes.

python -m npd.collect --status                 report without calling
python -m npd.collect --adapter mock           the five B.0b scenarios
python -m npd.collect --adapter openai         the live B.1 collection
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

from npd.callstate import ALL_STATES, CallState
from npd.collect import scenarios
from npd.config import CONFIG
from npd.data.store import open_store
from npd.ledger.evidence import EvidenceLedger
from npd.ledger.spend import SpendLedger
from npd.section0 import fire
from npd.window import derive_window


def window_dates() -> list[str]:
    with open_store() as con:
        sess = [r[0] for r in con.execute("SELECT date FROM session ORDER BY idx")]
    w = derive_window([dt.date.fromisoformat(d) for d in sess])
    return [d.isoformat() for d in w.sessions]


def clears_floor() -> bool:
    with open_store() as con:
        sess = [r[0] for r in con.execute("SELECT date FROM session ORDER BY idx")]
    return derive_window([dt.date.fromisoformat(d) for d in sess]).clears_power_floor


def cmd_status() -> int:
    dates = window_dates()
    with open_store() as con:
        rows = dict(con.execute("SELECT date, state FROM day_status"))
    counts = dict.fromkeys(ALL_STATES, 0)
    for d in dates:
        state = rows.get(d)
        if state is not None:
            counts[CallState(state)] += 1
    spend = SpendLedger()
    report = fire(counts, window_clears_power_floor=clears_floor())
    print(f"window days      {len(dates)}")
    for st in ALL_STATES:
        print(f"  {st.value:<20} {counts[st]}")
    print(f"eligible days    {report.eligible_days}")
    print(f"stored days      {report.stored_days}")
    print(f"coverage         {report.coverage:.1%}")
    print(f"spend            {spend.total_usd():.4f} USD of {CONFIG.spend_cap_usd:.2f}")
    print(f"verdict          {report.verdict.value}")
    print(f"                 {report.rationale}")
    return 0


def cmd_mock(which: str) -> int:
    outcome = scenarios.run_all() if which == "all" else scenarios.run_one(which)
    print(json.dumps(outcome, indent=2, default=str))
    return 0 if outcome.get("all_passed", False) else 1


def cmd_live(*, retry_failed: bool = False) -> int:
    from npd.collect.adapter import OpenAIAdapter
    from npd.env import load_env

    load_env()
    from npd.collect.collector import collect

    dates = window_dates()
    adapter = OpenAIAdapter()
    spend = SpendLedger()

    def show(date: str, state: CallState, done: int, total: int) -> None:
        if done % 10 == 0 or state is not CallState.STORED:
            print(
                f"  {done}/{total}  {date}  {state.value}  {spend.total_usd():.4f} USD",
                flush=True,
            )

    result = collect(
        dates,
        adapter,
        cfg=CONFIG,
        spend=spend,
        evidence=EvidenceLedger(),
        retry_failed=retry_failed,
        progress=show,
    )
    counts = {st: result.counts.get(st, 0) for st in ALL_STATES}
    report = fire(counts, window_clears_power_floor=clears_floor())
    print(
        json.dumps(
            {
                "counts": {k.value: v for k, v in counts.items()},
                "calls_sent": result.calls_sent,
                "spend_usd": round(result.spend_usd, 4),
                "stopped_early": result.stopped_early,
                "coverage": round(report.coverage, 4),
                "verdict": report.verdict.value,
                "rationale": report.rationale,
            },
            indent=2,
        )
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="npd.collect")
    ap.add_argument("--adapter", choices=("mock", "openai"))
    ap.add_argument("--scenarios", default="all")
    ap.add_argument("--status", action="store_true")
    ap.add_argument(
        "--retry-failed",
        action="store_true",
        help="reopen days that reached model_failed under a superseded procedure",
    )
    args = ap.parse_args(argv)

    if args.status:
        return cmd_status()
    if args.adapter == "mock":
        return cmd_mock(args.scenarios)
    if args.adapter == "openai":
        return cmd_live(retry_failed=args.retry_failed)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
