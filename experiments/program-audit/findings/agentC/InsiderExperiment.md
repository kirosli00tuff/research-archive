# InsiderExperiment — Agent C findings (referee and verifier)

Repository: `InsiderExperiment`
Anchored SHA: `12d9fd36cf055cb10ea67a3fc737e404217bc95a` (master, 2026-08-25) — also the live `HEAD`,
so the anchor and the git history coincide and the repository is closed.
Agent: **C** (referee; no thesis). Consolidated 2026-09-04.

Inputs merged: `findings/agentC/verification/InsiderExperiment.inventory.md` and `.inventory.json`;
`findings/agentC/verification/InsiderExperiment.verification.md` and `.claims.json`;
`findings/agentC/provenance/InsiderExperiment.md` and `.json`.
Snapshot re-read for this pass: `SNAP/InsiderExperiment/` (tracked, anchored). Live git objects and
untracked ledgers re-read read-only on 2026-09-04 18:45 UTC for the load-bearing checks; see §Live-repo
access log.

---

## Summary

The deciding number reproduces exactly. The minimum detectable effect of 49.35 bp per month, the
BLOCKED branch it fires, the tracking error and effective-period count behind it, the corpus totals
and attrition funnel, the lag distribution, the cost band, the Section 0.4 floor derivation, the
universe port and the zero-dollar fetch record all recompute from the repository's own stored
primitives and agree to the precision at which they are stated. The pre-registration ordering also
holds: Section 0 is byte-identical from the first commit to the anchor, every enforced bar was frozen
22 seconds before the first wire request, and the primary/secondary weighting labels predate the
first number by twelve minutes.

Ten findings survive consolidation. None of them moves the BLOCKED verdict and none of them touches
49.3543. Five are stale or mis-transcribed descriptive figures, two are pairs of numbers computed on
two different books and then presented as one comparison, one is a process breach (a registered
configuration field deleted after the verdict was visible, against a Section 16 that says no amendment
is in force), one is a session-cost record the git history does not support, and one is a timezone
label. What could not be checked is stated as such and not guessed at: the sealed alpha store was
never opened, every cross-repository and literature figure needs its source, and the decayed 30–40 bp
literature band that the BLOCKED floor was placed against is load-bearing and external to this
repository.

---

## Verification scoreboard

### Claims

| Status | Count |
|---|---|
| VERIFIED | **33** |
| CONTRADICTED | **9** |
| UNVERIFIABLE | **5** |
| **Total claims audited** | **47** |

(Counts are the rows of the claims table in `verification/InsiderExperiment.verification.md` §A.
Separately, §B recomputed **49** derived quantities from stored primitives: **44** agree, **5**
disagree — the role-rejection share, the ETA column sum, the collected test count, the printed
by-year table, and the priced-vs-membership book width.)

**MUST-VERIFY claims (Ranks 1–7 of the inventory), with status:**

| Rank | Claim | Status |
|---|---|---|
| 1 | "The minimum detectable effect is 49.35 bp per month against a registered BLOCKED floor of 40" (`REGISTRATION.md:812-816`) | **VERIFIED** — recomputed 49.3543 from the 2,581 stored centered values |
| 2 | "CORPUS-GO. 4,585 qualifying events … Mean book width 71.9 names" plus the by-year table (`REGISTRATION.md:594-608`) | **PARTLY CONTRADICTED** — 4,585, 99.5 % and 71.909 all verify; the printed by-year table sums to 4,542 and is pre-fix (finding -2) |
| 3 | "tracking error … 9.993 percent across 2,869.9 effective independent periods from 2,581 sessions, and that tracking error is the whole of the 49.35" (`REGISTRATION.md:844-848`) | **VERIFIED** — 9.9933 %, 2,869.9, VIF 0.8993, and the identity closes to 1e-3 |
| 4 | "The value-weighted book holds a mean of 71.9 names and behaves like 29.7 effective names" (`REGISTRATION.md:839-841`) | **CONTRADICTED** — the two figures are computed on two different books (finding -3); 14.9 % and 33.8 % verify |
| 5 | "214 wire requests totalling 2.78 GB with zero non-200 responses" and the byte-exact cache (`REGISTRATION.md:827-833`) | **VERIFIED** — 214 wire records, 2,783,280,665 bytes, 0 non-200, cache equal byte for byte |
| 6 | "The commit record puts Stage A.1 at about 51 minutes … and Stage Z.1 at about 20 minutes" (`progress.md:115-117`) | **CONTRADICTED** — the document's own actuals sum to 111 min, and the record carries one Z.1 commit (finding -5) |
| 7 | "the equal-weighted book holds 71.9 and behaves like 66.9, with tracking error of 6.86 percent and an MDE of 34.29 bp per month, which would have fired DEGRADED" (`REGISTRATION.md:852-854`) | **PARTLY CONTRADICTED** — 6.86 %, 34.29 and the DEGRADED branch verify exactly; the "71.9 → 66.9" pair does not (finding -4) |

### Intervals

| Metric | Count |
|---|---|
| Intervals audited | **3** |
| Independence doubtful | **0** |
| Recomputed | **1** |
| Conclusion moved | **0** |

**There is no confidence interval anywhere in this repository.** Stage A.1 computes second moments
only; Stage B, where an interval would have lived, was never written (`REGISTRATION.md:483-488`,
`:769-774`, `:889-891`). The three audited rows are: (i) the absent interval itself — UNVERIFIABLE,
nothing to check; (ii) the *registered but never fired* Stage B interval — day-clustered SEs with a
Newey-West Bartlett kernel at lag 21 over the grid 5/21/63/126, which **explicitly rejects
independence across days** (`REGISTRATION.md:452-465`, `:340-349`); (iii) the interval-shaped object
that was computed, the Bartlett variance inflation feeding N_eff (`dispersion.py:104-120`) —
**recomputed and VERIFIED** at 0.8993 and across the whole lag grid.

Direction of the adjustment, stated because it matters for the referee's job: VIF < 1 at every lag, so
the serial-correlation treatment *raises* N_eff and *lowers* the MDE. It moves the verdict toward GO,
not toward BLOCKED. The verdict survives the entire registered grid (49.11 to 50.19 bp, all above 40).

### Tests

| Metric | Count |
|---|---|
| Test-statistic-shaped quantities audited | **9** |
| Tail mismatch | **0** |
| Degrees-of-freedom issue | **0** |
| Multiplicity-correction mismatch | **0** |

