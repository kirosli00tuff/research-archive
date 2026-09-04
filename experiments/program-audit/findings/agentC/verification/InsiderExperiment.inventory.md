# InsiderExperiment — verification inventory (Agent C, LOCATE)

Repository: `InsiderExperiment`
Anchored SHA: `12d9fd36cf055cb10ea67a3fc737e404217bc95a` (master, 2026-08-25)
Snapshot read: `SNAP/InsiderExperiment/` (tracked files, anchored)
Live tree read: `/home/kiros-li/Documents/GitHub/InsiderExperiment/` (git objects and untracked data only, read-only)
Prepared: 2026-09-04 (UTC)

Scope note. This repository has **no** `report.md`, `FINDINGS.md`, `README.md`, `HYPOTHESES.md`,
`registrations/` directory, or `reports/*.md` other than `reports/stage_a1/refusals.md`. The
numeric claims live in `REGISTRATION.md` (896 lines), `DECISIONS.md` (416 lines, ADR-001 to
ADR-013), `progress.md` (315 lines) and `CLAUDE.md`. `docs/` exists in the live tree and is empty.

---

## 1. Artifacts

### 1.1 Analysis code, tracked (anchored)

| Path | What it holds | Which figures it backs |
|---|---|---|
| `src/insider/section0.py` | `fire_power_gate` / `fire_corpus_gate`; the GO/DEGRADED/BLOCKED and CORPUS-GO/BLOCKED branches, boundaries inclusive at the lower edge | The BLOCKED verdict itself; the rationale string reproduced verbatim in `power.json` |
| `src/insider/config.py` | Every registered parameter as a frozen dataclass: `mde_go_ceiling_bp=20.0`, `mde_degraded_ceiling_bp=40.0`, `corpus_event_floor=1000`, `corpus_coverage_floor=0.80`, `t_critical=2.0`, `sessions_per_month=21`, `newey_west_lags=21`, grid `(5,21,63,126)`, `decayed_gross_band_bp=(30.0,40.0)`, `round_trip_bp_low/high=32/100`, `spread_bp_low/high=15.8/50.0`, `primary_hold_sessions=126`, `primary_weighting="value_weighted"`, `routine_consecutive_years=3`, `assistant_prior=0.12` | Every bar and every registered constant in REGISTRATION Sections 0, 3, 6, 7, 8, 10 |
| `src/insider/power/dispersion.py` | `sample_sd` (ddof 1), `autocorrelation`, `variance_inflation` (Bartlett `1+2*sum(1-k/(L+1))*rho_k`), `summarize`; annualized TE = `sd*sqrt(21*12)`; `effective_periods = n/vif`; `book_width_mean` from the stored `book_width` column | 62.95 bp daily SD, VIF 0.899, N_eff 2,869.9, TE 9.993 % |
| `src/insider/power/mde.py` | `standard_error_monthly = 21*sd/sqrt(N_eff)`; `mde = t_critical * se * 1e4`; `band_position` | **49.35 bp per month**, 24.68 bp monthly SE, the "above the whole band" phrasing |
| `src/insider/power/report.py` | Runs the four series and the NW grid, fires the gate, writes `power.json`, records to the evidence ledger | Table at REGISTRATION 15.5 and the lag-sensitivity row |
| `src/insider/cost.py` | `monthly_cost_drag` (round trip / hold months) and `net_band_bp_per_month` (`gross_low - pessimistic`, `gross_high - optimistic`) | 5.33 and 16.67 bp/month drag; the 13.3 to 34.7 bp net band |
| `src/insider/portfolio/returns.py` | Book construction, weights, `_effective_names` (inverse Herfindahl), `_share`, the split write to `insider_sealed.db` (raw) and `insider_dispersion.db` (centered). `widths.append(len(priced))` — the dispersion store's book width is the **priced** book | 29.7 / 66.9 effective names, 14.9 % / 33.8 % top-1 / top-5, corr 0.904 / 0.953, the 13,750 `not_priced` drop |
| `src/insider/portfolio/membership.py` | `mean_width()` averages `len(book)` over **non-empty sessions**, before the not-priced drop; `coverage()` = non-empty sessions / all sessions | 71.9 mean book width; 99.5 % session coverage |
| `src/insider/portfolio/build.py` | Writes `portfolio.json`; `book_width_mean` here is `series.mean_width()`, i.e. the pre-drop width | The 71.9 figure everywhere it appears |
| `src/insider/corpus/build.py`, `classify.py`, `cluster.py`, `routine.py`, `store.py` | The eight call states, the CMP routine rule, the five-day cluster window, the Johnsen filter, the surrogate-key event store | 4,585; the attrition and sub-reason tables; 773/209 clusters; the lag distribution |
| `src/insider/corpus/validate.py` | The three-route validation: index-vs-datasets ratio, 25-document XML field check, 25-issuer submissions check | `validation.json` |
| `src/insider/market/universe.py`, `build.py`, `source.py`, `store.py`, `port_check.py` | The ported `U-LIQ-500-stk-w60-m40-p5` rule, the immutable read-only SQLite URI onto AiTrader, hashing before and after | `port.json`; the "500 of 500 members reproduced" claim in ADR-004 |
| `src/insider/edgar/{throttle,client,bulk,fullindex,submissions,xml_form4}.py` | The 8 req/s throttle, retry set, the DERA zips, the full-index route, per-filing XML | 214 wire requests, zero non-200 |
| `src/insider/ledger/{append_only,fetch,evidence}.py` | fsynced append-only JSONL ledgers | `ledgers/fetch.jsonl`, `ledgers/evidence.jsonl` |
| `src/insider/{absence,callstate,paths,registration_check}.py`, `eval/evaluator.py` | The absence type, the eight states, path table, the operator-prior gate, the sole sealed-store reader | Section 12, Section 13 |
| `scripts/mutations.py` | The five registered mutations, bytecode purge, guard invocation | `mutations.json` |
| `tests/` (11 files) | 105 collected test cases by AST count (96 functions, `test_section0` ×8 and `test_universe_port` ×3 parametrized); `test_guards.py` holds 23 | The "106 tests green" claim |

