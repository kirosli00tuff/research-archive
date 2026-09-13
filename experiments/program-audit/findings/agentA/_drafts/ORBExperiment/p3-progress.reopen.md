# REOPEN LEDGER — ORBExperiment, part p3-progress

**Repository / anchored SHA:** ORBExperiment / `f2aa675a80fc06b74979040b3028154d1add5ec0` (main, 2026-08-29)
**Scope:** entries and verdict-bearing artifacts whose primary evidence sits in my assigned documents
(`progress.md`, `reports/**`, `tools/**`). Rows whose primary text lives in `HYPOTHESES.md`,
`REGISTRATION.md`, `DECISIONS.md` or `docs/` are marked *(primary text outside my assignment)* and are
included because progress.md records or reproduces the same figures.
**This ledger is factual, not advocacy.** Every figure carries its n and a file:line.
All line numbers are in the anchored snapshot at
`/home/kiros-li/.cache/program-audit/scratchpad/snap/ORBExperiment/`.

---

## H1 — H-ORB, opening-range breakout on relative-volume-selected names

| field | value |
|---|---|
| **status** | **CLOSED** |
| **closure kind** | `cost-bound` ("The effect may be real; it does not survive the modeled cost"), precedent MLCryptoEngine H6 |
| **closure date** | **2026-08-30** (A.3 rescue pass TASK 5, Amendment 28) |
| **deciding figure (n)** | measured pessimistic-minus-central slippage **shift 0.467065 USD/share** against a `RESCUED_DEGRADED` threshold of **0.040386** (the implied central mean at the registered 1.40 Sharpe); pessimistic-cost mean **−0.426679**; **E2 power 0.000000, JOINT power 0.000000, minimum n jointly Absent**. Band ends: entry central 0.087019 / pess 0.354645 (**n = 550**), stop 0.033529 / 0.198061 (**n = 210**), close 0.040000 / 0.261000 (**n = 340**); stop-exit share 0.381818 (**n = 550**); dispersion 2.029585 USD/share (**n = 550**); measured on **28 evaluable sessions of 42 pulled**, **199 tickers of a 5,317-name listing**, 2026-07-01 to 2026-08-28 |
| **file:line** | progress.md:3613-3615 (verdict), progress.md:3583-3593 (band table), progress.md:3659 (closure), reports/stage_a3rescue/task3_rescue_verdict.json, reports/stage_a3rescue/task2_slippage_band.json, reports/stage_a2repair/task3_execution_mix.json |
| **blockers (file:line)** | **(1)** deciding band is post-holdout-regime only, "may misstate in-sample dispersion in either direction by an amount this repository has not measured and does not claim to bound" — progress.md:2336-2338, task3_rescue_verdict.json `carve_out_caveat`. **(2)** band is a **lower bound**: 457 of 550 entry triggers and 195 of 210 stop triggers crossed intrabar and were recorded at 0.0 overshoot; market impact not measured at all — progress.md:3604-3607. **(3)** the frozen Section 6 cost model **refuses 550 of 550 trades** because the SEC Section 31 effective date is `Absent` — progress.md:2674-2683. **(4)** no real execution evidence, "This repository holds none, has no broker credential, and none is planned" — HYPOTHESES.md:62, docs/HANDOVER.md:272-275 *(primary text outside my assignment)*. **(5)** in-sample window is single-sourced: cross-vendor agreement covers 459 holdout and **0 of 1,762 in-sample** sessions (SL-3) — progress.md:2388-2401 |
| **reopen conditions (file:line)** | **The register entry states none.** HYPOTHESES.md:7-9 requires a closed entry to "state what would reopen it — or state that nothing would"; no row of the H1 entry does either *(primary text outside my assignment)*. The **only** reopen route recorded anywhere in the repository is docs/HANDOVER.md:272-275: "**Pursue Amendment 21 route (b)** — narrow the registered cost band on **real execution evidence** … **It is the only route that could reopen a cost-bound closure**". Also standing but explicitly **not** reopening routes: the 2026-09-12 bar-integrity re-pull, which "would measure bar integrity; it would not reopen H1" (docs/HANDOVER.md:151); and the H1b floor scan, which "cannot rescue H1" (progress.md:3432, Amendment 24 §6) |
| **possibly met by another repo?** | **YES, flag for the cross-repo pass.** The single reopen route needs **real US-equity execution evidence**. progress.md:354 records that **HFExperiment reaches an equity broker** and is the source of the IBKR error-10243 integer-share constraint carried into this registration (progress.md:90). If HFExperiment holds realized fills, quoted spreads at fill time, or an IBKR/broker execution log for US equities, it may satisfy the exact condition ORBExperiment declares unavailable. Secondary flag: **ETFExperiment** (US-listed ETF flow) and **AiTrader** (carries a 09:30 US session boundary, progress.md:355-356) for any US-equity quote or execution substrate |
| **notes for the cross-repo pass** | The closure's arithmetic reproduces exactly and is robust at the registered 1.40 assumption. See draft findings DRAFT-p3-progress-1 to -4 for three defects in the deciding number (an unsigned one-minute price change charged as close-exit slippage, 29.3 % of the shift; an entry slippage exceeding the registered marketable-limit cap, 57.3 %; no interval on any of the three deciding percentiles) and for the six of eight registered trials never run |

