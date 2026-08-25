# Binding registration

Written 2026-08-25, before the first call. Every number below is derived, not
assumed. Changing any registered value after B.1 starts requires a numbered
amendment appended to Section 17.

---

## Section 0. Outcome map

Committed before any call goes out. Coverage decides this verdict and nothing
else does. No statistic relating a stored ranking to any outcome enters here.

| verdict | condition | consequence |
|---|---|---|
| GO | at least 90 percent of eligible days carry a stored, parseable ranking | B.2 proceeds against the registered target |
| DEGRADED | between 70 and 90 percent | recorded. B.2 proceeds with the achieved sample and states its recomputed power beside the registered target |
| BLOCKED | under 70 percent, or the derived window falls under the power floor | no verdict claimed |

`excluded_pre_cutoff` never enters the denominator. It is sample composition,
not a failure to collect. Every other state does enter, including
`model_failed`, because a day the model could not answer is a day the sample
does not have.

Enforced by `npd.section0.fire`.

---

## Section 1. Hypothesis

**Given anonymized per-name numeric feature blocks, a frontier LLM ranks
next-window cross-sectional returns better than cheap mechanical baselines.**

This is a replication. The original AiTrader LLM council was fed price-derived
numbers and measured to a properly powered negative on 2026-07-27:

- 274 scorable directional calls across 80 independent symbol clusters
- pooled excess minus 0.5 bp per call at z minus 0.046
- interval minus 22.5 to plus 21.4
- hit rate 50.0 percent
- the interval excluding the 50 bp effect the design was powered for

Across three sessions the council was measured on five axes, direction,
calibration, abstention, rejection, and asset class, with nothing demonstrated
on any. Zero trades in system history carried a council decision id.

This experiment reruns the numeric question under two changed conditions,
frontier capability and sane formulation: cross-sectional ranking instead of
per-symbol direction, anonymized features, real baselines, and powered
post-cutoff windows.

---

## Section 2. Gate model and derived window

| field | value | provenance |
|---|---|---|
| model | `gpt-5-2025-08-07` | the dated snapshot, never the bare `gpt-5` alias |
| knowledge cutoff | **2024-09-30** | verified at A.2.0 |
| cutoff source | https://developers.openai.com/api/docs/models/gpt-5 | 301 redirect from platform.openai.com/docs/models/gpt-5 |
| verbatim string on the page | `Sep 30, 2024 knowledge cutoff` | captured from the served HTML |
| retrieved on | 2026-08-25 | |
| context window | 400,000 tokens | same page |
| max output tokens | 128,000 | same page |
| list price | 1.25 USD per million input, 0.125 USD per million cached input, 10.00 USD per million output | same page |
| temperature | 0 where the endpoint accepts it. See Section 12.1. | |
| output format | JSON | |
| reasoning effort | **minimal**, set by the Section 12.2 decision rule. See Amendment 2. | |

Prior chat estimates of a 2024-05-31 cutoff and a 515 day window were
**unverified and are wrong**. They are not carried into this registration.

**Window derivation.** The guard band exists because the memorization
literature shows leakage past claimed dates, so the month immediately after the
cutoff is discarded rather than trusted.

| step | value |
|---|---|
| cutoff | 2024-09-30 |
| guard band, one calendar month | ends 2024-10-30 |
| first session strictly after the guard band | **2024-10-31** |
| last complete session in the bar store | **2026-07-24** |
| trading days in the window | **432** |
| registered minimum | 200 |
| clears the floor | **yes** |

The session calendar is the exchange calendar held in the source store's
`trading_calendar` table, not the dates any one symbol happened to trade.

Days whose forward return lands past the end of the store are still collected.
Their forward return is absent, recorded as absent, and never filled. The
evaluable counts are 427 at the five-session horizon and 431 at the
one-session horizon.

---

## Section 3. Task

Each eligible trading day, 30 names are drawn deterministically from the
`U-LIQ-500-stk-w60-m40-p5` universe at that day's governing monthly formation.
The draw is seeded and stratified so it reproduces exactly.

The model receives 30 anonymized feature rows and returns a full ranking, best
to worst expected relative next-window return, as a JSON list of row labels.