### 1.2 Stored artifacts, tracked (anchored)

| Path | What it holds | Backs | Tracked |
|---|---|---|---|
| `reports/stage_a1/power.json` (3,904 B) | Four series rows (N, VIF, N_eff, sd_bp, TE %, SE, MDE, autocorrs, book widths), the four-point NW grid, `dropped_primary`, the bands, `verdict: BLOCKED`, `stage_b_authorized: false` | REGISTRATION 15.5, 17.1, 17.3; progress "The numbers" table; ADR-010 | yes |
| `reports/stage_a1/portfolio.json` (3,170 B) | Per-series `sessions_with_a_return`, `membership_coverage`, `book_width_mean`, `dropped`, and the diagnostics block (`book_effective_names`, top-1/top-5 shares, corr) | 71.9 / 29.7 / 66.9 / 14.9 % / 33.8 % / 1.9 % / 8.5 % / 0.904 / 0.953 | yes |
| `reports/stage_a1/corpus.json` (3,738 B) | `qualifying_events: 4585`, `events_per_year` (sums to 4,585), the 30-key attrition map, prefunnel, routine labels, `unclassifiable_by_year`, the 88-bin lag distribution, `flag_absent_events: 3350`, clusters 773/209, `session_coverage 0.9954110898661568`, `mean_book_width 71.90895…`, `verdict: CORPUS-GO` | REGISTRATION 15.1 to 15.4, 17.2 | yes |
| `reports/stage_a1/validation.json` (15,084 B) | 53 quarter rows (index rows vs dataset documents, ratio 2.043 to 2.140), 25 XML field checks (25 agree), `xml_tally`, 25 submissions ticker checks (21 present) | ADR-002, ADR-007 | yes |
| `reports/stage_a1/port.json` (525 B) | `sessions 2615`, `formations 124`, `distinct_symbols 1218`, `bars_copied 2713496`, both AiTrader SHA-256 values before and after, `bars_size_bytes 7320629248`, `unchanged: true` | The boundary claim in progress.md and ADR-004 | yes |
| `reports/stage_a1/mutations.json` (2,749 B) | Five mutation records, each with `guard_failed_when_mutated: true` and `guard_green_when_restored: true`; `final_suite` is a **pytest progress line** (33 dots, `[100%]`), not a pass count | ADR-012, progress "Two guards that did not fire" | yes |
| `reports/stage_a1/refusals.md` (5,563 B) | Two serialized Johnsen cluster rejections (DRI, 2020-04-23/27, sizes 12 and 11, modal fraction 1.0 against 0.80) and two `insufficient_history` refusals | REGISTRATION 15.4, standing guard 4 | yes |

### 1.3 Untracked data in the live working tree (UNANCHORED)

Read read-only at **2026-09-04 05:29–05:33 UTC**. All of it is gitignored, so it is not covered by
the anchor and may have changed after 2026-08-25. `ls -la` mtimes are all 2026-08-25 18:35–19:06
local, i.e. contemporaneous with the A.1 session.

| Path | Size (bytes) | mtime (local) | What it holds | Backs |
|---|---|---|---|---|
| `var/insider_dispersion.db` | 913,408 | 2026-08-25 19:05:40 | `centered_excess` (date, centered, book_width) for the four series, and `dropped` | **The 49.35 deciding number.** Recomputable primitive |
| `var/insider_sealed.db` | 884,736 | 2026-08-25 19:05:40 | Raw daily portfolio excess returns; its mean is the realized alpha | **NOT OPENED by this audit.** Existence and size only |
| `var/insider_corpus.db` | 643,072 | 2026-08-25 19:05:33 | `event` (4,585 rows, surrogate key), `attrition` (30), `lag` (88), `cluster` (773), `refusal` (10), `meta` (5) | 4,585, the by-year counts, 209/773, 3,350 flag-absent |
| `var/insider_market.db` | 234,700,800 | 2026-08-25 18:36:05 | `session` 2,615; `membership` 62,000 (= 124 × 500); `bar` 2,713,496 | `port.json`; ADR-004's "500 of 500" |
| `ledgers/fetch.jsonl` | 144,800 | 2026-08-25 19:06:24 | 684 records: 214 `wire`, 470 `cache`, **every status 200** | The 214 / 2.78 GB / zero non-200 claim |
| `ledgers/evidence.jsonl` | 28,878 | 2026-08-25 19:06:24 | 14 records: 1 `market_port`, 4 `corpus_gate`, 3 `portfolio_build`, 3 `power_gate`, 2 `corpus_validation`, timestamped 01:36:26Z to 02:06:24Z | The run timeline; every `power_gate` records the same 49.3543 |
| `cache/edgar/` | 2,783,280,665 (`du -sb`), 214 files in 147 dirs | 2026-08-25 19:06:23 | The SEC responses. Not opened | The "cache equals the wire total byte for byte" claim |
| `docs/` | empty | 2026-08-25 18:24 | nothing | — |
| `_CLOSED_DO_NOT_RUN_HERE` | 747 | 2026-09-02 22:38 | An operator marker excluded via `.git/info/exclude`, written 2026-09-02, **after** the anchor. Not an experiment artifact | Records that a session was opened in the closed repo by mistake on 2026-09-02 |
| `.env` | 64 | 2026-08-25 18:35 | Not read. Holds `SEC_USER_AGENT` per `.env.example` | — |

Also present and ignored: `.venv/`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `__pycache__/`.

### 1.4 External artifact the boundary claim points at

`~/Documents/GitHub/AiTrader/analysis_bars.db` is **7,323,656,192 bytes, mtime 2026-09-03 15:32**,
against `port.json`'s recorded `bars_size_bytes: 7320629248`. The AiTrader collector has written to
it since 2026-08-25, so the SHA-256 recorded at closure cannot be re-verified today and its failure
to re-verify now would **not** be evidence against InsiderExperiment. `backtest/universe.py` is
13,634 bytes, mtime 2026-07-26, i.e. unchanged since before the A.1 session.

---

## 2. Numeric claims, ranked

