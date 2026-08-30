"""A.1 TASK 3 (inference repair) — the stop-versus-close mix and the ambiguous rate.

**Both were assumptions until this ran, and Amendment 19 needs both.** The
pessimistic-minus-central shift that defines the amended E2's null is charged on
the entry leg and on **whichever exit leg the trade actually took**, so it cannot
be computed without the realized mix.

**It reads the same sealed post-holdout slice A.1 TASK 5 read** — sessions
strictly after 2026-06-30 under the two-sided carve-out of Amendment 11, boundary
enforced **per bar**. **It sends no request**: the bytes are already on disk,
sealed on 2026-08-29, and re-reading a stored file is not a vendor call.

**The exit mix is read off the bars, not off priced trades.** The frozen Section
6 model refuses every trade, its SEC Section 31 effective date being unmeasured;
reading the mix off priced trades would have made it **silently zero**, and a
zero stop share understates the pessimistic shift by 0.030 USD per share on every
trade.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import DATA, REPORTS, write_report

from orb.calendar import sessions
from orb.config import CONFIG
from orb.costs import Band
from orb.costs_registered import REGISTERED_COST_MODEL
from orb.dispersion import measure_carve_out_execution_mix
from orb.ledger import AppendOnlyLedger
from orb.redact import say

MANIFEST = REPORTS / "task5b_post_holdout_pull.json"
SEALED_ROOT = DATA / "sealed_credentialed"
OUT = Path(__file__).resolve().parent.parent / "reports" / "stage_a2repair"

MATERIAL_EXCLUSION_THRESHOLD = 0.10
"""Above this the registered ambiguous-session exclusion removes a non-trivial
part of the sample, and that is flagged for operator decision. **The exclusion
rule itself is not changed by this tool or by this pass.**"""

TRIGGER_RATE_ASSUMPTION = 0.55
STOP_SHARE_PRIOR_ESTIMATE = 0.381818
"""The A.1 TASK 5 figure, 210 stop exits of 550 **priced** trades. It was an
estimate of the mix rather than a measurement of it, because it was read off
trades the cost model had priced."""


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    tickers: list[str] = list(manifest["tickers"])
    files: dict[str, list[str]] = {}
    for entry in manifest["manifest"]:
        files.setdefault(str(entry["ticker"]), []).append(str(entry["stored_file"]))

    slice_sessions = list(
        sessions(
            date.fromisoformat(manifest["first_session"]),
            date.fromisoformat(manifest["last_closed_session"]),
        )
    )

    def load(ticker: str) -> list[bytes]:
        return [(SEALED_ROOT / name).read_bytes() for name in files.get(ticker, [])]

    say(
        f"measuring the execution mix over n = {len(slice_sessions)} post-holdout "
        f"sessions, {manifest['first_session']} .. {manifest['last_closed_session']}, "
        f"{len(tickers)} tickers"
    )
    mix = measure_carve_out_execution_mix(
        tickers,
        load,
        slice_sessions,
        REGISTERED_COST_MODEL,
        allow_short=True,
        band_from=Band.CENTRAL,
        band_to=Band.PESSIMISTIC,
    )
    long_only = measure_carve_out_execution_mix(
        tickers,
        load,
        slice_sessions,
        REGISTERED_COST_MODEL,
        allow_short=False,
        band_from=Band.CENTRAL,
        band_to=Band.PESSIMISTIC,
    )

    excluded_material = mix.ambiguous_rate > MATERIAL_EXCLUSION_THRESHOLD
    findings: dict[str, Any] = {
        "kind": "carve_out_execution_mix",
        "measured_at": date.today().isoformat(),
        "carve_out_half": "post_holdout",
        "carve_out_boundary_ms": CONFIG.post_holdout_start_ms,
        "first_session": manifest["first_session"],
        "last_closed_session": manifest["last_closed_session"],
        "sessions_pulled": manifest["session_count"],
        "requests_sent": 0,
        "requests_sent_note": (
            "the bytes were sealed on 2026-08-29; re-reading a stored file is "
            "not a vendor call"
        ),
        # --- the four scalars Amendment 20 names ---
        "stop_exit_share": mix.stop_exit_share,
        "ambiguous_rate": mix.ambiguous_rate,
        "mean_pessimistic_shift_usd_per_share": (
            mix.mean_pessimistic_shift_usd_per_share
        ),
        "sessions_used": mix.sessions_used,
        # --- the denominators standing rule 13 requires ---
        "name_sessions_evaluated": mix.name_sessions_evaluated,
        "name_sessions_ambiguous": mix.name_sessions_ambiguous,
        "name_sessions_triggered": mix.name_sessions_triggered,
        "trades_with_a_resolved_exit": mix.trades_with_a_resolved_exit,
        "stop_exits": mix.stop_exits,
        "close_exits": mix.close_exits,
        "trades_with_an_unresolved_exit": mix.trades_with_an_unresolved_exit,
        "bars_read": mix.bars_read,
        "tickers_with_bars": mix.tickers_with_bars,
        # --- measured against the assumption each replaces ---
        "stop_share_prior_estimate": STOP_SHARE_PRIOR_ESTIMATE,
        "stop_share_disagreement": mix.stop_exit_share - STOP_SHARE_PRIOR_ESTIMATE,
        "shift_at_the_prior_estimate": (
            REGISTERED_COST_MODEL.mean_slippage_shift_per_share(
                STOP_SHARE_PRIOR_ESTIMATE,
                band_from=Band.CENTRAL,
                band_to=Band.PESSIMISTIC,
            )
        ),
        "shift_bounds_usd_per_share": {
            "all_close_exits": REGISTERED_COST_MODEL.slippage_shift_per_share(
                __import__("orb.costs", fromlist=["Leg"]).Leg.CLOSE_EXIT,
                band_from=Band.CENTRAL,
                band_to=Band.PESSIMISTIC,
            ),
            "all_stop_exits": REGISTERED_COST_MODEL.slippage_shift_per_share(
                __import__("orb.costs", fromlist=["Leg"]).Leg.STOP_EXIT,
                band_from=Band.CENTRAL,
                band_to=Band.PESSIMISTIC,
            ),
        },
        "trigger_rate_assumption_falsified_at_a1_task5": TRIGGER_RATE_ASSUMPTION,
        # --- the Section 2 exclusion, and whether it is material ---
        "material_exclusion_threshold": MATERIAL_EXCLUSION_THRESHOLD,
        "ambiguous_exclusion_is_material": excluded_material,
        "ambiguous_exclusion_note": (
            "Section 2 excludes ambiguous sessions and this pass does NOT change "
            "that rule. The share is reported with its n so the operator can see "
            "how much of the sample the registered exclusion removes."
        ),
        "long_only_sensitivity": {
            "stop_exit_share": long_only.stop_exit_share,
            "ambiguous_rate": long_only.ambiguous_rate,
            "mean_pessimistic_shift_usd_per_share": (
                long_only.mean_pessimistic_shift_usd_per_share
            ),
            "name_sessions_triggered": long_only.name_sessions_triggered,
            "stop_exits": long_only.stop_exits,
            "close_exits": long_only.close_exits,
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "task3_execution_mix.json").write_text(
        json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8"
    )
    write_report("task3_execution_mix.json", findings)

    AppendOnlyLedger(DATA / "carve_out_reads.jsonl").append(
        {
            "kind": "carve_out_execution_mix",
            "half": "post_holdout",
            "sessions": manifest["sessions"],
            "sessions_used": mix.sessions_used,
            "stop_exit_share": mix.stop_exit_share,
            "ambiguous_rate": mix.ambiguous_rate,
            "mean_pessimistic_shift_usd_per_share": (
                mix.mean_pessimistic_shift_usd_per_share
            ),
        }
    )

    say("")
    say(
        f"STOP-EXIT SHARE   {mix.stop_exit_share:.6f}  "
        f"n = {mix.trades_with_a_resolved_exit} triggered trades with a resolved "
        f"exit ({mix.stop_exits} stop, {mix.close_exits} close), against a prior "
        f"estimate of {STOP_SHARE_PRIOR_ESTIMATE}"
    )
    say(
        f"AMBIGUOUS RATE    {mix.ambiguous_rate:.6f}  "
        f"n = {mix.name_sessions_evaluated} selected name-sessions "
        f"({mix.name_sessions_ambiguous} ambiguous)"
    )
    say(
        f"PESSIMISTIC SHIFT {mix.mean_pessimistic_shift_usd_per_share:.6f} USD/share "
        f"(bounds 0.030 all-close, 0.060 all-stop)"
    )
    say(f"SESSIONS USED     {mix.sessions_used}")
    if excluded_material:
        say(
            "FLAG: the registered ambiguous-session exclusion removes MORE than "
            f"{MATERIAL_EXCLUSION_THRESHOLD:.0%} of the sample. Recorded as a "
            "candidate scope limitation for operator decision. The exclusion "
            "rule is NOT changed."
        )
    else:
        say(
            "The registered ambiguous-session exclusion removes at most "
            f"{MATERIAL_EXCLUSION_THRESHOLD:.0%} of the sample; no scope "
            "limitation is raised on it."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