---

## H1b — H-ORB with a raised price floor

| field | value |
|---|---|
| **status** | **REGISTERED_NOT_OPEN** |
| **closure kind** | n/a — not closed |
| **closure date** | n/a; **registered 2026-08-30** (Amendment 25) |
| **deciding figure (n)** | feasibility scan only, **28 sessions, 199 tickers**: `central_mean_to_shift_ratio` 0.9742 (floor 5, 560 name-sessions) → 0.9983 (10) → 1.1415 (20) → 1.4767 (50, 446) → **2.1424** (100, 310); mean relative volume of selection falls 2.0652 → 1.4103; dispersion rises 2.0296 → 3.1992; top-20 unfillable in the scan sample at floors 50 and 100 |
| **file:line** | progress.md:3634-3651, reports/stage_a3rescue/task4_floor_scan.json |
| **blockers (file:line)** | the scan's ratio column uses the **registered Section 6 (carried) band shift ≈ 0.0415**, not the measured 0.467065 — disclosed in `comparison_figure_note`, reports/stage_a3rescue/task4_floor_scan.json; under the measured band the same ratios run 0.086 → 0.183 and no floor clears 1.0. The `entry_overshoot_median_usd_per_share` "independent check" on price-invariance is **0.0 at every floor** and carries no information. The "top-20 fillable" column is a **1-in-26 subsample artefact**, labelled as one at progress.md:3648-3651. H1b "inherits the closure's problem" — docs/HANDOVER.md:266-271 *(primary text outside my assignment)* |
| **reopen conditions (file:line)** | opening requires **its own full registration, its own power gate computed rather than inherited, and explicit operator instruction — none of the three exists**; the floor itself is deliberately not registered — progress.md:3555-3567. Multiplicity cost pre-paid: DSR trial count 8 → 9 for H1b only — progress.md:3561-3564 |
| **possibly met by another repo?** | no |

---

## H2 — pre-FOMC drift

| field | value |
|---|---|
| **status** | **PARKED** (not closed, not refuted, not tested) |
| **closure kind** | n/a |
| **closure date** | n/a; parked **2026-08-29** |
| **deciding figure (n)** | none — no measurement was ever taken |
| **file:line** | progress.md:181 (registration instruction), HYPOTHESES.md "Parked" section *(primary text outside my assignment)* |
| **blockers (file:line)** | the parking reason only: "no second repo opens while H1 is unresolved" — progress.md:181 |
| **reopen conditions (file:line)** | **TRIGGER ALREADY MET, and explicitly not acted on.** The parking condition was H1 being unresolved; H1 closed `cost-bound` 2026-08-30 (progress.md:3659), and HYPOTHESES.md records "**H1 closed `cost-bound` on 2026-08-30** (Amendment 28), so the condition that parked these two no longer holds. **They are not thereby opened**: each still needs its own registration, its own power gate and explicit operator instruction, and **none of the three exists for either.**" *(primary text outside my assignment)* |
| **possibly met by another repo?** | no for the parking trigger; the substrate (session calendar) is local |

---

## H3 — VIX term-structure roll yield

