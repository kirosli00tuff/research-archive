"""A.1 TASK 5, phase 2 — the E2 dispersion input and the E2 power figures.

**Runs the sealed writer over the post-holdout carve-out and reports two
scalars.** The writer returns nothing else; see `orb.dispersion`.

**The frozen Section 6 cost model refuses every trade, and that is not a bug.**
A.2 TASK 2 measured the SEC Section 31 rate at **0.0000206 per dollar** and
**did not measure its effective date** — `sec.gov` answered `403 Request Rate
Threshold Exceeded` then, and answered the same on two further attempts in this
pass, `n = 4` refusals across two sessions. `SEC_FEE_SCHEDULE` is therefore empty
on purpose and **the model refuses to price a trade rather than take a fee from
the wrong year**. It is also not recoverable from the stored vendor pages: the
IBKR schedule states `SEC Transaction Fee: USD 0.0000206 * Value of Aggregate
Sales` and **carries no effective date anywhere on the page**.

**So the figure is delivered as a measured bracket rather than as an absence.**
The only unmeasured component is varied across its two ends and everything else
is held at the frozen model:

- **zero** — a fee cannot be negative, so this is a fact about arithmetic;
- **0.0000206** — the one rate this repository has measured.

**If the two ends agree, the unmeasured effective date does not matter for this
figure, and that is a measurement rather than a hope.** The registered figure
under the frozen model is still reported, and it is still `Absent`.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import DATA, REPORTS, write_report

from orb.calendar import sessions
from orb.config import CONFIG
from orb.costs import Band, CostModel, Leg, SecFeeSchedule, Side
from orb.costs_registered import REGISTERED_COST_MODEL, SEC_RATE_MEASURED
from orb.dispersion import CarveOutDispersion, measure_carve_out_dispersion
from orb.ledger import AppendOnlyLedger
from orb.power import e2_power, power_one_sided, sessions_for_power
from orb.redact import say
from orb.verdict import alpha_adj

MANIFEST = REPORTS / "task5b_post_holdout_pull.json"
SEALED_ROOT = DATA / "sealed_credentialed"
EQUITY_USD = 100_000.0
"""A **non-binding normalisation**. Section 4 registers a risk fraction and no
equity level, and every figure this tool feeds into E2 is a ratio, so it cancels.
The writer's scalar is per share and is invariant to it outright."""

HOLDOUT_N = 875
IN_SAMPLE_N = 1762

CARVE_OUT_CAVEAT = (
    "Amendment 11: the dispersion input comes from a POST-HOLDOUT regime "
    "(2026-07-01 onward), later than the sample it is applied to. A pre-2016 "
    "estimate would have reflected an earlier one. Neither is neutral; the "
    "compromise now runs forward rather than backward, and this figure may "
    "misstate in-sample dispersion in either direction by an amount this "
    "repository has not measured and does not claim to bound."
)

TRIGGER_RATE_ASSUMPTION = 0.55
"""The figure used until now in the **non-binding** per-trade power note. It was
never a measurement, and Section 9 says so: *a trigger rate that is a measurement
target and never an assumption*."""

CARRIED_GROSS_EDGE_PER_SHARE = 0.070
"""C-6, **carried**: the independent replication measured a gross edge of 0.070
USD per share on the **sibling index strategy**. Applying it to the registered
stock universe is a **cross-application of a carried figure**, and it is labelled
here rather than absorbed."""


def _model_with_sec_rate(rate: float) -> CostModel:
    """The frozen model with the one unmeasured component set to ``rate``."""
    return replace(
        REGISTERED_COST_MODEL,
        sec_fees=SecFeeSchedule(
            effective_dates=(date(2026, 1, 1),), rates_per_dollar=(rate,)
        ),
    )


def _cost_per_share(model: CostModel, leg: Leg) -> float | None:
    """Modeled round-trip cost per share on a 1,000-share, 50 USD trade.

    A pure function of the cost model and stated inputs. **It reads no bar.**
    """
    cost = model.round_trip_cost(
        1000, 50.0, 50.0, leg, Side.LONG, date(2026, 7, 15), Band.CENTRAL
    )
    return None if not isinstance(cost, float) else cost / 1000