**There is no p-value and no realized test statistic anywhere in this repository.** No hypothesis test
was run. Summary of the nine audited quantities: the critical value 2.0 is a registered constant used
as a normal-approximation two-sided bound, no dof is claimed and none is needed; the registered
direction is one-sided (positive alpha) while the applied bound is two-sided, which is the *harder*
bar and therefore conservative, not flattering; the corpus gate is a **conjunction** (both the
1,000-event floor and the 80 % coverage floor required, chained early returns at `section0.py:106,117`)
and correctly carries no union-type correction; the Newey-West lag grid is a declared non-verdict-bearing
sensitivity report (`REGISTRATION.md:474-476`), the verdict is read off the registered lag rather than
the best of four, so there is no selection to correct; the three secondaries were labelled
non-verdict-bearing in the first commits, before any of them was computed, and none is promoted, so
there is no multiple-comparisons family to correct. One quantity (the cross-repository "H-F at z 1.668
against a 2.50 bar") is UNVERIFIABLE here.

Recorded, not raised as a finding: the MDE convention is `t_crit·SE`, i.e. 50 % power, not the
conventional 80 %-power `(z_{α/2}+z_β)·SE`. It was registered before measurement and applied
identically to every series and every bar in Section 0.4, and it cannot flatter the verdict — at the
conventional convention the primary MDE would be 69.1 bp, i.e. more strongly BLOCKED.

### Provenance

| Status | Count |
|---|---|
| SUPPORTED | **17** |
| NOT_SUPPORTED | **4** |
| PARTIAL | **2** |
| UNVERIFIABLE | **1** |
| **Total provenance rows audited** | **24** (16 registration claims IP-01…IP-16, 8 post-data parameter changes C-1…C-8) |

NOT_SUPPORTED: IP-06 and C-1 (the same breach — finding -1), IP-15 (the Z.1 duration — finding -5),
IP-16 (the timezone label — finding -10). PARTIAL: IP-09 (no systemd unit — true today, the 2026-08-25
state is not observable) and IP-10 (one of the two AiTrader hashes independently reconfirmed, the other
no longer reproducible through no fault of this repository). UNVERIFIABLE: IP-14 (the program calibration
ledger lives outside this repository).

### Merge and de-duplication record

Twelve draft findings entered consolidation: nine from the verification pass (DRAFT-V-1…V-9) and three
from the provenance pass (DRAFT-P-1…P-3). Two merges were made and **no draft was dropped** — every one
carried a verbatim quote with a file and line and at least one figure with its n.

- DRAFT-V-6 + DRAFT-P-1 → **-1**. Same quoted claim (`REGISTRATION.md:800`), same git object. Merged;
  class taken as PROVENANCE, with the process dimension stated in the evidence.
- DRAFT-V-5 + DRAFT-P-2 → **-5**. Same quoted passage (`progress.md:115-119`); DRAFT-P-2 itself flagged
  the overlap. Merged; both evidence strands (the 111-minute column sum and the single Z.1 commit) kept.

Drops for want of a locatable quote or figure: **0**.

---

## Findings

### AUDIT-C-InsiderExperiment-1
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** the registration's amendment discipline — the frozen `Config` and Section 16
- **Direction:** neutral (referee finding; no measured figure moves either way)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "None in force. Section 0 fired BLOCKED, so no amendment can authorize
  Stage B." — InsiderExperiment/REGISTRATION.md:800, read against "Changing a registered value after that
  commit requires a numbered / amendment in Section 17 carrying its own evidence." —
  InsiderExperiment/REGISTRATION.md:8-9, and against the config file's own rule at
  InsiderExperiment/src/insider/config.py:8-9.
- **Evidence:**
  - A registered field was deleted after the verdict was visible. `git -C <live> diff fbfc74e 672b343 --
    src/insider/config.py` (read 2026-09-04 18:45 UTC) is exactly two deletions, verbatim:
    ```
    @@ -21,7 +20,6 @@ class Config:
         universe_id: str
    -    benchmark_id: str
    @@ -87,7 +86,6 @@ CONFIG: Final = Config(
         universe_id="U-LIQ-500-stk-w60-m40-p5",
    -    benchmark_id="U-LIQ-500-VW",
    ```
    n/a — a code object, not a sample. `git log -S 'benchmark_id' -- src/insider/config.py` returns exactly
    two commits: `fbfc74e` (2026-08-25T18:34:56−07:00, the introduction) and `672b343`
    (2026-08-25T19:11:45−07:00, the deletion).
  - The deletion is **after** the corpus was built (`ccc9b13`, 18:47:16) and **after** the power gate fired
    BLOCKED (first `power_gate` evidence record 18:51:14 local, `ledgers/evidence.jsonl`, UNANCHORED, read
    18:24 UTC). CORPUS-GO had fired four times and the power gate three times before the field was removed.
  - No amendment records it. `REGISTRATION.md:798-800` is the quoted "None in force."; `git grep benchmark_id
    HEAD` and `git grep "U-LIQ-500-VW" HEAD` both return nothing; none of the thirteen ADRs in
    `DECISIONS.md` mentions the identifier.
  - The mechanism is visible in the same commit. `src/insider/config.py:3-6` states that every declared field
    must be referenced by at least one module outside the file, and `tests/test_guards.py:119-130`
    (`test_every_config_field_has_an_enforcement_site`) asserts exactly that over the AST — a guard that
    `672b343` introduced and that mutation 5 of `reports/stage_a1/mutations.json` targets. `git grep -n
    benchmark_id fbfc74e -- src tests scripts` returns only the declaration and the value, so the field had
    **no enforcement site**: it was deleted to satisfy the new guard rather than enforced or amended.
  - No figure moves. Because no module ever read the field at any commit, its removal cannot have touched
    49.3543, 4,585, 71.909 or any other number; `reports/stage_a1/portfolio.json` still carries a
    `no_benchmark: 0` drop key, so the benchmark itself is still computed in `portfolio/returns.py`. Only its
    registered *identifier* is gone, leaving Section 5's benchmark (`REGISTRATION.md:351-357`) as prose with
    nothing enforcing it — and that prose is ambiguous, since `returns.py:202` passes each series' own
    weighting into the benchmark, so the equal-weighted series is benchmarked against an equal-weighted
    universe (`portfolio.json[3].diagnostics.bench_weight_top1_share` 0.002 = 1/500 against 0.070165 for the
    value-weighted rows).
  - Second instance of the same statement failing, cited only for shape: the registered sentence "**Three
    years of trading history is required to classify at all.**" (InsiderExperiment/REGISTRATION.md:258,
    committed `398755b` and never amended) is superseded by the routine-order reversal in `672b343`. That
    change **is** disclosed, dated and reasoned in ADR-008 (DECISIONS.md:226-256); the finding does not rest
    on it.
- **Recomputation:** none required — this is a git-object claim. Inputs: `git diff fbfc74e 672b343 --
  src/insider/config.py`, `git log -S benchmark_id`, `ledgers/evidence.jsonl` timestamps.
- **What would resolve it:** a numbered amendment recording that `benchmark_id` was removed on 2026-08-25 at
  19:11:45, why, what data existed at the time, and that no computed figure depends on it — plus a matching
  correction to "None in force."; or an explicit statement that deleting an unenforced decorative field is
  not "changing a registered value" under the Section 0 rule.
- **Confidence:** HIGH — the diff, the commit date, the absence of the identifier anywhere at `HEAD` and the
  "None in force." line are all direct reads of git objects and the anchored tree.
