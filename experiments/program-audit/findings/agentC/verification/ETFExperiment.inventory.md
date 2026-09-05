# ETFExperiment — LOCATE inventory (Agent C, referee)

**Repository:** ETFExperiment
**Anchored SHA:** `4d110027674e7b4cd2861cf4e0e74f975111daf1` (master, 2026-08-28)
**Snapshot read:** `/home/kiros-li/.cache/program-audit/scratchpad/snap/ETFExperiment/`
**Live repo touched read-only for:** git history and untracked `data/`
**Status of the repository:** CLOSED at `untestable-at-achievable-power`, 2026-08-28,
Amendments 5 and 6, ADR-019 and ADR-020. No outcome value was ever read; both collectors
are disarmed.

This is a LOCATE pass. It establishes **where** each number could be checked and **what**
each closure rests on. It reaches no verdict on any claim; nothing below is a finding.

---

## 1. Artifacts

Counts: **31 tracked** entries (measured artifacts, analysis
code and guard suites) and **9 untracked** entries in the
live working tree. Every raw primitive this repository measured is untracked, because
`.gitignore` excludes `data/` in full; the tracked `reports/*.json` files are summaries computed
from those primitives.

### A1. Tracked (anchored at 4d11002)

**`ETFExperiment/reports/stage_a1/robots_and_terms.json`** — measured artifact (JSON), 2901 B
- Holds: 9 access probes: 8 hosts' robots.txt plus farside /terms-of-use/; url, http_status, byte_count, content_type, requested_at (08:12:19Z-08:12:54Z), body_path, call state
- Backs: docs/ACCESS.md sec.1 'robots.txt sweep across 8 hosts'; farside robots 33 bytes; /terms-of-use/ 404; TheBlock and Glassnode routed OUT on stated prohibitions; 'the first network activity of this repository'

**`ETFExperiment/reports/stage_a1/venue_and_archive.json`** — measured artifact (JSON), 3355 B
- Holds: 8 live probes of Hyperliquid candleSnapshot/fundingHistory/meta, Wayback availability and timemap, Kraken OHLC; byte counts, elapsed, row counts, gated_rows/readable_rows
- Backs: report.md 'the pre-period pin, demonstrated live': 72 readable / 0 gated pre-period vs 0 readable / 72 of 72 gated post-period; ACCESS.md sec.3 and sec.4 probe tables

**`ETFExperiment/reports/stage_a1/rate_ceilings.json`** — measured artifact (JSON), 7195 B
- Holds: 6 endpoints x 2-3 spacing rungs x 6 requests; every status, observed_rate_per_min, elapsed_s, first_refusal_verbatim (all null), highest_verified_clean_rate_per_min, operating_min_spacing_s, finding='no_ceiling_found_at_or_above_floor'
- Backs: report.md 'A.1 Task 2' table and '96 probe requests across 6 endpoints, every one HTTP 200'; REGISTRATION.md Amendment 1 sec.2; ACCESS.md sec.6
- Note: Rung counts sum to exactly 96 (18+18+18+12+12+18). All statuses 200.

**`ETFExperiment/reports/stage_a1/candle_horizon.json`** — measured artifact (JSON array, 9 probes), 1670 B
- Holds: 1h probes at 730/550/400/300/200/100/30 days back and 1d probes at 900/600; row_count and first_open_utc per probe
- Backs: report.md Finding 3 'Probes at 730, 550, 400, 300, 250 and 225 days back returned 0 rows'; the 'n = 17 bisection probes' count (9 here + 8 in the bisect file)

**`ETFExperiment/reports/stage_a1/candle_horizon_bisect.json`** — measured artifact (JSON array, 8 probes), 1525 B
- Holds: 1h probes at 250/225/212/206/203/201 days back and 1d probes at 1200/1000
- Backs: the rolling-window boundary at 2026-02-01T11:00:00Z (the 212-day probe returns 81 rows starting exactly there); the 'n = 17 probes' total

**`ETFExperiment/reports/stage_a1/depth.json`** — measured artifact (JSON array, 5 probes), 1070 B
- Holds: candle_cap_1h row_count 5001 with first_open 2026-02-01T11:00:00Z; candle_cap_1d 2201; three funding pages with gated_rows 0/0/500
- Backs: 'candleSnapshot caps at 5,001 rows'; ACCESS.md sec.3.2 table (1h 5,001 / 1d 2,201); 'a third page from 2025-05-01 gated 500 of 500'

**`ETFExperiment/reports/stage_a1/archive_density.json`** — measured artifact (JSON), 3090 B
- Holds: oos_date_rows 336, oos_days_with_a_printed_signal 333; per page (recent, all_data) and union: total_mementos (346 / 105 / 451), admissible_days (32 / 10 / 37), admissible_share (0.0961 / 0.0300 / 0.1111), capture_too_late_days (45 / 19 / 53), no_capture_days (256 / 304 / 243), and the explicit admissible date lists
- Backs: REGISTRATION.md Amendment 1 sec.3(b) '37 of 333 ... share 0.1111'; the 53 / 243 exclusion counts carried into the census; '676 date rows ... 336 ... 333'
- Note: This file still holds the FALSIFIED 0.1111 timemap-only figure; the corrected 11/333 lives only in retro_revision.json. No artifact stores the corrected density as a share.

**`ETFExperiment/reports/stage_a1/retro_revision.json`** — measured artifact (JSON, 37 rows), 14715 B
- Holds: one row per archive-admissible day: archive_url, archive_captured_at, http_status, byte_count, state (stored 11 / no_data 25 / source_failed 1), as_printed_usd, current_usd, delta_usd, delta_share, revised, sign_flipped, threshold_crossed, positions; summary keys comparable_days 11, intact_days 11, revised_days 0, sign_flip_days 0, threshold_cross_days 0, registered_minimum_sample 30, meets_registered_minimum false
- Backs: THE deciding artifact: archive capture density 11 of 333 = 0.0330 (GO closed); the retro revision rate 0/11; the 8-day retro cohort; the +04:05 to +08:00 served-value capture-time range and the -03:38 to +04:29 dashed range
- Note: as_printed_absent='dash_in_cell' on 23 rows; the other 2 no_data rows carry no row for the day. 11 + 23 + 2 + 1 = 37.

**`ETFExperiment/reports/stage_a2/census.json`** — measured artifact (JSON), 2430 B
- Holds: rows 336, admissible 11 (retro_archive 11, forward_capture 0), revised_flagged 0, operational_unknown 1, exclusion_reasons {capture_too_late 53, no_capture 243, capture_served_no_value 25, no_printed_value 3, archive_fetch_failed 1}, by_month table, and two labelled signal distributions (admissible n=11 median 86.8M trade_share 0.7273; live descriptive n=333 median 27.4M trade_share 0.7568, 138 long / 114 short / 81 flat)
- Backs: README.md line 37 census row; REGISTRATION.md Amendment 3; report.md A.2 census table; the 0.7568 trade share that feeds every E2 power number

**`ETFExperiment/reports/stage_a2/preperiod_inputs.json`** — measured artifact (JSON), 500 B
- Holds: daily_sd 0.027430504889517645 on n_volatility_returns 475 (first_close_ms 2024-01-11, last_close_ms 2025-04-30T23:59:59.999Z); mean_hourly_funding_rate 2.2264894449794276e-05 on n_funding_hours 11423 across funding_pages 23; daily_funding_sum 0.0005343574667950626; annualized_funding_pct 19.504047538019787; carve_out_boundary_ms 1746057600000
- Backs: report.md 'daily log-return sd 0.027431 (n = 475 returns) ... mean hourly funding 0.00002226 (n = 11,423 hours, 23 pages), a 24-hour hold sum of 0.000534 and 19.5 percent per year'; every E2 power figure
- Note: The 23 pre-period funding pages and the pre-period 1d candle payload were NEVER written to disk (scripts/preperiod_inputs.py writes only the summary). These figures are unanchored at the primitive level: irreproducible without refetching the venue.

**`ETFExperiment/reports/stage_a2/power.json`** — measured artifact (JSON), 2551 B
- Holds: alpha_adj 0.025320565519103666, target_power 0.8, permutation_draws 20000, power_simulations 2000, three assumptions, scenarios {achieved_total 11, achieved_forward_only 0, forward_only_by_interim 88, forward_only_by_deadline 152, all_cohorts_by_deadline 163}, printed_day_rate 0.9910714285714286, weekdays_to_interim 89, weekdays_to_deadline 153, economic_inputs, powers grid (E1 and E2 at each scenario x assumption), minimum_n_for_e1 {0.18:237, 0.09:845, 0.045:3776}
- Backs: the whole Amendment 3 power table; E1 0.6105 at N=163 (the figure that stopped BLOCKED); the 237/845/3776 minimums; the projected N = 163
- Note: No field records the '20.8 admissible days per month' accrual rate. N=163 comes from 11 + round(153 weekdays x 333/336).

**`ETFExperiment/reports/stage_a2/e2_minimum_n.json`** — measured artifact (JSON), 446 B
- Holds: target 0.8; grid published_0.18 {200:0.6767, 250:0.7100, 300:0.8000} (loop breaks at 300) and registered_0.09 {200:0.2133, 250:0.2133, 300:0.3100, 350:0.3567, 400:0.3433, 600:0.4867, 900:0.7200, 1200:0.7467}
- Backs: Amendment 4's governing minimum N = 300; the 'above 1,200' at the registered assumption; the non-monotonicity 0.3567 at n=350 against 0.3433 at n=400
- Note: The file records neither the draw count nor the simulation count; the 1,200 draws / 300 sims figure is only in scripts/e2_minimum.py line 42.

**`ETFExperiment/reports/stage_a2/substrate_coverage.json`** — measured artifact (JSON, 333 per-day rows), 99115 B
- Holds: days_covered_at_registered_bars 142, hourly_rows_sealed 5002, funding_hours_sealed 5002, funding_pages_sealed 11, hourly_window_start 2026-02-01T11:00:00Z, min_outcome_coverage 0.95/0.95, and per_day {trade_date, span_start, span_end, expected_hours 48, candle_hours, candle_coverage, funding_hours, funding_coverage, covered}
- Backs: '142 of 333 out-of-sample trading days are covered at the registered 0.95/0.95 bars'; the 48-hour span from D+1 00:00Z; 'roughly 190 of 333 days already have no registered outcome' (189 of the 333 rows are dated before 2026-02-01)
- Note: Counts rows and hours only; it holds no price.

