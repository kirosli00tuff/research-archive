# VRPExperiment — provenance verification (Agent C, referee)

**No thesis. This pass establishes what the git objects, the stored artifacts and the file
system actually support about when bars, parameters, maps, priors and decision rules were
fixed. A verified claim is reported as verified. Unverifiable is reported as unverifiable and
is never guessed at.**

| | |
|---|---|
| Repository | `VRPExperiment` |
| Anchored SHA | `d37cf6d190dfdaef8e613daf099a507fe1a77dcf` (main, 2026-08-30) |
| Snapshot read for document text | `/home/kiros-li/.cache/program-audit/scratchpad/snap/VRPExperiment/` |
| Live repo | `/home/kiros-li/Documents/GitHub/VRPExperiment/` — **read-only**: `git log/show/diff/ls-tree/cat-file/rev-parse/status`, plus `ls`/`stat`/`find` on the gitignored `data/` tree |
| Compiled | 2026-09-05, 03:56Z–04:10Z |
| Input | `findings/agentC/verification/VRPExperiment.inventory.md` §4 (23 provenance claims P1–P23) |
| Result | Registration claims (23): **20 SUPPORTED, 2 PARTIAL, 1 NOT_SUPPORTED**. Parameter/artifact changes after data existed (9): **6 SUPPORTED, 3 PARTIAL**, of which one is wholly unrecorded. **4 draft findings**, all S3. Nothing contradicts the closure, the hurdle, the estimator or the pre-data ordering |

## The authoritative timeline

The whole history is 12 commits on one evening, all by one author, all with author date ==
committer date, all at `-0700` (PDT). Converted to UTC from the raw commit objects
(`git cat-file -p`):

| commit | UTC (from the commit object) | subject |
|---|---|---|
| `eda2d65` | 2026-08-30T04:22:18Z | Repo init: scaffold placeholder |
| `31c9345` | 04:33:00Z | log governing Stage A prompt to progress.md |
| `7df214c` | 04:37:16Z | TASK 0 — preconditions, remote, duplication screen |
| `8bcc5bf` | 04:43:31Z | TASK 1 — uv scaffold, five structural guards, TASK 6 latch |
| **`7827592`** | **04:47:08Z** | **TASK 2 — REGISTRATION.md, "committed before any network call"** |
| `3ad6098` | 06:22:23Z | TASK 3 — venue reachability measured |
| `0c873f5` | 06:30:32Z | TASK 4 — public data access measured |
| `c51b4f7` | 06:49:19Z | TASK 5 — cost measured; **`src/vrp/sealed_read.py` first appears** |
| `adac707` | 06:55:29Z | TASK 6 machinery; **latch 1 written 06:55:35.492Z (6.5 s later)** |
| `ef07f19` | 06:58:00Z | attempt 1 aborted; Amendment 1; **latch 2 written 06:58:05.858Z** |
| `ba50596` | 07:02:58Z | TASK 6/7 — the sealed read and the fired verdict |
| `d37cf6d` | 07:08:02Z | TASK 8 — artifact, README, ADRs, handover (**the anchor**) |

**When data first existed.** The `data/` tree is gitignored, so the only evidence is
filesystem timestamps, read from the live tree at **2026-09-05T04:05:58Z** (UNANCHORED — these
may have changed since the 2026-08-30 anchor):

- `data/` directory **birth 2026-08-30T04:37:46Z** — an empty directory created ~30 s after
  the TASK 0 commit. It held nothing.
- `data/raw/` **birth 2026-08-30T04:47:24.128Z**.
- **First byte of network-fetched data anywhere: `data/raw/robots/www.deribit.com.robots.txt`,
  mtime 2026-08-30T04:47:24.3064702500Z** — **16.2 seconds after the registration commit**.
- First data artifact committed to git: `reports/task3/*` in `3ad6098`, 06:22:23Z.
- First `progress.md` entry recording a measurement: the TASK 3 block appended in `3ad6098`.

**No file under `data/` and no blob in any commit before `7827592` contains a network
result.** The four commits preceding the registration add only local material: a placeholder
README, the verbatim prompt, `docs/DUPLICATION.md` (a local `grep -rniI` screen), the guard
modules, and `reports/env_report.json` (a local toolchain report).

---

## 1. Registration claims table

Every claim from the inventory's §4, with the git object that settles it. Line numbers are in
the anchored snapshot; `REGISTRATION.md` lines 1–528 are **byte-identical** between `7827592`
and the anchor (verified by `diff` of the two blobs), so a §0–§9 line number is valid at both.

