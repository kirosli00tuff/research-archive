# REOPEN LEDGER — HFExperiment

Repository: HFExperiment, anchored SHA `82e77a021256d917c665ff6d4304c25b08f35451` (main,
2026-08-28). Live HEAD verified identical at 2026-09-03T05:08Z, so nothing here is at risk from
later commits.

This ledger is **factual, not advocacy**. It records every hypothesis, stage, deferred parameter,
kill criterion, verdict bar and ADR "Changes it" clause in the repository, with its status, closure
kind and date, the deciding figure with its n and `file:line`, stated blockers, registered reopen
conditions, and whether a different repository in the program could plausibly satisfy a reopen
condition. Commit times are from git objects (UTC); document dates are as written by the authors.
Merged and de-duplicated from the draft ledger; no entry was removed, and entries B11 and A2 were
cross-linked because they share the same trigger clause.

---

## A. Hypotheses and outcome maps

| # | Entry | Status | Closure kind | Closure date | Deciding figure (n) — file:line | Blockers — file:line | Registered reopen conditions — file:line | Possibly met by another repo? |
|---|---|---|---|---|---|---|---|---|
| A1 | **H-F signal hypothesis**: EW top-5 by 12-1 momentum in U-LIQ-500 earns positive daily excess over the EW universe; 27.99 bp/day against a 4.07 bp/day cost hurdle (REGISTRATION.md:47-57) | closed (terminal, operator decision); hypothesis **untested here** | administrative — zero observations, not evidential | stated 2026-08-26 (REGISTRATION.md:306-308); commit `f13e1d3` 2026-08-25T07:45:29Z | **n = 0 shadow observations** (reports/monitor/verdict.txt:5,14,23; REGISTRATION.md:314-315). Registered projection: mean 27.99 bp/day, sigma 418, lower bound clears zero at day 2,061 and clears the hurdle 4.07 at day 2,852 (REGISTRATION.md:259-261; src/hfexperiment/registered.py:104-107). Registered prior 0.15 (REGISTRATION.md:276-278,289). Source figures from the AiTrader round of 2026-07-26: excess 27.99 bp/day, TE 66.40 pct/yr, IR 1.062 at width 5; 10.04 / 31.70 / 0.798 at width 50 (REGISTRATION.md:113-118; README.md:3-5) | 8-11 year positive clock (REGISTRATION.md:255-263); Alpaca data keys into `.env` (raised progress.md:147-148; resolved progress.md:99-100); B.1 paper-api 401 on `/v2/assets`, a "one-line fix" needed before 2026-09-01 (DECISIONS.md:378-387; progress.md:84-90) — cancelled as moot (progress.md:18-19); futility bar unreachable in practice (recomputed, AUDIT-A-HFExperiment-3) | **none registered for the signal question.** Section 12 forbids amendments responding to observed shadow outcomes (REGISTRATION.md:271-273); ADR-015 "Changes it: nothing after the series starts" (DECISIONS.md:255-256) — the series never started, so a formation-aligned restart is registration-clean (DECISIONS.md:244-253) | **YES** — AiTrader is the source of the 27.99 bp / IR 1.062 figures (README.md:3-5; REGISTRATION.md:53,91-95,113-118); any later powered momentum test there bears on this. See lead L1/L2 |
| A2 | **Section 0 broker outcome map** (GO / DEGRADED / BLOCKED) for the live execution sleeve at 1,000 USD (REGISTRATION.md:6-45) | closed — labelled BLOCKED (label disputed, AUDIT-A-HFExperiment-2) | measurement (paper-order behaviour) | 2026-08-25 (REGISTRATION.md:297-304); A.1b run 02:57-03:07Z (reports/stage_a1b/a1b_report.md:3) | n = 3 decimal orders on 2 names x 2 order types refused error 10243; 1 cashQty order refused error 10244; 1 whole-share control accepted (a1b_report.md:49-93; evidence.jsonl:28-49). All 20 names MinSize/SizeIncrement 0.0001 (a1b_report.md:14-35; evidence.jsonl:3-22) | IBKR TWS API refuses fractional equity quantities (a1b_report.md:67-70,78-82); Alpaca excludes Canadian residents (docs/ACCESS.md:12,31-32); Questrade API partner-only (ACCESS.md:13,33-34); Wealthsimple no API (ACCESS.md:14,35-36) | "IBKR shipping fractional support in the TWS API, or an Alpaca Canadian launch per ADR-003. Either is a new measurement" (DECISIONS.md:427-429); "An Alpaca Canadian launch would reopen the table" (DECISIONS.md:65-66; a1b_report.md:115-116; progress.md:44-46); "Recheck at stage C if Task 3 resolves badly" (ACCESS.md:19-20) — **trigger met 2026-08-25, no recheck recorded** (see B11) | **YES** — any repository trading US equities from Canada through a broker API may hold current broker/account facts. See lead L4 |
| A3 | **DEGRADED branch** — whole-share sizing at a 1,000 USD stake (REGISTRATION.md:21-31,147-159; DECISIONS.md:192-203) | closed | arithmetic on the registered stake | 2026-08-23 (A.2; progress.md:171-174; ADR-012) | median book share price 144 USD at the last two width-20 formations (REGISTRATION.md:150-151; reports/stage_a1/formations.md:27-28 — 143.80, 143.89); "20 names at one share each already cost about 2,880 USD" (REGISTRATION.md:152-153). Recomputed sum of one share each (n = 20): 7,890 USD at 2026-07-01 closes, 6,240 USD at A.2 mids, 5,936 USD at 2026-08-03 closes (formations.json; book_spreads.json; reports/stage_c1/formation_2026-08-03.json) | stake 1,000 USD, 900 deployed (REGISTRATION.md:133) | "Changes it: a materially larger stake, which is a new registration, not an amendment. A collapse in book share prices does not reopen it" (DECISIONS.md:201-203). Whole-share API trading confirmed open (ACCESS.md:197,205-206; progress.md:258-259). **Note:** this reopener is absent from every post-A.1b closure entry (AUDIT-A-HFExperiment-2) | no — the stake is operator-specific, not a fact another repository can supply |
| A4 | **Registered prior** that the sleeve ever clears its verdict: 0.15 (REGISTRATION.md:276-278; DECISIONS.md:221-222) | accepted 2026-08-24, never updated | n/a | acceptance 2026-08-24 (REGISTRATION.md:286-295) | 0.15 (REGISTRATION.md:289) | — | "Changes it: the operator at acceptance, for the prior" (DECISIONS.md:227) | no |

