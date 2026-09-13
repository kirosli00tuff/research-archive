# NPDExperiment — provenance verification (Agent C, referee)

Repository: `NPDExperiment`
Anchored SHA: `2d3d0aebf977fb2821ec78c25b370c84ec055920` (main, 2026-08-25)
Live repo used read-only for git objects and for the untracked ledgers under `ledgers/`
and the untracked stores under `var/`. Document text read from
`SNAP/NPDExperiment/` (tracked, anchored). Live HEAD equals the anchored SHA.
Ledger and `ls` reads: 2026-09-04T18:21Z – 18:31Z (UNANCHORED — those files are untracked).

**Method.** For every registration claim I located the commit that first contains the
bar, parameter, map, prior or rule, took its author date, and compared it against the
first moment data of the relevant kind existed (first billed API call in
`ledgers/spend.jsonl`; first attempt row in `ledgers/evidence.jsonl`; the mtime of the
sealed forward-return store). For every parameter I diffed the registration files across
all eleven commits and checked each change against the amendment that claims to record it,
including whether the amendment's account of *the data that existed at the time* matches
the ledgers.

---

## 0. The timeline everything is measured against

All eleven commits are 2026-08-25, author date == committer date on every one, so the
history has not been rewritten after the fact. `git rev-list --count HEAD` = 11.

