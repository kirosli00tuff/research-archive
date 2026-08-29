"""Guards over the gate pipeline (REGISTRATION.md Sections 0.6 and 10).

Two guards, each with a test that fails when the guard is removed:

1. Outcome blindness: no gate module may reference a resolution-outcome
   field, by identifier or by string key. Scanned over the AST so prose in
   docstrings cannot trip it and subscript keys cannot slip past it.
2. Enforcement sites: every registered bar must actually be read by the gate
   code. A bar nothing reads is not a gate.

The scanner itself is tested against a synthetic violating source, so the
suite contains proof that the guard can fail.
"""

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent / "pmexperiment"

# Modules that feed or fire a gate. band.py joined in Stage B: Amendment 3
# orders the band gate ahead of the power gate, so it is bound by the same
# outcome-blindness rule even though it reads no venue at all.
GATE_MODULES = ("power.py", "band.py")

FORBIDDEN_TOKENS = frozenset(
    {
        "result",
        "results",
        "outcome",
        "outcomes",
        "yes_result",
        "no_result",
        "settlement_value",
        "winner",
    }
)


def _violations(source: str) -> list[str]:
    """Every forbidden token appearing as an identifier or exact string key."""
    tree = ast.parse(source)
    found: list[str] = []
    for node in ast.walk(tree):
        candidates: list[str] = []
        if isinstance(node, ast.Name):
            candidates.append(node.id)
        elif isinstance(node, ast.Attribute):
            candidates.append(node.attr)
        elif isinstance(node, ast.arg | ast.keyword):
            if node.arg is not None:
                candidates.append(node.arg)
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            candidates.append(node.name)
        elif isinstance(node, ast.alias):
            candidates.append(node.asname or node.name)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            candidates.append(node.value)
        found.extend(c for c in candidates if c in FORBIDDEN_TOKENS)
    return found


def test_gate_modules_never_reference_an_outcome_field() -> None:
    for module in GATE_MODULES:
        source = (PACKAGE / module).read_text(encoding="utf-8")
        assert _violations(source) == [], (
            f"{module} references a resolution-outcome token; "
            "the gate must stay outcome-blind (REGISTRATION.md Section 10)"
        )


def test_the_scanner_itself_can_fail() -> None:
    """A guard that has never failed is not a guard: feed it a violation."""
    bad_attribute = "def f(m):\n    return m.result\n"
    bad_key = 'def f(m):\n    return m["outcome"]\n'
    assert _violations(bad_attribute) == ["result"]
    assert _violations(bad_key) == ["outcome"]


def test_every_registered_bar_has_an_enforcement_site() -> None:
    """The check demands the actual registry reference, not the bare name.

    First mutation run caught a weakness here: replacing the reference with a
    literal passed, because a docstring mentions the bare name. The guard now
    requires `registry.<bar>` in the code itself.
    """
    source = (PACKAGE / "power.py").read_text(encoding="utf-8")
    for bar in ("EFFECT_BAND_LO", "EFFECT_BAND_HI", "Z_CRITICAL"):
        assert f"registry.{bar}" in source, (
            f"{bar} is registered but nothing enforces it"
        )


def test_the_band_gate_enforces_both_band_edges_and_the_turnover() -> None:
    """Amendment 4 reports both quantifiers, so both band edges must be read.

    The turnover is on this list because a registered constant no code reads
    is not a gate. `registry.FX_TURNOVER_REGISTERED` is the default argument
    of every priced function in band.py, so the registered k = 1 case binds
    unless a caller names another and the amendment cannot drift from the code.
    """
    source = (PACKAGE / "band.py").read_text(encoding="utf-8")
    for bar in ("EFFECT_BAND_LO", "EFFECT_BAND_HI", "FX_TURNOVER_REGISTERED"):
        assert f"registry.{bar}" in source, (
            f"{bar} is registered but the band gate never reads it"
        )
