"""Operating paces, measured 2026-08-27T01:00-01:18Z. Measured beats documented.

The solattn lesson holds here: ceilings are per endpoint, never per host, and
measured never assumed. The A.1 Task 2 escalation (docs/ACCESS.md) found
refusals on exactly two endpoints at probe scale; everywhere else the ceiling
sits above what the probe reached, and the operating pace is half the highest
verified-clean rate instead, with the basis recorded beside each figure.

A 429's body on this venue is the four bytes `null` — the refusal shape,
verbatim.
"""

from __future__ import annotations

from typing import Final

from npl.api import (
    EP_CANDLE_SNAPSHOT,
    EP_FUNDING_HISTORY,
    EP_L2_BOOK,
    EP_META,
    EP_META_AND_CTXS,
    EP_PERP_DEXS,
)

# endpoint -> seconds between sends. Derivations, all from the A.1 measurement:
#   meta:            no refusal at probe scale; highest verified clean 160/min
#                    sustained -> half = 80/min -> 0.75 s; 0.8 chosen.
#   metaAndAssetCtxs: no refusal; verified clean burst ~176/min -> half -> 0.8 s.
#   perpDexs:        MEASURED ceiling: 79 admitted then 429 -> half = 39/min
#                    -> 1.54 s; 1.6 chosen.
#   candleSnapshot:  MEASURED ceiling at 5000 rows: 23 admitted then 429,
#                    23/min sustained clean -> half = 11.5/min -> 5.2 s; 5.3
#                    chosen for every candle request regardless of size.
#   fundingHistory:  no refusal at probe scale (45-burst, 500 rows); highest
#                    verified clean 89/min sustained -> half = 45/min -> 1.4 s.
#   l2Book:          no refusal; highest verified clean 240/min sustained ->
#                    half = 120/min -> 0.5 s.
OPERATING_PACING_S: Final[dict[str, float]] = {
    EP_META: 0.8,
    EP_META_AND_CTXS: 0.8,
    EP_PERP_DEXS: 1.6,
    EP_CANDLE_SNAPSHOT: 5.3,
    EP_FUNDING_HISTORY: 1.4,
    EP_L2_BOOK: 0.5,
}

REFUSAL_BODY_VERBATIM: Final = b"null"
