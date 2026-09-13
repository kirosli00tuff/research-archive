"""Secrets, account numbers, and the figures this repository is not allowed to lose.

Rule 5 of ``CLAUDE.md``: secrets and account numbers never enter the repo. This
scans every **tracked** file for both key shapes and the IBKR account shapes, so a
pasted account number breaks the build rather than reaching a commit.

It scans tracked files rather than the working tree because ``.env`` is
deliberately present and deliberately untracked. Scanning the tree would fail on
the file the design requires to exist; scanning what git tracks asks the question
that actually matters, which is what a push would carry.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

#: IBKR account shapes. Paper accounts carry D (DU, DUR, DF); live carry U. Both
#: are treated as credential-shaped even though they are identifiers, because an
#: account number in a public repository is an invitation to a targeted attempt.
ACCOUNT_PATTERNS = (
    re.compile(r"\bDU[0-9]{6,9}\b"),
    re.compile(r"\bDUR[0-9]{5,9}\b"),
    re.compile(r"\bDF[0-9]{6,9}\b"),
    re.compile(r"\bU[0-9]{7,9}\b"),
)

#: Key shapes. Deliberately broad: a false positive costs a rename and a false
#: negative costs a rotated credential.
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{12,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"),
)

#: The ONLY exemption, and it is line-scoped rather than file-scoped. A line
#: carrying this marker may hold an account shape. A file-wide allowlist would
#: mean a real account pasted anywhere in an exempt file passes unnoticed; a
#: line marker makes every exemption visible at the exact line and makes claiming
#: one a deliberate act rather than an accident.
SYNTHETIC_MARKER = "SYNTHETIC-FIXTURE"

#: Files permitted to carry the marker at all. A marker outside these is itself
#: a finding, so the exemption cannot spread into the package.
MARKER_PERMITTED_IN = frozenset({"tests/test_honesty.py", "tests/test_guards.py"})


def scan_lines(text: str, patterns: tuple[re.Pattern[str], ...]) -> list[tuple[int, str]]:
    """Match ``patterns`` line by line, skipping lines marked synthetic."""
    hits: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if SYNTHETIC_MARKER in line:
            continue
        for pattern in patterns:
            for match in pattern.finditer(line):
                hits.append((number, match.group()))
    return hits


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=REPO, capture_output=True, text=True, check=True
    )
    return [REPO / name for name in result.stdout.split("\0") if name]


def readable_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def test_no_tracked_file_carries_an_ibkr_account_number() -> None:
    """An account shape is a finding unless its own line is marked synthetic."""
    offenders: list[str] = []
    for path in tracked_files():
        text = readable_text(path) if path.exists() else None
        if text is None:
            continue
        relative = str(path.relative_to(REPO))
        offenders += [f"{relative}:{n}: {m!r}" for n, m in scan_lines(text, ACCOUNT_PATTERNS)]
    assert not offenders, "tracked files carry IBKR account shapes:\n" + "\n".join(offenders)


def test_no_tracked_file_carries_a_key_shaped_string() -> None:
    offenders: list[str] = []
    for path in tracked_files():
        text = readable_text(path) if path.exists() else None
        if text is None:
            continue
        relative = str(path.relative_to(REPO))
        offenders += [f"{relative}:{n}: {m[:40]!r}" for n, m in scan_lines(text, SECRET_PATTERNS)]
    assert not offenders, "tracked files carry key shapes:\n" + "\n".join(offenders)


def test_the_synthetic_marker_cannot_spread_beyond_the_test_suite() -> None:
    """The exemption is narrow by construction, and this keeps it narrow."""
    offenders = []
    for path in tracked_files():
        relative = str(path.relative_to(REPO))
        if relative in MARKER_PERMITTED_IN or not path.exists():
            continue
        text = readable_text(path)
        if text is not None and SYNTHETIC_MARKER in text:
            offenders.append(relative)
    assert not offenders, f"the synthetic marker appears outside the suite: {offenders}"


def test_the_exemption_is_line_scoped_and_does_not_reach_the_next_line() -> None:
    """A marker on one line must not exempt the line below it."""
    marked = "acct = 'DU1234567'  # " + SYNTHETIC_MARKER  # SYNTHETIC-FIXTURE
    unmarked = "leak = 'DU7654321'"  # SYNTHETIC-FIXTURE
    hits = scan_lines(marked + "\n" + unmarked + "\n", ACCOUNT_PATTERNS)
    assert [n for n, _ in hits] == [2], f"expected only line 2 to be a finding, got {hits}"


def test_the_env_file_is_not_tracked() -> None:
    tracked = {str(p.relative_to(REPO)) for p in tracked_files()}
    assert ".env" not in tracked, ".env must never be tracked"
    assert ".env.example" in tracked, ".env.example is the tracked template"


def test_the_scanner_actually_matches_the_shapes_it_claims_to() -> None:
    """A scanner nobody has seen fire is a scanner nobody has tested."""
    paper = "acct DU1234567 x"  # SYNTHETIC-FIXTURE
    live = "acct U1234567 x"  # SYNTHETIC-FIXTURE
    dur = "acct DUR123456 x"  # SYNTHETIC-FIXTURE
    key = 'api_key = "abcdefghijklmnop"'  # SYNTHETIC-FIXTURE
    assert any(p.search(paper) for p in ACCOUNT_PATTERNS)
    assert any(p.search(live) for p in ACCOUNT_PATTERNS)
    assert any(p.search(dur) for p in ACCOUNT_PATTERNS)
    assert any(p.search(key) for p in SECRET_PATTERNS)


@pytest.mark.parametrize(
    "phrase",
    [
        "7,812.46",
        "12.80%",
        "49.610",
        "34.600",
        "142.740",
        "112.72",
        "21.760",
        "60.4%",
    ],
)
def test_claude_md_still_carries_every_load_bearing_figure(phrase: str) -> None:
    """A project that can quietly drop an inconvenient measured figure will.

    Every figure the two gates rest on is pinned into the build, so deleting one
    from the operating manual breaks the suite rather than passing unnoticed.
    """
    text = (REPO / "CLAUDE.md").read_text(encoding="utf-8")
    assert phrase in text, f"CLAUDE.md no longer carries {phrase!r}"


def test_no_execution_shaped_name_exists_in_the_package() -> None:
    """The scope statement says this package transmits no order. A name that can
    only mean placing one contradicts it, and prose alone cannot hold that."""
    banned = ("def place_order", "def submit_order", "def send_order", "def transmit")
    for path in sorted((REPO / "src" / "mbt").rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for name in banned:
            assert name not in text, f"{path.name} defines {name!r}"
