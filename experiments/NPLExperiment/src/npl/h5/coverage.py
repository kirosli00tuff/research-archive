"""H5's own coverage accounting: the six call states, never merged, never absent.

Separate from `npl.coverage`, which counts H1/H2 outcome-window rows. This
module counts **one H5 pass**: how many instruments were planned, what
terminal state each probe reached, and how many carried a served reference,
a served funding field, and a computable basis.

Every one of the six registered call states appears in the result **even at
zero**. An omitted key reads as "no such state"; a zero reads as "measured,
and none". Operational health and sample composition never merge here
either: `rate_limited` and `source_failed` are the instrument refusing,
`excluded_ineligible` is a registered rule narrowing, and they are counted
apart.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from npl.callstate import ALL_STATES, CallState
from npl.h5.census import InstrumentRow
from npl.h5.listing import STATUS_LIVE


@dataclass(frozen=True, slots=True)
class PassCoverage:
    """One H5 pass, accounted. Every figure travels with its n."""

    pass_id: str
    at_ms: int
    session_tag: str
    instruments_enumerated: int
    instruments_resolved: int
    instruments_live: int
    instruments_probed: int
    ctx_states: dict[str, int] = field(default_factory=dict)
    funding_states: dict[str, int] = field(default_factory=dict)
    l2_states: dict[str, int] = field(default_factory=dict)
    reference_served: int = 0
    reference_unserved: int = 0
    funding_field_served: int = 0
    basis_served: int = 0
    basis_absent_by_reason: dict[str, int] = field(default_factory=dict)


def _all_states(observed: Sequence[str]) -> dict[str, int]:
    """Counts over the six registered states, each present even at zero."""
    counts = {state.value: 0 for state in ALL_STATES}
    for value in observed:
        if value not in counts:
            raise ValueError(
                f"unregistered call state {value!r} in an H5 coverage view; the six "
                f"registered states are {[s.value for s in ALL_STATES]}"
            )
        counts[value] += 1
    return counts


def coverage_of(
    pass_id: str,
    at_ms: int,
    session_tag: str,
    rows: Sequence[InstrumentRow],
) -> PassCoverage:
    """Account one pass from its census rows. Counts and states only."""
    resolved = [r for r in rows if r.resolution_state == "resolved"]
    live = [r for r in resolved if r.listing_status == STATUS_LIVE]
    probed = [r for r in resolved if r.l2_state != CallState.EXCLUDED_INELIGIBLE.value]
    absent: dict[str, int] = {}
    for row in resolved:
        reason = row.basis_absence
        if reason:
            absent[reason] = absent.get(reason, 0) + 1
    return PassCoverage(
        pass_id=pass_id,
        at_ms=at_ms,
        session_tag=session_tag,
        instruments_enumerated=len(rows),
        instruments_resolved=len(resolved),
        instruments_live=len(live),
        instruments_probed=len(probed),
        ctx_states=_all_states([r.ctx_state for r in rows]),
        funding_states=_all_states([r.funding_history_state for r in resolved]),
        l2_states=_all_states([r.l2_state for r in resolved]),
        reference_served=sum(1 for r in resolved if r.reference_served),
        reference_unserved=sum(1 for r in resolved if not r.reference_served),
        funding_field_served=sum(1 for r in resolved if r.funding_field_served),
        basis_served=sum(1 for r in resolved if r.basis_bp is not None),
        basis_absent_by_reason=absent,
    )
