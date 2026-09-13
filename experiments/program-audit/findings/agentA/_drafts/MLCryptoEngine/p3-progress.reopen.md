# REOPEN LEDGER — MLCryptoEngine, part p3-progress

Repository **MLCryptoEngine** @ anchored SHA `5359a11fc753cdcd2606aea991dae826293d0307`
(main, 2026-08-22). Scope: entries whose stage record lives in my assigned documents —
`progress.md` (read in full), `research/` (incl. `research/experiments.jsonl`), `backtest/`.

**This ledger is factual, not advocacy.** Every figure is transcribed from the snapshot with a
file:line. Where the register (`HYPOTHESES.md`) is the authoritative statement of a status or a
reopening condition, that is another reader's primary document and is marked `[HYP]`; the
`progress.md` line is given wherever the same fact appears there. Line numbers are snapshot
line numbers and are identical to `git show <SHA>:<path>`.

Two ledger entries are read from **live-repo untracked data** and are therefore **UNANCHORED**
(read 2026-09-05T05:55Z, may have changed after the anchor): `data/vendor/spend_ledger.jsonl`
and `data/vendor/helius_credit_ledger.jsonl`.

---

## Part 1 — Phases

| entry | status | closure kind | closure date | deciding figure (n) | file:line | blockers (file:line) | registered reopen / completion condition (file:line) | possibly met by another repo? |
|---|---|---|---|---|---|---|---|---|
| **Phase A — data pipeline** | **open (checkbox unticked at the anchor)**; criteria met, box deliberately left unchecked | n/a — completion, not a hypothesis | criteria met 2026-08-01; never ticked | 2026-07-31 PASS both venues: Kraken 17,489,620 msgs / 17,361,554 CRC32 comparisons / 0 failures / coverage 100.00%; Coinbase 3,408,568 msgs / 3,408,568 sequence checks / 0 gaps / 100.00% (n = 1 calendar day, 86,400 s span per venue) | progress.md:210-224 | Rust toolchain + webkit2gtk-4.1/gtk+-3.0/dbus-1 dev packages absent, installation needs sudo (progress.md:44-49, 138-143) — desktop half only, not the data pipeline | "Phase A passes only when a full day of Kraken data and a full day of Coinbase data both reconstruct with zero unexplained crossed-book events and full-day coverage outside logged reconnect gaps." (progress.md:19-22); "checking the box is the operator's call" (progress.md:227-228) | no |
| **Phase B — features/labels/GBT/purged CV** | **open by its own text; hypotheses closed on it anyway** | n/a | pipeline validated 2026-08-01; H1/H2 closed 2026-08-03 | Kraken BTC/USD AUC 0.940 @100 ms → 0.668 @30 s; EV ≈ −50 bps maker (n = 1 day, 153,942 valid samples) at first run (progress.md:320-331); restated on corrected fees 2026-08-02 (progress.md:495-520) | progress.md:10-13, 320-336 | "that depends on continuous recording, not more code" (progress.md:12-13) — recording stopped 2026-08-13 (progress.md:2762) | "the research conclusion stays open until it has run over enough days to cover multiple volatility regimes" (progress.md:10-13). **Never satisfied**: "six days is not six regimes" (progress.md:1811-1812); CME sample "not regime-diverse" (progress.md:1106-1108) | no |
| **Phase C — hftbacktest simulation** | superseded in substance; never ticked | n/a | — | "hftbacktest/numba absent and the sparse-touch/slow-L2 shape doesn't fit its queue models — **custom bounded replay required**" (n/a) | progress.md:2565-2567 | hftbacktest/numba absent; venue shape unsuitable (progress.md:2565-2567) | none registered | no |
| **Phase D — paper trading on a VPS** | reached D.1a–D.1d as simulation only; never ticked | n/a | — | D.1d bounded replay: PUMP −4.75, MERL −4.23 bps per filled notional (corrected −4.81 / −4.35); 28.7M records, 19 variants | progress.md:2663-2664, 2716-2719 | Hyperliquid latency "not measured" at D.1a; probe started 2026-08-12, usable 2026-08-19 (progress.md:2563-2565, 2619-2626) — **recording stopped 2026-08-13, so it never became usable** | none registered | no |
| **Phase E — minimum viable live capital** | not started; E.1/E.2 are write-up and a test fix | n/a | — | — | progress.md:2807-2977 | "No order placed/simulated with capital; engine/ risk code stays line-by-line-review-gated" (progress.md:2574-2575) | none registered | no |

*Note:* at the anchor the file header still reads "Current phase: **Phase A — data pipeline**"
(progress.md:3-4) nine days after "the project is complete" (progress.md:2762). All five phase
checkboxes are unticked (progress.md:8-19).

---

## Part 2 — Alpha-track hypotheses (H1–H11)

