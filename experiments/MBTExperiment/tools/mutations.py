#!/usr/bin/env python3
"""Apply five registered mutations to real source and show the right guard fails.

**A guard that has never failed is a guard nobody has tested.** Each mutation
below edits a **real file**, runs the check that is supposed to catch it,
requires a failure, restores the file **byte for byte**, and requires the check
to come back green. Nothing here uses a fixture or a copy.

**Python bytecode is purged before every run.** CPython validates a cache entry
on the source mtime in WHOLE SECONDS and the source size. A mutation that changes
one token can leave both identical, so a restore inside the same second can leave
the MUTATED bytecode valid and the harness reports a result from source that is
no longer on disk. That is not hypothetical: it is why a predecessor's restore
once read as still-red. A mutation harness that reports results from source no
longer on disk is worse than no harness.

**Two things are demonstrated, and they are different.** The refusal artifacts in
``reports/guards/refusals.json`` show each guard **refusing when exercised**. The
artifact this tool writes shows that the **test detects the guard being
disabled**. A guard can refuse correctly while its test asserts nothing, and only
the second check catches that.

Ported by copying from solcopy's mutation harness.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "src" / "mbt"
PYTHON = REPO / ".venv" / "bin" / "python"
REPORTS = REPO / "reports" / "mutations"


@dataclass(frozen=True, slots=True)
class Mutation:
    """One registered mutation, the defect it imitates, and the check that catches it."""

    name: str
    intent: str
    defect: str
    path: Path
    old: str
    new: str
    check: str
    check_kind: str


MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        name="a whatIf literal is flipped to False",
        intent="turn the only order construction in the package into a transmitting one",
        defect=(
            "this repository transmits no order, ever. The flag that makes every broker "
            "interaction a preview is a single literal, and flipping it is the smallest "
            "possible edit that would change what the package does at a venue"
        ),
        path=SRC / "broker.py",
        old="        whatIf=True,\n        transmit=False,",
        new="        whatIf=False,\n        transmit=False,",
        check="no_transmit_scan",
        check_kind="build",
    ),
    Mutation(
        name="the whatIf flag is supplied from an expression rather than a literal",
        intent="keep the run-time value True while removing the build-time guarantee",
        defect=(
            "bool(1) evaluates to True, so the package still behaves correctly and every "
            "run-time check still passes. What is lost is the STATIC guarantee: a value "
            "that is not a literal cannot be verified at build time, and the next edit to "
            "whatever supplies it is unreviewed. This is the sharpest of the five, because "
            "nothing observable changes"
        ),
        path=SRC / "broker.py",
        old="        whatIf=True,\n        transmit=False,",
        new="        whatIf=bool(1),\n        transmit=False,",
        check="no_transmit_scan",
        check_kind="build",
    ),
    Mutation(
        name="a session trusts its declared environment instead of the connected account",
        intent="let configuration state the environment rather than the connection",
        defect=(
            "config states an INTENT and the connection states a FACT, and the fact wins. "
            "This mutation makes the declaration self-certifying, so a session declaring "
            "live while connected to a D-prefixed paper account would record its figures "
            "as live. Every downstream provenance tag would be a copy of a wish"
        ),
        path=SRC / "provenance.py",
        old="        measured = environment_from_account(connected_account)",
        new="        measured = declared",
        check="tests/test_guards.py",
        check_kind="test",
    ),
    Mutation(
        name="a paper margin becomes admissible to a gate",
        intent="drop MARGIN from the kinds that require a live environment",
        defect=(
            "a paper margin read is development evidence. Promoting one into a verdict is "
            "the single failure the paper-only clause exists to prevent, and after this "
            "edit the MARGIN gate would happily fire on a simulated account's number"
        ),
        path=SRC / "gates.py",
        old="_LIVE_ONLY_KINDS = frozenset({ProvenanceKind.MARGIN, ProvenanceKind.COMMISSION_REPORT})",
        new="_LIVE_ONLY_KINDS = frozenset({ProvenanceKind.COMMISSION_REPORT})",
        check="tests/test_guards.py",
        check_kind="test",
    ),
    Mutation(
        name="the deciding latch's spent check is inverted",
        intent="invert the condition that makes one spend per registered figure",
        defect=(
            "the latch exists so a deciding read happens once. An inverted condition is a "
            "classic single-token defect and it breaks the guard in both directions: the "
            "first spend raises when it should succeed, and a second would succeed when it "
            "should raise LatchAlreadySpentError"
        ),
        path=SRC / "latch.py",
        old="        if path.exists():",
        new="        if not path.exists():",
        check="tests/test_guards.py",
        check_kind="test",
    ),
)


def purge_bytecode() -> int:
    """Drop every cached .pyc before a run. Returns how many caches were removed."""
    removed = 0
    for cache in REPO.rglob("__pycache__"):
        if ".venv" in cache.parts:
            continue
        shutil.rmtree(cache, ignore_errors=True)
        removed += 1
    return removed


def run_check(mutation: Mutation) -> tuple[int, str, int]:
    """Run one check with bytecode purged and bytecode writing disabled."""
    purged = purge_bytecode()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    if mutation.check_kind == "build":
        command = [str(PYTHON), str(REPO / "tools" / "no_transmit_scan.py")]
    else:
        command = [
            str(PYTHON),
            "-m",
            "pytest",
            "-q",
            "--no-header",
            "-p",
            "no:cacheprovider",
            mutation.check,
        ]
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, check=False, env=env)
    return result.returncode, (result.stdout + result.stderr).strip(), purged


def summary_line(output: str) -> str:
    """The last line that reads like a result, or the last line at all."""
    for line in reversed(output.splitlines()):
        stripped = line.strip()
        if any(word in stripped for word in ("passed", "failed", "error", "CLEAN", "FAILED")):
            return stripped
    return output.splitlines()[-1].strip() if output else ""


def fired_checks(output: str) -> list[str]:
    """Every test id or scan rule that fired, so the artifact names them all.

    A mutation that trips three guards is stronger evidence than one that trips
    one, and a harness that prints only the last line cannot tell them apart.
    """
    fired = {
        line.split(" ")[1].split(" - ")[0]
        for line in output.splitlines()
        if line.startswith("FAILED ")
    }
    fired |= {
        part.split("]")[0]
        for line in output.splitlines()
        for part in line.split("[")[1:]
        if "]" in part and part.split("]")[0].islower() and "_" in part.split("]")[0]
    }
    return sorted(fired)


def main() -> int:
    print(f"{len(MUTATIONS)} registered mutations, each applied to real source\n")
    results: list[dict[str, Any]] = []
    failures = 0

    for index, mutation in enumerate(MUTATIONS, start=1):
        original = mutation.path.read_text(encoding="utf-8")
        relative = mutation.path.relative_to(REPO)
        print(f"{index}. {mutation.name}")
        print(f"   intent: {mutation.intent}")
        print(f"   file:   {relative}")
        print(f"   check:  {mutation.check}")

        if mutation.old not in original:
            print(f"   SKIPPED: the anchor is not present in {relative}\n")
            failures += 1
            results.append(
                {
                    "mutation": mutation.name,
                    "file": str(relative),
                    "check": mutation.check,
                    "anchor_found": False,
                    "check_failed_when_mutated": False,
                    "check_green_when_restored": False,
                }
            )
            continue

        caught = False
        mutated_summary = ""
        fired: list[str] = []
        try:
            mutation.path.write_text(
                original.replace(mutation.old, mutation.new, 1), encoding="utf-8"
            )
            code, output, purged = run_check(mutation)
            caught = code != 0
            mutated_summary = summary_line(output)
            fired = fired_checks(output)
            state = "CHECK FAILED as required" if caught else "CHECK STAYED GREEN"
            print(f"   mutated:  {state} ({purged} bytecode caches purged first)")
            print(f"             {mutated_summary}")
            for name in fired:
                print(f"             fired: {name}")
        finally:
            mutation.path.write_text(original, encoding="utf-8")

        restored_text = mutation.path.read_text(encoding="utf-8")
        byte_exact = restored_text == original
        if not byte_exact:
            raise AssertionError(f"restore of {relative} was not byte-exact")

        code, output, purged = run_check(mutation)
        restored = code == 0
        restored_summary = summary_line(output)
        print(f"   restored: {'green' if restored else 'STILL RED'} ({purged} caches purged)")
        print(f"             {restored_summary}\n")

        if not (caught and restored):
            failures += 1
        results.append(
            {
                "mutation": mutation.name,
                "intent": mutation.intent,
                "defect_it_imitates": mutation.defect,
                "file": str(relative),
                "check": mutation.check,
                "check_kind": mutation.check_kind,
                "anchor_found": True,
                "check_failed_when_mutated": caught,
                "check_green_when_restored": restored,
                "restore_was_byte_exact": byte_exact,
                "mutated_summary": mutated_summary,
                "checks_that_fired": fired,
                "restored_summary": restored_summary,
            }
        )

    print("running the whole suite on the restored tree")
    purge_bytecode()
    whole_result = subprocess.run(
        [str(PYTHON), "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    whole = summary_line((whole_result.stdout + whole_result.stderr).strip())
    print(f"  {whole}")
    if whole_result.returncode != 0:
        failures += 1

    payload = {
        "stage": "B",
        "at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": (
            "Every refusal here is DEMONSTRATED as a produced artifact, never asserted. "
            "Python bytecode is purged before every run, because a same-byte-length "
            "restore once left mutated bytecode valid under CPython's mtime-and-size "
            "cache check and the harness reported a restore as still red."
        ),
        "what_this_shows": (
            "reports/guards/refusals.json shows each guard REFUSING when exercised. This "
            "artifact shows each TEST DETECTING the guard being disabled. A guard can "
            "refuse correctly while its test asserts nothing, and only this catches that."
        ),
        "mutations": [asdict(m) | {"path": str(m.path.relative_to(REPO))} for m in MUTATIONS],
        "results": results,
        "whole_suite_after_restore": whole,
        "failures": failures,
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "mutations.json").write_text(
        json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8"
    )
    print(f"\nwrote {(REPORTS / 'mutations.json').relative_to(REPO)}")
    if failures:
        print(f"{failures} mutation(s) did not behave as registered")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
