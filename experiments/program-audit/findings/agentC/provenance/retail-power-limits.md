# retail-power-limits — provenance verification (Agent C)

Repository: `retail-power-limits`
Anchored SHA: `dda39b2f148569a6fe9be956a979471b2330611d` (main, 2026-08-29)
Document text read from `SNAP/retail-power-limits/`. Git objects read from the live repositories,
read-only (`log`/`show`/`diff`/`rev-parse`/`ls-tree`/`cat-file`/`grep <rev>`/`rev-list`/`reflog`/
`for-each-ref`). Verification window: 2026-09-04T00:10Z – 2026-09-04T00:20Z.

## What this repository is, and what "provenance verification" therefore means

`retail-power-limits` measures nothing. It is a note plus a typed registry that pins each quoted
figure to a sibling repository, file and commit. **Every provenance claim it makes is a claim
about a sibling repository's git history.** Verifying them from inside `retail-power-limits`
alone is impossible; verifying them from the siblings' git objects is straightforward, and that
is what was done. Eight sibling repositories were touched read-only: `InsiderExperiment`,
`NPDExperiment`, `ETFExperiment`, `HFExperiment`, `AiTrader`, `MLCryptoEngine`, `solattn`,
`solclear`. The full before/after `git status --porcelain` for all nine repositories is at the
end of this file.

**Headline result: 21 of 22 provenance claims verify as SUPPORTED. One (P-01) is PARTIAL, and
the part that fails is disclosed by the authors in three places in their own text. One claim
(P-14) was true at the anchored SHA and became false 11 hours 24 minutes later; it is recorded
as the single draft finding, at S4.**

The strongest claim in the note — P-02, that InsiderExperiment's power gate and its 20/40 bp bars
were committed in that repository's first commit, before any corpus or portfolio existed — is
**fully supported by git objects, including the boundary convention quoted verbatim.** Section 0
of `InsiderExperiment/REGISTRATION.md` is **byte-identical from the first commit to the closing
commit**, and the four bar constants in `config.py` were set in the first commit and never
touched. This is not a claim that merely survives checking; it is a claim that checks out
exactly, in the strongest form available from git.

---

## Registration claims table

All 22 claims from the inventory's *Provenance claims* section. "Data first existed" is the
earliest commit adding a data artifact, or the earliest filesystem evidence of one, in the
sibling the claim concerns.

