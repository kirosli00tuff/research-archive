# Agent A — MLCryptoEngine, part p3-progress (draft findings)

Repository: **MLCryptoEngine** @ anchored SHA `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22).
Assigned primary documents: `progress.md` (2,977 lines, read in full), `research/` (93 files incl.
`research/experiments.jsonl`), `backtest/`. `report.md`, `HYPOTHESES.md`, `DECISIONS.md` and
`AUDIT.md` belong to other readers; where I quote them it is corroboration and is flagged as such.

Direction A throughout: I am arguing that closures were reached on weaker grounds than their labels
imply. Everything below is quoted verbatim from the snapshot with file:line, or recomputed from
stored primitives with the inputs named.

---

### DRAFT-p3-progress-1
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H11 — medium-horizon prediction on untested feature classes (Stage C.17), the stage whose FAIL terminated the project's alpha search by decision. Specifically feature class B, exchange netflows.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Coin Metrics community: genuine\n  `FlowInEx*/FlowOutEx*/SplyEx*` exist free for BTC/ETH to genesis — class B\n  survives — **but the snapshot ends 2026-05-23: a measured 75-day staleness**,\n  and the registered measured-beats-documented rule sent it into the grid at\n  **+75 days**." — MLCryptoEngine/progress.md:2036-2040
- **Evidence:**
  - The pre-registration for the same stage, written before any data was touched, registers a *different* lag for this exact source: "Registered lags: **unknown-lag daily sources +1 day beyond\nthe metric date** (the conservative default); Coin Metrics community **+1 day**; DefiLlama stablecoin supplies **+1 day**" — MLCryptoEngine/progress.md:1987-1989.
  - The applied lag is not a narrative claim; it is a constant in the shipped code: `LAG_DAYS = {"A": 1, "B": 75, "C": 0, "D": 0}` — MLCryptoEngine/research/medium/features.py:38, with the rationale in the module docstring: "the Coin\nMetrics community snapshot retrieved 2026-08-06 ends 2026-05-23, so CM-derived\nfeatures carry a measured **75-day** lag rather than the +1 default" — MLCryptoEngine/research/medium/features.py:6-9.
  - It is also recorded in the stage's own stored artifact: `"lags_applied_days": {"A": 1, "B": 75, "C": 0, "D": 0}` — MLCryptoEngine/research/experiments.jsonl:19 (run_id `f68a8075-d75b-4ca5-bac0-03a87fef34ea`, `git_sha` 370ba414…, logged 2026-08-06T18:23:31Z).
  - The 75 days is derived from **one** snapshot's last row date. The source URL in the code is a git-hosted CSV: `CM_URL = "https://raw.githubusercontent.com/coinmetrics/data/master/csv/{asset}.csv"` — MLCryptoEngine/research/medium/data.py:37. A single retrieval cannot distinguish "this source refreshes daily and was 75 days behind on 2026-08-06" from "this source refreshes every 75 days"; the repository records no measurement of the source's refresh cadence, and it is a git repository whose per-row first-publication dates are recoverable free from commit history — a measurement this project performs routinely elsewhere.
  - The lag is then applied **uniformly to every weekly decision from 2020-08-02 to 2026-07-26** (`WEEK_END_MS = 1_753_574_400_000  # 2026-07-26` — MLCryptoEngine/research/medium/__main__.py:31), i.e. as if a 2021 decision could only see 2021 netflow data 75 days old. That is a claim about historical availability that a 2026 snapshot's end date does not establish.
  - Even at +75 days, class B did not behave like a dead class: `"class_consistency_positive_fraction": {"A": 0.0, "B": 0.875, "C": 0.75, "D": 1.0, "E": 0.875}` — MLCryptoEngine/research/experiments.jsonl:19. B posted positive net Sharpe in **7 of its 8 cells** and satisfied registered bar 6 outright.
  - Corroboration in another reader's document (cited, not relied on as primary): the per-cell table gives B/h1w/LO net +28.4%/yr, Sharpe 0.657 and B/h1w/LS net +22.6%/yr, Sharpe 0.426 with **beta 0.04 and alpha +21.0%/yr** — MLCryptoEngine/report.md:2712-2719 region (cell rows `B/h1w/LO` … `B/h8w/LS`).
  - The stage's failure is binding on the whole project: "**The end condition, agreed in advance and binding: if this stage fails its\nregistered bars, the alpha search of this project ends by decision.**" — MLCryptoEngine/progress.md:1953-1955; executed at MLCryptoEngine/progress.md:2030-2033.
  - ADR-042 ("publication lag: measured beats documented") — the rule invoked to override the registered lag — is itself listed as an output *of this same stage*: "ADR-042 (publication lag: measured beats documented; living snapshots dated)" — MLCryptoEngine/progress.md:2063. A rule created inside the stage overrode a lag registered before the stage, in the direction that made the class fail.
- **Recomputation (if any):** No re-fit is possible without the source data, and I claim none. The arithmetic that matters is the deviation itself: registered lag 1 day (progress.md:1988) vs applied lag 75 days (features.py:38, experiments.jsonl:19) = **75× the registered value**, applied to a grid whose shortest horizon is 1 week (7 days), i.e. the feature is 10.7 horizons stale at every decision in the h1w cells. n = 207 scored weeks for every class-B cell (report.md cell table, `weeks` column).
- **What would resolve it:** Re-score the eight class-B cells at the registered +1-day lag (and, separately, at a lag measured from the Coin Metrics repository's own commit history per row date rather than from one snapshot's end date). Publish both columns. If B still fails bars 2 and 3 at +1 day, the C.17 FAIL — and the end-of-search decision that rests on it — stands on the grounds it claims.
- **Confidence:** HIGH — the registered lag, the applied lag and the stage's binding consequence are all three stated in the repository's own text and code, and the deviation is not disclosed as a deviation anywhere in progress.md.
- **Invalidated by later commits?:** no — the anchor (2026-08-22) is the project's final research state; progress.md's last entries (E.1, E.2) are write-up and a test fix, and no later stage revisits C.17's lags.
- **Disclosed by authors?:** Partially, and in a way that makes it worse. progress.md:2038-2040 and features.py:6-11 disclose the *75-day figure* and defend it as "measured beats documented", but neither says that the pre-registration of the same stage had registered +1 day for this source, and neither treats the change as a deviation from a pre-registration the project otherwise polices to the character (cf. progress.md:1747-1750, where a mis-specified bar is fixed "to match the registered text, not the reverse").

---

