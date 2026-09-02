"""ADR-012's check, fired first over this repository's own three claims.

Task 1 of Stage D says to apply ADR-012 to itself before applying it to
anything else. These fixtures are therefore not synthetic: they are the three
claims about permission this repository has actually made, reconstructed from
the record, and the procedure is judged by whether it classifies them the way
an honest reader would.

One of the three does not come out the way the record says it does, and that
is written down here rather than smoothed over. See
`test_stage_a_kalshi_claim_carries_no_effective_date_in_the_record`.
"""

from dataclasses import replace

import pytest

from pmexperiment.admissibility import (
    Admissibility,
    CandidateVerdict,
    DocumentReading,
    PermissionClaim,
    admit,
    missing_elements,
    permits,
)

# --- The three claims this repository has made, reconstructed ---------------

# Stage C, 2026-08-30. The one claim in the record carrying all three elements:
# a clause quoted verbatim, an effective date on the face of the document, and
# the date it was fetched (docs/ACCESS.md, REGISTRATION.md Amendment 6).
POLYMARKET_STAGE_C = PermissionClaim(
    source="Polymarket",
    document="POLYMARKET.COM TERMS OF USE (Adventure One QSS, Inc.)",
    clause=(
        "Use any data mining tools, robots, crawlers, or similar data gathering "
        "and extraction tools to scrape or otherwise remove data from the Site, "
        "any other Interface, or Features;"
    ),
    effective_date="2026-08-11",
    fetch_date="2026-08-30",
    claimed=CandidateVerdict.PROHIBITED,
)

# Stage A, 2026-08-29. docs/ACCESS.md quotes the prohibitions verbatim and
# records the fetch date. It records no effective date, and neither does any
# other tracked document.
KALSHI_STAGE_A = PermissionClaim(
    source="Kalshi",
    document="Kalshi Data Terms of Use",
    clause=(
        "use of any Kalshi Data (including associated metadata) in any manner "
        "for any machine learning and/or artificial intelligence ... is "
        "expressly prohibited."
    ),
    effective_date=None,
    fetch_date="2026-08-29",
    claimed=CandidateVerdict.PROHIBITED,
)

# Amendment 1, 2026-08-30. The claim that moved an entire measurement venue.
# It cited no document, no clause, no effective date and no fetch date, and
# Amendment 6 retracts its ground.
AMENDMENT_ONE = PermissionClaim(
    source="Polymarket",
    document="",
    clause="",
    effective_date=None,
    fetch_date=None,
    claimed=CandidateVerdict.PERMITTED,
)


def test_a_complete_claim_is_admissible_and_returns_what_it_claims() -> None:
    reading = admit(POLYMARKET_STAGE_C)
    assert reading.admissibility is Admissibility.ADMISSIBLE
    assert reading.missing == ()
    assert reading.verdict is CandidateVerdict.PROHIBITED


def test_a_claim_stripped_of_its_effective_date_is_unmeasured() -> None:
    """The mutation Stage D's Task 1 names explicitly.

    The claim is otherwise the strongest one in the record — quoted clause,
    fetch date, a real document — and it still falls to UNMEASURED without the
    one element. That is the whole of ADR-012: the elements are conjunctive.
    """
    stripped = replace(POLYMARKET_STAGE_C, effective_date=None)
    reading = admit(stripped)
    assert reading.admissibility is Admissibility.UNMEASURED
    assert reading.missing == ("effective_date",)
    assert reading.verdict is CandidateVerdict.UNMEASURED


def test_stage_a_kalshi_claim_carries_no_effective_date_in_the_record() -> None:
    """ADR-012 applied to itself, and it does not flatter the record.

    ADR-012 states that "Stage A's Kalshi finding met that bar." Measured
    against the procedure, it met two elements of three: docs/ACCESS.md quotes
    the prohibitions verbatim and records the fetch date of 2026-08-29, and no
    tracked document records an effective date for the Kalshi Data Terms of
    Use. The claim is therefore UNMEASURED, not admissible.

    **This changes no verdict.** UNMEASURED and PROHIBITED carry the same
    operational consequence — the stage proceeds as if permission were absent —
    so Kalshi stays closed either way. What it changes is the strength of the
    evidence the record claims to hold, and it is recorded because a procedure
    that only ever convicts other people's documents is not a procedure.
    """
    reading = admit(KALSHI_STAGE_A)
    assert reading.admissibility is Admissibility.UNMEASURED
    assert reading.missing == ("effective_date",)
    assert not permits(reading.verdict), "the door does not open on a missing date"