| field | value |
|---|---|
| **status** | **PARKED** |
| **closure kind** | n/a |
| **closure date** | n/a; parked **2026-08-29** |
| **deciding figure (n)** | none |
| **file:line** | progress.md:181; HYPOTHESES.md "Parked" *(primary text outside my assignment)* |
| **blockers (file:line)** | same parking reason (progress.md:181); additionally "shares no substrate with H1 at all" |
| **reopen conditions (file:line)** | **TRIGGER ALREADY MET** on the same reasoning as H2, and explicitly not acted on |
| **possibly met by another repo?** | possible — a VIX-futures term-structure substrate is not held here; flag any repo carrying a futures curve |

---

## Ten candidates closed before opening at registration (2026-08-29)

| field | value |
|---|---|
| **status** | **CLOSED before opening**, all ten |
| **closure kind** | not typed with one of the five house kinds; each carries a one-line reason. **None was closed on a measurement taken in this repository** |
| **closure date** | **2026-08-29** |
| **deciding figure (n)** | only candidate 1 carries figures, and they are **carried, not measured**: index-ETF ORB closed on the replication's 1,775 trades vs the paper's 1,795, gross Sharpe 1.06, gross edge **0.070 USD/share**, net PnL crossing zero at **≈0.022 USD/share** entry slippage against a QQQ spread near 0.010 (carried C-5, C-6) |
| **file:line** | progress.md:181 (the registration instruction naming all ten), progress.md:82 (the carried replication figures), HYPOTHESES.md "Closed before opening" table *(primary text outside my assignment)* |
| **blockers (file:line)** | none stated; the closures are judgements at registration time |
| **reopen conditions (file:line)** | none stated for any of the ten; HYPOTHESES.md records "none of them is reopened by anything H1 does" (HYPOTHESES.md:118) |
| **possibly met by another repo?** | **YES for three.** #9 New Hyperliquid listing drift is labelled **DUPLICATE against NPLExperiment** (closed there as H1, FAIL, 197/312 positive, exact lower bound 0.5707 against a 0.60 bar). #10 Spot Bitcoin ETF flow is labelled **DUPLICATE against ETFExperiment** (running as H-ETF). #1 Index-ETF ORB was closed **entirely on carried literature figures**; this repository has since measured a real single-name quoted spread band (progress.md:3583-3595) that does **not** apply to an ETF, so #1's closure remains untested against any ETF quote measurement — flag for any repo holding ETF quote data |

---

## Section 0 outcome map — the verdict-bearing artifact

| field | value |
|---|---|
| **status** | **OPEN / PENDING**; last fired **PENDING_REVISION** 2026-08-30T03:42:21Z |
| **closure kind** | n/a — a verdict state, not a hypothesis closure. `GO` and `DEGRADED` are structurally unreachable while an integrity input is absent, pinned by test and by tools that exit 78 |
| **closure date** | four firings: **PENDING_ACCESS** 2026-08-29 (Amendment 4); **PENDING_REVISION** 2026-08-29 (Amendment 10); 2026-08-29 (Amendment 16); 2026-08-30 (A.3 TASK 5) |
| **deciding figure (n)** | at the last firing: α per co-primary **0.05**; holdout **875** sessions; **E1 0.832450** at 1.40 / 0.999835 at 2.81 / 0.366747 at 0.70; **E2 0.000000, JOINT 0.000000**; delisted with intraday history **203 (n = 229) PASS**; tape **SAME_TAPE median 1.005197 (n = 100)**; reach Alpaca **2016-01-04 (n = 16 probes)**, Massive **2024-08-29 (n = 16)**; bar revision **Absent**; agreement share **Absent** |
| **file:line** | progress.md:1995-2024 (Amendment 10 firing with every input), progress.md:2796-2824 (Amendment 16), progress.md:3307-3328 (final), reports/stage_a1r/task10_section0.json, reports/stage_a1amend/task6b_section0.json, reports/stage_a2repair/task6_section0.json, reports/stage_a3rescue/task5_section0.json |
| **blockers (file:line)** | both integrity inputs are recorded absences until **2026-09-12** — progress.md:2021-2022, reports/stage_a3rescue/task5_section0.json `inputs` |
| **reopen conditions (file:line)** | `PENDING_ACCESS` clause is pinned inert "the moment both measurements exist" — progress.md:489-497. `PENDING_SPEND` is **registered and did not fire**, trigger = a measured reach shortfall against the registered windows — progress.md:2028-2031. Amendment 1's ordering refinement: when a vendor serves, a BLOCKED trigger with a **measured** input fires ahead of the pending states; boundary pinned at delisted 20 → PENDING_REVISION, 19 → BLOCKED-5 — progress.md:2054-2061 |
| **possibly met by another repo?** | no |