---

## B. Stages

| # | Entry | Status | Closure kind | Closure date | Deciding figure (n) — file:line | Blockers — file:line | Registered reopen conditions — file:line | Other repo? |
|---|---|---|---|---|---|---|---|---|
| B1 | Stage A.1 (scaffold, broker access, formation reproduction) | shipped, green | — | 2026-08-23 (progress.md:187-223) | 124 of 124 formation dates identical; universe exact at 10 checked dates, 500 rows each (progress.md:207-209; reports/stage_a1/universe_check.json, 10 entries); churn width 20 = 5.2 names/month over 6 formations (progress.md:209-210; formations.md:9-16); db hash `c30d3f4486e975a0` unchanged (progress.md:211-212) | Task 3 blocked on "no IBKR account" (progress.md:214-216) — superseded by A.1b and corrected by ADR-026 (DECISIONS.md:432-454) | ADR-005: "a full-pool refresh with a recorded new pull end" (DECISIONS.md:95); ADR-006: "If the recorded round's formation code ever enters scope and differs, the reproduction reruns" (DECISIONS.md:112-114) | **YES** — both conditions concern the AiTrader database and formation code (DECISIONS.md:89-93,99-101). See lead L2 |
| B2 | Stage A.2 (cost model, spread measurement, Sections 1-12 registered) | shipped, green | — | 2026-08-23 (progress.md:152-185) | book median spread 12.77 bp, p75 17.2, p90 20.7, max 27.4; n = 20 names x 9 cells over sessions 2026-08-19 to 21 (progress.md:156-161; REGISTRATION.md:170-173); width-5 spread 13.08 bp at median mid 201.91 (reports/stage_a2/cost_table.md:36); hurdle 4.07 bp/day (cost_table.md:36) | TAF one-cent floor UNMEASURED (REGISTRATION.md:179-180; ACCESS.md:98-102); mixed-order billing UNMEASURED (REGISTRATION.md:180-182) | ADR-007: "measured billing on paper and live fills" (DECISIONS.md:124); ADR-009: "recorded measurements at more widths would replace the two-point fit" (DECISIONS.md:157-158); ADR-013: "Re-measuring near each future formation would change it" (DECISIONS.md:215-216) | **YES for ADR-009** — more recorded widths would come from the AiTrader round. See lead L2 |
| B3 | Stage B.1 (bar pipeline, shadow series, verdict engine, monitor, timer) | shipped, green; armed 2026-08-24, **disarmed 2026-08-25 at n = 0** | — | built 2026-08-24 (progress.md:102-150); disarmed (progress.md:12-15; REGISTRATION.md:310-313) | 123 tests green, 3 mutations caught (progress.md:141-145); price reconciliation: 0 corporate actions in window across 20 names, medians 143.89 / 103.25 / 97.45 (reports/stage_b1/price_reconciliation.md:52-58); timer state at disarm: enabled + active, next formation 2026-09-01 (reports/monitor/health.txt:4-10) | Alpaca keys (resolved, progress.md:99-100); paper-api 401 (see A1) | ADR-016: "Changes it: nothing" (DECISIONS.md:273); ADR-017 benchmark handling: "evidence that the recorded round handled a missing member differently, which must be reported and corrected before 2026-09-01" (DECISIONS.md:283-285); halt confirmation: "a real halt feed" (DECISIONS.md:291-292); monitor: "a later stage may add HTML" (DECISIONS.md:309-311) | **YES for ADR-017** — the recorded round's member handling lives in AiTrader. See lead L2 |
| B4 | Stage B.1a (paper-api.alpaca.markets fix for the `/v2/assets` 401) | cancelled as moot | administrative (folded into the closure) | stated 2026-08-26 (progress.md:18-19) | 401 on `/v2/assets` with paper keys against api.alpaca.markets (DECISIONS.md:378-381; progress.md:84-86) | none technical — the authors size it as "a one-line fix" (progress.md:88-89) | "Changes it: the fix landing, which closes this note" (DECISIONS.md:387) | no |
| B5 | Stage B.2 | "registered and unrun" (progress.md:18) | — | — | **no registration text exists** in the repository or its history: `grep` returns n = 1 hit (the claim itself); `git log --all -S'B.2'` returns n = 1 commit, the closure commit (AUDIT-A-HFExperiment-7) | unknown | unknown | unknown — content is not recoverable from this repository. Possibly in the external stage prompt referenced at DECISIONS.md:22-23. See lead L7 |
| B6 | Stage C.1 (order-intent pipeline, wired gate with 8 refusals, spend ledger, read-only probe) | shipped, green | — | 2026-08-25 (progress.md:56-100) | 158 tests green, 4 mutations caught (progress.md:92-96); 8 refusals demonstrated against the real 2026-08-03 width-20 book, formation hash `0b28a5cfda7516fa` reproduced (reports/stage_c1/refusals.md:7-9); probe: [paper account ID removed] in a managed list of 1, server version 187 (refusals.md:325-334) | Amendment 1 not landed (refusals.md:11-17) | ADR-018: "the operator adopting the scoped username" (DECISIONS.md:334-336); ADR-019: "D.1's real adapter" (DECISIONS.md:350-351); ADR-020: "nothing" (DECISIONS.md:365); ADR-021 formation source: "a recorded instruction to backfill formations into the B.1 store" (DECISIONS.md:374-376) | no |
| B7 | Stage A.1b (paper capability test) | shipped; fired BLOCKED | measurement | 2026-08-25 (progress.md:23-54); commit `669eb5c` 2026-08-25T03:09:06Z | see A2; 5 of 10 authorized orders used, no fills, account verified flat twice (a1b_report.md:5-6,104-105) | Read-Only API state to be re-checked by the operator (progress.md:51-52) | see A2 | see A2 / lead L4 |
| B8 | Stage C.2 (paper fills for the three deferred parameters) | moot at this stake | administrative | 2026-08-25 (progress.md:53-54,98) | — | waits on paper fills that the channel cannot produce at fractional size (progress.md:98) | implicit: the A2 reopeners, or the A3 larger stake | no |
| B9 | Stage D.1 (live adapter, statement reconciliation) | moot at this stake | administrative | 2026-08-25 (progress.md:53-54) | reconciliation stub status `awaiting_broker_statement` (refusals.md:311-319) | Amendment 1 (REGISTRATION.md:273-274) | implicit: A2 / A3 | no |
| B10 | Billing-plan sub-test: Tiered vs Fixed on a real SmartRouted paper fill | **RUNNABLE, unscheduled** | open | — | the documentation contradicts itself; only a fill settles it (ACCESS.md:199; DECISIONS.md:466-468) | none — "gateway reachable and account pinned" (ACCESS.md:199); safety constraints per ADR-018 (DECISIONS.md:470-476) | "whenever an equity leg is next proposed" (progress.md:268-271) | **YES** — any repository in the program proposing an IBKR equity leg meets the trigger. See lead L5 |
| B11 | Alpaca eligibility recheck | **trigger met 2026-08-25, recheck not recorded** | — | — | trigger: "Recheck at stage C if Task 3 resolves badly" (ACCESS.md:19-20); Task 3 resolved badly 2026-08-25 (REGISTRATION.md:297-304); n = 0 rechecks recorded across the four post-trigger entries (AUDIT-A-HFExperiment-4). Cited primary source no longer carries the quoted text (fetched 2026-09-03T04:58Z, UNANCHORED) | — | the same clause (ACCESS.md:19-20), plus DECISIONS.md:427-429 | **YES** — any repository using Alpaca from Canada. See lead L4 |

