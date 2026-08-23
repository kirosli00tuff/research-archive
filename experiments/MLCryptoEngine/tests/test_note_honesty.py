"""Honesty tests for the standalone write-up notes under ``docs/notes/``.

A note written for an outside reader restates figures that live in
``HYPOTHESES.md`` and ``report.md``. Restated numbers drift: the register gets
corrected, or the note gets edited, and the two quietly stop agreeing. Because
the note is the artefact an outsider reads and the register is the artefact the
project trusts, a divergence is worse than either file being wrong alone.

These tests make drift a build failure in **both** directions. Every pinned
figure must appear in the note *and* in the specific register entry it is drawn
from, so editing either side without the other fails here. The pins are matched
against the note's own prose with the verbatim quotation block removed —
otherwise a note that merely quoted the register would satisfy every pin
without stating a single number itself.

The reopening condition gets a stricter test still: it must be reproduced
character-for-character, because a paraphrased reopening condition is how a
closed question gets quietly reopened on the wrong grounds.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = REPO_ROOT / "docs" / "notes" / "h1-predictability-without-capturability.md"
HYPOTHESES_PATH = REPO_ROOT / "HYPOTHESES.md"
REPORT_PATH = REPO_ROOT / "report.md"
README_PATH = REPO_ROOT / "README.md"

H1_HEADING = "### H1 — Short-horizon directional prediction on crypto spot"
H2_HEADING = "### H2 — Transfer of that edge to CME micro futures"
COST_HEADING = "### The measured venue cost landscape"

NOTE_QUOTE_HEADING = "## The registered reopening condition, verbatim"

# The line break the register uses inside a markdown table cell. The note
# renders it as a paragraph break and says so; nothing else may differ.
CELL_LINE_BREAK = "<br><br>"

# Anchors the H1 reopening cell and nothing else in the register.
H1_REOPENING_ANCHOR = "$250M trailing 30-day volume"


def _section(text: str, heading: str, stop: str) -> str:
    """Return ``heading`` and everything under it up to the next ``stop`` heading."""
    start = text.find(heading)
    assert start != -1, f"heading not found: {heading!r}"
    end = text.find(stop, start + len(heading))
    return text[start:] if end == -1 else text[start:end]


def _read(path: Path) -> str:
    assert path.is_file(), f"missing file: {path}"
    return path.read_text(encoding="utf-8")


def _note_text() -> str:
    return _read(NOTE_PATH)


def _note_prose() -> str:
    """The note with its verbatim quotation block removed.

    Pins are checked against this rather than the whole file so that quoting
    the register cannot, by itself, satisfy a claim the note never makes.
    """
    text = _note_text()
    start = text.find(NOTE_QUOTE_HEADING)
    assert start != -1, f"note is missing the section {NOTE_QUOTE_HEADING!r}"
    end = text.find("\n## ", start + len(NOTE_QUOTE_HEADING))
    assert end != -1, "the verbatim quotation section must be followed by another section"
    return text[:start] + text[end:]


def _register_reopening_paragraphs() -> list[str]:
    """H1's registered reopening condition, split on the cell's own line break."""
    for line in _read(HYPOTHESES_PATH).splitlines():
        if line.startswith("| **What would reopen it** |") and H1_REOPENING_ANCHOR in line:
            cell = line.split("|")[2].strip()
            return [part.strip() for part in cell.split(CELL_LINE_BREAK)]
    raise AssertionError("H1's 'What would reopen it' row was not found in HYPOTHESES.md")


def _note_quoted_paragraphs() -> list[str]:
    """The blockquote paragraphs under the note's verbatim-quotation heading."""
    text = _note_text()
    start = text.find(NOTE_QUOTE_HEADING)
    assert start != -1, f"note is missing the section {NOTE_QUOTE_HEADING!r}"
    end = text.find("\n## ", start + len(NOTE_QUOTE_HEADING))
    block = text[start:] if end == -1 else text[start:end]

    paragraphs: list[str] = []
    current: list[str] = []
    for line in block.splitlines():
        if not line.startswith(">"):
            continue
        body = line[1:].strip()
        if body:
            current.append(body)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs


# The pins below deliberately carry the characters the documents actually use —
# U+2212 MINUS SIGN, U+00D7 MULTIPLICATION SIGN, U+2013 EN DASH — because these
# are byte-exact containment checks against markdown, not arithmetic. Rewriting
# them to ASCII (RUF001's suggestion) would make every pin fail, which is why
# each such line is exempted individually rather than the rule being relaxed.

# Figures the note and the H1 register entry must both state, in the note's own
# prose. Traced in the note's sources table to report.md §Phase B, §C.8, §C.14.
H1_SHARED_FIGURES = (
    # AUC at the 900 s horizon, Coinbase BTC-USD
    "0.596",
    # the withdrawn headline gross capture
    "3.31 bps",
    # Coinbase Advanced round-trip maker cost
    "80.00 bps",
    # net EV at that horizon
    "−76.69 bps",  # noqa: RUF001
    # the same capture measured across four full days
    "−2.44 to +3.05 bps",  # noqa: RUF001
    # four-day AUC range at 100 ms
    "0.0044",
    # Spearman rho, confidence vs |move|, Kraken at 100 ms
    "−0.32",  # noqa: RUF001
    # the same on Coinbase
    "−0.37",  # noqa: RUF001
    # best top-confidence decile in the study
    "5.00 bps",
    # by how much that decile misses the economic bar
    "16×",  # noqa: RUF001
    # top-decile capture against the all-sample mean
    "2–24×",  # noqa: RUF001
    # by how much the original closure's arithmetic failed
    "23×",  # noqa: RUF001
    # planted-future canary AUC — the leakage probe demonstrably fires
    "0.9714",
)