**`ETFExperiment/reports/stage_a4/mutations.log`** — measured artifact (text, 6 lines), 1201 B
- Holds: one line per registered mutation: caught=True restored_green=True plus the failure it would have caused
- Backs: report.md Stage A.4 table 'All six registered mutations were applied to real source, each caught, source restored green'
- Note: Records only the outcome, not the diff applied or the failing test id.

**`ETFExperiment/tests/fixtures/farside-recent.html`** — test fixture (HTML), 267010 B
- Holds: a 267,010-byte capture of https://farside.co.uk/btc/
- Backs: the parser tests; the byte count quoted in ACCESS.md sec.2.1

**`ETFExperiment/src/etf/power.py`** — analysis code, 8828 B
- Holds: spearman / spearman_from_ranks, pearson_for_spearman (Gaussian copula inversion), e1_critical_value, e1_power (default draws=20000, simulations=2000, seed=20260828), EconomicInputs, e2_power (default draws=2000, simulations=400), _two_sided_cut, _inverse_normal_cdf (Acklam), minimum_n (binary search, draws=4000, simulations=600)
- Backs: every power figure: 0.6105, 0.5225, 0.2015, 0.1700, and the minimums 237 / 845 / 3776
- Note: minimum_n runs at 4,000 draws and 600 simulations - neither of the two budgets the documents attribute to it (20,000/2,000 in report.md line 329; 1,200 draws/300 sims in REGISTRATION.md line 1011). It also bisects a simulated (noisy) power curve.

**`ETFExperiment/scripts/power_gate.py`** — analysis code, 5514 B
- Holds: builds the scenarios from census.json + preperiod_inputs.json; trading_days_between counts calendar weekdays; printed_rate = 333/336 hardcoded at line 71; writes power.json
- Backs: N = 163, N = 152, N = 88, and therefore the deadline finding
- Note: The 'measured forward accrual' is a calendar weekday count scaled by the printed-day rate. No forward admissible day existed when it ran (census admissible_forward_capture = 0).

**`ETFExperiment/scripts/e2_minimum.py`** — analysis code, 2065 B
- Holds: E2 power over the grid (200, 250, 300, 350, 400, 600, 900, 1200) at draws=1200, simulations=300, breaking at the first cell >= 0.80
- Backs: the governing minimum N = 300 and the 'above 1,200'

**`ETFExperiment/src/etf/archive.py`** — analysis code, 4582 B
- Holds: parse_timemap (RFC 7089 link-format), qualifying_window(D) = [D 20:00Z, anchor on D+1), density() with capture_too_late bounded to the day after the anchor
- Backs: the archive density figures and the 53 / 243 split
- Note: qualifying_window's LOWER bound (20:00Z on D) comes from CONFIG.snapshot_peak_start_hour_utc, a Section 12 cadence constant. Section 3.3 of the registration states only 'strictly before the entry anchor'.

**`ETFExperiment/scripts/archive_density.py`** — analysis code, 4785 B
- Holds: fetches both timemaps, computes per-page and union density against the printed-value universe, writes archive_density.json
- Backs: the 37 / 0.1111 figure and the memento counts

**`ETFExperiment/scripts/retro_revision.py`** — analysis code, 7117 B
- Holds: fetches the LAST qualifying pre-anchor memento per admissible day, parses the as-printed aggregate, compares to the live value, writes retro_revision.json and the bodies
- Backs: 11 of 333, 0 revised, 0 sign flips, 0 threshold crosses

**`ETFExperiment/scripts/census.py`** — analysis code, 8385 B
- Holds: builds the 336-row census from the live all-data page, both timemaps, the snapshot ledger and retro_revision.json; computes both signal distributions
- Backs: census.json in full, including the 0.7568 trade share

**`ETFExperiment/scripts/preperiod_inputs.py`** — analysis code, 4805 B
- Holds: one 1d candleSnapshot request ending at pre_period_end_ms - 1, then paged fundingHistory; asserts is_pre_period on every row; writes only the summary
- Backs: daily sd 0.027431 and mean hourly funding 0.00002226

**`ETFExperiment/src/etf/section0.py`** — analysis code, 7840 B
- Holds: fire_section0: three BLOCKED triggers first (observability FAIL, unstable share > 0.50, E1 published < 0.50), then GO, then the DEGRADED residual
- Backs: the Section 0 map as registered
- Note: Never called outside tests/test_section0.py. No section0 verdict artifact exists; the Amendment 3 verdict was written in prose.

**`ETFExperiment/src/etf/observability.py`** — analysis code, 4433 B
- Holds: fire_observability: PASS/PARTIAL/FAIL from the density share against 0.60 and the intact share against 0.90
- Backs: the 'PASS is closed; the verdict is PARTIAL or FAIL' claim
- Note: Never called outside tests/test_observability.py. No observability verdict artifact exists.

**`ETFExperiment/src/etf/config.py`** — analysis code (frozen registered constants), 8464 B
- Holds: ALPHA_ADJ, PRE_PERIOD_END_MS, and CONFIG with the bars: archive_density_pass_share 0.60, revision_intact_pass_share 0.90, retro_revision_sample_min 30, power_go_floor 0.80, power_blocked_floor 0.50, rho 0.09/0.18/0.045, permutation_draws 20000, power_simulations 2000, entry_anchor_hour_utc 8, signal_threshold_usd 1e8, hyperliquid_round_trip_bp (3,9,18), interim_deadline 2026-12-31, projection_deadline 2027-03-31, lag_min_trading_days 15, assistant_prior_edge 0.10
- Backs: every registered bar quoted anywhere in the documents

**`ETFExperiment/src/etf/verdict.py`** — analysis code (dark), 8515 B
- Holds: E1, E2 and the named secondaries; refuse_sealed_path raises on data/outcomes, data/funding, data/retro, data/census
- Backs: 'verdict.py is built dark, refuses sealed paths in code, and is imported by nothing'

**`ETFExperiment/src/etf/costs.py`** — analysis code, 1958 B
- Holds: hyperliquid_band (3/9/18 bp), kraken band, ibkr_band returning None
- Backs: the 9 bp central round trip used by every E2 power number; 'IBKR carries no band'

**`ETFExperiment/src/etf/registration_check.py`** — analysis code, 3055 B
- Holds: parses REGISTRATION.md Section 13 for a probability followed by (independent) or (adopted); raises OperatorPriorMissing otherwise
- Backs: 'the empty slot blocks Stage B structurally'

**`ETFExperiment/src/etf/preperiod.py + src/etf/preperiod_prices.py`** — analysis code, 7598 B
- Holds: require_pre_period / gate_pre_period at CONFIG.pre_period_end_ms; the only module that reads a close, refusing the whole payload if one row crosses the boundary
- Backs: the pre-period carve-out claims and the 'no BTC price parsed outside the carve-out' claim

**`ETFExperiment/tests/test_guards.py`** — structural guard suite, 12866 B
- Holds: parse-tree guards: every Config field must be read outside config.py; no module may read a priced candle field; the funding reader must route through gate_pre_period; only preperiod_prices.py may read the boundary
- Backs: the five standing guards and the blindness claims

### A2. Untracked — live working tree only (UNANCHORED, read 2026-09-05T03:46Z to 03:49Z)

Everything under `data/` is gitignored (`.gitignore` line 2). None of it is in the anchored snapshot. It may have changed after the anchor; where it did, the change is noted.

**`ETFExperiment/data/access/ (36 files, 3.4 MB)`** — untracked raw primitives, mtime 2026-08-28 01:12 to 13:14 local
- Holds: farside-btc-all.html 794,472 B (mtime 2026-08-28 12:55 local, requested_at 19:54:47Z), farside-btc.html 267,010 B, farside_all_parsed.json 79,245 B (header + 676 rows, last row '28 Aug 2026' all-dash with Total '0.0'), sosovalue-btc.html 1,086,812 B, theblock-btc.html 735,287 B, glassnode-charts.html, timemap-recent.txt 45,231 B, timemap-all_data.txt 16,300 B, 6 robots.txt bodies, hl-*.json probes, kraken_ohlc.txt, and .meta.json sidecars carrying requested_at / http_status / byte_count / server
- Backs: 676 / 336 / 333; the archive density and every memento-derived figure; the SoSoValue cross-check; the Total-column hazard
- Note: UNANCHORED. The only route to recomputing 0.316 mementos/day, 48.37% in-window and the unbounded-window 112 of 333, none of which is stored in any artifact.

**`ETFExperiment/data/archive_bodies/ (36 files, 8.7 MB)`** — untracked raw primitives, mtime 2026-08-28 13:22 to 13:32 local
- Holds: one archived Wayback capture per admissible day, named <trade_date>-<capture stamp>.html, 2025-05-02 through 2026-08-26; 36 bodies for 37 admissible days (the HTTP 403 day has none)
- Backs: the 11-served / 23-dashed / 2-no-row split, and every as_printed_usd in retro_revision.json
- Note: UNANCHORED but self-describing: each body carries its own capture timestamp in the filename and its Wayback URL in retro_revision.json.

**`ETFExperiment/data/census/census.jsonl`** — untracked append-only ledger, 79033 B, mtime 2026-08-28 13:34 local
- Holds: 336 rows, one per out-of-sample date row: trade_date, state, admissible, exclusion_reason, source, capture_timestamp, printed_signal_present, revised, census_run_at 2026-08-28T20:34:47Z
- Backs: the census counts in census.json, day by day

**`ETFExperiment/data/ledgers/requests.jsonl`** — untracked append-only ledger, 61572 B, mtime 2026-08-28 19:40 local
- Holds: 476 lines = 238 charge rows + 238 settle rows, 2026-08-28T08:12:19Z to 2026-08-29T02:40:32Z; settle statuses 231 x 200, 5 x 404, 1 x 401, 1 x 403; charges by source venue 108 / archive 79 / flow 51
- Backs: '220 charged requests ... 33 flow, 79 archive, 108 venue' and 'the request ledger (143 charged requests)' at Amendment 1
- Note: Charge #143 lands at 20:12:49Z and charge #220 at 20:40:46Z with the split exactly 33/79/108; the ledger then continues to 238 charges by the disarm. The lifetime figure in Amendment 6 is a snapshot taken ~6 hours before that amendment was committed.