---

## C. Deferred parameters (Amendment 1, never landed)

| # | Parameter | Status | Stated blocker — file:line | Note |
|---|---|---|---|---|
| C1 | `per_name_notional_usd` | DEFERRED; Amendment 1 never landed (REGISTRATION.md:293-295) | "the billing regime of a mixed integer-plus-fraction order decides it and only a paper fill measures that" (src/hfexperiment/registered.py:110-115; REGISTRATION.md:136-145) | mixed orders are refused at validation by error 10243, so the sub-test is MOOT (ACCESS.md:200). The reason string surfaces verbatim in gate output (refusals.md:11-17) |
| C2 | `broker_min_notional_usd` | DEFERRED | "MinSize and SizeIncrement come from reqContractDetails on a live-permissioned account that does not exist yet" (registered.py:116-121) | **STALE**: measured 0.0001 on all 20 names on 2026-08-25 (a1b_report.md:14-35; evidence.jsonl:3-22; ACCESS.md:196) and the account exists (ACCESS.md:187-189). ADR-026 corrected two documents "and no code" (progress.md:228-229). See AUDIT-A-HFExperiment-5 |
| C3 | `mixed_order_billing_regime` | DEFERRED | "whether a mixed integer-plus-fraction order bills whole on the fractional schedule is not determinable from IBKR's page" (registered.py:122-127) | MOOT on this channel (ACCESS.md:200); would be settled by the B10 sub-test on a different order shape |