### DRAFT-p3-progress-2
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H1 — short-horizon directional prediction, closed "cost-bound" with a reopening condition of a sub-~3 bps round trip.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "H1\nclosed on **cost** and reopens only below ~3 bps round trip." — MLCryptoEngine/progress.md:1676-1677
- **Evidence:**
  - The project records, verifies and *uses* a venue at exactly that number, at base tier with no volume requirement: "**Fees:** hyperliquid base tier 1.5/4.5 bps maker/taker (verified\n    2026-08-01…)" — MLCryptoEngine/progress.md:394-395; and in code, `HYPERLIQUID_MAKER_BPS = 1.5` … `HYPERLIQUID_MAKER_ROUND_TRIP_BPS = 2.0 * HYPERLIQUID_MAKER_BPS` — MLCryptoEngine/research/microstructure/fees.py (module constants; docstring records base tier "< $5M 14-day volume, no staking discount").
  - The project explicitly established, in writing, that this venue can carry the H1 label set, and said why it mattered: "Net: Hyperliquid can test 500 ms -> 900 s, losing only\n    the shortest horizon — and it is the venue whose 1.5/4.5 bps fees make\n    the cost side of this comparison worth running at all." — MLCryptoEngine/progress.md:541-543.
  - The venue then recorded BTC and ETH continuously for **13 days** (2026-08-01 → 2026-08-13, 2.2 GB) — MLCryptoEngine/progress.md:2789-2793 (final archive table).
  - **The directional pipeline was never run on it.** `research/experiments.jsonl` is the append-only experiment log and contains 19 runs, the last logged 2026-08-06T18:23:31Z. The only run whose `results` keys include `hyperliquid BTC` / `hyperliquid ETH` is run 2 (2026-08-02T01:05:18Z), and both entries read `{"error": "no valid samples"}` — MLCryptoEngine/research/experiments.jsonl:2. Consistent with progress.md:501 ("hyperliquid skipped — no data for 2026-07-31") and progress.md:544 ("No Hyperliquid results computed: only partial days exist"). No later run in the log has a hyperliquid series.
  - Instead the transfer test went to a **more expensive** venue that had to be bought: CME MBT at "**5.33 bps**" round trip — MLCryptoEngine/progress.md:1128-1129 — at a ledger cost of $82.1179 (verified below).
  - The closure kind's own definition names this trigger: "**cost-bound** — a real signal smaller than the cost of capturing it, which\n    reopens at a materially lower fee tier" — MLCryptoEngine/progress.md:1543-1545.
  - The project's own 2026-08-22 write-up carries both halves of the arithmetic and never multiplies them: "Against Kraken's own\n  50 bps round trip that is a miss of roughly **1,700×**; against the cheapest\n  reachable venue at 3 bps, roughly **100×**" (that is the 100 ms figure, 0.0291 bps) and, four bullets later, "3.31 bps at 900 s came from one day; across four\n  full days the same measurement ranges **−2.44 to +3.05 bps**" — MLCryptoEngine/progress.md:2824-2835. The 3-bps venue is applied only to the 100 ms capture, never to the 900 s capture.
  - Corroboration (another reader's document): H1's registered reopening cell enumerates only unreachable spot tiers — "On Coinbase that is the 0 bps maker tier requiring **$250M trailing 30-day volume**; on Kraken, the 0 bps maker tier at **$10M**. Neither is reachable at this project's capital." — MLCryptoEngine/HYPOTHESES.md:53. Hyperliquid's base tier, which the project measured at 3.0 bps round trip and recorded 13 days of, does not appear in that cell.
- **Recomputation (if any):** Inputs: gross capture at 900 s = 3.31 bps (progress.md:1128, Coinbase BTC-USD) and its four-full-day range −2.4378 to +3.0497 bps (progress.md:1781-1783); round-trip cost = 3.0 bps (fees.py, `2.0 * 1.5`). Method: net EV = capture − round trip. Result: **+0.31 bps** at the headline figure, **+0.05 bps** at the best full day, **−5.44 bps** at the worst full day. At Coinbase's 80 bps the sign is negative on every day by 76–82 bps; at 3.0 bps the sign is *undetermined across the four days on which the project itself says the measurement lives*. The closure's deciding arithmetic ("arithmetic fails by 23×", progress.md:1550) is a statement about an 80 bps venue only.
- **What would resolve it:** Run the existing Phase B/C.14 pipeline unchanged on the recorded Hyperliquid BTC and ETH bbo+trades days (2026-08-01 → 2026-08-12 overlap with the Kraken/Coinbase window), at horizons 500 ms – 900 s per progress.md:541-543, and report gross capture against the 3.0 bps round trip with the same per-day stability table C.14 Task 2 registered. This costs no money, no new access and no new code — the capability matrix, the bbo plumbing and the label horizons were all built for it in Stages C.1–C.2.
- **Confidence:** HIGH — every input (the reopen threshold, the venue's fee, the venue's measurability, the recorded days, and the absence of any hyperliquid directional run in the append-only log) is in the repository, and the arithmetic is subtraction.
- **Invalidated by later commits?:** no — the anchor is the project's terminal state and recording was stopped on 2026-08-13 (progress.md:2762-2764), so no later commit runs this test.
- **Disclosed by authors?:** no. The repository discloses the *venue's* cost (progress.md:394, 2825) and the *plan* to use it (progress.md:541-543), but nowhere states that the H1 pipeline was not run on the venue that meets its own reopening threshold, nor gives a reason for not running it. The nearest thing to a reason is progress.md:2638 ("H1 cost-bound") being used as a justification for retiring the *other* two venues, which assumes the conclusion.

---

### DRAFT-p3-progress-3
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H2 — transfer of the Phase B edge to CME micro futures; and the Stage C.7 backfill that supplied its sample.
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Whether June was actually billed is not determinable from the client** —\n  `metadata` exposes `get_cost` and `get_billable_size` (pre-request\n  estimates) and no usage endpoint. The stream ran ~19 minutes before the\n  kill. If the Databento portal shows June was *not* billed, reversing that\n  ledger entry restores $74.17 and the full four months fit with $16.69 to\n  spare, no cap change. **Check the portal before any retry** — the gate\n  cannot detect a double-spend it already recorded." — MLCryptoEngine/progress.md:1012-1018
- **Evidence:**
  - The charge is real and still stands. Live-repo untracked ledger `data/vendor/spend_ledger.jsonl`, read 2026-09-05T05:55Z (UNANCHORED — this file is gitignored working-tree data and may have changed after the anchor): 29 entries, total **$82.1179**, last write `2026-08-04T05:37:07Z`. The June entry is `{"date":"2026-06-01..2026-07-01","usd":35.514444664121,"billable_bytes":76266689184,"note":"C.7 four-month MBT backfill"}`. **There is no negative/reversing entry anywhere in the file** (checked: `[r for r in rows if r['usd']<0]` → `[]`).
  - The charge bought nothing: "| 2026-06 | $36.1880 | **$35.5144** | **no** | — |" (quoted / charged / delivered / on disk) — MLCryptoEngine/progress.md:986.
  - The document states plainly that the ledger is intent, not a vendor-confirmed charge: "Quoted and charged agree to the cent **because they are the same number**… This is not an independent reconciliation and must not be read as one. The only true actual is the Databento invoice." — MLCryptoEngine/progress.md:983-990.
  - The consequence is the sample H2 closed on: "**The four-month range no longer fits.** Ledger: **$81.3416 spent,\n  $38.6584 remaining** of the $120 cap. Finishing needs $57.4835" — MLCryptoEngine/progress.md:1007-1009 — and the halved range is carried straight into the H2 evidence: "**Range conditions (Task 4): two months, one regime**" — MLCryptoEngine/progress.md:1100; "There is a visible step down inside May… This is April–May 2026 only — it is **not**\n  regime-diverse" — MLCryptoEngine/progress.md:1104-1108; and "**Walk-forward: one clean fold, not three (ADR-024).** 42/14-day windows over\n  a 61-day span yield 2 folds, the second truncated 5 days past the data" — MLCryptoEngine/progress.md:1150-1152.
  - The named remedy was never taken. `grep -n "portal" progress.md` returns exactly two hits, both inside the C.7 entry (progress.md:1015, 1017). Twenty subsequent stages (C.8 → E.2, 2026-08-03 → 2026-08-22) contain no reconciliation, no invoice check and no ledger reversal, and the ledger's own last write is 2026-08-04.
- **Recomputation (if any):** Inputs: ledger total $82.1179 (data/vendor/spend_ledger.jsonl, read 2026-09-05T05:55Z), June entry $35.5144 (same file), cap $120.00 (progress.md:960-962), July quote $21.2955 (progress.md:975). Method: recompute headroom with the undelivered June charge reversed. Result: $82.1179 − $35.5144 = **$46.6035 spent**, **$73.3965 remaining**, against the $57.4835 needed to finish June + July — the four-month range fits with **$15.91 to spare**, no cap change. (The document's own $74.17/$16.69 figures differ by the $0.7763 CME survey spent after C.7 was written; the conclusion is the same.)
- **What would resolve it:** One free look at the vendor's invoice or usage page for 2026-08-03, deciding whether $35.5144 was billed for a stream that was OOM-killed at 19 minutes and delivered nothing. If it was not billed, H2's "two months, one regime, one clean fold" limitation was self-inflicted by an unreconciled ledger entry and the June + July months were affordable throughout.
- **Confidence:** HIGH — the charge, its non-delivery, the absence of any reversal, and the fact that the halved range is the stated limitation of H2 are all directly observable; the only thing I cannot see is the vendor invoice, which is precisely the check the document says to make.
- **Invalidated by later commits?:** no — the ledger's last write predates the anchor by 18 days and no later commit touches it. (The ledger read is UNANCHORED working-tree data; if it changed after 2026-09-05T05:55Z my reading of "no reversal" could go stale, but no tracked commit after the anchor exists.)
- **Disclosed by authors?:** Partially — progress.md:1012-1018 discloses the uncertainty and names the check, which is why this is a PROCESS finding at S2 rather than a claim that the figure is wrong. What is *not* disclosed is that the check was never performed, and H2's "two months of one contract" limitation is stated (HYPOTHESES.md:64, another reader's document) without noting that the third and fourth months were blocked by an unverified ledger entry rather than by cost.

---

### DRAFT-p3-progress-4
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 — thin-perp spread capture, closed by Stage D.1d; and the pre-registered blind four-week universe window (D.1b, commit 4bde24c) that was abandoned one day after it opened.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "- **The blind universe window**, earliest close 2026-09-09, existed to test\n  whether the C.27 survivors were a selection artefact. Any survivor of a blind\n  selection meets the same order-lifecycle fill model that closed PUMP and MERL.\n\nRecording further data would not change an answer." — MLCryptoEngine/progress.md:2778-2782
- **Evidence:**
  - The blind window was pre-registered, built, tested and subscribed one day earlier: "**⏱ Blind four-week scoring window earliest close: 2026-09-09**… Universe rule registered blind in 4bde24c BEFORE retrieval — 24h-notional bands, seeded sample, seed 20260812, structurally blind to every spread/impact/price field (decoy-perturbation test). Applied: 25 blind picks of 177 live perps… 27 subscribed, all confirmed flowing." — MLCryptoEngine/progress.md:2627-2635. The module exists at the anchor: `SEED = 20260812`, `BANDS` B0–B4, `extract_assets` reducing the payload to `name`/`isDelisted`/`dayNtlVlm` only — MLCryptoEngine/research/microstructure/blind_universe.py:1-55, with `tests/test_blind_universe.py` in the suite.
  - **The same document said the opposite one day earlier, in the D.1d entry itself**: "The blind window closing 2026-09-09 still reads out as a\n    selection-bias check, since any future survivor faces this same gate." — MLCryptoEngine/progress.md:2699-2700. Between that sentence (2026-08-12) and its reversal (2026-08-13) the only intervening work is the adversarial audit, which *strengthened* the case for re-selection: "**A3/A6/A8** — census intervals assume independence and are 2–17× too\n    narrow… **GMX flips** (+0.288 → −0.070 day-clustered) and is now recorded as unresolved rather than a survivor." — MLCryptoEngine/progress.md:2735-2740.
  - The generalisation is from **n = 2 instruments**. D.1d's numbers are PUMP and MERL only: "**PUMP −4.75 bps (−$7,321),\n    MERL −4.23 bps (−$467)**" — MLCryptoEngine/progress.md:2663-2664 (later corrected to −4.81 / −4.35 at progress.md:2716-2719).
  - The project's own D.1c measurements show the fill model's outcome is **instrument-specific**, not a venue property: PUMP's collapse is driven by tick geometry — "PUMP: tick 3.5–4.6\n    bps, spread at **one tick 85.5% of the quoted week** (99.2% ≤2) — price\n    improvement impossible, always-last is modal" — MLCryptoEngine/progress.md:2585-2588 — while "MERL: tick 0.56 bps\n    under ~7-tick spread — range [+5.42, +6.45] stands" — MLCryptoEngine/progress.md:2589-2590. Two instruments with opposite tick geometry are not a sample of 177.
  - This is the exact reasoning error the project itself identified and corrected at Stage C.9: "After C.8 a claim was made and not\n  verified: spread capture is dead everywhere because fees exceed the spread.\n  It was checked on **two instruments**… and generalised — from two of the *tightest* instruments\n  available, which is the worst possible basis." — MLCryptoEngine/progress.md:1194-1198.
  - The selection-bias debt was explicitly still outstanding: "Survivors demote to **screened positives**: BH corrected the 10\n    tested, not the 177 screened. Unbiased re-selection (pre-registered volume-band rule blind to spread fields) folds into the ≥4-week re-run (~2026-09-08)." — MLCryptoEngine/progress.md:2608-2610.
  - And the standing caveat that the window was accruing at zero cost: "rests on the single census week; a D.1 conclusion on more\n  than one week needs the bounded measure re-run on ≥ 4 weeks across regimes\n  (recorders accrue at zero cost by ~2026-09-08)." — MLCryptoEngine/progress.md:2571-2573.
  - Recording was stopped **27 days before** the registered window could close: "**Recording stopped 2026-08-13T05:02:49Z.**" — MLCryptoEngine/progress.md:2762; leaving "the 27-instrument blind\nuniverse subscribed on 2026-08-12… with 1 day of capture" — MLCryptoEngine/progress.md:2782-2784. Disk was not the constraint: "270 GB free" against "~301 MB/day" post-retirement — MLCryptoEngine/progress.md:2644-2646.
- **Recomputation (if any):** Arithmetic of the abandonment only. Registered window 2026-08-12 → 2026-09-09 (progress.md:2627); recording stopped 2026-08-13 (progress.md:2762) = **1 of 28 days captured, 96.4% of the registered window forgone**. Population: 25 blind picks + 2 carried over, drawn from 177 live perps (progress.md:2631-2633); the closing argument generalises a result measured on 2 of those 177 (**1.1%**) to all of them.
- **What would resolve it:** Nothing now — the data was never recorded, and this is the one finding in this file that cannot be closed by re-analysis of what exists. What *would* have resolved it is 27 more days of a recorder already running at ~301 MB/day against 270 GB free. Failing that, H6's closure should carry the blind-window abandonment in its limitations, and the "reopens only on order-level book data" condition should be restated as "reopens on a blind-selected instrument set as well", since that is the check the project registered and then dropped.
- **Confidence:** MEDIUM-HIGH — the facts (registration, one day of capture, the one-day-earlier opposite statement, the n=2 basis) are all quoted; what is a judgement is whether the fill-model result generalises, and I am asserting only that the project's own C.9 correction says a two-instrument generalisation is not evidence.
- **Invalidated by later commits?:** no — the anchor is the terminal commit and recording is stopped; no later commit can supply the window.
- **Disclosed by authors?:** Partially. progress.md:2694-2697 restates the caveats (one census week, one regime, PUMP a screened positive, MERL inside a 10-of-177 correction) and progress.md:2782-2784 warns the 1-day capture "should not be treated as" a scoreable window. What is not disclosed is that the abandonment argument rests on generalising an n=2 result, nor that the same document endorsed the window's value on the preceding day.

---

### DRAFT-p3-progress-5
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H10 — liquidation aftermath reversion, closed at Task 1 as "unidentifiable-in-available-data" (Stage C.15).
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "(4)\n  no public global history: three plausible info-endpoint types → HTTP 422, and\n  the venue's per-user `liquidation` label requires already knowing the\n  liquidated address — the enumeration query the public API does not offer." — MLCryptoEngine/progress.md:1928-1931
- **Evidence:**
  - Fact (1) of the same four-fact list states that every recorded fill names both counterparties: "every fill shares ONE key-set —\n  `(coin, hash, px, side, sz, tid, time, users)`" — MLCryptoEngine/progress.md:1923-1924. The `users` array **is** an address enumeration, supplied by the recorded stream rather than by an API query.
  - Fact (3) of the same list shows the per-user endpoint was successfully used in this very stage to attach labels to recorded fills: "the\n  one anomalous value, all-zeros hash at **18.0%** of fills, ground-truths via\n  `userFillsByTime` to **TWAP fills** (`twapId`, `dir='Close Short'`, no\n  `liquidation` key)" — MLCryptoEngine/progress.md:1925-1928. The stage therefore already did address → `userFillsByTime` → per-fill label, which is exactly the operation it declares impossible for liquidations.
  - **Verified against the recorded data** (live repo, untracked/gitignored, read-only, UTC read time 2026-09-05T05:55Z — UNANCHORED): one hour file, `data/raw/venue=hyperliquid/date=2026-08-05/hour=12/messages.ndjson.zst`, contains **45,108 trade fills** carrying **6,652 distinct `users` addresses**; the key-set is exactly `('coin','hash','px','side','sz','tid','time','users')`, matching progress.md:1924. Example fill: `{"coin":"ETH","side":"A","px":"1868.0","sz":"1.6393","time":1785931200016,"hash":"0x000…000","tid":296140610341295,"users":["0xf9109ada…","0xe5d844a6…"]}`.
  - The all-zeros-hash class — the natural candidate pool for protocol-initiated (non-user-signed) fills — is large and was dismissed by prevalence rather than by sampling it for liquidations: "prevalence alone had already ruled out liquidations" — MLCryptoEngine/progress.md:1928. Measured in the same hour file: **7,958 of 45,108 fills = 17.64%** zero-hash, reproducing the document's 18.0%. The document does not state how many of that class were sampled through `userFillsByTime`, only that it "ground-truths … to TWAP fills".
  - The bar the closure has to clear is small: "≥ **300 labeled liquidations**" — MLCryptoEngine/progress.md:1936-1937 — against a swept population of "**2,639,510 trade fills, 116 hour files, 2026-08-01 → 08-06, 12\n  instruments**" — MLCryptoEngine/progress.md:1921-1922.
  - The project's own standing rule for declaring a source unusable is to *price* the path, not to assert it (Stage C.26 fires its end condition on a measured credit price, progress.md:2458-2462; Stage C.19 measures rate limits "as observed, not as published", progress.md:2192-2193). No cost or feasibility measurement of a `users` → `userFillsByTime` liquidation sweep appears anywhere in progress.md.
- **Recomputation (if any):** Direct measurement rather than re-derivation. Inputs: one hour of recorded Hyperliquid trades (path and read time above). Method: parse each NDJSON line's `raw` field as JSON, keep `channel == "trades"`, count fills, distinct `users` entries, and all-zero hashes. Result: 45,108 fills / 6,652 distinct addresses / 7,958 (17.64%) zero-hash in one hour. Extrapolating the distinct-address count over the swept week is not sound (addresses repeat), so I claim only what is measured: the enumeration the closure says does not exist is present in the recorded data at ~6.6k distinct addresses per hour.
- **What would resolve it:** Measure the cost of the path the closure dismissed: take the zero-hash fills in the recorded week, query `userFillsByTime` for their `users` addresses around each fill timestamp, and count how many carry the venue's `liquidation` key. Report the observed request cost and the labeled count against the registered floor of 300. If the sweep is unaffordable, say so with the measured number (the C.26 pattern) instead of asserting that the enumeration does not exist.
- **Confidence:** HIGH on the factual contradiction (the `users` field is present and the per-user endpoint was used in the same stage); MEDIUM on whether the sweep is affordable, which is exactly the quantity nobody measured.
- **Invalidated by later commits?:** no — C.15 is never revisited in progress.md, and the recorded week that would answer it is preserved (progress.md:2789-2793).
- **Disclosed by authors?:** no. The `users` field is disclosed (progress.md:1924) and `userFillsByTime` is disclosed (progress.md:1926), but the document does not reconcile them with its own claim at progress.md:1930-1931 that address enumeration is unavailable, and states the opposite conclusion — "nothing reachable can measure it" (progress.md:1941).

---

### DRAFT-p3-progress-6
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D2 / Stage C.23 — the honest-vs-slow-rug boundary on pre-event on-chain state, declared "absent signal".
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Limiting factor, named:** not threshold, not sample, not unbuilt features —\n  **absent signal at the honest/soft-slow boundary.**" — MLCryptoEngine/progress.md:2370-2371
- **Evidence:**
  - The deciding number and its n: "on a proper 2024 test fold (n=194), the honest\n  bar is reachable as machinery, not cleared as signal. Decontaminated honest\n  precision **0.574 @ recall≥0.5** at a 50% base rate — +0.07 above chance." — MLCryptoEngine/progress.md:2353-2356.
  - The registered bar it is judged against: "**honest-candidate precision ≥ 0.60 at recall\n≥ 0.50**" — MLCryptoEngine/progress.md:2255-2256.
  - The gap is 0.026 in precision, against a base rate 0.074 below the estimate. No confidence interval is reported for this figure anywhere in the C.23 entry, although the project computes intervals as a matter of course elsewhere (e.g. C.26 reports "SE 0.039, 95% CI\n  [−0.045, +0.109]" for a lift of comparable size — MLCryptoEngine/progress.md:2465-2467).
  - The control the entry offers for "signal, not sample" is a *different* label version on the same fold — "same fold, same n, same train — v0\n  separates at 0.98, decon sits at base rate with a flat PR curve" (MLCryptoEngine/progress.md:2358-2360) — which establishes that the fold can separate an easy class, not that it has the power to resolve 0.574 from 0.60.
- **Recomputation (if any):** Inputs, all from MLCryptoEngine/progress.md:2353-2356: test fold n = 194, base rate 0.50 → 97 honest; precision 0.574 at recall ≥ 0.50. Method: recover the implied confusion counts (TP = 97 × recall, predicted positives = TP / 0.574), then Wilson 95% interval on the precision proportion and a one-sided z-test against the 0.50 base rate; then a two-proportion power calculation for the sample needed to resolve 0.60 from 0.50 at 80% power, α = 0.05 one-sided. Script and output: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-mlcrypto-p3/recompute.txt`.
  - recall 0.50 → TP 48, predicted positives 84 → precision 95% Wilson CI **[0.465, 0.672]**; the 0.60 bar is **inside** the interval. z vs base 0.50 = **1.36**, one-sided p = 0.087.
  - recall 0.55 → 92 predicted positives → CI [0.474, 0.672], z = 1.42, p = 0.078. recall 0.60 → 101 → CI [0.477, 0.666], z = 1.49, p = 0.068. The bar sits inside the interval on every reading.
  - Power: resolving a true precision of 0.60 from a 0.50 base at 80% power needs **≥ 153 predicted positives**; the fold supplied about **84**. The test was underpowered for its own bar by roughly **1.8×**.
  - So the correct label for this measurement is "underpowered / inconclusive at the registered bar", not "absent signal": the data are equally consistent with precision 0.60 (the PASS threshold) and with 0.50 (chance).
- **What would resolve it:** Report the interval on 0.574 beside the 0.60 bar, and either re-score on a fold with ≥ ~150 predicted positives at recall ≥ 0.5, or restate D2's launch-state branch as underpowered rather than signal-absent. The distinction matters because the project's own taxonomy treats "signal-absent" as a closure that "**does not reopen on a\n    better model, a better feature set, or lower fees**" (MLCryptoEngine/progress.md:1546-1548), i.e. the harsher label removes the cheapest reopening route.
- **Confidence:** HIGH on the arithmetic (the inputs are stated and the recomputation is elementary); MEDIUM on the exact predicted-positive count, which I reconstruct from precision and recall rather than read directly — I report the interval across recall 0.50–0.60 so the conclusion does not depend on that reconstruction.
- **Invalidated by later commits?:** no — C.24/C.25/C.26 extend the *post-launch* behavioural branch and never re-score the C.23 launch-state fold; D2 is concluded at progress.md:2470-2474 carrying C.23's "absent" reading forward ("the **C.23\n  boundary** (honest-vs-slow-rug absent at T0)").
- **Disclosed by authors?:** no for this figure. The project discloses intervals elsewhere and, for the C.26 lift, states honestly that the CI "still includes zero" (progress.md:2466-2467). For C.23's 0.574 no interval is given, and the entry asserts positively that sample size is *not* the limiting factor.

---

### DRAFT-p3-progress-7
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D2 / Stage C.26 — the decontaminated-unbiased test declared "measured-unaffordable", firing the detection track's pre-registered end condition.
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The decon-unbiased test, priced:** pool-path ≈ **124,764 weighted** (53\n  thriving honest pools at ~2,000 each dominate; one active pool ~7,970 for its\n  30-day detail alone) — **~1.9× the entire 60,000 cap**, a raise to ~180,000,\n  far beyond the registered 65,000 threshold. **Measured-unaffordable** → the\n  pre-registered **end condition fires**." — MLCryptoEngine/progress.md:2458-2462
- **Evidence:**
  - The unit in which that verdict is denominated is explicitly unverified, and was so from the first credit ever counted: "Credit gate with cap 30,000 (dated, weights {rpc:1,\n  enhanced:10} marked UNVERIFIED, method = request-count derivation since no\n  keyless usage endpoint)" — MLCryptoEngine/progress.md:2298-2300.
  - The key arrived the next day — "Key landed; probe 67 req (670 weighted)" — MLCryptoEngine/progress.md:2317 — and was used through C.22–C.26 (2026-08-07). No reconciliation of the derived weights against the vendor's own usage record appears anywhere in progress.md after the key landed; the only "actual" figures quoted ("Sweep estimate 12,600 checked before fetch; **actual 9,865**", progress.md:2339-2340) are produced by the same request-count derivation, so they check the estimator against itself.
  - **The weight is where most of the number comes from.** Live-repo untracked ledger `data/vendor/helius_credit_ledger.jsonl`, read 2026-09-05T05:55Z (UNANCHORED): 24,025 entries, `enhanced` 3,864 requests and `rpc` 20,161 requests, weighted total **58,801**. The ×10 multiplier alone contributes 3,864 × 9 = 34,776, i.e. **59.1%** of every credit the project believes it consumed.
  - The cap is self-imposed, not the vendor's: "**Cap 30k→60k, dated, AFTER method proof** (C.7 pattern); self-imposed, not\n  the Helius limit." — MLCryptoEngine/progress.md:2338-2339. Dollar spend on this track is zero throughout ("**Buy-nothing held: zero spent, zero keys created**", progress.md:2228-2229; "0 estimated, 0 spent, 0 sent", progress.md:2293-2294).
- **Recomputation (if any):** Inputs: ledger request mix (3,864 enhanced / 20,161 rpc, weighted 58,801) from `data/vendor/helius_credit_ledger.jsonl` read 2026-09-05T05:55Z; terminal estimate 124,764 weighted and cap 60,000 from MLCryptoEngine/progress.md:2458-2461. Method: rescale the terminal estimate to an enhanced weight of 1 using the ledger's observed request mix. Result: 124,764 × (24,025 / 58,801) ≈ **50,976 weighted — below the 60,000 cap**, i.e. the "measured-unaffordable" verdict reverses. Because the priced work is dominated by *enhanced* 30-day detail calls, its mix is more enhanced-heavy than the historical ledger, so 50,976 is an upper bound: at 100% enhanced the same estimate would reprice to ≈12,476. Result stands: the terminal verdict of an entire research track is not robust to the value of a constant the repository itself labels UNVERIFIED, and the sensitivity was never tested.
- **What would resolve it:** Reconcile the derived weights against Helius's own usage record for the account (the key was held from 2026-08-07), or state the verdict as a request count (which is directly observed: 24,025 requests consumed, and the priced test's request count) rather than in an unverified synthetic unit. Then re-decide the end condition on the reconciled number.
- **Confidence:** MEDIUM-HIGH — the UNVERIFIED label, the absence of any reconciliation, and the ledger's 59.1% multiplier share are all directly evidenced; the rescaling is a sensitivity analysis under an explicitly stated assumption, not a claim that the true weight is 1.
- **Invalidated by later commits?:** no — the ledger's last entry is 2026-08-07 and the detection track is concluded at progress.md:2470-2474; no later commit reconciles it.
- **Disclosed by authors?:** Partially. The UNVERIFIED weighting is disclosed once, at progress.md:2299, in the stage that created the gate. It is not restated when the same unit is used to fire a terminal end condition five stages later, and no sensitivity to it is reported. This is the project's own "measured beats documented" rule (ADR-042) unapplied to its own budget instrument.

---

### DRAFT-p3-progress-8
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** Stage C.19 — the rug-detection availability audit; the disqualification of RugCheck's `rugged` flag as a label source.
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "RugCheck keyless at ~0.85 s/report, zero 429s in a burst — but\n  its `rugged` flag recovered **0 of 4 documented rugs** and is disqualified\n  as ground truth." — MLCryptoEngine/progress.md:2204-2206
- **Evidence:**
  - The stage's own pre-registration asked for roughly 10 cases, not 4: "A heuristic label set… must be spot-checked against ~10\npublicly documented Solana rug pulls with well-attested on-chain histories" — MLCryptoEngine/progress.md:2164-2166.
  - Four is also the count the project's own heuristic was scored on, with three of the four coming back indeterminate: "**Known-answer spot-check: hit 1 (LIBRA…), indeterminate 3 (HAWK, kid-QUANT, M3M3 …), missed 0.**" — MLCryptoEngine/progress.md:2213-2216. The same four cases therefore support "hit 1 of 4" for the in-house heuristic and "disqualified" for RugCheck.
  - The consequence is not cosmetic: the disqualification removes the only keyless third-party label source, and the label track proceeds on SolRPDS end-of-life aggregates alone — "labels are end-of-life aggregates — label\n    side only" (progress.md:2200-2201), "RugCheck `rugged` discarded per C.19" (progress.md:2277-2278).
- **Recomputation (if any):** Inputs: 0 detections out of 4 documented rugs (MLCryptoEngine/progress.md:2205). Method: Clopper–Pearson exact 95% interval on the binomial proportion, plus the one-sided 95% upper bound 1 − 0.05^(1/4). Result: 95% CI on the flag's true recall = **[0.000, 0.602]**; one-sided 95% upper bound = **0.527**. A flag whose true recall is anywhere up to ~53% is not excluded by 0/4. For comparison, the registered n of 10 would have given, on the same 0 hits, a CI of [0.000, 0.308]. Script/output: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-mlcrypto-p3/recompute.txt`.
- **What would resolve it:** Run the registered ~10-case spot-check (RugCheck is keyless, ~0.85 s per report, and the stage measured zero rate-limit rejections — so the additional six cases cost seconds), and report the interval beside the count. If 0/10 holds, the disqualification is supported at [0, 0.31] and the claim is safe.
- **Confidence:** HIGH on the arithmetic and on the registered-vs-executed n; MEDIUM on materiality, since SolRPDS did clear the 5,000-token GO floor by 15× without RugCheck (progress.md:2198-2199), so the disqualification did not block the stage — it narrowed the label options for the C.23 boundary that later failed.
- **Invalidated by later commits?:** no — C.19's inventory is never re-run.
- **Disclosed by authors?:** Partially — the count "0 of 4" is stated plainly, and the stage discloses that vague cases were "dropped, not forced" (progress.md:2216-2217). What is not disclosed is that 4 falls short of the registered ~10, nor what 0/4 does and does not exclude.

---

### DRAFT-p3-progress-9
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H1 — the Stage C.14 Task 2 sample-stability test that withdrew H1's headline number.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**The ETH pair was not run**: the full four-symbol stride-1 sweep is ~5 hours\n  of LightGBM fits." — MLCryptoEngine/progress.md:1756-1757
- **Evidence:**
  - The registered scope of Task 2 was per-venue and per-day across everything validated: "Per-day, per-venue, per-horizon AUC across every validated day." — MLCryptoEngine/progress.md:1625. The registration also forbids a pooled figure standing alone: "A pooled number\n  that hides a range is not permitted to stand alone." — MLCryptoEngine/progress.md:1633-1634.
  - The pairs dropped include **the highest gross capture the project ever measured**: "Read the gap from the\n    floor as the gross edge the model actually captures: **~3.9 bps at 900 s\n    on kraken ETH/USD, ~3.3 bps on coinbase BTC-USD**" — MLCryptoEngine/progress.md:509-512. The 3.3 bps pair (Coinbase BTC-USD) was re-run and its headline withdrawn; the 3.9 bps pair (Kraken ETH/USD) was not re-run at all.
  - The withdrawal that closes H1 harder therefore rests on one symbol on one venue: "**Coinbase 900 s gross capture ranges\n    −2.4378 to +3.0497 bps.** Phase B's **3.31 bps at 900 s was 2026-07-31**,\n    the +3.05 day. **The number that defined H1 is a single-day draw from a\n    distribution centred near zero**" — MLCryptoEngine/progress.md:1781-1785.
  - The ETH pairs were in scope for the original Phase B run and did produce results — `research/experiments.jsonl:2` (run logged 2026-08-02T01:05:18Z) carries `kraken ETH/USD` and `coinbase ETH-USD` result blocks alongside the BTC pairs — so the omission is a C.14 scope decision, not a data gap.
- **Recomputation (if any):** Arithmetic of the omission only. The stability test that decides whether H1's headline is an artefact covers 2 of the 4 symbol-venue series the project had validated (50%), and excludes the series with the largest measured gross capture (3.9 bps vs 3.3 bps, progress.md:511). Against the round trip the project itself calls "the cheapest reachable venue at 3 bps" (progress.md:2825-2826), 3.9 bps is **+0.9 bps net** and 3.3 bps is **+0.3 bps net** — so the excluded series is the one whose stability most directly bears on whether H1's cost-bound closure survives at a 3 bps venue (see DRAFT-p3-progress-2).
- **What would resolve it:** Run C.14 Task 2 on Kraken ETH/USD and Coinbase ETH-USD over the same six validated days at the same stride, and publish the per-day 900 s capture range beside the BTC series. The stated obstacle is "~5 hours of LightGBM fits" on a machine that was otherwise idle for the stage's duration.
- **Confidence:** MEDIUM — the omission and the excluded series' higher capture are both quoted, but the pooled Phase B ETH figure is a single-day number too, so the ETH stability range is genuinely unknown rather than known to be favourable. I claim only that it was not measured.
- **Invalidated by later commits?:** no — no later stage re-runs C.14, and progress.md:2812-2818 (the 2026-08-22 write-up) restates the six-day BTC-only scope as final.
- **Disclosed by authors?:** yes — MLCryptoEngine/progress.md:1755-1757 and again at progress.md:1811-1814 ("six days is not six regimes; the ETH pair was\n  not run"). This finding is therefore READ and capped at S3; the authors named the gap. What they did not name is that the omitted pair carried the study's largest gross capture.

---

### DRAFT-p3-progress-10
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H11 / Stage C.17 — the one-line summary of class B (exchange netflows) and class C in progress.md.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "B and C: the pre-named beta artifact — LO beta 0.43–0.56,\n  alpha t ≤ 0.95, LS collapses." — MLCryptoEngine/progress.md:2050-2051
- **Evidence:**
  - The long-short (LS) cells for class B do not collapse. From the stage's own per-cell table (corroboration in another reader's document, MLCryptoEngine/report.md, section "Stage C.17", rows `B/h1w/LS` and `B/h2w/LS`): B/h1w/LS net **+22.6%/yr**, net Sharpe **0.426**, **beta 0.04**, alpha **+21.0%/yr**, alpha t **0.95**; B/h2w/LS net +15.1%/yr, Sharpe 0.248, beta 0.00, alpha +15.0%/yr, t 0.66 — over **207** and **205** scored weeks respectively.
  - "LS collapses" is the registered artifact pattern for a long-only effect that is really beta ("an effect in **only one variant**", MLCryptoEngine/progress.md:2026). Class B's LS variant retains a **higher** alpha (+21.0 vs +7.9%/yr) and a **higher** alpha t (0.95 vs 0.63) than its LO variant, at beta 0.04 — the opposite of the pattern being asserted. What class B's LS cells show is a beta-neutral positive that is not statistically significant, which is a different and weaker closure than "beta artifact".
  - The same class is the one carried at a 75-day lag (see DRAFT-p3-progress-1), so the diagnosis and the handicap compound.
