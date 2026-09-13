# Agent B draft findings — NPLExperiment, part p2-progress

**Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c (main, 2026-09-02)
**Assigned documents:** DECISIONS.md, progress.md, docs/ (ACCESS, H5_ACCESS, PAIR_FEASIBILITY, STAGES, SUBSTRATE), reports/
**Direction:** B (claimed more than earned)
**Snapshot read:** /home/kiros-li/.cache/program-audit/scratchpad/snap/NPLExperiment/
**Unanchored data read from the live working tree (read-only) at 2026-09-12T12:40–12:48Z** — see the access log at the end. Every figure drawn from `data/` is marked UNANCHORED and may have changed since the anchor.
**Recomputation venv:** /home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python; scratch scripts under /home/kiros-li/.cache/program-audit/scratchpad/work/agentB-npl-p2/

---

### DRAFT-p2-progress-1
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H5 — Amendment H5-2 (the delisted exclusion), ADR-030, and the shipped stratum table in docs/H5_ACCESS.md §5
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Every observation above the bar lived in dead markets.**" — NPLExperiment/DECISIONS.md:498 (ADR-030). The same claim, in the shipped access document: "**Every observation above the 54 bp VIABLE bar lives in the delisted stratum.**" — NPLExperiment/docs/H5_ACCESS.md:197; and the table row it rests on, "| **live** | **94** | **3.72 bp** | 0.73 – 7.31 | 51.4 bp | 8.5 % | **0.0 %** |" — NPLExperiment/docs/H5_ACCESS.md:193, repeated at progress.md:1280 and progress.md:1288-1289 ("against **3.72 bp and 0.0 percent** for live instruments").
- **Evidence:**
  - The repository's own fired verdict artifact records live-only observations above the bar: `primary_registered_basis` / `by_session_tag.extended` carries `"share_over_viable": 0.015957446808510637` on `"n": 188` — NPLExperiment/reports/h5/verdict.json (snapshot copy). 0.015957… × 188 = **3 observations strictly above 54 bp**. `npl/h5/stats.py:87` defines the share as `sum(1 for m in magnitudes if m > viable_bp) / n`, i.e. strictly greater, matching ADR-029's registered convention (DECISIONS.md:484).
  - The pool is live-only by construction: `scripts/h5_fire.py:60` skips any row where `coin not in live_coins or row["listing_status"] != STATUS_LIVE`, and `verdict.json` `inputs.snapshots_counted` is `{h5-census-2026-08-28T21:51:54Z: 94, h5-census-2026-08-28T22:00:14Z: 94}`.
  - Reproduced exactly from the live stores (UNANCHORED, read 2026-09-12T12:41Z, `data/h5/census.jsonl` + `data/h5/snapshots.jsonl`): the 188-row live pool gives median 4.14463090419424 bp, share_over_floor 0.09574468085106383, share_over_viable 0.015957446808510637 — identical to verdict.json to every digit. The three offending rows are **live** instruments: `xyz:URNM` (etf) −55.64056196967594 bp at 21:51:54Z, `xyz:URNM` −63.29113924050584 bp at 22:00:14Z, `xyz:QCOM` (equity) +54.45090241664208 bp at 22:00:14Z. All three carry `session_tag: extended` and `listing_status: live`.
  - The stratum table itself is from the wrong pass. docs/H5_ACCESS.md:6 states "Both passes returned **identical** counts on every figure below; the second is the one recorded (`h5-census-2026-08-28T21:51:54Z` …)". Recomputing both passes from `data/h5/census.jsonl` (UNANCHORED, read 2026-09-12T12:44Z): pass 1 (`h5-census-2026-08-28T21:44:11Z`, resolved & not `is_delisted`) → n=94, median 3.7227, IQR 0.7576–7.3007, max **51.3919**, >18 bp 8.51 %, >54 bp **0.0 %** — exactly the published row. The **recorded** pass (`21:51:54Z`, resolved & `listing_status == live`) → n=94, median **4.2137**, IQR 0.7412–9.0865, max **55.6406**, >18 bp 7.45 %, >54 bp **1.06 %** (1 of 94). So the published "live" row is the unrecorded pass, and on the pass the document says is recorded, one live instrument sits above the VIABLE bar.
  - Instrument counts *are* identical across the two passes (151 resolved in both), so the "identical counts" sentence is true of counts and false of the basis figures in the table it introduces.
- **Recomputation (if any):** inputs — `data/h5/census.jsonl` (546 rows, 2 census passes) and `data/h5/snapshots.jsonl`, read 2026-09-12T12:41–12:44Z; method — reproduce `scripts/h5_fire.py:46-76` (live_coins from the latest census row per coin with `resolution_state=="resolved"`, `listing_status=="live"`, `reference_served`), then `npl/h5/stats.py:64-88` median/quantile/exceedance verbatim. Result — verdict pool n=188, median 4.14463090419424, >54 bp = 3/188 = 0.015957446808510637 (bit-identical to reports/h5/verdict.json); recorded census pass live stratum n=94, max 55.6406 bp, >54 bp = 1/94. Script: /home/kiros-li/.cache/program-audit/scratchpad/work/agentB-npl-p2/h5_check3.py and h5_check4.py.
- **What would resolve it:** restate the ADR-030 / H5_ACCESS.md §5 sentence as "every observation above the bar in the 21:44:11Z reconnaissance pass", republish the §5 table against the recorded pass (or label it as pass 1), and note the three live above-bar observations the fired verdict already records. The amendment's *direction* argument ("a market with no participants cannot deviate", DECISIONS.md:511) stands without the categorical sentence.
- **Confidence:** HIGH — the contradicting figure is inside the repository's own fired verdict artifact and reproduces bit-identically from the stores.
- **Invalidated by later commits?:** no — the only post-anchor commit (dff1663, 2026-09-10, Amendment H5-3) touches progress.md and registrations/H5 only, and moves the fire date; it does not touch ADR-030, docs/H5_ACCESS.md, or the verdict artifact.
- **Disclosed by authors?:** no — the authors disclose the delisted/live split and that the amendment was made with the census in hand (DECISIONS.md:509-513), but they nowhere disclose that the shipped live-stratum row comes from the unrecorded pass or that the recorded pass and the fired verdict both contain live observations above the bar.

---