- **Invalidated by later commits?:** no — `12d9fd3` is both the anchor and the live `HEAD`; there is no
  commit after it and the repository carries a `_CLOSED_DO_NOT_RUN_HERE` marker.
- **Disclosed by the authors?:** no. No ADR, progress entry or registration section mentions `benchmark_id`
  or its removal, and Section 16 asserts the opposite. ADR-012 (DECISIONS.md:356-374) discloses that the
  config-enforcement guard was strengthened during the mutation exercise — the mechanism — but not the
  consequence. The routine-order instance cited above is separately disclosed at DECISIONS.md:226-256.

### AUDIT-C-InsiderExperiment-2
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** Section 15.1, the qualifying-events-by-year table
- **Direction:** neutral (no verdict number depends on it)
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** the by-year table at InsiderExperiment/REGISTRATION.md:603-608, read
  against the headline at InsiderExperiment/REGISTRATION.md:594 —
  > `| 2016 | 262 | 2022 | 502 |`
  > `| 2017 | 406 | 2023 | 505 |`
  > `| 2018 | 524 | 2024 | 410 |`
  > `| 2019 | 457 | 2025 | 363 |`
  > `| 2020 | 717 | 2026 | 99 |`
  > `| 2021 | 297 | | |`
- **Evidence:**
  - The printed table sums to **4,542** against the "**4,585** qualifying events" stated nine lines above at
    InsiderExperiment/REGISTRATION.md:594. n = 11 year cells.
  - `reports/stage_a1/corpus.json` `events_per_year` at the anchor reads 263 / 409 / 531 / 462 / 728 / 298 /
    504 / 508 / 418 / 365 / 99 and sums to **4,585** (re-read from `SNAP/InsiderExperiment/reports/stage_a1/corpus.json`
    2026-09-04). Nine of the eleven cells differ from the printed table and none matches downward.
  - `git show ccc9b13:reports/stage_a1/corpus.json` carries exactly the printed cells (262 / 406 / 524 / …,
    sum 4,542). The correction landed in `cb17046` (2026-08-25T19:11:45−07:00); Section 15 was first written
    in `d8b81f1` (19:11:55), ten seconds later, and the corrected `corpus.json` had been on disk since
    19:05:33. The document therefore transcribes a console output the run had already superseded.
  - Independent rebuild: expanding the 4,585 rows of `var/insider_corpus.db.event` by `entry_session`
    reproduces the JSON cells exactly (UNANCHORED, read 2026-09-04 18:27 UTC).
  - The stale cells propagate: InsiderExperiment/DECISIONS.md:148-149 reads "the corpus shows 717 qualifying
    events in 2020 against 297 in 2021" — the artifact says 728 and 298.
- **Recomputation:** inputs `reports/stage_a1/corpus.json` `events_per_year` (11 cells) and
  `var/insider_corpus.db.event.entry_session` (4,585 rows); method: sum the printed cells, group the event
  rows by year of `entry_session`; results 4,542 printed against 4,585 stored, a shortfall of exactly 43 —
  the count ADR-013 attributes to the composite-natural-key merge; tolerance exact.
- **What would resolve it:** replacing the eleven cells at REGISTRATION.md:603-608 and the two figures at
  DECISIONS.md:148-149 with the post-fix values, or a note beside the table stating it is the pre-fix
  composition and pointing at ADR-013.
- **Confidence:** HIGH — the superseded values are recoverable byte for byte from `ccc9b13` and the corrected
  values reproduce independently from the event store.
- **Invalidated by later commits?:** no — closed repository; `12d9fd3` is the tip.
- **Disclosed by the authors?:** **partly, and this must be said plainly.** ADR-013
  (InsiderExperiment/DECISIONS.md:400-407) discloses the merge defect and names the very figure: "The build
  reported 4,585 qualifying events while the table held 4,542." What is **not** disclosed anywhere is that
  the published Section 15.1 table still carries the pre-fix cells; ADR-013 presents the defect as corrected,
  and in the store it was.

### AUDIT-C-InsiderExperiment-3
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** Sections 17.3 and 15.6, the "what did fail" explanation of the BLOCKED verdict
- **Direction:** neutral — it does not weaken the closure; it slightly *overstates* the concentration
  collapse the closure is attributed to
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "The value-weighted book holds a mean of **71.9 names and behaves like
  29.7 / effective names**, because the heaviest name carries **14.9 percent** of the book and the heaviest
  five carry **33.8 percent**." — InsiderExperiment/REGISTRATION.md:839-841
- **Evidence:**
  - The two figures are computed on **two different books**. 71.909 is `MembershipSeries.mean_width()`
    (InsiderExperiment/src/insider/portfolio/membership.py:46-54), written to `portfolio.json` at
    InsiderExperiment/src/insider/portfolio/build.py:59; it averages `len(book)` over non-empty sessions
    **before** the `not_priced` drop.
  - 29.731282, 0.149323 and 0.337911 are computed at InsiderExperiment/src/insider/portfolio/returns.py:213-217
    on `priced`, the book **after** that drop (`priced = [n for n in book if n in members]`, returns.py:189-190).
    The same drop removes **13,750** name-sessions (`power.json` `dropped_primary.not_priced`).
  - The book that actually produced 29.7, the weight shares and the 49.35 has a mean width of **66.93**:
    `reports/stage_a1/power.json` series[0] `book_width_mean: 66.93`, whose source is `widths.append(len(priced))`
    at returns.py:210. Re-read from SNAP 2026-09-04; the `portfolio.json` row for the same series carries
    `book_width_mean 71.909` and `book_effective_names 29.731282`, which is the pairing the sentence makes.
  - Recomputed from the dispersion store's own `book_width` column: mean **66.92522278186749** over n = 2,581
    sessions (`var/insider_dispersion.db`, UNANCHORED, read 2026-09-04 18:22 UTC).
  - Effect on the stated collapse: the document's ratio is 71.909/29.731 = **2.42×**; the like-for-like ratio
    on the book that produced both numbers is 66.925/29.731 = **2.25×**. The error makes the concentration look
    worse than it is, i.e. it favours the BLOCKED explanation. The verdict itself is untouched — the MDE
    reproduces exactly.
  - The same pairing appears at InsiderExperiment/REGISTRATION.md:749 ("| 126, value-weighted | 71.9 | **29.7** |",
    under a column headed "Names held") and at InsiderExperiment/progress.md:31-32 and :249-250.
- **Recomputation:** inputs `var/insider_dispersion.db` `centered_excess.book_width` for (hold_sessions 126,
  weighting value_weighted), n = 2,581, and the membership series rebuilt from `var/insider_corpus.db.event` ×
  `var/insider_market.db.session`; method: arithmetic mean of each width series; results 66.92522278186749
  (priced) and 71.90895121014215 (pre-drop, which reproduces `corpus.json` `mean_book_width` exactly);
  tolerance 1e-9.
