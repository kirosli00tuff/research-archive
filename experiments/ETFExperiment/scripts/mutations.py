"""The mutation harness. Applied to real source, never to a copy.

Each mutation edits a real file, runs the guard suite, asserts it goes red,
restores the file, and asserts it goes green again. Bytecode is purged before
every run: a one-digit edit leaves file size and mtime-in-seconds unchanged, so
CPython will happily reuse mutated bytecode after a restore and the harness
will report on source no longer on disk (InsiderExperiment defect 3).

Populated at Stage A.4 Task 2 with at least six mutations. The purge and the
runner live here from Stage A.0 so the harness is never the thing written last.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "etf"


@dataclass(frozen=True, slots=True)
class Mutation:
    name: str
    path: Path
    find: str
    replace: str
    expect_failing_tests: tuple[str, ...]
    why: str


def purge_bytecode() -> None:
    """Remove every __pycache__ under the repo before a run.

    A mutation harness that can report on absent source is worse than no
    harness. This is the InsiderExperiment lesson, ported by copying.
    """
    for cache in ROOT.rglob("__pycache__"):
        shutil.rmtree(cache, ignore_errors=True)


def run_tests(targets: Sequence[str]) -> subprocess.CompletedProcess[bytes]:
    purge_bytecode()
    return subprocess.run(
        ["uv", "run", "pytest", "-q", "-p", "no:cacheprovider", *targets],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )


def apply_and_check(mutation: Mutation) -> bool:
    original = mutation.path.read_text(encoding="utf-8")
    if mutation.find not in original:
        print(f"[{mutation.name}] SKIPPED: anchor text not found in {mutation.path}")
        return False
    mutated = original.replace(mutation.find, mutation.replace, 1)
    try:
        mutation.path.write_text(mutated, encoding="utf-8")
        red = run_tests(mutation.expect_failing_tests)
        caught = red.returncode != 0
    finally:
        mutation.path.write_text(original, encoding="utf-8")
    green = run_tests(mutation.expect_failing_tests)
    restored = green.returncode == 0
    print(f"[{mutation.name}] caught={caught} restored_green={restored} :: {mutation.why}")
    return caught and restored


MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        name="1-delete-a-blindness-pin",
        path=SRC / "blindness.py",
        find=(
            'FundingRow(time_ms=time_ms, rate=gate_pre_period(time_ms, float(row["fundingRate"])))'
        ),
        replace='FundingRow(time_ms=time_ms, rate=float(row["fundingRate"]))',
        expect_failing_tests=("tests/test_blindness.py", "tests/test_guards.py"),
        why=(
            "the funding reader stops routing rates through the pre-period pin, so every "
            "post-2025-05-01 rate becomes readable outside the carve-out"
        ),
    ),
    Mutation(
        name="2-coerce-an-absence-to-zero",
        path=SRC / "flow.py",
        find="    if text in DASH_TOKENS:\n        return DASH_IN_CELL",
        replace="    if text in DASH_TOKENS:\n        return 0.0",
        expect_failing_tests=("tests/test_flow.py", "tests/test_snapshot.py"),
        why=(
            "a dash becomes a fabricated flat day, which on the open day would make every "
            "capture before the print look like a printed zero"
        ),
    ),
    Mutation(
        name="3-merge-rate-limited-into-no-data",
        path=SRC / "callstate.py",
        find=(
            "OPERATIONAL_HEALTH_STATES: frozenset[CallState] = frozenset(\n"
            "    {CallState.SOURCE_FAILED, CallState.RATE_LIMITED, CallState.EXPIRED}\n"
            ")"
        ),
        replace=(
            "OPERATIONAL_HEALTH_STATES: frozenset[CallState] = frozenset(\n"
            "    {CallState.SOURCE_FAILED, CallState.EXPIRED}\n"
            ")"
        ),
        expect_failing_tests=("tests/test_callstate.py",),
        why="a source refusing a request becomes indistinguishable from a source answering emptily",
    ),
    Mutation(
        name="4-move-the-anchor-boundary",
        path=SRC / "anchor.py",
        find="    return capture_ts < entry_anchor(trade_day, anchor_hour_utc)",
        replace="    return capture_ts <= entry_anchor(trade_day, anchor_hour_utc)",
        expect_failing_tests=("tests/test_anchor.py",),
        why=(
            "a capture taken exactly at the anchor becomes admissible, which admits a value "
            "the registered rule could not have read before entering"
        ),
    ),
    Mutation(
        name="5-substitute-a-live-value-for-a-missing-capture",
        path=SRC / "census.py",
        find=(
            "        later = window is not None and any("
            "m.captured_at >= window[1] for m in ordered)"
        ),
        replace=(
            "        if not qualifying:\n"
            "            rows.append(\n"
            "                CensusRow(\n"
            "                    trade_date=day.trade_date,\n"
            "                    admissible=True,\n"
            "                    state=CallState.STORED,\n"
            "                    source=AdmissibilitySource.RETRO_ARCHIVE,\n"
            "                    capture_timestamp=None,\n"
            "                    revised=False,\n"
            "                    exclusion_reason=None,\n"
            "                    printed_signal_present=True,\n"
            "                )\n"
            "            )\n"
            "            continue\n"
            "        later = window is not None and any("
            "m.captured_at >= window[1] for m in ordered)"
        ),
        expect_failing_tests=("tests/test_census.py",),
        why=(
            "a day with no qualifying archive capture is admitted anyway, so its value could "
            "only come from the source's current page - the substitution Section 3 forbids"
        ),
    ),
    Mutation(
        name="6-read-a-post-carve-out-price",
        path=SRC / "preperiod_prices.py",
        find=(
            "        require_pre_period(close_ms, "
            '"pre-period price reader (Section 9 carve-out)")\n'
        ),
        replace="",
        expect_failing_tests=("tests/test_preperiod_prices.py", "tests/test_guards.py"),
        why=(
            "the carve-out reader stops enforcing its own date pin, so a window straddling "
            "2025-05-01 would serve test-sample closes to the power computation"
        ),
    ),
)


def main() -> int:
    if not MUTATIONS:
        print("no mutations registered yet; Stage A.4 Task 2 populates this harness")
        return 0
    results = [apply_and_check(m) for m in MUTATIONS]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