### H1 — Short-horizon directional prediction on crypto spot
- **Status:** Closed. `[HYP]` "**Closed — cost-bound** · 2026-08-03" (HYPOTHESES.md:49).
- **Closure kind:** cost-bound — defined in progress.md:1543-1545 as "a real signal smaller than the cost of capturing it, which reopens at a materially lower fee tier".
- **Closure date:** 2026-08-03 (register); the register entry itself was created at Stage C.12, 2026-08-04 (progress.md:1531-1577).
- **Deciding figure (n):** 3.31 bps gross capture at 900 s vs 80.00 bps round-trip maker, AUC 0.596, net EV −76.69 bps, Coinbase BTC-USD, **n = 1 day (2026-07-31)**; 31,640 samples for that venue-symbol in the first run (research/experiments.jsonl:1, `coinbase BTC-USD` → `n_samples`). Superseded 2026-08-05: across **four full days** the same measurement ranges **−2.4378 to +3.0497 bps**.
- **file:line:** progress.md:1128-1129 (3.31 vs 80), progress.md:1549-1551 (register summary), progress.md:1778-1785 (supersession), progress.md:1594-1598 (restated table).
- **Blockers:** none stated for the measurement itself. Cost blockers stated: Kraken/Coinbase base-tier maker fees; the fee schedule itself was wrong twice (progress.md:333-341 → 0.40/0.80; progress.md:2494-2496 → back to 0.25/0.40).
- **Registered reopen conditions:** "H1 closed on **cost** and reopens only below ~3 bps round trip." (progress.md:1676-1677). `[HYP]` fuller text at HYPOTHESES.md:53: "A round-trip cost below roughly **3 bps**, i.e. under 1.5 bps per side… **Reopens on cost, not on modelling**… Reopening now additionally requires the top-confidence decile to clear a round trip somewhere".
- **Possibly met by other-repo work?** **Yes — flag for the cross-repo pass.** The trigger may already be met *inside this repository* (Hyperliquid base tier = 3.0 bps round trip, research/microstructure/fees.py; 13 recorded days, progress.md:2789-2793 — see DRAFT-p3-progress-2). For the cross-repo pass: any repository holding a measured sub-3 bps round-trip venue, a maker-rebate venue, or a directional-model capture figure on a low-fee perp venue would meet H1's condition.

### H2 — Transfer of the edge to CME micro futures
- **Status:** Closed. `[HYP]` "**Closed — signal-absent** · 2026-08-03" (HYPOTHESES.md:65).
- **Closure kind:** signal-absent — "does **not** reopen on a better model, a better feature set, or lower fees" (progress.md:1546-1548).
- **Closure date:** 2026-08-03 (Stage C.8, progress.md:1115).
- **Deciding figure (n):** AUC 0.596 → **0.501**; capture 0.22 bps against 5.33 bps cost; net EV −5.11. **n = 53 days of samples** from 224,425,675 vendor events over 989.00 h scheduled-open (April + May 2026 MBT); 1,109,072 training samples; one clean walk-forward fold, not three.
- **file:line:** progress.md:1128-1131 (headline), progress.md:1120-1123 (event/day counts), progress.md:1150-1152 (fold count), progress.md:1100-1108 (regime caveat), research/experiments.jsonl:3 (run `99ad7dde…`, 53 dates, stride) and :4 (10-day stride-1 control).
- **Blockers:** budget. Cap $25 → $120 (progress.md:961-963); four-month range priced $97.08 (progress.md:975-976); June download OOM-killed after the charge was committed, $35.5144 charged and never delivered (progress.md:986, 995-1005); "**The four-month range no longer fits.** Ledger: **$81.3416 spent, $38.6584 remaining**" (progress.md:1007-1009). Ledger verified UNANCHORED: 29 entries, total $82.1179, no reversing entry (`data/vendor/spend_ledger.jsonl`, read 2026-09-05T05:55Z).
- **Registered reopen conditions:** "H2 closed on **absent signal** and reopens only on measurable AUC — which Task 4 is the test of." (progress.md:1677-1679). `[HYP]` HYPOTHESES.md:69: "Reopens only on evidence of measurable AUC on a *different* instrument or feature class — never on a re-run of the same pipeline against the same contract with a stronger learner."
- **Unresolved blocker with a named, untried remedy:** "**Check the portal before any retry**" (progress.md:1017) — never performed; see DRAFT-p3-progress-3.
- **Possibly met by other-repo work?** Possibly — flag any repository that measures order-book-ML AUC on a *different* futures instrument or a new feature class. Not met inside this repository.

