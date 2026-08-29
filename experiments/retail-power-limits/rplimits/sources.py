"""Every figure in this repository resolves to a repository, a file and a commit.

The note is a secondary source. It quotes numbers measured elsewhere, and a
reader who does not trust it must be able to check each one against the
primary record without asking this repository for help. That is what this
module exists to make mechanical: a figure with no resolvable source cannot be
added, because :mod:`rplimits.cases` types every value as a
:class:`~rplimits.cases.Figure` carrying a key into :data:`SOURCES`, and
``tests/test_sources.py`` fails on a key that does not resolve.

Commits are recorded as the short hash that last touched the cited file, or as
the commit whose message carries the claim. Both forms are stable: these
repositories are closed, and a closed repository does not move.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Source:
    """One citable location in one of the sibling repositories."""

    repo: str
    path: str
    commit: str
    date: str
    detail: str

    @property
    def label(self) -> str:
        """``repo/path @ commit`` — the form quoted inline in the note."""
        return f"{self.repo}/{self.path} @ {self.commit}"


#: Keyed by the short slug used throughout :mod:`rplimits.cases`.
SOURCES: dict[str, Source] = {
    "npd-registration": Source(
        repo="NPDExperiment",
        path="REGISTRATION.md",
        commit="2d3d0ae",
        date="2026-08-25",
        detail="Section 9 power derivation, Section 17 amendments, and the Closure section",
    ),
    "npd-progress": Source(
        repo="NPDExperiment",
        path="progress.md",
        commit="2d3d0ae",
        date="2026-08-25",
        detail="Stage Z.1 closure, B.2 evaluation, B.1 collection, A.2 registration",
    ),
    "npd-decisions": Source(
        repo="NPDExperiment",
        path="DECISIONS.md",
        commit="2d3d0ae",
        date="2026-08-25",
        detail="ADR-007 registering the contrast power honestly; ADR-011 reading realized power first",
    ),
    "npd-close": Source(
        repo="NPDExperiment",
        path="(closing commit)",
        commit="2d3d0ae",
        date="2026-08-25",
        detail='"Close the experiment at unresolved-at-achievable-power, two attempts and zero positives, artifacts preserved"',
    ),
    "insider-registration": Source(
        repo="InsiderExperiment",
        path="REGISTRATION.md",
        commit="12d9fd3",
        date="2026-08-25",
        detail="Section 0 gates, Section 15.5-15.7 the fired gate, Section 17 closure",
    ),
    "insider-decisions": Source(
        repo="InsiderExperiment",
        path="DECISIONS.md",
        commit="12d9fd3",
        date="2026-08-25",
        detail="ADR-001 answering power before alpha; ADR-010 closure; ADR-011 reopening boundary",
    ),
    "insider-section0": Source(
        repo="InsiderExperiment",
        path="(commit)",
        commit="fbfc74e",
        date="2026-08-25",
        detail='"feat: scaffold, standing guards, and REGISTRATION Section 0 power gate" — the gate committed before the measurement it judges',
    ),
    "insider-gate": Source(
        repo="InsiderExperiment",
        path="(commit)",
        commit="cb17046",
        date="2026-08-25",
        detail='"feat: the power gate, computed without reading alpha. BLOCKED at 49.35 bp"',
    ),
    "insider-close": Source(
        repo="InsiderExperiment",
        path="(closing commit)",
        commit="12d9fd3",
        date="2026-08-25",
        detail='"Close at BLOCKED on the power gate, weight concentration not corpus, artifacts preserved"',
    ),
    "etf-registration": Source(
        repo="ETFExperiment",
        path="REGISTRATION.md",
        commit="4d11002",
        date="2026-08-28",
        detail="Section 0 outcome map, Section 9 power method, Amendments 3 to 6",
    ),
    "etf-readme": Source(
        repo="ETFExperiment",
        path="README.md",
        commit="fe60a22",
        date="2026-08-28",
        detail="the measured-so-far table, each figure with its n",
    ),
    "etf-close": Source(
        repo="ETFExperiment",
        path="(closing commit)",
        commit="3f5d629",
        date="2026-08-28",
        detail='"Close H1 at untestable-at-achievable-power on the deadline finding, artifacts preserved"',
    ),
    "etf-disarm": Source(
        repo="ETFExperiment",
        path="(closing commit)",
        commit="4d11002",
        date="2026-08-28",
        detail='"Disarm etf-snap; correct the reopen-path mislabel in Amendment 5 and ADR-019"',
    ),
    "hf-registration": Source(
        repo="HFExperiment",
        path="REGISTRATION.md",
        commit="f13e1d3",
        date="2026-08-25",
        detail="Section 4 widths, Section 11 verdict schedule, and the amendment log closure entry",
    ),
    "hf-readme": Source(
        repo="HFExperiment",
        path="README.md",
        commit="0a0d214",
        date="2026-08-23",
        detail="the one-line statement of what H-F is and how it resolved",
    ),
    "hf-progress": Source(
        repo="HFExperiment",
        path="progress.md",
        commit="82e77a0",
        date="2026-08-28",
        detail="the 2026-08-26 closure entry and the Stage A.1b broker verdict",
    ),
    "hf-close": Source(
        repo="HFExperiment",
        path="(closing commit)",
        commit="f13e1d3",
        date="2026-08-25",
        detail='"docs: terminal closure, shadow timer disarmed, closure recorded in amendment log and progress"',
    ),
    "aitrader-return": Source(
        repo="AiTrader",
        path="RETURN.md",
        commit="f819b68",
        date="2026-07-29",
        detail="the cross-sectional round headline and the H-F width tables",
    ),
    "aitrader-round": Source(
        repo="AiTrader",
        path="(round commit)",
        commit="a0a9ef6",
        date="2026-07-26",
        detail='"Cross-sectional hypothesis round against the breadth universe, scored as a 5-position book at Level 1 sizing, holdout touched once, findings only, nothing applied"',
    ),
    "mlc-hypotheses": Source(
        repo="MLCryptoEngine",
        path="HYPOTHESES.md",
        commit="d2a0f05",
        date="2026-08-12",
        detail="the eleven-entry hypothesis register with each closure type and deciding number",
    ),
    "mlc-h1note": Source(
        repo="MLCryptoEngine",
        path="docs/notes/h1-predictability-without-capturability.md",
        commit="ae03bf6",
        date="2026-08-22",
        detail="the AUC-versus-capture note and the fee-floor arithmetic",
    ),
    "solattn-registration": Source(
        repo="solattn",
        path="REGISTRATION.md",
        commit="b3f5062",
        date="2026-08-28",
        detail="Amendment 7, which records the Stage B readout and the horizon never analysed",
    ),
    "solattn-findings": Source(
        repo="solattn",
        path="FINDINGS.md",
        commit="b3f5062",
        date="2026-08-28",
        detail="the Stage B documented negative, with every figure carrying its n",
    ),
    "solclear-findings": Source(
        repo="solclear",
        path="FINDINGS.md",
        commit="c692032",
        date="2026-08-22",
        detail="the Stage E outcome study, the crawler-survivorship result, and the priced-out confirmation",
    ),
}
