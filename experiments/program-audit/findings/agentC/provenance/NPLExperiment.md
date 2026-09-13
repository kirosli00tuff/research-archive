# NPLExperiment — Agent C PROVENANCE

- Repository: `NPLExperiment`
- Anchored SHA: **`8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`** (main, 2026-09-02T09:24:43Z)
- Live HEAD at read time: `dff16632eca6eea05b290ade5464339f44c75744` (2026-09-10T04:46:02Z) — **one commit ahead of the anchor**, that commit being *"docs: Amendment H5-3 — fire date recomputed at measured 0.77 passes/day; no bar moved, projection was falsified by three lost collection days"*.
- Document text read from `SNAP = /home/kiros-li/.cache/program-audit/scratchpad/snap/NPLExperiment/`.
- Git objects read read-only from the live repository (`log`, `show`, `rev-parse`, `status` only). Untracked data (`data/ledgers/requests.jsonl`, `data/h5/*.jsonl`, `data/state/*`) read read-only and marked **UNANCHORED** wherever used.
- All commit times below are **UTC**. The repository's author/committer stamps are `-07:00`; UTC = local + 7 h. Every `%ad` equals `%cd` on all 32 commits (no rebase/amend skew).
- Agent C has read nothing under `findings/agentA` or `findings/agentB`.

**Result in one line.** 43 rows recorded: **23 registration claims** (19 SUPPORTED, 3 PARTIAL, 1 NOT_SUPPORTED) and **20 parameter/rule changes** (18 SUPPORTED, 1 PARTIAL, 1 NOT_SUPPORTED). Of the 20 claims the inventory listed, **19 verify outright and one (P20) is PARTIAL**; the NOT_SUPPORTED rows are a one-hour timestamp in `report.md` and the operator-prior slot fill. Of everything that moved after data existed, **one change carries no dated amendment and no logged authorization**. Four draft findings — one S3, three S4 — **and none of them touches a verdict figure, a bar, an alpha, an n target or a cost band**. The deciding machinery of this repository — the Stage B verdict table, the 21-module hash chain, the two spent-read sha256 values, the H5 bars and mapping, the familywise alpha, the H2 amendment ordering — verifies to the digit.

---

## 1. The commit spine (UTC), so every claim below can be placed on it

| commit | UTC | what it is |
|---|---|---|
| `f6841d2` | 2026-08-27T00:54:38Z | init, operator prompt logged, `src/npl/config.py` created |
| `cd640b6` | 2026-08-27T00:54:38Z | **REGISTRATION.md Sections 0–13, 301 lines, before any network call** |
| — | 2026-08-27T00:56:49Z | **first row in `data/ledgers/requests.jsonl`** (first network call) |
| `f1def31` | 2026-08-27T01:22:36Z | A.1; **Amendment 1**; `funding_archive_epoch_ms` added |
| `6dfdbb1` | 2026-08-27T05:29:04Z | A.2 census/eligibility/power; Section 0 verdict record GO |
| `bfd169d` | 2026-08-27T05:31:31Z | A.3 collectors armed |
| `acd122d` | 2026-08-27T09:12:57Z | A.4 close-out |
| `2d2edc1` | 2026-08-27T19:30:34Z | **operator prior slot filled `0.40 (adopted)`** |
| `aaddb23` | 2026-08-27T23:43:56Z | stage ladder |
| `8e31e78` | 2026-08-28T02:48:19Z | B.0; **Amendment 2**; preconditions 312/312 + 176/176 |
| `6399d63` | 2026-08-28T02:49:19Z | **Amendment 3 — the Stage B verdict table** (REGISTRATION.md only) |
| `32b3f9e` | 2026-08-28T03:00:42Z | B.1 — `stageb/reader.py` + `stageb/cli.py` first exist; `hashes_b1.json` |
| — | 2026-08-28T03:01:01Z | latch `data/state/stage_b_read.json` written |
| — | 2026-08-28T03:01:08Z | **the single H1 read** (`reports/stage_b/read.json:read_at`) |
| `844f7c2` | 2026-08-28T03:03:19Z | B.2 — FAIL recorded, `read.json` committed |
| `fd92459` | 2026-08-28T03:06:07Z | B.3 close-out |
| `77ee522` | 2026-08-28T03:53:20Z | **Amendment 4**; HYPOTHESES.md; H2/H3/H4 registrations; quarantine |
| `c4003e5` | 2026-08-28T05:21:55Z | register A.1 — first successor measurement |
| `2b44c59` | 2026-08-28T05:45:38Z | register A.2 — **the cull: k = 1, alpha_h = 0.05** |
| `76319e7` | 2026-08-28T06:23:20Z | register A.3 |
| `e89b187` | 2026-08-28T06:27:22Z | register A.4 close-out |
| — | 2026-08-28T06:51:10Z | `reports/stage_a_h2/amend_preconditions.json:checked_at` |
| `f31f7a3` | 2026-08-28T07:01:06Z | **Amendment H2-3**, docs + precondition artifact only |
| `f8e54d8` | 2026-08-28T07:40:26Z | H2-3 **implemented**; `config.py` floor 2.0→1.0, share 0.60→0.625 |
| `546b2e3` | 2026-08-28T07:46:42Z | **Amendment H2-4** |
| `5bd1fb8` | 2026-08-28T07:51:34Z | look-aware dark reader, per-look latches |
| `fc639c7` | 2026-08-28T07:56:13Z | H2 amendment close-out |
| `f72af92` | 2026-08-28T21:23:35Z | H5 Task 0 — `reports/h5/preconditions.json` (checked_at 21:24:00Z) |
| `98e7e01` | 2026-08-28T21:38:58Z | **H5 registration + mapping + calendar + dark outcome map** |
| — | 2026-08-28T21:39:45–48Z | **first H5 network charges** — the 6-request recon probe |
| — | 2026-08-28T21:44:11Z | **census pass 1** (`data/h5/census.jsonl`, 273 rows, no `listing_status`) |
| — | 2026-08-28T21:51:54Z | **census pass 2** (273 rows, **with** `listing_status`) |
| `13c6965` | 2026-08-28T21:59:42Z | **Amendments H5-1 and H5-2** + census artifacts + `outcome.py` change |
| — | 2026-08-28T22:00:14Z | forward collector pass (`data/h5/snapshots.jsonl`) |
| `e0eab81` | 2026-08-28T22:03:21Z | forward collector armed; `outcome.py` gains the projection helpers |
| — | 2026-08-28T22:04:30Z | **the H5 map fires** (`reports/h5/verdict.json:fired_at`) |
| `c7bdf64` | 2026-08-28T22:07:26Z | H5 Section 6 verdict record |
| `b685d30` | 2026-08-28T22:10:08Z | H5 close-out; `h2_verification.json` |
| `449ff1e` | 2026-08-28T22:11:11Z | **timestamp corrections** (progress.md, H5 reg, h2_verification.json) |
| `c2aaa27` | 2026-08-28T22:12:23Z | H5 spend figure corrected 1,124 → 888 |
| `8f1fef8` | 2026-09-02T09:24:43Z | **ANCHOR** — ADR-032 DNS wait |
| `dff1663` | 2026-09-10T04:46:02Z | post-anchor: **Amendment H5-3** (fire date recomputed) |

