"""A.1 Task 4: the as-printed observability verdict. Two measurements, both first-class.

Neither leg reads an outcome. The archive leg counts captures per US trading
day; the revision leg compares a first-served flow value against the value
standing 48 hours later. Flow is signal, so both are readable.

- **Archive capture density (retro).** The share of out-of-sample US trading
  days for which at least one archive capture exists strictly between the print
  window and the entry anchor. Bar: at least 60 percent.
- **Forward revision integrity.** The share of days on which a revision leaves
  the signal's sign and its position relative to the 100M threshold intact.
  Bar: at least 90 percent. The sign-flip and threshold-cross rates are the
  figures that matter, because they are the ones that would corrupt the test
  toward a false positive.

PASS means both hold. PARTIAL means one holds and the other does not, demoting
the retro cohort to descriptive with the forward cohort carrying the verdict
alone. FAIL means neither holds.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from etf.config import CONFIG


class Observability(StrEnum):
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    FAIL = "FAIL"


@dataclass(frozen=True, slots=True)
class ObservabilityVerdict:
    verdict: Observability
    archive_density_share: float
    archive_density_n: int
    revision_intact_share: float
    revision_n: int
    rationale: str

    def retro_cohort_is_descriptive_only(self) -> bool:
        """Under anything but a full PASS the retro cohort carries no verdict."""
        return self.verdict is not Observability.PASS


def _share(numerator: int, denominator: int, label: str) -> float:
    if denominator <= 0:
        raise ValueError(
            f"{label}: a share over zero days is an absence, not a number. "
            "Record the absence and report the reason."
        )
    return numerator / denominator


def fire_observability(
    *,
    archive_admissible_days: int,
    archive_trading_days: int,
    revision_intact_days: int,
    revision_days: int,
) -> ObservabilityVerdict:
    """Fire the registered A.1 Task 4 verdict from two measured shares."""
    density = _share(archive_admissible_days, archive_trading_days, "archive capture density")
    intact = _share(revision_intact_days, revision_days, "forward revision integrity")
    density_ok = density >= CONFIG.archive_density_pass_share
    intact_ok = intact >= CONFIG.revision_intact_pass_share

    if density_ok and intact_ok:
        verdict = Observability.PASS
        rationale = (
            f"archive capture density {density:.4f} (n = {archive_trading_days} out-of-sample "
            f"trading days) at or above the registered {CONFIG.archive_density_pass_share:.2f} "
            f"bar, and forward revision integrity {intact:.4f} (n = {revision_days} days with "
            f"at least two captures) at or above the registered "
            f"{CONFIG.revision_intact_pass_share:.2f} bar. Both cohorts carry the verdict."
        )
    elif density_ok or intact_ok:
        verdict = Observability.PARTIAL
        failed = "forward revision integrity" if density_ok else "archive capture density"
        value = intact if density_ok else density
        bar = CONFIG.revision_intact_pass_share if density_ok else CONFIG.archive_density_pass_share
        n = revision_days if density_ok else archive_trading_days
        rationale = (
            f"{failed} {value:.4f} (n = {n}) misses its registered {bar:.2f} bar while the other "
            f"leg holds. The retro cohort is demoted to descriptive and the forward cohort "
            f"carries the verdict alone."
        )
    else:
        verdict = Observability.FAIL
        rationale = (
            f"both legs miss their bars: archive capture density {density:.4f} "
            f"(n = {archive_trading_days}) against {CONFIG.archive_density_pass_share:.2f}, and "
            f"forward revision integrity {intact:.4f} (n = {revision_days}) against "
            f"{CONFIG.revision_intact_pass_share:.2f}. No admissible as-printed cohort exists."
        )
    return ObservabilityVerdict(
        verdict=verdict,
        archive_density_share=density,
        archive_density_n=archive_trading_days,
        revision_intact_share=intact,
        revision_n=revision_days,
        rationale=rationale,
    )
