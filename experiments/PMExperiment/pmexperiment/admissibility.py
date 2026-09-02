"""ADR-012 as a procedure: a claim about permission must be checkable to count.

DECISIONS.md ADR-012, recorded 2026-08-30 after Amendment 1 moved an entire
measurement venue on a claim about permission that cited no clause, no
effective date and no fetch date:

    A claim in this repository about what a venue's terms permit carries a
    quoted clause, the document's effective date, and the date it was fetched
    — or it is recorded as unmeasured and the stage proceeds as if permission
    were absent.

This module is that sentence as code. It judges the **form** of a claim and
never its merits: it cannot tell whether a clause was read correctly, only
whether the three elements that make the claim checkable by someone else are
present. That is the whole of ADR-012 and deliberately not more, because a
procedure that scored the persuasiveness of a clause would be dressing a
judgement up as a measurement.

Two failure directions, named rather than balanced. A claim wrongly recorded
UNMEASURED costs a candidate that might have been usable. A claim wrongly
admitted lets an unmeasured assertion about permission move a venue — which is
the failure that actually happened here, twice recorded so it is not made a
third time. The check therefore fails closed, and **UNMEASURED is never read
as permission** (standing rule 5).

UNMEASURED is not a synonym for PROHIBITED. They carry the same operational
consequence — the stage proceeds as if permission were absent — and different
epistemic content: one is a measured refusal, the other is an absence.

No request leaves this module and no venue is read from it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum

# The one client-rendered page this repository has measured sets this bar.
# docs/ACCESS.md records `polymarket.com/tos` returning HTTP 200 with a 217 KB
# body that stripped to 1,354 characters of text — a text share near 0.6 % —
# while the terms document it embeds runs to 59,617 bytes. A plain or lightly
# marked-up document sits far above 5 %; an app shell sits far below it.
#
# Direction of error, named rather than balanced: a genuine document served
# under unusually heavy markup is flagged as a shell and its claim is recorded
# UNMEASURED, which fails closed. The reverse error — reading a shell as the
# document — is the one that would have produced a false report in Stage C.
MIN_DOCUMENT_TEXT_RATIO: float = 0.05

# ADR-012's three elements, in the order the ADR names them. Every one of them
# is verified load-bearing by mutation in tests/test_guards.py: blank any
# single element and an otherwise complete claim must fall to UNMEASURED.
REQUIRED_ELEMENTS: tuple[str, str, str] = ("clause", "effective_date", "fetch_date")


class Admissibility(Enum):
    """Whether a claim carries the three elements ADR-012 requires."""

    ADMISSIBLE = "ADMISSIBLE"
    UNMEASURED = "UNMEASURED"


class CandidateVerdict(Enum):
    """The three rows a source may return on what it permits for this use."""

    PERMITTED = "PERMITTED"
    PROHIBITED = "PROHIBITED"
    UNMEASURED = "UNMEASURED"


@dataclass(frozen=True)
class DocumentReading:
    """What was actually read, in bytes of body and characters of text.

    Recorded so a later reader can check that the document read was the
    document. Stage C's near miss is the reason this exists: an HTTP 200 and a
    large body are together no evidence that any terms were retrieved.
    """

    url: str
    body_bytes: int
    text_chars: int

    def __post_init__(self) -> None:
        if self.body_bytes < 0 or self.text_chars < 0:
            raise ValueError("a reading cannot carry negative byte or character counts")

    @property
    def text_ratio(self) -> float:
        """Characters of extracted text per byte of body. A zero body reads zero."""
        if self.body_bytes == 0:
            return 0.0
        return self.text_chars / self.body_bytes

    @property
    def looks_client_rendered(self) -> bool:
        """True when the body is mostly not text — the app-shell signature."""
        return self.text_ratio < MIN_DOCUMENT_TEXT_RATIO

    @property
    def is_established(self) -> bool:
        """True when this reading may be treated as the document itself.

        Absolute length is deliberately not a bar. A short licence — an MIT
        file, a CC BY notice — is a whole document at a thousand characters,
        while Stage C's shell was short *and* almost entirely markup. The ratio
        separates those two; a length floor would condemn the first with the
        second.
        """
        return self.text_chars > 0 and not self.looks_client_rendered


@dataclass(frozen=True)
class PermissionClaim:
    """One assertion about what a source permits, with its evidence attached."""

    source: str
    document: str
    clause: str
    effective_date: str | None
    fetch_date: str | None
    claimed: CandidateVerdict


@dataclass(frozen=True)
class AdmissibilityReading:
    """One firing of the check, preserved as fired."""

    claim: PermissionClaim
    admissibility: Admissibility
    missing: tuple[str, ...]
    verdict: CandidateVerdict


def _is_iso_date(value: str | None) -> bool:
    """A date must be present and parseable, not merely non-empty."""
    if value is None:
        return False
    try:
        date.fromisoformat(value.strip())
    except ValueError:
        return False
    return True


def missing_elements(claim: PermissionClaim) -> tuple[str, ...]:
    """The ADR-012 elements this claim does not carry, in the ADR's order."""
    absent: list[str] = []
    if not claim.clause.split():
        absent.append("clause")
    if not _is_iso_date(claim.effective_date):
        absent.append("effective_date")
    if not _is_iso_date(claim.fetch_date):
        absent.append("fetch_date")
    return tuple(absent)


def admit(claim: PermissionClaim) -> AdmissibilityReading:
    """Fire ADR-012 over one claim.

    A claim carrying all three elements returns what it claims. A claim missing
    any of them returns UNMEASURED with the gaps named, whatever it claimed —
    including a claim that permission is absent, because an unevidenced refusal
    is no more measured than an unevidenced permission.
    """
    absent = missing_elements(claim)
    if absent:
        return AdmissibilityReading(
            claim=claim,
            admissibility=Admissibility.UNMEASURED,
            missing=absent,
            verdict=CandidateVerdict.UNMEASURED,
        )
    return AdmissibilityReading(
        claim=claim,
        admissibility=Admissibility.ADMISSIBLE,
        missing=(),
        verdict=claim.claimed,
    )


def permits(verdict: CandidateVerdict) -> bool:
    """Only PERMITTED permits.

    ADR-012's consequence clause in one line: an UNMEASURED source is worked
    with exactly as a PROHIBITED one, and the stage proceeds as if permission
    were absent.
    """
    return verdict is CandidateVerdict.PERMITTED
