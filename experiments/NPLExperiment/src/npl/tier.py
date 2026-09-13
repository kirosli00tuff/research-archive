"""The registered control tiers (Amendment H2-5 section 2), and nothing else.

Three integer constants in their own module, for the reason `npl.pairtype`
exists: the dark H2 pair reader names a tier stratum, and its structural pin
holds it to pure modules. A constant is pure; a ledger writer is not.
"""

from __future__ import annotations

from typing import Final

# Consulted in order; the first tier that yields a candidate wins.
TIER_SAME_DEX_EXACT_CLASS: Final = 1
TIER_ANY_DEX_EXACT_CLASS: Final = 2
TIER_ANY_DEX_EQUITY_COMPLEX: Final = 3

REGISTERED_TIERS: Final[tuple[int, int, int]] = (
    TIER_SAME_DEX_EXACT_CLASS,
    TIER_ANY_DEX_EXACT_CLASS,
    TIER_ANY_DEX_EQUITY_COMPLEX,
)

TIER_NAMES: Final[dict[int, str]] = {
    TIER_SAME_DEX_EXACT_CLASS: "same_dex_exact_class",
    TIER_ANY_DEX_EXACT_CLASS: "any_dex_exact_class",
    TIER_ANY_DEX_EQUITY_COMPLEX: "any_dex_equity_complex",
}
