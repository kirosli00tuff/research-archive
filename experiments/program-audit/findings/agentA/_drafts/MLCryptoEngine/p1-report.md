# Agent A draft findings — MLCryptoEngine, part p1-report

Repository: MLCryptoEngine @ `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22 — this SHA is HEAD of the live repository, so no later commit can invalidate anything below).
Assigned primary documents: `report.md` (5,190 lines, read in full), `README.md` (read in full).
Direction: A (closed too early / too hard). Advocacy, but every figure is quoted or recomputed.

Scratch work and recomputation scripts: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-mlcrypto-p1-report/`.

---

### DRAFT-p1-report-1
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H1 — short-horizon directional prediction on crypto spot; specifically the C.14 "no usable filter" verdict and the "does not reopen" restatement.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The absolute numbers settle it: the best top-decile capture across both venues and all horizons is **5.00 bps against an 80 bps round trip**. The economic bar is missed by 16×. **H1 does not reopen.**" — MLCryptoEngine/report.md:2328-2330
- **Evidence:**
  - The deciding capture figure is Kraken BTC/USD at 900 s, top-confidence decile **5.0020 bps**, all-sample capture 0.2093 bps, ratio 23.9×, over 6 validated days / **n = 165,075** samples — MLCryptoEngine/report.md:2298 and :2289.
  - The 80 bps round trip is a Kraken/Coinbase **spot** figure. Four days earlier the same repository measured a reachable venue at a different price: "against a maker round trip of **3.00 bps** (1.5 bps/leg, base tier, `config/venues.yaml`, verified 2026-08-01)" — MLCryptoEngine/report.md:1114. D.1a re-verified it: "Hyperliquid base tier **0.015% maker / 0.045% taker** (1.5 / 4.5 bps), verified against the live schedule 2026-08-11 … 3.0 bps maker round trip" — MLCryptoEngine/report.md:4226-4227.
  - H1's own registered reopening condition is a cost threshold at exactly that level: "A round-trip cost below roughly **3 bps**, i.e. under 1.5 bps per side. On Coinbase that is the 0 bps maker tier requiring **$250M trailing 30-day volume**; on Kraken, the 0 bps maker tier at **$10M**. Neither is reachable at this project's capital." — MLCryptoEngine/HYPOTHESES.md:54 (also quoted verbatim at MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md:261). The condition enumerates only Kraken and Coinbase fee tiers; the third recorded venue, whose base tier already sits at 1.5 bps/side with **no volume requirement**, is not considered in it.
  - Hyperliquid is present in the Phase B research-run configuration with its costs already wired: "cost assumptions: … / hyperliquid: maker 1.5 bps, taker 4.5 bps per leg (tier 0) + spread / …" — MLCryptoEngine/report.md:773. It was excluded once, for a reason that expired the next day: "**hyperliquid was skipped — it has no recorded data for 2026-07-31** (its recorder was activated 2026-08-01)" — MLCryptoEngine/report.md:775-776.
  - The blocker expired and was never revisited. Hyperliquid validated **PASS at 100.00% coverage** for 2026-08-03 (MLCryptoEngine/report.md:1289-1302), and by D.1b it was the project's *sole* live venue — "kraken and coinbase retired" (MLCryptoEngine/report.md:4662). No Phase B research run, and no C.14 run, was ever executed on Hyperliquid: the four Phase B run sections in report.md (:677, :769, :889, :924) carry only `coinbase`, `kraken` and `cme MBT` subsections, and C.14's scope is stated as "Six validated days (2026-07-30 → 2026-08-04) on Kraken BTC/USD and Coinbase BTC-USD" (MLCryptoEngine/report.md:2273-2274).
  - The project itself said this was the venue that made the cost question worth asking: "Net: Hyperliquid can test 500 ms -> 900 s, losing only the shortest horizon — and it is the venue whose 1.5/4.5 bps fees make the cost side of this comparison worth running at all. - No Hyperliquid results computed: only partial days exist." — MLCryptoEngine/progress.md:541-544 (primary evidence outside my assignment; corroborating only).
  - The internal inconsistency is visible inside a single document. The standalone H1 note tabulates all three venues — "| Hyperliquid perps, base tier | 1.5 bps | **3.0 bps** |" (MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md:76) — applies that 3.0 bps line to the 0.03 bps 100 ms capture ("Against the cheapest venue reachable from this operator's jurisdiction at all — Hyperliquid at **3 bps** — it still misses by roughly **100×**", :82-84), and then two sections later compares the 5.00 bps top-decile figure to 80 bps only: "**The best top-confidence decile anywhere in the study captures 5.00 bps, against an 80 bps round trip — missing the economic bar by 16×.**" (:99-101). The 3.0 bps row from its own table is never applied to the number the reopening condition turns on.
  - Live-data check (read-only, UTC 2026-09-05 05:56): `/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/raw/venue=hyperliquid/` holds `date=2026-08-01` … `date=2026-08-13`, i.e. 13 days of Hyperliquid capture existed before recording ended, so the run was affordable in data terms at zero cost. UNANCHORED (working-tree data; may have changed after the anchor).
