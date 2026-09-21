# Register entry H5 — mutation evidence

Each mutation edits real source on the H5 surface; the suite must go red;
the source is restored byte-for-byte; the suite must go green. Bytecode is
purged before every run. **No mutation could touch a live verdict**: H5 has
no Stage B, no latch and no capital, the map is fired only from H5's own
stores, and every H2 store is read-only to this entry by construction.

**Result: 7 of 7 CAUGHT.**

Baseline: suite green before any mutation.

## MH1: compute a basis from a field the venue did not serve in the same snapshot

- file: `src/npl/h5/basis.py`
- expected catch: tests/test_h5_registration.py (a mark from snap-1 against an oracle from snap-0 must raise CrossSnapshotBasis; Section 3 admits only same-snapshot fields)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MH2: let an H5 path write into an H2 store

- file: `src/npl/h5/stores.py`
- expected catch: tests/test_h5_registration.py (the refusal is produced on the real path data/controls/h2_pairs.jsonl, not asserted in a comment)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MH3: interpolate an absent reference

- file: `src/npl/h5/basis.py`
- expected catch: tests/test_h5_registration.py (a middle gap must stay Absent and the served n must drop from 3 to 2; the carry-forward makes it 3 again)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MH4: mis-tag a weekend snapshot as regular hours

- file: `src/npl/h5/calendar.py`
- expected catch: tests/test_h5_registration.py (Saturday 2026-08-29 at noon ET must tag weekend; the moved boundary tags it regular, and the fixture sits ON Saturday)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MH5: bypass the retrospective cohort gate

- file: `src/npl/h5/retro.py`
- expected catch: tests/test_h5_retro.py and tests/test_h5_guards.py (a generating-sample coin must reach nothing; the structural pin also requires the gate to be the first statement of fetch_series)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MH6: let the named secondary series fire VIABLE

- file: `src/npl/h5/outcome.py`
- expected catch: tests/test_h5_registration.py (a secondary at 300 bp must land INDETERMINATE, never VIABLE: a differently constructed number could be an artefact)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MH7: exclude a delisted instrument on the flag alone

- file: `src/npl/h5/listing.py`
- expected catch: tests/test_h5_listing.py (a flagged instrument with live open interest must read conflicting, not excluded; Amendment H5-2's rule is conjunctive)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

