"""The revision clock — the registered wait between the probe pull and its twin.

**The wait is the measurement.** A.1 TASK 3 measures the **bar revision rate**:
the share of already-served bars whose stored bytes change when the identical
request set is sent again. A re-pull sent an hour later measures nothing, because
a vendor that regenerates its history nightly has not yet had a chance to do so.
`CONFIG.revision_repull_wait_days` is **14 calendar days**, and this module is
the only place that decides whether the wait has elapsed.

The precedent this exists for: **MLCryptoEngine H11 died on a measured 75-day
publication lag** in a free source with whole-file regeneration that revised past
rows — and the lag was **discovered rather than registered**. Here the clock is
started deliberately, its earliest eligible date is written down before any
re-pull is possible, and the refusal before that date is **loud**.
"""

from __future__ import annotations

from datetime import date, timedelta

from orb.config import CONFIG


class RepullNotDueError(PermissionError):
    """Raised when a re-pull is attempted before the registered wait elapses."""


def registered_wait_days() -> int:
    """The registered wait, in calendar days."""
    return CONFIG.revision_repull_wait_days


def earliest_eligible(pulled_on: date) -> date:
    """The first date on which a re-pull is evidence rather than noise."""
    return pulled_on + timedelta(days=CONFIG.revision_repull_wait_days)


def days_waited(pulled_on: date, today: date) -> int:
    """Calendar days elapsed. Negative if ``today`` precedes the pull."""
    return (today - pulled_on).days


def is_due(pulled_on: date, today: date) -> bool:
    """True on and after the earliest eligible date, never before."""
    return today >= earliest_eligible(pulled_on)


def require_due(pulled_on: date, today: date) -> int:
    """Refuse loudly before the wait elapses. Returns the days waited.

    A re-pull that runs early does not produce a *weaker* revision figure — it
    produces a **wrong** one, biased toward zero, and a zero revision share is
    the shape of a `PASS`. **The refusal is what stops a manufactured pass.**
    """
    waited = days_waited(pulled_on, today)
    if not is_due(pulled_on, today):
        raise RepullNotDueError(
            f"re-pull is not due: {waited} calendar days have elapsed since "
            f"{pulled_on.isoformat()}, and the registered wait is "
            f"{CONFIG.revision_repull_wait_days}. The earliest eligible date is "
            f"{earliest_eligible(pulled_on).isoformat()}. A re-pull run early "
            "measures a revision rate biased toward zero, and zero is the shape "
            "of a PASS."
        )
    return waited