- **Recomputation (if any):**
  - Inputs: top-decile capture 5.0020 bps (report.md:2298); Hyperliquid maker round trip 3.00 bps (report.md:1114, :4227); Hyperliquid taker 4.5 bps/leg (report.md:773, :4227); Kraken base tier corrected to 0.25% maker = 50 bps round trip (HYPOTHESES.md:442-443).
  - Method: direct ratio of capture to round-trip cost. Script `recompute2.py`.
  - Result: 5.00 vs 80.0 → 0.063 (misses by 16.0×, as published). 5.00 vs 50.0 → 0.100 (misses by 10.0×). **5.00 vs 3.0 → 1.667 (clears).** 5.00 vs 9.0 (both legs taker) → 0.556 (misses by 1.8×). So the deciding ratio inverts under the maker cost mode that H1's own headline and reopening condition are written in, and only survives if both legs are assumed to be takers — an assumption the report never states.
- **What would resolve it:** Run the C.14 confidence-versus-magnitude measurement (and the underlying Phase B fixed-horizon pipeline) on the 13 recorded Hyperliquid days for BTC and ETH at 500 ms – 900 s, and report the top-confidence-decile capture and per-day stability against the venue's own 3.0 bps maker round trip, net of the measured adverse selection (+0.215 bps at 1 s on Hyperliquid BTC, report.md:1200). Either the decile clears 3 bps there — in which case H1's registered reopening condition is met — or it does not, in which case the closure is finally supported at the venue that matters.
- **Confidence:** MEDIUM — the arithmetic inversion is certain and the untested venue is named in the repository's own run config, but the 5.00 bps was measured on Kraken's book (a Kraken fill cannot be paid for at Hyperliquid fees), the 900 s capture is known to be unstable day-to-day (−2.44 to +3.05 bps on Coinbase, report.md:2366), and no per-day stability check is reported for the top-decile figure.
- **Invalidated by later commits?:** no — the anchored SHA is HEAD of the live repository; there are no later commits.
- **Disclosed by authors?:** partially (MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md:76-85) — the H1 note lists Hyperliquid at 3.0 bps and applies it to the 0.03 bps figure, but never applies it to the 5.00 bps top-decile figure that the "does not reopen" sentence rests on, and neither report.md nor the register records that H1 was never tested on that venue.

---

### DRAFT-p1-report-2
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H10 — liquidation aftermath reversion; Stage C.15's "the data does not exist" closure.
- **Direction:** A
- **Class:** ARITHMETIC
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "labeling the recorded week through per-user queries would take one polite request per fill-participant against 2.64M fills — weeks of querying to label seven days of history, and nothing before 2026-08-01 at any price." — MLCryptoEngine/report.md:2668-2670
- **Evidence:**
  - The stated cost is the only thing standing between C.15 and a labelled dataset. The report establishes that the label exists and is reachable: "The venue *does* label liquidations — `userFillsByTime` fills carry a `liquidation` object when the fill was one — but only **per user**: you must already know the liquidated address to ask." (MLCryptoEngine/report.md:2664-2666), and it successfully executed exactly one such lookup: "cross-referencing a recorded zero-hash fill against the venue's own `userFillsByTime` endpoint matched it by `tid` to a fill carrying `twapId` and `dir='Close Short'`" (MLCryptoEngine/report.md:2656-2659).
  - Every recorded fill already carries both participant addresses. The report's own field inventory says so: "Every trade fill in the recorded week — **2,639,510 fills across 116 hour files, 2026-08-01 → 2026-08-06, twelve instruments** — has exactly one key-set: `(coin, hash, px, side, sz, tid, time, users)`." — MLCryptoEngine/report.md:2644-2647.
  - The number of *addresses* is two orders of magnitude below the number of *fills*, and the report never measures it. Measured directly on the live recorded archive (read-only, UTC 2026-09-05 05:58, `/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/raw/venue=hyperliquid/date=2026-08-0{1..6}/hour=*/messages.ndjson.zst`, 126 hour files): **2,953,327 fills** and **62,905 distinct participant addresses**. UNANCHORED (working-tree data). My window is a superset of the report's stated 116-file / 2,639,510-fill window, so 62,905 is an *upper bound* on the distinct-address count inside their window.
  - `userFillsByTime` is a per-address, time-ranged query returning many fills per call, so the query count scales with distinct addresses, not fills — which is the arithmetic the quoted sentence gets wrong ("one polite request per fill-participant against 2.64M fills").
  - The closure this feeds is absolute: "**Identifiable liquidations in the recorded data: zero.**" (MLCryptoEngine/report.md:2678) and the register records H10 as "**Closed — unidentifiable in available data** · 2026-08-06" (MLCryptoEngine/HYPOTHESES.md:163) with a reopening condition that names only external sources — "the venue flagging liquidations in the public trades stream, a global history endpoint, or labeled vendor data — covering **≥ 300 labeled liquidations**" (MLCryptoEngine/HYPOTHESES.md:168). A per-address enumeration of the addresses already recorded is a fourth path the condition does not consider.
- **Recomputation (if any):**
  - Inputs: 62,905 distinct addresses (measured, above); the project's own polite-pacing conventions — "measured median 0.21 s/call + 0.9 s courtesy sleep" (MLCryptoEngine/report.md:3094) and "~0.85 s/report, 6-burst → zero 429s" (MLCryptoEngine/report.md:2950).
  - Method: one request per distinct address × pacing. Script `recompute2.py`.
  - Result: at 1.11 s/request (the project's own GoPlus pacing) → **19.4 hours**; at 0.85 s → 14.9 hours; at a deliberately slow 2.0 s → 34.9 hours. Fills-to-addresses ratio **46.9 : 1** on my window (**42.0 : 1** against the report's own stated fill count). The blocker is therefore overstated by roughly one and a half orders of magnitude: the labelling pass is under a day of free, keyless querying, not "weeks".
