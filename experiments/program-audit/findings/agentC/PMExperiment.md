# PMExperiment — Agent C findings (referee and verifier)

Repository: `PMExperiment`
Anchored SHA: `03d16e71dbf25a86c529884662d02136f8e82334` (main, 2026-09-02, closed project) — also the
live `HEAD`, so the anchor is this repository's last commit and nothing below can be overtaken by a
later commit here.
Agent: **C** (referee; no thesis). Consolidated 2026-09-12.

Inputs merged: `findings/agentC/verification/PMExperiment.inventory.md` and `.inventory.json`;
`findings/agentC/verification/PMExperiment.verification.md` and `.claims.json`;
`findings/agentC/provenance/PMExperiment.md` and `.json`.
Snapshot re-read for this pass: `SNAP/PMExperiment/` — **every quote below was re-located in the
snapshot at the line cited during consolidation**, and every load-bearing figure was recomputed
first-hand. Live git objects were re-read read-only on 2026-09-12 02:54–02:55Z for the commit dates,
the `blame` attributions, the `52d39ec` test-count diff, the `98ce2d4` one-line edit, the
`1ba50aa` object counts and the single-commit histories of `admissibility.py` and `docs/BAND.md`;
see **§ Live-repo access log**. Each finding carries a **Consolidation check** bullet recording what
that re-check found. **Nine draft findings entered consolidation, one pair merged, none dropped,
eight leave it.**

**The single fact that shapes this report.** This repository contains **no stored data artifact of
any kind, and never has**: `git log --all --diff-filter=A --name-only` over all 36 commits adds 32
files — ten Markdown documents, five Python modules, seven test files, three `.gitkeep` markers and
seven config files — and **not one** with a `.json`, `.csv`, `.parquet`, `.db`, `.ndjson`, `.txt`,
`.pkl`, `.npy` or `.sqlite` extension. So the verifiable surface is exactly two things: arithmetic
over constants that are themselves registered and pinned to quoted registration sentences by tests,
and the git objects. Both were checked exhaustively and both hold. Everything measured over HTTP is
irreproducible **by construction**, and the repository says so itself: "the raw probe responses were
not retained beyond this report" (`PMExperiment/docs/ACCESS.md:88-89`). That is recorded as
UNVERIFIABLE — neither confirmation nor contradiction.

---

## Summary

Every figure this repository derives for itself reproduces exactly: the BAND-OPEN verdict (0.0585
required against a registered band top of 0.0800), all sixty cells of the Pass-1 band table, both
power bars (475 and 30), the cost floor in both of its written forms, the margins, slacks and
survival counts, the eight stage-by-stage suite totals, and the closing git audit (32 commits, 189
reachable objects at the commit where that audit ran). The registration is genuinely fixed and the
git objects, not the prose, establish it: `registry.py` has zero deleted lines across its three
commits, `band.py`, `power.py`, `admissibility.py` and `docs/BAND.md` have one commit each,
Sections 0–14 of `REGISTRATION.md` are byte-identical across all eleven versions, and the band gate
was defined 79 minutes before it fired. Seven of the fifty-five claim and derived rows are
contradicted; they resolve into six distinct defects and **none moves a verdict**: a divisor
(0.676) that does not match the "two-thirds" premise stated beside it, a blanket "nothing here is
hand arithmetic" sentence covering figures that are hand arithmetic (all of them correct), a
settled-history bracket a month tighter than its own six probes support, a commit message off by one
test, a registration date wrong by one calendar day in the direction that makes the registration look
*later* than it was, and a GO bar labelled as resolving the published band that in fact resolves a
0.02 effect at 50 % power. Twenty of the sixty-seven items could not be checked at all — every HTTP
measurement, six figures imported from other repositories and two outside papers, and three pieces of
registered machinery that never ran because the access gate fired PENDING_ACCESS before any universe
was enumerated. **Eight findings leave consolidation, two at S3 and six at S4, and not one of them
changes the repository's only verdict.**

---

## Verification scoreboard

### Claims

| Status | Count |
|---|---|
| VERIFIED | **34** |
| CONTRADICTED | **7** |
| UNVERIFIABLE | **14** |
| **Total claim + derived rows audited** | **55** |

Split by kind: **28 claim rows** (13 VERIFIED, 2 CONTRADICTED, 13 UNVERIFIABLE) and **27 derived
quantities** (21 VERIFIED, 5 CONTRADICTED, 1 UNVERIFIABLE). Counted separately below and not in that
table: **3 intervals** and **9 test-statistic-shaped quantities**. Across all four kinds: **67 items,
40 VERIFIED, 7 CONTRADICTED, 20 UNVERIFIABLE.**

The seven CONTRADICTED rows are **six distinct defects** — the `475 / 0.676` market count appears
twice, once as a claim row and once as the derived quantity behind it. Each maps to exactly one
finding below (**-1** and **-3** through **-6**, **-8**); the two S3 findings that come from the
provenance pass (**-1**, **-2**) are the date error and the unregistered text-ratio bar.

**MUST-VERIFY claims (the 8 marked ★ in the inventory), with status:**

| # | Claim | Status |
|---|---|---|
| MV1 | "**BAND-OPEN** — a surviving region exists that the permitted subset admits, at entry prices 91–99c held to resolution, requiring **5.85 points** of underpricing … against a registered band whose top is **8.00 points**." (`REGISTRATION.md:409-412`) | **VERIFIED** — `0.02 + 0.01 + 0.03 × 0.95 = 0.0585` exact at 4 dp against `EFFECT_BAND_HI = 0.08`; `band.py:96` applies the strict `<` the rationale registers |
| MV2 | "fee and half-spread alone total **0.0300** on the held route before any FX at all, against a registered band bottom of **0.0200**" (`REGISTRATION.md:456-459`) | **VERIFIED** — `0.02 + 0.01 = 0.03` exactly; strict reading survives at 0/10 buckets on both routes at k = 1, 12, ∞ |
| MV3 | "There are no crossings inside the tradeable price range … p = **−0.3333** … p = **+1.6667** … p = **−1.0000** … p = **+1.0000**" (`docs/BAND.md:212-227`) | **VERIFIED** — all four crossings and the 0.0015 gap reproduce exactly at 4 dp |
| MV4 | the Pass-1 band table: required underpricing by registered decile, R_H and R_X at k = 1, 12, ∞ (`docs/BAND.md:199-210`) | **VERIFIED** — **60 of 60 cells** match at `'%.4f'`, recomputed from the registered constants alone, 0 mismatches |
| MV5 | "route H clears by **4.84** points … falling to **2.15** … route X clears by **2.83** … falling to **0.15**" with slacks 0.00195 / 0.00135 and "a factor of **16**" (`docs/BAND.md:255-265`) | **VERIFIED** — 4.835 → 4.84, 2.835 → 2.83, 0.0215, 0.0015, 0.00195, 0.00135, 0.0215/0.00135 = 15.926 → 16 |
| MV6 | the unit determination: "−0.02 … **−40.0 %** … +0.03 … **+3.16 %** … **0.117** … **0.043**" (`docs/BAND.md:128-137, 151-155`) | **VERIFIED** — every conversion reproduces at the printed precision (+3.1579 → "+3.16"; 0.883; 0.0565; 0.0765) |
| MV7 | the power bars: "GO, MDE ≤ 0.02 \| **≥ 475**"; "stay out of BLOCKED \| **≥ 30**"; "sqrt(v̄) ≈ **0.218**"; "GO needs about **703** markets (475 / 0.676)" (`REGISTRATION.md:120-137`, `:148-150`) | **SPLIT: bars VERIFIED, derived market count CONTRADICTED** — `4 × 0.0475/0.0004 = 475.0` and `= 29.6875 → 30` exactly, `sqrt(0.0475) = 0.21794`; but `475/0.676 = 702.66` while the stated premise "two-thirds" gives **712.5** (finding **-4**) |
| MV8 | the cost floor in its two written forms: "C(p) = 0.04 + 0.01 + 0.03·p … **0.0785**" and "C(p) = 0.05 + 0.03·p … C(0.95) = 0.0785. C(0.05) = **0.0515**." (`REGISTRATION.md:203-212`, `:335-338`) | **VERIFIED** — float-identical in both forms and identical to `power.cost_floor` |

