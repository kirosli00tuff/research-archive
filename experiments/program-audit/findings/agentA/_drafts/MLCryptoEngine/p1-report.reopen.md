# REOPEN LEDGER — MLCryptoEngine, part p1-report

Repository: MLCryptoEngine @ `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22; this SHA is HEAD of the live repository).
Scope: the entries covered by my assigned documents — `report.md` (read in full) and `README.md`. Stage sections live in `report.md`; the register rows live in `HYPOTHESES.md`, which is another reader's document — every `HYPOTHESES.md` citation below is marked **[reg]** and is given for completeness of the ledger, not as primary evidence.

This ledger is factual, not advocacy.

**Project-wide facts that condition every "awaiting data" entry below:**
- Kraken and Coinbase recorders were retired 2026-08-12 — MLCryptoEngine/report.md:4662-4686.
- **All recording stopped 2026-08-13T05:02:49Z** — MLCryptoEngine/progress.md:2762-2768 [outside my assignment]. `report.md` is not amended for this anywhere; its forward-looking dates (2026-08-19, 2026-09-08, 2026-09-09) at :4606, :4635, :4704-4708, :4794, :4952, :4993 all refer to clocks that stopped after 1 of 7 and 1 of 28 days.
- Databento vendor spend ledger stands at $81.3416 of a $120.00 self-imposed cap — MLCryptoEngine/progress.md:1007-1011 [outside my assignment].
- Helius credit ledger stands at 58,801 of a 60,000 self-imposed cap (1,199 remaining) — MLCryptoEngine/report.md:3998-3999.

---

## H1 — Short-horizon directional prediction on crypto spot

| field | value |
|---|---|
| **Status** | closed |
| **Closure kind** | cost-bound |
| **Closure date** | 2026-08-03 (strengthened 2026-08-05 by C.14) |
| **Deciding figure (n)** | 3.31 bps gross capture at 900 s vs 80.00 bps round-trip maker cost, AUC 0.596, Coinbase BTC-USD, n = 29,838 (report.md:801, :979); superseded by C.14 — top-confidence decile 5.0020 bps vs 80 bps round trip, Kraken BTC/USD 900 s, n = 165,075 over 6 days (report.md:2289, :2298, :2328-2330); and by the four-day 900 s capture range −2.4378 to +3.0497 bps, Coinbase (report.md:2366) |
| **file:line** | report.md:2328-2330 (deciding sentence); report.md:2289-2298 (table); report.md:801 (Phase B origin) |
| **Blockers stated** | 80 bps round-trip retail spot fee (report.md:681, :773); 0-bps maker tiers requiring $250M (Coinbase) / $10M (Kraken) trailing 30-day volume, "Neither is reachable at this project's capital" [reg] HYPOTHESES.md:54; ETH pair not run in C.14 for time (report.md:2276-2279); six days is not six regimes (report.md:2488-2490) |
| **Registered reopen conditions** | "A round-trip cost below roughly **3 bps**, i.e. under 1.5 bps per side … **Reopens on cost, not on modelling** … It does not reopen on more data at the same venues." [reg] HYPOTHESES.md:54, quoted verbatim at docs/notes/h1-predictability-without-capturability.md:261. Additional condition added by C.14: "Reopening now additionally requires the top-confidence decile to clear a round trip somewhere, which it does not." [reg] HYPOTHESES.md:54; report.md:2495-2497 |
| **Trigger already met inside this repository?** | **Arguably yes.** Hyperliquid base tier is 1.5 bps/side = 3.00 bps round trip with no volume requirement — report.md:1114 (verified 2026-08-01) and report.md:4226-4227 (re-verified 2026-08-11). The condition's own text considers only Coinbase and Kraken tiers. The C.14 top-decile figure of 5.0020 bps exceeds 3.00 bps. See DRAFT-p1-report-1. |
| **Possibly met by a different repository?** | Yes — flag for the cross-repo pass: any repository holding a measured sub-3-bps round-trip venue reachable from British Columbia, or a maker-rebate schedule. |

## H2 — Transfer of that edge to CME micro futures

| field | value |
|---|---|
| **Status** | closed |
| **Closure kind** | signal-absent |
| **Closure date** | 2026-08-03 |
| **Deciding figure (n)** | AUC 0.501 and +0.215 bps gross capture at 900 s against 5.33 bps round-trip cost; best net EV −5.11 bps; CME MBT, n = 1,101,582 at 900 s / 1,109,072 valid samples over 53 days (report.md:899, :917, :981, :1009). Control at stride 1, 10 days, n = 896,018: gross capture −0.785 bps, AUC 0.490 (report.md:952, :1029-1032) |
| **file:line** | report.md:974-992 (verdict), report.md:1000-1013 (per-horizon table) |
| **Blockers stated** | all seven cross-venue features 100% NaN on the April–May CME sample because the crypto recorders started later (report.md:1053-1057); only one volatility regime covered (report.md:966-972); walk-forward yields "one complete train/test split", not three (report.md:1069-1077); the June/July MBT backfill did not fit the $120 cap (progress.md:1007-1011 [outside my assignment]) |
| **Registered reopen conditions** | "The open possibilities, in order of cheapness: a regime that is not a two-month uptrend; cross-venue features against the crypto recorders …; and MES, which is 2.49x MBT's event rate on a 5.2x larger notional, so its costs in bps are ~7x lower" — report.md:1084-1088. Register form: "Reopens only on evidence of measurable AUC on a *different* instrument or feature class — never on a re-run of the same pipeline against the same contract with a stronger learner." [reg] HYPOTHESES.md:70 |
| **Trigger already met inside this repository?** | Partly retired: the cross-venue item was tested and found immaterial (ΔAUC ≤ +0.0044, report.md:2399-2411). The **regime** item and the **MES** item were never run; MES.c.0 2026-07-31 is validated PASS with 14,989,106 events and already on disk (report.md:1376-1378). See DRAFT-p1-report-5. |
| **Possibly met by a different repository?** | Yes — flag: any repository reporting measurable AUC on a different futures instrument or a feature class MLCryptoEngine has not tested. |

## H3 — Passive spread capture

| field | value |
|---|---|
| **Status** | closed (with a tail routed to H6) |
| **Closure kind** | cost-bound |
| **Closure date** | 2026-08-03 |
| **Deciding figure (n)** | spread − adverse − cost: Hyperliquid BTC −3.05 (n = 491,982 trades), Hyperliquid ETH −2.75 (n = 278,835), CME MBT −4.25 (n = 148,768) — report.md:1198-1214. 28-instrument survey: no spread-to-cost ratio above 1.0, best M6A micro AUD 0.98 (report.md:1156, :1167) |
| **file:line** | report.md:1208-1221, :1231-1238 |
| **Blockers stated** | "This assumes a fill, which no part of this pipeline models" — every figure an upper bound (report.md:1223-1229); CME bbo-1s carries no trades so adverse selection cannot be measured on the thin CME tail (report.md:1243-1245); 2YY/5YY a failed measurement (report.md:1180-1186); yield contracts unratioable (report.md:1178, :1182-1183) |
| **Registered reopen conditions** | "Re-run this census in a week. If the thin end survives spread − adverse − cost there, that is the first positive result this project has produced and it earns a fill simulation" — report.md:1247-1251. Register form: a maker-rebate venue, or an instrument whose ratio exceeds 1.0 with adverse selection below the excess [reg] HYPOTHESES.md:86 |
| **Trigger already met inside this repository?** | **Yes, and honoured.** The re-run is C.18/C.27; three instruments cleared, H6 opened as the tail (report.md:2864-2925, :4001-4106). |
| **Possibly met by a different repository?** | Yes — flag: any repository documenting a reachable maker-rebate venue. |

## H4 — Cointegration pairs trading

| field | value |
|---|---|
| **Status** | closed |
| **Closure kind** | signal-absent |
| **Closure date** | 2026-08-04 |
| **Deciding figure (n)** | 0 of 180 formation-window BH survivors still significant out of sample (175 re-testable, 18 = 10.3% significant uncorrected against a 5.9% base rate); holdout 91 raw hits vs 77.0 expected; deflated Sharpe of the best pair 0.026 on n = 1,095 observations across 1,653 trials — report.md:1462, :1474-1479, :1588-1593 |
| **file:line** | report.md:1605-1628 |
| **Blockers stated** | universe built from Binance daily bars, "a venue this project cannot trade" (report.md:1388-1394); rests on Binance not purging delisted directories (report.md:1430-1432); only 5 of 12 subscribed perps existed at 2021-08 (report.md:1526-1529); power floor removes 132 of 175 pairs (report.md:1495, :1522) |
| **Registered reopen conditions** | "(a) a reachable venue offers shorts across a materially broader instrument set … **and** (b) relationships persist out of sample, which they did not at any correction level" [reg] HYPOTHESES.md:102 |
| **Trigger already met inside this repository?** | No. The 2024-06→2026-07 executable re-screen produced 1 raw hit against 1.8 expected and 0 survivors (report.md:1555-1563). |
| **Possibly met by a different repository?** | Partly — flag: any repository documenting a reachable venue offering shorts on a materially broader crypto instrument set. Clause (b) is internal and unmet. |

## H5 — Funding rate carry

| field | value |
|---|---|
| **Status** | closed |
| **Closure kind** | currently unattractive — decayed, not disproved |
| **Closure date** | 2026-08-04 |
| **Deciding figure (n)** | 8.07% (ETH) / 8.00% (BTC) net annualised on deployed capital, 5 of 10 modelled instruments clearing a 4% risk-free rate; against 2026 funding of 1.94% (BTC) and 0.97% (ETH), at which "the trade does not clear cash at all". n = 27,761 hourly funding rows for BTC over 3.23 years — report.md:1653, :1709-1710, :1764-1765, :1831-1840 |
| **file:line** | report.md:1829-1858 |
| **Blockers stated** | no full bear market in the Hyperliquid sample (report.md:1659-1664, :2215-2219); HYPE and MERL unmodellable for want of a Binance spot leg (report.md:1775-1778); cross-venue basis not measured, only basis to Hyperliquid's own index (report.md:1794-1800); protocol failure, venue insolvency, oracle manipulation, solo-operator failure and Canadian regulatory change all unmeasurable (report.md:1820-1827) |
| **Registered reopen conditions** | "**Current funding above roughly 10% annualised sustained for a quarter**, measured live rather than from a trailing average" [reg] HYPOTHESES.md:118; report.md:1856-1858 |
| **Trigger already met inside this repository?** | No — later entries move the wrong way: C.13 (2026-08-05) measures the 2026 cross-section level at −9.23% (report.md:2039). |
| **Possibly met by a different repository?** | Yes — flag: any repository carrying post-2026-08 perp funding measurements above ~10% annualised sustained for a quarter. |

## H8 — Cross-sectional funding carry (Stage C.13)

| field | value |
|---|---|
| **Status** | closed |
| **Closure kind** | signal present, cancelled by its own hedge |
| **Closure date** | 2026-08-05 |
| **Deciding figure (n)** | funding +43.68%/yr, price −42.91%, cost −0.66% → net **+0.11%** vs a 4% risk-free rate; max drawdown −75.85%; n = 4,411,046 hourly funding observations over 1,182 days, 231 usable perps — report.md:2074-2075, :2117-2122, :2207 |
| **file:line** | report.md:2221-2244 |
| **Blockers stated** | no bear market in the sample (report.md:2215-2219); break-even cost 1.76 bps/side against 1.5 modelled — a 17% margin (report.md:2185-2189); residual purge bias undetectable (report.md:2098-2103); parameter surface unstable across rebalance interval (report.md:2191-2198) |
| **Registered reopen conditions** | dispersion widening back **and** the price term ceasing to cancel the carry [reg] HYPOTHESES.md:135; report.md:2229-2240 |
| **Trigger already met inside this repository?** | No. Fixed-cohort dispersion fell 77% to 53.45% and did not plateau (report.md:2050-2055). |
| **Possibly met by a different repository?** | Possibly — flag: any repository measuring post-2026-08 cross-sectional perp funding dispersion. |

## H9 — Time-series momentum on daily bars (Stage C.16)

| field | value |
|---|---|
| **Status** | closed |
| **Closure kind** | insignificant after deflation, and untradeable where it appears |
| **Closure date** | 2026-08-06 |
| **Deciding figure (n)** | primary L90/H30 net Sharpe 0.302 vs BTC 0.183, deflated Sharpe **0.446** against 12 trials, alpha t = 1.01, 7 of 12 specs positive; executable subset (27 of 58 symbols) collapses to Sharpe 0.013. n = 1,736 daily bars, 58-symbol matrix — report.md:2537-2563, :2599-2603 |
| **file:line** | report.md:2611-2619 |
| **Blockers stated** | the earning book is short the untradeable tail — 31 of 58 symbols have no live Hyperliquid perp (report.md:2595-2597); the entire income arrives in down-trending periods (report.md:2572-2573, :2621-2625) |
| **Registered reopen conditions** | on data including a full bear regime, **at least half the registered grid** beating buy-and-hold BTC with DSR ≥ 0.95 **and** surviving on the executable subset; "A single cell clearing any bar reopens nothing" [reg] HYPOTHESES.md:30-line block at HYPOTHESES.md:152 |
| **Trigger already met inside this repository?** | No. |
| **Possibly met by a different repository?** | Unlikely — the condition is specific to this grid and universe. Flag only if another repository runs the same 12-cell grid on a bear-inclusive sample. |

## H10 — Liquidation aftermath reversion (Stage C.15)

| field | value |
|---|---|
| **Status** | closed |
| **Closure kind** | untestable / unidentifiable in available data |
| **Closure date** | 2026-08-06 |
| **Deciding figure (n)** | "Identifiable liquidations in the recorded data: **zero**", from a field inventory over n = 2,639,510 fills across 116 hour files, 12 instruments, 2026-08-01 → 2026-08-06; zero occurrences of `liquidat` in any recorded message; 18.0% zero-hash fills ruled out as a marker by a ground-truth cross-reference — report.md:2644-2670, :2678 |
| **file:line** | report.md:2676-2688 |
| **Blockers stated** | recorded feed carries no liquidation field (report.md:2644-2647); no public global liquidation endpoint — HTTP 422 (report.md:2662-2664); `userFillsByTime` is per-user only (report.md:2664-2666); **stated query cost:** "one polite request per fill-participant against 2.64M fills — weeks of querying" (report.md:2668-2670); "nothing before 2026-08-01 at any price" (report.md:2670); the Task 2 bar was never registered (report.md:2685-2688) |
| **Registered reopen conditions** | "Any one of: the venue adding a liquidation flag to the public trades stream; a public global liquidation-history endpoint; or labeled vendor history covering the subscribed instruments with timestamps alignable to recorded BBO mids at one-second precision." — report.md:2692-2696. Register form adds a size floor: "≥ 300 labeled liquidations across the subscribed instruments" [reg] HYPOTHESES.md:168 |
| **Trigger already met inside this repository?** | The stated *query-cost* blocker does not survive recomputation: the recorded week contains **62,905 distinct participant addresses** against 2,953,327 fills (measured on the live archive, UTC 2026-09-05 05:58), a 47:1 ratio, so per-address enumeration is ~15–20 h of free keyless querying rather than weeks. See DRAFT-p1-report-2. Whether that yields ≥ 300 labelled liquidations is unmeasured. |
| **Possibly met by a different repository?** | Yes — flag: any repository holding liquidation-labelled vendor history or a global liquidation endpoint for perpetual venues. |

## H11 — Medium-horizon prediction on untested feature classes (Stage C.17)

| field | value |
|---|---|
| **Status** | closed — and its FAIL ended the project's alpha search by pre-registered decision |
| **Closure kind** | FAIL on all six pre-registered bars |
| **Closure date** | 2026-08-06 |
| **Deciding figure (n)** | zero of 40 cells pass all six bars; best deflated Sharpe **0.499** against a 0.95 bar, best alpha t **1.35** against a 2 bar. n = 193–207 scored weeks for classes A–C, **45–59** for classes D–E — report.md:2754-2799 |
| **file:line** | report.md:2838-2845 (verdict), report.md:2847-2858 (the decision it triggered) |
| **Blockers stated** | Coin Metrics community snapshot 75 days stale, applied as a +75 d lag on every CM feature (report.md:2734); CryptoQuant free tier out — HTTP 401 (report.md:2736); Blockchain.com has no exchange-flow series (report.md:2737); "no reachable exchange publishes wallet-flow history free" (report.md:2739); class D's Hyperliquid premium series begins 2023-05, leaving 45–59 scored weeks (report.md:2815-2817) |
| **Registered reopen conditions** | "**(a)** a free exchange-flow source at **≤ 2-day** publication lag with **≥ 3 years** of history — the measured 75-day staleness is the binding data constraint on class B; or **(b)** the basis class sustaining **DSR ≥ 0.95 and alpha t ≥ 2 over ≥ 156 scored weeks including a full bear regime**" [reg] HYPOTHESES.md:185. Note: "Reopening H11 does not reopen the alpha search; that decision is the operator's to reverse, not a threshold's." |
| **Trigger already met inside this repository?** | Condition (a) is in question: the 75-day figure is the end-of-file date of a single snapshot in which **every** column including `PriceUSD` also stops (measured on the live archive, UTC 2026-09-05 06:01), so it may measure a stalled mirror rather than a publication lag. See DRAFT-p1-report-3. Condition (b) is unmet and, per DRAFT-p1-report-4, was unreachable at class D's window length. |
| **Possibly met by a different repository?** | Yes — flag: any repository using a free exchange-flow / on-chain netflow source at ≤ 2-day lag with ≥ 3 years of history. |

## H7 — Cross-venue divergence

| field | value |
|---|---|
| **Status** | closed |
| **Closure kind** | by decision (the C.17 end condition), not by evidence |
| **Closure date** | 2026-08-06 |
| **Deciding figure (n)** | none — no H7 experiment was run; the closure is the C.17 decision. Nearest measured figure: C.14's cross-venue A/B, max ΔAUC +0.0044 (Kraken) / +0.0037 (Coinbase), 6 days, n = 165,075 / 41,780 — report.md:2397-2401 |
| **file:line** | report.md:2847-2850 ("H7 closed by this same decision") |
| **Blockers stated** | needs months of simultaneous three-venue history; the Kraken/Coinbase/Hyperliquid overlap stopped accruing at 12 days when those feeds were retired on 2026-08-12 (report.md:4662-4686; [reg] HYPOTHESES.md:505-508) |
| **Registered reopen conditions** | "reopening requires the operator reversing that decision, at which point the original design above stands unchanged" [reg] HYPOTHESES.md:220; restarting the retired recorders is "one config flip, ADR-060" [reg] HYPOTHESES.md:508 |
| **Trigger already met inside this repository?** | No — and the closure note at [reg] HYPOTHESES.md:220 ("The three-venue overlap keeps accumulating at zero cost") is contradicted at the same SHA by the retirement (report.md:4662) and by the 2026-08-13 recording stop (progress.md:2762-2768). Recorded in DRAFT-p1-report-6. |
| **Possibly met by a different repository?** | No. |

## H6 — Spread capture on thin perpetuals

| field | value |
|---|---|
| **Status** | closed (after resolving positive at C.27 and surviving four D.1c kill conditions) |
| **Closure kind** | signal does not survive an order-lifecycle fill model |
| **Closure date** | 2026-08-12 (re-confirmed the same day under audit correction) |
| **Deciding figure (n)** | tightened net at the declared 2.5×Q cap and the 162 ms latency floor: **PUMP −4.75, MERL −4.23 bps** per filled notional as published (n = 32,018 / 4,270 fills), corrected to **PUMP −4.81, MERL −4.35** (n = 31,875 / 2,536); no zero-crossing anywhere on the +0…+800 ms grid — report.md:4854-4864, :4941-4948, :5048-5051, :5120-5126. Prior positive: C.27 census PUMP +4.30 (CI +4.27, n = 499,944 trades), MERL +6.45 (CI +6.07, n = 25,378) — report.md:4055-4056 |
| **file:line** | report.md:4971-4986 (verdict), report.md:5130-5132 (re-read against the corrected engine) |
| **Blockers stated** | a specific resting order's queue position is unobservable in principle from this feed (report.md:4159-4170); 83% (PUMP) / 97% (MERL) of touch changes have no trade to explain them (report.md:4179-4183); no precise queue model estimable — median absolute error 100% vs a 25% bar (report.md:4189-4196); latency is a proxy floor measured on `/info`, not the order path (report.md:4623-4628); `hftbacktest` unusable on this feed (report.md:4228-4232); one census week, one regime (report.md:4989-4990); PUMP a screened positive and MERL inside a 10-of-177 multiplicity correction (report.md:4991-4995); GMX demoted to unresolved by the A3 interval correction (report.md:5148-5153); "The D.1d replay ran once and no second pair of eyes has checked it" (report.md:5105-5106); "`spread.py` and `adverse.py` still have no direct test of their own" (report.md:5189) |
| **Registered reopen conditions** | report.md:5005-5010: reopens only on "**order-level book data** — a venue stream carrying arrivals, cancellations, or order IDs … — or venue-provided fill-level ground truth"; explicitly **not** on lower latency, a better queue model on this feed, or more weeks of the same accounting. Rewritten in the register to add a third route: "(c) a **materially different cost structure**, e.g. a maker-rebate tier" [reg] HYPOTHESES.md:197. Two pre-registered follow-ups: the 2026-08-19 accrued latency distribution (report.md:4704-4705) and the blind-universe window closing 2026-09-09 (report.md:4606, :4706-4708, :4993-4995) |
| **Trigger already met inside this repository?** | No — and the two follow-ups can no longer run: recording stopped 2026-08-13, 1 day into the 28-day blind window and 1 of 7 latency days (progress.md:2762-2784). See DRAFT-p1-report-6. Separately, NOT (+31.15) and TNSR (+35.50) cleared every bar but the median-daily-volume clause of the capacity tier and were never put through the D.1d model that produced the closure (report.md:4057-4058, :4083-4085). See DRAFT-p1-report-7. |
| **Possibly met by a different repository?** | Yes — flag strongly: any repository holding **order-level / L3 / MBO book data** (arrivals, cancellations, order IDs), venue fill-level ground truth from resting orders, or a documented maker-rebate fee tier. |

## Detection track (Stages C.19–C.26) — Solana rug detection

| field | value |
|---|---|
| **Status** | concluded, with a shipped deliverable |
| **Closure kind** | pre-registered end condition fired; the confirming test is **measured-unaffordable** |
| **Closure date** | 2026-08-07 |
| **Deciding figure (n)** | the decontaminated unbiased test prices at **≈ 124,764 weighted credits**, ~1.9× the entire 60,000 cap and ~28× the 1,199 remaining (report.md:3921-3932). Substantive result: 6h behavioural mid-activity-stratum lift settles at **+0.032, SE ≈ 0.039, 95% CI [−0.045, +0.109]**, n = 103 (report.md:3941-3953). Shipped: hard-rug clearance scorer at 0.984 precision / 0.538 recall on the 2024 fold (report.md:3968-3971) |
| **file:line** | report.md:3984-3999 (verdict), report.md:3886-3893 (the end condition, registered in advance) |
| **Blockers stated** | Helius key absent at C.21 (report.md:3147-3154); 12-page pagination cap truncating 55% of pools (report.md:3224-3227); signature metadata carries no signer, making "unique signers" ~100× dearer (report.md:3554-3561); the from-now pagination wall correlating with the label (report.md:3565-3574); the creator not identifiable on any of 8 probed pools (report.md:3902-3914); 30-day pool detail at 4,136–79,628 signatures on active pools (report.md:3916-3919); **the 60,000 cap is self-imposed, "not a Helius tier limit"** (report.md:3929-3930) |
| **Registered reopen conditions** | C.24's version: "(a) a data source giving pre-event visibility into **creator intent** (off-chain deploy provenance, social/funding graph before launch), or (b) an **observation cutoff beyond 24h**"; explicitly not on "a better model or a richer on-chain feature set at the cutoffs tested" — report.md:3539-3545. C.26's end condition records the decon-unbiased question as "**measured-unaffordable, not untested**" — report.md:3886-3893 |
| **Trigger already met inside this repository?** | No. Condition (b) (a cutoff beyond 24h) was registered as a reopening condition at C.24 and never exercised; C.25/C.26 stayed at 6h and 24h. |
| **Possibly met by a different repository?** | Yes — flag: any repository holding off-chain deploy provenance or a pre-launch social/funding graph for Solana token launches, or a paid/entitled Solana indexer. |

---

## Stage-level items in `report.md` that carry a named-but-unrun variant, for the cross-repo pass

| stage | named variant | ever run? | file:line |
|---|---|---|---|
| C.8 | MES (7× lower cost in bps) | no — validated MES day already on disk (report.md:1376) | report.md:1086-1088 |
| C.8 | "a regime that is not a two-month uptrend" on CME | no — "CME was not re-run" | report.md:1084-1085; report.md:2490-2491 |
| C.8 | cross-venue features against the crypto recorders | **yes**, C.14 §3, immaterial | report.md:1085-1086; report.md:2385-2411 |
| Phase B | hyperliquid (costs wired into the run config at maker 1.5 / taker 4.5 bps) | no — skipped once for missing data, never revisited | report.md:773, :775-777 |
| C.14 | ETH pair on both venues | no — dropped for a deadline, disclosed | report.md:2276-2279 |
| C.9 | the ten thin Hyperliquid perps' adverse selection | **yes**, C.27 | report.md:1240-1251; report.md:4040-4066 |
| C.13 | a version hedging cross-sectional price exposure | no — declared "a different hypothesis" needing its own test | [reg] HYPOTHESES.md:135 |
| C.24 | an observation cutoff beyond 24h | no | report.md:3541-3542 |
| D.1d | NOT and TNSR through the order-lifecycle fill model | no — excluded on the volume clause of the capacity tier | report.md:4057-4058, :4083-4085 |
| D.1b | the blind-universe scoring window | no — terminated at 1 of 28 days | report.md:4604-4607; progress.md:2782-2784 |
| D.1b | the accrued Hyperliquid latency distribution | no — terminated at 1 of 7 days | report.md:4634-4635, :4704-4705; progress.md:2775-2777 |
