"""A paced HTTP client. Charges the request ledger **before** it sends.

Pacing is keyed **per endpoint, never per host** (solattn ADR-021: one endpoint
refused 47.5 percent of n = 1,863 attempts while a second endpoint on the same
host and the same IP took 0 of 360). An endpoint nobody has measured keeps its
vendor's figure rather than a faster default: **an unmeasured endpoint is not a
licence to speed up.**

The client returns a status code, a byte count and an elapsed time. **It never
parses a response body.** The bytes go to a sealed writer.
"""

from __future__ import annotations

import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final, final

from orb.callstate import HealthState
from orb.ledger import RequestLedger
from orb.redact import redact_data, redact_text

USER_AGENT: Final[str] = (
    "ORBExperiment/0.1 (measurement-only research; no automated collection "
    "against a stated prohibition)"
)

DEFAULT_MIN_SPACING_S: Final[float] = 6.0
"""The conservative default for an endpoint nobody has measured."""


@final
@dataclass(frozen=True, slots=True)
class Response:
    """What a probe returns. Status, counts and timing. No body is parsed."""

    url: str
    status_code: int
    byte_count: int
    """Bytes the vendor served, counted **before** redaction. A measurement."""
    elapsed_s: float
    body: bytes
    health: HealthState
    sent_at: str

    def __post_init__(self) -> None:
        """Guard 8. A Response is a recorded object, so it is redacted on birth.

        The URL carries the key for a query-parameter vendor and the body
        carries it for any vendor that echoes the request back inside an error.
        Redacting **here** rather than at each call site means a Response
        constructed by any caller, in any tool, is already safe to record.
        """
        object.__setattr__(self, "url", redact_text(self.url))
        object.__setattr__(self, "body", redact_data(self.body))

    @property
    def stored_byte_count(self) -> int:
        """Bytes after redaction — what a sealed writer would store."""
        return len(self.body)

    @property
    def redaction_changed_the_body(self) -> bool:
        """A length-based indicator that a credential was echoed back.

        It is an **indicator, not a proof**: the raw body is gone by the time
        anything can ask, and a placeholder that happened to match its secret's
        length would not register. None of the three registered placeholders
        matches its secret's length, so it registers for all three today. It is
        recorded as a finding shape rather than relied on as a guarantee.
        """
        return self.stored_byte_count != self.byte_count

    def refusal_fragment(self, limit: int = 400) -> str:
        """The first bytes of a refusal, decoded lossily, for the record."""
        return self.body[:limit].decode("utf-8", errors="replace")


@final
class PacedClient:
    """Paces per endpoint, charges the ledger before sending, parses nothing."""

    __slots__ = ("_last_sent", "_ledger", "_spacing", "_timeout")

    def __init__(
        self,
        ledger: RequestLedger,
        spacing_s: dict[str, float] | None = None,
        timeout_s: float = 30.0,
    ) -> None:
        self._ledger = ledger
        self._spacing = dict(spacing_s or {})
        self._last_sent: dict[str, float] = {}
        self._timeout = timeout_s

    def spacing_for(self, pace_key: str) -> float:
        return self._spacing.get(pace_key, DEFAULT_MIN_SPACING_S)

    def _wait(self, pace_key: str) -> None:
        last = self._last_sent.get(pace_key)
        if last is None:
            return
        gap = self.spacing_for(pace_key) - (time.monotonic() - last)
        if gap > 0:
            time.sleep(gap)

    def get(self, url: str, *, vendor: str, pace_key: str) -> Response:
        """Charge, pace, send. The charge happens first, and can refuse."""
        day = datetime.now(tz=UTC).strftime("%Y-%m-%d")
        self._ledger.charge(vendor, day, pace_key)
        self._wait(pace_key)

        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        sent_at = datetime.now(tz=UTC).isoformat(timespec="milliseconds")
        started = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as handle:
                body = handle.read()
                status = int(handle.status)
            health = HealthState.STORED if body else HealthState.NO_DATA
        except urllib.error.HTTPError as exc:
            body = exc.read()
            status = int(exc.code)
            health = (
                HealthState.RATE_LIMITED if status == 429 else HealthState.SOURCE_FAILED
            )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            body = str(exc).encode("utf-8")
            status = 0
            health = HealthState.SOURCE_FAILED
        finally:
            self._last_sent[pace_key] = time.monotonic()

        return Response(
            url=url,
            status_code=status,
            byte_count=len(body),
            elapsed_s=time.monotonic() - started,
            body=body,
            health=health,
            sent_at=sent_at.replace("+00:00", "Z"),
        )