| # | claim (abridged; verbatim quotes in the findings below) | file:line | commit named | commit found / date | data first existed | status |
|---|---|---|---|---|---|---|
| **P1** | "Registered 2026-08-30, **before any network call**. Commit `8bcc5bf` is the last commit before this file; no probe, fetch or measurement precedes it." | `REGISTRATION.md:3-4` | `8bcc5bf` | yes — `8bcc5bf01bd2d38ef48f529292d19c6d8187e8fc`, 04:43:31Z, and it **is** the parent of `7827592` (`git rev-parse 7827592^` ⇒ `8bcc5bf…`) | 04:47:24.306Z (first robots body) | **SUPPORTED** — registration blob predates the first artifact by 16.2 s. Qualified: see DRAFT-P-2 and §4 (fetches that leave no artifact cannot be timed) |
| **P2** | "`REGISTRATION.md`, commit `7827592`, **before any network call**." | `HYPOTHESES.md:18`; `docs/HANDOVER.md:95` | `7827592` | yes — `78275921ca8f4cad72fd7bf2f10155dcf58cb507`, 04:47:08Z, adds `REGISTRATION.md` (533 lines, `A`) | as P1 | **SUPPORTED** |
| **P3** | "`REGISTRATION.md` \| Sections 0–9, committed **before any network call**; Amendment 1" | `README.md:102` | — | `REGISTRATION.md` has exactly two commits: `A` at `7827592`, `M` at `ef07f19` | 04:47:24Z | **SUPPORTED** — `git diff 7827592 ef07f19 -- REGISTRATION.md` is one hunk at `@@ -529,5 +529,61 @@`: a 2-line replacement in the Amendment-log stub plus 56 appended lines. Nothing at or above line 528 changes |
| **P4** | "Any amendment is appended here with its date, its reason, and the commit that introduced it. **No section above is edited in place.**" | `REGISTRATION.md:531-533` | — | as P3 | 04:47:24Z | **SUPPORTED** |
| **P5** | "**Measured 2026-08-30, 04:32Z–05:35Z.**" | `reports/task3/venue_table.md:3` | — | introduced in `3ad6098`, 06:22:23Z | robots 04:47:24Z; TASK 3 page captures 06:13:56Z–06:17:54Z | **NOT_SUPPORTED** — see **DRAFT-P-2**. The stated window starts 15 min before the registration commit and ends ~43 min before the last artifact it describes |
| **P6** | "the conversion to basis points, **registered before any number exists** … **One volatility point of premium is 22.875 bps of notional.**" | `REGISTRATION.md:152, 166` | — | first and only introduction of "2,287.5" and of the §2.6 text is `7827592` (`git log -S`) | 04:47:24Z | **SUPPORTED** — pre-data by 16 s; code emits 22.874639 (`src/vrp/sealed_read.py`, added `c51b4f7` 06:49:19Z, 9.5 min before the first task6 byte) |
| **P7** | "Registered before any data so the rebalance count is not a free parameter … ±0.10 … additionally reported at **±0.05 and ±0.20**" | `REGISTRATION.md:287, 296` | — | text in `7827592`; the code sweep `(0.05, 0.10, 0.20)` first appears in `adac707` 06:55:29Z | 04:47:24Z (text); 06:58:57Z (task6 series) | **SUPPORTED** — the bands are registered pre-data; the implementation matches and predates the sealed read |
| **P8** | "with **the statistic assigned to each end registered here, before anything downstream is computed**" (central = median, pessimistic = p90) | `REGISTRATION.md:268` | — | `7827592` | 04:47:24Z | **SUPPORTED** |
| **P9** | "the lower bound of the premium's one-sided 95% confidence interval must exceed the PESSIMISTIC end … by a **factor of 2.0** … **Registered before any number exists**" | `REGISTRATION.md:314` | — | `git log -S"factor of 2.0"` ⇒ **`7827592` only**. Never edited | 04:47:24Z | **SUPPORTED** — the hurdle is pre-data and was never touched. The derived "8.57×" failure figure first appears in `ba50596` (07:02:58Z), i.e. with the result, as it should |
| **P10** | "**Newey–West HAC with bandwidth 30** … **Registered before any data, not after an audit.**" | `REGISTRATION.md:366-371` | — | `7827592` | 04:47:24Z | **SUPPORTED** — `newey_west_se` and `estimate_premium(bandwidth=TENOR_DAYS, alpha=0.05)` with `TENOR_DAYS = 30`, `MIN_OBSERVATIONS = 60` are present in the **first** version of `sealed_read.py` (`c51b4f7`) and the file is unchanged below line 304 thereafter |
| **P11** | "**Robustness, registered now:** … non-overlapping … **If they disagree in sign or significance, the disagreement is the finding**" | `REGISTRATION.md:372-375` | — | `7827592` | 04:47:24Z | **SUPPORTED** as a provenance claim (registered pre-data). Whether the clause was correctly evaluated is a verification question, not a provenance one |
| **P12** | "**Fallback, registered now so it is not chosen later** … recorded as used or not used; it is never blended" | `REGISTRATION.md:95-100` | — | `7827592` | 04:47:24Z | **SUPPORTED** — recorded **not used** at `docs/ACCESS.md:268-270` |
| **P13** | "**POPULATED BY TASK 3. NOT BEFORE.** **This section registers the criterion. It registers no venue and no figure.**" | `REGISTRATION.md:179-181` | — | `7827592` | 04:47:24Z | **SUPPORTED** — §3 at `7827592` (identical to the anchor) carries criteria and a candidate list only |
| **P14** | "**POPULATED BY TASK 5. NOT BEFORE.** **No carried figure is registered in this section. None.**" | `REGISTRATION.md:246-247` | — | `7827592` | 04:47:24Z | **SUPPORTED, with a note** — §4 registers no VRP cost figure. §4.2 (lines 275–283) *does* quote five ORBExperiment figures (0.467065 / 0.041455 / 11.27× / 0.033529 / 0.040) as a named precedent, immediately followed by "**This registration carries no cost figure from anywhere.**" Read as "no cost input for this experiment", the claim holds; read as "no number from elsewhere appears in §4", it does not. Not raised as a finding: the figures are labelled as a lesson, not as inputs |
| **P15** | "Assistant prior 0.12 / **0.76** / 0.12 … **recorded 2026-08-30 before any network call**" | `HYPOTHESES.md:17`; `REGISTRATION.md:475-497` | `7827592` | present in `7827592` §9.1; unchanged (P3) | 04:47:24Z | **SUPPORTED** |
| **P16** | "### 9.2 Operator prior > **RESERVED — EMPTY.** … the absence is recorded as an absence rather than backfilled" | `REGISTRATION.md:499-506`; `HYPOTHESES.md:92` | — | `7827592`; still empty at `d37cf6d` (P3 proves no edit) | — | **SUPPORTED** |
| **P17** | "At 2026-08-30T06:55:35.492Z the TASK 6 latch was written … recording the SHA-256 of all ten `src/vrp` modules and of the run tool, **at commit `adac707`**." | `REGISTRATION.md:537-539` | `adac707` | yes — `adac70715195e30c39ed5a09a8932385e8fe8ec3`, 06:55:29Z | latch written 6.5 s after the commit | **SUPPORTED — recomputed.** All **11** SHA-256 in `task6.latch.json` equal `sha256(git show adac707:<path>)` exactly, for the ten `src/vrp/*.py` and `tools/task6_sealed_run.py`. Same check on `task6.latch.2.json` against `ef07f19`: all 11 match |
| **P18** | "the only change between attempt 1 and attempt 2 is a **single string literal** … `"3600"` to `"60"` — plus the attempt-numbering … **No estimator, no window, no estimator parameter, no tenor, no sign convention and no inference rule was touched.**" | `REGISTRATION.md:578-584`; ADR-007 `DECISIONS.md:133-155` | `ef07f19` | yes — `ef07f19537b249a5e3aec96c17640da009ab192e`, 06:58:00Z | task6 series 06:58:57Z (after both) | **PARTIAL** — the *code* half is **fully verified**: `git ls-tree -r adac707 src/vrp` and `… ef07f19 src/vrp` are byte-identical (and stay identical through the anchor); the driver diff is exactly the `resolution` literal + a comment, `latch_path(attempt)`, `--attempt`, `report["attempt"]/["latch_path"]`, the latch note and the output-name suffix. **But the same commit also re-ran and replaced the committed fixture artifact** at a smaller window — see **DRAFT-P-4** |
| **P19** | "**No estimator ran.** `reports/task6/real_result.json` does not exist." | `REGISTRATION.md:559-561` | — | — | — | **SUPPORTED** — `git log --all --name-only \| grep real_result` returns nothing (exit 1). The only files ever added under `reports/task6/` are `fixture_result.json` (`adac707`), `task6.latch.json` (`ef07f19`), `real_attempt2_result.json` and `task6.latch.2.json` (`ba50596`) |
| **P20** | "**No data was written.** `data/raw/task6/` was empty after the abort." | `REGISTRATION.md:562-563` | — | — | 06:58:57Z / 06:59:48Z | **SUPPORTED (unanchored)** — `data/raw/task6/` holds exactly four files, mtimes 06:58:57Z (BTC pair) and 06:59:48Z (ETH pair), i.e. **after** latch 2 at 06:58:05.858Z and matching `finished_at 06:59:48Z` in the result. Nothing there predates attempt 2. Evidence is mtimes on gitignored files, read 2026-09-05T04:05:58Z |
| **P21** | "**The instant is fixed here, before the TASK 6 latch, at 08:00 UTC**" | `docs/ACCESS.md:275-280`; ADR-005 `DECISIONS.md:93-111` | — | `docs/ACCESS.md` §6 appended in `adac707`, 06:55:29Z; latch 1 written 06:55:35.492Z | TASK 4 data 06:23–06:27Z **preceded** the choice | **PARTIAL** — the ordering claim is **SUPPORTED**: §6 is in a commit 6.5 s before the latch, and `REGISTRATION.md:141-142` pre-authorised the deferral ("The instant is fixed at the first read and never moved"). Corroboration is strong: `src/vrp/tzguard.py:10` states "Deribit settles at 08:00 UTC" in `8bcc5bf` — **before the registration and before any network call** — and `reference_spreads_deribit.json` records expiry `2026-09-25T08:00:00Z`. **The justifying probe itself is unverifiable**: the "400-day window, timestamps only, no value read, n = 401 rows" measurement has no stored artifact and no committed tool (§4 below) |
| **P22** | "Measure it, label it **REFERENCE ONLY, not a cost input**, and let no verdict read it." | ADR-008 `DECISIONS.md:159-167`; `reference_spreads_deribit.json.status` | — | ADR-008 in `d37cf6d`; the artifact's own `status` field carries the label from `c51b4f7` | — | **SUPPORTED** — the deciding arithmetic in `HYPOTHESES.md:21` is commission-only ("measured commission-only cost 122.140 bps central / 162.853 bps pessimistic"). No Deribit spread figure enters it |
| **P23** | "**The TASK 6 latch is spent and is not re-runnable.** `--mode real` raises `LatchAlreadySpentError`." | `README.md:124-125`; `docs/HANDOVER.md:69-72` | — | `src/vrp/latch.py` (`8bcc5bf`, never changed) raises on `self._path.exists()` | — | **SUPPORTED, with a note** — the quoted sentence is exactly true: default `--attempt 1` resolves to `task6.latch.json`, which exists, so `--mode real` raises. The broader phrase "not re-runnable" is bounded by the mechanism: `latch_path(attempt)` (added in `ef07f19`) gives a *new* path per `--attempt`, so the bar is per-latch-file, not per-repository. Both the argument and its rationale are documented in the tool's own help text |