Row labels are per-call random letters, remapped every call.

There is **no confidence field**. The ranking is the entire output. See
Section 16, clause 3.

---

## Section 4. Features

The complete list. Nothing else ever enters the prompt.

| feature | definition |
|---|---|
| `ret_1` | trailing 1-session return |
| `ret_5` | trailing 5-session return |
| `ret_10` | trailing 10-session return |
| `ret_20` | trailing 20-session return |
| `ret_60` | trailing 60-session return |
| `rvol_20` | realized volatility over 20 sessions |
| `rvol_60` | realized volatility over 60 sessions |
| `dvol_z_60` | dollar-volume z-score over 60 sessions |
| `vtrend_5_60` | volume trend, mean volume over 5 sessions divided by mean volume over 60 |

Every feature is cross-sectionally z-scored within the day.

No tickers. No dates. No absolute prices. No market-level values, so an index
move cannot identify the date.

The brief describes the logistic baseline as fitting "the identical eight
features". The enumeration above holds nine. The enumeration governs, because
the brief also states the list is complete. Recorded as ADR-006.

---

## Section 5. Horizon

- **Primary.** Next-5-session return.
- **Secondary.** Next-session return.
- Overlap is handled by day-clustered inference with a moving-block bootstrap
  whose expected block length is 10 sessions, twice the primary horizon.

---

## Section 6. Baselines

Computed locally, free, on the identical feature block and the identical days.

1. **Sign of last 1-session return.** Rank descending by `ret_1`.
2. **12-1 momentum rank.** Trailing 12-month return excluding the most recent
   month, from the ported machinery.
3. **Logistic regression on the identical nine features.** Fit once on data
   strictly before the window start, then frozen. Never refit inside the
   window.

The logistic fit sample is every panel day from 2022-01-03 through 2024-10-30,
which is strictly before the window start of 2024-10-31. The fitted
coefficients are written once and hashed. A refit inside the window fails
`tests/test_guards.py`.

---

## Section 7. Contamination defenses

Three layers.

1. **Post-cutoff window primary.** Section 2.
2. **Anonymization.** Section 4. Per-call letter labels, remapped every call.
3. **Negative-control leakage audit at B.2.** Shuffle stored rankings within
   day. The rank IC must collapse toward zero. A non-zero result stops
   everything.

---

## Section 8. Inference

**Primary contrast.** Mean daily rank IC of the model minus mean daily rank IC
of the best baseline.

- Day-clustered bootstrap at 10,000 resamples.
- Two-sided at t 2.0.
- Within-day permutation null at 10,000.

A single pre-registered contrast on a single pre-registered model, so no family
correction applies. The registration states why: **this hypothesis was not
selected from a sweep.** It was written before any output existed.

**Per-model inference is primary. Pooled numbers are descriptive and never
touch a verdict.** See Section 16, clause 1.

---

## Section 9. Power, derived from the window in Section 2

The predecessor registered its power against a 50 bp effect and delivered a
sample that could not distinguish no effect from no power. These numbers are
produced before a cent is spent, from the derived day count.

Under the null, a daily Spearman rank IC across 30 names has standard deviation
1 / sqrt(29) = **0.185695**.

### 9.1 Registered power floor

The floor named in the B.3 replay schedule is detectable IC 0.025 at 30 names.
It is a one-sample test of the model's own daily rank IC against zero, at t
2.0, with no overlap adjustment.

    MDE = 2.0 * 0.185695 / sqrt(432) = 0.01787

**0.01787 is below 0.025. The window clears the registered power floor.**
Collection is authorized.

### 9.2 The number that governs interpretation

The primary contrast is a difference of two daily IC series. Its standard
deviation depends on how correlated the model and the baseline turn out to be,
and its effective sample size depends on the overlap a five-session horizon
induces. Consecutive start dates share four fifths of their forward window, so
the variance of the mean inflates by

    VIF = 1 + 2 * sum_{k=1..4} (1 - k/5)^2 = 3.4

which takes 427 evaluable days to **125.6** independent-equivalent days.

Primary horizon, 5 sessions, D = 427, effective D = 125.6:

