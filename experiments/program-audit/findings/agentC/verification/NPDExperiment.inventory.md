# NPDExperiment — verification inventory (Agent C, LOCATE)

Repository: `NPDExperiment`
Anchored SHA: `2d3d0aebf977fb2821ec78c25b370c84ec055920` (main, 2026-08-25)
Snapshot read: `SNAP/NPDExperiment/` (tracked files, anchored)
Live repo touched read-only for: git objects, `ledgers/*.jsonl`, `var/*.db`, `ls -la`
Live HEAD at read time equals the anchored SHA. Working tree clean before and after.

Scope note. This is the LOCATE pass. Where a figure was cheap to recompute from the
stored primitives, the recomputation is reported inline and labelled DERIVED, because a
verified claim is as much a result as a contradicted one. Everything else is left marked
MUST-VERIFY without a guess.

---

## 1. Artifacts

### 1.1 Tracked (anchored at `2d3d0ae`) — documents

| path | holds | backs which figures | anchored |
|---|---|---|---|
| `REGISTRATION.md` (790 lines) | 17 registered sections, Amendments 1-7, the Closure block | window 432 days, power floor 0.01787, power grid, spend arithmetic, verdict table, calibration decision rule, closure headline figures | yes |
| `DECISIONS.md` (289 lines) | ADR-001 … ADR-014 | ADR-007 power limitation, ADR-010 after-the-fact best baseline, ADR-011 realized power, ADR-014 dormant momentum observation | yes |
| `progress.md` (351 lines) | per-stage log A.1 → Z.1 with ETA/actual | duplicates the B.1 and B.2 headline tables and the closure language | yes |
| `CLAUDE.md` | standing rules, seal rule, boundaries, layout | the "collection is not evaluation" rule, the single-reader seal | yes |
| `reports/stage_b0/build.md` (108 lines) | data build report | 15,474,106 bars; 18,474 symbols; 55 formations; 308,610 feature rows; 432 panels; logistic fit 21322 rows / 711 days; MDE 0.01787; VIF 3.4 / 125.6 | yes |
| `reports/stage_b0b/mock_run.md` (74 lines) | five mock scenarios | superseded prompt digest `9a174e01…`; mock spend 5.832 USD | yes |
| `reports/stage_b1/collection.md` (105 lines) | B.1 collection report | 415/432 stored, 96.1% coverage, GO, 920 gate calls, 6.9378 USD, token totals, effort split, 74 superseded | yes |
| `reports/stage_b1/collection.json` | machine-readable B.1 counts | coverage 0.9606, verdict GO, spend 6.9378, escalated_days 53, integrity 415×5 | yes |
| `reports/stage_b1/calibration.json` | the `low` calibration call | 1,753 in / 2,508 out / 2,432 reasoning; 0.027271 USD; projected 11.7812; safety budget 7.9782 | yes |
| `reports/stage_b1/calibration_minimal.json` | the `minimal` calibration call | 1,753 in / 106 out / 0 reasoning; 0.003251 USD; projected 1.4045; safety budget 7.9756 | yes |
| `reports/stage_b2/evaluation.md` (262 lines) | the one-shot evaluation | **every B.2 number**: gate, primary contrast, permutation null, verdict row, secondaries, window halves, realized-power appendix | yes |
| `reports/mutations.json` / `reports/mutations.md` | mutation harness output | six mutations, each with the guard output that failed | yes |
| `reports/session_a1_b1.md` (295 lines) | consolidated A.1→B.1 narrative | restates B.1 figures; adds "26 superseded attempts / 0.0286 USD"; 52 label/ticker collisions | yes |
| `reports/session_record.html` (461 lines) | HTML session record of A.1→B.1 | restates B.1 figures; masthead "38 modules · 4,699 lines · 113 tests" | yes |

### 1.2 Tracked — analysis code (what actually produced the figures)

| path | role | figures it produces |
|---|---|---|
| `src/npd/eval/evaluator.py` (722 lines) | the only permitted reader of the sealed store; `run_b2()` | model/baseline mean daily rank IC, best-baseline selection, block-bootstrap interval, bootstrap SE, daily contrast sd, realized MDE, effective n, the within-day null (gate + permutation), window halves, verdict row |
| `src/npd/eval/report.py` (~305 lines) | renders `reports/stage_b2/evaluation.md` | every table in the B.2 report; holds the literal `REGISTERED_PROJECTION = "0.026 to 0.047"` |
| `src/npd/eval/__main__.py` | B.2 entry point | — |
| `src/npd/power.py` (150 lines) | `null_ic_sd`, `overlap_vif`, `effective_days`, `detection_mde`, `powered_mde`, `contrast_grid`, `registered_floor_mde` | 0.185695; VIF 3.4; 125.6; the whole Section 9 grid; the 0.01787 floor |
| `src/npd/section0.py` (90 lines) | `fire()` | the GO/DEGRADED/BLOCKED verdict and the 96.1% coverage string |
| `src/npd/config.py` (121 lines) | frozen registered parameters | panel 30, horizons 5/1, bootstrap 10,000, permutation 10,000, t 2.0, band (0.01, 0.05), cap 10.0, prices, ladder |
| `src/npd/window.py` | derives window from cutoff + guard band + exchange calendar | 2024-10-31 → 2026-07-24, 432 days |
| `src/npd/ledger/spend.py` | `cost_of()` and the pre-batch cap refusal | every `cost_usd` in `ledgers/spend.jsonl` |
| `src/npd/ledger/evidence.py`, `ledger/append_only.py` | append-only evidence rows | `ledgers/evidence.jsonl` |
| `src/npd/data/{build,extract,features,formations,forward_returns,panel,series,source,store,universe,anonymize}.py` | B.0 data layer | bars, formations, panels, features, the two forward-return stores |
| `src/npd/baselines/{logistic,mom_12_1,sign_last}.py` | the three baselines | `baseline_ranking` rows |
| `src/npd/collect/{collector,adapter,prompt,scenarios,mock,__main__}.py` | B.1 collector | stored rankings, call states, evidence and spend rows, prompt digest |
| `scripts/report_b1.py` | writes `reports/stage_b1/collection.{md,json}` | all B.1 report figures |
| `scripts/calibrate.py` | the one pre-registered calibration call | both `calibration*.json` |
| `scripts/mutations.py` | mutation harness | `reports/mutations.{md,json}` |
| `tests/` (12 files, 107 `test_` functions at `433dabe`) | guards: seal, config enforcement, five call states, no confidence field, Amendment 0 refusal, absence, anonymization, universe port, window/power | the structural claims |

