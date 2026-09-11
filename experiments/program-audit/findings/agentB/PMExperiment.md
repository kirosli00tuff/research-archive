# Agent B — PMExperiment

**Repository:** PMExperiment, anchored SHA `03d16e71dbf25a86c529884662d02136f8e82334`
(main, 2026-09-02, closed project).
**Snapshot read:** `/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/`.
Live repository touched read-only for git history only; access log at the end.
**Direction:** B — the program claimed more than it earned.
**Findings:** 15, consolidated from two draft parts (`p1-register`, `p2-progress`).

---

## Summary — the strongest case for the thesis in this repository

This repository produced exactly one substantive quantitative verdict, BAND-OPEN, and
that verdict does not survive its own arithmetic. The region it registers as "the only
region the power gate may fire over" — entry prices 91–99c — is arithmetically empty over
five of its nine cents, because the edge is defined as a gap between a true probability and
the entry price and so cannot exceed 1 − p; at the 0.950 midpoint at which every headline
figure in the repository is quoted, the largest edge that can exist is 0.0500 against a
stated requirement of 0.0585. The "10 of 10 buckets" that carry the "not BAND-EMPTY" leg
are counted over all ten deciles, at eight of which the same document says supplying a
magnitude "would violate standing rule 5"; inside the cell the band is actually registered
for the count is 2 of 2. The one input that keeps the verdict positive-flavoured — a band
top of 0.08 rounded up from a single published 7.7-point figure — carries no n, no
retrievable identifier and no fetch record, and the repository's own standing rule 4
("Verify every external figure live") was never applied to it, while the same repository
recorded UNMEASURED against a 1.2-billion-row dataset for one missing date. The shipped
power gate that the repository's central self-claim rests on ("This repository followed
Insider, not NPD") is a 2-standard-error bar with no power term, i.e. ≈50 % power, with
clustering and multiplicity deferred past the gate that consumes them.

Against that: the repository is unusually well self-disclosed, its band arithmetic
reproduces cell for cell, no bar was moved after a result existed, and it refuses at every
turn to write BAND-OPEN as evidence of an edge. The findings below are about arithmetic and
design that the disclosures do not reach — not about disclosure failures.

---

### AUDIT-B-PMExperiment-1

- **ID:** AUDIT-B-PMExperiment-1
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** BAND-OPEN, the repository's only positive verdict, and the
  surviving region it registers (entry prices 91–99c held to resolution, k = 1)
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Entry prices 91–99c — the favourite half of the
  registered tail cell — held to resolution, on either side of the book (YES on a
  documented-underpriced favourite, or NO on a documented-overpriced longshot), requiring an
  edge above 5.85 points at the registered turnover k = 1: 5.73 points at 91c rising to 5.97
  points at 99c.**" — PMExperiment/docs/BAND.md:314-318. Registered in the same words at
  PMExperiment/REGISTRATION.md:420-424.
- **Evidence:**
  - The break-even rule is registered as a requirement on the **true probability**:
    "Break-even therefore requires the true probability to exceed the market price by … |
    held to resolution | one side, $0.02 | **≥ 2.0 percentage points** |" —
    PMExperiment/REGISTRATION.md:717-722; restated in the form the inference consumes at
    PMExperiment/REGISTRATION.md:334-335 and in code, "Break-even edge: the true probability
    must exceed the price by this." — PMExperiment/pmexperiment/band.py:73. A probability
    cannot exceed 1, so at entry price p the largest edge that can exist is **1 − p**.
  - That bound appears nowhere in the repository. `grep -rnE "cannot exceed|attainab|feasib"`
    over every tracked `*.md` and `*.py` in the snapshot returns **0 hits** (n = 6,769 lines
    across the 13 principal documents and modules).
  - The requirement curve is R_H(p) = 0.03 + 0.03p (PMExperiment/docs/BAND.md:219;
    `fee_borne + HALF_SPREAD_USD + fx_cost` at PMExperiment/pmexperiment/band.py:80, over
    `FEE_PER_SIDE_USD = 0.02` PMExperiment/pmexperiment/registry.py:53, `HALF_SPREAD_USD =
    0.01` :55, `FX_PER_DIRECTION = 0.015` × `FX_DIRECTIONS = 2` :56-57). Feasibility needs
    1 − p > 0.03 + 0.03p, i.e. p < 0.97/1.03 = **0.941748**.
  - Inside the fired region (n = 9 integer-cent prices): 91c, 92c, 93c, 94c are feasible;
    **95c, 96c, 97c, 98c and 99c are arithmetically empty — 5 of the 9 cents the verdict
    names.** At 99c the document's own stated requirement of 5.97 points implies a true
    probability of **1.0497**.
  - **The region's registered representative price is one of the empty ones.**
    `bucket_midpoint((91,99))` = 0.950 (PMExperiment/pmexperiment/band.py:108-111, pinned at
    PMExperiment/tests/test_band.py:177), and every headline figure in the repository is
    quoted there: PMExperiment/REGISTRATION.md:409-412, PMExperiment/docs/BAND.md:15-18,
    PMExperiment/progress.md:362-368, PMExperiment/report.md:61-64,
    PMExperiment/README.md:139-141, PMExperiment/HYPOTHESES.md:130-133. At p = 0.950 the
    ceiling is **0.0500** against a requirement of **0.0585** — a shortfall of **0.0085**,
    not a margin.
  - The published margin is measured against an effect that cannot exist at the price it is
    measured at: "route H clears by 4.84 points at 1–10c falling to **2.15 points** at
    91–99c" — PMExperiment/docs/BAND.md:257-259. The 2.15 points is 0.0800 − 0.0585 at
    p = 0.950, where the ceiling is 0.0500.
  - The band top itself is unattainable over most of the region: an underpricing of 0.08
    requires p ≤ 0.92, so the surviving window against the **registered** band is
    91c (0.0573, 0.0800], 92c (0.0576, 0.0800], 93c (0.0579, 0.0700], 94c (0.0582, 0.0600] —
    at 94c a window **0.18 points wide**. The round-trip route is infeasible from 93c up:
    R_X(p) = 0.05 + 0.03p feasible only for p < 0.95/1.03 = **0.922330**.
