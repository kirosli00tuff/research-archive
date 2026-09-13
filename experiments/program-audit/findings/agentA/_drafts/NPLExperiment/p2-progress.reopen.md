# REOPEN LEDGER — NPLExperiment, part "p2-progress"

Repository **NPLExperiment**, anchored SHA `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c` (main, 2026-09-02).
Live `HEAD` equals the anchor (verified 2026-09-04T23:13Z and 23:17Z), so nothing below has moved in git
since the anchor. Rows marked **LIVE** carry a figure measured from untracked machine-local data on
2026-09-04 (UNANCHORED).

This ledger is factual, not advocacy. Citations are `<path>:<line>` in the anchored snapshot. Entries
whose deciding text sits in the *other* reader's documents (`HYPOTHESES.md`, `REGISTRATION.md`,
`registrations/*`, `report.md`, `README.md`) are cited as such and marked ▲.

---

## 1. Entry-by-entry

### H1 — H-NPL, the naive new-listing short

| field | value |
|---|---|
| **Status** | CLOSED — NEGATIVE |
| **Closure kind** | Registered outcome-map row `FAIL`, fired mechanically from the Amendment 3 table |
| **Closure date** | 2026-08-28 (latch 03:01:01Z, read 03:01:08Z) — progress.md:501; reports/stage_b/read.json (`read_at`, `row_fired`) |
| **Deciding figure (n)** | P1 197/312 positive, Clopper–Pearson one-sided lower bound **0.5707** against the 0.60 bar — FAIL; P2 111/312 at ≤ −15 % net, sign-test p = **1.000** — FAIL; P3 114/175 pairs, p = **3.767e-05** — PASS. Effective N 312/312/175 against minimums 34/103/60 — progress.md:501-505; reports/stage_b/read.json (`co_primaries`) |
| **Sensitivity carried** | Cost-insensitive: P1 lower bound 0.5740 / 0.5707 / 0.5609 across the registered bands, n = 312 each — progress.md:482, 505; reports/stage_b/read.json (`secondaries.cost_band_sensitivity`) |
| **Secondary horizon (not verdict-bearing)** | 90-day: P1 208/312, lower bound **0.6069** (clears the 0.60 bar), P2 159/312 p = 0.3886, P3 111/175 p = 2.360e-04, n = 312 / 312 / 175 — reports/stage_b/read.json (`secondaries.horizon_90d_co_primaries`); also ▲ REGISTRATION.md:570-571 and ▲ report.md:233-235 |
| **Blockers, stated** | (1) Operator prior slot, Section 13 — blocked Stage B structurally; **spent**, filled 0.40 (adopted) at the read — progress.md:446-447. (2) Sealed-completeness and coverage preconditions — cleared 312/312 events, 175/176 controls at 30 d (NEIROETH excluded underpowered, counted) — progress.md:446-453. (3) Standing: "equities stay closed at this stake regardless (HFExperiment A.1b measured IBKR refusing fractional orders, error 10243)" — docs/STAGES.md:74 → **cross-repo** |
| **Registered reopen conditions** | ▲ HYPOTHESES.md:56 — "**Nothing reopens H1 itself** … The residual worth testing is precisely what P3 and the H8 decomposition measured … That residual is H2, H3, and H4". In my documents the equivalent statement is progress.md:517-519 — "**Open operator items: none.** The hypothesis is closed; any redesign (funding-conditioned, magnitude-recalibrated) is a new hypothesis requiring its own registration"; and docs/STAGES.md:71-72 — Stages C and D "Void with the FAIL row; never bound" |
| **Trigger already met?** | No trigger is registered, so none can be met. **Open observation** (raised as DRAFT-p2-progress-6): the 90-day horizon named in the hypothesis statement itself (progress.md:10; CLAUDE.md:8-10) has P1 clearing its bar and P3 clearing at p = 2.4e-04, and it is carried into none of H2/H3/H4/H5 |
| **Possibly met by another repo?** | **Yes, indirectly** — the standing equities note at docs/STAGES.md:74 rests on **HFExperiment** A.1b / ADR-026. If a later dated HFExperiment entry lifts the fractional-order refusal or the 40–100 bp whole-share cost, that note is stale |

