"""The power gate. It reads a bucket count and a dispersion, and nothing else.

REGISTRATION.md Section 0.3 defines the verdict map this module fires and
Section 9 the arithmetic. No field carrying a market's resolution ever enters
this module: tests/test_guards.py scans it and fails if one appears, and that
guard is verified by mutation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum

from pmexperiment import registry


class Verdict(Enum):
    """The registered verdict rows of REGISTRATION.md Section 0.3."""

    GO = "GO"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class GateReading:
    """One gate firing for one cell, preserved as fired."""

    cell: str
    tail_count: float
    mean_dispersion: float
    mde: float | None
    verdict: Verdict


def minimum_detectable_effect(
    tail_count: float, mean_dispersion: float
) -> float | None:
    """MDE = z * sqrt(v̄ / n). None when the cell is empty (nothing detectable)."""
    if tail_count <= 0:
        return None
    if mean_dispersion <= 0:
        raise ValueError("a non-empty cell must carry a positive dispersion")
    return registry.Z_CRITICAL * math.sqrt(mean_dispersion / tail_count)


def fire_power_gate(
    cell: str, tail_count: float, mean_dispersion: float
) -> GateReading:
    """Map a cell's MDE to the registered verdict.

    Boundaries are inclusive at the lower edge, following Insider: an MDE of
    exactly EFFECT_BAND_LO is GO, exactly EFFECT_BAND_HI is DEGRADED.
    """
    mde = minimum_detectable_effect(tail_count, mean_dispersion)
    if mde is None:
        verdict = Verdict.BLOCKED
    elif mde <= registry.EFFECT_BAND_LO:
        verdict = Verdict.GO
    elif mde <= registry.EFFECT_BAND_HI:
        verdict = Verdict.DEGRADED
    else:
        verdict = Verdict.BLOCKED
    return GateReading(
        cell=cell,
        tail_count=tail_count,
        mean_dispersion=mean_dispersion,
        mde=mde,
        verdict=verdict,
    )


def cost_floor(entry_price: float) -> float:
    """C(p) = fees + half-spread + FX on committed capital (Sections 2 and 11)."""
    if not 0.0 < entry_price < 1.0:
        raise ValueError("entry price must sit strictly inside (0, 1) dollars")
    return (
        registry.FEE_PER_SIDE_USD * registry.FEE_SIDES
        + registry.HALF_SPREAD_USD
        + registry.FX_PER_DIRECTION * registry.FX_DIRECTIONS * entry_price
    )