**7 VERIFIED, 0 CONTRADICTED, 1 SPLIT (bars verified, the market count derived from them
contradicted).** Every claim the repository's only verdict rests on — MV1 through MV6 — reproduces
exactly. The one contradicted MUST-VERIFY component is a derived market requirement on a gate that
never fired.

### Intervals

| Metric | Count |
|---|---|
| Intervals audited | **3** |
| Independence doubtful | **0** |
| Recomputed | **0** |
| Conclusion moved | **0** |

**No interval was ever constructed in this repository**, so "recomputed" is 0 for the only honest
reason: there is no sample to recompute one from. The three rows are: **I1**, the verified negative —
no confidence interval, standard error or interval estimate appears anywhere (an independent grep
over all ten documents and all twelve Python files returns exactly two hits, both to machinery that
never ran: `DECISIONS.md:15` and the unfilled Section 8 at `REGISTRATION.md:294`); **I2**, the
registered but never-computed Wilson 95 % lower bound on the sampled tail share
(`REGISTRATION.md:88-95`, `registry.py:33`); and **I3**, Section 8 itself, "*To be registered after
the gate fires*", still unfilled at HEAD.

**Independence, where it would have mattered.** I2's own construction would have supplied
independence — a uniform sample of m = 2,000 settled markets without replacement from an enumerated
universe, seed 20260829, estimand a share over markets — so it is **not** recorded as doubtful; the
finite-population correction is unmentioned and would only have made the bound more conservative.
The gate that bound feeds is the place a clustering problem would have appeared: `n_T` enters
`MDE = z·sqrt(v̄/n_T)` as if the tail cell held `n_T` independent contracts, while contracts nest in
events that resolve together, so the effective n would be below the raw count. The registration knows
this is open — Section 8 names "**the clustering unit**" as something still to be registered
(`REGISTRATION.md:291-295`) — and it was never filled because the gate never fired. **Not raised as a
finding**: nothing was ever computed for it to bias.

**One naming question examined and deliberately not raised.** `WILSON_Z = 1.96` is labelled "the 95%
lower bound" (`registry.py:33`). Read as the lower endpoint of the two-sided 95 % Wilson interval —
the ordinary usage — 1.96 is exactly right; read as a one-sided 95 % bound the conventional constant
is 1.645. The usage is standard and the ambiguity runs in the conservative direction the registration
says it wants ("understating the tail count rather than overstating it", `REGISTRATION.md:93-94`).

### Tests

| Metric | Count |
|---|---|
| Test-statistic-shaped quantities audited | **9** |
| Tail mismatch | **0** |
| Degrees-of-freedom issue | **0** |
| Multiplicity-correction mismatch | **0** |

**Tail.** The only tail anywhere is `z = 2.0 two-sided` (`REGISTRATION.md:99`, `:301`,
`registry.py:9`) and the code applies exactly that (`power.py:45`). 2.0 is a rounded 1.96 and the
rounding *enlarges* the MDE — the conservative direction. There is no registered direction of effect
for it to mismatch: H1 is registered as a two-sided calibration question.

**Degrees of freedom.** Nothing uses a t, χ² or F distribution. Every figure is a normal
approximation on a proportion, so no dof is owed and none is stated. **0 issues.**

**Multiplicity — two places it could have been owed, both clean.** (i) The power gate fires over two
verdict cells and applies no correction; the rule is not a family-wise claim, each cell carries its
own verdict and a split verdict is registered *in advance* as its own reportable finding
(`REGISTRATION.md:113-118`), so per-cell reporting owes none. (ii) The band gate's rule is a union
over ten deciles — exactly the shape where a union correction would be owed *if the comparisons were
statistical*. They are not: all sixty are exact comparisons between registered constants with no
sampling error. The strict (all-must-pass) reading is reported **beside** the existential one rather
than substituted for it (`docs/BAND.md:229-234`), which is the honest way to expose a quantifier.

**No p-value, test statistic or standard error is reported anywhere in this repository** — a negative
re-verified independently by grep in this pass. The one substantive statistical finding (**-3**) is
not a tail, dof or correction defect; it is that the MDE bar the GO row is attached to corresponds to
50 % power.

### Provenance

| Status | Count |
|---|---|
| SUPPORTED | **20** |
| NOT_SUPPORTED | **2** |
| PARTIAL | **9** |
| UNVERIFIABLE | **6** |
| **Total provenance items audited** | **37** |

Split by kind: **25 registration claims** (P1–P25) — 13 SUPPORTED, 5 PARTIAL, 1 NOT_SUPPORTED, 6
UNVERIFIABLE — and **12 parameter/gate/rule changes made after the first measurement existed**
(C1–C12) — 7 SUPPORTED, 4 PARTIAL, 1 NOT_SUPPORTED.

**The pre-registration guarantee verifies, and it verifies by plumbing rather than by reading.**
`pmexperiment/registry.py` has three commits (`9080186` +49, `9b4bd4f` +9, `f789079` +8) and **zero
deleted lines across all three**; `band.py`, `power.py`, `admissibility.py` and `docs/BAND.md` have
**one commit each**; SHA-256 of the whole Sections 0–14 region of `REGISTRATION.md` is identical at
**all eleven versions** from `9080186` to HEAD, as is Section 16's original paragraph. No bar,
threshold, horizon, universe bound, z-value, n target or cost figure in this repository was ever
edited after it was first committed — an exhaustive deletion sweep across all 36 commits returns no
removed line carrying one. The band gate was defined in `f686036` (2026-08-29T18:05:26Z) and fired in
`32dc10a` (19:24:06Z), **79 minutes later**, with the FX constant landing at 19:15:55Z and the
Amendment 4 text that cites it 86 seconds after that — a lag the repository discloses and gets right
itself (`DECISIONS.md:304-307`). The operator's prior enters the repository at closure, in the
operator's own logged Stage E prompt (`2006ae6`, 2026-09-02T09:23:41Z), and every document that
mentions it says it was **not** pre-registered.

The two NOT_SUPPORTED items are P2 (finding **-1**, the one-day date error) and C9 (finding **-7**,
the single in-place edit above the amendment line). The nine PARTIAL items are: P1 (commit half
exact, ordering half resting on the session log alone), P11 (substance verifies, literal sentence
does not — **-7**), P15 (`data/raw/` never existed, so Section 14's reproducibility clause is
**vacuous rather than violated**), P18 (`LICENSE` "17 lines" is the non-blank count; 21 physical),
P24 (`test_registry.py` pins 17 of 18 constants; the eighteenth is pinned in two other test files, so
the guarantee exists and only its attribution to one file is over-broad), and C1, C2, C3 (the three
Amendment 1–3 changes, each amended, numbered, reasoned and carrying its data — failing only on the
stated date, **-1**) and C7 (the text-ratio bar, **-2**).

### Merge and de-duplication record

| Draft | Origin | Disposition |
|---|---|---|
| DRAFT-P-1 | provenance §3 | **merged** with DRAFT-V-5 → **AUDIT-C-PMExperiment-1** |
| DRAFT-V-5 | verification §5 | **merged** with DRAFT-P-1 → **-1** |
| DRAFT-P-3 | provenance §3 | → **-2**, unchanged in substance |
| DRAFT-V-6 | verification §5 | → **-3**, unchanged |
| DRAFT-V-1 | verification §5 | → **-4**, unchanged |
| DRAFT-V-2 | verification §5 | → **-5**, unchanged |
| DRAFT-V-3 | verification §5 | → **-6**, unchanged |
| DRAFT-P-2 | provenance §3 | → **-7**, unchanged |
| DRAFT-V-4 | verification §5 | → **-8**, unchanged |

**Nine drafts in, one merge, eight findings out. Nothing was dropped.** All nine carry a verbatim
quote that re-locates in `SNAP/PMExperiment/` at the line cited (or, for **-8**, in an immutable git
commit object re-read in this pass), and all nine carry a figure that recomputed here. **No drop is
recorded because none was warranted.**

One reconciliation was required. **Severity of -1.** The verification draft graded the one-day
registration date error **S4** (hygiene); the provenance draft graded it **S3**. Resolved to **S3**:
the date is carried by eight separate statements across four files and it labels the registration of
the **only gate this repository ever fired**, so it is a stale figure on a load-bearing record rather
than decoration — even though the true date is a day *earlier*, which strengthens rather than
weakens the ordering claim. Class (`PROVENANCE`), label (`DERIVED`) and direction (neutral) agreed
between the two drafts and are unchanged. The provenance draft's evidence is the fuller of the two —
eight quoted statements against the verification draft's five — and is carried forward whole, with
the verification draft's Amendment-4 ordering oddity retained as a corroborating bullet.

