# REOPEN LEDGER — MLCryptoEngine (part p2-register)

**Repository:** MLCryptoEngine · **Anchored SHA:** `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22)
**Scope:** every entry whose primary record sits in my assigned documents — `HYPOTHESES.md` (the alpha
register + the off-register detection track), `DECISIONS.md` (ADR-001 … ADR-066), `AUDIT.md`,
`docs/notes/`, `audit/`. Factual, not advocacy. Line references are to the snapshot at the anchored SHA
and are identical to `git show <SHA>:<path>`.

**Project-level facts that bind every row.** The alpha search ended by pre-registered decision on
2026-08-06 (ADR-043, DECISIONS.md:1907-1911); reversing it "is an explicit operator decision that reopens
nothing retroactively, while every register entry keeps its own evidence-based reopening condition
independently" (DECISIONS.md:1917-1920). **Recording ended 2026-08-13** (DECISIONS.md:2583), which
forecloses every reopening condition phrased as "the recorders accrue this at zero cost" unless a feed is
restarted (one config flip, DECISIONS.md:2426-2427). Kraken and Coinbase were retired 2026-08-12
(ADR-060, DECISIONS.md:2402-2430); all recorded history is immutable and still replayable.

---

## Alpha register (HYPOTHESES.md)

### H1 — Short-horizon directional prediction on crypto spot
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:49) |
| Closure kind | **cost-bound** (HYPOTHESES.md:49; kind defined at :29-31) |
| Closure date | 2026-08-03 (HYPOTHESES.md:49) |
| Deciding figure (n) | 3.31 bps gross capture @900 s vs **80.00 bps** round-trip maker cost; AUC 0.596; net EV −76.69 bps — HYPOTHESES.md:50. **Superseded by C.14**: the same measurement across **four full days** ranges −2.44 to +3.05 bps (n=4 days; per-day values +3.05/+0.15/−2.44/+0.74 at report.md:2366,2378) — HYPOTHESES.md:50. Sample: Coinbase + Kraken spot, "single-digit days", 42 features, horizons 100 ms–900 s — HYPOTHESES.md:51; C.14 sample counts 165,075 (Kraken) / 41,780 (Coinbase) / 123,864 (deep) over six validated days — docs/notes/h1-predictability-without-capturability.md:301 |
| Blockers | retail spot round trips 50 bps (Kraken) / 80 bps (Coinbase) — HYPOTHESES.md:305-306; "sub-3 bps round trip needs $10M–$250M of trailing 30-day volume" — HYPOTHESES.md:516-517; "Anything requiring co-location or sub-millisecond latency, ruled out by ADR-002's 5–100 ms design tier" — HYPOTHESES.md:518-519 |
| Reopen conditions | "A round-trip cost below roughly **3 bps**, i.e. under 1.5 bps per side… It does not reopen on more data at the same venues." + "Reopening now additionally requires the top-confidence decile to clear a round trip somewhere, which it does not." — HYPOTHESES.md:54; quoted character-for-character and pinned by test at docs/notes/h1-predictability-without-capturability.md:261-263 (rule: DECISIONS.md:2623-2626) |
| Trigger met inside this repo? | **Arguably yes, unrevisited.** The same file records the cheapest reachable venue at exactly the threshold: Hyperliquid perps base tier 1.5 bps/side = **3.0 bps round trip** (HYPOTHESES.md:307) and "The cheapest venue reachable from British Columbia is Hyperliquid at 3 bps" (HYPOTHESES.md:322-323). No directional test was ever run on that venue. See DRAFT-p2-register-3. |
| Possibly met by another repo? | **Yes** — any repository measuring directional microstructure capture at a ≤3 bps round-trip venue, or any venue-access change reaching a 0 bps maker tier. |

### H2 — Transfer of the edge to CME micro futures
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:65) |
| Closure kind | **signal-absent** (HYPOTHESES.md:65; kind defined at :32-34 — "Does not reopen on a better model, a better feature set, or lower fees") |
| Closure date | 2026-08-03 (HYPOTHESES.md:65) |
| Deciding figure (n) | AUC **0.501** at every horizon; 0.22 bps gross capture vs **5.33 bps** cost; best net EV −5.11 bps; the one figure clearing noise (+0.215 bps @900 s) reversed to −0.785 on a stride-1 control — HYPOTHESES.md:66,70. n = **224,425,675 events / 989 scheduled-open hours / two validated MBT months (2026-04, 2026-05)** — HYPOTHESES.md:67; **one clean walk-forward fold** — DECISIONS.md:1005 |
| Blockers | range is two months not four because the backfill stopped under the $120 cap after a $35.51 charge for undelivered bytes — DECISIONS.md:855-859; "Resuming June and July requires first reconciling the June charge against the Databento invoice — … only the portal can say whether the killed stream was billed" — DECISIONS.md:865-868 (never executed; live `data/vendor/spend_ledger.jsonl` totals $82.1179 of the $120 cap, last entry 2026-08-04, read 2026-09-05T05:59Z, UNANCHORED); vendor client exposes no usage endpoint — DECISIONS.md:894-897 |
| Reopen conditions | "Reopens only on evidence of measurable AUC on a *different* instrument or feature class — never on a re-run of the same pipeline against the same contract with a stronger learner." — HYPOTHESES.md:70 |
| Trigger met inside this repo? | No. The one different feature class measured (cross-venue) is worth ΔAUC ≤ +0.0044 — HYPOTHESES.md:70. A different instrument/venue (Hyperliquid perps) was recorded and never tested — see DRAFT-p2-register-3. |
| Possibly met by another repo? | **Yes** — any repository reporting measurable directional AUC on a different instrument class or feature class. |

### H3 — Passive spread capture
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:81); its "measured tail" resolved into H6 and is declared to close with it at HYPOTHESES.md:205 |
| Closure kind | **cost-bound**, "with a measured tail still open (see H6)" (HYPOTHESES.md:81) |
| Closure date | 2026-08-03; tail closed 2026-08-12 (HYPOTHESES.md:81,196,205) |
| Deciding figure (n) | spread − adverse − cost, bps: Hyperliquid BTC **−3.05**, ETH **−2.75**, CME MBT **−4.25**; **0 of 28** surveyed instruments with ratio > 1.0, best M6A 0.98 — HYPOTHESES.md:82. n = 53.13 quoted hours / **2,151,124 bbo updates** (Hyperliquid, ~2 days) + a 16-contract CME bbo-1s survey on a **single day** costing $0.7763 — HYPOTHESES.md:83-84 |
| Blockers | no reachable maker-rebate venue — HYPOTHESES.md:86 and :515; every figure is an upper bound because a fill is assumed — HYPOTHESES.md:84, ADR-026 DECISIONS.md:1102-1108 |
| Reopen conditions | "A venue paying **maker rebates** (none reachable from British Columbia does), or an instrument whose spread-to-cost ratio exceeds 1.0 *with* adverse selection below the excess." — HYPOTHESES.md:86 |
| Trigger met inside this repo? | **Yes, on five instruments, and retired for only two.** C.27 found PUMP +4.30, MERL +6.45, GMX +0.40, NOT +31, TNSR +35 net of adverse and cost — HYPOTHESES.md:198. PUMP and MERL were replayed and closed; GMX was discounted; **NOT and TNSR were never replayed** — see DRAFT-p2-register-1. |
| Possibly met by another repo? | **Yes** — a maker-rebate venue reachable elsewhere in the program, or a spread-to-cost > 1.0 instrument measured in another repository. |

### H4 — Cointegration pairs trading
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:97) |
| Closure kind | **signal-absent** (HYPOTHESES.md:97) |
| Closure date | 2026-08-04 (HYPOTHESES.md:97) |
| Deciding figure (n) | **0 of 180** formation-window survivors remain significant out of sample; holdout **91 raw hits vs 77.0 expected by chance**; BTC/ETH p = **0.1169**; deflated Sharpe of best survivor **0.026** — HYPOTHESES.md:98. n = **1,826 daily bars** (2021-08-01 → 2026-07-31), **1,653 pairs**, 60-symbol point-in-time universe of which 12 (20%) died in sample — HYPOTHESES.md:99 |
| Blockers | break-even costs 300–550 bps vs a 3 bps venue — cost explicitly *not* binding — HYPOTHESES.md:102; venue (Binance) cannot be traded from British Columbia — DECISIONS.md:1357-1359; only 5 of 12 subscribed Hyperliquid perps existed at the 2021 sample start; HYPE and MERL never listed on Binance — HYPOTHESES.md:102 |
| Reopen conditions | "(a) a reachable venue offers shorts across a materially broader instrument set … **and** (b) relationships persist out of sample, which they did not at any correction level." — HYPOTHESES.md:102 |
| Trigger met inside this repo? | No — (b) fails at every correction level; (a) is about 2021-era historical coverage, not present breadth. |
| Possibly met by another repo? | **Yes** for clause (a) — any repository with a reachable venue offering shorts across a broader instrument set with multi-year history. |

### H5 — Funding rate carry
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:113) |
| Closure kind | **"Closed as currently unattractive — decayed, not disproved"** (HYPOTHESES.md:113) |
| Closure date | 2026-08-04 (HYPOTHESES.md:113) |
| Deciding figure (n) | **8.07% (ETH) / 8.00% (BTC)** net annualised on deployed capital, 5 of 10 instruments clearing a 4% risk-free rate by 1.6–4.1 points, against a **~85% yield decay**: Binance BTC funding 30.61% (2021) → 11.92% (2024) → 5.13% (2025) → **1.94% (2026)**; ETH 37.54% → 0.97% — HYPOTHESES.md:114. n = Hyperliquid hourly funding 2023-05-12 → 2026-08-04, **3.23 years, 27,761 rows for BTC, 12 perps**; Binance 8-hourly 2020-01 → 2026-07 for the decay curve — HYPOTHESES.md:115 |
| Blockers | "**Contains no full bear market.** Hyperliquid launched *after* the 2022 drawdown" — HYPOTHESES.md:116; perp prices reconstructed as `spot × (1 + premium)` because the candle endpoint serves only ~5,000 bars — HYPOTHESES.md:116 |
| Reopen conditions | "**Current funding above roughly 10% annualised sustained for a quarter**, measured live rather than from a trailing average" — HYPOTHESES.md:118 |
| Trigger met inside this repo? | No. The only later funding measurement is D.1c's, which found funding immaterial at ≤0.33 bps of filled notional — HYPOTHESES.md:204. |
| Possibly met by another repo? | **Yes** — a live-measured funding series after 2026-08-04 anywhere in the program would test this trigger directly. |

### H6 — Spread capture on thin perpetuals
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:196); previously *resolved-positive* at C.27 and routed to D.1 (HYPOTHESES.md:200) |
| Closure kind | **kill condition fired** — "By the pre-registered kill condition (both ≤ 0 at declared cap and floor) **H6 closes and D.2 does not follow**" (HYPOTHESES.md:197); reconfirmed under audit correction the same day (HYPOTHESES.md:196) |
| Closure date | 2026-08-12 (HYPOTHESES.md:196) |
| Deciding figure (n) | **PUMP −4.81, MERL −4.35 bps** per filled notional **per leg** at the declared 2.5×Q cap and 162 ms latency floor (corrected; pre-correction −4.75 / −4.23) — HYPOTHESES.md:196-197, report.md:5122. Per round trip: **−9.62** (report.md:5177). No zero-crossing on the {+0…+800} ms latency grid — HYPOTHESES.md:197. n = 8 replay days / **28,658,883 records** (AUDIT.md:490); underlying census n = **499,912** scored prints (PUMP) and **25,348** (MERL) at the worst horizon (`audit/census_ci.json`); 32,018 / 4,270 fills pre-correction, 31,875 / 2,536 post (report.md:5051) |
| Blockers | no per-order stream on the feed, so queue position is unobservable and "**no precise queue model is estimable**" (87–99% of levels clear by cancellation) — HYPOTHESES.md:203, DECISIONS.md:2273-2279; latency measurable only as a **proxy floor** (p50 162 ms), true path unmeasurable without placing an order — DECISIONS.md:2480-2483; the Hyperliquid maker fee is a **documented, not measured** figure and "the weakest input in the chain" — AUDIT.md:350-370, report.md:5169-5175; the D.1d replay "has still only run once with no second pair of eyes" — DECISIONS.md:2538; **recording ended 2026-08-13** — DECISIONS.md:2583 |
| Reopen conditions | rewritten 2026-08-12 (audit A13): the net must survive an order-lifecycle fill model, by one of **(a) order-level book data** carrying arrivals/cancellations/order IDs; **(b) venue fill-level ground truth** from actually resting orders — paper or minimum-size live; **(c) a materially different cost structure, e.g. a maker-rebate tier** — HYPOTHESES.md:197. Explicitly **not** reopened by lower latency, a better queue model from this feed, more weeks of per-fill accounting, or re-attribution between edge and inventory — HYPOTHESES.md:197. Standing caveat: a D.1 conclusion resting on more than one week needs "**≥ 4 weeks spanning more than one volatility regime**" — HYPOTHESES.md:205; blind-universe re-scoring rule with "Earliest close 2026-09-09" — DECISIONS.md:2391-2393 |
| Trigger met inside this repo? | No for (a)/(b)/(c). **The ≥4-week and blind-universe clocks can no longer be met**: recording stopped 2026-08-13, one day after the blind universe was subscribed — DECISIONS.md:2583 vs :2390-2393; disclosed at progress.md:2782-2784 but not in the register (see DRAFT-p2-register-7). The "screened positives" demotion (HYPOTHESES.md:204, ADR-059 DECISIONS.md:2395-2396) is therefore permanent. |
| Possibly met by another repo? | **Yes** — a repository holding order-level (MBO / order-ID) book data for any thin perpetual, or venue fill-level ground truth from resting orders, or access to a maker-rebate tier. |

### H7 — Cross-venue divergence
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:216) |
| Closure kind | **closed by decision** — "the C.17 end condition, not evidence" (HYPOTHESES.md:216) |
| Closure date | 2026-08-06 (HYPOTHESES.md:216) |
| Deciding figure (n) | **none measured directly** (HYPOTHESES.md:217). Nearest evidence: Hyperliquid perp-to-own-index premium mean **0.65 bps**, p99 **14.59 bps**, worst adverse hourly move **38.2 bps** — explicitly "**not** the cross-venue number" — HYPOTHESES.md:217 |
| Blockers | three-venue overlap only since 2026-08-01, "measured in weeks" — HYPOTHESES.md:218; kraken/coinbase retired at D.1b so the overlap **stopped accruing at 12 days** — HYPOTHESES.md:507-508, DECISIONS.md:2413-2421; two-leg round-trip cost of 160 bps for spot-to-spot — HYPOTHESES.md:219 |
| Reopen conditions | operator reversal of the 2026-08-06 decision, "at which point the original design above stands unchanged" — HYPOTHESES.md:220; plus restarting the retired recorders — HYPOTHESES.md:508 (ADR-060, one config flip, DECISIONS.md:2426-2427) |
| Trigger met inside this repo? | No — the decision has not been reversed and the overlap stopped at 12 days. Fully disclosed by the authors at HYPOTHESES.md:505-508. |
| Possibly met by another repo? | **Yes** — a cross-venue basis measured over months in another repository would supply the evidence H7's own design calls for. |

### H8 — Cross-sectional funding carry
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:130) |
| Closure kind | **"signal present, cancelled by its own hedge"** (HYPOTHESES.md:130) |
| Closure date | 2026-08-05 (HYPOTHESES.md:130) |
| Deciding figure (n) | funding income **+43.68%/yr**, price return **−42.91%**, cost −0.66% → **net +0.11%** vs a 4% risk-free rate (shortfall 3.89 points); max drawdown **−75.85%**; price-term daily vol **10.9×** the funding term's — HYPOTHESES.md:131. n = **231 usable perps / 55 delisted and retained, 4,411,046 hourly funding observations, 1,182 days** (2023-05-12 → 2026-08-05) — HYPOTHESES.md:132 |
| Blockers | "**Contains no bear market**" — HYPOTHESES.md:133; delisted perps assumed to liquidate at last printed price while the venue settles at an unobservable oracle price — HYPOTHESES.md:133; break-even **1.76 bps/side against 1.5 modelled** at 51.7× annual turnover, a 17% margin — HYPOTHESES.md:135 |
| Reopen conditions | two independent changes, both required: dispersion must widen back (it fell 77%, 241.50% → 53.45% decile spread on a fixed cohort) **and** "the price term would have to stop cancelling the carry" (baskets correlate −0.718) — HYPOTHESES.md:135. A cross-sectionally price-hedged version "would be a different hypothesis, and would need its own test" — HYPOTHESES.md:135 (named variant, never run; disclosed as out of scope) |
| Trigger met inside this repo? | No. |
| Possibly met by another repo? | **Yes** — a later-dated dispersion measurement, or a cross-sectional carry book with a beta/sector hedge tested elsewhere in the program. |

### H9 — Time-series momentum on daily bars
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:146) |
| Closure kind | **"insignificant after deflation, and untradeable where it appears"** (HYPOTHESES.md:146) |
| Closure date | 2026-08-06 (HYPOTHESES.md:146) |
| Deciding figure (n) | primary spec L90/H30 net-of-3bps Sharpe **0.302** vs BTC buy-and-hold **0.183**, but **deflated Sharpe 0.446** against 12 registered trials, **alpha t = 1.01**, **7/12** specs positive; the three specs clearing the literal bar are all at the 7-day hold; on the **27 executable symbols** the primary collapses to Sharpe **0.013**; best single cell L30/H7 net Sharpe 0.647 deflating to 0.732 — HYPOTHESES.md:147. n = 58 symbols in matrix from a 60-member point-in-time universe (12 died in sample), 2021-08 → 2026-07 daily bars — HYPOTHESES.md:148 |
| Blockers | measured book is net short (−0.275 mean exposure), negative beta in every cell, earning +56.9%/yr in down-trends vs −14.7%/yr in up — "Its income requires an alt bear market to exist" — HYPOTHESES.md:149; the full-universe result lives in coins no reachable venue lists — HYPOTHESES.md:151 |
| Reopen conditions | "on data that includes a full bear regime, **at least half the registered grid** beats buy-and-hold BTC risk-adjusted with **deflated Sharpe ≥ 0.95**, **and** the effect survives on the executable subset … A single cell clearing any bar reopens nothing" — HYPOTHESES.md:151 |
| Trigger met inside this repo? | No. |
| Possibly met by another repo? | **Yes** — a momentum grid run on a universe including a full bear regime and a broader executable subset. |

### H10 — Liquidation aftermath reversion
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:163) |
| Closure kind | **"unidentifiable in available data"** — a data-availability closure, explicitly "a **third kind**, distinct from cost-bound and signal-absent" (HYPOTHESES.md:163,166) |
| Closure date | 2026-08-06 (HYPOTHESES.md:163) |
| Deciding figure (n) | **Zero identifiable liquidations in 2,639,510 recorded fills** (2026-08-01 → 2026-08-06, 12 instruments); one key-set on every fill `(coin, hash, px, side, sz, tid, time, users)` with no flag; zero `liquidat` occurrences in any channel; the anomalous all-zeros hash (18.0% of fills) ground-truths via `userFillsByTime` to TWAP fills; three global-history endpoint names return HTTP 422 — HYPOTHESES.md:164. No bar was ever registered because the comparison is unsupported — report.md:2685-2688 |
| Blockers | no liquidation flag in the public trades stream and no public global-history endpoint (HTTP 422) — HYPOTHESES.md:164; the venue's label is per-user only, and per-user labelling was priced as "weeks of querying" — report.md:2664-2670 (**contested: 62,905 distinct addresses, see DRAFT-p2-register-4**); "nothing before 2026-08-01 at any price" — report.md:2670; large-trade proxies declined by design — HYPOTHESES.md:166 |
| Reopen conditions | "A liquidation-labeled source: the venue flagging liquidations in the public trades stream, a global history endpoint, or labeled vendor data — covering **≥ 300 labeled liquidations across the subscribed instruments** with timestamps alignable to recorded BBO mids at ≤ 1 s." Below 300 the answer is "too thin" by prior declaration. "nothing reopens on proxied labels." — HYPOTHESES.md:168 |
| Trigger met inside this repo? | **Contested.** The recorded fills carry counterparty addresses and the venue's `userFillsByTime` carries the `liquidation` object; the closure declined that route on a cost estimate the raw capture contradicts by ~47–94× (DRAFT-p2-register-4). Whether ≥300 labelled events exist in the recorded week is unmeasured. |
| Possibly met by another repo? | **Yes** — any repository holding liquidation-labelled venue or vendor history for these instruments. |

### H11 — Medium-horizon prediction on untested feature classes
| field | value |
|---|---|
| Status | closed (HYPOTHESES.md:180) — "the closure that ended the alpha search by decision" |
| Closure kind | **FAIL on all six pre-registered bars** (HYPOTHESES.md:180; binding end condition ADR-043, DECISIONS.md:1907-1911) |
| Closure date | 2026-08-06 (HYPOTHESES.md:180) |
| Deciding figure (n) | **0 of 40 registered cells pass**; best deflated Sharpe **0.499** vs the 0.95 bar; best alpha t **1.35** vs 2; stablecoin class negative in 8/8 cells; break-even costs 22–1,059 bps/side vs 1.5 modelled — HYPOTHESES.md:181. n = weekly 2020-08-02 → 2026-07-26 (up to 207 scored weeks; **class D only 45–59 weeks**), BTC + ETH, ridge λ=1 walk-forward with purge+embargo — HYPOTHESES.md:182-183 |
| Blockers | free Coin Metrics snapshot **measured 75 days stale**, applied as a +75d lag to class B — HYPOTHESES.md:182,185, DECISIONS.md:1865-1868 (**n = 1 retrieval, 2026-08-06; see DRAFT-p2-register-5**); class D's Hyperliquid premium series begins 2023-05, capping its scored window at 45–59 weeks — HYPOTHESES.md:181,183; CryptoQuant free tier HTTP 401 without an account key and no reachable exchange publishes free wallet-flow history — report.md:2736,2739 |
| Reopen conditions | "**(a)** a free exchange-flow source at **≤ 2-day** publication lag with **≥ 3 years** of history … or **(b)** the basis class sustaining **DSR ≥ 0.95 and alpha t ≥ 2 over ≥ 156 scored weeks including a full bear regime** — three times its current window. Reopening H11 does not reopen the alpha search" — HYPOTHESES.md:185 |
| Trigger met inside this repo? | No, but (a)'s binding figure is a single measurement never repeated — DRAFT-p2-register-5. |
| Possibly met by another repo? | **Yes** — a repository naming a free exchange-flow source at ≤2-day lag with ≥3 years of history would satisfy (a) outright; a repository holding ≥156 weeks of basis data spanning a bear regime would enable (b). |

---

## Detection track (off the alpha register — ADR-044, DECISIONS.md:1929-1964)

### D1 — Hard-rug detection from launch-window state
| field | value |
|---|---|
| Status | **shipped** — "Works — shipped as a clearance scorer" (HYPOTHESES.md:238) |
| Closure kind | positive result, shipped as a clearance (never as an alarm) — HYPOTHESES.md:239 |
| Closure date | 2026-08-07 (HYPOTHESES.md:238) |
| Deciding figure (n) | honest-clearance precision **0.984 at recall 0.538** on the 2024 test fold; the complementary hard-rug alarm is only **0.464** precision — HYPOTHESES.md:239. n = **281 pools reached to T0, 194 in the 2024 test fold** — HYPOTHESES.md:240 |
| Blockers | detects hard rugs only; ~99% of launches are scam-adjacent so it filters a small honest minority — HYPOTHESES.md:241 |
| Reopen conditions | none — "Nothing reopens the *result* — it works. Extension is live deployment (score at T0+30min) or widening past hard rugs, which is D2." — HYPOTHESES.md:243 |
| Trigger met inside this repo? | n/a |
| Possibly met by another repo? | n/a |

### D2 — Honest-versus-slow-rug separation
| field | value |
|---|---|
| Status | **concluded** at C.26 — "real but small and unconfirmed" (HYPOTHESES.md:252) |
| Closure kind | **measured-unaffordable** — the confirmation has a price the project declines to pay; "a **measured closure, not a gap**" (DECISIONS.md:2233-2235); explicitly "**Concluded, not closed-absent**" (HYPOTHESES.md:257) |
| Closure date | 2026-08-07 (HYPOTHESES.md:252; ADR-054, DECISIONS.md:2204-2239) |
| Deciding figure (n) | mid-activity-stratum 6 h lift **+0.032, SE 0.039, 95% CI [−0.045, +0.109]** — the firming sweep moved the estimate *down* from C.25's +0.051 — HYPOTHESES.md:253. n = **84** in the mid stratum (HYPOTHESES.md:255); sample = 281 decon-labelled pools + **120 random honest pools** retrieved depth-independently via Method B (HYPOTHESES.md:254) |
| Blockers | decon-unbiased test priced at **≈124,764 weighted credits, ~1.9× the entire 60,000 cap**, needing a raise to ~180,000 against a registered 65,000 threshold — DECISIONS.md:2222-2226; the creator-address restructure **fails on identification** — 0 of 8 pools resolved a creator, because the mint predates pool-activity T0 — DECISIONS.md:2216-2221; C.24's magnitude was reachability-inflated (57% of deep honest pools excluded) — HYPOTHESES.md:255 |
| Reopen conditions | "Reopens on an **affordable decontaminated label** … A soft/slow-rug label cheaper than 30-day insider-sell detail — or a **live forward-recorded cohort** labelled as outcomes arrive — plus a Method-B sample several times larger … Does **not** reopen on a better model" — HYPOTHESES.md:257; restated at DECISIONS.md:2235-2238 |
| Trigger met inside this repo? | No. |
| Possibly met by another repo? | **Possibly** — a repository holding cheaper Solana soft/slow-rug labels or a forward-recorded launch cohort. |

---

## Register-level and cross-cutting items

| item | record | line |
|---|---|---|
| Alpha search concluded by pre-registered decision | C.17 FAIL on six bars ends the search; reversal is an explicit operator decision reopening nothing retroactively | DECISIONS.md:1907-1920; HYPOTHESES.md:538-545 |
| Recording ended | 2026-08-13; every register entry closed | DECISIONS.md:2583 (disclosure of consequences at progress.md:2762-2804) |
| Blind universe (ADR-059) | registered 2026-08-12, seed 20260812, 25 blind picks of 177 live perps, PUMP/MERL carried over as non-blind; **earliest close 2026-09-09**; 1 day of capture actually taken | DECISIONS.md:2373-2400; report.md:4641-4660; progress.md:2782-2784 |
| Screened-positive demotion | C.9 selection was spread-motivated; BH corrected 10 of 177 screened; survivors demoted to "screened positives", to be resolved by the blind ≥4-week re-run | HYPOTHESES.md:204; DECISIONS.md:2377-2380; AUDIT.md:282-296 |
| Kraken/Coinbase retired | 2026-08-12, venue kind `retired`; history immutable; resurrection is one config flip | DECISIONS.md:2402-2430 |
| Fee-schedule staleness rule | "Every fee schedule in this project has been found stale at least once"; Kraken corrected 0.40/0.80 → 0.25/0.40, no closure flips | HYPOTHESES.md:297-301; DECISIONS.md:2241-2266 |
| Hyperliquid maker fee provenance | hardcoded, unsourced and undated at audit time; now one sourced statement but still **documented, not measured** — "the weakest input in the chain" | AUDIT.md:350-370; report.md:5169-5175 |
| Audit scope limit | H1, H2, H4, H5, H8–H11 are **"unaudited, not clean"** — read, not re-derived | AUDIT.md:535-539, :642-647; restated docs/notes/h1-predictability-without-capturability.md:210-218 |
| Test coverage of the closure chain | no leakage suite, canary or prefix-invariance test reaches `registered.py`, `census.py`, `d1c.py`, `d1d.py` or `fill_replay.py`; `spread.py` and `adverse.py` have **no test file importing them** | AUDIT.md:553-566; report.md:5186-5189 |
| Standalone-note discipline | closed results written up under `docs/notes/`, figures pinned to the register by test, reopening conditions quoted character-for-character | DECISIONS.md:2579-2641 |
