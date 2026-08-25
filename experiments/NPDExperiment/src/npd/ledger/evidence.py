"""Append-only evidence ledger. One row per call, raw response kept verbatim.

The raw response is stored exactly as it arrived. A later reader can reparse a
stored ranking without trusting this session's parser, which is what makes the
collection replayable.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from npd.callstate import CallState
from npd.ledger.append_only import AppendOnlyLedger
from npd.paths import EVIDENCE_LEDGER


@dataclass(frozen=True, slots=True)
class EvidenceRow:
    ts: str
    date: str
    state: str
    model: str
    attempt: int
    reasoning_effort: str
    input_tokens: int
    cached_input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    cost_usd: float
    latency_s: float
    raw_response: str
    detail: str


class EvidenceLedger:
    def __init__(self, path: Path = EVIDENCE_LEDGER) -> None:
        self._ledger = AppendOnlyLedger(path)

    @property
    def path(self) -> Path:
        return self._ledger.path

    def record(
        self,
        *,
        date: str,
        state: CallState,
        model: str,
        attempt: int,
        reasoning_effort: str = "",
        input_tokens: int = 0,
        cached_input_tokens: int = 0,
        output_tokens: int = 0,
        reasoning_tokens: int = 0,
        cost_usd: float = 0.0,
        latency_s: float = 0.0,
        raw_response: str = "",
        detail: str = "",
    ) -> EvidenceRow:
        row = EvidenceRow(
            ts=dt.datetime.now(dt.UTC).isoformat(),
            date=date,
            state=state.value,
            model=model,
            attempt=attempt,
            reasoning_effort=reasoning_effort,
            input_tokens=input_tokens,
            cached_input_tokens=cached_input_tokens,
            output_tokens=output_tokens,
            reasoning_tokens=reasoning_tokens,
            cost_usd=cost_usd,
            latency_s=latency_s,
            raw_response=raw_response,
            detail=detail,
        )
        self._ledger.append(asdict(row))
        return row

    def rows(self) -> list[dict[str, Any]]:
        return self._ledger.read().rows

    def terminal_state_by_date(self) -> dict[str, CallState]:
        """The last recorded state for each date. Drives idempotent resume."""
        out: dict[str, CallState] = {}
        for r in self._ledger.iter_rows():
            out[str(r["date"])] = CallState(r["state"])
        return out

    def last_row_by_date(self) -> dict[str, dict[str, Any]]:
        """The last recorded row for each date, whatever its state."""
        out: dict[str, dict[str, Any]] = {}
        for r in self._ledger.iter_rows():
            out[str(r["date"])] = r
        return out