- **What would resolve it:** stating the priced width beside the membership width — "holds a mean of 71.9 names
  of which 66.9 are priced on an average session, and behaves like 29.7 effective names" — or labelling the
  Section 15.6 column "Names in the book before the mid-hold universe drop".
- **Confidence:** HIGH — both figures are recomputed from stored primitives and the two code paths that produce
  them are three lines apart in the same function.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by the authors?:** no. ADR-009 (DECISIONS.md:258-280) discloses the mid-hold drop and its 13,750
  name-sessions, and Section 15.1 correctly labels 71.9 as the corpus-side mean book width. Nothing states that
  the width and the effective-names figure are computed on different books, and Section 17.3 presents them as
  one sentence about one book.

### AUDIT-C-InsiderExperiment-4
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** Section 17.4 and ADR-011, the equal-weighted secondary
- **Direction:** neutral — the true figures make the secondary's book *less* collapsed, not more
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "On the identical names, the equal-weighted book holds **71.9 and behaves
  like / 66.9**, with tracking error of **6.86 percent** and an MDE of **34.29 bp per / month, which would have
  fired DEGRADED**." — InsiderExperiment/REGISTRATION.md:852-854
- **Evidence:**
  - The 6.86 %, the 34.29 and the DEGRADED branch all verify exactly (recomputed TE 6.8556 % and MDE 34.2897;
    20 < 34.2897 ≤ 40 at InsiderExperiment/src/insider/section0.py:62). This finding concerns only the "71.9 and
    behaves like 66.9" pair.
  - For an equal-weighted book the inverse Herfindahl **is** the name count by construction: `_effective_names`
    at InsiderExperiment/src/insider/portfolio/returns.py:118-124 with `raw = np.ones(len(names))` at
    returns.py:101. The effective-names figure for the EW series can therefore only equal the mean **priced**
    width.
  - It does, to six decimals: `reports/stage_a1/portfolio.json[3].diagnostics.book_effective_names` =
    **66.925223** (re-read from SNAP 2026-09-04), and the mean of `book_width` for (126, equal_weighted) in
    `var/insider_dispersion.db` is **66.92522278186749** over n = 2,581. The agreement is forced, not
    coincidental. `power.json` series[3] carries `book_width_mean: 66.93` for the same series.
  - So the equal-weighted book **holds 66.93 names and behaves like 66.93 names**. The stated "71.9 → 66.9"
    implies a ~7 % concentration effect inside an equal-weighted book, which cannot exist.
  - Asserted more strongly at InsiderExperiment/REGISTRATION.md:863 ("Both books hold 71.9 names.") and at
    InsiderExperiment/progress.md:42 and :252-253.
  - The *membership* half of the claim is true: both 126-session rows of `portfolio.json` carry
    `book_width_mean 71.909` and identical `dropped` maps, so the two books do hold the same names. It is the
    pairing of that width with the effective-names figure that is not.
- **Recomputation:** inputs `var/insider_dispersion.db` `centered_excess.book_width` for (126, equal_weighted),
  n = 2,581 (UNANCHORED, read 2026-09-04 18:22 and 18:26 UTC), against
  `reports/stage_a1/portfolio.json[3].diagnostics.book_effective_names`; method: arithmetic mean against the
  stored diagnostic; result 66.92522278186749 against 66.925223; tolerance 1e-6 — they agree.
- **What would resolve it:** restating as "the equal-weighted book prices 66.9 names on an average session and
  behaves like all 66.9 of them, against the value-weighted book's 29.7", which is a sharper statement of the
  same point.
- **Confidence:** HIGH — the identity is forced by the code and confirmed numerically to six decimals.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by the authors?:** no.

### AUDIT-C-InsiderExperiment-5
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** the session-cost record and the ETA-against-actual table
- **Direction:** B (a cost figure is presented as record-backed when the record does not carry it)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "**Cost, measured rather than asserted.** The commit record puts Stage A.1 at
  / about 51 minutes of session wall clock, 18:20 to 19:11, and Stage Z.1 at about / 20 minutes. The Z.1 brief
  records five hours. The commit record cannot confirm / that figure, which presumably counts operator time
  between stages that this / repository does not observe." — InsiderExperiment/progress.md:115-119
- **Evidence:**
  - The eight "Actual" entries in the table at InsiderExperiment/progress.md:198-205 read 5, 10, 4, 4, 14, 20,
    32 and 22 minutes. They sum to **111 minutes** against the 51 claimed at progress.md:115-116 for the same
    stage. n = 8 task rows.
  - The table's own header at InsiderExperiment/progress.md:193-194 says "Timings are wall clock, session start
    18:20 UTC, boundaries taken from commit timestamps where one exists", so the actuals are asserted to
    partition the same interval.
  - The commit record (`git -C <live> log --date=iso-strict`, re-read 2026-09-04 18:45 UTC, n = 7 commits):
    `fbfc74e` 2026-08-25T18:34:56−07:00, `398755b` 18:38:50, `ccc9b13` 18:47:16, `cb17046` 19:11:45, `672b343`
    19:11:45, `d8b81f1` 19:11:55, `12d9fd3` 23:24:15. Wall clock 18:20 → 19:11:55 is **51.9 min**.
  - Three of the eight actuals cannot come from commit boundaries: tasks 5, 6 and 7 claim 20 + 32 + 22 = **74
    minutes** but sit across `cb17046`/`672b343` (identical timestamp, Δ = 0 s) and `d8b81f1` (Δ = 10 s); the
    whole `ccc9b13` → `d8b81f1` interval is 24 min 39 s. Task 4's 14 min also exceeds its commit interval
    `398755b` → `ccc9b13` (8 min 26 s).
  - The Z.1 figure is unsupported in a second, sharper way: **exactly one** commit belongs to Stage Z.1
    (`12d9fd3`, 23:24:15). A single commit has no interior interval, so the commit record supplies **no** Z.1
    duration at all — it can put Z.1 at "about 20 minutes" no more than it can confirm five hours. The only
    interval the record carries across the boundary is `d8b81f1` 19:11:55 → `12d9fd3` 23:24:15 = **4 h 12 min
    20 s**, which is not inconsistent with the brief's five hours.
  - No artifact narrows it: every mtime under `reports/`, `var/` and `ledgers/` is ≤ 2026-08-25 19:10:28 −07:00
    (`mutations.json`; the last ledger append is 19:06:24), so nothing was written during the Z.1 window. That
    is the same fact that makes the "Z.1 changed no result" claim SUPPORTED.
  - The 51-minute A.1 figure is itself only partly from the record: its 18:20 start precedes the first commit
    (18:34:56) and the first ledger record (18:35:18) and comes from progress.md:193, not from any git object.
- **Recomputation:** inputs the eight Actual cells at InsiderExperiment/progress.md:198-205 and the seven commit
  author dates from `git log --format='%h %ad' --date=iso-strict`; method: sum the column, difference consecutive
  commit times, count Z.1 commits; results 111 min against 51.9 min of wall clock, 74 min of claimed task time
  across a 24 min 39 s commit interval, one Z.1 commit and a 4 h 12 min 20 s gap; tolerance ±1 s on the commit
  arithmetic, ±1 min on the column.
