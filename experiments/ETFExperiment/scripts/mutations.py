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


MUTATIONS: tuple[Mutation, ...] = ()


def main() -> int:
    if not MUTATIONS:
        print("no mutations registered yet; Stage A.4 Task 2 populates this harness")
        return 0
    results = [apply_and_check(m) for m in MUTATIONS]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
