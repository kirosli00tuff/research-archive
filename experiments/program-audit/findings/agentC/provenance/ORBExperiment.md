# ORBExperiment — provenance verification (VERIFY)

**Agent C (referee/verifier). No thesis.** This document establishes what the git objects, the
stored artifacts and the untracked ledgers actually support about the repository's ordering
claims. A verified claim is recorded as plainly as a contradicted one. Unverifiable is a
legitimate result and is never guessed at.

| | |
|---|---|
| Repository | `ORBExperiment` |
| Anchored SHA | `f2aa675a80fc06b74979040b3028154d1add5ec0` (main, 2026-08-29 local / 2026-08-30T03:46:22Z) |
| Snapshot read for document text | `/home/kiros-li/.cache/program-audit/scratchpad/snap/ORBExperiment/` |
| Live repo, read-only | `/home/kiros-li/Documents/GitHub/ORBExperiment/` — git objects + untracked `data/` |
| Verified | 2026-09-12, 22:32Z–22:48Z |
| Inventory this builds on | `findings/agentC/verification/ORBExperiment.inventory.{md,json}` §4, claims P1–P22 |

**Counts. 22 inventory provenance claims plus 4 further ordering claims found during VERIFY
(P23–P26) = 26 registration claims examined: **17 SUPPORTED, 4 PARTIAL, 4 NOT_SUPPORTED,
1 UNVERIFIABLE**. **9 parameter/rule changes after data existed** were located: 8 SUPPORTED,
1 PARTIAL — and **all 9 are recorded by a dated amendment that also declares the data state.
No unamended parameter change was found.** **5 draft findings, none above S3, none touching a
verdict-relevant figure.**

---

## A structural fact that governs everything below: the repository runs on two clocks

`REGISTRATION.md` amendment headers, `progress.md` entry timestamps and `docs/DUPLICATION.md`
all use **UTC dates**. The commit author dates are **local `-07:00`**, and the rescue-pass
result artifacts stamp themselves with `datetime.date.today()`, which is the **local** date
(`ORBExperiment/tools/slippage_band.py:166`, `ORBExperiment/tools/rescue_verdict.py:115`).
Because the whole rescue pass ran between **20:12 and 20:46 local on 2026-08-29**, which is
**03:12–03:46Z on 2026-08-30**, every date in that pass exists in two versions one day apart.
The **ordering claims are all correct**; two records of them are not (DRAFT-P-1, DRAFT-P-3).

**The decisive timeline, on one clock (UTC), from git objects and the untracked request ledger:**

| UTC | event | source |
|---|---|---|
| 2026-08-30T03:12:32Z | `progress.md` Entry 33 records the rescue prompt verbatim, incl. the median→central / p90→pessimistic assignment | `ORBExperiment/progress.md:3397,3454,3474` |
| 2026-08-30T03:13:26Z | **`4ae14dc` authored/committed** — Amendment 24, the pre-committed criterion | `git show 4ae14dc` |
| 2026-08-30T03:13:27Z | **`4ae14dc` pushed to `origin/main`** | `.git/logs/refs/remotes/origin/main`, epoch 1788059607 |
| 2026-08-30T03:14:34Z / 03:14:36Z | `416c1f4` committed / pushed (Amendment 25, H1b) | git + reflog |
| 2026-08-30T03:15:35.818Z, 03:15:36.372Z | **2** `alpaca:quotes` rows — the feed probe | `data/access/requests.jsonl` (untracked, read 2026-09-12T22:36Z) |
| 2026-08-30T03:20:57.459Z → 03:39:19.048Z | **759** `alpaca:quotes` rows — the measurement itself, separated from the probe by a 321.1 s gap | same ledger |
| 2026-08-30T03:39:20.385Z | `carve_out_slippage_band` row, `measured_shift_usd_per_share = 0.46706520287790176` | `data/access/carve_out_reads.jsonl` |
| 2026-08-30T03:41:12Z / 03:41:14Z | **`5899e1b` committed / pushed** — first appearance of `tools/slippage_band.py`, `rescue_verdict.py`, `floor_scan.py`, Amendments 26 **and** 27, ADR-038, and the three result JSONs | git + reflog |
| 2026-08-30T03:46:22Z | `f2aa675`, the anchor | git |

The criterion was on the remote **26 minutes before** the measurement finished and **2 min 08 s
before the first quote request of any kind**. The ledger contains **zero** requests between
2026-08-30T00:00:00Z and the criterion push, and the only requests after it are the 761
`alpaca:quotes` rows. On every clock checked, the order claimed is the order that happened.

---

## 1. Registration claims table

Status is against **git objects and stored ledgers**, never against prose alone.

