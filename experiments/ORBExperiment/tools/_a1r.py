"""Shared wiring for the A.1 resumption tools.

Every tool here loads credentials **through** ``orb.credentials.load_credentials``,
which installs the Guard 8 redactor before any caller holds a value. Nothing in
this package prints, writes or raises a string that has not passed a recording
boundary.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orb.comparator import count_bars  # noqa: E402
from orb.credentials import CredentialStore, load_credentials  # noqa: E402
from orb.http import PacedClient, Response  # noqa: E402
from orb.ledger import AppendOnlyLedger, RequestLedger  # noqa: E402
from orb.redact import say  # noqa: E402
from orb.seal import SealedWriter  # noqa: E402
from orb.vendors import (  # noqa: E402
    CONSERVATIVE_SPACING_S,
    PROVISIONAL_DAILY_CAPS,
    VendorRequest,
)

DATA = ROOT / "data" / "access"
REPORTS = ROOT / "reports" / "stage_a1r"


def wire() -> tuple[CredentialStore, PacedClient, SealedWriter]:
    """Load credentials, install the redactor, and build a paced client."""
    store = load_credentials(ROOT / ".env")
    missing = store.missing()
    if missing:
        raise SystemExit(f"credentials absent: {missing}")
    caps = dict(PROVISIONAL_DAILY_CAPS)
    ledger = RequestLedger(DATA / "requests.jsonl", caps)
    client = PacedClient(ledger, dict(CONSERVATIVE_SPACING_S), timeout_s=60.0)
    seal = SealedWriter(
        DATA / "sealed_credentialed", AppendOnlyLedger(DATA / "seals.jsonl")
    )
    return store, client, seal


def send(client: PacedClient, request: VendorRequest) -> Response:
    """Send one built request. Headers go out; they are never recorded."""
    return client.get(
        request.url,
        vendor=request.vendor,
        pace_key=request.pace_key,
        headers=request.headers,
    )


def record_body(response: Response, limit: int = 700) -> str:
    """The recording policy for a response body, and the reason for it.

    **A refusal is recorded verbatim. A served payload is not recorded at all.**

    `docs/ACCESS.md` exists to carry refusal payloads verbatim, and a refusal
    carries no bar. A **served** payload carries bars, and a bar value written
    into a report, a console line or a commit has left the sealed writer — which
    is the one thing Stage A does not do. So the policy is asymmetric on
    purpose, and it is asymmetric on the axis that matters: **status code**,
    which is itself a readable field.

    What is recorded for a served payload instead: its byte count, its SHA-256,
    and its bar count, all three on the readable field list.
    """
    if 200 <= response.status_code < 300:
        return "<served payload, not recorded: a bar value never leaves the seal>"
    return response.refusal_fragment(limit)


def probe_row(
    label: str, request: VendorRequest, response: Response, sha256: str
) -> dict[str, object]:
    """One probe's recordable row. Readable fields and counts only."""
    return {
        "probe": label,
        "vendor": request.vendor,
        "pace_key": request.pace_key,
        "url": response.url,
        "status_code": response.status_code,
        "served_byte_count": response.byte_count,
        "stored_byte_count": response.stored_byte_count,
        "redaction_changed_the_body": response.redaction_changed_the_body,
        "bar_count": count_bars(response.body),
        "latency_s": round(response.elapsed_s, 3),
        "health": response.health.value,
        "sha256": sha256,
        "sent_at": response.sent_at,
        "body_redacted": record_body(response),
    }


def write_report(name: str, payload: Any) -> Path:
    """Write a JSON report. The payload is already redacted at its boundaries."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    target = REPORTS / name
    target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    say(f"wrote {target}")
    return target
