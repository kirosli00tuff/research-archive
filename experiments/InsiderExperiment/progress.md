# progress

Append-only. Newest at top.

---

## 2026-08-25, Stage Z.1. Closure

Records only. No statistic computed, no alpha read, no sealed store opened, no
request sent, no result changed. The A.1 power verdict stands exactly as fired.

### The closure language

**The registered primary design cannot resolve the effect at achievable power.
The minimum detectable effect is 49.35 bp per month against a registered BLOCKED
floor of 40 and against a decayed literature band of 30 to 40 bp per month gross
and 13 to 35 bp per month net at the six-month hold. Stage B is never written.
The repo closes on the finding.**

### The corpus did not fail

4,585 qualifying events against a registered floor of 1,000. 99.5 percent session
coverage against a floor of 80. 53 quarterly SEC structured Form 345 data sets
covering 2013q1 to 2026q1, retrieved in 214 wire requests totalling 2.78 GB with
zero non-200 responses under an 8 per second throttle against the SEC's stated 10
per second ceiling. Zero dollars spent. No paid API used. The cache on disk
equals the wire total byte for byte, so nothing was fetched twice.

### What did fail

Weight concentration in the registered primary. The value-weighted book holds a
mean 71.9 names and behaves like 29.7 effective names, because the heaviest name
carries 14.9 percent and the heaviest five carry 33.8 percent. Median dollar
volume is heavily skewed, so weighting by it collapses a wide book into a narrow
one. Annualized tracking error came in at 9.993 percent across 2,869.9 effective
independent periods from 2,581 sessions, and that tracking error is the whole of
the 49.35. The variance inflation of 0.899 is below one, so the period count
worked in the design's favour. Sample size did not cause this verdict.

### The secondary, and the temptation

The equal-weighted book holds the identical 71.9 names, behaves like 66.9, has
6.86 percent tracking error, and lands at 34.29 bp per month, which would have
fired DEGRADED. Registered as secondary in Section 7 and non-verdict-bearing in
Section 10, both before any number was visible. Not promoted.

Section 7 chose value-weighted to get a wide book rather than a concentrated one,
citing H-F at 42 to 66 percent tracking error. The primary chosen to avoid
concentration was concentrated by its weighting rather than by its name count.

The reopening boundary is recorded in Section 17.4 and ADR-011. A fresh
registration naming equal-weight as primary is not a clean experiment, must
disclose in its own Section 0 that the choice followed a seen A.1 secondary, and
must carry a higher bar. Assessed borderline at best. The honest alternative is a
different universe or a different disclosure regime.

### The three defects, the most reusable finding

All three surfaced in the mutation exercise, the only task that ran over its ETA,
and it ran over for the right reason. Two were guards passing vacuously.

1. The config-enforcement guard scanned raw text and matched a config key left in
   a trailing comment after its enforcement site became a literal. It now walks
   the parse tree. ADR-012 records a correction to the brief's framing: the
   parse-tree version still cannot tell an identifier read to enforce from one
   read to display, so it catches decoration and not misuse. That residual is
   unsolved here and belongs in the next scaffold.
2. The routine-rule guard had a fixture carrying four years of history, so
   raising the requirement to four did not flip the label. Tightening it to the
   registered boundary exposed ADR-008: `classify` tested the history gate before
   the routine pattern, filing a definitionally routine insider under
   `insufficient_history`. One transaction moved label. The qualifying set and
   the MDE did not move.
3. The mutation harness reported results from source no longer on disk. A
   one-digit edit leaves file size and mtime-in-seconds unchanged, so CPython
   reused mutated bytecode after a restore. The harness now purges bytecode
   before every run.

A guard that has never been shown to fail is not a guard. A harness that can
report on absent source is worse than no harness. Both belong in any scaffold
ported from this one, and so does putting every fixture on the registered
boundary rather than comfortably inside it.

### The count that did not agree with its store

`write_events` first used a composite natural key. Two identical purchase lines on
one filing are two reported transactions, and the key silently merged 43 of them,
so the build reported 4,585 while the table held 4,542. The store now uses a
surrogate key and the build raises when the offered and stored counts diverge.
Recorded under its standing rule in ADR-013: absence is a recorded state, never a
synthesized value, and a silent merge is a synthesized agreement.