- **Recomputation (if any):** Consistency check only, on figures read from the stage's own table. Class B LS Sharpe by horizon: 0.426 (h1w) · 0.248 (h2w) · −0.229 (h4w) · 0.011 (h8w). "Collapses" describes h4w/h8w; it does not describe h1w/h2w, whose alphas are the largest beta-neutral alphas in the entire 40-cell grid outside class D's 45–59-week bull-compression window. Implied t on B/h1w/LS from its Sharpe over 207 weeks: 0.426 × √(207/52) = **0.85**, consistent with the reported alpha t of 0.95 and far from the bar of 2 — so the *conclusion* (FAIL) is unaffected; the *characterisation* is not supported.
- **What would resolve it:** Restate class B's summary line as "LO is beta-carried; LS is beta-neutral and positive but far from significant (alpha t ≤ 0.95 over 207 weeks)", and note it as the class whose lag was the binding handicap. That is the sentence a future reader needs before deciding whether H11's data-threshold reopening (a "free flow source ≤2d lag ≥3y history") is worth chasing.
- **Confidence:** MEDIUM-HIGH — the claim challenged is in my document; the contradicting per-cell figures are in report.md, another reader's primary document, so this should be de-duplicated against their pass.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — the LS cells' beta and alpha are published in the table but the summary line asserts the opposite behaviour, and the register's H11 entry (HYPOTHESES.md:185, another reader's document) carries the "measured 75-day staleness is the binding data constraint on class B" framing without the LS numbers.