| ID | Claim (short) | Commit named | Found? | Commit date | Data first existed | Status |
|---|---|---|---|---|---|---|
| P-01 | Four independent pre-registered experiments; each closed at unresolved/untestable-at-achievable-power or BLOCKED on a power gate | none | n/a | n/a | per-repo, below | **PARTIAL** — HFExperiment's Section 0 fired BLOCKED on the *broker*, not on a power gate, and it closed by operator decision. Disclosed by the authors at `docs/the-power-limit.md:141-146`, `DECISIONS.md:125-129`, `rplimits/cases.py:286-294` |
| P-02 | The gate was committed in InsiderExperiment's first commit `fbfc74e`, before the corpus and portfolio existed; bars fixed at 20 bp GO / 40 bp BLOCKED | InsiderExperiment `fbfc74e` | yes | 2026-08-25T18:34:56−07:00 | market store `var/insider_market.db` mtime 2026-08-25 18:36; corpus commit `ccc9b13` 18:47:16 | **SUPPORTED** (all four sub-conditions) |
| P-03 | NPD closing commit 13:26:58; Insider first commit 18:34:56, "five hours and eight minutes later"; Insider closure 23:24:15 | NPD `2d3d0ae`, Insider `fbfc74e`, `12d9fd3` | yes | 2026-08-25T13:26:58 / 18:34:56 / 23:24:15, all −07:00 | n/a | **SUPPORTED** — one timezone throughout; exact gap 5 h 07 m 58 s, i.e. 5 h 08 m to the nearest minute; `2d3d0ae` is genuinely NPD's HEAD and closing commit |
| P-04 | NPD's ADR-007 registered the failure mode as a risk before collection began, and chose not to promote the better-powered secondary | NPD `2d3d0ae` | yes | ADR-007 introduced at root `64b7d41`, 2026-08-25T09:39:00−07:00 | 2026-08-25T10:12:23−07:00 (`3c2a152` adds `reports/stage_b1/calibration.json`) | **SUPPORTED** — ADR-007 predates the first data artifact by 33 min |
| P-05 | NPD's 0.01–0.05 effect band was registered in Section 9.2 before any call went out | NPD `2d3d0ae` | yes | Section 9.2 and "0.01 to 0.05" both introduced at root `64b7d41`, 09:39:00 | 10:12:23 (as above) | **SUPPORTED** |
| P-06 | InsiderExperiment's 40 bp BLOCKED floor was committed before the measurement existed | `fbfc74e` (floor), `cb17046` (measurement) | yes | 18:34:56 vs 19:11:45, same day | corpus `ccc9b13` 18:47:16 | **SUPPORTED** — `git diff fbfc74e cb17046 -- REGISTRATION.md` is 434 insertions, **0 deletions**; Section 0 untouched |
| P-07 | The equal-weight secondary was registered non-verdict-bearing before any number was visible, and the disclosure obligation was recorded | none directly; implied `fbfc74e` | yes | Section 10 secondaries registered at `398755b`, 2026-08-25T18:38:50−07:00 | measurement `cb17046` 19:11:45 | **SUPPORTED** — registered 33 min before the measurement; obligation at `InsiderExperiment/REGISTRATION.md:865-870` |
| P-08 | Structural separation: one sealed store with a single permitted reader, one demeaned store whose mean is never written, power module barred by import guard | none | yes | code present at `12d9fd3` | n/a | **SUPPORTED** — all three mechanisms verified in source, see Evidence below |
| P-09 | solclear's underpowered rule was registered before the measurement and fired 2026-08-14, eleven days before NPDExperiment | solclear `c692032` | yes | rule registered `8a49833` 2026-08-13T17:31:20−07:00; Stage E result `f0244eb` 18:44:41 | n/a | **SUPPORTED** — rule precedes measurement by 1 h 13 m; the 2026-08-14 date is solclear's own (`FINDINGS.md:7,38,109`) and is the UTC date of `f0244eb` (2026-08-14T01:44:41Z); 2026-08-25 − 2026-08-14 = 11 days |
| P-10 | HFExperiment's Section 11, registered 2026-08-23, priced the forward verdict at eight to eleven years and the operator proceeded anyway | none at that line; cited to `f13e1d3` | yes | Section 11 with 2,061/2,852 introduced at `a8f4b0d`, **2026-08-23T21:40:25−07:00** | HF first live measurement `0a0d214` 2026-08-23T15:42:34 | **SUPPORTED** — the prose date 2026-08-23 is correct; the citation to `f13e1d3` (2026-08-25) points at the file that *carries* Section 11 at closure, not at its introduction |
| P-11 | The sibling repositories are closed; the short hashes are stable references | all 24 | yes | see table below | n/a | **SUPPORTED** — all 24 citations resolve unambiguously (`rev-parse --disambiguate` returns exactly 1 each), every claimed date equals the actual author date, and every named path exists at its commit. No sibling has a commit after 2026-08-28T23:28:41−07:00, i.e. none moved after the note was written |
| P-12 | The 845 / above-1,200 / about-302 triple is Amendment 6's, not the closure's; the closure fired on 163-vs-300 | ETF `4d11002` | yes | Amendment 6 introduced at `4d11002`, 2026-08-28T19:43:48−07:00; closure `3f5d629` 16:39:33 | ETF first live measurement `97da329` 13:04:41 | **SUPPORTED** — Amendment 6 states "roughly 291 … plus the 11 … about 302", "clears the governing 300 by two days", "E1 needs 845 and E2 needs above 1,200"; the closure's deciding numbers are "Projected N 163 … against a governing minimum of 300" |
| P-13 | HFExperiment did not fire a power gate; Section 0 fired BLOCKED on IBKR fractional refusal (errors 10243/10244); closed by operator decision 2026-08-26, shadow series never started; resolution inherited | `82e77a0`, `0a0d214` | yes | closure entry written at `f13e1d3` 2026-08-25T00:45:29−07:00 | n/a | **SUPPORTED** — `HFExperiment/progress.md:5-9` "Closed. Experiment closed by operator decision, instruction dated 2026-08-26"; `progress.md:14` "The shadow series never produced an observation"; errors at `progress.md:32-33`; README first sentence at `0a0d214` reads exactly as the note says |
| P-14 | Four of the seven source repositories are not published and have no remote | none | n/a | n/a | n/a | **SUPPORTED at the anchored SHA, NOT_SUPPORTED as of 2026-09-04T00:10Z** — see DRAFT-P-1 |
| P-15 | This repository wrote to nothing; it imports nothing from the siblings at runtime | none | n/a | n/a | n/a | **SUPPORTED** — no sibling has any commit dated 2026-08-29; `rplimits/` imports only `dataclasses`, `pathlib`, `re` and its own modules — no `subprocess`, `requests`, `urllib`, no path outside `ROOT` (`rplimits/docsync.py:27`) |
| P-16 | Exactly one figure (411 minutes) is derived; every other number is quoted | NPD `2d3d0ae` for the addends | n/a | n/a | n/a | **SUPPORTED** — every ratio-shaped candidate the inventory flagged is stated verbatim by its sibling, not formed here: 1,700× and 100× at `MLCryptoEngine/docs/notes/h1-…md:82-84` @ `ae03bf6`; 100–180× at `MLCryptoEngine/HYPOTHESES.md:102` @ `d2a0f05`; 37.6× at `solclear/FINDINGS.md:287,299` @ `c692032`; 1.5x at `AiTrader/RETURN.md:2899` @ `f819b68`; 137 and 74 at `ETFExperiment` closure `3f5d629`; "Eight to eleven years" at `HFExperiment` Section 11 @ `a8f4b0d` |
| P-17 | NPD's registration voided the post-hoc two-horizon amendment; InsiderExperiment's alpha is still sealed | NPD `2d3d0ae`, Insider `12d9fd3` | yes | Amendment 7 VOID at `NPDExperiment/REGISTRATION.md:661-674` | n/a | **SUPPORTED (NPD half, verbatim); PARTIAL (Insider half)** — the void language is exact; the "never read" half rests on InsiderExperiment's own text plus structural code evidence, and no read-record artifact was opened. See "What could not be checked" |
| P-18 | Every figure is typed `Figure(value, source)`; the constructor refuses an unresolvable source; generated blocks are drift-tested | rpl `dda39b2` | yes | anchor | n/a | **SUPPORTED, including the limit** — `rplimits/cases.py:29-33` raises `KeyError`/`ValueError`; `tests/test_render.py:31-37` re-renders and compares; **`README.md` contains zero `GENERATED` markers**, so the four blocks live only in `SOURCES.md` (3) and `docs/the-power-limit.md` (1) |
| P-19 | The boundary convention was written down with the bar ("An MDE of exactly 20.00 bp is GO") | Insider `fbfc74e` | yes | 2026-08-25T18:34:56−07:00 | as P-02 | **SUPPORTED** — verbatim at `fbfc74e:REGISTRATION.md:45` |
| P-20 | AiTrader's 2.55-year holdout was touched once at `a0a9ef6` | AiTrader `a0a9ef6` | yes | 2026-07-26T19:26:53−07:00 | n/a | **SUPPORTED** — commit subject verbatim; pre-registration committed 12 min earlier at `00c2d17`; `AiTrader/RETURN.md:2723` @ `f819b68`: "The cross-sectional round's holdout was touched once and its results stand exactly as recorded at commit `a0a9ef6`" |
| P-21 | ETFExperiment's 2027-03-31 deadline was registered, not chosen at closure | ETF `4d11002`, `3f5d629` | yes | present in the governing prompt at root `4b9c874` 2026-08-28T00:57:16−07:00, in `src/etf/config.py:164` at `815f888` 01:05:56, and in Section 0 at `44567f6` 01:07:59 | ETF first live measurement `97da329` 13:04:41 | **SUPPORTED** — registered ~12 hours before the first network call and never amended |
| P-22 | This repository's own ADR dates (Accepted, 2026-08-29) | none | n/a | all three rpl commits 2026-08-29T00:19:47 / 00:20:34 / 00:21:28 −07:00 | nothing measured here | **SUPPORTED** — `progress.md:15` records scaffold 00:07:32 and gates green 00:18, consistent with the commit times |

