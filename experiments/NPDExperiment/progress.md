# Progress

Append-only. Newest at top. Each stage states its ETA before it starts and its
actual after it finishes.

---

## Z.1. Closure. 2026-08-25

**Prompt logged before work began, as instructed.**

> NPDExperiment, Stage Z.1. Closure. This stage writes records. It computes no
> statistic, opens no sealed store, sends no API call, and changes no result.
> The B.2 verdict stands exactly as fired. Nothing below reinterprets it.
>
> Task 1, the terminal state recorded as post-read. Task 2, the closure note and
> its exact language. Task 3, the dormant observation. Task 4, what survives and
> what does not. Task 5, deactivate and delete nothing. Task 6, document and
> commit.

Work follows below.

### The closure language, as fixed

**The numeric-LLM question is unresolved at achievable power. Two serious
attempts have produced zero positives.**

The 2026-07-27 council measurement was a properly powered negative on direction:
274 scorable calls across 80 independent clusters, five axes, nothing
demonstrated on any.

The 2026-08-25 replication reformulated the task as cross-sectional ranking with
anonymized features, a frontier model chosen by knowledge cutoff, and a
three-baseline battery. It returned a model mean daily rank IC of plus 0.0061
with an interval spanning zero, below the best baseline `mom_12_1` at plus
0.0222, primary contrast minus 0.0161, permutation p 0.5174.

**The replication is an underpowered unresolved, not a tight null.** The realized
minimum detectable contrast was 0.0512, above the entire realistic effect band of
0.01 to 0.05, so the design could not have detected an effect anywhere in the
range the literature reports. The cause is recorded: realized daily contrast
standard deviation of 0.36339 against a registered assumption of at most 0.2626,
driven by a strong negative correlation between model and momentum daily ICs that
fell outside the range the registration contemplated. ADR-007 registered this
failure mode as a risk before collection. It was not discovered afterwards.

**The consequence.** The burden of proof now sits heavily on anyone claiming a
numeric-LLM effect exists. The question is closed by operator decision, not by
evidence.

**What a powered version would cost.** Sizing against the measured 0.36339
rather than the registered assumption requires roughly four times the evaluable
days, landing near 1,700 trading days of post-cutoff window. No model has one.
The window would have to accumulate from the calendar at about 21 trading days a
month.

### The terminal state

Amendment 6 is recorded **POST-READ**. It was drafted before the B.2 evaluation
ran and arrived after it, so it carries no pre-registration force and is
preserved as a record of intent. The row-three verdict authorizes nothing, so it
describes a destination never reached. Four gates sat between this experiment and
that engine, and **the first was never authorized**.

Amendment 7 is **void**. Scoring spent data against new horizons is a second look
however it is labelled.

### The dormant observation

The model daily rank IC and the momentum daily rank IC were strongly negatively
correlated. The model was not producing noise around momentum. It was leaning
systematically against it. **This is not a finding.** It may only be promoted by
a future test that names it in advance.

### Layer accounting

L1 RiskGate survived every audit and remains in service. L2 the council is what
this experiment addressed, twice, with no positive. L3 DNN advisory and L4 whale
tracking were each measured to nothing independently. **This closure ends the
last attempt to revive L2. It says nothing about L1.**

The running AiTrader news-drift experiment is untouched and unaffected. It tests
text, not numbers. **Its verdict remains due at 60 clusters.**

### Deactivation

This repository never installed a systemd unit, a timer, or a cron entry.
Verified at closure: no user or system units match, no timers, no crontab
entries, no unit files anywhere reference this repository, and no process is
running. Nothing needed disabling and nothing was deleted.

Every file, ledger, report, and stored ranking stays in place. The 415 stored
rankings, the evidence ledger, the spend ledger, and the frozen prompt digest
`7e6f3d6801506bd7...` are the artifacts that make the result auditable.

**Correction carried into the record.** The closing instruction named
`9a174e0155fadfbf...` as the frozen digest. That is the superseded
pre-Amendment-4 template, and it produced zero of the 415 stored rankings. The
digest in force is `7e6f3d6801506bd7...`.

### Outstanding operator actions, outside the repository

- Revoke or retain the OpenAI key at the operator discretion.
- Measured spend 6.9378 USD against the 10.00 USD cap, 3.0622 USD unspent.

---

## B.2. The one-shot evaluation. 2026-08-25

**ETA stated before start: 55 minutes. Actual: 41 minutes.**

**Prompt logged before work began, as instructed.**

> NPDExperiment, Stage B.2. The one-shot evaluation. Read the registration in
> full including Section 0 and all five amendments, progress.md, DECISIONS.md
> ADR-001 through ADR-009, CLAUDE.md, and the three stage reports.
>
> This is the one read. It happens once and cannot be repeated. The registration
> fixes a single evaluation of the sealed window. If a defect surfaces
> mid-evaluation, stop and report rather than fixing and re-running, because a
> second pass over the same outcomes is a second look however it is labelled.
> Do not modify the sealed store, the stored rankings, the frozen prompt digest,
> the baselines, or any registered parameter. Do not add a horizon, a baseline,
> a model, or a robustness variant that the registration does not already name.
>
> Task 1, Amendment 0 recorded before any outcome is read. Task 2, the pipeline
> validity audit, and it gates everything. Task 3, the primary contrast. Task 4,
> the permutation null. Task 5, secondaries and descriptives, clearly
> subordinate. Task 6, fire the verdict, once. Task 7, tests and two mutations.
> Task 8, document and commit.