**Additionally established and not claimed by the repository:**

- `progress.md` is **strictly append-only** across all nine commits that touch it: every diff
  is a single hunk with **zero deletions** (`+68/-0`, `+43/-0`, `+83/-0`, `+104/-0`, `+84/-0`,
  `+95/-0`, `+94/-0`, `+39/-0`). No narrative was ever rewritten.
- `src/vrp/sealed_read.py` was extended once (`c51b4f7` → `adac707`) and the diff is
  `@@ -304,3 +304,102 @@` — **pure append**. Not one line of the estimator (mean, HAC SE,
  t, one-sided p, CI lower, bps scaling) was altered after it was written, and it was written
  9.5 minutes before the first byte of TASK 6 data existed.
- `tests/test_estimators.py` was likewise extended by pure append (`@@ -252,3 +252,72 @@`).
- `d37cf6d` is titled "venue-table corrections" but **does not touch
  `reports/task3/venue_table.md`**. The corrections are written to a new file,
  `docs/VENUE_TABLE_UPDATE.md`, addressed to a *different* repository (MLCryptoEngine), with
  an explicit "The MLCryptoEngine repository was not edited and must not be edited by this
  repository." No post-verdict edit was made to the venue table.
- The one carried figure in the whole repository — MLCryptoEngine's `$6,505` MBT notional,
  quoted pre-data in the prior at `REGISTRATION.md:491` — is explicitly retired against the
  measurement at `reports/task3/venue_table.md:95` ("The measurement wins… Every sleeve
  calculation above uses $7,812.46").

---

## 2. Parameter changes after data existed

"Data existed" is taken as **2026-08-30T04:47:24.306Z** (the first fetched byte) for
registration parameters, and as the relevant task's own data time where narrower.

| # | what changed | where | commit / UTC | data that existed at the time | dated amendment? | verdict-relevant? | status |
|---|---|---|---|---|---|---|---|
| C1 | `REGISTRATION.md` Amendment log stub replaced and Amendment 1 (56 lines) appended | `REGISTRATION.md:529-586` | `ef07f19` / 06:58:00Z | all of TASK 3/4/5; **no TASK 6 premium value** | **yes — Amendment 1, dated 2026-08-30, with reason, cause, and the commit named** | the amendment governs the sealed read | **SUPPORTED** — and it is the only edit `REGISTRATION.md` ever received |
| C2 | request literal `"resolution": "3600"` → `"60"` on the underlying leg | `tools/task6_sealed_run.py:155` | `ef07f19` / 06:58:00Z | TASK 3/4/5 data; the abort produced an HTTP 400 and no series | **yes — Amendment 1** | yes (it is what made the read possible) | **SUPPORTED** — diff verified; `src/vrp` blobs identical either side |
| C3 | attempt plumbing: `latch_path(attempt)`, `--attempt`, output-name suffix, latch note, `report["attempt"]`, `report["latch_path"]` | `tools/task6_sealed_run.py` | `ef07f19` / 06:58:00Z | as C2 | **yes — Amendment 1** ("plus the attempt-numbering that keeps the first latch") | no | **SUPPORTED** |
| C4 | fixture re-run: `days_requested` **900 → 300**, so `n` 870 → 270 per asset; the committed `fixture_result.json` was replaced | `reports/task6/fixture_result.json` | `ef07f19` / 06:57:32Z (run) | TASK 3/4/5 data; synthetic fixture data only for this artifact | **no** — Amendment 1 does not mention it, and it says "the only change … is a single string literal … plus the attempt-numbering" | no — the fixture is synthetic machinery verification, planted premium unchanged at 0.08 | **PARTIAL → DRAFT-P-4** |
| C5 | observation instant fixed at **08:00 UTC**; sampling changed to hourly-and-filter | `docs/ACCESS.md:275-303` (new §6) | `adac707` / 06:55:29Z | TASK 4 probes (06:23–06:27Z) and an unstored 400-day timestamp probe | **not an amendment** — `REGISTRATION.md:141-142` explicitly deferred the instant to "the first read"; recorded dated-by-commit in `ACCESS.md` §6 and later in ADR-005 | **yes** — it selects which hourly row becomes each daily observation | **SUPPORTED as ordering (pre-latch), UNVERIFIABLE as justification** (see §4) |
| C6 | `docs/ACCESS.md` §4 table row edited **in place**: "sampling frequency … `resolution=43200` and `3600` both served" → "**08:00 UTC**, taken hourly and filtered — see below" | `docs/ACCESS.md:264` | `adac707` / 06:55:29Z | TASK 4 data | no marker on the edited row itself; §6 immediately below explains the change | no | **PARTIAL** — hygiene only; the substance is disclosed 11 lines later, and the edit is visible in the diff |
| C7 | `docs/ACCESS.md` §1.2 supported-resolution list extended `60, 3600, 43200` → `+ 1D` | `docs/ACCESS.md:62-66` | `adac707` / 06:55:29Z | TASK 4 data | **yes, in line** — "*(`1D` was found on a later probe during TASK 6 preparation and is appended here rather than silently folded into the original list…)*" | no | **SUPPORTED** — a model self-correction, disclosed at the point of edit |
| C8 | fetch horizon `--days-back` default set to **1992** | `tools/task6_sealed_run.py:427` | `adac707` / 06:55:29Z | TASK 4's bisection, 06:23Z | not an amendment; the figure is the measured `deepest_served_days_back: 1992` in `reports/task4/deribit_probe.json:158,629` and is reported as such in `docs/ACCESS.md` and `README.md:88` | it sets the maximum available `n`, but is a measurement of *availability*, not of outcome | **SUPPORTED** — data-derived, but derived from a depth probe taken before any premium value could be seen, and openly sourced |
| C9 | `reports/env_report.json` regenerated (`git_head` `7df214c…` → `ba50596…`) | `reports/env_report.json:2-3` | `d37cf6d` / 07:08:02Z | everything | n/a — it is a toolchain snapshot | no | **SUPPORTED** — the recorded `git_head` and porcelain are consistent with generation during TASK 8 |

**No other file was ever modified after being added.** The complete set of files with an `M`
in history is: `progress.md` (8 appends), `README.md`, `.gitignore`, `REGISTRATION.md`,
`docs/ACCESS.md`, `reports/env_report.json`, `reports/task6/fixture_result.json`,
`src/vrp/sealed_read.py`, `tests/test_estimators.py`, `tools/task6_sealed_run.py`. Every one
is accounted for above or is a pure append.

---

## 3. Draft findings

Four. All are DERIVED from git objects or stored artifacts. **None contradicts the closure,
the hurdle, the estimator, or the registration's pre-data ordering** — the ordering survives
every check I could make against git objects and file births.

### DRAFT-P-1

- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** the TASK 8 data-revision re-check (`reports/task4/revision_recheck.json`), which is the evidence that Deribit does not silently revise history and therefore that a single sealed read is safe
- **Direction:** B — it makes a stated robustness figure weaker than claimed: the interval over which the venue was shown not to revise is **half** the interval stated
- **Class:** PROVENANCE (equally INTERNAL_INCONSISTENCY — the figure contradicts the timestamps inside the very artifact that carries it)
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**all six fixed windows byte-identical after ≈ 70 minutes**" — VRPExperiment/README.md:91. Repeated verbatim at `docs/ARTIFACT.md:280` ("re-fetched ≈ 70 minutes later"), `DECISIONS.md:190` ("re-checked after ≈ 70 minutes"), `progress.md:819-820` ("data-only baselines recorded at 06:05Z were re-fetched at ~07:15Z, a gap of **≈ 70 minutes**"), and inside the artifact itself as `"gap": "≈70 minutes"` — VRPExperiment/reports/task4/revision_recheck.json:3
- **Evidence:**
  - The artifact's own machine-written timestamps, all six windows (n = 6): `taken_at` = `2026-08-30T06:26:08.230Z`, `.399Z`, `.569Z`, `.772Z`, `.941Z`, `2026-08-30T06:26:09.144Z`; `recheck_taken_at` = `2026-08-30T07:03:22Z` (window 0) and `07:03:23Z` (windows 1–5) — VRPExperiment/reports/task4/revision_recheck.json:3 ff.
  - The baseline artifact agrees: `"retrieved_at": "2026-08-30T06:25:49.532Z"` — VRPExperiment/reports/task4/rate_and_revision_baseline.json; and the underlying files carry mtimes 2026-08-30T06:26Z (live tree, read 2026-09-05T04:00:18Z, UNANCHORED).
  - `progress.md:819`'s two component stamps are both wrong against the artifact: "06:05Z" vs the recorded 06:26:08Z, and "~07:15Z" vs the recorded 07:03:22Z. The claimed re-fetch time 07:15Z is also **after** `d37cf6d`'s commit time of 07:08:02Z, which is the commit that adds the file — impossible.
- **Recomputation:** inputs `revision_recheck.json` `windows[0].taken_at` = 06:26:08.230Z and `windows[0].recheck_taken_at` = 07:03:22Z; method: difference of the two ISO-8601 UTC stamps; result **37 min 13.77 s**; range across all six windows 37 min 12.9 s – 37 min 14.9 s; tolerance ±1 s. The stated "≈ 70 minutes" is **1.88× the elapsed interval**.
- **What would resolve it:** correcting the four documents and the artifact's `gap` string to "≈ 37 minutes"; or producing a second, earlier baseline at 06:05Z that the recheck was actually compared against (no such artifact exists, and `rate_and_revision_baseline.json`'s own `retrieved_at` is 06:25:49.532Z).
- **Confidence:** HIGH — the contradicting timestamps are machine-written and sit in the same JSON file as the claim.
- **Invalidated by later commits?:** no — `revision_recheck.json` is added in the anchor commit itself and both files are tracked and unchanged since.
- **Disclosed by authors?:** no. The repository does disclose that the CDD arm of the same re-check is "a **weak** test and is recorded as one" (`progress.md:823-826`), but nowhere records that the 70-minute figure is not what its own artifact says.

