"""A.1 TASK 4 — tape identification, measured rather than documented.

**The question.** Does each feed reflect **consolidated, SIP-derived** activity,
or a **single-venue subset** such as IEX alone? The answer decides whether the
registered cross-vendor agreement thresholds of Section 0 mean anything on this
pair: a single-venue feed is not a *disagreeing* measurement of the consolidated
tape, it is a **correct measurement of a different thing**, and scoring it
against the 0.95 / 0.85 bars would fire BLOCKED on a fact about entitlement.

**The method.** For a fixed list of 20 liquid tickers across 5 sessions, compare
**per-session first-5-minute total volume** between two feeds, **through the
sealed comparator**, which returns a ratio distribution and returns no bar value
to any caller. A single-venue subset presents a systematically small fraction of
a consolidated feed's volume.

**Three comparisons, not one.** The pair the experiment would actually use is
Massive against Alpaca-SIP. The other two are **controls**, and they are what
turn a number into evidence:

- **Massive vs Alpaca-IEX** — a positive control on a pair that *must* come back
  DIFFERENT_TAPE if the discriminator works at all.
- **Alpaca-SIP vs Alpaca-IEX** — a **within-vendor** control. Same vendor, same
  API, same request, one parameter changed. If this does not separate, nothing
  in this task is measuring what it claims to.

**The window, and why it is not the registered one.** The prompt specifies the
pre-period carve-out. **A.1 TASK 3 measured that neither credential serves it**:
Massive refuses with `403 NOT_AUTHORIZED` and Alpaca serves an empty set. The
sessions used here sit **strictly after `holdout_end` = 2026-06-30**, so they lie
**outside both the in-sample and the holdout windows** — the identical property
that makes the pre-period carve-out safe, applied at the other end of the
registered windows. No observation any verdict will be computed on is touched.

**This tool parses a vendor envelope and never reads a bar field.** It calls
``json.loads``, hands the resulting array straight to the sealed comparator, and
inspects no element of it.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import send, wire, write_report  # noqa: E402
from orb.calendar import sessions  # noqa: E402
from orb.comparator import SealedComparator, count_bars  # noqa: E402
from orb.config import CONFIG  # noqa: E402
from orb.redact import say  # noqa: E402
from orb.vendors import alpaca_minute_bars, massive_minute_bars  # noqa: E402

TICKERS: tuple[str, ...] = (
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL",
    "META", "TSLA", "JPM", "V", "UNH",
    "XOM", "JNJ", "WMT", "PG", "MA",
    "HD", "CVX", "ABBV", "KO", "PEP",
)
"""Twenty mega-cap US common stocks. **Documented liquidity, never measured.**