### 1.3 Untracked / gitignored — UNANCHORED data in the live working tree

Read `2026-09-04T05:25Z – 05:34Z`. All of this is outside git and may have changed since the
anchor; nothing here is protected by the anchored SHA.

| path | size (bytes) | mtime (local) | holds | backs |
|---|---|---|---|---|
| `var/npd.db` | 939,966,464 | 2026-08-25 12:46:42 | `bar` 15,474,106; `feature` 308,610; `panel` 34,290; `formation` 27,500; `anonymization` 12,960; `model_ranking` 12,450; `baseline_ranking` 38,880; `day_status` 432; `session` 2,907; `logistic_coefficient` 10; `meta` 23,042 | every B.0 build figure; the 415 stored rankings; the three baseline rankings; the B.2 inputs |
| `var/npd_sealed.db` | 1,585,152 | 2026-08-25 **09:54:33** | `forward_return` 25,920 rows, dates 2024-10-31…2026-07-24 (432), horizons 1 and 5, 32 and 156 NULL returns | **every outcome-bearing B.2 figure** |
| `var/npd_fit.db` | 2,609,152 | 2026-08-25 09:54:33 | `forward_return` 42,660 rows, dates 2022-01-03…2024-10-30 (711 distinct), 21,330 per horizon | the logistic fit sample |
| `var/npd.db-shm` / `-wal` | 32,768 / 0 | 2026-08-25 13:26:58 | sqlite sidecars | — |
| `var/source_hashes_before.txt` | 128 | 2026-08-25 09:29:42 | one line: `8188eea0…5529  …/AiTrader/backtest/universe.py` | the source-integrity hash in `stage_b0/build.md:9-12` |
| `ledgers/spend.jsonl` | 202,163 | 2026-08-25 12:46:42 | 922 rows: 920 `gate`, 2 `calibration` | spend 6.9378 USD, 920 calls, 0.007508/call, cap arithmetic |
| `ledgers/evidence.jsonl` | 806,001 | 2026-08-25 12:46:42 | 959 rows: 883 current-procedure (all carrying `prompt_digest`), 74 superseded gate, 2 calibration; raw responses kept verbatim | token totals, effort split, attempts/day, model_failed, prompt-digest supersession, Amendment 3/4/5 tables |
| `docs/` | — | 2026-08-25 09:26 | **empty directory** | nothing |
| `_CLOSED_DO_NOT_RUN_HERE` | 747 | 2026-09-02 22:38 | closure marker, excluded via `.git/info/exclude` | post-anchor operator note, not evidence |
| `.env` | 180 | 2026-08-25 01:30 | API key, mode 600 | **not opened** |

Anchoring consequence worth stating plainly: **every outcome number in this repository
rests on two untracked sqlite files and two untracked jsonl ledgers.** The tracked tree
contains no stored ranking, no forward return, and no ledger row. A reader who clones the
repository at the anchored SHA can re-derive none of the B.1 or B.2 figures.

---

## 2. Numeric claims, ranked (MUST-VERIFY marked)

Ranked by how much rests on the number. `[MV]` = MUST-VERIFY. `DERIVED:` lines record a
recomputation I performed from the stored primitives during this LOCATE pass.

### 1. `[MV]` The causal story behind the closure — "strongly negatively correlated"

> "**The realized 0.36339 sits at 98 percent of that maximum.** The model daily
> rank IC and the momentum daily rank IC are therefore strongly negatively
> correlated across this window, far outside the 0.0 to 0.7 range the registration
> contemplated."
> — `NPDExperiment/reports/stage_b2/evaluation.md:229-233`

