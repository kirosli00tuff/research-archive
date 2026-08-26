"""Copy the market data this experiment needs out of the neighbouring repository.

Runs once. Hashes both permitted source files before and after, copies the
trading calendar, the stored universe membership for the registered rule, and
the daily bars of every symbol that is ever a member, then hashes again and
records the pair. Nothing downstream reads across the boundary.
"""

from __future__ import annotations

import json
import sys

from insider.config import CONFIG
from insider.ledger.evidence import record
from insider.market import source, store
from insider.paths import REPORTS, ensure_dirs


def main() -> int:
    ensure_dirs()
    cfg = CONFIG
    print("hashing both source files before any read")
    before = source.hash_sources()
    print(f"  bars     {before[0]}")
    print(f"  universe {before[1]}")

    with source.read_only_bars() as src, store.connect() as dst:
        calendar = source.sessions(src, cfg.bars_start, cfg.bars_end)
        store.write_sessions(dst, calendar)
        print(f"sessions {len(calendar)} from {calendar[0]} to {calendar[-1]}")

        formations = [
            f
            for f in source.formation_dates_available(src, cfg.universe_id)
            if cfg.bars_start <= f <= cfg.bars_end
        ]
        symbols: set[str] = set()
        for formation in formations:
            rows = source.stored_membership(src, cfg.universe_id, formation)
            store.write_membership(dst, formation, rows)
            symbols.update(r[0] for r in rows)
        print(f"formations {len(formations)} covering {len(symbols)} distinct symbols")

        written = 0
        batch: list[tuple[str, str, float, float]] = []
        for row in source.daily_bars_for(src, sorted(symbols), cfg.bars_start, cfg.bars_end):
            batch.append(row)
            if len(batch) >= 200_000:
                written += store.write_bars(dst, batch)
                batch.clear()
                print(f"  bars copied {written}", flush=True)
        written += store.write_bars(dst, batch)
        print(f"bars copied {written}")

        store.set_meta(dst, "universe_id", cfg.universe_id)
        store.set_meta(dst, "bars_start", cfg.bars_start)
        store.set_meta(dst, "bars_end", cfg.bars_end)
        store.set_meta(dst, "distinct_symbols", str(len(symbols)))
        store.set_meta(dst, "bars_copied", str(written))

    print("hashing both source files after the read")
    after = source.hash_sources()
    result = source.integrity(before, after)
    print(f"  bars     {after[0]}")
    print(f"  universe {after[1]}")
    print(f"source unchanged: {result.unchanged}")

    payload = {
        "sessions": len(calendar),
        "formations": len(formations),
        "distinct_symbols": len(symbols),
        "bars_copied": written,
        "bars_sha256_before": result.bars_sha256_before,
        "bars_sha256_after": result.bars_sha256_after,
        "universe_sha256_before": result.universe_sha256_before,
        "universe_sha256_after": result.universe_sha256_after,
        "bars_size_bytes": result.bars_size_bytes,
        "unchanged": result.unchanged,
    }
    record("market_port", **payload)
    out = REPORTS / "stage_a1"
    out.mkdir(parents=True, exist_ok=True)
    (out / "port.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if not result.unchanged:
        print("SOURCE CHANGED DURING THE READ. The port is not trustworthy.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