### H3 — Passive spread capture
- **Status:** Closed with a tail. `[HYP]` "**Closed — cost-bound, with a measured tail still open (see H6)** · 2026-08-03" (HYPOTHESES.md:81).
- **Closure kind:** cost-bound.
- **Closure date:** 2026-08-03 (Stage C.9, progress.md:1188).
- **Deciding figure (n):** spread − adverse − cost = HL BTC **−3.05**, HL ETH **−2.75**, CME MBT **−4.25** bps; best spread-to-cost ratio among liquid contracts **0.98** (M6A). **n = 28 surveyed instruments** over 53.13 quoted hours (Hyperliquid) and one CME day (2026-07-15, bbo-1s, 16 micro contracts).
- **file:line:** progress.md:1231-1233 (nets), progress.md:1211-1217 (CME ratios), progress.md:1200-1205 (HL hours), progress.md:1551-1552 (register summary).
- **Residue never closed:** 3 contracts "too inactive to call a market" reported as an open question (SIL ratio 3,889 on 69 quote updates/day; MHG 65.0 on 1,494) — progress.md:1218-1221; 2 contracts a "failed measurement" from an unresolved continuous symbol (2YY 10 records, 5YY 1 record) — progress.md:1222-1224; 4 micro-yield contracts with no ratio computed — progress.md:1225-1226. None is mentioned again anywhere in progress.md or HYPOTHESES.md.
- **Blockers:** Hyperliquid was subscribed to 2 of 177 perps at the time (progress.md:1200-1201) — lifted the same stage by extending to 12 coins at zero cost (progress.md:1206-1210). Symbology resolution for 2YY/5YY — a known, free fix (progress.md:650-652, 928-929) — never applied.
- **Registered reopen conditions:** the thin tail was routed to H6 (progress.md:1240-1243). `[HYP]` HYPOTHESES.md:205: "A **negative bounded D.1 closes the thin tail (and H3) completely**".
- **Possibly met by other-repo work?** Yes for the CME thin tail — flag any repository holding CME micro-contract quote data (SIL, MHG, 2YY, 5YY, 10Y, 30Y) or an instrument-level spread-to-cost survey.

### H4 — Cointegration pairs trading
- **Status:** Closed. `[HYP]` "**Closed — signal-absent** · 2026-08-04" (HYPOTHESES.md:97).
- **Closure kind:** signal-absent.
- **Closure date:** 2026-08-04 (Stage C.10, progress.md:1359).
- **Deciding figure (n):** **0 of 180** BH-surviving formation pairs still significant out of sample (175 re-testable, 18 = 10.3% significant uncorrected vs a 5.9% base rate); holdout 91 raw hits vs 77.0 expected; BTC/ETH p = 0.1169; deflated Sharpe **0.026** against an expected max per-bar Sharpe of 0.1058 over **n = 1,653 trials**; zero executable pairs. Sample: 60 symbols, 1,826 daily bars, 2021-08-01 → 2026-07-31.
- **file:line:** progress.md:1322-1344 (all figures), progress.md:1290-1296 (universe/n), research/experiments.jsonl:5-9.
- **Blockers:** Kraken OHLC hard-capped at 720 candles (~2 years) and Kraken/Coinbase list only live products, so neither can select a survivorship-free universe (progress.md:1297-1301) — worked around with the Binance monthly archive at zero cost.
- **Registered reopen conditions:** none stated in progress.md. `[HYP]` HYPOTHESES.md H4 block.
- **Possibly met by other-repo work?** Possibly — flag any repository with a survivorship-free crypto universe or a cointegration result on an executable pair set.

### H5 — Funding-rate carry
- **Status:** Closed. `[HYP]` "**Closed as currently unattractive — decayed, not disproved** · 2026-08-04" (HYPOTHESES.md:113).
- **Closure kind:** decayed / currently-unattractive (a fourth kind, not in the C.12 two-kind taxonomy).
- **Closure date:** 2026-08-04 (Stage C.11, progress.md:1447).
- **Deciding figure (n):** net on deployed capital ETH **8.07%**, BTC **8.00%** historically; 5 of 10 instruments clear a 4% risk-free rate by 1.6–4.1 points; but Binance BTC funding by year 30.61% (2021) → 11.92% (2024) → 5.13% (2025) → **1.94% (2026)**; decay slopes −6.31%/yr (BTC), −7.67%/yr (ETH). Sample: 27,761 hourly BTC funding rows, 2023-05-12 → 2026-08-04 (**n = 1,181 days** HL; Binance USD-M back to 2020-01).
- **file:line:** progress.md:1510-1514 (returns), progress.md:1482-1487 (decay), progress.md:1522-1527 (verdict), progress.md:1461-1466 (sample).
- **Confound recorded in the same entry:** "The carry is a bull-market phenomenon. Correlation of daily funding with the trailing 30-day trend is **0.57 / 0.50 / 0.54**" (progress.md:1489-1494) — so the 2026 level is regime-dependent, which the closure does not separate from structural decay.
- **Blockers:** none material — nothing purchased. Unmodellable risks stated: protocol failure, venue insolvency, oracle manipulation, solo-operator failure, regulatory loss of Hyperliquid access (progress.md:1519-1521).
- **Registered reopen conditions:** none in progress.md beyond "decayed, not disproved"; `[HYP]` HYPOTHESES.md H5 block.
- **Possibly met by other-repo work?** Yes — flag any repository measuring 2026 perp funding levels or a bull/bear split of funding yield.