---

## D. Kill criteria and gate (registered, never armed live)

| # | Entry | Status | Deciding figure (n) — file:line | Reopen / change condition — file:line |
|---|---|---|---|---|
| D1 | Restart floor of 500 USD account equity (Section 9; ADR-011) | registered, never armed | 1.31 sigma of 42.54 pct TE on 900 deployed, driftless one-year touch ~19 pct; 600 floor ~30 pct; 400 floor ~12 pct (n = 3 floors) (REGISTRATION.md:215-222; DECISIONS.md:173-179; registered.py:53-56) | "a measured book beta would refine the touch probabilities. The floor level itself changes only by amendment before the first live order" (DECISIONS.md:188-190) |
| D2 | Four terminations (Section 9) | registered, never armed | REGISTRATION.md:230-235 | — |
| D3 | Spend cap of 100 USD per rolling 365 days (Section 8) | registered, demonstrated in C.1 | 1.75x worst-case fractional projection of 56.84 USD/yr (REGISTRATION.md:196-198; cost_table.md:29; registered.py:57-59) | "A measured billing regime halves the projection under Tiered and the cap stays as a guard" (DECISIONS.md:217-219) — depends on B10 |
| D4 | Eight gate refusals including the account pin (Section 8; ADR-018/020) | registered, demonstrated | 34 refusal records in the demo ledger (refusals.md:339) | ADR-018 scoped username (DECISIONS.md:334-336); "may add refusals by amendment, never remove one" (REGISTRATION.md:204-205) |

---

## E. Verdict schedule (Section 11)

