# Stage A.4 mutation evidence

Each mutation edits real source; the suite must go red; the source is
restored byte-for-byte; the suite must go green. Bytecode is purged
before every run.

Baseline: suite green before any mutation.

## M1: delete a blindness pin (the funding gate becomes unconditional)

- file: `src/npl/blindness.py`
- expected catch: tests/test_blindness.py (post-entry absence), tests/test_guards.py (gate in AST)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## M2: coerce an absence to zero

- file: `src/npl/absence.py`
- expected catch: tests/test_absence.py, tests/test_blindness.py (gated rate refuses a sum)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## M3: merge rate_limited into no_data

- file: `src/npl/venue.py`
- expected catch: tests/test_venue.py (429 is rate_limited), tests/test_census.py
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## M4: move a registered boundary (GO requires strictly above 0.80)

- file: `src/npl/section0.py`
- expected catch: tests/test_section0.py (the fixture sits exactly on 0.80)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## M5: read a post-entry funding row inside matching

- file: `src/npl/controls.py`
- expected catch: tests/test_a3_modules.py (PostEntryRead is produced, not asserted)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