### The 24 source citations (P-11, mechanical result)

Every row resolved; `--disambiguate` returned exactly one object for each short hash; every
claimed date equals the actual author date; every named path exists at its commit.

| repo | commit | claimed date | actual author date | path check |
|---|---|---|---|---|
| NPDExperiment | `2d3d0ae` | 2026-08-25 | 2026-08-25T13:26:58−07:00 | REGISTRATION.md OK, progress.md OK, DECISIONS.md OK, (closing commit) n/a |
| InsiderExperiment | `12d9fd3` | 2026-08-25 | 2026-08-25T23:24:15−07:00 | REGISTRATION.md OK, DECISIONS.md OK, (closing commit) n/a |
| InsiderExperiment | `fbfc74e` | 2026-08-25 | 2026-08-25T18:34:56−07:00 | (commit) — subject verbatim |
| InsiderExperiment | `cb17046` | 2026-08-25 | 2026-08-25T19:11:45−07:00 | (commit) — subject verbatim |
| ETFExperiment | `4d11002` | 2026-08-28 | 2026-08-28T19:43:48−07:00 | REGISTRATION.md OK; subject verbatim |
| ETFExperiment | `fe60a22` | 2026-08-28 | 2026-08-28T13:39:00−07:00 | README.md OK |
| ETFExperiment | `3f5d629` | 2026-08-28 | 2026-08-28T16:39:33−07:00 | (closing commit) — subject verbatim |
| HFExperiment | `f13e1d3` | 2026-08-25 | 2026-08-25T00:45:29−07:00 | REGISTRATION.md OK; subject verbatim |
| HFExperiment | `0a0d214` | 2026-08-23 | 2026-08-23T15:42:34−07:00 | README.md OK |
| HFExperiment | `82e77a0` | 2026-08-28 | 2026-08-28T14:14:08−07:00 | progress.md OK |
| AiTrader | `f819b68` | 2026-07-29 | 2026-07-29T20:18:07−07:00 | RETURN.md OK |
| AiTrader | `a0a9ef6` | 2026-07-26 | 2026-07-26T19:26:53−07:00 | (round commit) — subject verbatim |
| MLCryptoEngine | `d2a0f05` | 2026-08-12 | 2026-08-12T21:49:53−07:00 | HYPOTHESES.md OK |
| MLCryptoEngine | `ae03bf6` | 2026-08-22 | 2026-08-22T17:38:15−07:00 | docs/notes/h1-…md OK |
| solattn | `b3f5062` | 2026-08-28 | 2026-08-28T23:28:41−07:00 | REGISTRATION.md OK, FINDINGS.md OK |
| solclear | `c692032` | 2026-08-22 | 2026-08-22T19:26:42−07:00 | FINDINGS.md OK |