---

## Bar-integrity measurement — A.1 TASK 3 (revision) and TASK 4 (agreement)

| field | value |
|---|---|
| **status** | **PARKED on a calendar**; machinery built, armed and verified refusing |
| **closure kind** | n/a — the measurement does not exist yet; explicitly **not** a `source-integrity-blocked` closure, "that requires a vendor whose bars were **measured** and found unstable, and **no bar has been served to fail**" — progress.md:771-773 |
| **closure date** | n/a |
| **deciding figure (n)** | probe slice sealed: **60 sessions × 40 tickers = 2,400 pairs, 480 files, 737,507 bars**, 200 on every one, 477 distinct SHA-256, 0 chunks needing a second page — progress.md:1902-1911. Feed confirmed consolidated by measurement: **7 of 7 discriminating chunks match the consolidated count, 0 of 7 match single-venue**, n = 8 chunks — progress.md:2506-2518 |
| **file:line** | progress.md:1886-1891 (earliest eligible re-pull), progress.md:1974-1982 (what is armed and what is not), reports/stage_a1r/task9_probe_manifest.json, reports/stage_a1amend/task3b_feed_confirmation.json |
| **blockers (file:line)** | **the registered ≥14-calendar-day wait. `orb.repull.require_due` refuses every earlier attempt, loudly, naming the date** — progress.md:1886-1891 |
| **reopen conditions (file:line)** | **trigger date 2026-09-12** — not reached at the anchor (2026-08-29/30) and **still not reached at the time of this audit (2026-09-04; 8 days out)**. Registered verdict thresholds unchanged: PASS ≤ 0.005 changed-bar share, PARTIAL ≤ 0.020, **FAIL > 0.020 fires BLOCKED-2** — progress.md:201, docs/HANDOVER.md:140-143. Agreement can only run over the **459** overlap sessions on or after 2024-08-29 — progress.md:1594-1602 |
| **possibly met by another repo?** | **MAYBE.** The revision measurement is vendor-specific (Alpaca SIP). Any repo holding a second US-equity minute-bar vendor on a **different upstream** would supply the Concretum test this repository registers as unavailable (progress.md:1504-1518). Flag **ETFExperiment**, **AiTrader**, **HFExperiment** |

---

## SL-3 — the in-sample window is single-sourced

| field | value |
|---|---|
| **status** | **OPEN scope limitation**, registered 2026-08-29 (REGISTRATION.md §11.1, Amendment 12) |
| **closure kind** | n/a — "It is **not a Section 0 branch**: it fires nothing and changes no figure" |
| **closure date** | n/a |
| **deciding figure (n)** | in-sample sessions **1,762**, with cross-vendor overlap **0**; holdout **875**, overlap **459**; reference vendor earliest served session **2024-08-29**; reach probes **n = 16 per credential** — progress.md:2394-2401 |
| **file:line** | progress.md:2375-2439 |
| **blockers (file:line)** | Massive's free tier serves a rolling 24-month window, measured to the day — progress.md:1550-1551 |
| **reopen conditions (file:line)** | **two routes, neither chosen, neither costed, no spend authorised**: a reference credential whose tier reaches **2016-01-04**, or **explicit operator acceptance** that the in-sample window is single-sourced — progress.md:2434-2436 |
| **possibly met by another repo?** | **YES, flag.** Route (a) is satisfied by any repo holding a US-equity minute-bar credential reaching 2016-01-04 on a **different upstream** from Alpaca/Massive SIP redistribution. Flag **ETFExperiment**, **AiTrader**, **HFExperiment** |

---

## Frozen Section 6 cost model — SEC Section 31 effective date