### H2 — the age-contrast pair

| field | value |
|---|---|
| **Status** | OPEN — survivor of the cull, amended to a two-look sequential plan; collectors armed |
| **Closure kind** | None fired. Section 0 fired **DEGRADED** 2026-08-28 (Amendment H2-1); recomputed after Amendments H2-3/H2-4 to a single-look **GO** at 0.8886 governing power, with the DEGRADED record "not edited and not re-fired" — progress.md:941; reports/stage_a_h2/ktable_amended.json (`section0_gate_recomputed`) |
| **Closure date** | n/a (open). Section 0 DEGRADED: 2026-08-28, progress.md:685-690 |
| **Deciding figure (n)** | Cull pass 2 (k = 1, alpha_h = 0.05): E2 deadline power **0.7604** at n = 141 by-dex pairs, E1 0.9743 — progress.md:679, 685-690. After the amendment: 62/62 pairs achieved (38 same_dex + 24 cross_dex); look-1 min N **59** (E1 42, E2 59), look-2 min N **117** (E1 84, E2 117); at look-2 min N k₁ = 38, k₂ = 69, exact spend 0.0182 + 0.0240 = 0.0422; recomputed power 0.8886 single-look / 0.8629 two-look — progress.md:1057-1071; reports/stage_a_h2/ktable_amended.json (`minimum_n`, `two_look_at_deadline`) |
| **Registered dates** | Look 1 **2026-11-26** at 59 readable pairs; look 2 **2027-03-01** at 117; registered deadline **2027-03-31** — progress.md:1062-1065; ktable_amended.json (`projected_look_dates`) |
| **Blockers, stated** | (1) **The H2 operator prior slot, reserved and empty — blocks BOTH looks structurally** (`npl.register.priors`) — progress.md:1098-1103; ▲ README.md:80-85. (2) Look-1 entry gate: 59 readable eligible pairs **and** the prior slot **and** explicit operator instruction **and** `h2_look1_latch.json` absent — docs/STAGES.md:25. (3) Look-2 entry gate: the earlier of 2027-03-31 and 117 readable pairs, the prior slot, operator instruction, look 1's latch **present** and look 2's absent — docs/STAGES.md:26. (4) All four H2 latches confirmed absent at the last close-out — progress.md:1084-1087. (5) Registered futility boundary at n₁ = 59: E1 f₁ = 31, E2 f₁ = 27 at the 0.10 conditional-power floor — progress.md:1070-1071 |
| **Registered reopen / exit conditions** | Look-1 exit: GO (both cross k₁), FAIL (either crosses futility), or CONTINUE which fires no row and spends no further alpha — docs/STAGES.md:25. Look-2 exit: GO when both have rejected **by** look 2, FAIL otherwise; terminal either way; a GO authorizes drafting Stage C (paper software) and never capital — docs/STAGES.md:26; DECISIONS.md:368-374 (ADR-025's corrected rule). Futility "only on the registered boundary … never on inspection" — DECISIONS.md:350-352 |
| **Trigger already met?** | **No.** Look 1 is not due until 2026-11-26 and the prior slot is empty. Nothing registered fires on 2026-09-30 — the offered interim tripwire was explicitly omitted, with the reason recorded: progress.md:865-873 |
| **Possibly met by another repo?** | **Yes, for the assumptions rather than the trigger** — E1's 0.65 and E2's 0.625/0.60 descend from the generating sample and from **MLCryptoEngine** H8's funding/price cancellation carried in as an assumption at progress.md:32. A later MLCryptoEngine revision of the H8 figures would move H2's registered power assumptions, though not its bars |

### H3 — the population-corrected naive short

| field | value |
|---|---|
| **Status** | BLOCKED (closed; nothing armed) |
| **Closure kind** | Section 0 outcome-map row `BLOCKED`, fired by the outcome-blind A.2 cull (any required co-primary under 0.50 power at achievable N by 2027-03-31) — progress.md:679, 691-693 |
| **Closure date** | 2026-08-28 (Amendment H3-1) — progress.md:682-683 |
| **Deciding figure (n)** | Measured main-dex accrual **0.5 events/month (n = 3 listings in 182 days)**, falsifying the register prompt's ~9.4/month planning figure — docs/ACCESS.md:265-266. Achieved fresh main-dex N = 2, deadline N = **5**, against P1 minimum N **262** at alpha 0.05 (361 at the k = 3 alpha). Powers at the deadline: P1 **0.0000**; magnitude leg **0.0057** at the governing generating-sample share 0.356 (0.1160 at the optimistic H1-registered 0.65) — progress.md:691-693, 760-762; reports/stage_a_h2/ktable_cull.json (`k_table."k=3".scenarios."deadline_2027-03-31"`, `min_n_for_080."H3/P1"`, `min_n_for_080."H3/MAG"`) |
| **Recorded structural fact** | `min_n_for_080."H3/MAG"` = `null`, note "governing true share at or below the null: no n reaches 0.80" — reports/stage_a_h2/ktable_cull.json. Requirement mode "all", weaker leg governs (▲ registrations/H3/REGISTRATION.md:102-103) |
| **Blockers, stated** | (1) The measured main-dex listing rate itself — docs/ACCESS.md:265-266. (2) The magnitude leg's governing assumption 0.356, below the sign-test null — ▲ registrations/H3/REGISTRATION.md:87, 175-177. (3) H3 operator prior slot reserved and empty, "moot — both hypotheses are BLOCKED and neither has a Stage B to gate" — progress.md:1101-1103 |
| **Registered reopen conditions** | ▲ registrations/H3/REGISTRATION.md:184-188 — "a main-dex listing rate near **40–50/month** sustained (min-N 262 against 0.5/month measured), a register deadline years longer, or a successor registration on a **different venue** whose main-population listing rate supports the bars". ▲ HYPOTHESES.md:89 gives the same condition as "an **order-of-magnitude higher** main-dex listing rate or a longer-horizon successor registration" — the two disagree by a factor of ≈ 8 (raised as DRAFT-p2-progress-5). My documents carry no reopen condition for H3 |
| **Trigger already met?** | **No.** The measured rate is 0.5/month and no later entry in this repository revises it. Note that neither the 40–50/month clause nor the order-of-magnitude clause can reopen the **magnitude** leg, which reaches no power at any n |
| **Possibly met by another repo?** | **Yes, for the "different venue" clause** — any repository measuring a main-dex-equivalent listing population with a materially higher rate (candidates in the program: **MLCryptoEngine**, **AiTrader**, **ORBExperiment**) would satisfy the third clause of the registration's reopen condition. Flagged for the cross-repository pass |

### H4 — the funding-conditioned short

| field | value |
|---|---|
| **Status** | BLOCKED (closed; nothing armed) |
| **Closure kind** | Section 0 outcome-map row `BLOCKED`, fired by the same outcome-blind cull; requirement mode "any — the best cell governs" (▲ registrations/H4/REGISTRATION.md:119-121) |
| **Closure date** | 2026-08-28 (Amendment H4-2) — progress.md:682-683 |
| **Deciding figure (n)** | Measured conditioning rates **0.1774 / 0.1290 / 0.0806 (n = 62 fresh events, 0 absent trailing means)**; median trailing entry funding **+31.6 %/yr** (n = 62) — progress.md:677, 694-697; reports/stage_a_h2/ktable_cull.json (`inputs.conditioning_rates`). Deadline cell Ns **30 / 22 / 13**; best-cell deadline power **0.0140** at the governing generating-sample share 0.631, against 0.7106 at the declined optimistic 0.85 — progress.md:694-697, 763-766 |
| **Recorded structural fact** | `min_n_for_080."H4/le_-10pct_ann"` = `null`, note "not reached by n=1200; power at 1200 = 0.518" (k = 1) / "power at 1200 = 0.354" (k = 3) — reports/stage_a_h2/ktable_cull.json; ▲ registrations/H4/REGISTRATION.md:224-225 |
| **Blockers, stated** | (1) The measured rarity of deeply negative entry funding — progress.md:694-697. (2) The governing power assumption (unconditional 0.631), registered by ADR-017 before the numbers existed — DECISIONS.md:202-211. (3) H4 operator prior slot reserved and empty, moot — progress.md:1101-1103 |
| **Registered reopen conditions** | ▲ registrations/H4/REGISTRATION.md:230-234 — "a funding regime in which deeply negative entry funding stops being rare (conditioning rates several times higher, sustained), a much larger listing rate, or a redesign of the conditioning claim strong enough to justify the near-0.85 conditional share — each a new registration". ▲ HYPOTHESES.md:106 gives only "a persistent negative-funding listing regime — a new registration". My documents carry no reopen condition for H4 |
| **Trigger already met?** | **No**, and the first two clauses cannot be met inside this design: at the governing share, power reaches the cull's 0.50 floor only near n ≈ 1600 (k = 3 alpha) / n ≈ 1150 (k = 1 alpha), against 173 fresh events by the deadline even at a conditioning rate of 1.000 (recomputation in DRAFT-p2-progress-4). Only the third clause — a redesigned conditional-share assumption — can fire |
| **Possibly met by another repo?** | **Yes, for the third clause** — a measured *conditional* share-positive on negative-funding perps from another repository would supply the justification the clause asks for. **MLCryptoEngine H8** already measures the funding/price cancellation on negative-funding perps (carried into this repo at progress.md:32: "+43.68 percent per year funding income against −42.91 percent price return"), and **MLCryptoEngine H5** measured MERL at −22.38 %/yr and TNSR at −32.41 %/yr. Flagged for the cross-repository pass |

### H5 — HIP-3 equity-style perpetual basis (feasibility entry, outside the familywise budget)

| field | value |
|---|---|
| **Status** | PENDING — census window open, collector armed |
| **Closure kind** | Non-terminal `PENDING` row of the registered outcome map; terminal states are VIABLE / INDETERMINATE / CLOSED |
| **Closure date** | Row fired 2026-08-28T22:04:30Z (the 22:20Z heading is corrected in progress.md:1492-1498). **Scheduled terminal firing: 2026-09-26** — progress.md:1388, 1401; docs/STAGES.md:40; reports/h5/verdict.json |
| **Deciding figures (n)** | Structural clauses **clear**: 94 instruments carry a served reference (bar ≥ 20); funding served on 94 of 94, share 1.000 (bar ≥ 0.500). Coverage clause **open**: **0** instruments at 30 days of coverage (bar ≥ 20). Basis so far: `extended` median absolute **4.14 bp**, IQR 0.71–9.15, n = 188 observations over 2 snapshots; 9.57 % over the 18 bp floor, 1.60 % over the 54 bp bar — progress.md:1393-1401; reports/h5/verdict.json. Live-only cross-section: median absolute **3.72 bp**, IQR 0.73–7.31, max 51.4, 0.0 % over 54 bp, n = 94 — docs/H5_ACCESS.md:193 |
| **Universe (n)** | 273 HIP-3 instruments over 10 dexs → 151 resolved (118 equity, 15 ETF, 18 index), 80 `excluded_non_equity`, 42 `excluded_unresolvable` → **94 live** after the three-field delisted rule (57 excluded, 0 conflicting) — docs/H5_ACCESS.md:133-145; progress.md:1269-1281 |
| **Retrospective branch** | Registered basis **does not exist** (no historical mark, no historical oracle in one row; `candleSnapshot` closed by standing rule 7) — progress.md:1325-1327; DECISIONS.md:531-533. Named secondary (`premium`) gated to 27 of 151, 124 `excluded_quarantined`; of the 27, 25 have no funding rows at all and 2 are days old → **39 observations, 2 instruments, 0 meeting coverage** — progress.md:1328-1336 |
| **Blockers, stated** | (1) **Time**: 29 daily passes needed from 2026-08-28 — progress.md:1401. **LIVE**: recomputed 2026-09-04T23:16Z from `data/h5/snapshots.jsonl`, the 20th-best-covered instrument has 7 covered days → 23 passes remain → fire **2026-09-27**, one day later than recorded (DRAFT-p2-progress-8). (2) **No external equity price feed** — "zero dollars, keyless endpoints, one venue"; every reference is the venue's own — DECISIONS.md:417-419. (3) **The retrospective cohort gate** — coins in the generating sample, the fresh plan, or either leg of an assigned H2 pair are refused; "It cost the entry its retrospective sample (27 of 151 eligible, 39 usable observations) and was kept anyway" — DECISIONS.md:544-546. (4) **The delisted exclusion (Amendment H5-2)** — "it makes VIABLE **strictly harder** and deleted this entry's only route to it", 57 excluded, 0 conflicting — DECISIONS.md:510-511; progress.md:1285-1292. (5) **The H5 operator prior slot, reserved and empty** — it blocks *the successor draft only*, never the map: "a verdict is never withheld for want of a prior" — ▲ README.md:87-91; docs/STAGES.md:41. (6) **Carried, cross-repo**: "the closed-and-carried IBKR economics (40–100 bp whole-share round trips, fractional orders refused at error 10243) mean no cross-venue pair is registrable here even if the deviation were real" — DECISIONS.md:432-434; source figure logged at progress.md:1120 |
| **Registered terminal conditions** | **VIABLE** — median absolute basis over 54 bp in at least one session tag → draft a successor registration **in a fresh repo, with an independent underlying feed**, and only once the operator prior slot is filled; **INDETERMINATE** (18–54 bp) → a recorded lead, no successor authorized; **CLOSED** (under 18 bp in every tag) → the family closes, collection stops. No capital in any branch — docs/STAGES.md:41; DECISIONS.md:464-487 (the 54 bp = 3 × 18 bp arithmetic and the boundary conventions) |
| **Trigger already met?** | **Partly.** The two structural clauses were met on 2026-08-28 and the collector was armed on that trigger (94 ≥ 20 served references — progress.md:1351-1353). The coverage clause is not yet met. **Open observation** (DRAFT-p2-progress-1): the terminal row is scheduled to fire with **zero `regular`-session observations** — measured live, 0 of 1,929 rows across 8 passes — because the only scheduled snapshot runs at 01:40 UTC, which the registered tagger can only ever classify `closed_weekday` or `weekend` |
| **Possibly met by another repo?** | **Yes, two ways.** (a) The IBKR blocker at DECISIONS.md:432-434 is carried from **HFExperiment** ADR-026 / A.1b; a later dated HFExperiment entry lifting the fractional-order refusal or the 40–100 bp cost would supersede the sentence that makes a cross-venue pair unregistrable here. (b) The VIABLE consequence is explicitly "a registration in a **different repository**, against an independent feed" — so any program repository already holding an independent equity feed could host that successor, and this ledger row should be matched against the program's other repositories in the cross-repo pass |

---

## 2. Non-hypothesis entries in my documents

| item | status | kind | date | deciding figure (n) | file:line |
|---|---|---|---|---|---|
| ADR-032 — bounded DNS wait as `ExecStartPre` on both collector units | Applied, closed | Infrastructure fix, explicitly **not** a registration amendment | 2026-09-02 | 4 watcher sweeps between 2026-08-31T21:23Z and 2026-09-02T09:10Z polled 0 dexs with a null http_status; each followed by a clean 11-dex sweep; a direct probe returned http 200 in 0.15 s | DECISIONS.md:549-602; progress.md:1520-1556 |
| Stage A postscript conflict (push vs "push nothing") | Resolved | Operator instruction (Amendment 2, 2026-08-28) superseded the push-nothing protocol | 2026-08-28 | n/a | progress.md:148, 368-374, 390-391; restated for H5 at progress.md:1151-1159 |
| ADR-026 — `para:IGV` recorded `not_in_registered_mapping` and **not added** | Open by design | Universe-fitting refusal; "a later amendment may add it" | 2026-08-28 | 1 instrument of 273 enumerated; it is delisted at birth | DECISIONS.md:406-407; docs/H5_ACCESS.md:176-180 |
| ADR-013 — simultaneous-drop cull semantics | Accepted, with a recorded caveat for future registers | "A future register weighing sequential (worst-first) removal should decide BEFORE any projection exists" | 2026-08-28 | Under the flat pair projection H2 would have dropped in pass 1 alongside H3/H4 (k = 0) | DECISIONS.md:159-164 |
| PENDING_ENFORCEMENT config list | Closed (burned to empty) | Process gate | end of register A.3, 2026-08-28 | list reached empty; one entry outstanding at A.0 (`h2_cost_floor_multiple`) | DECISIONS.md:127-137; docs/SUBSTRATE.md:34-39; progress.md:715 |

---

## 3. Cross-repository pass — carried figures and blockers to check elsewhere

| carried item | figure as carried here | file:line here | source repo to check |
|---|---|---|---|
| IBKR equity access | fractional orders refused at **error 10243**; whole-share round trips **40–100 bp** at this operator's sizes; "equities stay closed at this stake regardless" | DECISIONS.md:432-434; docs/STAGES.md:74; progress.md:1120 | **HFExperiment** (ADR-026, A.1b) |
| H8 funding/price cancellation | +43.68 %/yr funding income against −42.91 %/yr price return on negative-funding perps, "near cancellation" | progress.md:32 | **MLCryptoEngine** (H8) |
| Per-instrument funding levels | MERL −22.38 %/yr, TNSR −32.41 %/yr | progress.md:32 | **MLCryptoEngine** (H5) |
| Manufactured survivorship lesson | drove the delisting-observability test to first-class status; PASS 6/6 here | docs/ACCESS.md:200; progress.md:84 | **solclear** (Finding 2) |
| Per-endpoint (not per-host) rate ceilings | applied in advance; measured here at perpDexs ~79/min and candleSnapshot ~23/min at 5,000 rows | DECISIONS.md:56-68; docs/ACCESS.md:118-149 | **solattn** (Amendment 6) |
| Seal-the-closed-day defect | avoided by construction here | DECISIONS.md:70-79 | **solattn** (ADR-019) |
| Text-level guards pass vacuously | drove the AST guard here | DECISIONS.md:50-54; DECISIONS.md:127-137 | **InsiderExperiment** (ADR-012, mutation exercise) |
| Adopted-prior contamination | "an adopted prior corrupts the calibration ledger"; H1's slot was nonetheless filled **0.40 (adopted)** | progress.md:33, 446-447 | **NPDExperiment** (Amendment 0) |
| External drift studies (registration inputs, never re-verified in-repo) | Delphi 652 CEX listings since Jan 2025, 12 % profitable, median −82 %; Animoca 773 listings Jan–Sep 2024, median −40 to −70 %; Memento 118 TGEs 2025, 84.7 % below listing valuation | progress.md:31 | external; no in-repo verification recorded — the standing rule "Measured beats documented" (CLAUDE.md:23-24) was applied to venue figures but not to these |

---

## 4. Ledger-level observations (factual, no advocacy)

1. **Every terminal row in this repository was fired by a function against a table registered before the data existed**, and each carries its input figures with their n in the same entry. I found no closure recorded without its deciding number.
2. **Three of the five entries have reopen conditions stated only in the other reader's documents** (`HYPOTHESES.md`, `registrations/H3`, `registrations/H4`). My assigned documents — DECISIONS.md, progress.md, docs/, reports/ — record the closures and their inputs but not the reopen triggers, except for H2's look gates (docs/STAGES.md:25-26) and H5's terminal branches (docs/STAGES.md:41).
3. **Two registered reopen conditions cannot fire as worded** (H3's magnitude leg at any listing rate; H4's first two clauses at any conditioning rate reachable before ≈ n 1150–1600) — see DRAFT-p2-progress-4 and -5 for the arithmetic.
4. **One figure in this ledger is already stale against live data**: the H5 projected fire date, 2026-09-26 as recorded in progress.md:1401, docs/STAGES.md:40 and reports/h5/verdict.json, against 2026-09-27 recomputed from the store on 2026-09-04T23:16Z.