- **Recomputation:** inputs `registry.py:53-57`; R_H per `band.py:68-80`; bucket 91–99 per
  `registry.py:24`. Method: for each integer cent p in 0.91…0.99 compare R_H(p) with the
  ceiling 1 − p and with min(0.08, 1 − p). Script
  `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-PM-consol/verify.py`. Result:
  91c 0.0573/0.0900 feasible; 92c 0.0576/0.0800 feasible; 93c 0.0579/0.0700 feasible;
  94c 0.0582/0.0600 feasible; 95c 0.0585/**0.0500 empty**; 96c 0.0588/0.0400 empty;
  97c 0.0591/0.0300 empty; 98c 0.0594/0.0200 empty; 99c 0.0597/0.0100 empty. The same script
  reproduces the repository's published Pass 1 table (docs/BAND.md:199-210) exactly at every
  cell before the bound is applied.
- **What would resolve it:** restating the surviving region as 91–94c held to resolution
  with the per-cent windows shown and re-quoting the headline requirement at a feasible
  price rather than at the 0.950 midpoint; or a registered argument that the edge is not
  bounded by 1 − p at entry price p, which would contradict REGISTRATION.md:717-722 and
  Section 11.
- **Confidence:** HIGH — the bound follows directly from the repository's own definition of
  the edge as a probability difference at a stated entry price, and the arithmetic
  reproduces the repository's own published figures exactly before applying it.
- **Could later commits invalidate this?:** no — the anchor is the terminal commit of a
  closed project, and Sections 0–14 of REGISTRATION.md are byte-identical from `9080186` to
  `03d16e7` (verified by diff, 367 lines both sides, exit 0), as are `registry.py` and
  `band.py`.
- **Disclosed by the authors?:** **no.** The qualifications carried with the verdict
  (PMExperiment/docs/BAND.md:330-338, PMExperiment/REGISTRATION.md:431-446,
  PMExperiment/README.md:143-149) name the missing n, the absence of a magnitude at that
  bucket and the thinness of the band; none states that most of the fired region requires a
  probability above 1.

---

### AUDIT-B-PMExperiment-2

- **ID:** AUDIT-B-PMExperiment-2
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the power gate — `pmexperiment/power.py`, `registry.Z_CRITICAL`,
  REGISTRATION.md Sections 0.3, 0.4, 8 and 9 — the artifact the whole repository is framed
  around
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **GO** | MDE ≤ 0.02 | the design resolves the
  entire published band; Stage B is authorized for that universe against the registered
  target |" — PMExperiment/REGISTRATION.md:110. With the definition: "The minimum detectable
  effect for a cell, with z = 2.0 two-sided: MDE = z · sqrt(v̄ / n_T)" —
  PMExperiment/REGISTRATION.md:99-101 (restated at :301-302).
- **Evidence:**
  - `Z_CRITICAL: float = 2.0` — PMExperiment/pmexperiment/registry.py:9, consumed at
    `return registry.Z_CRITICAL * math.sqrt(mean_dispersion / tail_count)` —
    PMExperiment/pmexperiment/power.py:45, pinned at PMExperiment/tests/test_power.py:24-30.
    **Nothing multiplies in a z for β.**
  - **No target statistical power is stated anywhere in the repository.**
    `grep -rniE "80 ?%|1 ?− ?β|z_?β|type II|false negative|statistical power|power of the"`
    over every tracked `*.md` and `*.py` returns **1 hit**, at progress.md:995, about a
    mutation-harness false negative — nothing on the gate. The only near-mention is the
    DEGRADED row's "with the achieved power stated beside the registered target"
    (PMExperiment/REGISTRATION.md:111), which never defines that target.
  - A quantity defined as 2 standard errors is the effect a two-sided 5 % test detects
    **about half the time**, not one a design "resolves": power = **0.5160** at α = 0.05
    two-sided, **0.5000** if the registered z = 2.0 is itself the critical value.
  - The bars therefore understate the enumeration a conventionally powered design needs by a
    factor of **1.962**: GO would need n_T ≈ **932.05 → 933** rather than the registered
    ≥ 475 (PMExperiment/REGISTRATION.md:128), and staying out of BLOCKED would need
    n_T ≈ **58.25 → 59** rather than ≥ 30 (:129).
  - **The BLOCKED bar flips.** At the registered planning dispersion and n_T = 30 the
    80 %-power MDE is **0.11148**, above the band top of 0.08, i.e. BLOCKED — while
    `fire_power_gate("P30", 30, 0.0475)` returns DEGRADED and the test suite pins that
    (PMExperiment/tests/test_power.py:51-55). The gate as shipped would pass a
    Canadian-permitted cell at a tail count a conventionally powered version of the same gate
    would block.
  - **Clustering is deferred past the gate that consumes it.** Section 8 reads "*To be
    registered after the gate fires.* The estimator, the interval construction, the
    clustering unit, and the trial grid with its multiplicity correction." —
    PMExperiment/REGISTRATION.md:293-295. The gate's n_T is a count of contracts
    (PMExperiment/REGISTRATION.md:53-54), while the benchmark that sets the band reports
    **46,282 contracts across 12,403 events** (PMExperiment/REGISTRATION.md:226-227) —
    m̄ = 3.7315 contracts per event. Assumption, direction named: at an assumed intra-event
    ICC of 0.10 / 0.25 / 0.50 the design effect is 1.273 / 1.683 / 2.366 and the true MDE is
    1.128× / 1.297× / 1.538× the registered one. The ICC itself carries no n in this
    repository; every value of it inflates the MDE, i.e. the shipped gate overstates power in
    one direction only. Two verdict cells are fired at z = 2.0 each ("Fired separately for
    U24 and P30", :104) with the multiplicity correction deferred to the same Section 8.
  - Direction of bias: toward GO/DEGRADED and away from BLOCKED — toward H1 staying open.
    That omission breaches the register's own preamble: "Every number in this document is
    **derived, measured, or labelled an assumption with its direction of bias named**." —
    PMExperiment/REGISTRATION.md:13-14. z = 2.0 is none of the three.
  - What rests on it: "**This repository followed Insider, not NPD**"
    (PMExperiment/README.md:190) and "**Follow Insider.** Compute the minimum detectable
    effect from dispersion and bucket counts alone, commit the gate before the measurement it
    judges" (PMExperiment/CLAUDE.md:63-65), against NPDExperiment quoted here as "a design
    that could not have detected an effect anywhere in the range it was testing"
    (PMExperiment/README.md:184-185).
- **Recomputation:** inputs z = 2.0 (`registry.py:9`; REGISTRATION.md:99-101), band edges
  0.02 / 0.08 (`registry.py:10-11`; REGISTRATION.md:103), planning v̄ = 0.0475
  (REGISTRATION.md:122-123; `tests/test_power.py:21`), clustering inputs
  REGISTRATION.md:226-227. Method: power of a two-sided test when the true effect equals the
  registered MDE; n = (z_{α/2}+z_β)²·v̄/effect² at 80 % power; design effect 1 + (m̄ − 1)ρ.
  Script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-PM-consol/verify.py`.
  Result: power 0.5160 (z_crit 1.96) / 0.5000 (z_crit 2.0); z₈₀ = 2.8016, n ratio 1.962;
  GO 475.00 → 932.05; BLOCKED edge 29.69 → 58.25; MDE at n = 30, 80 % power = 0.11148;
  m̄ = 3.7315, DEFF 1.273/1.683/2.366.
- **What would resolve it:** a numbered amendment stating the power level the gate is set at
  and either restating the required counts at that power or relabelling GO's consequence from
  "the design resolves the entire published band" to what 2 SE actually buys; plus a
  clustering unit and a multiplicity statement for the two verdict cells, moved ahead of the
  gate rather than deferred past it.
- **Confidence:** HIGH on the arithmetic and on the absence of any stated power level;
  MEDIUM on severity, because the gate never fired, so no realized verdict is wrong — what is
  wrong is a registered verdict row's stated consequence and the self-comparison built on it.
- **Could later commits invalidate this?:** no — `power.py`, `registry.py` and Sections 0.3,
  0.4, 8 and 9 are unchanged to the anchor and the project is closed.
- **Disclosed by the authors?:** **no.** The repository discloses that the gate never fired,
  that 475 and 30 are "planning figures" (REGISTRATION.md:131), that the power question
  remains unanswered (README.md:190-192), and that Section 8's clustering unit and
  multiplicity correction are unregistered (:293-295). It nowhere discloses the power level
  implied by z = 2.0, nor names that choice's direction of bias, nor treats clustering as an
  input the gate's own figure depends on.

---

### AUDIT-B-PMExperiment-3

- **ID:** AUDIT-B-PMExperiment-3
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the "10 of 10 buckets" figure that carries the "not BAND-EMPTY"
  leg of BAND-OPEN, and `pmexperiment.band.surviving_buckets`
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| BAND-EMPTY | **does not fire.** The registered
  band exceeds the required underpricing at 10 of 10 registered buckets, on both exit routes,
  at k = 1, at k = 12 and in the k → ∞ limit. |" — PMExperiment/REGISTRATION.md:416 (same
  figure at PMExperiment/docs/BAND.md:233 and :303-305, PMExperiment/progress.md:455-458).
- **Evidence:**
  - Section 3 registers the effect band in the tail cell **only**: "**Registered band: 0.02
    to 0.08 absolute probability points of miscalibration in the tail cell** (snapshot prices
    1–10c and 91–99c)" — PMExperiment/REGISTRATION.md:221-222, quoted into
    PMExperiment/docs/BAND.md:33-34.
  - The same band document states the consequence twice, in the opposite direction to the
    count: "The registered effect magnitude column is populated **only in the tail cell**,
    because Section 3 registers the band there and nowhere else; elsewhere it is absent, not
    zero." — PMExperiment/docs/BAND.md:195-197; and "| the eight non-tail deciles | **no
    effect magnitude is registered outside the tail cell.** Supplying one would violate
    standing rule 5. |" — PMExperiment/docs/BAND.md:325. Standing rule 5 is "**Absence is a
    recorded state, never a synthesized value.**" — PMExperiment/CLAUDE.md:27-28.
  - The code nevertheless applies `registry.EFFECT_BAND_HI` (0.08) at every decile:
    `surviving_buckets` iterates `registry.BUCKET_EDGES_CENTS` (all ten,
    PMExperiment/pmexperiment/registry.py:14-25) rather than `registry.TAIL_BUCKETS_CENTS`,
    which is defined one line below it at PMExperiment/pmexperiment/registry.py:26 —
    PMExperiment/pmexperiment/band.py:114-122. The test suite pins the ten-bucket reading:
    `test_band_top_survives_at_every_bucket_on_both_routes`,
    PMExperiment/tests/test_band.py:110-118.
  - So the deciding figure of the "does not fire" row is produced by supplying a registered
    magnitude at **8 of the 10 buckets** where the same page says supplying one "would violate
    standing rule 5". Inside the cell the band is registered for, the honest count is **2 of
    2**; and after this stage's own direction correction ("the registered magnitudes there are
    **overpricing**, so a buy has the wrong sign", PMExperiment/docs/BAND.md:324) only **1 of
    2** carries an exploitable registered magnitude — the 91–99c bucket, at which the two
    cited magnitudes are 0.020 and 0.030 (n = 313,972 contract prices on 46,282 contracts
    across 12,403 events) and "**both fail**" (PMExperiment/docs/BAND.md:247-252).
  - The verdict is not overturned by this alone (2/2 still clears existentially), but the
    published strength of the "not BAND-EMPTY" leg is inflated fivefold, and the figure is
    repeated as load-bearing in the register, the band document, the progress entry and the
    report.
- **Recomputation:** inputs bucket edges `registry.py:14-25`, tail buckets `registry.py:26`,
  `EFFECT_BAND_HI` `registry.py:11`, requirement curve `band.py:68-96`. Method: evaluate
  `band_top_exceeds_requirement` at each decile midpoint for both routes at k = 1, 12 and
  →∞, once over all ten deciles and once over the two registered tail buckets. Script
  `.../work/agentB-PM-consol/verify.py`. Result: all-deciles **10/10** for both routes at
  every k (reproduces the published figure); tail-cell-only **2/2** for both routes at every k.
- **What would resolve it:** reporting the BAND-EMPTY test over `TAIL_BUCKETS_CENTS`, or an
  explicit registered statement that the band extends outside the tail cell for the purpose of
  the BAND-EMPTY test (which would contradict Section 3 and docs/BAND.md:325).
- **Confidence:** HIGH — the two statements are 128 lines apart in one document and the code
  makes the choice explicit by iterating the wider constant while the narrower one is defined
  beside it.
- **Could later commits invalidate this?:** no — `band.py`, `registry.py` and Section 3 are
  unchanged to the anchor and the project is closed.
- **Disclosed by the authors?:** **no.** The tail-cell restriction is disclosed, and the
  exclusion of the non-tail deciles from the *surviving region* is disclosed
  (docs/BAND.md:325); the fact that the BAND-EMPTY count is nevertheless taken over all ten
  deciles is not reconciled anywhere.

---

### AUDIT-B-PMExperiment-4

- **ID:** AUDIT-B-PMExperiment-4
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the registered cost model applied to Amendment 2's second exit
  route ("exited before resolution"), and the crossing-point and cost-floor conclusions drawn
  from it
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The plain statement: **the registered cost floor
  runs entirely inside the registered effect band at every price.** The band's bottom is below
  the floor everywhere and its top is above the floor everywhere." —
  PMExperiment/docs/BAND.md:222-224 (same conclusion at PMExperiment/REGISTRATION.md:452-454,
  PMExperiment/progress.md:445-447, PMExperiment/report.md:97-99), and "**There are no
  crossings inside the tradeable price range.**" — PMExperiment/docs/BAND.md:214.
- **Evidence:**
  - The spread component is registered as "**1 cent half-spread, paid once at entry** |
    assumption. **A settlement exit crosses no spread.**" —
    PMExperiment/REGISTRATION.md:200, quoted into PMExperiment/docs/BAND.md:75. The
    justification for charging it once is that the modelled participant exits at settlement:
    "a Canadian retail individual funding in CAD, converting to USD, **holding one side of one
    contract to settlement**, and converting back" — PMExperiment/REGISTRATION.md:193-195.
  - Amendment 2 later added a second route that is **not** a settlement exit — "| exited
    before resolution | both sides, $0.04 | **≥ 4.0 percentage points** |" —
    PMExperiment/REGISTRATION.md:723 — and the spread component was never amended. The code
    charges exactly one half-spread on both routes:
    `return fee_borne(route) + registry.HALF_SPREAD_USD + fx_cost(entry_price, turnover)` —
    PMExperiment/pmexperiment/band.py:80; and the test suite pins the omission:
    `assert exited - held == pytest.approx(registry.FEE_PER_SIDE_USD)` —
    PMExperiment/tests/test_band.py:53 (test at :44).
  - A non-settlement exit crosses the book a second time, so the round-trip route is
    understated by one half-spread = **0.0100 at every price** (n = 10 registered deciles).
    That is **5.1×** the 0.00195 understatement the same document does quantify and does use
    to exclude the route: "Two registered simplifications, both leaning toward H1, neither
    revised … Their sum is **0.00195**" (PMExperiment/docs/BAND.md:181-186); "**Route X's
    margin at the favourite tail (0.0015) is smaller than the 0.00195 by which Section 2's FX
    base understates cost at the same price.**" (:261-263). The larger omission is not among
    the two.
  - With the exit half-spread charged, R_X(p) = 0.06 + 0.03p. Then R_X(0.95) = **0.0885**
    against a registered band top of **0.0800**, and R_X crosses the band top at p =
    **0.6667** — inside the tradeable range — which falsifies both quoted claims. The
    existential survival count on route X falls from **10/10 to 7/10** at k = 1 (the 71–80,
    81–90 and 91–99 deciles fail).
  - Direction of the error is toward H1, the direction Section 2 forbids revising in: "No
    component of this table may be revised after a result is seen; a better cost estimate
    enters only as a numbered amendment with its evidence." —
    PMExperiment/REGISTRATION.md:214-215. The point is not a post-hoc revision — it is that a
    component registered for a settlement-exit participant was carried unamended onto a route
    that does not settle.
  - The fired verdict is not overturned: route X was excluded from the surviving region anyway
    (PMExperiment/docs/BAND.md:326). What is wrong is the **reason** given for excluding it (a
    0.0015-vs-0.00195 slack argument, when the route in fact fails by 0.0085 at 95c) and the
    two "at every price" conclusions above.
- **Recomputation:** inputs `HALF_SPREAD_USD = 0.01` (`registry.py:55`), `FEE_PER_SIDE_USD =
  0.02` (:53), FX 0.03p (:56-57), route fee sides `band.py:27-30`, band top 0.08
  (`registry.py:11`). Method: recompute the Pass 1 table as published, then recompute route X
  with two half-spreads. Script `.../work/agentB-PM-consol/verify.py`. Result: published
  R_X(k=1) at the ten deciles 0.0517 / 0.0547 / 0.0576 / 0.0607 / 0.0636 / 0.0667 / 0.0697 /
  0.0727 / 0.0756 / 0.0785 — identical to PMExperiment/docs/BAND.md:199-210; with the exit
  half-spread, 0.0616 / 0.0646 / 0.0677 / 0.0706 / 0.0736 / 0.0766 / 0.0796 / 0.0827 / 0.0857
  / **0.0885**; band-top crossing at p = (0.08 − 0.06)/0.03 = **0.666667**; survivors 7/10.
- **What would resolve it:** a numbered amendment either charging a second half-spread on the
  exited-before-resolution route and restating the crossing-point and "runs entirely inside the
  band" conclusions, or registering an explicit reason why an early exit crosses no spread.
- **Confidence:** HIGH — the omission is visible in one line of code and one pinned assertion,
  and Section 2's own justification sentence names settlement as the reason the spread is
  charged once.
- **Could later commits invalidate this?:** no — `registry.py`, `band.py` and Section 2 are
  unchanged from their introduction to the anchor; the project is closed.
- **Disclosed by the authors?:** **no** — the two registered simplifications disclosed at
  PMExperiment/docs/BAND.md:181-187 total 0.00195 and do not include this one; the exit
  half-spread is not mentioned anywhere in the snapshot.

---

### AUDIT-B-PMExperiment-5

- **ID:** AUDIT-B-PMExperiment-5
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the exclusion of BAND-NARROW — the alternative verdict that
  would have recorded a split finding rather than passing a region to the power gate
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "- **not BAND-NARROW** — its condition requires the
  surviving region to lie *only* outside the permitted categories or below usable volume; the
  category clause is contradicted by Krause's permitted-category attribution, and the volume
  clause cannot be evaluated because no floor was ever registered;" —
  PMExperiment/docs/BAND.md:306-309 (same reasoning at PMExperiment/REGISTRATION.md:417 and
  PMExperiment/progress.md:479-481).
- **Evidence:**
  - Both legs of the exclusion are defective, and both defects point toward the more permissive
    verdict.
  - **Leg 1, the volume clause.** The register records the input as absent: "| **the volume
    floor of Section 1** | **never registered.** Stage A Task 2 never armed (ADR-006,
    2026-08-29), so the permitted filter's third axis has no value | BAND-NARROW's 'below
    usable volume' clause **cannot be evaluated**. Recorded in Pass 2 rather than filled with a
    guess. |" — PMExperiment/docs/BAND.md:113. An unevaluable clause was then treated as an
    unmet clause, which is the definition of synthesizing a value for an absent input, against
    the repository's own standing rule 5 — "**Absence is a recorded state, never a synthesized
    value.**" (PMExperiment/CLAUDE.md:27-28) — and against its own house summary "Refusals fail
    closed. Absence is a recorded state, never a synthesized value."
    (PMExperiment/README.md:227-228). Here the absence fails **open**.
  - The floor was in fact registered the next stage — "Registered as **Amendment 5**: total
    traded volume **≥ $1,000** per contract" (PMExperiment/progress.md:706-707;
    PMExperiment/pmexperiment/registry.py:50) — committed `f789079` 2026-08-30T03:34:00Z,
    **after** the band verdict of `32dc10a` 2026-08-29T19:24:06Z, and never exercised: "**Its
    cost in sample: not measured.** No enumeration ran" (PMExperiment/progress.md:714-715),
    n = 0 contracts enumerated.
  - **Leg 2, the category clause.** The only category attribution in the registration belongs
    to Krause: "a bias of **−0.077** — about 7.7 points — inside a permitted-category
    (economic-indicator) series" — PMExperiment/REGISTRATION.md:236-238. The same stage
    measured Krause's exploitable entry price at **0.883** and placed it outside the fired
    region: "| Krause, sub-30c settling 4.0 % | NO | **0.883** | 0.077 | **not recorded** |"
    (PMExperiment/docs/BAND.md:155); "| 81–90 | 0.855 | … | not registered — though Krause's
    exploitable complement lands here at 0.883 |" (:209); "The only one large enough is
    Krause's 7.7 points at an exploitable price of 88.3c — the 81–90 decile, **outside the cell
    the band is registered for.**" (:332-334). So the attribution used to defeat BAND-NARROW at
    91–99c belongs to a price bucket the same verdict excludes.
  - **No magnitude cited at 91–99c carries any category attribution at all.** The two cited
    there are Bürgi's 0.020 and 0.030 (PMExperiment/docs/BAND.md:210, n = 313,972 contract
    prices on 46,282 contracts across 12,403 events), and Section 3 attributes no category to
    either (PMExperiment/REGISTRATION.md:225-234).
  - What turns on it: BAND-NARROW's registered consequence is "recorded as a **split finding**:
    an effect may be real, priced, and unreachable." (PMExperiment/REGISTRATION.md:741);
    BAND-OPEN's is "the power gate proceeds against that region, and only that region." (:742).
    The difference between the two verdicts is the whole of what this repository's one positive
    licensed.
- **Recomputation:** none — this is a reading of the registered verdict conditions against
  inputs the stage itself recorded as absent or as attributed to a different price bucket.
- **What would resolve it:** a registered rule for how an unevaluable clause of a verdict
  condition is resolved (the register has none), or a category attribution for a magnitude
  cited at 91–99c.
- **Confidence:** MEDIUM-HIGH — every fact is stated by the repository itself; what is
  contested is the inference, and the repository's own fail-closed rule points the other way.
- **Could later commits invalidate this?:** no — Amendment 2's verdict definitions and Section
  15.2 are unchanged to the anchor and the project is closed.
- **Disclosed by the authors?:** **no** for the limitation raised here; **partly** for the facts it rests on — the absence of the volume floor
  (PMExperiment/docs/BAND.md:113) and Krause's 88.3c placement (:332-334) are both disclosed,
  and BAND-OPEN's thinness is disclosed at length. What is not disclosed anywhere is that the
  exclusion of BAND-NARROW depends on resolving an absent input in the permissive direction and
  on importing a category attribution from a price bucket the verdict excludes.

---

### AUDIT-B-PMExperiment-6

- **ID:** AUDIT-B-PMExperiment-6
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the closure framing — "What follows is the method working, not a
  disappointment" — and the operator prior of 5 to 8 percent (Amendment 7)
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "The operator's prior was 5 to 8 percent, so **a null
  was the modal expected outcome** before any of this began. What follows is the method
  working, not a disappointment." — PMExperiment/README.md:20-23. And in the report: "at a
  prior of 5 to 8 percent, **a null was the modal expected outcome from the beginning.** This
  ending is the method working, not a disappointment." — PMExperiment/report.md:443-445.
- **Evidence:**
  - The register's own binding prohibition: "**This prior may not be described anywhere as
    pre-registered, and no verdict in this repository may be read against it as though it had
    been.** It is a **stated** prior, dated at closure." —
    PMExperiment/REGISTRATION.md:1027-1029 (Amendment 7).
  - The prior did not exist during the project: "Section 13, `The operator prior`, reads *'To
    be filled by the operator before the gate fires, and recorded with the date it was
    given.'* It has read that since Section 0 was committed on 2026-08-29 and **it was never
    filled**. The operator's prior is now given as **5 to 8 percent** that H1 holds — supplied
    **2026-09-02**, at closure, after two gates had already fired." —
    PMExperiment/REGISTRATION.md:1018-1022. Git confirms the interval (n = 3 gate firings
    before the prior existed): Section 0 committed `9080186` 2026-08-29T07:37:33Z, the band
    gate fired `32dc10a` 2026-08-29T19:24:06Z, the two access gates fired `98ce2d4`
    2026-08-29T07:53:10Z and `1b3124e` 2026-08-30T03:40:52Z, and the prior first appears in
    `fe7e6b9` 2026-09-02T09:32:22Z.
  - "before any of this began" and "from the beginning" are assertions about the ex-ante state
    of expectation. No document records any operator expectation before 2026-09-02; Section 13
    is empty and a test pins it empty (PMExperiment/tests/test_honesty.py:517-525).
  - The framing was written to instruction, and the instruction's error was caught only in
    part. The Stage E operator prompt, logged verbatim, reads: "State the registered prior and
    that a null was the modal expected outcome, so the closure reads as the method working
    rather than as a disappointment." — PMExperiment/progress.md:1310. The repository corrected
    "registered" to "stated" (PMExperiment/progress.md:1504-1505, pinned by
    `test_the_operator_prior_is_never_described_as_pre_registered`,
    PMExperiment/tests/test_honesty.py:508-514) but kept the retrospective clause. The guard
    checks for the *presence* of the disclaimer 150 lines further down the README, not for the
    *absence* of the reading Amendment 7 forbids.
  - The consequence is the tone of the whole closure: that sentence is what converts "five
    stages, zero contracts enumerated, no statistic relating a price to an outcome" into "the
    method working, not a disappointment", in the opening block of the public README.
- **Recomputation:** none — the finding is documentary. Dates cross-checked against
  `git -C /home/kiros-li/Documents/GitHub/PMExperiment log --format='%h %aI %s'` (read-only;
  see the access log).
- **What would resolve it:** either a dated record of an operator prior given before
  2026-09-02, or a one-line edit dropping "before any of this began" / "from the beginning" so
  the prior is used only where Amendment 7 permits it — as the recorded input to the cost
  decision.
- **Confidence:** HIGH — both the prohibition and the two sentences that breach it are verbatim
  in tracked documents at the anchored SHA.
- **Could later commits invalidate this?:** no — the README block is the last README state
  (`1ba50aa`, 2026-09-02T09:36:29Z) and the repository is closed; a later commit could of
  course amend it.
- **Disclosed by the authors?:** **no** for the limitation raised here; **partly** for the facts it rests on — PMExperiment/README.md:168-175 ("stated, not
  pre-registered") and Amendment 7 both disclose that the prior is post-hoc, and Amendment 7
  itself makes a milder version of the same move ("which is the frame the closure should be
  read in", PMExperiment/REGISTRATION.md:1034). The specific breach — a retrospective claim
  about ex-ante expectation, in the README's opening block and in the report's closure — is
  disclosed nowhere.

---

### AUDIT-B-PMExperiment-7

- **ID:** AUDIT-B-PMExperiment-7
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the evidence standard as applied to the effect-band sources —
  standing rule 4, ADR-012's scope, and the README's symmetry-of-convenience claim
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "4. **Measured beats documented.** Verify every
  external figure live. A documented rate limit is a claim, not a measurement." —
  PMExperiment/CLAUDE.md:25-26. And the symmetry claim built on the same practice: "A venue may
  not be held to a **looser** reading than another because its verdict would be more convenient
  — and **the rule runs both ways.**" — PMExperiment/README.md:53-54.
- **Evidence:**
  - **No effect-band source was ever verified live, and none carries a fetch record.**
    `docs/ACCESS.md` and `docs/LICENCES.md` record fetch dates, byte counts and HTTP codes for
    the permission documents (11 `Fetched` stamps between them — 3 in ACCESS.md, 8 in
    LICENCES.md). They record **none** for any of the three effect-band sources (Bürgi, Krause,
    Page-Clemen); "Krause" appears **0 times** in either file.
  - **The deciding source carries no retrievable identifier.** The full citation is "Krause,
    *Market Efficiency and the Favorite-Longshot Bias in Unemployment Prediction Markets*,
    2026" — PMExperiment/REGISTRATION.md:235-236 — with no venue, no DOI, no SSRN number and no
    page, while the *companion* study in the very same bullet is given as "SSRN 7087538, 95
    contracts over 12 months" (:239-240). `grep -rn "Krause" --include=*.md --include=*.py`
    over the whole snapshot returns **32 mentions**, of which **0** carry a DOI, SSRN number,
    URL or arXiv/NBER identifier.
  - **The evidence procedure was scoped so that it can never fire over this input.** ADR-012 is
    registered as governing claims about permission only: "A claim in this repository about
    what a venue's terms permit carries **a quoted clause, the document's effective date, and
    the date it was fetched** — or it is recorded as unmeasured and the stage proceeds as if
    permission were absent." — PMExperiment/DECISIONS.md:367-370. Every negative in this
    repository was decided under it; the one positive-flavoured verdict was decided against
    literature figures to which neither ADR-012 nor standing rule 4 was applied.
  - **The asymmetry with the standard applied to the negatives, in figures.** A dataset
    documenting all four gate inputs over **1,201,580,990 rows** (2022-11-21 → 2026-04-28) was
    recorded UNMEASURED because "**neither the dataset card nor the CC BY 4.0 legal code prints
    any date**" — PMExperiment/DECISIONS.md:462-463. The repository's own Stage A finding was
    convicted on two elements of three (`Effective` 0 occurrences, `Last Updated` 0) —
    PMExperiment/README.md:67-69. The Kalshi institutional reply was recorded UNMEASURED for
    want of an effective date and a quotation — PMExperiment/REGISTRATION.md:546-556. Against
    that, the single input that keeps the positive-flavoured verdict alive was admitted with
    **no n, no identifier and no fetch record**, and never tested by any procedure
    (n = 3 candidate routes refused on the strict standard vs 1 input admitted on none).
  - The register's own preamble makes the omission a breach of its own rule: "Every number in
    this document is **derived, measured, or labelled an assumption with its direction of bias
    named**." — PMExperiment/REGISTRATION.md:13-14.
- **Recomputation:** none. Counts are greps over the snapshot, quoted above with their
  patterns.
- **What would resolve it:** applying standing rule 4 to the effect-band sources — a fetch
  record with date, byte count and status for each, in the shape `docs/ACCESS.md` already uses
  for permission documents — or a numbered amendment recording explicitly that literature
  figures are exempt from rule 4 and from ADR-012, with the direction of bias of that exemption
  named.
- **Confidence:** HIGH — the absence of any fetch record and of any identifier is verifiable by
  grep over the whole snapshot, and the scope sentence for ADR-012 is quoted verbatim.
- **Could later commits invalidate this?:** no — Section 3, CLAUDE.md and DECISIONS.md's
  ADR-012 are unchanged to the anchor and the project is closed.
- **Disclosed by the authors?:** **no.** The repository discloses that Krause's *n* is missing
  (see AUDIT-B-PMExperiment-8) but nowhere discloses that (a) the source carries no retrievable
  identifier while its own companion study does, (b) standing rule 4's live-verification
  requirement was never applied to any effect-band source, or (c) the asymmetry between that
  admission and the UNMEASURED verdicts issued against candidates missing a single element.

---

### AUDIT-B-PMExperiment-8

- **ID:** AUDIT-B-PMExperiment-8
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the registered effect-band top of 8.00 points — the single input
  that produces BAND-OPEN
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3 *(capped: the core limitation is disclosed by the authors — see below)*
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**In one sentence: BAND-OPEN — a surviving region
  exists that the permitted subset admits, at entry prices 91–99c held to resolution, requiring
  5.85 points of underpricing at the registered FX turnover against a registered band whose top
  is 8.00 points.**" — PMExperiment/REGISTRATION.md:409-412. And the bar it is judged against:
  "Its top, 0.08, rounds the largest single-category published figure, Krause's 7.7 points. The
  gate (Section 0.3) is judged against this band and nothing else." —
  PMExperiment/REGISTRATION.md:254-256.
- **Evidence:**
  - **The band's top is the only thing that makes BAND-OPEN fire.** Recomputed from the
    registered constants: with the registered top 0.08, 10 of 10 buckets survive on both routes
    at every k; with the top set instead to the largest cited magnitude that carries an n —
    Bürgi's **0.030**, n = 313,972 contract prices on 46,282 contracts across 12,403 events
    (PMExperiment/REGISTRATION.md:226-231) — **0 of 10 buckets survive on either route at
    k = 1, k = 12 or k → ∞, i.e. the registered verdict flips to BAND-EMPTY.** With the
    unrounded 0.077, route X already loses a bucket at k = 1 (9/10).
  - **The top carries no n.** "**The band's top carries no n** (standing rule 13). Bürgi sets
    the bottom with 313,972 contract prices …; Krause sets the top, and no sample size for it
    appears anywhere in this document." — PMExperiment/REGISTRATION.md:440-443; "**Krause's n
    is nowhere in the registration**" — PMExperiment/DECISIONS.md:267; "| **Krause's n** |
    **absent from the registration** …" — PMExperiment/docs/BAND.md:115.
  - **Its own exploitable price is outside the fired cell.** Krause's figure is measured at
    longshots priced below 30c (PMExperiment/REGISTRATION.md:236-237); the stage's own
    direction correction put its exploitable entry price at **0.883** — the 81–90 decile —
    "**outside the cell the band is registered for**" (PMExperiment/docs/BAND.md:332-334,
    :155, :209). Section 3 nevertheless transplants that magnitude into a band declared "in the
    tail cell (snapshot prices 1–10c and 91–99c)" (PMExperiment/REGISTRATION.md:221-222), and
    Section 2's non-revision rule (:214-215) then locked it in.
  - **Everything actually cited at the fired bucket fails.** "With the registered k = 1, both
    magnitudes cited at 91–99c fail: | Bürgi, 5c/3 % → NO at 95c | 0.950 | 0.020 | 0.0585
    **fail** … | Bürgi, 95c/98 % → YES at 95c | 0.950 | 0.030 | 0.0585 **fail** …" —
    PMExperiment/docs/BAND.md:247-252; at the FX-free limit the better of the two is a "**dead
    heat**" (:252). So the positive is carried by exactly one number, from one source, at a
    price one decile away, with no sample size.
  - **What it binds.** The region derived from that top is carried forward as a constraint on
    any future work — "**A reopened measurement starts at the power gate over 91–99c held to
    resolution and no other region**" (PMExperiment/REGISTRATION.md:1109-1111) — and the band's
    thinness is one of the two stated inputs to the operator's closure decision (:1046-1054).
- **Recomputation:** inputs `registry.py:53-57` and :66; routes per Amendment 2
  (REGISTRATION.md:720-723); `FX(p) = 0.03·p/k` per Amendment 4. Method:
  `R(p, sides, k) = 0.02·sides + 0.01 + 0.03·p/k`; a bucket survives when `R(midpoint) <
  band_top` (the existential test `band_top_exceeds_requirement`,
  PMExperiment/pmexperiment/band.py:83-96). Script `.../work/agentB-PM-consol/verify.py`.
  Result:
  ```
  top = 0.080 (Krause 7.7 rounded up, n absent):  k=1 H 10/10 X 10/10; k=12 10/10 10/10; k→∞ 10/10 10/10  → not BAND-EMPTY
  top = 0.077 (Krause unrounded,       n absent): k=1 H 10/10 X  9/10; k=12 10/10 10/10; k→∞ 10/10 10/10  → not BAND-EMPTY
  top = 0.030 (Bürgi, n = 313,972 prices):        k=1 H  0/10 X  0/10; k=12  0/10  0/10; k→∞  0/10  0/10  → BAND-EMPTY
  ```
  The published required-underpricing table reproduces exactly: R_H(0.95) = 0.0585,
  R_X(0.95) = 0.0785, R_H(0.91) = 0.0573, R_H(0.99) = 0.0597, margin at 0.95 = 0.0215. Krause's
  placement also reproduces: 0.04 + 0.077 = 0.117 mean bucket price, complement 0.883,
  NO-side underpricing 0.96 − 0.883 = 0.077.
- **What would resolve it:** a band top sourced to a magnitude measured at, or exploitable at,
  91–99c with its n; or a numbered amendment restating the top from a source that carries an n,
  with the band verdict re-fired against it.
- **Confidence:** HIGH on the arithmetic and on the absence of an n; MEDIUM on materiality,
  because the repository states every element of this itself and refuses to read BAND-OPEN as
  evidence of an edge.
- **Could later commits invalidate this?:** no — Sections 0–14 of REGISTRATION.md are
  byte-identical from `9080186` to the anchor (diff exit 0, 367 lines both sides), Amendment 2
  fixes the band as "computed once" (:744-745), and the project is closed.
- **Disclosed by the authors?:** **yes — and it is disclosed prominently, repeatedly, and in
  every conclusion-bearing document.** PMExperiment/REGISTRATION.md:433-443 (qualifications 1
  and 2, "registered with the verdict and not separable from it");
  PMExperiment/README.md:146-149 ("The band survives on its top alone, and that top is set by
  the one source whose **n the registration never recorded**.");
  PMExperiment/docs/BAND.md:330-336; PMExperiment/DECISIONS.md:265-270;
  PMExperiment/report.md:113-121. **This finding is therefore recorded at S3 and is not
  presented as a discovery.** What it adds to the authors' own disclosure is only the
  counterfactual: substituting the largest n-carrying magnitude for the top flips the verdict
  to BAND-EMPTY at 0 of 10 buckets on both routes at every k. The separate, undisclosed
  grounds — no retrievable identifier, no live verification, and the asymmetric standard — are
  recorded as AUDIT-B-PMExperiment-7 and are not double-counted here.

---

### AUDIT-B-PMExperiment-9

- **ID:** AUDIT-B-PMExperiment-9
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the made-dates of Amendments 1–3 — including Amendment 2, which
  defines the verdict rows the repository's only positive was judged against — and of the
  ADR-006(2)/ADR-007(2)/ADR-008 trio
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Made 2026-08-30.** A new gate, ordered ahead of the
  power gate, because it is free and may be decisive on its own." —
  PMExperiment/REGISTRATION.md:707, under "### Amendment 2 — the fee-versus-edge band fires
  before any measurement" (:705) — against "### 15.2 The fee-versus-edge band, **fired
  2026-08-29**: BAND-OPEN" (:402) and "**Fired on Amendment 2's registered definitions**"
  (:404).
- **Evidence:**
  - As written, the register says the verdict fired a day **before** the amendment that defines
    its verdict rows was made. The stage entry agrees with the verdict's date: "## Entry 5 —
    Stage B: the fee-versus-edge band — 2026-08-29" (PMExperiment/progress.md:360).
  - **n = 6 document entries carry the wrong stamp, from one commit.** Amendment 1 "**Made
    2026-08-30, before any statistic relating a price to an outcome exists.**"
    (PMExperiment/REGISTRATION.md:667), Amendment 2 (:707), Amendment 3 (:751), and
    PMExperiment/DECISIONS.md ADR-006(2) "**Status:** accepted, 2026-08-30" (:140), ADR-007(2)
    (:160), ADR-008 (:180).
  - Git settles the actual order, and the actual order is sound: `f686036` "docs: amendments
    1-3 — Polymarket measures the phenomenon, the fee band fires first", author date
    **2026-08-29T11:05:26-07:00 = 2026-08-29T18:05:26Z**. The Stage B prompt log `e2d8f10`
    landed 19:07:37Z, the band arithmetic `9b4bd4f` 19:15:55Z, Amendment 4 `4d75f66` 19:17:21Z,
    and the verdict `32dc10a` 19:24:06Z — so the amendment preceded the arithmetic by 70
    minutes and the verdict by 79. `git show f686036:REGISTRATION.md` shows "**Made
    2026-08-30**" already present at lines 430, 470 and 514 of that revision, so the stamp is
    wrong under both local time (−07:00) and UTC.
  - **The register contradicts itself on the same page.** Amendment 4 is stamped "**Made
    2026-08-29, before the band gate fired**" (PMExperiment/REGISTRATION.md:783) yet is
    appended *after* three amendments stamped a day later; the same inversion appears in the
    hypothesis register, where "## Amended 2026-08-30 — the venue split"
    (PMExperiment/HYPOTHESES.md:87) precedes "## Amended 2026-08-29 — the fee band fired
    BAND-OPEN" (:119). ADR-009 and ADR-010, which report Stage B's own work, are stamped
    "accepted, 2026-08-29" (PMExperiment/DECISIONS.md:210, :276) and sit *after* the 08-30 trio
    in an append-only file. The numbering note compounds it: "## Note on numbering, **recorded
    2026-08-29**, not repaired" describing "the pair **dated 2026-08-30**"
    (PMExperiment/DECISIONS.md:195-199).
  - The repository corrected exactly this class of error once, and stated the principle:
    "**Entry 6 states it was logged at 2026-08-29T19:32Z. That figure is wrong.** It was
    extrapolated from Entry 5.1's measured 19:28:45Z rather than read from the clock … **a
    timestamp inferred from a previous timestamp is documented, not measured.**" —
    PMExperiment/progress.md:652-663. The correction was never applied backwards to Entry 3 or
    to Amendments 1–3.
  - Why it matters here specifically: this repository makes dates load-bearing evidence by its
    own rule — ADR-012 requires "the document's **effective date**"
    (PMExperiment/DECISIONS.md:368-369) and `pmexperiment/admissibility.py:136-144` rejects a
    claim whose date does not parse. The binding register's own amendment dates are off by a
    day, in the direction that makes the record read as if a bar had been set after the verdict
    it governs.
- **Recomputation:** none beyond timezone conversion — all commit timestamps carry offset
  −07:00 and are converted to UTC by adding 7 hours; the conversion is checked against a case
  the repository states independently (Entry 10 records 2026-09-02T09:22:59Z; commit `2006ae6`
  author date 2026-09-02T02:23:41-07:00 = 09:23:41Z). Git reads were read-only `log` and
  `show`; see the access log.
- **What would resolve it:** an append-only correction in the shape of Entry 6.1, restating the
  made-date of Amendments 1–3 and the ADR trio as 2026-08-29 and naming the commit that carries
  them; or a statement of the timezone convention under which "2026-08-30" is the right stamp
  for a commit made at 2026-08-29T18:05:26Z.
- **Confidence:** HIGH — the commit object and the file content at that commit are both read
  directly, and the internal contradiction with Amendment 4 is visible in the register alone.
- **Could later commits invalidate this?:** no — `f686036` is an ancestor of the anchored SHA,
  the text is unchanged at the anchor, and the project is closed.
- **Disclosed by the authors?:** **no.** The repository discloses the ADR *numbering* collision
  (PMExperiment/DECISIONS.md:195-204) and one commit-ordering lag
  (`registry.FX_TURNOVER_REGISTERED` committed one commit before the Amendment 4 text that
  cites it, PMExperiment/DECISIONS.md:304-307) — which shows the authors track this class of
  defect — but nowhere records that Amendments 1–3 carry a date a day after the commit that
  made them.

---

### AUDIT-B-PMExperiment-10

- **ID:** AUDIT-B-PMExperiment-10
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** BAND-OPEN (REGISTRATION.md Section 15.2) and its "three
  qualifications registered with the verdict and not separable from it"
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "| BAND-EMPTY | **does not fire.** The registered band
  exceeds the required underpricing at 10 of 10 registered buckets, on both exit routes, at
  k = 1, at k = 12 and in the k → ∞ limit. |" — PMExperiment/REGISTRATION.md:416, immediately
  followed by "**Three qualifications registered with the verdict and not separable from it:**"
  — :431.
- **Evidence:**
  - Amendment 2's registered BAND-EMPTY condition is, verbatim: "| BAND-EMPTY | no price bucket
    where the registered effect band exceeds the required underpricing | …" —
    PMExperiment/REGISTRATION.md:740. Read as "the band (i.e. all of it) exceeds", the verdict
    is BAND-EMPTY; read existentially ("some of it"), BAND-OPEN.
  - The repository knows this and reports it — in the working documents only: "| **existential**
    … | **10 / 10** at k = 1, k = 12 and k → ∞ | **10 / 10** at every k | **not BAND-EMPTY** | /
    | strict — would *every* effect in the band survive? | **0 / 10** at every k | **0 / 10** at
    every k | BAND-EMPTY |" — PMExperiment/docs/BAND.md:233-234; also
    PMExperiment/pmexperiment/band.py:88-96 and :99-105,
    PMExperiment/tests/test_band.py:99-108, PMExperiment/progress.md:455-458.
  - It appears in **none** of the four conclusion-bearing documents. Grep for
    "quantifier|strict reading|existential|both readings" over the snapshot returns **0 hits**
    in REGISTRATION.md Section 15.2, report.md, README.md and HYPOTHESES.md. The register's
    three "not separable" qualifications (PMExperiment/REGISTRATION.md:433-446) are the missing
    magnitude, the missing n, and "BAND-OPEN is not a finding that an edge exists". The one
    qualification that flips the verdict is not among them.
  - The register's own standard for this is explicit — "The qualifier travels with it and is not
    separable" (PMExperiment/docs/BAND.md:20) and standing rule 13 (PMExperiment/CLAUDE.md:44).
    HYPOTHESES.md, whose stated job is to keep a settled question from being retried because the
    number that closed it is buried, carries the verdict at :119-160 with no trace of the
    alternative reading.
- **Recomputation:** confirmed independently: the minimum R_H over the ten registered midpoints
  at k = 1 is 0.0316 at the 1–10c bucket, so the band **bottom** 0.02 is exceeded at every
  bucket on every route at every k — 0/10 under the strict reading, exactly as
  PMExperiment/docs/BAND.md:234 reports. Script `.../work/agentB-PM-consol/verify.py`.
- **What would resolve it:** one sentence in Section 15.2 (and in the HYPOTHESES entry)
  recording that the same registered condition, read strictly, fires BAND-EMPTY at 10 of 10
  buckets, with the reason the existential reading was taken.
- **Confidence:** HIGH — the omission is verifiable by grep, and the alternative's consequence
  is stated by the authors themselves.
- **Could later commits invalidate this?:** no — the project is closed and Amendment 2 fixes the
  band as computed once (PMExperiment/REGISTRATION.md:744-745).
- **Disclosed by the authors?:** **yes**, in the working documents —
  PMExperiment/docs/BAND.md:116 and :229-237, PMExperiment/pmexperiment/band.py:88-96,
  PMExperiment/progress.md:455-458 — and the amendment's own pre-existing rationale ("no price
  region where a documented effect **could** survive") genuinely predates the arithmetic, so the
  existential reading was not chosen after the numbers existed. Severity is capped at S3
  accordingly. The finding is only that the disclosure did not travel into Section 15.2,
  report.md, README.md or HYPOTHESES.md, where the verdict is stated to a reader who will not
  open docs/BAND.md.

---

### AUDIT-B-PMExperiment-11

- **ID:** AUDIT-B-PMExperiment-11
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** candidate 3's PROHIBITED verdict on Dune, and the ADR-012 element
  (2) standard applied across the three licence candidates
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Dune Terms of Service**, label **`Last updated on:
  June 3rd, 2026`** — a *last-updated* label, and the substitution for an *effective* label is
  disclosed here rather than silently made." — PMExperiment/docs/LICENCES.md:548-550.
- **Evidence:**
  - ADR-012's element (2) is "the document's **effective date**"
    (PMExperiment/DECISIONS.md:368-369), enforced in code by `_is_iso_date(claim.effective_date)`
    with no substitute (PMExperiment/pmexperiment/admissibility.py:136-156); `admit()` returns
    UNMEASURED "whatever it claimed — including a claim that permission is absent, because an
    unevidenced refusal is no more measured than an unevidenced permission"
    (PMExperiment/pmexperiment/admissibility.py:159-174). A Dune claim carrying no effective
    date would therefore return UNMEASURED; the record publishes **PROHIBITED**
    (PMExperiment/docs/LICENCES.md:23-25; PMExperiment/DECISIONS.md:503-505;
    PMExperiment/progress.md:1021).
  - The same page refuses precisely this substitution when it would help a different question:
    "a schema.org `dateModified` exists in its metadata and **a modification timestamp is not an
    effective date**. … The tier price is recorded UNMEASURED rather than filled in." —
    PMExperiment/docs/LICENCES.md:592-597. A "Last updated on" label is a modification
    timestamp.
  - **The asymmetry runs toward convenience, over n = 3 candidates.** Candidate 2 — the only
    candidate whose verdict could have been PERMITTED, documenting all four gate inputs over
    **1,201,580,990 rows** — was refused on exactly this element: "**Element (2) fails.** The
    dataset card prints no effective, last-updated or revision label … **The CC BY 4.0 legal
    code prints no date whatsoever**" (PMExperiment/docs/LICENCES.md:398-403;
    PMExperiment/DECISIONS.md:462-463). Candidate 3, whose verdict is PROHIBITED and therefore
    convenient for the terminal "there is none", was admitted on a last-updated label over a
    **172,750-byte** body.
  - The repository's own flagship rule forbids this: "A venue may not be held to a **looser**
    reading than another because its verdict would be more convenient — and **the rule runs both
    ways.**" — PMExperiment/README.md:53-54. The looser reading is applied here to reach the
    PROHIBITED end of the same rule.
  - Materiality is limited: an UNMEASURED verdict on Dune leaves "**No candidate returns
    PERMITTED.**" (PMExperiment/docs/LICENCES.md:19) intact. What changes is the strength of one
    leg of the terminal claim — README's route ledger reads "| third-party platforms |
    **PROHIBITED** / **UNMEASURED** | Dune's in-force terms; four others never retrieved |"
    (PMExperiment/README.md:119) and the closure leans on "Two venues and three third-party
    routes now say the same thing, in five documents, for four different reasons."
    (PMExperiment/progress.md:1169-1170).
- **Recomputation:** none — this is a reading of the module's own rule against the verdicts the
  documents publish.
- **What would resolve it:** either recording candidate 3 as UNMEASURED on element (2) alongside
  its quoted clauses, or a numbered amendment registering a last-updated label as satisfying
  element (2) — which would then also have to be applied to candidate 2's assessment.
- **Confidence:** MEDIUM — the substitution is disclosed and argued, and the verdict does not
  change; the finding is that the standard was relaxed only where relaxing it made the record
  stronger.
- **Could later commits invalidate this?:** no — LICENCES.md's candidate sections are explicitly
  preserved as written ("**This section is appended, not an edit.** Everything above it stands as
  Stage D wrote it", PMExperiment/docs/LICENCES.md:795-797) and the project is closed.
- **Disclosed by the authors?:** **partly** — the substitution itself is disclosed in the
  sentence quoted above (PMExperiment/docs/LICENCES.md:549-550), which is why this is capped at
  S3. The inconsistency with the `dateModified` refusal 45 lines later, and with candidate 2's
  treatment, is not disclosed.

---

### AUDIT-B-PMExperiment-12

- **ID:** AUDIT-B-PMExperiment-12
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the registered planning counts of Section 0.4 — "| GO, MDE ≤ 0.02
  | ≥ 475 |" and "| stay out of BLOCKED, MDE ≤ 0.08 | ≥ 30 |"
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "At the tail cell's planning dispersion — prices near
  5c or 95c give p(1−p) ≈ 0.0475, so sqrt(v̄) ≈ 0.218 — inverting MDE = 2·sqrt(v̄/n) at each bar
  gives the required tail count" — PMExperiment/REGISTRATION.md:122-124.
- **Evidence:**
  - The tail cell is not "prices near 5c or 95c". It is registered as the union of two whole
    deciles: "**The tail cell T** is the union of 1–10 and 91–99" —
    PMExperiment/REGISTRATION.md:70-71 (`TAIL_BUCKETS_CENTS = ((1, 10), (91, 99))`,
    PMExperiment/pmexperiment/registry.py:26). And v̄ is registered as "the mean of p_i(1−p_i)"
    over the cell's prices (:75-77), restated at :301-302, not the value at its centre.
  - Recomputed: the uniform mean of p(1−p) over the **19** integer-cent prices of the registered
    cell is **0.049105**, not 0.0475, so the required counts are understated by 3.4 %: GO needs
    n_T ≥ **491.05**, not 475. The registration's preamble requires "Every number in this
    document is **derived, measured, or labelled an assumption with its direction of bias
    named**" (:13-14); this one is presented as derived, is derived from a different quantity
    than the one it names, and carries no direction.
  - A second, larger staleness in the same figures: after BAND-OPEN, "**The surviving region,
    registered here as the only region the power gate may fire over:** entry prices **91–99c**"
    (PMExperiment/REGISTRATION.md:420-421) — half the cell the 475/30 bars were derived for, and
    half the population the supporting expectation rests on ("The published benchmark … reports
    two-thirds of its 313,972 contract prices in the 1–10c and 90–99c bands, so the unrestricted
    universe reaching 475 tail contracts is expected", :132-134). No amendment restates the
    required n_T for the halved region; the register continues to carry 475 and 30.
- **Recomputation:** inputs cell definition REGISTRATION.md:70-71 / `registry.py:26`; v̄
  definition REGISTRATION.md:75-77; planning value :123; formula :101. Method: mean of p(1−p)
  over integer cents, then n = z²v̄/MDE² at z = 2.0. Script `.../work/agentB-PM-consol/verify.py`.
  Result:
  ```
  1–10c  uniform mean p(1−p) = 0.051150 (n = 10 prices)
  91–99c uniform mean p(1−p) = 0.046833 (n =  9 prices)
  union T                     = 0.049105 (n = 19 prices)   registered planning v̄ = 0.047500
  n_T for GO at v̄ = 0.049105: 491.05   (registered: 475)
  n_T for MDE ≤ 0.08        :  30.69   (registered: 30, from 29.69)
  ```
- **What would resolve it:** restating the planning dispersion as the cell mean with its
  direction of bias named, and restating the required counts for the 91–99c region the band gate
  left as the only firing region.
- **Confidence:** MEDIUM — the arithmetic is certain, but the realized v̄ was to be measured
  (:131) and the true price distribution inside the deciles is unknown, so the sign of the error
  on real data could go either way; what is certain is that a direction of bias was required and
  not given.
- **Could later commits invalidate this?:** no — Sections 0–14 are byte-identical from `9080186`
  to the anchor and the project is closed.
- **Disclosed by the authors?:** **partly** — "Both are planning figures; the realized v̄ is
  measured from snapshot prices in Task 3 and reported beside them"
  (PMExperiment/REGISTRATION.md:131-132) discloses that they are provisional, and "That gate was
  not designed here" (PMExperiment/report.md:126) discloses that the narrowed region's gate was
  never specified. Neither discloses that 0.0475 is the point value at the cell's centre rather
  than the cell mean the register defines, nor names its direction of bias.

---

### AUDIT-B-PMExperiment-13

- **ID:** AUDIT-B-PMExperiment-13
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the carried-forward requirement "an edge above 5.85 points" over
  the region 91–99c, in README.md and HYPOTHESES.md
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**BAND-OPEN**, fired 2026-08-29: over entry prices
  **91–99c held to resolution**, an edge above **5.85 points** at FX turnover k = 1 is required,
  against a registered band top of **8.00 points**." — PMExperiment/README.md:139-141; and "entry
  prices **91–99c** held to resolution, requiring an edge above **5.85 points** at the registered
  FX turnover k = 1, against a registered band top of **8.00 points**." —
  PMExperiment/HYPOTHESES.md:130-133.
- **Evidence:**
  - 5.85 points is the requirement at the bucket **midpoint** 95c, not over the region.
    PMExperiment/REGISTRATION.md:422-424 states the range correctly — "requiring an edge above
    **5.85 points** at the binding k = 1 — 5.73 points at 91c rising to **5.97** at 99c" — and
    PMExperiment/docs/BAND.md:316-318 likewise. Both carried-forward statements drop the range
    and state the midpoint value as the requirement for the whole region.
  - Recomputed from the registered constants (n = 3 price points across the 9-cent region):
    R_H(0.91) = **0.0573**, R_H(0.95) = **0.0585**, R_H(0.99) = **0.0597**. Stating 5.85 as *the*
    requirement over 91–99c understates it by up to **0.12 points** at the top of the region,
    i.e. it overstates the surviving margin there by 0.12 of the 2.15 points the register calls
    the surviving share (the true margin at 99c is **2.03 points**).
  - HYPOTHESES.md is the document whose stated job is to carry "the figure that closed it, with
    its n" so a question is not re-asked without it (:5-9); it is the one place the range most
    needs to survive.
- **Recomputation:** inputs `registry.py:53-57` and Amendment 4's `FX(p) = 0.03·p/k`
  (PMExperiment/REGISTRATION.md:799); method `R_H(p) = 0.02 + 0.01 + 0.03p`; result 0.0573 /
  0.0585 / 0.0597 at p = 0.91 / 0.95 / 0.99, margins to the band top 0.02270 / 0.02150 / 0.02030.
  Script `.../work/agentB-PM-consol/verify.py`.
- **What would resolve it:** carry "5.73 at 91c to 5.97 at 99c" into README.md and HYPOTHESES.md
  alongside the 95c figure, as REGISTRATION.md and docs/BAND.md already do.
- **Confidence:** HIGH — arithmetic over registered constants; the register itself states the
  range.
- **Could later commits invalidate this?:** no — README.md is unchanged after `1ba50aa` at the
  anchor and the project is closed.
- **Disclosed by the authors?:** **yes**, in the register and the band document
  (PMExperiment/REGISTRATION.md:422-424, PMExperiment/docs/BAND.md:316-318), which is why this
  is S4. The finding is only that the range did not travel into the two documents that carry the
  verdict forward.

---

### AUDIT-B-PMExperiment-14

- **ID:** AUDIT-B-PMExperiment-14
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** README.md "What would reopen this" versus REGISTRATION.md
  Amendment 9's fourth reopening condition
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "## What would reopen this / Each is an operator action,
  not a measurement: / 1. **an established legal entity applying for Internal Use** … / 2. **an
  academic tier offered by Kalshi, if one is** … / 3. **a licensed dataset whose licensor held
  authority to license**" — PMExperiment/README.md:151-162.
- **Evidence:**
  - The register at the anchored SHA carries **four**, not three: "**Fourth reopening condition,
    added to Amendment 8's three:** / 4. **a Polymarket data licence or written authorization** —
    the same instrument Stage C found absent, obtained." —
    PMExperiment/REGISTRATION.md:1161-1165. HYPOTHESES.md carries it too (:352-358). The README
    does not, and the README is the document a cold reader is told to read first.
  - Git shows why: the README was rewritten in `1ba50aa` "docs: Task 4 — rewrite README.md for a
    cold reader" at 2026-09-02T09:36:29Z, and Amendment 9 landed **14 minutes later** in
    `03d16e7` at 2026-09-02T09:50:29Z, whose stat touches DECISIONS.md, HYPOTHESES.md,
    REGISTRATION.md, progress.md and tests/test_honesty.py — **5 files, not README.md** (verified
    by `git show --stat 03d16e7`).
  - Direction: the public document understates the routes by which the question could be
    reopened (3 of 4), which makes the terminal framing ("**terminal**",
    PMExperiment/README.md:6) look tighter than the register supports.
- **Recomputation:** none beyond the read-only `git show --stat 03d16e7` and `git log` quoted
  above; see the access log.
- **What would resolve it:** one line in README.md's reopening list, or a sentence saying the
  list is Amendment 8's three and that Amendment 9 adds a fourth.
- **Confidence:** HIGH — the omission and the commit order are both directly verifiable.
- **Could later commits invalidate this?:** **yes in principle** — `03d16e7` is the last commit
  at the anchor and a subsequent README edit would close it; nothing after 2026-09-02T09:50:29Z
  exists in the live repository as of my read (2026-09-05T23:17Z).
- **Disclosed by the authors?:** **no.** PMExperiment/README.md:164-166 says "**A reply to the
  pending academic-tier question is a one-line register update, not a reopening.** No fourth
  venue is proposed" — which is about venues, not about the count of reopening conditions, and
  does not flag the omission.

---

### AUDIT-B-PMExperiment-15

- **ID:** AUDIT-B-PMExperiment-15
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** "The Canadian doubt, registered before any measurement and never
  tested" (README.md), against Section 3's registered magnitudes
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "**The Canadian doubt, registered before any measurement
  and never tested:** the permitted categories are economic indicators, financial markets and
  climate — the well-calibrated ones — and a **30-day minimum maturity** removes the
  fast-resolving contracts." — PMExperiment/README.md:194-197.
- **Evidence:**
  - "the well-calibrated ones" is registered nowhere. Grep over the snapshot returns the phrase
    **once**, at PMExperiment/README.md:196; the only other "well-calibrated" hits are the title
    of Page and Clemen (2013) at PMExperiment/REGISTRATION.md:244 and
    PMExperiment/docs/BAND.md:56.
  - The register's own Section 3 attributes the **largest** cited magnitude — the one that sets
    the band's top — to a permitted category: "longshots priced below 30c settled YES 4.0 % of
    the time, a bias of **−0.077** — about 7.7 points — inside a permitted-category
    (economic-indicator) series" — PMExperiment/REGISTRATION.md:236-238. Section 15.2 uses that
    attribution to refuse BAND-NARROW: "The category clause is contradicted by Krause's
    permitted-category (economic-indicator) attribution" (:417).
  - What the registration actually registered as the doubt is narrower and does not claim the
    categories are well calibrated: "**Registered expectation, stated before any measurement:**
    the effect is plausibly real in the unrestricted universe … **The doubt is the filter.**" —
    PMExperiment/HYPOTHESES.md:47-52. The only support for "well-calibrated" in the record is the
    companion CPI study at **n = 95 contracts over 12 months**
    (PMExperiment/REGISTRATION.md:238-243), which the register itself frames as evidence of
    heterogeneity, not of good calibration.
  - Direction: the sentence makes the unmeasured Canadian question look more likely to have come
    out negative, which supports the closure's comfort ("the method working, not a
    disappointment"); and it is attributed to the pre-registration ("registered before any
    measurement"), which it is not.
- **Recomputation:** none.
- **What would resolve it:** drop "the well-calibrated ones", or cite a registered source for it
  and reconcile it with Section 3's permitted-category attribution of the 7.7-point figure.
- **Confidence:** MEDIUM — the phrase is a compressed gloss in a README and one registered source
  (the CPI companion, n = 95) is consistent with it; the inconsistency with the band's top is
  nonetheless direct.
- **Could later commits invalidate this?:** no — README.md is unchanged after `1ba50aa` at the
  anchor.
- **Disclosed by the authors?:** **no** — the register nowhere flags that the README's
  characterisation of the permitted categories differs from Section 3's own attribution.

---

## What Agent B checked and found sound

The B-thesis did **not** hold on the following. Each was opened expecting it to.

1. **The registration was not edited in place.** `REGISTRATION.md` at the Section 0 commit
   `9080186` (2026-08-29T07:37:33Z) and at the anchored SHA, everything through
   `## 15. Results`: **byte-identical, 367 lines both sides, diff exit 0** (re-verified at
   consolidation). The cost model (Section 2), the effect band (Section 3), the gate map (0.3),
   the planning counts (0.4), the access gate (0.5), outcome blindness (10) and the cost floor
   (11) are exactly as registered before the first request. Section 16 gained only a prepended
   annotation, and the annotation says so (REGISTRATION.md:640-641).

2. **The band arithmetic reproduces exactly, cell for cell.** Every cell of the Pass 1 table
   (docs/BAND.md:199-210) recomputes from the registered constants: R_H and R_X at all ten bucket
   midpoints at k = 1, 12 and →∞; 0.0585 / 0.0785 at 95c; 0.0573 at 91c; 0.0597 at 99c; 0.0565 at
   88.3c; the 2.15-point margin; C(0.95) = 0.0785 and C(0.05) = 0.0515; the crossing solutions
   −0.3333 / +1.6667 / −1.0000 / +1.0000; the 0.0015 round-trip margin; Amendment 4's
   0.0015 + 0.00045 = 0.00195 slack, the held route's 0.00135, and the 16× ratio. Section 0.4's
   inversions (475, 29.6875 → 30) are right for the dispersion they name. **No arithmetic error
   was found anywhere in the band document.**

3. **The unit determination and the direction correction are right, and both made the
   repository's own case worse.** Bürgi 5c/3 % → NO at 0.950, 0.020; 95c/98 % → YES at 0.950,
   0.030; Krause sub-30c/4.0 % → NO at 0.883, 0.077 — every cell reconstructs
   (docs/BAND.md:128-159, README.md:84-88). The direction correction, which moves every
   exploitable expression to 88–95c where proportional FX is largest, is published at the top of
   the README.

4. **The exit-route exclusion is applied against the repository's own interest.** Route X clears
   the band top at 95c by 0.0015 while the register's own named FX understatement is 0.00195; the
   register excludes route X on exactly that ground (REGISTRATION.md:427-429,
   docs/BAND.md:261-263). 0.0015 − 0.00195 = −0.00045: the exclusion is correct and it removes a
   route that would otherwise have widened the positive.

5. **BAND-OPEN is never written as evidence of an edge.** Every occurrence carries the refusal —
   REGISTRATION.md:444-446, README.md:143-145, report.md:449-451, HYPOTHESES.md:147-151,
   DECISIONS.md:729-731 — and a test pins two of them (tests/test_honesty.py:226-232). This is
   the single most obvious place a repository would overclaim, and it does not.

6. **No bar was moved after the deciding numbers existed.** Amendments 1–3 precede the band
   arithmetic by 70 minutes in git; Amendment 4 fixes k = 1, the treatment that biases *toward*
   BAND-EMPTY, and refuses k > 1 explicitly because it "lowers the cost floor in the direction
   that helps H1" (REGISTRATION.md:809-813); Amendment 5's volume floor was imported verbatim
   from a study that predates this repository and biases every gate count toward BLOCKED
   (registry.py:44-50). Amendment 2's held-to-resolution route does lower the floor from 0.0785
   to 0.0585 at 95c, but it is a numbered amendment made before the gate fired (`f686036` 18:05Z
   vs `32dc10a` 19:24Z), is consistent with Section 2's own "settlement carries no fee" note
   (:199), is reported beside the round-trip figure throughout, and BAND-OPEN does not depend on
   it — BAND-EMPTY fails to fire on the round-trip route too. **I expected this to be the finding
   and it is not one.**

7. **The Section 13 prior was never backfilled.** The slot is still empty at the anchor, the
   README says so plainly, and `tests/test_honesty.py:517-525` fails if it is filled. This is the
   opposite of a bar lowered after data existed, and is the strongest single piece of evidence
   against the thesis that this repository backfills to flatter itself. (My finding
   AUDIT-B-PMExperiment-6 is about the *use* of that prior in the closure framing, not about the
   slot.)

8. **The closure does not pretend to be the registered closure.** Section 16's conditions are
   recorded as never met, with the gap stated rather than smoothed (REGISTRATION.md:605-612;
   report.md:458-462; progress.md:1487-1490), and "H1 therefore does not close under Section 16
   at all" (:609). The operator's cost decision is filed in its own category and explicitly
   denied evidentiary force (Amendment 7; ADR-017, DECISIONS.md:648-664).
   "EXISTS-AND-UNTRAVELLED" is a precise label and it is defended precisely.

9. **The self-conviction is real, not decorative.** ADR-012's own claim that "Stage A's Kalshi
   finding met that bar" is convicted at DECISIONS.md:434-440 on a measurable ground (`Effective`
   0 occurrences, `Last Updated` 0); Amendment 1's premise is retracted in Amendment 6 after the
   entire measurement venue had been moved on it; the Dune read is convicted of publishing
   PROHIBITED from an unread instrument (ADR-015). I looked for a correction that rescued a
   verdict rather than recording a falsification and found none — "Every correction made the
   record narrower or weaker. None changed a verdict." (report.md:303-304) checks out against the
   ADRs.

10. **Stage D's completeness caveat was written before it was needed, not after.** "There is
    none" is a verdict over what was read, in the Stage D material committed `7b5a751` /
    `baa2bf3` on 2026-08-29T23:22-23:35 −07:00; the Kalshi reply that vindicated it arrived
    2026-09-01. I checked git for a retro-fit and found none.

11. **Outcome blindness holds.** No statistic relating a price to an outcome exists anywhere in
    the snapshot; `data/` and `scripts/` hold only `.gitkeep`; `power.py` and `band.py` reference
    no resolution field and `tests/test_guards.py` enforces it. The one exception (two settled
    records carrying `result`) is a pre-registered access-gate condition capped at 5 records
    (registry.py:37), is recorded rather than rounded away (README.md:101-106), and no statistic
    was computed from it. The "zero requests / zero dollars / no statistic" totals reconcile,
    including the 11-vs-13 request difference (11 keyless market requests inside a 13-request
    budget).

12. **The guards fail when mutated, and the harness faults are recorded.**
    `tests/test_guards.py:80-85` proves the outcome-blindness scanner can fail; `:139-166` proves
    each ADR-012 element is load-bearing and first asserts the baseline is admissible. The three
    occasions on which the mutation harness produced a false green are recorded as ADRs, not
    hidden (ADR-020, ADR-021; progress.md Entries 7.1 and 9.1), with the affected mutations
    re-run (progress.md:1229).

13. **`pmexperiment/admissibility.py`'s disclosed blind spot is the real one.** `missing_elements()`
    checks that dates *parse*, not merely that they are present (`_is_iso_date`, :136-144), and
    `admit()` fails closed on a claimed PROHIBITED as well as a claimed PERMITTED (:159-180) —
    both stronger than ADR-012 requires. `MIN_DOCUMENT_TEXT_RATIO = 0.05` rests on a single
    measured observation, and the comment says so and names its direction of error (:39-49).

14. **The Polymarket and Kalshi access verdicts are sound, and the counterarguments are recorded
    against them.** The strongest counterargument to the Polymarket verdict (the crawlers bullet
    is scoped to "the Site, any other Interface, or Features") is set out at full strength with
    three reasons it is not taken; robots.txt's permissiveness (HTTP 200, 73 bytes, no
    `Disallow`) is recorded *against* the verdict. Kalshi's conditions 3 and 4 fail **closed** on
    n = 20 and n = 1, and the depth finding is phrased as a property of the keyless surface, a
    phrasing that survived contact with the Kalshi reply (docs/ACCESS.md:317-326).

**Where I expected the thesis to hold and it did not:** I looked for a bar lowered, widened or
re-specified after the deciding numbers existed; an amendment rescuing a verdict; and a
limitation disclosed in a footnote and dropped from the README or the register. I found none of
the three. Every qualification attached to BAND-OPEN in `docs/BAND.md` travels into
`REGISTRATION.md` Section 15.2, `report.md`, `HYPOTHESES.md` and `README.md` without softening —
with the single exception recorded as AUDIT-B-PMExperiment-10. The findings above are about
arithmetic and design that the disclosures do not reach.

---

## Dropped at consolidation

Nothing was dropped for lack of a locatable quote, a figure or an n: all 17 draft findings carry
all three. What changed:

1. **Merged — the power gate.** DRAFT-p1-register-3 and DRAFT-p2-progress-5 challenged the same
   claim (REGISTRATION.md:110 / :122-129) on the same ground (z = 2.0 carries no power term).
   Merged into **AUDIT-B-PMExperiment-2**, keeping p1's power figures (0.5160 / 0.5000, n
   inflation 1.962) and p2's additional evidence (the n = 30 BLOCKED flip at MDE 0.11148, the
   clustering deferral, and the two-cell multiplicity point). Both drafts' file:line sets are
   retained.
2. **Merged — the amendment dates.** DRAFT-p1-register-5 and DRAFT-p2-progress-6 challenged the
   same claim (REGISTRATION.md:707, "Made 2026-08-30") on the same ground (the commit that made
   it is dated a day earlier). Merged into **AUDIT-B-PMExperiment-9**, keeping p1's ADR-006(2) /
   ADR-007(2) / ADR-008 stamps and the numbering note, and p2's HYPOTHESES.md inversion and the
   Entry 6.1 principle the authors themselves stated.
3. **Merged and split — the band top.** DRAFT-p1-register-1 and DRAFT-p2-progress-8 challenged
   the same claim (BAND-OPEN) on the same ground (the deciding input has no n and its source sits
   outside the fired cell). Merged into **AUDIT-B-PMExperiment-8**. Because the authors disclose
   that ground prominently in every conclusion-bearing document, the merged finding is **capped
   at S3** and says so — p1's S2 was too high for a disclosed limitation. The genuinely
   undisclosed material inside p1's evidence — no retrievable identifier for the deciding source,
   standing rule 4 never applied to any effect-band source, and ADR-012 scoped so it can never
   fire over that input — challenges a different claim (CLAUDE.md:25-26 and README.md:53-54) on a
   different ground, and is carried separately as **AUDIT-B-PMExperiment-7** rather than being
   lost to the cap. The two are cross-referenced so neither is double-counted.
4. **Corrected — wrong line numbers throughout the p2 draft's Python citations.** Every
   `pmexperiment/registry.py` and `pmexperiment/power.py` line number in `p2-progress.md` and
   `p2-progress.positives.md` was wrong by roughly +217 and +135 respectively (e.g.
   `registry.py:270-283` for constants that sit at :53-66; `registry.py:226` for `Z_CRITICAL` at
   :9; `power.py:180` for the MDE return at :45) — `registry.py` is 66 lines and `power.py` is 82.
   All were re-verified against the snapshot and corrected. `band.py`, `admissibility.py`,
   `tests/*` and every Markdown citation in both drafts checked out as written.
5. **Corrected — one paraphrased quote.** DRAFT-p1-register-1 rendered README.md:148-149 as "the
   band survives on its top alone, set by the one source whose n the registration never
   recorded"; the source reads "The band survives on its top alone, and that top is set by the
   one source whose **n the registration never recorded**." Quoted verbatim here.
6. **Corrected — two counts.** The Krause grep returns **32** mentions in the snapshot, not the
   30 the p1 draft states; and the 80 %-power GO bar is 932.05 contracts, quoted as "932.05 →
   933" rather than p1's bare 932 or p2's bare 933.
7. **Label changed.** DRAFT-p2-progress-4 (BAND-NARROW) was labelled DERIVED but carries no
   recomputation and rests entirely on documents; it is **READ** here
   (AUDIT-B-PMExperiment-5).
8. **Demoted to an assumption, not dropped.** The intra-event ICC values (0.10 / 0.25 / 0.50) in
   the clustering leg of AUDIT-B-PMExperiment-2 carry no n anywhere in this repository. They are
   kept but marked explicitly as an assumption with the direction of bias named, and the
   finding's load-bearing figures are the power ones, which are exact.
9. **Disclosure fields tightened.** DRAFT-p1-register-2 (now AUDIT-B-PMExperiment-6) and
   DRAFT-p2-progress-4 (now AUDIT-B-PMExperiment-5) were drafted as "partly disclosed". The
   limitation each actually raises is disclosed nowhere — only the facts it rests on are — so
   both are recorded as **not disclosed for the limitation raised**, with the adjacent
   disclosures named in full, and both keep S2. Nothing here is presented as a discovery that
   the authors had already written down.
10. **Not raised.** `MIN_DOCUMENT_TEXT_RATIO = 0.05` resting on one observation (disclosed with
   its direction of error at admissibility.py:39-49); the `missing_elements()` quotation blind
   spot (disclosed at README.md:47-49, docs/ACCESS.md:291-300); the drift in H2's stated parking
   reason between HYPOTHESES.md:73 and :323-324 (it runs toward leaving a hypothesis open, not
   toward claiming anything). Each is recorded in the positives ledger instead.

---

## Live-repo access log

Live repository touched: `/home/kiros-li/Documents/GitHub/PMExperiment`, **read-only, git
history only** — `status --porcelain`, `log --format='%h %aI %s'`, `show --stat <sha>`,
`show <sha>:REGISTRATION.md`. No working-tree file was opened for writing, no untracked or
gitignored data was read, and no repository script was executed. All content citations are from
the anchored snapshot.

Read windows: 2026-09-05T18:20Z–18:37Z (draft part p1-register), the p2-progress part's git
reads in the same session, and 2026-09-05T23:17:43Z–23:18:05Z (this consolidation).

Before first access this session
(`git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain`, 2026-09-05T23:17:43Z):

```
```

(empty output, exit 0)

After last access (same command, 2026-09-05T23:18:05Z):

```
```

(empty output, exit 0)

Both draft parts recorded the same empty-before, empty-after result. Clean before and after;
nothing of mine, and no pre-existing dirt, in this repository.

Scratch scripts and outputs for this consolidation:
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-PM-consol/verify.py`.
