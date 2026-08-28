"""The registered H5 measurement definitions (Section 3). No outcome field.

Basis is **perp mark minus reference over reference, in basis points,
computed only from fields the venue serves in the same snapshot**. The "same
snapshot" half of that sentence is enforced, not documented: every served
number carries the id of the snapshot it came from, and a basis built across
two snapshots is a loud refusal.

The registered field names, fixed before any price was read:

- the mark is ``markPx`` and nothing else;
- the reference is the first served of ``oraclePx`` then ``indexPx`` — the
  venue's own oracle or index price — and which one was used is recorded per
  instrument;
- ``midPx``, ``prevDayPx`` and ``impactPxs`` are **registered non-references**:
  book and mark state, not a reference, and substituting one for an unserved
  oracle is exactly the defect the honesty clause (Section 4) exists for.

Funding is recorded as **service**, never as a value: this module reports
whether the venue carries a funding field for an instrument and never reads
the number, so no H5 path can read a funding rate stamped after any
registered event entry.
"""

from __future__ import annotations

import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from npl.absence import NON_FINITE, NOT_SERVED, ZERO_DENOMINATOR, Absent, Maybe, is_absent

MARK_FIELD: Final = "markPx"
REFERENCE_FIELDS: Final[tuple[str, ...]] = ("oraclePx", "indexPx")
NON_REFERENCE_FIELDS: Final[tuple[str, ...]] = ("midPx", "prevDayPx", "impactPxs")
OPEN_INTEREST_FIELD: Final = "openInterest"
DAY_VOLUME_FIELD: Final = "dayNtlVlm"
FUNDING_FIELD: Final = "funding"

BP: Final = 1e4


class CrossSnapshotBasis(RuntimeError):
    """A basis was asked for across two snapshots. Refused; nothing computed."""


class AssetContextShape(RuntimeError):
    """A metaAndAssetCtxs payload arrived in a shape this parser refuses to guess."""


@dataclass(frozen=True, slots=True)
class Served:
    """One number the venue served, with the field and snapshot it came from."""

    value: float
    field: str
    snapshot_id: str


@dataclass(frozen=True, slots=True)
class AssetContext:
    """One instrument's venue-served state in one snapshot. No outcome field."""

    coin: str
    dex: str
    snapshot_id: str
    at_ms: int
    served_fields: tuple[str, ...]
    mark: Maybe[Served]
    reference: Maybe[Served]
    open_interest: Maybe[float]
    day_notional_volume: Maybe[float]
    funding_served: bool

    @property
    def reference_field(self) -> str | None:
        return self.reference.field if isinstance(self.reference, Served) else None


def _served_number(ctx: dict[str, object], field: str, snapshot_id: str) -> Maybe[Served]:
    raw = ctx.get(field)
    if raw is None:
        return NOT_SERVED
    try:
        value = float(str(raw))
    except (TypeError, ValueError):
        return NOT_SERVED
    if not math.isfinite(value):
        return NON_FINITE
    return Served(value=value, field=field, snapshot_id=snapshot_id)


def _served_scalar(ctx: dict[str, object], field: str) -> Maybe[float]:
    raw = ctx.get(field)
    if raw is None:
        return NOT_SERVED
    try:
        value = float(str(raw))
    except (TypeError, ValueError):
        return NOT_SERVED
    return value if math.isfinite(value) else NON_FINITE


def pick_reference(ctx: dict[str, object], snapshot_id: str) -> Maybe[Served]:
    """First served of the registered reference fields, in registered order."""
    for field in REFERENCE_FIELDS:
        found = _served_number(ctx, field, snapshot_id)
        if isinstance(found, Served):
            return found
    return NOT_SERVED