- **What would resolve it:** marking the per-task actuals as estimates rather than commit-derived and reconciling
  the column to the 51.9-minute interval it says it partitions; and attributing the 20 minutes to its actual
  source (a session clock or the Z.1 brief) rather than to "the commit record", or stating plainly that the
  record bounds neither figure and that the only observable is the 4 h 12 min gap.
- **Confidence:** HIGH — both sides are direct reads, one from the document and one from git objects, and the
  inference that one commit yields no interval is arithmetic.
- **Invalidated by later commits?:** no — closed repository; a later commit could only add Z.1 boundaries that
  did not exist when the sentence was written.
- **Disclosed by the authors?:** **partly, and the disclosed half is the other one.** The same passage says "The
  commit record cannot confirm that figure" of the **five-hour brief** figure
  (InsiderExperiment/progress.md:117-118) and closes "Both are recorded rather than one being picked"
  (progress.md:119). What is not disclosed is that the 20-minute figure is equally unsupported by the record it
  is attributed to, nor that the document's own ETA table contradicts its own 51-minute figure by more than a
  factor of two.

### AUDIT-C-InsiderExperiment-6
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** Section 15.2, "three facts this table settles"
- **Direction:** neutral (hygiene)
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "The strict ten-percent-owner reading, registered in Section 3.3, cost
  **46,706** / officer-or-director purchases. That is 51 percent of all role rejections and / roughly ten times
  the surviving corpus." — InsiderExperiment/REGISTRATION.md:652-654
- **Evidence:**
  - `reports/stage_a1/corpus.json` `attrition` gives the four role-rejection sub-reasons (re-read from SNAP
    2026-09-04): `filtered_role/tenpercentowner` 46,958; `filtered_role/tenpercentowner_also_titled` **46,706**;
    `filtered_role/roles_other` 32,536; `filtered_role/roles_none` 5,022. Total **131,222**, matching the
    printed funnel row at InsiderExperiment/REGISTRATION.md:623. n = 4 sub-reasons.
  - 46,706 / 131,222 = **35.593 %**, not 51 %.
  - The narrowest defensible denominator — ten-percent-owner rejections only, 46,958 + 46,706 = 93,664 — gives
    46,706 / 93,664 = **49.87 %**, which rounds to 50, not 51.
  - No denominator in the artifact yields 51 %: it would require a base of 91,580.
  - The companion figure in the same sentence verifies: 46,706 / 4,585 = **10.19**, "roughly ten times the
    surviving corpus".
- **Recomputation:** inputs the four `filtered_role/*` keys of `reports/stage_a1/corpus.json`; method: ratio
  against each candidate denominator; results 35.593 % and 49.87 %; tolerance 0.5 pp.
- **What would resolve it:** replacing "51 percent of all role rejections" with "36 percent of all role
  rejections" or "half of all ten-percent-owner rejections", whichever was meant.
- **Confidence:** HIGH — the arithmetic is unambiguous and the artifact is tracked at the anchor.
- **Invalidated by later commits?:** no — closed repository, and the `filtered_role/*` counts are identical in
  the pre-fix `ccc9b13` artifact, so this is not a staleness artifact.
- **Disclosed by the authors?:** no.

### AUDIT-C-InsiderExperiment-7
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** Section 15.4, the `insufficient_history` by-year series
- **Direction:** neutral (hygiene)
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "The front / truncation it causes is visible in the by-year counts: 449
  unclassifiable in / 2016, 257 in 2017, 257 in 2018, falling to 84 by 2023 as the look-back window / fills." —
  InsiderExperiment/REGISTRATION.md:701-704
- **Evidence:**
  - `reports/stage_a1/corpus.json` `unclassifiable_by_year` at the anchor (re-read from SNAP 2026-09-04): 2008 1,
    2012 1, 2014 1, 2015 11, 2016 **449**, 2017 **257**, 2018 **256**, 2019 188, 2020 174, 2021 110, 2022 **296**,
    2023 **84**, 2024 95, 2025 96, 2026 38. Sum **2,057**, matching the prose's own "2,057 transactions carry that
    state" at InsiderExperiment/REGISTRATION.md:701. n = 15 year cells.
  - 2018 is **256**, not 257. `git show ccc9b13:reports/stage_a1/corpus.json` has 2018 = 257; `cb17046` moved one
    transaction from `insufficient_history` to `routine` (attrition 2058 → 2057, 155 → 156), which is exactly the
    ADR-008 correction, and it is the 2018 cell that lost it.
  - The prose is internally mixed: the total (2,057) is post-fix while the 2018 cell (257) is pre-fix.
  - "falling to 84 by 2023" is not what the series does: 2021 is 110 and **2022 is 296**, so the count nearly
    triples before it falls to 84. The 2022 = 296 value is identical in the pre- and post-fix artifacts, so this
    half is not a staleness artifact but a mischaracterization of the stored series.
- **Recomputation:** inputs `reports/stage_a1/corpus.json` `unclassifiable_by_year` (15 cells); method: read the
  cells and sum; results sum 2,057, 2018 = 256, 2022 = 296; tolerance exact.
- **What would resolve it:** correcting 257 → 256 for 2018, and either dropping "falling to 84 by 2023" or
  restating it as "falling to 84 by 2023 apart from a 2022 rebound to 296".
- **Confidence:** HIGH — read directly from the tracked artifact and confirmed against the superseded version in
  git.
- **Invalidated by later commits?:** no — closed repository, anchor is the tip.
- **Disclosed by the authors?:** partly. ADR-008 (InsiderExperiment/DECISIONS.md:245-249) discloses that one
  transaction moved label and asserts the qualifying set and the MDE are unchanged — both of which verify — but
  it does not say which year cell moved, and nothing anywhere discloses the 2022 rebound.

### AUDIT-C-InsiderExperiment-8
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** the scaffold record
- **Direction:** neutral (hygiene)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "`make all` runs clean: ruff, ruff format, mypy strict on 56 files, 106 /
  tests." — InsiderExperiment/progress.md:216-218 (the same count is the commit subject of `672b343`, "test: 106
  tests green, and five registered mutations that fail the right guard")
