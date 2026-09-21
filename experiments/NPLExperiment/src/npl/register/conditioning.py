"""H4 conditioning: the pre-entry trailing-funding feature and its cells.

The conditioning feature is the signed trailing 168-hour mean hourly funding
at the event entry — pre-entry by construction (standing rule 13: a rate
stamped at or before its event entry is a feature, never an outcome), and
computed elsewhere through the same trailing-only path the H1 matcher uses
(npl.controls.trailing_mean, whose post-entry refusal is pinned by test).
This module is pure arithmetic over that feature: the registered threshold
grid, the at-or-below cell rule, and the Sidak correction within the
hypothesis. An absent trailing mean stays absent; it never enters a share.
"""

from __future__ import annotations

from dataclasses import dataclass

from npl.absence import Absent
from npl.config import CONFIG, Config

HOURS_PER_YEAR = 8760


@dataclass(frozen=True, slots=True)
class ThresholdCell:
    """One registered conditioning cell: at or below the signed threshold."""

    label: str
    annualized: float
    hourly: float


def threshold_cells(cfg: Config = CONFIG) -> tuple[ThresholdCell, ...]:
    """The registered grid, annualized percent per year -> mean hourly rate."""
    cells: list[ThresholdCell] = []
    for annualized in cfg.h4_funding_thresholds_annualized:
        if annualized >= 0.0:
            raise ValueError(
                f"the registered H4 grid is negative-funding conditioning; got {annualized}"
            )
        cells.append(
            ThresholdCell(
                label=f"le_{round(annualized * 100)}pct_ann",
                annualized=annualized,
                hourly=annualized / HOURS_PER_YEAR,
            )
        )
    return tuple(cells)


def cell_clears(trailing_mean_hourly: float, cell: ThresholdCell) -> bool:
    """At or below the signed threshold clears the cell (inclusive bound)."""
    return trailing_mean_hourly <= cell.hourly


def sidak_within(alpha_h: float, m: int) -> float:
    """The within-hypothesis Sidak correction across the m grid cells."""
    if not 0.0 < alpha_h < 1.0 or m < 1:
        raise ValueError(f"impossible correction inputs: alpha_h={alpha_h}, m={m}")
    return 1.0 - float((1.0 - alpha_h) ** (1.0 / m))


@dataclass(frozen=True, slots=True)
class CellShare:
    """One cell's conditioning rate over the fresh cohort, with its n."""

    label: str
    cleared: int
    measured_n: int
    absent_n: int

    def rate(self) -> float:
        if self.measured_n <= 0:
            return 0.0
        return self.cleared / self.measured_n


def conditioning_shares(
    trailing_means: list[float | Absent], cfg: Config = CONFIG
) -> tuple[CellShare, ...]:
    """Per-cell conditioning rates. Absent means are counted, never zeros."""
    cells = threshold_cells(cfg)
    present = [m for m in trailing_means if not isinstance(m, Absent)]
    absent_n = len(trailing_means) - len(present)
    return tuple(
        CellShare(
            label=cell.label,
            cleared=sum(1 for m in present if cell_clears(m, cell)),
            measured_n=len(present),
            absent_n=absent_n,
        )
        for cell in cells
    )