---

## Findings

Eight. Ordered by descending severity. **None of them changes the registered verdict**, and each says
so explicitly.

**Schema note on `Direction`.** COMMON_RULES enumerates two directions, A (closed too early) and B
(claimed too much). Findings **-1**, **-2**, **-5**, **-6**, **-7** and **-8** are recorded as
`neutral`, which is outside that enumeration. This is a deliberate deviation and is flagged as such:
each is a provenance or hygiene defect whose corrected reading moves the repository's position in
*neither* direction — in **-1** the correction makes the registration *earlier*, i.e. it strengthens
the authors' own claim — and forcing A or B on them would assert a direction the evidence does not
support. Where a direction does apply it is given: **-3** and **-4** are B.

### AUDIT-C-PMExperiment-1
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the stated registration date of Amendments 1, 2 and 3, of the second
  ADR-006, the second ADR-007 and ADR-008, of `HYPOTHESES.md`'s venue-split amendment and of
  `progress.md` Entry 3 — i.e. the recorded date of the commit that registered the fee-versus-edge
  band gate, this repository's only fired verdict.
- **Direction:** neutral — the true registration is one day **earlier** than stated, so the ordering
  claim ("registered before it fired") is strengthened, not weakened.
- **Class:** PROVENANCE
- **Severity:** S3 — a stated figure on a load-bearing provenance record is stale/wrong; no
  conclusion depends on it
- **Label:** DERIVED (git objects)
- **Claim challenged (verbatim):** "**Made 2026-08-30, before any statistic relating a price to an
  outcome exists.**" — PMExperiment/REGISTRATION.md:667; "**Made 2026-08-30.** A new gate, ordered
  ahead of the power gate, because it is" — PMExperiment/REGISTRATION.md:707; "**Made 2026-08-30.** A
  deliberate scope change, recorded rather than allowed to" — PMExperiment/REGISTRATION.md:751;
  "**Status:** accepted, 2026-08-30." — PMExperiment/DECISIONS.md:140, :160, :180; "## Amended
  2026-08-30 — the venue split, and what H1 now means" — PMExperiment/HYPOTHESES.md:87; "## Entry 3 —
  amendments 1 to 3: venue, fee band, scope — 2026-08-30" — PMExperiment/progress.md:202
- **Evidence:**
  - All eight statements landed in **one commit**, `f686036ac2cab96b7c451c23a48c53d2bbb8431a`, whose
    author date and committer date are both **2026-08-29T11:05:26−07:00 = 2026-08-29T18:05:26Z**.
    Re-read in this pass: `git show -s --format='%ad %cd' --date=iso-strict f686036` (live repo,
    2026-09-12T02:55Z). **No timezone reachable from −07:00 places 18:05:26Z on 2026-08-30.**
  - `git blame -L` at the anchor attributes `REGISTRATION.md:667`, `:707`, `:751` and
    `DECISIONS.md:140`, `:160`, `:180` to `f686036` — all six re-confirmed in this pass. The wrong
    date was therefore written at the time, not introduced by a later edit.
  - **The repository's own record contradicts it twice more.** The next commit, `e2d8f10`
    (2026-08-29T19:07:37Z), logs Entry 4 as "**Logged 2026-08-29T19:08Z, per standing rule 1**"
    (PMExperiment/progress.md:248-249) — a *later* event correctly dated 08-29. And ADR-009/ADR-010,
    committed 77 minutes after `f686036` in `34307b6` (2026-08-29T19:22:44Z), are dated "**Status:**
    accepted, 2026-08-29." The register therefore reads, in document order, 08-30 → 08-29 → 08-29.
  - **The internal oddity this produces:** Amendment 4 (`4d75f66`, 2026-08-29T19:17:21Z) is dated
    "**Made 2026-08-29**" (PMExperiment/REGISTRATION.md:783), so as the documents read, Amendment 4
    was made a day *before* the Amendment 2 it operates under.
  - **Every other date in the repository is right.** Amendment 5 (`f789079`, 2026-08-30T03:34:00Z)
    says 08-30 ✓; Amendment 6 (`1b3124e`, 03:40:52Z) says 08-30 ✓; Amendments 7/8/9 and ADR-016…021
    (2026-09-02, 09:31:26Z–09:50:29Z) say 2026-09-02 ✓. The `f686036` block is the sole exception in
    36 commits — which is what makes it an omission rather than a convention.
  - This is the exact error class the repository names and corrects elsewhere: "**Entry 6 states it
    was logged at 2026-08-29T19:32Z. That figure is wrong.** It was extrapolated … rather than read
    from the clock" — PMExperiment/progress.md:652-656 — under the principle "**a timestamp inferred
    from a previous timestamp is documented, not measured**" (PMExperiment/progress.md:660-662) and
    standing rule 4, "**Measured beats documented.**" (PMExperiment/CLAUDE.md:25).
- **Recomputation:** none required — a date comparison. Inputs: `git show -s --format='%ad %cd'
  --date=iso-strict f686036` and `git blame -L <n>,<n> 03d16e7 -- <file>` (live repo, read-only,
  2026-09-12T02:55Z) against the eight quoted lines in `SNAP/PMExperiment/`. Method: compare the
  stated calendar date to the commit's author date in UTC and in −07:00. Result: stated 2026-08-30,
  actual 2026-08-29 in both. Tolerance: exact to the calendar day.
- **What would resolve it:** an appended, dated correction in `progress.md` in the shape Entry 6.1
  already uses, recording that Amendments 1–3, the second ADR-006/007, ADR-008, the `HYPOTHESES.md`
  venue-split amendment and Entry 3 were made at 2026-08-29T18:05:26Z and that the recorded
  2026-08-30 was inferred rather than read. **No registered value needs to change.**
- **Confidence:** HIGH — author and committer dates are immutable git object fields and the eight
  document lines are in that same commit's tree.
- **Invalidated by later commits?:** no — `03d16e7` is the anchored HEAD and the final commit;
  `f686036`'s object cannot change and nothing after it corrects the date.
- **Disclosed by authors?:** **no.** The repository corrects an analogous timestamp error at
  PMExperiment/progress.md:650-666 and nowhere mentions this one; PMExperiment/progress.md:511-512 in
  fact repeats it, describing the two ADR-006/007 pairs as coming from "the **2026-08-29 and
  2026-08-30** sessions" when git dates both sessions to 2026-08-29 (07:53:10Z and 18:05:26Z).
- **Why it decides nothing:** `f686036` (18:05Z) precedes the band verdict `32dc10a` (19:24:06Z), so
  "registered before it fired" is verified by the objects regardless of the calendar label — and the
  correction moves the registration *earlier*, i.e. in the direction that strengthens it.
- **Consolidation check:** re-verified first-hand. `f686036` author = committer =
  `2026-08-29T11:05:26-07:00`; `blame` returns `f686036ac2cab96b7c451c23a48c53d2bbb8431a` for all six
  `REGISTRATION.md`/`DECISIONS.md` lines; all eight quotes re-located in `SNAP` at the lines cited;
  `4d75f66` = 19:17:21Z, `32dc10a` = 19:24:06Z, `f789079` = 2026-08-30T03:34:00Z, `1b3124e` =
  03:40:52Z all re-read. **No correction.** Merged from DRAFT-P-1 (evidence carried whole) and
  DRAFT-V-5 (Amendment-4 oddity retained); severity reconciled S4/S3 → **S3**.

### AUDIT-C-PMExperiment-2
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** `MIN_DOCUMENT_TEXT_RATIO = 0.05`, the bar separating a readable
  document from a client-rendered shell, which decides whether a permission claim is ADMISSIBLE or
  falls to UNMEASURED under ADR-012.
- **Direction:** neutral — the bar fails closed (toward UNMEASURED) and was non-binding on every
  recorded verdict, so no closure and no positive in this repository rests on it.
- **Class:** PROVENANCE
- **Severity:** S3 — a process gap on a registered-value rule; capped here because the authors
  disclose the derivation themselves (see **Disclosed**)