def test_amendment_one_is_inadmissible_on_all_three_elements() -> None:
    """The claim that moved a venue, judged by the rule its failure produced."""
    reading = admit(AMENDMENT_ONE)
    assert reading.admissibility is Admissibility.UNMEASURED
    assert reading.missing == ("clause", "effective_date", "fetch_date")
    assert reading.verdict is CandidateVerdict.UNMEASURED
    assert not permits(reading.verdict)


def test_an_unevidenced_refusal_is_no_more_measured_than_a_permission() -> None:
    """The check is symmetric, so it cannot be used to manufacture a closure."""
    unevidenced_refusal = replace(POLYMARKET_STAGE_C, clause="   ")
    reading = admit(unevidenced_refusal)
    assert reading.claim.claimed is CandidateVerdict.PROHIBITED
    assert reading.verdict is CandidateVerdict.UNMEASURED
    assert reading.missing == ("clause",)


def test_unmeasured_is_never_read_as_permission() -> None:
    assert permits(CandidateVerdict.PERMITTED)
    assert not permits(CandidateVerdict.PROHIBITED)
    assert not permits(CandidateVerdict.UNMEASURED)


def test_a_date_must_parse_and_not_merely_be_present() -> None:
    for bad in ("soon", "2026-13-01", "", "August 2026"):
        claim = replace(POLYMARKET_STAGE_C, effective_date=bad)
        assert missing_elements(claim) == ("effective_date",), bad


def test_all_three_elements_are_named_when_all_three_are_absent() -> None:
    empty = PermissionClaim(
        source="s",
        document="d",
        clause="",
        effective_date=None,
        fetch_date=None,
        claimed=CandidateVerdict.PERMITTED,
    )
    assert missing_elements(empty) == ("clause", "effective_date", "fetch_date")


# --- Establishing that the document read was the document -------------------


def test_the_client_rendered_shell_is_not_the_document() -> None:
    """Stage C's measured near miss, pinned as the calibration case.

    docs/ACCESS.md records `polymarket.com/tos` at HTTP 200 with a 217 KB body
    stripping to 1,354 characters. The exact byte count behind "217 KB" was not
    recorded, so both conventional conversions are asserted: the classification
    does not turn on which one is meant, because 1,354 characters is far below
    5 % of either.
    """
    for body_bytes in (217_000, 217 * 1024):
        shell = DocumentReading(
            url="https://polymarket.com/tos", body_bytes=body_bytes, text_chars=1_354
        )
        assert shell.looks_client_rendered
        assert not shell.is_established
        assert shell.text_ratio < 0.01


def test_the_embedded_terms_document_is_established() -> None:
    """The document Stage C actually read: 59,617 bytes of terms."""
    terms = DocumentReading(
        url="docs.google.com (embedded terms document)",
        body_bytes=59_617,
        text_chars=59_617,
    )
    assert terms.is_established
    assert not terms.looks_client_rendered


def test_a_short_licence_is_still_a_whole_document() -> None:
    """No absolute length floor: an MIT file is a document at about 1 KB.

    This is the false conviction the ratio test exists to avoid. A length floor
    calibrated on a 59,617-byte terms document would record every short licence
    as unmeasured, which would fail closed for a reason that has nothing to do
    with the evidence.
    """
    mit = DocumentReading(url="LICENSE", body_bytes=1_070, text_chars=1_070)
    assert mit.is_established
    assert not mit.looks_client_rendered


def test_an_empty_body_establishes_nothing() -> None:
    empty = DocumentReading(url="x", body_bytes=0, text_chars=0)
    assert empty.text_ratio == 0.0
    assert not empty.is_established


def test_a_reading_cannot_carry_negative_counts() -> None:
    with pytest.raises(ValueError, match="negative byte or character counts"):
        DocumentReading(url="x", body_bytes=-1, text_chars=0)


def test_the_check_itself_can_fail() -> None:
    """A gate that has never failed is not a gate (standing rule 14).

    The suite must contain proof that an admissible claim exists and that a
    complete one can be broken, or the procedure could be a function returning
    ADMISSIBLE unconditionally and every test above would still pass.
    """
    assert admit(POLYMARKET_STAGE_C).admissibility is Admissibility.ADMISSIBLE
    broken_each_way = (
        replace(POLYMARKET_STAGE_C, clause=""),
        replace(POLYMARKET_STAGE_C, effective_date=None),
        replace(POLYMARKET_STAGE_C, fetch_date=None),
    )
    for broken in broken_each_way:
        assert admit(broken).admissibility is Admissibility.UNMEASURED