Ranked by how much rests on them. Ranks 1 to 7 are marked **MUST-VERIFY** (the brief demands at
least three).

### Rank 1 — MUST-VERIFY. The deciding number
> "**The registered primary design cannot resolve the effect at achievable power. The minimum
> detectable effect is 49.35 bp per month against a registered BLOCKED floor of 40** and against a
> decayed literature band of 30 to 40 bp per month gross and 13 to 35 bp per month net at the
> six-month hold. Stage B is never written. The repo closes on the finding."

`REGISTRATION.md:812-816` (Section 17.1). Same language verbatim at `progress.md:14-18`,
`progress.md:174-179`, `DECISIONS.md:288-292` (ADR-010), and `REGISTRATION.md:708-719`
(Section 15.5); `progress.md:186-188` and `progress.md:241`.
Figure: 49.35 bp/month (stored 49.3543). n = 2,581 sessions, N_eff 2,869.9.
Produced by: `src/insider/power/mde.py:38-67` + `dispersion.py:151-192` reading
`var/insider_dispersion.db`; fired by `section0.py:46-87`; serialized to
`reports/stage_a1/power.json`.
*Locator note: recomputed from the stored centered series at read time and it reproduces to four
decimals (49.3543); the series sums to -1.4e-16, i.e. it is genuinely centered.*

### Rank 2 — MUST-VERIFY. The corpus count against its own by-year table
> "**CORPUS-GO.** 4,585 qualifying events against a registered floor of 1,000, with 99.5 percent
> of in-span sessions carrying a non-empty book against a floor of 80 percent. Mean book width 71.9
> names at the six-month hold."