### DRAFT-p2-progress-2
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H5 — the armed daily forward collector and the Section 6 outcome map it will fire (docs/STAGES.md H5 ladder; `npl.h5.collector` wired into `npl.cli.cmd_daily`)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "so **deviation is characterized within each session tag separately** and every figure carries its tag and its n." — NPLExperiment/DECISIONS.md:446-448 (ADR-028); and the shipped exit gate "**H5 census window** (open; collector armed) | Over 30 days and **all four session tags**, how far does the mark sit from the venue's own oracle?" with terminal row "**CLOSED** (under 18 bp in every tag) → the family closes, collection stops" — NPLExperiment/docs/STAGES.md:40-41.
- **Evidence:**
  - The armed collector runs once a day inside the daily pass: "The collector is `npl.h5.collector.run_daily_pass`, wired into `npl.cli.cmd_daily` as the **last** block of the daily pass" — NPLExperiment/progress.md:1355-1356. The daily pass is `OnCalendar=*-*-* 01:40:00 UTC` — NPLExperiment/ops/systemd/npl-daily.timer:5.
  - The registered tagger maps 01:40 UTC to 21:40 `America/New_York` (EDT) or 20:40 (EST); `npl/h5/calendar.py:154-175` returns `regular` only for 09:30 ≤ clock < close and `extended` only for 04:00–09:30 or close–20:00, otherwise `closed_weekday` / `weekend`. 21:40 and 20:40 both fall after `POSTMARKET_CLOSE = time(20, 0)` (`npl/h5/calendar.py:45`).
  - Recomputed over the 29 projected passes 2026-08-29 → 2026-09-26 at 01:40 UTC using the registered 2026 holiday/early-close tables (`npl/h5/calendar.py:74-112`): **21 `closed_weekday`, 8 `weekend`, 0 `regular`, 0 `extended`.** Script: work/agentB-npl-p2/session_tags.py.
  - Realized, UNANCHORED (read 2026-09-12T12:41Z, `data/h5/snapshots.jsonl` + `census.jsonl`): 13 scheduled passes have run since arming. Live-instrument observations by tag are `closed_weekday` **848**, `weekend` **282**, `extended` **188**, `regular` **0**. All 188 `extended` rows are the two manual 2026-08-28 passes (21:51:54Z and 22:00:14Z); **every scheduled pass since has landed in `closed_weekday` or `weekend`.**
  - The map does not require the tags to be populated. `npl/h5/outcome.py:98-102` builds `present` from tags that carry a served median, and line 156 fires CLOSED when `all(value < floor for value in present.values())` — over measured tags only. Amendment H5-1 is recorded as having closed exactly this hole — "the CLOSED floor clause waits for the coverage bars, because a single cross-section lands in one session tag and \"under 18 bp in every tag\" would have been satisfied vacuously. Makes CLOSED **strictly harder**" (NPLExperiment/progress.md:1304-1306) — but the gate it added is the coverage-day count (`npl/h5/outcome.py:145`), not tag population, so the vacuity is deferred, not removed.
  - Consequence: on the schedule as armed, the row that fires will be decided on a pool that is ~100 % observations taken while the underlying US equity market is shut, against a design whose own ADR says "A perpetual on a closed underlying has no reference market at all. Pooling a Saturday snapshot with a Tuesday-morning one is the fastest way to manufacture a basis that is really a stale reference" (NPLExperiment/DECISIONS.md:444-446). The `regular` tag — the only one in which an underlying reference market exists — will be empty at firing.
- **Recomputation (if any):** inputs — ops/systemd/npl-daily.timer:5 (01:40 UTC), npl/h5/calendar.py:41-46 and 154-175 (session boundaries), npl/h5/calendar.py:74-112 (2026 holiday/early-close dates), progress.md:1401 (29 passes, fire 2026-09-26). Method — tag each of the 29 projected 01:40 UTC instants with the registered rule. Result — {closed_weekday: 21, weekend: 8, regular: 0, extended: 0}. Cross-checked against realized live data: {closed_weekday: 848, weekend: 282, extended: 188 (all pre-schedule), regular: 0}.
- **What would resolve it:** either add at least one intraday pass inside the US regular session (the hourly `npl-watch` timer already fires every hour and would supply `regular` and `extended` tags at no extra design change), or amend Section 6 so the CLOSED clause names the tags it requires and refuses to fire on an unpopulated `regular` tag. Publishing the row at 2026-09-26 with `regular` absent, without saying so, is the outcome this finding is about.
- **Confidence:** HIGH — the schedule, the tagger and the map are all in the snapshot, and the realized tag histogram from 13 scheduled passes confirms the arithmetic.
- **Invalidated by later commits?:** no — the post-anchor commit dff1663 (2026-09-10, Amendment H5-3) moves the fire date to ~2026-10-05 and explicitly states "The registered gate is untouched"; it does not change the pass time, the tagger, or the map, and the realized tag histogram above already includes every post-anchor pass.
- **Disclosed by authors?:** no — progress.md:1400 records "`regular`, `closed_weekday`, `weekend` | **no observations yet** | — | absent, not zero" as a state of the census at firing, but nothing anywhere says that the armed schedule cannot produce a `regular` observation at all.

---

### DRAFT-p2-progress-3
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H1 — A.1 Task 4, the delisting-observability test, and the cohort-validity conclusion it carries into every downstream entry
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Verdict: PASS in full — 6 of 6 probed delisted perps serve both their candle history (through their delisting date) and their funding history.** The retrospective cohort is not survivorship-manufactured by the venue's serving behaviour." — NPLExperiment/docs/ACCESS.md:213-216. Carried into the register without the hedge: "Delisting observability PASS 6/6 — the cohort is not survivorship-manufactured." — NPLExperiment/HYPOTHESES.md:53 (primary evidence outside my assignment for that one line).
- **Evidence:**
  - The probe set: "Probe: the full 1d span and the first funding page for six perps flagged `isDelisted` in meta" — docs/ACCESS.md:202. The six named in the table at docs/ACCESS.md:206-211 are MATIC, RNDR, FTM, UNIBOT, CYBER, FRIEND — **all main-dex vanilla perps; zero HIP-3 instruments were probed.**
  - The cohort the claim certifies is half HIP-3: "retro-eligible N = 312 (112 vanilla / 46 hyperp_conversion / **154 hip3**" — NPLExperiment/progress.md:274-275. The successor cohort is almost entirely HIP-3: "fresh cohort 62 (**60 hip3**, 2 vanilla)" — NPLExperiment/progress.md:662.
  - The census contains the counterexamples the probe was built to find. "excluded 129 (74 epoch_censored, **53 no_candles**, 1 no_funding_rows, 1 died_before_entry)" — NPLExperiment/progress.md:275. Reading the census ledger directly (UNANCHORED, `data/census/census.jsonl`, 505 rows / 504 distinct coins, read 2026-09-12T12:46Z): **53 instruments carry `state: "no_data"` with zero candle rows; all 53 have `is_delisted: true`; all 53 sit on HIP-3 builder dexs** (mkts 19, xyz 14, para 7, io 4, vntl 2, hyna 2, cash 2, flx 1, km 1, abcd 1) and **none on the main dex**. That is precisely the registered FAIL condition — "FAIL means delisted history is unreachable" (progress.md:84) — realised on 53 instruments, in the population the probe never sampled.
  - The exclusion is not neutral in direction. The repository's own secondary shows retained delisted events underperform: `secondaries/truncated_by_delisting_30d` = `n: 10, share_positive: 0.5` against `retro share_positive 0.6314102564102564` (NPLExperiment/reports/stage_b/read.json). Dropping 53 further delisted instruments whose history the venue will not serve therefore plausibly raises the measured share positive — conservative for H1's FAIL row, but the claim being made is not about H1's row, it is that the cohort is *not* survivorship-manufactured, and that claim is what the census contradicts.
  - The two facts are never related anywhere in the repository: `no_candles` appears exactly four times (report.md:62, report.md:190, REGISTRATION.md:391, progress.md:275), always as a bare count, never beside the delisting-observability verdict.