- **Evidence:**
  - AST enumeration of the tracked test tree at the anchor gives **96** functions named `test_*` across the ten
    `test_*.py` files — `test_absence` 7, `test_cluster` 10, `test_cost` 6, `test_edgar` 7, `test_guards` 23,
    `test_ledger` 5, `test_membership` 9, `test_power` 12, `test_section0` 7, `test_universe_port` 10
    (recomputed from `SNAP/InsiderExperiment/tests/` on 2026-09-04).
  - Two parametrize decorators expand the collection: the 8-case `@pytest.mark.parametrize(("mde","expected"), …)`
    at InsiderExperiment/tests/test_section0.py:16 adds 7, and the 3-case
    `@pytest.mark.parametrize("formation", ["2016-04-01","2021-04-01","2026-07-01"])` at
    InsiderExperiment/tests/test_universe_port.py:87 adds 2. Total collected = 96 + 9 = **105**.
  - Nothing else can add to the collection: there are no test classes (an AST scan for `class` statements in
    `tests/` returns none), `tests/conftest.py` contains only a `sys.path` insertion and no collection hook, and
    InsiderExperiment/pyproject.toml:63-64 sets `testpaths = ["tests"]` with `addopts = "-q --strict-markers"` —
    no `--doctest-modules`.
  - Corroboration from the run's own artifact: `reports/stage_a1/mutations.json` `final_suite` is a pytest
    progress line of **33 dots** padded to 79 columns before `[100%]`. On an 80-column terminal the preceding
    full line holds 72 dots, giving 72 + 33 = **105**.
  - The tracked test tree is byte-identical from `672b343` to the anchor (`git diff --stat 672b343 12d9fd3 --
    tests/ src/ scripts/` is empty), so the claim and the count refer to the same code.
- **Recomputation:** inputs `SNAP/InsiderExperiment/tests/*.py`; method: `ast.parse`, count `FunctionDef` nodes
  whose name starts with `test_`, add `len(elts) − 1` for each `parametrize` decorator's literal case list;
  result 105; tolerance exact. pytest itself was **not** run — the audit venv has no pytest, and installing into
  or running inside an audited repository is out of scope.
- **What would resolve it:** a `pytest --collect-only -q` count run by the author, or correcting 106 → 105.
- **Confidence:** MEDIUM — the AST enumeration is complete for every collection mechanism this suite uses and is
  independently corroborated by the stored progress line, but pytest was not executed, so a collection subtlety
  cannot be ruled out entirely.
- **Invalidated by later commits?:** no — closed repository, and the test tree is unchanged from the commit that
  made the claim.
- **Disclosed by the authors?:** no. `reports/stage_a1/mutations.json` `final_suite` evidences no pass count
  either way — it captured a progress line rather than pytest's summary because `summary_line()`
  (InsiderExperiment/scripts/mutations.py:118-122) fell through to its last-line fallback; the harness's own
  exit-code check (scripts/mutations.py:178-179) is what established that the suite was green.

### AUDIT-C-InsiderExperiment-9
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** ADR-002, the route decision
- **Direction:** neutral (hygiene)
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "They are the SEC's parse of the same XML documents, published free, in / 53
  files totalling about 750 MB." — InsiderExperiment/DECISIONS.md:57-58
- **Evidence:**
  - `ledgers/fetch.jsonl` (684 records, untracked and UNANCHORED, re-read 2026-09-04 18:45 UTC) holds **53**
    `wire` records whose URL contains `form345`, i.e. the 53 quarterly DERA zips. Their `bytes_read` sum to
    **570,492,991 bytes = 570.5 MB (544 MiB)**, not ~750 MB. n = 53.
  - The 2.78 GB the repository reports elsewhere is dominated by a different route: the 53 full-index responses
    account for 2,207,515,405 bytes, the 82 per-filing XML documents 458,435 bytes, the 25 submissions responses
    4,018,868 bytes, and one `company_tickers.json`. The four groups plus the DERA zips sum to the verified
    2,783,280,665 bytes across 214 wire records, with 0 non-200 responses among all 684 — all re-confirmed at
    18:45 UTC.
  - The on-disk cache is exactly 2,783,280,665 bytes across exactly 214 files (`du -sb cache/edgar`, read
    2026-09-04 18:28 UTC), so `bytes_read` is the delivered body size and not an estimate.
- **Recomputation:** inputs `ledgers/fetch.jsonl`, records with `served_from == "wire"` and `"form345" in url`;
  method: sum `bytes_read`; result 570,492,991; tolerance exact.
- **What would resolve it:** correcting "about 750 MB" to "about 570 MB", or stating explicitly if the 750 MB
  refers to the uncompressed content of the zips rather than the download, which the ledger cannot measure.
- **Confidence:** MEDIUM — the download figure is exact, but "750 MB" could plausibly have been intended as an
  uncompressed or published-catalogue figure, neither of which any stored artifact records.
- **Invalidated by later commits?:** no — closed repository. The ledger is untracked and therefore UNANCHORED;
  its mtime (2026-08-25 19:06:24) falls inside the A.1 session window.
- **Disclosed by the authors?:** no.

### AUDIT-C-InsiderExperiment-10
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** the ETA-against-actual table header and the session timeline
- **Direction:** neutral (hygiene)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "Timings are wall clock, session start 18:20 UTC, boundaries taken from commit
  / timestamps where one exists." — InsiderExperiment/progress.md:193-194
- **Evidence:**
  - Every commit in the repository is stamped `−07:00`: `fbfc74e` `2026-08-25T18:34:56-07:00`, `12d9fd3`
    `2026-08-25T23:24:15-07:00` (n = 7 commits, `git log --date=iso-strict`, re-read 2026-09-04 18:45 UTC).
  - The ledgers are stamped in true UTC and are one calendar day later: `ledgers/fetch.jsonl` line 1
    `"recorded_at":"2026-08-26T01:35:18+00:00"` and `ledgers/evidence.jsonl` record 1
    `"recorded_at":"2026-08-26T01:36:26+00:00"` (UNANCHORED, re-read 2026-09-04 18:45 UTC; n = 684 fetch records
    and 14 evidence records).
  - 18:35:18 −07:00 = 2026-08-26T01:35:18Z. The stated "session start 18:20 UTC" is therefore a local (PDT) clock
    time mislabelled as UTC; in UTC the session began 2026-08-26T01:20Z. The same mislabelling carries into the
    "18:20 to 19:11" span at InsiderExperiment/progress.md:116 and into every row of the task table at
    progress.md:196-205.
  - The internal arithmetic is unaffected: 18:20 → 19:11 is 51 minutes in either zone.
- **Recomputation:** inputs the commit author date of `fbfc74e` (−07:00) and `fetch.jsonl` line 1 (`+00:00`);
  method: convert and difference; result: the two clocks differ by exactly 7 h, confirming the commit clock is
  UTC−07:00 and the "UTC" label on 18:20 is wrong; tolerance ±1 s.
- **What would resolve it:** relabelling the session start as local time, or restating it as 2026-08-26T01:20Z,
  so that a later reader comparing the task table against the UTC-stamped ledgers does not find a seven-hour
  discrepancy.
- **Confidence:** HIGH — both clocks are read directly and their offset is exact.
- **Invalidated by later commits?:** no — there is no commit after the anchor.
- **Disclosed by the authors?:** no. The sentence asserts the zone rather than qualifying it.

---

## Sound

What verified cleanly, stated as plainly as the contradictions. A verified claim is as important a
result as a contradicted one, and this repository's closure is supported by its own artifacts.

