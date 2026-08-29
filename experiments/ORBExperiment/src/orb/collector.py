"""A.3 TASK 1 and TASK 2 — the durable collector and the actions watcher.

**Built and left inert.** Section 0 fired `PENDING_ACCESS` on 2026-08-29, and
Stage A.3 is registered as armed *only on GO or DEGRADED*. Nothing here runs on
a timer today; the units exist and are not enabled.

What it does when armed: pulls the prior session's regular-session 1-minute bars
for the registered universe each evening, **diffs each pull against the last
sealed manifest**, and on a changed bar for a **closed** session appends a
revision row carrying **both hashes and both pull timestamps**.

Two rules that are not negotiable and are pinned by test:

- **A 429 or a 5xx writes a loud error marker and is never read as no-data.**
  Standing rule 7: operational health and sample composition never merge.
- **The prior session's manifest is sealed at the daily pass, and the open
  session is never sealed.** The solattn ADR-019 shape: a seal must attest a day
  that is closed and final, and an attestation of the wrong content is worth
  less than no attestation.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from typing import final

from orb.callstate import CompositionState, HealthState
from orb.ledger import AppendOnlyLedger


class SealedOpenSessionError(RuntimeError):
    """Raised when a pass tries to seal a session that has not closed."""


@final
@dataclass(frozen=True, slots=True)
class PullOutcome:
    """One request's result. Health and composition are recorded separately."""

    key: str
    health: HealthState
    composition: CompositionState | None
    status_code: int
    sha256: str | None
    pulled_at: str

    def is_error_marker(self) -> bool:
        """A 429 or a 5xx. **Never a no_data.**"""
        return self.health in {HealthState.RATE_LIMITED, HealthState.SOURCE_FAILED}


def classify(
    status_code: int, body: bytes, refusal_markers: tuple[bytes, ...]
) -> HealthState:
    """Health from the status code **and** the body.

    The body matters because A.1 TASK 1 measured a vendor serving a **refusal at
    HTTP 200**: Alpha Vantage's demo key returns `200` with an `Information`
    string and no series, and its delisted query returns a 2-byte `{}`. A
    status-code-only classifier records `stored` for both and then counts a
    session with zero bars — the exact health/composition merge Guard 4 exists
    to prevent. Recorded as ADR-008.
    """
    if status_code == 429:
        return HealthState.RATE_LIMITED
    if status_code >= 500 or status_code == 0:
        return HealthState.SOURCE_FAILED
    if status_code >= 400:
        return HealthState.SOURCE_FAILED
    if not body or body.strip() in {b"{}", b"[]"}:
        return HealthState.NO_DATA
    if any(marker in body for marker in refusal_markers):
        return HealthState.SOURCE_FAILED
    return HealthState.STORED


def seal_closed_session(
    ledger: AppendOnlyLedger,
    session: date,
    now: datetime,
    payloads: Mapping[str, bytes],
) -> str:
    """Seal a **closed** session's manifest. The open session is never sealed."""
    if session >= now.date():
        raise SealedOpenSessionError(
            f"refusing to seal {session.isoformat()}: the session has not closed "
            f"as of {now.isoformat()}. A seal attests a day that is final."
        )
    digest = hashlib.sha256()
    for key in sorted(payloads):
        digest.update(key.encode("utf-8"))
        digest.update(hashlib.sha256(payloads[key]).digest())
    manifest = digest.hexdigest()
    ledger.append(
        {
            "kind": "session_seal",
            "session_date": session.isoformat(),
            "manifest_sha256": manifest,
            "bar_files": len(payloads),
            "sealed_at": now.isoformat(timespec="seconds"),
        }
    )
    return manifest


def diff_against_manifest(
    previous: Mapping[str, str],
    current: Mapping[str, bytes],
    previous_pulled_at: str,
    current_pulled_at: str,
) -> list[dict[str, object]]:
    """Revision rows for a **closed** session, carrying both hashes and times.

    A vendor that rewrites a closed session's bars is the MLCryptoEngine H11
    hazard in a different costume, and this is where it becomes a measurement
    rather than a discovery.
    """
    rows: list[dict[str, object]] = []
    for key in sorted(set(previous) | set(current)):
        before = previous.get(key)
        after = hashlib.sha256(current[key]).hexdigest() if key in current else None
        if before != after:
            rows.append(
                {
                    "kind": "bar_revision",
                    "key": key,
                    "sha256_before": before,
                    "sha256_after": after,
                    "pulled_at_before": previous_pulled_at,
                    "pulled_at_after": current_pulled_at,
                    "disappeared": after is None,
                    "appeared": before is None,
                }
            )
    return rows
