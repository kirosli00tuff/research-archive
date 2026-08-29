"""Load-bearing honesty tests. These pin the scope AND the headline figures.

Three things break the build here, deliberately:

* a **deletion of the scope-limit sentence** from README.md or from the note,
* a **deletion of one of the headline figures** from either document, and
* a **credential-shaped string** anywhere in a tracked file.

The scope limit is the sentence that keeps this note honest: four cases, about
detectability, not about whether the anomalies exist. It is the first thing a
later session would be tempted to trim for length, and trimming it turns a
bounded claim into an unbounded one. The headline figures are the other
direction of the same failure: a note whose inconvenient numbers have quietly
gone missing reads stronger than the evidence it rests on.

Each detector carries a canary asserting it actually fires. A guard that has
never been shown to fail is not a guard — the lesson InsiderExperiment recorded
as its most reusable finding, and it applies to this repository too.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
NOTE = "docs/the-power-limit.md"


def flat(text: str) -> str:
    """Collapse whitespace so a markdown reflow does not break a pin.

    The pin exists to catch a DELETION, not a rewrap. Collapsing both sides
    keeps it sensitive to the former and blind to the latter. Blockquote
    markers are stripped first, because two of the pinned passages are quoted
    from a sibling repository and a leading "> " would otherwise land
    mid-sentence.
    """
    stripped = [line.lstrip().removeprefix("> ").removeprefix(">") for line in text.splitlines()]
    return " ".join(" ".join(stripped).split())


def document(name: str) -> str:
    return flat((ROOT / name).read_text(encoding="utf-8"))


#: The scope limit, in the exact words the note and the README both carry. It
#: appears twice on purpose: a reader who only ever sees the README must still
#: see the boundary of the claim.
SCOPE_LIMIT = (
    "This is not evidence that those anomalies are absent, and four cases are "
    "four cases rather than a survey; the note claims a detectability result "
    "about retail-scale replication and nothing more."
)

SCOPE_PINNED = {
    "README.md": [
        SCOPE_LIMIT,
        "It holds no market data, opens no data source, computes no statistic, and makes no claim about any market.",
    ],
    NOTE: [
        SCOPE_LIMIT,
        "Nothing here refutes the literature it tested against.",
        '"Independent" means independent hypotheses, not independent investigators.',
        "Four cases are four cases.",
    ],
}


@pytest.mark.parametrize("name", sorted(SCOPE_PINNED))
def test_scope_limit_is_present(name: str) -> None:
    """Deleting the scope limit breaks the build."""
    text = document(name)
    missing = [phrase for phrase in SCOPE_PINNED[name] if flat(phrase) not in text]
    assert missing == [], (
        f"{name} lost pinned scope statements: {missing}. These bound the claim; "
        "they are not editorial."
    )


#: The headline figures, pinned so the RESULT cannot be quietly softened.
#:
#: Each is load-bearing for a different reason: the realized MDEs and their
#: effect bands ARE the finding; the ETF sample figures are the ones most
#: easily mis-scoped, and the note corrects them explicitly; 6.9378 USD is the
#: before-the-gate half of the cost asymmetry, which means nothing without it.
FIGURES_PINNED = {
    "README.md": [
        "0.0512",
        "0.01 to 0.05",
        "49.35 bp per month",
        "845",
        "above 1,200",
        "302",
        "z 1.668",
        "2.50",
        "6.9378 USD",
    ],
    NOTE: [
        "0.0512",
        "0.01 to 0.05",
        "49.35 bp per month",
        "845",
        "above 1,200",
        "302",
        "z 1.668",
        "2.50",
        "6.9378 USD",
        "unresolved at achievable power",
        "untestable at achievable power",
        "BLOCKED",
        "0 USD",
        "−1.0779",
        "300 to 550 bps",
    ],
}


@pytest.mark.parametrize("name", sorted(FIGURES_PINNED))
def test_headline_figures_are_present(name: str) -> None:
    """Deleting a headline figure breaks the build, exactly as deleting scope does."""
    text = document(name)
    missing = [figure for figure in FIGURES_PINNED[name] if flat(figure) not in text]
    assert missing == [], (
        f"{name} lost pinned headline figures: {missing}. These are the evidence "
        "the claim rests on."
    )


def test_presence_checker_fires() -> None:
    """Canary: the presence check must fail on a phrase that is genuinely absent."""
    for name in ("README.md", NOTE):
        assert f"this phrase is deliberately not in {name}" not in document(name)


def test_figure_pin_detector_fires() -> None:
    """Canary: a figure pin must fail on a number the note genuinely does not report.

    The counter-figure is the NPDExperiment MDE moved below its effect band —
    the single edit that would turn an underpowered unresolved into a tight null.
    """
    text = document(NOTE)
    assert "0.0512" in text
    assert "minimum detectable contrast was 0.0012" not in text


def test_the_note_never_claims_the_anomalies_are_absent() -> None:
    """The one sentence this note must never contain, in its likeliest phrasings."""
    text = document(NOTE).lower()
    for forbidden in (
        "the effect does not exist",
        "these anomalies do not exist",
        "we have shown the effect is absent",
        "proves there is no effect",
    ):
        assert forbidden not in text, f"the note overclaims: {forbidden!r}"


#: A 32-character hex run is the shape of an API key hash. sha256 digests are 64
#: and git object hashes are 40, so neither collides with this pattern.
CREDENTIAL_SHAPED = re.compile(rb"(?<![0-9a-fA-F])[0-9a-fA-F]{32}(?![0-9a-fA-F])")
SECRET_ASSIGNMENT = re.compile(
    rb"(?i)(api[_-]?key|secret|token|password|passwd)\s*[=:]\s*['\"][^'\"]{8,}['\"]"
)


def tracked_files() -> list[Path]:
    listing = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    return [ROOT / name for name in listing.stdout.split("\n") if name]


def test_the_credential_scan_has_something_to_scan() -> None:
    """A scan over an empty file list passes and looks exactly like a clean scan.

    Before ``git init`` ran, ``git ls-files`` returned nothing and the scan below
    was green over zero files for the whole build. It went red the moment the
    first commit made the files tracked — and it was right to. This assertion
    exists so the vacuous state is a failure rather than a pass.
    """
    assert len(tracked_files()) > 10, "the credential scan has no files; it would pass vacuously"


def test_no_credential_shaped_strings_in_tracked_files() -> None:
    """Secrets never enter the repo — enforced by a scan, not by a filename glob."""
    offenders: list[str] = []
    for path in tracked_files():
        if not path.is_file():
            continue
        raw = path.read_bytes()
        if CREDENTIAL_SHAPED.search(raw) or SECRET_ASSIGNMENT.search(raw):
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == [], f"credential-shaped strings in tracked files: {offenders}"


def test_credential_detector_fires() -> None:
    """Canary: the scanners must catch synthetic strings of each shape.

    Both synthetic strings are BUILT at runtime rather than written as literals.
    A literal here would be caught by the scanner above, which is exactly the
    behaviour that test asserts — and the assignment canary WAS written as a
    literal first, and the scanner caught it. That was a true positive, not a
    false one.
    """
    synthetic_hex = ("dead" + "beef") * 4
    assert len(synthetic_hex) == 32
    assert CREDENTIAL_SHAPED.search(synthetic_hex.encode()) is not None

    key_word = "api" + "_key"
    synthetic_assignment = f'{key_word} = "{"x" * 20}"'.encode()
    assert SECRET_ASSIGNMENT.search(synthetic_assignment) is not None

    assert CREDENTIAL_SHAPED.search(b"the power limit") is None
    assert SECRET_ASSIGNMENT.search(b"the power limit") is None
