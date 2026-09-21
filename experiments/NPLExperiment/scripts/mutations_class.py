"""Task 6 of H2 Amendment Stage 2: mutations on the Amendment H2-5 surface.

Each mutation edits real source, the suite must go red, the source is
restored byte-for-byte, and the suite must go green again. Bytecode is
purged before every run (the InsiderExperiment harness defect: CPython's
cache check can report results from source no longer on disk, and a harness
that can report on absent source is worse than no harness).

No mutation can touch a live verdict. **No H2 look has been read** — all
three H2 latches are absent, the pair reader has only ever seen synthetic
fixtures — and every mutation below is on machinery that has never seen an
outcome value.

The registered five (stage prompt, Task 6):

  MC1  admit a cross-complex elder at any tier
  MC2  let tier 3 accept an fx, rates, commodity, or vol leg
  MC3  read a post-entry funding row inside tiered selection
  MC4  write into the superseded h2_pairs.jsonl
  MC5  silently classify an unmapped ticker as equity instead of recording
       excluded_unclassifiable

Three more ride along because the amendment created their surface too:

  MC6  let a lower tier win over a higher one
  MC7  impute a missing tier on a ledger row instead of refusing
  MC8  drop the crypto dex rule so builder-dex crypto silently reclassifies
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "npl"
REPORT = ROOT / "reports" / "stage_a_h2" / "mutations_class.md"


@dataclass(frozen=True)
class Mutation:
    name: str
    path: Path
    old: str
    new: str
    catches: str


MUTATIONS = [
    Mutation(
        name="MC1: admit a cross-complex elder at any tier",
        path=SRC / "register" / "tiered.py",
        old="        return [c for c in candidates if c.asset_class == event_class]",
        new="        return list(candidates)",
        catches=(
            "tests/test_tiered.py — the tier-2 filter stops naming the class, so a "
            "commodity elder wins an equity leg on funding proximity, which is exactly "
            "the H2-3 defect this amendment exists to refuse"
        ),
    ),
    Mutation(
        name="MC2: let tier 3 accept an fx, rates, commodity, or vol leg",
        path=SRC / "register" / "tiered.py",
        old="        if not in_equity_complex(event_class):\n            return []",
        new="        if False:\n            return []",
        catches=(
            "tests/test_tiered.py — a rates leg would be rescued into the equity complex, "
            "and `para:10Y` would pair with an equity instead of being excluded"
        ),
    ),
    Mutation(
        name="MC3: read a post-entry funding row inside tiered selection",
        path=SRC / "controls.py",
        old="        mean = trailing_mean(candidate.rows, entry_ms, cfg)",
        new=(
            "        mean = trailing_mean(\n"
            "            tuple(r for r in candidate.rows if r.time_ms <= entry_ms), entry_ms, cfg\n"
            "        )"
        ),
        catches=(
            "tests/test_tiered.py — PostEntryRead is produced through the tiered path; "
            "silently dropping the offending row would let a rate from the event's own "
            "future reach the matcher without a refusal"
        ),
    ),
    Mutation(
        name="MC4: write into the superseded h2_pairs.jsonl",
        path=SRC / "register" / "tiered.py",
        old="    if resolved == H2_PAIRS_LEDGER.resolve():",
        new="    if False:",
        catches=(
            "tests/test_tiered.py — the superseded Amendment H2-3 assignment would become "
            "writable, and the record this stage promises to retain byte-identical could "
            "be appended to"
        ),
    ),
    Mutation(
        name="MC5: silently classify an unmapped ticker as equity",
        path=SRC / "register" / "assetclass.py",
        old="    return TICKER_CLASS.get(bare_ticker(coin))",
        new="    return TICKER_CLASS.get(bare_ticker(coin), CLASS_EQUITY)",
        catches=(
            "tests/test_assetclass.py — the six tickers whose refusal is the whole measured "
            "cost of the class test (QNT, BOT, SHAZ, LYTE, NCLD, ANSEM) would silently "
            "become equity, and `excluded_unclassifiable` would never be recorded"
        ),
    ),
    Mutation(
        name="MC6: let a lower tier win over a higher one",
        path=SRC / "register" / "tiered.py",
        old="    for tier in REGISTERED_TIERS:",
        new="    for tier in reversed(REGISTERED_TIERS):",
        catches=(
            "tests/test_tiered.py - tier order is the rule; reversing it makes the loosest "
            "tier win, so an exact-class same-dex elder loses to an equity-complex one"
        ),
    ),
    Mutation(
        name="MC7: impute a missing tier on a ledger row instead of refusing",
        path=SRC / "register" / "tiered.py",
        old='    tier = row.get("tier")',
        new='    tier = row.get("tier", TIER_SAME_DEX_EXACT_CLASS)',
        catches=(
            "tests/test_tiered.py — an absent tier would read as tier 1 rather than as the "
            "defect it is, which is the H2-3 `pair_type` imputation mistake repeated"
        ),
    ),
    Mutation(
        name="MC8: drop the crypto dex rule",
        path=SRC / "register" / "assetclass.py",
        old="    if dex in CRYPTO_DEXS:\n        return CLASS_CRYPTO",
        new="    if dex == 'hyna':\n        return CLASS_CRYPTO",
        catches=(
            "tests/test_assetclass.py — every main-dex instrument would fall through to the "
            "builder-dex table, where BTC and ETH are registered as "
            "`crypto_reference_on_builder_dex` and most crypto tickers appear at all"
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
        "# Amendment H2-5 mutation evidence",
        "",
        "Each mutation edits real source on the taxonomy and tiered-rule surface;",
        "the suite must go red; the source is restored byte-for-byte; the suite",
        "must go green. Bytecode is purged before every run. **No H2 look has been",
        "read** — all three H2 latches are absent and the pair reader has only ever",
        "seen synthetic fixtures — so no mutation could touch a live verdict.",
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
