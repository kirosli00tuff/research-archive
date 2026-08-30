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


@unique
class TapeVerdict(StrEnum):
    """A.1 TASK 4 tape identification, registered by Amendment 7.

    **This is a new registered branch, not a reinterpretation of an existing
    one.** The registered cross-vendor agreement thresholds of Section 0 assume
    two feeds that are *trying to measure the same thing*. A feed carrying a
    **single-venue subset** — IEX alone, say — is not a disagreeing measurement
    of the consolidated tape; it is a **correct measurement of a different
    thing**, and scoring it against the 0.95/0.85 bars would fire BLOCKED on a
    fact about entitlement rather than a fact about integrity.
    """

    SAME_TAPE = "SAME_TAPE"
    """Median ratio inside [0.90, 1.10]. The registered agreement thresholds
    apply **as written**."""

    DIFFERENT_TAPE = "DIFFERENT_TAPE"
    """Median ratio strictly below 0.50. **The registered agreement thresholds
    do not apply and must not fire.**"""

    AMBIGUOUS = "AMBIGUOUS"
    """Anything between. **Fire nothing. Record the full distribution.**"""


@final
@dataclass(frozen=True, slots=True)
class TapeFinding:
    """The A.1 TASK 4 tape measurement. Ratios and counts. **No bar value.**

    The ratio is ``secondary first-5-minute volume / primary first-5-minute
    volume`` per session-ticker pair. A single-venue subset presents a
    systematically small fraction of a consolidated feed's volume, so the
    **median** of that ratio identifies the tape and the **interquartile range**
    says how consistently.
    """

    median_ratio: float
    iqr_low_ratio: float
    iqr_high_ratio: float
    min_ratio: float
    max_ratio: float
    share_below_single_venue_threshold: float
    session_ticker_pairs_compared: int
    pairs_with_volume_in_both: int
    pairs_with_volume_in_primary_only: int
    pairs_with_volume_in_secondary_only: int
    pairs_with_volume_in_neither: int

    def verdict(self) -> TapeVerdict:
        """SAME_TAPE inside [0.90, 1.10]; DIFFERENT_TAPE below 0.50; else AMBIGUOUS."""
        if (
            CONFIG.tape_same_min_ratio
            <= self.median_ratio
            <= CONFIG.tape_same_max_ratio
        ):
            return TapeVerdict.SAME_TAPE
        if self.median_ratio < CONFIG.tape_different_max_ratio:
            return TapeVerdict.DIFFERENT_TAPE
        return TapeVerdict.AMBIGUOUS

    def agreement_thresholds_apply(self) -> bool:
        """Only SAME_TAPE licenses the registered 0.95 / 0.85 agreement bars."""
        return self.verdict() is TapeVerdict.SAME_TAPE

    def looks_like_a_single_venue_subset(self) -> bool:
        """A majority of pairs below the 0.20 single-venue threshold."""
        return self.share_below_single_venue_threshold > 0.50
