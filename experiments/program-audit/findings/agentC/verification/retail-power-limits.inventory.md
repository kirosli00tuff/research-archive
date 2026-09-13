# retail-power-limits — verification inventory (Agent C, LOCATE)

Repository: `retail-power-limits`
Anchored SHA: `dda39b2f148569a6fe9be956a979471b2330611d` (main, 2026-08-29)
Snapshot read: `SNAP/retail-power-limits/` (tracked files at the anchor)
Live repo touched: `/home/kiros-li/Documents/GitHub/retail-power-limits/` — git metadata and
working-tree listing only. Access log at the end of this file.

## Orientation: what kind of repository this is

This repository **measures nothing**. It states so itself (`retail-power-limits/README.md:53`,
`retail-power-limits/SOURCES.md:11`, `retail-power-limits/pyproject.toml:4`). It is a note plus a
small typed data layer that pins each quoted figure to a sibling repository, file and commit.

Consequences for verification, stated plainly up front:

1. **There is no analysis code here to re-run.** `rplimits/` contains four modules totalling ~530
   lines: a frozen dataclass registry of quoted strings (`cases.py`), a citation registry
   (`sources.py`), markdown builders (`render.py`), and a marker-block writer (`docsync.py`).
   None of them computes a statistic; none reads data; none has a network path.