- **What would resolve it:** Enumerate the distinct `users` addresses in the recorded week (a single pass over data already on disk), issue one `userFillsByTime` request per address across the week's window, and count how many returned fills carry the `liquidation` object. If the count reaches the register's own ≥ 300-liquidation floor (HYPOTHESES.md:168) the matched-control design specified in H10 runs immediately at zero cost; if it does not, C.15's closure is finally supported by a measured liquidation count rather than by a query-cost estimate.
- **Confidence:** HIGH on the arithmetic (the address count is measured from the repository's own recorded bytes and the endpoint is per-user by the report's own description); MEDIUM on the conclusion, because the venue's rate limits for `userFillsByTime` are not measured anywhere in this repository, and a heavily-paginated market-maker address could need several requests.
- **Invalidated by later commits?:** no — the anchored SHA is HEAD; there are no later commits. The recorded archive is closed (recording ended 2026-08-13, MLCryptoEngine/progress.md:2762-2764), so the input data is fixed.
- **Disclosed by authors?:** no — the report presents the per-fill query count as the reason the labelling path is infeasible and does not report, or estimate, the number of distinct participants; the C.15 "what would make this testable" list (MLCryptoEngine/report.md:2692-2699) names only external data sources.

---

### DRAFT-p1-report-3
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H11 / Stage C.17 — medium-horizon prediction; feature class B (exchange netflow), and the alpha-search-ending FAIL it contributed 8 of 40 cells to.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**But the snapshot retrieved 2026-08-06 ends 2026-05-23: a measured 75-day staleness.** Registered rule says measured lag wins, so every CM feature carries **+75 days**." — MLCryptoEngine/report.md:2734
- **Evidence:**
  - The +75 days is applied as a per-observation publication lag over the whole six-year sample, not just to its final stretch. ADR-042 states the mechanism: "Every feature carries a lag. ``usable_at = metric_date + lag_days``; a decision dated t may read only observations with ``usable_at ≤ t``" (MLCryptoEngine/DECISIONS.md:1871-1873), and the code comment confirms the uniform application: "CM-derived features carry a measured **75-day** lag rather than the +1 default" and "- **B exchange netflow** … Lag +75 days, measured." (MLCryptoEngine/research/medium/features.py:7-9, :17-19). The sample runs "weekly, 2020-08-02 → 2026-07-26" (MLCryptoEngine/report.md:2750).
  - The measured quantity is the end-of-file date of a single snapshot, not a publication delay. Only one snapshot exists on disk: `/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/vendor/archive/coinmetrics/asset=btc/btc_2026-08-06.csv` and `asset=eth/eth_2026-08-06.csv` — read-only, UTC 2026-09-05 06:01, UNANCHORED. There is no second retrieval against which the source's cadence could have been differenced.
  - The whole file stops, not the flow columns. In that snapshot the last fully-populated row is `2026-05-23`; the final row `2026-05-24` carries values only in `ReferenceRate`, `ReferenceRateETH`, `ReferenceRateEUR`, `ReferenceRateUSD`, and is empty in **every** other column including `PriceUSD`, `AdrActCnt`, `TxCnt`, `SplyCur` and the `FlowInEx*`/`FlowOutEx*` columns (header positions 1–32 read out in my scratch log; last row verbatim: `2026-05-24,,,,,,,,,,,,,,,,,,,,,76619.8666090415,36.2068863443055,66037.9790137651,76619.8666090415,,,,,,,`). A daily close price is not published 75 days late by any provider; the gap therefore measures when the free GitHub mirror (`https://raw.githubusercontent.com/coinmetrics/data/master/csv/{asset}.csv`, MLCryptoEngine/research/medium/data.py:37) stopped regenerating, not the delay with which exchange-flow metrics become knowable.
  - The consequence is load-bearing. Class B supplied 8 of the 40 cells in the grid whose unanimous FAIL ended the alpha search — "**FAIL.** No cell passes all six registered bars" and "the alpha search of this project ends by decision, dated 2026-08-06" (MLCryptoEngine/report.md:2840, :2847-2848) — and class B was one of only two classes with a majority of positive cells ("Class consistency … B 7/8", MLCryptoEngine/report.md:2797-2798). Those cells were scored with the netflow feature **10.7 weeks stale at horizons of 1, 2, 4 and 8 weeks** (MLCryptoEngine/report.md:2754-2771), i.e. at the 1-week horizon the feature predates the decision by more than ten times the horizon.
  - The register makes the same figure the binding constraint on reopening: "**(a)** a free exchange-flow source at **≤ 2-day** publication lag with **≥ 3 years** of history — the measured 75-day staleness is the binding data constraint on class B" (MLCryptoEngine/HYPOTHESES.md:185). If the 75 days is a mirror stall rather than a publication lag, the source already in the project's own manifest may satisfy that condition.
- **Recomputation (if any):**
  - Inputs: lag 75 days (report.md:2734); horizons {1, 2, 4, 8} weeks (report.md:2720).
  - Method: express the applied lag in units of the shortest scored horizon.
  - Result: 75 d / 7 d = **10.7 weeks of staleness against a 1-week horizon (10.7×) and against an 8-week horizon (1.34×)**. A feature that is ten horizons old cannot be expected to carry horizon-scale information, so class B's 1- and 2-week cells were close to structurally guaranteed to fail regardless of the underlying signal. No recomputation of class B's returns is possible from the published tables; the lag is the only lever and it was set from one file's end date.
