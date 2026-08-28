"""The registered pair types (Amendment H2-3 Change 1), and nothing else.

Two string constants live in their own module so that the dark H2 pair
reader can name a stratum without importing anything that owns a path. The
reader's structural pin holds it to pure modules; a constant is pure, a
ledger writer is not.
"""

from __future__ import annotations

from typing import Final

# Tagged at assignment. The tag names a stratum; it never filters a
# primary statistic.
PAIR_TYPE_SAME_DEX: Final = "same_dex"
PAIR_TYPE_CROSS_DEX: Final = "cross_dex"
REGISTERED_PAIR_TYPES: Final[tuple[str, str]] = (PAIR_TYPE_SAME_DEX, PAIR_TYPE_CROSS_DEX)