Restated as load-bearing at `REGISTRATION.md:699-702`, `REGISTRATION.md:727-735` (the
Closure's only "dormant observation"), `DECISIONS.md:272-276` (ADR-014), `progress.md:41-45`,
`progress.md:70-73`, `progress.md:158-161`.
n = 404 evaluable days. Source: `var/npd.db:model_ranking` + `var/npd.db:baseline_ranking`
+ `var/npd_sealed.db:forward_return`. Produced by `src/npd/eval/evaluator.py:526-529`
(`contrast_sd_daily`) and the prose in `src/npd/eval/report.py`.

**DERIVED (recomputed from the stores, 2026-09-04):** the Pearson correlation between the
model daily rank IC series and the `mom_12_1` daily rank IC series over the 404 evaluable
days is **+0.1182**, i.e. weakly *positive*. Realized per-series sds are 0.25159 (model)
and 0.29364 (momentum), both far above the null 0.185695 the registration's formula
assumes. `sqrt(0.25159² + 0.29364² − 2·0.1182·0.25159·0.29364) = 0.36339`, reproducing the
reported contrast sd exactly with a *positive* correlation. The "strongly negative
correlation" is an artefact of inverting `sd_diff = sqrt(2(1−corr))·0.185695`
(`src/npd/power.py:116`) while holding each series at the null sd; the correlation that
formula implies is −0.9147, which is not the correlation the data has.

### 2. `[MV]` The closure's deciding number — realized minimum detectable contrast

> "| realized minimum detectable contrast | **0.0512** |"
> — `reports/stage_b2/evaluation.md:93`; restated `REGISTRATION.md:695`,
> `DECISIONS.md:215`, `DECISIONS.md:222`, `progress.md:39`, `progress.md:148`, `progress.md:156`

n = 404. Produced by `evaluator.py:524,544` as `t_critical × bootstrap_se`.
**DERIVED: 0.051242.** Reproduced exactly (bootstrap SE 0.0256209, t 2.0). The claim that
0.0512 sits above the whole registered band (0.01, 0.05) is arithmetically true.

### 3. `[MV]` The verdict row itself

> "| does not beat coin | **YES** |" … "**the replication confirms the council negative
> under frontier capability and sane formulation. Closed.**"
> — `reports/stage_b2/evaluation.md:123,127`

Deciding inputs, all `n = 404`, from `evaluator.py:496-547`:
model mean daily rank IC **+0.0061**, interval **−0.0276 to +0.0397**
(`evaluation.md:59,133`); primary contrast **−0.0161**, interval **−0.0673 to +0.0351**
(`evaluation.md:78-80,134`); `beats_coin = model_interval.low > 0` (`evaluator.py:546`).
**DERIVED:** model mean IC +0.0060772, interval −0.027575 … +0.039729; contrast
−0.0161048, interval −0.067347 … +0.035137. All reproduce to the printed precision.

### 4. `[MV]` Section 0 GO — the coverage number that authorized B.2

> "coverage: **96.1%**" / "## Section 0 verdict: **GO**"
> — `reports/stage_b1/collection.md:33,41`; `collection.json` `"coverage": 0.9606`;
> restated `progress.md:190-191`, `reports/session_a1_b1.md:197-201`
n: 415 stored of 432 eligible. Bars fixed at `REGISTRATION.md:16-18`, enforced by
`src/npd/section0.py:47-90`.
**DERIVED:** `var/npd.db:day_status` holds exactly `stored 415`, `model_failed 17`, total
432; `evidence.jsonl` final-state-per-day gives the same 415/17. 415/432 = 0.96065 → 96.1%.
Verifies.

### 5. `[MV]` The spend figure and the cap

> "- total spent: **6.9378 USD** of a 10.00 USD cap" / "gate calls billed: **920**" /
> "measured cost per gate call: **0.007508 USD**"
> — `reports/stage_b1/collection.md:47-51`; restated `REGISTRATION.md:789`, `progress.md:104,201`
**DERIVED:** `ledgers/spend.jsonl` holds 922 rows (920 `gate` + 2 `calibration`); Σcost =
**6.937784**; gate Σ = 6.907261, mean 0.0075079; calibration Σ = 0.030522. All verify.
Caveat already disclosed by the authors at `REGISTRATION.md:617-622`: 37 superseded
attempts carry `cost_usd = 0` because their usage was discarded, so the true spend exceeds
6.9378 by an unrecoverable amount (they state 0.2936 USD).

### 6. `[MV]` The permutation p-value

> "| **two-sided p** | **0.5174** |" — `reports/stage_b2/evaluation.md:113`
n = 404 days × 10,000 draws. `evaluator.py:663-668`.
**DERIVED: 0.51745** (5,173 hits + 1 over 10,001). Verifies.

### 7. `[MV]` The pipeline validity gate

> "| shuffled mean daily rank IC | **+0.0001** |" … "**Gate verdict: PASS.**"
> — `reports/stage_b2/evaluation.md:36,42`
n = 404 × 10,000 draws; tolerance 0.02 fixed at `REGISTRATION.md:174-175` and
`evaluator.py:553`.
**DERIVED:** gate mean +0.00011025, MC 95% −0.0000711 … +0.00029165, sd 0.0092549,
2.5/97.5 pct −0.017890 … +0.018138. All four reproduce.

### 8. `[MV]` The registered power arithmetic

> "MDE = 2.0 * 0.185695 / sqrt(432) = 0.01787" — `REGISTRATION.md:212`
> "VIF = 1 + 2 * sum_{k=1..4} (1 - k/5)^2 = 3.4 … 427 evaluable days to **125.6**" — `REGISTRATION.md:225-227`
> the eight-cell grid — `REGISTRATION.md:231-245`
**DERIVED:** 1/sqrt(29) = 0.1856953; 2·0.185695/sqrt(432) = 0.017872; VIF = 3.4 exactly;
427/3.4 = 125.588; every one of the eight grid cells (0.2626/0.0469/0.0666 … 0.1438/0.0139/0.0197)
reproduces to the printed digit. Verifies.

### 9. `[MV]` "26 superseded attempts … 0.0286 USD"

> "The 26 superseded attempts stay in the ledger and their 0.0286 USD still counts
> against the cap." — `reports/session_a1_b1.md:254`
> "It produced the two calibration calls and the 26 superseded attempts, and **zero** of
> the 415 stored rankings." — `REGISTRATION.md:779-780`
> compare "The 9 superseded attempts cost 0.0286 USD" — `REGISTRATION.md:543` (Amendment 3)
> compare "superseded attempts, kept in the ledger and excluded from these counts: **74**" — `reports/stage_b1/collection.md:73`
**DERIVED:** `evidence.jsonl` holds **74** superseded gate attempts (26 pre-Amendment-3
with no `reasoning_effort` field, 48 Amendment-3-era with one), total cost
**0.318852 USD**; the 26 pre-Amendment-3 rows alone cost 0.026807 USD across 13 dates.
The superseded prompt template therefore produced 74 gate attempts, not 26. Three different
counts (9, 26, 74) appear in the documents for "superseded attempts".

### 10. `[MV]` "zero of the 415 stored rankings" came from the superseded digest

> "Every stored ranking carries `7e6f3d6801506bd7…`" — `REGISTRATION.md:780-781`; `progress.md:96-99`
**DERIVED:** all 883 current-procedure evidence rows carry
`prompt_digest = 7e6f3d6801506bd7b158d7937b8fc3bae82c8fffac6770acaeb924bc4391c7fb`; no other
digest appears on any row that carries the field. The 415 stored days are all drawn from
those 883 rows. Verifies.

### 11. Amendment 4's compliance table

> "| `minimal` | 29 | 12 | 41 percent | / | `low` | 19 | 9 | 47 percent |" — `REGISTRATION.md:558-560`
**DERIVED:** the 48 Amendment-3-era evidence rows split exactly `minimal` 29 (17 stored /
12 model_failed) and `low` 19 (10 stored / 9 model_failed). 12/29 = 41.4%, 9/19 = 47.4%.
Verifies, including the free-form "17 of 29, 59 percent" at `REGISTRATION.md:576`.

### 12. B.1 operational-health figures

> "attempts under the current procedure: **883**, across 432 days, 2.04 per day";
> "days needing more than one attempt: **175**";
> "attempts by reasoning effort: **{'minimal': 813, 'low': 70}**";
> "days whose stored answer came from `low` after an escalation: **53**";
> "input tokens: 3,514,278"; "output tokens: 361,641, of which reasoning 217,728"
> — `reports/stage_b1/collection.md:70-75,52-53`
**DERIVED:** all seven reproduce exactly from the 883 `prompt_digest`-bearing evidence rows
(883/432 = 2.0440). Verifies.

### 13. The B.0 build counts

> "daily bars copied: **15,474,106**"; "distinct symbols: **18,474**"; "formations
> reproduced: **55** … members per formation: **500 to 500**"; "feature rows stored …
> **308,610**"; "days carrying an anonymization mapping: **432**"; baselines "432" each
> — `reports/stage_b0/build.md:18,19,26,29,62,63,71-73`
**DERIVED:** `var/npd.db` gives 15,474,106 `bar` rows over 18,474 distinct symbols;
55 distinct `formation_date`, min = max = 500 members; 308,610 `feature` rows;
432 distinct `anonymization` dates; 432 distinct dates for each of the three baselines.
All verify.

### 14. `[MV]` "roughly four times the evaluable days … near 1,700 trading days"

> "Sizing against the measured 0.36339 rather than the registered assumption requires
> roughly **four times the evaluable days**, landing near **1,700 trading days** of
> post-cutoff window." — `REGISTRATION.md:716-718`; `progress.md:51-53`
4 × 427 = 1,708, so the arithmetic is internally consistent. What it buys is not stated:
4× the days halves the MDE to ≈0.0256, still above the 0.01 lower edge of the registered
band. Worth checking against the band claim it is offered in support of.

### 15. Mutation count: five or six

> "**All five caught and restored: True**" — `reports/mutations.md:14` (the table above it
> lists six mutations, numbered 1,2,3,4,6,5)
> "Six mutations run, all caught and restored" — `progress.md:176`
> "### Five mutations, all caught" — `reports/session_a1_b1.md:155` (table lists five)
`reports/mutations.json` holds six objects, each `"guard_failed_as_required": true` and
`"restored_green": true`. S4 hygiene at most, but the summary line contradicts its own table.

### 16. `[MV]` A registered B.2 deliverable that was not delivered

> "B.2 reports the outcome split by realized effort alongside the primary contrast.
> The split is descriptive." — `REGISTRATION.md:535` (Amendment 3); repeated
> `reports/session_a1_b1.md:269-270`
`reports/stage_b2/evaluation.md` contains **no** split by realized reasoning effort.
`grep -n effort src/npd/eval/{evaluator,report}.py` returns only the Amendment 2 limitation
prose at `report.py:292-293`. The 53 escalated days are stored (`evidence.jsonl`) but the
registered descriptive split was never computed. The confound Amendment 3 raised at
`REGISTRATION.md:531-536` therefore stands unexamined.

### 17. The logistic fit sample

> "fitted once on **21322** rows across **711** days, 2022-01-03 through 2024-10-30"
> — `reports/stage_b0/build.md:75`; `progress.md:279`; `reports/session_a1_b1.md:115`
**DERIVED:** `var/npd_fit.db` holds 711 distinct dates in exactly that range and 21,330
`forward_return` rows per horizon. 21,322 is 8 fewer; the gap is presumably rows dropped
for an absent feature or target, which the documents do not state.

### 18. `[MV]` Registered evaluable counts against realized ones

> "The evaluable counts are 427 at the five-session horizon and 431 at the one-session
> horizon." — `REGISTRATION.md:92-93` (and the power grid is built on D = 427 / D = 431)
> "**404 evaluable days.** 6 days dropped because a name in the panel carried no
> realized return." — `reports/stage_b2/evaluation.md:51-54`
**DERIVED:** `var/npd_sealed.db` has complete 30-name panels on **421** days at h=5 and
**429** days at h=1, not 427 and 431. Intersecting with the 415 stored days gives 404 and
412, matching the report. The 415 → 404 gap is 11, of which the report explains only 6; the
other 5 are days whose forward window runs past the store end and which carry no h=5 return
at all. The registration's D = 427 is therefore an upper bound that was never realized, and
the registered power grid is stated against it.

### 19. Amendment 3's live-failure counts

> "**Raised 2026-08-25, 14 gate calls into B.1.**" / "Across the first 14 live attempts the
> model failed to return a usable permutation … on 9 of them" / "The 7 days stored before
> this amendment followed the superseded procedure." — `REGISTRATION.md:504-510,538`
**DERIVED:** the pre-Amendment-3 evidence rows number **26** attempts across **13** dates,
with 10 rows in state `stored` and 16 in `model_failed`. The "14 gate calls" and "7 days
stored" figures do not match what the ledger retained.

### 20. The HTML masthead counts

> "38 modules · 4,699 lines" / "113 tests" — `reports/session_record.html:191-192`
**DERIVED:** at the commit that added the file (`433dabe`), `src/**/*.py` is exactly 38
files and 4,699 lines. `def test_` count is 107 (113 may be pytest's collected count with
parametrisation). Modules and lines verify.

### 21. Section 12.1 pre-spend arithmetic

> "432 calls * 0.01350 USD = 5.83 USD against a 10.00 USD cap" / "At 2,000 reasoning tokens
> the total reaches 10.15 USD" — `REGISTRATION.md:313,316`
**DERIVED:** 432 × 0.0135 = 5.832; at 2,000 reasoning tokens the per-call cost is
0.02350 USD and 432 × that = 10.152. Both verify.

### 22. Amendment 2's calibration projections and decision rule

> "| `low` | 1,753 | 2,508 | 2,432 | 0.027271 USD | **11.7812 USD** | / | `minimal` | 1,753
> | 106 | 0 | 0.003251 USD | **1.4045 USD** |" / "safety budget … 7.9756 USD"
> — `REGISTRATION.md:471-477`
**DERIVED:** 0.027271 × 432 = 11.7811; 0.003251 × 432 = 1.4044; 0.8 × (10 − 0.030522) =
7.9756. The two calibration rows are in `ledgers/spend.jsonl` at the stated token counts.
Verifies. The related "0.0194 against a floor of 0.025" for a 365-day `low` run
(`REGISTRATION.md:490`) recomputes to 0.01944.

### 23. Amendment 5's undercount

> "recorded 0.3494 USD against an actual 0.6429 USD, a 46 percent undercount"
> — `REGISTRATION.md:612`
(0.6429 − 0.3494)/0.6429 = 45.65%, so "46 percent" rounds correctly. The two dollar figures
themselves are not reconstructible from the surviving ledgers, because the usage behind the
37 unbilled attempts was discarded — which the authors state at `REGISTRATION.md:619-622`.

### 24. The window-halves diagnostic

> "| first | 202 | +0.0123 | / | second | 202 | −0.0001 | / difference … +0.0124" and
> "**The observed difference is about one third of one standard error.**"
> — `reports/stage_b2/evaluation.md:183-185,253-260`
**DERIVED:** 202/202 days, +0.012258 and −0.000104, difference +0.012361. The SE claim
(0.19 daily sd, VIF 3.4, n=202 → 0.0349 on the difference; 0.0124/0.0349 = 0.36) also
checks out, though the realized model daily IC sd is 0.2516 rather than 0.19, which would
widen the SE further and strengthen the authors' own "inside noise" reading.

### 25. Secondary-horizon table

> "evaluable days 412 / best baseline `logistic` / contrast −0.0300 / interval −0.0677 to
> +0.0077 / realized minimum detectable contrast 0.0377" — `reports/stage_b2/evaluation.md:158-173`
**DERIVED:** 412 days, model −0.020273, logistic +0.009725, mom_12_1 +0.008865, sign_last
−0.031531, contrast −0.029998, interval −0.067690 … +0.007694, realized MDE 0.037692. All
reproduce.

---

## 3. Every confidence interval and every test statistic or p-value in the documents

Estimator conventions that apply throughout: the interval is
`point ± t_critical × sd(bootstrap means)` with `t_critical = 2.0`
(`src/npd/eval/evaluator.py:190`), i.e. a normal-approximation interval on the bootstrap SE,
not a percentile interval. The resampling scheme is a **moving-block bootstrap** with block
length `2 × primary_horizon = 10` sessions, applied at both horizons — including the
one-session secondary, where no overlap exists (`evaluator.py:508`). Data structure: one
scalar Spearman rank IC per trading day over a 30-name panel, days ordered.

| # | file:line | quantity | estimator / test | figure | n |
|---|---|---|---|---|---|
| I1 | `reports/stage_b2/evaluation.md:37` | Monte Carlo 95% interval on the shuffled mean | ±1.96 × sd/√draws (`evaluator.py:360-365`) | −0.0001 to +0.0003 | 404 days × 10,000 draws |
| I2 | `reports/stage_b2/evaluation.md:39` | null distribution 2.5–97.5 percentile | order statistic (`evaluator.py:342-344`) | −0.0179 to +0.0181 | 10,000 draws |
| I3 | `reports/stage_b2/evaluation.md:79` | interval on the primary contrast | moving-block bootstrap, 10,000 resamples, block 10, t 2.0 | −0.0673 to +0.0351 | 404 |
| I4 | `reports/stage_b2/evaluation.md:81` | bootstrap standard error | sd of 10,000 block-bootstrap means | 0.02562 | 404 |
| I5 | `reports/stage_b2/evaluation.md:112` | permutation null 2.5–97.5 percentile | within-day permutation, 10,000 draws | −0.0184 to +0.0177 | 404 × 10,000 |
| I6 | `reports/stage_b2/evaluation.md:133` | interval on the model mean daily rank IC | same block bootstrap, seed+1 | −0.0276 to +0.0397 | 404 |
| I7 | `reports/stage_b2/evaluation.md:170` | interval on the secondary contrast | same, block 10 at a 1-session horizon | −0.0677 to +0.0077 | 412 |
| I8 | `reports/stage_b2/evaluation.md:192` | interval, model against a coin (descriptive) | same as I6 | −0.0276 to +0.0397 | 404 |
| I9 | `reports/stage_b2/evaluation.md:250-251` | half-width of the model-against-coin test | derived from I6 | 0.0337 | 404 |
| I10 | `REGISTRATION.md:38-39` | predecessor council interval (external, carried in) | not recomputed here; AiTrader | −22.5 to +21.4 bp | 274 calls / 80 clusters |
| I11 | `reports/stage_b2/evaluation.md:94` / `REGISTRATION.md:231-245` | registered projection band for the detectable contrast | analytic grid, `power.py:98-126` | 0.026 to 0.047 | D = 427, n_eff = 125.6 |

| # | file:line | test statistic / p-value | test | figure | n |
|---|---|---|---|---|---|
| T1 | `reports/stage_b2/evaluation.md:36,42` | shuffled mean daily rank IC vs a registered tolerance of 0.02 | within-day permutation "pipeline validity gate"; **not a hypothesis test — no p is computed**, `abs(mean) <= 0.02` (`evaluator.py:627`) | +0.0001, PASS | 404 × 10,000 |
| T2 | `reports/stage_b2/evaluation.md:113` | two-sided permutation p | `(hits+1)/(draws+1)` on \|mean\| ≥ \|observed\| (`evaluator.py:667-668`) | **0.5174** | 404 × 10,000 |
| T3 | `reports/stage_b2/evaluation.md:80,134` | "excludes zero: False" on the contrast | `contrast_interval.low > 0` (`evaluator.py:547`) | False | 404 |
| T4 | `reports/stage_b2/evaluation.md:133,193` | "beats a coin: False" | `model_interval.low > 0` (`evaluator.py:546`) | False | 404 |
| T5 | `reports/stage_b2/evaluation.md:171-172` | secondary "excludes zero" / "model IC excludes zero" | as T3/T4 at h=1 | False, False | 412 |
| T6 | `reports/stage_b2/evaluation.md:92-93` | achieved effective sample size and realized MDE | `(sd_daily/se)²` and `t×se` (`evaluator.py:529,544`) | 201.2 and 0.0512 | 404 |
| T7 | `REGISTRATION.md:36` | predecessor council z (external) | carried in from AiTrader | z −0.046 | 274 |
| T8 | `REGISTRATION.md:418-420` / `DECISIONS.md:82-84` | predecessor pooled confidence Spearman (external) | carried in | +0.0357 pooled vs −0.0996 / −0.1156 / −0.2724 | not stated |
| T9 | `REGISTRATION.md:434-437` | predecessor `consolidat` rationale cell (external) | carried in, dormant | 71.7 percent on 53 calls | 53 |
| T10 | `REGISTRATION.md:558-560` | Amendment 4 format-failure rates | raw proportions from the live ledger | 12/29 = 41%, 9/19 = 47% | 48 attempts |
| T11 | `REGISTRATION.md:576` | first-attempt compliance, free-form vs strict schema | raw proportions | 17/29 = 59% vs 7/8 = 88% | 29 and 8 |

Two structural notes for the VERIFY pass, both DERIVED, neither yet a finding:
- `evaluator.evaluate()` (the legacy path, `evaluator.py:267`) caps the permutation at
  `min(cfg.permutation_resamples, 1000)`. The B.2 path (`run_b2`, `evaluator.py:663-664`)
  uses the full 10,000, so the reported p is at the registered resample count. The 1,000-cap
  path is exercised only by tests.
- The block bootstrap uses block length 10 at **both** horizons (`evaluator.py:508` uses
  `cfg.primary_horizon_sessions` regardless of the horizon being evaluated). The secondary
  interval at h=1 is therefore wider than an independent-day bootstrap would give. The
  registration specifies block length only for the primary (`REGISTRATION.md:144-146`).

---

## 4. Provenance claims

| # | claim (verbatim) | file:line | commit named | what would have to be true | status from git |
|---|---|---|---|---|---|
| P1 | "Written 2026-08-25, before the first call. Every number below is derived, not assumed." | `REGISTRATION.md:3` | none | REGISTRATION.md exists in a commit whose time precedes the first API call | **VERIFIED.** `64b7d41` (2026-08-25T16:39:00Z) contains the full 17-section registration; the earliest ledger row is `2026-08-25T17:10:48Z`. |
| P2 | "Committed before any call goes out. Coverage decides this verdict and nothing else does." (Section 0 outcome map) | `REGISTRATION.md:11` | none | the GO/DEGRADED/BLOCKED bars are byte-identical from a pre-call commit | **VERIFIED.** Section 0 is unchanged between `64b7d41` and HEAD. |
| P3 | "Written now, before any output exists." (Section 10 verdict table) | `REGISTRATION.md:268` | none | the three verdict rows are unchanged from a pre-call commit | **VERIFIED.** `git diff 64b7d41 HEAD -- REGISTRATION.md` shows no change inside Sections 9, 10 or 11. |
| P4 | "These numbers are produced before a cent is spent, from the derived day count." (Section 9 power) | `REGISTRATION.md:201` | none | the power floor and the eight-cell grid predate the first call | **VERIFIED.** Present verbatim in `64b7d41`; grid values recompute. |
| P5 | "A single pre-registered contrast on a single pre-registered model … **this hypothesis was not selected from a sweep.** It was written before any output existed." | `REGISTRATION.md:188-190`; `reports/stage_b2/evaluation.md:84-86` | none | Sections 1, 5, 6 and 8 unchanged since `64b7d41` | **VERIFIED** for the text. Note the contrast is defined against "the best baseline" without naming it; the selection is made after the fact under ADR-010 (see P9). |
| P6 | "**The operator's registered prior. Recorded 2026-08-25, before any module touched the sealed store.**" | `REGISTRATION.md:343-344`; `reports/stage_b2/evaluation.md:9` | none | a repository state exists in which Section 13 holds 0.05 and B.2 has not run | **NOT VERIFIABLE FROM GIT.** The fill of Section 13 and the B.2 artefacts land in the *same* commit `2c6d683`. What git does show: `64b7d41` … `433dabe` all carry `[ EMPTY.` in Section 13, `evaluation.md` records the run at `2026-08-25T20:10:48Z`, and `2c6d683` was committed at `20:13:28Z`. The only in-repo mechanism is `require_amendment_zero()` (`evaluator.py:73-78`), which refuses to run on the empty marker — an ordering enforced by code, not recorded by git. The document itself discloses the prior was adopted from the assistant and yields no calibration evidence (`REGISTRATION.md:349,367-368`). |
| P7 | "Prompts freeze at B.0b. The frozen prompt hash is recorded in `reports/stage_b0b/mock_run.md` and every replay uses it byte for byte." | `REGISTRATION.md:374-375` | none | the digest in force predates every call it governs | **VERIFIED for the re-freeze.** `7e6f3d68…` first enters git at `250bc8f` (2026-08-25T17:35:37Z); the earliest evidence row carrying it is `17:35:44Z`, seven seconds later. The original freeze `9a174e01…` entered at `943ba05` (17:06:55Z), before the first call. |
| P8 | "The corrected template digest is `7e6f3d68…` and every B.3 replay uses these bytes." + "**Supersession now keys on the prompt digest.**" | `REGISTRATION.md:592-603` | none | every stored ranking carries that digest | **VERIFIED from data.** All 883 current-procedure evidence rows carry it; the 415 stored days come from those rows. |
| P9 | "The best baseline is the one with the highest mean daily rank IC inside the evaluable window, **designated after the fact** … Choosing after the fact is **conservative in this direction and only this direction.**" | `DECISIONS.md:193-206` (ADR-010, "Accepted, 2026-08-25, at B.2") | none | ADR-010 is honestly labelled post-hoc | **VERIFIED as disclosed.** ADR-010 first appears in `2c6d683`, the same commit as the evaluation, and its own first line says "at B.2". The conservatism argument is checkable from the printed per-baseline table and holds: `mom_12_1` +0.0222 is the highest of the three. |
| P10 | "**ADR-007 registered this failure mode as a risk before collection. It was not discovered afterwards.**" | `REGISTRATION.md:704-705`; `progress.md:44-45` | none | ADR-007 predates the first call | **VERIFIED.** ADR-007 is present in `64b7d41`, and its text (underpowered lower half of the band, do not promote the secondary) is unchanged at HEAD. What ADR-007 registered is the *overlap* risk; the realized widening is attributed to a correlation claim that item 1 above contradicts. |
| P11 | "Amendment 6 carries POST-READ in its first line, states that it has no pre-registration force" | `DECISIONS.md:231-247` (ADR-012); `REGISTRATION.md:624-631` | none | Amendment 6 arrived after the read and says so | **VERIFIED.** Both Amendment 6 and Amendment 7 (VOID) first appear in `2d3d0ae`, the closure commit, after the evaluation commit `2c6d683`. The label matches the git order. |
| P12 | "Forward returns live in their own store, `var/npd_sealed.db`. The only module permitted to name that path or open that store is `npd.eval.evaluator`." | `DECISIONS.md:61-66` (ADR-004); ADR-008 `DECISIONS.md:150-164` | none | the split is real and the fit store holds no window date | **VERIFIED from data.** `var/npd_fit.db` holds 0 rows dated on or after 2024-10-31; `var/npd_sealed.db` holds 0 rows before it. `tests/test_guards.py:72-127` enforces the single-reader rule and `reports/mutations.md:46-59` shows mutation 3 failing it. |
| P13 | "Its hash and mtime are unchanged from the B.0 build, because it was opened read-only." (the sealed store at B.2) | `progress.md:168-169` | none | the sealed store mtime predates B.2 | **VERIFIED (unanchored read).** `var/npd_sealed.db` mtime is `2026-08-25 09:54:33 -0700`, i.e. before the B.1 collection (12:46) and before the B.2 run (13:10). The hash claim itself is unverifiable — no pre-image hash of the sealed store was recorded anywhere in the repository. |
| P14 | "`backtest/universe.py` sha256 before the extract … after the extract … unchanged: **True**" | `reports/stage_b0/build.md:9-12` | none | the AiTrader source file still hashes to `8188eea0…5529` | Partially checkable. `var/source_hashes_before.txt` (untracked) records the before-hash for `universe.py` only. The bar store `analysis_bars.db` has **no** recorded hash on either side, so "two read-only paths were opened and no others" is asserted for one of the two. Re-hashing the live AiTrader file is a cross-repo read left to the VERIFY pass. |
| P15 | "This repository never installed a systemd unit, a timer, or a cron entry. Verified at closure" | `progress.md:87-90` | none | no unit/timer/cron references this path | Not checked here; a host-state claim, not a repository claim. |
| P16 | "Nothing is deleted. The artifacts that make the result auditable stay in place" + the artifact table | `REGISTRATION.md:764-775` | none | the ledgers, stores and 415 rankings still exist | **VERIFIED (unanchored read).** All present in the live tree; **none of them is tracked**, so the anchored commit preserves the claim but not the artifacts. |
| P17 | "The question is closed **by operator decision, not by evidence.**" | `REGISTRATION.md:710` | none | — | A disclosure, not a verifiable claim. Recorded here because it is the correct frame for reading claims 1-3 and the authors state it themselves. |

---

## Live-repo access log

`/home/kiros-li/Documents/GitHub/NPDExperiment` — read-only throughout. No write, no
checkout, no script executed inside the repository. All recomputation ran from
`/tmp/.../scratchpad/work/agentC/recompute_npd.py` against read-only `file:…?mode=ro&immutable=1`
sqlite URIs and the jsonl ledgers.

**`git -C /home/kiros-li/Documents/GitHub/NPDExperiment status --porcelain` BEFORE first access
(2026-09-04T05:25:06Z):**

```
```
(empty — clean)

**`git -C /home/kiros-li/Documents/GitHub/NPDExperiment status --porcelain` AFTER last access
(2026-09-04T05:34:04Z):**

```
```
(empty — clean)

`git rev-parse HEAD` = `2d3d0aebf977fb2821ec78c25b370c84ec055920`, equal to the anchored SHA,
both before and after.

Reads performed against the live repository:
- `git log`, `git rev-list`, `git show`, `git diff`, `git grep`, `git ls-tree`, `git rev-parse` (history/provenance)
- `ls -la` / `ls -la --time-style=full-iso` on `/`, `var/`, `ledgers/`, `docs/`, `reports/`
- `cat` of `_CLOSED_DO_NOT_RUN_HERE` and `var/source_hashes_before.txt` (both small text)
- read-only line-by-line parse of `ledgers/spend.jsonl` (922 rows) and `ledgers/evidence.jsonl` (959 rows)
- read-only sqlite (`mode=ro&immutable=1`) queries against `var/npd.db`, `var/npd_sealed.db`, `var/npd_fit.db`
- `.env` was **not** opened.

Unanchored caveat: everything under `var/`, `ledgers/` and the `_CLOSED_DO_NOT_RUN_HERE`
marker is untracked. It was read at 2026-09-04T05:25Z–05:34Z and may have changed after the
2026-08-25 anchor; file mtimes (all 2026-08-25, except the 2026-09-02 closure marker)
are consistent with no change since the anchor, but mtimes are not proof.

Pre-existing dirt not caused by this audit: none. The live tree was clean apart from the
gitignored `.env`, caches, `.venv/`, `var/`, `ledgers/`, and `_CLOSED_DO_NOT_RUN_HERE`
(which the file itself says is excluded through `.git/info/exclude`).