One labelling nuance, recorded and **not** raised as a finding: `sources.py:125` gives
`etf-disarm` (`4d11002`) the path `"(closing commit)"`, though its subject is a post-closure
correction. The note's own `progress.md:40` says it read ETFExperiment's "**both closing
commits**", and ETF's Amendment 6 is titled "…`etf-snap` is disarmed and **the repository
stops**", so the author's usage is internally consistent and disclosed.

---

## Parameter changes after data existed

Every change to a registered figure, threshold, horizon, universe, alpha, n-target or cost figure
made after the first data artifact existed, in each of the four power cases. The task treats a
change without a dated amendment as a finding. **There are none.**

### InsiderExperiment — data first existed 2026-08-25 ~18:36 (market store) / 18:47:16 (`ccc9b13`)

| What could have changed | Verdict |
|---|---|
| Section 0 (the gates, the bars, the boundary convention, the floor derivation), lines 1–159 | **NEVER CHANGED.** `git show fbfc74e:REGISTRATION.md \| head -159` and `git show 12d9fd3:REGISTRATION.md \| head -159` are **byte-identical** (`diff` empty). From the first commit to the closing commit, across the corpus build, the power measurement and the closure. |
| `mde_go_ceiling_bp` = 20.0, `mde_degraded_ceiling_bp` = 40.0, `corpus_event_floor` = 1_000, `corpus_coverage_floor` = 0.80 | **NEVER CHANGED.** Introduced in `fbfc74e:src/insider/config.py`; the only later commit touching `config.py` (`672b343`) does not alter any of the four. |
| Any deletion anywhere in `REGISTRATION.md` history | Exactly two lines, both in `d8b81f1` (post-measurement, 19:11:55) and both placeholders, not parameters: `-Filled by Task 4 and Task 5. Empty at the time Section 0 was committed.` → `+…committed at 18:34 on 2026-08-25.`, and `-None in force.` → `+None in force. Section 0 fired BLOCKED, so no amendment can authorize Stage B.` |

