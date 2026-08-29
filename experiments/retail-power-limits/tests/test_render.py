"""Drift tests. A figure edited in one place and not the other fails the build.

The documents carry generated blocks between HTML-comment markers. These tests
re-render each block from :mod:`rplimits.cases` and compare it to what the
document holds on disk, so the prose and the sourced data cannot diverge
silently. Regenerate with ``uv run python -m rplimits --write``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from rplimits.docsync import DOCUMENTS, blocks_in, read_block
from rplimits.render import BLOCKS, cite, headline_table
from rplimits.sources import SOURCES

CASES = [(document, name) for document in DOCUMENTS for name in blocks_in(document)]


def test_every_document_exists() -> None:
    for document in DOCUMENTS:
        assert document.is_file(), f"{document} is missing"


def test_documents_carry_generated_blocks() -> None:
    assert CASES, "no generated blocks found; the drift check would pass vacuously"


@pytest.mark.parametrize(("document", "name"), CASES, ids=lambda v: getattr(v, "name", v))
def test_generated_blocks_are_current(document: Path, name: str) -> None:
    """The block on disk equals the block the data renders."""
    assert read_block(document, name) == BLOCKS[name](), (
        f"{document.name}: generated block {name!r} is stale. "
        "Run `uv run python -m rplimits --write`."
    )


def test_every_builder_is_used_by_some_document() -> None:
    """A renderer nothing renders is dead code, and dead code drifts unnoticed."""
    used = {name for _, name in CASES}
    assert set(BLOCKS) == used, f"unused builders: {set(BLOCKS) - used}"


def test_drift_detector_fires() -> None:
    """Canary: the comparison must fail when the rendered block genuinely differs."""
    assert headline_table() != BLOCKS["source-registry"]()


def test_citation_names_repository_file_and_commit() -> None:
    from rplimits.cases import NPD

    line = cite(NPD.realized_mde)
    source = SOURCES[NPD.realized_mde.source]
    assert source.repo in line
    assert source.path in line
    assert source.commit in line
    assert source.date in line
