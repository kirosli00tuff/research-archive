"""Register entry H5: HIP-3 equity-style perpetual basis feasibility.

H5 is a **feasibility entry, not a trade hypothesis**. It authorizes no
capital, no Stage B read of a trading outcome, and no Stage C. Everything
under this package is descriptive: it measures which fields the venue serves
on HIP-3 equity-style instruments, and how far the venue's own mark sits
from the venue's own reference, in basis points, tagged by underlying-market
session.

Three standing rules bind every module here and are pinned by test:

1. **No outcome field, ever.** No H5 path parses a candle payload, and no H5
   path reads a funding rate value. Funding *service* is recorded as a state
   with row counts and timestamps, through the existing blindness reader at
   ``entry_ms=None`` (every rate comes back ``Absent(blindness_gated)``).
2. **No write outside ``data/h5/``.** Every H5 write goes through
   ``npl.h5.stores.h5_store``, which refuses any path outside the H5 root.
   H2's collectors, ledgers, latches, and stores are read-only to this entry
   — and the quarantine lists are read precisely so they can be honoured.
3. **Absence is never interpolated.** An unserved reference is
   ``reference_unserved`` and contributes to the coverage census only.
"""
