"""The two bar-integrity verdicts. These are the experiment.

`A.1 TASK 3` measures the **bar revision rate** — the share of already-served
bars whose stored bytes change on an identical re-request after at least 14
calendar days. `A.1 TASK 4` measures **cross-vendor agreement** on the
first-5-minute high and low, which is the only disagreement that changes an
entry price, and **delisted-name coverage**, without which the universe is
survivor-only and every downstream figure is inflated beyond recovery.

Both verdicts are computed from counts and shares. **Neither reads a bar
value**: the sealed comparator supplies the aggregate rates and returns nothing
else.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, unique
from typing import final

from orb.config import CONFIG


@unique
class IntegrityVerdict(StrEnum):
    """Three states. PARTIAL is a recorded scope limitation, not a soft pass."""

    PASS = "PASS"
    PARTIAL = "PARTIAL"
    FAIL = "FAIL"


@final
@dataclass(frozen=True, slots=True)
class RevisionFinding:
    """The A.1 TASK 3 measurement. Every figure carries its n."""

    changed_bar_share: float
    bars_compared: int
    changed_bar_count: int
    session_ticker_pairs_compared: int
    pairs_with_changed_bar_count: int
    pairs_with_timestamp_change: int
    changes_coinciding_with_corporate_action: int
    wait_days_observed: int

    def verdict(self) -> IntegrityVerdict:
        """PASS at or below 0.5 percent; PARTIAL to 2.0 percent; FAIL above."""
        if self.changed_bar_share <= CONFIG.revision_pass_max_share:
            return IntegrityVerdict.PASS
        if self.changed_bar_share <= CONFIG.revision_partial_max_share:
            return IntegrityVerdict.PARTIAL
        return IntegrityVerdict.FAIL

    def wait_satisfied(self) -> bool:
        """The re-pull is only evidence after the registered wait has elapsed."""
        return self.wait_days_observed >= CONFIG.revision_repull_wait_days


@final
@dataclass(frozen=True, slots=True)
class AgreementFinding:
    """The A.1 TASK 4 measurements, both first-class. Every figure carries its n."""

    first5_high_low_agreement_share: float
    session_ticker_pairs_compared: int
    bars_present_in_both: int
    bars_agreeing_to_the_cent: int
    delisted_names_served: int
    delisted_names_with_intraday_history: int

    def agreement_verdict(self) -> IntegrityVerdict:
        """PASS at or above 0.95; PARTIAL down to 0.85 inclusive; FAIL below."""
        share = self.first5_high_low_agreement_share
        if share >= CONFIG.agreement_pass_min_share:
            return IntegrityVerdict.PASS
        if share >= CONFIG.agreement_partial_min_share:
            return IntegrityVerdict.PARTIAL
        return IntegrityVerdict.FAIL

    def delisted_verdict(self) -> IntegrityVerdict:
        """PASS at 100 or more; PARTIAL from 20 inclusive; FAIL below 20."""
        count = self.delisted_names_with_intraday_history
        if count >= CONFIG.delisted_pass_min_count:
            return IntegrityVerdict.PASS
        if count >= CONFIG.delisted_partial_min_count:
            return IntegrityVerdict.PARTIAL
        return IntegrityVerdict.FAIL

    def verdict(self) -> IntegrityVerdict:
        """Worst of the two. A survivor-only universe is not offset by agreement."""
        parts = (self.agreement_verdict(), self.delisted_verdict())
        if IntegrityVerdict.FAIL in parts:
            return IntegrityVerdict.FAIL
        if IntegrityVerdict.PARTIAL in parts:
            return IntegrityVerdict.PARTIAL
        return IntegrityVerdict.PASS
