"""The registered mutation exercise. A guard that has never been shown to
fail is not a guard.

Each mutation edits real source, the suite must go red, the source is
restored byte-for-byte, and the suite must go green again. Bytecode is
purged before every run: a one-character edit can leave file size and
mtime-in-seconds unchanged, and CPython's cache check then reports results
from source no longer on disk (the InsiderExperiment harness defect).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "npl"
REPORT = ROOT / "reports" / "stage_a4" / "mutations.md"


@dataclass(frozen=True)
class Mutation:
    name: str
    path: Path
    old: str
    new: str
    catches: str


MUTATIONS = [
    Mutation(
        name="M1: delete a blindness pin (the funding gate becomes unconditional)",
        path=SRC / "blindness.py",
        old=(
            "        if entry_ms is not None and time_ms <= entry_ms:\n"
            '            rate = float(row["fundingRate"])\n'
            "        else:\n"
            "            rate = BLINDNESS_GATED"
        ),
        new='        rate = float(row["fundingRate"])',
        catches="tests/test_blindness.py (post-entry absence), tests/test_guards.py (gate in AST)",
    ),
    Mutation(
        name="M2: coerce an absence to zero",
        path=SRC / "absence.py",
        old=(
            "    def __float__(self) -> float:\n"
            "        raise TypeError(\n"
            '            "refusing to coerce a recorded absence to a float. "\n'
            '            "Handle AbsenceReason explicitly or drop the row."\n'
            "        )"
        ),
        new="    def __float__(self) -> float:\n        return 0.0",
        catches="tests/test_absence.py, tests/test_blindness.py (gated rate refuses a sum)",
    ),
    Mutation(
        name="M3: merge rate_limited into no_data",
        path=SRC / "venue.py",
        old=(
            "    if status == 429:\n        return CallState.RATE_LIMITED\n"
            "    return CallState.SOURCE_FAILED"
        ),
        new=(
            "    if status == 429:\n        return CallState.NO_DATA\n"
            "    return CallState.SOURCE_FAILED"
        ),
        catches="tests/test_venue.py (429 is rate_limited), tests/test_census.py",
    ),
    Mutation(
        name="M4: move a registered boundary (GO requires strictly above 0.80)",
        path=SRC / "section0.py",
        old="    if delisting is DelistingObservability.PASS and pmin >= cfg.power_go_floor:",
        new="    if delisting is DelistingObservability.PASS and pmin > cfg.power_go_floor:",
        catches="tests/test_section0.py (the fixture sits exactly on 0.80)",
    ),
    Mutation(
        name="M5: read a post-entry funding row inside matching",
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
        "# Stage A.4 mutation evidence",
        "",
        "Each mutation edits real source; the suite must go red; the source is",
        "restored byte-for-byte; the suite must go green. Bytecode is purged",
        "before every run.",
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