### DRAFT-P-2

- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** the TASK 3 venue table — the measurement that fires the VENUE_BLOCKED closure — and its stated measurement window
- **Direction:** neutral (hygiene) — the artifact evidence resolves the ordering question *in the repository's favour*; what fails is the stated window itself
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Measured 2026-08-30, 04:32Z–05:35Z.** Every classification below is evidenced by published text recorded with its URL and its date." — VRPExperiment/reports/task3/venue_table.md:3
- **Evidence:**
  - Stated start **04:32Z** is **15 min 8 s before** the registration commit `7827592` at **04:47:08Z** (raw commit object: `1788065228 -0700`). Taken literally it contradicts "no probe, fetch or measurement precedes it" — VRPExperiment/REGISTRATION.md:3-4 — and "committed **before any network call**" — VRPExperiment/README.md:102.
  - The artifacts the section describes do not fit the window at either end (live tree, read 2026-09-05T04:05:58Z, UNANCHORED): the seven `data/raw/robots/*.txt` bodies are 04:47:24.306Z–04:48:02.855Z, and the TASK 3 page captures run **06:13:56.669Z – 06:17:54.479Z** (n = 15 files), ending ~43 min *after* the stated 05:35Z end.
  - The in-document retrieval stamps in the same task are offset from their own artifacts by almost exactly one hour: "Retrieved: 2026-08-30T05:13Z" (`reports/task3/deribit_restricted_jurisdictions_verbatim.md:7`) against `deribit_restricted_jurisdictions.html` mtime 06:13:57.084Z; "retrieved 2026-08-30T05:15Z" (`venue_table.md:38`) against `ibkr_ca_mbt_met_options.html` mtime 06:15:29.921Z; "Retrieved 2026-08-30T05:27Z" (`robots_and_terms.md:20`) against `cme_refusal.json` mtime 06:17:54.479Z.
  - The machine clock was correct: machine-written stamps agree with mtimes to the second (`rate_and_revision_baseline.json` `retrieved_at` 06:25:49.532Z vs mtimes 06:26Z; `real_attempt2_result.json` `finished_at` 06:59:48Z vs `dvol_ETH_daily.json` mtime 06:59:48Z). Only the hand-written stamps drift.
  - What the artifacts **can** settle: `data/raw/` was born 04:47:24.128Z and its first file 04:47:24.306Z, so **no fetched byte predates the registration**. What they cannot settle: the section's live spot measurement (Coinbase and Kraken, `venue_table.md:9-16`) **wrote no file** — `data/raw/task3/` contains no Coinbase or Kraken response — so that particular fetch cannot be timed from evidence at all.
