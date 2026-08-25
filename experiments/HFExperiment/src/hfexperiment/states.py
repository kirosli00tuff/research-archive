"""The five daily accrual states. Never merged, each enforced.

Stage B.1 registered them: computed, missing_bar, halted, delisted,
source_failed. The design rule that caught seven fabrications in the
predecessor project: absence is a recorded state, never a synthesized
value. A day that cannot compute honestly is a recorded absence, not an
estimate, so no branch here ever produces a price.

Two disjoint families and their enforcement sites:

  marking    halted, delisted. The name marks at its last available
             close and redeploys at the next formation, never
             intra-month (REGISTRATION.md Section 3). Enforced in
             shadow.accrue_book_day and shadow.advance_panel, which
             give a marked name exactly zero return.
  excluding  missing_bar, source_failed. The day leaves the confidence
             sequence, the exclusion is recorded and retried next run,
             because bars backfill. Enforced in shadow.day_exclusion
             and accrual.py, which refuse to accrue past either state.
"""
from __future__ import annotations

from enum import Enum

# Sessions of confirmed absence, with successful fetches and an active
# asset, before an unexplained missing bar is classified as a halt. A
# data lag does not survive three retried sessions. A regulatory halt
# does.
HALT_CONFIRM_SESSIONS = 3


class AccrualState(Enum):
    """One name's state for one session. Five values, no sixth."""

    COMPUTED = "computed"
    MISSING_BAR = "missing_bar"
    HALTED = "halted"
    DELISTED = "delisted"
    SOURCE_FAILED = "source_failed"


MARKING_STATES = frozenset({AccrualState.HALTED, AccrualState.DELISTED})
EXCLUDING_STATES = frozenset(
    {AccrualState.MISSING_BAR, AccrualState.SOURCE_FAILED}
)


def classify_name_day(
    *,
    fetch_ok: bool,
    has_bar: bool,
    asset_active: bool,
    bar_exists_later: bool,
    absent_streak: int,
    already_marked: AccrualState | None = None,
) -> AccrualState:
    """One name's state for one session. The single classification site.

    already_marked carries a mark from earlier in the month. Section 3
    marks a halted or delisted name at its last available close until
    the next formation, so a mark persists even when bars resume: the
    resume-gap return must not enter the series intra-month.

    A missing bar becomes a confirmed halt on evidence only: a bar
    exists at a later session, so the name skipped this one while
    listed, or the absence has persisted HALT_CONFIRM_SESSIONS sessions
    of successful fetches. Until evidence arrives it stays missing_bar,
    which excludes the day and retries.
    """
    if already_marked is not None:
        if already_marked not in MARKING_STATES:
            raise ValueError("only halted or delisted marks persist")
        return already_marked
    if not fetch_ok:
        return AccrualState.SOURCE_FAILED
    if has_bar:
        return AccrualState.COMPUTED
    if not asset_active:
        return AccrualState.DELISTED
    if bar_exists_later or absent_streak >= HALT_CONFIRM_SESSIONS:
        return AccrualState.HALTED
    return AccrualState.MISSING_BAR


def excludes_day(state: AccrualState) -> bool:
    """Whether this state excludes the day from the confidence sequence."""
    return state in EXCLUDING_STATES


def marks_at_last_close(state: AccrualState) -> bool:
    """Whether this state marks at the last available close, Section 3."""
    return state in MARKING_STATES