**No amendment was needed, because nothing moved.**

### NPDExperiment — data first existed 2026-08-25T10:12:23−07:00 (`3c2a152` adds `reports/stage_b1/calibration.json`, `calibration_minimal.json`, `reports/mutations.json`)

| # | Change | Commit / date | Dated amendment? | Records the data that existed? |
|---|---|---|---|---|
| 1 | Amendment 1 — `temperature` omitted, endpoint refused it | `3c2a152` 10:12:23 | yes | yes — "**Raised 2026-08-25 by the Section 12.2 calibration call, before B.1 started.**" + the verbatim API refusal |
| 2 | Amendment 2 — `reasoning_effort` fixed at `minimal` by the registered decision rule; and the row "reasoning effort — **minimal** … See Amendment 2" added to the Section 2 parameter table | `3c2a152` 10:12:23 | yes | yes — same header, plus the measured cost table (`low` 0.027271 USD/call → 11.7812 USD projected; `minimal` 0.003251 → 1.4045) and an explicit "**The road not taken, and why**" paragraph refusing the `low`-over-365-days option because it would mean changing the design after seeing cost data |
| 3 | Amendment 3 — `reasoning_effort_ladder` registered as `("minimal","low")` | `c4da18c` 10:17:32 | yes | yes — "**Raised 2026-08-25, 14 gate calls into B.1. The run was stopped to record this before it went further.**" + the 9-of-14 failure table |
| 4 | Amendment 4 — strict JSON output schema; ladder re-tuned to `("minimal","minimal","minimal","minimal","low")`; prompt digest re-frozen to `7e6f3d68…` | `250bc8f` 10:35:37 | yes | yes — "**Raised 2026-08-25, 29 gate days into B.1. The run was stopped again.**" + the `minimal` 41% / `low` 47% failure table that falsifies Amendment 3's own diagnosis, superseded rather than "quietly dropped" |
| 5 | Amendment 5 — rejected answers billed and ledgered | `250bc8f` 10:35:37 | yes | yes — "**Raised 2026-08-25, during the same stop.**" + "recorded 0.3494 USD against an actual 0.6429 USD, a 46 percent undercount" |
| 6 | Section 13 Amendment 0 — the reserved operator-prior slot filled with `0.05, ADOPTED FROM THE ASSISTANT. NOT INDEPENDENT.` | `2c6d683` 13:13:28 | yes | yes — "Recorded 2026-08-25, **before any module touched the sealed store**", and "**Calibration status: one prior, not two.**" This fills a slot the registration reserved; it moves no bar |
| 7 | Amendment 6 — POST-READ terminal state, "recorded as intent and not as registration" | `2d3d0ae` 13:26:58 | yes | yes (self-labelled POST-READ) |
| 8 | Amendment 7 — **VOID.** Would have added 10- and 20-session descriptive horizons | `2d3d0ae` 13:26:58 | yes | yes — "**Drafted in the same batch as Amendment 6. Arrived after the read. Void.**" |
| — | **Registered power floor (detectable IC 0.025 at 30 names), effect band 0.01–0.05, five-session primary horizon** | — | — | **NEVER CHANGED.** Present at root `64b7d41` and identical at anchor `2d3d0ae` (`REGISTRATION.md:207-213` → `:208-214`) |