- **What would resolve it:** Measure the source's actual per-row publication delay instead of one snapshot's end date — the CM community CSVs live in a public git repository, so `git log` on the file gives, for each metric date, the commit date at which that row first appeared, at zero cost and with no key. Then re-run the class B and class E cells with the measured per-row lag (and apply +75 days only to the tail where the mirror had genuinely stalled). If class B still fails, the alpha-search closure is supported on a fair test of the class; if it does not, C.17's FAIL — and the decision it triggered — rests on a handicap the data did not justify.
- **Confidence:** MEDIUM — the fact that `PriceUSD` also stops at 2026-05-23 is decisive that the gap is not a flow-metric publication delay, but I cannot verify the mirror's historical cadence from inside this repository (only one snapshot exists and I did not fetch anything), and even at lag +1 class B's long-only cells carry beta 0.43–0.56 (report.md:2764-2771) and would likely still be judged the pre-registered beta artifact.
- **Invalidated by later commits?:** no — the anchored SHA is HEAD; there are no later commits.
- **Disclosed by authors?:** no — ADR-042 presents the 75 days as the measured publication lag of the class and treats the override as the stage's methodological win ("Without the measured override, class B would have shown the freshest signal in the study on data no free operator could have had", MLCryptoEngine/DECISIONS.md:1890-1892); nothing in report.md, DECISIONS.md or HYPOTHESES.md records that the same snapshot's price column stops on the same date, or that only one snapshot was ever taken.

---

### DRAFT-p1-report-4
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H11 / Stage C.17 — the deflated-Sharpe bar as applied to feature class D (basis), the only class that reached four of six registered bars.
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The best deflated Sharpe in the grid is 0.499 against a bar of 0.95; the best alpha t is 1.35 against a bar of 2.**" — MLCryptoEngine/report.md:2798-2799
- **Evidence:**
  - A single DSR threshold (≥ 0.95 at n_trials = 40, MLCryptoEngine/report.md:2722-2724) was applied across cells whose scored windows differ by 4.6×: classes A–C score **193–207 weeks**, classes D–E score **45–59 weeks** (MLCryptoEngine/report.md:2756-2795). The report names the short window as a *reason to distrust* class D — "Sharpe 0.89–1.62, returns 37–87%/yr — and **45–59 scored weeks**" (MLCryptoEngine/report.md:2815) — but nowhere states that the short window also makes the two statistical bars mechanically harder for exactly that class.
  - Class D failed only the two bars whose stringency scales with n: "The two cells reaching four of six bars (D/h2w, both variants) fail precisely the two bars that measure evidence rather than return: alpha significance and deflation." — MLCryptoEngine/report.md:2834-2836.
  - The benchmark on class D's own window is itself high: "On those same windows **buy-and-hold BTC's Sharpe is 1.16–2.06**" (MLCryptoEngine/report.md:2818-2819), and the best cell D/h2w/LS posts an annualised net Sharpe of 1.616 on n = 57 weeks against a same-window BTC Sharpe of 1.386 (MLCryptoEngine/report.md:2783).
- **Recomputation (if any):**
  - Inputs: n_trials = 40 and DSR bar 0.95 (report.md:2722-2724); scored weeks n = 45, 57, 59, 201, 207 (report.md:2756-2795); best cell annualised Sharpe 1.616 at n = 57 with reported DSR 0.499 (report.md:2783); same-window BTC Sharpe 1.386 (report.md:2783).
  - Method: Bailey & López de Prado deflated Sharpe, with the expected-maximum benchmark `SR0 = sqrt(Var[SR])·[(1−γ)Z(1−1/N) + γ Z(1−1/(Ne))]` and `Var[SR] ≈ 1/n` — the same estimator C.10 reports, which my implementation reproduces to within 3% (C.10 states "expected max per-bar Sharpe under the null, 1,653 trials | **0.1058**" at n = 1,095, report.md:1590; my value 0.1026). Solved for the per-week Sharpe at which DSR = 0.95, ignoring skew and at kurtosis 3. Scripts `recompute.py`, `recompute2.py`.
  - Result: at **n = 57 weeks** the bar demands an annualised Sharpe of **3.78**; at **n = 207 weeks** it demands **1.94** — the identical bar is **1.95× harder** for class D purely because its window is shorter. 3.78 is **2.73× the buy-and-hold BTC Sharpe on class D's own window** (1.386). Because my SR0 is stricter than theirs, I also solved under the report's own implied calibration (their DSR of 0.499 at Sharpe 1.616 implies SR0 ≈ SR_hat, i.e. 1.616 annualised): the required annualised Sharpe is then **3.28**, still **2.37×** the same-window benchmark. On either calibration, no class-D cell could have cleared bar 3 at any plausible effect size on a 45–59-week window.
