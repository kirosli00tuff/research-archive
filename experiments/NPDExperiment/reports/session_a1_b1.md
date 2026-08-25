# Session record, stages A.1 through B.1

Written 2026-08-25. One session. Scaffold, binding registration, data layer,
mock-verified collector, and the live gate collection.

**Nothing was evaluated.** No rank IC was computed, no output was joined to any
outcome, and no hypothesis verdict was fired. B.2 runs once, later, after the
operator writes his registered prior into REGISTRATION.md Section 13.

---

## Stage A. Registration

ETA 25 plus 40 minutes. Actual 22 plus 34 minutes.

### A.2.0 gated everything, and it corrected the premise

The verified knowledge cutoff for `gpt-5-2025-08-07` is **2024-09-30**. OpenAI
own model page for `gpt-5`, which lists that snapshot, reads
`Sep 30, 2024 knowledge cutoff` verbatim. Retrieved 2026-08-25 from
https://developers.openai.com/api/docs/models/gpt-5, reached by a 301 redirect
from the older platform.openai.com path. The same page gives a 400,000 token
context window, 128,000 max output tokens, and list prices of 1.25, 0.125, and
10.00 USD per million for input, cached input, and output.

Prior chat carried an estimate of 2024-05-31 and 515 trading days. **Both were
wrong.** The verified cutoff sits four months later and the derived window holds
432 days, not 515. Carrying the estimate would have overstated the power
arithmetic by 19 percent and started the guard band inside territory the model
had already read.

### The derived window

| step | value |
|---|---|
| verified cutoff | 2024-09-30 |
| guard band, one calendar month | ends 2024-10-30 |
| first session strictly after the band | 2024-10-31 |
| last complete session in the bar store | 2026-07-24 |
| **trading days** | **432** |
| registered minimum | 200, cleared |

The calendar came from the source store own `trading_calendar`, not from any one
symbol bars.

### Power, and the limitation registered beside it

The registered floor is a detectable rank IC of 0.025 at 30 names. The derived
window gives **0.01787**, so collection was authorized.

The floor is not the number that governs interpretation. The primary contrast is
a difference of two daily IC series over a five-session horizon, so consecutive
start dates share four fifths of their forward window. Variance of the mean
inflates by 3.4 and 427 evaluable days fall to 125.6 effective.

| corr(model, best baseline) | detectable at t 2.0 | 80 percent powered |
|---|---|---|
| 0.00 | 0.0469 | 0.0666 |
| 0.30 | 0.0392 | 0.0557 |
| 0.50 | 0.0331 | 0.0471 |
| 0.70 | 0.0257 | 0.0365 |

Against a realistic band of 0.01 to 0.05, the primary detects the upper half and
is underpowered for the lower half. A null on the primary does not distinguish
no effect from an effect below 0.033.

The one-session secondary carries no overlap penalty and detects 0.014 to 0.025.
**It stays secondary.** Promoting the better powered horizon after seeing a
result is the move this repository exists to prevent. Recorded as ADR-007.

### What else A.2 fixed in advance

Section 0 outcome map, the verdict table, the epistemic boundary verbatim, the
spend cap arithmetic, the five call states, the four council clauses each with
its evidence, the B.3 replay schedule with Qwen 3.8 Max flagged as
cutoff-unverified, and Amendment 0 reserved and empty with the assistant prior
of 0.05 recorded beside it.

---

## Stage B.0 and B.0b. Data, baselines, collector

ETA 75 plus 60 minutes. Actual 68 plus 52 minutes.

### Source integrity

Two read-only paths opened and no others. `news_experiment.db` never opened, and
it appears nowhere in the source except inside the guard that forbids opening
it. The bar store opened through a SQLite immutable read-only URI, so a write is
impossible at the driver level rather than by convention. `backtest/universe.py`
hashed identically before and after at
`8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529`.

### The port is verified, not asserted

The universe machinery was copied in, never imported across repositories. It
rebuilt every formation the pipeline needs from bars, and each was compared
against the source own stored membership.

