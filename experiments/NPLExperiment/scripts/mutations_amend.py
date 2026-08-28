"""Task 5 of the H2 amendment stage: mutations on the Amendment H2-3 surface.

Each mutation edits real source, the suite must go red, the source is
restored byte-for-byte, and the suite must go green again. Bytecode is
purged before every run (the InsiderExperiment harness defect: CPython's
cache check can report results from source no longer on disk).

No mutation can touch a live verdict. No H2 look has been read: both
per-look latches are absent, the pair reader has only ever seen synthetic
fixtures, and every mutation below is on machinery that has never seen an
outcome value.

The registered four (register prompt, Task 5):

  MA1  spend look 2's alpha at look 1
  MA2  admit a cross_dex pair into the same_dex stratum
  MA3  read a post-entry funding row inside fallback assignment
  MA4  bypass a per-look latch

Two more ride along because the amendment created their surface too:

  MA5  drop the pair-type tag from a fallback assignment
  MA6  let the look-2 read run without look 1's counts
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "npl"
REPORT = ROOT / "reports" / "stage_a_h2" / "mutations_amend.md"


@dataclass(frozen=True)
class Mutation:
    name: str
    path: Path
    old: str
    new: str
    catches: str


MUTATIONS = [
    Mutation(
        name="MA1: spend look 2's alpha at look 1",
        path=SRC / "register" / "sequential.py",
        old="    k1 = critical_k(n1, p0, alpha_1)",
        new="    k1 = critical_k(n1, p0, alpha_1 + alpha_2)",
        catches=(
            "tests/test_amend.py (the recorded boundary: k1 is 38 at alpha_1 alone and 37 at "
            "the whole budget — the interim would spend the entire 0.05)"
        ),
    ),
    Mutation(
        name="MA2: admit a cross_dex pair into the same_dex stratum",
        path=SRC / "register" / "pairs.py",
        old="    subset = [(pair, net) for pair, net in present if pair.pair_type "
        "== PAIR_TYPE_SAME_DEX]",
        new="    subset = list(present)",
        catches=(
            "tests/test_amend.py (the stratum is 20 same-dex pairs of 30; admitting the "
            "cross_dex 10 makes it 30)"
        ),
    ),
    Mutation(
        name="MA3: read a post-entry funding row inside fallback assignment",
        path=SRC / "controls.py",
        old="        mean = trailing_mean(candidate.rows, entry_ms, cfg)",
        new=(
            "        mean = trailing_mean(\n"
            "            tuple(r for r in candidate.rows if r.time_ms <= entry_ms), entry_ms, cfg\n"
            "        )"
        ),
        catches=(
            "tests/test_amend.py (PostEntryRead is produced through the fallback path; the "
            "silent pre-filter swallows the refusal instead of raising it)"
        ),
    ),
    Mutation(
        name="MA4: bypass a per-look latch",
        path=SRC / "register" / "latches.py",
        old=(
            "    target = path if path is not None else look_latch_path(hypothesis, look)\n"
            "    if target.exists():\n"
            "        raise RegisterReadAlreadySpent("
        ),
        new=(
            "    target = path if path is not None else look_latch_path(hypothesis, look)\n"
            "    if False:\n"
            "        raise RegisterReadAlreadySpent("
        ),
        catches="tests/test_amend.py (a spent look must refuse a second read, loudly)",
    ),
    Mutation(
        name="MA5: drop the pair-type tag from a fallback assignment",
        path=SRC / "controls.py",
        old="            pair_type = PAIR_TYPE_CROSS_DEX",
        new="            pair_type = PAIR_TYPE_SAME_DEX",
        catches=(
            "tests/test_amend.py (the fallback pair is tagged cross_dex in the assignment and "
            "in the append-only ledger row)"
        ),
    ),
    Mutation(
        name="MA6: let the look-2 read run without look 1's counts",
        path=SRC / "register" / "pairs.py",
        old="    if prior is None:\n        raise LookOrderViolation(",
        new="    if False:\n        raise LookOrderViolation(",
        catches=(
            "tests/test_amend.py (a look-2 read with no look-1 record must refuse; the "
            "boundary it would compute has no k1 to condition on)"
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
        "# Amendment H2-3 mutation evidence",
        "",
        "Each mutation edits real source on the amendment surface; the suite must",
        "go red; the source is restored byte-for-byte; the suite must go green.",
        "Bytecode is purged before every run. **No H2 look has been read** — both",
        "per-look latches are absent and the pair reader has only ever seen",
        "synthetic fixtures — so no mutation could touch a live verdict.",
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