### ETFExperiment — data first existed 2026-08-28T13:04:41−07:00 (`97da329`, "A.1 Task 1 access verification, **measured live**")

Every amendment opens with a bolded section literally headed **"What data existed when this
amendment was made."** (`REGISTRATION.md:598, 700, 821, 949, 995, 1098`).

| # | Change | Commit / date | Dated amendment? | Verdict-relevant? |
|---|---|---|---|---|
| 1 | Amendment 1 — flow source selected, paces measured, two structural constraints | `294eab7` 13:16:31 | yes | yes |
| 2 | Amendment 2 — Amendment 1's archive-density figure **falsified by measurement**; retro revision rate recorded | `41351a9` 13:36:13 | yes | yes — a figure corrected against data, with the correction stated rather than the original edited |
| 3 | Amendment 3 — Section 0 verdict record: GO eliminated on measured inputs | `67f25f3` 13:40:58 | yes | yes |
| 4 | **Amendment 4 — the governing minimum N changed from E1's 237 to E2's 300** | `cf6efaf` 13:45:53 | yes | **yes — this is the verdict-relevant figure change, and it moves the bar *against* the experiment** (300 > 237 makes the deadline finding harder to avoid, not easier). Amendment 3 is named in the closure as having "understated it" |
| 5 | Amendment 5 — H1 closes at untestable-at-achievable-power on the deadline finding | `3f5d629` 16:39:33 | yes | yes |
| 6 | Amendment 6 — corrects Amendment 5 §5's reopen-path mislabel; `etf-snap` disarmed | `4d11002` 19:43:48 | yes | yes — and states "**It moves no bar and reopens nothing**", and that the earlier error "**flattered the decision it was defending**" |
| — | **The 2027-03-31 registered deadline** | — | — | **NEVER CHANGED.** Present from the governing prompt at root `4b9c874` (00:57:16), in `config.py` at `815f888` (01:05:56) and in Section 0 at `44567f6` (01:07:59) — all ≈12 hours before the first live measurement |

### HFExperiment — data first existed 2026-08-23T15:42:34−07:00 (`0a0d214`, "verified broker access, formation reproduced")

`REGISTRATION.md` is append-only in fact, not only in policy. The four commits touching it after
the first measurement are `a8f4b0d` (+235/−0), `8c4c3bc` (+12/−1), `669eb5c` (+9/−0), `f13e1d3`
(+11/−0). **The single deletion in the whole history is the placeholder line `-Append-only. No
entries yet.`, replaced by the first amendment-log entry.** No parameter changed. Section 11 and
its 2,061 / 2,852 / "Eight to eleven years" schedule were introduced at `a8f4b0d`
(2026-08-23T21:40:25) and never edited. The policy is stated at `HFExperiment/REGISTRATION.md:271`:
"Amendments are dated, numbered, appended, and each records what data…".

### retail-power-limits itself

Three commits, all 2026-08-29, all before any figure could go stale: `0974f96` (the note),
`710093d` ("the scope section counts four limits, not three" — a self-correction to its own
prose), `dda39b2` (a credential-scan test fix). Nothing is measured here, so there is no
"after data existed" for its own parameters.

---

## Draft findings