- **What would resolve it:** Either extend class D's window — the Hyperliquid premium series starts 2023-05 (report.md:2816), but a perpetual-basis series back to 2020 is constructible free from the Binance USD-M archive this project already uses for funding ("Binance perps 2020-01 to 2026-07, 8-hourly", report.md:1655; `data.binance.vision`, report.md:1423) — and re-run the class at n ≈ 300 weeks where the bar is reachable; or state in the report that classes D and E faced a bar their window made unreachable, so that the FAIL is read as "insufficient window" rather than as evidence against the class.
- **Confidence:** MEDIUM — the asymmetry is arithmetic and reproduces the project's own C.10 estimator, but the report gives several *independent* substantive reasons to reject class D (beta up to 0.96, a single-regime window, earnings concentrated in one trend direction — report.md:2814-2824), any one of which would fail the class even with an achievable DSR bar.
- **Invalidated by later commits?:** no — the anchored SHA is HEAD; there are no later commits.
- **Disclosed by authors?:** partially (MLCryptoEngine/report.md:2815, HYPOTHESES.md:183) — the short window is disclosed and used as a criticism of class D, and H11's reopening condition asks for "≥ 156 scored weeks"; what is not disclosed is that the registered DSR and alpha-t bars were therefore unreachable for that class before any data was seen.

---

### DRAFT-p1-report-5
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H2 — transfer of the Phase B edge to CME micro futures; Stage C.8's closure on MBT alone.
- **Direction:** A
- **Class:** UNDER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "and MES, which is 2.49x MBT's event rate on a 5.2x larger notional, so its costs in bps are ~7x lower and the same gross edge would clear them." — MLCryptoEngine/report.md:1086-1088
- **Evidence:**
  - This is the stage's own list of what would change its answer, and the item it puts last in "order of cheapness" — "The open possibilities, in order of cheapness: a regime that is not a two-month uptrend; cross-venue features against the crypto recorders …; and MES" (MLCryptoEngine/report.md:1084-1087). The middle item *was* followed up (C.14 §3 measured cross-venue features at ΔAUC ≤ +0.0044, report.md:2399-2401). MES was not; nor was the regime item ("CME was not re-run", report.md:2490-2491).
  - The register closed H2 on MBT alone the same day: "**Closed — signal-absent** · 2026-08-03", deciding number "**AUC 0.501** at every horizon, and **0.22 bps** gross capture against **5.33 bps** cost. CME MBT (micro bitcoin) via Databento", sample "two validated MBT months (2026-04, 2026-05)" (MLCryptoEngine/HYPOTHESES.md:65-67), and its reopening condition names precisely the untested axis: "Reopens only on evidence of measurable AUC on a *different* instrument or feature class" (MLCryptoEngine/HYPOTHESES.md:70).
  - MES data is already bought, validated and on disk. report.md records "### cme MES.c.0 — 2026-07-31 — **PASS** (vendor, `mbp-10`)" with "Events: **14,989,106** · scheduled open: 21.00 h · covered: 21.00 h (100.00%)" (MLCryptoEngine/report.md:1376-1378) — against MBT's FAIL at 71.49% coverage on the same date (report.md:1364-1368). Live read-only check (UTC 2026-09-05 06:02): `data/vendor/databento/GLBX.MDP3/date=2026-07-15/` and `date=2026-07-31/` each contain `MES_c_0.mbp-10.dbn.zst` and `MES_c_0.trades.dbn.zst` (394 MB and 374 MB per date dir). UNANCHORED. A first Phase B run on MES therefore costs **$0** and is the same one-day scale as the evidence H1 was originally closed on ("Data range: 2026-07-31", report.md:681).
  - The cost gap that C.8's sentence rests on is measured elsewhere in the same document: MES round trip **0.642 bps** on a $38,027 notional versus MBT **6.211 bps** on $6,505 (MLCryptoEngine/report.md:1161, :1164).
  - The capability question was settled in MES's favour and never revisited for research: ADR-018 records MES at 10,649,955 book updates and a 50 ms median trade interval against MBT's 4,275,234 and 1,000 ms on the same mid-life session (MLCryptoEngine/DECISIONS.md:666-671).
- **Recomputation (if any):**
  - Inputs: MBT best gross capture **+0.215 bps at 900 s** (report.md:1009); MES round-trip cost **0.642 bps** (report.md:1161); MBT round-trip cost 5.325–6.211 bps (report.md:997, :1164).
  - Method: compare MBT's own best measured capture against MES's measured cost.
  - Result: **0.215 bps < 0.642 bps** — carrying MBT's own capture across to MES's cost still fails, by ~3.0×, not the ~24× it fails by on MBT. So MES is *not* an obvious rescue and I say so plainly; the honest claim is narrower: the named cheapest-open-possibility, on an instrument the register's own reopening condition asks for, with a validated day already paid for, was never run, and the gap between the measured capture and the measured cost narrows from 24× to 3× when it is.
- **What would resolve it:** One Phase B research run on `MES.c.0` for 2026-07-31 (data on disk, zero spend), reporting AUC by horizon and gross capture against the measured 0.642 bps round trip, exactly as the MBT run at report.md:897-922 does. That either produces the "measurable AUC on a different instrument" H2's reopening condition asks for, or closes the last cheap door C.8 left open.
- **Confidence:** MEDIUM — that MES was never run is verifiable from the report's own section headings, and the instrument is named by the stage itself; but my own recomputation shows MES would need roughly 3× MBT's best gross capture to clear, so this is an untested door rather than a demonstrable error.
- **Invalidated by later commits?:** no — the anchored SHA is HEAD; there are no later commits.
- **Disclosed by authors?:** partially (MLCryptoEngine/progress.md:875-885) — a C.5 note records the deliberate choice not to buy MES history ("MES is a different asset class and answers a new question rather than the open one") and prices a multi-month MES backfill at ~$287–574; what is not disclosed anywhere is that a validated MES day is already on disk, so a first look needs no purchase at all.

---

