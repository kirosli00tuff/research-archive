"""A.1 Task 4, retro leg part 2: the retro revision rate, measured.

For each archive-admissible retro day, fetch the qualifying pre-anchor archive
capture, extract the **as-printed** five-fund aggregate for that day, and
compare it against the value the source serves **today**.

This is the direct measurement of the MLCryptoEngine H11 hazard on this source:
a free flow table that is "generated automatically, in real time" and whose past
rows may revise. H11 died on that property, discovered rather than registered.

The archived value is never substituted for a live one and the live value is
never substituted for a missing archived one. A day whose archived capture does
not parse is a recorded absence with its reason.
"""

from __future__ import annotations

import json
import sys
from datetime import date

from etf.absence import Absent
from etf.archive import density, parse_timemap
from etf.clock import iso_z, now_utc
from etf.config import CONFIG
from etf.http import PacedClient, TransportFailure
from etf.ledger.requests import RequestLedger
from etf.paths import DATA, REPORTS
from etf.signal import position
from etf.snapshot import FlowTableShape, parse_flow_table

REPORT = REPORTS / "stage_a1" / "retro_revision.json"
BODIES = DATA / "archive_bodies"


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    BODIES.mkdir(parents=True, exist_ok=True)
    client = PacedClient(RequestLedger())

    live_days = parse_flow_table(
        (DATA / "access" / "farside-btc-all.html").read_text(errors="replace")
    )
    live = {d.trade_date: d.signal_usd for d in live_days if not isinstance(d.signal_usd, Absent)}
    oos_start = date.fromisoformat(CONFIG.oos_start_date)
    universe = [d for d in sorted(live) if d >= oos_start]

    mementos = []
    for label in ("recent", "all_data"):
        mementos += list(parse_timemap((DATA / "access" / f"timemap-{label}.txt").read_bytes()))
    report = density(universe, mementos)
    admissible = [d for d in report.days if d.admissible]
    print(f"archive-admissible retro days n = {len(admissible)}")

    rows: list[dict[str, object]] = []
    for day in admissible:
        # The qualifying capture is the LAST one strictly before the anchor:
        # it is the value that stood when the registered rule would have read.
        memento = day.qualifying[-1]
        try:
            response = client.get(memento.url, source="archive", endpoint="archive.snapshot")
        except TransportFailure as exc:
            rows.append(
                {
                    "trade_date": day.trade_date.isoformat(),
                    "state": "source_failed",
                    "detail": str(exc)[:200],
                    "archive_url": memento.url,
                }
            )
            continue
        entry: dict[str, object] = {
            "trade_date": day.trade_date.isoformat(),
            "archive_url": memento.url,
            "archive_captured_at": iso_z(memento.captured_at),
            "http_status": response.status,
            "byte_count": len(response.body),
        }
        if response.status != 200:
            entry["state"] = "source_failed"
            rows.append(entry)
            print(f"{day.trade_date} HTTP {response.status}")
            continue
        stem = f"{day.trade_date.isoformat()}-{memento.captured_at.strftime('%Y%m%d%H%M%S')}.html"
        (BODIES / stem).write_bytes(response.body)
        try:
            archived = parse_flow_table(response.body.decode("utf-8", "replace"))
        except (FlowTableShape, ValueError) as exc:
            entry |= {"state": "no_data", "detail": f"{type(exc).__name__}: {exc}"[:200]}
            rows.append(entry)
            print(f"{day.trade_date} unparseable: {type(exc).__name__}")
            continue
        served = {d.trade_date: d.signal_usd for d in archived}
        as_printed = served.get(day.trade_date)
        if as_printed is None:
            entry |= {
                "state": "no_data",
                "detail": "the archived capture serves no row for this day",
            }
            rows.append(entry)
            print(f"{day.trade_date} archived capture carries no row for the day")
            continue
        if isinstance(as_printed, Absent):
            entry |= {"state": "no_data", "as_printed_absent": as_printed.reason.value}
            rows.append(entry)
            print(f"{day.trade_date} as-printed absent: {as_printed.reason.value}")
            continue
        current = live[day.trade_date]
        assert not isinstance(current, Absent)
        delta = current - as_printed
        entry |= {
            "state": "stored",
            "as_printed_usd": as_printed,
            "current_usd": current,
            "delta_usd": delta,
            "delta_share": (delta / abs(as_printed)) if as_printed != 0 else None,
            "revised": delta != 0.0,
            "sign_flipped": (as_printed > 0) != (current > 0)
            and as_printed != 0.0
            and current != 0.0,
            "threshold_crossed": position(as_printed) is not position(current),
            "as_printed_position": int(position(as_printed)),
            "current_position": int(position(current)),
        }
        rows.append(entry)
        flag = ""
        if entry["sign_flipped"]:
            flag += " SIGN-FLIP"
        if entry["threshold_crossed"]:
            flag += " THRESHOLD-CROSS"
        print(
            f"{day.trade_date} as-printed {as_printed / 1e6:9.1f}M "
            f"current {current / 1e6:9.1f}M delta {delta / 1e6:8.1f}M{flag}"
        )

    stored = [r for r in rows if r.get("state") == "stored"]
    revised = [r for r in stored if r.get("revised")]
    flips = [r for r in stored if r.get("sign_flipped")]
    crosses = [r for r in stored if r.get("threshold_crossed")]
    intact = [r for r in stored if not r.get("sign_flipped") and not r.get("threshold_crossed")]
    out = {
        "measured_at": iso_z(now_utc()),
        "archive_admissible_days": len(admissible),
        "comparable_days": len(stored),
        "registered_minimum_sample": CONFIG.retro_revision_sample_min,
        "meets_registered_minimum": len(stored) >= CONFIG.retro_revision_sample_min,
        "revised_days": len(revised),
        "revised_share": (len(revised) / len(stored)) if stored else None,
        "sign_flip_days": len(flips),
        "sign_flip_share": (len(flips) / len(stored)) if stored else None,
        "threshold_cross_days": len(crosses),
        "threshold_cross_share": (len(crosses) / len(stored)) if stored else None,
        "intact_days": len(intact),
        "intact_share": (len(intact) / len(stored)) if stored else None,
        "rows": rows,
    }
    REPORT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(
        f"\ncomparable n = {len(stored)} of {len(admissible)} admissible; "
        f"revised {len(revised)}, sign flips {len(flips)}, threshold crosses {len(crosses)}, "
        f"intact {len(intact)}"
    )
    print(f"wrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