def parse_asset_contexts(
    payload: bytes | str, dex: str, snapshot_id: str, at_ms: int
) -> tuple[AssetContext, ...]:
    """Parse one metaAndAssetCtxs response into per-instrument served state.

    The venue serves `[meta, [ctx, ...]]` with the two lists positionally
    aligned. A length mismatch is a refusal, never a zip that silently
    truncates and mislabels every instrument after the gap.
    """
    parsed = json.loads(payload)
    if not isinstance(parsed, list) or len(parsed) != 2:
        raise AssetContextShape(
            f"metaAndAssetCtxs payload is not a two-element list "
            f"({type(parsed).__name__}); refusing to guess"
        )
    meta, ctxs = parsed
    if not isinstance(meta, dict) or "universe" not in meta or not isinstance(ctxs, list):
        raise AssetContextShape("metaAndAssetCtxs carries no universe/contexts pair; refusing")
    universe = meta["universe"]
    if len(universe) != len(ctxs):
        raise AssetContextShape(
            f"metaAndAssetCtxs universe has {len(universe)} rows against {len(ctxs)} "
            f"contexts; the positional alignment is broken and nothing here guesses"
        )
    out: list[AssetContext] = []
    for row, ctx in zip(universe, ctxs, strict=True):
        if not isinstance(row, dict) or not isinstance(ctx, dict):
            raise AssetContextShape("metaAndAssetCtxs row is not an object; refusing to guess")
        # The venue already serves the dex prefix inside `name` on a HIP-3 dex
        # (measured 2026-08-28: `{"name": "xyz:XYZ100", ...}`), so the coin is
        # the served name verbatim. Re-prefixing here would invent `xyz:xyz:...`
        # and silently detach every H5 row from the census and the cohorts.
        coin = str(row["name"])
        out.append(
            AssetContext(
                coin=coin,
                dex=dex,
                snapshot_id=snapshot_id,
                at_ms=at_ms,
                served_fields=tuple(sorted(str(k) for k in ctx)),
                mark=_served_number(ctx, MARK_FIELD, snapshot_id),
                reference=pick_reference(ctx, snapshot_id),
                open_interest=_served_scalar(ctx, OPEN_INTEREST_FIELD),
                day_notional_volume=_served_scalar(ctx, DAY_VOLUME_FIELD),
                funding_served=FUNDING_FIELD in ctx,
            )
        )
    return tuple(out)


def basis_bp(mark: Maybe[Served], reference: Maybe[Served]) -> Maybe[float]:
    """(mark - reference) / reference in bp, from one snapshot or not at all."""
    if is_absent(mark):
        return NOT_SERVED
    if is_absent(reference):
        return NOT_SERVED
    assert isinstance(mark, Served) and isinstance(reference, Served)
    if mark.snapshot_id != reference.snapshot_id:
        raise CrossSnapshotBasis(
            f"refusing a basis from {mark.field}@{mark.snapshot_id} against "
            f"{reference.field}@{reference.snapshot_id}: Section 3 admits only fields "
            f"the venue served in the same snapshot."
        )
    if reference.value == 0.0:
        return ZERO_DENOMINATOR
    value = (mark.value - reference.value) / reference.value * BP
    return value if math.isfinite(value) else NON_FINITE


def context_basis_bp(ctx: AssetContext) -> Maybe[float]:
    """One instrument's basis from its own snapshot."""
    return basis_bp(ctx.mark, ctx.reference)


def basis_series(contexts: Sequence[AssetContext]) -> tuple[Maybe[float], ...]:
    """One basis per snapshot, in order. An absent reference stays absent.

    Nothing here carries the last served reference forward, back-fills, or
    interpolates: a gap is a recorded absence and the n drops by one.
    """
    out: list[Maybe[float]] = []
    for ctx in contexts:
        out.append(context_basis_bp(ctx))
    return tuple(out)


def present_values(values: Sequence[Maybe[float]]) -> tuple[float, ...]:
    """The served numbers only. Absences are dropped, never coerced to zero."""
    return tuple(v for v in values if not is_absent(v) and isinstance(v, float))


def absence_reasons(values: Sequence[Maybe[float]]) -> dict[str, int]:
    """How many observations were absent, by recorded reason."""
    counts: dict[str, int] = {}
    for value in values:
        if isinstance(value, Absent):
            counts[value.reason.value] = counts.get(value.reason.value, 0) + 1
    return counts
