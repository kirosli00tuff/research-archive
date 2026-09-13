# REOPEN LEDGER — MLCryptoEngine (consolidated)

**Repository:** MLCryptoEngine · **Anchored SHA:** `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22) — this SHA is HEAD of the live repository.
Merged and de-duplicated from three drafting passes (`report.md`/`README.md`; `HYPOTHESES.md`/`DECISIONS.md`/`AUDIT.md`/`docs/notes/`/`audit/`; `progress.md`/`research/`/`backtest/`). Line references are snapshot line numbers, identical to `git show <SHA>:<path>`.

**This ledger is factual, not advocacy.** Where a row records a contested figure, the contest is named by finding ID and the ledger states both readings.

**Project-level facts that bind every row below:**
- **The alpha search ended by pre-registered decision on 2026-08-06** (C.17 FAIL; ADR-043, DECISIONS.md:1907-1911). Reversing it "is an explicit operator decision that reopens nothing retroactively, while every register entry keeps its own evidence-based reopening condition independently" — DECISIONS.md:1917-1920.
- **Kraken and Coinbase recorders were retired 2026-08-12** (ADR-060, DECISIONS.md:2402-2430; report.md:4662-4686). History is immutable and still replayable; restarting is "one config flip" (DECISIONS.md:2426-2427).
- **All recording stopped 2026-08-13T05:02:49Z** (progress.md:2762; DECISIONS.md:2583). This forecloses every reopening condition phrased as "the recorders accrue this at zero cost". `report.md` is **not amended anywhere** for it: its forward-looking dates at :4606, :4635, :4704-4708, :4794, :4952, :4993 all refer to clocks that stopped after 1 of 7 and 1 of 28 days (AUDIT-A-MLCryptoEngine-10).
- **Final archive, immutable and retained in full: 14 GB** — kraken 14 days (2026-07-30 → 08-12, 6.8 GB), coinbase 14 days (5.1 GB), hyperliquid 13 days (2026-08-01 → 08-13, 2.2 GB) — progress.md:2788-2792, :2786.
- **Databento vendor spend:** $82.1179 of a $120.00 self-imposed cap, 29 entries, last write 2026-08-04, **no reversal of the $35.5144 undelivered June charge** (live `data/vendor/spend_ledger.jsonl`, read 2026-09-05T05:55Z, UNANCHORED; document figures at progress.md:1007-1011).
- **Helius credits:** 58,801 weighted of a 60,000 self-imposed cap (24,025 requests; live `data/vendor/helius_credit_ledger.jsonl`, read 2026-09-05T05:55Z, UNANCHORED; report.md:3998-3999). The cap is self-imposed, not a vendor limit (report.md:3929-3931), and the weighting is UNVERIFIED (progress.md:2299).

---

## Part 1 — Alpha register (H1–H11)

### H1 — Short-horizon directional prediction on crypto spot
| field | value |
|---|---|
| **Status** | Closed — "**Closed — cost-bound** · 2026-08-03" (HYPOTHESES.md:49) |
| **Closure kind** | cost-bound — "a real signal smaller than the cost of capturing it, which reopens at a materially lower fee tier" (progress.md:1543-1545; kind defined HYPOTHESES.md:29-31) |
| **Closure date** | 2026-08-03; register entry written at C.12 on 2026-08-04 (progress.md:1531-1577); strengthened 2026-08-05 by C.14 |
| **Deciding figure (n)** | 3.31 bps gross capture at 900 s vs **80.00 bps** round-trip maker cost, AUC 0.596, net EV −76.69 bps, Coinbase BTC-USD, **n = 1 day (2026-07-31)**, 31,640 samples for that venue-symbol (HYPOTHESES.md:50; progress.md:1128-1129; research/experiments.jsonl:1). Superseded by C.14: top-confidence decile **5.0020 bps** vs 80 bps, Kraken BTC/USD 900 s, **n = 165,075 over 6 days** (report.md:2289, :2298, :2328-2330); and the four-day 900 s range **−2.4378 to +3.0497 bps**, Coinbase, **n = 4 days** (report.md:2366, :2378) |
| **file:line** | report.md:2328-2330 (deciding sentence); report.md:2289-2298 (table); report.md:801 (Phase B origin); HYPOTHESES.md:49-54 |
| **Blockers stated** | 80 bps retail spot round trip (report.md:681, :773); 0-bps maker tiers requiring $250M (Coinbase) / $10M (Kraken) trailing 30-day volume, "Neither is reachable at this project's capital" (HYPOTHESES.md:54, restated HYPOTHESES.md:516-517); ETH pair not run in C.14 for time (report.md:2276-2279); "six days is not six regimes" (report.md:2488-2490; progress.md:1811-1812); the Kraken fee schedule was wrong twice (progress.md:333-341; :2494-2496) |
| **Registered reopen conditions** | "A round-trip cost below roughly **3 bps**, i.e. under 1.5 bps per side… **Reopens on cost, not on modelling**… It does not reopen on more data at the same venues." + "Reopening now additionally requires the top-confidence decile to clear a round trip somewhere, which it does not." — HYPOTHESES.md:54; quoted character-for-character and pinned by test at docs/notes/h1-predictability-without-capturability.md:261-263 (rule: DECISIONS.md:2623-2626). Short form: progress.md:1676-1677 |
| **Trigger already met inside this repository?** | **Arguably yes, and unrevisited.** The register's own fee table records Hyperliquid perps base tier at **3.0 bps round trip** with no volume requirement (HYPOTHESES.md:307) and calls it "**The cheapest venue reachable from British Columbia is Hyperliquid at 3 bps**" (HYPOTHESES.md:322-323); the code constant is `HYPERLIQUID_MAKER_ROUND_TRIP_BPS = 2.0 * 1.5` (research/microstructure/fees.py:36,42); 13 days were recorded; **no directional run on that venue exists in the append-only log** (research/experiments.jsonl:2 — both hyperliquid entries `{"error": "no valid samples"}`). See **AUDIT-A-MLCryptoEngine-1**. The n = 4 supersession that "closed it harder" has a 95% CI of [−3.21, +3.97] bps, which straddles both zero and 3.0 (**AUDIT-A-MLCryptoEngine-6**) |
| **Possibly met by a different repository?** | **Yes** — any repository measuring a sub-3-bps round-trip venue reachable from British Columbia, a maker-rebate schedule, or directional microstructure capture at a low-fee perp venue |

### H2 — Transfer of the edge to CME micro futures
| field | value |
|---|---|
| **Status** | Closed — "**Closed — signal-absent** · 2026-08-03" (HYPOTHESES.md:65) |
| **Closure kind** | signal-absent — the register's non-reopening kind: "**Does not reopen on a better model, a better feature set, or lower fees.**" (HYPOTHESES.md:32-34; progress.md:1546-1548) |
| **Closure date** | 2026-08-03 (Stage C.8, progress.md:1115) |
| **Deciding figure (n)** | AUC **0.501** at every horizon; 0.22 bps gross capture against **5.33 bps** cost; best net EV **−5.11 bps**; the one figure clearing rounding noise (+0.215 bps at 900 s) reverses to −0.785 on a stride-1 control. **n = 224,425,675 events / 989 scheduled-open hours / two validated MBT months (2026-04, 2026-05) / 53 days / 1,109,072 training samples; one clean walk-forward fold** (HYPOTHESES.md:66-67, :70; report.md:899, :917, :981, :1009, :952; DECISIONS.md:1005) |
| **file:line** | report.md:974-992 (verdict), report.md:1000-1013 (per-horizon table), progress.md:1128-1131 |
| **Blockers stated** | all seven cross-venue features 100% NaN on the April–May sample (report.md:1053-1057); one volatility regime (report.md:966-972; progress.md:1104-1108); "one complete train/test split", not three (report.md:1069-1077; progress.md:1150-1152); the June/July backfill did not fit the $120 cap after a **$35.5144 charge for undelivered bytes** (DECISIONS.md:855-859; progress.md:1007-1009); the vendor client exposes no usage endpoint (DECISIONS.md:894-897) |
| **Unresolved blocker with a named, free remedy** | "Resuming June and July requires first reconciling the June charge against the Databento invoice — … only the portal can say whether the killed stream was billed." (DECISIONS.md:865-868); "**Check the portal before any retry**" (progress.md:1017). **Never performed**; ledger holds the charge with no reversal, $37.8821 of headroom remaining, July alone quoted at $21.2955. See **AUDIT-A-MLCryptoEngine-5** |
| **Registered reopen conditions** | "Reopens only on evidence of measurable AUC on a *different* instrument or feature class — never on a re-run of the same pipeline against the same contract with a stronger learner." (HYPOTHESES.md:70). Stage form, in order of cheapness: "a regime that is not a two-month uptrend; cross-venue features against the crypto recorders …; and MES" (report.md:1084-1088) |
| **Trigger already met inside this repository?** | Partly retired: the cross-venue item was tested and found immaterial (ΔAUC ≤ +0.0044, report.md:2399-2411). The **regime** item was not ("CME was not re-run", report.md:2490-2491) and **MES was never run**, although `MES.c.0` 2026-07-31 is validated PASS at 14,989,106 events / 100.00% coverage and already on disk (report.md:1376-1378). See **AUDIT-A-MLCryptoEngine-12**. A different *venue* (Hyperliquid perps) was recorded and never tested either (**AUDIT-A-MLCryptoEngine-1**) |
| **Possibly met by a different repository?** | **Yes** — any repository reporting measurable order-book-ML AUC on a different futures instrument or a feature class MLCryptoEngine has not tested |

### H3 — Passive spread capture
| field | value |
|---|---|
| **Status** | Closed with a tail — "**Closed — cost-bound, with a measured tail still open (see H6)** · 2026-08-03" (HYPOTHESES.md:81); the tail is declared to close with H6 at HYPOTHESES.md:205 |
| **Closure kind** | cost-bound |
| **Closure date** | 2026-08-03 (Stage C.9, progress.md:1188); tail closed 2026-08-12 |
| **Deciding figure (n)** | spread − adverse − cost: Hyperliquid BTC **−3.05** (n = 491,982 trades), Hyperliquid ETH **−2.75** (n = 278,835), CME MBT **−4.25** (n = 148,768) — report.md:1198-1214. 28-instrument survey: no spread-to-cost ratio above 1.0, best M6A micro AUD **0.98** (report.md:1156, :1167). **n = 28 instruments** over 53.13 quoted hours (Hyperliquid, 2,151,124 bbo updates) and one CME day (2026-07-15, bbo-1s, 16 micro contracts, $0.7763) |
| **file:line** | report.md:1208-1221, :1231-1238; progress.md:1231-1233 |
| **Blockers stated** | "This assumes a fill, which no part of this pipeline models" — every figure an upper bound (report.md:1223-1229; ADR-026 DECISIONS.md:1102-1108); CME bbo-1s carries no trades so adverse selection cannot be measured on the CME tail (report.md:1243-1245); no reachable maker-rebate venue (HYPOTHESES.md:86, :515) |
| **Residue never closed** | 3 contracts "too inactive to call a market" (SIL ratio 3,889 on 69 quote updates/day; MHG 65.0 on 1,494) — progress.md:1218-1221; 2 a "failed measurement" from an unresolved continuous symbol (2YY 10 records, 5YY 1) — progress.md:1222-1224; 4 micro-yield contracts with no ratio computed — progress.md:1225-1226. None is mentioned again in progress.md or HYPOTHESES.md. See **AUDIT-A-MLCryptoEngine-15** |
| **Registered reopen conditions** | "A venue paying **maker rebates** (none reachable from British Columbia does), or an instrument whose spread-to-cost ratio exceeds 1.0 *with* adverse selection below the excess." (HYPOTHESES.md:86). Stage form: "Re-run this census in a week. If the thin end survives spread − adverse − cost there, that is the first positive result this project has produced and it earns a fill simulation" (report.md:1247-1251) |
| **Trigger already met inside this repository?** | **Yes, and honoured for the Hyperliquid tail**: the re-run is C.18/C.27; five of ten instruments cleared the bars and H6 opened (report.md:2864-2925, :4001-4106). **But** PUMP and MERL were replayed, GMX was discounted, and **NOT (+31.15) and TNSR (+35.50) were never replayed** (**AUDIT-A-MLCryptoEngine-4**); the CME residue above was never revisited (**AUDIT-A-MLCryptoEngine-15**) |
| **Possibly met by a different repository?** | **Yes** — a documented reachable maker-rebate venue; or CME micro-contract quote data (SIL, MHG, 2YY, 5YY, 10Y, 30Y) or any instrument-level spread-to-cost survey |

### H4 — Cointegration pairs trading
| field | value |
|---|---|
| **Status** | Closed — "**Closed — signal-absent** · 2026-08-04" (HYPOTHESES.md:97) |
| **Closure kind** | signal-absent |
| **Closure date** | 2026-08-04 (Stage C.10, progress.md:1359) |
| **Deciding figure (n)** | **0 of 180** formation-window BH survivors still significant out of sample (175 re-testable, 18 = 10.3% significant uncorrected vs a 5.9% base rate); holdout **91 raw hits vs 77.0 expected**; BTC/ETH p = 0.1169; deflated Sharpe of the best pair **0.026** against an expected max of 0.1058 over **n = 1,653 trials**; zero executable pairs. Sample: 60-symbol point-in-time universe (12 died in sample), **1,826 daily bars**, 2021-08-01 → 2026-07-31 (HYPOTHESES.md:98-99; report.md:1462, :1474-1479, :1588-1593) |
| **file:line** | report.md:1605-1628; progress.md:1322-1344 |
| **Blockers stated** | universe built from Binance daily bars, "a venue this project cannot trade" (report.md:1388-1394; DECISIONS.md:1357-1359); rests on Binance not purging delisted directories (report.md:1430-1432); only 5 of 12 subscribed perps existed at 2021-08 (report.md:1526-1529); power floor removes 132 of 175 pairs (report.md:1495, :1522); Kraken OHLC capped at 720 candles and live-products-only listings cannot build a survivorship-free universe (progress.md:1297-1301) |
| **Registered reopen conditions** | "(a) a reachable venue offers shorts across a materially broader instrument set … **and** (b) relationships persist out of sample, which they did not at any correction level" (HYPOTHESES.md:102) |
| **Trigger already met inside this repository?** | No. The 2024-06 → 2026-07 executable re-screen produced 1 raw hit against 1.8 expected and 0 survivors (report.md:1555-1563). Cost was never the constraint: break-even 300–550 bps against a 3 bps venue (HYPOTHESES.md:102) |
| **Possibly met by a different repository?** | **Partly** — clause (a) only: any repository with a reachable venue offering shorts across a broader crypto instrument set with multi-year history, or a survivorship-free crypto universe |

### H5 — Funding-rate carry
| field | value |
|---|---|
| **Status** | Closed — "**Closed as currently unattractive — decayed, not disproved** · 2026-08-04" (HYPOTHESES.md:113) |
| **Closure kind** | decayed / currently-unattractive (a fourth kind, outside the C.12 two-kind taxonomy) |
| **Closure date** | 2026-08-04 (Stage C.11, progress.md:1447) |
| **Deciding figure (n)** | **8.07% (ETH) / 8.00% (BTC)** net annualised on deployed capital, 5 of 10 modelled instruments clearing a 4% risk-free rate by 1.6–4.1 points, against an ~85% yield decay: Binance BTC funding 30.61% (2021) → 11.92% (2024) → 5.13% (2025) → **1.94% (2026)**; ETH 37.54% → 0.97%; decay slopes −6.31%/yr (BTC), −7.67%/yr (ETH). **n = 27,761 hourly BTC funding rows over 3.23 years** (2023-05-12 → 2026-08-04, 12 perps); Binance 8-hourly 2020-01 → 2026-07 for the decay curve (HYPOTHESES.md:114-115; report.md:1653, :1709-1710) |
| **file:line** | report.md:1829-1858; progress.md:1510-1527 |
| **Blockers stated** | "**Contains no full bear market.** Hyperliquid launched *after* the 2022 drawdown" (HYPOTHESES.md:116; report.md:1659-1664); perp prices reconstructed as `spot × (1 + premium)` because the candle endpoint serves ~5,000 bars (HYPOTHESES.md:116); HYPE and MERL unmodellable for want of a Binance spot leg (report.md:1775-1778); cross-venue basis not measured (report.md:1794-1800); protocol failure, venue insolvency, oracle manipulation, solo-operator failure and Canadian regulatory change all unmeasurable (report.md:1820-1827) |
| **Confound recorded but not separated** | "**The carry is a bull-market phenomenon.** Correlation of daily funding with the trailing 30-day trend is **0.57 / 0.50 / 0.54** (BTC/ETH/SOL)." (progress.md:1487-1489) — so the 2026 level is regime-dependent, which the closure does not separate from structural decay |
| **Registered reopen conditions** | "**Current funding above roughly 10% annualised sustained for a quarter**, measured live rather than from a trailing average" (HYPOTHESES.md:118; report.md:1856-1858) |
| **Trigger already met inside this repository?** | No — and later entries move the wrong way: C.13 measures the 2026 cross-section level at −9.23% (report.md:2039); D.1c found funding immaterial at ≤ 0.33 bps of filled notional (HYPOTHESES.md:204) |
| **Possibly met by a different repository?** | **Yes** — any repository carrying post-2026-08 perp funding measured live above ~10% annualised sustained for a quarter, or a bull/bear split of funding yield |

### H6 — Spread capture on thin perpetuals
| field | value |
|---|---|
| **Status** | Closed — "**Closed at D.1d — 2026-08-12; closure re-confirmed under audit correction the same day.**" (HYPOTHESES.md:196). Trajectory: registered 2026-08-06 (C.18) → resolved-positive 2026-08-11 (C.27) → D.1-feasible (D.1a) → survives four kill conditions (D.1c) → closed negative (D.1d) |
| **Closure kind** | kill condition fired — the per-fill positive does not survive an order-lifecycle fill model |
| **Closure date** | 2026-08-12 |
| **Deciding figure (n)** | tightened net at the declared 2.5×Q cap and the 162 ms proxy latency floor: **PUMP −4.75, MERL −4.23 bps** per filled notional per leg as published, corrected by audit A4 to **PUMP −4.81, MERL −4.35** (per round trip: **−9.62**, report.md:5177); no zero-crossing anywhere on the {+0…+800} ms grid. **n = 8 replay days / 28,658,883 records** (AUDIT.md:490); 31,875 / 2,536 fills post-correction (report.md:5051). Prior positive: C.27 census **PUMP +4.30** (n = 499,912 scored prints), **MERL +6.45** (n = 25,348) at the worst horizon (audit/census_ci.json; report.md:4055-4056) |
| **file:line** | report.md:4971-4986 (verdict), report.md:5120-5132 (re-read against the corrected engine), HYPOTHESES.md:196-197 |
| **Blockers stated** | queue position unobservable in principle from this feed, "**no precise queue model is estimable**" (87–99% of levels clear by cancellation) — report.md:4159-4196, HYPOTHESES.md:203, DECISIONS.md:2273-2279; 83% (PUMP) / 97% (MERL) of touch changes have no trade to explain them (report.md:4179-4183); latency measurable only as a proxy floor on `/info`, not the signed order path (report.md:4623-4628; DECISIONS.md:2480-2483); `hftbacktest` unusable on this feed (report.md:4228-4232); one census week, one regime (report.md:4989-4990); PUMP a screened positive and MERL inside a 10-of-177 multiplicity correction (report.md:4991-4995); GMX demoted to unresolved on the A3 correction (report.md:5148-5153; contested — **AUDIT-A-MLCryptoEngine-9**); the Hyperliquid maker fee is documented, not measured, "the weakest input in the chain" (AUDIT.md:350-370; report.md:5169-5175); "The D.1d replay ran once and no second pair of eyes has checked it" (report.md:5105-5106; DECISIONS.md:2538); `spread.py` and `adverse.py` have no direct test (report.md:5189) |
| **Registered reopen conditions** | Rewritten 2026-08-12 under audit A13: the net must survive an order-lifecycle fill model, by one of **(a) order-level book data** carrying arrivals, cancellations or order IDs; **(b) venue fill-level ground truth** from actually resting orders (paper or minimum-size live); **(c) a materially different cost structure, e.g. a maker-rebate tier** — HYPOTHESES.md:197; report.md:5005-5010. Explicitly **not** reopened by lower latency, a better queue model from this feed, more weeks of per-fill accounting, or re-attribution between edge and inventory |
| **Registered follow-ups that were abandoned** | the 2026-08-19 accrued latency distribution (report.md:4634-4635, :4704-4705) — **1 of 7 days**; the blind-universe scoring window closing 2026-09-09 (DECISIONS.md:2391-2393; report.md:4604-4607) — **1 of 28 days**; the ≥ 4-week re-run "which the recorders accrue at zero cost by ~2026-09-08" (HYPOTHESES.md:205; report.md:4252-4255) — **1 of 28 days**. All three foreclosed by the 2026-08-13 stop; the screened-positive demotion ADR-059 existed to resolve (DECISIONS.md:2395-2396) is therefore permanent. See **AUDIT-A-MLCryptoEngine-10** |
| **Also registered and never invoked** | the C.18 outcome-to-action map row "| survivors within noise of zero | **extend recording 30 days and re-run under these same bars** — no building |" (progress.md:2121, table at :2116-2123); GMX became "unresolved" without triggering it |
| **Trigger already met inside this repository?** | No for (a)/(b)/(c). Two bar-clearing instruments were never put through the deciding model: NOT (+31.15) and TNSR (+35.50), excluded on the median-daily-volume clause alone (report.md:4057-4058, :4083-4085) — **AUDIT-A-MLCryptoEngine-4** |
| **Possibly met by a different repository?** | **Yes — flag strongly:** any repository holding **order-level / L3 / MBO book data** (arrivals, cancellations, order IDs) for any venue, venue fill-level ground truth from resting orders, or a documented maker-rebate fee tier |

### H7 — Cross-venue divergence
| field | value |
|---|---|
| **Status** | Closed — "**Closed by decision — the C.17 end condition, not evidence** · 2026-08-06" (HYPOTHESES.md:216) |
| **Closure kind** | by decision; the design is preserved (progress.md:2059-2060) |
| **Closure date** | 2026-08-06 |
| **Deciding figure (n)** | **none measured directly** (HYPOTHESES.md:217). Nearest evidence: C.14's two-venue cross-venue A/B, max ΔAUC **+0.0044** (Kraken) / +0.0037 (Coinbase), max Δcapture +0.04 bps, 6 days, n = 165,075 / 41,780 (report.md:2397-2401; progress.md:1787-1792); Hyperliquid perp-to-own-index premium mean 0.65 bps, p99 14.59, worst adverse hourly move 38.2 bps — explicitly "**not** the cross-venue number" (HYPOTHESES.md:217) |
| **file:line** | report.md:2847-2850; HYPOTHESES.md:216-220 |
| **Blockers stated** | needs months of simultaneous three-venue history; the overlap began 2026-08-01 and **stopped accruing at 12 days** when Kraken/Coinbase were retired on 2026-08-12 (HYPOTHESES.md:218, :507-508; DECISIONS.md:2413-2421); two-leg spot-to-spot round trip of 160 bps (HYPOTHESES.md:219) |
| **Registered reopen conditions** | operator reversal of the 2026-08-06 decision, "at which point the original design above stands unchanged" (HYPOTHESES.md:220), plus restarting the retired recorders — one config flip, ADR-060 (HYPOTHESES.md:508; DECISIONS.md:2426-2427) |
| **Trigger already met inside this repository?** | No. Note the register's own closure note still asserts "The three-venue overlap keeps accumulating at zero cost" (HYPOTHESES.md:220), contradicted at the same SHA by the retirement and the 2026-08-13 stop and acknowledged at HYPOTHESES.md:507-508 (**AUDIT-A-MLCryptoEngine-10**) |
| **Possibly met by a different repository?** | **Yes** — any repository with simultaneous multi-venue book capture over months, or a cross-venue basis measured over months |

### H8 — Cross-sectional funding carry
| field | value |
|---|---|
| **Status** | Closed — "**Closed — signal present, cancelled by its own hedge** · 2026-08-05" (HYPOTHESES.md:130) |
| **Closure kind** | signal present but cancelled by its own hedge (a distinct kind) |
| **Closure date** | 2026-08-05 (Stage C.13, progress.md:1682) |
| **Deciding figure (n)** | funding **+43.68%/yr**, price return **−42.91%**, cost −0.66% → **net +0.11%** against a 4% risk-free rate (shortfall 3.89 points); max drawdown **−75.85%**; price-term daily vol 10.9× the funding term's. **n = 231 usable perps (232 considered, 55 delisted retained), 4,411,046 hourly funding observations, 1,182 days** (2023-05-12 → 2026-08-05) (HYPOTHESES.md:131-132; report.md:2074-2075, :2117-2122, :2207) |
| **file:line** | report.md:2221-2244; progress.md:1709-1722 |
| **Blockers stated** | "**Contains no bear market**" (HYPOTHESES.md:133); delisted perps assumed to liquidate at last printed price while the venue settles at an unobservable oracle price (HYPOTHESES.md:133); break-even **1.76 bps/side against 1.5 modelled** at 51.7× annual turnover — a 17% margin (HYPOTHESES.md:135; report.md:2185-2189); residual purge bias undetectable (report.md:2098-2103); parameter surface unstable across rebalance interval (report.md:2191-2198) |
| **Registered reopen conditions** | two independent changes, both required: dispersion must widen back (it fell 77%, 241.50% → 53.45% decile spread on a fixed cohort) **and** "the price term would have to stop cancelling the carry" (baskets correlate −0.718) — HYPOTHESES.md:135 |
| **Named variant, never run, disclosed as out of scope** | a cross-sectionally price/beta-hedged version — "would be a different hypothesis, and would need its own test" (HYPOTHESES.md:135) |
| **Trigger already met inside this repository?** | No. Fixed-cohort dispersion fell 77% and did not plateau (report.md:2050-2055) |
| **Possibly met by a different repository?** | **Possibly** — a post-2026-08 cross-sectional perp funding dispersion measurement, or a cross-sectional carry book with a beta/sector hedge tested elsewhere |

### H9 — Time-series momentum on daily bars
| field | value |
|---|---|
| **Status** | Closed — "**Closed — insignificant after deflation, and untradeable where it appears** · 2026-08-06" (HYPOTHESES.md:146) |
| **Closure kind** | FAIL against pre-registered bars (registration commit 88b69d8, progress.md:1819-1877) |
| **Closure date** | 2026-08-06 (Stage C.16, progress.md:1879) |
| **Deciding figure (n)** | primary L90/H30 net Sharpe **0.302** vs BTC 0.183, **deflated Sharpe 0.446** against 12 registered trials, alpha t **1.01**, 7 of 12 specs positive; best single cell L30/H7 net Sharpe 0.647 → DSR 0.732; executable subset (27 of 58 symbols) collapses to Sharpe **0.013**. **n = 1,736 daily bars, 58-symbol matrix** from a 60-member point-in-time universe (HYPOTHESES.md:147-148; report.md:2537-2563, :2599-2603) |
| **file:line** | report.md:2611-2619; progress.md:1893-1905 |
| **Blockers stated** | the earning book is net short (−0.275 mean exposure) with negative beta in every cell, earning +56.9%/yr in down-trends vs −14.7%/yr in up — "Its income requires an alt bear market to exist" (HYPOTHESES.md:149); 31 of 58 symbols have no live Hyperliquid perp (report.md:2595-2597); "Kraken adds nothing (BTC/ETH spot, no shorts)" (progress.md:1904-1905) |
| **Registered reopen conditions** | on data including a full bear regime, "**at least half the registered grid** beats buy-and-hold BTC risk-adjusted with **deflated Sharpe ≥ 0.95**, **and** the effect survives on the executable subset … A single cell clearing any bar reopens nothing" (HYPOTHESES.md:151; progress.md:1908-1910) |
| **Trigger already met inside this repository?** | No |
| **Possibly met by a different repository?** | **Yes** — a repository whose crypto sample includes a full bear regime *and* a broader executable short universe; both halves of the condition would then be testable |

### H10 — Liquidation aftermath reversion
| field | value |
|---|---|
| **Status** | Closed — "**Closed — unidentifiable in available data** · 2026-08-06" (HYPOTHESES.md:163) |
| **Closure kind** | data-availability closure, "a **third kind**, distinct from cost-bound and signal-absent" (HYPOTHESES.md:166; progress.md:1939-1943) |
| **Closure date** | 2026-08-06 (Stage C.15) |
| **Deciding figure (n)** | "**Identifiable liquidations in the recorded data: zero.**", from a field inventory over **n = 2,639,510 fills across 116 hour files, 12 instruments, 2026-08-01 → 2026-08-06**; one key-set `(coin, hash, px, side, sz, tid, time, users)` with no flag; zero `liquidat` occurrences in any channel; the 18.0% all-zeros-hash class ground-truthed via `userFillsByTime` to TWAP fills; three global-history endpoint names return HTTP 422 (HYPOTHESES.md:164; report.md:2644-2670, :2678) |
| **file:line** | report.md:2676-2688; progress.md:1921-1934 |
| **Blockers stated** | no liquidation flag in the public trades stream; no public global-history endpoint (HTTP 422); `userFillsByTime` is per-user only; **stated query cost** "one polite request per fill-participant against 2.64M fills — weeks of querying" (report.md:2668-2670); "nothing before 2026-08-01 at any price"; no Task 2 bar was ever registered (report.md:2685-2688); large-trade proxies declined by design (HYPOTHESES.md:166) |
| **Registered reopen conditions** | "A liquidation-labeled source: the venue flagging liquidations in the public trades stream, a global history endpoint, or labeled vendor data — covering **≥ 300 labeled liquidations across the subscribed instruments** with timestamps alignable to recorded BBO mids at ≤ 1 s… Below 300 events the answer is 'too thin' by prior declaration… nothing reopens on proxied labels." (HYPOTHESES.md:168; progress.md:1936-1939) |
| **Trigger already met inside this repository?** | **Contested.** The stated query-cost blocker does not survive recomputation: the recorded week holds **62,905 distinct participant addresses** against 2,953,327 fills (measured on the live archive, 2026-09-05 05:55–05:58Z, UNANCHORED) — a 47:1 ratio, so per-address enumeration is ~15–20 h of free keyless querying, not weeks (**AUDIT-A-MLCryptoEngine-3**). Whether that yields ≥ 300 labelled liquidations is **unmeasured** |
| **Possibly met by a different repository?** | **Yes** — any repository holding liquidation-labelled venue or vendor history, a global liquidation endpoint, or a dataset of ≥ 300 identified liquidations on any perp venue |

### H11 — Medium-horizon prediction on untested feature classes
| field | value |
|---|---|
| **Status** | Closed — "**Closed — FAIL on all six pre-registered bars; the closure that ended the alpha search by decision** · 2026-08-06" (HYPOTHESES.md:180) |
| **Closure kind** | FAIL on six pre-registered bars, with a binding end condition agreed in advance (progress.md:1953-1955; ADR-043 DECISIONS.md:1907-1911) |
| **Closure date** | 2026-08-06 (Stage C.17) |
| **Deciding figure (n)** | **0 of 40 registered cells pass**; best deflated Sharpe **0.499** vs the 0.95 bar; best alpha t **1.35** vs 2; class A negative 8/8; class consistency A 0.0 / B 0.875 / C 0.75 / D 1.0 / E 0.875; break-even costs 22–1,059 bps/side vs 1.5 modelled. **n = 40 cells at n_trials = 40; weekly 2020-08-02 → 2026-07-26, up to 207 scored weeks (classes A–C), 45–59 for D–E**; BTC+ETH, ridge λ=1 walk-forward with purge+embargo (HYPOTHESES.md:181-183; report.md:2754-2799; research/experiments.jsonl:19) |
| **file:line** | report.md:2838-2858; progress.md:2046-2056 |
| **Blockers stated** | free Coin Metrics snapshot "measured 75 days stale", applied as +75 d on every CM feature (report.md:2734; HYPOTHESES.md:182,185; features.py:38) — **contested: n = 1 retrieval, and the same snapshot's `PriceUSD` stops on the same date; the stage's own pre-registration said +1 day (AUDIT-A-MLCryptoEngine-2)**; CryptoQuant free tier HTTP 401; Blockchain.com has no exchange-flow series; "No exchange publishes flows free" (report.md:2736-2739); class D's Hyperliquid premium series begins 2023-05, capping its window at 45–59 weeks (report.md:2815-2817) — **and at that window the DSR and alpha-t bars were unreachable before any data was seen (AUDIT-A-MLCryptoEngine-11)** |
| **Registered reopen conditions** | "**(a)** a free exchange-flow source at **≤ 2-day** publication lag with **≥ 3 years** of history — the measured 75-day staleness is the binding data constraint on class B; or **(b)** the basis class sustaining **DSR ≥ 0.95 and alpha t ≥ 2 over ≥ 156 scored weeks including a full bear regime** — three times its current window. Reopening H11 does not reopen the alpha search" (HYPOTHESES.md:185) |
| **Trigger already met inside this repository?** | (a) is **in question**: the 75-day figure may measure a stalled GitHub mirror rather than a publication lag, in which case the source the stage itself used already satisfies (a). (b) is unmet and was unreachable at class D's window length |
| **Possibly met by a different repository?** | **Yes** — any repository using a free exchange-flow / on-chain netflow source at ≤ 2-day lag with ≥ 3 years of history satisfies (a) outright; any repository holding ≥ 156 weeks of perp-basis data spanning a bear regime enables (b) |

---

## Part 2 — Detection track (off the alpha register — ADR-044, DECISIONS.md:1929-1964)

### D1 — Hard-rug detection from launch-window state
| field | value |
|---|---|
| **Status** | **Shipped** — "Works — shipped as a clearance scorer" (HYPOTHESES.md:238) |
| **Closure kind** | positive result, shipped as a clearance (never as an alarm) |
| **Closure date** | 2026-08-07 (Stage C.24, progress.md:2383) |
| **Deciding figure (n)** | honest-clearance precision **0.984 at recall 0.538** on the 2024 test fold; the complementary hard-rug alarm only **0.464** precision. **n = 281 pools reached to T0, 194 in the 2024 test fold**; C.24 sweep 360 designed → 281 reached (78.1%) (HYPOTHESES.md:239-240; report.md:3968-3971) |
| **Blockers** | detects hard rugs only; ~99% of launches are scam-adjacent so it filters a small honest minority (HYPOTHESES.md:241). `MLCE_HELIUS_API_KEY` absent at C.21 — **lifted** 2026-08-07 (progress.md:2291-2295, :2317). Credit weights `{rpc:1, enhanced:10}` **UNVERIFIED and never reconciled** (progress.md:2299) |
| **Registered reopen conditions** | none — "Nothing reopens the *result* — it works. Extension is live deployment (score at T0+30min) or widening past hard rugs, which is D2." (HYPOTHESES.md:243) |
| **Possibly met by a different repository?** | n/a |

### D2 — Honest-versus-slow-rug separation
| field | value |
|---|---|
| **Status** | **Concluded** at C.26 — "real but small and unconfirmed" (HYPOTHESES.md:252); "**Concluded, not closed-absent**" (HYPOTHESES.md:257) |
| **Closure kind** | absent at T0 (C.23) + qualified positive post-launch, unconfirmed, with a pre-registered end condition fired on a **measured-unaffordable** price (ADR-054, DECISIONS.md:2204-2239) |
| **Closure date** | 2026-08-07 (Stage C.26, progress.md:2450) |
| **Deciding figures (n)** | Launch window (C.23): decontaminated honest precision **0.574 @ recall ≥ 0.5** against a 0.60 bar at a 0.50 base rate, **n = 194** test fold — labelled "absent signal" (progress.md:2353-2356, :2370-2372). **Contested: 95% Wilson CI [0.465, 0.672] contains the bar; the fold is underpowered for it by ~1.8× (AUDIT-A-MLCryptoEngine-7).** Post-launch (C.24): precision 0.654 @ recall 0.53 vs 0.557 base, lift +0.097 (~1.8 SE). Depth-unbiased (C.25): 6 h mid-stratum lift +0.051 (~0.8 SE), n = +120 honest / 96 reached. Firming (C.26): mid-stratum **+0.032, SE 0.039, 95% CI [−0.045, +0.109]**, n = 84 in the mid stratum / 328 honest / 447 total (HYPOTHESES.md:253-255) |
| **Blockers** | the decon-unbiased test priced at **≈ 124,764 weighted credits, ~1.9× the entire 60,000 cap**, needing a raise to ~180,000 against a registered 65,000 threshold (progress.md:2458-2462; DECISIONS.md:2222-2226) — **contested: denominated in the UNVERIFIED credit unit that supplies 59.1% of the number; rescaled at weight 1 the same estimate is ≈ 50,976, below the cap (AUDIT-A-MLCryptoEngine-8)**; the creator-address restructure fails on identification (0 of 8 pools resolved a creator, DECISIONS.md:2216-2221); C.24's magnitude was reachability-inflated (57% of deep honest pools excluded); SolRPDS has no creator field and covers only the post-graduation stratum (progress.md:2266-2268, :2367-2369); RugCheck's `rugged` flag disqualified on 0 of 4 documented rugs where the registration asked ~10 (**AUDIT-A-MLCryptoEngine-16**) |
| **Registered reopen conditions** | "Reopens on an **affordable decontaminated label** … A soft/slow-rug label cheaper than 30-day insider-sell detail — or a **live forward-recorded cohort** labelled as outcomes arrive — plus a Method-B sample several times larger … Does **not** reopen on a better model" (HYPOTHESES.md:257; DECISIONS.md:2235-2238; progress.md:2473-2474). C.24's earlier form also registered "(b) an **observation cutoff beyond 24h**" (report.md:3539-3545) — **never exercised**; C.25/C.26 stayed at 6 h and 24 h |
| **Trigger already met inside this repository?** | No — but affordability rests on an unverified unit, and the 24 h+ cutoff condition was registered and never run |
| **Possibly met by a different repository?** | **Possibly** — a repository holding cheaper Solana soft/slow-rug labels, a forward-recorded launch cohort, off-chain deploy provenance / pre-launch social-funding graph, or a paid/entitled Solana indexer |

---

## Part 3 — Phases

| phase | status at the anchor | completion condition as registered | met? | file:line |
|---|---|---|---|---|
| **A — data pipeline** | checkbox unticked; criteria met 2026-08-01 | "Phase A passes only when a full day of Kraken data and a full day of Coinbase data both reconstruct with zero unexplained crossed-book events and full-day coverage outside logged reconnect gaps" (progress.md:19-22); "checking the box is the operator's call" (progress.md:227-228) | **Yes** — 2026-07-31 PASS both venues: Kraken 17,489,620 msgs / 17,361,554 CRC32 comparisons / 0 failures / 100.00%; Coinbase 3,408,568 msgs / 0 gaps / 100.00% (n = 1 calendar day per venue) | progress.md:210-224 |
| **B — features/labels/GBT/purged CV** | open by its own text; H1/H2 closed on it anyway | "the research conclusion stays open until it has run over enough days to cover multiple volatility regimes — that depends on continuous recording, not more code" (progress.md:10-13) | **No** — "six days is not six regimes" (progress.md:1811-1812); CME sample "not regime-diverse" (progress.md:1106-1108); the dependency was terminated 2026-08-13. See **AUDIT-A-MLCryptoEngine-17** | progress.md:10-13, 320-336 |
| **C — hftbacktest simulation** | superseded in substance; never ticked | none registered | n/a — "hftbacktest/numba absent and the sparse-touch/slow-L2 shape doesn't fit its queue models — **custom bounded replay required**" | progress.md:2565-2567 |
| **D — paper trading on a VPS** | reached D.1a–D.1d as simulation only; never ticked | none registered | n/a — latency probe started 2026-08-12, usable 2026-08-19; **recording stopped 2026-08-13, so it never became usable** | progress.md:2563-2565, 2619-2626 |
| **E — minimum viable live capital** | not started; E.1/E.2 are write-up and a test fix | none registered | n/a — "No order placed/simulated with capital; engine/ risk code stays line-by-line-review-gated" | progress.md:2574-2575, 2807-2977 |

*The file header still reads "Current phase: **Phase A — data pipeline**" (progress.md:3-4) nine days after "the project is complete" (progress.md:2762), and all five checkboxes are unticked (progress.md:8-19).*

---

## Part 4 — Stage-level blockers recorded in the repository

| blocker | stated at | status at the anchor |
|---|---|---|
| Rust toolchain / webkit2gtk-4.1 / gtk+-3.0 / dbus-1 dev packages absent; install needs sudo | progress.md:44-49, 138-143 | **never lifted**; desktop Rust half never compiled (data pipeline unaffected) |
| `DATABENTO_API_KEY` absent — adapter validated against synthetic records only | progress.md:384-387 | **lifted** 2026-08-02 (progress.md:640-651) |
| Databento exposes no account-balance / usage endpoint; spend tracked from per-request quotes only | progress.md:620-626, 983-990; DECISIONS.md:894-897 | **never lifted** — the ledger records intent, not billing |
| Databento vendor cap $25 | progress.md:666-670 | raised to $120 on 2026-08-02 (progress.md:961-963); $37.8821 still unspent at the anchor |
| June 2026 MBT month charged $35.5144 and never delivered (OOM in `fetch_range`); "Check the portal before any retry" | progress.md:995-1018; DECISIONS.md:855-868 | **never reconciled**; no reversal in the ledger (UNANCHORED read 2026-09-05T05:55Z). **AUDIT-A-MLCryptoEngine-5** |
| `data/databento/session.py` has no CME holiday calendar — every exchange holiday fails coverage | progress.md:1067-1071 | **never fixed** |
| Roll exclusion centred on the splice removes 0 s of the expiry-day dead book | progress.md:1044-1060 | superseded by the C.8 observed-silence exclusion (progress.md:1153-1162) |
| CME's own fee finder is interactive; the exchange fee component rests on a broker's republication | progress.md:1142-1145 | **never independently verified** |
| Kraken base-tier fee wrong (0.25/0.40 → 0.40/0.80 → 0.25/0.40) | progress.md:333-341, 2494-2496; DECISIONS.md:2241-2266 | corrected 2026-08-08; every Kraken figure published 2026-08-01 → 08-08 carries the 2× cost, and the final write-up still quotes 80 bps against a Kraken-measured decile (**AUDIT-A-MLCryptoEngine-17**) |
| 2YY/5YY unresolved continuous symbol — a free, known symbology fix | progress.md:650-652, 928-929, 1222-1224 | **never applied**. **AUDIT-A-MLCryptoEngine-15** |
| 22.6 s host stall 2026-08-03T19:51:25Z, all three venues, no logged gap, cause unknown | progress.md:1323-1335 | "Recorded for a future stage" — **never revisited** |
| `MLCE_HELIUS_API_KEY` absent; the registered bar "**not attempted** — distinct from not cleared" | progress.md:2291-2295 | **lifted** 2026-08-07 (progress.md:2317) |
| Helius credit weights `{rpc:1, enhanced:10}` UNVERIFIED; no keyless usage endpoint | progress.md:2298-2300 | **never verified**, including after the key landed. **AUDIT-A-MLCryptoEngine-8** |
| pump.fun API HTTP 530; Bitquery/Dune/Birdeye 401; MELT "availability unverified" | progress.md:2208-2212 | recorded, not designed around |
| RugCheck `rugged` disqualified on 0 of 4 documented rugs (registration asked ~10) | progress.md:2164-2166, 2204-2206 | **never re-tested**. **AUDIT-A-MLCryptoEngine-16** |
| No per-order Hyperliquid stream (`orderUpdates` is auth'd own-orders only) | progress.md:2549-2553; DECISIONS.md:2273-2279 | **never lifted**; becomes H6's reopening condition. No availability audit was ever performed for order-level data, unlike the C.15/C.19 pattern |
| Hyperliquid latency unmeasured; probe is a proxy floor (POST `/info`, not the signed `/exchange` path); usable 2026-08-19 | progress.md:2563-2565, 2619-2626; DECISIONS.md:2480-2483 | **never accrued** — recording stopped 2026-08-13 |
| hftbacktest/numba absent and unsuitable for the venue's touch shape | progress.md:2565-2567 | replaced by a custom bounded replay (D.1d) |
| Hyperliquid maker fee is documented, not measured — "the weakest input in the chain" | AUDIT.md:350-370; report.md:5169-5175 | **unresolved at the anchor** |
| Leakage suites reach none of `registered.py` / `census.py` / `d1c.py` / `d1d.py` / `fill_replay.py`; `spread.py` and `adverse.py` have no test importing them; H1, H2, H4, H5, H8–H11 are "unaudited, not clean" | progress.md:2756-2760; AUDIT.md:553-566, :535-539, :642-647 | **stated and unresolved at the anchor** |
| The D.1d replay "has still only run once with no second pair of eyes" | DECISIONS.md:2538; report.md:5105-5106 | **unresolved at the anchor**, disclosed in those words |

---

## Part 5 — Named-but-unrun variants

| stage | named variant | ever run? | file:line |
|---|---|---|---|
| Phase B | hyperliquid (costs already wired into the run config at maker 1.5 / taker 4.5 bps) | **no** — skipped once for missing data, never revisited | report.md:773, :775-777; research/experiments.jsonl:2 |
| C.8 | MES (7× lower cost in bps) | **no** — a validated MES day is already on disk | report.md:1086-1088; report.md:1376-1378 |
| C.8 | "a regime that is not a two-month uptrend" on CME | **no** — "CME was not re-run" | report.md:1084-1085; :2490-2491 |
| C.8 | cross-venue features against the crypto recorders | **yes** — C.14 §3, immaterial (ΔAUC ≤ +0.0044) | report.md:1085-1086; :2385-2411 |
| C.9 | the ten thin Hyperliquid perps' adverse selection | **yes** — C.27 | report.md:1240-1251; :4040-4066 |
| C.9 | SIL / MHG (open question) and 2YY / 5YY (failed measurement) | **no** | progress.md:1218-1226 |
| C.13 | a version hedging cross-sectional price exposure | **no** — declared "a different hypothesis" needing its own test | HYPOTHESES.md:135 |
| C.14 | ETH pair on both venues | **no** — dropped for a deadline, disclosed | report.md:2276-2279; progress.md:1756-1757 |
| C.19 | the registered ~10-case known-answer spot check | **no** — executed on 4 | progress.md:2164-2166, :2204-2206 |
| C.24 | an observation cutoff beyond 24 h | **no** | report.md:3541-3542 |
| D.1d | NOT and TNSR through the order-lifecycle fill model | **no** — excluded on the volume clause of the capacity tier | report.md:4057-4058, :4083-4085 |
| D.1b | the blind-universe scoring window | **no** — terminated at 1 of 28 days | report.md:4604-4607; progress.md:2782-2784 |
| D.1b | the accrued Hyperliquid latency distribution | **no** — terminated at 1 of 7 days | report.md:4634-4635, :4704-4705; progress.md:2775-2777 |
| C.18 | outcome-map branch "survivors within noise of zero → extend recording 30 days and re-run" | **no** — never invoked when GMX became unresolved | progress.md:2115-2122 |

---

## Part 6 — Registered triggers in one list

| # | condition, as registered | file:line | met inside this repository? |
|---|---|---|---|
| 1 | H1: round-trip cost below roughly 3 bps | HYPOTHESES.md:54; progress.md:1676-1677 | **arguably yes** — Hyperliquid base tier is exactly 3.0 bps with 13 recorded days, never tested (AUDIT-A-MLCryptoEngine-1) |
| 2 | H2: measurable AUC on a *different* instrument or feature class | HYPOTHESES.md:70 | no — one feature class tested (immaterial); MES and Hyperliquid untested |
| 3 | H3: a maker-rebate venue, or ratio > 1.0 with adverse below the excess | HYPOTHESES.md:86 | **yes on five instruments**, retired for two; NOT and TNSR still meet it (AUDIT-A-MLCryptoEngine-4); CME residue unaddressed (AUDIT-A-MLCryptoEngine-15) |
| 4 | H4: (a) reachable venue with broader shorts **and** (b) out-of-sample persistence | HYPOTHESES.md:102 | no — (b) fails at every correction level |
| 5 | H5: current funding > ~10% annualised sustained for a quarter, measured live | HYPOTHESES.md:118 | no — later measurements move the wrong way |
| 6 | H6: (a) order-level book data, (b) venue fill-level ground truth, or (c) a maker-rebate cost structure | HYPOTHESES.md:197 | no; and no availability audit was performed for (a) |
| 7 | H6 standing: bounded measure re-run over ≥ 4 weeks across regimes | HYPOTHESES.md:205 | **no — abandoned** at 1 of 28 days (AUDIT-A-MLCryptoEngine-10) |
| 8 | H6/D.1b: blind four-week window, earliest close 2026-09-09 | DECISIONS.md:2391-2393 | **no — abandoned** after 1 day |
| 9 | H7: operator reversal of the C.17 decision + restarted recorders | HYPOTHESES.md:220, :508 | no |
| 10 | H8: dispersion widens back **and** the price term stops cancelling the carry | HYPOTHESES.md:135 | no |
| 11 | H9: ≥ half the grid clearing DSR ≥ 0.95 vs BTC on the executable subset with a full bear regime | HYPOTHESES.md:151 | no |
| 12 | H10: ≥ 300 labeled liquidations from a labeled source | HYPOTHESES.md:168 | **possibly, unmeasured** — the `users` → `userFillsByTime` path was never priced (AUDIT-A-MLCryptoEngine-3) |
| 13 | H11: (a) free flow source ≤ 2-day lag, ≥ 3 years history, **or** (b) basis at DSR ≥ 0.95 / t ≥ 2 over ≥ 156 weeks incl. a bear | HYPOTHESES.md:185 | (a) is **in question** — the binding 75-day figure rests on one snapshot (AUDIT-A-MLCryptoEngine-2); (b) unmet and unreachable at the window scored (AUDIT-A-MLCryptoEngine-11) |
| 14 | D2: an affordable decontaminated label or a live forward-recorded cohort | HYPOTHESES.md:257 | no — affordability rests on an UNVERIFIED unit (AUDIT-A-MLCryptoEngine-8) |
| 15 | Phase B: "enough days to cover multiple volatility regimes" | progress.md:10-13 | **no — never met**, and the dependency was terminated (AUDIT-A-MLCryptoEngine-17) |
| 16 | Phase A: a full Kraken day and a full Coinbase day both reconstructing cleanly | progress.md:19-22 | **yes, met 2026-08-01**; box left unticked by operator-call convention |

---

## Leads for the cross-repository pass

Every blocker or reopen condition below might be satisfied, bounded, or contradicted by work held in another repository in the programme. Best guess of the repository in each case; the guess is a starting point, not a claim about that repository's contents.

1. **A measured sub-3-bps round-trip venue, or a maker-rebate tier → VRPExperiment, ORBExperiment, HFExperiment, AiTrader.** This single figure is the reopening condition for **H1** (HYPOTHESES.md:54) and route (c) for **H6** (HYPOTHESES.md:197), and it also decides whether H3's thin tail is economic. MLCryptoEngine's own answer is Hyperliquid at 3 bps, with nothing cheaper reachable from British Columbia (HYPOTHESES.md:322-323). Any repository in the programme that has priced a venue's maker schedule — especially one working equities/futures where rebate tiers are common — either confirms that ceiling or breaks it. Note MLCryptoEngine's own standing rule while checking: "Every fee schedule in this project has been found stale at least once" (HYPOTHESES.md:297-301).
2. **Order-level / L3 / MBO book data carrying arrivals, cancellations or order IDs → ORBExperiment or HFExperiment (equity/futures MBO), secondarily AiTrader.** This is H6's reopening route (a) verbatim (HYPOTHESES.md:197) and the only thing that would let the D.1d closure be re-tested rather than argued. MLCryptoEngine already buys Databento `mbp-10` for CME (report.md:1376-1378), so a sibling repository holding MBO/L3 for *any* venue would show whether the queue-position question is answerable at this programme's budget at all. It would also settle the gap recorded in Part 4: no availability audit was ever performed for order-level Hyperliquid data, unlike the C.15/C.19 pattern this project applies elsewhere.
3. **Venue fill-level ground truth from resting orders (paper or minimum-size live) → AiTrader, or any repository that has run a paper/live execution loop.** H6's route (b), which "measures the net directly and needs no attribution at all" (HYPOTHESES.md:197). MLCryptoEngine declined to spend capital confirming a negative, which is defensible; another repository that already has a paper or $10-minimum live loop could discharge it for free.
4. **CME micro-contract cost decomposition and quote data (MES, MBT, MET, SIL, MHG, 2YY, 5YY) → VRPExperiment first, then ORBExperiment.** Three separate items ride on this: **H2**'s untested MES door (report.md:1086-1088; a validated MES day is already on disk here), **H3**'s unresolved CME residue (progress.md:1218-1226), and the un-verified exchange-fee component ("the exchange component rests on a broker's republication because CME's own fee finder is interactive", progress.md:1142-1144). VRPExperiment works on CME micros and is the most likely holder of a corrected notional or fee decomposition; if it has corrected MBT/MET notionals, every MLCryptoEngine figure quoted in bps of those notionals inherits the staleness.
5. **A free exchange-flow / on-chain netflow source at ≤ 2-day publication lag with ≥ 3 years of history → NPDExperiment, InsiderExperiment, solattn, solclear.** This satisfies **H11 reopening condition (a)** outright (HYPOTHESES.md:185). It is doubly worth chasing because MLCryptoEngine's own binding figure — the 75-day Coin Metrics staleness — rests on one retrieval of a mirror whose price column stops on the same day (AUDIT-A-MLCryptoEngine-2). Any sibling repository that has retrieved the same Coin Metrics community CSVs on a different date settles the question immediately: compare last-row date against retrieval date.
6. **≥ 156 weeks of perpetual-basis data spanning a full bear regime → any repository with a pre-2022 crypto sample.** **H11 condition (b)** (HYPOTHESES.md:185), and the same absence blocks **H5**, **H8** and **H9**, all three of which record "contains no bear market" as their binding limitation (HYPOTHESES.md:116, :133, :149). One repository holding a 2021–2023 crypto series would put four closures back in play at once. Best guess: whichever repository built the longest crypto history — MLCryptoEngine itself reached 2020-01 for *funding* via the free Binance USD-M archive (report.md:1655, :1423), so the same archive is the cheapest route for any sibling.
7. **Post-2026-08 live funding levels and cross-sectional funding dispersion → any repository still recording crypto perps after 2026-08-13.** **H5** reopens on "**Current funding above roughly 10% annualised sustained for a quarter**, measured live rather than from a trailing average" (HYPOTHESES.md:118) and **H8** on dispersion widening back (HYPOTHESES.md:135). MLCryptoEngine's recorders are stopped, so it can never test either trigger again from inside itself; a sibling with a live feed can.
8. **Liquidation-labelled venue or vendor history, or ≥ 300 identified liquidations on any perp venue → any repository holding a perp-venue vendor feed.** **H10**'s reopening condition (HYPOTHESES.md:168). Note the cheaper lead first: the path *inside* MLCryptoEngine (62,905 recorded addresses × `userFillsByTime`) was never priced (AUDIT-A-MLCryptoEngine-3), so a cross-repo lead is only needed if that measurement comes back below 300.
9. **Simultaneous multi-venue book capture over months → any repository recording more than one venue.** **H7** was closed by decision with no measurement at all and its three-venue overlap stopped at 12 days (HYPOTHESES.md:218, :507-508). A sibling with months of two- or three-venue overlap supplies the evidence H7's own preserved design calls for.
10. **A survivorship-free crypto universe, or a reachable venue offering shorts on a materially broader instrument set → any repository that built a point-in-time universe.** **H4** clause (a) (HYPOTHESES.md:102) and half of **H9**'s condition (HYPOTHESES.md:151). MLCryptoEngine solved the universe problem with the Binance monthly archive (progress.md:1297-1301); the *shorts* half is a venue-access question a sibling may have answered.
11. **Cheaper Solana soft/slow-rug labels, a forward-recorded launch cohort, or off-chain deploy provenance → solattn, solclear, InsiderExperiment.** **D2**'s reopening condition (HYPOTHESES.md:257) and C.24's "creator intent" route (report.md:3539-3545). Also worth checking against MLCryptoEngine's identification failure — "0 of 8 pools resolved a creator, because the mint predates pool-activity T0" (DECISIONS.md:2216-2221) — which a sibling with a different indexer may not share.
12. **Helius (or equivalent) credit-weight ground truth → solattn or solclear.** The terminal verdict of MLCryptoEngine's entire detection track is denominated in an UNVERIFIED `{rpc:1, enhanced:10}` unit that supplies 59.1% of the number (AUDIT-A-MLCryptoEngine-8). Any sibling repository holding a Helius account statement, dashboard reading, or documented weight table would either confirm the verdict or reverse it, at zero cost.
13. **Databento invoice or usage reconciliation → any repository with a Databento account.** MLCryptoEngine's **H2** sample was halved by a $35.5144 charge for undelivered bytes that was never reconciled because "the client exposes no usage endpoint, so only the portal can say" (DECISIONS.md:865-868). A sibling repository that has read a Databento invoice knows whether an OOM-killed stream is billed — which is the whole question. Best guess: VRPExperiment or ORBExperiment if either buys Databento; otherwise this is an operator action, not a repository lead.
14. **The methodological precedents MLCryptoEngine exports, checked in the other direction → ORBExperiment, VRPExperiment.** MLCryptoEngine's ADR-023 ("notional decides everything on CME"), ADR-034 (venue-cost asymmetry) and its A3/A6 interval corrections (AUDIT.md:191-195, :264-271) are cited by sibling repositories. Two of them are contested here: the day-clustered interval convention that demoted GMX is inconsistent between the register and the shipped code (AUDIT-A-MLCryptoEngine-9), and the "measured beats documented" rule (ADR-042) was applied to a source measured once (AUDIT-A-MLCryptoEngine-2) while being left unapplied to the project's own credit unit (AUDIT-A-MLCryptoEngine-8). Any repository that inherited those precedents should re-check the inheritance.