| # | Entry | Status | Deciding figure — file:line | Recomputed (AUDIT-A-HFExperiment-3) | Change condition |
|---|---|---|---|---|---|
| E1 | Success bar: lower bound above 4.07 bp/day; alpha 0.05 one-sided at width 5, 0.025 at widths 20 and 50 | registered, **never evaluated** (0 observations) | REGISTRATION.md:246-252; registered.py:62-78 | at true mean 27.99: day 2,852 (reproduces the registration exactly); at 15.10: day 15,060; at 10.04 with sigma 199.7 and alpha 0.025 (width 50): day 13,178 | ADR-010: "an amendment before the shadow series starts. Nothing after" (DECISIONS.md:169) |
| E2 | Futility bar: upper bound below 10 bp/day | registered, **never evaluated** | REGISTRATION.md:251-252; registered.py:70 | at true mean 0: day 18,650 (74.0 trading years); at 4.07: day 58,309; futility precedes success for every true mean below 7.035 bp/day | **no derivation of the 10 bp bar is recorded anywhere** — `grep -rn "futility"` over all `.md` returns n = 1 hit, the bar itself |
| E3 | rho frozen at 0.071641, crossing target 1,600 days | registered | REGISTRATION.md:247-248; registered.py:69,91 | reproduces | — |

---

## F. ADR "Changes it" clauses not covered above

| ADR | Clause — file:line | Status |
|---|---|---|
| ADR-001 | "nothing at this stage. This is the design's spine." (DECISIONS.md:18) | the design closed with the experiment |
| ADR-002 | "nothing. A later stage that couples the shadow series to a broker dependency violates this ADR." (DECISIONS.md:28-29) | **the closure did exactly this** — see AUDIT-A-HFExperiment-1 |
| ADR-003 | "the Task 3 test resolves GO or DEGRADED. An Alpaca Canadian launch would reopen the table." (DECISIONS.md:65-66) | the Task 3 result was labelled BLOCKED instead — see AUDIT-A-HFExperiment-2; superseded note at DECISIONS.md:47-55 |
| ADR-004 | "Amendment 1, if Task 3 forces whole-share sizing." (DECISIONS.md:85) | Amendment 1 never landed; superseded by ADR-008/010 |
| ADR-008 | "any design change that lets live data feed the verdict" (DECISIONS.md:138-139) | n/a — no live data ever existed |
| ADR-014 | "nothing. An acceptance is a fact about a date." (DECISIONS.md:242) | — |
| ADR-022 | "IBKR shipping fractional support in the TWS API, or an Alpaca Canadian launch per ADR-003" (DECISIONS.md:427-429) | open external reopeners for A2 |
| ADR-026 | "nothing about the verdicts. A future measurement supersedes a measurement." (DECISIONS.md:478-479) | — |
| ADR-023 / -024 / -025 | absent from the tree and from all history (`git log --all --oneline -S` returns 0 commits each) | numbering gap only |

---

## Leads for the cross-repository pass

Every blocker or reopen condition above that might be satisfied by work in another repository, with
a best guess at which one. Repository guesses are **guesses**, made from the program's repository
list and this repository's own citations; only L1-L3 name a repository the record itself names.

**L1 — The entire effect-size basis of H-F is imported and unverifiable here.** The 27.99 bp/day,
TE 66.40 pct/yr and IR 1.062 (width 5), and 10.04 / 31.70 / 0.798 (width 50), come from the AiTrader
cross-sectional round of 2026-07-26 (README.md:3-5; REGISTRATION.md:110-118). Their n, their
confidence interval and their holdout status are nowhere in this repository. Every day-count in the
verdict schedule (2,061; 2,852) is conditional on them.
*Best guess:* **AiTrader**. Ask there: what n and what interval produced 27.99 bp/day at width 5, and
was the holdout already spent (REGISTRATION.md:60-61 says it was)?

**L2 — Four registered reopen conditions point at AiTrader artefacts.** ADR-005 "a full-pool refresh
with a recorded new pull end" (DECISIONS.md:95); ADR-006 "If the recorded round's formation code ever
enters scope and differs, the reproduction reruns" (DECISIONS.md:112-114); ADR-009 "recorded
measurements at more widths would replace the two-point fit" (DECISIONS.md:157-158); ADR-017
"evidence that the recorded round handled a missing member differently, which must be reported and
corrected before 2026-09-01" (DECISIONS.md:283-285). All four concern AiTrader's database pull end,
formation code, recorded widths and benchmark member handling (DECISIONS.md:89-93,99-101).
*Best guess:* **AiTrader**. Any of the four, if satisfied there, reopens a closed HFExperiment item.