`REGISTRATION.md:594-596`. The by-year table immediately below it, `REGISTRATION.md:601-608`,
reads 2016 262, 2017 406, 2018 524, 2019 457, 2020 717, 2021 297, 2022 502, 2023 505, 2024 410,
2025 363, 2026 99. n = 11 year cells.
Produced by: `corpus/build.py:448,465-466` → `reports/stage_a1/corpus.json` `events_per_year`,
which reads 263/409/531/462/728/298/504/508/418/365/99.
*Locator note: the printed table sums to **4,542**, not 4,585; the JSON table sums to 4,585. The
gap is exactly the 43 rows ADR-013 says the composite natural key silently merged. `git diff
ccc9b13 cb17046 -- reports/stage_a1/corpus.json` shows the printed numbers are the superseded
pre-fix values. Also affected: `DECISIONS.md:148-149` ("717 qualifying events in 2020 against 297
in 2021") and `REGISTRATION.md:702-704` ("257 in 2018" against the JSON's 256).*

### Rank 3 — MUST-VERIFY. What the verdict is attributed to
> "Annualized tracking error came in at **9.993 percent** across **2,869.9 effective independent
> periods from 2,581 sessions**, and **that tracking error is the whole of the 49.35**. The period
> count worked in the design's favour: the variance inflation of 0.899 is below one, so effective
> periods exceeded raw sessions. Nothing about the sample size caused this verdict."

`REGISTRATION.md:844-848` (Section 17.3); same at `progress.md:35-38`, `DECISIONS.md:294-298`.
Figures: TE 9.9933 %, N_eff 2,869.9, N 2,581, VIF 0.8993, sd 62.9519 bp.
Produced by: `power/dispersion.py:151-192`, `power.json` series[0].

### Rank 4 — MUST-VERIFY. Book width against effective width
> "The value-weighted book holds a mean of **71.9 names and behaves like 29.7 effective names**,
> because the heaviest name carries **14.9 percent** of the book and the heaviest five carry
> **33.8 percent**."

`REGISTRATION.md:839-842`; also `progress.md:32-34`, `REGISTRATION.md:749`, `DECISIONS.md:296-297`.
Figures: 71.909 (mean width), 29.731 (effective names), 0.149323, 0.337911. n = 2,581 sessions.
Produced by: `portfolio/build.py:59` (`series.mean_width()` → 71.909) and
`portfolio/returns.py:118-124,217,231` (`book_effective_names` → 29.731).
*Locator note: the two numbers are computed on different books. `mean_width()`
(`membership.py:46-54`) counts every name in the book on non-empty sessions, before the 13,750
`not_priced` name-sessions are dropped; the effective-names and weight-share diagnostics are
computed on the surviving `priced` book. The dispersion store's own `book_width` column, written
at `returns.py:210` as `len(priced)`, gives `book_width_mean = 66.93` for the same 126-session
value-weighted series (`power.json` series[0], and reproduced from `var/insider_dispersion.db`).*

### Rank 5 — MUST-VERIFY. The cost claim
> "53 quarterly SEC structured Form 345 data sets covering 2013q1 to 2026q1, retrieved in **214
> wire requests** totalling **2.78 GB** with **zero non-200 responses** under an 8 per second
> throttle against the SEC's stated 10 per second ceiling. **Zero dollars were spent. No paid API
> was used.**" … "The cache on disk is 2,783,280,665 bytes, which equals the wire total exactly,
> so nothing was fetched twice."

`REGISTRATION.md:827-833` (Section 17.2); also `progress.md:23-27`, `progress.md:144-146`.
Figures: 214, 2,783,280,665 bytes, 0 non-200. n = 684 ledger records.
Produced by: `ledger/fetch.py` + `edgar/client.py` → `ledgers/fetch.jsonl` (untracked).
*Locator note: verified at read time from the untracked ledger — 214 `wire` and 470 `cache`
records, all 684 with status 200, wire bytes summing to exactly 2,783,280,665, and `du -sb
cache/` returning exactly 2,783,280,665 across exactly 214 files. Wire breakdown: 53 DERA
`form345.zip`, 53 full-index, 82 per-filing, 25 submissions, 1 other.*

### Rank 6 — MUST-VERIFY. The stated session cost
> "**Cost, measured rather than asserted.** The commit record puts Stage A.1 at about 51 minutes
> of session wall clock, 18:20 to 19:11, and Stage Z.1 at about 20 minutes. The Z.1 brief records
> five hours. The commit record cannot confirm that figure, which presumably counts operator time
> between stages that this repository does not observe."

`progress.md:115-119`. Read against the ETA table at `progress.md:196-205`, whose "Actual" column
reads 5, 10, 4, 4, 14, 20, 32 and 22 minutes, and whose header (`progress.md:192-193`) says
"Timings are wall clock, session start 18:20 UTC, boundaries taken from commit timestamps where
one exists."
Figures: 51 min claimed; the eight task actuals sum to **111 min**. n = 7 commits.
Produced by: the git commit record — 18:34:56, 18:38:50, 18:47:16, 19:11:45, 19:11:45, 19:11:55,
23:24:15 (local −07:00).
*Locator note: three of the eight tasks (5, 6, 7) share the same two commit timestamps ten seconds
apart, so their 20/32/22-minute actuals cannot come from commit boundaries. The gap from the last
A.1 commit to the Z.1 commit is 4 h 12 min, not 20 minutes.*

### Rank 7 — MUST-VERIFY. The secondary that would have changed the verdict
> "On the identical names, the equal-weighted book holds **71.9 and behaves like 66.9**, with
> tracking error of **6.86 percent** and an MDE of **34.29 bp per month, which would have fired
> DEGRADED**."

`REGISTRATION.md:852-854` (Section 17.4); also `progress.md:42-46`, `DECISIONS.md:318-321`,
`REGISTRATION.md:764-767`, `REGISTRATION.md:715`.
Figures: 34.2897 bp, TE 6.8556 %, effective names 66.925, N_eff 2,798.1. n = 2,581.
Produced by: `power.json` series[3], `portfolio.json[3]`.
*Locator note: 34.29 sits inside the DEGRADED band (20, 40], so the "would have fired DEGRADED"
statement is checkable directly against `section0.py:62`. The claim that the equal-weighted book
holds "the identical 71.9 names" is checkable against `portfolio.json` — both 126-session rows
carry `book_width_mean 71.909` and identical `dropped` maps.*

### Rank 8. The net band the MDE is read against
> "Against the decayed gross band of 30 to 40 bp per month, the net band at the six-month hold is
> **13.3 to 34.7 bp per month**. `insider.cost` computes this rather than asserting it."

`REGISTRATION.md:420-422`; the band restated at `REGISTRATION.md:736` and, rounded to "13 to 35",
in the closure language at `REGISTRATION.md:815`, `progress.md:16-17`, `DECISIONS.md:291`.
Produced by: `cost.py:48-57`, `power.json` `net_band_bp_per_month [13.3333, 34.6667]`.
*Locator note: the band's low end pairs the pessimistic 100 bp round trip with the weak gross and
its high end pairs the optimistic 32 bp with the strong gross; `cost.py:50-54` discloses exactly
this. Section 8 (`REGISTRATION.md:409-411`) names the pessimistic bar as primary, under which the
net band would be 13.3 to 23.3.*

### Rank 9. The attrition funnel
> "| Intake, non-derivative transactions on original Form 4 filings in span | 2,876,095 | 100.00% |"
> … "| **`parsed`, qualifying** | **4,585** | **0.16%** |"

`REGISTRATION.md:620-628` plus the sub-reason table at `REGISTRATION.md:632-644`.
Figures: 2,876,095 intake; 8,613 / 2,578,217 / 131,222 / 148,883 / 2,362 / 2,213 / 0 / 4,585.
Produced by: `corpus/build.py` → `corpus.json` `attrition`.
*Locator note: the eight funnel rows sum to exactly 2,876,095 and each sub-reason group sums to its
parent; the percentage column reproduces to two decimals.*

### Rank 10. The scope cost of the universe narrowing
> "**Only 5.8 percent of qualifying-shaped insider purchases happen at a liquid-500 name.** The
> narrowing removes sixteen of every seventeen candidates, and it removes exactly the band the
> literature says carries the signal."

`REGISTRATION.md:656-660`; restated as "94.2 percent" at `REGISTRATION.md:778-779` and
`REGISTRATION.md:893-894`; ADR-004 at `DECISIONS.md:120-125`.
Figures: 148,883 rejected against 9,160 passing. n = 158,043.
Produced by: `corpus.json` attrition (`9,160 = 4,585 + 2,362 + 2,213`).

### Rank 11. The 10b5-1 absence share
> "The 10b5-1 box is **absent for 3,350 of the 4,585 qualifying events**, 73.1 percent, because the
> checkbox became a Form 4 cover-page field only in 2023."

`REGISTRATION.md:662-663`. Produced by `corpus.json` `flag_absent_events: 3350`; the corpus store's
`event.flag_reported` column splits 3,350 / 1,235.

### Rank 12. The filing-lag distribution
> "| p99 | 230 | | max | 1,988 | | mean | 9.52 |" … "73.0 percent file within two calendar days and
> 95.9 percent within four"

`REGISTRATION.md:672-684`. Companion claim in ADR-003: "51.3 percent of qualifying events file
within one calendar day and 95.9 percent within four" (`DECISIONS.md:97-99`).
n = 4,585. Produced by `corpus.json` `lag_distribution` (88 bins, summing to 4,585) and the corpus
store's `lag` table.

### Rank 13. The floor derivation in Section 0.4
> "**The floor is set at 1,000 qualifying events**, which is a book of about 50 names."

`REGISTRATION.md:125-140`, resting on the tables at `REGISTRATION.md:97-100`, `110-113`, `119-123`
and the planning values at `REGISTRATION.md:90-93` (N 2,520, VIF 1.5, N_eff 1,680, sqrt 40.99),
plus "at 1,000 events the expected tracking error is about 4.24 percent and the expected MDE about
27 bp per month" (`REGISTRATION.md:137-138`) and "dropping from 2,520 to 2,016 sessions raises the
MDE by 11.8 percent" (`REGISTRATION.md:143-144`).
Produced by: hand arithmetic in the document; the inversion identity is the same one implemented in
`power/mde.py:38-50`.

### Rank 14. The refusals
> "The Johnsen filter rejected 209 of 773 clusters." … "2,057 transactions carry that state. The
> front truncation it causes is visible in the by-year counts: 449 unclassifiable in 2016, 257 in
> 2017, 257 in 2018, falling to 84 by 2023 as the look-back window fills."

`REGISTRATION.md:693` and `REGISTRATION.md:699-704`.
Produced by: `corpus.json` (`clusters_found 773`, `clusters_rejected 209`,
`unclassifiable_by_year`), `reports/stage_a1/refusals.md`, and the corpus store's `cluster` table
(773 rows, 209 with `rejected=1`).
*Locator note: `unclassifiable_by_year` sums to 2,057 and gives 2018 = **256**, not 257; and 2022
is 296, so the series does not fall monotonically to 84.*

### Rank 15. The mid-hold universe exit
> "This removed 13,750 name-sessions from the primary series, about 7.4 percent of held
> name-sessions."

`DECISIONS.md:262-264` (ADR-009). Produced by `returns.py:190` (`not_priced`), stored in the
dispersion store's `dropped` table and echoed in `power.json.dropped_primary` and
`portfolio.json[0].dropped`.
*Locator note: 13,750 / (71.909 × 2,581) = 7.41 %, so the denominator is the pre-drop held
name-sessions.*

### Rank 16. The mutation exercise
> "**The power module.** Structurally incapable of emitting a mean, enforced by four guards and
> exercised by two of the five mutations."

`progress.md:228-229`; the five mutations and the three defects at `progress.md:265-290` and
`DECISIONS.md:352-396` (ADR-012).
Produced by: `scripts/mutations.py` → `reports/stage_a1/mutations.json` (five records, all with
`guard_failed_when_mutated: true` and `guard_green_when_restored: true`).
*Locator note: `mutations.json`'s `final_suite` field records a pytest **progress line**
(33 dots + `[100%]`), not a pass/fail count, because `summary_line()`
(`scripts/mutations.py:118-122`) fell through to its last-line fallback. The stored artifact
therefore does not itself evidence that the full suite passed; the harness's own exit-code check
(`scripts/mutations.py:178-179`) does.*

### Rank 17. Scaffold size
> "**Scaffold.** uv, ruff, mypy strict, pytest, pre-commit, Makefile. 56 source files. `make all`
> runs clean: ruff, ruff format, mypy strict on 56 files, 106 tests."

`progress.md:216-218`; the commit subject of `672b343` reads "test: 106 tests green".
*Locator note: `pyproject.toml:56` sets mypy `files = ["src/insider", "tests", "scripts"]`, which
is 43 + 11 + 3 = **57** `.py` files. An AST count of the test tree gives **105** collected cases
(96 functions, `test_section0` parametrized ×8, `test_universe_port` ×3), and `mutations.json`'s
final progress line carries 33 dots on an 80-column second row, i.e. 72 + 33 = 105.*

### Rank 18. The disk-pressure correction
> "**A correction to the brief:** it describes this as 2.78 GB on a 14 GB machine. The 2.78 GB is
> right. The host is not: `/home` sits on a 466 GB filesystem with 328 GB available, 26 percent
> used."

`progress.md:146-149`. `df -h /home` at read time returns 466G size, 324G available, 27 % used —
consistent within a week of drift.

### Rank 19. The boundary hashes
> "Both AiTrader hashes re-verified unchanged at closure: `analysis_bars.db`
> `d599ccf0…f924` … `backtest/universe.py` `8188eea0…5529`"

`progress.md:135-138`; the same pair in `port.json` before and after, with `unchanged: true`.
*Locator note: the AiTrader bars file has been written to since (size 7,323,656,192 today against
`port.json`'s 7,320,629,248, mtime 2026-09-03), so this claim is verifiable only as of 2026-08-25.*

### Rank 20. Cross-repository figures (READ-only in this repository)
- "Its realized minimum detectable contrast came in at 0.0512 against a realistic effect band of
  0.01 to 0.05" — `REGISTRATION.md:21-23`, `CLAUDE.md:4-6`, `DECISIONS.md:12-14`.
- "after 415 days of collection and 6.9378 USD of spend" — `REGISTRATION.md:24-25`,
  `CLAUDE.md:7-8`, `DECISIONS.md:15-16`, `progress.md:111-112`.
- "cut NPDExperiment's 427 evaluable days to 125.6 effective, a loss of 70 percent" —
  `REGISTRATION.md:345-347`, `DECISIONS.md:152-155`, `REGISTRATION.md:727-729`.
- "H-F at z 1.668 against a 2.50 bar" — `progress.md:107-108`.
- "concentrated books are what killed H-F at 42 to 66 percent tracking error" —
  `REGISTRATION.md:389-391`, `760-761`, `861-862`, `progress.md:48`, `DECISIONS.md:341-343`.
- "**Eight price-based and signal-based hypothesis families have now been tested** across AiTrader,
  HFExperiment, NPDExperiment and InsiderExperiment. **Zero have produced a positive result that
  survived its own registered bar.**" — `progress.md:103-106`.
- "P26 is the standing reference point. 19,648 trades at minus 1.97 bp per trade, exactly the fee,
  gross edge precisely zero." — `REGISTRATION.md:424-425`, `cost.py:3-5`.
None of these is verifiable inside InsiderExperiment; each needs its source repository.

### Rank 21. Literature figures (external, READ)
- "Cohen, Malloy and Pomorski report 82 bp per month value-weighted on opportunistic purchases over
  1989 to 2007. That replicates at roughly 30 to 40 bp per month on 2008 to 2024 data, a 60 to 70
  percent decay." — `REGISTRATION.md:49-51`, `181-183`.
- "Ozlen and Batumoglu (SSRN 5966834, December 2025, Russell 2000 Form 4) report 70 to 80 percent
  of total alpha dissipating between the transaction date and the following trading day" —
  `REGISTRATION.md:51-55`, `183-186`.
- "Taking sigma at 30 percent annualized, which is a standard figure for the liquid band this
  universe covers" — `REGISTRATION.md:107-108`.
The 30-to-40 decayed band is the number the BLOCKED bar was placed against
(`REGISTRATION.md:57-59`), so it is load-bearing but is not derivable from any artifact here.

### Rank 22. Validation-route figures
> "The ratio of index rows to data set documents is 2.04 to 2.14 and stable across all 53
> quarters, so no quarter is short." / "**Per-filing XML.** Field-by-field validation on a
> 25-document sample … 25 agree, 0 disagree." / "the SEC's current ticker list carries the symbol
> for only 21 of 25 sampled corpus issuers"

`DECISIONS.md:60-66` and `DECISIONS.md:209-210`. Produced by `validation.json` (min ratio 2.043,
max 2.140, 53 quarters; 25/25 agree; 21/25 tickers present; 5,077,629 index rows against 2,440,873
dataset documents).

### Rank 23. The route-cost arithmetic
> "The universe issuers file on the order of two million Form 4 documents across the 2013 to 2026
> span, and at the registered 8 requests per second that is above 69 hours of wall clock."

`REGISTRATION.md:558-560`; ADR-002 at `DECISIONS.md:50-54`, which also says the data sets are "53
files totalling about 750 MB" (`DECISIONS.md:58`) against the 2.78 GB total cache elsewhere.
*Locator note: `validation.json` gives 2,440,873 Form 4 documents in total across all issuers, not
universe issuers; the 53 DERA zips are 53 of the 214 cached responses.*

### Rank 24. The universe port
> "ported by copy from `AiTrader/backtest/universe.py` and verified against the source's own stored
> membership at three formation dates spanning the corpus, 500 of 500 members reproduced exactly at
> each."

`DECISIONS.md:109-112` (ADR-004). Produced by `src/insider/market/port_check.py` and
`tests/test_universe_port.py:87` (parametrized over 2016-04-01, 2021-04-01, 2026-07-01). The live
`var/insider_market.db` holds 62,000 membership rows = 124 formations × 500.

---

## 3. Intervals and test statistics

**There is no confidence interval anywhere in this repository, and no p-value or realized test
statistic.** This is a designed property, not an omission: Stage A.1 computes only second moments
and Stage B was never written (`REGISTRATION.md:483-488`, `REGISTRATION.md:769-774`). A grep of
`REGISTRATION.md`, `DECISIONS.md`, `progress.md`, `CLAUDE.md` and `reports/stage_a1/refusals.md`
for "confidence interval", "95 %", "p-value", "p = 0.", "CI", "t-stat", "z-stat" returns no hit.

The test-statistic-shaped quantities that do appear:

| Quantity | Value | file:line | Stated estimator / test | n | Data structure |
|---|---|---|---|---|---|
| Critical value | t = 2.0, two-sided | `REGISTRATION.md:478-480`; `config.py:147` | **Registered, not estimated.** Applied identically to A.1 power and (had it run) B inference | — | scalar constant |
| Monthly standard error, primary | 24.68 bp | `REGISTRATION.md:717-719`; `power.json` `standard_error_monthly_bp 24.6771` | `21 * sd_daily / sqrt(N_eff)` (`power/mde.py:38-50`) | N_eff 2,869.9 from 2,581 sessions | centered daily series in `var/insider_dispersion.db` |
| Daily excess-return SD | 62.95 bp | `REGISTRATION.md:717`; `power.json` `sd_daily_excess_bp 62.9519` | Sample SD, ddof 1 on an already-centered series (`dispersion.py:151-160`) | 2,581 | same |
| Annualized tracking error | 9.993 % (EW 6.856 %, 21-sess 15.703 %, 63-sess 11.827 %) | `REGISTRATION.md:712-715`, `844` | `sd * sqrt(21*12)` (`dispersion.py:179`) | 2,581 / 2,513 / 2,563 | same |
| Newey-West variance inflation | 0.899 primary; 0.9667, 0.8606, 0.9224 for the other three | `REGISTRATION.md:712-715`, `847`; `DECISIONS.md:158-160` | Bartlett kernel `1 + 2*sum_k (1 - k/(L+1)) * rho_k` at registered lag 21 (`dispersion.py:104-120`) | as above | same |
| NW lag sensitivity | MDE 50.19 / **49.35** / 49.11 / 49.53 at lags 5 / 21 / 63 / 126 | `REGISTRATION.md:721-723`; `power.json` `newey_west_grid` | Same estimator at the registered grid `(5,21,63,126)` | 2,581 | same |
| Autocorrelations | lag 1 0.00645, lag 5 −0.03824, lag 21 0.01029 (primary) | `power.json` series[0]; summarized in prose at `REGISTRATION.md:725-727` | `rho_k` on the centered series (`dispersion.py:92-101`) | 2,581 | same |
| Portfolio-benchmark correlation | 0.904 value-weighted, 0.953 equal-weighted | `REGISTRATION.md:749-750` | `np.corrcoef` on the two daily return series (`returns.py:224-226`) | 2,581 | `portfolio.json` diagnostics |
| Effective names (inverse Herfindahl) | 29.7 VW, 66.9 EW | `REGISTRATION.md:749-752` | `1 / sum(p_i^2)` on the daily weight vector, averaged over sessions (`returns.py:118-124`) | 2,581 | `portfolio.json` diagnostics |
| Planned inference (never run) | day-clustered SEs, Newey-West Bartlett at lag 21, grid 5/21/63/126, single pre-registered contrast, no family correction | `REGISTRATION.md:452-480` | Registered for Stage B | planned N 2,520 | — |
| Cross-repository statistic (READ) | "H-F at **z 1.668** against a **2.50** bar" | `progress.md:107-108` | Not produced here; belongs to HFExperiment | not stated | not present in this repo |

Registered but unfired: verdict rows V1 to V4 (`REGISTRATION.md:437-440`) each name a
significance test at t 2.0 that was never computed. `REGISTRATION.md:771-774` states plainly that
V3 (a measured null) did not fire and V7 (unpowered) did.

---

## 4. Provenance claims

Each entry gives the claim verbatim, its location, the commit or artifact it names, and what would
have to be true. The commit record is: `fbfc74e` 2026-08-25T18:34:56−07:00, `398755b` 18:38:50,
`ccc9b13` 18:47:16, `cb17046` 19:11:45, `672b343` 19:11:45, `d8b81f1` 19:11:55, `12d9fd3`
23:24:15. The fetch ledger runs 01:35:18Z to 02:06:24Z, i.e. 18:35:18 to 19:06:24 local.

**P1.** "Registered 2026-08-25, Stage A.1. Every parameter in this document is fixed before any
measurement runs. **Section 0 is committed before Task 4 computes anything**, so the answer cannot
be read against a threshold its own measurement could see. Changing a registered value after that
commit requires a numbered amendment in Section 17 carrying its own evidence."
`REGISTRATION.md:5-9`. Commit named: none explicitly; `progress.md:223-224` names the time.
What would have to be true: `REGISTRATION.md` lines 1-157 unchanged from `fbfc74e` to HEAD, and
`fbfc74e` earlier than every measurement artifact.
*Locator note: `git diff fbfc74e HEAD -- REGISTRATION.md` is a single hunk `@@ -157,3 +157,740 @@`,
purely additive. Section 0 and everything before it is byte-identical at the anchor.*

**P2.** "**REGISTRATION.md.** Section 0 committed at 18:34, before Task 4 computed anything.
Sections 1 to 16 committed at 18:38. **Every parameter frozen first.**"
`progress.md:223-224`. Commits named by time: `fbfc74e` (18:34:56) and `398755b` (18:38:50).
What would have to be true: no measurement preceded 18:34:56, and no registered parameter changed
after it.
*Locator note: `src/insider/config.py` at `fbfc74e` is byte-identical to HEAD once two lines are
removed (md5 of the non-`benchmark_id` lines matches HEAD exactly). The first SEC wire request is
timestamped 18:35:18 local, 22 seconds after `fbfc74e`. `reports/stage_a1/port.json` was committed
in `398755b` (18:38:50) but the market port that produced it is recorded in the evidence ledger at
18:36:26, i.e. between the two commits — the market data was copied before Sections 1 to 16 were
committed, though every enforced parameter it used was already frozen at 18:34:56.*

**P3.** "**Section 15. Results.** Filled by Task 4 and Task 5. **Empty at the time Section 0 was
committed at 18:34 on 2026-08-25.**"
`REGISTRATION.md:589-590`. Commit named by time: `fbfc74e`.
What would have to be true: Section 15 absent from `fbfc74e`. Confirmed by the additive diff in P1;
Section 15 first appears in `d8b81f1` (19:11:55).

**P4.** "Section 7 chose value-weighted to get a wide book rather than a concentrated one … the
registration named value-weighted as primary **before any number was visible**."
`progress.md:47-48`, `REGISTRATION.md:761-762`, `REGISTRATION.md:856-858`.
What would have to be true: `primary_weighting="value_weighted"` present at `fbfc74e`, and no
tracking-error or MDE figure computed before it.
*Locator note: `config.py` at `fbfc74e` already carries `primary_weighting="value_weighted"` and
`secondary_weighting="equal_weighted"`; the first `power_gate` evidence record is 18:51:14 local.*

**P5.** "It was registered as the secondary weighting in Section 7 and labelled
non-verdict-bearing in Section 10, **both before any number was visible. It is not promoted.**"
`REGISTRATION.md:856-858`; also `progress.md:45-46`, `DECISIONS.md:323-326`.
What would have to be true: Sections 7 and 10 committed at `398755b` (18:38:50) and unchanged
since; the equal-weighted MDE first computed after that.
*Locator note: Sections 1 to 16 arrive in `398755b`; the `git diff fbfc74e HEAD` hunk boundary
means nothing before line 157 moved, and `git show --stat d8b81f1` shows 211 insertions with 2
deletions in `REGISTRATION.md` — the two deletions need locating before this is settled.*

**P6.** "## Section 16. Amendments — **None in force.** Section 0 fired BLOCKED, so no amendment
can authorize Stage B."
`REGISTRATION.md:798-800`. Read against `REGISTRATION.md:8-9` ("Changing a registered value after
that commit requires a numbered amendment in Section 17 carrying its own evidence").
What would have to be true: no registered value changed after `fbfc74e`.
*Locator note: one registered field did change. `git diff fbfc74e 672b343 -- src/insider/config.py`
removes two lines — the declaration `benchmark_id: str` and the value
`benchmark_id="U-LIQ-500-VW"` — at 19:11:45, i.e. after the corpus was built (18:47), after the
power gate fired (18:51), and with no numbered amendment. Section 5's benchmark
(`REGISTRATION.md:351-357`) is prose only after that commit. The likely cause is the
config-enforcement guard, which fails on any field with no enforcement site
(`config.py:3-6`).*

**P7.** "`insider.power` is structurally incapable of emitting a mean. It reads
`var/insider_dispersion.db`, which holds daily portfolio excess returns already centered on their
own mean, and the mean itself is never written there. The raw series lives in
`var/insider_sealed.db` and `insider.eval.evaluator` is its only permitted reader.
`tests/test_guards.py` fails when any other module names it."
`CLAUDE.md:20-24`; also `REGISTRATION.md:155-159`, `DECISIONS.md:165-193` (ADR-006),
`REGISTRATION.md:490-493`.
What would have to be true: the stored dispersion series sums to zero; no module outside the
permitted set names `SEALED_DB`; `DispersionStats` and `MdeResult` carry no first-moment field.
*Locator note: the four stored series sum to −1.4e-16, 1.7e-16, −2.9e-16 and −7.5e-17 at read
time. `mutations.json` records two mutations aimed at exactly this property, both caught. The
sealed store was not opened by this audit.*

**P8.** "**The verdict stands on the registered primary.** The equal-weighted 34.29 bp would have
fired DEGRADED. It is a labelled non-verdict-bearing secondary, registered as such before
measurement, and it is not promoted."
`progress.md:261-263`; ADR-011 at `DECISIONS.md:314-338`.
What would have to be true: the primary/secondary labels predate the numbers (P4, P5) and no
document reports the verdict on the secondary.

**P9.** "**No systemd unit was ever installed by this repository.** Stage A.1 was a one-shot batch,
not a scheduled collector, so there was nothing to disable or stop. Verified against
`~/.config/systemd/user`, `/etc/systemd/system`, `systemctl --user list-units --all`,
`systemctl --user list-timers --all`, and `crontab -l`. None matched. Nothing remains scheduled."
`progress.md:127-131`; ADR-010 at `DECISIONS.md:303-306`.
What would have to be true: no unit or timer naming this repository exists on the host. Checkable,
but only as of today, not as of 2026-08-25.

**P10.** "Both AiTrader hashes re-verified unchanged at closure … `analysis_bars.db`
`d599ccf0b8d70a5b2b8c7fca2461f0d6e0e09f0e8c990405f7c25e3fa767e924` … `backtest/universe.py`
`8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529`"
`progress.md:135-138`; the same values before and after in `reports/stage_a1/port.json` with
`unchanged: true`; the read-only-boundary rule at `CLAUDE.md:53-58`.
What would have to be true: the two files carried those digests on 2026-08-25 and nothing under
AiTrader other than these two paths was read, and `news_experiment.db` was never opened.
*Locator note: `analysis_bars.db` is now 7,323,656,192 bytes with mtime 2026-09-03, against
`port.json`'s recorded 7,320,629,248, so the digest is no longer reproducible; `universe.py` has
mtime 2026-07-26 and is unchanged. `paths.py:36-40` restricts the source paths to exactly these two
and names no other AiTrader file.*

**P11.** "**Section 12. The operator prior, reserved** … `[ EMPTY. The operator writes a number
here himself, before Stage B runs. ]` … **This slot blocks Stage B while it is empty.**
`insider.registration_check.require_operator_prior` raises `OperatorPriorMissing` rather than
warning. … **The assistant's prior, recorded beside it and never inside it: 0.12.**"
`REGISTRATION.md:497-513`; closure record at `REGISTRATION.md:876-885` and `progress.md:93-99`.
What would have to be true: the marker is still present and unfilled at the anchor, and the
assistant's 0.12 lives outside the slot. Both are checkable in `REGISTRATION.md` and
`src/insider/registration_check.py`; `config.py:153` carries `assistant_prior=0.12`.

**P12.** "**ADR-008.** … **Impact on the corpus.** One transaction moved from
`insufficient_history` to `routine`. The qualifying set is unchanged at 4,585 … and the minimum
detectable effect is unchanged at 49.35 bp per month. The defect was in the reported composition,
not the sample."
`DECISIONS.md:245-249`.
What would have to be true: exactly one label moved and neither 4,585 nor 49.35 changed.
*Locator note: `git diff ccc9b13 cb17046 -- reports/stage_a1/corpus.json` moves
`filtered_routine/insufficient_history` 2058 → 2057 and `filtered_routine/routine` 155 → 156, and
`routine_labels` 2472 → 2471 and 159 → 160 — one transaction, as claimed. The same commit also
rewrites all eleven `events_per_year` cells (see Rank 2), which ADR-008 does not mention;
ADR-013 (`DECISIONS.md:400-416`) covers that separately.*

**P13.** "Records only. No statistic computed, no alpha read, no sealed store opened, no request
sent, no result changed. The A.1 power verdict stands exactly as fired."
`progress.md:9-10`; the same sentence at `REGISTRATION.md:806-808` and in the Z.1 brief logged
verbatim at `progress.md:163-165`.
What would have to be true: `12d9fd3` touches only `DECISIONS.md`, `REGISTRATION.md` and
`progress.md`, and no artifact mtime falls inside the Z.1 window.
*Locator note: `git show --stat 12d9fd3` lists exactly those three files, 408 insertions and 0
deletions. Every file under `var/`, `ledgers/`, `cache/` and `reports/` has an mtime of
2026-08-25 19:10 or earlier.*

**P14.** "the assistant's 0.12 sitting beside it is not that number" / "**the calibration ledger
still holds zero independently formed entries.**"
`progress.md:305-306`, `REGISTRATION.md:882-885`.
What would have to be true: a claim about the program's calibration ledger, which lives outside
this repository. Not verifiable here.

**P15.** "The Z.1 brief records five hours. The commit record cannot confirm that figure."
`progress.md:117-118`. See Rank 6. The observable gap between the last A.1 commit (19:11:55) and
the Z.1 commit (23:24:15) is 4 h 12 min.

---

## Live-repository access log

Purpose of access: git history and provenance (`log`, `show`, `diff`, `rev-parse`,
`check-ignore`), and untracked/gitignored data that exists only in the working tree
(`var/*.db` except the sealed store, `ledgers/*.jsonl`, `cache/` sizes only, `reports/` mtimes,
`_CLOSED_DO_NOT_RUN_HERE`). No repository script was executed. Nothing was written. `.env` was not
opened. `var/insider_sealed.db` was **not** opened.

**`git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain` before first
access — 2026-09-04T05:29:24Z:**

```
```
(empty output, exit 0 — clean working tree)

**`git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain` after last
access — 2026-09-04T05:33:28Z:**

```
```
(empty output, exit 0 — clean working tree, unchanged)

Untracked-but-ignored entries present at both reads (`git status --ignored --porcelain`):
`.env`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `.venv/`, `_CLOSED_DO_NOT_RUN_HERE`,
`cache/`, `ledgers/`, `var/`, and eight `__pycache__/` directories. `_CLOSED_DO_NOT_RUN_HERE` is
excluded via `.git/info/exclude:7`, is dated 2026-09-02, and states it was written after a session
was opened in the closed repository by mistake. It is not an experiment artifact and it is not
pre-existing dirt of the kind COMMON_RULES lists; it is reported here for the record.

All untracked-data figures in this inventory were read at **2026-09-04 05:29–05:33 UTC** and are
UNANCHORED: they sit outside the anchored SHA and may have changed after 2026-08-25, though every
mtime observed falls inside the 2026-08-25 session window.

Scratch computation ran under
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/2c6a58bc-6f69-48c9-a930-b20684f1e1e4/scratchpad/work/agentC`
with the audit venv; no repository script was copied or executed.
