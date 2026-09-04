# NPDExperiment — verification (Agent C, VERIFY)

Repository: `NPDExperiment`
Anchored SHA: `2d3d0aebf977fb2821ec78c25b370c84ec055920` (main, 2026-08-25)
Snapshot read: `SNAP/NPDExperiment/`; live repo read-only for git objects, `var/*.db`,
`ledgers/*.jsonl`. Live HEAD equals the anchored SHA before and after; tree clean both times.
Recomputation ran under `~/.cache/program-audit/scratchpad/work/agentC/npd_verify/` with the audit venv,
against read-only `file:…?mode=ro&immutable=1` sqlite URIs. No repository script was executed
in place.

Reference: the LOCATE inventory at `findings/agentC/verification/NPDExperiment.inventory.md`.
This pass re-derived every figure independently rather than carrying the inventory's numbers.

**Anchoring caveat that governs everything below.** Every outcome figure in this repository
rests on four untracked files (`var/npd.db`, `var/npd_sealed.db`, `var/npd_fit.db`,
`ledgers/{spend,evidence}.jsonl`). They were read `2026-09-04T18:21Z – 18:32Z`. Their mtimes
(2026-08-25) are consistent with no change since the anchor, but mtimes are not proof, and a
reader who clones the repository at `2d3d0ae` can re-derive none of these numbers.

**Headline.** 20 of 26 numeric claims VERIFY, most of them exactly to the printed digit. The
inference machinery — block bootstrap, permutation null, validity gate, verdict rule, power
grid, spend ledger, coverage — reproduces without exception. Six claims do not: one is a
substantive statistical inversion (the "strong negative correlation" behind the closure's
account of its own power), one is a registered deliverable that was never produced, and four
are counting or provenance errors. Two further claims are UNVERIFIABLE because the ledger
discarded the inputs.

---

## A. Claims table

Tolerance convention: "printed digit" means the recomputed value rounds to the stated value at
the precision the document prints. Costs are compared to 1e-6 USD.

