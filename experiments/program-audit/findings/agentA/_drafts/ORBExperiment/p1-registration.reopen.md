# REOPEN LEDGER — ORBExperiment, part p1-registration

**Repository:** ORBExperiment · **anchored SHA:** `f2aa675a80fc06b74979040b3028154d1add5ec0` (main, 2026-08-29 20:46:22 -0700; live HEAD equals the anchor, clean tree, checked 2026-09-04).
**Documents covered:** `REGISTRATION.md`, `HYPOTHESES.md`, `report.md`. Entries whose primary record lives in `DECISIONS.md`, `progress.md`, `docs/ACCESS.md` or `docs/HANDOVER.md` are cross-referenced but belong to the other readers of this repository.
**This ledger is factual, not advocacy.** Every cell is a quotation or a direct read; where a field is genuinely absent the cell says **NONE REGISTERED** rather than inferring one.

## Index

| # | entry | status | closure kind | closure date | possibly met/affected by another repository? |
|---|---|---|---|---|---|
| 1 | **H1 — H-ORB** | CLOSED | `cost-bound` | 2026-08-30 | yes — see notes |
| 2 | **H1b — H-ORB with a raised price floor** | REGISTERED_NOT_OPEN | — | registered 2026-08-30 | no |
| 3 | **H2 — pre-FOMC drift** | PARKED | — | parked 2026-08-29 | no |
| 4 | **H3 — VIX term-structure roll yield** | PARKED | — | parked 2026-08-29 | no |
| 5 | cull 1 — index-ETF opening-range breakout (QQQ/TQQQ) | CLOSED before opening | not typed | at registration, 2026-08-28/29 | **yes** |
| 6 | cull 2 — CME Bitcoin weekend gap fill | CLOSED before opening | not typed | at registration | no |
| 7 | cull 3 — S&P addition / Russell reconstitution | CLOSED before opening | not typed | at registration | no |
| 8 | cull 4 — turn-of-the-month | CLOSED before opening | not typed | at registration | no |
| 9 | cull 5 — short-term reversal | CLOSED before opening | not typed | at registration | no |
| 10 | cull 6 — post-earnings announcement drift | CLOSED before opening | not typed | at registration | no |
| 11 | cull 7 — prediction-market mispricing | CLOSED before opening | not typed | at registration | **yes** (PMExperiment) |
| 12 | cull 8 — perpetual funding carry | CLOSED before opening | not typed | at registration | no |
| 13 | cull 9 — new Hyperliquid listing drift | CLOSED before opening, **DUPLICATE** | not typed here | at registration | **yes** (NPLExperiment) |
| 14 | cull 10 — spot Bitcoin ETF flow | CLOSED before opening, **DUPLICATE** | not typed here | at registration | **yes** (ETFExperiment) |
| 15 | Section 0 verdict (the outcome map) | PENDING_REVISION, re-fired 4× | n/a | last fired 2026-08-30 | no |
| 16 | bar-revision measurement (A.1 TASK 3) | BLOCKED on a calendar | n/a | due 2026-09-12 | no |
| 17 | cross-vendor agreement share (A.1 TASK 4) | ABSENT, scope-narrowed | n/a | — | no |
| 18 | SL-1 / SL-2 / SL-3 (scope limitations) | REGISTERED, unretired | n/a | 2026-08-29 | **yes** for SL-1 and SL-3 |

---

## 1. H1 — H-ORB (the opening-range breakout on relative-volume-selected names)