**`ETFExperiment/data/snapshots/flow_snapshots.jsonl + data/snapshots/bodies/ (20 files, 5.3 MB)`** — untracked append-only ledger + bodies, 69896 B, mtime 2026-08-28 19:40 local
- Holds: 20 capture rows, 2026-08-28T20:17:11Z to 2026-08-29T02:40:32Z, each with 15 day rows, sha256, byte_count, body_path; every row shows 2026-08-28 with signal_usd null and 2026-08-27 at 218,200,000
- Backs: 'the snapshotter was armed 2026-08-28T20:17:11Z'; 'the first capture recorded the open day as Absent(dash_in_cell)'; progress.md Entry 6's '2 captures exist'; census admissible_forward_capture = 0
- Note: 20 captures exist now, not 2; progress.md Entry 6 was written at 20:46Z when 2 existed. No capture ever served a value for 2026-08-28, so forward-capture 0 stands.

**`ETFExperiment/data/outcomes/btc-1h-servable-window.json`** — untracked sealed store, 695926 B, mtime 2026-08-28 13:19 local
- Holds: 5,002 hourly BTC perp candles, first open 1769943600000 (2026-02-01T11:00:00Z), last close 1787950799999 (2026-08-28T19:59:59.999Z); raw venue rows including o/h/l/c/v
- Backs: '5,002 hourly candle rows ... sealed as raw bytes'; substrate_coverage.json's candle_hours
- Note: This is the sealed outcome substrate. It was never opened by the repository (no Stage B latch exists under data/state/).

**`ETFExperiment/data/funding/ (11 files, 468 KB)`** — untracked sealed store, mtime 2026-08-28 13:19-13:20 local
- Holds: 11 fundingHistory pages, 5,002 rows in total, covering the same window
- Backs: '11 funding pages covering 5,002 hours'

**`ETFExperiment/data/state/`** — absent
- Holds: the Stage B latch path (STAGE_B_LATCH = data/state/stage_b_read.json) does not exist
- Backs: 'the latch was never spent'; 'Stage B ... Not written'
- Note: Directory absent from the live data/ tree at read time - consistent with the claim.

**`ETFExperiment/_CLOSED_DO_NOT_RUN_HERE`** — untracked owner marker (not mine), 747 B, mtime 2026-09-02 22:38 local
- Holds: a 747-byte marker written 2026-09-02 telling agents the repository is closed; excluded via .git/info/exclude line 7 so it does not dirty the tree
- Backs: nothing numeric; recorded here because it is the only untracked file outside data/
- Note: Pre-existing, owner-written, self-documenting. Not created by this audit.


### A3. What is NOT stored anywhere

These figures appear in the documents and in no artifact and in no committed code path:

| figure | where it is asserted | only route to it |
|---|---|---|
| **20.8 admissible days per month** (the accrual rate the closure turns on) | REGISTRATION.md:982, :1129; report.md:360, :447, :506; HYPOTHESES.md:70, :82, :84; progress.md:493, :533, :581; DECISIONS.md:555, :596 | reconstruct from `scripts/power_gate.py` (calendar weekdays × 333/336) or from Amendment 6's 291-in-14-months |
| **0.316 mementos per calendar day**, **48.37 % in-window**, **112 of 333 (0.3363)** unbounded | docs/ACCESS.md:380-385; REGISTRATION.md:676-680, :1062-1064; report.md:190-194, :438-442; HYPOTHESES.md:80, :84; README.md:32 | recompute from untracked `data/access/timemap-*.txt` |
| **315 of 333 within 2 %**, mean difference **47.42M** | docs/ACCESS.md:172-181; REGISTRATION.md:620-624; report.md:69-71; README.md:29 | recompute from untracked `data/access/sosovalue-btc.html` + `farside_all_parsed.json` |
| the **Section 0 verdict object** (GO eliminated, BLOCKED not fired) | REGISTRATION.md Amendment 3 sec.2; report.md:340-352 | `etf.section0.fire_section0` exists and is pinned by tests but is **called by nothing outside `tests/test_section0.py`**; the verdict was written in prose |
| the **as-printed observability verdict** (PASS closed, PARTIAL-or-FAIL) | report.md:250-254; docs/ACCESS.md:432-436 | `etf.observability.fire_observability` likewise called only from its test |
| the **pre-period candle and funding payloads** (n = 475 returns, n = 11,423 hours) | reports/stage_a2/preperiod_inputs.json summary only | irrecoverable without refetching the venue; `scripts/preperiod_inputs.py` writes no bodies |
| the **retro cohort intersection** (8 days) | REGISTRATION.md:742-745 | stated in prose; no script computes it |

---

## 2. Numeric claims, ranked

30 claims extracted. Ranked by how much rests on them: a closure's deciding number first.
**8 are marked MUST-VERIFY** (the brief requires at
least three).

The dependency spine of the closure, in one line:

```
676 date rows -> 336 out-of-sample -> 333 printed
   |-> 37 timemap-admissible -> 11 served a value -> density 0.0330 vs 0.60  => GO closed
   |-> census 336 rows, 11 admissible, trade share 0.7568 (n=333, descriptive)
   |-> pre-period sd 0.027431 + funding 0.000534 -> E2 power
   |-> weekdays-to-deadline 153 x 333/336 + 11 = N 163
   |-> E1 power 0.6105 at N=163 (BLOCKED floor 0.50 cleared)
   |-> E1 min N 237, E2 min N 300 -> governing 300 -> shortfall 137 (or 74)
   => CLOSED untestable-at-achievable-power
```

#### 1. `ETF-C01` — **MUST-VERIFY**

> GO requires the as-printed observability test of A.1 Task 4 to pass **in full**. Its archive-capture-density leg is measured at **11 of 333 = 0.0330 against the registered 0.60 bar** (Amendment 2), short by a factor of 18. **No subsequent measurement can restore it**, because the archive captures that would be needed do not exist and cannot be created. **GO is closed.**

- **Where:** `ETFExperiment/REGISTRATION.md:863-867`
- **Figures:** 11 / 333 = 0.0330 against a 0.60 bar; short by a factor of 18
- **n:** 333 printed out-of-sample trading days; 37 archive-admissible by timemap; 11 served a value
- **Backing artifact:** reports/stage_a1/retro_revision.json (comparable_days 11, archive_admissible_days 37); reports/stage_a1/archive_density.json (n_trading_days 333, union admissible_days 37)
- **Backing code:** src/etf/archive.py density()+qualifying_window(); scripts/retro_revision.py; src/etf/observability.py fire_observability (never invoked outside tests)
- **Notes:** This is the closure's irreversible leg. Also stated at report.md:187-188, report.md:438-443, HYPOTHESES.md:79, README.md:32, progress.md:443, docs/ACCESS.md:361-362. Verify: the 11 served days, the 333 denominator, and whether the 20:00Z lower window bound is registered for admissibility (Section 3.3 states only 'strictly before the entry anchor').

#### 2. `ETF-C02` — **MUST-VERIFY**

> **At the measured forward accrual rate of 20.8 admissible days per month:** projected achieved N at the registered deadline of **2027-03-31: 163**; **achieved N = 300 arrives around 2027-10-26 - roughly seven months past the registered deadline**

- **Where:** `ETFExperiment/REGISTRATION.md:981-986`
- **Figures:** 20.8 admissible days per month; N = 163 at 2027-03-31; N = 300 around 2027-10-26
- **n:** 163 = 11 achieved + round(153 weekdays x 333/336); forward-capture admissible days = 0
- **Backing artifact:** reports/stage_a2/power.json (scenarios.all_cohorts_by_deadline 163, weekdays_to_deadline 153, printed_day_rate 0.9910714285714286); reports/stage_a2/census.json (admissible_forward_capture 0)
- **Backing code:** scripts/power_gate.py lines 29-43 (trading_days_between counts calendar weekdays) and lines 69-81 (printed_rate = 333/336 hardcoded)
- **Notes:** MUST-VERIFY, highest priority after C01: the closure's deciding arithmetic. The phrase 'measured forward accrual' appears at REGISTRATION.md:982, :1129, report.md:360, :447, :506, HYPOTHESES.md:70, :82, :84, progress.md:493, :533, :581, DECISIONS.md:555, :596. The figure 20.8 appears in NO artifact and in NO line of code; 21 weekdays/month x 333/336 = 20.81. The repository's own forward accrual measured 0 admissible days in 20 captures.

#### 3. `ETF-C03` — **MUST-VERIFY**

> **The governing minimum N is therefore 300, not 237.** ... | minimum N at the published 0.18 | 237 | 300 | **300** |

- **Where:** `ETFExperiment/REGISTRATION.md:974-978`
- **Figures:** E2 minimum N 300 at published 0.18 (power exactly 0.8000); E1 minimum N 237; governing 300; shortfall 137 days, or 74 days against E1's 237
- **n:** E2 grid at 1,200 draws and 300 simulations per cell; E1 minimum from a bisection at 4,000 draws and 600 simulations
- **Backing artifact:** reports/stage_a2/e2_minimum_n.json (published_0.18: 200 0.6767, 250 0.7100, 300 0.8000); reports/stage_a2/power.json (minimum_n_for_e1.published_0.18 = 237)
- **Backing code:** scripts/e2_minimum.py line 42 (draws=1200, simulations=300, break at first cell >= 0.80); src/etf/power.py minimum_n lines 225-252 (draws=4000, simulations=600, binary search)
- **Notes:** MUST-VERIFY. REGISTRATION.md:1011 attributes E1's 237 to '1,200 draws, 300 sims/cell', which is E2's budget; report.md:329-330 attributes E1 to '20,000 permutation draws and 2,000 simulations', which is the power-table budget. The code says 4,000/600. Also verify that bisecting a noisy simulated power curve returns a well-defined minimum.

#### 4. `ETF-C04` — **MUST-VERIFY**

> **BLOCKED does not fire on power.** Its power trigger is E1 under 0.50 at the published-magnitude assumption at the achievable count by 2027-03-31. Measured: **0.6105**. The trigger is not met.

