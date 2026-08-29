"""Write generated blocks into the documents, and read them back out.

A generated block lives between a pair of HTML comments so the document stays
readable markdown and the block stays machine-owned::

    <!-- BEGIN GENERATED: headline-table -->
    ...
    <!-- END GENERATED: headline-table -->

Prose outside the markers is written by hand and is never touched. An empty
block is a legal starting state: that is how a new block is added to a document
before it has ever been rendered.

:func:`write_blocks` raises rather than reporting success when a marker pair it
found cannot be substituted. A sync tool that can report on work it did not do
is worse than no sync tool, because the drift test downstream would then be
comparing against a document nobody wrote.
"""

from __future__ import annotations

import re
from pathlib import Path

from rplimits.render import BLOCKS

ROOT = Path(__file__).resolve().parent.parent

BEGIN = "<!-- BEGIN GENERATED: {name} -->"
END = "<!-- END GENERATED: {name} -->"

#: Matches any begin marker and captures the block name.
BLOCK_NAME = re.compile(r"<!-- BEGIN GENERATED: ([a-z-]+) -->")


def _pattern(name: str) -> re.Pattern[str]:
    begin = re.escape(BEGIN.format(name=name))
    end = re.escape(END.format(name=name))
    return re.compile(rf"({begin}\n)(.*?)({end})", re.DOTALL)


def read_block(document: Path, name: str) -> str:
    """Return the contents of one generated block, without its framing newlines."""
    match = _pattern(name).search(document.read_text(encoding="utf-8"))
    if match is None:
        raise LookupError(f"{document.name} has no generated block named {name!r}")
    return match.group(2).strip("\n")


def blocks_in(document: Path) -> list[str]:
    """Every generated block name present in a document, in order."""
    return BLOCK_NAME.findall(document.read_text(encoding="utf-8"))


def write_blocks(document: Path) -> list[str]:
    """Regenerate every known block in a document. Returns the names rewritten."""
    text = document.read_text(encoding="utf-8")
    rewritten: list[str] = []
    for name in blocks_in(document):
        if name not in BLOCKS:
            raise LookupError(f"{document.name} names an unknown generated block: {name!r}")
        rendered = BLOCKS[name]()
        text, count = _pattern(name).subn(
            lambda m, body=rendered: f"{m.group(1)}{body}\n{m.group(3)}",  # type: ignore[misc]
            text,
        )
        if count != 1:
            raise RuntimeError(
                f"{document.name}: block {name!r} matched {count} times, expected exactly 1"
            )
        rewritten.append(name)
    document.write_text(text, encoding="utf-8")
    return rewritten


#: The documents that carry generated blocks.
DOCUMENTS = (ROOT / "SOURCES.md", ROOT / "docs" / "the-power-limit.md")