| field | value |
|---|---|
| **status** | **BLOCKED** — `Absent(sec_section_31_effective_date_not_measured)`; the model refuses to price any trade |
| **closure kind** | n/a — a recorded absence, deliberately not a synthesized value (standing rule 5) |
| **closure date** | first recorded 2026-08-29 (A.2 TASK 2, Amendment 3); re-attempted and re-recorded 2026-08-29 (A.1 TASK 5) |
| **deciding figure (n)** | rate measured **0.0000206 × value of aggregate sales**, effective date **not measured**; `REGISTERED_COST_MODEL` **refused 550 of 550 trades**; the bracket across SEC rate 0 to 0.0000206 is **0.000171 USD/share wide, 8.43 × 10⁻⁵ relative**, so the missing date moves no deciding figure — progress.md:2674-2698 |
| **file:line** | progress.md:649-655 (first record), progress.md:2672-2698 (re-attempt and bracket), progress.md:2910 (the sec.gov attempts recorded as **uncharged, unregistered vendor, no cap exists**) |
| **blockers (file:line)** | `sec.gov` **HTTP 403 "Request Rate Threshold Exceeded"**, **n = 4 across two sessions**, two of them 20 s apart — progress.md:651-652, 2679-2683. The stored IBKR page carries the rate and no effective date — progress.md:2681-2683 |
| **reopen conditions (file:line)** | **none registered.** The repository states the datum is "not recoverable offline either" (progress.md:2683) and does not name a retry condition, a pace, or an alternative publisher. See DRAFT-p3-progress-6: the host was never registered as a paced vendor under the repository's own request ledger, and no second publisher of the same datum is named anywhere (`grep -rn "federalregister\|Federal Register"` over the snapshot returns 0 hits) |
| **possibly met by another repo?** | **MAYBE, flag.** Any repo modelling US-equity or US-ETF round-trip cost needs the dated Section 31 schedule. Flag **HFExperiment** (equity broker) and **ETFExperiment** |

---

## E2 dispersion input and the pre-period carve-out

| field | value |
|---|---|
| **status** | **RESOLVED by amendment** — falsified blocker, superseded rather than worked around |
| **closure kind** | n/a |
| **closure date** | blocker recorded 2026-08-29 (progress.md:1357-1368); amended two-sided 2026-08-29 (Amendment 11) |
| **deciding figure (n)** | **n = 2 credentials, 0 serving any session before 2016-01-04** — Massive refuses (403 NOT_AUTHORIZED), Alpaca serves 200 with 0 bars — progress.md:1357-1360. Amended region: strictly before 2016-01-04T14:30:00.000Z **or** at/after 2026-07-01T04:00:00.000Z; four boundary fixtures all exercised on their edges — progress.md:2348-2356 |
| **file:line** | progress.md:2308-2372 |
| **blockers (file:line)** | the amended post-holdout half carries an **unbounded directional cost**: "may misstate in-sample dispersion in either direction by an amount this repository has not measured and does not claim to bound" — progress.md:2336-2338 |
| **reopen conditions (file:line)** | the post-holdout region **grows as real time advances**, and the sessions used are recorded in the ledger at the time of computation rather than fixed in advance — progress.md:2211. This is the standing route to a larger dispersion and slippage sample at **0 dollars** |
| **possibly met by another repo?** | no |

---

## Rate ceilings and pacing

| field | value |
|---|---|
| **status** | **Massive MEASURED; Alpaca sustained ceiling still `None` (unreached)** |
| **closure kind** | n/a |
| **closure date** | Massive 2026-08-29 (A.1 TASK 7); Alpaca re-attempted 2026-08-29 (amendment pass TASK 4) |
| **deciding figure (n)** | Massive **5.00/min**, first refusal at request 6 of 8 on **both** endpoints, n = 53 requests over 4 cells — progress.md:1747-1753. Alpaca: **burst 384 admitted then a 429 at request 385 within 55.96 s** (n = 391), then **250 of 250 admitted at a sustained 199.73/min over 75.10 s** (n = 250); ceiling recorded as **`None` — a lower bound, never a ceiling** — progress.md:2564-2620 |
| **file:line** | progress.md:1740-1813, progress.md:2542-2645, reports/stage_a1r/task7_ceilings.json |
| **blockers (file:line)** | "the whole escalation fit inside one rolling minute — 55.96 s", so a token bucket near 400 refilling at 200/min and a hard 411/min limiter are **not distinguished** by the measurement — progress.md:2582-2587 |
| **reopen conditions (file:line)** | a sustained measurement longer than one rolling minute at a rate above 199.73/min would establish the ceiling; until then `MEASURED_CEILING_PER_MINUTE["alpaca:bars"]` stays `None` and the test refuses to let a lower bound be written into the ceiling dict — progress.md:2608-2611 |
| **possibly met by another repo?** | **MAYBE** — a repo holding an Alpaca credential on a different tier could measure the same endpoint; the ceiling is per endpoint and per tier |