- **Statement:** "Among US common stocks with elevated opening relative volume, a breakout of the first 5-minute regular-session range predicts continuation to the session close, net of modeled costs, out of sample from 2023-01-03." — HYPOTHESES.md:52-54; restated as a direction rule at REGISTRATION.md:233.
- **Status:** **CLOSED** — HYPOTHESES.md:50, 58.
- **Closure kind:** `cost-bound` — HYPOTHESES.md:50, 58; REGISTRATION.md:4142-4143; report.md:1003-1004.
- **Closure date:** **2026-08-30** (A.3 rescue pass TASK 5, Amendment 28) — HYPOTHESES.md:58; REGISTRATION.md:4066-4069. Commit `34a91b3`, authored 2026-08-29 20:43:15 −0700 = 2026-08-30 03:43 UTC.
- **Deciding figures, with n and file:line:**
  - measured slippage **shift 0.467065 USD/share** against a required "strictly below **0.040386**", exceeded by **11.56×** — REGISTRATION.md:4081-4083; criterion at REGISTRATION.md:3711-3712.
  - pessimistic-cost mean **−0.426679 USD/share** at the registered 1.40 assumption, n = 875 holdout sessions / 17,188 implied trades — REGISTRATION.md:4084-4085, 4097.
  - **E2 power 0.000000**, **JOINT power 0.000000**, minimum n "none" at every assumption — REGISTRATION.md:4093-4100.
  - band inputs: entry central **0.087019** / pessimistic **0.354645**, n = **550**; stop central **0.033529** / pessimistic **0.198061**, n = **210**; close central **0.040000** / pessimistic **0.261000**, n = **340** — REGISTRATION.md:3975-3980, 3990-3996.
  - dispersion **2.029585 USD/share**, n = **550 priced trades** — REGISTRATION.md:2631-2633.
  - stop-exit share **0.381818**, n = **550** (210 stop / 340 close) — REGISTRATION.md:3274.
  - trigger rate **0.982143**, n = **560 selected name-sessions** over **28 evaluable sessions** — REGISTRATION.md:2639-2640.
  - E1 power **0.832450** at 1.40 on n = 875, min n **795** — **unchanged by the closure and still above its bar** — REGISTRATION.md:3081, 4097.
  - superseded deciding figure (carried band): pessimistic-cost mean **−0.001068**, E2 power **0.043277**, break-even Sharpe **1.437035**, registered 1.40 sits **2.577 percent** below it — REGISTRATION.md:3360-3365, 3419-3422.
- **Sample the deciding figures were measured on:** 42 post-holdout sessions 2026-07-01 to 2026-08-28, **28 evaluable**, **200 tickers** — a 1-in-26 systematic sample of a 5,317-name listing; mean relative volume of the selection **2.0652** — REGISTRATION.md:3966-3967, 2570-2573, 3873.
- **Stated blockers, with file:line:**
  1. **No execution evidence / no broker credential.** "This repository holds none, has no broker credential, and none is planned." — REGISTRATION.md:4156; also REGISTRATION.md:3466-3467, HYPOTHESES.md:62. Credentials held are Alpaca **paper-account** keys; the live trading host refuses them (401) — docs/HANDOVER.md:31-34.
  2. **One-minute resolution.** "457 of 550 entry triggers and 195 of 210 stop triggers crossed their boundary INTRABAR, and one-minute data cannot locate the first trade through a boundary inside a bar" — REGISTRATION.md:4042-4044; same limit for the floor scan at REGISTRATION.md:3920-3927.
  3. **Market impact unmeasured.** "Market impact is not measured at all and is a further addition." — REGISTRATION.md:4048.
  4. **Post-holdout regime for every E2 input.** "may misstate in-sample dispersion in either direction by an amount this repository has not measured and does not claim to bound" — REGISTRATION.md:2083-2088; carried to every E2 figure at REGISTRATION.md:2681-2684, 3390-3392.
  5. **No further rescue lever, by pre-commitment.** "Stage A.3 applies **one** lever to H1 ... and **no further rescue lever is applied afterwards.**" — REGISTRATION.md:3679-3682; "`GO` is unreachable and is not a tier." — REGISTRATION.md:3720.
  6. **Spend.** "Zero dollars in Stage A. Free and trial tiers only." and "Any paid tier requires an explicit operator instruction and its own ADR." — REGISTRATION.md:723, 739.
  7. **Power that cannot accrue.** "the 875 sessions are historical and no further accrual is possible inside the registered window ... This registration does not extend it" — REGISTRATION.md:1168-1174.