def _as_row(result: CarveOutDispersion) -> dict[str, Any]:
    return {
        "net_pnl_per_share_stdev": result.net_pnl_per_share_stdev,
        "trigger_rate": result.trigger_rate,
        "sessions_evaluated": result.sessions_evaluated,
        "name_sessions_evaluated": result.name_sessions_evaluated,
        "name_sessions_triggered": result.name_sessions_triggered,
        "name_sessions_ambiguous": result.name_sessions_ambiguous,
        "trades_priced": result.trades_priced,
        "trades_refused_by_cost_model": result.trades_refused_by_cost_model,
        "trades_below_one_share": result.trades_below_one_share,
        "stop_exits": result.stop_exits,
        "close_exits": result.close_exits,
        "bars_read": result.bars_read,
        "tickers_with_bars": result.tickers_with_bars,
    }


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

    alpha = alpha_adj()
    runs: dict[str, CarveOutDispersion] = {}
    variants = [
        ("frozen_section_6_model", REGISTERED_COST_MODEL, True),
        ("bracket_sec_rate_zero", _model_with_sec_rate(0.0), True),
        ("bracket_sec_rate_measured", _model_with_sec_rate(SEC_RATE_MEASURED), True),
        (
            "bracket_sec_rate_measured_long_only",
            _model_with_sec_rate(SEC_RATE_MEASURED),
            False,
        ),
    ]
    for label, model, allow_short in variants:
        say(f"running the sealed writer: {label} (allow_short={allow_short})")
        runs[label] = measure_carve_out_dispersion(
            tickers,
            load,
            slice_sessions,
            model,
            allow_short=allow_short,
            equity_usd=EQUITY_USD,
        )
        r = runs[label]
        say(
            f"  sd/share={r.net_pnl_per_share_stdev:.6f} "
            f"trigger_rate={r.trigger_rate:.6f} "
            f"priced={r.trades_priced} refused={r.trades_refused_by_cost_model} "
            f"name_sessions={r.name_sessions_evaluated}"
        )

    frozen = runs["frozen_section_6_model"]
    zero = runs["bracket_sec_rate_zero"]
    measured = runs["bracket_sec_rate_measured"]
    long_only = runs["bracket_sec_rate_measured_long_only"]

    dispersion = measured.net_pnl_per_share_stdev
    bracket_width = abs(zero.net_pnl_per_share_stdev - dispersion)
    trades = measured.trades_priced
    per_session = (
        trades / measured.sessions_evaluated if measured.sessions_evaluated else 0.0
    )

    # --- E2 power at the three registered assumptions --------------------
    e2_rows: list[dict[str, Any]] = []
    for name, sharpe in (
        ("published_2.81", CONFIG.published_sharpe_assumption),
        ("REGISTERED_1.40", CONFIG.registered_sharpe_assumption),
        ("quartered_0.70", CONFIG.quartered_sharpe_assumption),
    ):
        daily = sharpe / math.sqrt(CONFIG.trading_days_per_year)
        for horizon, n_sessions in (
            ("holdout_875", HOLDOUT_N),
            ("in_sample_1762", IN_SAMPLE_N),
        ):
            k = per_session if per_session > 0 else 1.0
            implied_mean = dispersion * daily / math.sqrt(k)
            n_trades = max(1, round(n_sessions * k))
            power = e2_power(dispersion, implied_mean, n_trades, alpha)
            e2_rows.append(
                {
                    "assumption": name,
                    "annual_sharpe": sharpe,
                    "horizon": horizon,
                    "sessions": n_sessions,
                    "trades_implied": n_trades,
                    "per_trade_dispersion_usd_per_share": dispersion,
                    "implied_mean_usd_per_share": implied_mean,
                    "e2_power": power if isinstance(power, float) else str(power),
                    "e1_power_same_inputs": power_one_sided(sharpe, n_sessions, alpha),
                    "min_n_sessions_for_80_percent": sessions_for_power(
                        sharpe, alpha, CONFIG.target_power
                    ),
                    "carve_out_caveat": CARVE_OUT_CAVEAT,
                }
            )

    # --- where the dispersion actually binds: the net edge ---------------
    edge_rows: list[dict[str, Any]] = []
    model = _model_with_sec_rate(SEC_RATE_MEASURED)
    for leg in (Leg.CLOSE_EXIT, Leg.STOP_EXIT):
        cost = _cost_per_share(model, leg)
        for name, sharpe in (
            ("published_2.81", CONFIG.published_sharpe_assumption),
            ("REGISTERED_1.40", CONFIG.registered_sharpe_assumption),
            ("quartered_0.70", CONFIG.quartered_sharpe_assumption),
        ):
            gross = CARRIED_GROSS_EDGE_PER_SHARE * (
                sharpe / CONFIG.published_sharpe_assumption
            )
            net = None if cost is None else gross - cost
            ir = None if (net is None or dispersion <= 0) else net / dispersion
            edge_rows.append(
                {
                    "exit_leg": leg.value,
                    "assumption": name,
                    "gross_edge_usd_per_share_carried_scaled": gross,
                    "modeled_cost_usd_per_share": cost,
                    "net_edge_usd_per_share": net,
                    "measured_dispersion_usd_per_share": dispersion,
                    "implied_per_trade_information_ratio": ir,
                    "carve_out_caveat": CARVE_OUT_CAVEAT,
                }
            )

    findings: dict[str, Any] = {
        "kind": "carve_out_dispersion_and_e2_power",
        "computed_at": date.today().isoformat(),
        "carve_out_half": "post_holdout",
        "carve_out_boundary_ms": CONFIG.post_holdout_start_ms,
        "sessions_pulled": manifest["session_count"],
        "sessions_evaluable_after_trailing_window": measured.sessions_evaluated,
        "relvol_lookback_sessions": CONFIG.relvol_lookback_sessions,
        "tickers_sampled": manifest["ticker_count"],
        "universe_stride": manifest["universe_stride"],
        "reference_pool_size": manifest["reference_pool_size"],
        "equity_normalisation_usd": EQUITY_USD,
        "equity_normalisation_note": (
            "non-binding: Section 4 registers a risk fraction and no equity "
            "level, the writer's scalar is per share, and every E2 input is a "
            "ratio, so this cancels"
        ),
        "alpha_adj": alpha,
        "runs": {label: _as_row(result) for label, result in runs.items()},
        "registered_figure_under_the_frozen_model": (
            "Absent(sec_section_31_effective_date_not_measured): the frozen "
            f"Section 6 model refused {frozen.trades_refused_by_cost_model} of "
            f"{frozen.trades_refused_by_cost_model} trades. sec.gov answered 403 "
            "Request Rate Threshold Exceeded on n = 4 attempts across two "
            "sessions, and the stored IBKR schedule carries the rate 0.0000206 "
            "with no effective date anywhere on the page."
        ),
        "dispersion_usd_per_share": dispersion,
        "dispersion_bracket_low_sec_rate_zero": zero.net_pnl_per_share_stdev,
        "dispersion_bracket_high_sec_rate_measured": dispersion,
        "dispersion_bracket_width": bracket_width,
        "dispersion_bracket_relative_width": (
            bracket_width / dispersion if dispersion else None
        ),
        "measured_trigger_rate": measured.trigger_rate,
        "measured_trigger_rate_n_name_sessions": measured.name_sessions_evaluated,
        "trigger_rate_assumption_used_until_now": TRIGGER_RATE_ASSUMPTION,
        "trigger_rate_disagreement": measured.trigger_rate - TRIGGER_RATE_ASSUMPTION,
        "trades_per_session_measured": per_session,
        "long_only_sensitivity": _as_row(long_only),
        "e2_power_rows": e2_rows,
        "net_edge_rows": edge_rows,
        "carve_out_caveat": CARVE_OUT_CAVEAT,
    }
    write_report("task5c_dispersion_e2.json", findings)

    AppendOnlyLedger(DATA / "carve_out_reads.jsonl").append(
        {
            "kind": "carve_out_dispersion_computation",
            "half": "post_holdout",
            "sessions": manifest["sessions"],
            "sessions_evaluated": measured.sessions_evaluated,
            "tickers": manifest["ticker_count"],
            "bars_read": measured.bars_read,
            "dispersion_usd_per_share": dispersion,
            "trigger_rate": measured.trigger_rate,
            "trigger_rate_n": measured.name_sessions_evaluated,
        }
    )

    say("")
    say(
        f"MEASURED TRIGGER RATE  {measured.trigger_rate:.6f}  "
        f"n = {measured.name_sessions_evaluated} selected name-sessions, "
        f"against an assumption of {TRIGGER_RATE_ASSUMPTION}"
    )
    say(
        f"DISPERSION             {dispersion:.6f} USD/share, "
        f"n = {trades} priced trades; bracket width {bracket_width:.9f}"
    )
    say("")
    for row in e2_rows:
        power = row["e2_power"]
        rendered = f"{power:.4f}" if isinstance(power, float) else str(power)
        say(
            f"  E2 {row['assumption']:<16} {row['horizon']:<16} "
            f"n={row['sessions']:>5} trades={row['trades_implied']:>7} "
            f"power={rendered}  minN80={row['min_n_sessions_for_80_percent']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
