"""A.4 TASK 2 — the mutation harness.

Each mutation is applied to **real source**, the suite is run, the mutation must
be **caught**, and the source is **restored green**. **Bytecode is purged before
every run**: a harness that can report on absent source is worse than no
harness, because it reports success from a stale `.pyc`.

Two mutations are of a different kind and are marked `expect_green`: they
demonstrate a guard **failing to bind** rather than firing. Mutation 4 moves a
boundary fixture off the registered boundary *and* moves the threshold with it,
and the suite goes green — which is the InsiderExperiment lesson made visible.
Mutation 1 deletes the blindness pin and shows a priced-bar read becoming
reachable with the suite still green.

**Mutation 13 was a third, and is no longer.** It was written at A.0 TASK 1
against the post-holdout edge of Amendment 11, and it **went green** — the edge
had exactly one pin, in `tests/test_preperiod.py`, and disabling it left nothing
behind. A.1 TASK 5 then added `orb.dispersion`, whose own boundary fixture sits
on the **same instant** and is not among the tests mutation 13 disables. **The
harness reported a failure on the next run, and the failure was the harness
being right**: the mutation's premise had stopped being true. It is now marked
`expect_green=False` and it is **caught**. Nothing about the mutation changed;
what changed is that the boundary is pinned twice.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = ROOT / ".venv" / "bin" / "python"


@dataclass(frozen=True, slots=True)
class Mutation:
    number: int
    name: str
    lesson: str
    edits: tuple[tuple[str, str, str], ...]  # (relative path, find, replace)
    expect_green: bool = False
    """True when the point is that the guard **stops** binding."""


MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        1,
        "delete the blindness pin",
        "with the pin deleted a priced-bar read is reachable and nothing complains",
        (
            (
                "tests/test_guards.py",
                "    assert not violations, (",
                "    violations = []  # MUTATION 1\n    assert not violations, (",
            ),
            (
                "src/orb/calendar.py",
                "def session_counts(",
                "def _leak(bar: dict[str, float]) -> float:\n"
                '    return bar["close"] + bar["volume"]  # MUTATION 1\n\n\n'
                "def session_counts(",
            ),
        ),
        expect_green=True,
    ),
    Mutation(
        2,
        "coerce a recorded absence to zero",
        "a missing bar becomes a measured zero and every coverage figure inflates",
        (
            (
                "src/orb/absence.py",
                '    def __float__(self) -> Never:\n        self._refuse("float()")',
                "    def __float__(self) -> float:  # MUTATION 2\n        return 0.0",
            ),
        ),
    ),
    Mutation(
        3,
        "merge rate_limited into no_data",
        "a vendor refusal is counted as an empty session and the denominator inflates",
        (
            (
                "src/orb/callstate.py",
                '    RATE_LIMITED = "rate_limited"',
                '    RATE_LIMITED = "no_data"  # MUTATION 3',
            ),
        ),
    ),
    Mutation(
        4,
        "move a boundary fixture off the registered 09:35:00.000 boundary",
        "a fixture inside its boundary lets a moved threshold pass unnoticed",
        (
            (
                "tests/test_preperiod.py",
                "ONE_MS_BEFORE = BOUNDARY_MS - 1",
                "ONE_MS_BEFORE = BOUNDARY_MS - 86_400_000  # MUTATION 4",
            ),
            (
                "tests/test_preperiod.py",
                "def test_the_boundary_instant_itself_is_refused() -> None:",
                "def _disabled_boundary_instant() -> None:  # MUTATION 4",
            ),
            (
                "tests/test_preperiod.py",
                "def test_one_millisecond_after_the_boundary_is_refused() -> None:",
                "def _disabled_after_boundary() -> None:  # MUTATION 4",
            ),
            (
                "tests/test_preperiod.py",
                "def test_the_gate_returns_a_recorded_absence_at_the_boundary() -> None:",
                "def _disabled_gate_at_boundary() -> None:  # MUTATION 4",
            ),
            (
                "tests/test_preperiod.py",
                "def test_the_gate_refuses_after_the_boundary() -> None:",
                "def _disabled_gate_after() -> None:  # MUTATION 4",
            ),
            (
                "tests/test_preperiod.py",
                "def test_the_sealed_window_between_the_two_edges_is_refused_throughout"
                "() -> None:",
                "def _disabled_sealed_window_sweep() -> None:  # MUTATION 4",
            ),
            (
                "tests/test_dark.py",
                "def test_a_pre_period_bar_must_actually_be_pre_period() -> None:",
                "def _disabled_bar_provenance_boundary() -> None:  # MUTATION 4",
            ),
            (
                "tests/test_known_answers.py",
                "        assert b.timestamp_ms < CONFIG.pre_period_end_ms",
                "        pass  # MUTATION 4",
            ),
            (
                "src/orb/preperiod.py",
                "    return timestamp_ms < CONFIG.pre_period_end_ms",
                "    return timestamp_ms < CONFIG.pre_period_end_ms + 86_400_000"
                "  # MUTATION 4",
            ),
        ),
        expect_green=True,
    ),
    Mutation(
        5,
        "replace the DST-aware Eastern anchor with a fixed UTC offset",
        "the opening range is taken from the wrong five minutes on a third of the sample",
        (
            (
                "src/orb/sessionclock.py",
                'EASTERN: Final[ZoneInfo] = ZoneInfo("America/New_York")',
                "EASTERN: Final[timezone] = timezone(timedelta(hours=-5))"
                "  # type: ignore[assignment]  # MUTATION 5",
            ),
        ),
    ),
    Mutation(
        6,
        "read a bar stamped on or after 2016-01-04 through the carve-out",
        "a verdict-window observation leaks into the power computation that plans the verdict",
        (
            (
                "src/orb/preperiod.py",
                "    if not is_carve_out(timestamp_ms):",
                "    if False:  # MUTATION 6",
            ),
        ),
    ),
    Mutation(
        7,
        "make the sealed comparator return a bar value to a caller",
        "the single blindness exception becomes a hole; price leaves the seal",
        (
            (
                "src/orb/comparator.py",
                "    def compare_vendors(",
                "    def leak_a_bar_value(self, bar: dict[str, object]) -> int | None:"
                "  # MUTATION 7\n"
                "        return _ohlc_cents(bar)[1]\n\n"
                "    def compare_vendors(",
            ),
        ),
    ),
    Mutation(
        8,
        "point the verdict module at real bars before the latch",
        "the dark strategy becomes reachable from a Stage A collection path",
        (
            (
                "src/orb/collector.py",
                "from orb.ledger import AppendOnlyLedger",
                "from orb.ledger import AppendOnlyLedger\n"
                "from orb.verdict import fire_verdict  # MUTATION 8\n"
                "from orb.bars import Bar  # MUTATION 8",
            ),
        ),
    ),
    Mutation(
        9,
        "let a manifest seal attest the open session",
        "the seal describes a partial file and teaches readers to expect mismatches",
        (
            (
                "src/orb/collector.py",
                "    if session >= now.date():",
                "    if False:  # MUTATION 9",
            ),
        ),
    ),
    Mutation(
        10,
        "allow a second read of a spent window",
        "the hypothesis is voided and nothing says so",
        (
            (
                "src/orb/latch.py",
                "    if target.exists():",
                "    if False:  # MUTATION 10",
            ),
        ),
    ),
    Mutation(
        11,
        "remove the secret redactor",
        "a credential value reaches a sealed file, a ledger row and the console",
        (
            (
                "src/orb/redact.py",
                '        """Redact a string bound for a log, a report, a message or the console."""\n        out = value',
                '        """Redact a string bound for a log, a report, a message or the console."""\n        return value  # MUTATION 11\n        out = value',
            ),
            (
                "src/orb/redact.py",
                '        """Redact raw bytes bound for a sealed file. Deterministic."""\n        out = value',
                '        """Redact raw bytes bound for a sealed file. Deterministic."""\n        return value  # MUTATION 11\n        out = value',
            ),
        ),
    ),
    Mutation(
        12,
        "force the tape verdict to SAME_TAPE",
        "a single-venue feed is scored against the registered agreement bars and "
        "BLOCKED-4 fires on entitlement while recording it as integrity",
        (
            (
                "src/orb/integrity.py",
                '        """SAME_TAPE inside [0.90, 1.10]; DIFFERENT_TAPE below 0.50; else AMBIGUOUS."""\n        if (',
                '        """SAME_TAPE inside [0.90, 1.10]; DIFFERENT_TAPE below 0.50; else AMBIGUOUS."""\n        return TapeVerdict.SAME_TAPE  # MUTATION 12\n        if (',
            ),
        ),
    ),
    Mutation(
        13,
        "move the post-holdout boundary fixture off its registered edge",
        "when this was written the edge had ONE pin and the suite went green — "
        "the InsiderExperiment lesson. A.1 TASK 5 added a second, independent "
        "fixture at the same instant inside the carve-out writer, and the "
        "harness now CATCHES it. The mutation is unchanged; what changed is "
        "that the boundary is pinned twice",
        (
            (
                "tests/test_preperiod.py",
                "LAST_MS_OF_HOLDOUT = POST_MS - 1",
                "LAST_MS_OF_HOLDOUT = POST_MS - 172_800_000  # MUTATION 13",
            ),
            (
                "tests/test_preperiod.py",
                "def test_the_post_holdout_boundary_is_eastern_midnight_not_utc_"
                "midnight() -> None:",
                "def _disabled_eastern_midnight() -> None:  # MUTATION 13",
            ),
            (
                "tests/test_preperiod.py",
                "def test_the_sealed_window_between_the_two_edges_is_refused_"
                "throughout() -> None:",
                "def _disabled_sealed_window_sweep_13() -> None:  # MUTATION 13",
            ),
            (
                "src/orb/preperiod.py",
                "    return timestamp_ms >= CONFIG.post_holdout_start_ms",
                "    return timestamp_ms >= CONFIG.post_holdout_start_ms "
                "- 86_400_000  # MUTATION 13",
            ),
        ),
    ),
    Mutation(
        14,
        "flip the configured tape to the single-venue feed",
        "every bar is real and every one is wrong about the market: a median "
        "0.027761 of consolidated first-5-minute volume, invisible downstream",
        (
            (
                "src/orb/config.py",
                '    consolidated_feed="sip",',
                '    consolidated_feed="iex",  # MUTATION 14',
            ),
        ),
    ),
    Mutation(
        15,
        "make the carve-out dispersion writer return a trade list",
        "the two-scalar contract becomes a hole and a per-trade series — the "
        "outcome itself — leaves a sealed writer before the Stage C latch",
        (
            (
                "src/orb/dispersion.py",
                "def measure_carve_out_dispersion(",
                "def leak_the_trades(values: list[float]) -> list[float]:"
                "  # MUTATION 15\n"
                "    return list(values)\n\n\n"
                "def measure_carve_out_dispersion(",
            ),
        ),
    ),
)


def purge_bytecode() -> None:
    """A harness that can report on absent source is worse than no harness."""
    for cache in ROOT.rglob("__pycache__"):
        if ".venv" in cache.parts:
            continue
        shutil.rmtree(cache, ignore_errors=True)


def run_suite() -> tuple[bool, str]:
    purge_bytecode()
    result = subprocess.run(
        [str(PY), "-m", "pytest", "-q", "-x", "--no-header", "-p", "no:cacheprovider"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0, (result.stdout + result.stderr)


def apply(mutation: Mutation) -> dict[str, str]:
    originals: dict[str, str] = {}
    for rel, find, replace in mutation.edits:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if rel not in originals:
            originals[rel] = text
        if find not in text:
            raise SystemExit(f"mutation {mutation.number}: anchor not found in {rel}")
        path.write_text(text.replace(find, replace, 1), encoding="utf-8")
    return originals


def restore(originals: dict[str, str]) -> None:
    for rel, text in originals.items():
        (ROOT / rel).write_text(text, encoding="utf-8")
    purge_bytecode()


def main() -> int:
    green, _ = run_suite()
    if not green:
        print("baseline suite is RED; refusing to mutate a broken tree")
        return 1
    print(f"baseline GREEN, n = {len(MUTATIONS)} mutations\n")

    lines: list[str] = []
    failures = 0
    for mutation in MUTATIONS:
        originals = apply(mutation)
        try:
            suite_green, output = run_suite()
        finally:
            restore(originals)

        caught = (not suite_green) if not mutation.expect_green else suite_green
        verdict = "CAUGHT" if not mutation.expect_green else "GUARD STOPPED BINDING"
        status = "PASS" if caught else "**HARNESS FAILURE**"
        if not caught:
            failures += 1

        summary = ""
        for line in output.splitlines():
            if line.startswith("FAILED") or " failed" in line or " passed" in line:
                summary = line.strip()
        print(f"  {mutation.number:>2}. {mutation.name:<58} {status:<20} {summary}")

        restored_green, _ = run_suite()
        if not restored_green:
            print(
                f"      !! source did not restore green after mutation "
                f"{mutation.number}"
            )
            failures += 1

        lines.append(
            f"| {mutation.number} | {mutation.name} | {mutation.lesson} | "
            f"{verdict} | {'yes' if caught else '**NO**'} | `{summary}` |"
        )

    report = ROOT / "reports" / "stage_a4" / "mutations.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "# A.4 TASK 2 — the mutation harness\n\n"
        f"**Run 2026-08-29. n = {len(MUTATIONS)} mutations applied to real source, "
        "each restored green afterwards. Bytecode is purged before every run.**\n\n"
        "Two mutations are of a different kind and are marked *GUARD STOPPED "
        "BINDING*: the point is to show a guard **failing to catch** something, "
        "which is how a boundary fixture placed comfortably inside its boundary "
        "goes unnoticed.\n\n"
        "| # | mutation | what it would have cost | expected | detected | suite |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    print(f"\nwrote {report}")
    print(f"harness failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
