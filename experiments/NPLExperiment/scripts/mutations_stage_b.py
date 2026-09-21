"""The Stage B mutation exercise: three mutations on the new read surface.

Each mutation edits real source, the suite must go red, the source is
restored byte-for-byte, and the suite must go green again. Bytecode is
purged before every run (the InsiderExperiment harness defect: CPython's
cache check can report results from source no longer on disk). This runs
only after the read is spent — the latch already exists — so no mutation
can touch a live verdict path.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "npl"
REPORT = ROOT / "reports" / "stage_b" / "mutations.md"


@dataclass(frozen=True)
class Mutation:
    name: str
    path: Path
    old: str
    new: str
    catches: str


MUTATIONS = [
    Mutation(
        name="MB1: bypass the latch so a second read is allowed",
        path=SRC / "stageb" / "cli.py",
        old=(
            "    if latch_path.exists():\n"
            "        raise ReadAlreadySpent(\n"
            '            f"the latch {latch_path} exists: the single registered read is spent; "\n'
            '            f"recovery works from partial artifacts under an amendment, '
            'never a re-run"\n'
            "        )\n"
            "    precondition_report, windows = run_preconditions("
        ),
        new="    precondition_report, windows = run_preconditions(",
        catches="tests/test_stageb_reader.py (ReadAlreadySpent is produced, not asserted)",
    ),
    Mutation(
        name="MB2: widen the blindness allowlist to two modules",
        path=SRC / "stageb" / "__init__.py",
        old='STAGE_B_OUTCOME_EXEMPT: Final[tuple[str, ...]] = ("stageb/reader.py",)',
        new=(
            'STAGE_B_OUTCOME_EXEMPT: Final[tuple[str, ...]] = ("stageb/reader.py", "stageb/cli.py")'
        ),
        catches="tests/test_guards.py (the equality pin holds the allowlist at length one)",
    ),
    Mutation(
        name="MB3: flip the funding sign convention inside the reader",
        path=SRC / "stageb" / "reader.py",
        old="    rates = [rate for t, rate in funding if entry_ms < t <= funding_end]",
        new="    rates = [-rate for t, rate in funding if entry_ms < t <= funding_end]",
        catches="tests/test_stageb_reader.py (the known-answer gate, sign pin -0.0729)",
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
        "# Stage B mutation evidence",
        "",
        "Each mutation edits real source on the new Stage B surface; the suite",
        "must go red; the source is restored byte-for-byte; the suite must go",
        "green. Bytecode is purged before every run. The read was already spent",
        "when this ran (the latch exists), so no mutation touched a live verdict.",
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