2. **There are no data artifacts.** No `data/`, `reports/`, `audit/`, `var/`, no JSON, CSV,
   parquet, sqlite, ledger or manifest — tracked or untracked. The only untracked material in the
   live working tree is `.venv/`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/` and
   `__pycache__/`, all gitignored build residue.
3. **The documents the brief asks for do not exist here.** There is no `REGISTRATION.md`, no
   `registrations/`, no `HYPOTHESES.md`, no `report.md`, no `FINDINGS.md`, no `reports/*.md`.
   The numeric claims live in `README.md`, `docs/the-power-limit.md`, `SOURCES.md`, `DECISIONS.md`
   and `progress.md`; every one of them is also carried as a string literal in `rplimits/cases.py`,
   which is the single definition the generated document blocks are rendered from.
4. **Every numeric claim is therefore a transcription claim.** Verifying it means going to the
   sibling repository named in `rplimits/sources.py` at the commit named there. Verification
   *inside* this repository is limited to three things: internal consistency between the prose and
   the generated blocks, arithmetic among figures the note itself states, and the one figure the
   note flags as its own arithmetic (411 minutes).

### Where each citation can be checked

24 source keys in `rplimits/sources.py`. Eleven cite a commit whose short hash equals the audit's
anchored SHA for that sibling, so they can be checked from `SNAP/<repo>/` with no live access.
Thirteen cite an earlier commit and need live `git show`/`git log` in the sibling repository.

| citation commit == anchored SHA | keys |
|---|---|
| yes (checkable from SNAP) | `npd-registration`, `npd-progress`, `npd-decisions`, `npd-close` (`2d3d0ae`); `insider-registration`, `insider-decisions`, `insider-close` (`12d9fd3`); `etf-registration`, `etf-disarm` (`4d11002`); `hf-progress` (`82e77a0`); `solattn-registration`, `solattn-findings` (`b3f5062`) |
| no (needs live sibling git history) | `insider-section0` `fbfc74e`; `insider-gate` `cb17046`; `etf-readme` `fe60a22`; `etf-close` `3f5d629`; `hf-registration` `f13e1d3`; `hf-readme` `0a0d214`; `hf-close` `f13e1d3`; `aitrader-return` `f819b68`; `aitrader-round` `a0a9ef6`; `mlc-hypotheses` `d2a0f05`; `mlc-h1note` `ae03bf6`; `solclear-findings` `c692032` |

(The "yes" row lists 12 keys covering 11 distinct commits, since `solattn-registration` and
`solattn-findings` share `b3f5062`.)

---

## 1. Artifacts

Every tracked file, plus everything in the live working tree. Nothing here holds measured data;
the "what it holds" column says what a verifier can get from it.

| path | tracked | what it holds | which document figures it backs |
|---|---|---|---|
| `retail-power-limits/rplimits/cases.py` (19,210 B, 430 lines) | tracked (anchored) | **The single definition of every quoted figure.** 4 `PowerCase` records × 7 `Figure` fields + a `caveat`, 3 `ContrastCase` records × 2 `Figure` fields + `why_not_power`, 4 `Headline` records. All values are string literals; nothing is computed. | Every generated block in `SOURCES.md` and the headline table in the note; by transitive drift-testing, the figures repeated in `README.md` and `docs/the-power-limit.md` prose |
| `retail-power-limits/rplimits/sources.py` (7,359 B, 207 lines) | tracked (anchored) | The citation registry: 24 `Source(repo, path, commit, date, detail)` entries. This is the map from every figure to the sibling repo/file/commit that could confirm it. | The `source-registry` block, `SOURCES.md:210-236`; the inline `*Source: …*` lines under every figure |
| `retail-power-limits/rplimits/render.py` (3,442 B) | tracked (anchored) | Four markdown builders (`headline-table`, `power-records`, `contrast-records`, `source-registry`). Pure string assembly. | The four generated blocks |
| `retail-power-limits/rplimits/docsync.py` (2,822 B) | tracked (anchored) | Marker-block reader/writer; `DOCUMENTS = (SOURCES.md, docs/the-power-limit.md)` | Mechanism only, no figures |
| `retail-power-limits/rplimits/__main__.py`, `__init__.py` | tracked (anchored) | CLI entry (`--write`) and version | none |
| `retail-power-limits/SOURCES.md` (23,127 B, 300 lines) | tracked (anchored) | The full extraction. Lines 27-155 `power-records`, 165-201 `contrast-records`, 209-236 `source-registry` are **generated** from `cases.py`/`sources.py`. Lines 240-300 are hand-written: the two `git` commands, the published/unpublished table, and the derived-figure disclosure. | The primary carrier of nearly all numeric claims |
| `retail-power-limits/docs/the-power-limit.md` (24,378 B, 407 lines) | tracked (anchored) | The note. Lines 69-76 are the generated `headline-table`; everything else is hand-written prose that restates figures also held in `cases.py`. | The four case summaries, the progression, the cost-asymmetry table (236-243), the contrast cases, the practice |
| `retail-power-limits/README.md` (4,762 B, 86 lines) | tracked (anchored) | The claim, the scope limit, the four-case table (18-23), the list of honesty-pinned figures (78-80). **The four-case table is hand-written, not generated** — it is not covered by the drift test. | The headline four-case figures |
| `retail-power-limits/DECISIONS.md` (9,190 B, 193 lines) | tracked (anchored) | Six ADRs. ADR-003 (87-118) states the four corrections; ADR-004 (121-148) states the HFExperiment inheritance; ADR-006 (177-193) discloses the one derived figure and its six addends. | The correction claims, the HF-inheritance claim, the 411-minute derivation |
| `retail-power-limits/progress.md` (7,472 B, 141 lines) | tracked (anchored) | Stage record for this repository only: ETA vs actual, what was read from each sibling (36-45), three build defects, the "no remote" finding (111-127), and the self-reported gate result (65-68: "111 tests", "11 source files") | Self-report figures about this repository |
| `retail-power-limits/tests/test_honesty.py` (8,270 B, 218 lines) | tracked (anchored) | The figure pins (`FIGURES_PINNED`, 90-119) and scope pins (`SCOPE_PINNED`, 59-70), plus the credential scan and its canaries. **This file is the machine-readable statement of which nine figures the authors consider load-bearing.** | Pins `0.0512`, `0.01 to 0.05`, `49.35 bp per month`, `845`, `above 1,200`, `302`, `z 1.668`, `2.50`, `6.9378 USD` in both README and note; additionally in the note `−1.0779`, `300 to 550 bps`, `0 USD` and three closure phrases |
| `retail-power-limits/tests/test_render.py` (2,131 B) | tracked (anchored) | The drift check: re-renders each of the 4 blocks and compares to disk | Guarantees `SOURCES.md` blocks and the note's headline table equal `cases.py` |
| `retail-power-limits/tests/test_cases.py` (2,335 B), `tests/test_sources.py` (1,740 B) | tracked (anchored) | Structural checks: every figure resolves to a source; exactly four power cases in a fixed order; every commit is a 7-hex short hash; all seven repos represented | Integrity of the citation layer, not of any figure's value |
| `retail-power-limits/Makefile`, `pyproject.toml`, `uv.lock`, `LICENSE`, `.gitignore`, `tests/__init__.py` | tracked (anchored) | Build config. `uv.lock` (75,212 B) is the only large tracked file. | none |
| `.venv/` (91 MB), `.mypy_cache/` (6.1 MB), `.pytest_cache/` (40 KB), `.ruff_cache/` (32 KB), `rplimits/__pycache__/`, `tests/__pycache__/` | **untracked, gitignored** | Build residue only. Listed by `git status --ignored`; contains no repository-authored data. mtimes 2026-08-29 00:13-00:18 local. | none — **there is no unanchored data in this repository** |

**Untracked-data verdict: none.** Every figure this repository asserts is anchored in git. The
unanchored risk sits entirely in the sibling repositories, which this repository does not contain
and does not read at runtime (`retail-power-limits/progress.md:31-34`: "this repository imports
nothing from them at runtime — the figures are transcribed, not loaded").

---

## 2. Numeric claims, ranked

Ranked by how much rests on the number. Ranks 1-8 are marked **MUST-VERIFY**; the brief demands at
least three. Each claim is quoted verbatim with `file:line` at the anchored SHA. "Produced by"
names the artifact or sibling record a verifier must reach.

### MUST-VERIFY

**C-01 — MUST-VERIFY. NPDExperiment's deciding number.**
> "realized MDE **0.0512** — above the whole band"
`retail-power-limits/docs/the-power-limit.md:72` (generated); also
`retail-power-limits/README.md:20`, `retail-power-limits/SOURCES.md:38`,
`retail-power-limits/rplimits/cases.py:95,405`.
Figures: MDE 0.0512; band 0.01 to 0.05; pre-registered projection 0.026 to 0.047; realized daily
contrast sd 0.36339 against a registered assumption of "at most 0.2626". n: 415 stored rankings,
404 evaluable days, 125.6 independent-equivalent days.
Produced by: NPDExperiment `progress.md` and `REGISTRATION.md` Section 9 @ `2d3d0ae` — which is the
anchored SHA, so checkable from `SNAP/NPDExperiment/`.
Why it ranks first: it is the deciding number of the first of the four cases, it is the number the
whole "progression" argument turns on, it is quoted a second time inside InsiderExperiment
(`retail-power-limits/docs/the-power-limit.md:186`), and `tests/test_honesty.py:146-147` names the
single edit that would invert the note's meaning ("minimum detectable contrast was 0.0012").
In-repo arithmetic note for the verifier: with the stated sd 0.36339 and N_eff 125.6, the stated
MDE 0.0512 implies a `t * M` multiplier of 1.579 (1.645 would give 0.0533; 1.96 would give
0.0636). The note's own identity `MDE = t * scale * sd / sqrt(N_eff)`
(`retail-power-limits/docs/the-power-limit.md:324`) leaves `scale` unstated here, so the figure is
**not** closable from this repository alone.

**C-02 — MUST-VERIFY. InsiderExperiment's deciding number and its gate.**
> "The minimum detectable effect is 49.35 bp per month against a registered BLOCKED floor of 40"
`retail-power-limits/SOURCES.md:86` (generated); also
`retail-power-limits/docs/the-power-limit.md:73,92,208`, `retail-power-limits/README.md:21`,
`retail-power-limits/rplimits/cases.py:146,172,412`.
Figures: MDE 49.35 bp/month; BLOCKED floor 40; GO bar 20; gross band 30-40; net band 13.3-34.7.
n: 4,585 qualifying events, 2,581 sessions, 2,869.9 effective independent periods.
Produced by: InsiderExperiment `REGISTRATION.md` Sections 0 and 15.5-15.7 @ `12d9fd3` (anchored,
checkable from SNAP) and the gate commit `cb17046` (**not** the anchor — needs live sibling git).
Why: it is the only case in the four where a power gate actually fired as a registered verdict, and
the entire "progression from expensive discovery to cheap refusal" claim
(`retail-power-limits/README.md:36-39`) rests on it.

**C-03 — MUST-VERIFY. ETFExperiment's closure comparison.**
> "The closure itself fired on 163 projected against 300 governing at the 2027-03-31 deadline."
`retail-power-limits/SOURCES.md:122` (generated); also
`retail-power-limits/docs/the-power-limit.md:138-139`, `retail-power-limits/DECISIONS.md:102-104`,
`retail-power-limits/rplimits/cases.py:235-236`.
Figures: 163 projected; 300 governing; forward accrual 20.8 admissible days per month; 11 admissible
days at closure; deadline 2027-03-31. n: a 336-row census (53 + 243 + 25 + 3 + 1 + 11 = 336, which
sums correctly).
Produced by: ETFExperiment `REGISTRATION.md` @ `4d11002` (anchored) and the closing commit
`3f5d629` (not anchored).
Why: this is the note's *own correction* #2 — the note asserts that the numbers it was handed
(845 / above-1,200 / about-302) are not the closure's numbers, and that 163-vs-300 is. If that
re-scoping is wrong, ADR-003 and a headline table cell are both wrong.
In-repo arithmetic note: projecting 20.8/month forward from the 2026-08-29 note date to 2027-03-31
and adding the 11 already held gives ~157, not 163; the same projection to 2027-10-31 gives ~303.5,
consistent with the stated "about 302". The 163 therefore implies an accrual start earlier than the
note's own date, which only ETFExperiment's record can settle.

**C-04 — MUST-VERIFY. HFExperiment's inherited resolution.**
> "**z 1.668** against a 2.50 bar; needed 104.0 %/yr of excess, delivered 70.5"
`retail-power-limits/docs/the-power-limit.md:75` (generated); also
`retail-power-limits/README.md:23`, `retail-power-limits/SOURCES.md:134`,
`retail-power-limits/DECISIONS.md:133-134`, `retail-power-limits/rplimits/cases.py:257-259,426`.
Figures: z 1.668; corrected bar 2.50; needed 104.0 %/yr; delivered 70.5 %/yr; excess 27.99 bp/day;
noise ~418 bp/day; TE 66.4 % annualized. n: one 2.55-year holdout (~643 sessions), touched once.
Produced by: AiTrader `RETURN.md` @ `f819b68` (**not** the anchored AiTrader SHA `705e0ed` — needs
live sibling git history, or a check of whether `RETURN.md` changed between `f819b68` and the
anchor).
Why: this is the fourth case's entire evidentiary basis, and it is the one case the repository
concedes did not fire its own power gate (ADR-004).
In-repo arithmetic notes for the verifier, all computable from figures the note itself states:
66.4 %/√252 = 418.3 bp/day (**consistent** with "near 418"); 27.99 bp × 252 = 70.53 %/yr
(**consistent** with "delivered 70.5"); but 70.5 × (2.50 / 1.668) = **105.7 %/yr**, not the stated
104.0 — equivalently, 104.0 / 70.5 = 1.4752 implies a bar of 2.461, not 2.50. A ~1.6 pp gap that
needs AiTrader's own arithmetic to resolve.

**C-05 — MUST-VERIFY. The progression clock (the note's stated "transferable output").**
> "NPDExperiment's closing commit is stamped 2026-08-25 13:26:58. InsiderExperiment's first commit
> — the one carrying the gate — is stamped 18:34:56 the same day, five hours and eight minutes
> later. Its own closure came at 23:24:15."
`retail-power-limits/docs/the-power-limit.md:211-214`.
Figures: three commit timestamps; a 5 h 08 m gap; "under ten hours" total.
Produced by: git objects in NPDExperiment (`2d3d0ae`, the anchor) and InsiderExperiment (`fbfc74e`
first commit, `12d9fd3` closing commit) — commit-date verifiable with `git log --format=%ad`.
Why: `retail-power-limits/README.md:38-39` calls this progression "the transferable output, and it
matters more than any individual closure". It is the strongest claim in the repository that is
purely git-verifiable.
In-repo arithmetic note: 18:34:56 − 13:26:58 = 5 h 07 m 58 s, so "five hours and eight minutes" is
a round-up of seconds; 13:26:58 → 23:24:15 = 9 h 57 m 17 s, consistent with "under ten hours".
Timezone is not stated in the note and must be pinned when reading the git objects.

**C-06 — MUST-VERIFY. The one figure this repository computes itself.**
> "The 411 minutes is stated as this note's arithmetic over six quoted addends — A.1 22, A.2 34,
> B.0 68, B.0b 52, B.1 194, B.2 41"
`retail-power-limits/DECISIONS.md:184-186`; the derivation is restated at
`retail-power-limits/SOURCES.md:292-300`; the figure is used at
`retail-power-limits/docs/the-power-limit.md:241` and `retail-power-limits/rplimits/cases.py:112`.
Figures: 411 minutes total; addends 22, 34, 68, 52, 194, 41; excludes Z.1.
Produced by: this repository's own arithmetic over NPDExperiment `progress.md` @ `2d3d0ae`
(anchored, checkable from SNAP).
Why: it is the only derived number in the repository, it is a column of the cost-asymmetry table,
and ADR-006 stakes the repository's "everything else is quoted" claim on it.
In-repo check: 22+34+68+52+194+41 = **411** — the sum is correct. What remains is whether each
addend is what NPDExperiment's `progress.md` records, and whether six stages is the complete set.

**C-07 — MUST-VERIFY. NPDExperiment's effective-sample base: two different numbers in two places.**
> "the effective day count fell from 427 to 125.6"
`retail-power-limits/docs/the-power-limit.md:165` (hand-written prose)
versus
> "404 evaluable days; 125.6 independent-equivalent days after the 3.4 variance inflation"
`retail-power-limits/SOURCES.md:42` / `retail-power-limits/rplimits/cases.py:102` (generated).
Figures: 427 vs 404 as the base; 125.6 as the deflated count; variance inflation 3.4.
Produced by: NPDExperiment `progress.md` @ `2d3d0ae` (anchored).
Why it is MUST-VERIFY: 427 / 3.4 = 125.59 (**consistent**), but 404 / 3.4 = 118.82
(**inconsistent** with 125.6). A related third statement, "NPDExperiment lost 70 percent of its
sample to overlapping five-session horizons" (`retail-power-limits/docs/the-power-limit.md:380`),
also fits the 427 base (1 − 125.6/427 = 70.6 %) and not the 404 base (68.9 %). One of the two
bases is being used loosely; only NPDExperiment's record says which. Note that the prose figure
(427) sits **outside** the generated blocks and so is not covered by the drift test.

**C-08 — MUST-VERIFY. HFExperiment's width-widening arithmetic.**
> "Widening 5 names to 50 halves tracking error (66.4 to 31.7 percent) and cuts excess
> proportionally (27.99 to 10.04 bp per day), so z moves only 1.668 to 1.455 and neither width
> clears."
`retail-power-limits/SOURCES.md:134` / `retail-power-limits/rplimits/cases.py:259-261`.
Figures: TE 66.4 → 31.7 %; excess 27.99 → 10.04 bp/day; z 1.668 → 1.455.
Produced by: AiTrader `RETURN.md` "H-F width tables" @ `f819b68` (not the anchor).
Why: it is the sentence that forecloses the obvious repair ("just hold more names"), and it is the
supporting argument for the claim that a better estimator would not change the conclusion
(`retail-power-limits/docs/the-power-limit.md:363-368`).
In-repo arithmetic note: if z scales as excess/TE, then (10.04/31.7)/(27.99/66.4) = 0.7513, giving
z = 1.253, not the stated 1.455. Also "cuts excess proportionally" does not describe the stated
numbers: TE falls ×0.477 while excess falls ×0.359. Either the transcription is lossy or AiTrader's
table uses a term this repository does not carry. Verifiable only against AiTrader.

### Not marked MUST-VERIFY, ranked below

**C-09.** "about 302 admissible days by 2027-10-31, which clears the governing 300 at the published
0.18 by two days and clears nothing at the registered 0.09, where E1 needs 845 and E2 needs above
1,200" — `retail-power-limits/docs/the-power-limit.md:132-139`, `SOURCES.md:122`,
`DECISIONS.md:101-104`, `cases.py:230-236`. n: Amendment 6. Produced by ETFExperiment
`REGISTRATION.md` Amendment 6 @ `4d11002` (anchored). Four figures pinned by
`tests/test_honesty.py:96-97,107-108` (`845`, `above 1,200`, `302`).

**C-10.** "**6.9378 USD** across 920 billed model calls" — `docs/the-power-limit.md:239`;
"6.9378 USD of a 10.00 USD cap across 920 billed gate calls" — `SOURCES.md:50`, `cases.py:112`;
"920 billed calls plus 2 calibration calls" — `docs/the-power-limit.md:240`. Produced by
NPDExperiment `progress.md` @ `2d3d0ae` (anchored). Pinned by `tests/test_honesty.py:100,111`.

**C-11.** "4,585 qualifying events against a registered floor of 1,000; 2,581 sessions at 99.5
percent coverage against a floor of 80 percent; 2,869.9 effective independent periods … variance
inflation of 0.899 is below one" — `SOURCES.md:74`, `cases.py:152-154`. Produced by
InsiderExperiment `REGISTRATION.md` @ `12d9fd3` (anchored). In-repo check: 2,581 / 0.899 = 2,870.97
against the stated 2,869.9, i.e. the implied inflation is 0.89933 and "0.899" is its rounding —
internally consistent.

**C-12.** "a book of 71.9 names that behaves like 29.7, whose 9.993 percent tracking error is the
whole of the 49.35" — `docs/the-power-limit.md:96-97`; fuller at `SOURCES.md:78` /
`cases.py:158-161` ("Section 0.4 required about 23 effective names…top name 14.9 percent and top
five 33.8 percent"). Produced by InsiderExperiment `REGISTRATION.md` @ `12d9fd3` (anchored).

**C-13.** "Stable across Newey-West bandwidths: 50.19 at lag 5, 49.11 at lag 63, 49.53 at lag 126"
— `SOURCES.md:70`, `cases.py:148`. Produced by InsiderExperiment gate commit `cb17046` (not
anchored). This is the robustness evidence behind C-02.

**C-14.** "The equal-weighted secondary, on the identical 71.9 names, would have landed at 34.29 bp
and fired DEGRADED" — `docs/the-power-limit.md:227-229`; restated `docs/the-power-limit.md:388-390`.
Produced by InsiderExperiment `REGISTRATION.md` @ `12d9fd3` (anchored). Load-bearing for the
"refusal was honest about what it forwent" argument.

**C-15.** "94.2 percent of qualifying-shaped insider purchases happen outside the liquid-500 band
this design could trade" — `SOURCES.md:90`, `cases.py:179-180`. Produced by InsiderExperiment
`REGISTRATION.md` @ `12d9fd3` (anchored). This is a scope-limiting figure, so it bounds rather than
supports the claim.

**C-16.** "415 stored daily rankings of 432 eligible window days, 96.1 percent coverage against a
90 percent bar" — `SOURCES.md:42`, `cases.py:100-102`; "415 stored daily rankings covering a
432-day historical window" — `docs/the-power-limit.md:130`. In-repo check: 415/432 = 96.06 %,
consistent with "96.1". Produced by NPDExperiment `progress.md` @ `2d3d0ae` (anchored).

**C-17.** "The projection ran 0.026 to 0.047 across a grid of assumed correlations from 0.0 to 0.7.
The realized figure came in at 0.0512, outside and above the entire grid … the realized contrast
standard deviation of 0.36339 sits at 98 percent of the theoretical maximum reachable only at
correlation minus one" — `docs/the-power-limit.md:169-176`; the sd pair also at `SOURCES.md:38`
("against a registered assumption of at most 0.2626"). Produced by NPDExperiment `REGISTRATION.md`
Section 9 and `progress.md` @ `2d3d0ae` (anchored). This is the mechanism claim for C-01.

**C-18.** "Roughly four times the evaluable days, landing near 1,700 trading days of post-cutoff
window … the window accrues at about 21 trading days a month" — `SOURCES.md:46`, `cases.py:106-108`;
echoed at `docs/the-power-limit.md:366-368`. Produced by NPDExperiment `REGISTRATION.md` @
`2d3d0ae` (anchored). In-repo check: 4 × 415 ≈ 1,660 and 4 × 432 ≈ 1,728, so "near 1,700" is
consistent with either base.

**C-19.** "archive capture density measured 11 of 333 days, 3.30 percent, against a registered 60
percent bar" — `docs/the-power-limit.md:103-104`, versus the generated record's "11 admissible days
at closure, from a 336-row census" — `SOURCES.md:106`, `cases.py:206-210`. In-repo check:
11/333 = 3.303 % (consistent with "3.30"); the census breakdown sums to exactly 336; the two
denominators 333 and 336 differ by 3, matching the "3 no-printed-value" census row. Worth
confirming which denominator the registered 60 % bar was written against. Produced by
ETFExperiment `REGISTRATION.md` @ `4d11002` (anchored).

**C-20.** "E1 needs 237 admissible days at the published 0.18 and 845 at the registered 0.09; E2
needs 300 at 0.18 and above 1,200 at 0.09 … the governing minimum is 300" — `SOURCES.md:102`,
`cases.py:200-203`; the shortfall pair "137 days against the governing figure, and 74 days against
E1's 237" — `SOURCES.md:110`, `cases.py:215-217`. In-repo check: 300−163 = 137 and 237−163 = 74,
both correct. Produced by ETFExperiment `REGISTRATION.md` Section 9 @ `4d11002` (anchored).

**C-21.** "Zero dollars, no capital and no credential at any point. 220 charged requests over the
repository's lifetime. No outcome value was ever read." — `SOURCES.md:114`, `cases.py:220-222`.
Produced by ETFExperiment `REGISTRATION.md` @ `4d11002` (anchored). The "never read an outcome
value" half also backs the note's claim at `docs/the-power-limit.md:35`.

**C-22.** "The raw outperformance was the largest that project ever measured — 90.3 percent per
year against a benchmark's 19.7 — and it still could not clear a significance bar, because a
five-position limit gave the book 66.4 percent annualized tracking error" —
`docs/the-power-limit.md:110-114`. Produced by AiTrader `RETURN.md` @ `f819b68` (not anchored).
Note "the largest that project ever measured" is a superlative over AiTrader's whole record, not a
single figure, and needs the whole register to confirm.

**C-23.** "the lower bound clears zero at day 2,061 and clears the measured 4.07 bp per day cost
hurdle at day 2,852. Eight to eleven years." — `SOURCES.md:142`, `cases.py:269-273`; also
`docs/the-power-limit.md:114-116`, `DECISIONS.md:135-136`. In-repo check: 2,061/252 = 8.18 yr and
2,852/252 = 11.32 yr, consistent with "eight to eleven years". Produced by HFExperiment
`REGISTRATION.md` Section 11 @ `f13e1d3` (not anchored; HFExperiment's anchor is `82e77a0`).

**C-24.** "Primary trial lift −1.0779 net of the central 450 bps cost band, 95 percent
day-clustered bootstrap interval [−3.3354, +0.0204], n = 12,798 amm pools over three birth days,
2,107 measurable at the d0+2 anchor, Q5 cell n = 412" — `SOURCES.md:184`, `cases.py:337-339`;
prose at `docs/the-power-limit.md:297-301`. Produced by solattn `FINDINGS.md` @ `b3f5062`
(**anchored** — checkable from SNAP). `−1.0779` is pinned by `tests/test_honesty.py:116`. This is
one of only three figures the repository offers as evidence *against* its own thesis, so it carries
the scope limit.

**C-25.** "AUC 0.9432 at 100 ms and captured 0.0291 bps per trade on Kraken BTC/USD, which charges
50 bps round trip — a miss of roughly 1,700x … Hyperliquid at 3 bps, it still misses by roughly
100x … H4 cointegration break-even transaction costs ran 300 to 550 bps against that same 3 bps
actual, a margin of 100 to 180x" — `SOURCES.md:172`, `cases.py:311-317`; prose at
`docs/the-power-limit.md:148-153,285-292`. In-repo checks: 50/0.0291 = 1,718 (consistent with
"roughly 1,700x"); 3/0.0291 = 103.1 ("roughly 100x"); 300/3 = 100 and 550/3 = 183.3 ("100 to 180x",
a round-down of 183). Produced by MLCryptoEngine `HYPOTHESES.md` @ `d2a0f05` and
`docs/notes/h1-predictability-without-capturability.md` @ `ae03bf6` (neither is MLCryptoEngine's
anchor `5359a11`). `300 to 550 bps` is pinned by `tests/test_honesty.py:117`.

**C-26.** "18 cleared against a floor of 20 at 30 days, and 4 at 90 days … priced out at 4,695,489
weighted credits, 37.6x the stale 124,764 estimate" and "archived-page sampling manufactures
survivorship by 60 points at 30 days and 79 at 90, 97.5 percent death on 40 birth-ordered pools
against 18.75 percent on 16 attention-crawled ones" — `SOURCES.md:192,196`, `cases.py:353-367`;
prose at `docs/the-power-limit.md:304-312`. In-repo checks: 4,695,489/124,764 = 37.63 (consistent
with "37.6x"); 97.5 − 18.75 = 78.75 points, consistent with "79 at 90"; the "60 points at 30 days"
pair is not stated here and needs solclear. Produced by solclear `FINDINGS.md` @ `c692032` (not
solclear's anchor `d298576`).

**C-27.** "214 wire requests totalling 2.78 GB with zero non-200 responses. About 51 minutes for
Stage A.1 and 20 for Z.1 by the commit record." — `SOURCES.md:82`, `cases.py:165-167`; the time
pair is the right-hand column of the cost-asymmetry table, `docs/the-power-limit.md:241`. Produced
by InsiderExperiment `REGISTRATION.md` @ `12d9fd3` (anchored); "by the commit record" makes the
minute figures git-verifiable in the sibling.

**C-28.** This repository's self-report: "mypy strict clean over 11 source files, 111 tests
passing" — `retail-power-limits/progress.md:68`, restated `progress.md:59`. Verifiable *here*:
mypy's configured scope is `files = ["rplimits", "tests"]` (`pyproject.toml:46`), which contains
**10** `.py` files at the anchor, and a static count of the parametrized suite gives **112** tests
(test_sources 3×24+2 = 74; test_cases 19; test_render 9; test_honesty 10). Both figures are
one-off from the self-report. Hygiene-grade only; nothing in the note rests on it, and a live
collection run (in a scratch copy, never in place) would settle it exactly.

**C-29.** "The note quotes about ninety figures from seven repositories." —
`retail-power-limits/DECISIONS.md:35-36`. Countable in-repo: `cases.py` holds 34 `Figure` objects
(4 power cases × 7 + 3 contrast cases × 2) plus 4 `Headline` records; the number of distinct
*numeric* values across the documents is what "ninety" must mean. Rhetorical scale claim, no
verdict rests on it.

**C-30.** "four of the seven source repositories have no remote. NPDExperiment,
InsiderExperiment, ETFExperiment and HFExperiment are local-only." —
`retail-power-limits/progress.md:113-116`; tabulated at `retail-power-limits/SOURCES.md:262-271`;
restated in the note's scope section at `docs/the-power-limit.md:44-52`. Verifiable with
`git -C <sibling> remote -v` in each of the seven. This is a claim that *weakens* the note, so it is
a disclosure rather than a support; but if it has gone stale (a repo published since 2026-08-29)
the note understates its own checkability.

---

## 3. Intervals and tests

Complete enumeration. **No p-value appears anywhere in this repository**, and **no significance
level, alpha, or target power is stated for any of the required-N or MDE figures** — verified by
grep over `README.md`, `DECISIONS.md`, `progress.md`, `SOURCES.md`, `docs/the-power-limit.md` and
`rplimits/*.py` for `p-value`, `p =`, `alpha`, `significance level`, `one-sided`, `two-sided`,
`power of`. The only hits for "significance" are the phrase "at any significance level"
(solattn, `SOURCES.md:180`) and "could not clear a significance bar" (HF,
`docs/the-power-limit.md:113`).

### Intervals

| # | interval | file:line | stated estimator | n | data structure |
|---|---|---|---|---|---|
| I-01 | `[−3.3354, +0.0204]` around a point lift of `−1.0779`, net of a 450 bps cost band | `retail-power-limits/SOURCES.md:184`; `retail-power-limits/rplimits/cases.py:337-339`; prose `retail-power-limits/docs/the-power-limit.md:298-300` | "95 percent day-clustered bootstrap interval" — the only interval in the repository whose level, clustering and method are all stated | n = 12,798 AMM pools over three birth days; 2,107 measurable at the d0+2 anchor; Q5 cell n = 412 | cross-sectional pools grouped by birth day; clustering on day |
| I-02 | `interval -4.9 to +60.9` | `retail-power-limits/SOURCES.md:134`; `retail-power-limits/rplimits/cases.py:257-258` | **Not stated.** No confidence level, no units, no method. Sits beside "z 1.668 against a corrected bar of 2.50 over a 2.55-year holdout"; the units are presumably bp/day, matching the 27.99 point estimate, and the interval covers zero, consistent with z < bar | one 2.55-year holdout (~643 daily observations), touched once | daily excess return of a 5-position book vs an equal-weighted universe |
| I-03 | "the frozen confidence sequence … the lower bound clears zero at day 2,061 and clears the measured 4.07 bp per day cost hurdle at day 2,852" | `retail-power-limits/SOURCES.md:142`; `retail-power-limits/rplimits/cases.py:269-273` | A **confidence sequence** (an anytime-valid sequential interval), named but with no level, no boundary family and no alpha-spending rule stated | forward daily observations, n = 0 realized (the series was disarmed before its first accrual, `SOURCES.md:138`) | a hypothetical forward daily series; the arithmetic assumes "the sample mean holding at 27.99 bp per day" |
| I-04 | "0.026 to 0.047 across a grid of assumed correlations from 0.0 to 0.7" | `retail-power-limits/docs/the-power-limit.md:169-171`; also `SOURCES.md:38` "a pre-registered projection of 0.026 to 0.047" | **Not an interval.** A pre-registered projection range over a sensitivity grid | grid over assumed correlation between model and baseline | sensitivity analysis, not inference |
| I-05 | "30 to 40 bp per month decayed gross … 13.3 to 34.7 bp per month net"; "Daily rank IC 0.01 to 0.05"; "rank correlation 0.09 registered, against a published magnitude of 0.18 … a quartered 0.045" | `retail-power-limits/SOURCES.md:66,34,98`; `cases.py:139-143,89-92,195-197` | **Not intervals.** Literature-derived effect bands, sourced to Cohen/Malloy/Pomorski 82 bp/month over 1989-2007 decayed 60-70 % on 2008-2024 data | not applicable | the bands the MDEs are judged against |

### Test statistics and decision rules

| # | statistic | file:line | stated test / estimator | n | data structure |
|---|---|---|---|---|---|
| T-01 | `z 1.668` vs a "corrected bar of 2.50" | `retail-power-limits/docs/the-power-limit.md:75,109`; `README.md:23`; `SOURCES.md:134`; `DECISIONS.md:133`; `cases.py:257,426` | A z/t statistic on daily excess return; the bar is described as "corrected", implying a multiplicity adjustment whose family size is not stated here. **No p-value given.** | one 2.55-year holdout, ~643 sessions | daily time series of a 5-position book's excess return |
| T-02 | MDE `49.35 bp per month`; robustness `50.19 / 49.11 / 49.53` | `SOURCES.md:70,86`; `cases.py:146-148` | Minimum detectable effect on a calendar-time portfolio with **Newey-West** standard errors at lags 5, 63 and 126. The governing identity is stated at `docs/the-power-limit.md:195-198`: `t * M * sd / sqrt(N_eff)`. `t` and `M` are not given numerically anywhere in this repository. | 4,585 events; 2,581 sessions; N_eff = 2,869.9 | monthly calendar-time portfolio built from Form 4 events |
| T-03 | MDE `0.0512` (minimum detectable *contrast*) | `docs/the-power-limit.md:72,84`; `SOURCES.md:38`; `cases.py:95` | Same MDE identity; the note names "a permutation test on a rank correlation" as one admissible form (`docs/the-power-limit.md:326`) but does not say which form NPDExperiment used. Variance inflation 3.4 for the overlapping five-session horizon. | 415 stored / 404 evaluable / 125.6 (or 427-based) independent-equivalent days | daily cross-sectional rank IC series with a 5-session forward window |
| T-04 | Required N: `237`, `845`, `300`, `above 1,200` | `SOURCES.md:102`; `cases.py:200-203` | Power calculations expressed as required admissible days for two co-primaries E1 and E2 at two assumed magnitudes (0.18 published, 0.09 registered, plus a quartered 0.045). **The target power and the alpha are stated nowhere in this repository.** Section 10 of the sibling is cited for the "both co-primaries" rule that makes 300 governing. | 11 admissible days achieved; 163 projected | daily rank correlation of ETF flow prints against next-day BTC return |
| T-05 | "Kill criterion K1 fired at 100.0 percent outcome coverage … all 120 computable cells carry a negative point lift with none positive at any significance level" | `SOURCES.md:180`; `cases.py:330-333`; prose `docs/the-power-limit.md:295-297` | A registered kill criterion plus a 120-cell sign/sweep summary; the underlying interval is I-01 | 120 computable cells; n = 12,798 pools | quantile cells × cohorts × horizons |
| T-06 | "a registered underpowered rule — 18 cleared against a floor of 20 at 30 days, and 4 at 90 days — so no significance was claimed in either direction" | `SOURCES.md:192`; `cases.py:354-357`; prose `docs/the-power-limit.md:305-308` | A pre-registered minimum-n rule that suppresses inference rather than a test statistic. The note calls this the earliest power-shaped refusal in the program. | 18 cleared pools at 30 days; 4 at 90 days; floor 20 | pool-level outcome study |
| T-07 | `AUC 0.9432` at 100 ms | `SOURCES.md:172`; `cases.py:312`; prose `docs/the-power-limit.md:149,286` | A discrimination statistic, offered as evidence the closure was *not* power-bound. Related: "H9 insignificant after deflation" (`SOURCES.md:168`) implies a deflated performance statistic whose form is not given. **No p-value, no interval.** | not stated in this repository | short-horizon classification on Kraken BTC/USD trades |
| T-08 | The MDE identity itself: "`MDE = t * scale * sd / sqrt(N_eff)`" | `retail-power-limits/docs/the-power-limit.md:324`; the quoted sibling form "`t * M * sd / sqrt(N_eff)`" at `docs/the-power-limit.md:196` | The load-bearing methodological claim of the whole note: that the right-hand side needs no first moment. Two different symbols (`scale`, `M`) for the same term, neither given a value in any case. | — | — |

---

## 4. Provenance claims

Statements that a bar, parameter, outcome map, prior or decision rule was fixed at a named commit
or before data existed. Quoted verbatim with `file:line`, the commit named, and what would have to
be true for the claim to hold.

**P-01. The framing claim.**
> "Across four independent pre-registered experiments, the binding constraint was not whether a
> published effect exists."
`retail-power-limits/docs/the-power-limit.md:11-12`; `retail-power-limits/README.md:3-5`;
`retail-power-limits/pyproject.toml:4`.
Commit named: none. Would have to be true: each of the four carries a registration committed before
its own measurement, and each closed on a detectability figure rather than a measured null. The
repository itself weakens the "independent" half at `docs/the-power-limit.md:54-60` ("independent
hypotheses, not independent investigators") and concedes at `docs/the-power-limit.md:141-146` that
one of the four (HFExperiment) did not fire a power gate at all.

**P-02. The gate-before-the-measurement claim — the strongest provenance claim in the note.**
> "The gate was committed in the repository's first commit, `fbfc74e`, titled 'scaffold, standing
> guards, and REGISTRATION Section 0 power gate' — before the corpus existed, before the portfolio
> existed, and before there was anything for it to judge. The bars were fixed at 20 bp for GO and
> 40 bp for BLOCKED"
`retail-power-limits/docs/the-power-limit.md:218-223`; the same claim as a source detail at
`retail-power-limits/rplimits/sources.py:86` and `retail-power-limits/SOURCES.md:226`.
Commit named: InsiderExperiment `fbfc74e` (**not** InsiderExperiment's anchored SHA `12d9fd3`).
Would have to be true: (a) `fbfc74e` is genuinely the first commit in InsiderExperiment's history
(`git rev-list --max-parents=0`); (b) its subject is as quoted; (c) the 20/40 bars and the boundary
convention "An MDE of exactly 20.00 bp is GO" (`docs/the-power-limit.md:223-224`) are present in
that commit's `REGISTRATION.md` Section 0; (d) no corpus or portfolio artifact exists in that tree.
All four are decidable from git objects alone.

**P-03. The progression clock.** (Also numeric claim C-05.)
> "NPDExperiment's closing commit is stamped 2026-08-25 13:26:58. InsiderExperiment's first commit
> … is stamped 18:34:56 the same day, five hours and eight minutes later. Its own closure came at
> 23:24:15."
`retail-power-limits/docs/the-power-limit.md:211-214`.
Commits named implicitly: NPDExperiment `2d3d0ae`, InsiderExperiment `fbfc74e` and `12d9fd3`.
Would have to be true: those three commit timestamps, read in a single consistent timezone, and
`2d3d0ae` genuinely being NPDExperiment's closing commit.

**P-04. NPDExperiment registered the risk before spending.**
> "Its ADR-007 had registered the exact failure mode as a risk before collection began … The
> registration said so, in writing, before a cent was spent, and chose not to repair it by
> promoting the better-powered secondary"
`retail-power-limits/docs/the-power-limit.md:161-168`; cited via
`retail-power-limits/rplimits/sources.py:58` ("ADR-007 registering the contrast power honestly").
Commit named: NPDExperiment `2d3d0ae` (the anchor). Would have to be true: ADR-007 exists at that
commit with the stated content, and — for "before a cent was spent" — the ADR predates the billed
collection in NPDExperiment's own commit history, not merely in the final tree.

**P-05. NPDExperiment's effect band was registered before any call went out.**
> "Daily rank IC 0.01 to 0.05, the realistic band from the literature, registered in Section 9.2
> before any call went out."
`retail-power-limits/rplimits/cases.py:89-92`; `retail-power-limits/SOURCES.md:34`.
Commit named: NPDExperiment `2d3d0ae` (anchor). Would have to be true: Section 9.2 with the
0.01-0.05 band is present in a commit that precedes the first billed API call.

**P-06. InsiderExperiment's BLOCKED floor was committed before the measurement existed.**
> "against a registered BLOCKED floor of 40 bp committed before the measurement existed"
`retail-power-limits/rplimits/cases.py:147`; `retail-power-limits/SOURCES.md:70`.
Commits named: `fbfc74e` (the floor) and `cb17046` (the measurement). Would have to be true:
`fbfc74e` precedes `cb17046` in both commit order and timestamp, and the 40 bp floor is unchanged
between them (a `git diff fbfc74e cb17046 -- REGISTRATION.md` on Section 0 settles it).

**P-07. The tempting secondary was registered as non-verdict-bearing before any number was visible.**
> "It was registered as non-verdict-bearing before any number was visible, and it was not promoted.
> The repository recorded the temptation explicitly, and recorded that any future test naming
> equal-weight as primary would have to disclose that the choice was made after seeing this number."
`retail-power-limits/docs/the-power-limit.md:227-232`.
Commit named: none directly; implied `fbfc74e`. Would have to be true: the equal-weight secondary
is marked non-verdict-bearing in a commit predating `cb17046`, and the disclosure obligation is
recorded in InsiderExperiment's own text.

**P-08. The structural separation of the first moment from the power path.**
> "The raw daily excess returns went into one store whose mean *is* the answer, with a single
> permitted reader. A second store held the same series with its own mean already subtracted, and
> the mean was never written there, so it could not be recovered. The power module was forbidden by
> import guard from reaching the portfolio, market or evaluation packages — the path from the power
> computation to a first moment does not exist, rather than existing and being avoided."
`retail-power-limits/docs/the-power-limit.md:200-206`; the outcome restated at
`docs/the-power-limit.md:208-209` ("The alpha is still sealed") and
`retail-power-limits/rplimits/cases.py:167`.
Commit named: none. Would have to be true: an import guard exists in InsiderExperiment's source at
`12d9fd3`, with a test enforcing it, and the demeaned store genuinely never persists a mean. This
is the one provenance claim that is a *code* claim and is checkable by reading the sibling's source
rather than its prose.

**P-09. solclear's underpowered rule predates the measurement, and predates NPDExperiment by
eleven days.**
> "Its underpowered rule was registered before the measurement and fired on 2026-08-14, eleven days
> before NPDExperiment."
`retail-power-limits/rplimits/cases.py:370-372`; `retail-power-limits/SOURCES.md:200`; prose at
`docs/the-power-limit.md:264-266`.
Commit named: solclear `c692032` (dated 2026-08-22 in the registry, i.e. **after** the 2026-08-14
firing it documents). Would have to be true: the rule appears in a solclear commit predating the
Stage E measurement. In-repo check: 2026-08-25 − 2026-08-14 = 11 days, so the "eleven days"
arithmetic is correct. This claim carries weight because it is the note's own evidence that the
practice was not novel (`docs/the-power-limit.md:262-272`).

**P-10. HFExperiment's Section 11 was registered on 2026-08-23 and priced the forward verdict in
advance.**
> "HFExperiment's Section 11, registered 2026-08-23, priced its own forward verdict at eight to
> eleven years and the operator proceeded anyway, deliberately"
`retail-power-limits/docs/the-power-limit.md:266-269`.
Commit named: none at this line; the Section 11 figures are cited to `hf-registration` = `f13e1d3`
dated 2026-08-25 (`retail-power-limits/rplimits/sources.py:130-136`) — **two days after the
2026-08-23 registration date asserted in the prose**, and to a README at `0a0d214` dated
2026-08-23. Would have to be true: Section 11 with the 2,061/2,852 schedule exists in an
HFExperiment commit dated 2026-08-23. Worth checking because the note's argument here is that the
arithmetic was "present, correct, and non-binding" *before* the operator proceeded.

**P-11. The commit hashes are stable because the sibling repositories are closed.**
> "The sibling repositories are closed. Their closing commits do not move, so the short hashes
> below are stable references rather than moving branch tips."
`retail-power-limits/SOURCES.md:8-9`; the same in module prose at
`retail-power-limits/rplimits/sources.py:11-13` ("these repositories are closed, and a closed
repository does not move"), and again at `SOURCES.md:279-282` ("A hash recorded now against a
closed repository is a real commitment, not a placeholder").
Commits named: all 24. Would have to be true: each of the 24 short hashes resolves, unambiguously,
in the named repository, and each named file path exists at that commit. Note that the audit's own
anchor table shows several siblings moved after this note was written — the corresponding claim to
check is not "the hashes moved" (they cannot) but whether a *cited file's content* differs between
the cited commit and the sibling's anchored SHA, which is exactly the drift ADR-001 warns about
(`retail-power-limits/DECISIONS.md:45-47`: "the copy can go stale in a way the original cannot").

**P-12. The ETF triple belongs to Amendment 6, not to the closure.**
> "The 845 / above-1,200 / about-302 triple is real but does not belong to the closure firing.
> Those are Amendment 6's numbers"
`retail-power-limits/rplimits/cases.py:230-236`; `retail-power-limits/SOURCES.md:122`;
`DECISIONS.md:101-104`; prose `docs/the-power-limit.md:132-139`.
Commit named: ETFExperiment `4d11002` (the anchor). Would have to be true: Amendment 6 exists at
that commit and carries those three figures, and the closure commit `3f5d629` states the 163-vs-300
comparison instead. Both are readable from `SNAP/ETFExperiment/` for the first half.

**P-13. HFExperiment did not fire a power gate; the resolution is inherited.**
> "HFExperiment did not. Its Section 0 fired BLOCKED on IBKR's refusal of fractional quantities
> through the API, and it then closed by operator decision on 2026-08-26 with its shadow series
> never started."
`retail-power-limits/DECISIONS.md:125-129`; the same as a case caveat at
`retail-power-limits/rplimits/cases.py:286-294` and `SOURCES.md:154`; in the note at
`docs/the-power-limit.md:141-146` including "errors 10243 and 10244".
Commits named: `hf-progress` `82e77a0` (the anchor) for the closure entry; `hf-readme` `0a0d214`
for the inheritance sentence. Would have to be true: the closure entry dated 2026-08-26 exists in
HFExperiment's `progress.md` at `82e77a0` (checkable from SNAP), and the README's first sentence
reads as quoted at `0a0d214`. This is a self-weakening disclosure and is the reason the note's
own headline says "resolved on statistical power" rather than "BLOCKED" for this case.

**P-14. Four of the seven sources are unpublished.**
> "Four of the seven source repositories are not published. The four power cases — NPDExperiment,
> InsiderExperiment, ETFExperiment and HFExperiment — exist only on the operator's machine and have
> no remote."
`retail-power-limits/docs/the-power-limit.md:44-47`; table at
`retail-power-limits/SOURCES.md:262-271`; discovery recorded at
`retail-power-limits/progress.md:111-123`.
Commit named: none. Would have to be true: `git remote -v` is empty in those four and non-empty
(GitHub, `kirosli00tuff/…`) in the other three plus AiTrader, as of the reading date. This is a
time-sensitive disclosure: it can only have become *wrong in the note's favour*.

**P-15. This repository wrote to nothing.**
> "Read-only, nothing modified in any sibling repository. No sibling repository was written to, and
> this repository imports nothing from them at runtime — the figures are transcribed, not loaded,
> so a stale sibling checkout cannot change what this note says."
`retail-power-limits/progress.md:31-34`; the same in ADR-001 at
`retail-power-limits/DECISIONS.md:42-43` ("It reads all seven sibling repositories and writes to
none of them").
Commit named: none. Would have to be true: no sibling repository has a commit authored on
2026-08-29 attributable to this work, and `rplimits/` contains no filesystem or network read of a
sibling path. The second half is **verifiable in-repo and holds**: `rplimits/docsync.py:27` roots
every path at this repository's own parent, and no module imports `subprocess`, `requests`,
`urllib` or reads any path outside `ROOT`.

**P-16. Exactly one figure is derived; everything else is quoted.**
> "The 411 minutes is stated as this note's arithmetic over six quoted addends … Every other number
> in the repository is quoted rather than computed."
`retail-power-limits/DECISIONS.md:184-187`; restated at `retail-power-limits/SOURCES.md:294-300`
("Every other number in this repository is quoted, not computed") and
`retail-power-limits/README.md:53-55`.
Commit named: NPDExperiment `2d3d0ae` for the addends. Would have to be true: no other figure in
`cases.py`, the note or the README is an arithmetic combination the siblings do not themselves
state. This is checkable exhaustively and is the repository's central honesty claim about itself.
Candidates that a verifier should test against it include the ratios "roughly 1,700x" / "roughly
100x" / "100 to 180x" (C-25), the shortfalls 137 and 74 (C-20), "37.6x" (C-26), "a shortfall of
1.5x" (C-04) and "eight to eleven years" (C-23) — each is derivable from stated primitives, so the
question is whether the *sibling* states the ratio or whether this repository formed it.

**P-17. The one-shot read, and the still-sealed alpha.**
> "NPDExperiment's design permitted a single evaluation of its sealed store … When a post-hoc
> amendment proposed scoring the same data at two more horizons, the registration voided it:
> *scoring spent data against new horizons is a second look however it is labelled*."
`retail-power-limits/docs/the-power-limit.md:248-253`; the counterpart claim
> "**intact** — the sealed alpha was never opened"
`retail-power-limits/docs/the-power-limit.md:242`, and "The realized alpha was never read and sits
sealed" `retail-power-limits/rplimits/cases.py:167` / `SOURCES.md:82`.
Commits named: NPDExperiment `2d3d0ae` (Section 17 amendments per
`retail-power-limits/rplimits/sources.py:44`); InsiderExperiment `12d9fd3`.
Would have to be true: the voided amendment exists in NPDExperiment's Section 17 with that
language, and InsiderExperiment's sealed store shows no read in its record.

**P-18. This repository's own drift guarantee.**
> "Every figure is typed as `Figure(value, source)` in `rplimits/cases.py`, and
> `Figure.__post_init__` raises on a source key that does not resolve. A figure cannot be added
> without a citation, because the constructor refuses."
`retail-power-limits/DECISIONS.md:67-70`; the generated-block half at `DECISIONS.md:74-76`.
Commit named: this repository's own anchor `dda39b2`. **Verifiable in-repo, and the mechanism is
present as described**: `rplimits/cases.py:29-33` raises `KeyError` on an unknown source and
`ValueError` on an empty value; `tests/test_render.py:31-37` re-renders all four blocks and
compares. The limit a verifier should record: the drift test covers only the four marker-delimited
blocks. **`README.md` carries no generated block at all**, so its four-case table
(`retail-power-limits/README.md:18-23`) and its figure list (`README.md:78-80`) are pinned only by
string-presence assertions in `tests/test_honesty.py`, not by re-rendering. A figure could be
changed consistently in the README prose without the drift test noticing, provided the nine pinned
substrings survive.

**P-19. The boundary convention was written down with the bar.**
> "with the boundary conventions written down ('An MDE of exactly 20.00 bp is GO')"
`retail-power-limits/docs/the-power-limit.md:222-224`.
Commit named: InsiderExperiment `fbfc74e`. Would have to be true: that exact sentence, or its
equivalent, is in Section 0 at the first commit.

**P-20. The AiTrader holdout was touched once.**
> "One 2.55-year holdout, touched once at commit a0a9ef6."
`retail-power-limits/SOURCES.md:138`; `retail-power-limits/rplimits/cases.py:265`; the commit's
subject is quoted at `retail-power-limits/rplimits/sources.py:170` ("…holdout touched once,
findings only, nothing applied").
Commit named: AiTrader `a0a9ef6` (not AiTrader's anchor `705e0ed`). Would have to be true: the
commit subject reads as quoted, and no later AiTrader commit re-scores that holdout for H-F.

**P-21. ETFExperiment's deadline was registered, not chosen at closure.**
> "the registered deadline of 2027-03-31"
`retail-power-limits/SOURCES.md:118` (closure language) and `SOURCES.md:106`;
`retail-power-limits/rplimits/cases.py:209,226`.
Commit named: ETFExperiment `4d11002` (anchor) and the closing commit `3f5d629`. Would have to be
true: 2027-03-31 appears as the deadline in a registration commit predating the closure, not
introduced by an amendment after the 163 projection was computed. This matters because the whole
"untestable at achievable power" verdict is a statement about what is reachable *by that date*.

**P-22. This repository's own ADR dates.**
> "**Status.** Accepted, 2026-08-29." (six times: `retail-power-limits/DECISIONS.md:10,58,89,123,154,179`)
Commit named: none. Verifiable in-repo, and consistent: all three commits in this repository are
dated 2026-08-29 local (`0974f96` 00:19:47−07:00, `710093d` 00:20:34, `dda39b2` 00:21:28), and
`progress.md:15` records the scaffold at 00:07:32 with gates green at 00:18. The ADRs cannot have
been "accepted before" anything measured here, because nothing was measured here.

---

## Summary counts

- Artifacts inventoried: **21 tracked files** (5 `rplimits` modules, 5 test files, 5 markdown
  documents, 4 build/config files, `LICENSE`, `.gitignore` — counted as 21 paths in
  `git ls-files`) plus **6 untracked/gitignored cache and venv directories**.
- Numeric claims listed: **30**, of which **8 are marked MUST-VERIFY**.
- Intervals: **5** (3 genuine intervals, 2 recorded as ranges that are not intervals).
- Test statistics / decision rules: **8**. **Zero p-values anywhere in the repository.** Zero
  stated alphas or target power levels.
- Provenance claims: **22**.
- Source citations to be resolved: **24**, of which **12 keys / 11 commits** match a sibling's
  anchored SHA and are checkable from the snapshots, and **12 keys** require live sibling git.

## What a verifier can and cannot close inside this repository

**Closable here (no sibling access needed):** the 411-minute sum (correct); the census sum
53+243+25+3+1+11 = 336 (correct); the shortfalls 137 and 74 (correct); 415/432 = 96.06 % ≈ 96.1
(correct); 11/333 = 3.303 % ≈ 3.30 (correct); 4,695,489/124,764 = 37.63 ≈ 37.6x (correct);
50/0.0291 ≈ 1,718 ≈ "roughly 1,700x" and 3/0.0291 ≈ 103 ≈ "roughly 100x" (correct); 300/3 = 100 and
550/3 = 183 against "100 to 180x" (a round-down); 66.4/√252 = 418.3 bp ≈ "near 418" (correct);
27.99 × 252 = 70.53 ≈ "delivered 70.5" (correct); 2,061/252 = 8.2 yr and 2,852/252 = 11.3 yr ≈
"eight to eleven years" (correct); 2,581/0.89933 = 2,869.9 (consistent within the stated rounding);
97.5 − 18.75 = 78.75 ≈ "79 at 90" (correct); the 11-day gap 2026-08-14 → 2026-08-25 (correct); the
5 h 07 m 58 s gap against "five hours and eight minutes" (a seconds round-up); the presence and
behaviour of the `Figure` constructor guard and the drift test (present as described).

**Three internal tensions that need a sibling to settle, all carried into the MUST-VERIFY list:**
C-07 (427 vs 404 as the base for 125.6), C-08 (z 1.668 → 1.455 does not follow from the stated TE
and excess ratios; implied 1.253), C-04 (104.0 %/yr needed does not follow from 70.5 delivered and
a 2.50 bar; implied 105.7, or a bar of 2.461).

**Not closable here at all:** every value's fidelity to its sibling record — which is, by the
repository's own design and its own ADR-002 admission, the entire risk surface: "a transcription
slip here is invisible, because there is no measurement to disagree with it"
(`retail-power-limits/DECISIONS.md:61-63`).

---

## Live-repo access log

Live path accessed: `/home/kiros-li/Documents/GitHub/retail-power-limits/`
Purpose: git history/provenance (purpose 1) and working-tree listing for untracked data
(purpose 2). No file in the live repository was opened for writing. No `.env`, keystore, session or
credential file was read; none exists in this repository.

**`git -C /home/kiros-li/Documents/GitHub/retail-power-limits status --porcelain` BEFORE first
access — 2026-09-03T23:55:51Z — output verbatim:**

```
```

(empty — clean working tree, no untracked entries)

**`git -C /home/kiros-li/Documents/GitHub/retail-power-limits status --porcelain` AFTER last
access — 2026-09-03T23:59:15Z — output verbatim:**

```
```

(empty — clean working tree, unchanged)

No unexpected working-tree entries were found; nothing was modified.

**Commands run against the live repository, all read-only:**

| command | time (UTC) | why |
|---|---|---|
| `git status --porcelain` | 2026-09-03T23:55:51Z | mandatory before-log |
| `ls -la` (top level, `docs/`, `rplimits/`, `tests/`) | 2026-09-03T23:56Z | untracked-data inventory: sizes and mtimes |
| `git status --ignored=matching --porcelain` | 2026-09-03T23:57Z | enumerate gitignored material |
| `du -sh .venv .mypy_cache .pytest_cache .ruff_cache` | 2026-09-03T23:57Z | sizes of ignored directories, without opening them |
| `find … -printf` (caches and `.git` pruned) | 2026-09-03T23:57Z | confirm no data files outside git |
| `git ls-files` | 2026-09-03T23:57Z | tracked-file list |
| `git rev-parse HEAD`; `git log --format=…`; `git remote -v`; `git branch -a` | 2026-09-03T23:58Z | confirm the anchor and read commit provenance |
| `git status --porcelain` | 2026-09-03T23:59:15Z | mandatory after-log |

**Unanchored reads:** none. Every figure cited in this inventory was read from
`SNAP/retail-power-limits/` at the anchored SHA `dda39b2f148569a6fe9be956a979471b2330611d`. The
only live-repo content quoted above is git metadata (HEAD, three commit records, the remote URL)
and the directory listing, both read at the times logged. The live working tree matched the anchor:
`git status --porcelain` was empty at both ends, so no tracked file differs from `dda39b2`.

**Scratch work:** arithmetic checks were written to and run from
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/2c6a58bc-6f69-48c9-a930-b20684f1e1e4/scratchpad/work/agentC/checks.py`.
No repository script was executed, in place or otherwise.