| # | claim (short) | file:line | stated | source of truth | recomputed | tol | status |
|---|---|---|---|---|---|---|---|
| C1 | model and momentum daily ICs "strongly negatively correlated" | `reports/stage_b2/evaluation.md:229-233` | strong negative correlation | `var/npd.db:model_ranking` + `baseline_ranking` + `var/npd_sealed.db:forward_return`, n=404 | Pearson **+0.1182** | ±0.001 | **CONTRADICTED** |
| C2 | realized minimum detectable contrast | `reports/stage_b2/evaluation.md:93` | 0.0512 | `evaluator.py:524,544`, rerun on the stores | 0.0512418 | printed digit | VERIFIED |
| C3 | verdict row "does not beat coin" | `reports/stage_b2/evaluation.md:123,127` | YES / Closed | `evaluator.py:546-547,686-706`, rerun | model IV −0.027575…+0.039729 (low<0) ⇒ same row | exact | VERIFIED |
| C4 | Section 0 coverage and GO | `reports/stage_b1/collection.md:33,41` | 96.1%, GO | `var/npd.db:day_status`, `section0.py:47-90` | 415 stored / 432 eligible = 0.960648 → "96.1%", ≥0.90 ⇒ GO | exact | VERIFIED |
| C5 | spend, calls, unit cost | `reports/stage_b1/collection.md:47-51` | 6.9378 USD; 920 gate calls; 0.007508/call; 3.0622 remaining | `ledgers/spend.jsonl` (922 rows) | Σ=6.9377835; gate n=920, Σ=6.907261, mean=0.00750789; 10−Σ=3.062216 | 1e-6 | VERIFIED |
| C6 | permutation two-sided p | `reports/stage_b2/evaluation.md:113` | 0.5174 | `evaluator.py:663-668`, 10,000 draws, seed 20260845 | 0.5174483 (5,174 hits) | printed digit | VERIFIED |
| C7 | validity gate | `reports/stage_b2/evaluation.md:36-42` | +0.0001, MC −0.0001…+0.0003, sd 0.00925, pct −0.0179…+0.0181, PASS | `evaluator.py:368-400,620-628` | +0.00011025; −0.0000711…+0.00029165; sd 0.0092549; −0.017890…+0.018138; |mean|≤0.02 ⇒ PASS | printed digit | VERIFIED |
| C8 | registered power arithmetic | `REGISTRATION.md:204,212,225-227,231-245` | 0.185695; 0.01787; VIF 3.4; 125.6; 8-cell grid | `src/npd/power.py:33-126` | 0.18569534; 0.0178685; 3.4; 125.588; all 16 grid cells reproduce (0.2626/0.0469/0.0666 … 0.1438/0.0139/0.0197) | printed digit | VERIFIED |
| C9 | "the 26 superseded attempts and their 0.0286 USD" | `reports/session_a1_b1.md:254`; `REGISTRATION.md:779-780` | 26 attempts, 0.0286 USD | `ledgers/evidence.jsonl` | **74** superseded gate attempts, **0.318852 USD** (the 26 pre-Amendment-3 rows alone cost 0.026807) | 1e-6 | **CONTRADICTED** |
| C10 | every stored ranking carries the re-frozen digest | `REGISTRATION.md:780-781` | zero of the 415 from the superseded template | `ledgers/evidence.jsonl` | all 883 current-procedure rows carry `7e6f3d68…`; the 415 stored days are drawn from those rows; no second digest appears | exact | VERIFIED |
| C11 | Amendment 4 compliance table | `REGISTRATION.md:558-560,577` | minimal 29/12/41%; low 19/9/47%; first-attempt 17 of 29 = 59%; 7 of 8 = 88% | `ledgers/evidence.jsonl`, 48 Amendment-3-era rows | minimal 29 (17 stored/12 failed) = 41.4%; low 19 (10/9) = 47.4%; all 29 minimal rows are attempt 1, 17 stored = 58.6% → 59%; 7/8 = 87.5% → 88% | printed digit | VERIFIED |
| C12 | B.1 operational health | `reports/stage_b1/collection.md:52-53,70-75` | 883 attempts / 432 days / 2.04; 175 multi-attempt days; {minimal 813, low 70}; 74 superseded; 53 escalated; 3,514,278 in; 361,641 out of which 217,728 reasoning | `ledgers/evidence.jsonl`, 883 digest-bearing rows | 883/432 = 2.0440; 175; {minimal 813, low 70}; 74; 53; 3,514,278; 361,641; 217,728 | exact | VERIFIED |
| C13 | B.0 build counts | `reports/stage_b0/build.md:18,19,26,29,62,63,71-73` | 15,474,106 bars; 18,474 symbols; 55 formations, 500–500 members; 308,610 features; 432 anonymization days; 432 days per baseline | `var/npd.db` | 15,474,106; 18,474; 55, min=max=500; 308,610; 432; 432/432/432 (and `model_ranking` = 12,450 = 415×30) | exact | VERIFIED |
| C14 | "four times the evaluable days … near 1,700 trading days" | `REGISTRATION.md:716-718` | ×4, ≈1,700 | arithmetic on the realized MDE | 4×427 = 1,708 (4×404 = 1,616); MDE at 4× days = 0.02562, i.e. at the 0.026 floor of the registered projection | printed digit | VERIFIED |
| C15 | "All five caught and restored: True" | `reports/mutations.md:14` | five | `reports/mutations.json`; `scripts/mutations.py:214` at the anchor | the json holds **six** mutation objects and the table above the line lists six rows; the committed generator emits `All {len(results)}` → would print "All 6" | exact | **CONTRADICTED** |
| C16 | "B.2 reports the outcome split by realized effort alongside the primary contrast" | `REGISTRATION.md:535`; `reports/session_a1_b1.md:269` | delivered at B.2 | `reports/stage_b2/evaluation.md` (262 lines); `src/npd/eval/{evaluator,report}.py` | no effort split anywhere in the report; no effort term anywhere in the evaluator or the renderer | exact | **CONTRADICTED** |
| C17 | logistic fit sample | `reports/stage_b0/build.md:75` | 21322 rows, 711 days, 2022-01-03…2024-10-30 | `var/npd_fit.db` | 711 distinct dates in exactly that range; 21,330 rows per horizon of which **21,322 non-null at h=5** | exact | VERIFIED |
| C18 | "evaluable counts are 427 at the five-session horizon and 431 at the one-session horizon" | `REGISTRATION.md:92-93` | 427 / 431 | `var/npd_sealed.db` | 432 dates; 5 dates all-null at h=5 (2026-07-20…07-24) ⇒ **427**; 1 all-null at h=1 (2026-07-24) ⇒ **431** | exact | VERIFIED |
| C19 | Amendment 3's trigger counts | `REGISTRATION.md:504-510,538` | raised 14 gate calls in; 9 of the first 14 attempts failed; run stopped; 7 days stored before the amendment | `ledgers/evidence.jsonl`, 26 pre-Amendment-3 rows | the superseded procedure ran **26 attempts across 13 dates**, 16 failures, **10 days stored**, ending 17:14:59Z; the amended procedure starts 17:17:38Z. At attempt 14 the failure count is 7, not 9; the stated 5 label + 4 length failures is the state at attempt **16** | exact | **CONTRADICTED** |
| C20 | HTML masthead | `reports/session_record.html:191-192` | 38 modules · 4,699 lines; 113 tests | `git ls-tree`/`show` at `433dabe` | 38 `.py` files, 4,699 lines — exact; `def test_` count is **107** | exact / n.a. | VERIFIED (modules, lines); UNVERIFIABLE (113 tests) |
| C21 | Section 12.1 pre-spend arithmetic | `REGISTRATION.md:313,316` | 432×0.01350 = 5.83; 10.15 at 2,000 reasoning tokens | arithmetic on `config.py` prices | 5.832; per-call 0.02350 → 10.152 | printed digit | VERIFIED |
| C22 | Amendment 2 calibration projections | `REGISTRATION.md:471-477,490` | 0.027271→11.7812; 0.003251→1.4045; safety budget 7.9756; 0.0194 vs 0.025 | `ledgers/spend.jsonl` calibration rows + arithmetic | 11.78118; 1.40454; 0.8×(10−0.030522) = 7.97558; 0.019444 | printed digit | VERIFIED |
| C23 | Amendment 5 undercount | `REGISTRATION.md:612` | recorded 0.3494 vs actual 0.6429, 46 percent | `ledgers/evidence.jsonl` + `spend.jsonl` | recorded = 74 superseded rows 0.318852 + 2 calibration 0.030522 = **0.349374** ⇒ 0.3494 exact; 0.6429 = 0.349374 + the stated unrecoverable 0.2936; (0.6429−0.3494)/0.6429 = 45.65% → 46% | 1e-6 / n.a. | VERIFIED (0.3494, 46%); UNVERIFIABLE (0.6429) |
| C24 | window halves | `reports/stage_b2/evaluation.md:183-185,255-259` | 202/202, +0.0123, −0.0001, +0.0124, "about one third of one standard error" | `evaluator.py:679-683`, rerun | 202/202; +0.0122578; −0.0001035; +0.0123614; SE on the difference from sd 0.19 and VIF 3.4 = 0.0349 ⇒ ratio 0.354 | printed digit | VERIFIED |
| C25 | secondary horizon table | `reports/stage_b2/evaluation.md:158-173` | 412 days; best `logistic`; contrast −0.0300; IV −0.0677…+0.0077; MDE 0.0377; model −0.0203, logistic +0.0097, mom +0.0089, sign_last −0.0315 | rerun of `evaluate_horizon` at h=1, seed 20260855 | 412; logistic; −0.0299977; −0.0676895…+0.0076941; 0.0376918; −0.0202728, +0.0097249, +0.0088653, −0.0315313 | printed digit | VERIFIED |
| C26 | "404 evaluable days. 6 days dropped because a name in the panel carried no realized return" | `reports/stage_b2/evaluation.md:51-53` (with `progress.md:147` "404 of 415 stored") | 6 dropped | `var/npd.db:model_ranking` × `var/npd_sealed.db` | **11** of the 415 stored days are not evaluable: 6 partial panels (counted) **plus 5 whose entire forward window runs past the store end** (2026-07-20…07-24), which `read_sealed_returns` filters out before the `dropped` counter is reached | exact | **CONTRADICTED** (incomplete accounting) |
| C27 | Amendment 4 latency | `REGISTRATION.md:578` | free-form 16.3 s/attempt vs strict 2.3 s | `ledgers/evidence.jsonl` | every rejected attempt carries `latency_s = 0.0`, so no per-attempt mean is reconstructible; over the 17 successful free-form `minimal` attempts the mean is **2.031 s**, over the 10 successful free-form `low` attempts **30.63 s**, per-day total across the 29 superseded days **12.469 s**. None is 16.3 s, and the 8 held-out strict probe calls are not identifiable in the ledger | n.a. | UNVERIFIABLE |
| C28 | Amendment 4 spend projection | `REGISTRATION.md:579` | 9.12 USD free-form vs 2.86 USD strict over 432 days | `ledgers/spend.jsonl` | the 8 held-out probe calls cannot be isolated. For context the realized current-procedure gate spend is 6.58841 USD over 432 days (0.015251/day), 2.3× the 2.86 projection | n.a. | UNVERIFIABLE |
| C29 | source-integrity hash | `reports/stage_b0/build.md:9-12` | `backtest/universe.py` sha256 `8188eea0…5529`, unchanged | live `AiTrader/backtest/universe.py`, read 2026-09-04T18:31Z | `8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529` — matches | exact | VERIFIED (cross-repo, unanchored) |
| C30 | "The realized 0.36339 sits at 98 percent of that maximum" | `reports/stage_b2/evaluation.md:229`; `REGISTRATION.md:731-735` | 98% of 0.3714 | arithmetic | 0.36339 / (2×0.185695) = 0.97846 → 98% | printed digit | VERIFIED as arithmetic (the *inference* drawn from it is C1) |