### H6 — Spread capture on thin perpetuals
- **Status:** Closed. `[HYP]` "**Closed at D.1d — 2026-08-12; closure re-confirmed under audit correction the same day.**" (HYPOTHESES.md:196). Trajectory: registered 2026-08-06 (C.18) → positive 2026-08-11 (C.27) → D.1-feasible 2026-08-11 (D.1a) → survives four kills 2026-08-12 (D.1c) → **closed negative 2026-08-12 (D.1d)**.
- **Closure kind:** measured-negative under an order-lifecycle fill model.
- **Closure date:** 2026-08-12 (progress.md:2599); audit corrections the same day (progress.md:2705-2760).
- **Deciding figure (n):** always-last queue + 162 ms bidirectional latency + ALO rejection + 2.5×Q cap → **PUMP −4.75 bps (−$7,321), MERL −4.23 bps (−$467)** per filled notional; corrected by audit finding A4 to **PUMP −4.81, MERL −4.35**; negative at every cap and at every latency on the 0–800 ms grid. **n = 28.7M records, one census week (2026-08-04 → 08-11), 2 instruments**; PerformanceReports carry 32,018 / 4,270 / 14,085 leg records (MERL falls to 2,536 after A4).
- **file:line:** progress.md:2663-2670 (result), progress.md:2683-2688 (latency grid), progress.md:2716-2721 (A4 correction), progress.md:2529-2537 (C.27 census survivors PUMP +4.30, MERL +6.45, GMX +0.40), progress.md:2741-2746 (A3/A6/A8 interval correction; GMX flips to unresolved).
- **Blockers:** "no per-order stream (no arrivals/cancels/order IDs; `orderUpdates` is auth'd own-orders only)" (progress.md:2549-2553); consumption prediction fails at "median error 100%" because "87–99% of levels clear by cancellation" (progress.md:2558-2561); Hyperliquid latency unmeasured, proxy floor only (progress.md:2563-2565, 2619-2626); hftbacktest unsuitable (progress.md:2565-2567).
- **Registered reopen conditions:** "**Reopens only on order-level book data** (arrivals/cancels/order IDs) or venue fill-level ground truth — not on lower latency, not on a better queue model from this feed, not on more weeks of per-fill accounting." (progress.md:2701-2703). **Note:** no availability audit was performed for order-level Hyperliquid data, unlike the C.15/C.19 pattern the project applies elsewhere.
- **Standing conditions registered and then abandoned:** ≥4 weeks across regimes, accruing at zero cost by ~2026-09-08 (progress.md:2571-2573, 2610); the blind four-week window with earliest close 2026-09-09, registered in commit 4bde24c and implemented at research/microstructure/blind_universe.py (progress.md:2627-2635). Recording stopped 2026-08-13 with **1 of 28 days captured** (progress.md:2762, 2782-2784). See DRAFT-p3-progress-4.
- **Also registered and unused:** the C.18 outcome-to-action map, including "survivors within noise of zero | **extend recording 30 days and re-run under these same bars** — no building" (progress.md:2115-2122).
- **Possibly met by other-repo work?** **Yes — flag for the cross-repo pass.** Any repository holding order-level (message-by-message, order-ID-bearing) book data for a perp or spot venue, or venue-side fill ground truth, meets H6's stated reopening condition.

### H7 — Cross-venue divergence
- **Status:** **Closed by decision, not by evidence.** `[HYP]` "**Closed by decision — the C.17 end condition, not evidence** · 2026-08-06" (HYPOTHESES.md:216).
- **Closure kind:** by decision (the C.17 end condition).
- **Closure date:** 2026-08-06 (progress.md:2059-2060: "**H7 closed by decision**, design preserved").
- **Deciding figure (n):** **none — never measured.** At C.12 it was "in flight, awaiting data only, neither needing new access or capital … needs months of simultaneous three-venue overlap; recorders together only since 2026-08-01" (progress.md:1556-1559). The nearest measurement is C.14 Task 3 on two venues: max ΔAUC +0.0044 / +0.0037, max Δcapture +0.04 bps, six days (progress.md:1787-1792).
- **file:line:** progress.md:1556-1559 (in flight), progress.md:2059-2060 (closed by decision), progress.md:2638 ("H7 by decision" used to justify retiring Kraken/Coinbase).
- **Blockers:** three-venue simultaneous overlap began 2026-08-01; the requirement was "months" (progress.md:1558-1559). Kraken and Coinbase were retired 2026-08-12 and all recording stopped 2026-08-13 (progress.md:2636-2643, 2762), so the overlap ended at 12 days.
- **Registered reopen conditions:** none in progress.md; the design is preserved (progress.md:2060).
- **Possibly met by other-repo work?** Yes — flag any repository with simultaneous multi-venue book capture over months.