### DRAFT-P-1
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** P-14 — the disclosure that four of the seven source repositories are unpublished and therefore not independently checkable.
- **Direction:** neutral (pure hygiene). The error runs *against* the note's own interest: it tells readers to discount evidence that is in fact now checkable.
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED (git reflogs and `.git/config` mtimes)
- **Claim challenged (verbatim quote):** "**Four of the seven source repositories are not published.** The four power cases — NPDExperiment, InsiderExperiment, ETFExperiment and HFExperiment — exist only on the operator's machine and have no remote." — retail-power-limits/docs/the-power-limit.md:44-46. Restated as a table at retail-power-limits/SOURCES.md:268-271 ("**no — local only, no remote** | requires the operator's working copy", four rows) and at retail-power-limits/progress.md:113-116.
- **Evidence:**
  - All four repositories now have a GitHub remote. `git -C <repo> remote -v`, read 2026-09-04T00:10:56Z (UNANCHORED, live working tree): `NPDExperiment → https://github.com/kirosli00tuff/NPDExperiment.git`; `InsiderExperiment → …/InsiderExperiment.git`; `ETFExperiment → …/ETFExperiment.git`; `HFExperiment → …/HFExperiment.git`.
  - The remotes were added **after** the note. `git reflog show <remote branch>` gives a single entry each, all "update by push": ETFExperiment `origin/master@{2026-08-29T11:45:06−07:00}`, HFExperiment `origin/main@{2026-08-29T11:45:10−07:00}`, InsiderExperiment `origin/master@{2026-08-29T11:45:14−07:00}`, NPDExperiment `origin/main@{2026-08-29T11:45:18−07:00}`. The four `.git/config` mtimes match those times to the second.
  - retail-power-limits' last commit is `dda39b2`, 2026-08-29T00:21:28−07:00 (`git log`). The gap is **11 h 23 m 38 s**.
  - So the claim was **true when written and committed**, and became false the same day.
- **Recomputation (if any):** none required; the comparison is of two timestamps — `dda39b2` author date 2026-08-29T00:21:28−07:00 against the earliest push reflog entry 2026-08-29T11:45:06−07:00.
- **What would resolve it:** editing `SOURCES.md:262-271`, `docs/the-power-limit.md:44-52` and `progress.md:113-123` to record that the four were published on 2026-08-29, and that every citation in the registry now resolves against a public remote — which is exactly the outcome `SOURCES.md:279-282` anticipated. No figure changes; only the checkability disclosure does.
- **Confidence:** HIGH — the reflog entries and config mtimes are unambiguous and mutually corroborating, and the direction of the gap is not close.
- **Invalidated by later commits?:** No. retail-power-limits has had no commit since `dda39b2`, so the stale text still stands. The finding would be *resolved*, not invalidated, by a later commit updating the disclosure.
- **Disclosed by authors?:** Partly, and honestly. The note anticipated exactly this change and built for it: "every citation carries the commit hash that will resolve against them **if they ever are**" (`docs/the-power-limit.md:49-51`) and "**if any of the four is published later, every citation in this file resolves against it without amendment**" (`SOURCES.md:279-281`). `progress.md:113` also records that the fact was "**Checked at push time rather than assumed**". What is not disclosed is that the publication then happened. This is why the finding is S4 and not higher.

**No other finding.** Nothing else in the 22 claims contradicted the git record, and no parameter
change anywhere lacked a dated amendment.

---

## What could not be checked, and why

1. **Whether InsiderExperiment's sealed store was ever actually opened (P-17, second half).** What
   *is* verified is structural and strong: `read_sealed_returns` is defined exactly once, in
   `src/insider/eval/evaluator.py:33`; no module in `src/` calls it; the only call site anywhere is
   `tests/test_guards.py:461`, inside `test_the_evaluator_refuses_before_it_opens_the_seal`, which
   asserts the call *raises* `OperatorPriorMissing`; and `tests/test_guards.py:160-167` fails the
   build if a second definition or any non-evaluator caller appears. `var/insider_sealed.db` exists
   (884,736 B, mtime 2026-08-25 19:05, read 2026-09-04T00:17:57Z, UNANCHORED). But no read-audit
   record was opened, so "never read" rests on the repository's own statement
   (`InsiderExperiment/REGISTRATION.md:772`) plus this structural evidence. An interactive read
   outside the code path would leave no trace I inspected. **Status: PARTIAL, not contradicted.**