### DRAFT-p1-report-6
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 — the screened-positive demotion registered at D.1c kill condition 4, and the D.1b blind-universe window and D.1a ≥ 4-week re-run that were registered to resolve it.
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "the blind window closing **2026-09-09** remains the first unbiased test — its role after this closure is to check the selection-bias question, since any future survivor would face this same replay gate." — MLCryptoEngine/report.md:4993-4995
- **Evidence:**
  - D.1c found the C.9 selection was outcome-linked and demoted the survivors accordingly: "PUMP's own annotation reads '**first above cost**' … **Consequence, per the registered condition: the survivors are demoted to screened positives.**" (MLCryptoEngine/report.md:4509-4525). The remedy was registered as a blind universe with a fixed seed and a fresh window: "**Earliest window close: subscription date + 28 days — subscribing 2026-08-12 puts that at 2026-09-09**" (MLCryptoEngine/report.md:4604-4607), applied and subscribed the same day ("25 blind picks + PUMP and MERL carried over … = 27 subscribed instruments", report.md:4654-4655).
  - Two further standing commitments in report.md depend on the recorders continuing: "**A usable distribution (7 days spanning the daily cycle, ~10,080 samples) exists on 2026-08-19.**" (MLCryptoEngine/report.md:4634-4635) and "a D.1 conclusion resting on more than one week needs the bounded measure re-run on **≥ 4 weeks spanning more than one volatility regime** — which the recorders accrue at zero cost, reaching that by roughly 2026-09-08." (MLCryptoEngine/report.md:4252-4255).
  - Recording was stopped one day into the 28-day window: "**Recording stopped 2026-08-13T05:02:49Z.** `mlce-recorder` and `mlce-telemetry` were stopped and disabled through systemd" and "The 27-instrument blind universe subscribed on 2026-08-12 is therefore left with 1 day of capture and is **not** a scoreable window; it should not be treated as one." — MLCryptoEngine/progress.md:2762-2784 (primary evidence outside my assignment). Confirmed against the live working tree (read-only, UTC 2026-09-05 06:03): `data/raw/venue=hyperliquid/` ends at `date=2026-08-13`. UNANCHORED.
  - report.md is not amended anywhere for this, and neither is the register: HYPOTHESES.md:197 still reads "The blind window closing 2026-09-09 still reads out — as a selection-bias check, since any future survivor faces this same replay gate", and HYPOTHESES.md:265 lists "the blind-universe scoring window (2026-09-09, now a selection-bias check)" as an item on the record. The same file's H7 closure note also still asserts "The three-venue overlap keeps accumulating at zero cost" (MLCryptoEngine/HYPOTHESES.md:220), which the retirement at D.1b and the 2026-08-13 stop both contradict (and which HYPOTHESES.md:506-508 separately acknowledges).
- **Recomputation (if any):**
  - Inputs: window opened 2026-08-12 (report.md:4657-4659), earliest close 2026-09-09 (report.md:4606, :4706), recording stopped 2026-08-13 (progress.md:2764), Hyperliquid capture directory ends `date=2026-08-13`.
  - Method: elapsed days of the registered window that were actually recorded.
  - Result: **1 of 28 days (3.6%)**. The latency clock ran 1 of its 7 registered days. Both pre-registered follow-ups are permanently unreachable on this archive, so the D.1c screened-positive demotion of PUMP and MERL — and with it the multiplicity caveat that "BH q=0.10 was corrected across the 10 tested, not the 177 screened" (report.md:4522-4524) — can never be discharged.
- **What would resolve it:** Amend report.md §D.1d.5 and the H6 register row to state that the blind window and the ≥ 4-week re-run were terminated at 1 of 28 days on 2026-08-13, that the screened-positive demotion is therefore permanent and the C.27 multiplicity accounting stands uncorrected for the 177-perp screen — or restart the recorder (one config flip, ADR-060) and let the registered window run.
- **Confidence:** HIGH — the dates and the directory listing are unambiguous, and the two documents contradict each other at the same SHA.
- **Invalidated by later commits?:** no — the anchored SHA is HEAD; there are no later commits, so the contradiction stands as published.
- **Disclosed by authors?:** partially (MLCryptoEngine/progress.md:2762-2784) — the stop and its rationale are recorded openly and honestly in progress.md, including the explicit warning not to treat the blind universe as scoreable; but report.md and HYPOTHESES.md, the two documents a reader is directed to ("`HYPOTHESES.md` for the register and every reopening condition", progress.md:2800-2802), both still present the window as one that will read out.

---

