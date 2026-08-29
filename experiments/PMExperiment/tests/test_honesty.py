"""Honesty tests.

These assert that the repository's scope statement and its power precedent
stay in the documents a reader arrives at first. They are load-bearing: if a
future session removes one of these sentences, the build fails.

A gate that has never failed is not a gate, so each assertion here names a
specific sentence rather than a vague property.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read(name: str) -> str:
    """Read a document with whitespace folded to single spaces.

    Markdown hard-wraps prose, so a sentence that is genuinely present can
    still fail a literal substring match purely because a line break landed
    mid-phrase. Folding whitespace makes these tests assert on content rather
    than on line-wrap accidents. The fix belongs here, in the reader, not in
    rewording the document to satisfy a brittle matcher.
    """
    raw = (ROOT / name).read_text(encoding="utf-8")
    return " ".join(raw.split())


def test_readme_states_it_never_trades() -> None:
    readme = _read("README.md")
    assert "never trades, holds no account, places no order" in readme
    assert "no stage in which one is planned" in readme


def test_readme_states_a_negative_is_valid() -> None:
    readme = _read("README.md")
    assert "A documented negative is a valid and expected outcome" in readme
    assert "BLOCKED" in readme


def test_readme_carries_the_npd_power_precedent_with_its_figures() -> None:
    readme = _read("README.md")
    assert "0.0512" in readme
    assert "0.01 to 0.05" in readme
    assert "415 days" in readme


def test_readme_carries_the_insider_gate_figure() -> None:
    readme = _read("README.md")
    assert "49.35 bp" in readme


def test_readme_states_the_canadian_doubt_rather_than_hiding_it() -> None:
    readme = _read("README.md")
    assert "30-day minimum maturity" in readme
    assert "not reachable from Canada" in readme


def test_claude_md_carries_the_no_first_moment_rule() -> None:
    claude = _read("CLAUDE.md")
    assert "No first moment before the gate" in claude
    assert "counts and dispersion only" in claude


def test_claude_md_forbids_tuning_the_filter() -> None:
    claude = _read("CLAUDE.md")
    assert "Do not tune a filter to increase a sample" in claude


def test_registration_is_not_yet_registered() -> None:
    """Section 0 must be written before the first request.

    This test is deliberately inverted: while the scaffold banner is present,
    no request may be sent. Stage A Task 0 removes the banner in the same
    commit that registers Section 0, and this test is replaced then.
    """
    reg = _read("REGISTRATION.md")
    assert "NOT YET REGISTERED" in reg


def test_env_example_declares_no_credential() -> None:
    env = _read(".env.example")
    assert "=" not in env, "Stage A needs no credential; .env.example stays empty"