### H8 — Cross-sectional funding carry
- **Status:** Closed. `[HYP]` "**Closed — signal present, cancelled by its own hedge** · 2026-08-05" (HYPOTHESES.md:130).
- **Closure kind:** signal present but cancelled (a distinct kind).
- **Closure date:** 2026-08-05 (Stage C.13, progress.md:1682).
- **Deciding figure (n):** funding **+43.68%**, price **−42.91%**, cost −0.66%, **net +0.11%** on deployed capital vs a 4% risk-free rate; max drawdown **−75.85%**; price daily vol 1.81% vs funding 0.166% (10.9×). **n = 232 perps considered / 231 usable / 4,411,046 funding rows / 1,182 days**, cross-section 21 → 190 instruments.
- **file:line:** progress.md:1709-1712 (three terms), progress.md:1718-1722 (drawdown), progress.md:1687-1691 (universe/n), progress.md:1713-1717 (vol ratio).
- **Blockers:** "the venue launched after the 2022 drawdown, so **no bear market is inside this history**" (progress.md:1731-1733). Cost margin is thin: break-even 1.76 bps/side against 1.5 modelled at 51.7× turnover — a 17% margin (progress.md:1723-1727).
- **Registered reopen conditions:** none in progress.md.
- **Possibly met by other-repo work?** Yes — flag any repository whose crypto sample spans a full bear regime (H8's named absent regime).

### H9 — Time-series momentum on daily bars
- **Status:** Closed. `[HYP]` "**Closed — insignificant after deflation, and untradeable where it appears** · 2026-08-06" (HYPOTHESES.md:146).
- **Closure kind:** FAIL against pre-registered bars (registration commit 88b69d8, progress.md:1819-1877).
- **Closure date:** 2026-08-06 (Stage C.16, progress.md:1879).
- **Deciding figure (n):** primary L90/H30 net Sharpe 0.302 vs BTC 0.183, **DSR 0.446**, alpha t **1.01**; consistency **7/12** positive, median 0.167; best cell L30/H7 net Sharpe 0.647 → **DSR 0.732** after **n = 12 registered trials**; executable subset 27 of 58 → primary Sharpe **0.013**. Sample: 60-member universe, 48 live at the end, 2021-08 → 2026-07.
- **file:line:** progress.md:1893-1899 (grid + DSR), progress.md:1900-1905 (beta control + executable subset), progress.md:1883-1889 (universe).
- **Blockers:** none — "nothing bought" (progress.md:1913). "Kraken adds nothing (BTC/ETH spot, no shorts)" (progress.md:1904-1905).
- **Registered reopen conditions:** "H9 reopens only on ≥ half the grid clearing DSR ≥ 0.95 vs BTC **on the executable subset** with a full bear regime in sample — never on fees." (progress.md:1908-1910).
- **Possibly met by other-repo work?** Yes — flag any repository whose sample contains a full crypto bear regime *and* an executable short universe; both halves of H9's condition would then be testable.

### H10 — Liquidation aftermath reversion
- **Status:** Closed. `[HYP]` "**Closed — unidentifiable in available data** · 2026-08-06" (HYPOTHESES.md:163).
- **Closure kind:** unidentifiable-in-available-data — a third kind introduced here (progress.md:1939-1943).
- **Closure date:** 2026-08-06 (Stage C.15, progress.md:1915).
- **Deciding figure (n):** **zero identifiable liquidation events** in **n = 2,639,510 recorded fills** across 116 hour files, 2026-08-01 → 08-06, 12 instruments. Four supporting facts: one key-set `(coin, hash, px, side, sz, tid, time, users)` with no liquidation field; zero `liquidat` strings in any channel; all-zeros hash at 18.0% of fills ground-truthed to TWAP fills; three plausible info-endpoint types → HTTP 422.
- **file:line:** progress.md:1921-1931 (all four facts), progress.md:1932-1934 (sample size stated first).
- **Blockers:** "no public global history: three plausible info-endpoint types → HTTP 422, and the venue's per-user `liquidation` label requires already knowing the liquidated address — the enumeration query the public API does not offer." (progress.md:1928-1931). **This blocker is challenged** — the `users` field enumerates counterparty addresses in the recorded stream (measured: 6,652 distinct addresses in one hour file), and `userFillsByTime` was used in the same stage; see DRAFT-p3-progress-5.
- **Registered reopen conditions:** "≥ **300 labeled liquidations**, size/instrument/time-of-day matching, mid moves at 1/10/60/300 s, 95% CI, economics vs spread-at-event + 3 bps." (progress.md:1936-1939).
- **Possibly met by other-repo work?** **Yes — flag for the cross-repo pass.** Any repository holding labeled liquidation events (a venue liquidation feed, a per-user fill label, or a dataset of ≥300 identified liquidations on any perp venue) meets H10's threshold directly.

### H11 — Medium-horizon prediction on untested feature classes
- **Status:** Closed. `[HYP]` "**Closed — FAIL on all six pre-registered bars; the closure that ended the alpha search by decision** · 2026-08-06" (HYPOTHESES.md:180).
- **Closure kind:** FAIL against six pre-registered bars, with a binding end condition agreed in advance (progress.md:1953-1955).
- **Closure date:** 2026-08-06 (Stage C.17, progress.md:2030).
- **Deciding figure (n):** **0 of 40 registered cells pass all six bars**; best DSR **0.499** vs 0.95; best alpha t **1.35** vs 2; class consistency A 0.0 / B 0.875 / C 0.75 / D 1.0 / E 0.875. **n = 40 cells, n_trials = 40**, weekly 2020-08-02 → 2026-07-26 (207 scored weeks for classes A/B/C; 45–59 for D/E).
- **file:line:** progress.md:2046-2056 (grid result), research/experiments.jsonl:19 (`verdict`, `grid`, `lags_applied_days`).
- **Blockers:** Coin Metrics community snapshot "ends 2026-05-23: a measured 75-day staleness" (progress.md:2038-2039); CryptoQuant free tier 401; Blockchain.com has no flow series; "No exchange publishes flows free" (progress.md:2040-2043). Applied lag recorded in code: `LAG_DAYS = {"A": 1, "B": 75, "C": 0, "D": 0}` (research/medium/features.py:38). **The +75-day lag contradicts this stage's own pre-registration of "+1 day" for the same source (progress.md:1987-1989); see DRAFT-p3-progress-1.**
- **Registered reopen conditions:** "data-threshold reopening (free flow source ≤2d lag ≥3y history, or basis at DSR ≥0.95 / t ≥2 over ≥156 weeks incl. a bear)" (progress.md:2058-2061). `[HYP]` fuller text at HYPOTHESES.md:185.
- **Possibly met by other-repo work?** **Yes — flag for the cross-repo pass.** Condition (a) is met by any repository holding a free exchange-flow series at ≤2-day lag with ≥3 years of history; condition (b) by any repository with ≥156 weeks of perp-basis data including a bear regime.

---

## Part 3 — Detection-track entries (D1, D2)

### D1 — Hard-rug detection / honest-clearance scorer
- **Status:** **Shipped.** `[HYP]` "**Works — shipped as a clearance scorer** · 2026-08-07 (C.23/C.24)" (HYPOTHESES.md:238).
- **Closure kind:** shipped (positive), scope-documented.
- **Closure date:** 2026-08-07 (Stage C.24, progress.md:2383).
- **Deciding figure (n):** honest-clearance precision **0.984 at recall 0.538** on the 2024 test fold (train ≤ 2023); complementary hard-rug alarm only **0.464** precision. **n = 194** on the C.23 fold; C.24 sweep 360 designed → 281 T0-reached (78.1%).
- **file:line:** progress.md:2400-2403 (deliverable + direction correction), progress.md:2353-2357 (v0 0.984), progress.md:2377-2380 (sweep n).
- **Blockers:** `MLCE_HELIUS_API_KEY` absent at C.21 (progress.md:2291-2295) — **lifted 2026-08-07** (progress.md:2317). Self-imposed credit cap 30,000 → 60,000, never raised again (progress.md:2298-2300, 2338-2339, 2414-2415). Credit weights `{rpc:1, enhanced:10}` "marked UNVERIFIED" (progress.md:2299) and never reconciled; ledger verified UNANCHORED at 24,025 requests → 58,801 weighted (`data/vendor/helius_credit_ledger.jsonl`, read 2026-09-05T05:55Z).
- **Registered reopen conditions:** none — this entry shipped rather than closed.
- **Possibly met by other-repo work?** No.

### D2 — Honest-versus-slow-rug separation
- **Status:** Concluded. `[HYP]` "**Concluded (C.26) — real but small and unconfirmed.**" (HYPOTHESES.md:252).
- **Closure kind:** absent at T0 (C.23) + qualified positive post-launch, unconfirmed, with a pre-registered end condition fired on a measured-unaffordable price (C.26).
- **Closure date:** 2026-08-07 (Stage C.26, progress.md:2450).
- **Deciding figures (n):**
  - Launch window (C.23): decontaminated honest precision **0.574 @ recall ≥ 0.5** against a 0.60 bar at a 0.50 base rate, **n = 194** test fold — labelled "absent signal" (progress.md:2353-2356, 2370-2372). *Recomputed 95% Wilson CI [0.465, 0.672]; the bar is inside the interval — see DRAFT-p3-progress-6.*
  - Post-launch (C.24): precision **0.654 @ recall 0.53 vs 0.557 base**, lift +0.097, ~1.8 SE (progress.md:2385-2394).
  - Depth-unbiased (C.25): 6h v0 lift **+0.047**; mid-stratum **+0.051**, ~0.8 SE, n = +120 honest / 96 reached (progress.md:2426-2436).
  - Firming (C.26): mid-stratum **+0.032, SE 0.039, 95% CI [−0.045, +0.109]**, n = 328 honest / 447 total (progress.md:2463-2469).
- **file:line:** as above; registered bar at progress.md:2254-2257.
- **Blockers:** the decon-unbiased confirmation priced at "≈ **124,764 weighted** … **~1.9× the entire 60,000 cap**" → "**Measured-unaffordable**" (progress.md:2458-2462) — denominated in the UNVERIFIED credit unit, see DRAFT-p3-progress-7. Creator restructure "fails on identification, not cost … **0 resolved a creator**" on n = 8 pools (progress.md:2452-2457). SolRPDS has no creator field (progress.md:2367-2369). SolRPDS covers only the post-graduation stratum; bonding-curve instant deaths are outside it (progress.md:2266-2268).
- **Registered reopen conditions:** "D2 reopens only on an affordable decon label or a live cohort — not new access or a better model." (progress.md:2473-2474).
- **Possibly met by other-repo work?** Unlikely, but flag any repository holding Solana pool/transaction indexer data or a labeled soft/slow-rug dataset.

---

## Part 4 — Stage-level blockers recorded in progress.md (whether or not they gate a hypothesis)

| blocker | stated at | status at the anchor |
|---|---|---|
| Rust toolchain / webkit2gtk-4.1 / gtk+-3.0 / dbus-1 dev packages absent; install needs sudo | progress.md:44-49, 138-143 | **never lifted**; desktop Rust half never compiled |
| `DATABENTO_API_KEY` absent — adapter validated against synthetic records only | progress.md:384-387 | **lifted** 2026-08-02 (progress.md:640-651) |
| Databento exposes no account-balance / usage endpoint; spend tracked from per-request quotes only | progress.md:620-626, 983-990 | **never lifted**; the ledger records intent, not billing |
| Databento vendor cap $25 | progress.md:666-670 | raised to $120 on 2026-08-02 (progress.md:961-963) |
| June 2026 MBT month charged $35.5144 and never delivered (OOM in `fetch_range`); "Check the portal before any retry" | progress.md:995-1018 | **never reconciled**; ledger holds the charge with no reversal (UNANCHORED read 2026-09-05T05:55Z) |
| `data/databento/session.py` has no CME holiday calendar — every exchange holiday fails coverage | progress.md:1067-1071 | **never fixed** |
| Roll exclusion centred on the splice removes 0 s of the expiry-day dead book | progress.md:1044-1060 | superseded by the C.8 observed-silence exclusion (progress.md:1153-1162) |
| CME's own fee finder is interactive; the exchange fee component rests on a broker's republication | progress.md:1142-1145 | **never independently verified** |
| Kraken base-tier fee wrong (0.25/0.40 → 0.40/0.80 → 0.25/0.40) | progress.md:333-341; progress.md:2494-2496 | corrected 2026-08-08; every Kraken figure published 2026-08-01 → 08-08 carries the 2× cost |
| No account API in Stage 1, so the operator's real Kraken tier cannot be read | progress.md:2019-2024 | recorded as an operator action; reconciled at C.27 |
| Hyperliquid `xv_leadlag_m100/p100` unmeasurable (100 ms bins vs a 123 ms median interval) | progress.md:456-462 | resolved by moving them to `SUB_100MS_FEATURES` |
| 22.6 s host stall 2026-08-03T19:51:25Z, all three venues, no logged gap, cause unknown | progress.md:1323-1335 (C.9.1) | "Recorded for a future stage" — **never revisited** |
| `MLCE_HELIUS_API_KEY` absent; the registered bar "not attempted — distinct from not cleared" | progress.md:2291-2295 | **lifted** 2026-08-07 (progress.md:2317) |
| Helius credit weights `{rpc:1, enhanced:10}` UNVERIFIED; no keyless usage endpoint | progress.md:2298-2300 | **never verified**, including after the key landed |
| pump.fun API HTTP 530; Bitquery/Dune/Birdeye 401; Helius free-key-required; MELT "availability unverified" | progress.md:2208-2212 | recorded, not designed around |
| RugCheck `rugged` flag disqualified as ground truth on 0 of 4 documented rugs (registration asked ~10) | progress.md:2164-2166, 2204-2206 | **never re-tested** |
| No per-order Hyperliquid stream (`orderUpdates` is auth'd own-orders only) | progress.md:2549-2553 | **never lifted**; becomes H6's reopening condition |
| Hyperliquid latency unmeasured; probe is a "proxy floor" (POST /info, not the signed /exchange path); usable 2026-08-19 | progress.md:2563-2565, 2619-2626 | **never accrued** — recording stopped 2026-08-13 |
| hftbacktest/numba absent and unsuitable for the venue's touch shape | progress.md:2565-2567 | replaced by a custom bounded replay (D.1d) |
| Leakage suites reach none of the census / D.1c / D.1d modules; `spread.py` / `adverse.py` have no direct test; H1, H2, H4, H5, H8–H11 read but not run by the external audit | progress.md:2756-2760 | **stated and unresolved at the anchor** |

---

## Part 5 — Registered conditions that are triggers, in one list (for the cross-repo pass)

| # | condition, as registered | file:line | met inside this repository? | candidate for another repository? |
|---|---|---|---|---|
| 1 | H1: "reopens only below ~3 bps round trip" | progress.md:1676-1677 | **arguably yes** — Hyperliquid base tier is exactly 3.0 bps round trip (research/microstructure/fees.py) with 13 recorded days (progress.md:2789-2793), and the pipeline was never run on it | yes — any measured sub-3 bps or rebate venue |
| 2 | H2: "reopens only on measurable AUC on a *different* instrument or feature class" | progress.md:1677-1679 | no | yes |
| 3 | H3 tail: closed by "a negative bounded D.1" `[HYP]` HYPOTHESES.md:205 | progress.md:1240-1243 | yes for the Hyperliquid tail; **no** for the CME residue (SIL/MHG/2YY/5YY, progress.md:1218-1226) | yes — CME micro-contract quote data |
| 4 | H6: "Reopens only on order-level book data (arrivals/cancels/order IDs) or venue fill-level ground truth" | progress.md:2701-2703 | no; and no availability audit was performed for it | yes |
| 5 | H6 standing: bounded measure re-run on "≥ 4 weeks across regimes … by ~2026-09-08" | progress.md:2571-2573 | **no — abandoned**, recording stopped 2026-08-13 with 1 of 28 days | no |
| 6 | H6/D.1b: blind four-week window, earliest close 2026-09-09, rule registered in 4bde24c | progress.md:2627-2635; research/microstructure/blind_universe.py | **no — abandoned after 1 day** | no |
| 7 | C.18 outcome map: "survivors within noise of zero → extend recording 30 days and re-run under these same bars" | progress.md:2115-2122 | not invoked; GMX became "unresolved" under the audit (progress.md:2741-2746) without triggering it | no |
| 8 | H9: "≥ half the grid clearing DSR ≥ 0.95 vs BTC on the executable subset with a full bear regime in sample" | progress.md:1908-1910 | no | yes — a repository with a bear-regime crypto sample |
| 9 | H10: "≥ 300 labeled liquidations, size/instrument/time-of-day matching, mid moves at 1/10/60/300 s, 95% CI" | progress.md:1936-1939 | **possibly** — the `users` enumeration and `userFillsByTime` path was never priced (DRAFT-p3-progress-5) | yes — any labeled liquidation dataset |
| 10 | H11: "free flow source ≤2d lag ≥3y history, **or** basis at DSR ≥0.95 / t ≥2 over ≥156 weeks incl. a bear" | progress.md:2058-2061 | branch (a) is exactly the source the stage used, at a lag it derived from one snapshot rather than measuring (DRAFT-p3-progress-1) | yes |
| 11 | D2: "reopens only on an affordable decon label or a live cohort" | progress.md:2473-2474 | affordability rests on an UNVERIFIED credit unit (DRAFT-p3-progress-7) | unlikely |
| 12 | Phase B: "stays open until it has run over enough days to cover multiple volatility regimes" | progress.md:10-13 | **no — never met**, and the phase's dependency (continuous recording) was terminated | no |
| 13 | Phase A: "passes only when a full day of Kraken data and a full day of Coinbase data both reconstruct with zero unexplained crossed-book events and full-day coverage outside logged reconnect gaps" | progress.md:19-22 | **yes, met 2026-08-01** (progress.md:210-224) — box left unticked by explicit operator-call convention | no |