# Figures the note and the H2 register entry must both state.
H2_SHARED_FIGURES = (
    # CME MBT at 900 s — a coin flip
    "AUC 0.501",
    # gross capture there
    "0.22 bps",
    # round-trip cost there
    "5.33 bps",
    # best net EV, which never crosses zero at any horizon
    "−5.11 bps",  # noqa: RUF001
    # the one figure clearing rounding noise
    "+0.215",
    # what it became on a stride-1 control
    "−0.785",  # noqa: RUF001
)

# Cost-floor rows, pinned as whole table rows because the note reproduces the
# register's table verbatim rather than restating its numbers loose.
COST_FLOOR_ROWS = (
    "| Hyperliquid perps, base tier | 1.5 bps | **3.0 bps** |",
    "| Kraken spot, base tier | 25 bps | **50 bps** |",
    "| Coinbase Advanced spot, base tier | 40 bps | **80 bps** |",
)

# C.14 figures the register does not restate, pinned against report.md instead
# so the note cannot drift from the stage that produced them either.
REPORT_ONLY_FIGURES = (
    "0.9432",  # AUC at 100 ms, Kraken BTC/USD — the note's headline
    "0.0291 bps",  # gross capture at that same horizon
    "−0.3175",  # noqa: RUF001  (Kraken rho at 100 ms, to four places)
    "−0.3665",  # noqa: RUF001  (Coinbase rho at 100 ms)
    "5.0020",  # top-decile capture at 900 s
    "0.6086",  # worst calibration gap, Kraken
    "0.4628",  # worst calibration gap, Coinbase
    "165,075",  # Kraken sample count over six validated days
    "41,780",  # Coinbase sample count over the same days
    "123,864",  # deep-learning sample count at 900 s
)


class TestNoteExistsAndIsLinked:
    def test_note_file_is_present(self) -> None:
        assert NOTE_PATH.is_file(), f"the H1 note is missing at {NOTE_PATH}"

    def test_readme_links_the_note(self) -> None:
        # Arrange
        readme = _read(README_PATH)
        relative = "docs/notes/h1-predictability-without-capturability.md"

        # Act / Assert — a note nobody can find is not published.
        assert relative in readme, "README must link the note by its repository path"
        assert "## Findings" in readme, "README must carry a findings section"


class TestNoteMatchesTheRegister:
    @pytest.mark.parametrize("figure", H1_SHARED_FIGURES)
    def test_h1_figure_matches_register(self, figure: str) -> None:
        # Arrange
        entry = _section(_read(HYPOTHESES_PATH), H1_HEADING, "\n### ")
        prose = _note_prose()

        # Act / Assert — both directions, so either file drifting fails here.
        assert figure in entry, (
            f"{figure!r} is no longer stated in the H1 register entry; "
            "the note still claims it — reconcile HYPOTHESES.md and the note together"
        )
        assert figure in prose, (
            f"{figure!r} is stated in the H1 register entry but not in the note's "
            "own prose — the note must restate the figures it is built on"
        )

    @pytest.mark.parametrize("figure", H2_SHARED_FIGURES)
    def test_h2_figure_matches_register(self, figure: str) -> None:
        # Arrange
        entry = _section(_read(HYPOTHESES_PATH), H2_HEADING, "\n### ")
        prose = _note_prose()

        # Act / Assert
        assert figure in entry, f"{figure!r} is no longer stated in the H2 register entry"
        assert figure in prose, f"{figure!r} is in the H2 register entry but not in the note"

    @pytest.mark.parametrize("row", COST_FLOOR_ROWS)
    def test_cost_floor_row_matches_register(self, row: str) -> None:
        # Arrange
        landscape = _section(_read(HYPOTHESES_PATH), COST_HEADING, "\n### ")

        # Act / Assert — the cost floor is what turns a real signal into a
        # closed hypothesis, so it is pinned as a whole row, not as loose bps.
        assert row in landscape, f"cost row drifted in HYPOTHESES.md: {row!r}"
        assert row in _note_prose(), f"cost row drifted in the note: {row!r}"

    @pytest.mark.parametrize("figure", REPORT_ONLY_FIGURES)
    def test_diagnostic_figure_matches_report(self, figure: str) -> None:
        # Arrange — these are C.14 figures the register summarises rather than
        # restates, so report.md is the file they are pinned against.
        report = _read(REPORT_PATH)

        # Act / Assert
        assert figure in report, f"{figure!r} is no longer stated in report.md"
        assert figure in _note_prose(), f"{figure!r} is in report.md but not in the note"


class TestReopeningConditionIsQuotedVerbatim:
    def test_quote_reproduces_the_register_character_for_character(self) -> None:
        # Arrange
        registered = _register_reopening_paragraphs()

        # Act
        quoted = _note_quoted_paragraphs()

        # Assert — a paraphrase is how a closure gets reopened on grounds the
        # register never granted. Only the documented <br><br> may differ.
        assert quoted == registered, (
            "the note's reopening quotation no longer matches HYPOTHESES.md verbatim"
        )

    def test_the_register_cell_really_does_split_into_two_paragraphs(self) -> None:
        # Guards the normalisation itself: if the register stops using the
        # <br><br> break, the equality test above would pass vacuously on a
        # single blob and the note would silently keep a stale second half.
        assert len(_register_reopening_paragraphs()) == 2

    def test_the_note_states_the_normalisation_it_applied(self) -> None:
        # The one permitted difference has to be disclosed to the reader,
        # not just to this test.
        assert CELL_LINE_BREAK in _note_text(), (
            "the note must name the <br><br> line break it renders as a paragraph break"
        )
