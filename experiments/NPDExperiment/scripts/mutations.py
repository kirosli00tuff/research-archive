"""Apply five mutations to real source, prove each fails the right test, restore.

A guard that has never been seen to fail is a guard nobody has tested. Each
mutation below is applied to the actual module, not to a copy, and the harness
restores the exact original bytes afterwards whether the run passes or not.

    python scripts/mutations.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv" / "bin" / "python"


@dataclass(frozen=True)
class Mutation:
    name: str
    describes: str
    target: Path
    find: str
    replace: str
    must_fail: str
    also_touch: tuple[tuple[Path, str, str], ...] = ()


MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        name="1. carry a value forward across a missing bar",
        describes=(
            "Fill a hole in a feature span with the previous close, which is the "
            "exact shape of the seven historical fabrications."
        ),
        target=ROOT / "src/npd/data/features.py",
        find="""    out: list[float] = []
    for i in range(start, t + 1):
        v = values[i]
        if v is None:
            return NO_BAR""",
        replace="""    out: list[float] = []
    for i in range(start, t + 1):
        v = values[i]
        if v is None:
            v = out[-1] if out else 1.0""",
        must_fail="tests/test_absence.py",
    ),
    Mutation(
        name="2. merge model_failed into source_failed",
        describes=(
            "Collapse operational health into a data fault, destroying the "
            "distinction between a model that could not answer and a source that "
            "could not serve."
        ),
        target=ROOT / "src/npd/callstate.py",
        find='    MODEL_FAILED = "model_failed"',
        replace='    MODEL_FAILED = "source_failed"',
        must_fail="tests/test_guards.py",
    ),
    Mutation(
        name="3. let a non-evaluator module read the sealed forward returns",
        describes="Give the collector a peek at the outcomes it is collecting against.",
        target=ROOT / "src/npd/collect/collector.py",
        find="def utc_now() -> str:",
        replace='''def peek_at_outcomes(date: str) -> list[tuple[str, float]]:
    """A module other than the evaluator reading the sealed store."""
    import sqlite3 as _s

    from npd.paths import SEALED_DB

    con = _s.connect(f"file:{SEALED_DB}?mode=ro", uri=True)
    try:
        return [
            (r[0], float(r[1]))
            for r in con.execute(
                "SELECT symbol, ret FROM forward_return WHERE date = ?", (date,)
            )
        ]
    finally:
        con.close()


def utc_now() -> str:''',
        must_fail="tests/test_guards.py",
    ),
    Mutation(
        name="4. add a config field with no enforcement site",
        describes="A knob that reads as registered and is enforced nowhere.",
        target=ROOT / "src/npd/config.py",
        find="    universe_id: str",
        replace="    decorative_knob: float\n    universe_id: str",
        must_fail="tests/test_guards.py",
        also_touch=(
            (
                ROOT / "src/npd/config.py",
                '    universe_id="U-LIQ-500-stk-w60-m40-p5",',
                '    decorative_knob=0.42,\n    universe_id="U-LIQ-500-stk-w60-m40-p5",',
            ),
        ),
    ),
    Mutation(
        name="5. let a real ticker reach a prompt",
        describes="Label each row with its own symbol, defeating anonymization.",
        target=ROOT / "src/npd/data/anonymize.py",
        find="    labels = rng.sample(pool, len(symbols))",
        replace="    labels = list(symbols)",
        must_fail="tests/test_anonymization.py",
    ),
)


def run_tests(target: str | None = None) -> tuple[bool, str]:
    cmd = [str(PY), "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"]
    if target:
        cmd.append(target)
    else:
        cmd.append("tests/")
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    tail = (proc.stdout + proc.stderr).strip().splitlines()
    return proc.returncode == 0, "\n".join(tail[-6:])


def main() -> int:
    results = []
    ok, summary = run_tests()
    if not ok:
        print("the suite is not green before any mutation. Stopping.")
        print(summary)
        return 1
    print(f"baseline green: {summary.splitlines()[-1]}\n")

    for m in MUTATIONS:
        files = {m.target: m.target.read_text(encoding="utf-8")}
        for path, _f, _r in m.also_touch:
            files.setdefault(path, path.read_text(encoding="utf-8"))
        try:
            text = files[m.target]
            if m.find not in text:
                raise RuntimeError(f"mutation anchor not found in {m.target}")
            m.target.write_text(text.replace(m.find, m.replace, 1), encoding="utf-8")
            for path, find, replace in m.also_touch:
                cur = path.read_text(encoding="utf-8")
                if find not in cur:
                    raise RuntimeError(f"secondary anchor not found in {path}")
                path.write_text(cur.replace(find, replace, 1), encoding="utf-8")

            failed_ok, detail = run_tests(m.must_fail)
            caught = not failed_ok
        finally:
            for path, original in files.items():
                path.write_text(original, encoding="utf-8")

        restored_ok, restored_detail = run_tests()
        results.append(
            {
                "mutation": m.name,
                "describes": m.describes,
                "target": str(m.target.relative_to(ROOT)),
                "guard": m.must_fail,
                "guard_failed_as_required": caught,
                "guard_output": detail,
                "restored_green": restored_ok,
            }
        )
        mark = "CAUGHT" if caught else "MISSED"
        print(f"{mark}  {m.name}")
        print(f"        guard {m.must_fail} -> {'failed' if caught else 'PASSED, which is wrong'}")
        print(f"        restored green: {restored_ok}")
        if not restored_ok:
            print(restored_detail)
        print()

    every = all(r["guard_failed_as_required"] and r["restored_green"] for r in results)
    _write_report(results, every)
    print(f"all five caught and restored: {every}")
    return 0 if every else 1


def _write_report(results: list[dict[str, object]], every: bool) -> None:
    out = ROOT / "reports" / "mutations.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Mutation results",
        "",
        "Each mutation was applied to real source, not to a copy. The harness "
        "restores the exact original bytes whether the run passes or fails, and "
        "reruns the full suite afterwards to prove the restore worked.",
        "",
        "| mutation | target | guard | caught | restored green |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| {r['mutation']} | `{r['target']}` | `{r['guard']}` | "
            f"{'yes' if r['guard_failed_as_required'] else 'NO'} | "
            f"{'yes' if r['restored_green'] else 'NO'} |"
        )
    lines += ["", f"**All five caught and restored: {every}**", ""]
    for r in results:
        lines += [
            f"## {r['mutation']}",
            "",
            str(r["describes"]),
            "",
            f"Target `{r['target']}`. Guard `{r['guard']}`.",
            "",
            "```",
            str(r["guard_output"]),
            "```",
            "",
        ]
    out.write_text("\n".join(lines), encoding="utf-8")
    (ROOT / "reports" / "mutations.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    sys.exit(main())