- **Registered reopen conditions, with file:line:** **NONE REGISTERED IN `HYPOTHESES.md`.** The register's own rule requires one — "A closed entry carries the figure that closed it, with its n, and states what would reopen it — or states that nothing would." HYPOTHESES.md:7-9 — and H1's 30-row entry (HYPOTHESES.md:56-87) contains no such row and no statement that nothing would reopen it. See draft finding DRAFT-p1-registration-6.
  - The nearest thing inside my documents is prose, not a condition: "**The honest attack is (2): real execution evidence could narrow the band.**" — HYPOTHESES.md:62; REGISTRATION.md:4154-4155; report.md:1012-1015. And "Amendment 21's route (b) — narrowing the band on measured execution evidence — is unaffected and **remains open to the operator**" — REGISTRATION.md:4060-4062.
  - Stated as a reopen route only outside my documents: "**(d) Pursue Amendment 21 route (b)** — narrow the registered cost band on **real execution evidence**. ... **It is the only route that could reopen a cost-bound closure**" — docs/HANDOVER.md:272-275 *(primary evidence outside my assignment)*.
- **Reopen triggers already met?** No registered trigger exists to be met. Of the un-registered routes: route (b)'s blocker is unlifted in the repository's own terms, but see DRAFT-p1-registration-9 — the held tier serves historical NBBO quotes (760 minutes, 0 refused, REGISTRATION.md:3967-3969) and the trade-print endpoint on the same host and version prefix was never probed.
- **Possibly met/affected by another repository:** **yes, for the cross-repo pass.**
  - The `cost-bound` kind's precedent is **MLCryptoEngine H6** ("per-fill positive, negative under an order-lifecycle fill model", HYPOTHESES.md:36); that precedent rests on a measured PnL and this closure has none. Whether the house record's use of the kind is consistent is a cross-repo question.
  - The alternative kind named by Amendment 21 route 3 is `untestable-at-achievable-power`, whose precedent is **InsiderExperiment** (HYPOTHESES.md:39, REGISTRATION.md:3468-3474).
  - The carried figures that set the whole cost frame (C-5, C-6, C-13) are external; **C-6's QQQ band was measured 4.35× low on single names here** (REGISTRATION.md:3975), which is a measured fact that bears on any other repository carrying the same QQQ-derived slippage assumption — check **ETFExperiment** and any repo carrying C-6.
  - The carried house figures C-17 (HFExperiment `reports/stage_a1b/a1b_report.md` line 52), C-19 (MLCryptoEngine H11), C-20 (NPLExperiment), C-21 (solattn ADR-021) are re-quotations of other repositories' measurements and should be checked against their sources — REGISTRATION.md:887-891.

## 2. H1b — H-ORB with a raised price floor

- **Statement:** HYPOTHESES.md:93-96.
- **Status:** **`REGISTERED_NOT_OPEN`** — HYPOTHESES.md:100; REGISTRATION.md:3760-3764, 3934-3935.
- **Closure kind / date:** none — it is registered, not closed. Registered **2026-08-30** (Amendment 25).
- **Deciding figures:** none; the pass produced a feasibility scan only. Scan table, post-holdout carve-out, n = 42 sessions / 28 evaluable / 200 tickers — REGISTRATION.md:3871-3877. Central-mean-to-shift ratio rises **0.9742 → 0.9983 → 1.1415 → 1.4767 → 2.1424** across floors 5/10/20/50/100; mean relvol of the selection falls **2.0652 → 1.4103**; dispersion rises **2.0296 → 3.1992**.
- **Blockers, with file:line:**
  1. "**Its own full registration** ... **its own power gate**, computed rather than inherited ... **explicit operator instruction**. **None of the three exists.**" — HYPOTHESES.md:106; REGISTRATION.md:3830-3837.
  2. "**H1b increments the Section 8 deflated-Sharpe trial count from 8 to 9**" — REGISTRATION.md:3818-3819; HYPOTHESES.md:105.
  3. The scan's price floors above 20 USD cannot be read as facts about the registered universe: "the scan sample thins out there, and the scan cannot establish what the registered universe does. Establishing that needs a full-universe pull at those floors, which **this pass did not do and does not authorise.**" — REGISTRATION.md:3911-3914.
  4. The scan's own invariance check is a resolution limit: "**The entry overshoot is 0.0000 at every floor, and that is a resolution limit** ... **Not a measurement that overshoot is zero.**" — REGISTRATION.md:3920-3927.
  5. It inherits the closure's problem: the measured entry half spread of 0.076572 median "is what killed H1, and a raised floor improves the ratio only if the spread does not scale with price — which the scan's overshoot column **cannot** confirm at one-minute resolution." — docs/HANDOVER.md:268-271 *(outside my assignment)*.