| # | claim (abbreviated) | file:line | commit named | commit found / author date (UTC) | data first existed | status | evidence |
|---|---|---|---|---|---|---|---|
| **P1** | *"The closure was decided by a criterion committed and pushed as `4ae14dc` BEFORE the measurement that decided it"* | `README.md:30-32`; `HYPOTHESES.md:58,60`; `DECISIONS.md:1342-1345`; `report.md:879-882`; `REGISTRATION.md:3959-3961` | `4ae14dc` | **yes**, `4ae14dc62328cab8a0db486622ab341cd61d2d5a`, 2026-08-30T03:13:26Z, pushed 03:13:27Z | the deciding datum (measured shift) at 2026-08-30T03:39:20.385Z | **SUPPORTED** | criterion push 03:13:27Z < first quote request 03:15:35.818Z < measurement rows 03:20:57–03:39:19Z < tool commit 03:41:12Z. `4ae14dc` touches only `REGISTRATION.md` (+96) and `progress.md` (+116) |
| **P2** | *"Amendment 24 was written, committed and pushed as `4ae14dc` **before a single line of the measuring tool existed**"* | `report.md:879-882`; `REGISTRATION.md:3671-3673` | `4ae14dc` | yes, as above | — | **SUPPORTED** | `git ls-tree --name-only 4ae14dc tools/` lists 27 tools and **none** of `slippage_band.py`, `rescue_verdict.py`, `floor_scan.py`; `git log --diff-filter=A` puts all three in `5899e1b` (03:41:12Z) |
| **P3** | *"`GO` was ruled out arithmetically in that same commit: it needed a **21.89-fold** reduction in the shift"* | `README.md:32-34`; `REGISTRATION.md:3684-3707` | `4ae14dc` | yes | — | **SUPPORTED** | the table is **inside** `git show 4ae14dc -- REGISTRATION.md`: *"required effect, `z(0.95) + z(0.80)` \| **2.486475** … **required shift** \| **0.001893 USD/share or below** … **required reduction** \| **21.89-fold**"*, and *"`GO` is unreachable and is not a tier"* |
| **P4** | *"the **assignment of median to the central band end and 90th percentile to the pessimistic end** were all nailed down in advance"* | `report.md:893-896`; `DECISIONS.md:1367-1373`; `REGISTRATION.md:3998-4000` | (none) | assignment present in **`4ae14dc`** | tool + result in `5899e1b` | **SUPPORTED** | the inventory flagged this as possibly self-attested. It is not. `4ae14dc`'s `progress.md` hunk carries the operator prompt verbatim: *"The 90th percentile is the pessimistic-end candidate and the median is the central-end candidate"* (`progress.md:3454`) and *"The assignment of median to central and 90th percentile to pessimistic is fixed in TASK 2 before the shift is computed, and any deviation voids the pass"* (`progress.md:3474`) — **28 minutes before** the tool's commit |
| **P5** | *"had bar integrity passed in full, the same power inputs fire `DEGRADED` — exactly what Section 0 predicted **in writing, before any measurement existed**"* | `README.md:85-87`; `report.md:223-228` | (none) | first commit carrying the prediction: **`bf14fa5`**, 2026-08-29T02:10:01Z | first charged vendor request 2026-08-29T02:15:46.683Z; the A.2 firing 2026-08-29T02:43:20Z | **SUPPORTED** | `git show bf14fa5:REGISTRATION.md` §"Registered expectation": *"**The Section 9 arithmetic and the decay evidence of Section 14 point to DEGRADED.** … This is stated **before any measurement exists**"*, and the residual clause *"It is registered here as **DEGRADED**"*. The prediction predates the first vendor request by 5 m 45 s and the firing by 33 min. `counterfactual_if_integrity_passed_in_full` first appears in `799e5bd` (02:44:00Z), after both |
| **P6** | *"the registered Section 6 cost model and its pessimistic band, **registered before any data existed**"* | `HYPOTHESES.md:62`; `report.md:1006-1008` | (none) | **`f69702e`**, 2026-08-29T02:06:28Z (`src/orb/config.py` created with all three tuples) | first stored fetched artifact `data/access/robots/*.txt` mtime 2026-08-29T02:13Z; first charged request 02:15:46.683Z | **SUPPORTED** | `git show f69702e:src/orb/config.py` lines 189-191: `entry_slippage_usd=(0.010, 0.020, 0.040)`, `stop_slippage_usd=(0.020, 0.040, 0.080)`, `close_slippage_usd=(0.005, 0.010, 0.020)`. Caveat, **disclosed by the authors**: three connectivity calls at ~2026-08-29T01:52Z preceded the repository itself and returned *"exactly three integers — 401, 200, 200"* (`progress.md:282-291,304`) — no market data |
| **P7** | *"Frozen `3789221b…fba3`, **latched**, and pinned by a test that recomputes it"* | `report.md:169`; `docs/STAGES.md:18` | (none) | freeze commit `9afcc33`, 2026-08-29T02:33:31Z; ledger row 02:32:28.834Z | — | **SUPPORTED (recomputed)** | I re-derived the digest from the snapshot's `orb.costs_registered.REGISTERED_COST_MODEL` with `freeze_costs.canonical`'s algorithm in my own work dir: `canonical_bytes 359`, `sha256 3789221b9dd3fea5a9680547dfdf8ec7b1febaf246042fe1fa70e27ca610fba3` — byte-for-byte the value in `data/state/cost_model_latch.json` and `cost_model.jsonl`. Scope note: `tests/test_costs.py:327-338` recomputes and asserts, but `pytest.skip`s when the untracked latch is absent, so the pin is live only in a tree that has `data/` |
| **P8** | *"A.1 TASK 9 **sealed** the registered probe slice on 2026-08-29 — 480 files, 737,507 bars, 2,400 session-ticker pairs — and the registered **14-calendar-day wait** … runs to **2026-09-12**"* | `README.md:70-77` | (none) | `ec5d17d`, 2026-08-29T07:44:12Z | — | **SUPPORTED** | `reports/stage_a1r/task9_probe_manifest.json`: `files_stored 480`, `bars_stored 737507`, `session_ticker_pairs 2400`, `pulled_at 2026-08-29`, `registered_wait_days 14`, `earliest_eligible_repull 2026-09-12` (60 sessions × 40 tickers = 2,400 ✓; 2026-08-29 + 14 d = 2026-09-12 ✓). Live `data/access/sealed_credentialed/` holds exactly **480** `task9_*` bar files plus `task9_reference_pool.raw`. `tools/repull_probe.py:87-93` returns **78** on `RepullNotDueError` |
| **P9** | *"**No vendor coverage, revision, agreement, delisting, trigger-rate or slippage figure in this repo is registered before it is measured.**"* | `docs/STAGE_A_PROMPT.md:70` (operator prompt, reproduced verbatim at `progress.md:~250`) | (none) | — | — | **NOT_SUPPORTED (one of six classes)** | five of the six classes hold — `CONFIG` carries no coverage, revision, agreement, delisting or trigger-rate constant. The **slippage band is a registered constant** at `src/orb/config.py:252-254` and `REGISTRATION.md:388-392` from `f69702e`, **before any data existed**, and was the operative input to every E2 figure until Amendment 26 measured it on 2026-08-30 at up to **13.05×** the carried value. See **DRAFT-P-4**; the carried status is **disclosed** at `REGISTRATION.md:401-405` |
| **P10** | *"Two planning figures were falsified by measurement in this pass, both **recorded rather than quietly corrected**"* | `README.md:138-144` | (none) | Amendments 11 and 15 | — | **SUPPORTED** | `REGISTRATION.md` carries **0 deleted lines** in its entire history except one placeholder line in `ba68021` (*"(Open. No amendment has been made…)"*), so no superseded figure could have been edited away. The 0.55 trigger-rate assumption survives at `REGISTRATION.md:2641,2790` beside the measured 0.982143; `README.md:410-411` carries a struck-through `~~E2 power: Absent in all nine cells~~` |
| **P11** | *"Amendment 27 was appended while this amendment's measurement was still running, and `src/orb/dispersion.py` and ADR-038 already referred to this one as 26 **in text that is committed and pushed**"* | `REGISTRATION.md:3950-3956` | (none) | Amendments 26 **and** 27, the `dispersion.py` rewrite and ADR-038 **all first appear in `5899e1b`** | — | **NOT_SUPPORTED (as to "committed and pushed")** | file order does confirm the out-of-sequence numbering (27 at `:3852`, 26 at `:3944`). But `git show 416c1f4:DECISIONS.md \| grep -c ADR-038` = **0** and `git show db92b18:src/orb/dispersion.py \| grep -c 'Amendment 26'` = **0**; the reflog shows exactly **one** push between 03:14:36Z and 03:42:01Z. No text referring to "Amendment 26" was committed or pushed before Amendment 26's own commit. The intra-commit append order is **UNVERIFIABLE**. See **DRAFT-P-5** |
| **P12** | *"H1b increments the Section 8 deflated-Sharpe trial count from 8 to 9, for H1b. **H1's count of 8 is unchanged.**"* | `DECISIONS.md:1392-1394`; `HYPOTHESES.md:105` | (none) | `f69702e` set `trial_count=8`; never edited | — | **SUPPORTED** | `src/orb/config.py:257` reads `trial_count=8` at the anchor, and `git diff f69702e f2aa675 -- src/orb/config.py` removes **0** lines — the constant has never been touched |
| **P13** | *"**No in-sample or holdout bar was ever read. Both latches remain absent.**"* | `README.md:49-50`; `HYPOTHESES.md:63`; `report.md:1018-1019` | (none) | — | — | **PARTIAL** | the absence is confirmed: `latch_path()` writes `data/state/{stage}_read.json` (`src/orb/latch.py:99-100`) and `find data -iname '*latch*'` returns only `data/state/cost_model_latch.json`, a cost-model freeze record. Neither `C_read.json` nor `D_read.json` exists. The *"never read"* half rests on Guard 5's AST walk plus the sealed-writer contract and **cannot be established from git objects**; the carve-out reads are all post-holdout (`carve_out_reads.jsonl`: sessions 2026-07-01 … 2026-08-28, all after `holdout_end 2026-06-30`) |
| **P14** | *"Storing bars is not reading them — the probe slice overlaps the holdout from **2026-05-05 to 2026-06-30** as collection"* | `HYPOTHESES.md:66`; `docs/HANDOVER.md:165-168` | (none) | — | — | **SUPPORTED** | `task9_probe_manifest.json` sessions run **2026-05-05 → 2026-07-30**; **39 of 60** fall inside the registered holdout, earliest 2026-05-05 — exactly the overlap the authors state. **Disclosed by the authors** |
| **P15** | *"**Assistant prior 0.15**, recorded **2026-08-28** before any measurement. **Operator prior 0.30** … recorded **2026-08-29** … the assistant's 0.15 was recorded first and was **visible to the operator**"* | `HYPOTHESES.md:64,83-84`; `report.md:1026-1027` | (none) | 0.15 → `b5ea51b` 2026-08-29T02:12:08Z and `14d37ea` 02:13:02Z; 0.30 → `4147bb8` 2026-08-29T06:38:38Z | first charged request 2026-08-29T02:15:46.683Z | **PARTIAL** | the **substantive claims verify**: 0.15 precedes 0.30 by **4 h 26 m**, and 0.15 precedes the first charged vendor request by **3 m 39 s**, so *"before any measurement"* holds. `git show 14d37ea:HYPOTHESES.md:57` reads *"**Assistant prior** \| **0.15**, recorded 2026-08-28, before any measurement"* with the operator slot **EMPTY**. But the two *dates as written* use different clocks — both priors fall on **2026-08-28 local** and both on **2026-08-29 UTC**; neither clock separates them by a day. The non-blindness is **disclosed** at `HYPOTHESES.md:84`. See **DRAFT-P-3** |
| **P16** | *"**A later reader can verify the ordering in `git log`**: this commit precedes the commit that contains the measuring tool."* | `REGISTRATION.md:3727-3729`; `DECISIONS.md:1345` | `4ae14dc` | yes | — | **SUPPORTED** | `git log` shows `4ae14dc` (03:13:26Z) two commits before `5899e1b` (03:41:12Z); the `origin/main` reflog additionally shows the **push** order (03:13:27Z vs 03:41:14Z), which `git log` alone would not |
| **P17** | *"**`CONFIG.entry_slippage`, `stop_slippage` and `close_slippage` are unchanged** … This amendment records a measurement beside them; it does not re-register them."* | `REGISTRATION.md:4053-4057` | (none) | last `config.py` change is `c9b73e9`, 2026-08-29T19:18:48Z | — | **SUPPORTED** | the `src/orb/config.py` **blob is byte-identical** (`43a63452d893ad52e87aa0409b4c6adb7ca531a2`) at `c9b73e9`, `df16da1`, `4ae14dc`, `416c1f4`, `5899e1b`, `7edeea7`, `68a1c65`, `34a91b3` and `f2aa675`. The measuring commit does not touch it |
| **P18** | *"**Everything above was measured before any credential existed and is left standing.** `n = 1,026` requests charged on 2026-08-29."* | `README.md:181-182` | (none) | keyless probes 2026-08-29T02:15–02:19Z; credentialed pulls from 06:35Z | — | **SUPPORTED (with a scope note)** | `data/access/sealed/` and `probe_findings.json` mtimes 2026-08-28 19:13–19:19 local (= 02:13–02:19Z); earliest file in `sealed_credentialed/` is 2026-08-28 23:42 local (= 06:42Z) — the keyless table predates the credentials by ~4.5 h. The **1,026** is exact as of the commit that wrote it: the ledger holds precisely 1,026 rows at or before `d535dc4` (2026-08-29T07:56:19Z). It is a **pass-scoped increment**, not a repository total; the README's four increments 1,026 + 979 + 0 + 759 = 2,764 against a ledger total of 2,766, the difference being the 2 pre-tool feed-probe quote rows |
| **P19** | `criterion_precommitted_on: "2026-08-30"` recorded beside `computed_at`/`measured_at: "2026-08-29"` | `reports/stage_a3rescue/task3_rescue_verdict.json:3-6`; `task2_slippage_band.json:52` | `4ae14dc` | — | — | **NOT_SUPPORTED (as a record; the underlying order is SUPPORTED)** | `tools/rescue_verdict.py:45` hard-codes `CRITERION_DATE = "2026-08-30"` (the amendment's **UTC** date) while `:115` and `tools/slippage_band.py:166` use `date.today()` (the **local** date, 2026-08-29). The artifact therefore asserts `criterion_precommitted_before_the_measurement: true` beside two dates that say the opposite. See **DRAFT-P-1** |
| **P20** | *"Run 2026-08-29, STAGE A.-1 TASK 0, **before a single line of design was written.** … **Verdict: CLEAR.** … All 14,002 raw hits across 11 repositories are incidental"* | `docs/DUPLICATION.md:3-12` | (none) | `c26d9ae`, 2026-08-29T01:58:37Z | — | **PARTIAL** | the **ordering holds**: `c26d9ae` precedes every design commit — `f69702e` (scaffold/guards, 02:06:28Z), `93db5ad` (CLAUDE.md), `bf14fa5` (Section 0), `b2b7cba`/`b5ea51b` (Sections 1-14), `14d37ea` (HYPOTHESES.md). Only `840de7c` (a 3-file placeholder: `.env.example`, `.gitignore`, a 9-line README), `3c8d836` (the operator's own prompt) and `a167b5d` (the prompt log) precede it. The **14,002 hit count is UNVERIFIABLE**: no stored output artifact exists, the screened set includes `MLCryptoTrader` and `[personal repo, name removed]` which are **out of this audit's scope and must not be re-run**, and a re-run today would not reproduce the 2026-08-29 state |
| **P21** | *"mutation 13 … **when this was written the edge had ONE pin and the suite went green** … A.1 TASK 5 added a second, independent fixture … and the harness now CATCHES it."* | `reports/stage_a2repair/mutations.md:21` | (none) | — | — | **SUPPORTED (from git objects)** | tracked through `reports/stage_a4/mutations.md`: at `389cce7` and `b84b941` row 13 reads `… \| GUARD STOPPED BINDING \| yes \| ` ` (expected-green, no failing test); at `ecec44d` (A.1 TASK 5, where `orb.dispersion` lands) the same row flips to `**NO** \| FAILED tests/test_dispersion.py…`; from `d33c2b2` the prose explanation appears. **Disclosed by the authors** and additionally corrected in the open at `REGISTRATION.md:2870-2895` (Amendment 17 §1) rather than by editing Amendment 11 §6 |
| **P22** | *"**The operator pre-committed to this on 2026-08-30, before the measurement**, and this amendment is the record of that commitment."* | `REGISTRATION.md:3726-3727` | `4ae14dc` | commit verified | — | **UNVERIFIABLE (the operator act); SUPPORTED (the commit)** | the commit and its push are git facts. The **operator's** act of pre-committing is attested only by the amendment written inside that commit. Nothing outside the repository corroborates it and nothing inside it could. Recorded, not scored |
| **P23** *(found during VERIFY)* | *"The branch text was written before the numbers were read, and the three verdicts, their thresholds and their consequences were fixed in `orb.integrity.TapeVerdict` and pinned by boundary test **before** `tools/tape_identify.py` sent its first request."* | `REGISTRATION.md:1404-1408` | (none) | `TapeVerdict`, `tape_same_*` constants, `tools/tape_identify.py` and `tests/test_tape.py` **all** first appear in **`86a2553`**, 2026-08-29T06:59:36Z | first `massive:aggs` request 2026-08-29T06:42:59.099Z | **PARTIAL / self-attested** | the only commit carrying the thresholds postdates the first tape request by **16 m 37 s**, so git can neither confirm nor deny. Recorded because Amendment 24 shows the repository knows how to make such an ordering checkable and did not do so here. No sign of a band fitted to the answer: the measured median ratio 1.005197 sits mid-band in `[0.90, 1.10]` and the two controls ≈0.0278 sit far below the 0.50 `DIFFERENT_TAPE` edge |
| **P24** *(found during VERIFY)* | *"It changes no Section 0 branch. `src/orb/section0.py` is **byte-identical** to its state before this pass."* | `REGISTRATION.md:3657-3659` (Amendment 23) | (none) | `section0.py` last changed in `1c4a244`, 2026-08-29T07:49:44Z | — | **SUPPORTED** | the blob is `8dc49b006af7b2c4e9ccf9b67941bc3262f7bb17` at `c4ccb4e`, `c9b73e9`, `421113d`, `db92b18`, `3d3ef1d`, `56409d9`, `acd85fe`, `df16da1`, `4ae14dc`, `5899e1b` and `f2aa675` — identical across both the inference-repair and rescue passes |
| **P25** *(found during VERIFY)* | *"this amendment deliberately fixes the null before the figures that will be fed into it exist"* (Amendment 19, the E2 replacement) | `REGISTRATION.md:3128-3131` | (none) | Amendment 19 lands in **`421113d`**, 2026-08-29T19:21:19Z | the execution-mix measurement it feeds: `carve_out_reads.jsonl` row at 2026-08-29T**19:25:20.212Z**; its commit `db92b18` at 19:26:19Z | **SUPPORTED** | the amendment commit precedes the measurement by **4 m 01 s** and its commit by 5 m 00 s. Amendment 20 relies on this (*"including Amendment 19, which fixed E2's null before these figures existed, so the null cannot have been chosen to suit them"*, `REGISTRATION.md:3256-3258`) and the reliance is sound |
| **P26** *(found during VERIFY)* | *"Every entry states the ETA given before the task was armed and the **actual elapsed** against it"* | `progress.md:3-4`; totals at `progress.md:878,2147,2973,3364,3712` | (none) | — | — | **NOT_SUPPORTED** | the five "actual" totals sum to **2,191 min (36.5 h)**. The repository's **entire** commit history spans **26 h 09 m 11 s** (`840de7c` 2026-08-29T01:37:11Z → `f2aa675` 2026-08-30T03:46:22Z), and the five working windows sum to **~4 h 20 m**. See **DRAFT-P-2** |

---

## 2. Parameter changes after data existed

Method: `git log --follow -p` on every registration-bearing source file, plus a per-commit
deletion scan over `src/orb/**`, `REGISTRATION.md`, `HYPOTHESES.md`, `DECISIONS.md`,
`README.md`, `report.md` and `progress.md`. **`src/orb/config.py` removes zero lines across its
whole history** (`git diff f69702e f2aa675 -- src/orb/config.py` shows no `-` line), so no
registered constant was ever edited or deleted — every change below is an **addition beside**
the superseded figure.

| # | what changed | where | commit / UTC | data that existed | dated amendment? | verdict-relevant? | note |
|---|---|---|---|---|---|---|---|
| C1 | **per-co-primary alpha 0.02532057 → 0.05** (Šidák union correction replaced by an intersection-union test) | `src/orb/config.py:256`; `src/orb/verdict.py` `per_test_alpha()` | `c9b73e9`, 2026-08-29T19:18:48Z | E1/E2 power tables at the old alpha already published (`reports/stage_a2/power.json`, Amendments 15-16) | **yes — Amendment 18**, `REGISTRATION.md:3000-3117`, dated 2026-08-29, with *"What data existed when this amendment was made"* | **YES — it moved E1 across the 0.80 GO floor** | the amendment states the consequence itself, unprompted: *"**At the registered 1.40 Sharpe assumption, E1 crosses its 80 percent bar on the achievable holdout for the first time: 0.743521 → 0.832450.**"* (`:3088`) and *"the minimum session count … falls from 1,006 to 795"*. `alpha_adj` is kept and kept correct. **Loosening in direction, but the Berger (1982) IUT argument is correct** and the conjunction supplies the conservatism. **Recorded, not a finding** |
| C2 | **E2's null replaced** — from a Sharpe-rescale to a pessimistic-cost economic null; new estimators `e2_pessimistic_mean`, `e2_power_pessimistic`, `trades_for_e2_power` | `src/orb/power.py` (+76 lines, **0 removed**) | `421113d`, 2026-08-29T19:21:19Z | measured dispersion 2.029585 (n = 550) and E1 at the corrected alpha; **the exit mix and shift did not yet exist** | **yes — Amendment 19**, `REGISTRATION.md:3120-3248` | **YES** — E2 power 0.743533 → 0.043277 → 0.000000 | fixed **before** the figures it consumes (P25, verified to the minute). The change moved the design **against** the hypothesis. **Recorded, not a finding** |
| C3 | **post-holdout carve-out added** (`post_holdout_start_ms = 1_782_878_400_000`), turning a one-sided pre-period carve-out into a two-sided one; `src/orb/preperiod.py` rewritten (-29/+…) | `src/orb/config.py:232`; `src/orb/preperiod.py`; `src/orb/bars.py` | `389cce7`, 2026-08-29T18:01:56Z | the falsifying measurement: 0 of 2 credentials serve any session before 2016-01-04 (n = 16 probes each) | **yes — Amendment 11**, `REGISTRATION.md:2003-2179`, with a data-state paragraph | indirectly — it is the window every later measurement used | boundary set at Eastern midnight, with the reason written out (`config.py:26-35`). **Recorded, not a finding** |
| C4 | **`consolidated_feed = "sip"` promoted from a function default to a guarded config field** | `src/orb/config.py:237`; `src/orb/vendors.py` | `b84b941`, 2026-08-29T18:12:15Z | the A.1 TASK 4 tape measurement, n = 100 pairs | **yes — Amendment 13**, `REGISTRATION.md:2243-2384` | no | **Recorded, not a finding** |
| C5 | **tape thresholds registered**: `tape_same_min_ratio 0.90`, `tape_same_max_ratio 1.10`, `tape_different_max_ratio 0.50`, `tape_single_venue_share_max 0.20` | `src/orb/config.py:274-277`; `src/orb/integrity.py` | `86a2553`, 2026-08-29T06:59:36Z | the tape pulls themselves — `massive:aggs` from 2026-08-29T06:42:59.099Z | **yes — Amendment 7**, `REGISTRATION.md:1391-…`, with *"Exactly what data existed…"* | it gates whether BLOCKED-4 may fire | **the only change whose "fixed before the measurement" claim git cannot check** (P23): thresholds, tool and boundary tests all land in one commit **after** the first request |
| C6 | **`alpaca:bars` operating pace 1.0 s → 0.61 s** (98.36/min) | `src/orb/vendors.py:147` | `d24584c`, 2026-08-29T18:23:38Z | measured burst allowance 384 in 55.96 s; 250 admitted at 199.73/min over 75.10 s | **yes — Amendment 14**, `REGISTRATION.md:2386-2541` | no | `PACE_BASIS` records exactly what each pace rests on, and labels `alpaca:quotes` *"unmeasured endpoint; carries its vendor's figure"* |
| C7 | **Alpaca provisional daily cap 2,000 → 3,000** | `src/orb/vendors.py` `PROVISIONAL_DAILY_CAPS` | `d24584c`, 2026-08-29T18:23:38Z | ≥1,026 requests already charged | **yes — Amendment 14**, and the docstring says so in place: *"Alpaca's moved from 2,000 to 3,000 by Amendment 14, 2026-08-29"* | no | the raise was not load-bearing: Alpaca's actual 2026-08-29 total was **1,879**, under the old cap |
| C8 | **Section 0 outcome map extended** — `PENDING_SPEND` and `PENDING_REVISION` states added and the Amendment-1 precedence clause refined so a *measured* BLOCKED trigger fires ahead of the pending states | `src/orb/section0.py` (-39/+…) | `1c4a244`, 2026-08-29T07:49:44Z | credentials authenticating, measured reach, tape verdict | **yes — Amendment 10**, `REGISTRATION.md:1839-2001`, with a data-state paragraph | **YES — it is the map that fires the standing verdict** | the new states are documented in the code itself as *"Registered by Amendment 10, 2026-08-29"*. **Recorded, not a finding** |
| C9 | **cross-vendor agreement gate narrowed to the measured overlap** (459 holdout sessions, 0 in-sample) | `REGISTRATION.md` Amendment 8; SL-3 at Amendment 12 | `f4534f1` / `56409d9` era, 2026-08-29 | measured reach: Alpaca 2016-01-04, Massive 2024-08-29, n = 16 probes each | **yes — Amendments 8 and 12** | it narrows a BLOCKED trigger's scope | narrowing recorded as a scope limitation (SL-3) rather than a silent edit. **Recorded, not a finding** |

**Result: 9 of 9 changes are covered by a dated amendment that also declares the data state.
All 28 amendments carry a `**Date:**` header and a "what data existed" paragraph. No unamended
parameter change was found, and `REGISTRATION.md` is append-only across its whole history.**

---

## 3. Draft findings

Five findings. **None is above S3 and none touches a verdict-relevant figure.** The
repository's central provenance claim — the pre-committed criterion — verifies in full.

### DRAFT-P-1
- **Repository / SHA:** ORBExperiment / `f2aa675a80fc06b74979040b3028154d1add5ec0`
- **Hypothesis or artifact:** H1 closure; `reports/stage_a3rescue/task3_rescue_verdict.json` and `task2_slippage_band.json`
- **Direction:** neutral (pure hygiene — the underlying order is the one claimed)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** `"computed_at": "2026-08-29",` / `"criterion_commit": "4ae14dc",` / `"criterion_precommitted_before_the_measurement": true,` / `"criterion_precommitted_on": "2026-08-30",` — ORBExperiment/reports/stage_a3rescue/task3_rescue_verdict.json:3-6; and `"measured_at": "2026-08-29",` — ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json:52
- **Evidence:** the deciding artifact records a criterion date **one day after** the measurement date while simultaneously asserting the criterion came first. The two fields are produced on different clocks: `CRITERION_DATE = "2026-08-30"` is a hard-coded constant copied from Amendment 24's UTC-dated header (ORBExperiment/tools/rescue_verdict.py:45), while `computed_at` and `measured_at` come from `date.today().isoformat()`, the **local** date (ORBExperiment/tools/rescue_verdict.py:115; ORBExperiment/tools/slippage_band.py:166). The pass ran 20:12–20:46 local `-07:00` = 03:12–03:46Z. `reports/stage_a3rescue/task5_section0.json:3,79` repeats the mixture: `"fired_at": "2026-08-30T03:42:21+00:00"` beside `"rescue_criterion_precommitted_on": "2026-08-30"` and, in the same tree, `measured_at: "2026-08-29"`. No document anywhere in the repository discloses the clock mixture (grep for `UTC`/`timezone`/`local time`/`-07:00` across README, REGISTRATION, HYPOTHESES, DECISIONS, report and HANDOVER returns only session-clock and carve-out-boundary material). Ledger and reflog read from `/home/kiros-li/Documents/GitHub/ORBExperiment/data/access/requests.jsonl` and `.git/logs/refs/remotes/origin/main` at **2026-09-12T22:36Z** (untracked / UNANCHORED).
- **Recomputation (if any):** criterion pushed at reflog epoch **1788059607** = 2026-08-30T03:13:27Z (ORBExperiment/.git/logs/refs/remotes/origin/main); first `alpaca:quotes` charge 2026-08-30T03:15:35.818Z; 759 measurement charges 03:20:57.459Z → 03:39:19.048Z; `carve_out_slippage_band` row 03:39:20.385Z; tool commit `5899e1b` 03:41:12Z, pushed 1788061274 = 03:41:14Z. Criterion precedes the measurement by **26 min** on a single clock. Tolerance: none needed; the gap is minutes.
- **What would resolve it:** stamp both fields from the same clock — either `datetime.now(UTC).date()` in both tools, or record full ISO-8601 instants with offsets instead of bare dates. A one-line note in Amendment 26 or 28 saying which field is UTC and which is local would also resolve it.
- **Confidence:** HIGH — the constant and the `date.today()` call are both in the anchored tree and the reflog times are unambiguous.
- **Invalidated by later commits?:** no — the artifacts and tools are anchored at `f2aa675`; a later commit could add the missing note but cannot change what these bytes say.
- **Disclosed by authors?:** no — the repository discloses the session-clock issue for market data (ADR-014, `DECISIONS.md:376-396`) and the Eastern-vs-UTC carve-out boundary (`report.md:446`), but never that its own record dates run on two clocks.

### DRAFT-P-2
- **Repository / SHA:** ORBExperiment / `f2aa675a80fc06b74979040b3028154d1add5ec0`
- **Hypothesis or artifact:** the five `progress.md` ETA tables — the repository's only record of what the work cost
- **Direction:** neutral (pure hygiene — no verdict figure depends on it)
- **Class:** PROVENANCE (process record)
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** *"Append-only. One entry per sub-stage. Every entry states the ETA given before the task was armed and the **actual elapsed** against it, per standing rule 2."* — ORBExperiment/progress.md:3-4; and *"| | **total** | **370 min (6.17 h)** | **348 min (5.80 h)** |"* — ORBExperiment/progress.md:3712; and *"**The estimate was 5.9 percent high.** The single overrun was **TASK 2 (+6)**, where **759 quote requests at a one-second registered pace took thirteen minutes of wall clock that no amount of planning removes**"* — ORBExperiment/progress.md:3714-3717
- **Evidence:** the five recorded totals are **658** min (ORBExperiment/progress.md:878), **438** min (`:2147`), **401** min (`:2973`), **346** min (`:3364`) and **348** min (`:3712`) — **2,191 min = 36.5 h**. The repository's entire git history spans **26 h 09 m 11 s**: `840de7c` authored 2026-08-29T01:37:11Z to `f2aa675` authored 2026-08-30T03:46:22Z (`git log --date=iso-strict`). The five working windows, taken from each pass's first to last commit, are 79 m 33 s, 80 m 50 s, 49 m 08 s, 18 m 01 s and 32 m 56 s — **260 m 28 s ≈ 4 h 20 m** in total. The rescue pass in particular claims **348 min** for work bounded by `progress.md:3397` (*"Recorded 2026-08-30T03:12:32Z … Nothing was written, measured, requested or amended before this line"*) and the final commit at 03:46:22Z — **33 m 50 s**, a factor of **10.3**. The "thirteen minutes of wall clock" sub-claim is also short: the 759 measurement quote rows in `data/access/requests.jsonl` (read 2026-09-12T22:36Z, UNANCHORED) run 2026-08-30T03:20:57.459Z → 03:39:19.048Z = **18 m 22 s**, median inter-request gap 1.382 s rather than the 1.0 s the sentence assumes. The claimed total (36.5 h) **exceeds the whole wall-clock span of the repository (26.2 h)**, so no interpretation of "actual" as elapsed time can be made to fit.
- **Recomputation (if any):** inputs — the five totals at ORBExperiment/progress.md:878, 2147, 2973, 3364, 3712; commit author dates from `git log --format='%ad' --date=iso-strict`; entry timestamps at ORBExperiment/progress.md:284, 910, 2174, 3015, 3397. Method: sum the "actual" column; subtract each pass's first commit instant from its last; compare with the full-history span. Result: claimed 2,191 min vs. an available 1,569 min of total elapsed history and ~260 min of commit-bounded working time. Tolerance: the conclusion survives any reasonable allowance for pre-first-commit and post-last-commit work, because the claimed total exceeds the whole history.
- **What would resolve it:** state the unit the "actual" column is in (it is plainly not elapsed wall clock), or replace the column with commit-to-commit elapsed times, which git already records exactly. A one-line note in `CLAUDE.md` standing rule 2 would suffice.
- **Confidence:** HIGH — commit timestamps and the ledger are unambiguous, and the shortfall is an order of magnitude, not a rounding.
- **Invalidated by later commits?:** no — the tables are anchored text and the timestamps that contradict them are immutable git objects.
- **Disclosed by authors?:** no — `progress.md:3-4` explicitly calls the column "actual elapsed", and `progress.md:3716` interprets one entry as "wall clock", so no alternative unit is offered anywhere.

### DRAFT-P-3
- **Repository / SHA:** ORBExperiment / `f2aa675a80fc06b74979040b3028154d1add5ec0`
- **Hypothesis or artifact:** the session log's ordering record, and the calibration-ledger prior dates
- **Direction:** neutral (pure hygiene — every substantive ordering it supports independently verifies)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** *"**Recorded 2026-08-30T00:00Z.** Standing rule 1 requires the operator prompt to be reproduced verbatim in this file before any other work."* — ORBExperiment/progress.md:910; and *"**Assistant prior** | **0.15**, recorded **2026-08-28**, before any measurement"* / *"**Operator prior** | **0.30**, label **INDEPENDENT**, recorded **2026-08-29**"* — ORBExperiment/HYPOTHESES.md:83-84
- **Evidence:** (a) `progress.md` Entry 7 stamps itself **2026-08-30T00:00Z**, but it was introduced by commit `cc086ad`, authored **2026-08-29T06:35:29Z** (`git log -S 'Entry 7 — the A.1 resumption prompt' -- progress.md`) — the entry claims to have been written **17 h 24 m after the commit that contains it**, and its stamp is later than Entry 20's (`progress.md:2174`, 2026-08-29T17:51:28Z) and Entry 28's (`:3015`, 19:16:04Z), both of which appear **after** it in the append-only file. Every other entry stamp is consistent to within minutes of its commit: `:284` 01:57:20Z vs `a167b5d` 01:57:58Z (38 s); `:2174` 17:51:28Z vs `389cce7` 18:01:56Z (10 m); `:3015` 19:16:04Z vs `c9b73e9` 19:18:48Z (2 m 44 s); `:3397` 03:12:32Z vs `4ae14dc` 03:13:26Z (54 s). Entry 7 is the single outlier and 00:00Z reads as a placeholder. (b) the two priors' recorded dates use different clocks: 0.15 enters at `b5ea51b` 2026-08-29T02:12:08Z and `14d37ea` 02:13:02Z, 0.30 at `4147bb8` 2026-08-29T06:38:38Z — **both fall on 2026-08-28 local and both on 2026-08-29 UTC**, 4 h 26 m apart, so the stated "2026-08-28" / "2026-08-29" separation exists on no single clock.
- **Recomputation (if any):** n/a — commit author dates from `git log --date=iso-strict`, pickaxe searches `git log -S` on `progress.md` and `HYPOTHESES.md`.
- **What would resolve it:** an appended correction entry giving Entry 7's true recording instant (the repository's own Amendment 17 pattern), and one clock for both prior dates.
- **Confidence:** HIGH for (a) — a commit cannot contain text written 17 hours later; HIGH for (b) — both commit instants are exact.
- **Invalidated by later commits?:** no — both are anchored text contradicted by anchored commit metadata.
- **Disclosed by authors?:** no. The **substantive** claims both hold and should be recorded as verified: 0.15 was recorded **first**, 4 h 26 m before 0.30 and 3 m 39 s before the first charged vendor request; and the operator's non-blindness is disclosed at ORBExperiment/HYPOTHESES.md:84.

### DRAFT-P-4
- **Repository / SHA:** ORBExperiment / `f2aa675a80fc06b74979040b3028154d1add5ec0`
- **Hypothesis or artifact:** H1; the Section 6 slippage band and every E2 figure computed from it before 2026-08-30
- **Direction:** neutral — the eventual measurement made the closure **stronger**, not weaker; the pre-measurement figures it affected have all been superseded in the anchored tree
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** READ (the rule) + DERIVED (the registered constant and its commit)
- **Claim challenged (verbatim quote):** *"No vendor coverage, revision, agreement, delisting, trigger-rate or slippage figure in this repo is registered before it is measured. Every such figure below is named as an A.1 or A.2 measurement target, never as an input."* — ORBExperiment/docs/STAGE_A_PROMPT.md:70
- **Evidence:** a slippage band **was** registered before it was measured and was used as an input. `src/orb/config.py:252-254` carries `entry_slippage_usd=(0.010, 0.020, 0.040)`, `stop_slippage_usd=(0.020, 0.040, 0.080)`, `close_slippage_usd=(0.005, 0.010, 0.020)` from commit `f69702e`, authored 2026-08-29T02:06:28Z — before the first charged vendor request at 2026-08-29T02:15:46.683Z. `REGISTRATION.md:388-392` registers the same table. These figures are the operative input to the pessimistic shift `0.020 + 0.381818×0.040 + 0.618182×0.010 = 0.04145455` and thus to the E2 pessimistic-cost mean of **−0.001068** and E2 power **0.043277** that Amendment 21 reported as "E2 collapses". They were measured for the first time on 2026-08-30, at up to **13.05×** the carried value (ORBExperiment/REGISTRATION.md:3973-3996; `reports/stage_a3rescue/task2_slippage_band.json`). The other five named classes hold: `CONFIG` contains no coverage, revision, agreement, delisting or trigger-rate constant, and the 0.55 trigger-rate **assumption** was never a config constant and was recorded as falsified (Amendment 15).
- **Recomputation (if any):** shift check — inputs `REGISTRATION.md:388-392` (band) and `reports/stage_a3rescue/task3_execution_mix.json` (`stop_exit_share 0.38181818181818183`); method `0.020 + s×0.040 + (1−s)×0.010`; result `0.04145454545454545`, matching `mean_pessimistic_shift_usd_per_share` in `data/access/carve_out_reads.jsonl` exactly. This confirms the carried band, not a measurement, produced that figure.
- **What would resolve it:** a line in Amendment 26 acknowledging that the band was the one figure in the prompt's six named classes that **was** registered before measurement, beside the reason it was kept (the §8 argument is otherwise sound).
- **Confidence:** HIGH — the constant, its commit and the prompt sentence are all anchored text.
- **Invalidated by later commits?:** no — Amendment 26 §8 explicitly declines to move the band, so the state persists at the anchor.
- **Disclosed by authors?:** **partially, and this matters.** The band's carried, unmeasured status is disclosed from the first registration commit: *"The independent replication measured the sibling index strategy's net PnL crossing zero at roughly 0.022 USD per share of entry slippage (**carried**, Section 14)"* — ORBExperiment/REGISTRATION.md:401-405, and it is labelled `C-6` at `:876` and `:3973`. What is **not** disclosed anywhere is the tension with the governing rule at `docs/STAGE_A_PROMPT.md:70`. Per the audit rules this finding is therefore capped at S3.

### DRAFT-P-5
- **Repository / SHA:** ORBExperiment / `f2aa675a80fc06b74979040b3028154d1add5ec0`
- **Hypothesis or artifact:** Amendment 26's account of its own out-of-sequence numbering
- **Direction:** neutral (pure hygiene)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** *"**This amendment is numbered 26 and appears in this file after Amendment 27.** Amendment 27 was appended while this amendment's measurement was still running, and `src/orb/dispersion.py` and ADR-038 already referred to this one as 26 **in text that is committed and pushed**. **The number is kept so every existing reference stays valid, the file order is the true chronology of appends, and the anomaly is recorded here rather than tidied away by editing pushed text.**"* — ORBExperiment/REGISTRATION.md:3950-3956
- **Evidence:** nothing referring to "Amendment 26" was committed or pushed before Amendment 26 itself. `git show 416c1f4:DECISIONS.md | grep -c 'ADR-038'` = **0**; `git show db92b18:src/orb/dispersion.py | grep -c 'Amendment 26'` = **0**. Amendment 26 (`REGISTRATION.md:3944`), Amendment 27 (`:3852`), the `dispersion.py` rewrite (+587 lines, whose `:145,152` carry the "Registered by Amendment 26" text) and ADR-038 (`DECISIONS.md:1424,1427`) **all first appear in the single commit `5899e1b`**, authored 2026-08-30T03:41:12Z. The `origin/main` reflog shows exactly one push between `416c1f4` (epoch 1788059676 = 03:14:36Z) and `7edeea7` (1788061321 = 03:42:01Z), namely `5899e1b` at 1788061274 = **03:41:14Z**. So the premise the note rests on — that the "26" references were already pushed and therefore immutable — is not what git records; the whole set went out in one push. The **file order** part of the claim does verify (27 at `:3852` sits above 26 at `:3944`), and the numbering anomaly is genuinely recorded rather than tidied away. The **intra-commit append order** is UNVERIFIABLE from commit boundaries.
- **Recomputation (if any):** none.
- **What would resolve it:** rephrasing to "in text committed in the same commit as this amendment", or nothing at all — the substance (an anomaly disclosed rather than hidden) is intact.
- **Confidence:** HIGH on the git facts; the finding is about the stated justification only.
- **Invalidated by later commits?:** no — `5899e1b` and the reflog are immutable.
- **Disclosed by authors?:** no, but note the authors volunteered the anomaly itself, which is the opposite of concealment. This is recorded as hygiene and nothing more.

---

## 4. What could not be checked, and why

1. **The operator's act of pre-committing (P22).** `REGISTRATION.md:3726-3727` records a human decision. The commit is verifiable; the decision behind it is attested only by the amendment the operator's assistant wrote inside that commit. Nothing outside the repository corroborates it and nothing inside it could. **UNVERIFIABLE, recorded, not scored.**
2. **The 14,002 duplication hits (P20).** No stored output artifact exists; the recorded `grep` (`docs/DUPLICATION.md:16-28`) screens `MLCryptoTrader` and `[personal repo, name removed]`, which are **out of this audit's scope and must not be read**, and a re-run in 2026-09 would not reproduce the 2026-08-29 state of eleven repositories. The **ordering** half of the claim is verified; the count is **UNVERIFIABLE**.
3. **Intra-commit ordering, twice.** Amendment 7's *"fixed … before `tools/tape_identify.py` sent its first request"* (P23) and Amendment 26's append order (P11/DRAFT-P-5) both assert an ordering **inside** a single commit. Git records commits, not working-tree edits. Both are **UNVERIFIABLE**; neither is contradicted.
4. **"No bar was ever read" (P13).** The absence of both stage latches is verified on the live filesystem. The blindness itself rests on Guard 5's AST walk (`test_no_module_reads_a_priced_bar_field_anywhere`) and the sealed-writer return-type contract. I did not run the suite — running a repository's tests in place is forbidden by the common rules — so the guard's coverage is **asserted, not verified here**. Two real catches are **disclosed by the authors** at `reports/stage_a4/gates.md:29-38`.
5. **Working-tree state before each commit.** The repository's strongest provenance device (splitting the criterion into its own commit and push, `4ae14dc`) is exactly the thing that makes P1–P4 checkable. Where a pass did not split — `5899e1b` carries TASK 2's tool **and** TASK 3's verdict artifact **and** TASK 4's floor scan in one commit, which `progress.md` Entry 35 discloses by grouping "TASKS 2, 3 and 4" in one entry — the finer ordering is simply not recorded anywhere git can reach.

**Checked and found sound, recorded so it is not re-opened:**

- `REGISTRATION.md` is **append-only across its entire history** — the only deletion in any commit is the two-line placeholder *"(Open. No amendment has been made…)"* replaced by Amendment 1 in `ba68021`. `DECISIONS.md`, `report.md` and `src/orb/power.py` have **zero** deleted lines in any commit.
- `src/orb/config.py` has **zero** deleted lines across its whole history; every registered constant that exists at the anchor has existed unchanged since the commit that introduced it.
- **All 28 amendments** carry a `**Date:**` header and a "what data existed when this amendment was made" declaration (Amendments 1-10 phrase it "Exactly what data existed…").
- **Pacing compliance.** Sub-registered-spacing gaps in `data/access/requests.jsonl` cluster exactly where the registered **ceiling-escalation measurements** ran (`alpaca:bars` 672 sub-0.61 s gaps ≈ the 384-request burst plus the 250-request sustained probe; `massive:*` likewise). The rescue-pass quote stream honoured its 1.0 s registered spacing on 758 of 760 gaps (median 1.382 s), the two exceptions being 0.524 s and one other. **No finding.**
- **Ledger reconciliation.** `quote_requests_sent = 759` in `task2_slippage_band.json` matches exactly 759 sealed `task2q_*` files and exactly 759 ledger rows once the 2 pre-tool feed-probe rows (separated by a 321.1 s gap) are excluded from the 761 `alpaca:quotes` rows. The 760 "quote minutes served" is 550 entry + 210 stop minutes. Everything reconciles.
- **Stray but unclaimed artifact placement.** `reports/stage_a1r/task5_section0.json` is the **identical blob** (`9fbbe44e…`) to `reports/stage_a3rescue/task5_section0.json`, both written in `34a91b3` (2026-08-30T03:43:15Z); likewise `reports/stage_a1r/task6c_section0.json` = `reports/stage_a2repair/task6_section0.json` (`3a05a991…`, both in `acd85fe`). `reports/stage_a4/mutations.md` is a **rolling** file rewritten in 8 commits and at the anchor holds the rescue pass's 17 mutations, not stage A.4's 10. No document claims these directories are pass-scoped, so this is recorded as an observation rather than a finding — though it was the rolling file that made P21 verifiable.
- **`README.md:181-182`'s `n = 1,026`** is exact as of the commit that wrote it (`d535dc4`) and is presented as one of four per-pass increments, not a total. **No finding.**

---

## 5. Live-repo access log

**Repository:** `/home/kiros-li/Documents/GitHub/ORBExperiment/`

| | verbatim output | time (UTC) |
|---|---|---|
| `git -C … status --porcelain` **before** first access | *(empty — no output, exit 0)* | **2026-09-12T22:32:03Z** |
| `git -C … status --porcelain` **after** last access | *(empty — no output, exit 0)* | **2026-09-12T22:48:25Z** |
| `git rev-parse HEAD` at both checks | `f2aa675a80fc06b74979040b3028154d1add5ec0` | both |

**Both status outputs were empty. No pre-existing dirt, and none introduced.**

**Read-only git operations performed:**
`git rev-parse HEAD` (×2); `git status --porcelain` (×2);
`git log --format=… --date=iso-strict` (full history, and `--follow` / `-S` / `--diff-filter=A`
per path on `REGISTRATION.md`, `HYPOTHESES.md`, `DECISIONS.md`, `progress.md`, `README.md`,
`report.md`, `src/orb/*.py`, `tools/slippage_band.py`, `tools/rescue_verdict.py`,
`tools/floor_scan.py`, `tools/tape_identify.py`, `tests/test_tape.py`,
`reports/stage_a4/mutations.md`, `reports/stage_a1r/*`);
`git show <sha> --stat` and `git show <sha> -- <path>` on `4ae14dc`, `5899e1b`, `7edeea7`,
`68a1c65`, `34a91b3`, `f2aa675`, `416c1f4`, `bf14fa5`, `f69702e`, `86a2553`, `389cce7`,
`b84b941`, `c9b73e9`, `421113d`, `d24584c`, `1c4a244`, `ba68021`, `c26d9ae`, `840de7c`,
`3c8d836`, `d535dc4`, `db92b18`, `ecec44d`, `d33c2b2`, `df16da1`, `acd85fe`;
`git show <sha>:<path>` (REGISTRATION.md, HYPOTHESES.md, DECISIONS.md, config.py, section0.py,
dispersion.py, reports/stage_a4/mutations.md);
`git ls-tree --name-only` on `4ae14dc tools/`, `5899e1b tools/`, `f2aa675 src/orb`;
`git rev-parse <sha>:<path>` for blob identity on `src/orb/section0.py`, `src/orb/config.py`,
`reports/stage_a1r/task5_section0.json`, `reports/stage_a3rescue/task5_section0.json`,
`reports/stage_a1r/task6c_section0.json`, `reports/stage_a2repair/task6_section0.json`;
`git diff f69702e f2aa675 -- <path>`;
`cat .git/logs/refs/remotes/origin/main`.

**Untracked data opened read-only** (all under `data/`, read 2026-09-12T22:33Z–22:44Z):
`ls -la` on `data/`, `data/state/`, `data/access/`, `data/access/{robots,fees,sealed,sealed_credentialed}`;
JSON/JSONL parse of `data/access/requests.jsonl` (fields `day`, `endpoint`, `kind`,
`recorded_at`, `vendor` only — the ledger carries no payload and no credential),
`data/access/carve_out_reads.jsonl` (4 rows, printed in full),
`data/state/cost_model.jsonl`, `data/state/cost_model_latch.json`;
filename census of `data/access/sealed_credentialed/` (names and mtimes only);
`find data -iname '*latch*'`.

**Not opened:** `.env` (never listed, never read). **No `.raw` payload, no sealed bar file, no
HTML fee body, no `seals.jsonl` row content was read.**

**Modifications made: none.** No file under `/home/kiros-li/Documents/GitHub/ORBExperiment/` was
created, edited, renamed or deleted; no repository script was executed in place; no git command
that writes was issued. The one recomputation (P7) was run in
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-prov-ORB/recompute2/` on a **copy**
of the read-only snapshot's `src/`, with the venv Python.

**Unanchored caveat:** everything read from `data/` is untracked working-tree state read
**fourteen days after the anchor** and may have changed since 2026-08-30. The mtimes and ledger
rows used above are all dated 2026-08-28/29/30 and are internally consistent with the git
timestamps, but they are not anchored objects. `_PARKED_CHECK_BEFORE_RUNNING` (dated 2026-09-02,
noted in the inventory) postdates the anchor and was **not** used to adjudicate anything here.

**Anchoring caveat:** every claim adjudicated here is a claim about `f2aa675` (2026-08-30T03:46:22Z).
ORBExperiment's last six commits all landed within 33 minutes of each other, and the repository's
own binding calendar date — the earliest eligible bar-revision re-pull — is **2026-09-12**, the day
this verification was run. A later commit could add the revision measurement and move the Section 0
verdict; it could not change the commit ordering, the blob identities or the ledger timestamps on
which every finding above rests.