- 55 formations rebuilt
- **55 verified exact**, on both the symbol set and the rank order
- 0 failures
- 500 members each

### Coverage

| layer | result |
|---|---|
| daily bars extracted | 15,474,106 across 18,474 symbols |
| window days with a full 30-name panel | **432 of 432** |
| `sign_last` days ranked | 432 |
| `mom_12_1` days ranked | 432 |
| `logistic` days ranked | 432 |

The logistic baseline was fitted once on 21,322 rows across 711 days,
2022-01-03 through 2024-10-30, strictly before the window start, then frozen.

### The seal

Forward returns split by date, and the split is the seal. `var/npd_fit.db` holds
only pre-window dates and the logistic baseline reads it. `var/npd_sealed.db`
holds the window and `npd.eval.evaluator` reads it and nothing else does. The
writer has no reader at all. A guard test walks every source file and fails when
another module names the sealed store, calls the sealed reader, or adds a read
to the writer. Recorded as ADR-008.

### Two defects the design caught before any spend

**The verdict pipeline carried an inverted sign.** Running B.2 end to end on
synthetic data with fake returns showed `daily_ic` returning minus one for a
perfect ranking. The experiment would have reported the exact opposite of what
it measured. Fixed, and pinned by a test that asserts the convention.

**Anonymization labels collided with real tickers.** Two-letter row labels are
also real symbols. KO is Coca-Cola, MA is Mastercard, MU is Micron. On **52 of
the 432 window days** a drawn label equalled a ticker standing in the same
panel. Panel symbols are now struck from the label pool before any label is
drawn, all 432 mappings were rebuilt, and the collision count is zero.

### Five scripted faults, all passed

| scenario | evidence |
|---|---|
| clean | 432 of 432 stored, 432 calls |
| kill_resume | killed after 137 answered, 0 double-called dates, 3 lost commits rebuilt from the ledger, 0 extra spend |
| model_failed | 4 dates, 5 attempts each, terminal state correct, zero leakage into other states |
| source_failed | 3 dates, 0 calls sent, state stays distinct |
| spend_refused | cap lowered to 0.20 USD, batch refused before sending, 0 calls, 0.0000 USD spent |

Building the kill scenario exposed a real gap. A process killed between the
ledger append and the store commit leaves a call that was paid for and a ranking
that never landed. The collector now rebuilds it from the raw response the
ledger kept and calls nothing.

### Five mutations, all caught

Each applied to real source, not a copy. The harness restores the original bytes
and reruns the full suite to prove the restore worked.

| mutation | guard that failed | caught |
|---|---|---|
| carry a value forward across a missing bar | `test_absence.py` | yes |
| merge `model_failed` into `source_failed` | `test_guards.py` | yes |
| let a non-evaluator module read the sealed returns | `test_guards.py` | yes |
| add a config field with no enforcement site | `test_guards.py` | yes |
| let a real ticker reach a prompt | `test_anonymization.py` | yes |

The config guard was not decorative. On first run it found four fields enforced
nowhere in the real config. Each was given a genuine enforcement site rather
than removed from the guard.

---

## Stage B.1. The live gate collection

ETA 60 minutes. Actual 194 minutes across three launches, two of which were
stopped deliberately to record an amendment before collecting further.

### Preconditions, all met before the first call

A.2.0 verified the cutoff and the derived window cleared 200 trading days at
432. The full suite was green. All five B.0b mock scenarios passed.

### The result

| state | days | class |
|---|---|---|
| `stored` | **415** | sample |
| `no_data` | 0 | sample composition |
| `model_failed` | 17 | operational health |
| `excluded_pre_cutoff` | 0 | sample composition |
| `source_failed` | 0 | operational health |
| **total** | **432** | |

- eligible days, `excluded_pre_cutoff` removed from the denominator: **432**
- days carrying a stored, parseable ranking: **415**
- coverage: **96.1 percent**

### Section 0 verdict: GO

96.1 percent of eligible days carry a stored, parseable ranking, at or above the
90 percent bar. Fired on coverage alone. No statistic relating an output to an
outcome was computed.

