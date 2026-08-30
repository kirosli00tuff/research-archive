"""A.3 TASK 4 — Change B. The H1b price-floor feasibility scan.

**H1b is `REGISTERED_NOT_OPEN`** (Amendment 25). This tool computes **no
verdict, no power figure and no chosen floor**. It produces a table and hands it
to the operator.

**Carve-out data only** — post-holdout sessions strictly after 2026-06-30, under
the Amendment 11 two-sided carve-out, boundary enforced per bar. **No request is
sent**: the bytes were sealed on 2026-08-29.

**The raised floor is applied on top of the registered Section 2 filter**, never
instead of it, so every scanned universe is a **strict subset** of the registered
one and no registered rule is changed.

**Amendment 24 §6, registered before this ran: whatever this shows, it is
feasibility evidence for a new hypothesis and never a continuation of H1.**
"""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import DATA, REPORTS

from orb.config import CONFIG
from orb.costs import SecFeeSchedule
from orb.costs_registered import REGISTERED_COST_MODEL, SEC_RATE_MEASURED
from orb.dispersion import measure_carve_out_floor_scan
from orb.redact import say

MANIFEST = REPORTS / "task5b_post_holdout_pull.json"
SEALED_ROOT = DATA / "sealed_credentialed"
OUT = Path(__file__).resolve().parent.parent / "reports" / "stage_a3rescue"
FLOORS = (5.0, 10.0, 20.0, 50.0, 100.0)
EQUITY_USD = 100_000.0


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    tickers: list[str] = list(manifest["tickers"])
    files: dict[str, list[str]] = {}
    for entry in manifest["manifest"]:
        files.setdefault(str(entry["ticker"]), []).append(str(entry["stored_file"]))

    from orb.calendar import sessions

    slice_sessions = list(
        sessions(
            date.fromisoformat(manifest["first_session"]),
            date.fromisoformat(manifest["last_closed_session"]),
        )
    )

    def load(ticker: str) -> list[bytes]:
        return [(SEALED_ROOT / name).read_bytes() for name in files.get(ticker, [])]

    # The frozen Section 6 model prices nothing, its SEC Section 31 effective
    # date being unmeasured. The scan uses the Amendment 15 bracket at the one
    # MEASURED rate, exactly as the dispersion measurement did, so the figures
    # are comparable across passes.
    model = replace(
        REGISTERED_COST_MODEL,
        sec_fees=SecFeeSchedule(
            effective_dates=(date(2026, 1, 1),),
            rates_per_dollar=(SEC_RATE_MEASURED,),
        ),
    )

    say(
        f"scanning price floors {FLOORS} over n = {len(slice_sessions)} "
        f"post-holdout sessions, {len(tickers)} tickers"
    )
    rows = measure_carve_out_floor_scan(
        tickers,
        load,
        slice_sessions,
        model,
        FLOORS,
        CONFIG.registered_sharpe_assumption,
        allow_short=True,
        equity_usd=EQUITY_USD,
    )

    table: list[dict[str, Any]] = []
    for row in rows:
        fillable = (
            row.sessions_with_a_full_selection == row.sessions_evaluated
            and row.sessions_evaluated > 0
        )
        table.append(
            {
                "price_floor_usd": row.price_floor_usd,
                "eligible_name_sessions": row.eligible_name_sessions,
                "selected_name_sessions": row.selected_name_sessions,
                "sessions_evaluated": row.sessions_evaluated,
                "sessions_with_a_full_top20_selection": (
                    row.sessions_with_a_full_selection
                ),
                "top20_still_fillable_on_every_session": fillable,
                "mean_relative_volume_of_selection": (
                    row.mean_relative_volume_of_selection
                ),
                "dispersion_usd_per_share": row.dispersion_usd_per_share,
                "entry_overshoot_median_usd_per_share": row.entry_overshoot_median,
                "central_mean_usd_per_share_at_1_40": row.central_mean_usd_per_share,
                "shift_usd_per_share": row.shift_usd_per_share,
                "central_mean_to_shift_ratio": row.central_mean_to_shift_ratio,
                "triggered_trades": row.triggered_trades,
                "priced_trades": row.priced_trades,
                "universe_emptied": row.selected_name_sessions == 0,
            }
        )

    findings: dict[str, Any] = {
        "kind": "h1b_price_floor_feasibility_scan",
        "hypothesis": "H1b",
        "hypothesis_status": "REGISTERED_NOT_OPEN",
        "scanned_at": date.today().isoformat(),
        "requests_sent": 0,
        "annual_sharpe_used_for_the_central_mean": (
            CONFIG.registered_sharpe_assumption
        ),
        "equity_normalisation_usd": EQUITY_USD,
        "comparison_figure": "central_mean_to_shift_ratio",
        "comparison_figure_note": (
            "The mechanism H1b registers is that per-share slippage is roughly "
            "price-invariant while per-share dispersion and edge scale with "
            "price, so this ratio should RISE with the floor. The shift here is "
            "the registered Section 6 band shift at each floor's own measured "
            "stop-exit share, and the measured entry overshoot is reported "
            "beside it as an independent check on the invariance half."
        ),
        "no_verdict_no_power_no_chosen_floor": (
            "H1b is REGISTERED_NOT_OPEN. Computing a verdict or a power figure "
            "would be opening it, and selecting a floor from the scan that "
            "motivated it would fit a parameter to its own evidence."
        ),
        "cannot_rescue_h1": (
            "Amendment 24 §6, registered before this ran: whatever this shows, "
            "it is feasibility evidence for a new hypothesis and never a "
            "continuation of H1."
        ),
        "rows": table,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "task4_floor_scan.json").write_text(
        json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8"
    )

    header = (
        f"{'floor':>7}{'selected':>10}{'sessions':>10}{'full20':>8}"
        f"{'mean relvol':>13}{'dispersion':>12}{'overshoot':>11}"
        f"{'central':>10}{'shift':>9}{'RATIO':>9}"
    )
    say("")
    say(header)
    say("-" * len(header))
    for r in table:
        say(
            f"{r['price_floor_usd']:>7.0f}{r['selected_name_sessions']:>10}"
            f"{r['sessions_evaluated']:>10}"
            f"{r['sessions_with_a_full_top20_selection']:>8}"
            f"{r['mean_relative_volume_of_selection']:>13.4f}"
            f"{r['dispersion_usd_per_share']:>12.4f}"
            f"{r['entry_overshoot_median_usd_per_share']:>11.4f}"
            f"{r['central_mean_usd_per_share_at_1_40']:>10.6f}"
            f"{r['shift_usd_per_share']:>9.6f}"
            f"{r['central_mean_to_shift_ratio']:>9.4f}"
        )
    say("")
    for r in table:
        if r["universe_emptied"]:
            floor_usd = r["price_floor_usd"]
            say(f"FINDING: the {floor_usd:.0f} USD floor EMPTIES the universe.")
        elif not r["top20_still_fillable_on_every_session"]:
            say(
                f"FINDING: at the {r['price_floor_usd']:.0f} USD floor the top-20 "
                f"selection is fillable on only "
                f"{r['sessions_with_a_full_top20_selection']} of "
                f"{r['sessions_evaluated']} sessions."
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