- **Recomputation:** none required; the finding is a comparison of a document string against commit-object epochs and inode mtimes.
- **What would resolve it:** correcting the header to the window the artifacts support (≈04:47Z–06:18Z); or storing the Coinbase/Kraken spot responses, which would let the one untimeable fetch in the deciding section be ordered against the registration.
- **Confidence:** HIGH for the mismatch (three independent stamp classes disagree with the artifacts); MEDIUM for the reading that it is a mis-stamp rather than a real pre-registration fetch — mis-stamp is strongly the more likely, since every hand-written TASK 3 stamp is offset the same way and no artifact predates the registration.
- **Invalidated by later commits?:** no — `venue_table.md` has exactly one commit (`3ad6098`) and was never edited, including by the anchor commit that is titled "venue-table corrections".
- **Disclosed by authors?:** no.

### DRAFT-P-3

- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** `progress.md`, the running provenance ledger, whose section headers are the repository's own record of when each task completed
- **Direction:** neutral (hygiene)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "## 2026-08-30T07:35Z — TASK 8 COMPLETE — artifact and close-out" — VRPExperiment/progress.md:814. (The same defect at `progress.md:249` "## 2026-08-30T05:04Z — TASK 2 COMPLETE — REGISTRATION.md, before any network call" and at `progress.md:758` "## 2026-08-30T07:12Z — TASK 7 COMPLETE — Section 0 fired".)
- **Evidence:** each header was introduced by a commit whose own timestamp is earlier than the header claims. `git log -S"<header>" -- progress.md` gives the introducing commit; raw commit objects give the UTC time. n = 10 headers:

  | header stamp | introduced by | commit UTC | header − commit |
  |---|---|---|---|
  | 04:32:03Z TASK 0 START | `31c9345` | 04:33:00Z | −57 s (consistent) |
  | 04:38Z TASK 0 COMPLETE | `7df214c` | 04:37:16Z | **+44 s** |
  | 04:52Z TASK 1 COMPLETE | `8bcc5bf` | 04:43:31Z | **+8 min 29 s** |
  | 05:04Z TASK 2 COMPLETE | `7827592` | 04:47:08Z | **+16 min 52 s** |
  | 05:40Z TASK 3 COMPLETE | `3ad6098` | 06:22:23Z | −42 min 23 s |
  | 06:12Z TASK 4 COMPLETE | `0c873f5` | 06:30:32Z | −18 min 32 s |
  | 07:00Z TASK 5 COMPLETE | `c51b4f7` | 06:49:19Z | **+10 min 41 s** |
  | 07:05Z TASK 6 COMPLETE | `ba50596` | 07:02:58Z | **+2 min 2 s** |
  | 07:12Z TASK 7 COMPLETE | `ba50596` | 07:02:58Z | **+9 min 2 s** |
  | 07:35Z TASK 8 COMPLETE | `d37cf6d` | 07:08:02Z | **+26 min 58 s** |

  Seven of ten headers are stamped **after** the commit that contains them, which cannot be
  true of text already inside that commit; two others are stamped 18–42 minutes early. The
  worst case, TASK 8, is off by 27 minutes; `progress.md:816` compounds it with "**ETA 45
  min · actual ~23 min**" for a task whose commit falls 5 min 4 s after the previous one.
  The consequence that matters: **`progress.md:249` read literally says the registration was
  completed at 05:04Z, i.e. 17 minutes after the first network fetch at 04:47:24.306Z.** The
  git objects say otherwise and are authoritative, so the pre-registration guarantee stands —
  but the repository's own ledger, read alone, would deny it.