- **Registered opening conditions (the analogue of a reopen condition):** the three at HYPOTHESES.md:106 / REGISTRATION.md:3832-3837.
- **Triggers already met?** No. **Note for the cross-repo pass and for the H1 record:** the scan's `shift` column is the **registered (carried)** band's shift at each floor's own stop-exit share, not the measured band's — REGISTRATION.md:3871-3877 and the tool's own note in `reports/stage_a3rescue/task4_floor_scan.json` (`comparison_figure_note`). The claim "the shift stays within a **4 percent band, 0.039967 to 0.041782**, which is the price-invariance the mechanism asserted, measured rather than assumed" (REGISTRATION.md:3886-3888) is a property of a band held fixed by construction, and the ratio crossing 1.0 between the 10 and 20 USD floors (REGISTRATION.md:3896-3899) does not survive substituting the measured shift of 0.467065. This is recorded here as a factual observation for whoever picks up H1b; it is not one of my draft findings because it points against the hypothesis rather than for it.
- **Possibly met by another repository:** no.

## 3. H2 — pre-FOMC drift

- **Statement:** "Equity index returns are systematically positive in the window before a scheduled FOMC announcement." — HYPOTHESES.md:148-149.
- **Status:** **PARKED**, 2026-08-29 — HYPOTHESES.md:151. "Not closed, not refuted, not tested."
- **Closure kind / date / deciding figure:** none — HYPOTHESES.md:151-154.
- **Blocker, with file:line:** "**No second repository opens while H1 is unresolved.** That was the reason, and it was the only reason." — HYPOTHESES.md:137-138; and "Opening it now would split attention across two registrations and put two hypotheses under one unbudgeted familywise error rate." — HYPOTHESES.md:153-154.
- **Reopen condition, with file:line:** implicitly the resolution of H1 (HYPOTHESES.md:137-138). **The trigger has been met and the register says so:** "**H1 closed `cost-bound` on 2026-08-30** (Amendment 28), so the condition that parked these two no longer holds. **They are not thereby opened**: each still needs its own registration, its own power gate and explicit operator instruction, and **none of the three exists for either.**" — HYPOTHESES.md:140-144. So this is a reopen trigger that **has fired**, was **noticed**, and was **replaced by three new preconditions** — recorded here because it is exactly the pattern the cross-repo pass is looking for, and here it is handled correctly.
- **Possibly met by another repository:** no.

## 4. H3 — VIX term-structure roll yield

- **Statement:** "The slope of the VIX futures term structure predicts the return to a short volatility position by enough to clear costs." — HYPOTHESES.md:158-159.
- **Status:** **PARKED**, 2026-08-29 — HYPOTHESES.md:161.
- **Closure kind / date / deciding figure:** none.
- **Blocker, with file:line:** same as H2 — HYPOTHESES.md:137-138, 161-163 ("Same reason. It shares no substrate with H1 at all, which makes it a genuinely separate repository rather than a variant, and that is another reason not to open it here.").
- **Reopen condition:** same as H2; **trigger met on 2026-08-30 and acknowledged at HYPOTHESES.md:140-144**, with the same three replacement preconditions.
- **Possibly met by another repository:** no.