| corr(model, baseline) | sd of daily contrast | detectable at t 2.0 | detectable at 80 percent power |
|---|---|---|---|
| 0.00 | 0.2626 | 0.0469 | 0.0666 |
| 0.30 | 0.2197 | 0.0392 | 0.0557 |
| 0.50 | 0.1857 | 0.0331 | 0.0471 |
| 0.70 | 0.1438 | 0.0257 | 0.0365 |

Secondary horizon, 1 session, D = 431, no overlap penalty:

| corr(model, baseline) | sd of daily contrast | detectable at t 2.0 | detectable at 80 percent power |
|---|---|---|---|
| 0.00 | 0.2626 | 0.0253 | 0.0359 |
| 0.30 | 0.2197 | 0.0212 | 0.0301 |
| 0.50 | 0.1857 | 0.0179 | 0.0254 |
| 0.70 | 0.1438 | 0.0139 | 0.0197 |

**Realistic effect band from the literature: 0.01 to 0.05.**

### 9.3 The registered limitation

The primary contrast detects effects in the **upper half** of the realistic
band and is **underpowered for the lower half**. At the most likely correlation
cell, 0.5, the primary detects 0.0331 and is 80 percent powered for 0.0471. The
secondary is better powered at every cell because it carries no overlap penalty.

The primary stays the primary. Promoting the better powered secondary after
seeing a result is exactly the move this repository exists to prevent. Recorded
as ADR-007.

A null on the primary therefore does not distinguish "no effect" from "an
effect below 0.033". The verdict table in Section 10 is read with that in mind,
and B.2 states the achieved interval rather than only its sign.

---

## Section 10. Verdict table

Written now, before any output exists.

| outcome | consequence |
|---|---|
| beats coin **and** beats every baseline at the bar | conditional phase C.1 authorized on the frontier trio, each on its own post-cutoff window, labelled a large-effect screen |
| beats coin, does **not** beat the baselines | an expensive wrapper for a subtraction. No phase. Finding recorded. |
| does **not** beat coin | the replication confirms the council negative under frontier capability and sane formulation. Closed. |
| coverage below the Section 0 floor | BLOCKED. No verdict claimed. |

---

## Section 11. Epistemic boundary

Verbatim, and it governs every sentence written about a positive result:

> A positive supports the claim the pipeline predicts, never the claim the
> model understands.

---

## Section 12. Spend

**Cap: 10.00 USD, ledger-enforced.** The collector refuses a batch before
sending it whenever completing that batch would cross the cap.

The 10 USD is a **leftover balance rather than a dedicated budget**, so the
effective cap is the lower of 10 USD and whatever the account actually has
left. The account side is unknowable from here until the API says so.
`insufficient_quota` is therefore a **clean stop**, not a failure. It records
the day as `no_data` with the reason, stops the run, and lets Section 0 fire on
achieved coverage.

### 12.1 Arithmetic against the derived day count

432 eligible days, one batched call per day, at the Section 2 list rates.

Per call, estimated before calibration:

| component | tokens | rate | cost |
|---|---|---|---|
| input, 30 rows of 9 features plus instructions | 1,600 | 1.25 USD per million | 0.00200 USD |
| output, visible ranking | 150 | 10.00 USD per million | 0.00150 USD |
| output, reasoning at effort `low` | 1,000 | 10.00 USD per million | 0.01000 USD |
| **total per call** | | | **0.01350 USD** |

    432 calls * 0.01350 USD = 5.83 USD against a 10.00 USD cap

The reasoning-token count is the only large unknown and it is the term that
dominates. At 2,000 reasoning tokens the total reaches 10.15 USD and crosses
the cap.

### 12.2 Calibration, pre-registered

One technical calibration call runs **before** B.1, on one day drawn from the
window. It is **excluded from the sample**, recorded in the spend ledger with
kind `calibration`, and used for two things only:

1. confirm which request parameters the endpoint accepts, including whether
   `temperature` is accepted for this reasoning model
2. measure actual tokens per call

**Decision rule, registered now.** `reasoning_effort` takes the highest value
in the ordered set (`low`, `minimal`) whose calibrated projected total spend is
at most 80 percent of the remaining cap. If neither qualifies, B.1 does not
start and the run reports BLOCKED on spend.