- **The deciding number.** MDE **49.3543** bp/month recomputed from the 2,581 stored centered values in
  `var/insider_dispersion.db` using the formula at `power/mde.py:38-66` — agrees to the last stored decimal.
  The BLOCKED branch fires correctly against the registered 40 bp ceiling (`config.py:142`,
  `section0.py:62,77`), and the rationale string in `power.json` is byte-identical to the f-string at
  `section0.py:80-85`.
- **Everything the MDE is built from.** TE 9.9933 %, N_eff 2,869.9 from N = 2,581, VIF 0.8993, sd 62.9519 bp,
  autocorrelations ρ1/ρ5/ρ21, the monthly SE 24.6771 — all reproduce. The identity "that tracking error is the
  whole of the 49.35" closes to 1e-3.
- **The whole Newey-West grid.** 50.1903 / 49.3543 / 49.1057 / 49.5319 at lags 5/21/63/126 — all four reproduce
  to 1e-4, and all four are above 40, so the verdict survives every registered bandwidth. VIF < 1 everywhere, so
  the serial-correlation treatment moves the verdict toward GO; the BLOCKED result is not an artifact of it.
- **The three secondary series.** 21-session VW (81.4849), 63-session VW (57.3398) and 126-session EW (34.2897)
  all reproduce exactly, including the DEGRADED branch the EW row would have fired.
- **The corpus and the funnel.** 4,585 events; session coverage **0.9954110898661568** and membership mean width
  **71.90895121014215**, both rebuilt independently from the corpus store crossed with the market store and
  agreeing to full double precision. The eight-row attrition funnel sums to exactly 2,876,095 across its 30
  sub-reason keys, every group sum matches its printed row, and the share column reproduces to 2 dp.
- **The descriptive corpus statistics.** 5.7959 % / 94.2041 % liquid-500 pass rate; 3,350 of 4,585 with the
  10b5-1 box absent (73.064 %); the whole 88-bin lag distribution (p99 230, max 1,988, mean 9.5154, ≤1 day
  51.320 %, ≤2 days 72.999 %, ≤4 days 95.856 %, tail of 91); 209 of 773 clusters rejected by the Johnsen filter,
  confirmed in both the JSON and the store; 2,057 unclassifiable; 13,750 dropped name-sessions at 7.41 %;
  "roughly ten times the surviving corpus" at 10.19.
- **The cost band.** 32/6 = 5.3333 and 100/6 = 16.6667 drags, net band 13.3333 to 34.6667 bp/month — computed by
  `insider.cost`, not asserted, and reproducing exactly.
- **The Section 0.4 floor derivation, in full.** 19.519/39.038 bp, 3.098/6.197 %, 23.44/93.77 names,
  468/1,000/1,874.5 events, 4.2426 % TE and 27.38 bp at 1,000 events, and the +11.8 % from √(2520/2016) — every
  inversion checks out on the registered planning values.
- **The zero-dollar claim.** 214 wire requests, 2,783,280,665 bytes, **zero** non-200 responses across all 684
  ledger records; the on-disk cache equals the wire total byte for byte across exactly 214 files, so nothing was
  fetched twice; and the maximum wire rate observed in any wall-clock second is **7**, inside the registered 8/s.
- **The universe port.** `port.json`'s 2,615 sessions, 124 formations, 1,218 symbols and 2,713,496 bars all match
  `var/insider_market.db` exactly; all 124 formation dates carry exactly 500 members (62,000 rows);
  `backtest/universe.py` still hashes to the recorded `8188eea0…5529`.
- **The validation route.** 53 quarters with an index-to-document ratio between 2.043 and 2.140, 25 XML agreements
  and 0 disagreements, 21 of 25 tickers present — all as stated.
- **The pre-registration ordering.** Lines 1–159 of `REGISTRATION.md` are byte-identical from the first commit to
  the anchor (both `head -159 | sha1sum` to `1091db55b22df21ba45963246d92219267242434`); the diff to the anchor is
  a single purely additive hunk with **zero** deletions. Every one of the eighteen registered literals returns
  exactly one commit under `git log -S` — none was ever edited. The first wire request is 22 seconds after that
  commit; the first power-gate record is 16 minutes later. Section 15 was genuinely empty when Section 0 was
  committed. The value-weighted primary and equal-weighted secondary labels are both present at `fbfc74e`, twelve
  minutes before the first number.
- **The structural guarantee.** The four stored series sum to −1.37e-16, +1.70e-16, −2.92e-16 and −7.52e-17 —
  genuinely centered. `DispersionStats` and `MdeResult` carry no first-moment field. `insider_sealed.db` has
  exactly one reader in the tree (`eval/evaluator.py`, opened `?mode=ro`); `portfolio/returns.py` writes to it and
  never selects from it. The operator-prior slot at `REGISTRATION.md:506` still carries its `[ EMPTY.` marker, so
  `operator_prior()` short-circuits to `None`, and the assistant's 0.12 does not match `_PRIOR_RE` and cannot be
  read as the operator's number.
- **Stage Z.1 changed nothing.** `12d9fd3` touches exactly three markdown files, 408 insertions and **0**
  deletions; every artifact under `reports/stage_a1/` has an mtime at or before 19:10:28, four hours before that
  commit.
- **ADR-008's own arithmetic.** Exactly one transaction moved label between `ccc9b13` and `cb17046`; 4,585 does
  not appear in the diff and all three `power_gate` records carry 49.3543, so the qualifying set and the MDE are
  unchanged, as claimed.
- **Five registered mutations.** All five records in `mutations.json` carry `guard_failed_when_mutated: true` and
  `guard_green_when_restored: true`, each naming a real node in `tests/test_guards.py`.
- **No statistical malpractice was found.** No p-value, no realized test statistic, no confidence interval, no
  multiplicity correction that mismatches its decision rule, no one-sided/two-sided sleight of hand (the tail
  choice is the conservative one), and no promotion of a secondary. The single verdict-bearing gate is a
  conjunction correctly implemented as chained early returns.

**What I would have expected to find if a "closed too early" or "claimed too much" thesis held here, and did
not find:** an MDE that fails to reproduce or that depends on the lag choice; a serial-correlation adjustment
pushed in the direction that manufactures BLOCKED (it runs the other way); a secondary quietly promoted after
its number was seen (the EW row would have fired DEGRADED and is explicitly not promoted, with its
non-verdict-bearing label verifiable in the first commits); registered thresholds edited after measurement (the
pickaxe says no threshold was ever edited); a first moment leaking into the power path; or an operator prior
filled in to unblock Stage B.

---

## Could not be checked and why

1. **`var/insider_sealed.db` was not opened**, by design. The realized alpha remains unread by this audit, as it
   was by the experiment. Consequence: this audit confirms the dispersion store is centered (all four series sum
   to ≤ 3e-16) and that no first-moment field exists on the power path, but it cannot confirm the centered series
   is the centering of *that particular* sealed series. Doing so would require opening the seal, destroying the
   property being audited.