### Spend

| item | value |
|---|---|
| gate calls billed | 920 |
| calibration calls, excluded from the sample | 2 |
| measured cost per gate call | 0.007508 USD |
| **total spent** | **6.9378 USD of a 10.00 USD cap** |
| remaining | 3.0622 USD |
| input tokens | 3,514,278 |
| output tokens | 361,641, of which reasoning 217,728 |

The batch refusal never fired. No `insufficient_quota` error was seen.

### Stored ranking integrity

Structural only. No forward return was read and no output was joined to any
outcome.

| check | days |
|---|---|
| days with a ranking in the store | 415 |
| ranks are exactly 1 to 30 | 415 |
| labels match that day mapping | 415 |
| symbols match that day panel | 415 |
| label to symbol is consistent | 415 |

### Operational health

- attempts under the current procedure: 883 across 432 days, 2.04 per day
- days needing more than one attempt: 175
- attempts by reasoning effort: 813 `minimal`, 70 `low`
- days whose stored answer came from `low` after an escalation: 53

### Five amendments, each recorded before collecting resumed

| n | raised by | what changed |
|---|---|---|
| 1 | the calibration call | `temperature` is not sent. The endpoint rejects any non-default value for this model. The registration no longer claims the output is deterministic. |
| 2 | the calibration call | `reasoning_effort` set to `minimal` by the registered spend rule. Measured `low` at 2,432 reasoning tokens per call, projecting 11.78 USD over a 10 USD cap. |
| 3 | 14 live calls | An escalation ladder after 9 of 14 attempts returned a malformed permutation. **This diagnosis was wrong.** |
| 4 | 29 live days | `low` failed at 47 percent against `minimal` at 41 percent, so the format was the problem, not the reasoning budget. A strict JSON schema pins 30 enum-constrained slots. Prompt freeze re-established. Supersession now keys on the prompt digest. |
| 5 | the same stop | Rejected answers are billed, so the ledger records them. It had been reading 46 percent under actual. |

Amendment 3 is superseded by Amendment 4 and is kept in the registration rather
than removed, because a wrong diagnosis that was acted on is part of the record.

### What the amendments cost, and what they bought

The 26 superseded attempts stay in the ledger and their 0.0286 USD still counts
against the cap. Amendment 4 cut the projected total from 9.12 USD to a measured
6.94 USD, cut mean latency from 16.3 to about 3 seconds per attempt, and lifted
coverage from a path that would have fired BLOCKED to one that fired GO.

### The limitation that survives into B.2

The gate ran at `minimal` reasoning on 813 of 883 attempts. **A null result is a
null for gpt-5-2025-08-07 at minimal reasoning effort, not for the model at its
best.** Every sentence written about the outcome carries that qualifier.

53 days carry an answer produced at `low` after an escalation. Days that needed
escalation are days where `minimal` could not hold the format, and if that
difficulty correlates with anything about the panel, the sample mixes two
configurations non-randomly. The realized effort is stored per day for exactly
this reason. B.2 reports the outcome split by realized effort beside the primary
contrast, as a descriptive split that never becomes a verdict, under Clause 1.

---

## One operator action outstanding

REGISTRATION.md Section 13 holds an empty slot for the operator registered
prior, the probability that a rigorous version of this experiment beats the best
baseline on the primary contrast.

**B.2 refuses to run while that slot is empty.** The refusal is a mechanism, not
a reminder. `require_amendment_zero()` raises, and a guard test asserts the slot
currently reads empty.

The assistant prior of 0.05 is recorded beside it, written before any output
existed so it cannot be adjusted after the operator writes his.

---

## What this session did not do

It computed no rank IC, read no outcome against any output, fired no hypothesis
verdict, called no frontier model, traded nothing, and touched no running
system. The nightly news-drift collection at 22:30 UTC was not disturbed. No git
remote exists, so nothing could be pushed. The API key was never printed,
logged, or committed, and `.gitignore` covered `.env` before the first commit.
