# PMExperiment — Agent B draft findings, part p2-progress

Repository: PMExperiment, anchored SHA `03d16e71dbf25a86c529884662d02136f8e82334`
(main, 2026-09-02, closed project). Snapshot read from
`/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/`.
Assigned primary documents: `progress.md` (1651 lines), `docs/` (ACCESS, BAND,
LICENCES), `pmexperiment/`, `data/`. All read in full. `README.md`,
`REGISTRATION.md`, `HYPOTHESES.md`, `report.md`, `CLAUDE.md` and `tests/` were
read for context and are cited where a bar, a framing or a pinned assertion
lives there; where a finding's primary evidence sits outside my document set it
says so.

Direction: B (claimed more than earned). Recomputations were run with
`/home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python` from scripts in
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-PM-p2/`
(`recompute.py`, `feasible.py`). No repository script was executed.

---

### DRAFT-p2-progress-1

- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** BAND-OPEN, the repository's only positive verdict, and the surviving region it names (entry prices 91–99c held to resolution, k = 1)
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Entry prices 91–99c — the favourite half of the registered tail cell — held to resolution, on either side of the book (YES on a documented-underpriced favourite, or NO on a documented-overpriced longshot), requiring an edge above 5.85 points at the registered turnover k = 1: 5.73 points at 91c rising to 5.97 points at 99c.**" — PMExperiment/docs/BAND.md:314-318
- **Evidence:**
  - The break-even rule is registered as a requirement on the *true probability*: "Break-even therefore requires the true probability to exceed the market price by … held to resolution | one side, $0.02 | **≥ 2.0 percentage points**" (PMExperiment/REGISTRATION.md:717-722), and Section 11 states the same in the form the inference consumes: "a candidate calibration edge at entry price p survives the registered Canadian retail path only if it exceeds C(p)" (PMExperiment/REGISTRATION.md:332-335). A probability cannot exceed 1, so the largest edge that can exist at entry price p is 1 − p. This bound is nowhere in the repository: `grep -rn "cannot exceed\|bounded\|1 - p\|attainab\|feasib"` over `*.md` and `*.py` in the snapshot returns only `tests/test_power.py:21` (a comment on p(1−p)) and two unrelated ADR-012 sentences.
  - The requirement curve the same document registers is R_H(p) = 0.03 + 0.03p (PMExperiment/docs/BAND.md:219, PMExperiment/pmexperiment/band.py:68-80, `registry.FEE_PER_SIDE_USD` 0.02 + `HALF_SPREAD_USD` 0.01 + `FX_PER_DIRECTION`·`FX_DIRECTIONS`·p = 0.03p, PMExperiment/pmexperiment/registry.py:270-283).
  - Feasibility therefore requires 1 − p > 0.03 + 0.03p, i.e. p < 0.97/1.03 = **0.941748**. Inside the fired region: 91c, 92c, 93c and 94c are feasible; **95c, 96c, 97c, 98c and 99c are arithmetically empty — five of the nine cents in the named region**. At 99c the document's own stated requirement of 5.97 points implies a true probability of **1.0497**.
  - **The region's registered representative price is one of the empty ones.** `band.bucket_midpoint((91,99))` = 0.950 (PMExperiment/pmexperiment/band.py:108-111; pinned at PMExperiment/tests/test_band.py:177). Every headline figure in the repository is quoted at that price: "requiring **5.85 points** of underpricing at the registered FX turnover against a registered band whose top is **8.00 points**" (PMExperiment/REGISTRATION.md:409-412), repeated at PMExperiment/docs/BAND.md:15-18, PMExperiment/progress.md:362-368, PMExperiment/progress.md:481-482, PMExperiment/report.md:61-64 and PMExperiment/README.md:139-141. At p = 0.950 the maximum edge that can exist is 0.0500 against a requirement of 0.0585 — **a shortfall of 0.0085, not a margin**.
  - The band top itself is unattainable over most of the region: an underpricing of 0.08 requires p ≤ 0.92. So the surviving window against the *registered* band is 91c (0.0573, 0.0800], 92c (0.0576, 0.0800], 93c (0.0579, 0.0700], 94c (0.0582, 0.0600] — at 94c a window **0.18 points wide**.
  - The published margin figure is measured against an effect that cannot exist at the price it is measured at: "At k = 1 against the band top, route H clears by 4.84 points at 1–10c falling to **2.15 points** at 91–99c" (PMExperiment/docs/BAND.md:257-259). The 2.15 points is 0.0800 − 0.0585 at p = 0.950, where the ceiling is 0.0500.
  - The same bound removes the round-trip route entirely from 93–99c: R_X(p) = 0.05 + 0.03p is feasible only for p < 0.95/1.03 = 0.92233.
- **Recomputation (if any):** inputs — FEE_PER_SIDE_USD = 0.02, HALF_SPREAD_USD = 0.01, FX_PER_DIRECTION = 0.015, FX_DIRECTIONS = 2 (PMExperiment/pmexperiment/registry.py:270-274); R_H per PMExperiment/pmexperiment/band.py:68-80; bucket 91–99 per PMExperiment/pmexperiment/registry.py:241. Method: for each integer cent price p in 0.91…0.99, compare R_H(p) = 0.03 + 0.03p against the ceiling 1 − p, and against min(0.08, 1 − p) for the registered band top. Result (`feasible.py`): 91c R=0.0573 ceiling 0.0900 feasible; 92c R=0.0576 ceiling 0.0800 feasible; 93c R=0.0579 ceiling 0.0700 feasible; 94c R=0.0582 ceiling 0.0600 feasible; 95c R=0.0585 ceiling 0.0500 **empty**; 96c 0.0588/0.0400 empty; 97c 0.0591/0.0300 empty; 98c 0.0594/0.0200 empty; 99c 0.0597/0.0100 empty. Crossover p = 0.97/1.03 = 0.9417476. Round trip crossover p = 0.95/1.03 = 0.9223301.
- **What would resolve it:** either a restatement of the surviving region as 91–94c held to resolution with the per-cent windows shown, and re-quoting the headline requirement at a feasible price rather than at the 0.950 midpoint; or a registered argument that the edge is not bounded by 1 − p at entry price p (which would contradict REGISTRATION.md:717-722 and Section 11).
- **Confidence:** HIGH — the bound follows directly from the repository's own definition of the edge as a probability difference at a stated entry price, and the arithmetic reproduces the repository's own published figures exactly before applying it.
- **Invalidated by later commits?:** no — the anchored SHA is the terminal commit of a closed project; `REGISTRATION.md` Sections 2, 3 and 11 and `registry.py` are byte-identical from the first Section 0 commit `9080186` (2026-08-29T07:37:33Z UTC) to the anchor, verified with `git show <sha>:REGISTRATION.md`.
- **Disclosed by authors?:** no — the qualifications carried with the verdict (PMExperiment/docs/BAND.md:330-338, PMExperiment/REGISTRATION.md:431-446, PMExperiment/README.md:143-149) name the missing n, the missing magnitude at that bucket and the thinness of the band, but nowhere state that most of the fired region requires a probability above 1.

---

### DRAFT-p2-progress-2

- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the registered cost model applied to Amendment 2's second exit route ("exited before resolution"), and the crossing-point and cost-floor conclusions drawn from it
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The plain statement: **the registered cost floor runs entirely inside the registered effect band at every price.** The band's bottom is below the floor everywhere and its top is above the floor everywhere." — PMExperiment/docs/BAND.md:222-224 (same conclusion at PMExperiment/progress.md:445-447, PMExperiment/REGISTRATION.md:452-454, PMExperiment/report.md:100-103)
- **Evidence:**
  - The spread component is registered as "**1 cent half-spread, paid once at entry** | assumption. **A settlement exit crosses no spread.**" (PMExperiment/REGISTRATION.md:200, quoted into PMExperiment/docs/BAND.md:75). The justification for charging it once is that the modelled participant exits at settlement — Section 2's participant is "a Canadian retail individual funding in CAD, converting to USD, **holding one side of one contract to settlement**, and converting back" (PMExperiment/REGISTRATION.md:193-195).
  - Amendment 2 later added a second route that is **not** a settlement exit — "exited before resolution | both sides, $0.04" (PMExperiment/REGISTRATION.md:720-723) — and the spread component was never amended. The code charges exactly one half-spread on both routes: `return fee_borne(route) + registry.HALF_SPREAD_USD + fx_cost(entry_price, turnover)` (PMExperiment/pmexperiment/band.py:80), and the test suite pins the omission: "assert exited - held == pytest.approx(registry.FEE_PER_SIDE_USD)" (PMExperiment/tests/test_band.py:53, test at :44).
  - A non-settlement exit crosses the book a second time, so the round-trip route is understated by one half-spread = **0.0100 at every price**. That is **5.1×** the 0.00195 understatement the same document does quantify and does use to exclude the route: "Two registered simplifications, both leaning toward H1, neither revised … Their sum is **0.00195**" (PMExperiment/docs/BAND.md:181-186); "Route X's margin at the favourite tail (0.0015) is smaller than the 0.00195 by which Section 2's FX base understates cost" (PMExperiment/docs/BAND.md:261-263). The larger omission is not among the two.
  - With the exit half-spread charged, R_X(p) = 0.06 + 0.03p. Then R_X(0.95) = **0.0885** against a registered band top of **0.0800**, and R_X crosses the band top at p = **0.6667** — inside the tradeable range — which falsifies "**There are no crossings inside the tradeable price range.**" (PMExperiment/docs/BAND.md:214, and PMExperiment/progress.md:442-443 "there are none inside the tradeable range"), and falsifies the quoted claim above. The existential survival count on route X falls from 10/10 to 7/10 at k = 1 (71–80, 81–90 and 91–99 fail).
  - Direction of the error is toward H1, the direction Section 2 forbids revising in: "No component of this table may be revised after a result is seen; a better cost estimate enters only as a numbered amendment with its evidence." (PMExperiment/REGISTRATION.md:214-215). The point here is not a post-hoc revision — it is that a component registered for a settlement-exit participant was carried unamended onto a route that does not settle.
  - The fired verdict is not overturned: route X was excluded from the surviving region anyway (PMExperiment/docs/BAND.md:326), and route H's arithmetic is correct because a settlement exit genuinely crosses no spread. What is wrong is the reason given for excluding route X (a 0.0015-vs-0.00195 slack argument, when the route in fact fails by 0.0085 at 95c), and the two "at every price" conclusions above.
- **Recomputation (if any):** inputs — HALF_SPREAD_USD = 0.01 (PMExperiment/pmexperiment/registry.py:272), FEE_PER_SIDE_USD = 0.02 (:270), FX 0.03p (:273-274), route fee sides from PMExperiment/pmexperiment/band.py:27-30, band top 0.08 (:registry.py:228). Method: recompute the Pass 1 table as published (reproduces PMExperiment/docs/BAND.md:199-210 exactly at every cell), then recompute route X with two half-spreads. Result (`recompute.py`): published R_X(k=1) at the ten deciles 0.0517 / 0.0547 / 0.0576 / 0.0607 / 0.0636 / 0.0667 / 0.0697 / 0.0727 / 0.0756 / 0.0785 — identical to the published table; with the exit half-spread, 0.0616 / 0.0646 / 0.0677 / 0.0706 / 0.0736 / 0.0766 / 0.0796 / 0.0827 / 0.0857 / **0.0885**; band-top crossing at p = (0.08 − 0.06)/0.03 = 0.6666667.
- **What would resolve it:** a numbered amendment either charging a second half-spread on the exited-before-resolution route and restating the crossing-point and "runs entirely inside the band" conclusions, or registering an explicit reason why an early exit crosses no spread.
- **Confidence:** HIGH — the omission is visible in one line of code and one pinned assertion, and Section 2's own justification sentence names settlement as the reason the spread is charged once.
- **Invalidated by later commits?:** no — `registry.py`, `band.py` and Section 2 are unchanged from their introduction to the anchor; the project is closed.
- **Disclosed by authors?:** no — the two registered simplifications disclosed at PMExperiment/docs/BAND.md:181-187 total 0.00195 and do not include this one; the exit half-spread is not mentioned anywhere in the snapshot.

---

### DRAFT-p2-progress-3

- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the "10 of 10 buckets" figure that carries the "not BAND-EMPTY" leg of the BAND-OPEN verdict, and `pmexperiment.band.surviving_buckets`
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| BAND-EMPTY | **does not fire.** The registered band exceeds the required underpricing at 10 of 10 registered buckets, on both exit routes, at k = 1, at k = 12 and in the k → ∞ limit. |" — PMExperiment/REGISTRATION.md:416 (same figure at PMExperiment/docs/BAND.md:233 and :303-305, PMExperiment/progress.md:478-479)
- **Evidence:**
  - Section 3 registers the effect band in the tail cell only: "**Registered band: 0.02 to 0.08 absolute probability points of miscalibration in the tail cell** (snapshot prices 1–10c and 91–99c)" (PMExperiment/REGISTRATION.md:221-222, quoted into PMExperiment/docs/BAND.md:33-34).
  - The same document states the consequence twice, in the opposite direction to the count: "The registered effect magnitude column is populated **only in the tail cell**, because Section 3 registers the band there and nowhere else; elsewhere it is absent, not zero." (PMExperiment/docs/BAND.md:195-197), and "| the eight non-tail deciles | **no effect magnitude is registered outside the tail cell.** Supplying one would violate standing rule 5. |" (PMExperiment/docs/BAND.md:325). Standing rule 5 is "Absence is a recorded state, never a synthesized value" (PMExperiment/CLAUDE.md:27-28).
  - The code nevertheless applies `registry.EFFECT_BAND_HI` (0.08) at every decile: `surviving_buckets` iterates `registry.BUCKET_EDGES_CENTS` (all ten) rather than `registry.TAIL_BUCKETS_CENTS`, which exists two lines below it in the registry — PMExperiment/pmexperiment/band.py:114-122, PMExperiment/pmexperiment/registry.py:231-243. The test suite pins the ten-bucket reading: `test_band_top_survives_at_every_bucket_on_both_routes` (PMExperiment/tests/test_band.py:110-118).
  - So the deciding figure of the "does not fire" row is produced by supplying a registered magnitude at eight buckets where the same page says supplying one "would violate standing rule 5". Inside the cell the band is actually registered for, the honest count is **2 of 2**; and after this stage's own direction correction ("At longshot prices the documented miscalibration is *over*pricing … a buy has the wrong sign", PMExperiment/docs/BAND.md:145-149, :201, :324) only **1 of 2** carries an exploitable registered magnitude — the 91–99c bucket, at which the two cited magnitudes are 0.020 and 0.030 and "**both fail**" (PMExperiment/docs/BAND.md:247-252).
  - The verdict is not overturned by this alone (2/2 still clears existentially), but the published strength of the "not BAND-EMPTY" leg is inflated fivefold, and the figure is repeated as a load-bearing number in the register, the band document, the progress entry and the report.
- **Recomputation (if any):** inputs — bucket edges PMExperiment/pmexperiment/registry.py:231-242, tail buckets :243, EFFECT_BAND_HI :228, requirement curve PMExperiment/pmexperiment/band.py:68-96. Method: evaluate `band_top_exceeds_requirement` at each decile midpoint for both routes at k = 1, 12 and →∞, once over all ten deciles and once over the two registered tail buckets. Result (`recompute.py`): all-deciles 10/10 for both routes at every k (reproduces the published figure); tail-cell-only **2/2** for both routes at every k.
- **What would resolve it:** reporting the BAND-EMPTY test over `TAIL_BUCKETS_CENTS`, or an explicit registered statement that the band extends outside the tail cell for the purpose of the BAND-EMPTY test (which would contradict Section 3 and BAND.md:325).
- **Confidence:** HIGH — the two statements are 128 lines apart in one document and the code makes the choice explicit by iterating the wider constant while the narrower one is defined.
- **Invalidated by later commits?:** no — `band.py`, `registry.py` and Section 3 are unchanged to the anchor.
- **Disclosed by authors?:** no — the tail-cell restriction is disclosed, and the non-tail exclusion from the *surviving region* is disclosed, but the fact that the BAND-EMPTY count is nevertheless taken over all ten deciles is not reconciled anywhere.

---

### DRAFT-p2-progress-4

- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the exclusion of BAND-NARROW, the alternative verdict that would have recorded a split finding rather than passing a region to the power gate
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**not BAND-NARROW** — its condition requires the surviving region to lie *only* outside the permitted categories or below usable volume; the category clause is contradicted by Krause's permitted-category attribution, and the volume clause cannot be evaluated because no floor was ever registered;" — PMExperiment/docs/BAND.md:306-309 (same reasoning at PMExperiment/REGISTRATION.md:417 and PMExperiment/progress.md:479-481)
- **Evidence:**
  - Both legs of the exclusion are defective, and both defects point the same way — toward the more permissive verdict.
  - **Leg 1, the volume clause.** The register records the input as absent: "| **the volume floor of Section 1** | **never registered.** Stage A Task 2 never armed (ADR-006, 2026-08-29) … | BAND-NARROW's 'below usable volume' clause **cannot be evaluated**. Recorded in Pass 2 rather than filled with a guess. |" (PMExperiment/docs/BAND.md:113; also :287). An unevaluable clause was then treated as an unmet clause, which is the definition of synthesizing a value for an absent input, against the repository's own standing rule 5 — "**Absence is a recorded state, never a synthesized value.**" (PMExperiment/CLAUDE.md:27-28) — and against its own house summary "Refusals fail closed. Absence is a recorded state, never a synthesized value." (PMExperiment/README.md:227-228). Here the absence fails **open**.
  - **Leg 2, the category clause.** The only category attribution in the registration belongs to Krause: "Krause's 7.7 points is 'inside a permitted-category (economic-indicator) series'" (PMExperiment/docs/BAND.md:283). The same document measures Krause's exploitable entry price at **0.883** and places it outside the fired region: "| Krause, sub-30c settling 4.0 % | NO | **0.883** | 0.077 | **not recorded** |" (PMExperiment/docs/BAND.md:155), "| 81–90 | 0.855 | … | not registered — though Krause's exploitable complement lands here at 0.883 |" (:209), and "The only one large enough is Krause's 7.7 points at an exploitable price of 88.3c — the 81–90 decile, **outside the cell the band is registered for**." (:333-334). So the attribution used to defeat BAND-NARROW at 91–99c belongs to a price bucket the same verdict excludes. **No magnitude cited at 91–99c carries any category attribution at all** — the two that are cited there are Bürgi's 0.020 and 0.030 (PMExperiment/docs/BAND.md:210), and Section 3 attributes no category to them (PMExperiment/REGISTRATION.md:225-246).
  - The volume floor was in fact registered the next stage — "Registered as **Amendment 5**: total traded volume **≥ $1,000** per contract" (PMExperiment/progress.md:706-707; PMExperiment/REGISTRATION.md:855 "Made 2026-08-30") — after the band verdict had already fired without it, and it has never been exercised: "**Its cost in sample: not measured.** No enumeration ran" (PMExperiment/progress.md:714-715).
  - BAND-NARROW's consequence in the register is "recorded as a **split finding**: an effect may be real, priced, and unreachable." (PMExperiment/REGISTRATION.md:741); BAND-OPEN's is "the power gate proceeds against that region, and only that region." (:742). The difference between the two verdicts is the whole of what the repository's one positive licensed.
- **Recomputation (if any):** none — this is a reading of the registered verdict conditions against the inputs the stage recorded as absent or as attributed to a different price bucket.
- **What would resolve it:** a registered rule for how an unevaluable clause of a verdict condition is to be resolved (the register has none), or a category attribution for a magnitude cited at 91–99c.
- **Confidence:** MEDIUM-HIGH — the facts are all stated by the repository itself; what is contested is the inference, and the repository's own fail-closed rule points the other way.
- **Invalidated by later commits?:** no — Amendment 2's verdict definitions and Section 15.2 are unchanged to the anchor, and the project is closed.
- **Disclosed by authors?:** partly — the absence of the volume floor and Krause's 88.3c placement are both disclosed (PMExperiment/docs/BAND.md:113, :287, :333-334), and BAND-OPEN's thinness is disclosed at length; what is not disclosed is that the exclusion of BAND-NARROW depends on resolving an absent input in the permissive direction and on importing a category attribution from a price bucket the verdict excludes.

---

### DRAFT-p2-progress-5

- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the shipped power gate — `pmexperiment/power.py`, `registry.Z_CRITICAL`, and the registered planning bars of 475 and 30 tail contracts
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "At the tail cell's planning dispersion — prices near 5c or 95c give p(1−p) ≈ 0.0475, so sqrt(v̄) ≈ 0.218 — inverting MDE = 2·sqrt(v̄/n) at each bar gives the required tail count: | GO, MDE ≤ 0.02 | ≥ 475 | | stay out of BLOCKED, MDE ≤ 0.08 | ≥ 30 |" — PMExperiment/REGISTRATION.md:122-129
- **Evidence:**
  - The registered statistic is "MDE = z · sqrt(v̄ / n_T), with z = 2.0 two-sided" (PMExperiment/REGISTRATION.md:301; also :99-101), implemented as `return registry.Z_CRITICAL * math.sqrt(mean_dispersion / tail_count)` with `Z_CRITICAL: float = 2.0` (PMExperiment/pmexperiment/power.py:180, PMExperiment/pmexperiment/registry.py:226), and pinned at PMExperiment/tests/test_power.py:24-62.
  - **There is no power term.** A quantity z_{α/2}·SE is the half-width of a 95 % interval — the effect a design detects with **50 %** power, not a minimum detectable effect at any conventional power. No β, 1−β, "80 %" or "power of" appears anywhere in the snapshot (`grep -rn "80 %\|80%\|z_β\|power of\|beta"` over `*.md`/`*.py` returns nothing on this point). At the conventional 80 % ( z = 1.9600 + 0.8416 = 2.8016 ) the same design needs **n ≥ 933** for GO rather than 475, and **n ≥ 59** to stay out of BLOCKED rather than 30 — the registered counts are **half** the sample they are presented as.
  - The consequence at the BLOCKED bar is a verdict flip: at the registered planning dispersion and n_T = 30 the 80 %-power MDE is **0.1115**, above the band top of 0.08, i.e. **BLOCKED** — while `fire_power_gate("P30", 30, 0.0475)` returns DEGRADED and the test suite pins that (PMExperiment/tests/test_power.py:51-55). The gate as shipped would pass a Canadian-permitted cell at a tail count that a conventionally powered version of the same gate would block.
  - **The independence assumption is one the register itself defers.** Section 8 reads "*To be registered after the gate fires.* The estimator, the interval construction, **the clustering unit**, and the trial grid with its **multiplicity correction**." (PMExperiment/REGISTRATION.md:291-295). The gate's n_T is a count of contracts (PMExperiment/REGISTRATION.md:53-54, "One settled Kalshi market contributes one observation"), and the benchmark whose magnitudes set the band reports **46,282 contracts across 12,403 events** (PMExperiment/REGISTRATION.md:226-227) — 3.73 contracts per event. At an intra-event ICC of 0.25 the design effect is 1.683 and the true MDE is 1.30× the registered one; at 0.5 it is 1.54×. Both directions inflate the MDE, i.e. the shipped gate overstates power.
  - Two verdict cells are fired at z = 2.0 each — "Fired separately for U24 and P30" (PMExperiment/REGISTRATION.md:104) — with the multiplicity correction deferred to the section that only exists after the gate.
  - The framing this artifact carries is the strongest in the repository: "**The measurement that was supposed to decide this repository. Not the calibration error. The power to detect one inside the Canadian filter.**" (PMExperiment/README.md:177-180), "**This repository followed Insider, not NPD**" (PMExperiment/README.md:190), "**Follow Insider.** Compute the minimum detectable effect from dispersion and bucket counts alone, commit the gate before the measurement it judges" (PMExperiment/CLAUDE.md:63-65). The gate never fired, so no verdict rests on it; what rests on it is the claim that this design would not have repeated NPDExperiment's failure.
- **Recomputation (if any):** inputs — Z_CRITICAL = 2.0 (PMExperiment/pmexperiment/registry.py:226), EFFECT_BAND_LO = 0.02 / HI = 0.08 (:227-228), planning dispersion v̄ = 0.0475 (PMExperiment/REGISTRATION.md:122-123, PMExperiment/tests/test_power.py:21), MDE formula PMExperiment/pmexperiment/power.py:172-180, clustering inputs PMExperiment/REGISTRATION.md:226-227. Method: invert n = z²·v̄ / MDE² at z = 2.0 and at z = 1.959964 + 0.841621 (80 % power); and compute the design effect 1 + (m − 1)ρ at m = 46282/12403 = 3.7315. Result (`recompute.py`): z = 2.0 → n = 475.00 (GO), 29.69 → 30 (BLOCKED bar) — reproduces Section 0.4 exactly. z = 2.8016 → n = 932.05 → **933** (GO), 58.25 → **59** (BLOCKED bar); n ratio 1.962. MDE at n = 30 with 80 % power = **0.11148**. Design effect at ρ = 0.1/0.25/0.5 = 1.273/1.683/2.366, MDE inflation 1.128×/1.297×/1.538×.
- **What would resolve it:** either relabelling the quantity as a 95 %-interval half-width rather than a minimum detectable effect, or adding z_β and a clustering unit to Section 9 and restating the planning counts; and a multiplicity statement for the two verdict cells that Section 8 currently defers past the gate.
- **Confidence:** MEDIUM-HIGH — the arithmetic is unambiguous and the clustering deferral is quoted from the register; the caveat is that the gate never fired, so this is a defect of a shipped design rather than of a reported result.
- **Invalidated by later commits?:** no — `power.py`, `registry.py` and Sections 0.3, 0.4, 8 and 9 are unchanged to the anchor and the project is closed.
- **Disclosed by authors?:** no — Section 8 discloses that the clustering unit and multiplicity correction are unregistered, but it places them *after* the gate rather than treating them as inputs the gate's own figure depends on; no document anywhere states the power level the z = 2.0 bar corresponds to.

---

### DRAFT-p2-progress-6

- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the registration dates of Amendments 1–3, including Amendment 2, the amendment that defines the bar the repository's only positive was judged against
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Made 2026-08-30.** A new gate, ordered ahead of the power gate, because it is free and may be decisive on its own." — PMExperiment/REGISTRATION.md:707-708, under the heading "### Amendment 2 — the fee-versus-edge band fires before any measurement" at PMExperiment/REGISTRATION.md:705
- **Evidence:**
  - The verdict fired against that amendment is dated the day **before** it: "### 15.2 The fee-versus-edge band, fired 2026-08-29: BAND-OPEN" (PMExperiment/REGISTRATION.md:402), and the stage entry that fired it is "## Entry 5 — Stage B: the fee-versus-edge band — 2026-08-29" (PMExperiment/progress.md:360). On the face of the register alone, the bar post-dates its own firing.
  - Live-repository git history (read-only) shows the stated date is wrong and the real ordering is sound. `git log --format='%h AD=%aI'`: `f686036` "docs: amendments 1-3 — Polymarket measures the phenomenon, the fee band fires first" AD = **2026-08-29T11:05:26-07:00 = 2026-08-29T18:05:26Z**; the Stage B prompt log `e2d8f10` at 2026-08-29T19:07:37Z; the band arithmetic `9b4bd4f` at 19:15:55Z; the verdict `32dc10a` "docs: the band gate fires BAND-OPEN over 91-99c held to resolution" at 19:24:06Z. The amendment therefore preceded the arithmetic by 70 minutes and the verdict by 79 minutes. `git show f686036:REGISTRATION.md` confirms the amendment already carried both the "Made 2026-08-30" line (line 470 of that revision) and the "no price region where a documented effect could survive" rationale (line 475) at first commit — so the rationale on which the quantifier was later disambiguated is genuinely pre-existing.
  - The error is not isolated and is internally contradictory. Amendments 1 and 3 carry the same "Made 2026-08-30" from the same commit (PMExperiment/REGISTRATION.md:667, :751); the progress entry that reports them is headed "## Entry 3 — amendments 1 to 3: venue, fee band, scope — 2026-08-30" (PMExperiment/progress.md:202) and asserts "These amendments were written before any measurement, which is the only time they can honestly be written." (PMExperiment/progress.md:208-209). Amendment 4, committed **71 minutes later** in `4d75f66` (2026-08-29T19:17:21Z), is dated "**Made 2026-08-29**, before the band gate fired" (PMExperiment/REGISTRATION.md:783) — so the register carries an amendment dated 2026-08-29 that follows three amendments dated 2026-08-30. The same inversion appears in the hypothesis register: "## Amended 2026-08-30 — the venue split" (PMExperiment/HYPOTHESES.md:87) precedes "## Amended 2026-08-29 — the fee band fired BAND-OPEN" (:119).
  - The repository corrected exactly this class of error once, and stated the principle: "**Entry 6 states it was logged at 2026-08-29T19:32Z. That figure is wrong.** It was extrapolated from Entry 5.1's measured 19:28:45Z rather than read from the clock … **a timestamp inferred from a previous timestamp is documented, not measured.**" (PMExperiment/progress.md:652-663). The correction was never applied backwards to Entry 3 or to Amendments 1–3.
- **Recomputation (if any):** none beyond timezone conversion — all commit timestamps carry offset −07:00 and are converted to UTC by adding 7 hours; the conversion is checked against a case the repository states independently (Entry 10 records 2026-09-02T09:22:59Z; commit `2006ae6` AD = 2026-09-02T02:23:41-07:00 = 09:23:41Z).
- **What would resolve it:** an append-only correction in the shape of Entry 6.1, restating the made-date of Amendments 1–3 as 2026-08-29 and noting the commit that carries them.
- **Confidence:** HIGH — the commit dates are unambiguous and the internal contradiction with Amendment 4 is visible in the register alone.
- **Invalidated by later commits?:** no — the anchor is the terminal commit and the dates were never corrected.
- **Disclosed by authors?:** no — Entry 6.1 discloses and repairs a different timestamp error and states the governing principle, but the amendment dates were never revisited.

---

### DRAFT-p2-progress-7

- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** candidate 3's PROHIBITED verdict on Dune, and the ADR-012 element (2) standard applied across the three licence candidates
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Dune Terms of Service**, label **`Last updated on: June 3rd, 2026`** — a *last-updated* label, and the substitution for an *effective* label is disclosed here rather than silently made." — PMExperiment/docs/LICENCES.md:548-550
- **Evidence:**
  - ADR-012's element (2) is "the document's **effective date**", enforced in code by `_is_iso_date(claim.effective_date)` with no substitute (PMExperiment/pmexperiment/admissibility.py:136-156); `admit()` returns UNMEASURED "whatever it claimed — **including a claim that permission is absent**, because an unevidenced refusal is no more measured than an unevidenced permission" (PMExperiment/pmexperiment/admissibility.py:159-174). A Dune claim carrying no effective date would therefore return UNMEASURED; the record publishes **PROHIBITED** (PMExperiment/docs/LICENCES.md:23-25, :509-510; PMExperiment/progress.md:1021).
  - The same page refuses precisely this substitution when it would help a different question: "The docs page that does carry a credit rate prints no effective date; a schema.org `dateModified` exists in its metadata and **a modification timestamp is not an effective date**. … The tier price is recorded UNMEASURED rather than filled in." (PMExperiment/docs/LICENCES.md:592-597). A "Last updated on" label is a modification timestamp.
  - The asymmetry runs in the direction of convenience. Candidate 2 — the one candidate whose verdict could have been PERMITTED — was refused on exactly this element: "**Element (2) fails.** The dataset card prints no effective, last-updated or revision label … **The CC BY 4.0 legal code prints no date whatsoever**" (PMExperiment/docs/LICENCES.md:398-403). Candidate 3, whose verdict is PROHIBITED and therefore convenient for the terminal "there is none", was admitted on a last-updated label.
  - The repository's own flagship rule forbids this: "A venue may not be held to a **looser** reading than another because its verdict would be more convenient — and **the rule runs both ways.**" (PMExperiment/README.md:53-54; ADR-015, cited at PMExperiment/docs/LICENCES.md:534-541 as "**PROHIBITED on an unread instrument is a synthesized value** … ADR-012 has no direction-of-travel exemption"). The looser reading is applied here to reach the PROHIBITED end of the same rule.
  - Materiality is limited: an UNMEASURED verdict on Dune leaves "no candidate returns PERMITTED" intact (PMExperiment/docs/LICENCES.md:19, :703-704). What changes is the strength of one leg of the terminal claim — README's route ledger reads "third-party platforms | **PROHIBITED** / **UNMEASURED** | Dune's in-force terms; four others never retrieved" (PMExperiment/README.md:119) and the closure sentence leans on "Two venues and three third-party routes now say the same thing, in five documents, for four different reasons." (PMExperiment/progress.md:1169-1170).
- **Recomputation (if any):** none — this is a reading of the module's rule against the verdicts the documents publish.
- **What would resolve it:** either recording candidate 3 as UNMEASURED on element (2) alongside its quoted clauses, or a numbered amendment registering a last-updated label as satisfying element (2) — which would then also have to be applied to candidate 2's assessment.
- **Confidence:** MEDIUM — the substitution is disclosed and argued, and the verdict does not change; the finding is that the standard was relaxed only where relaxing it made the record stronger.
- **Invalidated by later commits?:** no — LICENCES.md's candidate sections are explicitly preserved as written ("**This section is appended, not an edit.** Everything above it stands as Stage D wrote it", PMExperiment/docs/LICENCES.md:795-797) and the project is closed.
- **Disclosed by authors?:** partly — the substitution itself is disclosed in the sentence quoted above (PMExperiment/docs/LICENCES.md:549-550); the inconsistency with the `dateModified` refusal 45 lines later and with candidate 2's treatment is not.

---

### DRAFT-p2-progress-8

- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the registered effect-band top of 8.00 points, the single input that produces BAND-OPEN
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**BAND-OPEN.** A surviving region exists inside the permitted subset: at entry prices 91–99c held to resolution, an effect in the upper part of the registered band clears the registered cost, requiring **5.85 points** of underpricing at the registered FX turnover against a band whose top is **8.00 points**." — PMExperiment/docs/BAND.md:15-18
- **Evidence:**
  - The band top's sole source is Krause: "Its top, 0.08, rounds the largest single-category published figure, Krause's 7.7 points." (PMExperiment/REGISTRATION.md:253-255, quoted into PMExperiment/docs/BAND.md:66-67).
  - Krause's figure is measured at longshots priced below 30c (PMExperiment/REGISTRATION.md:247-250), and this stage's own direction correction measured its exploitable entry price at **0.883** — outside the cell the band is registered for (PMExperiment/docs/BAND.md:155, :209, :333-334). The registration transplanted a sub-30c magnitude into a band declared "in the tail cell (snapshot prices 1–10c and 91–99c)" (PMExperiment/REGISTRATION.md:221-222), and after the transplant's own price was measured the band was not re-derived — Section 2's non-revision rule (PMExperiment/REGISTRATION.md:214-215) locked in the favourable edge.
  - It carries no n: "| Krause, sub-30c settling 4.0 % | NO | **0.883** | 0.077 | **not recorded** |" (PMExperiment/docs/BAND.md:155); "**The band's top has no n.** Bürgi sets the bottom with 313,972 prices; Krause sets the top and the registration records no sample size for it." (:335-336). Standing rule 13 is "**Every figure travels with its n in the same sentence.**" (PMExperiment/CLAUDE.md:44) — the verdict sentences that carry the 8.00 (PMExperiment/REGISTRATION.md:409-412, PMExperiment/docs/BAND.md:15-18, PMExperiment/progress.md:362-368, PMExperiment/report.md:61-64) do not.
  - Everything actually cited at the fired bucket fails: "With the registered k = 1, both magnitudes cited at 91–99c fail: Bürgi 0.020 … 0.0585 **fail**; Bürgi 0.030 … 0.0585 **fail**" (PMExperiment/docs/BAND.md:247-252), and at the FX-free limit the better of the two is "a **dead heat**" (:252). So the positive is carried by one number, from one source, at a price the same stage placed one decile away, with no sample size.
- **Recomputation (if any):** Krause's placement checked against the registration's own figures: sub-30c longshots settling YES 4.0 % with a bias of −0.077 imply a mean bucket price of 0.04 + 0.077 = 0.117, so the complement entry price is 1 − 0.117 = **0.883** and the NO-side underpricing is 0.96 − 0.883 = **0.077** — reproducing PMExperiment/docs/BAND.md:132 and :155 exactly. 0.883 falls in the 81–90 decile of PMExperiment/pmexperiment/registry.py:240.
- **What would resolve it:** a band top sourced to a magnitude measured at, or exploitable at, 91–99c, with its n; or a restatement of the verdict as conditional on a band edge whose support lies outside the cell it is applied in.
- **Confidence:** HIGH on the facts, MEDIUM on materiality — the repository states every element of this itself; what the framing does not carry is that BAND-OPEN has exactly one load-bearing input and that input's own price sits outside the fired region.
- **Invalidated by later commits?:** no — Section 3 is byte-identical from `9080186` to the anchor and the project is closed.
- **Disclosed by authors?:** yes — PMExperiment/docs/BAND.md:20-25 and :330-336, PMExperiment/REGISTRATION.md:431-443, PMExperiment/report.md:113-121, PMExperiment/README.md:143-149. The authors disclose the missing n, the 88.3c placement and the failure of both cited magnitudes, in the register, the band document, the report and the README. This finding is recorded for the positives ledger and the cross-repository pass, not as a discovery.

---

## What I checked and found sound

- **The band arithmetic itself.** Every cell of the Pass 1 table (PMExperiment/docs/BAND.md:199-210) reproduces exactly from the registered constants: R_H and R_X at k = 1, 12 and →∞ across all ten deciles, the crossing solutions at p = −0.3333 / +1.6667 / −1.0000 / +1.0000 (:219-220), the margins 4.84 / 2.15 / 2.83 / 0.15 points (:257-259), the slack figures 0.00195 and 0.00135 (:186, :265), the 16× ratio (:265), C(0.95) = 0.0785 and C(0.05) = 0.0515 (PMExperiment/REGISTRATION.md:338), and the "fee and half-spread alone total 0.0300 against a band bottom of 0.0200" statement (PMExperiment/docs/BAND.md:241-243). No arithmetic error was found anywhere in the band document.
- **The unit determination (Stage B Task 2).** Both readings reconstruct as claimed: Bürgi's 5c/3 % is a −0.02 gap and a −40.0 % return; 95c/98 % is +0.03 and +3.16 %; Krause's −0.077 read as a probability implies a mean bucket price of 0.117 and read as a return implies 0.043 (PMExperiment/docs/BAND.md:128-137, PMExperiment/progress.md:396-406). The conclusion that the band is in probability points is correct and the derivation is honest.
- **The direction correction.** The complement arithmetic at PMExperiment/docs/BAND.md:151-155 and PMExperiment/README.md:84-88 is right in every cell (0.95/0.02, 0.95/0.03, 0.883/0.077), and it is a correction that made the repository's own case *worse*, published prominently.
- **The registered constants never moved.** `git show <sha>:REGISTRATION.md` at `9080186`, `98ce2d4`, `f686036`, `9b4bd4f`, `4d75f66`, `34307b6`, `32dc10a`, `ebdc116`, `f789079`, `1b3124e`, `baa2bf3`, `905d552`, `03d16e7` all carry the same `C(p) = 0.04 + 0.01 + 0.03·p`; Sections 2 and 3 are byte-identical between the first Section 0 commit and the anchor. No cost component and no band edge was revised after a result was seen.
- **The quantifier disambiguation has a genuine pre-registration.** `git show f686036:REGISTRATION.md` shows the "no price region where a documented effect **could** survive" rationale present at first commit (line 475 of that revision), 79 minutes before the verdict. The existential reading is therefore not a bar written after the numbers existed; the ambiguity is disclosed and both readings are reported (PMExperiment/docs/BAND.md:116, :229-237). Under the strict reading the verdict would be BAND-EMPTY at 0/10 — disclosed by the authors, not concealed.
- **The Section 13 prior.** The register never backfilled it, the README says so plainly, and a test fails if it is filled (PMExperiment/progress.md:1478-1483, PMExperiment/README.md:168-175). This is the opposite of a bar lowered after data existed.
- **Section 16 closure conditions.** The repository states plainly that its own registered closure conditions were **not** met and that H1 does not close under Section 16 (PMExperiment/progress.md:1487-1490). A repository claiming too much would have claimed the closure.
- **Outcome blindness.** No statistic relating a price to an outcome exists anywhere in the snapshot; `data/` holds only `.gitkeep`; `scripts/` holds only `.gitkeep`; `power.py` and `band.py` reference no resolution field and `tests/test_guards.py` enforces it. The one exception (`result` present on 2 settled records) is a pre-registered access-gate condition capped at 5 records (PMExperiment/REGISTRATION.md:145-147, `ACCESS_OUTCOME_PRESENCE_MAX_RECORDS = 5` at PMExperiment/pmexperiment/registry.py:254), it is recorded rather than rounded away (PMExperiment/README.md:101-106, PMExperiment/progress.md:1506-1513), and no statistic was computed from it.
- **The `missing_elements()` blind spot** (a clause check that cannot tell a quotation from a paraphrase) is disclosed by the authors at PMExperiment/README.md:47-49, PMExperiment/docs/ACCESS.md:291-300 and PMExperiment/progress.md:1434-1440, and is deliberately not repaired with the reason stated. Not a finding.
- **The self-conviction on the Kalshi finding** (two ADR-012 elements of three, `Effective` 0 occurrences, `Last Updated` 0) is disclosed at PMExperiment/progress.md:1000-1010 and PMExperiment/README.md:65-74. Not a finding.
- **Stage D's "there is none" caveat.** The completeness limits (PMExperiment/docs/LICENCES.md:665-688) were written into the same document as the terminal verdict, before the route that falsified it surfaced, and the falsification is recorded rather than buried (PMExperiment/progress.md:1442-1449). This is the pattern a repository claiming too much does not produce.
- **The Kalshi Internal Use route.** It is labelled EXISTS-AND-UNTRAVELLED, recorded UNMEASURED under the repository's own procedure, and explicitly not written as a licence, a refusal or a reopening (PMExperiment/docs/ACCESS.md:220-315). The distinction between "closed on access" and "the operator stopped paying" is drawn by the authors themselves (PMExperiment/progress.md:1468-1472).
- **Stage A's settled-history depth negative** (earliest retrievable close between 2024-01-01 and 2024-05-31, n = 6 bracketing probes, PMExperiment/docs/ACCESS.md:72) is phrased as a property of the keyless surface and not of the archive, and that phrasing survived contact with the Kalshi reply (PMExperiment/docs/ACCESS.md:317-326). It is a negative that was written narrowly enough to remain true.
- **`data/`** contains only `.gitkeep` in the snapshot; no unanchored data was read from the live repository for this part.

Where I expected the thesis to hold and it did not: I looked for a bar lowered, widened or re-specified after the deciding numbers existed (hunt item 2), an amendment rescuing a verdict (item 3), and a limitation disclosed in a footnote and dropped from the README or the register (item 4). I found none of the three. Amendments 1–3 predate the arithmetic in git; Amendment 4's turnover is registered at the value that biases *against* the surviving band; Amendment 6 retracts the repository's own premise rather than rescuing it; and every qualification attached to BAND-OPEN in `docs/BAND.md` is carried through to `REGISTRATION.md` Section 15.2, `report.md`, `HYPOTHESES.md` and `README.md` without softening. The findings above are about arithmetic and design that the disclosures do not reach, not about disclosure failures.

## Live-repo access log

Live repository touched read-only for git history only (`git log`, `git show`), path `/home/kiros-li/Documents/GitHub/PMExperiment`. No untracked or gitignored data was read for this part.

Before, `git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain`:

```
```

(empty — clean tree)

After, `git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain`:

```
```

(empty — clean tree; recorded at the end of the session, see the trailing check)