- **Where:** `ETFExperiment/REGISTRATION.md:869-871`
- **Figures:** E1 power 0.6105 at rho 0.18 and N = 163, against the registered 0.50 BLOCKED floor
- **n:** N = 163; 20,000 permutation draws; 2,000 power simulations; seed 20260828
- **Backing artifact:** reports/stage_a2/power.json powers.all_cohorts_by_deadline.published_0.18.e1 = 0.6105
- **Backing code:** src/etf/power.py e1_power / e1_critical_value; scripts/power_gate.py; src/etf/section0.py fire_section0 (the trigger it would have fired)
- **Notes:** MUST-VERIFY: recomputable exactly - the RNG is stdlib random.Random with a fixed seed and zero third-party dependencies, so the figure should reproduce bit-for-bit. Also stated at report.md:327, :348, HYPOTHESES.md:79, progress.md:445.

#### 5. `ETF-C05` — **MUST-VERIFY**

> | days revised | **0 of 11** | | sign flips | **0 of 11** | | threshold crosses | **0 of 11** | | intact | **11 of 11** | ... **This is below the registered minimum sample of 30** ... **The retro revision leg does not meet its registered minimum and cannot carry a verdict.**

- **Where:** `ETFExperiment/REGISTRATION.md:756-769`
- **Figures:** 0 revised, 0 sign flips, 0 threshold crosses, 11 of 11 intact; registered minimum 30
- **n:** n = 11 comparable days
- **Backing artifact:** reports/stage_a1/retro_revision.json (revised_days 0, sign_flip_days 0, threshold_cross_days 0, intact_days 11, meets_registered_minimum false)
- **Backing code:** scripts/retro_revision.py lines 108-124 (revised = delta != 0.0; threshold_crossed compares positions); src/etf/signal.py position()
- **Notes:** MUST-VERIFY: this is the figure the record repeatedly declines to promote, and the non-promotion is a load-bearing process claim. Verify the 11 deltas are genuinely zero and that 'revised' is not defined so loosely it cannot fire.

#### 6. `ETF-C06` — **MUST-VERIFY**

> **Census: 336 rows, 11 admissible.** ... | **admissible** (all retro-archive; forward-capture 0) | **11** | | excluded - capture too late | 53 | | excluded - no capture | 243 | | excluded - capture served no value | 25 | | excluded - no printed value | 3 | | **operational - archive fetch failed, admissibility unknown** | **1** |

- **Where:** `ETFExperiment/report.md:260-269`
- **Figures:** 336 rows; 11 admissible; 53 + 243 + 25 + 3 + 1 = 325 excluded/operational
- **n:** 336 out-of-sample date rows of which 333 print a value
- **Backing artifact:** reports/stage_a2/census.json; data/census/census.jsonl (336 rows, untracked); reports/stage_a1/archive_density.json (37 = 11 + 25 + 1)
- **Backing code:** scripts/census.py; src/etf/census.py build_census
- **Notes:** MUST-VERIFY the reconciliation: 11 + 325 = 336; 37 timemap-admissible = 11 served + 25 served-no-value + 1 fetch-failed; 333 printed + 3 no-printed-value = 336. Also README.md:37, HYPOTHESES.md:80.

#### 7. `ETF-C07` — **MUST-VERIFY**

> The archive crawls the flow pages **0.316 times per calendar day** (n = 153 out-of-sample mementos over 484 calendar days). **48.37 percent of those mementos already fall inside the registered 20:00-08:00 UTC window** ... and an **unbounded** window admitting any capture on D or D+1 would reach only **112 of 333 (33.63 percent)**

- **Where:** `ETFExperiment/docs/ACCESS.md:380-385`
- **Figures:** 0.316 mementos/calendar day; 48.37% in-window; 112 of 333 = 0.3363 unbounded ceiling
- **n:** n = 153 out-of-sample mementos; 484 calendar days; 333 trading days
- **Backing artifact:** NONE. No artifact under reports/ stores 153, 484, 48.37% or 112. Recomputable only from data/access/timemap-recent.txt + timemap-all_data.txt (untracked, 451 mementos total)
- **Backing code:** src/etf/archive.py parse_timemap + qualifying_window; no script computes these three figures
- **Notes:** MUST-VERIFY. This is the argument that 'widening the window is foreclosed as an explanation' - i.e. that the density failure is the archive's fault and not the registration's. It is carried into the reopen threshold (b) at HYPOTHESES.md:84 and into ADR-019's consequences (DECISIONS.md:568-570). It rests entirely on unanchored data.

#### 8. `ETF-C08`

> **Amendment 1 recorded an archive capture density of 37 of 333 (0.1111).** That figure was computed from the timemap alone, and it counted **captures**, not **served values**. ... **a figure that was not measured end-to-end entered a record, and measurement moved it by a factor of 3.4.**

- **Where:** `ETFExperiment/REGISTRATION.md:713-735`
- **Figures:** 0.1111 falsified to 0.0330; factor of 3.4
- **n:** 37 timemap-admissible days; 11 served
- **Backing artifact:** reports/stage_a1/archive_density.json (union admissible_share 0.1111111111111111) vs reports/stage_a1/retro_revision.json (comparable_days 11)
- **Backing code:** scripts/archive_density.py vs scripts/retro_revision.py
- **Notes:** 0.1111/0.0330 = 3.367. Both figures survive in artifacts; the falsified one is the only density share any artifact stores.

#### 9. `ETF-C09`

> Amendment 4's E2 power at n = 300 reads exactly 0.8000 from 300 simulations. Binomial standard error on a 0.80 estimate at 300 draws is **0.0231**, so an estimate landing precisely on its bar has roughly even odds of sitting below it, and the true E2 minimum could be 350 or 400.

- **Where:** `ETFExperiment/REGISTRATION.md:1017-1021`
- **Figures:** 0.8000; SE 0.0231; candidate true minimum 350 or 400
- **n:** 300 simulations per cell
- **Backing artifact:** reports/stage_a2/e2_minimum_n.json grid.published_0.18['300'] = 0.8
- **Backing code:** scripts/e2_minimum.py (simulations=300)
- **Notes:** sqrt(0.8*0.2/300) = 0.02309. Disclosed by the authors as an open caveat (REGISTRATION.md:1024-1025, DECISIONS.md:537-547, HYPOTHESES.md:84).

#### 10. `ETF-C10`

> **The sealed substrate.** 5,002 hourly candle rows (2026-02-01T11:00Z onward) and 11 funding pages covering 5,002 hours, sealed as raw bytes. **142 of 333 out-of-sample trading days are covered at the registered 0.95/0.95 bars.**

- **Where:** `ETFExperiment/report.md:288-290`
- **Figures:** 5,002 hourly rows; 11 funding pages; 142 of 333 days covered
- **n:** 333 out-of-sample printed trading days; 48 expected hours per day
- **Backing artifact:** reports/stage_a2/substrate_coverage.json (days_covered_at_registered_bars 142, hourly_rows_sealed 5002, funding_pages_sealed 11); data/outcomes/btc-1h-servable-window.json (5,002 rows, untracked); data/funding/ (11 pages, 5,002 rows, untracked)
- **Backing code:** src/etf/recorder.py; scripts/seal_substrate.py
- **Notes:** Reconfirmed by direct count of the untracked files at read time. Note the 5,001-vs-5,002 tension with depth.json's measured cap of 5,001 rows.

#### 11. `ETF-C11`

> **Pre-period carve-out inputs**, strictly before 2025-05-01: daily log-return sd **0.027431** (n = 475 returns, 2024-01-11 to 2025-04-30); mean hourly funding **0.00002226** (n = 11,423 hours, 23 pages), a 24-hour hold sum of **0.000534** and **19.5 percent per year**.

- **Where:** `ETFExperiment/report.md:296-299`
- **Figures:** sd 0.027431; mean hourly funding 2.2265e-05; 24h sum 0.000534; 19.504%/yr
- **n:** n = 475 daily returns; n = 11,423 funding hours across 23 pages
- **Backing artifact:** reports/stage_a2/preperiod_inputs.json
- **Backing code:** src/etf/preperiod_prices.py daily_volatility (statistics.stdev of log returns); scripts/preperiod_inputs.py
- **Notes:** The primitives were never written to disk. Only the summary is anchored; the underlying candle and funding payloads are irrecoverable without refetching. 2024-01-11 to 2025-04-30 inclusive is 476 daily candles, giving 475 returns.

#### 12. `ETF-C12`

> **No ceiling was found on any endpoint at or above this repository's own absolute floor of 1.0 s: 96 probe requests across 6 endpoints, every one HTTP 200.** ... Paces are set at **twice the fastest verified-clean spacing** - half the highest verified-clean *rate*, because there is no ceiling to halve.

- **Where:** `ETFExperiment/report.md:137-152`
- **Figures:** 96 probes, all 200; flow.table 12.17/min -> 10.0 s; archive.availability 59.92 -> 2.0 s; archive.timemap 21.28 -> 2.0 s; venue.candleSnapshot 59.90 -> 2.0 s; venue.fundingHistory 59.91 -> 2.0 s; kraken.ohlc 58.73 -> 2.0 s
- **n:** 6 endpoints x 6 requests per rung; n = 18, 18, 18, 12, 12, 18
- **Backing artifact:** reports/stage_a1/rate_ceilings.json
- **Backing code:** scripts/rate_ceiling.py; src/etf/pacing.py
- **Notes:** Rungs sum to exactly 96 and every status is 200. For archive.timemap the two stated rules disagree: twice the fastest clean spacing is 2.0 s, but half the highest verified-clean rate (21.28/min, achieved at the 2.0 s rung) is 10.64/min = 5.6 s.

#### 13. `ETF-C13`

> `candleSnapshot` caps at **5,001 rows** (n = 17 bisection probes). At `1h` that reaches back only to **2026-02-01T11:00:00Z** and **slides forward one hour per hour** - 5,001 hours is 208.4 days, and the served start matches to the hour. Probes at 730, 550, 400, 300, 250 and 225 days back returned **0 rows**.

- **Where:** `ETFExperiment/report.md:108-111`
- **Figures:** 5,001-row cap; window start 2026-02-01T11:00:00Z; 208.4 days
- **n:** n = 17 probes (9 in candle_horizon.json + 8 in candle_horizon_bisect.json)
- **Backing artifact:** reports/stage_a1/depth.json (candle_cap_1h row_count 5001, first_open 2026-02-01T11:00Z); reports/stage_a1/candle_horizon.json; reports/stage_a1/candle_horizon_bisect.json
- **Backing code:** scripts/candle_horizon.py; scripts/depth_probe.py; src/etf/blindness.py candle_times
- **Notes:** The six zero-row probes named in the text are exactly the six in the artifacts. 5001/24 = 208.375 days.