---

## B. Derived quantities table

Every row is recomputed by me from stored primitives; none is copied from a document.

| # | derived quantity | inputs (file:line / data path) | method | result | agrees with document? |
|---|---|---|---|---|---|
| D1 | coverage rate from counts | `var/npd.db:day_status` (stored 415, model_failed 17) | 415/432 | 0.9606481 → 96.1% | yes, `collection.json` "coverage": 0.9606 |
| D2 | mean cost per gate call | `ledgers/spend.jsonl`, 920 gate rows | Σcost / n | 0.00750789 | yes, 0.007508 |
| D3 | attempts per day | `ledgers/evidence.jsonl`, 883 digest rows / 432 days | ratio | 2.04398 | yes, 2.04 |
| D4 | format-failure rates | 48 Amendment-3-era rows | 12/29, 9/19, 17/29, 7/8 | 41.4%, 47.4%, 58.6%, 87.5% | yes |
| D5 | effective sample size | contrast series sd and bootstrap SE, `evaluator.py:529` | (sd/se)² = (0.3633892/0.0256209)² | 201.166 | yes, 201.2 |
| D6 | realized VIF implied by the bootstrap | 404 days / 201.166 n_eff | ratio | **2.008** | the registration assumes 3.4 (`REGISTRATION.md:225`); the realized overlap penalty was *smaller* than registered — not stated anywhere |
| D7 | realized per-series daily IC sd | 404-day model and `mom_12_1` IC series | sample sd | model **0.251585**, momentum **0.293645** | not stated; both are 35% and 58% **above** the null 0.185695 the power model assumes |
| D8 | contrast sd rebuilt from its parts | D7 + corr +0.1182418 | √(σm²+σb²−2ρσmσb) | **0.3633892** | reproduces the printed 0.36339 exactly, with a **positive** ρ |
| D9 | contrast sd at zero correlation, realized sds | D7 | √(σm²+σb²) | **0.386681** | the observed 0.36339 is **below** the independent-series value, which by itself implies ρ>0 |
| D10 | contrast sd from the registered formula at the realized correlation | `power.py:116`, ρ=+0.1182 | √(2(1−ρ))·0.185695 | **0.246599** | inside the registered grid range 0.1438–0.2626; the entire excess to 0.36339 comes from D7, not from ρ |
| D11 | correlation implied by inverting the registered formula at 0.36339 | `power.py:116` | 1 − sd²/(2·0.185695²) | **−0.91475** | this is the number the documents' "strong negative correlation" describes; it is an artefact of holding both series at the null sd |
| D12 | the missing effort split (C16) | 404 evaluable days × stored-answer effort from `ledgers/evidence.jsonl` | mean daily IC and mean contrast by realized effort | `minimal` n=353: model IC −0.00040, contrast −0.02580; `low` n=51: model IC **+0.05092**, contrast **+0.05098** (iid SE 0.0465; ×√3.4 ⇒ 0.086, i.e. 0.6 SE) | not reported anywhere; the registered split would have shown a large descriptive gap that is still not significant |
| D13 | Amendment 5 "recorded" figure | 74 superseded rows + 2 calibration rows | Σcost | 0.318852 + 0.030522 = **0.349374** | yes, 0.3494 |
| D14 | Amendment 5 undercount percentage | 0.3494, 0.6429 | (a−b)/a | 45.65% | yes, "46 percent" |
| D15 | stored ranking row count | `var/npd.db:model_ranking` | count | 12,450 = 415 × 30 | consistent with 415 stored days at panel size 30 |
| D16 | fit-store row gap | `var/npd_fit.db` | 21,330 rows at h=5, 8 with NULL ret | 21,322 non-null | resolves the 8-row gap the inventory flagged; `build.md:75` is exact |
| D17 | 4× sizing | realized MDE 0.0512418 | MDE/√4 | 0.0256209 at 1,616–1,708 days | consistent with `REGISTRATION.md:716-718` |
| D18 | secondary interval under an independent-day bootstrap | 412-day h=1 contrast series, block=1 | block bootstrap | SE 0.019982, IV −0.069963…+0.009967, MDE 0.039965 | the registered block-10 run gives SE 0.018846, IV −0.067690…+0.007694 — block 10 at h=1 is **narrower**, not wider; the conclusion (excludes zero: False) is unchanged either way |

---

## C. Intervals table

Estimator common to I3, I4, I6, I7, I8, I9: `block_bootstrap_interval`
(`src/npd/eval/evaluator.py:160-190`) — a moving-block bootstrap, 10,000 resamples, block
length `2 × primary_horizon_sessions = 10`, interval formed as `point ± 2.0 × sd(bootstrap
means)`. This is a **normal-approximation interval on the bootstrap SE, not a percentile
interval**, and `t_critical = 2.0` is a registered constant (`config.py`), not a t-quantile at
any degrees of freedom. Both facts are stated in the registration (`REGISTRATION.md:184-185`).

Data structure throughout: one scalar Spearman rank IC per trading day over a 30-name panel,
days ordered. At the primary horizon consecutive days share four fifths of their forward
window, so daily values are serially dependent by construction; within a day the 30 names are
one joint draw, so there is no within-day replication to cluster on.

