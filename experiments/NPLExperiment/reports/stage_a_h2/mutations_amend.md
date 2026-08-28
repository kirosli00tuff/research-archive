# Amendment H2-3 mutation evidence

Each mutation edits real source on the amendment surface; the suite must
go red; the source is restored byte-for-byte; the suite must go green.
Bytecode is purged before every run. **No H2 look has been read** — both
per-look latches are absent and the pair reader has only ever seen
synthetic fixtures — so no mutation could touch a live verdict.

**Result: 6 of 6 CAUGHT.**

Baseline: suite green before any mutation.

## MA1: spend look 2's alpha at look 1

- file: `src/npl/register/sequential.py`
- expected catch: tests/test_amend.py (the recorded boundary: k1 is 38 at alpha_1 alone and 37 at the whole budget — the interim would spend the entire 0.05)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MA2: admit a cross_dex pair into the same_dex stratum

- file: `src/npl/register/pairs.py`
- expected catch: tests/test_amend.py (the stratum is 20 same-dex pairs of 30; admitting the cross_dex 10 makes it 30)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MA3: read a post-entry funding row inside fallback assignment

- file: `src/npl/controls.py`
- expected catch: tests/test_amend.py (PostEntryRead is produced through the fallback path; the silent pre-filter swallows the refusal instead of raising it)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MA4: bypass a per-look latch

- file: `src/npl/register/latches.py`
- expected catch: tests/test_amend.py (a spent look must refuse a second read, loudly)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MA5: drop the pair-type tag from a fallback assignment

- file: `src/npl/controls.py`
- expected catch: tests/test_amend.py (the fallback pair is tagged cross_dex in the assignment and in the append-only ledger row)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MA6: let the look-2 read run without look 1's counts

- file: `src/npl/register/pairs.py`
- expected catch: tests/test_amend.py (a look-2 read with no look-1 record must refuse; the boundary it would compute has no k1 to condition on)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