- **Recomputation:** none; comparison of header strings against `git cat-file -p <commit>` epoch values.
- **What would resolve it:** stamping each `progress.md` section from the same clock that writes the JSON artifacts (which is demonstrably correct), or from the commit itself.
- **Confidence:** HIGH — a header inside commit *X* cannot postdate *X*'s own commit time, and both quantities are read directly from the objects.
- **Invalidated by later commits?:** no — `progress.md` is append-only (verified: nine diffs, zero deletions), so these strings are fixed at the anchor.
- **Disclosed by authors?:** no.

### DRAFT-P-4

- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** Amendment 1's completeness claim about the diff between sealed-read attempt 1 and attempt 2
- **Direction:** neutral — the undisclosed change *weakened* the machinery evidence (the discarded run had a larger n and a larger t), so it cuts against a selection reading rather than for one
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "the only change between attempt 1 and attempt 2 is a **single string literal** in a request parameter — `"3600"` to `"60"` — plus the attempt-numbering that keeps the first latch." — VRPExperiment/REGISTRATION.md:578-582
- **Evidence:**
  - `git show ef07f19 --name-only` lists four files: `REGISTRATION.md`, `tools/task6_sealed_run.py`, `reports/task6/task6.latch.json`, and **`reports/task6/fixture_result.json`**. The first three are exactly what the amendment describes.
  - `git diff adac707 ef07f19 -- reports/task6/fixture_result.json` shows the committed fixture artifact was **replaced by a fresh run at a different size**: `"days_requested": 900 → 300`; per asset `"n": 870 → 270`; `started_at`/`finished_at` `2026-08-30T06:55:02Z → 06:57:32Z`; `"attempt": 1` added. The planted premium is unchanged at `0.08` in both.
  - The discarded run was the stronger one: BTC recovered mean 0.097798 with t = 9.5682, p = 5.45×10⁻²¹ at n = 870; the surviving run recovers 0.094653 with t = 4.2725, p = 1.34×10⁻⁵ at n = 270 (ETH: 0.094699 / t = 13.0943 → 0.094101 / t = 7.4162).
  - Amendment 1 does not mention it, and `README.md:124-125` and `docs/HANDOVER.md:116-119`, which point the reader at the fixture, quote no n and do not say the artifact was re-generated.