- **Recomputation (if any):** inputs — docs/ACCESS.md:202-216 (probe set and verdict), progress.md:274-275 (cohort composition and exclusions), progress.md:662 (fresh cohort), data/census/census.jsonl (UNANCHORED, read 2026-09-12T12:46Z), reports/stage_b/read.json (`truncated_by_delisting_30d`, `forward_vs_retro_30d.retro.share_positive`). Method — group the latest census row per coin by `state`, `candle_rows`, `is_delisted` and `dex`. Result — 53 `no_data`/zero-candle rows, 53/53 delisted, 53/53 HIP-3, 0/53 main-dex; 179 of 504 instruments delisted overall, 123 of them on HIP-3 dexs, so 53 of 123 (43 %) of delisted HIP-3 instruments serve no candle history at all. Script: work/agentB-npl-p2 (inline, final Bash block).
- **What would resolve it:** re-run A.1 Task 4 on a HIP-3 delisted probe set of comparable size and report the result beside the main-dex one; and state the 53 `no_candles` exclusions as what they are — instruments removed from the cohort because the venue does not serve their history — next to the survivorship verdict rather than only inside an exclusion tally. If the HIP-3 probe fails, the registered consequence already exists (progress.md:47: a partial pass "demot[es] the retrospective cohort to descriptive").
- **Confidence:** HIGH — the probe set is named in the document, the cohort composition is in progress.md, and the 53 counterexamples are all in the repository's own census ledger with unanimous flags.
- **Invalidated by later commits?:** no — no post-anchor commit touches docs/ACCESS.md, the census rule, or the cohort.
- **Disclosed by authors?:** no — docs/ACCESS.md:215-216 carries the narrow hedge "by the venue's serving behaviour", which is the exact mechanism the 53 exclusions exhibit, and HYPOTHESES.md:53 drops even that hedge. No document links `no_candles` to the survivorship test.

---

### DRAFT-p2-progress-4
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** P3 — the single PASS in the repository — and its transport into H2's registered power assumption E1 = 0.65
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "P3 114/175, p = 3.767e-05 PASS" — NPLExperiment/progress.md:480-481; carried forward as "Figures carried in as assumptions, generating-sample-derived and labelled so in every registration: **P3 pair share 114/175 = 0.651** … strata share-positive vanilla 0.670 (n 112), hyperp_conversion 0.696 (n 46), **hip3 0.584 (n 154)**" — NPLExperiment/progress.md:533; and "Power assumptions: **E1 true share 0.65** … generating-sample-derived" — NPLExperiment/progress.md:549.
- **Evidence:**
  - P3 is computed on a cohort produced by an uncorrected screen. `reports/stage_b/read.json` records `co_primaries/p3`: `n = 175`, `successes = 114`, `statistic = 3.766632285793312e-05`, `n_underpowered = 137`. The 137 dropped events are those with no Section 6 control — "the 136 no-candidate events drop from P3 only, counted" (NPLExperiment/progress.md:322-323).
  - The screen is the same-dex 180-day elder rule (ADR-002, DECISIONS.md:17-28), so it selects on **dex maturity**, not at random. Reading the H1 pair ledger (UNANCHORED, `data/controls/pairs.jsonl`, 176 rows, read 2026-09-12T12:42Z): **156 pairs are main-dex (`dex: ""`) and 20 are `xyz`.** Against the P1/P2 cohort of 112 vanilla + 46 hyperp_conversion (=158 main-dex) + 154 hip3:
    - main-dex events entering P3: **156 of 158 = 98.7 %**
    - hip3 events entering P3: **20 of 154 = 13.0 %**
    - P3 cohort is **88.6 % main-dex** against **50.6 %** for the cohort P1 and P2 read.
  - The under-represented stratum is the weakest one the repository measured: `secondaries/per_type_strata_30d` in reports/stage_b/read.json gives hip3 `share_positive 0.5844155844155844` (n=154) against vanilla 0.6696 (n=112) and hyperp_conversion 0.6957 (n=46). The registered secondary list computes strata for the share-positive statistic only; **no document or artifact reports P3 by stratum**, so the paired differential is never shown for the 20 hip3 pairs.
  - The transport is in the opposite direction to the screen. H2's cohort is "fresh cohort 62 (**60 hip3**, 2 vanilla)" (progress.md:662) and its forward accrual is "18.57 events/month total … **main-dex 0.5/month (n = 3/182d)**" (progress.md:664-666) — i.e. ~97 % HIP-3. So E1's registered true share 0.65, taken from a sample that is 88.6 % main-dex, is applied to a cohort that is ~97 % HIP-3, the stratum that contributes **20 of the 175 P3 pairs**.
  - Scale of the evidence actually available for that stratum: at the pooled share 0.651, 20 pairs would give 13 successes, and the exact one-sided sign test returns p = 0.1316 — no evidence at the registered alpha_adj = 0.016952, let alone at H2's alpha_h = 0.05 after correction. The listing-age effect H2 exists to re-test is therefore essentially unevidenced in the population H2 will read.