---

### DRAFT-p3-progress-11
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H3 — spread capture, closed on "all 28 measurable instruments"; the five CME contracts left unresolved by Stage C.9.
- **Direction:** A
- **Class:** UNDER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Two contracts are a failed measurement, not data.** 2YY and 5YY returned 10\n  and 1 usable records with mids of 1.4e9 and 4.6e9 — an unresolved continuous\n  symbol. Recorded as failed rather than reported as thin." — MLCryptoEngine/progress.md:1222-1224
- **Evidence:**
  - Three more were left explicitly open in the same stage: "**Three contracts are too inactive to call a market.** SIL shows a ratio of\n  3,889 on **69 quote updates in a day**; MHG 65.0 on 1,494… Reported as an open question, not as an opportunity and not as a dismissal." — MLCryptoEngine/progress.md:1218-1221.
  - Neither the failed measurement nor the open question is ever revisited. `grep -n "SIL\|MHG\|2YY\|5YY" progress.md` returns hits only at lines 1218, 1219, 1222 and 1225 — all inside the C.9 entry. The same grep over `HYPOTHESES.md` (another reader's document) returns nothing.
  - The fix for the failed measurement was already in hand and free. Symbology resolution for continuous symbols was solved two stages earlier — "the supported pair is\n    **`continuous → instrument_id`**" (MLCryptoEngine/progress.md:650-652) — and it costs nothing against the budget: "Resolution\n    costs nothing, so it never touches the spend gate." (MLCryptoEngine/progress.md:928-929). The two bbo-1s day files that failed cost **$0.0000134** and **$0.0000013** (live-repo `data/vendor/spend_ledger.jsonl`, entries for `2YY.c.0` and `5YY.c.0`, read 2026-09-05T05:55Z, UNANCHORED), against "$37.8821 remaining" of the cap at the time (MLCryptoEngine/progress.md:1244-1245).
  - H3's thin tail was subsequently answered only on the *Hyperliquid* perp tail (H6 → D.1d). The CME thin tail was never brought back, and the closing statement for the family (HYPOTHESES.md:205, another reader's document) reads "A **negative bounded D.1 closes the thin tail (and H3) completely**" — i.e. a result on two Hyperliquid perps closes a family whose CME members were left as an explicit open question.