### DRAFT-p1-report-7
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 — spread capture on thin perpetuals; the scope of the "H6 closes" label against the instrument set the deciding fill model was run on.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**NOT (+31) and TNSR (+35)** are wide-spread but sub-capacity — a spread you are filled against a few hundred times a day at $60–70k daily volume is the \"positive but rare\" case the register named: report the arithmetic and stop." — MLCryptoEngine/report.md:4083-4085
- **Evidence:**
  - The census table shows NOT and TNSR with the two largest nets by a wide margin and every non-capacity bar cleared: "| NOT | 3,312 | +31.15 | +30.26 | yes | **no** ($71k med) | positive_but_rare |" and "| TNSR | 5,235 | +35.50 | +34.91 | yes | **no** ($63k med) | positive_but_rare |" — MLCryptoEngine/report.md:4057-4058. The survivors that carried H6 forward were an order of magnitude smaller: GMX +0.40, PUMP +4.30, MERL +6.45 (report.md:4054-4056).
  - The capacity tier has two clauses and they miss only one: "**Capacity tier:** ≥ 150 trades/day AND ≥ $100,000 median daily volume" (MLCryptoEngine/report.md:2887-2888).
  - Both remained economically live to the end: D.1c re-scored all ten at 300 s and 900 s and reports "NOT and TNSR stay hugely positive and remain sub-capacity" (MLCryptoEngine/report.md:4498-4499), i.e. the longer-horizon test that vindicated the GMX discount did not touch them. NOT then re-entered the blind universe as a genuine blind pick — "| B4 $10–100k | 23 | 6 | BIGTIME, COMP, DYM, KAS, NOT, SAGA |" (MLCryptoEngine/report.md:4652).
  - The closure, however, is stated without scope: "**By the registered kill condition, verbatim: the tightened net at the declared cap and the latency floor is ≤ 0 for both instruments, so H6 closes and D.2 does not follow.**" (MLCryptoEngine/report.md:4973-4975) — "both instruments" being PUMP and MERL only. The D.1d order-lifecycle model was never run on NOT or TNSR, and the D.1d caveat list (report.md:4987-5003) does not mention them.
- **Recomputation (if any):**
  - Inputs: NOT 3,312 trades and TNSR 5,235 trades over the 7-day census window (report.md:4057-4058); capacity floors 150 trades/day and $100k median daily volume (report.md:2887-2888); medians $71k and $63k (report.md:4057-4058); the D.1d fall on PUMP, +4.30 → −4.75 bps (report.md:4879-4880). Script `recompute2.py`.
  - Method: per-day trade rates; shortfall against the volume floor; the D.1d haircut applied to the census nets; a 100%-of-flow and a 10%-of-flow revenue ceiling.
  - Result: NOT **473 trades/day**, TNSR **748 trades/day** — both clear the 150/day clause by 3–5×; they fail only the volume clause, by **29%** and **37%**. Applying the full PUMP order-lifecycle haircut of 9.05 bps leaves NOT at **+22.1 bps** and TNSR at **+26.5 bps**. Revenue ceiling at 100% of the venue's own median daily volume: ~$221/day (NOT) and ~$224/day (TNSR), i.e. **~$81k/yr each** — and at a more realistic 10% share, ~$8k/yr each. So the "rare" label is right about deployable size and understated about margin: the two excluded instruments carry 7–8× the survivors' net and would survive the very model that closed H6.
- **What would resolve it:** Either run the D.1d bounded replay on NOT and TNSR from the recorded census week (data on disk, zero cost) and report their tightened nets alongside PUMP's and MERL's, or restate the closure with its scope — "H6 closes for the two capacity-clearing survivors; the two sub-capacity positives were never put through the fill model" — in report.md §D.1d.5 and the H6 register row.
- **Confidence:** MEDIUM — the arithmetic is straightforward from the report's own table, but the exclusion was pre-registered before the numbers existed (report.md:2887-2888, :2892-2897) and honestly executed, and $60–70k/day of venue volume genuinely cannot support meaningful deployed size, so this is a scope-of-label finding rather than a wrong number.
- **Invalidated by later commits?:** no — the anchored SHA is HEAD; there are no later commits.
- **Disclosed by authors?:** yes (MLCryptoEngine/report.md:4083-4085 and :4057-4058) — the exclusion, its reason and the two instruments' nets are all published, and the outcome-to-action map registered "survivors below capacity → report the fill-frequency arithmetic and stop" in advance (report.md:2893-2894). What is not disclosed is that the unqualified "H6 closes" sentence covers instruments the deciding model never scored.

---

## What I checked and found sound

Everything below is where I looked for the Direction-A thesis and did not find it, or found the project had already done the work.

