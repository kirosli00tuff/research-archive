"""The H5 outcome map (Section 6), built dark and fired from counts only.

Three terminal states — VIABLE, INDETERMINATE, CLOSED — plus one
non-terminal PENDING for a census window that is still open. The map judges
**venue-served deviation and field service**. It says nothing about returns,
tradability, or capital (Section 8).

The thresholds are arithmetic on the registered cost band, not free numbers:
the HIP-3 round-trip taker central of `CONFIG.hip3_round_trip_bp[1]` is the
**18 bp cost floor**, and the VIABLE bar is
`h5_viable_basis_multiple` times it — **3 x 18 = 54 bp**.

One asymmetry is registered here and enforced. A deviation series the venue
serves under a *different construction* from the registered basis (an
impact-price premium index, say, rather than mark against oracle) is a
**named secondary**: it may fire CLOSED, because a venue whose own deviation
bookkeeping never clears the cost floor leaves nothing for a better feed to
rescue, and it may **never** fire VIABLE, because a large differently-built
number could be an artefact of that construction rather than a deviation of
the registered kind.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Final

from npl.absence import Maybe, is_absent
from npl.config import CONFIG, Config

STATE_VIABLE: Final = "VIABLE"
STATE_INDETERMINATE: Final = "INDETERMINATE"
STATE_CLOSED: Final = "CLOSED"
STATE_PENDING: Final = "PENDING"

TERMINAL_STATES: Final[tuple[str, ...]] = (STATE_VIABLE, STATE_INDETERMINATE, STATE_CLOSED)

SERIES_REGISTERED_BASIS: Final = "registered_basis"
SERIES_SECONDARY_DEVIATION: Final = "secondary_deviation"
REGISTERED_SERIES_KINDS: Final[tuple[str, ...]] = (
    SERIES_REGISTERED_BASIS,
    SERIES_SECONDARY_DEVIATION,
)


class UnregisteredSeriesKind(ValueError):
    """A series kind outside the registered two reached the map. Refused."""


@dataclass(frozen=True, slots=True)
class Verdict:
    """One firing of the map, with every input figure beside the state."""

    state: str
    series_kind: str
    reasons: tuple[str, ...]
    instruments_with_reference: int
    instruments_meeting_coverage: int
    funding_served_instruments: int
    funding_share: float
    median_abs_bp_by_tag: dict[str, float] = field(default_factory=dict)
    n_by_tag: dict[str, int] = field(default_factory=dict)
    max_median_abs_bp: float | None = None
    floor_bp: float = 0.0
    viable_bp: float = 0.0


def cost_floor_bp(cfg: Config = CONFIG) -> float:
    """18 bp: the HIP-3 round-trip taker central of the registered cost band."""
    return cfg.hip3_round_trip_bp[1]


def viable_threshold_bp(cfg: Config = CONFIG) -> float:
    """54 bp: three times the cost floor, stated as the arithmetic it is."""
    return cost_floor_bp(cfg) * cfg.h5_viable_basis_multiple


def fire(
    *,
    series_kind: str,
    instruments_with_reference: int,
    instruments_meeting_coverage: int,
    median_abs_bp_by_tag: Mapping[str, Maybe[float]],
    n_by_tag: Mapping[str, int],
    funding_served_instruments: int,
    cfg: Config = CONFIG,
) -> Verdict:
    """Fire the registered map. Counts and medians only; no return is read."""
    if series_kind not in REGISTERED_SERIES_KINDS:
        raise UnregisteredSeriesKind(
            f"{series_kind!r} is not a registered series kind; the map admits "
            f"{list(REGISTERED_SERIES_KINDS)}"
        )
    floor = cost_floor_bp(cfg)
    viable = viable_threshold_bp(cfg)
    present = {
        tag: value
        for tag, value in median_abs_bp_by_tag.items()
        if not is_absent(value) and isinstance(value, float)
    }
    funding_share = (
        funding_served_instruments / instruments_with_reference
        if instruments_with_reference > 0
        else 0.0
    )
    max_median = max(present.values()) if present else None

    closed: list[str] = []
    if instruments_with_reference < cfg.h5_min_instruments_with_reference:
        closed.append(
            f"only {instruments_with_reference} instruments carry a served reference, "
            f"against the registered bar of {cfg.h5_min_instruments_with_reference}"
        )
    if funding_share < cfg.h5_funding_service_share:
        closed.append(
            f"funding is served on {funding_served_instruments} of "
            f"{instruments_with_reference} reference-carrying instruments "
            f"({funding_share:.3f}), under the registered "
            f"{cfg.h5_funding_service_share:.2f} share"
        )
    if present and all(value < floor for value in present.values()):
        closed.append(
            f"the median absolute basis is under the {floor:.0f} bp cost floor in every "
            f"session tag (max {max(present.values()):.2f} bp over "
            f"{len(present)} tag(s))"
        )

    def build(state: str, reasons: list[str]) -> Verdict:
        return Verdict(
            state=state,
            series_kind=series_kind,
            reasons=tuple(reasons),
            instruments_with_reference=instruments_with_reference,
            instruments_meeting_coverage=instruments_meeting_coverage,
            funding_served_instruments=funding_served_instruments,
            funding_share=funding_share,
            median_abs_bp_by_tag=dict(present),
            n_by_tag=dict(n_by_tag),
            max_median_abs_bp=max_median,
            floor_bp=floor,
            viable_bp=viable,
        )

    if closed:
        return build(STATE_CLOSED, closed)
    if instruments_meeting_coverage < cfg.h5_min_instruments_with_reference:
        return build(
            STATE_PENDING,
            [
                f"{instruments_meeting_coverage} instruments carry a served reference AND "
                f"{cfg.h5_min_coverage_days} days of coverage, against the registered bar "
                f"of {cfg.h5_min_instruments_with_reference}; the census window is open"
            ],
        )
    if max_median is None:
        return build(STATE_PENDING, ["no session tag carries a served median; nothing to fire on"])
    if max_median > viable:
        if series_kind == SERIES_SECONDARY_DEVIATION:
            return build(
                STATE_INDETERMINATE,
                [
                    f"the secondary deviation series reaches {max_median:.2f} bp median "
                    f"absolute, over the {viable:.0f} bp bar, but a named secondary may "
                    f"never fire VIABLE: it is differently constructed from the registered "
                    f"basis, so the size could be an artefact of that construction"
                ],
            )
        return build(
            STATE_VIABLE,
            [
                f"the median absolute basis reaches {max_median:.2f} bp in at least one "
                f"session tag, over the {viable:.0f} bp bar ({cfg.h5_viable_basis_multiple:g} "
                f"x the {floor:.0f} bp floor); {instruments_meeting_coverage} instruments "
                f"meet the coverage bar and funding is served on "
                f"{funding_served_instruments} of them"
            ],
        )
    return build(
        STATE_INDETERMINATE,
        [
            f"the coverage bars are met ({instruments_meeting_coverage} instruments) and the "
            f"median absolute basis sits at {max_median:.2f} bp, between the {floor:.0f} bp "
            f"floor and the {viable:.0f} bp bar"
        ],
    )