Work follows below in the order the prompt fixes.

### Result

**Verdict row fired: does not beat coin.** The replication confirms the council
negative under frontier capability and sane formulation. Closed. **C.1 is not
authorized.**

| quantity | value |
|---|---|
| pipeline validity gate, shuffled mean | +0.0001, inside the 0.02 tolerance. PASS |
| model mean daily rank IC | +0.0061, interval -0.0276 to +0.0397 |
| best baseline, designated after the fact | `mom_12_1` at +0.0222 |
| primary contrast | -0.0161, interval -0.0673 to +0.0351 |
| permutation p, two-sided | 0.5174 |
| evaluable days | 404 of 415 stored |
| realized minimum detectable contrast | 0.0512 against a projection of 0.026 to 0.047 |

The model did not beat a coin and did not beat momentum. It scored below the
best baseline, though not significantly so.

### The honest qualifier

**This is an underpowered unresolved, not a tight null.** The realized detectable
contrast of 0.0512 sits above the entire realistic effect band of 0.01 to 0.05,
so the design could not have detected an effect anywhere in the band the
literature reports. The realized daily contrast standard deviation came in at
0.36339 against a registered assumption of at most 0.2626, because the model and
momentum daily ICs turned out to be strongly negatively correlated, far outside
the 0.0 to 0.7 range the registration contemplated. ADR-011 records this.

The failure mode ADR-007 registered as a risk in advance is the one that
materialized. It was registered as a risk, not discovered afterwards.

### Discipline

The sealed store was read one time by one module. Its hash and mtime are
unchanged from the B.0 build, because it was opened read-only. Amendment 0 was
recorded before any module touched it, and the operator prior is logged as
**adopted from the assistant, not independent**, so the calibration record is not
corrupted by a prior that carries none of the operator own judgment. No horizon,
baseline, model, or robustness variant was added beyond what the registration
already named. Nothing was recomputed after being seen.

Six mutations run, all caught and restored, including the two this stage
required: bypassing the Amendment 0 refusal, and letting a non-evaluator module
read the sealed store.

Full evaluation in `reports/stage_b2/evaluation.md`.

---

## B.1. The live gate collection. 2026-08-25

**ETA stated before start: 60 minutes. Actual: 194 minutes across three
launches.** Two launches were stopped deliberately, each to record an amendment
before collecting further. The overrun is entirely those two stops.

**Section 0 verdict: GO.** 415 of 432 eligible days carry a stored, parseable
ranking. Coverage 96.1 percent against a 90 percent bar.

| state | days |
|---|---|
| `stored` | 415 |
| `model_failed` | 17 |
| `no_data` | 0 |
| `excluded_pre_cutoff` | 0 |
| `source_failed` | 0 |

Spend 6.9378 USD of a 10.00 USD cap across 920 billed gate calls at a measured
0.007508 USD each, plus 2 calibration calls excluded from the sample. The batch
refusal never fired and no quota error was seen.

All 415 stored rankings are structurally sound. Ranks are exactly 1 to 30,
labels match that day mapping, symbols match that day panel, and the label to
symbol relation is consistent on every day.

Contact with the real model forced five amendments in one evening. The
registration carries each with its evidence, including Amendment 3, which was a
wrong diagnosis that was acted on and is kept rather than removed. The most
consequential was Amendment 4: `low` reasoning failed to produce a valid
permutation 47 percent of the time against `minimal` at 41 percent, which showed
the output format was the problem rather than the reasoning budget. A strict
JSON schema pinning 30 enum-constrained slots cut the projected total from 9.12
USD to a measured 6.94 USD and turned a path heading for BLOCKED into one that
fired GO.

Amendment 5 mattered more than its size. The spend ledger recorded nothing for
attempts whose answer failed to parse, though those calls were billed. It was
reading 46 percent under actual, so the ledger-enforced cap was being enforced
against the wrong number.

Nothing was evaluated. No rank IC was computed, no output was joined to any
outcome, and no hypothesis verdict was fired. Amendment 0 remains empty and
B.2 remains blocked.

Details in `reports/stage_b1/collection.md` and `reports/session_a1_b1.md`.

---

## B.0b. The collector, built and mock-verified. 2026-08-25

**ETA stated before start: 60 minutes. Actual: 52 minutes.**

The collector runs in one command, resumes on date, retries by taxonomy, backs
off, refuses before it spends, and writes an evidence row per call with the raw
response kept verbatim.