---

## 2. Registration claims table

Every claim listed in `findings/agentC/verification/NPLExperiment.inventory.md` §4, verified against git objects and stored artifacts.

| # | claim (short) | file:line | commit named | commit found / date (UTC) | data first existed | status |
|---|---|---|---|---|---|---|
| **P1** | *"docs: register Sections 0-13 before any network call"* | commit subject of `cd640b6`; object is `REGISTRATION.md` | `cd640b6` | **yes**, 2026-08-27T00:54:38Z; 301 lines, `## 0.` … `## 13.` + `## Amendments` all present | first ledger charge **2026-08-27T00:56:49Z** (`data/ledgers/requests.jsonl` line 1, UNANCHORED, read 2026-09-12T12:32:30Z) | **SUPPORTED** — registration precedes the first request by 2 min 11 s |
| **P2** | *"Amendment 3 was committed and pushed (commit 6399d63) while the only data in existence were counts, timestamps, and coverage — before the reader existed."* | `report.md:157` | `6399d63` | **yes**, 2026-08-28T02:49:19Z, `--name-status` = `M REGISTRATION.md` **only** | `stageb/reader.py` + `stageb/cli.py` first appear in `32b3f9e` 2026-08-28T03:00:42Z; read at 03:01:08Z | **SUPPORTED** — 11 m 23 s before the reader existed, 11 m 49 s before the read |
| **P3** | *"the 312 retro event IDs are recorded in data/state/generating_sample.json, and every successor view refuses them"* | `report.md:322-325` | none | `register/generating_sample.py` + `views.py` added in `77ee522` 2026-08-28T03:53:20Z | `data/state/generating_sample.json` (UNANCHORED, mtime 2026-08-27 20:47 local, read 2026-09-12T12:38:13Z) holds `count = 312` and **312 `event_ids`, all distinct** | **SUPPORTED** (file half; the refusal-by-test half is code, not provenance) |
| **P4** | *"Amended the same day, before any pair outcome existed (H2-3, H2-4)"* | `HYPOTHESES.md:70` (also `:14`) | `f31f7a3` / `546b2e3` | **yes**, 2026-08-28T07:01:06Z and 07:46:42Z | `reports/stage_a_h2/amend_preconditions.json` at `f31f7a3`: `checked_at 2026-08-28T06:51:10Z`, `h2_read_json_absent true`, `h2_registered_latch_absent true`, `h2_outcome_artifacts_found []`, `head e89b187`. **Live `data/state/` still holds no `h2_read.json` and none of the three latches** (read 2026-09-12T12:37:59Z) | **SUPPORTED** — no H2 outcome has ever been read, then or since |
| **P5** | *"Amendment H2-3 registered three changes before a line of code moved, and was committed and pushed before any of them was implemented."* | `report.md:455` | `f31f7a3` | **yes**; `--name-status` = `M progress.md`, `M registrations/H2/REGISTRATION.md`, `A reports/stage_a_h2/amend_preconditions.json` — **no source file** | implementation lands in `f8e54d8` at 07:40:26Z, **39 m 20 s later** | **SUPPORTED** |
| **P6** | *"**Chosen before any pair outcome existed.** At the moment this line was written…"* | `registrations/H2/REGISTRATION.md:475` | none | the line enters at `f31f7a3` 07:01:06Z | as P4 | **SUPPORTED** |
| **P7** | *"The correction, made now, **before any outcome value exists and before the reader has seen anything but synthetic fixtures**"* | `registrations/H2/REGISTRATION.md:773` | `546b2e3` | **yes**, 2026-08-28T07:46:42Z | `reports/h5/preconditions.json` (`f72af92`) records at 2026-08-28T21:24:00Z: all three H2 latches absent, `no_h2_latch_exists true`; `reports/h5/h2_verification.json` repeats it at 22:09:00Z | **SUPPORTED** — independently re-verified 14 h later and still absent today |
| **P8** | *"`registrations/H5/REGISTRATION.md` was committed and pushed with **zero H5 requests sent**"* | `report.md:617` | `98e7e01` | **yes**, 2026-08-28T21:38:58Z (`A registrations/H5/REGISTRATION.md`) | ledger: **last charge before 21:38:58Z is 21:05:53Z `info:meta`** (the hourly H2 watcher, which also fires at 20:05 / 22:05 / 23:05). **First H5 charge 21:39:45Z** (`perpDexs`, `metaAndAssetCtxs` ×2, `fundingHistory` ×2, `l2Book` = exactly 6). UNANCHORED, read 2026-09-12T12:37:29Z | **SUPPORTED** — zero H5 requests before the registration commit |
| **P9** | *"an **exact-string mapping registered before any price was read**" (198 entries)* | `HYPOTHESES.md:125`; `report.md:619` | `98e7e01` | **yes**; `git show 98e7e01:src/npl/h5/resolution.py` contains **198** `"…": ` entries | `git log --follow -- src/npl/h5/resolution.py` returns **`98e7e01` and nothing else** — byte-frozen from 21:38:58Z through the anchor | **SUPPORTED** |
| **P10** | *"tagged by US market session against a calendar **registered before collection**"* | `HYPOTHESES.md:125`; `registrations/H5/REGISTRATION.md:209` | `98e7e01` | **yes**; `calendar.py` at `98e7e01` declares `SESSION_TAGS` (four) and NYSE holiday/early-close tables for 2024–2027 written out by date | `git log --follow -- src/npl/h5/calendar.py` returns **`98e7e01` only**; first snapshot 21:44:11Z | **SUPPORTED** |
| **P11** | *"the outcome map built dark with fixtures sitting exactly on 18.00 bp, 54.00 bp, 20 instruments and a 10-of-20 funding share"* | `report.md:621-623` | `98e7e01` | **yes**; `98e7e01:tests/test_h5_registration.py` carries `floor_bp=18.0, viable_bp=54.0`, `assert h5out.cost_floor_bp() == CONFIG.hip3_round_trip_bp[1] == 18.0`, `viable_threshold_bp() == 54.0`, `_fire(medians={"regular": 54.0})` on-the-bar case, defaults `n_ref=20, n_cov=20, funding=10` | census pass 1 at 21:44:11Z | **SUPPORTED** |
| **P12** | *"Three consequences were registered **before** measurement"* | `report.md:626` | `98e7e01` | **yes**; `98e7e01:registrations/H5/REGISTRATION.md` §0 carries all three as first committed: **Outcome blindness (rule 7)** → no retrospective basis from `candleSnapshot`; **Funding (rule 7, second half)** → no funding-rate *value* read; **The retrospective gate** | as P11 | **SUPPORTED** |
| **P13** | *"That amendment was made before any firing and makes CLOSED **strictly harder**; it cost this entry a same-day close."* | `report.md:681-683` | `13c6965` | **yes**, 2026-08-28T21:59:42Z | `reports/h5/verdict.json:fired_at = 2026-08-28T22:04:30Z` — **4 m 48 s later** | **SUPPORTED**, with the arithmetic recomputed below (§4a): under `98e7e01:outcome.py` the measured inputs fire **CLOSED**; under `13c6965:outcome.py` they fire **PENDING**. The claim is literally true in both halves |
| **P14** | *"**The amendment deleted this entry's only route to VIABLE** … it was made with the census in hand, disclosed in full in its own text"* | `report.md:662-665` | `13c6965` | **yes** | `registrations/H5/REGISTRATION.md:462` names the census in hand verbatim: *"the Task 2 census had completed: **323 requests**, one pass, snapshot `h5-census-2026-08-28T21:44:11Z`"* | **SUPPORTED** — the post-hoc character is stated by the authors in the amendment's own opening, and the direction (restrictive) is confirmed: 45.6 % of the excluded delisted stratum clears 54 bp against 0.0 % of the retained live stratum |
| **P15** | *"Latch … sha256 `2d204ccb…438f67e` (21 module hashes inside); artifact … sha256 `4455489675c…be840c`. Read 2026-08-28T03:01:08Z, exactly once."* | `HYPOTHESES.md:54` | none | — | recomputed 2026-09-12T12:38:13Z: latch sha256 = `2d204ccb23c4961597d2e4a3263b2abffeb1f8f2e32230ee3c4b97857438f67e` ✓, `module_hashes` n = **21** ✓, artifact sha256 = `4455489675c3774f05c977cb7edb9d8b26928f851400077b31263f5826be840c` ✓, `read.json:read_at = 2026-08-28T03:01:08Z` ✓ (latch `read_at` 03:01:01Z — written 7 s first, as the registered "latch written first" rule requires) | **SUPPORTED** — every digit reproduces |
| **P16** | *"**The B.1 re-hash** … exactly one diff against B.0 … Every other read-surface module is byte-identical to its B.0 hash."* | `report.md:200-206` | none | — | `hashes_b0.json` 19 modules, `hashes_b1.json` 21. Added: `stageb/cli.py`, `stageb/reader.py`. Changed: **`stageb/__init__.py` only**. Removed: none. The 21 latch hashes equal `hashes_b1.json` exactly **and** reproduce byte-for-byte against `git show 32b3f9e:src/npl/<mod>` and `git show 844f7c2:src/npl/<mod>` — **all 21 match at both** | **SUPPORTED** |
| **P17** | *"H2's collectors, ledgers, latches and stores are **read-only** to every H5 path"* | `HYPOTHESES.md:130` | none | — | `reports/h5/h2_verification.json` (anchored): `h2_store_hashes` 11 entries, **`"unchanged": true` ×11**, `h2_pair_count_now 62` = `h2_pair_count_precondition 62`, `h2_pair_count_unchanged true`, all three H2 latches `absent_now true`, `h5_wrote_only_under_data_h5` present | **SUPPORTED** |
| **P18** | *"alpha_h = 1 − 0.95^(1/k), fixed at the cull … **never revisited after any outcome exists**"* | `HYPOTHESES.md:142-143` | none | — | `git log --follow -p -- src/npl/config.py` (5 commits, full patch read): `family_confidence=0.95` enters at `77ee522` and **is never touched again** through the anchor. `k = 1` fixed by the cull at `2b44c59` 05:45:38Z. Amendment H2-3 restates *"k = 1 and alpha_h = 0.05, fixed by the cull and never revisited"* and splits it into α₁ 0.02 / α₂ 0.03 **summing to 0.05** — a split, not a change to the total. **No H2/H3/H4/H5 outcome value has ever existed**, so the "after any outcome exists" clause is vacuously satisfied for every surviving entry | **SUPPORTED** |
| **P19** | *"all three registrations … were committed and pushed before any successor measurement"* | `report.md:327-330` | `77ee522` | **yes**, 2026-08-28T03:53:20Z; `--name-status` shows `A registrations/H2|H3|H4/REGISTRATION.md` in that commit | first successor measurement is register A.1, `c4003e5` 2026-08-28T05:21:55Z — **88 minutes later** | **SUPPORTED** |
| **P20** | *"The verdict record above is headed **22:20Z**. That figure was typed by the assistant as an estimate … **The map actually fired at 2026-08-28T22:04:30Z**"* | `registrations/H5/REGISTRATION.md:634-636` | none (correction at `449ff1e`) | correction commit `449ff1e` 2026-08-28T22:11:11Z | `verdict.json:fired_at = 22:04:30Z` confirms. **But at the anchor `report.md:667` reads "### The row, fired 2026-08-28T22:20Z" and `HYPOTHESES.md:122` reads "fired 2026-08-28T22:20Z"** — the correction was appended to the registration and to `progress.md` but not propagated to the two summary documents | **PARTIAL** → draft finding **DRAFT-P-3** |
| **P20b** | (parallel case named in the inventory) `report.md:446` *"PASS at 07:51:10Z on the project clock"* | `report.md:446` | none | — | `git show f31f7a3:reports/stage_a_h2/amend_preconditions.json` → `"checked_at": "2026-08-28T06:51:10Z"`; `registrations/H2/REGISTRATION.md:377` and `progress.md:831` both also say **06:51:10Z**. 07:51:10Z would be *after* the amendment commit (07:01:06Z) and after Amendment H2-4 (07:46:42Z), which the sentence's own "checked and recorded before anything else" forbids | **NOT_SUPPORTED** → draft finding **DRAFT-P-2** |