- **C.9's own reopening trigger was honoured.** C.9 registered "Re-run this census in a week. If the thin end survives spread − adverse − cost there, that is the first positive result this project has produced and it earns a fill simulation" (report.md:1247-1250). C.18 pre-registered the bars before the window closed (report.md:2872-2897), C.27 ran it on the registered date and reported a *positive* against the project's own expectation (report.md:4001-4006). This is the pattern a Direction-A audit hopes to break and could not.
- **The known-answer gates are real and were re-audited.** C.18/C.27 reproduce C.9's closed BTC/ETH nets to −0.001 / −0.003 bps (report.md:2906-2911, :4035-4037), and where a gate turned out to be vacuous the project withdrew it in place rather than defending it: "In `generous` mode the engine short-circuits its entire order machine … execute **zero times** under this gate" (report.md:4823-4834) and the replacement differential test then "found a real defect on its first run" (report.md:5097-5099).
- **C.14's cross-venue A/B closed a genuine loose end rather than assuming it.** The feature class that was 100% NaN in C.8 was measured where it could be computed (coverage 67–100%) and found worth ΔAUC ≤ +0.0044 (report.md:2393-2411). That is the correct treatment of "absent is not zero".
- **C.14's deep-learning bar was pre-registered and the leakage canary demonstrably fires** (planted-future AUC 0.9714, label-shift control 0.5268 — report.md:2439-2450). A null result from a probe that can fire is informative; I checked whether the bar was set unreachably and it is not — the models scored *below* the baseline, not merely short of it (report.md:2426-2435).
- **C.10's deflated Sharpe is not a harsh label.** I checked whether "the benchmark exceeds the result" was arithmetic sleight of hand: the best pair's per-bar Sharpe of 0.0514 really is less than half the 0.1058 expected maximum under 1,653 trials (report.md:1588-1597), and my own implementation of that estimator returns 0.1026 on the same inputs — the report's figure is if anything slightly conservative against itself.
- **C.16's momentum FAIL survives a look for a harsher-than-warranted label.** The three specifications that beat the benchmark are all at one holding period (report.md:2555-2563), which the registration named as an artifact pattern in advance (report.md:2516-2518), and the executable subset collapses to Sharpe 0.013 (report.md:2599-2603). The full grid is published with nothing dropped.
- **C.11 (H5) is closed as "decayed, not disproved" with a live-measured reopening threshold** — "Current funding above roughly 10% annualised sustained for a quarter" (HYPOTHESES.md:118). I checked later entries in this repository for a trigger: C.13 measures the 2026 cross-section level at −9.23% (report.md:2039) and C.11 measures 2026 BTC funding at 1.94% (report.md:1709). No trigger is met.
- **C.13's parameter sweep is published in full including the cells that flatter it** (1-day +7.32%, 3-day +21.51% against the 7-day base spec's +0.11% — report.md:2177-2183), with the drawdowns beside them (−72% to −88%) and the non-monotonicity used as the argument for noise. I looked for a suppressed favourable cell and found the opposite.
- **C.22/C.23 removed their own preferred excuses before closing.** C.21's dominant feature `creator_allocation_t0` (147/169 importance) is reported as collapsing to 0 at larger n (report.md:3315-3319), and C.23's v0-versus-decontaminated control on the identical fold is exactly the right test for "signal or sample" (report.md:3363-3371).
- **C.24/C.25 registered their interpretation rule before seeing the strata and then reported against it when it hurt** — the high-activity stratum that carried C.24's headline collapses +0.156 → +0.015 under the correction (report.md:3806-3813), and C.26's firming sweep is reported as having moved the estimate *down* (report.md:3947-3953).
- **C.26's "measured-unaffordable" closure is labelled as a decision, not a fact** — "The cap is self-imposed, not a Helius tier limit, so this is a deliberate decision" (report.md:3929-3931). I probed whether a cheaper sufficient version was available (decontaminating only the 2024 test fold rather than all 258 honest pools) and could not price it from the published tables well enough to make a defensible finding; the ~124,764 figure is at ~2× the cap either way.
- **D.1a's go/no-go is honest about which clause fired**: the estimability bar failed by a wide margin (median absolute error 100% against a 25% threshold) and the GO rests only on the pessimistic-bound clause (report.md:4189-4215). A weaker project would have reported the GO without the failure.
- **The D.1d corrections section moves every corrected figure in the *unfavourable* direction and says so** (PUMP −4.75 → −4.81, MERL −4.23 → −4.35; report.md:5048-5057), withdraws the mechanism claim while keeping the closure (report.md:5108-5116), and demotes GMX from survivor to unresolved on the A3 interval correction (report.md:5148-5153).
- **The validation-run history (report.md:49-676, 1253-1385, 1866-2009) is a record of failing its own acceptance criteria repeatedly before passing**, including the pointed self-check "kraken: declares CRC32 book checksums but 0 were verified — a zero checksum-failure count here is evidence of absence, not of integrity" (report.md:345). I found no instance of a FAIL being relabelled.
- **C.14's stated coverage reduction** — "The ETH pair on both venues was **not run**: the full four-symbol stride-1 sweep is roughly five hours of LightGBM fits and this stage had a deadline. That is a real reduction in coverage and it is stated rather than omitted" (report.md:2276-2279) — is a named-but-unrun variant, but it is disclosed in the same breath, sits on the same venues whose cost already dominates the verdict, and would not move the deciding arithmetic. Recorded here rather than raised as a finding.
- **README.md** (all 83 lines) contains no closure claim, no deciding figure and no reopening condition; its only substantive research statement is the one-line summary of the H1 note (README.md:75), which is consistent with report.md §C.14. Nothing in it supports a Direction-A finding on its own.

---

## Live-repo access log

Live repository touched: `/home/kiros-li/Documents/GitHub/MLCryptoEngine` — read-only only (`git status --porcelain`, `git log --oneline`, `ls`, `find`, `du`, `head`, `tail`, `zstdcat` piped to `grep`/`sort`/`wc`). No file in the audited repository was opened for writing; all outputs went to `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-mlcrypto-p1-report/`.

Before (UTC 2026-09-05 05:55:00), `git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain`:

```
```
(empty — working tree clean)

After (UTC 2026-09-05 06:03:49), `git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain`:

```
```
(empty — working tree clean; unchanged)

Unanchored working-tree data read, with UTC read times:
- `data/raw/venue=hyperliquid/date=2026-08-01..2026-08-06/hour=*/messages.ndjson.zst` (126 files) — 2026-09-05 05:58 — distinct participant-address count and fill count for DRAFT-p1-report-2.
- `data/raw/venue=hyperliquid/` directory listing — 2026-09-05 05:56 and 06:03 — capture date range for DRAFT-p1-report-1 and -6.
- `data/vendor/archive/coinmetrics/asset=btc/btc_2026-08-06.csv` (header and last three rows only) and the `asset=eth` sibling filename — 2026-09-05 06:01 — for DRAFT-p1-report-3.
- `data/vendor/databento/GLBX.MDP3/` directory listing and `du -sh` — 2026-09-05 06:02 — for DRAFT-p1-report-5.

No `.env`, keystore, session, credential or key file was opened. No repository script was executed.