### The operator prior

Section 12 closes unfilled. Reserved, blocks Stage B structurally, and Stage B is
blocked independently by the power gate, so nothing waited on it operationally.
It stays outstanding for the calibration ledger. The assistant's 0.12 beside it is
not the operator's number, and NPDExperiment's prior was adopted rather than
formed, so the calibration ledger still holds zero independently formed entries.

### The family record

Eight price-based and signal-based hypothesis families have now been tested
across AiTrader, HFExperiment, NPDExperiment and InsiderExperiment. **Zero have
produced a positive result that survived its own registered bar.**

Two closed on power rather than on absent signal: H-F at z 1.668 against a 2.50
bar, and NPD at unresolved-at-achievable-power. This one closed on power alone
and closed before measurement.

Closing before measurement is cheaper than closing after it. NPD reached its
power finding after 415 days of collection and 6.9378 USD. This one reached the
equivalent finding before any alpha existed.

**Cost, measured rather than asserted.** The commit record puts Stage A.1 at
about 51 minutes of session wall clock, 18:20 to 19:11, and Stage Z.1 at about
20 minutes. The Z.1 brief records five hours. The commit record cannot confirm
that figure, which presumably counts operator time between stages that this
repository does not observe. Both are recorded rather than one being picked.
Zero dollars. No capital.

The running AiTrader news-drift experiment is untouched and unaffected. Its
verdict remains due at 60 clusters.

### Deactivation, and nothing deleted

**No systemd unit was ever installed by this repository.** Stage A.1 was a
one-shot batch, not a scheduled collector, so there was nothing to disable or
stop. Verified against `~/.config/systemd/user`, `/etc/systemd/system`,
`systemctl --user list-units --all`, `systemctl --user list-timers --all`, and
`crontab -l`. None matched. Nothing remains scheduled.

Every file, ledger, report and the 2.78 GB corpus cache stays in place.

Both AiTrader hashes re-verified unchanged at closure:

- `analysis_bars.db` `d599ccf0b8d70a5b2b8c7fca2461f0d6e0e09f0e8c990405f7c25e3fa767e924`
- `backtest/universe.py` `8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529`

### Outstanding operator actions

1. **The registered prior.** Section 12, empty. Nothing waits on it
   operationally. It is outstanding for the calibration ledger.
2. **Corpus pruning, discretionary.** The cache occupies 2,783,280,665 bytes,
   2.78 GB. Pruning it makes any future replication start from a fresh SEC pull
   of all 53 quarters. **A correction to the brief:** it describes this as 2.78
   GB on a 14 GB machine. The 2.78 GB is right. The host is not: `/home` sits on
   a 466 GB filesystem with 328 GB available, 26 percent used. There is no disk
   pressure here, so pruning is a preference and not a need.

---

## 2026-08-25, Stage Z.1 prompt logged before work began

Logged verbatim on receipt, before any file was touched, as the stage required.

**Stage Z.1: Closure. Model: Sonnet. Effort: medium.**

Read REGISTRATION.md in full including Section 0 and Sections 1 to 16,
progress.md, DECISIONS.md including ADR-008, and the Stage A.1 reports. Log this
prompt to progress.md before work begins.

This stage writes records. It computes no statistic, reads no alpha, opens no
sealed store, sends no request, and changes no result. The A.1 power verdict
stands exactly as fired. Nothing below reinterprets it.

Run autonomously. Commit before ending. Push nothing.

Eight tasks: the closure note and its exact language; the secondary and the
temptation it creates; the three defects recorded as the most reusable finding;
the count that did not agree with its store; the operator prior; the family
record; deactivate and delete nothing; document and commit.

The fixed verdict language, not to be softened or strengthened: the registered
primary design cannot resolve the effect at achievable power. The minimum
detectable effect is 49.35 bp per month against a registered BLOCKED floor of 40
and against a decayed literature band of 30 to 40 bp per month gross and 13 to 35
bp per month net at the six-month hold. Stage B is never written. The repo closes
on the finding.

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