#### 14. `ETF-C14`

> **676 date rows** 2024-01-11 -> 2026-08-28, **336 on or after 2025-05-01**, of which **333 print a value**. ... **The `Total` column prints `0.0` on a day where every per-fund cell is a dash: 3 of 3 such rows over n = 336.**

- **Where:** `ETFExperiment/report.md:64, 91-92`
- **Figures:** 676 date rows; 336 out-of-sample; 333 printed; 3 of 3 all-dash rows print Total 0.0
- **n:** n = 336 out-of-sample rows
- **Backing artifact:** reports/stage_a1/archive_density.json (oos_date_rows 336, oos_days_with_a_printed_signal 333); data/access/farside_all_parsed.json (676 rows, untracked - confirmed at read time, last row '28 Aug 2026' all dashes with Total '0.0')
- **Backing code:** src/etf/snapshot.py parse_flow_table; src/etf/flow.py aggregate/parse_cell; src/etf/table.py
- **Notes:** docs/ACCESS.md:137-141 names the three days: 26 May 2025, 19 Jun 2025, 28 Aug 2026.

#### 15. `ETF-C15` — **MUST-VERIFY**

> **The cross-check itself passes: 315 of 333 out-of-sample days agree within 2 percent** between Farside's all-fund `Total` and SoSoValue's `totalNetInflow` (n = 333). ... the registered five-fund aggregate differs from the all-fund total by a mean of **47.42M USD (median 27.20M, range -903.20M to +1,205.20M, n = 333)**

- **Where:** `ETFExperiment/docs/ACCESS.md:172-181`
- **Figures:** 315 of 333 within 2%; mean difference 47.42M, median 27.20M, range -903.20M to +1,205.20M
- **n:** n = 333 overlapping out-of-sample days
- **Backing artifact:** NONE under reports/. Recomputable only from data/access/sosovalue-btc.html (1,086,812 B, untracked) and data/access/farside_all_parsed.json (untracked)
- **Backing code:** no script in scripts/ computes the cross-check; no module names sosovalue
- **Notes:** MUST-VERIFY: this figure is called 'the strongest available evidence that the served flow surface is not idiosyncratic to one publisher' (ACCESS.md:183-185) and is repeated at README.md:29, REGISTRATION.md:624, report.md:69-71 and HYPOTHESES.md:80. It is entirely unanchored and produced by no committed code path.

#### 16. `ETF-C16`

> Live descriptive (n = 333, **not admissible**, labelled): median 27.4M, 138 long, 114 short, 81 flat, **trade share 0.7568** - the figure E2's power computation uses, with its n and its label attached.

- **Where:** `ETFExperiment/report.md:284-287`
- **Figures:** trade share 0.7568 (n = 333); admissible trade share 0.7273 (n = 11); medians 27.4M / 86.8M
- **n:** n = 333 live descriptive; n = 11 admissible
- **Backing artifact:** reports/stage_a2/census.json signal_distribution_live_descriptive.trade_share 0.7567567567567568; reports/stage_a2/power.json economic_inputs.trade_share
- **Backing code:** scripts/census.py summarise(); src/etf/power.py _two_sided_cut (turns the share into a standard-normal cut for E2)
- **Notes:** 252/333 = 0.75676. Disclosed that the verdict-relevant input is drawn from a non-admissible descriptive series.

#### 17. `ETF-C17`

> The **220 charged requests** stand as the total lifetime network cost. Zero dollars, no capital, no credential, at any point.

- **Where:** `ETFExperiment/REGISTRATION.md:1160-1161`
- **Figures:** 220 charged requests (33 flow, 79 archive, 108 venue); 213 x 200, 5 x 404, 1 x 401, 1 x 403
- **n:** whole-stage total
- **Backing artifact:** data/ledgers/requests.jsonl (untracked): 238 charge rows at read time, split flow 51 / archive 79 / venue 108, settling 231 x 200, 5 x 404, 1 x 401, 1 x 403
- **Backing code:** src/etf/ledger/requests.py RequestLedger
- **Notes:** Charge #220 lands at 2026-08-28T20:40:46Z with the split exactly 33/79/108, so the figure was true when taken. Amendment 6 was committed 2026-08-29T02:43:48Z, by which point the ledger held 238 charges (last at 02:40:32Z). Same figure at progress.md:514-516 and :603.

#### 18. `ETF-C18`

> **The retro cohort is 8 trading days**: 2026-06-15, 2026-07-07, 2026-07-09, 2026-07-10, 2026-07-30, 2026-07-31, 2026-08-25, 2026-08-26.

- **Where:** `ETFExperiment/REGISTRATION.md:742-745`
- **Figures:** 8 trading days
- **n:** the 11 served days intersected with the servable hourly window from 2026-02-01
- **Backing artifact:** reports/stage_a1/retro_revision.json (11 stored rows: 2025-05-02, 2025-07-03, 2025-10-22 fall before 2026-02-01); reports/stage_a1/depth.json (window start 2026-02-01T11:00Z)
- **Backing code:** none - the intersection is stated in prose, not computed by a committed script
- **Notes:** 11 - 3 pre-window days = 8; the eight dates match the served set exactly.

#### 19. `ETF-C19`

> All six registered mutations were applied to real source, each caught, source restored green, bytecode purged before every run ... **Two of the six required fixing the harness rather than the source**

- **Where:** `ETFExperiment/report.md:405-419`
- **Figures:** 6 of 6 mutations caught
- **n:** n = 6 mutations
- **Backing artifact:** reports/stage_a4/mutations.log (6 lines, all caught=True restored_green=True)
- **Backing code:** scripts/mutations.py
- **Notes:** The log records outcomes only, not the diffs or the failing test ids.

#### 20. `ETF-C20`

> `make lint`, `make typecheck` and `make test` are green: ruff clean, **mypy strict clean across 76 files**, and the full suite passing.

- **Where:** `ETFExperiment/report.md:401-403`
- **Figures:** 76 files
- **n:** n = 76
- **Backing artifact:** no artifact; pyproject.toml [tool.mypy] files = src/etf, tests, scripts
- **Backing code:** pyproject.toml lines 42-46
- **Notes:** src 34 + tests 26 + scripts 16 = 76 .py files at the anchor. Structurally consistent; the gate output itself is not stored.

#### 21. `ETF-C21`

> **One thing that reads oddly against every prior closure in this house record: costs are not the binding term here.** A 9 bp round trip is **3.3 percent of one daily standard deviation**.

- **Where:** `ETFExperiment/report.md:301-303`
- **Figures:** 9 bp / 0.027431 = 3.28%
- **n:** daily sd on n = 475 pre-period returns
- **Backing artifact:** reports/stage_a2/preperiod_inputs.json daily_sd; src/etf/costs.py hyperliquid_band central 9
- **Backing code:** src/etf/costs.py
- **Notes:** Arithmetic check: 0.0009 / 0.0274305 = 0.03281.

#### 22. `ETF-C22`

> | assumption | minimum N | Section 9's registered anchor | held? | | published **0.18** | **237** | "near 250 admissible days" | **yes** | | registered **0.09** | **845** | "high hundreds to low thousands" | **yes** |

- **Where:** `ETFExperiment/REGISTRATION.md:834-842`
- **Figures:** 237 against 'near 250'; 845 against 'high hundreds to low thousands'
- **n:** E1 minimum-N bisection
- **Backing artifact:** reports/stage_a2/power.json minimum_n_for_e1
- **Backing code:** src/etf/power.py minimum_n
- **Notes:** The Section 9 anchors were registered at REGISTRATION.md:381-382 before any data existed; whether they 'held' is a judgement on qualitative language.

#### 23. `ETF-C23`

> The published next-day leg reports **Newey-West t 3.12 over 313 days**, which implies a rank correlation near **0.18** (t ~ rho*sqrt(n-2)/sqrt(1-rho^2) gives rho ~ 0.176 at n = 313).

- **Where:** `ETFExperiment/REGISTRATION.md:343-345`
- **Figures:** t 3.12, n 313 -> rho 0.176 -> registered assumption 0.09
- **n:** n = 313 (carried, external)
- **Backing artifact:** no artifact - carried from SSRN 6592830 (Section 14.1)
- **Backing code:** src/etf/config.py rho_undecayed=0.18, rho_registered=0.09
- **Notes:** Pure arithmetic on a carried figure: rho = t / sqrt(n - 2 + t^2). Every power number in the repository ultimately rests on it.

#### 24. `ETF-C24`

> A thresholded test discards every day inside the +/-100M band, which the measured signal distribution puts at 81 of 333 days (24.3 percent, n = 333).

- **Where:** `ETFExperiment/DECISIONS.md:89-92`
- **Figures:** 81 of 333 = 24.32%
- **n:** n = 333
- **Backing artifact:** reports/stage_a2/census.json signal_distribution_live_descriptive.inside_band = 81
- **Backing code:** scripts/census.py band_counts()
- **Notes:** ADR-003 is dated 2026-08-28 and 'registered as REGISTRATION.md sec.8', but it cites a measured census figure that did not exist until 20:34Z. Worth checking the ADR's own commit time (46056f9, 13:38:24 -0700 = 20:38Z) against that.

#### 25. `ETF-C25`

> Simulation budgets are stated rather than implied: E1 at 20,000 permutation draws and 2,000 simulations; E2 at 1,500 draws and 400 simulations, whose simulation error near a power of one half is about 0.025.

- **Where:** `ETFExperiment/report.md:329-332`
- **Figures:** E1 20,000/2,000; E2 1,500/400; E2 SE ~0.025
- **n:** per power cell
- **Backing artifact:** reports/stage_a2/power.json permutation_draws 20000, power_simulations 2000
- **Backing code:** scripts/power_gate.py line 100 (e2_power(..., draws=1500, simulations=400)); src/etf/power.py e1_power defaults
- **Notes:** Consistent for the power table. Inconsistent for the minimums: see claim ETF-C03.

#### 26. `ETF-C26`

> Forward-only accrual at the measured **20.8 admissible days per month** reaches roughly **291** by 2027-10-31, plus the **11** already admissible, for about **302**. That clears the governing 300 by two days