| # | file:line | quantity | estimator actually used | independence assumed? | is that plausible here? | stated | recomputed | status |
|---|---|---|---|---|---|---|---|---|
| I1 | `evaluation.md:37` | MC 95% band on the shuffled mean | `grand_mean ± 1.96·sd/√draws` (`evaluator.py:354,360-365,399`) | across Monte Carlo draws only | yes — draws are i.i.d. by construction; this is not an inference about the data | −0.0001 to +0.0003 | −0.0000711 to +0.00029165 | VERIFIED |
| I2 | `evaluation.md:39` | null distribution 2.5–97.5 percentile | order statistic on 10,000 permutation means (`evaluator.py:342-344`) | permutation exchangeability within day | yes — the shuffle is applied within each day, so the day structure is preserved | −0.0179 to +0.0181 | −0.017890 to +0.018138 | VERIFIED |
| I3 | `evaluation.md:79` | interval on the primary contrast | moving-block bootstrap, block 10, t 2.0, seed 20260835 | blocks assumed independent; days inside a block not | plausible: block 10 = 2× the 5-session overlap, so the block spans the whole dependence range. The realized VIF implied by the bootstrap is 2.01 (D6), below the registered 3.4 | −0.0673 to +0.0351 | −0.0673466 to +0.0351370 | VERIFIED |
| I4 | `evaluation.md:81` | bootstrap standard error | sd of the 10,000 block-bootstrap means | as I3 | as I3 | 0.02562 | 0.0256209 | VERIFIED |
| I5 | `evaluation.md:112` | permutation null 2.5–97.5 percentile | within-day permutation, 10,000 draws, seed 20260845 | within-day exchangeability | yes | −0.0184 to +0.0177 | −0.0183912 to +0.0176819 | VERIFIED |
| I6 | `evaluation.md:133` | interval on the model mean daily rank IC | same block bootstrap, seed 20260836 | as I3 | as I3 | −0.0276 to +0.0397 | −0.0275751 to +0.0397294 | VERIFIED |
| I7 | `evaluation.md:170` | interval on the secondary contrast | same code path, but block length is **still 10** because `evaluator.py:508` uses `2 × primary_horizon_sessions` regardless of the horizon being evaluated | blocks assumed independent at a horizon with **no** overlap | the registration specifies the block length only for the primary (`REGISTRATION.md:144-146`); applying it at h=1 is a code choice. Recomputed at block 1 the interval is **wider** (−0.069963…+0.009967, SE 0.019982) than the reported block-10 one, so the choice did not manufacture the null; "excludes zero: False" holds under both | −0.0677 to +0.0077 | −0.0676895 to +0.0076941 | VERIFIED (estimator deviates from the registration's stated scope but does not change the comparison) |
| I8 | `evaluation.md:192` | model against a coin, descriptive | identical object to I6 | as I3 | as I3 | −0.0276 to +0.0397 | −0.0275751 to +0.0397294 | VERIFIED |
| I9 | `evaluation.md:250-251` | half-width of the model-against-coin test | (I6.high − point)/1 | as I3 | as I3 | 0.0337 | 0.0336523 | VERIFIED |
| I10 | `REGISTRATION.md:38-39` | predecessor council interval, carried in from AiTrader | not computed in this repository | 80 independent clusters claimed | out of scope of this repository's data | −22.5 to +21.4 bp | not recomputed | UNVERIFIABLE here — the estimator and data live in `AiTrader`, not in `NPDExperiment`; the figure is carried in as text |
| I11 | `evaluation.md:94` / `REGISTRATION.md:231-245` | registered projection band for the detectable contrast | analytic grid, `power.py:98-126`, hardcoded as the string `REGISTERED_PROJECTION = "0.026 to 0.047"` at `report.py:22` | daily contrast values independent within the effective-day count; both series held at the null sd 0.185695 | **the sd assumption is falsified by the data** (D7: realized sds 0.2516 and 0.2936). The band is a pre-registration projection, so this is a limitation of the projection, not an error in it — but it is the reason the realized MDE exceeded it, and the documents attribute that to correlation instead (see DRAFT-V-1) | 0.026 to 0.047 | grid detect column 0.0257 … 0.0469 | VERIFIED (the string matches the grid it summarizes) |

No interval in this repository is a percentile bootstrap, none carries a degrees-of-freedom
parameter, and none has a multiplicity correction applied to it.

---

## D. Tests table

| # | file:line | statistic / p | test as implemented | tail | registered direction | dof / distribution | correction applied | decision rule it feeds | correction matches rule? | stated | recomputed | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | `evaluation.md:36,42` | shuffled mean daily rank IC vs tolerance 0.02 | within-day permutation gate; **no p is computed** — the rule is `abs(gate.grand_mean) <= 0.02` (`evaluator.py:627`) | two-sided by construction (absolute value) | two-sided; `REGISTRATION.md:174-175` asks the IC to "collapse toward zero" | none — Monte Carlo distribution, 10,000 draws | none | single gate, all-or-nothing (a fail aborts B.2 entirely) | n/a — a single tolerance check needs none | +0.0001, PASS | +0.00011025, PASS | VERIFIED |
| T2 | `evaluation.md:113` | two-sided permutation p | `(hits+1)/(draws+1)` on `|mean| ≥ |observed|` (`evaluator.py:667-668`); **the observed statistic is the model mean daily rank IC, not the contrast** | two-sided | `REGISTRATION.md:185` registers "two-sided at t 2.0"; Section 7 layer 3 defines the within-day shuffle as operating on the model's own rankings | exact permutation distribution, 10,000 draws | none | descriptive — no verdict row reads it | n/a — not a decision input | 0.5174 | 0.5174483 (one-sided upper would be 0.2546) | VERIFIED. Note: `REGISTRATION.md:186` lists the permutation null under the heading "Primary contrast" while the code tests the model IC against zero; the report labels its own statistic correctly at `evaluation.md:109` |
| T3 | `evaluation.md:80` | "excludes zero" on the primary contrast | `Interval.excludes_zero()` = `low > 0 or high < 0` (`evaluator.py:142-143`) | two-sided | two-sided | normal approximation on the bootstrap SE, t 2.0 | none | one component of the verdict rule | see T5 | False | low = −0.0673 < 0 < high ⇒ False | VERIFIED |
| T4 | `evaluation.md:133,193` | "beats a coin" | `model_interval.low > 0.0` (`evaluator.py:546`) | **one-sided (upper)** on a two-sided ±2·SE interval, i.e. α ≈ 0.025 in the registered direction | the hypothesis is directional (the model *beats* the baseline), so a one-sided read of a two-sided interval is conservative, not liberal | as T3 | none | verdict row 2 (single test) and row 1 (conjunction) | yes — a single test needs no correction | False | low = −0.027575 ⇒ False | VERIFIED |
| T5 | `evaluation.md:121-123` | the verdict row itself | row 1 fires on `beats_coin AND beats_best_baseline`; row 2 on `beats_coin` alone; row 3 otherwise (`evaluator.py:686-706`) | one-sided per component | as T4 | as T3 | **none**, and the report states "No family correction applies" (`evaluation.md:84`) | row 1 is a **conjunction / intersection-union** rule; row 2 is a single test | **yes.** An IU rule needs no per-component correction, and the union {row1, row2} fires only if `beats_coin`, so the global type-I rate is bounded by that single one-sided test. Applying a Šidák or Bonferroni here would have been the mismatch | row 3 fires | row 3 fires | VERIFIED |
| T6 | `evaluation.md:171-172` | secondary "excludes zero" / "model IC excludes zero" | as T3 / T4 at h=1 | as T3 / T4 | subordinate by registration (`REGISTRATION.md:256-258`) | as T3 | none | descriptive only — explicitly barred from changing the verdict (`evaluation.md:153-154`) | n/a | False, False | −0.067690<0<+0.007694 ⇒ False; model IV −0.047638…+0.007093, low<0 ⇒ False | VERIFIED |
| T7 | `evaluation.md:92-93` | effective sample size and realized MDE | `(sd_daily/se)²`, `t·se` (`evaluator.py:529,544`) | n/a | n/a | n/a | none | descriptive power statement | n/a | 201.2, 0.0512 | 201.166, 0.0512418 | VERIFIED |
| T8 | `REGISTRATION.md:36` | predecessor council z −0.046 | carried in from AiTrader | not stated here | not stated here | not stated here | not stated here | none in this repository | n/a | z −0.046 on 274 calls | not recomputed | UNVERIFIABLE here — external figure, no inputs in this repository |
| T9 | `REGISTRATION.md:418-420`, `DECISIONS.md:82-84` | predecessor pooled confidence Spearman | carried in | not stated | not stated | not stated | not stated | none | n/a | +0.0357 pooled vs −0.0996 / −0.1156 / −0.2724 | not recomputed | UNVERIFIABLE here — external |
| T10 | `REGISTRATION.md:434-437` | predecessor `consolidat` rationale cell | carried in, dormant | n/a | n/a | n/a | n/a | none | n/a | 71.7% on 53 calls | not recomputed | UNVERIFIABLE here — external |
| T11 | `REGISTRATION.md:558-560,577` | Amendment 4 failure and compliance proportions | raw proportions from the live ledger; no test statistic, no interval, no p | n/a | n/a | n/a | none | operational decision to change the ladder and add a schema | n/a — no inference is drawn beyond the point estimates | 41%, 47%, 59%, 88% | 41.4%, 47.4%, 58.6%, 87.5% | VERIFIED |

Nothing in this repository applies a multiplicity correction, and nothing in this repository
needs one. The one place a correction would have been *wrong* — a union-type correction on the
conjunction that fires verdict row 1 — is correctly left uncorrected and the reason is stated
in advance at `REGISTRATION.md:188-190`.

---

## E. Draft findings

### DRAFT-V-1
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the closure's account of why the realized power fell short — the "dormant observation" that the model leaned against momentum (`reports/stage_b2/evaluation.md` Appendix; ADR-014; the Closure block)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The realized 0.36339 sits at 98 percent of that maximum.** The model daily rank IC and the momentum daily rank IC are therefore strongly negatively correlated across this window, far outside the 0.0 to 0.7 range the registration contemplated." — NPDExperiment/reports/stage_b2/evaluation.md:229-233. Restated as the causal account of the closure at NPDExperiment/REGISTRATION.md:699-702 ("driven by a strong negative correlation between the model and momentum daily ICs"), as the named observation at NPDExperiment/REGISTRATION.md:727-729 ("The model was not producing noise around momentum. It was leaning systematically against it."), as ADR-014 at NPDExperiment/DECISIONS.md:272-276, and at NPDExperiment/progress.md:41-45, 70-73, 158-161.
- **Evidence:**
  - The Pearson correlation between the 404-day model daily rank IC series and the 404-day `mom_12_1` daily rank IC series is **+0.1182** — weakly *positive*. n = 404. Data: `/home/kiros-li/Documents/GitHub/NPDExperiment/var/npd.db` tables `model_ranking`, `baseline_ranking` and `/home/kiros-li/Documents/GitHub/NPDExperiment/var/npd_sealed.db` table `forward_return`, read read-only 2026-09-04T18:22Z (untracked, unanchored).
  - The realized per-series daily IC standard deviations are **0.251585** (model) and **0.293645** (momentum), n = 404 each — 35% and 58% above the null value 0.185695 that the power model assumes (NPDExperiment/src/npd/power.py:34-42, NPDExperiment/REGISTRATION.md:203-204).
  - √(0.251585² + 0.293645² − 2·0.1182418·0.251585·0.293645) = **0.3633892**, reproducing the reported daily contrast sd of 0.36339 (NPDExperiment/reports/stage_b2/evaluation.md:82) exactly — **with a positive correlation**.
  - At zero correlation and the *realized* per-series sds, the contrast sd would be √(0.251585²+0.293645²) = **0.386681**, which is *larger* than the observed 0.36339. An observed contrast sd below the independent-series value can only arise from a positive correlation.
  - The "theoretical maximum of 0.3714" (NPDExperiment/REGISTRATION.md:732) is 2 × 0.185695, i.e. a maximum **conditional on both series carrying the null sd**. Given the realized sds the maximum is 0.251585 + 0.293645 = 0.545230, and 0.36339 is 67% of it, not 98%.
  - Correlation with the other two baselines is also positive: `logistic` +0.0642, `sign_last` +0.4114 (n = 404 each).
  - The claim is not code output. `src/npd/eval/report.py` ends at the line "model at its best." (NPDExperiment/src/npd/eval/report.py:290-297), which is `reports/stage_b2/evaluation.md:207`. Everything from line 210 on — the whole appendix containing this claim — was written by hand and committed with the machine-generated report in `2c6d683`.
- **Recomputation (if any):** inputs `var/npd.db:model_ranking`, `var/npd.db:baseline_ranking`, `var/npd_sealed.db:forward_return` (horizon 5, non-null), joined exactly as NPDExperiment/src/npd/eval/evaluator.py:481-497 does, giving the same 404 evaluable days and the same daily-IC series (model mean +0.0060772 vs the printed +0.0061, contrast −0.0161048 vs the printed −0.0161). Method: `numpy.corrcoef` on the two 404-length series; sample sd with ddof=1; the variance identity above. Result: ρ = +0.1182418, σ_diff = 0.3633892 against the printed 0.3633892. Tolerance: the contrast sd matches to 1e-7; the correlation is stable to ±0.001 under any reasonable tie convention. Inverting the registration's own formula `σ_diff = √(2(1−ρ))·0.185695` (NPDExperiment/src/npd/power.py:116) at σ_diff = 0.36339 returns ρ = **−0.9147** — that is the number the documents are describing, and it is an artefact of holding both series at the null sd rather than at their realized sds.
- **What would resolve it:** compute `corr(model daily IC, mom_12_1 daily IC)` on the 404 evaluable days directly, from the same two stores the evaluator reads, and replace the causal sentence. The correct diagnosis is available from the same data: the registered power model assumed each daily IC carried the null sd 0.185695; the realized sds were 0.2516 and 0.2936, and that alone raises the contrast sd from the 0.2466 the registered formula gives at ρ = +0.1182 to the observed 0.36339. If ADR-014 is to survive as a dormant observation it has to be re-stated with its sign reversed, or withdrawn.
- **Confidence:** HIGH — the identity σ_diff² = σm² + σb² − 2ρσmσb reproduces the repository's own printed 0.36339 to seven digits only at ρ = +0.1182, and the observed sd is below the zero-correlation value, which forecloses a negative ρ.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA, the repository carries a `_CLOSED_DO_NOT_RUN_HERE` marker dated 2026-09-02, and the claim is present verbatim in four tracked documents at the anchor.
- **Disclosed by authors?:** no. The authors disclose that the observation "is not a finding" and may only be promoted by a future pre-registered test (NPDExperiment/REGISTRATION.md:737-742, NPDExperiment/DECISIONS.md:278-289) — but that disclosure is about its evidential *status*, not its sign. The documents state the correlation as measured fact ("**The measured basis.**", NPDExperiment/REGISTRATION.md:731) and use it as the recorded cause of the power shortfall in the Closure block.

### DRAFT-V-2
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the registered B.2 deliverable that was to address the Amendment 3 / Amendment 4 effort confound
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The realized effort is stored per day for exactly this reason, and B.2 reports the outcome split by realized effort alongside the primary contrast. The split is descriptive. It does not become a verdict, under Clause 1." — NPDExperiment/REGISTRATION.md:534-536. Repeated at NPDExperiment/reports/session_a1_b1.md:268-270.
- **Evidence:**
  - `reports/stage_b2/evaluation.md` is 262 lines and contains no split by realized reasoning effort — the only effort text in it is the Amendment 2 limitation prose at NPDExperiment/reports/stage_b2/evaluation.md:204-207.
  - The renderer contains no effort term: the only match for "effort" in NPDExperiment/src/npd/eval/report.py is that same limitation prose at lines 292-293. There is no match at all in NPDExperiment/src/npd/eval/evaluator.py.
  - The inputs exist. 53 days' stored answers came from `low` after an escalation (NPDExperiment/reports/stage_b1/collection.md:75, reproduced from `ledgers/evidence.jsonl`), of which 51 fall in the 404 evaluable days.
  - The commitment was live going into B.2: `reports/session_a1_b1.md` was committed at `02b8560` (2026-08-25T12:48 −0700), after Amendment 4 superseded Amendment 3's ladder, and it repeats the promise at line 269. Amendment 4 (NPDExperiment/REGISTRATION.md:550-586) re-tunes the ladder but never withdraws the reporting commitment.
- **Recomputation (if any):** inputs `ledgers/evidence.jsonl` (stored-state row per day carries `reasoning_effort`), `var/npd.db:model_ranking`, `var/npd.db:baseline_ranking`, `var/npd_sealed.db:forward_return`; read 2026-09-04T18:26Z. Method: partition the 404 evaluable days by the effort of the attempt that produced the stored ranking, then take the mean daily rank IC and the mean contrast against `mom_12_1` in each cell. Result: `minimal` n = 353, model mean IC **−0.00040**, contrast **−0.02580**; `low` n = 51, model mean IC **+0.05092**, contrast **+0.05098**. The i.i.d. standard error on the `low` contrast is 0.0465; inflated by the registered VIF 3.4 it is 0.086, so +0.0510 is about 0.6 SE — a large descriptive gap that is **not** significant, and a post-hoc subgroup besides. Tolerance: means to 1e-5.
- **What would resolve it:** produce the registered split as a descriptive table in the B.2 report, or record an amendment stating that the deliverable was dropped and why. Either resolves it; neither exists at the anchor.
- **Confidence:** HIGH — the deliverable is registered in one sentence, the artifact is 262 lines and does not contain it, and neither module that could have produced it references effort.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA and the project is closed.
- **Disclosed by authors?:** partly. The B.2 report carries the Amendment 2 limitation that "the gate ran at `minimal` reasoning effort on the large majority of attempts" (NPDExperiment/reports/stage_b2/evaluation.md:204-207), which is the honest general caveat. It does not disclose that the specific registered split was not produced, and the closure does not list it as an outstanding item.

### DRAFT-V-3
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the closure's correction to the closing instruction, and the B.1 session narrative — the accounting of what the superseded prompt template produced
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "It produced the two calibration calls and the 26 superseded attempts, and **zero** of the 415 stored rankings." — NPDExperiment/REGISTRATION.md:779-780. And: "The 26 superseded attempts stay in the ledger and their 0.0286 USD still counts against the cap." — NPDExperiment/reports/session_a1_b1.md:254.
- **Evidence:**
  - `ledgers/evidence.jsonl` holds 959 rows: 883 carrying `prompt_digest = 7e6f3d68…`, 2 calibration rows, and **74** gate attempts carrying no digest. Read read-only 2026-09-04T18:24Z (untracked, unanchored).
  - Those 74 rows cost **0.318852 USD**, of which 37 rows carry `cost_usd = 0` because their usage was discarded (the Amendment 5 defect). The 26 pre-Amendment-3 rows alone cost **0.026807 USD**; the 48 Amendment-3-era rows cost 0.292045 USD.
  - The repository's own B.1 report gets it right: "superseded attempts, kept in the ledger and excluded from these counts: **74**" — NPDExperiment/reports/stage_b1/collection.md:73.
  - Amendment 5 also aggregates over the full superseded slice: its "recorded 0.3494 USD" (NPDExperiment/REGISTRATION.md:612) is exactly 0.318852 (74 superseded rows) + 0.030522 (2 calibration rows) = 0.349374. So the same registration reasons over 74 attempts in one amendment and calls them 26 in the closure.
  - The 26/74 split is the pre- versus post-Amendment-3 boundary: 26 rows carry no `reasoning_effort` field, 48 do. Amendment 4 re-froze the template *after* both groups, so all 74 were produced by the superseded digest `9a174e01…`.
  - Neither `0.0286` nor `26 attempts` reproduces: the 26 pre-Amendment-3 rows sum to 0.026807 USD, and no prefix of the superseded slice sums to 0.0286 (attempt 27 reaches 0.028186, attempt 28 reaches 0.029554 — and both are past the 26 the sentence names).
  - `reports/session_a1_b1.md:254` first enters git at `02b8560` (2026-08-25T12:48 −0700), i.e. in the same commit as `collection.md` with its 74, so the two were written together.
- **Recomputation (if any):** inputs `/home/kiros-li/Documents/GitHub/NPDExperiment/ledgers/evidence.jsonl` (959 lines) and `ledgers/spend.jsonl` (922 lines). Method: partition evidence rows on presence of `prompt_digest` and of `reasoning_effort`, sum `cost_usd` per partition, and cross-check the count of gate rows in the spend ledger (920 = 883 current + 37 superseded that were billed). Result: superseded 74 rows / 0.318852 USD; pre-Amendment-3 26 rows / 0.026807 USD. Tolerance 1e-6 USD.
- **What would resolve it:** correct the closure sentence to 74 attempts and 0.3189 USD (or state explicitly that it means only the pre-Amendment-3 subset, and fix 0.0286 to 0.0268). The substantive half of the claim — that **zero** of the 415 stored rankings came from the superseded digest — is independently VERIFIED and is unaffected.
- **Confidence:** HIGH — a direct count of two untracked ledgers, cross-checked against the repository's own B.1 report, which states 74.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA. The ledgers are untracked, so in principle they could have changed after the anchor; their mtime is 2026-08-25 12:46 and the row counts match every tracked B.1 figure exactly, which makes post-anchor mutation implausible.
- **Disclosed by authors?:** no. The authors disclose the *unrecoverable* portion of the superseded spend (NPDExperiment/REGISTRATION.md:617-622), but not that the closure's attempt count is a third of what the ledger holds.

### DRAFT-V-4
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** Amendment 3's record of the live failure that triggered it, and the stop-and-amend discipline it asserts
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Raised 2026-08-25, 14 gate calls into B.1. The run was stopped to record this before it went further.**" and "Across the first 14 live attempts the model failed to return a usable permutation of the 30 labels on 9 of them" — NPDExperiment/REGISTRATION.md:504-509. And: "**Days already collected are recollected.** The 7 days stored before this amendment followed the superseded procedure." — NPDExperiment/REGISTRATION.md:538-539.
- **Evidence:**
  - The pre-Amendment-3 slice of `ledgers/evidence.jsonl` (rows with no `prompt_digest` and no `reasoning_effort`) is **26 attempts across 13 dates**, timestamped 2026-08-25T17:12:52Z through 17:14:59Z, with **10 days stored** and **16 failures**. The Amendment-3-era rows (which carry `reasoning_effort`) begin at 17:17:38Z. Read read-only 2026-09-04T18:24Z (untracked, unanchored).
  - At attempt 14 the cumulative failure count is **7** (4 label mismatches, 3 wrong-length), not 9. The stated failure table — "ranking omitted or duplicated a label | 5" and "ranking had 31, 32, 35, or 37 entries instead of 30 | 4" (NPDExperiment/REGISTRATION.md:514-517) — is the cumulative state at attempt **16**, where the counts are exactly 5 and 4.
  - "7 days stored" is the state at attempts 14 through 18. By the end of the superseded slice, 10 days were stored (2024-10-31, 11-01, 11-04, 11-05, 11-06, 11-07, 11-08, 11-13, 11-14, 11-15).
  - The 2.5-minute gap between 17:14:59Z (last superseded attempt) and 17:17:38Z (first Amendment-3-era attempt) is the actual stop. It sits after attempt 26, not after attempt 14 or 16.
  - The companion cost sentence in the same amendment — "The 9 superseded attempts cost 0.0286 USD" (NPDExperiment/REGISTRATION.md:543) — is not reproducible either: every one of the 16 pre-Amendment-3 failures carries `cost_usd = 0.0` (which is precisely the defect Amendment 5 documents two amendments later), so the 9 attempts the sentence names have **zero** recorded cost, and the full 26-attempt slice costs 0.026807 USD.
- **Recomputation (if any):** inputs `/home/kiros-li/Documents/GitHub/NPDExperiment/ledgers/evidence.jsonl`. Method: filter to gate rows (`date != "calibration"`) with no `prompt_digest`, split on presence of `reasoning_effort`, sort by `ts`, and walk the prefix accumulating state, failure type and cost. Result: the cumulative (fails, label, length, stored-days, cost) vector reaches (7,4,3,7,0.018936) at attempt 14, (9,5,4,7,0.018936) at attempt 16, and (16,12,4,10,0.026807) at attempt 26. Tolerance: exact on counts, 1e-6 on cost.
- **What would resolve it:** restate the amendment against the ledger — 26 attempts across 13 dates, 16 failures, 10 days recollected — or state that the counts are a snapshot taken mid-run while collection continued, which would contradict "the run was stopped … before it went further". The mechanism the amendment relies on (rows with no `reasoning_effort` are treated as not-yet-collected and recollected) is independently VERIFIED: all 415 stored days come from the 883 rows carrying the re-frozen digest.
- **Confidence:** MEDIUM on the intent (the "9 failures / 5 + 4" figures match a real prefix of the ledger at attempt 16, so the amendment is describing a genuine mid-run snapshot rather than inventing numbers), HIGH on the counts themselves (a direct walk of the ledger).
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA and the amendment text is unchanged from the commit that introduced it.
- **Disclosed by authors?:** no. Amendment 5 discloses that rejected attempts were unbilled (NPDExperiment/REGISTRATION.md:609-615), which explains the zero costs, but nothing discloses that the superseded procedure ran to 26 attempts and 10 stored days rather than 14 and 7.

### DRAFT-V-5
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the mutation-harness report, which is the repository's evidence that its guards actually bite
- **Direction:** neutral
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**All five caught and restored: True**" — NPDExperiment/reports/mutations.md:14
- **Evidence:**
  - The table immediately above that line lists **six** mutations, numbered 1, 2, 3, 4, 6, 5 — NPDExperiment/reports/mutations.md:7-12.
  - `reports/mutations.json` holds **six** objects, in the same 1,2,3,4,6,5 order, each with `"guard_failed_as_required": true` and `"restored_green": true`.
  - The committed generator cannot produce the word "five": at the anchor it emits `f"**All {len(results)} caught and restored: {every}**"` — NPDExperiment/scripts/mutations.py:214 — which would print "All 6". The literal `"All five"` existed only in the previous revision of that line (`git show 3c2a152:scripts/mutations.py:203`), which was changed in the same commit `2c6d683` that added mutation 6 and committed this report.
  - `progress.md:176` says "Six mutations run, all caught and restored". `reports/session_a1_b1.md:155` says "### Five mutations, all caught" over a five-row table — correct for its own commit `02b8560`, which predates mutation 6.
- **Recomputation (if any):** inputs `reports/mutations.json` (6 objects), `scripts/mutations.py:195-220` (the writer), and `git show 3c2a152:scripts/mutations.py` (the previous writer). Method: compare the committed artifact against the string the committed generator would emit for `len(results) = 6`. Result: the artifact's summary line is not producible by the code committed beside it.
- **What would resolve it:** re-run the harness at the anchored code, or correct the line to "All 6". The substance — six mutations, each caught by the named guard and each restored green — is unaffected and is carried correctly in the json and in the table.
- **Confidence:** HIGH — the generator source at the anchor formats an integer where the artifact carries a word.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA.
- **Disclosed by authors?:** no.

### DRAFT-V-6
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the B.2 report's accounting of how 415 collected days became 404 evaluated days
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Primary horizon, next-5-session return. **404 evaluable days.** 6 days dropped because a name in the panel carried no realized return. The absence is recorded and the day is dropped, never filled." — NPDExperiment/reports/stage_b2/evaluation.md:51-53. Read against "| evaluable days | 404 of 415 stored |" — NPDExperiment/progress.md:147.
- **Evidence:**
  - 415 days carry a stored ranking (`var/npd.db:day_status`, `stored` 415 / `model_failed` 17). 404 are evaluated. The gap is **11**, of which the report explains 6.
  - Of the 415, exactly **6** fall on dates with a partially missing forward-return panel (2024-11-21, 2025-03-26, 2025-09-09, 2026-03-12, 2026-05-20, 2026-06-22) — these are the 6 the `dropped` counter reports.
  - A further **5** fall on the last five sessions of the window (2026-07-20 … 2026-07-24), whose entire 5-session forward window runs past the end of the sealed store. All 30 names on those dates carry `ret IS NULL`, so `read_sealed_returns` (NPDExperiment/src/npd/eval/evaluator.py:81-93, which filters `ret IS NOT NULL`) removes the dates entirely and they never reach the `dropped` counter at NPDExperiment/src/npd/eval/evaluator.py:484-490.
  - The same structure at the secondary horizon gives 415 − 1 tail − 2 partial = 412, matching NPDExperiment/reports/stage_b2/evaluation.md:167.
- **Recomputation (if any):** inputs `/home/kiros-li/Documents/GitHub/NPDExperiment/var/npd.db:model_ranking` (415 distinct dates) and `/home/kiros-li/Documents/GitHub/NPDExperiment/var/npd_sealed.db:forward_return` (432 dates × 30 names × 2 horizons = 25,920 rows; 156 NULLs at h=5, 32 at h=1), read 2026-09-04T18:22Z. Method: classify each date as all-null, partially null, or complete at each horizon, then intersect with the 415 stored dates. Result: h=5 → 5 all-null, 6 partial, 404 complete; h=1 → 1 all-null, 2 partial, 412 complete. Exact.
- **What would resolve it:** one sentence in the B.2 report reconciling 415 to 404 — "5 further days have no five-session forward window inside the store" — which is the mechanism the registration already anticipated.
- **Confidence:** HIGH — the classification is a direct count and reproduces the report's own 404 and 412 exactly.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA.
- **Disclosed by authors?:** partly, and this is why the severity is S4. The mechanism is registered in advance: "Days whose forward return lands past the end of the store are still collected. Their forward return is absent, recorded as absent, and never filled." — NPDExperiment/REGISTRATION.md:90-91. What is missing is the arithmetic tying that registered mechanism to the 5 missing days in the B.2 report, which presents "6 days dropped" as the whole of the gap.

---

## F. What could not be checked and why

| item | why |
|---|---|
| Amendment 4's "16.3 s" and "2.3 s" mean latencies (`REGISTRATION.md:578`) | `latency_s` is recorded as `0.0` on every rejected attempt — the same discard defect Amendment 5 documents for usage — so no per-attempt mean over the ledger is the quantity the amendment measured. The 8 held-out strict-schema probe calls the table names are not identifiable in `evidence.jsonl`. Recorded for the reader: the 17 successful free-form `minimal` attempts average 2.031 s, the 10 successful free-form `low` attempts 30.63 s, and the per-day total across the 29 superseded days 12.469 s. |
| Amendment 4's "9.12 USD" / "2.86 USD" 432-day projections (`REGISTRATION.md:579`) | same 8-call probe, not isolable. Realized current-procedure gate spend was 6.58841 USD over 432 days, 2.3× the 2.86 projection; the 10 USD cap held regardless. |
| Amendment 5's "actual 0.6429 USD" (`REGISTRATION.md:612`) | the usage behind the 37 unbilled attempts was discarded before it was recorded. The authors state this themselves at `REGISTRATION.md:619-622`. Only the "recorded 0.3494" half reconstructs (0.349374). |
| "113 tests" in the HTML masthead (`reports/session_record.html:192`) | `def test_` counts 107 at `433dabe`. 113 is plausibly pytest's collected count under parametrization, but establishing that would require running the repository's suite, which the audit rules forbid. Modules (38) and lines (4,699) verify exactly. |
| The predecessor AiTrader figures carried into the registration — the council interval −22.5 to +21.4 bp on 274 calls / 80 clusters (`REGISTRATION.md:38-39`), z −0.046 (`REGISTRATION.md:36`), the pooled confidence Spearman (`REGISTRATION.md:418-420`), the 71.7% `consolidat` cell (`REGISTRATION.md:434-437`) | external to this repository. No input, no estimator and no code for them exists under `NPDExperiment/`. They are carried in as text and are a matter for the AiTrader verification, not this one. |
| "This repository never installed a systemd unit, a timer, or a cron entry. Verified at closure" (`progress.md:87-90`) | a host-state claim, not a repository claim. Verifying it means enumerating the operator's units and crontabs, which is outside the audit's read scope. |
| The pre-image hash of `var/npd_sealed.db` claimed unchanged at B.2 (`progress.md:168-169`) | no hash of the sealed store was ever recorded, so "its hash … unchanged" cannot be checked. The mtime half does check: `2026-08-25 09:54:33 −0700`, before the B.1 collection (12:46) and before the B.2 run (13:10). |
| Every B.1 and B.2 figure, as a claim about the *anchored commit* | none of the four data files is tracked. The figures verify against the working tree read 2026-09-04T18:21Z–18:32Z; they do not verify against `2d3d0ae` itself, because `2d3d0ae` contains no ranking, no forward return and no ledger row. |
| The "9a174e01…" superseded digest as the producer of the 74 no-digest rows | those rows predate the field that records the digest, so the attribution rests on the ordering of the amendments rather than on a stored value. The complementary claim — that all 883 current rows carry `7e6f3d68…` and that the 415 stored days come from them — is directly VERIFIED. |

---

## G. Live-repo access log

`/home/kiros-li/Documents/GitHub/NPDExperiment` — read-only throughout. No write, no checkout,
no branch operation, no script executed inside the repository.

**`git -C /home/kiros-li/Documents/GitHub/NPDExperiment status --porcelain` BEFORE first access
(2026-09-04T18:21:17Z):**

```
```
(empty — clean)

**`git -C /home/kiros-li/Documents/GitHub/NPDExperiment status --porcelain` AFTER last access
(2026-09-04T18:44:17Z):**

```
```
(empty — clean)

`git rev-parse HEAD` = `2d3d0aebf977fb2821ec78c25b370c84ec055920`, equal to the anchored SHA,
before and after.

Reads performed against `NPDExperiment`:
- `git log`, `git show`, `git ls-tree`, `git rev-parse`, `git diff` (provenance of
  `reports/mutations.{md,json}`, `scripts/mutations.py`, `reports/session_a1_b1.md`,
  `reports/stage_b1/collection.md`, `reports/stage_b2/evaluation.md`)
- read-only sqlite (`mode=ro&immutable=1`) against `var/npd.db`, `var/npd_sealed.db`,
  `var/npd_fit.db`
- read-only line parse of `ledgers/spend.jsonl` (922 rows) and `ledgers/evidence.jsonl` (959 rows)
- `cat` of `var/source_hashes_before.txt`
- `.env` was **not** opened.

Cross-repo read for claim C29 (`AiTrader`, allowed as an audited repository, read-only):

**`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain` BEFORE
(2026-09-04T18:31:48Z):**

```
 M COLLECTION_LOG.md
```

**`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain` AFTER
(2026-09-04T18:31:48Z):**

```
 M COLLECTION_LOG.md
```

` M COLLECTION_LOG.md` is the pre-existing dirt named in the audit rules (a collector appends
to it) and is not caused by this audit. The only operation performed was
`sha256sum backtest/universe.py`.

Scratch scripts and outputs live under
`~/.cache/program-audit/scratchpad/work/agentC/npd_verify/` (the same files are visible at the older `/tmp/claude-1000/.../scratchpad/work/agentC/npd_verify/` path; the two snapshot trees were diffed and are byte-identical)
(`verify.py`, `ledger.py`, `acct.py`, `amend.py`, `a3b.py`, `a4.py`, `a5.py`, `b1.py`,
`lat.py`, `lat2.py`, `split.py`, `out.json`).

Unanchored caveat, restated: everything under `var/` and `ledgers/` is untracked. It was read
2026-09-04T18:21Z–18:32Z and may have changed after the 2026-08-25 anchor. Every row count I
derived matches a tracked figure exactly, which makes post-anchor mutation implausible, but
that is inference, not proof.

Pre-existing dirt not caused by this audit: none in `NPDExperiment`; ` M COLLECTION_LOG.md` in
`AiTrader`, as expected.