| UTC | event | source |
|---|---|---|
| 16:29:42 | B.0 source extraction begins (pre-extract hash written) | `var/source_hashes_before.txt` mtime (untracked) |
| **16:39:00** | **`64b7d41` the binding registration** — all 17 sections, Section 0 map, Section 9 power, Section 10 verdict table | `git log` |
| 16:54:33 | `var/npd_sealed.db` and `var/npd_fit.db` written (outcome data first exists) | mtime (untracked) |
| 17:06:55 | `943ba05` B.0 data layer, mock collector, `eval/evaluator.py` created, seed 20260825, control tolerance 0.02, prompt digest `9a174e01…` | `git log`, `git show` |
| **17:10:48.475** | **first billed API call** (calibration, `low`) | `ledgers/spend.jsonl` row 1 |
| 17:11:12.483 | second calibration call (`minimal`) | `ledgers/spend.jsonl` row 2 |
| 17:12:23 | `3c2a152` Amendments 1 and 2 (`send_temperature=False`, `reasoning_effort="minimal"`) | `git show` |
| 17:12:52.123 | first gate call | `ledgers/spend.jsonl` |
| 17:17:32 | `c4da18c` Amendment 3 (`reasoning_effort_ladder`) — 26 gate attempts / 13 days exist | `git show` + ledger |
| 17:19:11 | `f8304d9` amendments recorded in `CLAUDE.md` | `git show` |
| 17:30:37.688 | last attempt under the superseded prompt | `ledgers/evidence.jsonl` |
| *17:30:37 → 17:35:44* | **306 s with no row in either ledger** (Amendment 4's strict-schema measurement) | both ledgers |
| 17:35:37 | `250bc8f` Amendments 4 and 5 (ladder re-tuned, prompt re-frozen `7e6f3d68…`, usage on rejects) — 74 gate attempts / 29 days exist | `git show` + ledger |
| 17:35:44.085 | first attempt carrying `7e6f3d68…`, 7 s after the commit | `ledgers/evidence.jsonl` |
| 19:46:42.338 | last gate call, 920 gate rows, 6.937784 USD | `ledgers/spend.jsonl` |
| 19:48:04 | `02b8560` B.1 complete, Section 0 GO | `git log` |
| 20:10:48.471 | B.2 runs | `reports/stage_b2/evaluation.md:3` |
| 20:13:28 | `2c6d683` evaluation committed **together with** the Section 13 prior fill, `run_b2`, `report.py`, ADR-010/011 | `git show --name-status` |
| 20:26:58 | `2d3d0ae` closure, Amendments 6 (POST-READ) and 7 (VOID), ADR-012/013/014 | `git log` |

**The single most useful structural fact.** Between `64b7d41` and HEAD,
`git diff -U0 64b7d41 2d3d0ae -- REGISTRATION.md` deletes exactly two things: the
Section 13 Amendment-0 placeholder and the line `None yet. Amendment 0 is reserved in
Section 13 and is empty.` Everything else is an append. `DECISIONS.md` and `progress.md`
have **zero** deleted lines across the entire history. Sections 0, 1, 5, 6, 8, 9, 10 and 11
of the registration are byte-identical from the pre-call commit to the anchor. No bar, no
threshold, no horizon, no universe, no alpha, no n target and no cost figure in the
registration was edited after data existed.

---

## 1. Registration claims table

| # | claim (verbatim, trimmed) | file:line | commit named | commit found / date (UTC) | data first existed | status |
|---|---|---|---|---|---|---|
| R1 | "Written 2026-08-25, before the first call. Every number below is derived, not assumed." | `REGISTRATION.md:3` | none | `64b7d41` 2026-08-25T16:39:00Z — full 17-section registration present | first billed call 17:10:48.475Z (`ledgers/spend.jsonl`), 31 min later | **SUPPORTED** |
| R2 | "Committed before any call goes out. Coverage decides this verdict and nothing else does." (Section 0 map: GO ≥ 90 pct, DEGRADED 70–90, BLOCKED < 70) | `REGISTRATION.md:11`, bars `:14-18` | none | `64b7d41` 16:39:00Z; `git diff 64b7d41 2d3d0ae -- REGISTRATION.md` touches nothing in lines 5–67; `section0.py` differs only by `Enum`→`StrEnum` | 17:10:48Z | **SUPPORTED** |
| R3 | "Written now, before any output exists." (Section 10 verdict table, three outcome rows) | `REGISTRATION.md:268`, rows `:270-275` | none | `64b7d41` 16:39:00Z, unchanged to HEAD | 17:10:48Z | **SUPPORTED** |
| R4 | "These numbers are produced before a cent is spent, from the derived day count." + "MDE = 2.0 * 0.185695 / sqrt(432) = 0.01787" + the eight-cell grid | `REGISTRATION.md:200-201`, `:212`, `:231-245` | none | `64b7d41` 16:39:00Z, verbatim; unchanged to HEAD | first spend 17:10:48Z; outcome store `var/npd_sealed.db` written 16:54:33.875Z, i.e. *after* the commit | **SUPPORTED** |
| R5 | "this hypothesis was not selected from a sweep. It was written before any output existed." | `REGISTRATION.md:188-190` | none | `64b7d41` 16:39:00Z; Sections 1, 5, 6, 8 unchanged to HEAD | 17:10:48Z | **SUPPORTED** (the *identity* of the best baseline is post-hoc by design, disclosed at `DECISIONS.md:193-206`) |
| R6 | "The operator's registered prior. **Recorded 2026-08-25, before any module touched the sealed store.**" | `REGISTRATION.md:343-344` | none | fill first appears in `2c6d683` 20:13:28Z — the same commit as `reports/stage_b2/evaluation.md`, and 2 min 40 s after the run stamp `20:10:48.471` at `evaluation.md:3` | all outcome data existed by 19:46:42Z | **UNVERIFIABLE from git.** The ordering rests on code, not on a git object: `require_amendment_zero()` / `amendment_zero_filled()` existed at `943ba05` 17:06:55Z (before the first call) and refuse to run while the `[ EMPTY.` marker is present. That guard was *strengthened* in the same commit as the run (marker-absence → a parsed number in [0,1]). No finding: the authors disclose the prior was adopted, not independent, and that the experiment yields no calibration evidence (`REGISTRATION.md:351-360`). |
| R7 | "Prompts freeze at B.0b. The frozen prompt hash is recorded in `reports/stage_b0b/mock_run.md` and every replay uses it byte for byte." | `REGISTRATION.md:374-375` | none | `9a174e01…` first in git at `943ba05` 17:06:55Z, before the first call | 17:10:48Z | **PARTIAL.** True of the original freeze. `mock_run.md` was then overwritten in place at `250bc8f` 17:35:37Z, replacing the digest with `7e6f3d68…` and re-stamping "Generated" to 17:34:50Z — i.e. the B.0b artifact a reader sees was generated 22 min after the first live call. Amendment 4 records the re-freeze and its reason (`REGISTRATION.md:589-598`), so the change is amended; the superseded digest survives only in git. |
| R8 | "The corrected template digest is `7e6f3d68…` and every B.3 replay uses these bytes." + "Supersession now keys on the prompt digest." | `REGISTRATION.md:591-597`, `:599-603` | none | `250bc8f` 17:35:37Z; earliest evidence row carrying the digest 17:35:44.085Z, 7 s later | — | **SUPPORTED.** All 883 current-procedure rows carry it; no other digest appears on any row that has the field; the 415 stored days all come from those rows. |
| R9 | "The best baseline is the one with the highest mean daily rank IC inside the evaluable window, **designated after the fact**" (ADR-010) | `DECISIONS.md:193-206` | none | `2c6d683` 20:13:28Z, same commit as the evaluation; ADR's own first line says "Accepted, 2026-08-25, at B.2" | — | **SUPPORTED as disclosed.** Post-hoc, labelled post-hoc, in the commit that ran it. |
| R10 | "**ADR-007 registered this failure mode as a risk before collection. It was not discovered afterwards.**" | `REGISTRATION.md:704-705` | none | ADR-007 present in `64b7d41` 16:39:00Z; `DECISIONS.md` has zero deleted lines over the whole history, so the text is unchanged | 17:10:48Z | **SUPPORTED** |
| R11 | Amendment 6 "POST-READ … Arrived after it"; Amendment 7 "VOID … Arrived after the read" | `REGISTRATION.md:624-631`, `:661-675`; ADR-012/013 `DECISIONS.md:231-259` | none | both first appear in `2d3d0ae` 20:26:58Z, after the evaluation commit `2c6d683` 20:13:28Z | — | **SUPPORTED.** The labels match the git order. Amendment 7 would have added 10- and 20-session descriptive horizons; `config.py:85-86` holds only 5 and 1 and no other horizon appears in the code or reports, so the void was honoured. |
| R12 | "\| registered tolerance \| 0.02 \|" … "sits inside the registered tolerance of zero" | `reports/stage_b2/evaluation.md:40`, `:42-43` | none | the figure first enters git as a code default `assert_control_collapsed(verdict, tolerance: float = 0.02)` at `943ba05` 17:06:55Z; the module constant with the comment "# The registered tolerance for the pipeline validity gate" is added at `2c6d683` 20:13:28Z (`evaluator.py:551-553`) | threshold predates the first call | **NOT_SUPPORTED as "registered".** `toleran` and a bare `0.02` appear nowhere in `REGISTRATION.md` at any commit. Section 7's registered rule is qualitative: "The rank IC must collapse toward zero. A non-zero result stops everything." (`REGISTRATION.md:173-175`). → **DRAFT-P-3** |
| R13 | "It produced the two calibration calls and the **26** superseded attempts, and **zero** of the 415 stored rankings." | `REGISTRATION.md:779-780` | none | added at `2d3d0ae` 20:26:58Z | — | **NOT_SUPPORTED in part.** The "zero of 415" half verifies. The count is 74, not 26. → **DRAFT-P-4** |
| R14 | "\| evidence ledger \| every attempt, with the raw response verbatim \|" / "\| spend ledger \| every billed call \|" | `REGISTRATION.md:772-773` | none | added at `2d3d0ae` 20:26:58Z | — | **NOT_SUPPORTED.** The ≥8 live strict-schema calls behind Amendment 4's own table have no row in either ledger. → **DRAFT-P-2** |
| R15 | "Its hash and mtime are unchanged from the B.0 build, because it was opened read-only." (the sealed store) | `progress.md:168-169` | none | no commit records any hash of `var/npd_sealed.db`; the store is untracked | — | **PARTIAL.** mtime 2026-08-25T16:54:33.875Z (read 2026-09-04T18:30Z) precedes B.1 (19:46Z) and B.2 (20:10Z), consistent with the claim. The *hash* half is unverifiable: no pre-image hash was ever recorded in the repository. |
| R16 | "`backtest/universe.py` sha256 before the extract … after the extract … unchanged: **True**" | `reports/stage_b0/build.md:9-12` | none | `build.md` added at `943ba05`; `var/source_hashes_before.txt` (untracked, mtime 16:29:42Z) records the before-hash for `universe.py` only | — | **PARTIAL.** No hash of the second read-only path (`analysis_bars.db`) is recorded on either side, so "two read-only paths were opened and no others" is evidenced for one of the two. |
| R17 | "Nothing is pushed to any public remote." | `CLAUDE.md:56` | none | `origin` = `https://github.com/kirosli00tuff/NPDExperiment.git`; `origin/main` == HEAD == the anchored SHA; `.git/refs/remotes/origin/main` written 2026-08-29T18:45:18Z, **after** the anchor | — | **UNVERIFIABLE.** The repository was pushed to a GitHub remote four days after closure. Whether that repository is public cannot be determined from here and I did not attempt a network read. Post-anchor event; recorded, not raised. |

---

## 2. Parameter changes after data existed

Every row is a change to a frozen parameter, bar or rule made at or after 17:10:48Z, the
moment the first billed call created data.

| # | parameter | from → to | commit / UTC | data existing at that commit | dated amendment | status |
|---|---|---|---|---|---|---|
| C1 | `temperature` sent | `temperature=0.0` sent → `send_temperature=False` | `3c2a152` 17:12:23Z (`config.py:98`) | 2 calibration calls (17:10:48, 17:11:12), 0.030522 USD | **yes** — Amendment 1, `REGISTRATION.md:446-462`, dated, quotes the endpoint refusal verbatim, and Section 12.2 pre-registered exactly this contingency at `REGISTRATION.md:331-337` | **SUPPORTED** (made before the first gate call at 17:12:52) |
| C2 | `reasoning_effort` | `"low"` → `"minimal"` | `3c2a152` 17:12:23Z (`config.py:99`) | the same 2 calibration calls | **yes** — Amendment 2, `REGISTRATION.md:464-500`, with the measured token table; the *selection rule* was pre-registered in Section 12.2 | **SUPPORTED.** Recomputed: 0.027271×432 = 11.7811; 0.003251×432 = 1.4044; 0.8×(10 − 0.030522) = 7.9756. Both calibration rows are in `ledgers/spend.jsonl` at the stated token counts. |
| C3 | `reasoning_effort_ladder` | *(absent)* → `("minimal","low")` | `c4da18c` 17:17:32Z (`config.py:102`) | **26 gate attempts across 13 days**, 10 stored / 16 model_failed; gate spend 0.026807 USD over 10 billed rows | **yes** — Amendment 3, `REGISTRATION.md:502-548` | **PARTIAL.** The amendment is dated and gives its reason, but its account of the data does not match either ledger. → **DRAFT-P-1** |
| C4 | `reasoning_effort_ladder` | `("minimal","low")` → `("minimal","minimal","minimal","minimal","low")` | `250bc8f` 17:35:37Z (`config.py:102-105`) | **74 gate attempts across 29 days**, 37 stored / 37 model_failed; ledger 0.349374 USD | **yes** — Amendment 4, `REGISTRATION.md:550-603` | **PARTIAL.** The free-form arm verifies exactly (29 `minimal` attempts / 12 failed and 19 `low` / 9 failed; 17 of 29 first-attempt compliance). The strict-schema arm (`:573-579`) has no ledger record at all. → **DRAFT-P-2** |
| C5 | prompt template + frozen digest | `9a174e01…` free-form array → `7e6f3d68…` strict JSON schema, 30 enum-constrained slots | `250bc8f` 17:35:37Z (`collect/prompt.py`, `reports/stage_b0b/mock_run.md`) | 74 live attempts | **yes** — Amendment 4, `REGISTRATION.md:589-598`, states the re-freeze, why mock-only verification missed it, and that the sample is recollected in full | **SUPPORTED.** `collect/prompt.py` was untouched between `943ba05` and `250bc8f`, so all 74 superseded attempts did come from the one superseded template. |
| C6 | spend accounting | rejected answers unbilled → `UnparseableResponse` carries usage, logged as `gate` with note `rejected answer` | `250bc8f` 17:35:37Z (`ledger/evidence.py`, `collect/adapter.py`) | 74 attempts; ledger read 0.349374 USD | **yes** — Amendment 5, `REGISTRATION.md:605-622` | **SUPPORTED.** "recorded 0.3494 USD" reproduces exactly against the spend ledger at that instant (39 rows, Σ 0.349374). The "actual 0.6429 USD" is not reconstructible (the usage was discarded) — the authors say so at `:619-622` — but it is internally consistent: 432 × (0.6429 − 0.030522)/29 = 9.122, matching the "9.12 USD" projection at `:579`. |
| C7 | `CLAUDE.md` standing rules | "Three amendments are in force … A parse failure escalates that day to `low` and it stays there" | written `f8304d9` 17:19:11Z, **never updated** (only two commits ever touch `CLAUDE.md`) | at the anchor: seven amendments, and the ladder is 4×`minimal` then `low` | change recorded in Amendment 4 but **not propagated** to the standing-rules file | **PARTIAL.** → **DRAFT-P-5** (S4) |
| C8 | negative-control tolerance | 0.02 as a function default (`943ba05` 17:06:55Z) → module constant `CONTROL_TOLERANCE = 0.02` labelled "registered" | `2c6d683` 20:13:28Z (`evaluator.py:551-553`) | all outcome data | none, and none needed — **the value never changed** | **PARTIAL.** The threshold genuinely predates the data; only the word "registered" is unsupported. → **DRAFT-P-3** |
| C9 | bootstrap block length at the secondary horizon | *(never registered)* → `block = 2 * cfg.primary_horizon_sessions` = 10, applied at h = 1 as well as h = 5 | `2c6d683` 20:13:28Z (`evaluator.py:508`, inside `evaluate_horizon` written in that commit) | all outcome data | none | **Recorded, not raised.** The registration fixes block 10 only as "twice the primary horizon" (`REGISTRATION.md:143-144`) and says nothing about the secondary. A block of 10 at a one-session horizon widens the secondary interval, i.e. it is conservative, and the secondary is subordinate and negative (`evaluation.md:151-153,167-173`). A degree of freedom fixed after the data existed, with no effect that favours the authors. |
| C10 | resampling seed | `seed: int = 20260825` | `943ba05` 17:06:55Z (`evaluator.py:222`); `run_b2`'s own default added at `2c6d683` with the same value | none of the model output existed at 17:06:55Z | n/a | **SUPPORTED.** The seed was fixed before the series it resamples existed, so it cannot have been chosen against the result. |
| C11 | Amendment 0 guard | `amendment_zero_filled` = "the empty marker is absent" → `amendment_zero_prior` = "a number in [0,1] is present" | `2c6d683` 20:13:28Z (`evaluator.py:38-73`), with `tests/test_guards.py` rewritten in the same commit | all outcome data | none | **Recorded, not raised.** A strengthening: the new guard also refuses a section that *claims* a prior without recording one (`tests/test_guards.py`, `test_a_section_that_claims_a_prior_without_recording_one_is_blank`). The replaced test carried its own warning that it must be updated deliberately; git shows it was. |
| C12 | mutation set | five mutations → six (mutation 6, "let the evaluator run with Amendment 0 empty") | `2c6d683` 20:13:28Z (`scripts/mutations.py`, `reports/mutations.md`) | all outcome data | none | **Recorded, not raised.** An added guard, not a relaxed one. The stale summary line "**All five caught and restored: True**" above a six-row table (`reports/mutations.md:14`) is hygiene already recorded in the inventory (§2 item 15). |
| C13 | horizons | proposed 10- and 20-session descriptive secondaries | proposed post-read at `2d3d0ae`, **refused** | all outcome data, read | Amendment 7 VOID, `REGISTRATION.md:661-675` | **SUPPORTED.** Verified not applied: `config.py:85-86` holds 5 and 1; no 10- or 20-session horizon appears anywhere in the code or the reports. |

Parameters checked and found **unchanged** across all eleven commits: panel size 30,
`primary_horizon_sessions` 5, `secondary_horizon_sessions` 1, `bootstrap_resamples`
10,000, `permutation_resamples` 10,000, `t_critical` 2.0, `realistic_effect_band`
(0.01, 0.05), spend cap 10.0, the nine-feature enumeration, the three baselines, the
universe, the window (2024-10-31 → 2026-07-24, 432 days), the Section 0 bars, the
Section 9 power floor 0.01787 and its eight-cell grid, the Section 10 verdict table,
the Section 11 epistemic boundary.

---

## 3. Draft findings

### DRAFT-P-1
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** Amendment 3, the `reasoning_effort_ladder` registered mid-run at `c4da18c`
- **Direction:** neutral (process/provenance hygiene; no verdict figure moves)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED (git objects + both append-only ledgers)
- **Claim challenged (verbatim quote):** "**Raised 2026-08-25, 14 gate calls into B.1. The run was stopped to record this before it went further.** … Across the first 14 live attempts the model failed to return a usable permutation of the 30 labels on 9 of them" — NPDExperiment/REGISTRATION.md:504-509; and "The 7 days stored before this amendment followed the superseded procedure." — NPDExperiment/REGISTRATION.md:538-539; and "The 9 superseded attempts cost 0.0286 USD and that spend still counts against the cap." — NPDExperiment/REGISTRATION.md:543-544
- **Evidence:** `git log` gives `c4da18c` author date 2026-08-25T17:17:32Z. Counting rows with `ts < 17:17:32Z` in `ledgers/evidence.jsonl` (read 2026-09-04T18:25Z, untracked): **26** gate attempts, not 14, across **13** distinct dates, of which **10** ended `stored` and 16 `model_failed`. `ledgers/spend.jsonl` over the same interval holds **10** gate rows summing to **0.026807 USD** (plus the two calibration rows, 0.030522 USD), not "9 … 0.0286 USD". The amendment's own failure breakdown ("ranking omitted or duplicated a label | 5" and "31, 32, 35, or 37 entries | 4", `REGISTRATION.md:513-516`) matches the ledger exactly at the **16th** attempt (17:13:59.708Z), where cumulative failures are 5 label-mismatch + 4 length = 9 and exactly **7** days had stored — so the amendment describes a real snapshot, three and a half minutes before its commit, and mislabels it "14 attempts" while collection continued to 26 attempts before the stop was committed.
- **Recomputation (if any):** inputs `ledgers/evidence.jsonl` (959 rows) and `ledgers/spend.jsonl` (922 rows), read-only line parse, cut at the commit author date; method: count and sum by state and by timestamp; results 26 / 13 / 10 / 16 and 0.026807 USD; cumulative-gate-spend series shows no boundary at 0.0286 (row 10 = 0.026806, row 11 = 0.028186, and row 11 is timestamped 17:17:38Z, after the commit). Tolerance: exact to 6 dp.
- **What would resolve it:** either a corrected amendment giving 26 attempts / 13 days / 10 stored / 0.026807 USD, or a statement that the figures describe the snapshot at which the stop was decided (16 attempts, 9 failures, 7 days stored) rather than the state at the commit. "0.0286" against a ledger reading 0.0268 is consistent with a digit transposition.
- **Confidence:** HIGH — the ledgers are append-only, timestamped to the microsecond, and the commit date is a git object.
- **Invalidated by later commits?:** no — `c4da18c` is an ancestor of the anchor and Amendment 3's text is unchanged at HEAD; Amendment 4 supersedes the *ladder* but not this account of the data.
- **Disclosed by authors?:** no. Amendment 4 states that Amendment 3 was "the wrong diagnosis, correctly recorded" (`REGISTRATION.md:565-567`), which concedes the diagnosis but not the counts. No sample contamination follows: every one of the 415 stored days carries the current digest, so all superseded days were in fact recollected.

### DRAFT-P-2
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** Amendment 4's justifying measurement, and the closure's artifact table
- **Direction:** neutral (the spend total and the completeness of the evidence trail, not a verdict figure)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED (git objects + both append-only ledgers)
- **Claim challenged (verbatim quote):** "| evidence ledger | every attempt, with the raw response verbatim |" / "| spend ledger | every billed call |" — NPDExperiment/REGISTRATION.md:772-773; against "**Measured on 8 held-out window days at `minimal`:** … | first-attempt compliance | 17 of 29, 59 percent | 7 of 8, 88 percent | | mean latency | 16.3 s per attempt | 2.3 s | | projected total over 432 days | 9.12 USD | **2.86 USD** |" — NPDExperiment/REGISTRATION.md:573-579
- **Evidence:** the strict JSON schema and the digest `7e6f3d68…` first exist in git at `250bc8f`, author date 2026-08-25T17:35:37Z (`git show 250bc8f -- src/npd/collect/prompt.py reports/stage_b0b/mock_run.md`). The eight strict-schema calls that produced the "7 of 8", "2.3 s" and "2.86 USD" column must therefore predate 17:35:37Z. In `ledgers/evidence.jsonl` the last row before that commit is 17:30:37.688Z and the next row is 17:35:44.085Z — a **306-second gap containing no evidence row and no spend row** (read 2026-09-04T18:25Z, untracked). Cross-check: the 74 pre-Amendment-4 evidence rows carry Σ`cost_usd` = 0.318852 USD and the 37 gate rows in the spend ledger before that commit sum to exactly 0.318852 USD, so the spend ledger contains no row that is not accounted for by a recorded attempt — there is no room for the eight calls. At the observed strict-schema first-attempt price (0.00649–0.00673 USD per call, `ledgers/spend.jsonl` rows at 17:35:44–17:36:06) the unrecorded spend is roughly 0.05–0.06 USD against a "ledger-enforced" 10.00 USD cap (`REGISTRATION.md:290`). No script, report or artifact in any commit records the measurement either: the files changed at `250bc8f` are adapter, collector, mock, prompt, config, evidence-ledger and two test files.
- **Recomputation (if any):** inputs both ledgers; method: window scan on `ts` between 17:25:00Z and 17:37:00Z, plus Σ`cost_usd` over the 74 rows with `prompt_digest` absent versus Σ over gate rows with `ts < 17:35:37Z`; result 0.318852 = 0.318852, exact; gap 306.4 s.
- **What would resolve it:** the eight held-out calls' ledger rows, or a note in Amendment 4 stating that the schema was measured with a harness outside the ledgers, naming the eight dates and their cost. Absent that, the measurement that re-froze the prompt and re-tuned the ladder mid-run cannot be checked, and the reported 6.9378 USD total understates true spend by those calls.
- **Confidence:** HIGH for the absence of the rows and the timing (git object dates plus append-only ledgers); MEDIUM for the imputed 0.05–0.06 USD, which is an estimate from observed per-call prices.
- **Invalidated by later commits?:** no — `250bc8f` is an ancestor of the anchor and the artifact table is at HEAD.
- **Disclosed by authors?:** partly. Amendment 5 discloses an unrecoverable undercount of "0.2936 USD" but attributes it to "**the superseded attempts**" whose usage was discarded (`REGISTRATION.md:617-622`); it does not mention the held-out strict-schema calls, which are a separate set made after the undercount was measured. Note also that "held-out" has no support in any record: no artifact names the eight days, and every window day was subsequently recollected into the final 415.

### DRAFT-P-3
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the B.2 pipeline validity gate, Task 2 of `reports/stage_b2/evaluation.md`
- **Direction:** neutral (pure provenance labelling; the gate passes by three orders of magnitude either way)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED (git objects + document text)
- **Claim challenged (verbatim quote):** "| registered tolerance | 0.02 |" — NPDExperiment/reports/stage_b2/evaluation.md:40; and "**Gate verdict: PASS.** The shuffled mean sits inside the registered tolerance of zero." — NPDExperiment/reports/stage_b2/evaluation.md:42-43; and the source comment "# The registered tolerance for the pipeline validity gate." — NPDExperiment/src/npd/eval/evaluator.py:551
- **Evidence:** `REGISTRATION.md` contains no occurrence of "toleran" and no bare `0.02` at any commit (`grep -n -iE 'toleran' REGISTRATION.md` empty at `64b7d41` and at HEAD). What Section 7 registers is qualitative: "**Negative-control leakage audit at B.2.** Shuffle stored rankings within day. The rank IC must collapse toward zero. A non-zero result stops everything." — `REGISTRATION.md:173-175`, unchanged from `64b7d41`. The figure 0.02 first enters git at `943ba05` (2026-08-25T17:06:55Z) as the default argument of `assert_control_collapsed(verdict, tolerance: float = 0.02)`; `git log -S 'tolerance: float = 0.02' -- src/npd/eval/evaluator.py` returns that commit only. The module constant `CONTROL_TOLERANCE = 0.02` used by `run_b2` was added at `2c6d683` (20:13:28Z), the evaluation commit, with the "registered" comment.
- **Recomputation (if any):** none required. For scale: the realized gate mean is +0.00011025 against a null sd of 0.0092549, so any tolerance above ~0.001 passes.
- **What would resolve it:** calling it the *code-fixed* tolerance, or an amendment recording that 0.02 was adopted at `943ba05` before the first call. The substance is sound — the threshold does predate every call it gates — only the word "registered" is wrong.
- **Confidence:** HIGH — a grep over every committed version of the registration.
- **Invalidated by later commits?:** no — the anchor is the last commit.
- **Disclosed by authors?:** no. `progress.md:142` says "inside the 0.02 tolerance" without claiming registration; only `evaluation.md` and the source comment call it registered.

### DRAFT-P-4
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the closure's correction of the frozen prompt digest
- **Direction:** neutral (understates discarded work; no verdict figure moves)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED (git objects + evidence ledger)
- **Claim challenged (verbatim quote):** "That is the **superseded** pre-Amendment-4 template. It produced the two calibration calls and the 26 superseded attempts, and **zero** of the 415 stored rankings." — NPDExperiment/REGISTRATION.md:778-780
- **Evidence:** `ledgers/evidence.jsonl` (read 2026-09-04T18:25Z, untracked) holds **74** gate attempts with no `prompt_digest` field: 26 before Amendment 3 (17:12:52–17:14:59Z) and 48 under Amendment 3's ladder (17:17:38–17:30:37Z), Σ`cost_usd` = 0.318852 USD. `git show 250bc8f --name-status` shows `src/npd/collect/prompt.py` first modified at `250bc8f`; it is untouched between `943ba05` and `250bc8f`, so all 74 came from the one superseded template `9a174e01…`. The "zero of the 415" half is confirmed: all 883 rows carrying `7e6f3d68…` are the only rows with a digest, and the 415 stored days all come from them. Three different counts for "superseded attempts" appear in the documents: 9 (`REGISTRATION.md:543`), 26 (`REGISTRATION.md:779`, `reports/session_a1_b1.md:254`) and 74 (`reports/stage_b1/collection.md:73`) — the last is the correct one.
- **Recomputation (if any):** inputs `ledgers/evidence.jsonl`; method: count rows lacking `prompt_digest` and excluding the two `calibration` rows; result 74, Σ cost 0.318852 USD; the 26 figure is the pre-Amendment-3 subset only.
- **What would resolve it:** "the 74 superseded attempts", or "the 26 attempts made before Amendment 3 and the 48 made under it".
- **Confidence:** HIGH — the counts come from an append-only ledger and the template's git history.
- **Invalidated by later commits?:** no — the closure commit is the anchor.
- **Disclosed by authors?:** partly — `reports/stage_b1/collection.md:73` prints the correct 74 ("superseded attempts, kept in the ledger and excluded from these counts: **74**"), so the repository contains the right number elsewhere; the closure paragraph, which is what a future replicator reads, does not.

### DRAFT-P-5
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** `CLAUDE.md`, the standing-rules file, against the frozen config at the same SHA
- **Direction:** neutral (hygiene)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED (git objects)
- **Claim challenged (verbatim quote):** "- Three amendments are in force and REGISTRATION.md Section 17 carries the evidence for each. … A parse failure escalates that day to `low` and it stays there, because at `minimal` the model often cannot hold a 30 label permutation." — NPDExperiment/CLAUDE.md:42-47
- **Evidence:** `git log -- CLAUDE.md` returns two commits, `64b7d41` and `f8304d9` (2026-08-25T17:19:11Z). At the anchor `REGISTRATION.md:442-675` carries **seven** amendments, and `src/npd/config.py:102-105` holds `reasoning_effort_ladder=("minimal","minimal","minimal","minimal","low")`, set by Amendment 4 at `250bc8f` (17:35:37Z) — not "escalates to `low` and it stays there", which is Amendment 3's superseded ladder.
- **Recomputation (if any):** none.
- **What would resolve it:** one line in `CLAUDE.md` updating the amendment count and the ladder, or a pointer that Section 17 governs.
- **Confidence:** HIGH — both files are tracked and anchored.
- **Invalidated by later commits?:** no — the anchor is the last commit.
- **Disclosed by authors?:** no, though the authoritative statement is in Amendment 4 and the config is the enforced artifact, so nothing operational turned on the stale text.

---

## 4. What could not be checked, and why

- **Whether the operator's prior was recorded before the sealed store was read** (R6). The
  Section 13 fill and every B.2 artifact land in one commit, `2c6d683`, two and a half
  minutes after the run's own timestamp. Git cannot order events inside a working tree.
  The only in-repo mechanism is `require_amendment_zero()`, which existed before the first
  call and refuses to run on the empty marker; that is a code-enforced ordering, not a
  recorded one. I did not guess.
- **Whether B.2 ran exactly once.** `evaluation.md:3` asserts "Run … Once." Nothing in git
  or in the untracked stores records a second run or its absence; the sealed store was
  opened read-only, so its mtime cannot distinguish one read from five.
- **The pre-image hash of `var/npd_sealed.db`** (R15) and **the hash of
  `analysis_bars.db`** on either side of the extract (R16). Neither was ever recorded, so
  the "unchanged" claims cannot be verified from the repository. Only
  `var/source_hashes_before.txt` (untracked) survives, for `universe.py` only.
- **The "actual 0.6429 USD" in Amendment 5 and the "16.3 s per attempt" in Amendment 4.**
  Failed attempts recorded `latency_s = 0.0` and `cost_usd = 0.0` before Amendment 5, so
  neither figure is reconstructible from the retained ledgers. The authors state the spend
  half is unrecoverable (`REGISTRATION.md:619-622`). Both are *consistent* with what does
  survive — 432 × (0.6429 − 0.030522)/29 = 9.122 reproduces the "9.12 USD" projection to
  three digits, and the 27 non-zero latencies in the Amendment-3 era average 12.6 s, which
  a mean including the unrecorded failure latencies could plausibly lift to 16.3 s. Not
  contradicted, not verified.
- **Whether `github.com/kirosli00tuff/NPDExperiment` is public** (R17). The push happened
  2026-08-29, after the anchor. I made no network request.
- **`progress.md:87-90`'s "never installed a systemd unit, a timer, or a cron entry"** — a
  host-state claim, not a repository claim, and out of scope for a git pass.

## 5. What verified, stated plainly

The pre-registration story in this repository holds up under git. The binding registration
was committed 31 minutes before the first billed call and 15 minutes before the outcome
store was written. The Section 0 outcome map, the Section 9 power floor and its eight-cell
grid, the Section 10 verdict table, the Section 11 epistemic boundary, the horizons, the
baselines, the panel size, the resample counts, `t_critical`, the effect band and the spend
cap are byte-identical from that commit to the anchor. `DECISIONS.md` and `progress.md`
contain not one deleted line across the whole history. Every parameter that did change
after data existed changed in the model-call layer only — temperature, reasoning effort,
the retry ladder, the prompt template, and the billing of rejected answers — and every one
of those five carries a dated amendment that states what changed, why, and what the data
showed. The two post-read amendments are labelled POST-READ and VOID and the git order
confirms both labels; the voided one is verifiably not applied. The findings above are
about the accuracy of three of those records and two stale figures, not about the ordering
of the experiment.

---

## 6. Live-repo access log

`/home/kiros-li/Documents/GitHub/NPDExperiment` — read-only throughout. No write, no
checkout, no branch, no script executed inside the repository. All computation ran from
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/work/agentC-prov-npd/`
against read-only reads of the two jsonl ledgers.

**`git -C /home/kiros-li/Documents/GitHub/NPDExperiment status --porcelain` BEFORE first
access (2026-09-04T18:21:05Z):**

```
```
(empty — clean)

**`git -C /home/kiros-li/Documents/GitHub/NPDExperiment status --porcelain` AFTER last
access (2026-09-04T18:38:54Z):**

```
```
(empty — clean)

`git rev-parse HEAD` = `2d3d0aebf977fb2821ec78c25b370c84ec055920` = the anchored SHA,
before and after.

Reads performed: `git log`, `git show`, `git diff`, `git log -S`, `git log --follow`,
`git rev-parse`, `git rev-list --count`, `git branch -a`, `git tag`, `git remote -v`;
`ls -la --time-style=full-iso` on `var/`, `ledgers/`, `.git/refs/remotes/origin/`;
read-only line parse of `ledgers/spend.jsonl` (922 rows) and `ledgers/evidence.jsonl`
(959 rows). `.env` was **not** opened. No sqlite store was opened in this pass.

Unanchored caveat: `ledgers/` and `var/` are untracked and outside the anchored commit.
They were read 2026-09-04T18:21Z–18:31Z and may have changed since the 2026-08-25 anchor;
their mtimes (all 2026-08-25) are consistent with no change, but mtimes are not proof.

Pre-existing dirt not caused by this audit: none — the tree was clean before and after.