2. **`AiTrader/analysis_bars.db` SHA-256 cannot be re-verified.** The live file is 7,323,656,192 bytes with mtime
   2026-09-03 against `port.json`'s recorded 7,320,629,248; the AiTrader collector has written to it since
   2026-08-25. Its failure to reproduce today is **not** evidence against this repository. The companion hash,
   `backtest/universe.py`, was independently reconfirmed from the anchored AiTrader snapshot.
3. **The three-formation universe port check** (`tests/test_universe_port.py:87`, ADR-004's "500 of 500 members
   reproduced exactly at each") was not re-executed. The stored side was verified — all 124 formations carry
   exactly 500 members — but the comparison against AiTrader's own store would require running repository code
   against an audited tree.
4. **mypy's own file count ("56 files")** cannot be reproduced without running mypy. The three configured roots
   (`pyproject.toml:56`) hold 57 `.py` files (43 + 11 + 3); 56 if `tests/conftest.py` is excluded.
5. **The "on the order of two million Form 4 documents" premise** in ADR-002 is not derivable from any stored
   artifact. `validation.json` gives 2,440,873 Form 4 documents across **all** issuers over the 53 quarters;
   nothing counts documents restricted to universe issuers. The *arithmetic* on the stated premise (2 M / 8 per
   second = 69.44 h, "above 69 hours") is correct.
6. **Every cross-repository figure is READ-only here** — NPDExperiment's 0.0512, 415 days, 6.9378 USD and
   427 → 125.6 effective days; HFExperiment's z 1.668 against a 2.50 bar and 42–66 % tracking error; P26's 19,648
   trades at −1.97 bp; and "eight price-based and signal-based hypothesis families … zero positives". Each needs
   its source repository and none is checkable from anything stored here.
7. **Every literature figure is external.** Cohen–Malloy–Pomorski's 82 bp per month and its "roughly 30 to 40 bp
   on 2008 to 2024" decayed replication, Ozlen–Batumoglu's 70–80 % dissipation, and the 30 % annualized sigma
   used in Section 0.4. The decayed 30–40 bp band is the bar the BLOCKED floor of 40 was placed against
   (`REGISTRATION.md:57-59`), so it is **load-bearing and unverifiable inside this repository**; the whole closure
   is conditional on it. No primary source is stored here.
8. **The "no systemd unit was ever installed" claim** is verifiable only as of today. No unit, timer or cron entry
   matching `insider` exists at 2026-09-04 18:26–18:30 UTC. The host state on 2026-08-25 cannot be reconstructed,
   so the negative is confirmed but its date is not.
9. **The program calibration ledger** ("zero independently formed entries") lives outside this repository.
   Recorded as unverifiable rather than guessed at.
10. **Whether the working tree at 18:36:26 matched `fbfc74e` exactly** cannot be established — git records commits,
    not working trees. The port used only `universe_id`, `bars_start` and `bars_end`, all present at `fbfc74e`,
    and the four `market/` modules each have a one-commit `--follow` history there, so the code that ran is the
    code that was committed unless it was edited and reverted, which git cannot exclude. Separately, the tree at
    the final corpus build (19:05:33) matched no single commit: `cb17046` commits the corrected `corpus.json`
    while still holding the uncorrected `routine.py`, which lands one commit later in `672b343`. Both carry the
    same author timestamp to the second, so this is one commit operation split in two; the anchor `12d9fd3` is
    internally consistent. Recorded, not raised as a finding.
11. **All figures drawn from `var/`, `ledgers/` and `cache/` are UNANCHORED.** Those paths are gitignored and sit
    outside the anchored SHA. Every one was read on 2026-09-04 between 18:20 and 18:45 UTC; every observed mtime
    falls inside the 2026-08-25 18:35–19:10 session window, which is consistent with them being the artifacts the
    anchored reports were written from — corroboration, not proof.

A pointer note below the level of a finding: `REGISTRATION.md:8-9` requires "a numbered amendment in **Section
17**", but the anchored document places Amendments at Section 16 (`REGISTRATION.md:798`) and Closure at Section 17
(`REGISTRATION.md:804`). Lines 1–159 were written at `fbfc74e` before Sections 1–16 existed, so the numbering had
not yet been fixed. Recorded so a reader chasing the amendment rule is not sent to the wrong section.

---

## Live-repo access log

Merged from the LOCATE, VERIFY and PROVENANCE passes and this consolidation pass.

**Purpose of access — the two permitted kinds only.** (1) Git history and provenance: `log`, `show`, `diff`,
`grep <rev>`, `rev-parse`, `branch`. (2) Untracked or gitignored data existing only in the working tree:
`var/insider_corpus.db`, `var/insider_dispersion.db`, `var/insider_market.db` (all opened read-only via
`file:…?mode=ro` URIs), `ledgers/fetch.jsonl`, `ledgers/evidence.jsonl`, `cache/edgar` sizes and file counts only,
and mtimes under `reports/` and `var/`.

**Not opened:** `var/insider_sealed.db` (by design) and `.env`. **No file in any audited repository was opened for
writing. No repository script was copied or executed.** All computation ran under the audit scratchpad with the
audit venv. Outside this repository and read-only, for the boundary claim only: `sha256sum` of
`AiTrader/backtest/universe.py` (from the anchored AiTrader snapshot) and `ls -la` of
`AiTrader/analysis_bars.db`; `news_experiment.db` was not opened and no other AiTrader path was touched. Host
checks for the systemd claim (`systemctl --user list-units/list-timers --all`, `crontab -l`,
`ls ~/.config/systemd/user`, `grep -ril insider /etc/systemd/system`) ran outside every audited repository.

`git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain`, recorded verbatim at each pass
boundary:

| Pass | Before first access | After last access |
|---|---|---|
| VERIFY | 2026-09-04T18:20:55Z — empty output, exit 0 | 2026-09-04T18:30:48Z — empty output, exit 0 |
| PROVENANCE | 2026-09-04T18:21:00Z — empty output, exit 0 | 2026-09-04T18:29:24Z — empty output, exit 0 |
| CONSOLIDATE (this pass) | 2026-09-04T18:45:06Z — empty output, exit 0 | 2026-09-04T18:45:19Z — empty output, exit 0 |

```
```
(Every one of the six reads produced empty output with exit 0 — a clean working tree, unchanged throughout.
**Nothing was modified.**)

Untracked-but-ignored entries present at every read (`git status --ignored --porcelain`): `.env`, `.mypy_cache/`,
`.pytest_cache/`, `.ruff_cache/`, `.venv/`, `_CLOSED_DO_NOT_RUN_HERE`, `cache/`, `ledgers/`, `var/`, and eight
`__pycache__/` directories — an identical set at all three passes. **`_CLOSED_DO_NOT_RUN_HERE` is reported
loudly for the record:** it is excluded via `.git/info/exclude`, is dated **2026-09-02, after the anchor**, records
that a session was opened in this closed repository by mistake, is not an experiment artifact, and is not on the
COMMON_RULES list of pre-existing dirt. It was not created by this audit. No other unexpected entry appeared at
any read.