- **Recomputation:** none; the finding is the diff itself.
- **What would resolve it:** one sentence in Amendment 1 recording that the fixture was re-run at 300 days during the correction and that the 900-day run stands in `adac707`; or restoring both artifacts side by side.
- **Confidence:** HIGH that the change happened and is unrecorded; MEDIUM that the amendment's sentence should be read as covering artifacts rather than only the code diff — read as a statement about the *machinery* it is exactly true, and the estimator claim beside it ("No estimator, no window, no estimator parameter, no tenor, no sign convention and no inference rule was touched") is fully verified by identical `src/vrp` tree hashes.
- **Invalidated by later commits?:** no — `fixture_result.json` is unchanged from `ef07f19` to the anchor.
- **Disclosed by authors?:** no, not in words; but the diff is in git and the amendment explicitly invites the reader to it ("The diff is auditable in the commit that precedes attempt 2"), which is why this is S3 and not higher.

---

## 4. What could not be checked, and why

1. **Any network call that left no file.** The registration-precedence claim (P1/P2) is
   verified against every artifact that exists, but `data/` only ever received files from
   `curl`-style captures and the probe tools. The TASK 3 live spot measurement — Coinbase
   `$78,124.575` / Kraken `$78,115.50` for BTC, and the ETH pair
   (`reports/task3/venue_table.md:11-12`), which drive the `$390,622.88` and `$122,810.25`
   notionals and hence two CAPITAL_BLOCKED rows — wrote nothing to disk. There is therefore no
   evidence that can place it before or after `7827592`. This is the one gap in an otherwise
   complete precedence chain.