- **Where:** `ETFExperiment/REGISTRATION.md:1129-1131`
- **Figures:** 291 forward + 11 = 302 by 2027-10-31; clears 300 by two days
- **n:** 14 months of forward accrual
- **Backing artifact:** no artifact; derived in prose from the same unstored 20.8 figure
- **Backing code:** none
- **Notes:** 291 / 14 = 20.79, which is the arithmetic that pins down where 20.8 came from. Depends entirely on claim ETF-C02.

#### 27. `ETF-C27`

> **At the measured forward accrual rate the achievable N by 2027-03-31 is 163. Achieved N = 237 arrives around 2027-07-26 - roughly four months past the registered deadline.**

- **Where:** `ETFExperiment/REGISTRATION.md:911-913`
- **Figures:** N = 237 around 2027-07-26 (Amendment 3, later superseded by Amendment 4's 300/2027-10-26)
- **n:** same accrual rate
- **Backing artifact:** no artifact
- **Backing code:** none
- **Notes:** Amendment 3's figure is recorded as understated rather than corrected in place (REGISTRATION.md:953-956).

#### 28. `ETF-C28`

> **Neither selected source serves a per-row publication timestamp (n = 2 of 2).** ... The words "evening" and "night" appear **zero times** across both pages (n = 2 pages searched).

- **Where:** `ETFExperiment/docs/ACCESS.md:196, 124`
- **Figures:** 0 of 2 sources serve a publication timestamp; 0 occurrences of 'evening'/'night'
- **n:** n = 2 sources; n = 2 pages searched
- **Backing artifact:** no artifact stores the search result; data/access/farside-btc.html, farside-btc-all.html and sosovalue-btc.html (untracked) are the searchable primitives
- **Backing code:** none
- **Notes:** Feeds reopen threshold (a) at HYPOTHESES.md:84 and the README's 'n = 2 of 2' row. Trivially recomputable from the untracked bodies.

#### 29. `ETF-C29`

> every funding rate stamped at or after 2025-05-01 that has passed through a reader has been gated - measured live at 572 of 572 post-boundary rows across three pages.

- **Where:** `ETFExperiment/REGISTRATION.md:604-606`
- **Figures:** 572 of 572 post-boundary rows gated
- **n:** n = 572 rows across 3 pages
- **Backing artifact:** reports/stage_a1/venue_and_archive.json (funding_post_period gated_rows 72 of 72); reports/stage_a1/depth.json (funding_2025_05_page gated_rows 500 of 500)
- **Backing code:** src/etf/blindness.py funding_rows -> etf.preperiod.gate_pre_period
- **Notes:** 72 + 500 = 572 across the two post-boundary pages; the third page is the pre-period one (0 gated of 72). Verify the 'three pages' wording against the two gated pages.

#### 30. `ETF-C30`

> the retro cohort - 8 trading days - is **demoted to descriptive** and will carry no verdict. ... **Not armed**: any Stage B path. `verdict.py` is built dark against synthetic fixtures, refuses sealed paths in code, and is imported by nothing.

- **Where:** `ETFExperiment/REGISTRATION.md:934-938`
- **Figures:** 0 armed Stage B paths; 8 retro days demoted
- **n:** -
- **Backing artifact:** src/etf/verdict.py SEALED_MARKERS; data/state/ absent (no Stage B latch)
- **Backing code:** src/etf/verdict.py refuse_sealed_path; tests/test_verdict.py
- **Notes:** 'imported by nothing' is checkable by grep across the tree.


---

## 3. Intervals and tests

No confidence interval on any estimate is reported anywhere in this repository's documents. The five quantities above are the whole of the uncertainty reporting: three binomial standard errors on simulated powers, one min/max range of censored capture times, and one descriptive range on the cross-check difference. No E1 or E2 result exists to put an interval around, because neither co-primary was ever run on data.

**`ETFExperiment/REGISTRATION.md:1018-1021`** — standard error (no interval stated)

> Binomial standard error on a 0.80 estimate at 300 draws is **0.0231**, so an estimate landing precisely on its bar has roughly even odds of sitting below it, and the true E2 minimum could be 350 or 400.

- **Estimator:** binomial SE of a simulated power proportion, sqrt(p(1-p)/m)
- **Value:** 0.0231 on an estimate of 0.8000
- **n:** 300 power simulations
- **Data structure:** independent simulation replications of the E2 permutation test at n = 300 under a Gaussian copula with rho_s = 0.18
- **Backing:** reports/stage_a2/e2_minimum_n.json grid.published_0.18['300'] = 0.8
- **Note:** sqrt(0.8*0.2/300) = 0.023094. Repeated at DECISIONS.md:539-540, report.md:457-458, HYPOTHESES.md:84, progress.md:539.

**`ETFExperiment/REGISTRATION.md:966-970`** — standard error (no interval stated)

> At 300 simulations the standard error on a power near one half is **0.0289**, and the registered-assumption row shows it directly: 0.3567 at n = 350 against 0.3433 at n = 400. **That non-monotonicity is simulation noise, not a property of the test**

- **Estimator:** binomial SE at p = 0.5, sqrt(0.25/300)
- **Value:** 0.0289
- **n:** 300 power simulations per grid cell
- **Data structure:** the E2 minimum-N grid at rho_s = 0.09
- **Backing:** reports/stage_a2/e2_minimum_n.json grid.registered_0.09 {'350': 0.3566666666666667, '400': 0.3433333333333333}
- **Note:** sqrt(0.25/300) = 0.028868. The two grid values differ by 0.0133, well inside one SE. Also report.md:364-367.

**`ETFExperiment/REGISTRATION.md:856-859`** — standard error (no interval stated)

> E2 at 1,500 draws and 400 simulations, whose simulation error near a power of one half is about 0.025 - both registered floors sit far from these values.

- **Estimator:** binomial SE at p = 0.5, sqrt(0.25/400)
- **Value:** about 0.025
- **n:** 400 power simulations
- **Data structure:** the Amendment 3 power table cells for E2
- **Backing:** reports/stage_a2/power.json (the E2 cells); scripts/power_gate.py line 100
- **Note:** sqrt(0.25/400) = 0.025 exactly. Also report.md:329-332.

**`ETFExperiment/report.md:236-237`** — range, explicitly not an interval estimate

> The ranges overlap only between +04:05 and +04:29, so **the print appears to land between roughly 04:00 and 08:00 UTC on D+1**.

- **Estimator:** min/max of archived capture times, split by served-value vs dashed
- **Value:** served (n = 11): +04:05 to +08:00; dashed (n = 23): -03:38 to +04:29
- **n:** n = 11 served, n = 23 dashed, out of 34 parseable captures
- **Data structure:** archived Wayback capture timestamps, censored by the archive's own crawl schedule
- **Backing:** reports/stage_a1/retro_revision.json archive_captured_at per row
- **Note:** Recomputed from the artifact: served offsets 4.077, 4.484, 4.485, 6.394, 6.531, 7.189, 7.208, 7.274, 7.275, 7.275, 7.995 hours past midnight on D+1; dashed span -3.628 to +4.484. The document labels this corroborating and explicitly refuses to move the anchor on it (REGISTRATION.md:786-793).

**`ETFExperiment/REGISTRATION.md:623`** — range and location statistics, no interval

> the two differ by **a mean of 47.42M USD (median 27.20M, range -903.20M to +1,205.20M, n = 333)**

- **Estimator:** mean, median and min/max of the per-day difference between the registered five-fund aggregate and SoSoValue's all-fund total
- **Value:** mean 47.42M, median 27.20M, range -903.20M to +1,205.20M
- **n:** 333 overlapping out-of-sample days
- **Data structure:** two independently published daily series
- **Backing:** NONE stored; recomputable only from untracked data/access/sosovalue-btc.html and data/access/farside_all_parsed.json
- **Note:** See claim ETF-C15.

**`ETFExperiment/reports/stage_a2/census.json:signal_distribution_* blocks`** — empirical quantiles, not confidence intervals

> p05 / p25 / median / p75 / p95 for both signal distributions

- **Estimator:** nearest-rank quantiles (scripts/census.py quantiles())
- **Value:** admissible n=11: min -265.4M, p05 -265.4M, p25 -102.9M, median 86.8M, p75 302.8M, p95 674.9M, max 674.9M; live n=333: min -860.9M, p05 -503.7M, p25 -164.1M, median 27.4M, p75 224.5M, p95 613.6M, max 1,142.4M
- **n:** 11 and 333
- **Data structure:** daily aggregate net flow in USD
- **Backing:** reports/stage_a2/census.json
- **Note:** No dispersion figure for these is quoted in any document.


#### Test statistics and p-values

This repository computed NO test statistic and NO p-value on its own data. Every t, F and beta in the documents is labelled carried and comes from Section 14. The only statistics generated here are simulated powers, simulated permutation critical values, and the two engine-calibration assertions in tests/test_power.py.

**`ETFExperiment/REGISTRATION.md:284-286`** — Sidak-adjusted alpha for two co-primaries — *registered here*

> Two co-primaries, distribution-free, one-sided, at `alpha_adj = 1 - 0.95^(1/2) = 0.0253205655` each. Both must pass for the Stage B GO row.

- **Value:** 0.0253205655
- **n:** -
- **Data structure:** -
- **Backing:** src/etf/config.py line 25 (ALPHA_ADJ = 1.0 - 0.95 ** (1.0/2.0)); reports/stage_a2/power.json alpha_adj 0.025320565519103666
- **Note:** 1 - 0.95**0.5 = 0.02532056551910367.

**`ETFExperiment/REGISTRATION.md:290-293`** — E1: Spearman rho under a permutation null — *registered here; run only in simulation and against synthetic fixtures*

> Exact permutation test on the rank (Spearman) correlation between the admissible as-printed signal for day D and the next-day return, over all admissible days, no threshold, one-sided positive.

- **Value:** NEVER COMPUTED ON DATA - no test statistic and no p-value exists
- **n:** would have been the admissible-day count (11 at closure)
- **Data structure:** paired (signal, next-day return) series
- **Backing:** src/etf/verdict.py (dark); src/etf/power.py e1_power (simulation only)
- **Note:** The repository reports no p-value of its own anywhere.

**`ETFExperiment/REGISTRATION.md:302-306`** — E2: mean net return per trade under a label permutation — *registered here; simulation only*

> Mean net return per trade under the Section 4 rule at T = 100 million USD; exact one-sided lower bound above zero at alpha_adj by permutation

- **Value:** NEVER COMPUTED ON DATA
- **n:** would have been the admissible-day count
- **Data structure:** signed position labels against realised net returns
- **Backing:** src/etf/power.py e2_power; src/etf/verdict.py
- **Note:** e2_power computes a permutation p-value inside each simulated replication: (exceed + 1) / (draws + 1) <= alpha (src/etf/power.py:164).

**`ETFExperiment/tests/test_power.py:59-65`** — one-sided permutation critical value of Spearman rho against the 1/sqrt(n-1) asymptotic — *engine calibration, run here*

> Under H0 the permutation rho has sd 1/sqrt(n-1); the simulated cut must agree. ... expected = 1.6449 / math.sqrt(n - 1); assert abs(cut - expected) < 0.02

- **Value:** agreement within 0.02
- **n:** the test's fixture n
- **Data structure:** permutation null of ranks
- **Backing:** tests/test_power.py
- **Note:** This is the 'pinned by known answers' claim at report.md:334-336 and DECISIONS.md:99-102.

**`ETFExperiment/tests/test_power.py:75-78`** — empirical size of E1 under a zero true effect — *engine calibration, run here*

> test_power_at_a_zero_true_effect_sits_at_alpha_the_calibration_check ... assert 0.02 < power < 0.09

- **Value:** between 0.02 and 0.09 against a nominal 0.0253
- **n:** the test's fixture n and simulation budget
- **Data structure:** simulated bivariate normal with rho = 0
- **Backing:** tests/test_power.py
- **Note:** The tolerance band is wide relative to the nominal alpha.

**`ETFExperiment/REGISTRATION.md:493-502`** — carried external test statistics (Lim, SSRN 6592830) — *CARRIED - explicitly not measured by this repository (Section 14 preamble, REGISTRATION.md:482-485)*

> | same-day impact, OLS | **53 bp per 100M USD** | ... | **next-day prediction** | **Newey-West t 3.12** | | bidirectional Granger causality | beta **0.47**, t **9.75** | ... | conditional reversal (controlling for future flows) | t **-2.42 to -3.99** | | total impact at 10 days | **96 bp per 100M USD**, t **4.49** |

- **Value:** Newey-West t 3.12 (next-day); t 8.99 (variance share); IV first-stage F 21.58; Granger beta 0.47 t 9.75; conditional reversal t -2.42 to -3.99; 10-day total t 4.49
- **n:** 313 trading days
- **Data structure:** the source study's daily panel
- **Backing:** none in-repo
- **Note:** The t 3.12 is the only one that propagates into a bar, via rho ~ 0.18 -> the registered 0.09.

**`ETFExperiment/REGISTRATION.md:510-512`** — carried external t-statistic (SSRN 6567058) — *CARRIED*

> **563 days** January 2024 through April 2026, Farside data: **causal IV impact 0.20 percent per 100M USD at t 2.65**, against the earlier **0.41 percent OLS**.

- **Value:** t 2.65
- **n:** 563 days
- **Data structure:** the same author's extended daily panel
- **Backing:** none in-repo
- **Note:** Called 'the single most important number carried into this registration' (REGISTRATION.md:516); it is the sole justification for halving the effect assumption.

**`ETFExperiment/REGISTRATION.md:542-545`** — carried external rolling correlation — *CARRIED (CoinDesk, 2026-05-14, SoSoValue data)*

> the **90-day rolling coefficient** between daily BTC return and the daily change in cumulative net inflows stands at **0.16, indistinguishable from zero**, down from a **February peak of 0.68**.

- **Value:** 0.16, down from 0.68
- **n:** 90-day rolling window
- **Data structure:** rolling daily correlation
- **Backing:** none in-repo
- **Note:** 'indistinguishable from zero' is reported without a standard error or interval.


---

## 4. Provenance claims

19 provenance claims extracted.

#### P01 — `ETFExperiment/REGISTRATION.md:3-8`

> **STATUS: SECTION 0 REGISTERED 2026-08-28, BEFORE ANY NETWORK CALL.** At the moment this document was first committed, **this repository had sent no request to any endpoint, held no flow value, no price, no funding row, and no census row of any kind.** The request ledger did not exist.

- **Commit named:** none named in the text; the commit is 44567f6 'reg: REGISTRATION.md Section 0, the outcome map, before any network call'
- **What would have to be true:** REGISTRATION.md's first commit must precede the first row of data/ledgers/requests.jsonl, and no data file may exist in the tree at that commit.
- **Checkable by:** git log: 44567f6 authored 2026-08-28 01:07:59 -0700 = 08:07:59Z. First ledger charge row: 2026-08-28T08:12:19Z (meta.robots, farside). Gap = 4 min 20 s. data/ is gitignored so its absence at the commit cannot be read from the tree; the ledger's own first timestamp is the check.

#### P02 — `ETFExperiment/report.md:17-21`

> Then the scaffold, the five standing guards, CLAUDE.md, REGISTRATION.md Sections 0-14, and HYPOTHESES.md - **every one of them committed before this repository had sent a single request to any endpoint.**

- **Commit named:** 815f888, 44567f6, e33b03c, 38b9397, 0c29049
- **What would have to be true:** All five commits must be stamped before 2026-08-28T08:12:19Z.
- **Checkable by:** git log --date=iso: 815f888 08:05:56Z, 44567f6 08:07:59Z, e33b03c 08:09:26Z, 38b9397 08:11:17Z, 0c29049 08:11:50Z - all before 08:12:19Z.

#### P03 — `ETFExperiment/REGISTRATION.md:65-70`

> Enforced by `etf.section0.fire_section0`, committed with this document and pinned by `tests/test_section0.py`, with every boundary fixture sitting exactly on the registered boundary: 0.80 and 0.50 on the power floors, 0.50 on the majority share, and one-ULP steps across each.

- **Commit named:** 44567f6
- **What would have to be true:** src/etf/section0.py and tests/test_section0.py must be present in the same commit that introduced Section 0, and the fixtures must sit on 0.80/0.50/0.50 rather than inside them.
- **Checkable by:** git ls-tree -r 44567f6 lists REGISTRATION.md, src/etf/section0.py, src/etf/observability.py, tests/test_section0.py and tests/test_observability.py together. Fixture values are readable in tests/test_section0.py (test names name the boundary explicitly).

#### P04 — `ETFExperiment/CLAUDE.md:101-103`

> **Pre-register before results.** REGISTRATION.md is append-only; an amendment is dated, reasoned, and states exactly what data existed when it was made. **Nothing above an amendment line is ever edited.**

- **Commit named:** none named
- **What would have to be true:** Every commit touching REGISTRATION.md after 38b9397 must add lines below the last amendment line and change nothing above it.
- **Checkable by:** git diff between consecutive commits touching REGISTRATION.md: 294eab7 (Am1), 41351a9 (Am2), 67f25f3 (Am3), cf6efaf (Am4), 3f5d629 (Am5), 4d11002 (Am6). Six diffs to inspect.

#### P05 — `ETFExperiment/REGISTRATION.md:598-607`

> **What data existed when this amendment was made.** Stage A.1 access and rate-ceiling telemetry, the archive timemaps, and one capture each of the flow source's two pages ... and the request ledger (143 charged requests). ... No census row existed, no admissibility had been computed, and no power number existed.

- **Commit named:** 294eab7 (2026-08-28 13:16:31 -0700 = 20:16:31Z)
- **What would have to be true:** The ledger must hold exactly 143 charges at the amendment's commit time, and census.json / power.json must not yet exist.
- **Checkable by:** data/ledgers/requests.jsonl: charge #143 is stamped 2026-08-28T20:12:49Z and charge #144 follows after; census.json computed_at 20:34:47Z and power.json computed_at 20:35:37Z, both after 20:16:31Z. Consistent.

#### P06 — `ETFExperiment/REGISTRATION.md:700-709`

> **What data existed when this amendment was made.** Everything in Amendment 1, plus 37 archived captures of the flow source fetched from the Wayback Machine ... the sealed outcome substrate (5,002 hourly candle rows and 11 funding pages), the pre-period carve-out inputs, the admissible-day census (336 rows), and one forward flow capture taken at 2026-08-28T20:17:11Z. ... **No power number existed when this amendment was written.**

- **Commit named:** 41351a9 (2026-08-28 13:36:13 -0700 = 20:36:13Z)
- **What would have to be true:** power.json must postdate the amendment commit, and the census / substrate / retro artifacts must predate it.
- **Checkable by:** power.json computed_at 2026-08-28T20:35:37Z - which is BEFORE the 20:36:13Z commit of Amendment 2. The amendment says no power number existed when it was written; the artifact timestamp says one was computed 36 seconds earlier. Worth resolving: 'written' vs 'committed' may differ. retro_revision.json 20:32:34Z, census.json 20:34:47Z, substrate_coverage.json 20:19:50Z, preperiod_inputs.json 20:24:57Z all precede it.

#### P07 — `ETFExperiment/REGISTRATION.md:823-827`

> **No outcome value has been read.** Every power figure below is a simulation at a registered assumption; every empirical input to it is a count, a timestamp, a flow value, or a pre-period figure stamped strictly before 2025-05-01.

- **Commit named:** 67f25f3 (Amendment 3)
- **What would have to be true:** No module outside the sealed writers and preperiod_prices.py may parse o/h/l/c/v, and the sealed store must never have been opened.
- **Checkable by:** tests/test_guards.py::test_no_module_reads_a_priced_candle_field_anywhere walks the parse tree; data/state/ (the Stage B latch path) does not exist in the live tree; src/etf/verdict.py refuse_sealed_path lists data/outcomes, data/funding, data/retro, data/census.

#### P08 — `ETFExperiment/REGISTRATION.md:604-606`

> every funding rate stamped at or after 2025-05-01 that has passed through a reader has been gated - measured live at 572 of 572 post-boundary rows across three pages.

- **Commit named:** 294eab7 (Amendment 1)
- **What would have to be true:** The gated-row counts in the stored probes must sum to 572 over post-boundary pages only.
- **Checkable by:** reports/stage_a1/venue_and_archive.json funding_post_period gated_rows 72 / row_count 72; reports/stage_a1/depth.json funding_2025_05_page gated_rows 500 / row_count 500. 72 + 500 = 572 across TWO post-boundary pages; the third page (funding_pre_period) has 0 gated of 72.

#### P09 — `ETFExperiment/REGISTRATION.md:695-696, 790-793`

> **The anchor has not moved and cannot move until the A.1 Task 3 measurement exists.** ... Section 3 permits exactly one input to move it - the measured 95th percentile first-print time - and that measurement does not yet exist.

- **Commit named:** 294eab7, 41351a9
- **What would have to be true:** CONFIG.entry_anchor_hour_utc must still read 8 at the anchor, no amendment may move it, and the retro capture-time estimate must not have been used as an input.
- **Checkable by:** src/etf/config.py entry_anchor_hour_utc=8 at the anchored SHA; git log -p on config.py shows whether it ever changed; src/etf/anchor.py amended_anchor_hour is the only mover and is called by nothing outside tests.

#### P10 — `ETFExperiment/CLAUDE.md:113-114`

> **Secrets never enter the repo - and none are needed.** `.env.example` is empty on purpose. No API key exists anywhere in this project.

- **Commit named:** none named
- **What would have to be true:** .env.example must contain no key material and no credential may appear in history.
- **Checkable by:** .env.example is 200 bytes at the anchor (a comment block, not empty of bytes); git log --all -p searched for key-shaped strings.

#### P11 — `ETFExperiment/REGISTRATION.md:1090-1094`

> **Remains empty and is not filled by this closure.** ... The assistant's recorded **0.10** stands where it is and **was not copied into the slot** at any point.

- **Commit named:** 3f5d629 (Amendment 5)
- **What would have to be true:** The Section 13 slot must never have parsed at any commit in history.
- **Checkable by:** src/etf/registration_check.py regex against REGISTRATION.md at every commit touching it; the slot text at REGISTRATION.md:471-472 reads '_(empty - reserved for the operator)_'.

#### P12 — `ETFExperiment/REGISTRATION.md:1157-1159`

> **`etf-snap` is disarmed.** `etf-daily` was disarmed at Amendment 5. **The repository holds no armed collector and no running process.**

- **Commit named:** 4d11002 (Amendment 6, the anchored commit)
- **What would have to be true:** Both user timers must be disabled and inactive.
- **Checkable by:** systemctl --user is-enabled/is-active etf-snap.timer etf-daily.timer at 2026-09-05T03:48Z: both 'disabled' and 'inactive'; neither appears in systemctl --user list-timers --all. VERIFIED.

#### P13 — `ETFExperiment/REGISTRATION.md:1160-1161`

> The **220 charged requests** stand as the total lifetime network cost.

- **Commit named:** 4d11002 (committed 2026-08-28 19:43:48 -0700 = 2026-08-29T02:43:48Z)
- **What would have to be true:** The request ledger must hold 220 charge rows at or after the commit that asserts it.
- **Checkable by:** data/ledgers/requests.jsonl holds 238 charge rows, the last stamped 2026-08-29T02:40:32Z - three minutes BEFORE the commit. Charge #220 is stamped 2026-08-28T20:40:46Z. The figure is a stale snapshot carried into a later amendment.

#### P14 — `ETFExperiment/report.md:405-407`

> **All six registered mutations were applied to real source, each caught, source restored green, bytecode purged before every run**

- **Commit named:** a881956 'test: all six registered mutations caught, source restored green'
- **What would have to be true:** The working tree at that commit must be identical to the pre-mutation tree, and the harness must have purged bytecode.
- **Checkable by:** git show --stat a881956; reports/stage_a4/mutations.log; scripts/mutations.py.

#### P15 — `ETFExperiment/progress.md:520-524`

> Nothing was pushed to any remote; no remote exists. The four pre-existing user timers were verified untouched throughout: **npl-watch** (60 min), **news-collect** (22:31 UTC), **solattn-daily** (00:40 UTC), **npl-daily** (01:40 UTC).

- **Commit named:** none named
- **What would have to be true:** No git remote may be configured, and the four named timers must still exist with their stated schedules.
- **Checkable by:** git remote -v in the live repo; systemctl --user list-timers at 2026-09-05T03:48Z shows npl-watch, news-collect and npl-daily present; solattn-daily was not listed in that snapshot (outside this repository's scope).

#### P16 — `ETFExperiment/REGISTRATION.md:72-86`

> **Registered expectation, stated now so the verdict reads as a documented answer** ... The Section 9 arithmetic and the decay evidence of Section 14 point to DEGRADED. ... This is stated **before the census exists**

- **Commit named:** 44567f6 / e33b03c
- **What would have to be true:** The DEGRADED expectation must appear in the Section 0 commit, unedited afterwards.
- **Checkable by:** git show 44567f6:REGISTRATION.md and e33b03c:REGISTRATION.md; git log -p on the block.

#### P17 — `ETFExperiment/REGISTRATION.md:571-573`

> **Therefore: no accrual, coverage, lag, retention, revision, or capture-density figure in this repository is registered before it is measured.** Every such figure is named as an A.1 or A.2 **measurement target**, never as an input

- **Commit named:** 38b9397 (Section 14.7, committed 08:11:17Z)
- **What would have to be true:** No accrual/coverage/density figure may appear as a registered input anywhere in Sections 0-14, and the amendment log must show each such figure entering only after measurement.
- **Checkable by:** The 20.8 admissible-days-per-month accrual rate (claim ETF-C02) is used as an input to the deadline finding and is called 'measured'. Whether it satisfies 14.7 is exactly what the verification must decide. The Section 9 'rough anchors' at REGISTRATION.md:376-388 are explicitly labelled expectations rather than registered figures.

#### P18 — `ETFExperiment/REGISTRATION.md:400-408`

> **Stage B opens the sealed outcomes exactly once, behind a latch written first**, recording the sha256 of every module on the read surface. ... `verdict.py` is built dark in A.3 against synthetic fixtures and is never pointed at real sealed data before that single registered read.

- **Commit named:** e33b03c (Section 10)
- **What would have to be true:** data/state/stage_b_read.json must not exist, and verdict.py must be imported by nothing.
- **Checkable by:** data/state/ is absent from the live tree at 2026-09-05T03:47Z; grep for 'from etf.verdict' / 'import verdict' across src, scripts and tests.

#### P19 — `ETFExperiment/DECISIONS.md:74-92`

> ADR-003 ... **Date:** 2026-08-28 - **Status:** accepted - registered as REGISTRATION.md sec.8 ... a thresholded test discards every day inside the +/-100M band, which the measured signal distribution puts at 81 of 333 days (24.3 percent, n = 333).

- **Commit named:** 46056f9 'docs: DECISIONS.md, 18 numbered ADRs' (2026-08-28 13:38:24 -0700 = 20:38:24Z)
- **What would have to be true:** An ADR presented as registering Section 8 (committed 08:09:26Z) cites a census figure that did not exist until 20:34:47Z. The decision may predate the file; the citation cannot.
- **Checkable by:** git log -1 46056f9; reports/stage_a2/census.json census_run_at 2026-08-28T20:34:47Z.


---

## 5. Live-repo access log

Per COMMON_RULES, `git status --porcelain` was run on the live repository before the first
access and after the last. Both outputs are recorded verbatim.

**Before first access — 2026-09-05T03:46:12Z**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
(no output — clean)
```

**After last access — 2026-09-05T03:49:15Z**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
(no output — clean)
```

`git rev-parse HEAD` returned `4d110027674e7b4cd2861cf4e0e74f975111daf1` both before and after, matching the
anchored SHA. Nothing was modified.

**Note on an untracked file that does not appear in `status`.** The live tree contains
`_CLOSED_DO_NOT_RUN_HERE` (747 B, mtime 2026-09-02 22:38 local), excluded via
`.git/info/exclude` line 7. It is an owner-written marker dated 2026-09-02 saying the
repository is closed and that a session was opened there by mistake. **It is not mine and
predates this audit**; it is reported here because COMMON_RULES requires any working-tree
entry other than the listed pre-existing dirt to be named. No entry of mine exists.

**Read-only operations performed on the live repository**

| time (UTC) | operation | purpose |
|---|---|---|
| 03:46:12 | `git status --porcelain` | pre-access record |
| 03:46 | `git rev-parse HEAD`, `git log --oneline -40 --date=iso` | commit ordering for the provenance claims |
| 03:46 | `git log -1` and `git ls-tree -r --name-only` on 815f888, 44567f6, e33b03c, 38b9397, 0c29049 | confirm section0.py shipped with Section 0 |
| 03:46 | `cat _CLOSED_DO_NOT_RUN_HERE`, `git check-ignore -v`, `cat .git/info/exclude` | explain the one untracked entry |
| 03:47 | `ls -la` of the repo root and of `data/`, `data/access`, `data/archive_bodies`, `data/census`, `data/funding`, `data/ledgers`, `data/outcomes`, `data/snapshots`, `data/snapshots/bodies`; `du -sh` | untracked-artifact inventory (sizes and mtimes) |
| 03:47 | read `data/snapshots/flow_snapshots.jsonl` (20 rows) | forward-capture count and the open-day absence |
| 03:48 | read `data/ledgers/requests.jsonl` (476 lines) | the 220 / 143 charged-request claims |
| 03:48 | read `data/access/*.meta.json`, `data/access/farside_all_parsed.json` (row count and first/last row only) | 676 / 336 / 333 and the `Total 0.0` hazard |
| 03:48 | row counts of `data/outcomes/btc-1h-servable-window.json`, `data/funding/*.json`, `data/census/census.jsonl` | 5,002 / 5,002 / 336 |
| 03:48 | `systemctl --user is-enabled`, `is-active`, `list-timers --all` | the "no armed collector" claim (both timers disabled and inactive) |
| 03:49:15 | `git status --porcelain`, `git rev-parse HEAD` | post-access record |

No `.env`, keystore, session or credential file was opened. `data/outcomes/` and
`data/funding/` were opened only to count rows; no price series was extracted. No file in the
audited repository was written, and no repository script was executed.

**Anchoring caveat.** Every untracked figure above is UNANCHORED and carries its read time.
The live tree stands at the anchored SHA and is clean, but `data/` moved after the anchor's
documents were written: the request ledger grew from 220 to 238 charges and the snapshot
ledger from 2 to 20 captures, both between 2026-08-28T20:40Z and 2026-08-29T02:40Z, before
`etf-snap` was disarmed. Nothing has been added to it since.