- **Label:** DERIVED (git objects + code)
- **Claim challenged (verbatim):** "**Do not tune a filter to increase a sample.** Register it, then
  report what it yields. The sample it costs is a first-class output." —
  PMExperiment/CLAUDE.md:36-37 — read against "Changing a registered value now requires a numbered
  amendment appended to Section 17, carrying its own evidence." — PMExperiment/REGISTRATION.md:9-10
- **Evidence:**
  - The bar is set **from** a measurement rather than registered ahead of one, and the code says so:
    "The one client-rendered page this repository has measured sets this bar. `docs/ACCESS.md`
    records `polymarket.com/tos` returning HTTP 200 with a 217 KB body that stripped to 1,354
    characters of text — a text share near 0.6 % … A plain or lightly marked-up document sits far
    above 5 %; an app shell sits far below it." — PMExperiment/pmexperiment/admissibility.py:39-43,
    with `MIN_DOCUMENT_TEXT_RATIO: float = 0.05` at PMExperiment/pmexperiment/admissibility.py:49.
  - **Ordering, from git.** The measurement it is calibrated from was recorded in Stage C on
    2026-08-30 (PMExperiment/docs/ACCESS.md:125-126, committed `1b3124e` 2026-08-30T03:40:52Z). The
    bar was committed **47 minutes later** (47 min 13 s), in `b67fc84` at **2026-08-30T04:28:05Z**
    (re-read in this pass: `git log --follow -- pmexperiment/admissibility.py` returns **exactly one
    commit**, `b67fc84`, `2026-08-29T21:28:05-07:00`). It was applied to the three Stage D licence
    candidates in `7b5a751` at 06:22:49Z.
  - **The text-ratio bar appears nowhere in `REGISTRATION.md`.** grep over the registration for
    `text ratio`, `text share` and `client-render` returns **zero hits**. The string `0.05` does
    occur there, on seven lines (:32, :33, :42, :43, :335, :338, :844), but every one of them is
    something else — the precedent repositories' quoted MDE and effect band ("0.0512", "0.01 to
    0.05"), the cost model's fixed term (`C(p) = 0.05 + 0.03·p`, `C(0.05) = 0.0515`) or the
    `0.03 × 0.05` FX slack — and **none of them is this bar**. The dated ADR that records the rule —
    ADR-012, "**Status:** accepted, 2026-08-30" at PMExperiment/DECISIONS.md:346 — names the three
    required elements (`clause`, `effective_date`, `fetch_date`) and **no numeric bar**. So the bar
    exists in code with a dated commit and a disclosed rationale, but in no numbered amendment.
  - **It bound nothing.** The repository measured the same document two ways and recorded both: "On
    the same retained Dune body, the verification pass measured **18.05 %** text and this session's
    own tag-stripping measured **67.98 %**. Both clear the 5 % bar and the classification is
    unchanged" — PMExperiment/docs/LICENCES.md:77-79. No Stage D verdict turned on the ratio.
- **Recomputation:** none — an ordering and presence check. Inputs: `git log --follow --
  pmexperiment/admissibility.py` and `git log --follow -- docs/ACCESS.md` (live repo, read-only,
  re-run 2026-09-12T02:55Z); `grep` over `SNAP/PMExperiment/REGISTRATION.md` for `text ratio`, `text
  share`, `5 %`, `client-rendered`. Result: bar committed 2026-08-30T04:28:05Z, after the
  2026-08-30T03:40:52Z measurement that sets it, and absent from the registration. Tolerance: exact.
- **What would resolve it:** a numbered Section 17 amendment recording the 5 % bar, the measurement
  it was read off, the date and the direction of error — the treatment Amendments 4 and 5 give the FX
  turnover and the volume floor; or an explicit statement that ADR-012's numeric threshold is
  deliberately held in code and outside the registration, with the reason.
- **Confidence:** MEDIUM — the commit ordering and the absence from the registration are certain;
  whether a bar deciding ADMISSIBLE vs UNMEASURED counts as a "filter" under standing rule 9, as
  opposed to a procedural admissibility test, is a reading of the rule rather than a measurement.
- **Invalidated by later commits?:** no — `admissibility.py` has one commit and `03d16e7` is the
  anchored HEAD.
- **Disclosed by authors?:** **yes, substantially — and this finding is capped at S3 for that
  reason.** The derivation from the Polymarket shell measurement, and the direction of error it
  introduces, are stated in full by the authors at
  PMExperiment/pmexperiment/admissibility.py:39-48; the bar's method-dependence is recorded by them
  under the heading "**A limitation of the text-ratio bar, found by using it.**" at
  PMExperiment/docs/LICENCES.md:76-82, which also records that the classification is unchanged. What
  is **not** disclosed anywhere is only that the number sits in no numbered amendment. This is a
  process gap, not a discovery about any verdict.
- **Why it decides nothing:** both extraction methods clear the bar and the classification is
  unchanged by the authors' own measurement; every Stage D verdict stands either way.