2. **The 400-day timestamp-misalignment probe.** `docs/ACCESS.md:282-289` reports
   "Measured on a 400-day window, timestamps only, no value read" with `n = 401 rows` per leg
   and bucket stamps 00:00 UTC (implied) vs 08:00 UTC (underlying). **No artifact stores it and
   no committed tool produces it.** The five tools in `tools/` write only
   `deribit_probe.json`, `rate_and_revision_baseline.json`, `reference_spreads_deribit.json`,
   `env_report.json` and the task6 results. The claim that the choice of 08:00 was made from
   timestamps alone — which is what makes it outcome-blind — cannot be verified from the
   repository. It is corroborated indirectly and quite strongly by `src/vrp/tzguard.py:10`
   ("Deribit settles at 08:00 UTC"), which is in `8bcc5bf`, **before the registration and
   before any network call**, and by the measured expiry `2026-09-25T08:00:00Z` in
   `reference_spreads_deribit.json`. The latch forbids re-fetching, so it cannot be reproduced.
3. **Three stored artifacts have no committed generator**, so the step from raw capture to
   stored figure cannot be re-derived: `reports/task4/revision_recheck.json` (which carries the
   contested `"gap"` string of DRAFT-P-1), `reports/task5/commission_bps.json` (which carries
   the deciding 122.140 / 162.853 bps figures), and `reports/task5/ibkr_ca_commissions.json`.
   Their inputs (`data/raw/task5/commissions-futures.html`, 489,783 B, matching the byte count
   at `docs/COSTS.md:33`) are on disk, so recomputation is possible in principle but is a
   verification task, not a provenance one.
4. **Everything under `data/` is UNANCHORED.** It is gitignored; the only evidence is inode
   mtimes and birth times, read from the live tree at **2026-09-05 03:56Z–04:06Z**. mtimes can
   be rewritten and carry no cryptographic tie to the commits. Every dating of "when data first
   existed" in this report rests on them, and would be far stronger if the raw captures were
   hashed into a committed manifest at the time of capture. (The repository does this for its
   *code* — the latch — but not for its data.)
5. **The hourly row counts** quoted at `HYPOTHESES.md:22` (47,696 DVOL, 47,858 perpetual)
   appear in no artifact; the driver writes them to stdout only. Not provenance-decidable.
6. **Whether the operator saw any premium value during the aborted attempt 1** (P19 item 3,
   "No premium value was observed, printed, or logged, by the tool or by the operator") is a
   claim about a human, not about an object. The checkable parts of it — no result file, no
   raw series file, `src/vrp` unchanged — all verify.

---

## 5. Live-repo access log

Every access to `/home/kiros-li/Documents/GitHub/VRPExperiment/` in this task was read-only:
`git status --porcelain`, `git log`, `git show`, `git diff`, `git cat-file -p`, `git ls-tree`,
`git rev-parse`, `git grep <commit>`, plus `ls -la`, `stat` and `find -printf` on the
gitignored `data/` tree, and one `python3 -c "json.load(...)"` on a 4,400-byte tracked JSON
read from the **snapshot**, not the live tree. **No file in the repository was opened for
writing. No repository script was executed.** No `.env`, keystore, session, credential or
token file was opened. No large binary was opened (`data/raw/task4/alt/tardis_api`,
210,602,148 B, was never listed or read in this pass). Scratch work went to
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-vrp-prov/` and to `/tmp/a[1-4].txt`
(two `git ls-tree` listings for a diff); nothing was written under the audited repository.

**BEFORE first access — 2026-09-05T03:56:59Z:**

```
```

(empty — `git status --porcelain` exited 0 with no output; working tree clean.
`git rev-parse HEAD` = `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`, matching the anchored SHA.)

**AFTER last access — see the timestamp printed with the command below:**

**`git -C /home/kiros-li/Documents/GitHub/VRPExperiment status --porcelain`, AFTER last access — 2026-09-05T04:10:21Z:**

```

```

(empty — exited 0 with no output; working tree clean)

`HEAD` at both checks: `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`. **No modification was made to the audited repository and none is reported.**
