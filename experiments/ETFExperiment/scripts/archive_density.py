"""A.1 Task 4, retro leg: archive capture density per US trading day, measured.

The trading-day universe is taken from the flow source's own date rows rather
than from a hardcoded holiday calendar: Section 2 defines an event as "one per
US trading day on which an admissible as-printed flow value exists", so the
days the table prints a value for ARE the universe, and that is measured
rather than assumed.

Reads capture timestamps and flow values. No price field is touched.
"""

from __future__ import annotations

import json
import sys
from datetime import date

from etf.absence import Absent
from etf.archive import Memento, density, parse_timemap
from etf.clock import iso_z, now_utc
from etf.config import CONFIG
from etf.http import PacedClient
from etf.ledger.requests import RequestLedger
from etf.paths import DATA, REPORTS
from etf.snapshot import parse_flow_table

REPORT = REPORTS / "stage_a1" / "archive_density.json"
OUT = DATA / "access"

PAGES = (
    ("recent", CONFIG.flow_recent_url),
    ("all_data", CONFIG.flow_all_data_url),
)


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    client = PacedClient(RequestLedger())

    all_data = (OUT / "farside-btc-all.html").read_text(errors="replace")
    days = parse_flow_table(all_data)
    oos_start = date.fromisoformat(CONFIG.oos_start_date)
    universe = [
        d.trade_date
        for d in days
        if d.trade_date >= oos_start and not isinstance(d.signal_usd, Absent)
    ]
    all_rows = [d.trade_date for d in days if d.trade_date >= oos_start]
    print(f"out-of-sample date rows n = {len(all_rows)}; with a printed signal n = {len(universe)}")

    out: dict[str, object] = {
        "measured_at": iso_z(now_utc()),
        "oos_date_rows": len(all_rows),
        "oos_days_with_a_printed_signal": len(universe),
        "first_day": universe[0].isoformat(),
        "last_day": universe[-1].isoformat(),
        "pages": {},
    }
    pages: dict[str, object] = {}
    for label, url in PAGES:
        response = client.get(
            f"{CONFIG.wayback_timemap_url}/{url}", source="archive", endpoint="archive.timemap"
        )
        (OUT / f"timemap-{label}.txt").write_bytes(response.body)
        mementos = parse_timemap(response.body)
        report = density(universe, mementos)
        pages[label] = {
            "url": url,
            "http_status": response.status,
            "byte_count": len(response.body),
            "total_mementos": report.total_mementos,
            "first_memento": iso_z(report.first_memento) if report.first_memento else None,
            "last_memento": iso_z(report.last_memento) if report.last_memento else None,
            "n_trading_days": report.n_trading_days,
            "admissible_days": report.admissible_days,
            "admissible_share": report.admissible_share,
            "no_capture_days": report.no_capture_days,
            "capture_too_late_days": report.capture_too_late_days,
            "admissible_dates": [d.trade_date.isoformat() for d in report.days if d.admissible],
        }
        print(
            f"{label:9s} mementos={report.total_mementos:4d} "
            f"admissible={report.admissible_days}/{report.n_trading_days} "
            f"({(report.admissible_share or 0):.4f}) "
            f"no_capture={report.no_capture_days} too_late={report.capture_too_late_days}"
        )

    # The union of both pages: either page's capture serves the day's value,
    # because the recent page carries the most recent rows and the all-data
    # page carries every row. Union the intervals before summing (standing
    # rule 9), which here means unioning the memento sets, not adding shares.
    merged: list[Memento] = []
    for label, _ in PAGES:
        merged.extend(parse_timemap((OUT / f"timemap-{label}.txt").read_bytes()))
    union = density(universe, merged)
    pages["union"] = {
        "total_mementos": union.total_mementos,
        "n_trading_days": union.n_trading_days,
        "admissible_days": union.admissible_days,
        "admissible_share": union.admissible_share,
        "no_capture_days": union.no_capture_days,
        "capture_too_late_days": union.capture_too_late_days,
        "admissible_dates": [d.trade_date.isoformat() for d in union.days if d.admissible],
    }
    print(
        f"{'UNION':9s} mementos={union.total_mementos:4d} "
        f"admissible={union.admissible_days}/{union.n_trading_days} "
        f"({(union.admissible_share or 0):.4f}) "
        f"no_capture={union.no_capture_days} too_late={union.capture_too_late_days}"
    )
    out["pages"] = pages
    REPORT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
