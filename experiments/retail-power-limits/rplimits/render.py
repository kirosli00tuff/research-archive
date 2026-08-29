"""Markdown builders for the generated blocks in the documents.

Every generated block is delimited in the document by the markers in
:mod:`rplimits.docsync`, and ``tests/test_render.py`` re-renders each block and
compares it to what the document actually holds. A figure edited in the prose
but not in :mod:`rplimits.cases` — or the reverse — fails the build. That is
the whole point: the note quotes numbers it did not measure, so the numbers
have to be pinned to a single definition.
"""

from __future__ import annotations

from rplimits.cases import CONTRAST_CASES, HEADLINES, POWER_CASES, ContrastCase, Figure, PowerCase
from rplimits.sources import SOURCES


def cite(figure: Figure) -> str:
    """The inline citation line that follows a quoted figure."""
    source = SOURCES[figure.source]
    return f"*Source: {source.label} ({source.date}).*"


def headline_table() -> str:
    """The four cases, their effect bands, and their measured detectability."""
    rows = [
        "| experiment | effect band tested against | measured detectability | closed at |",
        "|---|---|---|---|",
    ]
    rows += [f"| **{h.case}** | {h.band} | {h.detectability} | {h.verdict} |" for h in HEADLINES]
    return "\n".join(rows)


def _power_block(case: PowerCase) -> str:
    fields = (
        ("Hypothesis", case.hypothesis),
        ("Effect band it was testing against", case.effect_band),
        ("Realized minimum detectable effect", case.realized_mde),
        ("Sample achieved", case.sample_achieved),
        ("Sample required", case.sample_required),
        ("Cost, in time and money", case.cost),
        ("Closure language, exact", case.closure_language),
    )
    parts = [f"### {case.repo} — closed {case.closed}", ""]
    for label, figure in fields:
        parts += [f"**{label}.** {figure.value}", "", cite(figure), ""]
    parts += [f"**Scope and correction.** {case.caveat}", ""]
    return "\n".join(parts).rstrip()


def _contrast_block(case: ContrastCase) -> str:
    fields = (
        ("What kind of closure", case.closure_type),
        ("Deciding number", case.deciding_number),
    )
    parts = [f"### {case.repo}", ""]
    for label, figure in fields:
        parts += [f"**{label}.** {figure.value}", "", cite(figure), ""]
    parts += [f"**Why it is not a power closure.** {case.why_not_power}", ""]
    return "\n".join(parts).rstrip()


def power_records() -> str:
    """The full extracted record for the four power cases."""
    return "\n\n".join(_power_block(case) for case in POWER_CASES)


def contrast_records() -> str:
    """The full extracted record for the three contrast cases."""
    return "\n\n".join(_contrast_block(case) for case in CONTRAST_CASES)


def source_registry() -> str:
    """Every cited location, so a reader can check the note without it."""
    rows = [
        "| key | repository | file | commit | date | what it carries |",
        "|---|---|---|---|---|---|",
    ]
    rows += [
        f"| `{key}` | {s.repo} | `{s.path}` | `{s.commit}` | {s.date} | {s.detail} |"
        for key, s in sorted(SOURCES.items())
    ]
    return "\n".join(rows)


#: Block name to builder. :mod:`rplimits.docsync` writes these into the
#: documents and ``tests/test_render.py`` checks them back out again.
BLOCKS = {
    "headline-table": headline_table,
    "power-records": power_records,
    "contrast-records": contrast_records,
    "source-registry": source_registry,
}