## 5–14. The ten candidates culled at registration

All ten share: **status CLOSED before opening; closure kind NOT TYPED** (the five-kind taxonomy at HYPOTHESES.md:34-40 was not applied to any of them); **closure date = at registration** (the register was first committed 2026-08-28/29 and the culls carry no individual date); **deciding figure = none measured by this repository** — "Each was considered as an alternative to H1 and closed **before any data existed**, with a one-line reason. **None was closed on a measurement**, and none of them is reopened by anything H1 does." — HYPOTHESES.md:116-118. **No reopen condition is registered for any of the ten.**

| # | candidate | stated reason (file:line) | figures carried into the reason | possibly met/affected elsewhere |
|---|---|---|---|---|
| 5 | index-ETF opening-range breakout (QQQ/TQQQ) | HYPOTHESES.md:122; ADR-013; also REGISTRATION.md:255-256, 613 | replication 1,775 trades vs 1,795, gross Sharpe 1.06; gross edge 0.070 USD/share; net PnL crosses zero at ~0.022 against a QQQ spread near 0.010 (carried, C-5/C-6, REGISTRATION.md:875-876) | **yes** — this repository has since **measured** that the QQQ-derived band understates single-name entry slippage 4.35× central and 8.87× pessimistic (REGISTRATION.md:3975-3976), i.e. the measured entry half spread on single names is **0.076572 median** (REGISTRATION.md:3991) against the carried QQQ spread near **0.010**. The cull's own logic — that the ETF variant's edge sits inside its spread — now has a measured single-name comparator that runs the other way. Flag for **ETFExperiment** and for anyone carrying C-6. |
| 6 | CME Bitcoin weekend gap fill | HYPOTHESES.md:123 | none | no |
| 7 | S&P addition / Russell reconstitution | HYPOTHESES.md:124 | none — "power at achievable N fails before costs are modeled" is asserted, not computed | no |
| 8 | turn-of-the-month | HYPOTHESES.md:125 | McLean–Pontiff decay (carried, C-12) | no |
| 9 | short-term reversal | HYPOTHESES.md:126 | this repo's own 25 percent borrow exclusion (REGISTRATION.md:277-280) | no |
| 10 | post-earnings announcement drift | HYPOTHESES.md:127 | none | no |
| 11 | prediction-market mispricing | HYPOTHESES.md:128 | none | **yes** — "Different venue, different cost structure, no shared substrate" is a substrate claim, not a finding; **PMExperiment** is a closed project in the audit set and should be checked for whether it holds a measured answer this cull would have wanted. |
| 12 | perpetual funding carry | HYPOTHESES.md:129 | none | no |
| 13 | new Hyperliquid listing drift | HYPOTHESES.md:130 | **DUPLICATE** — closed as H1 in **NPLExperiment** 2026-08-28, FAIL on the sealed read, 197/312 positive, exact lower bound 0.5707 against a 0.60 bar; "Its live successors H2, H3, H4 are registered there." | **yes** — check NPLExperiment's H1 record and whether H2/H3/H4 are still live at that repository's anchor (2026-09-02). |
| 14 | spot Bitcoin ETF flow | HYPOTHESES.md:131 | **DUPLICATE** — "Registered and running in **ETFExperiment** as H-ETF." | **yes** — check whether H-ETF is still running at ETFExperiment's anchor (2026-08-28); if it has closed, this repository's cull reason is stale in a way no entry here records. |

## 15. The Section 0 outcome map (verdict state)

