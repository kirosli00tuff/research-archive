"""The register Stage A mutation exercise: six mutations on the new surface.

Each mutation edits real source, the suite must go red, the source is
restored byte-for-byte, and the suite must go green again. Bytecode is
purged before every run (the InsiderExperiment harness defect: CPython's
cache check can report results from source no longer on disk). No mutation
can touch a live verdict: no successor read exists, the H1 latch already
exists, and the dark pair reader has only ever seen synthetic fixtures.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "npl"
REPORT = ROOT / "reports" / "stage_a_h2" / "mutations.md"


@dataclass(frozen=True)
class Mutation:
    name: str
    path: Path
    old: str
    new: str
    catches: str


MUTATIONS = [
    Mutation(
        name="MR1: open reports/stage_b/read.json from an H2 module",
        path=SRC / "register" / "views.py",
        old='MAIN_DEX = ""',
        new=(
            'MAIN_DEX = ""\n\n\n'
            "def _peek_spent_read() -> bytes:\n"
            '    with open("reports/stage_b/read.json", "rb") as fh:\n'
            "        return fh.read()"
        ),
        catches=(
            "tests/test_guards.py (the stage_b string quarantine pin: the reachable "
            "surface is exactly the two H1 modules)"
        ),
    ),
    Mutation(
        name="MR2: admit a generating-sample event ID into an H2 eligibility view",
        path=SRC / "register" / "views.py",
        old=(
            "def _require_fresh(events: tuple[FreshEvent, ...], sample: frozenset[str]) -> None:\n"
            "    refuse_generating_sample((event.event_id() for event in events), sample)"
        ),
        new=(
            "def _require_fresh(events: tuple[FreshEvent, ...], sample: frozenset[str]) -> None:\n"
            "    return None"
        ),
        catches="tests/test_register.py (the refusal is produced through the real views)",
    ),
    Mutation(
        name="MR3: read a post-entry funding row inside control assignment",
        path=SRC / "controls.py",
        old=(
            "    for row in rows:\n"
            "        if row.time_ms > entry_ms:\n"
            "            raise PostEntryRead(\n"
            '                f"a funding row stamped {row.time_ms} reached the matcher for an '
            'entry at "\n'
            '                f"{entry_ms}. Matching reads no row stamped after the event entry."\n'
            "            )\n"
            "    window_start"
        ),
        new="    window_start",
        catches="tests/test_a3_modules.py (PostEntryRead is produced, not asserted)",
    ),
    Mutation(
        name="MR4: flip a pair-leg sign in the dark reader",
        path=SRC / "register" / "pairs.py",
        old="        elder_funding_term=-float(sum(elder_hourly_rates)),",
        new="        elder_funding_term=+float(sum(elder_hourly_rates)),",
        catches=(
            "tests/test_register_a3.py (the four-leg known-answer gate and the both-legs sign pin)"
        ),
    ),
    Mutation(
        name="MR5: let the cull read an outcome field",
        path=SRC / "register" / "cull.py",
        old="SpecKey = tuple[str, str]",
        new=(
            "SpecKey = tuple[str, str]\n\n\n"
            "def _peek_close(row: dict[str, float]) -> float:\n"
            '    return row["c"]'
        ),
        catches=(
            "tests/test_guards.py (the repo-wide OHLCV pin: no module reads a priced candle field)"
        ),
    ),
    Mutation(
        name="MR6: widen a reader allowlist",
        path=SRC / "stageb" / "__init__.py",
        old='STAGE_B_OUTCOME_EXEMPT: Final[tuple[str, ...]] = ("stageb/reader.py",)',
        new=(
            "STAGE_B_OUTCOME_EXEMPT: Final[tuple[str, ...]] = "
            '("stageb/reader.py", "register/pairs.py")'
        ),
        catches="tests/test_guards.py (the equality pin holds the allowlist at length one)",
    ),
]


def purge_bytecode() -> None:
    for pycache in ROOT.rglob("__pycache__"):
        if ".venv" in pycache.parts:
            continue
        shutil.rmtree(pycache, ignore_errors=True)
    shutil.rmtree(ROOT / ".pytest_cache", ignore_errors=True)


def run_suite() -> bool:
    purge_bytecode()
    result = subprocess.run(
        ["uv", "run", "pytest", "-q", "--no-header", "-x"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Register Stage A mutation evidence",
        "",
        "Each mutation edits real source on the register surface; the suite",
        "must go red; the source is restored byte-for-byte; the suite must go",
        "green. Bytecode is purged before every run. No successor read exists,",
        "so no mutation could touch a live verdict.",
        "",
    ]
    if not run_suite():
        print("refusing: the suite is not green before mutations", file=sys.stderr)
        return 1
    lines.append("Baseline: suite green before any mutation.")
    lines.append("")
    failures = 0
    for mutation in MUTATIONS:
        original = mutation.path.read_text(encoding="utf-8")
        if mutation.old not in original:
            print(f"{mutation.name}: target text not found; the harness is stale", file=sys.stderr)
            return 1
        mutation.path.write_text(original.replace(mutation.old, mutation.new), encoding="utf-8")
        went_red = not run_suite()
        mutation.path.write_text(original, encoding="utf-8")
        restored = mutation.path.read_text(encoding="utf-8") == original
        green_again = run_suite()
        verdict = "CAUGHT" if (went_red and restored and green_again) else "MISSED"
        if verdict == "MISSED":
            failures += 1
        lines.append(f"## {mutation.name}")
        lines.append("")
        lines.append(f"- file: `{mutation.path.relative_to(ROOT)}`")
        lines.append(f"- expected catch: {mutation.catches}")
        lines.append(f"- suite red under mutation: **{went_red}**")
        lines.append(f"- source restored byte-for-byte: **{restored}**")
        lines.append(f"- suite green after restore: **{green_again}**")
        lines.append(f"- verdict: **{verdict}**")
        lines.append("")
        print(f"{verdict}: {mutation.name}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report -> {REPORT.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