If the endpoint rejects `temperature` for this model, the call is retried
without it and the deviation is recorded as an amendment. Determinism then
rests on the seeded panel draw and the frozen prompt, which is where it
already rests for everything except the model's own sampling.

---

## Section 13. Amendment 0, recorded

**The operator's registered prior. Recorded 2026-08-25, before any module
touched the sealed store.**

> Operator prior, probability that a rigorous version of this experiment beats
> the best baseline on the primary contrast:
>
>     0.05, ADOPTED FROM THE ASSISTANT. NOT INDEPENDENT.
>
> The operator adopted the assistant's prior of 0.05 rather than forming an
> independent one. The calibration ledger must show it as adopted rather than
> independent, because an adopted prior carries no information about the
> operator's own judgment and would corrupt the calibration record if logged as
> his.
>
> Recorded: 2026-08-25

**Assistant prior, recorded 2026-08-25, before any output existed: 0.05.**

The assistant's number was recorded beside the empty slot so it could not be
adjusted after the operator wrote his. The operator then adopted it. That
sequence is the reason this section states the adoption explicitly rather than
recording two agreeing priors, which a later reader would otherwise mistake for
two independent judgments that happened to coincide.

**Calibration status: one prior, not two. This experiment yields no evidence
about the operator's calibration.**

---

## Section 14. B.3 replay schedule

Prompts freeze at B.0b. The frozen prompt hash is recorded in
`reports/stage_b0b/mock_run.md` and every replay uses it byte for byte.

Each model replays when the calendar grows its clean window past the registered
power floor, detectable IC 0.025 at 30 names, which needs roughly 221 trading
days after its own guard band.

| model | cutoff | status |
|---|---|---|
| Kimi K3 | 2026 vintage, verify before computing the window | replays roughly mid 2027 |
| Qwen 3.8 Max | **undocumented in the material held. Verify before its window is computed. Never assume.** | blocked on verification |
| GLM-5.2 | 2026 vintage, verify before computing the window | replays roughly mid 2027 |

No window is computed from an assumed cutoff. A.2.0 already showed what an
assumed cutoff costs: the carried estimate of 2024-05-31 was wrong by four
months.

---

## Section 15. The five call states

Never merged.

| state | meaning | class |
|---|---|---|
| `stored` | a parseable ranking landed in the store | sample |
| `no_data` | the day had no eligible panel or no features | sample composition |
| `model_failed` | the model did not return a parseable ranking after the registered retries | **operational health** |
| `excluded_pre_cutoff` | the day falls inside the cutoff or the guard band | **sample composition** |
| `source_failed` | the source store could not serve the day | operational health |

`model_failed` is operational health. `excluded_pre_cutoff` is sample
composition. The news experiment drew the same boundary for the same reason.
Merging any pair destroys the distinction between a model that could not answer
and a sample that was never eligible.

---

## Section 16. The four council clauses

Each clause carries the evidence that produced it.

**Clause 1. Per-model inference is primary. Pooled numbers are descriptive and
never touch a verdict.**
The council's pooled confidence Spearman read plus 0.0357 while every provider
was individually negative: Opus minus 0.0996, Gemini minus 0.1156, GPT-5.5
minus 0.2724. A pooling artifact wore the costume of a result.

**Clause 2. Power is registered before the first call.**
The council's wide sample pre-registered 272 calls and 66 clusters against a
50 bp detectable effect and delivered 274 and 80. This experiment registers its
minimum detectable rank IC in Section 9 and shows the window covers the floor,
before spending a cent.

**Clause 3. No confidence field exists in version one.**
The council's confidence was decoration. The buckets were non-monotone, the top
bucket was worst at 25 percent, and no verdict ever reached 0.65. The ranking is
the entire output.

**Clause 4. The consolidat cell is a dormant named secondary.**
The 2026-07-27 session preserved a rationale cell, stated reasons containing
"consolidat", at 71.7 percent on 53 calls, explicitly not a finding. It was kept
so a future pre-registered test could name it in advance. **This design emits no
rationales, so the cell stays dormant, named, and applicable only if a
rationale-emitting variant is ever registered.** Continuity recorded.

