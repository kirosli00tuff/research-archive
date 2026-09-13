# Agent B draft findings — PMExperiment, part p1-register

**Repository:** PMExperiment, anchored SHA `03d16e71dbf25a86c529884662d02136f8e82334`
(main, 2026-09-02, closed project). Read from
`/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/` unless a line says
otherwise. Live repo touched read-only for git history only (log/show/rev-parse); access
log at the end.

**Assigned documents:** `REGISTRATION.md`, `HYPOTHESES.md`, `DECISIONS.md`, `report.md`,
`README.md`. `docs/*`, `progress.md`, `pmexperiment/*` and `tests/*` were read for context
and are cited as corroboration; where a finding's primary evidence sits there it is marked.

**Direction:** B — this program claimed more than it earned. Nine findings follow; the
repository is unusually well self-disclosed, and the "What I checked and found sound"
section at the end is long on purpose.

---

### DRAFT-p1-register-1
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** BAND-OPEN (REGISTRATION.md Section 15.2), and the registered
  artifact it ships — "the surviving region, registered here as the only region the power
  gate may fire over: entry prices **91–99c** … **held to resolution**"
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**In one sentence: BAND-OPEN — a surviving region
  exists that the permitted subset admits, at entry prices 91–99c held to resolution,
  requiring 5.85 points of underpricing at the registered FX turnover against a registered
  band whose top is 8.00 points.**" — PMExperiment/REGISTRATION.md:409-412. And the bar it
  is judged against: "Its top, 0.08, rounds the largest single-category published figure,
  Krause's 7.7 points. The gate (Section 0.3) is judged against this band and nothing
  else." — PMExperiment/REGISTRATION.md:254-256.
- **Evidence:**
  - The band's top is the *only* thing that makes BAND-OPEN fire. Recomputed from the
    registered constants (`FEE_PER_SIDE_USD = 0.02` PMExperiment/pmexperiment/registry.py:53,
    `HALF_SPREAD_USD = 0.01` :55, `FX_PER_DIRECTION = 0.015` × `FX_DIRECTIONS = 2` :56-57,
    `FX_TURNOVER_REGISTERED = 1.0` :66): with the registered top 0.08, 10 of 10 buckets
    survive on both routes at every k; with the top set instead to the largest cited
    magnitude that carries an n — Bürgi's 0.030, n = 313,972 contract prices
    (PMExperiment/REGISTRATION.md:230-233) — **0 of 10 buckets survive on either route at
    k = 1, k = 12 or k → ∞, i.e. the registered verdict flips to BAND-EMPTY.**
  - The source that sets that top carries **no n**: "Krause sets the top, and no sample
    size for it appears anywhere in this document" — PMExperiment/REGISTRATION.md:442-443;
    "**Krause's n is nowhere in the registration**" — PMExperiment/DECISIONS.md:267.
  - It also carries **no retrievable identifier**. The full citation is "Krause, *Market
    Efficiency and the Favorite-Longshot Bias in Unemployment Prediction Markets*, 2026"
    (PMExperiment/REGISTRATION.md:235-238) — no venue, no DOI, no SSRN number, no page —
    while the *companion* study in the same bullet is given as "SSRN 7087538, 95 contracts
    over 12 months" (PMExperiment/REGISTRATION.md:240-241). Grep over the whole snapshot
    returns 30 mentions of "Krause" and no identifier, no n and no fetch record on any of
    them.
  - There is **no recorded live verification of any effect-band source**. Standing rule 4
    is "**Measured beats documented.** Verify every external figure live."
    (PMExperiment/CLAUDE.md:25). `docs/ACCESS.md` records fetch dates, byte counts and
    HTTP codes for every permission document read; it records none for Bürgi, Krause or
    Page-Clemen. Standing rule 13, "**Every figure travels with its n in the same
    sentence.**" (PMExperiment/CLAUDE.md:44), is recorded as breached for exactly this
    figure and not repaired.
  - The asymmetry with the standard the same repository applied to its **negatives**: a
    1,201,580,990-row dataset documenting all four gate inputs was recorded UNMEASURED
    because "**neither the dataset card nor the CC BY 4.0 legal code prints any date**"
    (PMExperiment/DECISIONS.md:462-463); the repository's own Stage A finding was convicted
    on one missing element (PMExperiment/DECISIONS.md:434-440); Kalshi's institutional
    reply was recorded UNMEASURED for want of an effective date and a quotation
    (PMExperiment/REGISTRATION.md:546-556). The one input that keeps the positive-flavoured
    verdict alive was admitted with no n, no identifier and no fetch record, and the
    evidence procedure (`pmexperiment/admissibility.py`) was never fired over it — it is
    scoped to permission claims only (PMExperiment/DECISIONS.md:367-371).
  - Consequence, not academic: the region derived from that top is carried forward as a
    binding constraint on any future work — "**A reopened measurement starts at the power
    gate over 91–99c held to resolution and no other region**"
    (PMExperiment/REGISTRATION.md:1109-1111) — and the band's thinness is one of the two
    stated inputs to the operator's closure decision (PMExperiment/REGISTRATION.md:1046-1054).