### Two claims that verify only in part, and are recorded as PARTIAL rather than contradicted

| # | claim | what verifies | what does not | status |
|---|---|---|---|---|
| **P-H5-1a** | `registrations/H5/REGISTRATION.md:385` — *"**No H5 census had been run. No basis table existed. No session-tagged sample existed.**"* (Amendment H5-1's data-existence statement) | The ordering the amendment asserts is independently corroborated by artifacts the authors did not control for this purpose: census pass 1 (`h5-census-2026-08-28T21:44:11Z`, 273 rows) **carries no `listing_status` field** and is counted by `scripts/h5_fire.py` as `rows_skipped_pre_amendment = 273` (matching `verdict.json`), while pass 2 (`21:51:54Z`) carries it — so the H5-2 rule was implemented **between** the two passes; and Amendment H5-2 at `:462` names pass 1 as its census-in-hand. H5-1 sitting earlier still, in the 21:39:48 → 21:44:11Z window, is consistent with all of it | **The only durable timestamp is the commit, `13c6965` at 21:59:42Z**, by which time both census passes had run and the census artifacts are in that same commit. Unlike Amendment H2-3 — separately committed at `f31f7a3` **before** its implementation at `f8e54d8`, which git can prove — H5-1's precedence over the census rests on internal consistency and on the `listing_status` field boundary, not on a commit boundary | **PARTIAL** — corroborated, not pinned. No contradiction; **not a finding** |
| **P-H5-1b** | `registrations/H5/REGISTRATION.md:368-369` — *"**six requests**, charged to the shared ledger at 2026-08-28T21:41Z"* | **Six** is exact: the ledger holds exactly six `charge` rows in that burst (`perpDexs` 1, `metaAndAssetCtxs` 2, `fundingHistory` 2, `l2Book` 1) | The ledger stamps them **21:39:45Z–21:39:48Z**, and the six matching `settle` rows likewise. There is no 21:41Z activity of any kind; the next charge is 21:44:11Z | **PARTIAL** → draft finding **DRAFT-P-4** |

---

## 3. Parameter changes after data existed

Every parameter, bar, threshold, horizon, universe rule, alpha, N target, cost figure or decision rule that moved after any data existed. "Data existed" is dated from the first ledger charge, **2026-08-27T00:56:49Z**; everything in this table therefore post-dates data by construction.

| # | what changed | from → to | commit / UTC | dated amendment? | amendment ref | data stated in the amendment? | status |
|---|---|---|---|---|---|---|---|
| PC-1 | `funding_archive_epoch_ms` **added** | — → `1_683_849_600_000` (2023-05-12T00:00:00Z) | `f1def31` 2026-08-27T01:22:36Z | **yes** | Amendment 1, `REGISTRATION.md:301` | yes — *"Stage A.1 access, rate-ceiling, retention, and delisting telemetry only … no outcome value of any kind had been read"*, n = 12 retention + 6 delisted instruments | **SUPPORTED** |
| PC-2 | Section 3 listing day gains a funding cross-check; **epoch censoring** rule added; Section 2 hyperp tag becomes mechanical; Section 12 pacing figures recorded as measured | rule additions/replacements | `f1def31` (same) | **yes** | Amendment 1 | yes; and it names what is **unchanged** (universe, entry anchor, outcome definition, costs, control, horizons, all Section 8 bars, power method, Stage B trigger, priors) and states the bias direction | **SUPPORTED** |
| PC-3 | **Operator prior slot filled** `_reserved — empty_` → `0.40 (adopted)` | empty → 0.40 (adopted) | `2d2edc1` 2026-08-27T19:30:34Z | **NO** | — | — | **NOT_SUPPORTED** → draft finding **DRAFT-P-1**. The value is the assistant's own `assistant_prior_stage_b = 0.40`; `REGISTRATION.md:282` says the assistant's numbers *"must not be copied into the slot below"*; the authorizing operator instruction of 2026-08-27 is asserted in the commit subject and at `report.md:86` but is **not logged verbatim in `progress.md`**, which standing rule 1 requires. Disclosed as `(adopted)` and as assistant-written at `report.md:86,126-127` |
| PC-4 | Push protocol: push-nothing → push all commits to origin main | process rule | `8e31e78` 2026-08-28T02:48:19Z | **yes** | Amendment 2, `REGISTRATION.md:422` | yes — full Stage A stores, *"No outcome value has been parsed"*, remote state measured (n = 1 `gh repo view`) | **SUPPORTED** (process rule, no bar) |
| PC-5 | **Stage B verdict table + 7 reading rules + 5 riding rules registered** (GO / PARTIAL_DRIFT / FAIL) | none → registered | `6399d63` 2026-08-28T02:49:19Z | **yes** | Amendment 3, `REGISTRATION.md:447` | yes — B.0 precondition report of 02:47:28Z, effective N 312/312/175 vs minimums 34/103/60, latch absent, `hashes_b0.json` | **SUPPORTED** — and the fired row (`read.json:row_fired = "FAIL"`, P1 lower bound 0.5707 < 0.60) is the FAIL row of that table |
| PC-6 | Register architecture: single hypothesis → 4-entry register; quarantine of the spent read and the 312 generating-sample events | architecture | `77ee522` 2026-08-28T03:53:20Z | **yes** | Amendment 4, `REGISTRATION.md:614` | yes — names the spent read with both hashes and states *"No successor-hypothesis data of any kind existed"* | **SUPPORTED** |
| PC-7 | H2/H3/H4 power assumptions **added** (`h2_e1_true_share 0.65`, `h2_e2_true_share 0.60`, `h2_cost_floor_multiple 2.0`, `h3_share_positive_true 0.677`, `h3_magnitude_true_* 0.65/0.356`, `h4_funding_thresholds_annualized (−0.10,−0.20,−0.40)`, `h4_true_share_* 0.85/0.631`, `family_confidence 0.95`) | — → registered | `77ee522` (same) | **yes** | Amendment 4 §3 | yes — each is labelled **generating-sample-derived** in `config.py` comments and in each registration; Amendment 4 registers the quarantine that makes them power-only | **SUPPORTED** — derived from the spent H1 read, disclosed as such, barred from any successor verdict |
| PC-8 | **k fixed at 1; alpha_h fixed at 0.05** | k unknown → 1 | `2b44c59` 2026-08-28T05:45:38Z | **yes** | Amendments H2-1 / H3-1 / H4-2 (`registrations/H2:251`, `H3:150`, `H4:197`) | yes — the cull reads counts, rates and timestamps only (`reports/stage_a_h2/ktable_cull.json`) | **SUPPORTED**; never revisited (see P18) |
| PC-9 | **`h2_cost_floor_multiple` 2.0 → 1.0** | 2.0 → 1.0 | `f8e54d8` 2026-08-28T07:40:26Z | **yes**, registered 39 m earlier | Amendment H2-3 Change 2 (`registrations/H2:436…`); ADR-023 | yes — full data-existence paragraph naming the 06:51:10Z precondition scan; *"This amendment weakens the registered bar. It is made for calendar reasons, on operator instruction dated 2026-08-28."* | **SUPPORTED** |
| PC-10 | **`h2_e2_true_share` 0.60 → 0.625**; `h2_e2_true_share_two_times_floor 0.60` and `h2_cost_floor_multiple_secondary 2.0` added | 0.60 → 0.625 | `f8e54d8` (same) | **yes** | Amendment H2-3 Change 2 | yes — the interpolation is stated as *"a choice, not a measurement"*, and every minimum-N is required to be reported twice | **SUPPORTED** |
| PC-11 | Section 6 control gains a **main-dex fallback**; `pair_type` tagged at assignment | rule relaxation | `f8e54d8` (same) | **yes** | Amendment H2-3 Change 1; ADR-022 | yes; direction stated (*"a relaxation"*); the 38 pre-amendment pair rows' treatment is pinned by rule, not imputation | **SUPPORTED** |
| PC-12 | **Two-look sequential plan**: `h2_alpha_look1 0.02`, `h2_alpha_look2 0.03`, `h2_planning_interim_fraction 0.5`, `h2_futility_conditional_power 0.10`; Section 10 opens 1 → 2 behind per-look latches | — → registered | `f8e54d8` (same) | **yes** | Amendment H2-3 Change 3; ADR-024 | yes; *"The alpha split, fixed here and never revisited"*, with a materiality test defined **before** it could be applied | **SUPPORTED** |
| PC-13 | Look-2 pass condition corrected: `S₁ < k₁ and S₂ ≥ k₂` → `S₁ ≥ k₁ **or** S₂ ≥ k₂` | decision rule | `546b2e3` 2026-08-28T07:46:42Z | **yes** | Amendment H2-4 (`registrations/H2:635`); ADR-025 | yes — *"made now, before any outcome value exists and before the reader has seen anything but synthetic fixtures"*, corroborated by P7 | **SUPPORTED** |
| PC-14 | **All H5 bars added**: `h5_min_instruments_with_reference 20`, `h5_min_coverage_days 30`, `h5_funding_service_share 0.5`, `h5_viable_basis_multiple 3.0` (54 bp = 3 × 18), `h5_retro_lookback_days 180`, `h5_retro_page_budget 12`, `h5_daily_request_cap 1000`, `h5_assistant_prior_edge 0.05` | — → registered | `98e7e01` 2026-08-28T21:38:58Z | n/a — **initial registration**, not a change | — | ledger shows zero H5 charges before this commit (P8) | **SUPPORTED** |
| PC-15 | **H5 outcome map firing order changed**: the floor→CLOSED clause moves out of the pre-coverage `closed` list and behind the coverage gate | decision rule | `13c6965` 2026-08-28T21:59:42Z (code); amendment same commit | **yes** | Amendment H5-1 Change 1 (`registrations/H5:365`) | yes — but the statement is *"No H5 census had been run"*, which git cannot pin (see P-H5-1a). Direction is stated and verified restrictive (§4a) | **PARTIAL** — dated amendment present, reason present, restrictive direction verified; the data-existence statement is corroborated but not commit-pinned. **Not a finding** |
| PC-16 | **Universe rule changed**: delisted instruments excluded on a conjunctive three-field test (`isDelisted` ∧ `openInterest == 0` ∧ `dayNtlVlm == 0`) | universe | `13c6965` (same) | **yes** | Amendment H5-2 (`registrations/H5:459`); ADR-030 | **yes, fully** — names snapshot `h5-census-2026-08-28T21:44:11Z`, 323 requests, and lists the complete stratum table it was seeing, including that the excluded stratum holds every observation over the bar | **SUPPORTED** — post-data by the authors' own statement, restrictive, disclosed |
| PC-17 | `h5/basis.py` coin naming: `f"{dex}:{name}"` → `str(row["name"])` | defect fix | `13c6965` (same) | no amendment (not a bar) | disclosed at `progress.md:1315-1316` and `docs/H5_ACCESS.md:50-51` | the measured fact (the venue already prefixes the dex inside `name`) came from the 21:39 recon probe | **SUPPORTED** — a parser defect fix, no registered figure moves |
| PC-18 | `h5/outcome.py` gains `passes_needed()` / `projected_fire_date()` and `CensusWindowNotProjectable` | new derived figure | `e0eab81` 2026-08-28T22:03:21Z — **after** both census passes, **before** the fire at 22:04:30Z | **no amendment** | — | — | **SUPPORTED with a note**: no registered bar, threshold, horizon, alpha or universe moves; the functions read only `h5_min_instruments_with_reference` and `h5_min_coverage_days`, both already registered at `98e7e01`. They produce the descriptive *"29 passes / 2026-09-26"* figure at `HYPOTHESES.md:122` and `verdict.json:census_window`, which is **not verdict-bearing** (PENDING is fired by the coverage gate, not by the projection). The authors amended the projection themselves post-anchor at `dff1663` (Amendment H5-3). **Not a finding** |
| PC-19 | `reports/h5/h2_verification.json:checked_at` corrected **in place** 22:36:00Z → 22:09:00Z; `head` c7bdf64 → b685d30 | stored artifact edit | `449ff1e` 2026-08-28T22:11:11Z | **yes** — the correction is written **inside the file** as `checked_at_correction`, and in `progress.md` and the H5 registration | `449ff1e` | yes | **SUPPORTED** — an in-place edit of a committed artifact, but self-recording and confined to a typed timestamp; the 11 store hashes and 62 pair count are untouched by the diff |
| PC-20 | *(post-anchor, for completeness)* H5 fire-date projection recomputed at a measured 0.77 passes/day | 2026-09-26 → recomputed | `dff1663` 2026-09-10T04:46:02Z | **yes** | Amendment H5-3 | commit subject: *"no bar moved, projection was falsified by three lost collection days"* | **outside the anchor** — recorded here so no finding against the 2026-09-26 projection can be presented as undiscovered |

**Registration-file write discipline, checked mechanically.** `git log --follow --numstat` on all five registration files: every commit to `REGISTRATION.md`, `registrations/H2|H3|H4|H5/REGISTRATION.md` is **pure insertion (deletions = 0)** with exactly two classes of exception — (i) `2d2edc1`, 1 insertion / 3 deletions, which is PC-3, the operator prior slot fill; (ii) `2b44c59`, 2 deletions each in H2/H3/H4, which is the removal of the placeholder couplet *"None yet. An amendment is dated, reasoned, states exactly what data existed when it was made, and never edits anything above its own line."* when the first real amendment was appended. `HYPOTHESES.md` edits (3/3, 4/2, 18/11) are all **Status-row rewrites in the register index**, which the register's own design requires. **No bar, threshold or figure was ever edited in place above an amendment line.**

---

## 4. Recomputations that back the table

### 4a. What Amendment H5-1 actually did to the fired row (backs P13)

Inputs as recorded in `reports/h5/verdict.json` (anchored): `instruments_with_reference = 94`, `funding_served_instruments = 94` (share 1.000), `instruments_meeting_coverage = 0`, `median_abs_bp_by_tag = {"extended": 4.1446…}`, `floor_bp = 18.0`.

- **Pre-amendment map** (`git show 98e7e01:src/npl/h5/outcome.py`): the floor clause is appended to the `closed` list before any coverage test, and `if closed: return build(STATE_CLOSED, closed)` runs **first**. With 94 ≥ 20 and share 1.000 ≥ 0.50 the two structural clauses stay silent, but `all(value < 18.0 for value in present.values())` is true at 4.14 bp, so `closed` is non-empty → **CLOSED**.
- **Post-amendment map** (`git show 13c6965:src/npl/h5/outcome.py`): the floor clause is deleted from the `closed` list (diff hunk `@@ -119,12 +122,6 @@`, six lines removed) and re-inserted as a `return build(STATE_CLOSED, …)` **after** the `instruments_meeting_coverage < 20` PENDING gate (hunk `@@ -155,6 +152,15 @@`). With `instruments_meeting_coverage = 0` the PENDING gate returns first → **PENDING**.

The CLOSED-on-floor acceptance region is a strict subset of the pre-amendment one, so *"makes CLOSED strictly harder"* is exact; and on the data in hand it converted a terminal CLOSED into a non-terminal PENDING, which is exactly what *"it cost this entry a same-day close"* says. Both halves of the claim verify. The amendment discloses the same fact in its own words at `registrations/H5:432-435`: *"Under the unamended order this entry would have closed today on a single cross-section."*

### 4b. Module-hash chain (backs P15, P16)

| check | result |
|---|---|
| sha256(`SNAP/reports/stage_b/read.json`) | `4455489675c3774f05c977cb7edb9d8b26928f851400077b31263f5826be840c` — **matches `HYPOTHESES.md:54`** |
| sha256(`data/state/stage_b_read.json`) *(UNANCHORED, read 2026-09-12T12:38:13Z)* | `2d204ccb23c4961597d2e4a3263b2abffeb1f8f2e32230ee3c4b97857438f67e` — **matches `HYPOTHESES.md:54`** |
| latch `module_hashes` count | **21** |
| latch `module_hashes` == `read.json:module_hashes` == `hashes_b1.json` | **true** |
| all 21 vs `git show 32b3f9e:src/npl/<mod>` | **21/21 match** |
| all 21 vs `git show 844f7c2:src/npl/<mod>` | **21/21 match** |
| all 21 vs `git show 8f1fef8:src/npl/<mod>` (the anchor) | 16/21 match; `blindness.py`, `config.py`, `coverage.py`, `paths.py`, `power.py` differ — **each first diverges at `77ee522` (03:53:20Z) or later, i.e. after the 03:01:08Z read**, so the Amendment 3 rule *"any diff in a B.0-hashed read-surface module after the B.1 re-hash voids the read authorization"* is not breached |
| `hashes_b0` vs `hashes_b1` | 19 → 21 modules; added `stageb/cli.py`, `stageb/reader.py`; **changed: `stageb/__init__.py` only**; removed: none |

---

## 5. Draft findings

### DRAFT-P-1
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H1 (H-NPL) Section 13 operator prior slot — the registered structural block on the single Stage B read
- **Direction:** A — it makes the H1 closure weaker than labelled: the read that produced the CLOSED — NEGATIVE verdict is presented as gated by an operator condition that was in fact satisfied by the assistant, with the assistant's own number
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED (git object `2d2edc1`, plus the verbatim-logged operator prompts)
- **Claim challenged (verbatim quote):** "are context, not the operator's number, and they **must not be copied into the** slot below." — NPLExperiment/REGISTRATION.md:282 (the sentence runs `:281-283`). The slot three lines later reads: "> Operator prior on the Stage B bars clearing: 0.40 (adopted)" — NPLExperiment/REGISTRATION.md:287
- **Evidence:**
  - The assistant's own recorded prior is **0.40**: "0.40 that the Stage B bars clear on the registered sample." — NPLExperiment/REGISTRATION.md:277; `src/npl/config.py` carries `assistant_prior_stage_b=0.40` from `f6841d2` onward. The slot was filled with that identical number.
  - The Stage A.0 operator prompt, **logged verbatim** by the repository's own standing rule 1: "The NPD Amendment 0 lesson applies: an adopted prior corrupts the calibration ledger. **The operator prior slot stays empty. Do not fill it.**" — NPLExperiment/progress.md:33
  - The Stage B.0 operator prompt, logged verbatim the next day, repeats it: "On an empty or malformed slot, stop the entire stage, report BLOCKED-ON-OPERATOR with the accepted format, push the report, end. **Never fill it.**" — NPLExperiment/progress.md:395
  - `git show 2d2edc1 --stat` (2026-08-27T19:30:34Z, subject *"operator prior 0.40 (adopted), written by assistant on operator instruction 2026-08-27"*) touches **`REGISTRATION.md` (1 insertion, 3 deletions) and `tests/test_registration_check.py` only**. It does **not** touch `progress.md`: the operator instruction of 2026-08-27 said to authorise the fill is nowhere logged verbatim, and `progress.md` has **no entry at all** between `## 2026-08-27T09:20Z` (line 315) and `## 2026-08-28T02:31:22Z` (line 376).
  - No amendment records the departure. `REGISTRATION.md`'s amendment log runs 1, 2, 3, 4; none mentions the prior slot except Amendment 4 §5, which merely notes it is "filled 0.40 adopted" (`REGISTRATION.md:653`). `DECISIONS.md` contains **no ADR on the prior** (`grep -n "prior" DECISIONS.md` → no match).
  - The same commit rewrote the pin that had enforced the empty state: `test_the_real_registration_slot_is_still_empty_and_blocks_stage_b` → `test_the_real_registration_slot_is_filled_0_40_adopted`, with the refusal preserved only on a `tmp_path` fixture (`git show 2d2edc1 -- tests/test_registration_check.py`).
  - The gate is load-bearing: `REGISTRATION.md:290-292` — "**The empty slot blocks Stage B structurally**"; `report.md:126-127` records it passing as a Stage B precondition.
- **Recomputation (if any):** none required; the finding is an ordering and identity fact over git objects.
- **What would resolve it:** the operator instruction of 2026-08-27 logged verbatim in `progress.md` as standing rule 1 requires, plus a numbered amendment in `REGISTRATION.md` recording that the Section 13 prohibition at :282 was set aside, by whom, on what instruction, and with what effect on the calibration ledger.
- **Confidence:** HIGH — the prohibition, the fill, the identity of the number, the missing prompt log and the absence of an amendment are each a single quoted line or a single git object.
- **Invalidated by later commits?:** no — `REGISTRATION.md` is archived and unedited after `77ee522`, and nothing at or after the anchor (including `dff1663`) touches it.
- **Disclosed by authors?:** **partly, and that caps this at S3.** The adoption and the assistant's authorship are stated three times — "The Section 13 prior slot was filled 0.40 (adopted) on operator instruction dated 2026-08-27" (report.md:85-87); "the Section 13 slot is filled — 0.40 (adopted), **written by the assistant** on operator instruction 2026-08-27" (report.md:126-127); and the resolution is reported at report.md:265-266. What is **not** disclosed anywhere is that this is the exact act `REGISTRATION.md:282` forbids, or that the authorizing instruction was never logged. The authors' own later practice reads as a correction: the H5 registration, written 2026-08-28, strengthens the wording to "must not be copied into the slot below. **The assistant never fills the slot.**" (registrations/H5/REGISTRATION.md:346) — a sentence absent from H2's, H3's and H4's otherwise identical paragraphs.

### DRAFT-P-2
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H2 amendment stage — the precondition scan that licenses Amendment H2-3
- **Direction:** neutral (hygiene)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED (git object `f31f7a3:reports/stage_a_h2/amend_preconditions.json`)
- **Claim challenged (verbatim quote):** "(`reports/stage_a_h2/amend_preconditions.json`, PASS at 07:51:10Z on the project clock)" — NPLExperiment/report.md:446
- **Evidence:**
  - `git show f31f7a3:reports/stage_a_h2/amend_preconditions.json` → `"checked_at": "2026-08-28T06:51:10Z"` (n = 1 artifact, the only one of its kind).
  - The same figure is **06:51:10Z** in the registration itself — "PASS at 2026-08-28T06:51:10Z" — NPLExperiment/registrations/H2/REGISTRATION.md:377 — and in the state log — "### Preconditions — PASS (2026-08-28T06:51:10Z, `reports/stage_a_h2/amend_preconditions.json`)" — NPLExperiment/progress.md:831. `report.md:446` is the only place carrying 07:51:10Z.
  - 07:51:10Z is not merely different, it is impossible for the sentence it sits in ("**The preconditions, checked and recorded before anything else**", report.md:445): Amendment H2-3 was committed at **07:01:06Z** and Amendment H2-4 at **07:46:42Z**, both before the stated check time. No timezone reading reconciles it — the repository clock is `-07:00`, so 06:51:10Z is 23:51:10 local and 07:51:10Z is 00:51:10 local, neither of which is "07:51" in any frame.
- **Recomputation (if any):** none; direct comparison of one field across four files.
- **What would resolve it:** correcting `report.md:446` to 06:51:10Z, or an appended note in the repository's own correction style (as `449ff1e` did for the H5 timestamps).
- **Confidence:** HIGH — a single field, four sources, three agreeing.
- **Invalidated by later commits?:** no — `report.md` last changed at `c7bdf64` (2026-08-28T22:07:26Z), before the anchor, and is untouched at `dff1663`.
- **Disclosed by authors?:** **no.** The H5 correction sweep at `449ff1e` restated the H5 stage's ETA figures against the commit clock and corrected two artifacts, but it did not reach this line, and nothing in the repository flags it.

### DRAFT-P-3
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H5 Section 6 verdict record — the time the outcome map fired
- **Direction:** neutral (hygiene)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED (stored artifact `reports/h5/verdict.json` + git objects `c7bdf64`, `449ff1e`)
- **Claim challenged (verbatim quote):** "### The row, fired 2026-08-28T22:20Z" — NPLExperiment/report.md:667; and "**PENDING — the census window is open** · fired 2026-08-28T22:20Z." — NPLExperiment/HYPOTHESES.md:122
- **Evidence:**
  - `reports/h5/verdict.json` (anchored, tracked): `"fired_at": "2026-08-28T22:04:30Z"` — n = 1, the artifact written by `npl.h5.outcome.fire` itself.
  - The authors corrected this 3 m 45 s after committing it: "**The map actually fired at 2026-08-28T22:04:30Z**, recorded by the artifact itself (`reports/h5/verdict.json`, field `fired_at`)." — NPLExperiment/registrations/H5/REGISTRATION.md:635-637, added by `449ff1e` (2026-08-28T22:11:11Z), with the same correction in progress.md:1494-1496.
  - `git show 449ff1e --name-status` = `M progress.md`, `M registrations/H5/REGISTRATION.md`, `M reports/h5/h2_verification.json`. **`report.md` and `HYPOTHESES.md` are not in that list**, and neither file changes again before the anchor (`report.md` and `HYPOTHESES.md` both last touched at `c7bdf64`). At the anchored SHA a reader of either summary document gets 22:20Z with no cross-reference to the correction.
- **Recomputation (if any):** none.
- **What would resolve it:** propagating the correction note to `report.md:667` and `HYPOTHESES.md:122`, or a pointer from each to `registrations/H5/REGISTRATION.md:632-639`.
- **Confidence:** HIGH — the artifact, the correction, and the two uncorrected lines are each a single quoted line.
- **Invalidated by later commits?:** **no at the anchor.** `dff1663` (post-anchor) appends Amendment H5-3 to the H5 registration only and does not touch `report.md` or `HYPOTHESES.md`, so the 22:20Z lines still stand at live HEAD.
- **Disclosed by authors?:** **yes, in one of three places** — registrations/H5/REGISTRATION.md:632-639 and progress.md:1494-1496 both record the correct time and name the slip. The finding is that the correction was not propagated, not that it was concealed; per the rules this is READ-adjacent, capped at S3, and recorded here at S4 because no figure depends on it.

### DRAFT-P-4
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** Amendment H5-1's "what data existed" record — the reconnaissance probe's charge time
- **Direction:** neutral (hygiene)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED (untracked ledger, **UNANCHORED**)
- **Claim challenged (verbatim quote):** "The Task 2 / reconnaissance probe had run: **six requests**, charged to the shared ledger / at 2026-08-28T21:41Z." — NPLExperiment/registrations/H5/REGISTRATION.md:367-369
- **Evidence:**
  - `data/ledgers/requests.jsonl` (untracked, **UNANCHORED** — mtime 2026-09-12 05:06, read 2026-09-12T12:37:29Z) holds exactly six `charge` rows in that burst and six matching `settle` rows, all stamped **2026-08-28T21:39:45Z – 21:39:48Z**: `perpDexs` ×1 (21:39:45Z), `metaAndAssetCtxs` ×2 (21:39:45Z, 21:39:45Z), `fundingHistory` ×2 (21:39:46Z, 21:39:46Z), `l2Book` ×1 (21:39:48Z). The count of **six** in the claim is exact.
  - There is **no ledger activity of any kind at 21:41Z**: the last charge before the burst is 21:05:53Z and the next after it is 21:44:11Z (census pass 1).
  - The discrepancy is ~1 m 45 s and matters only because the amendment's whole force rests on that time bounding what was visible when it was written; nothing downstream reads the figure.
- **Recomputation (if any):** enumeration of the ledger between 21:39:00Z and 21:44:12Z; 6 charges, 6 settles, all HTTP 200.
- **What would resolve it:** restating 21:41Z as 21:39:45–21:39:48Z in the repository's own correction style, or an ordinary ledger append-only archive of that window committed alongside.
- **Confidence:** MEDIUM — the ledger is append-only by design and its prefix is hash-verified stable across the H5 stage (`reports/h5/h2_verification.json:shared_append_only_ledgers`), but it is untracked and 15 days of appends have landed since the anchor, so I can only assert what the file says today.
- **Invalidated by later commits?:** no — no commit at or after the anchor touches this line.
- **Disclosed by authors?:** **no.** The `449ff1e` correction sweep restated the stage's ETA figures but did not reach this one.

---

## 6. What could not be checked, and why

1. **Whether Amendment H5-1 was *written* before census pass 1 (21:44:11Z).** Its text asserts it. Git gives only the commit, `13c6965` at 21:59:42Z, which is after both census passes and which also carries the census artifacts and the implementing code. The assertion is corroborated — pass 1 lacks the `listing_status` field that Amendment H5-2 introduced, `scripts/h5_fire.py` counts those 273 rows as `rows_skipped_pre_amendment`, and Amendment H5-2 names pass 1 as its own census-in-hand — but **corroboration is not a commit boundary**. Amendment H2-3 shows the program can do better: registered in `f31f7a3` with no source file in the commit, implemented 39 minutes later in `f8e54d8`, which git proves outright. Recorded as **PARTIAL**, not a finding, because nothing contradicts it.
2. **Push times.** The documents repeatedly say "committed **and pushed**". Only commit times are observable here; `origin` was not contacted and the reflog of a remote is not readable from this side. Where the claims say "pushed", I verified "committed" and noted it. The repository records its own push verification in `amend_preconditions.json` (`origin_equals_head true`, `origin_main e89b187…`) and in `reports/h5/preconditions.json` (`origin_main fc639c7…`), which is an authored record, not an independent one.
3. **Whether the operator's 2026-08-27 instruction authorizing the prior fill exists.** Only its absence from `progress.md` is checkable. It may have been given in chat; the repository's own standing rule 1 is what makes the absence checkable at all.
4. **The 21 module hashes inside the latch at the moment of the read.** Verified to reproduce against `32b3f9e` and `844f7c2` sources, which is as close as git can put it; the latch file itself is untracked and its mtime (2026-08-27 20:01 local = 2026-08-28T03:01Z) is consistent but not cryptographic.
5. **Anything under `findings/agentA` or `findings/agentB`** — not read, per the task.
6. **Post-anchor drift.** `data/ledgers/requests.jsonl`, `data/h5/snapshots.jsonl` and `data/state/watcher.jsonl` were all appended to as recently as 2026-09-12. Every figure I drew from them is marked UNANCHORED with its read time. `data/h5/census.jsonl` (mtime 2026-08-28 14:55 local) and `data/state/generating_sample.json` (mtime 2026-08-27 20:47 local) have not moved since the stages that wrote them.

---

## 7. Live-repo access log

Live path: `/home/kiros-li/Documents/GitHub/NPLExperiment/`. All access read-only. No file under the audited repository was opened for writing, no script belonging to it was executed, no working-directory command was run inside it, and no git command other than `status`, `log`, `show`, `rev-parse` was issued.

**Pre-access `git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain`, 2026-09-12T12:31:5xZ — output verbatim:**

```
```

(empty — clean tree, no modified, staged or untracked entries; `data/` is covered by `.gitignore`)

**Post-access `git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain`, 2026-09-12T12:41:45Z — output verbatim:**

```
```

(empty — unchanged. Nothing was written to the audited repository, and no entry outside the COMMON_RULES pre-existing-dirt list appeared.)

**What was read live, and when (all UTC 2026-09-12):**

1. 12:31:5x — `git status --porcelain` (pre-access), `git rev-parse HEAD`, `git rev-parse --abbrev-ref HEAD`.
2. 12:32–12:34 — `git log --all` with `%h %ad %cd %an %s`, twice (local and `TZ=UTC --date=iso-local`); `git log --follow` on `REGISTRATION.md`, `HYPOTHESES.md`, `registrations/H2|H3|H4|H5/REGISTRATION.md`, `src/npl/config.py`, `DECISIONS.md`, `report.md`, and on eight `src/npl/h5/*.py` modules; `git log --follow --numstat` on the five registration files; `git log -S "0.40 (adopted)" --all`.
3. 12:32–12:39 — `git show` on `cd640b6`, `6399d63`, `32b3f9e`, `844f7c2`, `f31f7a3`, `f8e54d8`, `546b2e3`, `f72af92`, `98e7e01`, `13c6965`, `e0eab81`, `c7bdf64`, `b685d30`, `449ff1e`, `c2aaa27`, `2d2edc1`, `f1def31`, `6dfdbb1`, `8e31e78`, `77ee522`, `2b44c59` — `--stat`, `--name-status`, path-scoped diffs, and `<commit>:<path>` object reads. Git objects only.
4. 12:32:30 — `data/ledgers/requests.jsonl` (6,648,724 B, mtime 2026-09-12 05:06): `head -c 1200`, `wc -l` (58,599). **UNANCHORED.**
5. 12:35:19, 12:35:35, 12:37:29 — the same ledger re-read three times by a scratch script under `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl-prov/`, extracting only `ts`, `kind`, `endpoint`, `status`, `http_status` for 2026-08-28T20:00Z–23:59Z. **UNANCHORED.**
6. 12:35:39, 12:37:14 — `data/h5/snapshots.jsonl` (3,719,818 B, mtime 2026-09-11 18:56) and `data/h5/census.jsonl` (547,294 B, mtime 2026-08-28 14:55), read for `snapshot_id` counts only. **UNANCHORED** (`census.jsonl` has not moved since 2026-08-28).
7. 12:37:06, 12:37:59, 12:38:13 — `ls -la data/h5/`, `ls -la data/state/`, `ls -la data/ledgers/`; `sha256sum data/state/stage_b_read.json`; `json.load` of `data/state/stage_b_read.json` (2 keys: `read_at`, `module_hashes`) and `data/state/generating_sample.json` (`count`, `event_ids`). **UNANCHORED.**
8. 12:38:24, 12:38:38 — module-hash comparison scripts, reading `git show <commit>:src/npl/<module>` into memory and hashing; no file written inside the repository.
9. 12:41:45 — `git status --porcelain` (post-access).

No `.env`, `.keystore/`, `*.session`, credential, token or API-key file was read or listed; `.env.example` appeared in one directory listing of the snapshot and was not opened.

Scratch work written only under `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl-prov/`; all computation used `/home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python`.