- **Status:** **`PENDING_REVISION`**, clause `PENDING-REVISION Amendment 10`, fired four times — Amendment 10 (REGISTRATION.md:1935-1941), Amendment 16 (REGISTRATION.md:2759-2762), Amendment 23 (REGISTRATION.md:3590-3593), and again at A.3 TASK 5 on 2026-08-30 (HYPOTHESES.md:65).
- **Superseded state:** `PENDING_ACCESS` (Amendment 4, REGISTRATION.md:1113-1120), fired on 0 of 9 vendors serving a bar, n = 15 robots fetches and n = 25 API probes.
- **Deciding figures with n:** E1 power at the published 2.81 = **0.999835** against the 0.50 BLOCKED-1 floor, n = 875 (REGISTRATION.md:3616); delisted names with intraday history **203**, n = **229** checked → `PASS` against a bar of 100 (REGISTRATION.md:3629); bar revision **`Absent(not_yet_measured)`** and agreement share **`Absent(not_yet_measured)`** (REGISTRATION.md:3630-3631).
- **Blockers:** the two absent integrity inputs; earliest eligible re-pull **2026-09-12** (REGISTRATION.md:1965).
- **Reopen / re-fire condition:** both integrity inputs present. Explicitly recorded: "**`GO` and `DEGRADED` would still be unreachable**, because both require the co-primaries at power and **joint power is 0.000000**." — docs/HANDOVER.md:149-151 *(outside my assignment)*.
- **Recorded but not acted on:** "**Had BLOCKED-1 been defined on JOINT power at the registered assumption, it would fire** — that figure is 0.043277, an order of magnitude below the floor." — REGISTRATION.md:3644-3645. The branch was not changed (REGISTRATION.md:3647-3651).
- **Possibly met by another repository:** no.

## 16. The bar-revision measurement (A.1 TASK 3)

- **Status:** **BLOCKED on a calendar**, not on a design question — "> ## **2026-09-12.**" REGISTRATION.md:2925-2934.
- **Deciding figure:** none yet. Registered thresholds: `PASS` at a changed-bar share at or below **0.005**; `PARTIAL` above that to **0.020**; `FAIL` above 0.020, firing BLOCKED-2 — REGISTRATION.md:99, 108-111.
- **Blocker with file:line:** the registered 14-calendar-day wait between the probe pull and its identical re-pull; `orb.repull.require_due` refuses every earlier attempt with exit 78 — REGISTRATION.md:2929-2934, 1962-1965.
- **Reopen / unblock condition:** the arrival of **2026-09-12**. **As of this audit (2026-09-04) the trigger has NOT been met** — it is 8 days away. The blocker is live, not expired.
- **Consequence recorded:** the closure does not wait for it — "**It does not change the 2026-09-12 re-pull date**, which now governs a repository whose primary hypothesis is closed." — REGISTRATION.md:4192-4193; "H1 closed on cost before it arrived." — report.md:1080.
- **Possibly met by another repository:** no.

## 17. The cross-vendor agreement share (A.1 TASK 4)

- **Status:** **ABSENT**, and scope-narrowed by amendment before any number existed.
- **Deciding figure:** none. Registered thresholds `PASS ≥ 0.95`, `PARTIAL ≥ 0.85`, `FAIL` below, firing BLOCKED-4 — REGISTRATION.md:101, 113-116.
- **Blockers with file:line:** the two feeds overlap only from 2024-08-29 — **459 of 875 holdout and 0 of 1,762 in-sample sessions** — REGISTRATION.md:1661-1675; and the pair "scores a redistribution pipeline, not two independent feeds" (SL-1, REGISTRATION.md:1554-1558, 630-634).
- **Reopen / unblock condition:** a third feed on a genuinely different upstream (REGISTRATION.md:1567-1572), or a paid reference tier whose reach extends (REGISTRATION.md:1691-1711).
- **STALE-FIGURE NOTE (drifts with real time, not marked as drifting):** Massive's free tier is "a rolling window of exactly 24 months, measured to the day" with earliest served session 2024-08-29 measured on 2026-08-29 — REGISTRATION.md:1624-1626. The **459 of 875** overlap therefore **shrinks by one session for every session that passes**; by the audit date (2026-09-04) roughly four sessions of overlap have been lost since the measurement, and no document marks the figure as time-decaying. Recorded here for the cross-repo pass rather than raised as a finding.
- **Possibly met by another repository:** no, but see SL-1 below.

