"""Build the calendar-time series at every registered hold and weighting.

Writes the raw series to the seal and the centered series to dispersion. Reads
neither back. This is the last module that can see a portfolio's first moment,
and it does not look at one.
"""

from __future__ import annotations

import json
import sys

from insider.config import CONFIG
from insider.corpus import store as corpus_store
from insider.ledger.evidence import record
from insider.market import store as market_store
from insider.paths import REPORTS, ensure_dirs
from insider.portfolio import returns
from insider.portfolio.membership import Event
from insider.portfolio.membership import build as build_membership


def main() -> int:
    ensure_dirs()
    cfg = CONFIG

    with corpus_store.connect() as ccon:
        pairs = corpus_store.events(ccon)
    if not pairs:
        print("no qualifying events. The corpus gate governs, not this step.")
        return 1
    events = [Event(symbol=s, entry_session=e) for s, e in pairs]
    print(f"{len(events)} qualifying events")

    with market_store.connect() as mcon:
        sessions = market_store.sessions(mcon)
        print("loading the price panel")
        panel = returns.load_panel(mcon)
        print(f"  {len(panel.symbols)} symbols by {len(panel.dates)} sessions")
        rets = returns.simple_returns(panel)

        plan = [(cfg.primary_hold_sessions, cfg.primary_weighting)]
        plan += [(h, cfg.primary_weighting) for h in cfg.secondary_hold_sessions]
        plan += [(cfg.primary_hold_sessions, cfg.secondary_weighting)]

        builds = []
        summary = []
        for hold, weighting in plan:
            series = build_membership(events, sessions, hold)
            built = returns.build_series(mcon, panel, rets, series, weighting)
            builds.append(built)
            widths = sorted(built.book_width)
            summary.append(
                {
                    "hold_sessions": hold,
                    "weighting": weighting,
                    "sessions_with_a_return": len(built.dates),
                    "membership_coverage": round(series.coverage(), 6),
                    "book_width_mean": round(series.mean_width(), 3),
                    "book_width_min": widths[0] if widths else 0,
                    "book_width_p10": widths[len(widths) // 10] if widths else 0,
                    "book_width_p50": widths[len(widths) // 2] if widths else 0,
                    "book_width_p90": widths[len(widths) * 9 // 10] if widths else 0,
                    "book_width_max": widths[-1] if widths else 0,
                    "dropped": built.dropped,
                    "diagnostics": {k: round(v, 6) for k, v in built.diagnostics.items()},
                }
            )
            d = built.diagnostics
            print(
                f"  hold {hold:>3} {weighting:<15} sessions {len(built.dates):>5} "
                f"width {series.mean_width():6.1f}  eff names {d['book_effective_names']:6.1f}  "
                f"top1 {d['book_weight_top1_share']:5.1%}  top5 {d['book_weight_top5_share']:5.1%}  "
                f"corr {d['corr_portfolio_benchmark']:5.3f}"
            )

    returns.write(builds)
    print("wrote the raw series to the seal and the centered series to dispersion")

    out = REPORTS / "stage_a1"
    out.mkdir(parents=True, exist_ok=True)
    (out / "portfolio.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    record("portfolio_build", series=summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
