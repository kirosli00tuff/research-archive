# progress

Append-only. Newest at top.

---

## 2026-08-25, Stage A.1. Scaffold, registration, corpus, and the power gate

**Outcome. CORPUS-GO, then BLOCKED.** The corpus cleared its floor by a factor
of four and a half. The design then failed its own power bar. The minimum
detectable effect for the registered primary portfolio is **49.35 bp per month**
against a BLOCKED floor of 40. Stage B is never written. The repo closes on the
finding.

### ETA against actual

Timings are wall clock, session start 18:20 UTC, boundaries taken from commit
timestamps where one exists.

| Task | ETA stated before starting | Actual |
|---|---|---|
| 0. Orientation, source hash, feasibility probes | 11 min | 5 min |
| 1. Scaffold and standing guards | 20 min | 10 min |
| 2. REGISTRATION Section 0, the power gate | 25 min (stated jointly with the Task 1 close-out) | 4 min |
| 3. REGISTRATION Sections 1 to 16 | 30 min | 4 min |
| 4. The corpus, built free | **not stated** | 14 min |
| 5. The power gate, computed | 35 min | 20 min |
| 6. Tests and mutations | 30 min | 32 min |
| 7. Document and commit | 25 min | 22 min |

**Task 4's ETA was not stated before starting it.** The stage brief required one
per task and this one was skipped. Recorded rather than smoothed over.

Task 6 was the only task to run over, and it ran over for the right reason: two
of the five mutations were not caught on the first attempt and both exposed real
defects. See below.

### What was built

- **Scaffold.** uv, ruff, mypy strict, pytest, pre-commit, Makefile. 56 source
  files. `make all` runs clean: ruff, ruff format, mypy strict on 56 files, 106
  tests.
- **The four standing guards, ported by copying.** Recorded absence that refuses
  coercion to a number. The structural config-enforcement guard. Append-only
  fsynced ledgers that report a truncated line rather than repairing it. Eight
  call states that never merge operational health with sample composition.
- **REGISTRATION.md.** Section 0 committed at 18:34, before Task 4 computed
  anything. Sections 1 to 16 committed at 18:38. Every parameter frozen first.
- **The corpus.** 53 quarterly SEC structured Form 345 data sets, 2013q1 to
  2026q1, 214 wire requests, 2.78 GB, zero non-200 responses. The 8 per second
  throttle held against the SEC's stated 10 per second ceiling.
- **The power module.** Structurally incapable of emitting a mean, enforced by
  four guards and exercised by two of the five mutations.

### The numbers

| Quantity | Value |
|---|---|
| Qualifying events | 4,585 against a registered floor of 1,000 |
| Session coverage | 99.5 percent against a floor of 80 |
| Mean book width, 6-month hold | 71.9 names |
| **Effective book width, value-weighted** | **29.7 names** |
| Annualized tracking error, primary | 9.993 percent |
| Effective independent periods | 2,869.9 from 2,581 sessions |
| **MDE, primary** | **49.35 bp per month** |
| MDE, equal-weighted secondary | 34.29 bp per month |

### Why BLOCKED fired

Not the corpus. The corpus is four and a half times its floor and the book is
covered on 99.5 percent of sessions.

**Weight concentration.** The value-weighted book holds 71.9 names and behaves
like 29.7. The heaviest name carries 14.9 percent of the book and the heaviest
five carry 33.8. Median dollar volume is heavily skewed, so weighting by it
collapses a wide book into a narrow one. The equal-weighted book holds the same
71.9 names and behaves like 66.9, and its tracking error is 6.86 percent against
the value-weighted 9.99.

This is the failure Section 7 registered against in advance: wide book, not
concentrated, because concentrated books are what killed H-F at 42 to 66 percent
tracking error. The value-weighted book is concentrated by construction and the
registration named value-weighted as primary before any number was visible.

**The verdict stands on the registered primary.** The equal-weighted 34.29 bp
would have fired DEGRADED. It is a labelled non-verdict-bearing secondary,
registered as such before measurement, and it is not promoted.

### Two guards that did not fire, and what they exposed

Both were found by the mutation exercise and both were real defects.

1. **The config-enforcement guard scanned raw text.** The mutation replaced
   `rate = cfg.sec_requests_per_second` with a literal, leaving the key in a
   trailing comment. The text search matched the comment and called it
   enforcement. That is precisely the decoration the guard exists to catch. The
   guard now walks the parse tree and counts only identifiers the module reads.

2. **The routine-rule guard had a slack fixture.** Its insider carried four
   years of history, so raising the requirement from three to four did not flip
   her label. Tightening the fixture to the registered boundary then exposed a
   defect in the source: `classify` tested the history gate before the routine
   pattern, so an insider who traded the candidate month in three consecutive
   prior years, but whose earliest trade fell eight days short of three calendar
   years, was filed `insufficient_history` when she is definitionally routine.
   ADR-008 records the correction. One transaction moved label. The qualifying
   set and the MDE did not move.

A third defect surfaced in the mutation harness itself. `routine_consecutive_years=3,`
and `=4,` are the same byte length, so restoring inside the same second left the
mutated bytecode valid under CPython's mtime-and-size cache check and the harness
reported a restore as still red. The harness now purges bytecode before every
run. A mutation harness that reports results from source no longer on disk is
worse than no harness.

### One more count that did not agree with its own store

`write_events` first used a composite natural key. Two identical purchase lines
on one filing are two reported transactions, and the key silently merged 43 of
them, so the build reported 4,585 while the table held 4,542. The store now uses
a surrogate key and the build raises if the offered count and the stored count
diverge.

### Outstanding

**One operator action.** REGISTRATION.md Section 12 reserves the operator prior
and it is empty. It blocks Stage B structurally, and Stage B is already blocked
by the power gate, so nothing waits on it operationally. It is still outstanding
because the calibration ledger needs an independently formed number, and the
assistant's 0.12 sitting beside it is not that number.

### Boundaries held

`analysis_bars.db` hashed before and after at
`d599ccf0b8d70a5b2b8c7fca2461f0d6e0e09f0e8c990405f7c25e3fa767e924`, unchanged.
`backtest/universe.py` at
`8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529`, unchanged.
Nothing else under AiTrader was read. `news_experiment.db` was never opened.
Nothing was pushed to any remote. No money was spent.