## 18. SL-1, SL-2, SL-3 — the registered scope limitations

| SL | statement | file:line | blocker | route(s) that would retire it | met? |
|---|---|---|---|---|---|
| **SL-1** | the two feeds share an upstream; ratio IQR 0.46 percentage points wide over n = 100 pairs; a PASS establishes only that two redistributors of one upstream agree, and "it is **not** the Concretum test" | REGISTRATION.md:630-634; 1541-1572 | no third feed held | a third feed on a genuinely different upstream (REGISTRATION.md:1567-1572; docs/HANDOVER.md:210-216) | **no** |
| **SL-2** | the two feeds overlap only from 2024-08-29; the agreement gate is narrowed to the overlap | REGISTRATION.md:635-636; 1666-1675 | measured vendor reach | a reference tier reaching earlier (REGISTRATION.md:1696-1711) | **no** |
| **SL-3** | "**All 1,762 in-sample sessions rest on a single unverified feed**", and "a PASS computed on the in-sample window is conditional on a single vendor's rendering of that window being faithful, and this repository holds no measurement supporting that condition" | REGISTRATION.md:640-680 (measurement table at 645-652; consequence at 668-674) | cost, and an unpurchased reference tier | **(1)** a reference credential whose tier reaches 2016-01-04 — "It costs money", requires explicit operator instruction and its own ADR, and "the reach a paid tier actually delivers is deliberately not recorded here as a number"; **(2)** explicit operator acceptance that the in-sample window is single-sourced — REGISTRATION.md:685-694 | **no** |

- **Exposure named for all three:** Concretum, "**226,000 to 726,000 USD** final equity from four vendors on identical opening-range code, dates, parameters and starting capital" (carried, C-13) — REGISTRATION.md:661-666, 883.
- **Possibly met by another repository:** **yes for SL-1 and SL-3** — any repository in the audit set holding a credential on a genuinely different upstream (or a paid tier reaching 2016) would retire one of these on measurement. The cross-repo pass should check **HFExperiment**, **AiTrader**, **MLCryptoEngine** and **ETFExperiment** for market-data entitlements this repository does not know about.

---

## Ledger notes for the cross-repository pass

1. **H1 has no registered reopen condition at all**, against its own register's stated rule (HYPOTHESES.md:7-9). The only route stated as a reopen route lives in `docs/HANDOVER.md`:272-275. Any cross-repo trigger therefore has nothing here to fire against.
2. **The closure's kind is contested by its own text.** `cost-bound` (HYPOTHESES.md:36, precedent MLCryptoEngine H6) vs `untestable-at-achievable-power` (HYPOTHESES.md:39, precedent InsiderExperiment), where the repository's own sentence is "It is a finding that this design cannot clear its own registered cost band" and "Nothing in this repository measured whether the directional edge is real" (REGISTRATION.md:4162, report.md:1020). The house-wide consistency of the five closure kinds is a cross-repo question.
3. **Two parked entries (H2, H3) have had their parking trigger fire and were correctly not opened** (HYPOTHESES.md:140-144). This is the pattern the cross-repo pass hunts for, handled well; record it as a positive control.
4. **Two culls are DUPLICATEs pointing at live repositories** (NPLExperiment H1 and successors; ETFExperiment H-ETF). Their cull reasons are statements about those repositories' current states and can go stale without anything here noticing.
5. **One measured fact here bears on another repository's registration**: the carried QQQ slippage band (C-6) was measured **4.35× low central and 8.87× low pessimistic** on single names (REGISTRATION.md:3975-3976). Any repository carrying C-6 or an ETF-derived slippage assumption onto single names is carrying a figure this repository has measured against.
6. **One blocker in this repository is live and unexpired at the audit date**: the 2026-09-12 bar-revision re-pull. It should not be reported as an expired blocker.
7. **One figure decays with real time and is not marked as decaying**: the 459-of-875 cross-vendor overlap, because Massive's free tier is a rolling 24-month window (REGISTRATION.md:1624-1626).