- **Recomputation (if any):**
  Inputs, all from PMExperiment/pmexperiment/registry.py:53-66 and REGISTRATION.md:206
  (`C(p) = 0.04 + 0.01 + 0.03·p`) / Amendment 2's two routes (REGISTRATION.md:720-724) /
  Amendment 4's `FX(p) = 0.03·p/k` (REGISTRATION.md:799).
  Method: `R(p, sides, k) = 0.02·sides + 0.01 + 0.03·p/k`; a bucket "survives" when
  `R(midpoint) < band_top` (the existential test `band_top_exceeds_requirement`,
  PMExperiment/pmexperiment/band.py:83-96). Script:
  `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-PM-p1/counterfactual.py`.
  Result:
  ```
  top = 0.080 (Krause 7.7 rounded up, n absent): k=1 H 10/10 X 10/10; k=12 10/10 10/10; k→∞ 10/10 10/10  → not BAND-EMPTY
  top = 0.077 (Krause unrounded,  n absent):     k=1 H 10/10 X  9/10; k=12 10/10 10/10; k→∞ 10/10 10/10  → not BAND-EMPTY
  top = 0.030 (Bürgi, n = 313,972 prices):       k=1 H  0/10 X  0/10; k=12  0/10  0/10; k→∞  0/10  0/10  → BAND-EMPTY
  ```
  The full required-underpricing table reproduces the register exactly (see
  `recompute.py` in the same directory): R_H(0.95) = 0.0585, R_X(0.95) = 0.0785,
  R_H(0.91) = 0.0573, R_H(0.99) = 0.0597, held-route margin at 0.95 = 0.02150 ("the top
  2.15 of 6.0 points"). The arithmetic is right; the input is the problem.
- **What would resolve it:** a retrievable identifier for Krause 2026 (DOI/SSRN/URL) with
  its n and its price-bucket definition, fetched and dated the way every permission
  document in this repository was; or a numbered amendment restating the band top from a
  source that carries an n, with the band verdict re-fired against it.
- **Confidence:** HIGH — the counterfactual is arithmetic over the repository's own
  registered constants, and the absence of an n and of any identifier for the deciding
  source is verifiable by grep over the whole snapshot.
- **Invalidated by later commits?:** no — Sections 0–14 of REGISTRATION.md are byte-identical
  from the Section 0 commit `9080186` to the anchored SHA (verified by diff), Amendment 2
  fixes the band as "computed once" (REGISTRATION.md:744-745), and the project is closed.
- **Disclosed by authors?:** partly. The missing n **is** disclosed, repeatedly and
  prominently — "**The band's top carries no n** (standing rule 13)"
  (PMExperiment/REGISTRATION.md:440), "the band survives on its top alone, set by the one
  source whose n the registration never recorded" (PMExperiment/README.md:148-149),
  DECISIONS.md:265-270. What is **not** disclosed anywhere is (a) that the source carries
  no retrievable identifier while its own companion study does, (b) that standing rule 4's
  live-verification requirement was never applied to any effect-band source, and (c) the
  asymmetry between that admission and the UNMEASURED verdicts the same repository issued
  against candidates missing a single element.

---

### DRAFT-p1-register-2
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the closure framing — "What follows is the method working,
  not a disappointment" — and the operator prior of 5 to 8 percent (Amendment 7)
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "The operator's prior was 5 to 8 percent, so **a
  null was the modal expected outcome** before any of this began. What follows is the
  method working, not a disappointment." — PMExperiment/README.md:20-23. And, in the
  report: "at a prior of 5 to 8 percent, **a null was the modal expected outcome from the
  beginning.** This ending is the method working, not a disappointment." —
  PMExperiment/report.md:443-445.
- **Evidence:**
  - The register's own binding prohibition: "**This prior may not be described anywhere as
    pre-registered, and no verdict in this repository may be read against it as though it
    had been.** It is a **stated** prior, dated at closure." —
    PMExperiment/REGISTRATION.md:1027-1029 (Amendment 7).
  - The prior did not exist during the project. "Section 13, `The operator prior`, reads
    *'To be filled by the operator before the gate fires, and recorded with the date it was
    given.'* It has read that since Section 0 was committed on 2026-08-29 and **it was
    never filled**. The operator's prior is now given as **5 to 8 percent** … supplied
    **2026-09-02**, at closure, after two gates had already fired." —
    PMExperiment/REGISTRATION.md:1018-1022. Git confirms the interval: Section 0 committed
    `9080186` 2026-08-29T07:37:33Z, the band gate fired `32dc10a` 2026-08-29T19:24:06Z,
    both access gates fired 2026-08-29 (`98ce2d4`, `1b3124e`), and the prior first appears
    in `fe7e6b9` 2026-09-02T09:32:22Z.
  - "before any of this began" and "from the beginning" are assertions about the ex-ante
    state of expectation. No document records any operator expectation before 2026-09-02;
    Section 13 is empty and a test pins it empty
    (PMExperiment/tests/test_honesty.py:517-525).
  - The framing was written to instruction, and the instruction's error was caught only in
    part. The Stage E operator prompt, logged verbatim, reads: "State the registered prior
    and that a null was the modal expected outcome, so the closure reads as the method
    working rather than as a disappointment." — PMExperiment/progress.md:1310. The
    repository corrected "registered" to "stated" (PMExperiment/progress.md:1504, and the
    correction is pinned by `test_the_operator_prior_is_never_described_as_pre_registered`,
    PMExperiment/tests/test_honesty.py:508-514) but kept the retrospective clause. The
    guard checks for the *presence* of the disclaimer 150 lines further down the README, not
    for the *absence* of the reading Amendment 7 forbids.
  - The consequence is the whole tone of the closure: the sentence is what converts "five
    stages, zero contracts enumerated, no statistic relating a price to an outcome" into
    "the method working, not a disappointment", in the opening block of the public README.
- **Recomputation (if any):** none — the finding is documentary. Dates cross-checked against
  `git -C /home/kiros-li/Documents/GitHub/PMExperiment log --date=iso-strict`.
- **What would resolve it:** either a dated record of the operator's prior given before
  2026-09-02, or a one-line edit dropping "before any of this began" / "from the
  beginning" so the prior is used only where Amendment 7 permits it — as the recorded input
  to the cost decision.
- **Confidence:** HIGH — both the prohibition and the sentence that breaches it are
  verbatim in tracked documents at the anchored SHA.
- **Invalidated by later commits?:** no — the README block is the last README state
  (`1ba50aa`, 2026-09-02T09:36:29Z) and the repository is closed; a later commit could of
  course amend it.
- **Disclosed by authors?:** partly — README.md:168-175 ("The prior, and why it is not
  called registered") and Amendment 7 both disclose that the prior is post-hoc, and
  Amendment 7 itself makes a milder version of the same move
  ("which is the frame the closure should be read in", REGISTRATION.md:1034). The specific
  breach — a retrospective claim about ex-ante expectation in the README's opening and in
  the report's closure — is disclosed nowhere.

---

### DRAFT-p1-register-3
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the power gate (REGISTRATION.md Sections 0.3, 0.4, 9;
  `pmexperiment/power.py`), the artifact the whole repository is framed around
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **GO** | MDE ≤ 0.02 | the design resolves the
  entire published band; Stage B is authorized for that universe against the registered
  target |" — PMExperiment/REGISTRATION.md:110. With the definition: "The minimum
  detectable effect for a cell, with z = 2.0 two-sided: MDE = z · sqrt(v̄ / n_T)" —
  PMExperiment/REGISTRATION.md:99-101 (restated at :301-302).
- **Evidence:**
  - `Z_CRITICAL: float = 2.0` — PMExperiment/pmexperiment/registry.py:9, consumed at
    `return registry.Z_CRITICAL * math.sqrt(mean_dispersion / tail_count)` —
    PMExperiment/pmexperiment/power.py:45. Nothing multiplies in a z for β.
  - **No target statistical power is stated anywhere in the repository.** Grep over every
    tracked `.md` and `.py` for "beta", "80 %", "80%", "1 − β", "type II", "false negative"
    returns nothing on the power gate; the only near-mention is the DEGRADED row's
    "with the achieved power stated beside the registered target"
    (PMExperiment/REGISTRATION.md:111), which never defines it.
  - A quantity defined as 2 standard errors is the effect a two-sided 5 % test detects
    **about half the time**, not one the design "resolves". Recomputed below: power = 0.516
    at α = 0.05 two-sided, 0.500 if the registered z = 2.0 is itself the critical value.
  - The bars therefore understate the enumeration a real 80 %-power design needs by a
    factor of 1.96: GO would need n_T ≈ 932 rather than the registered ≥ 475
    (PMExperiment/REGISTRATION.md:128), and staying out of BLOCKED would need n_T ≈ 59
    rather than ≥ 30 (:129).
  - Direction of bias: toward GO/DEGRADED and away from BLOCKED — toward H1 staying open.
    The registration's own preamble makes that omission a breach of its own rule: "Every
    number in this document is **derived, measured, or labelled an assumption with its
    direction of bias named**." — PMExperiment/REGISTRATION.md:13-14. z = 2.0 is none of
    the three.
  - Why this matters for the repository's central claim about itself: "This repository
    **followed Insider, not NPD**" (PMExperiment/README.md:190) and CLAUDE.md:63-65
    "**Follow Insider.** Compute the minimum detectable effect from dispersion and bucket
    counts alone…". NPDExperiment's failure is quoted here as "a design that could not have
    detected an effect anywhere in the range it was testing"
    (PMExperiment/README.md:184-185). A gate that returns GO for a design with coin-flip
    power against the band bottom is a weaker protection than the framing implies, and
    Section 8 — "the clustering unit, and the trial grid with its multiplicity correction"
    (PMExperiment/REGISTRATION.md:294-295) — defers to *after* the gate fires the two
    corrections that would push the realized MDE further up, so the gate is the optimistic
    end of the repository's own inference plan.
- **Recomputation (if any):**
  Inputs: z = 2.0 (REGISTRATION.md:99-101; registry.py:9), band edges 0.02 / 0.08
  (REGISTRATION.md:221; registry.py:10-11), planning v̄ = 0.0475 (REGISTRATION.md:123).
  Method: power of a two-sided test when the true effect equals the registered MDE,
  `P(|Z| > z_crit | mean = 2.0)`; and `n = (z_{α/2}+z_β)²·v̄ / effect²` for 80 % power.
  Script: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-PM-p1/recompute.py`.
  Result:
  ```
  power at the registered MDE, α = 0.05 two-sided (z_crit = 1.96):   0.5160
  power at the registered MDE, taking z_crit = the registered 2.0:   0.5000
  z for 80 % power, two-sided 5 %: 2.8016  → n inflation vs z = 2.0: 1.9622
  GO  (MDE ≤ 0.02): registered n_T = 475.00  → n_T at 80 % power = 932.05
  BLOCKED edge (MDE ≤ 0.08): registered n_T = 29.69 (doc: 30) → 58.25 at 80 % power
  ```
- **What would resolve it:** a numbered amendment stating the power level the gate is set
  at, and either restating the required counts at that power or relabelling GO's
  consequence from "the design resolves the entire published band" to what 2 SE actually
  buys.
- **Confidence:** HIGH on the arithmetic and on the absence of any stated power level;
  MEDIUM on severity, because the gate never fired, so no realized verdict is wrong — what
  is wrong is a registered verdict row's stated consequence and the framing built on it.
- **Invalidated by later commits?:** no — Sections 0–14 are byte-identical from `9080186`
  to the anchored SHA and the project is closed.
- **Disclosed by authors?:** no. The repository discloses that the gate never fired, that
  475 and 30 are "planning figures" (REGISTRATION.md:131), and that the power question
  remains unanswered (REGISTRATION.md:339 / README.md:190-192). It nowhere discloses the
  power level implied by z = 2.0, nor names the direction of bias of that choice.

---

### DRAFT-p1-register-4
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** BAND-OPEN (REGISTRATION.md Section 15.2) and its
  "three qualifications registered with the verdict and not separable from it"
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "| BAND-EMPTY | **does not fire.** The registered
  band exceeds the required underpricing at 10 of 10 registered buckets, on both exit
  routes, at k = 1, at k = 12 and in the k → ∞ limit. |" —
  PMExperiment/REGISTRATION.md:416, immediately followed by "**Three qualifications
  registered with the verdict and not separable from it:**" — :431.
- **Evidence:**
  - Amendment 2's registered BAND-EMPTY condition is, verbatim: "no price bucket where the
    registered effect band exceeds the required underpricing" —
    PMExperiment/REGISTRATION.md:740. Read as "the band (i.e. all of it) exceeds", the
    verdict is BAND-EMPTY; read existentially ("some of it"), BAND-OPEN.
  - The repository knows this and reports it — in the working document only: "| reading |
    surviving buckets, route H | … | **existential** … **10 / 10** … | strict — would
    *every* effect in the band survive? | **0 / 10** at every k | **0 / 10** at every k |
    BAND-EMPTY |" — PMExperiment/docs/BAND.md:229-234 (primary evidence outside my
    assignment); also PMExperiment/pmexperiment/band.py:88-96,
    PMExperiment/tests/test_band.py:99-108, PMExperiment/progress.md:455-458.
  - It appears in **none** of the four conclusion-bearing documents. Grep for
    "quantifier|strict reading|existential|both readings" over the snapshot returns zero
    hits in REGISTRATION.md Section 15.2, report.md, README.md and HYPOTHESES.md. The
    register's three "not separable" qualifications (REGISTRATION.md:431-446) are the
    missing magnitude, the missing n, and "BAND-OPEN is not a finding that an edge exists".
    The one qualification that flips the verdict is not among them.
  - The register's own standard for this is explicit — "The qualifier travels with it and
    is not separable" (PMExperiment/docs/BAND.md:20) and standing rule 13 (CLAUDE.md:44).
    HYPOTHESES.md, whose stated job is "to prevent retrying a settled question because the
    number that closed it is buried" (:5-6), carries the verdict at :119-160 with no trace
    of the alternative reading.
- **Recomputation (if any):** confirmed by my own table
  (`/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-PM-p1/recompute.py`):
  min R_H over the ten registered midpoints at k = 1 is 0.0316 at the 1–10c bucket, so the
  band bottom 0.02 is exceeded at every bucket on every route at every k — 0/10 under the
  strict reading, exactly as docs/BAND.md reports.
- **What would resolve it:** one sentence in Section 15.2 (and in the HYPOTHESES entry)
  recording that the same registered condition, read strictly, fires BAND-EMPTY at 10 of 10
  buckets, with the reason the existential reading was taken.
- **Confidence:** HIGH — the omission is verifiable by grep; the alternative's consequence
  is stated by the authors themselves.
- **Invalidated by later commits?:** no — the project is closed and Amendment 2 fixes the
  band as computed once (REGISTRATION.md:744-745).
- **Disclosed by authors?:** yes (PMExperiment/docs/BAND.md:116 and :229-237;
  PMExperiment/pmexperiment/band.py:88-96; PMExperiment/progress.md:455-458). The authors
  disclose the alternative reading and its BAND-EMPTY consequence in the working document.
  My finding is only that it did not travel into Section 15.2, report.md, README.md or
  HYPOTHESES.md, where the verdict is stated to a reader who will not open docs/BAND.md.

---

### DRAFT-p1-register-5
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** Amendments 1–3 and ADR-006(2)/ADR-007(2)/ADR-008 — the
  amendment that registers the band gate's verdict rows
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Made 2026-08-30.** A new gate, ordered ahead of
  the power gate, because it is free and may be decisive on its own." —
  PMExperiment/REGISTRATION.md:707 (Amendment 2), against "### 15.2 The fee-versus-edge
  band, **fired 2026-08-29**: BAND-OPEN" (:402) and "**Fired on Amendment 2's registered
  definitions**" (:404).
- **Evidence:**
  - As written, the register says the verdict fired a day *before* the amendment that
    defines its verdict rows was made. Three more instances of the same stamp:
    Amendment 1 "**Made 2026-08-30**" (REGISTRATION.md:667), Amendment 3 (:751), and
    DECISIONS.md ADR-006(2) "**Status:** accepted, 2026-08-30" (:140), ADR-007(2) (:160),
    ADR-008 (:180) — while ADR-009 and ADR-010, which report Stage B's own work, are
    stamped "accepted, 2026-08-29" (DECISIONS.md:210, :276) and sit *after* them in an
    append-only file. Amendment 4 is stamped "**Made 2026-08-29, before the band gate
    fired**" (REGISTRATION.md:783) yet is appended after three amendments stamped a day
    later. The numbering note compounds it: "## Note on numbering, **recorded 2026-08-29**,
    not repaired" describing "the pair **dated 2026-08-30**" (DECISIONS.md:195-199).
  - Git settles the actual order, and the actual order is fine: `git -C
    /home/kiros-li/Documents/GitHub/PMExperiment show f686036` — "docs: amendments 1-3 —
    Polymarket measures the phenomenon, the fee band fires first",
    **2026-08-29T11:05:26-07:00 = 2026-08-29T18:05:26Z**, touching REGISTRATION.md,
    DECISIONS.md, HYPOTHESES.md, progress.md, tests/test_honesty.py. The band arithmetic
    landed in `9b4bd4f` at 19:15:55Z, Amendment 4 in `4d75f66` at 19:17:21Z, and the
    verdict in `32dc10a` at 19:24:06Z — six hours *after* Amendment 2. `git show
    f686036:REGISTRATION.md` shows the "**Made 2026-08-30**" text present in that very
    commit, so the stamp is wrong under both local time (-07:00) and UTC.
  - This repository makes dates load-bearing evidence by its own rule — ADR-012 requires
    "a quoted clause, the document's effective date, and the date it was fetched"
    (PMExperiment/DECISIONS.md:367-370), and `pmexperiment/admissibility.py:136-144`
    rejects a claim whose date does not parse. The binding register's own amendment dates
    are off by a day, in the direction that makes the record read as if a bar had been set
    after the verdict it governs.
- **Recomputation (if any):** none beyond the git reads quoted above (read-only
  `log`/`show`; access log at the end of this file).
- **What would resolve it:** a correction note in Section 17 recording the true commit
  timestamps for Amendments 1–3 and the ADR pair, or a statement of the timezone convention
  under which "2026-08-30" is the right stamp for a commit made at 2026-08-29T18:05:26Z.
- **Confidence:** HIGH — the commit object and the file content at that commit are both
  read directly.
- **Invalidated by later commits?:** no — `f686036` is an ancestor of the anchored SHA and
  the text is unchanged at the anchor.
- **Disclosed by authors?:** no. The repository discloses the ADR *numbering* collision
  (DECISIONS.md:195-204) and one commit-ordering lag ("`registry.FX_TURNOVER_REGISTERED`
  was committed in `9b4bd4f`, one commit *before* the Amendment 4 text it cites landed in
  `4d75f66`", DECISIONS.md:304-307) — which shows the authors do track this class of defect
  — but nowhere records that Amendments 1–3 carry a date a day after the commit that made
  them.

---

### DRAFT-p1-register-6
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the registered planning counts of Section 0.4 — "| GO,
  MDE ≤ 0.02 | ≥ 475 |" and "| stay out of BLOCKED, MDE ≤ 0.08 | ≥ 30 |"
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "At the tail cell's planning dispersion — prices
  near 5c or 95c give p(1−p) ≈ 0.0475, so sqrt(v̄) ≈ 0.218 — inverting MDE = 2·sqrt(v̄/n) at
  each bar gives the required tail count" — PMExperiment/REGISTRATION.md:122-124.
- **Evidence:**
  - The tail cell is not "prices near 5c or 95c". It is registered as the union of two
    whole deciles: "**The tail cell T** is the union of 1–10 and 91–99" —
    PMExperiment/REGISTRATION.md:70-71 (`TAIL_BUCKETS_CENTS = ((1, 10), (91, 99))`,
    PMExperiment/pmexperiment/registry.py:26). And v̄ is registered as "the mean of
    p_i(1−p_i)" over the cell's prices (:76-77), not the value at its centre.
  - Recomputed: the uniform mean of p(1−p) over the 19 integer-cent prices of the
    registered cell is **0.049105**, not 0.0475, so the required counts are understated by
    3.4 %: GO needs n_T ≥ **491**, not 475. The registration's preamble requires "Every
    number in this document is **derived, measured, or labelled an assumption with its
    direction of bias named**" (:13-14); this one is presented as derived, is derived from
    a different quantity than the one it names, and carries no direction.
  - A second, larger staleness in the same figures: after BAND-OPEN, "**The surviving
    region, registered here as the only region the power gate may fire over:** entry prices
    **91–99c**" (REGISTRATION.md:420-422) — half the cell the 475/30 bars were derived for,
    and half the population the supporting expectation rests on ("The published benchmark …
    reports two-thirds of its 313,972 contract prices in the 1–10c and 90–99c bands, so the
    unrestricted universe reaching 475 tail contracts is expected", :132-134). No amendment
    restates the required n_T for the halved region; the register continues to carry
    475 and 30.
- **Recomputation (if any):**
  Inputs: cell definition REGISTRATION.md:70-71 / registry.py:26; v̄ definition
  REGISTRATION.md:76-77; planning value REGISTRATION.md:123; formula REGISTRATION.md:101.
  Method: mean of p(1−p) over integer cents, then n = z²v̄/MDE² at z = 2.0. Script
  `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-PM-p1/recompute.py`. Result:
  ```
  1–10c  uniform mean p(1−p) = 0.051150 (n = 10 prices)
  91–99c uniform mean p(1−p) = 0.046833 (n =  9 prices)
  union T                     = 0.049105 (n = 19 prices)     registered planning v̄ = 0.047500
  n_T for GO at v̄ = 0.049105: 491.05   (registered: 475)
  n_T for MDE ≤ 0.08        :  30.69   (registered: 30, from 29.69)
  ```
- **What would resolve it:** restating the planning dispersion as the cell mean with its
  direction of bias named, and restating the required counts for the 91–99c region the band
  gate left as the only firing region.
- **Confidence:** MEDIUM — the arithmetic is certain, but the realized v̄ was to be measured
  (":131") and the true price distribution inside the deciles is unknown, so the sign of
  the error on real data could go either way; what is certain is that a direction of bias
  was required and not given.
- **Invalidated by later commits?:** no — Sections 0–14 are byte-identical from `9080186`
  to the anchor.
- **Disclosed by authors?:** partly — "Both are planning figures; the realized v̄ is
  measured from snapshot prices in Task 3 and reported beside them"
  (PMExperiment/REGISTRATION.md:131-132) discloses that they are provisional, and "That
  gate was not designed here" (PMExperiment/report.md:126) discloses that the narrowed
  region's gate was never specified. Neither discloses that 0.0475 is the point value at
  the cell's centre rather than the cell mean, nor names its direction of bias.

---

### DRAFT-p1-register-7
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** README.md "What would reopen this" versus REGISTRATION.md
  Amendment 9's fourth reopening condition
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "## What would reopen this / Each is an operator
  action, not a measurement: / 1. **an established legal entity applying for Internal
  Use** … / 2. **an academic tier offered by Kalshi, if one is** … / 3. **a licensed dataset
  whose licensor held authority to license**" — PMExperiment/README.md:151-162.
- **Evidence:**
  - The register at the anchored SHA carries four: "**Fourth reopening condition, added to
    Amendment 8's three:** / 4. **a Polymarket data licence or written authorization** —
    the same instrument Stage C found absent, obtained." —
    PMExperiment/REGISTRATION.md:1161-1165. HYPOTHESES.md carries it too (:352-358). The
    README does not, and the README is the only one of the three a cold reader is told to
    read first.
  - Git shows why: the README was rewritten in `1ba50aa` "docs: Task 4 — rewrite README.md
    for a cold reader" at 2026-09-02T09:36:29Z, and Amendment 9 landed 14 minutes later in
    `03d16e7` at 2026-09-02T09:50:29Z, whose stat touches DECISIONS.md, HYPOTHESES.md,
    REGISTRATION.md, progress.md and tests/test_honesty.py — **not** README.md.
  - The direction is mild but real for a B-thesis: the public document understates the
    routes by which the question could be reopened, which makes the terminal framing
    ("**terminal**", README.md:6) look tighter than the register supports.
- **Recomputation (if any):** none beyond the read-only `git show --stat 03d16e7` and
  `git log` quoted above.
- **What would resolve it:** one line in README.md's reopening list, or a sentence saying
  the list is Amendment 8's three and that Amendment 9 adds a fourth.
- **Confidence:** HIGH — the omission and the commit order are both directly verifiable.
- **Invalidated by later commits?:** yes in principle — this is the last commit at the
  anchor, and a subsequent README edit would close it; nothing after 2026-09-02T09:50Z
  exists in the live repository as of my read.
- **Disclosed by authors?:** no. README.md:164-166 says "**A reply to the pending
  academic-tier question is a one-line register update, not a reopening.** No fourth venue
  is proposed" — which is about venues, not about the count of reopening conditions, and
  does not flag the omission.

---

### DRAFT-p1-register-8
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** "The Canadian doubt, registered before any measurement and
  never tested" (README.md), against Section 3's registered magnitudes
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "**The Canadian doubt, registered before any
  measurement and never tested:** the permitted categories are economic indicators,
  financial markets and climate — **the well-calibrated ones** — and a **30-day minimum
  maturity** removes the fast-resolving contracts." — PMExperiment/README.md:194-197
  (emphasis on "the well-calibrated ones" mine for locating; the phrase is unemphasised in
  the source).
- **Evidence:**
  - "the well-calibrated ones" is registered nowhere. Grep over the snapshot returns the
    phrase once, at README.md:196; the only other "well-calibrated" hits are the title of
    Page and Clemen (2013) (REGISTRATION.md:244, docs/BAND.md:56).
  - The register's own Section 3 attributes the **largest** cited magnitude — the one that
    sets the band's top — to a permitted category: "Krause … longshots priced below 30c
    settled YES 4.0 % of the time, a bias of **−0.077** — about 7.7 points — **inside a
    permitted-category (economic-indicator) series**" — PMExperiment/REGISTRATION.md:235-239.
    The band document counts that attribution as pointing **toward** survival inside the
    permitted subset (PMExperiment/docs/BAND.md:283), and Section 15.2 uses it to refuse
    BAND-NARROW: "The category clause is contradicted by Krause's permitted-category
    (economic-indicator) attribution" (REGISTRATION.md:417).
  - What the registration actually registered as the doubt is narrower and does not claim
    the categories are well calibrated: "**Registered expectation, stated before any
    measurement:** the effect is plausibly real in the unrestricted universe … **The doubt
    is the filter.**" — PMExperiment/HYPOTHESES.md:47-52. The only support for
    "well-calibrated" in the record is the companion CPI study at n = 95 contracts
    (REGISTRATION.md:239-243), which the register itself frames as evidence of
    heterogeneity, not of good calibration.
  - Direction: the sentence makes the unmeasured Canadian question look more likely to have
    come out negative, which supports the closure's comfort ("the method working, not a
    disappointment"). It is also attributed to the pre-registration ("registered before any
    measurement"), which it is not.
- **Recomputation (if any):** none.
- **What would resolve it:** drop "the well-calibrated ones", or cite a registered source
  for it and reconcile it with Section 3's permitted-category attribution of the 7.7-point
  figure.
- **Confidence:** MEDIUM — the phrase is a compressed gloss in a README, and one registered
  source (the CPI companion, n = 95) is consistent with it; the inconsistency with the
  band's top is nonetheless direct.
- **Invalidated by later commits?:** no — README.md is unchanged after `1ba50aa` at the
  anchor.
- **Disclosed by authors?:** no — the register nowhere flags that the README's
  characterisation of the permitted categories differs from Section 3's own attribution.

---

### DRAFT-p1-register-9
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the carried-forward requirement "an edge above 5.85 points"
  over the region 91–99c, in README.md and HYPOTHESES.md
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**BAND-OPEN**, fired 2026-08-29: over entry prices
  **91–99c held to resolution**, an edge above **5.85 points** at FX turnover k = 1 is
  required, against a registered band top of **8.00 points**." —
  PMExperiment/README.md:139-141; and "entry prices **91–99c** held to resolution, requiring
  an edge above **5.85 points** at the registered FX turnover k = 1" —
  PMExperiment/HYPOTHESES.md:130-133.
- **Evidence:**
  - 5.85 points is the requirement at the bucket **midpoint** 95c, not over the region.
    REGISTRATION.md:422-423 states the range correctly — "requiring an edge above **5.85
    points** at the binding k = 1 — 5.73 points at 91c rising to **5.97** at 99c" — and
    docs/BAND.md:316-318 likewise. Both carried-forward statements drop the range and state
    the midpoint value as the requirement for the whole region.
  - Recomputed from the registered constants: R_H(0.91) = 0.0573, R_H(0.95) = 0.0585,
    R_H(0.99) = 0.0597. Stating 5.85 as *the* requirement over 91–99c understates it by up
    to 0.12 points at the top of the region, i.e. it overstates the surviving margin there
    by 0.12 of the 2.15 points the register calls the surviving share (the true surviving
    margin at 99c is 2.03 points).
  - HYPOTHESES.md is the document whose stated job is to carry "the figure that closed it,
    with its n" so a question is not re-asked without it (:5-9, :78-83); it is the one place
    the range most needs to survive.
- **Recomputation (if any):** inputs registry.py:53-66 and Amendment 4's
  `FX(p) = 0.03·p/k` (REGISTRATION.md:799); method `R_H(p) = 0.02 + 0.01 + 0.03p`; result
  0.0573 / 0.0585 / 0.0597 at p = 0.91 / 0.95 / 0.99, margins to the band top 0.02270 /
  0.02150 / 0.02030. Script `.../work/agentB-PM-p1/recompute.py`.
- **What would resolve it:** carry "5.73 at 91c to 5.97 at 99c" into README.md and
  HYPOTHESES.md alongside the 95c figure, as REGISTRATION.md and docs/BAND.md already do.
- **Confidence:** HIGH — arithmetic over registered constants; the register itself states
  the range.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** yes in the register and the band document
  (REGISTRATION.md:422-423, docs/BAND.md:316-318); the finding is that it did not travel
  into the two documents that carry the verdict forward.

---

## What I checked and found sound

The B-thesis did **not** hold on the following, each of which I opened expecting it to.

1. **The registration was not edited in place.** I extracted `REGISTRATION.md` at the
   Section 0 commit `9080186` (2026-08-29T07:37:33Z) and at the anchored SHA and diffed
   everything above `## 15. Results`: **byte-identical, 366 lines both sides, diff exit 0.**
   The cost model (Section 2), the effect band (Section 3), the gate map (Section 0.3), the
   planning counts (0.4), the access gate (0.5), outcome blindness (10) and the cost floor
   (11) are exactly as registered before the first request. Section 16 gained only a
   prepended annotation, and the annotation says so ("The paragraph below stands unedited as
   it was registered on 2026-08-29", REGISTRATION.md:640-641) — verified by diff.

2. **The band arithmetic reproduces exactly.** Every figure in Section 15.2 and in the
   docs/BAND.md table recomputes from the registered constants: R_H and R_X at all ten
   bucket midpoints at k = 1, k = 12 and k → ∞; 0.0585 / 0.0785 at 95c; 0.0573 at 91c;
   0.0597 at 99c; 0.0565 at 88.3c; the 2.15-point margin; C(0.95) = 0.0785; the 0.0015
   round-trip margin; Amendment 4's 0.0015 + 0.00045 = 0.00195 slack and the held route's
   comparable 0.00135. Section 0.4's inversions (475, 29.6875→30) are right for the
   dispersion they name.

3. **The exit-route exclusion is applied against the repository's own interest.** Route X
   clears the band top at 95c by 0.0015 while the register's own named FX understatement is
   0.00195; the register excludes route X on exactly that ground (REGISTRATION.md:427-429,
   docs/BAND.md:261-263). I recomputed 0.0015 − 0.00195 = −0.00045: the exclusion is
   correct and it removes a route that would otherwise have widened the positive.

4. **BAND-OPEN is never written as evidence of an edge.** I grepped for any sentence that
   converts it. Every occurrence carries the refusal — REGISTRATION.md:444-446,
   REGISTRATION.md:614-618, README.md:143-145, report.md:449-451, HYPOTHESES.md:147-151,
   DECISIONS.md:729-731 — and a test pins two of them
   (tests/test_honesty.py:226-232). This is the single most obvious place a repository would
   overclaim, and it does not.

5. **The closure does not pretend to be the registered closure.** Section 16's conditions
   are recorded as never met, with the gap stated rather than smoothed
   (REGISTRATION.md:605-612, :636-641; report.md:458-462; DECISIONS.md:720-727). The
   operator's cost decision is filed in its own category and explicitly denied evidentiary
   force (Amendment 7, REGISTRATION.md:1056-1067; ADR-017, DECISIONS.md:648-664).
   "EXISTS-AND-UNTRAVELLED" is a precise label and it is defended precisely.

6. **The self-conviction is real, not decorative.** ADR-012's own claim that "Stage A's
   Kalshi finding met that bar" is convicted at DECISIONS.md:434-440 on a measurable ground
   (`Effective` 0 occurrences, `Last Updated` 0); Amendment 1's premise is retracted in
   Amendment 6 (REGISTRATION.md:918-965) after moving the entire measurement venue on it;
   the Dune read is convicted of publishing PROHIBITED from an unread instrument
   (ADR-015, DECISIONS.md:523-540). Each correction narrows the record. I looked for a
   correction that rescued a verdict rather than recording a falsification and found none —
   Stage D's "Every correction made the record narrower or weaker. None changed a verdict."
   (report.md:303-304) checks out against the ADRs.

7. **Stage D's completeness caveat was written before it was needed, not after.** "'There
   is none' is a verdict over what was read" appears in the Stage D material committed
   `7b5a751`/`baa2bf3` on 2026-08-30 (UTC), and the Kalshi reply that vindicated it arrived
   2026-09-01. I checked git for a retro-fit and found none: the caveat is in the Stage D
   commits, not added at closure.

8. **No amendment lowered a registered cost component toward H1.** Amendment 4 explicitly
   refuses to move the binding FX model to k > 1 on the ground that it "lowers the cost floor
   in the direction that helps H1" (REGISTRATION.md:809-813), and the code enforces
   k = 1 as the default (band.py:52, 71, 86, 102, 115). Amendment 2's held-to-resolution
   route does charge one fee side rather than two, which lowers the floor from 0.0785 to
   0.0585 at 95c — but it is a numbered amendment made **before** the gate fired
   (`f686036` 18:05Z vs `32dc10a` 19:24Z), it is consistent with Section 2's own registered
   note that "settlement carries no fee" (REGISTRATION.md:199), and the round-trip figure is
   reported beside it throughout (REGISTRATION.md:448-454, HYPOTHESES.md:142). BAND-OPEN
   does not depend on it: BAND-EMPTY fails to fire on the round-trip route too. I expected
   this to be the finding and it is not one.

9. **The "zero requests / zero dollars / no statistic" totals are consistent.** The one
   fact that could have contradicted them is disclosed rather than rounded away: "Stage A's
   11 keyless probe requests did receive two settled records carrying `last_price_dollars`
   and `result` — that is recorded here rather than rounded to 'no market price was ever
   read', because rounding it is precisely the kind of claim this repository exists to
   refuse" (README.md:101-106; the same correction at progress.md:1506-1507). The 11-vs-13
   difference between README.md:102 and ADR-007's "whole probe budget was 13 requests"
   (DECISIONS.md:131-132) reconciles: 11 keyless *market* requests inside a 13-request
   budget.

10. **H1 is left OPEN rather than closed, correctly.** I checked whether the register closes
    a hypothesis it had no right to close, and whether any open hypothesis should already
    have closed on its own rule. H1's entry stays "Status: OPEN" (HYPOTHESES.md:30) while
    the file's terminal line says "unmeasurable" (:14-15) — consistent, because
    REGISTRATION.md:609 states "**H1 therefore does not close under Section 16 at all.**"
    H2 and H3 stay PARKED with the reason attached (HYPOTHESES.md:323-324). H1t is UNTESTED
    with its three grounds carried everywhere it appears, including the cross-repository
    MLCryptoEngine H2 AUC 0.501 figure.

11. **The guards do fail when mutated, and the harness faults are recorded.** `tests/
    test_guards.py:80-85` proves the outcome-blindness scanner can fail;
    `:139-166` proves each ADR-012 element is load-bearing and first asserts the baseline is
    admissible ("a mutation that does not mutate is not evidence"). The three occasions on
    which the mutation harness produced a false green are recorded as ADRs, not hidden
    (ADR-021, DECISIONS.md:785-796; ADR-020, :769-781; progress.md Entries 7.1 and 9.1), and
    progress.md:1229 records the affected mutations being re-run. README.md:230-232's
    blanket "every guard … verified by mutation" is therefore supported, if generously.

12. **`pmexperiment/admissibility.py`'s disclosed blind spot is the real one.** I read the
    module looking for undisclosed weaknesses beyond the paraphrase gap the authors report
    (README.md:47-49, DECISIONS.md:598-609). `missing_elements()` does check that dates
    *parse*, not merely that they are present (`_is_iso_date`, :136-144), and `admit()`
    fails closed on a claimed PROHIBITED as well as a claimed PERMITTED (:159-180) — both
    stronger than the ADR requires. `MIN_DOCUMENT_TEXT_RATIO = 0.05` rests on a single
    measured observation, but the comment says so in as many words ("The one client-rendered
    page this repository has measured sets this bar", :39-40) and names its direction of
    error, so I did not raise it.

---

## Live-repo access log

Live repository touched: `/home/kiros-li/Documents/GitHub/PMExperiment`, read-only, git
history only (`status --porcelain`, `log --format --date=iso-strict`, `show <sha> --stat`,
`show <sha>:REGISTRATION.md`). No working-tree file was opened for writing and no untracked
data was read. Read window 2026-09-05T18:20Z–2026-09-05T18:37Z.

Before first access (`git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain`):

```
(empty output, exit 0)
```

After last access (same command, 2026-09-05T18:37:27Z):

```
(empty output, exit 0)
```

Clean before and after; nothing of mine, and no pre-existing dirt, in this repository.