Building the kill scenario exposed a real gap. A process killed between the
ledger append and the store commit leaves a call that was paid for and a ranking
that never landed. Resume would have skipped that date and lost the answer. The
fix is reconciliation: the collector rebuilds the ranking from the raw response
the ledger kept, and calls nothing. That is the reason the raw response is kept
at all.

All five scenarios pass.

| scenario | evidence |
|---|---|
| clean | 432 of 432 stored, 432 calls, 5.8320 USD at registered token estimates |
| kill_resume | killed after 137 answered, 0 double-called dates, 3 lost commits rebuilt from the ledger, 0 extra spend |
| model_failed | 4 dates, 5 attempts each, terminal `model_failed`, zero leakage into `no_data` or `source_failed` |
| source_failed | 3 dates, 0 calls sent for them, state stays distinct |
| spend_refused | cap lowered to 0.20 USD, batch refused before sending, 0 calls, 0.0000 USD spent |

Prompt template frozen. Digest
`9a174e0155fadfbf12906773ff26e3c13fb01d30c2a9207831520b02df54bbae`.
Every B.3 replay uses these bytes.

Evidence in `reports/stage_b0b/mock_run.md`.

---

## B.0. Data, features, baselines, sealed. 2026-08-25

**ETA stated before start: 75 minutes. Actual: 68 minutes.**

Two read-only source paths opened and no others. `news_experiment.db` never
opened. The ported universe file hashed identically before and after.

The port is verified rather than asserted. The ported machinery rebuilt all 55
formations from bars, and every one matched the source own stored membership on
both the symbol set and the rank sequence. 500 members each, zero failures.

- 15,474,106 daily bars extracted across 18,474 symbols
- 432 window days, 432 panels drawn, zero days lost
- all three baselines complete on all 432 days
- logistic fitted once on 21,322 rows across 711 days, 2022-01-03 through
  2024-10-30, then frozen at digest `fe6f6006...`

Forward returns split by date, and the split is the seal. The fit store holds
only pre-window dates. The sealed store holds the window and has one permitted
reader. The writer has no reader at all.

The full verdict pipeline runs end to end on synthetic data with fake returns,
which proved B.2 works without touching one real outcome. It also caught a real
defect: `daily_ic` carried an inverted sign, so a perfect ranking would have
scored minus one. Fixed and pinned by a test.

Details in `reports/stage_b0/build.md`. Two decisions recorded, ADR-008 and
ADR-009.

---

## A.2. Binding registration. 2026-08-25

**ETA stated before start: 40 minutes. Actual: 34 minutes.**

A.2.0 ran first and gated everything downstream.

**Verified.** `gpt-5-2025-08-07` carries a knowledge cutoff of **2024-09-30**.
The served page reads `Sep 30, 2024 knowledge cutoff` verbatim. Source
https://developers.openai.com/api/docs/models/gpt-5, reached by 301 redirect
from platform.openai.com/docs/models/gpt-5, retrieved 2026-08-25. The same page
lists the snapshot `gpt-5-2025-08-07`, a 400,000 token context window, 128,000
max output tokens, and list prices of 1.25, 0.125, and 10.00 USD per million
for input, cached input, and output.

**The carried estimate was wrong.** Prior chat estimated 2024-05-31 and 515
days. The verified cutoff is four months later. The estimate is discarded.

**Derived.** Guard band of one calendar month ends 2024-10-30. Window runs
2024-10-31 through 2026-07-24. **432 trading days** from the source store's
own exchange calendar. The registered minimum is 200. The window clears it.

**Power.** Registered floor MDE 0.01787 against a floor of 0.025, so the window
is authorized. The primary contrast is weaker than the floor suggests: the
five-session horizon inflates variance by 3.4, cutting 427 evaluable days to
125.6 effective, and the minimum detectable contrast lands between 0.026 and
0.047. Registered as a limitation rather than repaired by swapping the primary.
ADR-007.

REGISTRATION.md written in full, 17 sections. Amendment 0 reserved and empty.
Assistant prior 0.05 recorded beside it.

---

## A.1. Scaffold. 2026-08-25

**ETA stated before start: 25 minutes. Actual: 22 minutes.**

Repository created at `~/Documents/GitHub/NPDExperiment`. `.env` was already
present at mode 600 and was never read, printed, or logged. `.gitignore`
covers it and `git check-ignore` confirms the match before the first commit.

Tooling: uv, ruff, mypy strict, pytest, pre-commit, Makefile.

Written: CLAUDE.md, DECISIONS.md with ADR-001 through ADR-007, progress.md,
REGISTRATION.md, `.env.example` carrying `OPENAI_API_KEY` commented and
valueless.

The two standing rules landed as code rather than prose. `npd.absence` makes
absence a type that refuses coercion to a number. `npd.callstate` holds the
five states and the classification that keeps them apart. `npd.config` holds
the frozen registered parameters, and every field in it needs an enforcement
site elsewhere or the structural guard fails.

Section 0's outcome map is committed in `npd.section0` and in REGISTRATION.md
Section 0. Both append-only ledgers exist, JSON lines, fsynced per row, and
they survive restart.
