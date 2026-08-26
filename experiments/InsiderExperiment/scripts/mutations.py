"""Apply five registered mutations to real source and show the right guard fails.

A guard that has never failed is a guard nobody has tested. Each mutation below
edits a real file, runs the test that is supposed to catch it, requires a
failure, restores the file byte for byte, and requires the suite to come back
green. Nothing here uses a fixture or a copy.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "src" / "insider"
PYTHON = REPO / ".venv" / "bin" / "python"


@dataclass(frozen=True, slots=True)
class Mutation:
    name: str
    intent: str
    path: Path
    old: str
    new: str
    guard: str


MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        name="power module returns a mean",
        intent="give the dispersion result a first moment of the return series",
        path=SRC / "power" / "dispersion.py",
        old="    book_width_mean: float\n    book_width_min: int",
        new="    mean_excess_return: float\n    book_width_mean: float\n    book_width_min: int",
        guard="tests/test_guards.py::test_the_power_dataclasses_carry_exactly_the_registered_fields "
        "tests/test_guards.py::test_no_name_in_the_power_package_says_first_moment_of_a_return",
    ),
    Mutation(
        name="non-evaluator module reads the sealed alpha table",
        intent="let insider.power open the store whose mean is the realized alpha",
        path=SRC / "power" / "dispersion.py",
        old="from insider.paths import DISPERSION_DB",
        new="from insider.paths import DISPERSION_DB, SEALED_DB",
        guard="tests/test_guards.py::test_only_the_permitted_set_names_the_sealed_store",
    ),
    Mutation(
        name="a sale is admitted past the purchases-only filter",
        intent="add transaction code S to the registered admitted codes",
        path=SRC / "config.py",
        old='    allowed_transaction_codes=("P",),',
        new='    allowed_transaction_codes=("P", "S"),',
        guard="tests/test_guards.py::test_purchases_only_a_sale_is_refused",
    ),
    Mutation(
        name="a routine insider is admitted past the three-year rule",
        intent="require four consecutive years, so a three-year routine insider reads "
        "as opportunistic and reaches the portfolio",
        path=SRC / "config.py",
        old="    routine_consecutive_years=3,",
        new="    routine_consecutive_years=4,",
        guard="tests/test_guards.py::test_a_routine_insider_is_refused_by_the_three_year_rule",
    ),
    Mutation(
        name="the EDGAR throttle loses its enforcement site",
        intent="hard-code the rate so sec_requests_per_second is read nowhere, "
        "while the throttle still behaves correctly",
        path=SRC / "edgar" / "throttle.py",
        old="        rate = cfg.sec_requests_per_second",
        new="        rate = 8.0  # was cfg.sec_requests_per_second",
        guard="tests/test_guards.py::test_every_config_field_has_an_enforcement_site",
    ),
)


def purge_bytecode() -> None:
    """Drop every cached .pyc before a run.

    CPython validates a cache entry on the source mtime in whole seconds and the
    source size. A mutation that changes one digit leaves both identical, so a
    restore inside the same second can leave the MUTATED bytecode valid and the
    harness reports a result from source that is no longer on disk. This is why
    the routine mutation first read as restored-still-red.
    """
    for cache in REPO.rglob("__pycache__"):
        if ".venv" not in cache.parts:
            shutil.rmtree(cache, ignore_errors=True)


def run(targets: str) -> tuple[int, str]:
    purge_bytecode()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run(
        [
            str(PYTHON),
            "-m",
            "pytest",
            "-q",
            "--no-header",
            "-p",
            "no:cacheprovider",
            *targets.split(),
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    return result.returncode, (result.stdout + result.stderr).strip()


def summary_line(output: str) -> str:
    for line in reversed(output.splitlines()):
        if "passed" in line or "failed" in line or "error" in line:
            return line.strip()
    return output.splitlines()[-1] if output else ""


def main() -> int:
    print(f"{len(MUTATIONS)} registered mutations, each applied to real source\n")
    results: list[dict[str, object]] = []
    failures = 0

    for i, mutation in enumerate(MUTATIONS, start=1):
        original = mutation.path.read_text(encoding="utf-8")
        if mutation.old not in original:
            print(f"{i}. {mutation.name}\n   SKIPPED, the anchor is not in {mutation.path.name}")
            failures += 1
            continue

        print(f"{i}. {mutation.name}")
        print(f"   intent: {mutation.intent}")
        print(f"   file:   {mutation.path.relative_to(REPO)}")

        caught = False
        detail = ""
        try:
            mutation.path.write_text(
                original.replace(mutation.old, mutation.new, 1), encoding="utf-8"
            )
            code, output = run(mutation.guard)
            caught = code != 0
            detail = summary_line(output)
            print(f"   mutated: {'GUARD FAILED as required' if caught else 'GUARD STAYED GREEN'}")
            print(f"            {detail}")
        finally:
            mutation.path.write_text(original, encoding="utf-8")

        assert mutation.path.read_text(encoding="utf-8") == original
        code, output = run(mutation.guard)
        restored = code == 0
        print(f"   restored: {'green' if restored else 'STILL RED'}")
        print(f"            {summary_line(output)}\n")

        if not (caught and restored):
            failures += 1
        results.append(
            {
                "mutation": mutation.name,
                "intent": mutation.intent,
                "file": str(mutation.path.relative_to(REPO)),
                "guard": mutation.guard,
                "guard_failed_when_mutated": caught,
                "guard_green_when_restored": restored,
                "mutated_summary": detail,
            }
        )

    print("running the full suite on the restored tree")
    code, output = run("tests/")
    print(f"  {summary_line(output)}")
    if code != 0:
        failures += 1

    out = REPO / "reports" / "stage_a1"
    out.mkdir(parents=True, exist_ok=True)
    (out / "mutations.json").write_text(
        json.dumps({"mutations": results, "final_suite": summary_line(output)}, indent=2),
        encoding="utf-8",
    )
    print(f"\n{len(MUTATIONS) - failures} of {len(MUTATIONS)} mutations behaved as registered")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