---

## Section 17. Amendments

Amendment 0 is reserved in Section 13 and is empty. It blocks B.2.

### Amendment 1. Temperature is omitted, because the endpoint rejects it

**Raised 2026-08-25 by the Section 12.2 calibration call, before B.1 started.**

Section 2 registered temperature 0. The endpoint refused it verbatim:

    Unsupported value: 'temperature' does not support 0.0 with this model.
    Only the default (1) value is supported.

The call was retried without the parameter and succeeded, which is the behaviour
Section 12.2 registered in advance for exactly this case.

**Effect.** `temperature` is not sent. `send_temperature` is false in the frozen
config and the adapter reads it. Determinism now rests on the seeded panel draw
and the frozen prompt, which is where it already rested for everything except
the model own sampling. The model output is not deterministic and the
registration no longer claims it is.

### Amendment 2. reasoning_effort is minimal, set by the registered decision rule

**Raised 2026-08-25 by the Section 12.2 calibration call, before B.1 started.**

Section 12.1 estimated 1,000 reasoning tokens per call and 0.01350 USD. The
measurement disagreed.

| reasoning_effort | input | output | of which reasoning | cost per call | projected over 432 days |
|---|---|---|---|---|---|
| `low` | 1,753 | 2,508 | 2,432 | 0.027271 USD | **11.7812 USD** |
| `minimal` | 1,753 | 106 | 0 | 0.003251 USD | **1.4045 USD** |

The safety budget is 80 percent of the remaining cap, 7.9756 USD. `low` projects
11.7812 USD and fails it. `minimal` projects 1.4045 USD and clears it.

The registered rule reads: reasoning_effort takes the highest value in the
ordered set (`low`, `minimal`) whose calibrated projected total spend is at most
80 percent of the remaining cap. **The rule selects `minimal`.**

**The limitation this creates, stated plainly.** The gate runs the model with no
reasoning budget. A null result is a null for gpt-5-2025-08-07 **at minimal
reasoning effort**, not for the model at its best. Every sentence written about
the outcome carries that qualifier.

**The road not taken, and why.** A `low` effort run over 365 of the 432 days
would have fit the remaining cap and would still have cleared the registered
power floor, at a minimum detectable IC of 0.0194 against a floor of 0.025.
That option was **not** taken. Choosing it would mean changing the design after
seeing cost data, and picking which 67 days to drop after the fact. The rule was
registered before the measurement, so the rule governs. The `low` effort variant
over a shortened window is recorded here as a natural candidate for a future
registered variant, where it can be named in advance rather than chosen in
hindsight.

**Both calibration calls are in the spend ledger** under kind `calibration`,
keyed to the sentinel date `calibration`, excluded from the sample, and costing
0.030522 USD together.

### Amendment 3. A reasoning effort ladder, because minimal cannot hold the format

**Raised 2026-08-25, 14 gate calls into B.1. The run was stopped to record this
before it went further.**

Amendment 2 set `reasoning_effort` to `minimal`. The calibration call parsed
cleanly at that setting, but one call is not a sample. Across the first 14 live
attempts the model failed to return a usable permutation of the 30 labels on 9 of
them, and 2024-11-11 exhausted all five retries and landed in `model_failed`.

The failures are format compliance, not judgement:

| failure | count |
|---|---|
| ranking omitted or duplicated a label | 5 |
| ranking had 31, 32, 35, or 37 entries instead of 30 | 4 |

**Effect.** `reasoning_effort_ladder` is registered as `("minimal", "low")`.
Attempt one uses `minimal`. Any parse failure sends the next attempt to `low`,
where it stays. The ladder is identical for every day, so the procedure is
uniform even though the realized effort is not. The effort used is recorded on
every evidence row.

**Why this is an operational fix and not a design change.** Section 15 classifies
`model_failed` as **operational health**, not sample composition. Nothing here
touches the hypothesis, the features, the panel, the baselines, the horizon, or
the inference. It changes how reliably a ranking the model already produced gets
captured.

