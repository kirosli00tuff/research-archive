"""Guard one — the no-transmit scan. An AST walk, never a text search.

**Why this is a parse-tree walk and not a grep.** A previous project's config
guard scanned raw text, matched its key inside a trailing comment, and called
that enforcement. A text scan cannot tell a call from a comment, a live
assignment from a docstring, or a literal ``True`` from a variable that happens
to be spelled ``True``. Every check below inspects typed AST nodes.

**What the scan enforces, and why it has this shape rather than the literal one.**
Measured against ``ib_async 2.1.0``: ``IB.placeOrder(contract, order)``
**transmits** and accepts **no** ``whatIf`` keyword at all. ``whatIf`` is a field
on the ``Order`` object, and ``IB.whatIfOrder`` copies the order, sets
``whatIf = True`` and previews. So a ``whatIf=True`` keyword written onto a
``placeOrder`` call would be **theatre**: the method does not read one and would
transmit anyway.

The registered rule is therefore enforced where the flag genuinely lives, in
three parts:

1. **No transmitting call site exists in the package at all.** The set is empty,
   not guarded. A call that cannot be written cannot be misconfigured.
2. **Every order construction carries ``whatIf=True`` as a literal keyword.**
3. **Every call of the package's own preview wrapper carries ``whatIf=True`` as
   a literal keyword.**

Parts 2 and 3 fail the build on all three registered failure modes: a **missing**
flag, a **``False`` literal**, and a flag **supplied from a variable, an
attribute, a call or a ``**`` splat**. A value that is not a literal cannot be
verified at build time, so it is refused rather than trusted.

Run standalone (``python tools/no_transmit_scan.py``) or import
:func:`scan_package` from a test. Both paths walk the same trees.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import asdict, dataclass
from enum import StrEnum, unique
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "src" / "mbt"
TOOLS = REPO / "tools"

#: Broker methods that place, modify or cancel a live order. **Not one of these
#: may appear as a call site anywhere in the package.** ``placeOrder`` is the
#: registered name; the rest are the neighbouring transmit paths on the same
#: client object, banned together because banning only the registered one would
#: leave the others as an open door.
BANNED_TRANSMIT_METHODS = frozenset(
    {
        "placeOrder",
        "placeOrderAsync",
        "cancelOrder",
        "cancelOrderAsync",
        "reqGlobalCancel",
        "reqGlobalCancelAsync",
        "exerciseOptions",
        "exerciseOptionsAsync",
    }
)

#: Order constructors. Every one must carry ``whatIf=True`` as a literal.
ORDER_CONSTRUCTORS = frozenset(
    {"Order", "LimitOrder", "MarketOrder", "StopOrder", "StopLimitOrder"}
)

#: The package's own preview wrapper. The only broker order path that exists
#: here, and the one whose call sites carry the literal flag.
PREVIEW_WRAPPERS = frozenset({"what_if_order"})

#: Dynamic-attribute builtins. ``getattr(ib, "placeOrder")`` would defeat every
#: check above, so a string naming a banned method inside one of these is itself
#: a finding. This inspects Call and Constant NODES, not raw file text, so a
#: docstring mentioning a method name is not a false positive.
DYNAMIC_ATTRIBUTE_BUILTINS = frozenset({"getattr", "setattr", "hasattr"})

#: Builtins that execute source at runtime. A package that can ``exec`` cannot be
#: statically guaranteed by any AST walk, including this one.
BANNED_DYNAMIC_EXECUTION = frozenset({"eval", "exec"})


@unique
class Rule(StrEnum):
    """Which registered rule a finding violates."""

    TRANSMIT_CALL_SITE = "transmit_call_site"
    WHATIF_MISSING = "whatif_missing"
    WHATIF_FALSE_LITERAL = "whatif_false_literal"
    WHATIF_NOT_A_LITERAL = "whatif_not_a_literal"
    DYNAMIC_ATTRIBUTE_DODGE = "dynamic_attribute_dodge"
    DYNAMIC_EXECUTION = "dynamic_execution"


@dataclass(frozen=True, slots=True)
class Finding:
    """One violation, located precisely enough to fix."""

    rule: Rule
    path: str
    line: int
    col: int
    callee: str
    detail: str


def _callee_name(node: ast.expr) -> str:
    """The dotted-ish name of a call target, for reporting and matching."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return type(node).__name__


def _find_whatif_keyword(call: ast.Call) -> tuple[ast.keyword | None, bool]:
    """Return the ``whatIf`` keyword and whether a ``**`` splat is present.

    A ``**kwargs`` splat can supply ``whatIf`` from anywhere, so its presence is
    reported even when an explicit literal is also written: the splat can
    override, and which wins is not decidable at build time.
    """
    found: ast.keyword | None = None
    splat = False
    for keyword in call.keywords:
        if keyword.arg is None:
            splat = True
        elif keyword.arg == "whatIf":
            found = keyword
    return found, splat