- **Recomputation (if any):** Count only. Stage C.9 surveyed 16 CME micro contracts plus 12 Hyperliquid perps = 28 quoted, of which **10 CME contracts are reported with a ratio**, **3 are declared too inactive to call** (SIL, MHG and one more, progress.md:1218-1221), **2 are a failed measurement** (2YY, 5YY, progress.md:1222-1224) and 4 micro-yield contracts have "no ratio … computed for them" (progress.md:1225-1226). The closure label "all 28 measurable instruments" (progress.md:1551-1552) is therefore true by construction of the word "measurable", and the residue — 5 contracts, one of them a fixable symbology error costing cents — was never closed.
- **What would resolve it:** Re-resolve 2YY.c.0 and 5YY.c.0 through the working `continuous → instrument_id` path and re-price their bbo-1s day (cost: cents, budget: $37.88 remaining). For SIL/MHG, either record the open question in HYPOTHESES.md so it survives the register's closure, or state the dismissal on the grounds actually used (69 quote updates per day cannot support a fill), which the C.9 entry declines to do.
- **Confidence:** MEDIUM — the residue and its non-revisitation are directly evidenced; the materiality is limited because a 69-update-per-day book plainly cannot be traded, which is the reason C.9 gives and then declines to call a dismissal.
- **Invalidated by later commits?:** no — no later stage mentions these contracts.
- **Disclosed by authors?:** Partially — C.9 discloses both the failed measurement and the open question, in careful language. The failure is that the register's H3 closure does not carry either forward, so a reader of HYPOTHESES.md alone sees "all 28 measurable instruments" with no residue.

