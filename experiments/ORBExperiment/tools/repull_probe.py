"""A.1 TASK 3 — the identical re-pull, and the bar revision measurement.

**Armed, and refusing until the registered wait has elapsed.** Run it any day; it
refuses with the earliest eligible date until that date arrives. **No timer is
enabled and no systemd unit is armed by this file** — the collector and its
timers stay inert until the revision verdict exists.

**What it does when it is due.** Re-sends the identical request set recorded in
`reports/stage_a1r/task9_probe_manifest.json`, seals the bytes into a second
root, and hands both pulls to `orb.comparator.SealedComparator.compare_pulls`,
which returns a `RevisionFinding` of counts and **no bar value**.

**Two keyings, on purpose.** The **byte-level** comparison keys on the stored
file, which is a `(ticker, chunk, page)` triple. The **bar-level** comparison
re-keys to `(ticker, session)` from the readable timestamp, so the registered
`session_ticker_pairs_compared` is the registered 2,400 rather than an artefact
of how the request was chunked.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import DATA, REPORTS, send, wire, write_report  # noqa: E402
from orb.comparator import SealedComparator, count_bars  # noqa: E402
from orb.ledger import AppendOnlyLedger  # noqa: E402
from orb.redact import say  # noqa: E402
from orb.repull import RepullNotDueError, earliest_eligible, require_due  # noqa: E402
from orb.seal import SealedWriter  # noqa: E402
from orb.vendors import alpaca_minute_bars  # noqa: E402

MANIFEST = REPORTS / "task9_probe_manifest.json"
FIRST_ROOT = DATA / "sealed_credentialed"
SECOND_ROOT = DATA / "sealed_repull"


def session_of(stamp_ms_or_iso: object) -> str | None:
    """The session date of a bar timestamp. A **readable** field."""
    if isinstance(stamp_ms_or_iso, bool):
        return None
    if isinstance(stamp_ms_or_iso, int):
        return datetime.fromtimestamp(stamp_ms_or_iso / 1000, tz=UTC).date().isoformat()
    if isinstance(stamp_ms_or_iso, str):
        text = stamp_ms_or_iso.replace("Z", "+00:00")
        try:
            moment = datetime.fromisoformat(text)
        except ValueError:
            return None
        return None if moment.tzinfo is None else moment.date().isoformat()
    return None


def bars_by_session(payload: bytes, ticker: str) -> dict[str, list[dict[str, object]]]:
    """Bucket a served payload into session-ticker keys. Reads only the stamp."""
    out: dict[str, list[dict[str, object]]] = {}
    try:
        envelope = json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return out
    rows = envelope.get("bars") if isinstance(envelope, dict) else None
    if not isinstance(rows, list):
        return out
    for row in rows:
        if not isinstance(row, dict):
            continue
        session = session_of(row.get("t"))
        if session is None:
            continue
        out.setdefault(f"{ticker}:{session}", []).append(row)
    return out


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pulled_on = date.fromisoformat(manifest["pulled_at"])
    today = date.today()
    try:
        waited = require_due(pulled_on, today)
    except RepullNotDueError as refusal:
        say(str(refusal))
        say(
            f"EARLIEST ELIGIBLE RE-PULL: {earliest_eligible(pulled_on).isoformat()}. "
            "Nothing was sent."
        )
        return 78

    store, client, seal_unused = wire()
    del seal_unused
    seal = SealedWriter(SECOND_ROOT, AppendOnlyLedger(DATA / "seals.jsonl"))

    first_bytes: dict[str, bytes] = {}
    second_bytes: dict[str, bytes] = {}
    first_bars: dict[str, list[dict[str, object]]] = {}
    second_bars: dict[str, list[dict[str, object]]] = {}

    for entry in manifest["manifest"]:
        name = str(entry["stored_file"])
        ticker = str(entry["ticker"])
        original = (FIRST_ROOT / name).read_bytes()
        first_bytes[name] = original
        for key, rows in bars_by_session(original, ticker).items():
            first_bars.setdefault(key, []).extend(rows)

        response = send(
            client,
            alpaca_minute_bars(
                store,
                ticker,
                str(entry["start_iso"]),
                str(entry["end_iso"]),
                feed="sip",
                limit=10000,
            ),
        )
        seal.store(name, response.body)
        second_bytes[name] = response.body
        for key, rows in bars_by_session(response.body, ticker).items():
            second_bars.setdefault(key, []).extend(rows)
        say(f"  re-pulled {name}: http={response.status_code} bars={count_bars(response.body)}")

    finding = SealedComparator().compare_pulls(
        first_bytes,
        second_bytes,
        first_bars,
        second_bars,
        corporate_action_keys=frozenset(),
        wait_days_observed=waited,
    )
    payload = {
        "pulled_at": manifest["pulled_at"],
        "repulled_at": today.isoformat(),
        "wait_days_observed": waited,
        "wait_satisfied": finding.wait_satisfied(),
        "changed_bar_share": finding.changed_bar_share,
        "bars_compared": finding.bars_compared,
        "changed_bar_count": finding.changed_bar_count,
        "session_ticker_pairs_compared": finding.session_ticker_pairs_compared,
        "pairs_with_changed_bar_count": finding.pairs_with_changed_bar_count,
        "pairs_with_timestamp_change": finding.pairs_with_timestamp_change,
        "verdict": finding.verdict().value,
    }
    write_report("task3_revision.json", payload)
    say(
        f"revision share {finding.changed_bar_share:.6f} over n = "
        f"{finding.bars_compared} bars, verdict {finding.verdict().value}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
