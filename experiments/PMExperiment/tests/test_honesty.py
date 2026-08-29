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


def test_registration_section_zero_is_registered() -> None:
    """Section 0 was committed in Stage A Task 0, before the first request.

    This replaces the inverted scaffold test in the same commit that removed
    the NOT YET REGISTERED banner, exactly as that test's docstring promised.
    """
    reg = _read("REGISTRATION.md")
    assert "NOT YET REGISTERED" not in reg
    assert "Section 0 registered 2026-08-29" in reg
    assert "0.02 to 0.08" in reg
    assert "The split verdict is registered in advance as a finding" in reg
    assert "no cost can be chosen after seeing a result" in reg


def test_env_example_declares_no_credential() -> None:
    env = _read(".env.example")
    assert "=" not in env, "Stage A needs no credential; .env.example stays empty"


def test_hypotheses_register_exists_with_h1_open() -> None:
    h = _read("HYPOTHESES.md")
    assert "H1 OPEN, not yet registered" in h
    assert "Closed before opening" in h


def test_registration_carries_the_house_section_set() -> None:
    """Sections 0 through 17, with 17 reserved for amendments."""
    reg = (ROOT / "REGISTRATION.md").read_text(encoding="utf-8")
    for n in range(18):
        assert f"## {n}. " in reg, f"REGISTRATION.md is missing section {n}"
    assert "## 17. Amendments" in reg


def test_progress_reserves_entry_zero_for_the_operator_prompt() -> None:
    p = _read("progress.md")
    assert "Entry 0 is reserved" in p
    assert "logged verbatim before any other work" in p


def test_report_claims_nothing_yet() -> None:
    r = _read("report.md")
    assert "No stage has run" in r
    assert "Nothing is claimed here" in r