---

### DRAFT-p3-progress-12
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** Phase B's stated open condition, and the project-complete declaration.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "- [ ] Phase B — feature and label library, gradient boosted tree baseline, purged\n      cross-validation (pipeline built and validated 2026-08-01; the research\n      conclusion stays open until it has run over enough days to cover multiple\n      volatility regimes — that depends on continuous recording, not more code)" — MLCryptoEngine/progress.md:10-13
- **Evidence:**
  - The condition was never met, by the project's own statement: "**What this did NOT establish:** six days is not six regimes" — MLCryptoEngine/progress.md:1811-1812; and the standing caveat is repeated for CME: "This is April–May 2026 only — it is **not**\n  regime-diverse" — MLCryptoEngine/progress.md:1106-1108.
  - Phase B's dependency — continuous recording — was terminated 14 days after Phase B ran: "**Recording stopped 2026-08-13T05:02:49Z.**" — MLCryptoEngine/progress.md:2762; "Recording further data would not change an answer." — MLCryptoEngine/progress.md:2782.
  - Yet the Phase B hypotheses were closed on that sample (H1 2026-08-03, H2 2026-08-03) and the project was declared complete: "## 2026-08-13 — Recording ends: the archive is closed and the project is complete" — MLCryptoEngine/progress.md:2762 (section heading at MLCryptoEngine/progress.md:2762); "Every register entry is closed." — MLCryptoEngine/progress.md:2772.
  - The document's own header is still stale at the anchor, nine days after the project was declared complete: "Current phase: **Phase A — data pipeline** (implementation complete; the phase\ncheckbox stays unchecked until full recorded days clear `make validate`)" — MLCryptoEngine/progress.md:3-4 — while Phase A's stated criteria have been met since 2026-08-01 ("**Verdict for 2026-07-31 (report.md section \"2026-08-01 06:52 UTC\"): PASS\n    on both venues.**", MLCryptoEngine/progress.md:210-211). All five phase checkboxes remain unticked at MLCryptoEngine/progress.md:8-19.
  - A second, smaller stale figure in the final entry: the same 2026-08-22 write-up quotes Kraken's cost as **50 bps** in one bullet and **80 bps** two bullets later — "Against Kraken's own\n  50 bps round trip" (progress.md:2824-2825) and "the best decile in the study takes **5.00 bps\n  against 80 bps** — missing the economic bar by **16×**" (progress.md:2827-2829) — the 80 bps being the pre-ADR-055 figure withdrawn at MLCryptoEngine/progress.md:2494-2496 ("base tier corrected 0.40/0.80 →\n  **0.25/0.40** (live schedule, retrieved 2026-08-08)… Round-trip maker 80→50 bps").
