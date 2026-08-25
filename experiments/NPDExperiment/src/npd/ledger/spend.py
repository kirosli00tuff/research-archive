"""Append-only spend ledger and the projected-spend refusal.

The cap is the lower of the registered figure and whatever the account has
left, because the registered figure is a leftover balance rather than a
dedicated budget. The account side is unknowable from here until the API says
insufficient_quota, so that error is a clean stop rather than a failure.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass
from pathlib import Path

from npd.config import CONFIG, Config
from npd.ledger.append_only import AppendOnlyLedger
from npd.paths import SPEND_LEDGER


class SpendRefused(RuntimeError):
    """A batch was refused because completing it would cross the cap."""


class QuotaExhausted(RuntimeError):
    """The account ran out of balance. A clean stop, not a failure."""


@dataclass(frozen=True, slots=True)
class SpendRow:
    ts: str
    date: str
    kind: str
    input_tokens: int
    cached_input_tokens: int
    output_tokens: int
    cost_usd: float
    note: str


def cost_of(
    input_tokens: int,
    cached_input_tokens: int,
    output_tokens: int,
    cfg: Config = CONFIG,
) -> float:
    """Cost in USD at the registered list rates.

    Cached input bills at the cached rate and is not double counted, so the
    uncached portion is input minus cached.
    """
    uncached = max(0, input_tokens - cached_input_tokens)
    return (
        uncached / 1e6 * cfg.price_input_per_mtok_usd
        + cached_input_tokens / 1e6 * cfg.price_cached_input_per_mtok_usd
        + output_tokens / 1e6 * cfg.price_output_per_mtok_usd
    )


class SpendLedger:
    """Every cent, recorded before the next call goes out."""

    def __init__(self, path: Path = SPEND_LEDGER, cfg: Config = CONFIG) -> None:
        self._ledger = AppendOnlyLedger(path)
        self._cfg = cfg

    @property
    def path(self) -> Path:
        return self._ledger.path

    def record(
        self,
        *,
        date: str,
        kind: str,
        input_tokens: int,
        cached_input_tokens: int,
        output_tokens: int,
        note: str = "",
    ) -> SpendRow:
        row = SpendRow(
            ts=dt.datetime.now(dt.UTC).isoformat(),
            date=date,
            kind=kind,
            input_tokens=input_tokens,
            cached_input_tokens=cached_input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_of(input_tokens, cached_input_tokens, output_tokens, self._cfg),
            note=note,
        )
        self._ledger.append(asdict(row))
        return row

    def total_usd(self) -> float:
        return sum(float(r.get("cost_usd", 0.0)) for r in self._ledger.iter_rows())

    def n_calls(self, kind: str | None = None) -> int:
        return sum(1 for r in self._ledger.iter_rows() if kind is None or r.get("kind") == kind)

    def remaining_usd(self) -> float:
        return self._cfg.spend_cap_usd - self.total_usd()

    def mean_cost_per_call(self, kind: str) -> float | None:
        """Measured cost per call of one kind, or None when none have run."""
        costs = [float(r["cost_usd"]) for r in self._ledger.iter_rows() if r.get("kind") == kind]
        if not costs:
            return None
        return sum(costs) / len(costs)

    def refuse_if_projection_crosses_cap(
        self, *, calls_in_batch: int, projected_cost_per_call: float
    ) -> None:
        """Refuse a batch whose completion would cross the cap.

        Checked before the batch, not after, so the cap is never crossed and
        then reported. The projection uses measured cost per call once any
        call has run, and the registered estimate before that.
        """
        projected = calls_in_batch * projected_cost_per_call
        if self.total_usd() + projected > self._cfg.spend_cap_usd:
            raise SpendRefused(
                f"batch of {calls_in_batch} at {projected_cost_per_call:.5f} USD per call "
                f"projects {projected:.4f} USD on top of {self.total_usd():.4f} already spent, "
                f"crossing the {self._cfg.spend_cap_usd:.2f} USD cap. Refused before sending."
            )
