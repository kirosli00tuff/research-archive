"""The source registry has to be usable by a stranger, so it is checked as data."""

from __future__ import annotations

import re

import pytest

from rplimits.sources import SOURCES, Source

SHORT_HASH = re.compile(r"^[0-9a-f]{7}$")


@pytest.mark.parametrize("key", sorted(SOURCES))
def test_every_source_is_complete(key: str) -> None:
    """A source missing any field cannot be checked against the primary record."""
    source = SOURCES[key]
    assert source.repo, f"{key}: no repository"
    assert source.path, f"{key}: no file or commit marker"
    assert source.detail, f"{key}: no statement of what it carries"


@pytest.mark.parametrize("key", sorted(SOURCES))
def test_every_commit_is_a_short_hash(key: str) -> None:
    """Seven lowercase hex characters: the form the sibling repositories log."""
    assert SHORT_HASH.match(SOURCES[key].commit), (
        f"{key}: {SOURCES[key].commit!r} is not a 7-character short hash"
    )


@pytest.mark.parametrize("key", sorted(SOURCES))
def test_every_date_is_iso(key: str) -> None:
    assert re.match(r"^2026-\d{2}-\d{2}$", SOURCES[key].date), f"{key}: date is not ISO"


def test_label_is_the_inline_citation_form() -> None:
    source = Source(repo="R", path="F.md", commit="abc1234", date="2026-01-01", detail="d")
    assert source.label == "R/F.md @ abc1234"


def test_the_seven_source_repositories_are_all_represented() -> None:
    """The note was commissioned against seven repositories. All seven are cited."""
    expected = {
        "NPDExperiment",
        "InsiderExperiment",
        "ETFExperiment",
        "HFExperiment",
        "MLCryptoEngine",
        "solattn",
        "solclear",
    }
    assert expected <= {source.repo for source in SOURCES.values()}