2. **The exact wall-clock time of NPDExperiment's first billed API call.**
   `reports/stage_b1/calibration.json` carries no timestamp field. The bound used is therefore the
   commit that introduced the artifact (`3c2a152`, 10:12:23), with the collector built at `943ba05`
   (10:06:55). Either bound leaves ADR-007 and Section 9.2 (root `64b7d41`, 09:39:00) comfortably
   earlier, so tightening it would not change P-04 or P-05.
3. **Whether untracked data existed in InsiderExperiment's working tree at 18:34:56 (P-02, sub-condition d).**
   Git cannot answer this. The supporting evidence is filesystem mtimes read at
   2026-09-04T00:17:57Z (UNANCHORED): `var/insider_market.db` 2026-08-25 18:36,
   `insider_corpus.db` / `insider_dispersion.db` / `insider_sealed.db` all 19:05 — every one
   *after* the gate commit. Combined with the `fbfc74e` tree containing no data file at all and
   `src/insider/portfolio/` holding only an empty `__init__.py`, the claim is supported on every
   piece of evidence available, but the negative ("nothing untracked existed") is not provable
   from git alone.
4. **Whether solclear's "2026-08-14" is the intended calendar convention.** solclear's own
   `FINDINGS.md` dates Stage E as 2026-08-14 in three places, and `f0244eb` is
   2026-08-13T18:44:41−07:00 = 2026-08-14T01:44:41Z. The note transcribes solclear's own date
   faithfully, so the transcription is correct whichever convention solclear meant. If solclear
   intended local time the "eleven days" would be twelve; that is solclear's question, not this
   repository's, and it does not bear on any verdict here.

## What I checked and found sound

Recorded because a sound result is a result. Beyond the 22 claims: the four registered bar
constants in InsiderExperiment never moved; Section 0 is byte-identical across the repository's
entire life; NPDExperiment's power floor, effect band and primary horizon never moved; ETF's
deadline never moved and its one bar change moved *against* the experiment and carried an
amendment; HFExperiment's registration is append-only with a single placeholder deletion in its
whole history; all 24 short hashes resolve unambiguously with correct dates and existing paths;
every commit subject quoted in `sources.py` matches its commit verbatim; and every ratio the
inventory flagged as possibly self-computed is in fact stated by the sibling. If the thesis were
that this note's provenance claims were loose, I would have expected to find a bar edited without
an amendment, a hash that did not resolve, a "registered before" that postdated its data, or a
ratio the note formed and attributed. I found none of those.

---

## Live-repo access log

Access was read-only throughout: `git status --porcelain`, `log`, `show`, `diff`, `rev-parse`,
`rev-list`, `ls-tree`, `cat-file -e`, `grep <rev>`, `reflog show`, `for-each-ref`, plus `ls`/`stat`
on `var/` and `.git/config` for the unanchored evidence noted above. No repository was written to.

**Before first access — 2026-09-04T00:10:56Z**

```
=== retail-power-limits ===
=== InsiderExperiment ===
=== NPDExperiment ===
=== ETFExperiment ===
=== HFExperiment ===
?? Accept:
?? GET
?? Host:
?? User-Agent:
=== AiTrader ===
 M COLLECTION_LOG.md
=== solclear ===
=== solattn ===
=== MLCryptoEngine ===
```

**After last access — 2026-09-04T00:20:01Z**

```
=== retail-power-limits ===
=== InsiderExperiment ===
=== NPDExperiment ===
=== ETFExperiment ===
=== HFExperiment ===
?? Accept:
?? GET
?? Host:
?? User-Agent:
=== AiTrader ===
 M COLLECTION_LOG.md
=== solclear ===
=== solattn ===
=== MLCryptoEngine ===
```

**Identical before and after.** The only entries are the two pre-existing dirt cases the rules
file documents as not mine: HFExperiment's four stray files (`Accept:`, `GET`, `Host:`,
`User-Agent:`) and AiTrader's ` M COLLECTION_LOG.md` (a collector appends to it). Nothing else
appeared, and nothing was modified by this verification.