- **Recomputation (if any):** Inputs: top-decile capture 5.00 bps (progress.md:2827-2828); Kraken round trip 50 bps post-ADR-055 (progress.md:2494-2496). Method: miss factor = round trip / capture. Result: **10×**, not the 16× the same entry states; the 16× is computed against the withdrawn 80 bps figure. The conclusion (the decile does not clear a round trip) is unaffected on either number. Separately: Phase B's stated closing condition is "multiple volatility regimes"; the delivered sample is 6 validated days (progress.md:1753-1755) and 53 CME days over 2 consecutive months (progress.md:1100-1108) — n of regimes claimed by the project itself: **1**.
- **What would resolve it:** Either tick the phase checkboxes with the evidence that satisfies them and update the header, or state explicitly that Phase B's conclusion was closed *without* meeting the multi-regime condition it registered, and record that as a limitation on H1/H2 rather than leaving the condition standing unfulfilled at the top of the file. Restate the decile miss factor at 50 bps (10×) or label the 80 bps as the registered bar rather than the current cost.
- **Confidence:** HIGH — all figures are quoted from the document; the only judgement is whether an unfulfilled registered condition plus a "project is complete" declaration is a finding, and the project's own discipline on pre-registration says it is.
- **Invalidated by later commits?:** no — the anchor is the last commit and the header is stale at it.
- **Disclosed by authors?:** Partially — "six days is not six regimes" (progress.md:1811-1812) is disclosed repeatedly and honestly, and the Kraken correction is disclosed at progress.md:2494-2496. What is not disclosed is the mismatch between the registered Phase B closing condition and the closure that happened, nor is the header ever updated. This is why the finding is READ and S3.

