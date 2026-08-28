"""Stage B: the single registered read of the sealed retro cohort.

This package holds the Stage B surface and nothing else: the B.0
preconditions (counts, timestamps, and hashes only), the sealed reader
registered by Amendment 3 as the one blindness exemption, and the
one-shot CLI behind the latch. Stage B sends no network request; every
input is already on disk.
"""

from typing import Final

# Amendment 3: the blindness allowlist gains exactly one module. The AST
# pins in tests/test_guards.py hold this tuple at length one with the
# Stage B CLI as the reader's only importer; widening it is a caught
# mutation (reports/stage_b/mutations.md).
STAGE_B_OUTCOME_EXEMPT: Final[tuple[str, ...]] = ("stageb/reader.py",)