**The confound this creates, stated plainly.** Days that needed `low` are days
where `minimal` could not hold the format. If that difficulty correlates with
anything about the panel, the sample mixes two configurations in a way that is
not random. The realized effort is stored per day for exactly this reason, and
B.2 reports the outcome split by realized effort alongside the primary contrast.
The split is descriptive. It does not become a verdict, under Clause 1.

**Days already collected are recollected.** The 7 days stored before this
amendment followed the superseded procedure. Their evidence rows carry no
`reasoning_effort`, and the resume logic treats such a day as not yet collected,
so every day in the final sample came from one identical procedure. The
superseded rows stay in the ledger. A ledger is history and history is not
edited. The 9 superseded attempts cost 0.0286 USD and that spend still counts
against the cap.

**Spend.** At an assumed one fifth of days needing one escalated attempt, the
projection is roughly 3.8 USD against the 10 USD cap. The per-batch refusal uses
measured cost, so the cap holds regardless of how the assumption turns out.

### Amendment 4. A strict output schema, and the prompt freeze re-established

**Raised 2026-08-25, 29 gate days into B.1. The run was stopped again.**

Amendment 3 assumed the format failures were a reasoning budget problem and that
escalating to `low` would fix them. The live data says otherwise.

| effort | attempts | failed | failure rate |
|---|---|---|---|
| `minimal` | 29 | 12 | 41 percent |
| `low` | 19 | 9 | 47 percent |

**`low` fails as often as `minimal`.** The problem is the output format, not the
reasoning budget. Amendment 3 was the wrong diagnosis, correctly recorded, and it
is superseded here rather than quietly dropped.

**The fix.** The request now carries a strict JSON schema. The output is an
object with 30 required fields, `r01` through `r30`, each constrained by an enum
to the labels of that call. The grammar cannot produce a ranking of the wrong
length or a label that was never presented, which were eight of the nine observed
failures. Uniqueness is not expressible in strict mode, so the parser checks it
and the collector retries.

**Measured on 8 held-out window days at `minimal`:**

| metric | free-form array | strict schema |
|---|---|---|
| first-attempt compliance | 17 of 29, 59 percent | 7 of 8, 88 percent |
| mean latency | 16.3 s per attempt | 2.3 s |
| projected total over 432 days | 9.12 USD | **2.86 USD** |

The single failure was a repeat, not a length error.

**The ladder is re-tuned.** `("minimal", "minimal", "minimal", "minimal", "low")`.
Retries are independent samples, and at 88 percent per attempt four cheap
attempts leave an expected failure rate near zero. The expensive rung stays as a
last resort, where it is expected to run on a fraction of a day.

**The prompt freeze is re-established here.** B.0b froze a prompt that had never
met the real model, and no mock scenario could have exposed the problem, because
the mock returns a valid permutation by construction. That is a real gap in
mock-only verification and it is recorded as such. The corrected template digest
is

    7e6f3d6801506bd7b158d7937b8fc3bae82c8fffac6770acaeb924bc4391c7fb

and every B.3 replay uses these bytes. Re-freezing costs nothing scientifically
because no replay has run and the gate sample is recollected in full.

**Supersession now keys on the prompt digest.** Every evidence row records the
template digest that produced it. A day whose stored answer came from a different
prompt is recollected, because it answered a different question. This
generalizes what Amendment 3 needed and what Amendment 4 needs, and it will catch
the next one without further code.

### Amendment 5. Rejected answers are billed, so the ledger records them

**Raised 2026-08-25, during the same stop.**

The spend ledger recorded nothing for an attempt whose answer failed to parse.
Those calls were billed. Measured across the first 29 gate days the ledger read

    recorded 0.3494 USD against an actual 0.6429 USD, a 46 percent undercount

**A cap enforced against a number 46 percent too low is not a cap.** This is the
mechanism Section 12 relies on, so the defect matters more than its size.

**Effect.** `UnparseableResponse` carries the usage of the call that produced it.
The collector records that spend under kind `gate` with the note `rejected
answer`, and the evidence row carries the tokens and the rejected text. The
undercounted 0.2936 USD from the superseded attempts is not recoverable, because
the usage was discarded before it was seen. It is stated here instead, and the
superseded ledger rows stay exactly as they were written.