def _check_literal_whatif(call: ast.Call, path: Path, callee: str) -> list[Finding]:
    """Require ``whatIf=True`` as a literal keyword on one call site."""
    relative = str(path.relative_to(REPO))
    keyword, splat = _find_whatif_keyword(call)

    if splat:
        return [
            Finding(
                rule=Rule.WHATIF_NOT_A_LITERAL,
                path=relative,
                line=call.lineno,
                col=call.col_offset,
                callee=callee,
                detail=(
                    "keyword arguments are supplied by a ** splat, so whatIf may "
                    "be overridden from a value this scan cannot see. A flag that "
                    "is not a build-time literal cannot be verified at build time."
                ),
            )
        ]

    if keyword is None:
        return [
            Finding(
                rule=Rule.WHATIF_MISSING,
                path=relative,
                line=call.lineno,
                col=call.col_offset,
                callee=callee,
                detail="no whatIf keyword. Every order construction and preview call carries whatIf=True.",
            )
        ]

    value = keyword.value
    if isinstance(value, ast.Constant) and value.value is True:
        return []
    if isinstance(value, ast.Constant) and value.value is False:
        return [
            Finding(
                rule=Rule.WHATIF_FALSE_LITERAL,
                path=relative,
                line=keyword.value.lineno,
                col=keyword.value.col_offset,
                callee=callee,
                detail="whatIf=False. This repository transmits no order, ever.",
            )
        ]
    return [
        Finding(
            rule=Rule.WHATIF_NOT_A_LITERAL,
            path=relative,
            line=keyword.value.lineno,
            col=keyword.value.col_offset,
            callee=callee,
            detail=(
                f"whatIf is supplied from {type(value).__name__}, not a literal. "
                "A value that is not a literal cannot be verified at build time, "
                "so it is refused rather than trusted."
            ),
        )
    ]


def scan_source(source: str, path: Path, *, full: bool) -> list[Finding]:
    """Walk one parse tree. ``full`` adds the checks that only the package needs."""
    findings: list[Finding] = []
    tree = ast.parse(source, filename=str(path))
    relative = str(path.relative_to(REPO))

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        callee = _callee_name(node.func)

        if callee in BANNED_TRANSMIT_METHODS:
            findings.append(
                Finding(
                    rule=Rule.TRANSMIT_CALL_SITE,
                    path=relative,
                    line=node.lineno,
                    col=node.col_offset,
                    callee=callee,
                    detail=(
                        f"{callee} places, modifies or cancels a live order. No "
                        "such call site exists in this package. Every broker "
                        "interaction is a whatIf preview or a market-data read."
                    ),
                )
            )
            continue

        if not full:
            continue

        if callee in ORDER_CONSTRUCTORS or callee in PREVIEW_WRAPPERS:
            findings.extend(_check_literal_whatif(node, path, callee))
            continue

        if callee in BANNED_DYNAMIC_EXECUTION and isinstance(node.func, ast.Name):
            findings.append(
                Finding(
                    rule=Rule.DYNAMIC_EXECUTION,
                    path=relative,
                    line=node.lineno,
                    col=node.col_offset,
                    callee=callee,
                    detail=(
                        f"{callee} executes source at runtime, which no AST walk "
                        "can inspect. A package that can exec cannot be statically "
                        "guaranteed not to transmit."
                    ),
                )
            )
            continue

        if callee in DYNAMIC_ATTRIBUTE_BUILTINS:
            for argument in node.args:
                if (
                    isinstance(argument, ast.Constant)
                    and isinstance(argument.value, str)
                    and argument.value in BANNED_TRANSMIT_METHODS
                ):
                    findings.append(
                        Finding(
                            rule=Rule.DYNAMIC_ATTRIBUTE_DODGE,
                            path=relative,
                            line=node.lineno,
                            col=node.col_offset,
                            callee=f"{callee}(..., {argument.value!r})",
                            detail=(
                                "a transmitting method is named as a string inside "
                                "a dynamic-attribute builtin, which would reach the "
                                "method without ever writing a call site for it."
                            ),
                        )
                    )
    return findings


def scan_package(package: Path = PACKAGE, tools: Path | None = TOOLS) -> list[Finding]:
    """Scan the whole package, and the tools for transmitting call sites.

    The package gets every check. ``tools/`` gets the transmit-call-site check
    only: this module and the mutation harness both hold banned method names as
    data, and a scanner that flags its own vocabulary is a scanner nobody can run.
    """
    findings: list[Finding] = []
    for path in sorted(package.rglob("*.py")):
        findings.extend(scan_source(path.read_text(encoding="utf-8"), path, full=True))
    if tools is not None:
        for path in sorted(tools.rglob("*.py")):
            findings.extend(scan_source(path.read_text(encoding="utf-8"), path, full=False))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Guard one, the no-transmit AST scan.")
    parser.add_argument("--json", default="", help="also write findings to this path")
    args = parser.parse_args()

    findings = scan_package()
    payload = {
        "guard": "no_transmit_ast_scan",
        "method": "ast.walk over every parse tree in src/mbt, and over tools/ for transmit call sites",
        "package_files_scanned": len(list(PACKAGE.rglob("*.py"))),
        "tools_files_scanned": len(list(TOOLS.rglob("*.py"))),
        "banned_transmit_methods": sorted(BANNED_TRANSMIT_METHODS),
        "order_constructors_requiring_literal": sorted(ORDER_CONSTRUCTORS),
        "preview_wrappers_requiring_literal": sorted(PREVIEW_WRAPPERS),
        "findings": [asdict(f) | {"rule": str(f.rule)} for f in findings],
        "finding_count": len(findings),
        "verdict": "CLEAN" if not findings else "FAILED",
    }
    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if findings:
        print(f"NO-TRANSMIT SCAN FAILED: {len(findings)} finding(s)", file=sys.stderr)
        for finding in findings:
            print(
                f"  {finding.path}:{finding.line}:{finding.col} "
                f"[{finding.rule}] {finding.callee} — {finding.detail}",
                file=sys.stderr,
            )
        return 1
    print(
        f"no-transmit scan CLEAN: {payload['package_files_scanned']} package files "
        f"and {payload['tools_files_scanned']} tool files walked, 0 findings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