---

## What I checked and found sound

Thesis-driven checks where the closure held up, with references:

- **The C.14 pre-registration mechanics.** The bars were committed before results (progress.md:1579-1598), and when the registered instrument turned out to be mis-specified for the world that occurred, the code was fixed to match the *registered text* rather than the reverse, with the outcome reported as INCONCLUSIVE by the bar as written even though the finding was unambiguous (progress.md:1766-1772). That is the opposite of the failure mode I was hunting.
- **C.14 Task 4 (deep learning).** The bar was stated before training (progress.md:1647-1673), both models lost on both metrics at both horizons (progress.md:1793-1799), and the leakage canary was shown capable of firing at production settings before the null was accepted (progress.md:1801-1805). "Capacity was not the constraint" is supported by its own numbers.
- **C.10 (cointegration).** The universe is survivorship-free by construction and the construction is checked (progress.md:1290-1305); ticker reuse was caught explicitly (LUNAUSDT 177,400× jump, progress.md:1306-1310); the look-ahead bug that produced the *best* number was found and reported rather than shipped (progress.md:1345-1352); the deflated-Sharpe benchmark exceeds the result (progress.md:1338-1344). The closure is stronger than its label.
- **C.13/H8.** The three terms are kept apart, the drawdown (−75.85%) is reported against +0.11%/yr, and the parameter surface is called noise on its own sweep evidence (progress.md:1710-1730). Cost being "nearly binding" at a 17% margin is disclosed rather than buried.
- **C.16/H9.** The grid was registered whole and reported whole; the three cells that beat BTC all sit at the shortest hold, which the registration had named in advance as the artifact pattern (progress.md:1893-1899). Reopening is scoped to the executable subset with a bear regime — a threshold, not a bet.
- **C.18 → C.27 census machinery.** The scored population was genuinely untouched until the window closed, enforced in code rather than by promise (`run_registered_census` raising before `SCORED_END_NS`, research/microstructure/registered.py:47-49, tested); the known-answer gate reproduces C.9's closed BTC/ETH nets to within 0.004 bps (progress.md:2138-2142); the window close was verified by clock (progress.md:2518-2521).
- **The adversarial-audit response (progress.md:2705-2760).** The A4 correction moves both headline numbers *further* from zero and is reported as such; A13 causes an attribution claim to be withdrawn from the shipped `PerformanceReport` and from H6's reopening condition; A3/A6/A8 widen the census intervals and demote GMX from survivor to unresolved. The corrections are present in the anchored code (`_day_clustered_se`, one-sided vs two-sided critical values, research/microstructure/registered.py:146-207; the centralised fee module research/microstructure/fees.py). I looked specifically for a corrected number quietly reverting toward the favourable side and did not find one.
- **D.1d's negative is not an artifact of the most pessimistic rule** — the per-rule attribution and the "delete every crossing fill" counterfactual both leave it negative, and the counterfactual was itself re-run when the audit showed the first version mixed denominators (progress.md:2673-2680, 2742-2745).
- **The infrastructure honesty record.** Every coverage/interval defect I probed had already been found and fixed by the project, usually with a regression test and a named class: gap double-counting (progress.md:53-70), span clamping (progress.md:71-88), the checksum-vs-sequence asymmetry and the "declared mechanism that ran zero comparisons" FAIL (progress.md:89-108), the coverage numerator crediting gap time (progress.md:210-218), the CME closure-window double count (progress.md:704-712), and the E.2 finding that the memory guard was measuring pytest (progress.md:2901-2960). I found no instance of a metric flattering the data that the project had not already caught.
- **`backtest/`** (512 lines across `reporting/`): the `PerformanceReport` contract requires `mode` with no default and the TypeScript drift test is real; nothing here carries a research conclusion, so there is no closure to challenge.
- **`research/experiments.jsonl`** is genuinely append-only and internally consistent with the narrative: 19 runs, monotone timestamps, each carrying `git_sha`, `cost_summary` and `leakage_tests`. Where the narrative says a venue produced nothing, the log says `{"error": "no valid samples"}` rather than omitting it (line 2). I used it as evidence *against* the project only where it shows a run that was never made.

Where the thesis would have shown up and did not: I looked for (a) a reopening threshold quietly loosened after a result, (b) a bar edited between registration and execution, (c) a negative reported on a smaller sample than the positive it replaced, and (d) an exclusion window introduced to remove inconvenient data. I found the opposite of (a)–(c) in every stage I checked, and (d) only in the form the project itself flagged and fixed (the C.6 roll exclusion that removed 0 seconds of the damage it existed to exclude, progress.md:1044-1060).

## Live-repo access log

Purpose: (i) untracked/gitignored working-tree data that exists only in the live tree —
`data/vendor/spend_ledger.jsonl`, `data/vendor/helius_credit_ledger.jsonl`,
`data/raw/venue=hyperliquid/date=2026-08-05/hour=12/messages.ndjson.zst`; (ii) `git log` to confirm
HEAD equals the anchored SHA. All reads were read-only; no repository file was opened for writing and
no repository script was executed in place. Everything read this way is **UNANCHORED**: read times
2026-09-05T05:54:32Z → 2026-09-05T05:56:03Z, and it may have changed after the anchor.

```
=== BEFORE  git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain
    (2026-09-05T05:54:32Z) ===
<no output — working tree clean>
=== (end) ===

=== AFTER   git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain
    (2026-09-05T05:56:03Z) ===
<no output — working tree clean>
=== (end) ===
```

`git log --oneline -3` at the time of access: `5359a11` (HEAD, = the anchored SHA), `ae03bf6`,
`aeabff6`. No modification was made and none is suspected.

Scratch computation directory (outside every audited repo):
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-mlcrypto-p3/recompute.txt`.
