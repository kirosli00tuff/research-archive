"""Run Stage B.2. Once.

This module names no store and reads no outcome. It calls the evaluator, which
is the only module permitted to open the sealed store.
"""

from __future__ import annotations

import sys

from npd.eval.evaluator import run_b2
from npd.eval.report import write_report


def main() -> int:
    result = run_b2()
    path = write_report(result)
    print(f"B.2 complete. Report written to {path}")
    if not result.gate_passed:
        print(f"STOPPED AT THE VALIDITY GATE: {result.stopped_reason}")
        return 1
    print(f"Verdict row: {result.verdict_row}")
    print(f"C.1 authorized: {result.c1_authorized}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