- **Consolidation check:** re-verified first-hand. `admissibility.py` has exactly one commit
  (`b67fc84`, 2026-08-30T04:28:05Z); `MIN_DOCUMENT_TEXT_RATIO: float = 0.05` re-located at
  `SNAP/PMExperiment/pmexperiment/admissibility.py:49` with the docstring at :39-48; the
  `CLAUDE.md` quote re-located and its line span **corrected from :36 to :36-37** (the sentence wraps
  across two lines); the `docs/LICENCES.md` quote re-located and its span **corrected from :76-79 to
  :77-79** for the quoted sentence (the authors' disclosure block runs :76-82). Substance
  unchanged.

### AUDIT-C-PMExperiment-3
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** Section 0.3 / Section 9, the power gate — the GO row and the tail-count
  bar it is attached to.
- **Direction:** B (claimed too much)
- **Class:** STATISTICAL
- **Severity:** S4 — it would be S2 had the gate ever fired; no verdict in this repository depends on
  it, because no cell was ever built
- **Label:** DERIVED (code + recomputation)
- **Claim challenged (verbatim):** "| **GO** | MDE ≤ 0.02 | the design **resolves the entire
  published band**; Stage B is authorized for that universe against the registered target |" —
  PMExperiment/REGISTRATION.md:110 — read against its own bar, "| GO, MDE ≤ 0.02 | **≥ 475** |" —
  PMExperiment/REGISTRATION.md:128
- **Evidence:**
  - The estimator, as coded: `return registry.Z_CRITICAL * math.sqrt(mean_dispersion / tail_count)` —
    PMExperiment/pmexperiment/power.py:45, with `Z_CRITICAL: float = 2.0` —
    PMExperiment/pmexperiment/registry.py:9; as registered: "MDE = z · sqrt(v̄ / n_T), with z = 2.0
    two-sided" — PMExperiment/REGISTRATION.md:301.
  - **There is no power term anywhere.** grep over all ten documents and all twelve Python files for
    `z_beta`, `z_β`, `80 %`, `80%`, `50 %`, `power of`, `statistical power`, `1 − β`: **zero hits**.
    `z·SE` is the smallest effect that would reach two-sided significance when the estimate lands
    exactly on its own expectation — i.e. at **50 % power** — not the smallest effect a design would
    reliably detect, which is `(z_{α/2} + z_β)·SE`.
  - The planning inputs are stated and verify: `v̄ = 0.0475` and `sqrt(v̄) ≈ 0.218` —
    PMExperiment/REGISTRATION.md:120-123 (recomputed here: 0.0475 and 0.2179449).
  - The bar itself verifies exactly and is **not** what is challenged: `2.0² × 0.0475 / 0.02² =
    475.0` and `2.0² × 0.0475 / 0.08² = 29.6875 → ≥ 30`, with `tests/test_power.py` pinning the
    verdict map at n = 475/474/30/29/0 — all five boundaries reproduce.
- **Recomputation:** inputs `REGISTRATION.md:128` (n_T = 475), `:122-123` (v̄ = 0.0475) and
  `pmexperiment/power.py:45` (the estimator). Method: `SE = sqrt(v̄/n)`; power `= 1 − Φ(z − δ/SE)`
  with `δ = 0.02`; inverted bar `n = (z_{α/2} + z_β)² v̄ / δ²` via `scipy.stats.norm`. Results, re-run
  in this pass: **SE = 0.010000 exactly at n = 475**, so **power = 0.5000** at z = 2.0 (0.51595 at
  z = 1.96); a bar that resolves a 0.02 effect at the conventional **80 %** power is **n_T = 959**
  (z = 2.0) or **933** (z = 1.96), **2.02× the registered 475**; at 90 %, 1,279 / 1,248. Tolerance:
  power to 4 dp, n to 1 contract.
- **What would resolve it:** stating the power level the bar is set at — "the smallest effect that
  would reach significance at 50 % power" is an accurate description of what the gate computes — or
  raising the bar to the 80 %-power figure. Second-order consequence: finding **-4**'s market
  requirement is 475 divided by a tail share, so the same doubling carries through to it.
- **Confidence:** HIGH on the arithmetic; MEDIUM on its importance, since no cell was ever built, no
  dispersion was ever measured and the gate never fired on any venue.
- **Invalidated by later commits?:** no — `power.py`, `registry.py` and Sections 0–14 of
  `REGISTRATION.md` are unmodified at the anchor and `03d16e7` is the final commit.
- **Disclosed by authors?:** **no** — the registration states no power level anywhere, so it does not
  misstate one; what it does is attach the word "resolves" to a bar that misses a real 0.02 effect
  half the time. The form is inherited explicitly — "This repository follows Insider: the gate is
  committed before the measurement it judges" (PMExperiment/REGISTRATION.md:44-49) — so the same
  arithmetic is worth checking in InsiderExperiment and NPDExperiment, whose MDE figures (49.35 bp,
  0.0512) are quoted here as the motivating precedents.
- **Why it decides nothing:** the access gate fired PENDING_ACCESS before any universe was
  enumerated, so `power.py` has no caller anywhere in the history and no MDE was ever evaluated on a
  real cell.
- **Consolidation check:** re-verified first-hand with my own `scipy` run: SE = 0.01 exactly at
  n = 475, power = 0.500000 at z = 2.0 and 0.515953 at z = 1.96; 80 %-power n = 958.88 → **959**
  (z = 2.0) and 932.08 → **933** (z = 1.96); 90 % → 1,279 / 1,248; `4 × 0.0475/0.0004 = 475.0` and
  `= 29.6875`; `sqrt(0.0475) = 0.21794494717703367`; `MDE(100) = 0.04358898943540673`. Both quotes
  re-located in `SNAP` at `REGISTRATION.md:110` and `:128`. **No correction.**

### AUDIT-C-PMExperiment-4
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** Section 0.5, the access gate — clause 3's derived market requirement.
- **Direction:** B (claimed too much — the requirement is stated 10 markets lower than its own
  premise supports)
- **Class:** ARITHMETIC
- **Severity:** S4 — the registered floor is 1,000, which exceeds both candidate figures, and the
  gate never fired
- **Label:** DERIVED
- **Claim challenged (verbatim):** "At the published two-thirds tail share, GO needs about 703
  markets (475 / 0.676); the floor of 1,000 leaves margin for a lower realized share." —
  PMExperiment/REGISTRATION.md:148-150
- **Evidence:**
  - The premise, in the same registration: "The published benchmark (Section 3) reports two-thirds of
    its 313,972 contract prices in the 1–10c and 90–99c bands, so the unrestricted universe reaching
    475 tail contracts is expected." — PMExperiment/REGISTRATION.md:132-134.
  - The numerator verifies: "| GO, MDE ≤ 0.02 | ≥ 475 |" — PMExperiment/REGISTRATION.md:128 —
    reproduces exactly as `2.0² × 0.0475 / 0.02² = 475.0`.
  - **`0.676` occurs exactly once in the entire snapshot** (grep over all files, n = 1 hit, that
    line). It is defined nowhere, attributed to nothing, and pinned by no test.
  - Two-thirds and 0.676 are not the same divisor: they differ by 10 markets in the requirement.
- **Recomputation:** inputs `REGISTRATION.md:128` (475) and `:132-134` (two-thirds); method:
  division; results `475 / 0.676 = 702.663 → 703` (so the printed quotient is internally correct),
  `475 / (2/3) = 712.5`, `475 / 0.667 = 712.144`. Tolerance ± 1 market. Script:
  `scratchpad/work/agentC-PM-verify2/power_check.py`; re-run independently in this pass.
- **What would resolve it:** the tail share the benchmark actually reports, to three decimals — an
  external figure this repository never quotes — or one sentence saying where 0.676 came from. If the
  benchmark really reports 67.6 %, the sentence's own word "two-thirds" is the loose half and the
  arithmetic is right.
- **Confidence:** HIGH — the arithmetic is unambiguous; the only open question is which of the two
  numbers the outside paper supports, and the repository quotes neither.
- **Invalidated by later commits?:** no — Sections 0–14 of `REGISTRATION.md` are byte-identical from
  `9080186` to the anchor (SHA-256 of that region is stable across all eleven later versions), and
  the project closed on 2026-09-02.
- **Disclosed by authors?:** **no** — neither the divisor nor the discrepancy is mentioned anywhere.
- **Why it decides nothing:** the registered access floor is **1,000** markets, which exceeds both
  703 and 713, and the gate never fired — Stage C recorded PENDING_ACCESS before any enumeration.
- **Consolidation check:** re-verified first-hand: `475/0.676 = 702.662721893491`,
  `475/(2/3) = 712.5`, `475/0.667 = 712.143928`. Both quotes re-located in `SNAP` at
  `REGISTRATION.md:148-150` and `:132-134`. **No correction.**

### AUDIT-C-PMExperiment-5
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** `docs/BAND.md`, the provenance sentence that opens the band evidence.
- **Direction:** neutral — pure hygiene; **every figure the sentence covers recomputes exactly**.
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED (code + grep)
- **Claim challenged (verbatim):** "Every figure is computed by `pmexperiment.band` and pinned by
  `tests/test_band.py`, so nothing here is hand arithmetic." — PMExperiment/docs/BAND.md:8-9
- **Evidence:**
  - `pmexperiment/band.py` is 135 lines, read in full: it has **no solver for a crossing price** and
    **no probability-gap ↔ percent-return conversion**. Its public surface is `fee_borne`, `fx_cost`,
    `required_underpricing`, `band_top_exceeds_requirement`, `band_bottom_exceeds_requirement`,
    `bucket_midpoint`, `surviving_buckets`, `is_band_empty` —
    PMExperiment/pmexperiment/band.py:46-135.
  - grep over `pmexperiment/` and `tests/test_band.py` for `0.3333`, `1.6667`, `3.16`, `0.117`,
    `0.883`, `0.043`, `-40`, `0.077`: **zero hits**.
  - `tests/test_band.py` holds 14 test functions and **never opens `docs/BAND.md`**; the only tests
    that read that document are three in `tests/test_honesty.py:183-195`, `:208-216` and `:241-245`,
    and what they pin **in that document** is the strings `BAND-OPEN`, `0.0585`, `0.0785`, `0.0300`,
    `313,972` and three sentence fragments ("absolute probability points, not percent realized
    return", "No venue was read", "Zero dollars spent") — not the Task-2 table and not the crossing
    points.
  - **The document contradicts the sentence twice itself:** "### The crossing points, **stated rather
    than inferred**" — PMExperiment/docs/BAND.md:212 — and "Full derivation in DECISIONS.md ADR-009"
    for the unit determination — PMExperiment/docs/BAND.md:123-124 (ADR-009 at
    PMExperiment/DECISIONS.md:208).
- **Recomputation:** I recomputed every hand-derived figure the sentence over-claims for: the four
  crossing prices (−0.3333, +1.6667, −1.0000, +1.0000), the six unit-determination cells (−0.02,
  −40.0 %, +0.03, +3.16 %, 0.117, 0.043), the exploitable NO entry 0.883 with its two costs (0.0565,
  0.0765) and the 60-cell Pass-1 table. **All reproduce exactly** (tolerance 4 dp on prices and
  costs, 2 dp on percentages). Script: `work/agentC-pm-verify/recompute.py`.
- **What would resolve it:** replacing "every figure" with the accurate scope — the band table, the
  margins, the slacks and the survival counts are machine-computed and machine-pinned; the crossing
  points and the unit-determination table are hand arithmetic, correct, and derived in ADR-009.
- **Confidence:** HIGH — the module and the test file were read in full and the grep is decisive.
- **Invalidated by later commits?:** no — `docs/BAND.md` has **exactly one commit** in its entire
  history (`34307b6`, 2026-08-29T19:22:44Z, re-confirmed in this pass) and is unmodified at the
  anchor.
- **Disclosed by authors?:** **partly** — PMExperiment/docs/BAND.md:212 ("stated rather than
  inferred") and :123-124 (the ADR-009 pointer) disclose the derivation route for exactly the figures the
  blanket sentence at :8-9 mis-describes. The finding is that the two statements cannot both be true,
  not that a number is wrong.
- **Why it decides nothing:** the sentence is a provenance claim about figures that are all correct;
  the verdict's own number (0.0585) *is* machine-computed and machine-pinned.
- **Consolidation check:** re-verified first-hand. All three quotes re-located in `SNAP` at
  `docs/BAND.md:8-9`, `:212` and `:123-124`. `git log --follow -- docs/BAND.md` returns one commit,
  `34307b6` (`2026-08-29T12:22:44-07:00`). **No correction.**

### AUDIT-C-PMExperiment-6
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** Stage A Task 1, the keyless settled-history depth measurement.
- **Direction:** neutral — if anything it cuts *against* the repository's own closure, by claiming
  **more** retrievable history than the probes establish.
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ (the defect is visible entirely within the document's own sentence; no data or git
  object was needed to find it, and none exists that could settle it)
- **Claim challenged (verbatim):** "| settled-history depth | earliest retrievable settled close sits
  **between 2024-01-01 (empty page) and 2024-05-31 (present)**, bracketed by `max_close_ts` probes at
  2021-08-01, 2022-01-01, 2023-01-01, 2024-01-01 (all empty) and 2024-07-01, 2025-01-01 (both
  non-empty) | 2026-08-29 |" — PMExperiment/docs/ACCESS.md:72
- **Evidence:**
  - The six probes listed in that same cell bracket the earliest retrievable close to
    **[2024-01-01, 2024-07-01]**. **2024-05-31 is not one of the six probe dates and is not implied
    by them**; it is a full month tighter than the stated method supports.
  - The endpoint is restated **six more times — seven occurrences in all** — and six of the seven
    attribute it to the probe count and to nothing else: "between 2024-01-01 and 2024-05-31
    (bracketed by single-page probes, **n = 6 probes**)" — PMExperiment/REGISTRATION.md:391;
    "**n = 6 bracketing probes**" at PMExperiment/REGISTRATION.md:539,
    PMExperiment/report.md:34 and PMExperiment/progress.md:43; "(n = 6" at
    PMExperiment/docs/ACCESS.md:320; and without the probe count at
    PMExperiment/DECISIONS.md:103 (grep for `2024-05-31` over `SNAP`, n = 7 hits).
  - The raw responses are gone by the repository's own statement — "the raw probe responses were not
    retained beyond this report" — PMExperiment/docs/ACCESS.md:88-89 — so the figure cannot be
    reproduced from anything stored.
- **Recomputation:** interval arithmetic over the six stated probe endpoints:
  `max(empty) = 2024-01-01`, `min(non-empty) = 2024-07-01`; bracket = [2024-01-01, 2024-07-01].
  Stated bracket [2024-01-01, 2024-05-31]. Tolerance: exact dates.
- **What would resolve it:** one sentence saying where 2024-05-31 came from. **The innocent reading
  is available and likely**: if the non-empty 2024-07-01 page contained a market closing 2024-05-31,
  then 2024-05-31 is the earliest close *observed*, which is a legitimately tighter bound — but it is
  then a property of that page's contents, not of "n = 6 bracketing probes", and six of the seven
  occurrences say the latter. Retained responses would settle it; there are none.
- **Confidence:** MEDIUM — HIGH that the stated bracket does not follow from the stated probe set,
  LOWER that anything is actually wrong with the number itself.
- **Invalidated by later commits?:** no — `docs/ACCESS.md` is unmodified at the anchor and the
  project is closed.
- **Disclosed by authors?:** **no** for the bracket; **yes** for the irreproducibility
  (PMExperiment/docs/ACCESS.md:88-89), which is why the underlying measurement is recorded
  UNVERIFIABLE rather than contradicted, and why this finding is confined to the internal
  inconsistency the document can be held to on its own text.
- **Why it decides nothing:** the depth bound is a Stage A access observation; the access gate fired
  PENDING_ACCESS on other clauses and no verdict turns on which spring-2024 month the history starts
  in.
- **Consolidation check:** re-verified first-hand — `docs/ACCESS.md:72` re-located in `SNAP` and the
  six probe dates re-read from the cell; the bracket [2024-01-01, 2024-07-01] follows and 2024-05-31
  does not appear among them. **Correction made:** the draft said the endpoint is "restated four more
  times" and then listed six locations; an independent grep for `2024-05-31` over `SNAP` returns
  **seven** hits, so the count is corrected to **six more times, seven occurrences in all**. No
  substance changes.

### AUDIT-C-PMExperiment-7
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** `REGISTRATION.md`'s immutability guarantee for everything above the
  Section 17 amendment line.
- **Direction:** neutral — pure hygiene; the edited line is a results placeholder and carries no
  figure, bar or rule.
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED (git objects)
- **Claim challenged (verbatim):** "Amendments append here, numbered, each carrying its own evidence
  and the date it was made. Nothing above this line is edited after Section 0 is committed." —
  PMExperiment/REGISTRATION.md:660-661
- **Evidence:**
  - Section 0 was committed in `9080186` at 2026-08-29T07:37:33Z. Sixteen minutes later, `98ce2d4`
    (2026-08-29T07:53:10Z) edits `REGISTRATION.md` with **+32/−1**, and the one deleted line is above
    the amendment line: `git show 98ce2d4 -- REGISTRATION.md` shows
    `-*Written only after the gate fires. Empty until then.*` replaced by
    `+*Written only after a gate fires.*` at what is now PMExperiment/REGISTRATION.md:369
    (re-confirmed in this pass).
  - That is the **only** contradicting edit in the history. Every other change above Section 17 is a
    pure insertion — `git log --numstat -- REGISTRATION.md` gives `4d75f66` +72/−0, `32dc10a` +59/−0,
    `f789079` +59/−0, `1b3124e` +151/−0, `17dfebd` +56/−0, `fe7e6b9` +62/−0, `f8128b2` +117/−0,
    `03d16e7` +54/−0 — and `f686036`'s single deletion is the `*(empty)*` placeholder *below* the
    line, inside Section 17 itself.
  - **The substance of the guarantee verifies hard, and that is the more important result.** SHA-256
    of the whole Sections 0–14 region is `00a7e9aa6b36d3d1…` at **all eleven versions** of
    `REGISTRATION.md` from `9080186` to HEAD; SHA-256 of Section 16's original paragraph is
    `42173f13e69a04da…` at all eleven (script:
    `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-prov2/regions.py`, run
    2026-09-12T02:31Z). No registered value, bar, map, prior or rule was ever edited in place.
- **Recomputation:** inputs `git show <c>:REGISTRATION.md` for the eleven versions from `9080186` to
  `03d16e7`; method: extract the line range from the `## 0.` header to the `## 15. ` header, and from
  `Written before the read.` to the following `---`, SHA-256 each; result: one distinct digest per
  region across all eleven versions. Tolerance: exact byte equality.
- **What would resolve it:** narrowing the sentence to what is true and already provided for
  ("Sections 0–14 are never edited; Section 15 is written as gates fire and Section 16 may carry a
  dated closure annotation"), or an appended note recording the `98ce2d4` wording change.
- **Confidence:** HIGH — a single-line diff in a git object, with the surrounding history
  exhaustively checked for others.
- **Invalidated by later commits?:** no — `03d16e7` is the anchored HEAD and the final commit.
- **Disclosed by authors?:** **partly.** The registration itself designates Section 15 as "*Written
  only after a gate fires.*" (PMExperiment/REGISTRATION.md:369) and Section 16's annotation is
  explicitly flagged as "**Recorded 2026-09-02 at closure, before the paragraph it qualifies**"
  (PMExperiment/REGISTRATION.md:636-638), so the *practice* of writing above the line is disclosed;
  the specific in-place edit of the placeholder sentence is recorded nowhere.
- **Why it decides nothing:** the edit changes "the gate fires" to "a gate fires" in a results
  placeholder, and it sits in the **same commit**, `98ce2d4`, that recorded the first gate's verdict
  (Section 15.1, the access gate, PENDING_ACCESS) — nine minutes **after** the first probe request at
  ~07:44Z (PMExperiment/progress.md:58-59); no registered value moved, and the byte hashes prove none
  ever did.
- **Consolidation check:** re-verified first-hand — `git show 98ce2d4 -- REGISTRATION.md` returns
  exactly the one `-`/`+` pair quoted above with `32 1 REGISTRATION.md` in `--numstat`; commit date
  `2026-08-29T00:53:10-07:00` = 07:53:10Z; the claim quote re-located at
  `SNAP/PMExperiment/REGISTRATION.md:660-661` and the replacement text at `:369`. **No correction.**

### AUDIT-C-PMExperiment-8
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the Stage C commit message, `52d39ec`.
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED (git objects)
- **Claim challenged (verbatim):** "docs: Stage C report, Entry 7, ADR-012 and **nine honesty
  tests**" and, in the body, "**Nine honesty tests** pin the verdict, its clause and effective date,
  the retraction with the retracted claim still quoted, the zero-request record, the counterargument,
  the floor's absent sample cost, and the transfer statement." — PMExperiment git commit
  `52d39ec003f9c774a4e73760e75d4798cd905839` (subject and body; live repo, re-read
  2026-09-12T02:55Z)
- **Evidence:**
  - `git show 52d39ec --stat` touches exactly one test file, `tests/test_honesty.py` (+82 lines, no
    deletions).
  - `def test_` count in that file: **28 before, 36 after — exactly 8 added, none removed**
    (re-counted in this pass with `git show 52d39ec^:tests/test_honesty.py | grep -c '^def test_'`
    → 28 and `git show 52d39ec:tests/test_honesty.py | grep -c '^def test_'` → 36). The eight are
    `test_polymarket_access_verdict_is_recorded_with_its_clause`,
    `test_amendment_one_premise_is_retracted_not_quietly_dropped`,
    `test_stage_c_sent_no_market_data_requests`,
    `test_the_counterargument_to_the_access_verdict_is_recorded`,
    `test_the_gate_did_not_fire_and_both_passes_are_absent`,
    `test_the_terms_claim_practice_is_registered`,
    `test_transfer_statement_holds_even_with_no_polymarket_result`,
    `test_volume_floor_cost_in_sample_is_reported_absent_not_zero`.
  - **The same message's other count is right**: "72 tests green" — the tree at `52d39ec` holds
    14 + 4 + 36 + 9 + 9 = **72** test functions, up from 64. Eight, not nine, is what closes that
    arithmetic.
  - The repository's convention is otherwise accurate: `ebdc116` says "nine honesty tests" and added
    exactly 9 (19 → 28); `baa2bf3` says "six" and added exactly 6 (37 → 43).
- **Recomputation:** inputs `git show 52d39ec^:tests/test_honesty.py` and
  `git show 52d39ec:tests/test_honesty.py`; method `grep -c '^def test_'`; result 28 → 36; tolerance
  exact.
- **What would resolve it:** nothing needs resolving in the tree — the message is wrong by one and no
  document repeats the figure for this stage.
- **Confidence:** HIGH — counted directly from the git objects, twice.
- **Invalidated by later commits?:** no — a commit message is immutable once written, and `03d16e7`
  is the final commit.
- **Disclosed by authors?:** **no.**
- **Why it decides nothing:** it is a commit-message count; the suite total it accompanies ("72
  tests green") is right, and every stage total the documents state reproduces exactly at the commit
  it is claimed for.
- **Consolidation check:** re-verified first-hand — subject line re-read as "docs: Stage C report,
  Entry 7, ADR-012 and nine honesty tests"; 28 → 36 re-counted; commit date `2026-08-29T20:45:12-07:00`
  = 2026-08-30T03:45:12Z. **No correction.**

---

## Sound

What verified cleanly, and would have been the place to find a defect if a thesis held here.

**Every figure the repository derives for itself reproduces.**

* **The verdict.** `0.02 + 0.01 + 0.03 × 0.95 = 0.0585` against `EFFECT_BAND_HI = 0.08` — "5.85
  points against a band top of 8.00 points" is exact at four decimal places, and `band.py:96` applies
  the comparison the registration's own rationale registers (existential, at the band top).
* **The whole Pass-1 table: 60 of 60 cells match at four decimal places**, across ten registered
  deciles, two exit routes and three FX turnovers, recomputed from the registered constants alone.
* **Both power bars invert exactly**: `4 × 0.0475 / 0.0004 = 475.0` and
  `4 × 0.0475 / 0.0064 = 29.6875 → 30`; `tests/test_power.py` fires the verdict map at
  475/474/30/29/0 and pins `MDE(100) = 0.043589` — all five boundaries reproduce.
* **The two written forms of the cost floor are algebraically identical** — `0.04 + 0.01 + 0.03p` and
  `0.05 + 0.03p` agree float-for-float at every price tested, and `power.py:74-82` implements the
  same expression.
* **The margins, slacks and survival counts.** 4.84 / 2.83 / 2.15 / 0.15 points, the 0.00195 and
  0.00135 slacks, the factor of 16, 5.73 rising to 5.97 at 91–99c, the existential 10/10 and strict
  0/10 bucket counts at k = 1, 12 and ∞ on both routes — every one exact.
* **The unit determination**, the part the repository derived by hand: −40.0 %, +3.16 %, 0.117,
  0.043, 0.883, 0.0565, 0.0765 — all exact at the printed precision. (The only defect here is the
  provenance sentence that claims they were machine-computed — finding **-5**.)
* **The closing git audit is exact.** "32 commits, 189 reachable objects" reproduces **at
  `1ba50aa`**, which was HEAD when the Stage E Task 5 audit ran (`rev-list --count` = 32,
  `rev-list --objects | wc -l` = 189, re-run in this pass). At the anchor the same commands give 36
  and 213. `.env.example` is 294 bytes, 5 lines, zero `=`; `LICENSE` is MIT with the stated copyright
  line.
* **The suite totals 34 → 39 → 63 → 72 → 89 → 95 → 108 → 111 all reproduce at the commit each is
  claimed for**, and the anchored tree holds exactly 111 `def test_` functions.
* **The timing arithmetic** of the stage logs: 22.9 min against a 75-min ETA, the factor 3.3, 21.4
  min against 50, 43 %, 7.9 min, 2.5×, 5.5× — all exact at the printed precision.
* **The registered constants are pinned to the document.** Nine test functions in
  `tests/test_registry.py` assert each constant against a whitespace-folded substring of
  `REGISTRATION.md`; every constant the band gate consumes is covered, and `FX_TURNOVER_REGISTERED`
  is additionally pinned at `tests/test_band.py:182-184` and to its sentence at
  `tests/test_honesty.py:218-221`.

**Every provenance guarantee that could be checked from the objects holds.** `registry.py` has zero
deleted lines across its three commits; `band.py`, `power.py`, `admissibility.py` and `docs/BAND.md`
have one commit each; Sections 0–14 of `REGISTRATION.md` and Section 16's original paragraph are
byte-identical across eleven versions; `docs/BAND.md` — the table the verdict rests on — has exactly
one commit and has never been modified, so "computed once, never recomputed after seeing a result" is
verified by the object store rather than by assertion; the band gate's definition precedes its firing
by 79 minutes and its arithmetic by 8 minutes; Amendment 4's constant lands 86 seconds before the
text that cites it and the repository **discloses that lag itself and gets it right**; the retraction
of Amendment 1's premise is recorded as a numbered amendment rather than an edit; ADR-012's
three-element rule was fired **first over the authors' own Stage A position**, convicting it, and is
pinned by a test that says so; and the operator's prior enters only at closure, in the operator's own
logged prompt, with every document that mentions it saying it was not pre-registered.

**What I would have expected to find if a post-hoc-registration thesis held, and did not find:** a
bar edited after a result was seen; a threshold first appearing in the same commit as the verdict it
clears; a band recomputed after a calibration reading; an amendment back-dated to precede the data it
responds to; a prior filled in afterwards and then called pre-registered. **None is present.** The
one dating error found (**-1**) runs in the direction that makes the registration look *later* than
it was — the opposite of what back-dating would produce.

---

## Could not be checked and why

Twenty of the sixty-seven verification items and six of the twenty-five provenance claims are
UNVERIFIABLE. **None is unverifiable because something was hidden from me**, and none is converted
into a finding.

**(a) HTTP measurements whose responses were deliberately not retained — 11 verification rows, and
provenance P12, P13, P20, P21.** Every figure Stages A, C and D report from a network probe: the
11-request latency range 99.9–213.8 ms, the settled-history bracket, the `robots.txt` and terms
status codes and byte counts, the two Polymarket request logs, the character counts of rendered
pages, the occurrence counts inside the Kalshi PDF, the Dune dataset row counts and coverage windows,
the candlestick probe on `NASDAQ100-24OCT25-T21499.99`, the Kalshi desk reply and its 2026-09-01
received date. **No response body, no header, no timestamped request ledger and no `data/raw/`
directory exists at any commit** — checked over the whole history, not just the anchor:
`git log --all --diff-filter=A --name-only` adds no data-shaped file, ever. The repository states
this itself at `PMExperiment/docs/ACCESS.md:87-89`, and `CLAUDE.md:29`'s standing rule 6 ("Ledgers
are append-only and fsynced") has no file behind it here. Section 14's reproducibility clause — "the
gate verdict must be regenerable from the stored raw enumeration and candlestick responses under
`data/raw/`" (`REGISTRATION.md:359-363`) — is therefore **vacuous rather than satisfied or
violated**: consistent with the fact that no enumeration ever ran, but never tested. The internal
arithmetic of those logs *is* checkable and does verify (2 + 6 + 3 = 11 API reads, 2 + 11 = 13 total,
4 + 1 + 1 + 1 = 7 Polymarket requests, 14 + 3 = 17 attributed strings, and every text-share ratio).
**What would settle them:** retained response bodies with `Date` headers, or an append-only request
ledger committed at fetch time. **"Zero requests were sent" (P13) is additionally an unfalsifiable
negative from inside the repository** — the absence of stored responses is *consistent* with it and
is not evidence for it.

**(b) Figures imported from outside this repository — 6 verification rows, and provenance P23.** The
MLCryptoEngine AUC 0.501, the NPD minimum detectable contrast 0.0512 with its 415 days and 6.9378
USD, the Insider 49.35 bp, the Bürgi–Deng–Whelan magnitudes (313,972 prices; −40 %; +3.1 %; "lose
over 60 % after fees"), the Krause −0.077 at a 4.0 % settlement rate, and whether Bürgi–Deng–Whelan
really uses "total staked ≥ $1,000". Inside PMExperiment these are **quotations with no n attached**
— the registration says so itself for the band's top ("The band's top carries no n",
`REGISTRATION.md:440`) — pinned as strings by `tests/test_honesty.py` and `tests/test_registry.py`.
Their internal *use* verifies: every conversion and comparison built on them recomputes exactly.
Their *truth* is a question for MLCryptoEngine, NPDExperiment, InsiderExperiment and two outside
papers, not for this repository, and it is left there.

**(c) Registered machinery that never ran — 3 verification rows.** The MDE on a real cell, the Wilson
bound on a real sample, and `v̄` on real snapshot prices. There is nothing to reproduce because the
access gate fired PENDING_ACCESS before any universe was enumerated. Their *definitions* were checked
against the code and are exactly as registered; only their values do not exist.

**(d) The mutation tallies (provenance P25) and the credential scan (P16's second half).** "Every
guard here carries a test that fails when the guard is removed, verified by mutation" plus the
tallies 9, 5, 5, 6, 13, 14, 2 — no mutation log, harness script or CI artifact exists at any commit
(`scripts/` holds only `.gitkeep`). The tests that would be killed are present and readable; that
each mutation was *run* and killed is document-only. The repository itself records three harness
faults that produced false-green runs (`progress.md:815-833, 991-997, 1232-1246`), which is the
strongest internal reason to treat the tallies as unverified — **and it is the authors who recorded
them.** Likewise "zero credential-shaped strings over 189 objects": the scan's output was not
retained; its two object counts were, and both reproduce exactly.

**Two things I chose not to run, and why.** I did not execute the repository's test suite — the
read-only rule forbids running a repository's scripts in place, and the working tree carries an
untracked `_CLOSED_DO_NOT_RUN_HERE` marker (recorded by the LOCATE pass, 2026-09-05T23:28Z); every
test assertion cited above was verified by reading the test and recomputing the assertion
independently. And I attempted no network request: the figures that would need one are precisely the
ones this repository declined to make, and reproducing them now would measure 2026-09-12, not
2026-08-29.

---

## Live-repo access log

Every access to `/home/kiros-li/Documents/GitHub/PMExperiment/` across all three passes (LOCATE,
VERIFY/PROVENANCE, and this consolidation) was **read-only**. The commands used, across all passes:
`status --porcelain`, `rev-parse`, `log` (with `--format`, `--date=iso-strict`, `--reverse`,
`--follow`, `--numstat`, `-p`, `-S`, `--all --diff-filter=A --name-only`), `show` (including
`show <commit>:<path>` to stdout, `--stat`, `--numstat`, `-- <path>`), `blame -L`,
`rev-list --count`, `rev-list --objects`, `ls-tree`, `cat-file -s`, `count-objects -v`, and one
`ls -laR data/`. **No file in the repository was opened for writing, no repository script was
executed, and no commit, checkout, stash, reset, clean, add, branch, merge, rebase, worktree or gc
command was run.** No `.env`, keystore, session, credential or token file was opened. All document
and code content was read from the anchored snapshot at
`/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/`.

**Unanchored reads** (working tree, not the snapshot), carried forward from the earlier passes and
none added in this one: `ls -la` of the working tree and of `data/` at **2026-09-05T23:28Z**
(LOCATE), and `ls -laR data/` at **2026-09-12T02:41Z** (PROVENANCE) — in both, `data/` holds a single
0-byte `.gitkeep`, with no `data/raw/` and no `data/vendor/`. These may have changed after the
2026-09-02 anchor. **This consolidation pass made no unanchored read.**

### Status before and after, verbatim

**VERIFY pass — `git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain` BEFORE first
access, 2026-09-12T02:36:30Z:**

```
```

**VERIFY pass — AFTER last access, 2026-09-12T02:45:25Z:**

```
```

**PROVENANCE pass — BEFORE first access, 2026-09-12T02:20:41Z:**

```
```

**PROVENANCE pass — AFTER last access, 2026-09-12T02:44:52Z:**

```
```

**CONSOLIDATION pass — BEFORE first access, 2026-09-12T02:54:51Z:**

```
```

**CONSOLIDATION pass — AFTER last access, 2026-09-12T02:55:13Z:**

```
```

All six outputs are **empty** (exit status 0, working tree clean), and `git rev-parse HEAD` returns
`03d16e71dbf25a86c529884662d02136f8e82334` before and after every pass. **No modification was made to
the audited repository and none is reported.**

The working tree carries one untracked file, `_CLOSED_DO_NOT_RUN_HERE`, which does **not** appear in
`status` because it is listed in `.git/info/exclude`. This is **pre-existing operator dirt, not
mine** — it was already recorded by the LOCATE pass on 2026-09-05 and is dated 2026-09-02, before
every access above. It is reported here rather than passed over, per the common rules. No other
unexpected entry was seen in any pass.

### Scratch and work directories

All written by me; none copied from the repository; none executed with a working directory inside an
audited path.

| path | what it holds |
|---|---|
| `work/agentC-pm-verify/recompute.py` | The main recomputation — the BAND-OPEN headline, the fee+spread floor, the four crossing prices, all 60 Pass-1 cells, both bucket-count quantifiers at k = 1, 12, ∞, the margins and slacks, the six unit-determination cells, both power bars, `MDE(100)`, the cost floor in both forms and the `docs/LICENCES.md` text shares. |
| `work/agentC-pm-verify/mkjson.py` | Emits `PMExperiment.claims.json` (67 objects). |
| `work/agentC-pm-prov/` | Provenance scratch (`adrs.py`, `sections.py`, `mkjson.py`). |
| `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-PM-verify2/` | `power_check.py` (the power arithmetic behind **-3** and **-4**, using `scipy.stats.norm`) and `gen_tables.py` (renders the verification tables from the JSON so they cannot drift from it). |
| `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-prov2/` | `regions.py` (SHA-256 of the Sections 0–14 and Section 16 regions across eleven `REGISTRATION.md` versions) and `claims.txt`. |