The list is fixed before the first request and is not tuned by any result. Tape
identification does not depend on the selection being optimal — it depends on
the names carrying enough volume that a ratio is not dominated by rounding — and
mega-caps carry that by construction rather than by this repository's
measurement.
"""

WINDOW_START = date(2026, 7, 1)
WINDOW_END = date(2026, 7, 31)
SESSION_COUNT = 5


def chosen_sessions() -> list[object]:
    """Five full regular sessions strictly after the registered holdout end."""
    holdout_end = date.fromisoformat(CONFIG.holdout_end)
    out = []
    for session in sessions(WINDOW_START, WINDOW_END):
        if session.day <= holdout_end or session.is_half:
            continue
        out.append(session)
        if len(out) == SESSION_COUNT:
            break
    return out


def main() -> int:
    store, client, seal = wire()
    picked = chosen_sessions()
    days = [s.day.isoformat() for s in picked]
    say(f"sessions, n = {len(picked)}: {days}")
    say(f"tickers, n = {len(TICKERS)}")

    start_session, end_session = days[0], days[-1]
    start_iso = f"{start_session}T00:00:00Z"
    end_iso = f"{end_session}T23:59:59Z"

    feeds: dict[str, dict[str, list[dict[str, object]]]] = {
        "massive": {},
        "alpaca_sip": {},
        "alpaca_iex": {},
    }
    calls: list[dict[str, object]] = []

    def pull(label: str, feed_name: str, ticker: str, request: object) -> None:
        response = send(client, request)  # type: ignore[arg-type]
        record = seal.store(f"task4_{feed_name}_{ticker}.raw", response.body)
        counted = count_bars(response.body)
        calls.append(
            {
                "feed": feed_name,
                "ticker": ticker,
                "status_code": response.status_code,
                "served_byte_count": response.byte_count,
                "bar_count": counted,
                "health": response.health.value,
                "sha256": record.sha256,
                "latency_s": round(response.elapsed_s, 3),
            }
        )
        rows: list[dict[str, object]] = []
        if 200 <= response.status_code < 300:
            try:
                envelope = json.loads(response.body)
            except json.JSONDecodeError:
                envelope = {}
            if isinstance(envelope, dict):
                for key in ("results", "bars"):
                    found = envelope.get(key)
                    if isinstance(found, list):
                        rows = found
                        break
        feeds[feed_name][ticker] = rows
        say(f"  {label:24s} http={response.status_code} bars={counted}")

    for ticker in TICKERS:
        pull(
            f"massive {ticker}",
            "massive",
            ticker,
            massive_minute_bars(store, ticker, start_session, end_session),
        )
    for ticker in TICKERS:
        pull(
            f"alpaca sip {ticker}",
            "alpaca_sip",
            ticker,
            alpaca_minute_bars(store, ticker, start_iso, end_iso, feed="sip"),
        )
    for ticker in TICKERS:
        pull(
            f"alpaca iex {ticker}",
            "alpaca_iex",
            ticker,
            alpaca_minute_bars(store, ticker, start_iso, end_iso, feed="iex"),
        )

    windows: dict[str, tuple[int, int]] = {}
    keyed: dict[str, dict[str, list[dict[str, object]]]] = {
        name: {} for name in feeds
    }
    for session in picked:
        window = session.opening_range_utc()  # type: ignore[attr-defined]
        for ticker in TICKERS:
            key = f"{ticker}:{session.day.isoformat()}"  # type: ignore[attr-defined]
            windows[key] = window
            for name, rows_by_ticker in feeds.items():
                keyed[name][key] = rows_by_ticker.get(ticker, [])

    comparator = SealedComparator()
    pairs = (
        ("massive_vs_alpaca_sip", "massive", "alpaca_sip"),
        ("massive_vs_alpaca_iex", "massive", "alpaca_iex"),
        ("alpaca_sip_vs_alpaca_iex", "alpaca_sip", "alpaca_iex"),
    )
    results: list[dict[str, object]] = []
    for label, primary, secondary in pairs:
        finding = comparator.compare_tapes(keyed[primary], keyed[secondary], windows)
        results.append(
            {
                "comparison": label,
                "primary_feed": primary,
                "secondary_feed": secondary,
                "verdict": finding.verdict().value,
                "agreement_thresholds_apply": finding.agreement_thresholds_apply(),
                "looks_like_a_single_venue_subset": (
                    finding.looks_like_a_single_venue_subset()
                ),
                "median_ratio": finding.median_ratio,
                "iqr_low_ratio": finding.iqr_low_ratio,
                "iqr_high_ratio": finding.iqr_high_ratio,
                "min_ratio": finding.min_ratio,
                "max_ratio": finding.max_ratio,
                "share_below_single_venue_threshold": (
                    finding.share_below_single_venue_threshold
                ),
                "session_ticker_pairs_compared": (
                    finding.session_ticker_pairs_compared
                ),
                "pairs_with_volume_in_both": finding.pairs_with_volume_in_both,
                "pairs_with_volume_in_primary_only": (
                    finding.pairs_with_volume_in_primary_only
                ),
                "pairs_with_volume_in_secondary_only": (
                    finding.pairs_with_volume_in_secondary_only
                ),
                "pairs_with_volume_in_neither": finding.pairs_with_volume_in_neither,
            }
        )
        say(
            f"{label:26s} verdict={finding.verdict().value:14s} "
            f"median={finding.median_ratio:.4f} "
            f"iqr=[{finding.iqr_low_ratio:.4f}, {finding.iqr_high_ratio:.4f}] "
            f"n={finding.pairs_with_volume_in_both}"
        )

    write_report(
        "task4_tape.json",
        {
            "sessions": days,
            "tickers": list(TICKERS),
            "session_count": len(picked),
            "ticker_count": len(TICKERS),
            "calls": calls,
            "comparisons": results,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