**L3 — H-F's first closure, "resolved on statistical power rather than absent signal."**
README.md:3-5 records that H-F was already closed once, in AiTrader, on power. HFExperiment is
therefore the second non-evidential closure of the same hypothesis. Whether the first closure's power
analysis was itself sound is a direction-A question that only AiTrader can answer, and the two
closures together are the strongest cross-repository instance of the thesis.
*Best guess:* **AiTrader**.

**L4 — Broker facts: Alpaca Canadian eligibility, and IBKR fractional support through the API.**
The A2/B11 reopeners are "an Alpaca Canadian launch" and "IBKR shipping fractional support in the TWS
API" (DECISIONS.md:427-429), and the ACCESS.md:19-20 recheck trigger fired and was never executed
(AUDIT-A-HFExperiment-4). Any repository in the program that trades or paper-trades US equities from
Canada through a broker API may hold a dated observation of either fact.
*Best guess, in order:* **ORBExperiment** and **ETFExperiment** (US-equity strategies most likely to
carry a live broker channel), then **AiTrader** (the equity universe and its data keys), then
**InsiderExperiment** and **NPDExperiment**. **MLCryptoEngine** may hold Alpaca credentials under the
crypto eligibility regime, which is a different table and would not settle the equity question.

**L5 — The runnable IBKR billing-plan sub-test (B10) triggers program-wide.** "It resolves a
documentation contradiction cheaply whenever an equity leg is next proposed" (progress.md:268-271).
This is an open, cheap, unblocked measurement whose trigger is any equity leg anywhere in the
program, and it also feeds D3's spend-cap projection (DECISIONS.md:217-219).
*Best guess:* **ORBExperiment**, **ETFExperiment**, **AiTrader** — whichever next proposes an IBKR
equity leg.

**L6 — Does the same verdict-schedule construction appear elsewhere, and does it carry the same
defect?** The futility bar sits above the success hurdle here (E2; AUDIT-A-HFExperiment-3), so a true
positive effect between 4.07 and 7.03 bp/day is classified FUTILE before it can be classified
SUCCESS, and a negative is unreachable at 74 trading years. If sibling registrations reuse this
studentized-asymptotic-confidence-sequence template with a similarly ungrounded futility bar, the
same over-closure mechanism propagates.
*Best guess:* the other registered-experiment repositories — **NPLExperiment**, **VRPExperiment**,
**ORBExperiment**, **PMExperiment**, **NPDExperiment**, **ETFExperiment**, **InsiderExperiment**.
Check for `futility`, `acs_radius`, `rho`, `crossing_target_days` and for a registered prior phrased
like "A documented negative is a valid outcome" (REGISTRATION.md:279-280).

**L7 — Stage B.2's registration is not in this repository.** "B.2 registered and unrun"
(progress.md:18) with n = 1 occurrence in the tree and n = 1 commit in all history
(AUDIT-A-HFExperiment-7); ADR-002 points at an external "stage prompt" (DECISIONS.md:22-23) that was
never copied in. If the program keeps stage prompts centrally, or if a sibling repository copied its
own stage prompt into its tree, B.2's content and reopen conditions may be recoverable there.
*Best guess:* any sibling `*Experiment` repository that stores its stage prompt in-tree — try
**NPLExperiment** and **VRPExperiment** first as the most recently developed, then **ORBExperiment**.

**L8 — A beta- or sector-hedged residual endpoint was never considered.** `grep "beta"` finds only
the kill-floor use (REGISTRATION.md:219-223; DECISIONS.md:175-190). The registered book is described
by the authors as "four correlated sector bets" (REGISTRATION.md:126-128) at 418 bp/day noise; a
hedged residual would plausibly cut that noise and shorten the 2,852-day clock materially, but
nothing here quantifies it, so no finding was made (see "found sound", item 9).
*Best guess:* **AiTrader** (it holds the cross-sectional round and the universe), secondarily any
repository that already computes sector or factor betas on a US equity universe — **ETFExperiment**,
**ORBExperiment**.

**L9 — The registered prior 0.15 and its provenance.** A4 records the prior as drafted by the session
and confirmed by the operator (REGISTRATION.md:276-278,289; DECISIONS.md:221-227), with no stated
basis. If sibling repositories register priors on related hypotheses, their consistency (or their
identical boilerplate) is a cross-repository check.
*Best guess:* all `*Experiment` repositories.
