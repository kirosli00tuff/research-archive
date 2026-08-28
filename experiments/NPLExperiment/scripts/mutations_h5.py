"""Register entry H5, Task 6: mutations on the H5 surface.

Each mutation edits real source, the suite must go red, the source is
restored byte-for-byte, and the suite must go green again. Bytecode is
purged before every run (the InsiderExperiment harness defect: CPython's
cache check can report results from source no longer on disk).

**No mutation can touch a live verdict.** H5 has no Stage B, no latch, and
no capital; the map has been fired only on H5's own stores, and every H2
store is read-only to this entry by construction.

The registered four (operator prompt, Task 6):

  MH1  compute a basis from a field the venue did not serve in the same snapshot
  MH2  let an H5 path write into an H2 store
  MH3  interpolate an absent reference
  MH4  mis-tag a weekend snapshot as regular hours

Three more ride along, one per amendment surface this stage created:

  MH5  bypass the retrospective cohort gate
  MH6  let the named secondary series fire VIABLE
  MH7  exclude a delisted instrument on the flag alone
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "npl"
REPORT = ROOT / "reports" / "h5" / "mutations.md"


@dataclass(frozen=True)
class Mutation:
    name: str
    path: Path
    old: str
    new: str
    catches: str


MUTATIONS = [
    Mutation(
        name="MH1: compute a basis from a field the venue did not serve in the same snapshot",
        path=SRC / "h5" / "basis.py",
        old="    if mark.snapshot_id != reference.snapshot_id:",
        new="    if False:",
        catches=(
            "tests/test_h5_registration.py (a mark from snap-1 against an oracle from snap-0 "
            "must raise CrossSnapshotBasis; Section 3 admits only same-snapshot fields)"
        ),
    ),
    Mutation(
        name="MH2: let an H5 path write into an H2 store",
        path=SRC / "h5" / "stores.py",
        old="    if resolved != root and root not in resolved.parents:",
        new="    if False:",
        catches=(
            "tests/test_h5_registration.py (the refusal is produced on the real path "
            "data/controls/h2_pairs.jsonl, not asserted in a comment)"
        ),
    ),
    Mutation(
        name="MH3: interpolate an absent reference",
        path=SRC / "h5" / "basis.py",
        old=(
            "    out: list[Maybe[float]] = []\n"
            "    for ctx in contexts:\n"
            "        out.append(context_basis_bp(ctx))\n"
            "    return tuple(out)"
        ),
        new=(
            "    out: list[Maybe[float]] = []\n"
            "    last: Maybe[float] | None = None\n"
            "    for ctx in contexts:\n"
            "        value = context_basis_bp(ctx)\n"
            "        if is_absent(value) and last is not None:\n"
            "            value = last\n"
            "        else:\n"
            "            last = value\n"
            "        out.append(value)\n"
            "    return tuple(out)"
        ),
        catches=(
            "tests/test_h5_registration.py (a middle gap must stay Absent and the served n "
            "must drop from 3 to 2; the carry-forward makes it 3 again)"
        ),
    ),
    Mutation(
        name="MH4: mis-tag a weekend snapshot as regular hours",
        path=SRC / "h5" / "calendar.py",
        old="    return day.weekday() >= SATURDAY",
        new="    return day.weekday() > SATURDAY",
        catches=(
            "tests/test_h5_registration.py (Saturday 2026-08-29 at noon ET must tag weekend; "
            "the moved boundary tags it regular, and the fixture sits ON Saturday)"
        ),
    ),
    Mutation(
        name="MH5: bypass the retrospective cohort gate",
        path=SRC / "h5" / "retro.py",
        old="    require_ungated(coin, cohorts)",
        new="    _ = (coin, cohorts)",
        catches=(
            "tests/test_h5_retro.py and tests/test_h5_guards.py (a generating-sample coin "
            "must reach nothing; the structural pin also requires the gate to be the first "
            "statement of fetch_series)"
        ),
    ),
    Mutation(
        name="MH6: let the named secondary series fire VIABLE",
        path=SRC / "h5" / "outcome.py",
        old="        if series_kind == SERIES_SECONDARY_DEVIATION:",
        new="        if False:",
        catches=(
            "tests/test_h5_registration.py (a secondary at 300 bp must land INDETERMINATE, "
            "never VIABLE: a differently constructed number could be an artefact)"
        ),
    ),
    Mutation(
        name="MH7: exclude a delisted instrument on the flag alone",
        path=SRC / "h5" / "listing.py",
        old="    if is_delisted and oi_zero and vol_zero:",
        new="    if is_delisted:",
        catches=(
            "tests/test_h5_listing.py (a flagged instrument with live open interest must "
            "read conflicting, not excluded; Amendment H5-2's rule is conjunctive)"
        ),
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
    header = [
        "# Register entry H5 — mutation evidence",
        "",
        "Each mutation edits real source on the H5 surface; the suite must go red;",
        "the source is restored byte-for-byte; the suite must go green. Bytecode is",
        "purged before every run. **No mutation could touch a live verdict**: H5 has",
        "no Stage B, no latch and no capital, the map is fired only from H5's own",
        "stores, and every H2 store is read-only to this entry by construction.",
        "",
    ]
    if not run_suite():
        print("refusing: the suite is not green before mutations", file=sys.stderr)
        return 1
    body = ["Baseline: suite green before any mutation.", ""]
    failures = 0
    for mutation in MUTATIONS:
        original = mutation.path.read_text(encoding="utf-8")
        if mutation.old not in original:
            print(f"{mutation.name}: target text not found; the harness is stale", file=sys.stderr)
            return 1
        mutation.path.write_text(original.replace(mutation.old, mutation.new, 1), encoding="utf-8")
        went_red = not run_suite()
        mutation.path.write_text(original, encoding="utf-8")
        restored = mutation.path.read_text(encoding="utf-8") == original
        green_again = run_suite()
        verdict = "CAUGHT" if (went_red and restored and green_again) else "MISSED"
        if verdict == "MISSED":
            failures += 1
        body.extend(
            [
                f"## {mutation.name}",
                "",
                f"- file: `{mutation.path.relative_to(ROOT)}`",
                f"- expected catch: {mutation.catches}",
                f"- suite red under mutation: **{went_red}**",
                f"- source restored byte-for-byte: **{restored}**",
                f"- suite green after restore: **{green_again}**",
                f"- verdict: **{verdict}**",
                "",
            ]
        )
        print(f"{verdict}: {mutation.name}", flush=True)
    caught = len(MUTATIONS) - failures
    header.extend([f"**Result: {caught} of {len(MUTATIONS)} CAUGHT.**", ""])
    REPORT.write_text("\n".join(header + body) + "\n", encoding="utf-8")
    print(f"report -> {REPORT.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
