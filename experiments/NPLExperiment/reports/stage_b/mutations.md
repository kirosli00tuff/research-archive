# Stage B mutation evidence

Each mutation edits real source on the new Stage B surface; the suite
must go red; the source is restored byte-for-byte; the suite must go
green. Bytecode is purged before every run. The read was already spent
when this ran (the latch exists), so no mutation touched a live verdict.

Baseline: suite green before any mutation.

## MB1: bypass the latch so a second read is allowed

- file: `src/npl/stageb/cli.py`
- expected catch: tests/test_stageb_reader.py (ReadAlreadySpent is produced, not asserted)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MB2: widen the blindness allowlist to two modules

- file: `src/npl/stageb/__init__.py`
- expected catch: tests/test_guards.py (the equality pin holds the allowlist at length one)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MB3: flip the funding sign convention inside the reader

- file: `src/npl/stageb/reader.py`
- expected catch: tests/test_stageb_reader.py (the known-answer gate, sign pin -0.0729)
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