- **Recomputation (if any):** inputs — reports/stage_b/read.json (`co_primaries/p3`, `secondaries/per_type_strata_30d`), data/controls/pairs.jsonl (UNANCHORED, read 2026-09-12T12:42Z), progress.md:274-275 (cohort composition), progress.md:662 and :664-666 (H2 cohort and accrual). Method — count pair rows by `dex`; exact binomial one-sided tail `P(X ≥ 114 | n=175, p=0.5)`; and `P(X ≥ 13 | n=20, p=0.5)`. Result — P3 p = 3.76663228579e-05, reproducing reports/stage_b/read.json's 3.766632285793312e-05 exactly; P3 cohort 156 main / 20 xyz; hypothetical hip3-only sub-test p = 0.1316. Scripts: work/agentB-npl-p2/p3.py and pairs.py.
- **What would resolve it:** report P3 by the registered `vanilla` / `hyperp_conversion` / `hip3` strata (the strata are already registered secondaries, so this is not a new statistic), and state in registrations/H2 §8 that E1's 0.65 is estimated on a sample 88.6 % main-dex and applied to a cohort ~97 % HIP-3, with the HIP-3 sub-sample's n. If the hip3 P3 sub-share is materially below 0.651, H2's minimum-N and its two look dates all move.
- **Confidence:** HIGH on the composition and the transport (both derive from the repository's own ledger and its own stratum secondary); MEDIUM on how much the assumption would move, because the hip3 P3 sub-statistic was never computed and I did not open the sealed outcomes to compute it.
- **Invalidated by later commits?:** no — no post-anchor commit touches the H1 read, the pair ledger, or H2's registered power assumptions.
- **Disclosed by authors?:** partially — the drop count is disclosed ("the 136 no-candidate events drop from P3 only, counted", progress.md:322-323) and the H2 cohort's 60/62 HIP-3 composition is disclosed (progress.md:662), but the P3 cohort's own dex composition is nowhere stated and the mismatch between the two is never raised.

---

### DRAFT-p2-progress-5
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H2 — the recomputed power that lifts the amended design over its registered 0.80 target (Amendment H2-3 Change 2 / ADR-023)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Recomputed power beside the registered 0.80 target:** single-look governing 0.8886 (the Section 0 function returns GO), two-look governing 0.8629." — NPLExperiment/progress.md:939-941. Shipped in the README without the sensitivity row: "recomputed power at the deadline 0.889 single-look / 0.863 two-look" — NPLExperiment/README.md:16 (primary evidence outside my assignment).
- **Evidence:**
  - The governing figure is a function of a number the repository itself calls twice-removed from measurement. ADR-023: "the registered power assumption had to move with the floor — E2's 0.60 was **itself a judgment discount from E1's 0.651, not a measurement** — and the new figure is set by **linear interpolation in the floor multiple** … giving 0.625 at multiple 1. Linear is the neutral choice, **not a claim about a distribution nobody has measured**." — NPLExperiment/DECISIONS.md:308-313.
  - The entire GO/DEGRADED distinction turns on that 0.025. From reports/stage_a_h2/ktable_amended.json, `single_look_k_table_extension_at_deadline` → `H2/E2`: `n: 135`, `power_governing: 0.888596`, `power_reported: 0.731814`. Recomputed exactly: one-sided exact sign test at n=135, alpha=0.05 (critical k=78) gives power 0.8886 at true share 0.625 and **0.7318 at the registered 0.60**.
  - The break-even is narrow. At n=135 and alpha=0.05 the power crosses 0.80 at true share **0.6093** and crosses 0.50 at 0.5739. So the claim "above the registered 0.80 target" survives a downward revision of the unmeasured E2 share of only **0.0157** before it fails.
  - The measurement was available and permitted. The register's own rule 1 makes the generating sample "usable for power assumptions" (HYPOTHESES.md:138-141), and the sealed read already produced the 175 paired 30-day differentials whose means are recorded (`secondaries/h8_paired_30d`: `mean_price_term_diff 0.06426309349214424`, `mean_funding_term_diff 0.008815909155428573`, `n 175` — reports/stage_b/read.json). The share of those 175 differentials exceeding 1× and 2× the pair's central cost is directly computable from data the register says may be used for exactly this purpose, and was not computed; a judgment discount plus a linear interpolation was used instead.
- **Recomputation (if any):** inputs — reports/stage_a_h2/ktable_amended.json (`inputs.true_shares`, `single_look_k_table_extension_at_deadline`, `projection_by_month` deadline 135), DECISIONS.md:308-316, npl/power.py:44-63 (critical_k / exact_power). Method — exact one-sided binomial sign test, p0=0.5, alpha=0.05, n=135; bisection on true share for power targets 0.80 and 0.50. Result — power(0.600)=0.7318 (reproduces the artifact's 0.731814), power(0.625)=0.8886 (reproduces 0.888596), break-even at 0.80 = 0.6093, at 0.50 = 0.5739. Also verified at the cull's n=141: power(0.600)=0.7604 reproducing ktable_cull.json's 0.760372, and E1 power(0.65)=0.9743. Script: work/agentB-npl-p2/h2power.py.
- **What would resolve it:** compute the share of the 175 generating-sample paired differentials at or above 1× (and 2×) the pair's own central cost and register it as E2's true share, replacing the interpolation; or carry the 0.60 row ("does not reach 0.80 by the deadline") into the README and HYPOTHESES status line wherever the 0.889/0.863 figures appear.
- **Confidence:** HIGH on the arithmetic (it reproduces the repository's artifact exactly); MEDIUM on materiality, because the authors do publish the 0.60 alternative in three places.
- **Invalidated by later commits?:** no — no post-anchor commit touches H2's power assumptions.
- **Disclosed by authors?:** yes — DECISIONS.md:313-316 ("A reader who rejects the interpolation can read the second row and see that the design does not reach 0.80 by the deadline"), progress.md:1074-1076, HYPOTHESES.md:74. The finding is that the disclosure is absent from the README status line and from the "0.80 target cleared" framing, and that a measurable quantity was replaced by a judgment when the register's own rules permitted the measurement.

---

### DRAFT-p2-progress-6
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** the A.2 register cull — the choice of pair-projection model that decided whether H2 survived
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The by-dex pair projection governs; the flat summary rides beside" — NPLExperiment/DECISIONS.md:189 (ADR-016 title); "Both projections use only A.1-measured quantities committed before any cull arithmetic ran." — NPLExperiment/DECISIONS.md:198-200.
- **Evidence:**
  - The two models give opposite verdicts for the surviving hypothesis. reports/stage_a_h2/ktable_cull.json: `cull_bydex` → `k: 1`, `survivors: ["H2"]`, pass 1 required power `H2: 0.577117`; `cull_flat_sensitivity` → `k: 0`, `survivors: []`, `blocked: ["H2","H3","H4"]`, pass 1 required power `H2: 0.431772`. Deadline pair counts: by-dex 141, flat 106 (`inputs/scenarios/deadline_2027-03-31`).
  - The registration section that governs the cull, as committed at register A.0 (commit 77ee522, 2026-08-27T20:53:20-07:00, i.e. before the A.1 census refresh and before any projection existed), specifies only "at projected N by 2026-12-31 and 2027-03-31 using the **measured** accrual and match rates from A.1" (`git show 77ee522:registrations/H2/REGISTRATION.md`, Section 9, lines 176-181 of that blob). **It does not say whether the projection is by-dex or flat.** The choice is first stated in Amendment H2-1, the amendment that records the verdict itself, with both numbers already computed (`reports/stage_a_h2/ktable_cull.json` `computed_at: 2026-08-28T05:41:32Z`; the amendment and the ktable landed together in commit 2b44c59, 2026-08-27T22:45:38-07:00 = 2026-08-28T05:45:38Z).
  - The repository applied the opposite rule to the two hypotheses it blocked. ADR-017: "power computes at both ends of the honest range and **the generating-sample-derived end governs the cull — adopting the optimistic end after seeing the pessimistic one would be outcome-fitting**" — NPLExperiment/DECISIONS.md:206-210. Under that rule H3's magnitude leg governs at 0.356 (power 0.0000, BLOCKED) and H4's best cell at the measured conditioning rate (power 0.0140, BLOCKED), with the optimistic ends (0.65 and 0.85) declined and reported beside (progress.md:693-697). For H2 the **optimistic** of the two projections (141 vs 106) was adopted and governs, and H2 survived.
  - ADR-016 gives a substantive reason for the asymmetry — pairability is a deterministic function of measured dex age rather than a stationary share (DECISIONS.md:195-199) — and the reason is good. The finding is that it was recorded after both numbers existed, in a registration section that had not pre-specified it, on the one hypothesis whose survival it decided.
- **Recomputation (if any):** inputs — reports/stage_a_h2/ktable_cull.json (`cull_bydex`, `cull_flat_sensitivity`, `inputs/scenarios`), `git -C <live> show 77ee522d39950adc345540a2a500ead3deb8d86c:registrations/H2/REGISTRATION.md` Section 9, `git log` timestamps for 77ee522 (2026-08-27T20:53:20-07:00) and 2b44c59 (2026-08-27T22:45:38-07:00). Method — read-only git history against the artifact's own `computed_at`. Result — the governing-model statement postdates the arithmetic that made it decisive; no pre-registration of the model exists.
- **What would resolve it:** nothing can un-choose it now, but the register's own stated lesson applies verbatim — ADR-013's "A future register weighing sequential (worst-first) removal should decide BEFORE any projection exists" (DECISIONS.md:162-164) should be extended to the projection model itself, and the H2 status line should carry the flat-variant verdict (k = 0) beside the by-dex one wherever the DEGRADED/GO row is quoted.
- **Confidence:** MEDIUM-HIGH — the artifact and the git objects are decisive on timing; the judgement that this is a bar chosen after data existed rests on the absence of a pre-registration, which I verified by reading the A.0 blob.
- **Invalidated by later commits?:** no — the cull is fixed by Amendment H2-1 and "never revisited after any outcome exists"; no post-anchor commit touches it.
- **Disclosed by authors?:** yes — the sensitivity is disclosed plainly at DECISIONS.md:160-164, DECISIONS.md:195-200 and registrations/H2/REGISTRATION.md:286-289 ("under the flat variant H2's E2 leg sits at 0.4318 at the pass-1 alpha and the cull would fire k = 0 — recorded plainly"). The finding is the asymmetry against ADR-017's own standard, not the concealment of the alternative.

---

### DRAFT-p2-progress-7
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H5 — the census-window projection "29 daily passes needed; projected fire date 2026-09-26", and ADR-032's scope statement in the anchored commit itself
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| passes needed / projected fire | **29** / **2026-09-26** | — | binding instrument at 1 covered day |" — NPLExperiment/progress.md:1401; shipped as a scheduled event: "The map fires on **2026-09-26**, when the 20th-best-covered instrument reaches 30 covered days **at one pass per day**" — NPLExperiment/docs/STAGES.md:40, and "**H5's census window** runs 2026-08-28 to **2026-09-26** on the armed daily collector; **its row fires on schedule**" — NPLExperiment/docs/STAGES.md:56-58. And in the same anchored commit: "The honest cost-benefit. **Data integrity was not at risk**: the guard behaved correctly at every failure, the next hourly sweep recovered, **the daily pass catches up regardless**" — NPLExperiment/DECISIONS.md:592-594 (ADR-032).
- **Evidence:**
  - The projection assumes a lossless daily cadence and says so: `scripts/h5_fire.py:124-127` writes the note "one daily pass adds one covered day to every live instrument", and `npl/h5/outcome.py:200-217` computes `passes_needed` as `h5_min_coverage_days − binding` with no allowance for a missed or partial pass.
  - ADR-032, dated 2026-09-02 and *in the anchored commit*, documents the failure mode: "Four watcher sweeps between 2026-08-31T21:23Z and 2026-09-02T09:10Z polled zero dexs and recorded `source_failed` … Every one sat at a boot or resume boundary" (DECISIONS.md:551-555). Its mitigation claim — "the daily pass catches up regardless" — is true for the funding archive and candle windows (cursor-resumable, ADR-010) and **false for H5**, whose observations are point-in-time marks and books: a missed H5 pass is a permanently lost covered day, and covered days are the only input to the fire date.
  - Realized accrual, UNANCHORED (`data/h5/snapshots.jsonl`, read 2026-09-12T12:41Z): scheduled passes exist for 2026-08-29, 08-30, 08-31, 09-01, 09-02, **09-03 with only 4 live rows against a normal 138-150**, 09-04, **[09-05 absent]**, **[09-06 absent]**, 09-07, 09-08, 09-09 (06:18Z), 09-10 (04:49Z), 09-11, 09-12. The 20th-best-covered instrument stands at **13** covered days on day 15 of a 30-day window.
  - The repository conceded the point 8 days after the anchor: commit dff1663 (2026-09-10) "Amendment H5-3 - fire date recomputed at measured 0.77 passes/day; no bar moved, projection was falsified by three lost collection days", which states "The machine sleeps and `Persistent=true` recovers the schedule, not the data … H5 snapshots are point-in-time marks and depth, so a missed day is permanently unrecoverable" and moves the date to ~2026-10-05, adding "Second falsified assistant planning figure in this register, after main-dex accrual at 9.4 per month against a measured 0.5 in H3."
- **Recomputation (if any):** inputs — progress.md:1401, docs/STAGES.md:40 and :56-58, npl/h5/outcome.py:200-217, scripts/h5_fire.py:115-128, DECISIONS.md:551-555 and :592-594, data/h5/snapshots.jsonl (UNANCHORED, read 2026-09-12T12:41Z), `git show dff1663`. Method — enumerate distinct `snapshot_id` values and count live rows per pass; take the 20th-best `covered_days`. Result — 15 passes recorded over 15 UTC days with 2 days missing and 1 pass truncated to 4 rows; 20th-best covered days = 13 at day 15 of 30.
- **What would resolve it:** already partly resolved post-anchor by Amendment H5-3. What is still open at the anchor is ADR-032's blanket "Data integrity was not at risk … the daily pass catches up regardless": it should name the one collector it is false for.
- **Confidence:** HIGH — the shortfall is in the repository's own store and the authors have since recorded the same conclusion.
- **Invalidated by later commits?:** partially — commit dff1663 (2026-09-10, post-anchor) corrects the fire date and adopts this finding's reasoning; it does **not** amend ADR-032's scope claim, and the finding is a claim about the anchored SHA, where the 2026-09-26 date was shipped in STAGES.md as a scheduled event.
- **Disclosed by authors?:** no at the anchor; yes afterwards — the disclosure is the post-anchor Amendment H5-3 in commit dff1663, which did not exist at 8f1fef8.

---

### DRAFT-p2-progress-8
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H2 — the forward-accrual assumption that carries look 2 (2027-03-01) and the 135-pair deadline count
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Look-2 minimum N: 117** (E1 84, E2 117). **Projected look-2 date: 2027-03-01**, one month inside the registered 2027-03-31 deadline. At the deadline the projection is 135 pairs." — NPLExperiment/progress.md:1063-1065; resting on "accrual 18.57 events/month total (n = 113 listings/182d)" — NPLExperiment/progress.md:664.
- **Evidence:**
  - Look 1 does not depend on forward accrual and I am not challenging it: reports/stage_a_h2/ktable_amended.json `projection_by_month` shows `forward_pairs_readable: 0` through 2026-11-30, so the 59 pairs at 2026-11-26 come entirely from the 62 backfilled pairs maturing. Look 2 does: it needs `forward_pairs_readable` 54 by 2027-02-28 and 73 by 2027-03-31, at `readable_lag_days_forward: 94` — i.e. ~18.6 new pairs per month with entries from 2026-08-28 onward.
  - Realized, UNANCHORED (`data/controls/h2_pairs.jsonl`, read 2026-09-12T12:42Z): **63 rows — 62 assigned 2026-08-28 (the amendment backfill) and exactly one assigned since, `PONS` at 2026-09-02T02:01:32Z.** One forward pair in the 15 days after arming, against a projection of ~18.6/month.
  - The watcher is running and is not the cause: `data/state/watcher.jsonl` (read 2026-09-12T12:45Z) shows clean hourly heartbeats through 2026-09-12T12:05:58Z, 11 dexs polled, 0 failed. The births ledger (`data/births/*.jsonl`, 15 rows, 2026-08-27 → 2026-09-11) shows **12 of 15 births flagged `is_delisted: true` at sighting** (para:IGV, para:SOFI, para:ANTH, para:TTWO, xyz:YMTC, xyz:BMNR, io:SBE, para:CIFR, io:TCNT, para:TREAD, xyz:SNXX, io:EWY) and only 3 live at sighting (PONS main-dex 08-31, io:GPRO 09-02, USELESS main-dex 09-08). One of those three produced an H2 pair.
  - At the realized rate the look-2 count is unreachable: 117 readable pairs by 2027-03-01 requires ~55 forward pairs with entries on or before 2026-11-27; at 1 pair per 15 days that is ~6. The design would then reach the 2027-03-31 deadline near the 62–70 backfill pairs, at which Section 10's trigger — "both co-primaries at or above **80 percent power at achieved eligible pair N** (not projected)" (registrations/H2/REGISTRATION.md:195-196) — is not met, because E2's look-2 minimum is 117.
  - The register has falsified two planning-accrual figures already, by its own account: H3's ~9.4/month against a measured 0.5 (progress.md:664-666) and H5's 1.00 passes/day against a measured 0.77 (post-anchor commit dff1663).
- **Recomputation (if any):** inputs — reports/stage_a_h2/ktable_amended.json (`projection_by_month`, `inputs.measured_accrual_events_per_month`, `readable_lag_days_forward`), data/controls/h2_pairs.jsonl and data/births/*.jsonl and data/state/watcher.jsonl (UNANCHORED, read 2026-09-12T12:42–12:45Z). Method — count pair rows by `assigned_at` date; count birth rows by `sighted_at` and `is_delisted`. Result — 62 pairs assigned 2026-08-28, 1 assigned 2026-09-02, 0 since; 15 births in 16 days of which 12 delisted at sighting. Script: work/agentB-npl-p2/accrual.py.
- **What would resolve it:** recompute the projection from realized forward pair accrual on a longer window (the 15-day sample here is short and I say so), and state the look-2 date as a recomputed figure rather than a scheduled one — the same correction the repository applied to H5 in Amendment H5-3. If the shortfall holds, look 2 cannot be reached and H2's terminal read falls back to the deadline at an N below its own registered trigger.
- **Confidence:** MEDIUM — the direction and the arithmetic are clear, but 15 days is a short window against an accrual measured over 182 days, and I have not established why 2 of the 3 live births did not produce pairs.
- **Invalidated by later commits?:** no — no post-anchor commit changes H2's projection; the evidence is post-anchor data about a pre-anchor projection and only strengthens with time or dissolves with a burst of listings.
- **Disclosed by authors?:** no — the withdrawal sensitivity that *is* disclosed (ktable_amended.json `pair_projection_models.withdrawal_sensitivity`: "at the pre-amendment same-dex-only match rate of 0.613 the deadline pair count would be 82 instead of 135") varies the match rate, never the accrual rate.

---

### DRAFT-p2-progress-9
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H5 — the `n = 188` attached to every basis figure in the fired verdict
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| median absolute basis, `extended`, n = 188 | **4.14 bp** (IQR 0.71–9.15) | floor 18 / bar 54 | — |" and "| share over 18 bp / over 54 bp | **9.57 % / 1.60 %** | — | — |" — NPLExperiment/progress.md:1398-1399.
- **Evidence:**
  - The 188 are 94 instruments observed twice. reports/h5/verdict.json `inputs.snapshots_counted` = `{"h5-census-2026-08-28T21:51:54Z": 94, "h5-census-2026-08-28T22:00:14Z": 94}`. The two snapshot ids are **8 minutes 20 seconds apart**, both inside the same `extended` session on the same day.
  - The exceedance shares use 188 as the denominator (`npl/h5/stats.py:86-87`), so "1.60 % over the 54 bp bar" is 3 of 188 where the underlying evidence is 3 flags on 2 distinct instruments (`xyz:URNM` twice, `xyz:QCOM` once — see DRAFT-p2-progress-1).
  - The within-8-minute variation is of the same size as the reported signal: recomputing per pass (UNANCHORED, read 2026-09-12T12:44Z) gives 21:51:54Z median 4.2137, max 55.64, 1 of 94 over the bar; 22:00:14Z median 4.1404, max 63.29, 2 of 94 over the bar.
  - Standing rule 10 of this repository is "Every figure travels with its **n** in the same sentence" (CLAUDE.md:42), and ADR-028 requires "every figure carries its tag and its n" (DECISIONS.md:447-448). An n that doubles because the same cross-section was sampled twice in eight minutes does not carry the information the rule exists to carry.
- **Recomputation (if any):** inputs — reports/h5/verdict.json (`inputs.snapshots_counted`, `by_session_tag.extended`), data/h5/census.jsonl and snapshots.jsonl (UNANCHORED). Method — per-snapshot median/max/exceedance over the live pool. Result — 94 + 94 = 188 with the two passes 8 m 20 s apart; per-pass over-bar counts 1 and 2.
- **What would resolve it:** report the H5 basis figures as "94 instruments × 2 snapshots" rather than n = 188, or pool at the instrument level (one value per instrument per pass-day) as the coverage bar already does (`scripts/h5_fire.py:64` counts covered **days** per coin, not observations).
- **Confidence:** HIGH — the snapshot ids and their timestamps are inside the shipped artifact.
- **Invalidated by later commits?:** no — the verdict artifact is unchanged at and after the anchor.
- **Disclosed by authors?:** partially — "Two snapshots, **188** observations" appears at HYPOTHESES.md:126 and the snapshot ids are in the artifact, so a reader can reconstruct it; the 8-minute separation is nowhere stated and progress.md:1398 presents the figure as n = 188 without qualification.

---

### DRAFT-p2-progress-10
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** docs/PAIR_FEASIBILITY.md — the shipped H2 feasibility memo, stale against the same-day Amendment H2-3
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "Concurrent pairs in steady state = accrual × hold: **18.57 events/month × (32/30.44) months ≈ 19–20 open pairs** (measured accrual; entry+30d hold plus fill slack) — of which the pairable share (**~0.61 measured**, rising as young dexs age) gives **~12–14 open pairs today**, rising toward ~19." — NPLExperiment/docs/PAIR_FEASIBILITY.md:65-69; and the position definition "One pair = **short the young listing + long its funding-matched elder, on the same dex**" — NPLExperiment/docs/PAIR_FEASIBILITY.md:13-14.
- **Evidence:**
  - The memo is dated "Written 2026-08-28 at register Stage A.3 Task 6" (docs/PAIR_FEASIBILITY.md:8-9); Stage A.3 closed 06:35Z (progress.md:707). Amendment H2-3 landed the same day at 07:01Z and took the match rate to 1.000: "Match rate, backfillable cohort | **62/62 = 1.000** (was 38/62 = 0.613)" — NPLExperiment/progress.md:887.
  - The amendment's own close-out lists the documents it updated — "HYPOTHESES.md H2 entry rewritten …; DECISIONS.md **ADR-022 … ADR-025** …; report.md gained the amendment section; docs/STAGES.md gained the A-amend rung …; README status line" (progress.md:1019-1025). **docs/PAIR_FEASIBILITY.md is not in that list and was not updated.**
  - So the shipped memo still sizes the sleeve on a 0.61 pairable share that the same day's amendment replaced with 1.000, and still describes the position as same-dex when 24 of 62 pairs are `cross_dex` (progress.md:1057) with a mixed 27 bp cost class rather than the 18/36 the memo's own restatement uses (docs/PAIR_FEASIBILITY.md:15-16 does list 27 mixed, so the cost line is fine; the concurrency and the "same dex" premise are not).
  - Direction: the stale figure understates capital need (12–14 concurrent pairs instead of ~19–20), so the memo's conclusion "The sleeve is feasible at the venue minimum with margin to spare" (docs/PAIR_FEASIBILITY.md:77-78) is asserted on the easier of the two numbers. At 19–20 pairs × $22 ≈ $420–$440 against the $1,000 sleeve it still holds, so nothing downstream changes.
- **Recomputation (if any):** none needed — 18.57 × (32/30.44) ≈ 19.5 concurrent pairs at match rate 1.000, against the memo's 12–14.
- **What would resolve it:** update docs/PAIR_FEASIBILITY.md to the post-amendment match rate and pair-type mix, or stamp it as pre-amendment.
- **Confidence:** HIGH — the dates and the update list are both in progress.md.
- **Invalidated by later commits?:** no — no post-anchor commit touches docs/PAIR_FEASIBILITY.md.
- **Disclosed by authors?:** no — the memo carries its write date but no superseded-by note, and the amendment's close-out does not record that it was left behind.

---

### DRAFT-p2-progress-11
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** `scripts/h5_fire.py` — the firing script that will produce H5's terminal row
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "No computed figure moves: every number in the verdict record was produced by `npl.h5.outcome.fire` and written by the script, never transcribed." — NPLExperiment/progress.md:1496-1498 (the claim that the firing path is a faithful pipe from the data to the map).
- **Evidence:**
  - `scripts/h5_fire.py:73` builds the map's only basis input as `medians = {tag: s.median_abs_bp for tag, s in tag_summaries.items() if s.median_abs_bp}` — a truthiness test on a `float | None` (`npl/h5/stats.py:51`). A session tag whose median absolute basis is exactly **0.0** is silently dropped from `medians`, while `n_by_tag` (line 74) keeps its n, so the artifact would report a tag with an n and no median.
  - The consequence in `npl/h5/outcome.py`: a dropped tag is absent from `present` (line 98-102) and so is excluded from the registered "under the floor in **every** measured session tag" test at line 156. If every populated tag had median exactly 0.0 — the strongest possible evidence for CLOSED — `max_median` is `None` and the map returns **PENDING** with "no session tag carries a served median; nothing to fire on" (line 154-155), i.e. the clearest CLOSED evidence available would fire no row at all.
  - The intended test is `is not None`: `summarize` already returns `median_abs_bp=None` for an empty sample (`npl/h5/stats.py:69-77`), which is the only case the filter should drop.
  - Practical reach is small: an exactly-zero median over dozens of instruments is unlikely, and the direction (0.0 < 18) does not change a CLOSED verdict where other tags are populated. It is a defect in a shipped firing script, not a wrong number today.
- **Recomputation (if any):** inputs — scripts/h5_fire.py:69-74, npl/h5/stats.py:45-88, npl/h5/outcome.py:98-102 and 143-165. Method — read the truthiness filter against the `float | None` return type and trace the dropped tag through `fire`. Result — a `median_abs_bp == 0.0` tag is excluded from the map's input; all-zero medians return PENDING rather than CLOSED.
- **What would resolve it:** change the filter at scripts/h5_fire.py:73 to `if s.median_abs_bp is not None`, and add a fixture with a tag median of exactly 0.0 (the repository's own standard — "a fixture comfortably inside its boundary lets a moved threshold pass unnoticed", CLAUDE.md:79-81).
- **Confidence:** HIGH — the defect is a plain reading of the source in the snapshot.
- **Invalidated by later commits?:** no — no post-anchor commit touches scripts/h5_fire.py.
- **Disclosed by authors?:** no.

---

## What I checked and found sound

Everything below is a place where I looked for the thesis "conclusions outran evidence" and did not find it. Several of these are strong marks in the repository's favour.

1. **Every piece of arithmetic I recomputed reproduced the repository's figure exactly, to the digit or to the last stored decimal.** P1 Clopper-Pearson lower bounds at all three cost bands (0.5739630116873008 / 0.5706880326738533 / 0.5608793225336948 at n = 312 — reports/stage_b/read.json `secondaries/cost_band_sensitivity`); P2's sign test 0.9999998937952859; P3's 3.766632285793312e-05; E1 power 0.9743 and E2 power 0.760372 at n = 141, alpha 0.05 (reports/stage_a_h2/ktable_cull.json); E2 0.888596 / 0.731814 at n = 135 (ktable_amended.json); and the H5 median 4.14463090419424, IQR 0.70947242299609–9.145925118703394, share_over_floor 0.09574468085106383 and share_over_viable 0.015957446808510637 (reports/h5/verdict.json), all reproduced from the raw stores. I found no arithmetic error anywhere.
2. **The minimum-N semantics are stricter than the naive definition and correctly so.** `npl/power.py:66-82` returns "the first n from which power never drops below target again", which handles the exact test's saw-tooth; my naive first-crossing search gave 69 / 102 / 158 against the repository's 76 / 111 / 169, and the repository's figures are the right ones (power at n = 70, p = 0.65 is 0.7755, below target). This is the opposite of a lowered bar.
3. **P3 is genuinely cost-invariant and the repository does not claim otherwise.** The paired differential subtracts the same registered cost from both legs, so `secondaries/cost_band_sensitivity` shows p3 identical (114/175, 3.766632285793312e-05) at low, central and high bands. I looked for an uncorrected cost model on the one positive and there is none.
4. **The multiplicity correction on the H1 co-primaries is real and was applied to the positive as well as the negatives.** alpha_adj = 0.016952427508441503 = 1 − 0.95^(1/3), applied to P3 as to P1 and P2 (reports/stage_b/read.json `alpha_adj`).
5. **The familywise cull's fixed-point direction is sound.** Removing H3/H4 at the stricter k = 3 alpha and then re-evaluating H2 at the relaxed k = 1 alpha is monotone in the right direction, and re-running the blocked hypotheses at alpha 0.05 does not rescue them (H3 min-N 262 against a deadline N of 5; H4 power 0.518 at n = 1200 against deadline cell Ns of 30/22/13 — ktable_cull.json `min_n_for_080`).
6. **ADR-029's arithmetic claim holds in code.** "neither 18 nor 54 is written as a literal anywhere in the map" (DECISIONS.md:481) — verified: `npl/h5/outcome.py:70-77` derives both from `CONFIG.hip3_round_trip_bp[1]` and `CONFIG.h5_viable_basis_multiple`, and no literal 18 or 54 appears in the module.
7. **The registered boundary conventions are implemented as registered.** VIABLE strictly greater than 54 (`npl/h5/outcome.py:165`), CLOSED strictly under the floor (line 156), funding clearing at at least one half (line 119, `<` for failure), the instrument bar at least 20 (lines 114 and 145) — all matching ADR-029 (DECISIONS.md:483-487).
8. **H5's write containment and quarantine gate are enforced, not asserted.** `reports/h5/h2_verification.json` records all 11 H2 store hashes identical, pair count 62 unchanged, three latches absent, and the two shared append-only ledgers verified by byte-identical prefix — which is the correct verification for an append-only file two writers share (progress.md:1443-1452). The prefix-hash design is recorded in the preconditions artifact before the work, not after.
9. **The H5 retrospective shortfall is reported honestly and is not used.** 27 of 151 eligible after the gate, 39 observations, 0 meeting coverage, and the secondary "fires nothing, in either direction" (progress.md:1407-1412); the firing script explicitly refuses to feed the map the gate's residue (`scripts/h5_fire.py:99-105`). A repository willing to claim more would have read the 39 observations.
10. **The "25 of 57 delisted HIP-3 instruments return no funding rows" figure is correctly scoped by the authors** to the registered 180-day probe window (progress.md:1332, `reports/h5/retro.json` `pages_fetched: 1`, `state: no_data`), so it is *not* a counterexample to the full-history servability claim, and I do not raise it as one.
11. **The H2 amendments' "before any outcome existed" claims check out structurally.** The three H2 latches and `h2_read.json` are absent at the anchor and at my read time (reports/h5/preconditions.json `h2_latches_absent` all true; `data/state/` unchanged), the amendment preconditions artifact scans and lists the 8 files under reports/ (reports/stage_a_h2/amend_preconditions.json), and the ADR-025 self-correction (a look-2 wording defect that would have fired FAIL on strong early evidence) is a falsification recorded against the authors' own amendment, not a rescue.
12. **The `pair_type` handling is disciplined.** `data/controls/h2_pairs.jsonl` (UNANCHORED) carries 38 rows with no `pair_type` (pre-amendment, same-dex by the rule that produced them), 24 `cross_dex`, and 1 `same_dex` — exactly what ADR-022 (DECISIONS.md:288-291) says it should, with no back-imputation.
13. **The ETA-against-actual corrections are made against the commit clock and recorded as corrections rather than edited in place** (progress.md:1465-1498, including "That 236 was a guess" at progress.md:1502). The repository corrects its own soft figures unprompted.
14. **H3 and H4's BLOCKED rows survive the scrutiny I applied to the positive.** Both were culled at the pessimistic end of an honest range with the optimistic end reported beside (progress.md:693-697), the governing figures are measured rates rather than assumptions, and the registered expectation of BLOCKED was stated before measurement (progress.md:552, 555). I found no negative reached by a process that would also have produced a positive on noise.

Two places where I formed a concern but the evidence did not support a finding:
- **Clustering / with-replacement dependence in P3.** The 176 H1 pairs draw on 82 distinct controls (effective 1/Σp² ≈ 41; top control serves 15 pairs) and the mean pair has 12.6 other pairs with entries inside ±30 days, so the sign test's independence assumption is imperfect. But P3 at the observed share 0.651 stays under alpha_adj = 0.016952 down to an effective n of about 45 (p = 0.0164 at n = 50; it first fails at n ≈ 41, p = 0.0298). A design effect above ~4× would be needed to break it, and I have no evidence for one. Recorded here rather than raised as a finding.
- **The H2 fallback control (ADR-022) as an outcome-fitted relaxation.** It was made on counts and tags only, before any pair outcome existed, it is stated as a relaxation in its own text, the `same_dex` stratum is computed beside every primary at every look, and it changed no bar, no alpha and no outcome definition. The temporal claim is checkable: commit f31f7a3 (Amendment H2-3) precedes f8e54d8 (the backfill) by 39 minutes, and all three H2 latches were absent throughout. I looked for a rescue and found a documented relaxation.

## Live-repo access log

Read-only access to /home/kiros-li/Documents/GitHub/NPLExperiment for git history (`log`, `show`, `rev-parse`) and for untracked/gitignored data under `data/` (h5 stores, controls ledgers, census, births, watcher state). No repository script was executed; every computation ran from copies in /home/kiros-li/.cache/program-audit/scratchpad/work/agentB-npl-p2/. No `.env`, keystore, session or credential file was opened.

BEFORE (`git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain`, 2026-09-12T12:20Z):
```
```
(empty — clean tree)

AFTER (`git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain`, 2026-09-12T12:47:50Z):
```
```
(empty — clean tree; no modification of any kind)

HEAD at both readings: `dff16632eca6eea05b290ade5464339f44c75744` — **one commit ahead of the anchored SHA 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c**. The extra commit is `dff1663` (2026-09-10, "docs: Amendment H5-3 …"), which touches only progress.md and registrations/H5/REGISTRATION.md; its content is quoted in DRAFT-p2-progress-7.