---

## Massive paid tier / PENDING_SPEND

| field | value |
|---|---|
| **status** | **registered, NOT fired**; standing open operator item |
| **closure kind** | n/a |
| **closure date** | n/a |
| **deciding figure (n)** | Massive earliest served **2024-08-29**, **n = 16 probes**: 0 of 1,762 in-sample and 459 of 875 holdout sessions. The branch did not fire because Alpaca reaches **1,762/1,762 and 875/875** at zero cost — progress.md:1540-1541, 1609-1617 |
| **file:line** | progress.md:1609-1637, progress.md:2028-2031 |
| **blockers (file:line)** | spend requires an explicit operator instruction and its own ADR; the monthly figure **near 29 USD/month is carried, C-18, never measured**, and **the reach a paid tier delivers is not measured and not recorded as a number** — progress.md:1622-1633 |
| **reopen conditions (file:line)** | "**If the operator wants the paid reach, the honest way to get it is one month's spend and a second bisection**" — progress.md:1631-1633; the branch is registered so a later reach shortfall "has a clause to land in rather than being discovered without one" — progress.md:1635-1637 |
| **possibly met by another repo?** | **MAYBE** — a Polygon/Massive paid credential held anywhere else in the program would answer the reach question without new spend |

---

## Stage C and Stage D latches

| field | value |
|---|---|
| **status** | **both ABSENT, unopened**; no in-sample or holdout bar has ever been read for a verdict |
| **closure kind** | n/a |
| **closure date** | n/a |
| **deciding figure (n)** | Section 10 clause states at the last recorded check: clause 1 (power) **UNSATISFIED**, clause 2 (operator prior 0.30 INDEPENDENT) **SATISFIED**, clause 3 (explicit operator instruction) **UNSATISFIED** — progress.md:1234-1240. Section 10.1 restates clause 1 as a **JOINT** condition, bounded above by the smaller component power — progress.md:3259-3263 |
| **file:line** | progress.md:1234-1240, progress.md:2297-2299, progress.md:3390-3391 |
| **blockers (file:line)** | joint power **0.000000** at every assumption under the measured band makes clause 1 unsatisfiable — progress.md:3615, 3318 |
| **reopen conditions (file:line)** | all three clauses simultaneously; a second read of either window **voids the hypothesis** — progress.md:806-811 |
| **possibly met by another repo?** | no |

---

## Cross-repo pass — consolidated flags from this ledger

1. **H1's only reopen route (real US-equity execution evidence)** → check **HFExperiment** first (progress.md:354, :90 name it as reaching an equity broker and as the source of the carried IBKR error-10243 constraint); then ETFExperiment, AiTrader.
2. **SL-3 / the Concretum test (a second US-equity minute-bar upstream reaching 2016-01-04)** → ETFExperiment, AiTrader, HFExperiment.
3. **SEC Section 31 dated fee schedule** → HFExperiment, ETFExperiment; also note that no repository here names the Federal Register or the SEC Fee Rate Advisories as a source.
4. **Duplicate closures already resolved elsewhere** → candidate #9 in NPLExperiment (H1, FAIL, 197/312, lower bound 0.5707 vs a 0.60 bar); candidate #10 in ETFExperiment (H-ETF, running).
5. **Candidate #1, index-ETF ORB, closed on carried literature figures only** → any repo holding ETF quote data could test the carried 0.022 USD/share break-even that closed it.
6. **`cost-bound` precedent consistency** → MLCryptoEngine H6 is cited as the precedent for H1's kind; check that H6's closure rests on a comparable modeled-cost construction.
7. **Parked-trigger already met** → H2 and H3's parking condition ("no second repo opens while H1 is unresolved") was lifted by H1's closure on 2026-08-30 and both were explicitly left parked.
