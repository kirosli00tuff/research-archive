# Register Stage A mutation evidence

Each mutation edits real source on the register surface; the suite
must go red; the source is restored byte-for-byte; the suite must go
green. Bytecode is purged before every run. No successor read exists,
so no mutation could touch a live verdict.

Baseline: suite green before any mutation.

## MR1: open reports/stage_b/read.json from an H2 module

- file: `src/npl/register/views.py`
- expected catch: tests/test_guards.py (the stage_b string quarantine pin: the reachable surface is exactly the two H1 modules)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MR2: admit a generating-sample event ID into an H2 eligibility view

- file: `src/npl/register/views.py`
- expected catch: tests/test_register.py (the refusal is produced through the real views)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MR3: read a post-entry funding row inside control assignment

- file: `src/npl/controls.py`
- expected catch: tests/test_a3_modules.py (PostEntryRead is produced, not asserted)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MR4: flip a pair-leg sign in the dark reader

- file: `src/npl/register/pairs.py`
- expected catch: tests/test_register_a3.py (the four-leg known-answer gate and the both-legs sign pin)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MR5: let the cull read an outcome field

- file: `src/npl/register/cull.py`
- expected catch: tests/test_guards.py (the repo-wide OHLCV pin: no module reads a priced candle field)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MR6: widen a reader allowlist

- file: `src/npl/stageb/__init__.py`
- expected catch: tests/test_guards.py (the equality pin holds the allowlist at length one)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

