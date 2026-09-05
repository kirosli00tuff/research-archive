# VRPExperiment — Agent C findings (referee and verifier)

Repository: `VRPExperiment`
Anchored SHA: `d37cf6d190dfdaef8e613daf099a507fe1a77dcf` (main, 2026-08-30) — also the live `HEAD`,
so the anchor is the repository's last commit and nothing in this report can be overtaken by a
later commit in this repository.
Agent: **C** (referee; no thesis). Consolidated 2026-09-05.

Inputs merged: `findings/agentC/verification/VRPExperiment.inventory.md` and `.inventory.json`;
`findings/agentC/verification/VRPExperiment.verification.md` and `.claims.json`;
`findings/agentC/provenance/VRPExperiment.md` and `.json`.
Snapshot re-read for this pass: `SNAP/VRPExperiment/` — **every quote below was re-located in the
snapshot at the line cited**, and every load-bearing figure was recomputed first-hand during
consolidation. Live git objects and the untracked `data/` tree were re-read read-only on
2026-09-05 05:50–05:53Z for the commit timeline, the fixture diff, the `src/vrp` tree hashes, the
`progress.md` append history and the `data/raw/` mtimes; see §Live-repo access log.
Each finding carries a **Consolidation check** bullet recording what that re-check found. Eight
draft findings entered consolidation, **two pairs merged, none dropped, six leave it**.

**Independent citation check, 2026-09-05.** Every one of the six was then re-checked by a separate
checker that re-located each verbatim quote in `SNAP/VRPExperiment/`, re-ran every load-bearing
figure from the primitives with its own implementation, and re-derived the git and mtime evidence
first-hand. Each finding carries a **Citation check** bullet recording the outcome. **Four verified
with no correction (-2, -3, -5, -6); two carry citation corrections (-1, -4); none was dropped.**
Every correction was re-confirmed against the snapshot by the applier before being written, and one
proposed correction was declined on the evidence and is recorded as declined under **-1**. No
finding's substance, class, severity, label or direction changed.

**Anchoring caveat that governs the raw-data figures.** `data/` is gitignored. The four raw series
(`data/raw/task6/{dvol,underlying}_{BTC,ETH}_daily.json`), every TASK 3 page capture and every
`data/raw/` mtime quoted here exist only in the working tree and are **UNANCHORED** — read
2026-09-05, they may have changed since the 2026-08-30 anchor. They are authenticated in practice
rather than cryptographically: an independently written implementation of the registered estimators
reproduces roughly forty stored figures across two assets to full stored precision, which altered
inputs could not do. The code, by contrast, *is* anchored and cryptographically tied: all eleven
SHA-256 digests in the tracked `reports/task6/task6.latch.2.json` match the snapshot files at
`d37cf6d` byte for byte (re-verified in this pass, 11/11).

---

## Summary

The chain from raw data to closure is closed and it holds. Every number that decides this
repository's verdict reproduces — the premium means, the HAC standard errors, the t statistics, the
one-sided p-values to eleven significant figures, the CI lower bounds, the rebalance distributions,
the commission arithmetic and the two capital thresholds — and the registered decision rule fires as
written. The registration is genuinely pre-data: the first fetched byte on disk postdates the
registration commit by 16 seconds, `REGISTRATION.md` lines 1–528 are byte-identical from that commit
to the anchor, and the estimator file was written before the first byte of TASK 6 data existed —
9.6 minutes before it from its first commit (`c51b4f7`, 06:49:19Z) and 8.3 minutes before it from
its last write (mtime 06:50:39.475Z, against the first TASK 6 byte at 06:58:57.705Z) — and never
altered. Six findings survive consolidation and **none of them moves the verdict**.
One is S2: the artifact's flat assertion that the ether premium "does not cover the commission" rests
on a 3.09 bps gap that is **0.06 of one standard error** — the repository's own estimator cannot
separate that comparison from a tie, and at a rebalance count of 10 instead of the registered median
11 the sentence reverses. The registered rule that actually closes MET — CI lower bound against twice
the pessimistic cost — fails by 8.57× and survives every bandwidth and bootstrap tried, so the
closure itself stands. The other five are a robustness interval stated at 1.88× its measured length,
three hand-written timestamp records that contradict the machine evidence around them, an amendment
whose completeness claim omits one replaced artifact, and a units label wrong by a factor of 100 that
affects no computed figure. Four items could not be checked and are recorded as unverifiable rather
than guessed at.

---

## Verification scoreboard

### Claims

| Status | Count |
|---|---|
| VERIFIED | **25** |
| CONTRADICTED | **3** |
| UNVERIFIABLE | **4** |
| **Total claim rows audited** | **32** |

Counted separately below and not in that table: **39 derived quantities** (38 VERIFIED, 1
CONTRADICTED — the revision-gap of finding **-2**, which is the same defect as one of the three
contradicted claim rows), **4 intervals** (all VERIFIED) and **26 test-statistic-shaped quantities**
(all VERIFIED). Across all four kinds: **101 items, 93 VERIFIED, 4 CONTRADICTED, 4 UNVERIFIABLE**.

Three of the four UNVERIFIABLE rows are unverifiable only *in part*, because the sentence they come
from was split: `HYPOTHESES.md:22` verifies exactly on 1,985 / 1,992 / 30 dropped / n = 1,955 and the
2021-03-24 → 2026-07-30 span, and is unverifiable only on the two hourly row counts (47,696 / 47,858)
that the driver writes to stdout and stores nowhere; `README.md:122` verifies on "50 tests" (28 + 22
`def test_`) and on the 17 source files beside it, and is unverifiable only on the "mypy strict
clean, ruff clean" pass/fail, which would require executing the repository's tooling; and
`venue_table.md:95-97` verifies on both carried *notional* drifts (+20.099 %, +28.597 %) and is
unverifiable only on the ORBExperiment figures carried in the same row. The fourth — the BTCY/ETHY
management-expense ratios — is wholly unverifiable and decides nothing.

**MUST-VERIFY claims (the 8 marked `★` in the inventory), with status:**

| # | Claim | Status |
|---|---|---|
| MV1 | "The ether premium's point estimate is **119.05 bps**. The **central, commission-only, lower-bound cost is 122.14 bps**. **The premium does not cover the commission.**" (`docs/ARTIFACT.md:212-214`) | **VERIFIED on the arithmetic** — premium 119.0521, cost 32.570638 + 11 × 8.142659 = **122.139891**, gap 3.0878 bps, all exact. The *characterisation* of that gap as decisive is finding **-1** |
| MV2 | "Required for HARVESTABLE: **2.0 × 162.853 = 325.706 bps. FAILS BY 8.57×.**" (`HYPOTHESES.md:21`) | **VERIFIED** — 162.853188, 325.706376, 325.706376/38.0124 = **8.5684×** |
| MV3 | BTC "mean 0.086607 … 198.111 bps, n = 1,955, HAC bw 30, SE 0.014709, t = 5.888, p = 2.297 × 10⁻⁹, CI lower 142.740 bps, positive 73.86 %" (`HYPOTHESES.md:19`) | **VERIFIED** — reproduced from the raw series to every stored decimal; p = 2.2965959114e-09 |
| MV4 | ETH "mean 0.052045 = 119.052 bps, n = 1,955, SE 0.021528, t = 2.418, p = 7.859 × 10⁻³, CI lower 38.012 bps, positive 64.55 %" (`HYPOTHESES.md:19`) | **VERIFIED** — p = 7.8585401067e-03; t and CI lower re-derived independently in this pass |
| MV5 | "rebalances, registered ±0.10 band … **median 11, p90 16** (BTC max 20, ETH max 22) … 1,955 paths per asset" (`README.md:61`) | **VERIFIED** — BTC 2/11/10.8077/16/20, ETH 2/11/10.9913/16/22, n = 1,955 each, exact integers |
| MV6 | "MET option $245.62 $0.20 **8.143** **16.285**"; "MET 4 × $0.20 = $0.80 **32.571**"; "MBT 4 × $0.85 **4.352**" (`docs/COSTS.md:78, 88-89`) | **VERIFIED** — 8.142659 / 16.285319 / 32.570638 / 4.352022 / 1.088006 |
| MV7 | "Micro Ether option **$245.62** **4.07×** **407.1 %** … Micro Bitcoin option **$7,812.46** **0.128×** **12.80 %**" (`docs/ARTIFACT.md:142-143`) | **VERIFIED** — notionals re-derived from the two measured spot prices; 4.0713×, 0.128001, 390.62×, 0.256 %, 0.814 % |
| MV8 | "clears the registered 2× hurdle by **3.28×**, and would still clear it at the maximum possible **29** rebalances … must total **≤ 49.61 bps**" (`docs/ARTIFACT.md:222-231`) | **VERIFIED** — 142.7401/43.520223 = **3.2799×**; at 29 rebalances 35.904184 bps and 2× = 71.808368 ≤ 142.7401; 142.7401/2 − 21.760111 = **49.6099 bps** |

**8 VERIFIED, 0 CONTRADICTED, 0 UNVERIFIABLE.** Every claim the closure rests on reproduces. The one
finding that touches a MUST-VERIFY row (**-1**, on MV1) challenges the certainty attached to a
verified arithmetic comparison, not the arithmetic.

### Intervals

| Metric | Count |
|---|---|
| Intervals audited | **4** |
| Independence doubtful | **0** |
| Recomputed | **4** |
| Conclusion moved | **0** |

All four reported intervals are the same object: a **one-sided 95 % lower bound**,
`mean − t_crit(n−1, 0.05) · SE`, at `src/vrp/sealed_read.py:287-288`. The two primaries use a
Newey–West Bartlett HAC standard error at **bandwidth 30** — the registered remedy for the
overlapping 30-day forward windows, fixed at `REGISTRATION.md:366-371` before any data existed — so
they assume no independence to begin with. The bandwidth is well matched to the data: measured
ρ₁ = 0.952 (BTC) and 0.960 (ETH), falling below 0.05 at lag 25 and lag 30 respectively. The two
robustness intervals do assume independence ("IID by construction", `premium[::30]`, n = 66), and
that assumption **holds empirically**: Ljung–Box(5) = 1.232 (p = 0.94) for BTC and 2.467 (p = 0.78)
for ETH. Nothing is doubtful; nothing was recorded as such.

**The independence assumption was attacked deliberately and it did not break.** Widening the HAC
bandwidth to 45, 60, 90, 120 and 180, and a moving-block bootstrap at L = 30/90/180 with 4,000 draws,
move both bounds but move no stated comparison: the MBT clearance falls from 3.28× to **3.05×** at
bandwidth 180 and still clears; the MET failure factor **grows** from 8.57× to 23.4×, i.e. the
sensitivity runs in the direction that strengthens the repository's own conclusion; and ETH's
one-sided p stays below 0.05 at every bandwidth tried (worst 0.0313), so the branch that fires is
unchanged. The registered bandwidth-30 SE sits at the low end of the plausible range but inside it.

One estimator convention is recorded and not raised: `newey_west_se` divides autocovariances by `n`,
so at bandwidth 0 it returns the *population* SE. At n = 66 that is 0.77 % below the `ddof=1` sample
SE and moves the two robustness bounds by 0.6–0.8 bps; at n = 1,955 it is invisible.

### Tests

| Metric | Count |
|---|---|
| Test-statistic-shaped quantities audited | **26** |
| Tail mismatch | **0** |
| Degrees-of-freedom issue | **2** (recorded, immaterial — see below) |
| Multiplicity-correction mismatch | **0** |

Every inferential test in this repository is the same one: the single registered one-sided t-test of
**H₀: mean(VRP) ≤ 0** at α = 0.05 (`REGISTRATION.md:360-366`), evaluated with the repository's own
incomplete-beta Student-t survival function (`sealed_read.py:192-215`). **That implementation agrees
with `scipy.stats.t.sf` to eleven significant figures** on every reported p-value.

**Tail: 0 mismatches.** Every reported p is upper-tail, matching the registered one-sided
H₁ (`mean(VRP) > 0`). The useful check is ETH Q3, where a negative t = −0.246 correctly yields
p = 0.597 rather than 0.403.

**Degrees of freedom: 2 rows recorded, and they move nothing.** The two primary tests pair a
fixed-bandwidth HAC standard error — whose effective sample is roughly 65 independent 30-day windows
— with a Student-t critical value at `dof = n − 1 = 1954` (`sealed_read.py:285`). Using dof 65 would
raise `t_crit` from 1.6456 to 1.6686 and lower the ETH bound by 1.1 bps (38.01 → 36.9) and the BTC
bound by 0.8 bps (142.74 → 141.96). Every stated comparison survives: the MET failure factor rises
from 8.57× to 8.82×, the MBT clearance falls from 3.280× to 3.262×, and ETH's p stays below 0.05.
This is a convention fixed in code before the data existed, it is generous rather than punitive in
one direction only, and it is recorded here rather than raised as a finding because no figure that
decides anything moves. The other 24 rows carry no dof question: the quarterly and non-overlapping
tests are IID-SE tests where `n − 1` is simply correct, and the remaining rows are order statistics
and distributional summaries, not tests.

**Multiplicity: 0 mismatches, and this is the place a correction would have been the error.** The
registered endpoint is a conjunction — a premium exists **and** a venue is reachable — and the
two-asset premium component is itself an all-must-reject conjunction. An intersection-union test
takes the full nominal α per component; `REGISTRATION.md:381-393` says so, cites Berger (1982) for
it, and applies no correction. **The correction applied matches the decision rule it feeds.** A
Bonferroni or Šidák adjustment here would have lowered the level below nominal and made
SIGNAL_ABSENT *easier* to reach — the mismatch the registration explicitly names and avoids. The
four-quarter stability split likewise carries no correction and needs none: it is used to *weaken*
the ETH claim, and a correction would leave even fewer quarters significant and therefore strengthen
the stated limitation (disclosed at `HYPOTHESES.md:23` and `docs/ARTIFACT.md:100-102`).

One design-stage sentence is recorded and not raised: `REGISTRATION.md:430-433` joins four figures
that each reproduce (119.375 weeks, 477.502 weeks, 6.18517, d = 0.50786, 1.016 = 2 × 0.508,
6.19/1.016² = 6.0) into a claim that is internally garbled — halving an effect raises the required n
from 24 to ≈ 96, and n ≈ 6 is what a *doubled* effect needs. It is a pre-data power note that decides
nothing; the achieved n of 1,955 is 2.7× the registered depth.

### Provenance

| Status | Count |
|---|---|
| SUPPORTED | **26** |
| NOT_SUPPORTED | **1** |
| PARTIAL | **5** |
| UNVERIFIABLE | **0** |
| **Total provenance items audited** | **32** |

Split by kind: **23 registration claims** — 20 SUPPORTED, 2 PARTIAL (P18, P21), 1 NOT_SUPPORTED
(P5) — and **9 parameter/artifact changes after data existed** — 6 SUPPORTED, 3 PARTIAL (C4, C5, C6).

**The pre-registration guarantee verifies.** `7827592` ("TASK 2 — REGISTRATION.md, committed before
any network call") is dated **2026-08-30T04:47:08Z** from the raw commit object, its parent is
`8bcc5bf` exactly as `REGISTRATION.md:3-4` claims, and the earliest fetched byte anywhere under
`data/` is `data/raw/robots/www.deribit.com.robots.txt` at **04:47:24Z — 16 seconds later**. No blob
in any of the four preceding commits contains a network result. `REGISTRATION.md` has exactly two
commits, and lines 1–528 are byte-identical between them, so the hurdle (factor 2.0), the estimator
(Newey–West bandwidth 30), the ±0.10 rebalance band, the median/p90 assignment, the bps conversion
and the priors are all fixed pre-data and were never edited in place. `progress.md` is strictly
append-only across all nine commits that touch it (re-verified in this pass: additions
49/116/120/101/130/98/55/80/112, **deletions 0 in every one**). `src/vrp/sealed_read.py` was extended
exactly once and the diff is a pure append at `@@ -304,3 +304,102 @@`; not one line of the estimator
was altered after it was written — **9.6 minutes** before the first byte of TASK 6 data existed
measured from its first commit (`c51b4f7`, 06:49:19Z) and **8.3 minutes** measured from its last
write (mtime 06:50:39.475Z), against that first byte at 06:58:57.705Z. The
`src/vrp` tree hash is **identical** at `adac707`, `ef07f19` and the anchor.

The single NOT_SUPPORTED item is P5, the TASK 3 venue table's stated measurement window — finding
**-3**. The two PARTIAL registration claims are P18 (Amendment 1's completeness — finding **-4**;
its code half is fully verified) and P21 (the 08:00 UTC observation instant: the *ordering* is
supported, the justifying 400-day timestamp probe has no stored artifact). Of the three PARTIAL
parameter changes, C4 is finding **-4**, C6 is a one-row in-place edit whose substance is disclosed
eleven lines below it, and C5 is P21 seen from the other side.

### Merge and de-duplication record

| Draft | Origin | Disposition |
|---|---|---|
| DRAFT-V-1 | verification §5 | → **AUDIT-C-VRPExperiment-1**, unchanged in substance |
| DRAFT-V-2 | verification §5 | **merged** with DRAFT-P-1 → **-2** |
| DRAFT-P-1 | provenance §3 | **merged** with DRAFT-V-2 → **-2** |
| DRAFT-V-3 | verification §5 | **merged** with DRAFT-P-2 → **-3** |
| DRAFT-P-2 | provenance §3 | **merged** with DRAFT-V-3 → **-3** |
| DRAFT-P-4 | provenance §3 | → **-4**, unchanged |
| DRAFT-P-3 | provenance §3 | → **-5**, one figure corrected |
| DRAFT-V-4 | verification §5 | → **-6**, unchanged |

**Eight drafts in, two merges, six findings out. Nothing was dropped**: all eight carry a verbatim
quote that re-locates in `SNAP/VRPExperiment/` at the line cited, and all eight carry a figure that
recomputed in this pass. The two merges were both genuine duplicates — the same defect found
independently by the verification pass and the provenance pass, from different evidence.

Two reconciliations were required:

* **Severity of -2.** The verification draft graded the ≈70-minute error **S4** (hygiene); the
  provenance draft graded it **S3**. Resolved to **S3**: the figure is not decoration but the sole
  quantitative content of the revision-safety check that justifies taking a single sealed read, and
  it is stated at 1.88× its measured value in five places including the artifact's own `gap` field.
* **Class of -2.** The provenance draft filed it PROVENANCE, the verification draft
  INTERNAL_INCONSISTENCY. Resolved to **INTERNAL_INCONSISTENCY**, which is the more precise: the
  contradicting timestamps sit inside the very file that carries the claim.

One correction was made to a draft's supporting arithmetic. The provenance pass reported the
`progress.md` append diffs as "+68/-0, +43/-0, +83/-0, +104/-0, +84/-0, +95/-0, +94/-0, +39/-0"
(eight values). Re-run in this pass, `git log --numstat -- progress.md` gives **nine** commits with
additions 49, 116, 120, 101, 130, 98, 55, 80, 112 and **zero deletions in every one**. The
substantive claim — `progress.md` is strictly append-only and no narrative was ever rewritten — is
confirmed; the per-commit line counts in the draft are not reproduced and are corrected here. No
finding depends on them.

---

## Findings

Six. Ordered by descending severity. **None of them changes the registered verdict**, and each says
so explicitly.

**Schema note on `Direction`.** COMMON_RULES enumerates two directions, A (closed too early) and B
(claimed too much). Findings **-3**, **-4**, **-5** and **-6** are recorded as `neutral`, which is
outside that enumeration. This is a deliberate deviation and is flagged as such: each of the four is
a hygiene or provenance defect whose corrected reading moves the repository's position in *neither*
direction — in **-4** the undisclosed change actually weakened the authors' own evidence — and
forcing one of A or B on them would assert a direction the evidence does not support. Where a
direction does apply it is given: **-1** is A with B recorded as an equally fair reading, and **-2**
is B.

### AUDIT-C-VRPExperiment-1
- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** H1 closure, the MET (Micro Ether) route — the margin-free leg of the
  cost comparison in `docs/ARTIFACT.md` and `HYPOTHESES.md`
- **Direction:** A (closed too early). Direction B is an equally fair reading — the sentence
  overstates the evidence — and the two readings differ only in emphasis, because the registered rule
  closes MET independently either way.
- **Class:** STATISTICAL
- **Severity:** S2 — a label ("decided, and not by a close margin") contradicts its own evidence
- **Label:** DERIVED
- **Claim challenged (verbatim):** "**Micro Ether — decided, and not by a close margin.**
  The ether premium's point estimate is **119.05 bps**. The **central,
  commission-only, lower-bound cost is 122.14 bps**. **The premium does not cover
  the commission.**" — VRPExperiment/docs/ARTIFACT.md:211-214. And: "And the failure does not depend
  on the margin at all: **the ETH premium's point estimate, 119.052 bps, is below the central
  commission-only cost of 122.140 bps.**" — VRPExperiment/HYPOTHESES.md:21
- **Evidence:**
  - **The arithmetic is right and is not what is challenged.** ETH `mean_bps` = 119.0521, n = 1,955
    (VRPExperiment/reports/task6/real_attempt2_result.json, `assets/ETH/primary_overlapping_hac`,
    line 141); central cost = 0.80/245.62 × 10⁴ + 11 × 0.20/245.62 × 10⁴ = **122.139891 bps** from
    VRPExperiment/reports/task5/commission_bps.json:51-53 and :5 with the registered median
    rebalance count 11 at real_attempt2_result.json:164. The gap is **3.0878 bps**, 2.53 % of the
    cost.
  - **The gap is 0.06 of one standard error.** The repository's own HAC standard error on that mean
    is 0.021528 in decimal volatility (VRPExperiment/HYPOTHESES.md:19;
    real_attempt2_result.json:139), which at the registered conversion of 2,287.4639 bps per unit
    (VRPExperiment/src/vrp/sealed_read.py:43-51) is **49.2445 bps**. 3.0878/49.2445 = **0.0627 SE**.
    Testing the stated conclusion directly, H₀ *true mean = 122.140 bps* gives a two-sided
    **p = 0.9500** at n = 1,955, dof 1,954. The data are as consistent with the premium exactly
    covering the commission as with a very wide band of other values.
  - **The comparison turns on one integer.** The central cost uses the registered median rebalance
    count of 11, and the ETH ±0.10 distribution has median 11 with mean **10.9913** and min 2, max 22
    (real_attempt2_result.json:159-168) — the median sits just over the 10/11 boundary, with 44.8 %
    of the 1,955 paths at ≤ 10 and 53.4 % at ≤ 11. At a count of 10 the central cost is
    **113.99723 bps**, *below* the 119.0521 bps premium, and the quoted sentence reverses.
  - **The registration supplies the honest framing that the artifact drops.** The reported premium
    figure for a decision is a one-sided 95 % lower bound of **38.012 bps** (HYPOTHESES.md:19), and
    the registered decision rule compares that bound against twice the pessimistic cost
    (VRPExperiment/REGISTRATION.md:312-316), not the point estimate. That rule fails by **8.5684×**
    and is robust to every bandwidth and bootstrap tried (§Intervals).
- **Recomputation:** inputs — the ETH premium series rebuilt from
  `data/raw/task6/dvol_ETH_daily.json` and `underlying_ETH_daily.json` (live untracked, read
  2026-09-05T03:57Z) through an independent implementation of
  VRPExperiment/src/vrp/sealed_read.py:54-301, plus the stored rates in
  VRPExperiment/reports/task5/commission_bps.json. Method — reproduce the mean and HAC SE (they match
  the stored artifact to 6 dp), convert the SE to bps at the registered factor, express the stated
  gap in SE units, test H₀ that the true mean equals the stated cost, and re-run the ±0.10 rebalance
  rule to get the full count distribution. Result — gap 3.0878 bps; SE 49.2445 bps; 0.0627 SE;
  two-sided p 0.9500; 53.4 % of ETH paths at ≤ 11 rebalances; cost at 10 rebalances 113.99723 bps.
  Tolerance ±0.001 bps.
- **What would resolve it:** one sentence recording that the point-estimate comparison is within
  0.06 standard errors and is therefore illustrative rather than decisive, leaving the decisive
  statement where it belongs — the registered CI-lower-against-2×-pessimistic test, which fails by
  8.57×. The challenged sentence occurs in **five** places, not two, and the remedial sentence is
  needed beside each: `docs/ARTIFACT.md:211-214`, `HYPOTHESES.md:21`, `README.md:23-24` ("charges
  **more in commission alone (122.14 bps) than the ETH premium is worth**"), `HYPOTHESES.md:56`
  ("The point estimate (119.052 bps) does not cover the central commission (122.140 bps).") and
  `progress.md:788-790` ("The ETH premium's **point estimate, 119.052 bps, is below the central
  commission-only cost of 122.140 bps.**").
- **Confidence:** MEDIUM — the arithmetic verifies exactly and two *disclosed* asymmetries push the
  comparison the repository's way (three of five cost legs are `Absent(not_served)` and non-negative,
  so the true cost exceeds 122.14 bps — HYPOTHESES.md:24; and REGISTRATION.md:333-336 registers that
  discrete hedging earns less than the conversion implies, so the premium side is an upper bound).
  What is not supported is the *stated certainty* of a comparison the repository's own estimator
  cannot separate from a tie.
- **Invalidated by later commits?:** no — the figures are fixed by a spent latch
  (`reports/task6/task6.latch.2.json`) and by tracked artifacts at the anchor, and `d37cf6d` is the
  repository's last commit.
- **Disclosed by the authors?:** **no.** `HYPOTHESES.md:23` discloses instability, absent tail risk
  and the absence of a simulated sleeve, and `HYPOTHESES.md:24` discloses that every cost figure is a
  strict lower bound — but no document puts a standard error, an interval or the words "within noise"
  next to the 119.052-against-122.140 comparison. Re-run in this pass: `grep -niE "sampling
  error|standard error of the premium|within noise|close margin|3\.088|not decisive|illustrative"`
  over README.md, HYPOTHESES.md, docs/ARTIFACT.md, docs/HANDOVER.md, DECISIONS.md and progress.md
  returns exactly one line — `docs/ARTIFACT.md:211`, the claim itself.
- **Consolidation check:** verified. Quote EXACT at `docs/ARTIFACT.md:211-214` and
  `HYPOTHESES.md:21` in SNAP. Recomputed first-hand at consolidation from the tracked artifacts:
  MET round trip 32.570638, per-rebalance fill 8.142659, central 122.139891, pessimistic 162.853188,
  2× pessimistic 325.706376, gap 3.0878 bps, bps-per-unit 2287.4639, SE 49.2445 bps, gap/SE 0.0627,
  two-sided p 0.9500, cost at 10 rebalances 113.99723 < 119.0521, failure factor 8.5684×. The ETH
  ±0.10 median (11) and mean (10.9913) were re-read from `real_attempt2_result.json` and are
  consistent with the draft's 44.8 %/53.4 % split. ETH `t` and `ci_lower` were re-derived from the
  stored mean and SE at dof 1954 and reproduce the stored 2.4175 and 0.016618 exactly. Kept
  unchanged.
- **Citation check:** corrected — an independent checker re-ran the quote, the figures and the
  recomputation (quote EXACT at `docs/ARTIFACT.md:211-214` and `HYPOTHESES.md:21`; every figure
  reproduced from the raw series with a separate numpy/scipy implementation to full stored
  precision; recomputation reproduced). Three changes applied, each re-confirmed in SNAP by this
  applier: (i) the median rebalance count 11 is at `real_attempt2_result.json:164`, **not :163** —
  line 163 carries `"mean": 10.9913`; (ii) the commission inputs USD 0.80 and notional 245.62 are at
  `commission_bps.json:51` and `:52`, with the derived `"bps": 32.5706` at `:53`, so the citation is
  now **`commission_bps.json:51-53` and `:5`**; (iii) "what would resolve it" now names all **five**
  occurrences of the challenged sentence — `README.md:23-24`, `HYPOTHESES.md:56` and
  `progress.md:788-790` were missing, and all three were located in SNAP in this pass. One
  suggestion was **not** applied: the checker proposed aligning the MV1 scoreboard row from
  `docs/ARTIFACT.md:212-214` to 211-214, but MV1 quotes only the three sentences that begin on line
  212 and does not include the bolded heading on 211, so **:212-214 is the correct span for that
  quote** and is left as it stands; 211-214 is correct for this finding, which does quote the
  heading. Substance, severity S2, label DERIVED and direction unchanged; the checker independently
  confirmed the closure does not move (registered rule fails by 8.5684×, growing to 23.43× at
  bandwidth 180 and 8.83× at dof 65).

### AUDIT-C-VRPExperiment-2
- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** TASK 4 / ADR-009 — the data-revision re-check
  (`reports/task4/revision_recheck.json`), which is the evidence that Deribit does not silently
  revise history and therefore that a single sealed read is safe
- **Direction:** B (claimed too much) — the interval over which the venue was shown not to revise is
  a little over half the interval stated
- **Class:** INTERNAL_INCONSISTENCY (the provenance pass filed the same defect as PROVENANCE; both
  fit, and the contradicting timestamps sit inside the file that carries the claim)
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "| **revision** | **all six fixed windows byte-identical after
  ≈ 70 minutes** | 6 windows × 169 rows |" — VRPExperiment/README.md:91. Repeated at
  `docs/ARTIFACT.md:280` ("re-fetched ≈ 70 minutes later"), `DECISIONS.md:190` ("re-checked after
  ≈ 70 minutes"), `progress.md:818-820` ("The six data-only baselines recorded at 06:05Z were
  re-fetched at ~07:15Z, a gap of **≈ 70 minutes**"), and inside the artifact itself as
  `"gap": "≈70 minutes"` — VRPExperiment/reports/task4/revision_recheck.json:3
- **Evidence:**
  - The artifact's own machine-written stamps, all six windows (n = 6): `taken_at` =
    2026-08-30T06:26:08.230Z, .399Z, .569Z, .772Z, .941Z and 06:26:09.144Z; `recheck_taken_at` =
    07:03:22Z (window 0) and 07:03:23Z (windows 1–5) —
    VRPExperiment/reports/task4/revision_recheck.json:19,25 and the five sibling windows. The elapsed
    interval is **37.23–37.24 minutes** on every window. The stated figure is **1.88×** the measured
    one.
  - The baseline artifact agrees with the stamps and not with the prose: `"retrieved_at":
    "2026-08-30T06:25:49.532Z"` — VRPExperiment/reports/task4/rate_and_revision_baseline.json.
    Neither 06:05Z nor 07:15Z appears anywhere in either artifact.
  - `progress.md:819`'s claimed re-fetch time of **~07:15Z is after `d37cf6d`'s own commit time of
    07:08:02Z** — after the commit that adds the file, which cannot be.
  - **The substantive result verifies.** All six `data_only_sha256` equal their
    `recheck_data_only_sha256` and all six row counts are 169 → 169 (re-checked in this pass, 6/6).
    What is wrong is the stated length of the interval, not the finding of no revision.
- **Recomputation:** inputs — the twelve timestamps in
  VRPExperiment/reports/task4/revision_recheck.json; method — parse both stamps per window as
  ISO-8601 UTC and difference them; result — 37.2295, 37.2433, 37.2405, 37.2371, 37.2343, 37.2309
  minutes. Tolerance ±0.01 min.
- **What would resolve it:** replace "≈ 70 minutes" with "≈ 37 minutes" at `README.md:91`,
  `docs/ARTIFACT.md:280`, `DECISIONS.md:190`, `progress.md:819-820` and in the artifact's own `gap`
  field, and correct progress.md's 06:05Z / ~07:15Z to 06:26Z / 07:03Z.
- **Confidence:** HIGH — the contradicting timestamps are machine-written and sit in the same tracked
  JSON as the claim.
- **Invalidated by later commits?:** no — `revision_recheck.json` is added in the anchor commit
  itself and is the repository's last word on the question.
- **Disclosed by the authors?:** no. The repository does disclose that the *CryptoDataDownload* arm
  of the same re-check is "a **weak** test and is recorded as one" (`progress.md:823-826`), but
  nowhere records that the 70-minute figure is not what its own artifact says.
- **Consolidation check:** verified. Quote EXACT at `README.md:91`; the four repetitions re-located
  by grep at `progress.md:820`, `DECISIONS.md:190`, `docs/ARTIFACT.md:280` and
  `revision_recheck.json:3` (five occurrences of "70 minutes" in the snapshot, no more, no fewer).
  Re-differenced all six window pairs at consolidation: 37.2295–37.2433 min, and all six data digests
  and row counts re-confirmed identical. 70/37.23 = 1.880. Merged from DRAFT-V-2 (S4) and DRAFT-P-1
  (S3); severity resolved to S3 and class to INTERNAL_INCONSISTENCY, substance unchanged.
- **Citation check:** verified (quote EXACT at `README.md:91`; figures verified — all four
  repetitions re-located at `docs/ARTIFACT.md:280`, `DECISIONS.md:190`, `progress.md:820` and
  `revision_recheck.json:3`, and a whole-snapshot grep returns exactly five occurrences of
  "70 minutes", no more and no fewer; recomputation reproduced — all six window pairs re-differenced
  independently to 37.2295, 37.2433, 37.2405, 37.2371, 37.2343 and 37.2309 minutes, 70/37.2295 =
  1.8802×, `retrieved_at` 2026-08-30T06:25:49.532Z confirmed, all six `data_only_sha256` equal their
  recheck digests at 169 → 169 rows, and the live git objects confirm `revision_recheck.json` has
  exactly one commit, `d37cf6d` at 07:08:02Z, so `progress.md:819`'s "~07:15Z" does postdate the
  commit that introduces the file). No correction required. The checker recorded, and this applier
  agrees, that under a strict reading of the severity definitions the defect is arguably **S2** (the
  contradicting machine stamps sit inside the same tracked JSON as the claim) rather than S3; **S3
  is retained** because it understates rather than overstates, which is the conservative direction
  for a referee.

### AUDIT-C-VRPExperiment-3
- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** the TASK 3 venue table — the measurement that fires the VENUE_BLOCKED
  closure — and its stated measurement window, read against the pre-registration guarantee
- **Direction:** neutral (hygiene) — the artifact evidence resolves the ordering question **in the
  repository's favour**; what fails is the stated window itself
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "**Measured 2026-08-30, 04:32Z–05:35Z.** Every classification
  below is evidenced by published text recorded with its URL and its date." —
  VRPExperiment/reports/task3/venue_table.md:3
- **Evidence:**
  - The stated start of **04:32Z is 15 min 8 s before the registration commit** `7827592` at
    **04:47:08Z** (raw commit object: `author … 1788065228 -0700`; re-read read-only
    2026-09-05T05:51Z). Taken literally it contradicts "no probe, fetch or measurement precedes it"
    (VRPExperiment/REGISTRATION.md:3-4) and "committed **before any network call**"
    (VRPExperiment/README.md:102).
  - **No TASK 3 artifact has an mtime inside the stated window.** From the live untracked tree (read
    2026-09-05T05:52Z, UNANCHORED): the earliest network artifact anywhere in the repository is
    `data/raw/robots/www.deribit.com.robots.txt` at **04:47:24Z** — 16 seconds *after* the
    registration commit — and the fourteen TASK 3 page captures run **06:13:57Z – 06:17:54Z**,
    ending ~43 minutes *after* the stated 05:35Z end.
  - The in-document per-page stamps are offset the same way, by ~50–60 minutes: "**Retrieved:**
    2026-08-30T05:13Z" (reports/task3/deribit_restricted_jurisdictions_verbatim.md:7) against a file
    mtime of 06:13:57Z; "retrieved 2026-08-30T05:15Z" (reports/task3/venue_table.md:38) against
    06:15:29Z; "Retrieved 2026-08-30T05:27Z" (reports/task3/robots_and_terms.md:20) against
    06:17:54Z. TASK 5's stamp drifts 11 minutes in the same direction (`docs/COSTS.md:33`).
  - **The machine clock was correct; only the hand-written stamps drift.** `rate_and_revision_
    baseline.json`'s `retrieved_at` 06:25:49.532Z agrees with its files' mtimes at 06:26Z, and
    `real_attempt2_result.json`'s `finished_at` 06:59:48Z agrees with `dvol_ETH_daily.json`'s mtime
    to the second.
  - **The captures verify by content, so this is a clock problem and not a fabrication problem.**
    `data/raw/task3/deribit_restricted_jurisdictions.html` is 63,433 bytes with SHA-256
    `ec5a39b737030785…` and `data/raw/task3/cme_refusal.json` is 602 bytes with SHA-256
    `eecde3fafbde4090…`, exactly as quoted in
    reports/task3/deribit_restricted_jurisdictions_verbatim.md:9 and
    reports/task3/robots_and_terms.md.
- **Recomputation:** inputs — `git log` / `git cat-file -p` on the live repository and `find
  -printf`/`stat` on every file under `data/raw/` (both read-only, 2026-09-05T05:51–05:52Z); method —
  convert commit epochs and inode mtimes to UTC and order them; result — repo init 04:22:18Z → TASK 0
  04:37:16Z → TASK 1 04:43:31Z → **registration 04:47:08Z → first network artifact 04:47:24Z** →
  TASK 3 captures 06:13:57–06:17:54Z → TASK 3 commit 06:22:23Z → TASK 4 06:26Z → TASK 5 06:31Z →
  TASK 6 06:58–06:59Z → anchor 07:08:02Z. Monotone and consistent throughout, with only
  `venue_table.md:3`'s stated window out of line.
- **What would resolve it:** correct `reports/task3/venue_table.md:3` to the window the artifacts
  support (≈ 04:47Z–06:18Z, or 06:13Z–06:18Z for the page captures alone) and correct the three
  per-page retrieval stamps. The mtimes are gitignored and therefore unanchored, so an author
  statement of the true clock offset would settle it definitively; storing the Coinbase/Kraken spot
  responses would additionally let the one untimeable fetch in the deciding section be ordered
  against the registration.
- **Confidence:** HIGH for the mismatch — three independent classes of stamp disagree with the
  artifacts. MEDIUM for the reading that it is a mis-stamp rather than a real pre-registration fetch;
  mis-stamp is strongly the more likely, since every hand-written TASK 3 stamp is offset in the same
  direction and no artifact on disk predates the registration.
- **Invalidated by later commits?:** no — `venue_table.md` has exactly one commit (`3ad6098`, re-run
  in this pass) and was never edited, including by the anchor commit that is titled "venue-table
  corrections".
- **Disclosed by the authors?:** no — no document notes any clock offset. **Stated plainly: the
  substantive pre-registration guarantee VERIFIES.** Nothing under `data/` predates the registration
  commit; the earliest capture postdates it by 16 seconds. The finding is that a stated timestamp
  contradicts the repository's own evidence in a way that, read at face value, would wrongly appear
  to break that guarantee.
- **Consolidation check:** verified. Quote EXACT at `reports/task3/venue_table.md:3` in SNAP, and it
  is the only occurrence of "04:32Z" or "05:35Z" in the whole snapshot. Re-derived the twelve commit
  times from the live objects in this pass — every one matches the draft to the second — and re-listed
  `data/raw/` by mtime: first byte 04:47:24Z, TASK 3 captures 06:13:57Z–06:17:54Z, fourteen files.
  `git log -- reports/task3/venue_table.md` returns exactly one commit. Merged from DRAFT-V-3 and
  DRAFT-P-2, which found the same defect from the same evidence; substance, class and severity
  unchanged.
- **Citation check:** verified (quote EXACT at `reports/task3/venue_table.md:3`, and the only
  occurrence of "04:32Z" or "05:35Z" in the snapshot; figures verified — every commit time
  re-derived first-hand from the live git objects and every `data/raw/` mtime re-listed, all
  matching to the second: repo init 04:22:18Z, 04:33:00Z, TASK 0 04:37:16Z, TASK 1 04:43:31Z,
  registration `7827592` 04:47:08Z, TASK 3 `3ad6098` 06:22:23Z, TASK 4 `0c873f5` 06:30:32Z, TASK 5
  `c51b4f7` 06:49:19Z, `adac707` 06:55:29Z, `ef07f19` 06:58:00Z, `ba50596` 07:02:58Z, anchor
  `d37cf6d` 07:08:02Z; first network artifact 04:47:24.306Z = 16.3 s after the registration commit;
  exactly fourteen TASK 3 captures spanning 06:13:57.084Z–06:17:54.479Z; recomputation reproduced —
  both capture digests re-hash byte for byte to 63,433 B / `ec5a39b737030785…` and 602 B /
  `eecde3fafbde4090…`, and the machine-clock controls hold to the second). No correction required.
  Two report-level notes raised by the checker are applied outside this finding: the "9.5 minutes"
  figure in §Summary and §Provenance is refined to ~9.6 min from `sealed_read.py`'s first commit and
  8.3 min from its last write, and the non-schema `Direction: neutral` is acknowledged in the
  Findings preamble.

### AUDIT-C-VRPExperiment-4
- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** Amendment 1's completeness claim about the diff between sealed-read
  attempt 1 and attempt 2
- **Direction:** neutral — the undisclosed change *weakened* the machinery evidence (the discarded
  run had a larger n and a larger t), so it cuts against a selection reading rather than for one
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "the only change
  between attempt 1 and attempt 2 is a **single string literal** in a request
  parameter — `"3600"` to `"60"` — plus the attempt-numbering that keeps the first
  latch. No estimator, no window, no estimator parameter, no tenor, no sign
  convention and no inference rule was touched." — VRPExperiment/REGISTRATION.md:579-583
- **Evidence:**
  - `git show ef07f19 --name-only` lists **four** files: `REGISTRATION.md`,
    `tools/task6_sealed_run.py`, `reports/task6/task6.latch.json` and
    **`reports/task6/fixture_result.json`**. The first three are exactly what the amendment
    describes; the fourth is not mentioned.
  - `git diff adac707 ef07f19 -- reports/task6/fixture_result.json` shows the committed fixture
    artifact was **replaced by a fresh run at a different size**: `"days_requested"` 900 → 300; per
    asset `"n"` 870 → 270; `started_at`/`finished_at` 2026-08-30T06:55:02Z → 06:57:32Z; `"attempt":
    1` added. The planted premium is unchanged at 0.08 in both.
  - The discarded run was the **stronger** one: BTC recovered mean 0.097798 with t = 9.5682,
    p = 5.45 × 10⁻²¹ at n = 870; the surviving run recovers 0.094653 with t = 4.2725,
    p = 1.34 × 10⁻⁵ at n = 270 (ETH: 0.094699 / t = 13.0943 → 0.094101 / t = 7.4162).
  - Amendment 1 does not mention it, and `README.md:124-125` and `docs/HANDOVER.md:116-119`, which
    point the reader at the fixture, quote no n and do not say the artifact was regenerated.
  - **The estimator half of the same sentence is fully verified.** `git ls-tree -r <c> src/vrp`
    hashes to `0e6c8711a291a714…` identically at `adac707`, `ef07f19` **and** the anchor, so no
    estimator, window, parameter, tenor, sign convention or inference rule was touched. Independently,
    all eleven SHA-256 digests in `task6.latch.2.json` match the snapshot files at the anchor, and
    `task6.latch.json` differs from the snapshot in **exactly one** file —
    `tools/task6_sealed_run.py` — which is precisely what Amendment 1 says changed.
- **Recomputation:** none required beyond the diffs and tree hashes above, all re-run read-only at
  consolidation (2026-09-05T05:52Z).
- **What would resolve it:** one sentence in Amendment 1 recording that the fixture was re-run at 300
  days during the correction and that the 900-day run stands in `adac707`; or restoring both
  artifacts side by side.
- **Confidence:** HIGH that the change happened and is unrecorded; MEDIUM that the amendment's
  sentence should be read as covering artifacts rather than only the code diff — read as a statement
  about the *machinery*, it is exactly true.
- **Invalidated by later commits?:** no — `fixture_result.json` is unchanged from `ef07f19` to the
  anchor, which is the repository's last commit.
- **Disclosed by the authors?:** not in words; but the diff is in git and the amendment explicitly
  invites the reader to it ("The diff is auditable in the commit that precedes attempt 2",
  `REGISTRATION.md:583-584`), which is why this is S3 and not higher.
- **Consolidation check:** verified. Quote EXACT at `REGISTRATION.md:579-583` in SNAP; the draft
  cited 578-582, and the span is corrected here — the quoted text begins at the end of line 579 and
  ends at "was touched." in the first half of line 583.
  Re-ran at consolidation: `ef07f19` touches exactly the four named files; the fixture diff shows
  900 → 300 and n 870 → 270 as stated; the `src/vrp` tree hash is byte-identical at all three
  commits; and the latch check gives 11/11 matches for `task6.latch.2.json` against the anchored
  snapshot and 10/11 for `task6.latch.json` with the single mismatch on
  `tools/task6_sealed_run.py`. Substance unchanged; quote span corrected.
- **Citation check:** corrected — an independent checker re-ran the quote, the figures and the
  diffs (quote EXACT in `REGISTRATION.md`; `git show --name-only ef07f19` lists exactly the four
  files; the fixture diff reproduces 900 → 300 days, n 870 → 270 per asset, `started_at`/
  `finished_at` 06:55:02Z → 06:57:32Z and the added `"attempt": 1`, with the planted premium
  unchanged at 0.08; the discarded run is confirmed the stronger one, BTC t 9.5682 → 4.2725 and ETH
  t 13.0943 → 7.4162; the `src/vrp` tree hash `0e6c8711a291a714…` is identical at `adac707`,
  `ef07f19`, `ba50596` and the anchor; the latch check reproduces 11/11 and 10/11 with the single
  mismatch on `tools/task6_sealed_run.py`). **One correction applied**, re-confirmed in SNAP by this
  applier at `REGISTRATION.md:572-590`: the quoted claim ends at "was touched." in the first half of
  **line 583**, not 584 — lines 583-584 carry the separate sentence "The diff is auditable in the
  commit that precedes attempt 2." The claim span is corrected from 579-584 to **579-583** in both
  the report and the JSON, and the consolidation note that said "the estimator sentence beside it
  continues to 584" is corrected with it. The disclosure bullet's citation of
  `REGISTRATION.md:583-584` for that separate sentence is correct as it stands and is unchanged.
  Substance, severity S3, label DERIVED and direction unchanged.

### AUDIT-C-VRPExperiment-5
- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** `progress.md`, the running provenance ledger, whose section headers are
  the repository's own record of when each task completed
- **Direction:** neutral (hygiene)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "## 2026-08-30T07:35Z — TASK 8 COMPLETE — artifact and close-out"
  — VRPExperiment/progress.md:814. The same defect at
  "## 2026-08-30T05:04Z — TASK 2 COMPLETE — REGISTRATION.md, before any network call" —
  VRPExperiment/progress.md:249 — and at
  "## 2026-08-30T07:12Z — TASK 7 COMPLETE — Section 0 fired" — VRPExperiment/progress.md:758.
- **Evidence:** each header was introduced by a commit whose own timestamp is earlier than the header
  claims. `git log -S"<header>" -- progress.md` gives the introducing commit; the raw commit objects
  give the UTC time. n = 10 headers:

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

  Seven of ten headers are stamped **after** the commit that contains them, which cannot be true of
  text already inside that commit; two others are stamped 18–42 minutes early. The worst case,
  TASK 8, is off by 27 minutes, and `progress.md:816` compounds it with "**ETA 45 min · actual
  ~23 min**" for a task whose commit falls 5 min 4 s after the previous one. **The consequence that
  matters: `progress.md:249` read literally says the registration was completed at 05:04Z, i.e. 17
  minutes after the first network fetch at 04:47:24Z.** The git objects say otherwise and are
  authoritative, so the pre-registration guarantee stands — but the repository's own ledger, read
  alone, would deny it.
- **Recomputation:** none beyond comparing header strings against `git cat-file -p <commit>` epoch
  values; five of the ten rows were re-derived independently at consolidation and reproduce exactly.
- **What would resolve it:** stamping each `progress.md` section from the same clock that writes the
  JSON artifacts — which is demonstrably correct — or from the commit itself.
- **Confidence:** HIGH — a header inside commit *X* cannot postdate *X*'s own commit time, and both
  quantities are read directly from the objects.
- **Invalidated by later commits?:** no — `progress.md` is append-only (re-verified: nine commits,
  zero deletions in every one), so these strings are fixed at the anchor.
- **Disclosed by the authors?:** no.
- **Consolidation check:** verified, with one supporting figure corrected. Quotes EXACT at
  `progress.md:814`, `:249` and `:758` in SNAP. Re-derived five of the ten rows first-hand
  (TASK 1 / 2 / 5 / 7 / 8) and all five match the table to the second. `git log --numstat --
  progress.md` was re-run: the file has **nine** commits with additions 49, 116, 120, 101, 130, 98,
  55, 80, 112 and **zero deletions in every one** — the provenance draft's eight-value list
  ("+68/-0, +43/-0, …") is not reproduced and is corrected here. The append-only conclusion those
  numbers supported is confirmed. Finding otherwise unchanged.
- **Citation check:** verified (quotes EXACT at `progress.md:814`, `:249` and `:758`; figures
  verified — the checker re-derived **all ten** rows independently with `git log -S` against the raw
  commit objects, not the five re-done at consolidation, and every row matches to the second:
  −57 s, +44 s, +8 min 29 s, +16 min 52 s, −42 min 23 s, −18 min 32 s, +10 min 41 s, +2 min 2 s,
  +9 min 2 s, +26 min 58 s; `progress.md:816`'s "ETA 45 min · actual ~23 min" against `d37cf6d`
  falling 5 min 4 s after `ba50596` confirmed; recomputation reproduced — `git log --numstat --
  progress.md` independently returns **nine** commits with additions 49, 116, 120, 101, 130, 98, 55,
  80, 112 and zero deletions in every one, so the consolidation was right to replace the provenance
  draft's eight-value list, and the stated consequence at `progress.md:249` — 05:04Z read alone
  places the registration 16 min 36 s after the first fetched byte at 04:47:24.306Z, while the git
  objects place the commit 16 s before it — reproduces exactly). No correction required.

### AUDIT-C-VRPExperiment-6
- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** the premium's unit label in `README.md`, `HYPOTHESES.md` and
  `progress.md`
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ — the contradiction is established by reading two lines of one document against
  each other. (The corroborating explanation of *which* unit is stored comes from code and data, and
  is reported as such below, but the finding itself needs neither.)
- **Claim challenged (verbatim):** "| BTC premium, mean | **0.086607 vol points = 198.111 bps of
  notional** | **1,955 daily observations** |" — VRPExperiment/README.md:36, read against
  "| conversion, registered before any data | **1 volatility point = 22.875 bps of notional** | — |"
  — VRPExperiment/README.md:50
- **Evidence:**
  - 0.086607 × 22.875 = **1.9811 bps**, not 198.111. The two rows of the same table are inconsistent
    by a factor of 100.
  - The stored mean is **decimal** volatility, not volatility points: `mean_vol_points` = 0.086607
    (VRPExperiment/reports/task6/real_attempt2_result.json:19), and `estimate_premium` multiplies it
    by `bps_per_volatility_point()` = **2,287.4639 bps per unit of decimal volatility**
    (VRPExperiment/src/vrp/sealed_read.py:43-51, and :286, :298). In volatility points the mean is
    **8.6607**, and 8.6607 × 22.8746 = 198.1104 bps — the printed figure.
  - **The repository states it correctly elsewhere**, in the artifact that a reader is pointed to:
    "| **mean premium** | **8.66 volatility points** | **5.20 volatility points** |" followed by
    "| **as basis points of notional** | **198.11 bps** | **119.05 bps** |" —
    VRPExperiment/docs/ARTIFACT.md:71-72.
  - The same mislabel recurs at `README.md:41`, `HYPOTHESES.md:19` and `progress.md:725` and `:729`.
    `REGISTRATION.md:165-166` carries the same looseness — "`edge_bps = 2,287.5 × (IV − RV)` with
    `(IV − RV)` in decimal volatility points" immediately followed by "**One volatility point of
    premium is 22.875 bps of notional**" — and the docstring at `sealed_read.py:46-48` repeats it.
- **Recomputation:** inputs — README.md:36 and :50; method — multiply the stated mean by the stated
  conversion; result — 1.9811 bps against a stated 198.111 bps, a factor of 100. No tolerance needed.
- **What would resolve it:** write the mean as "8.6607 volatility points (0.086607 in decimal)" in
  README.md, HYPOTHESES.md and progress.md, matching `docs/ARTIFACT.md:71`, and rename the code field
  `mean_vol_points` to `mean_decimal_vol`.
- **Confidence:** HIGH — a direct arithmetic contradiction between two lines of the same table.
- **Invalidated by later commits?:** no — both lines are in the anchor commit.
- **Disclosed by the authors?:** no. **No computed figure is affected**: every bps figure in the
  repository is computed from the decimal value through the correct 2,287.4639 factor, and every one
  of them reproduces exactly. This is a labelling defect only, which is why it is S4.
- **Consolidation check:** verified. Quotes EXACT at `README.md:36` and `README.md:50` in SNAP.
  Recomputed at consolidation: 0.086607 × 22.875 = 1.9811; 0.086607 × 2287.4639 = 198.1104;
  8.6607 × 22.8746 = 198.1104. The four repetitions re-located by grep at `README.md:41`,
  `HYPOTHESES.md:19`, `progress.md:725` and `:729`, and the correct statement re-located at
  `docs/ARTIFACT.md:71-72`. Label kept **READ** rather than upgraded to DERIVED: the contradiction
  stands on the document alone, and READ is the honest floor. Substance unchanged.
- **Citation check:** verified (quotes EXACT at `README.md:36` and `README.md:50`; figures verified
  — 0.086607 × 22.875 = 1.98114 against the printed 198.111, a factor of 100; 0.086607 ×
  2287.4639406411516 = 198.1104; 8.6607 × 22.8746 = 198.1104; the stored field is confirmed decimal
  at `real_attempt2_result.json:19` and the conversion factor was recomputed independently as
  2287.4639406411516 from √(2/π) · √(30/365) · 10⁴ at `sealed_read.py:43-51`; all four repetitions
  re-located at `README.md:41`, `HYPOTHESES.md:19`, `progress.md:725` and `:729`, and the correct
  statement at `docs/ARTIFACT.md:71-72`; recomputation reproduced — an independent reimplementation
  of the estimator chain reproduces **every** stored bps figure for both assets to full stored
  precision, so the "no computed figure is affected" claim holds and the defect really is labelling
  only). No correction required. The checker judged DERIVED equally defensible; **READ is retained**
  as the honest floor, since the contradiction stands on `README.md:36` against `README.md:50`
  alone.

---

## Sound

What follows verified cleanly and is reported as such. A verified claim is as important a result as a
contradicted one.

**The estimator chain reproduces end to end.** An independently written implementation of the
registered estimators — numpy plus scipy's Student-t, not the repository's own incomplete-beta —
run over the four raw series reproduces **every figure in `reports/task6/real_attempt2_result.json`
to its full stored precision** for both assets: the means to 6 dp, the HAC standard errors to 6 dp,
the t statistics to 4 dp, the one-sided p-values to **eleven significant figures**, the CI lower
bounds, the positive shares, all eight quarterly rows, both non-overlapping rows, and all six
rebalance distributions including min, median, mean, p90, max and the median maximum drift. The
repository's own Student-t implementation agrees with `scipy.stats.t.sf` to eleven significant
figures on every reported p.

**The code that ran is the code in the anchor.** `reports/task6/task6.latch.2.json` records the
SHA-256 of all eleven participating modules; **all eleven match the snapshot files at `d37cf6d` byte
for byte** (re-verified 11/11 in this pass). `task6.latch.json` differs from the snapshot in exactly
one file, `tools/task6_sealed_run.py`, which is exactly what Amendment 1 says changed.

**The deciding cost arithmetic reproduces from primitives.** 32.570638 + 11 × 8.142659 =
**122.139891 bps**; 2 × (32.570638 + 16 × 8.142659) = **325.706376 bps**; 142.7401/43.520223 =
**3.2799×**; 142.7401/2 − 21.760111 = **49.6099 bps**. All of it comes out of the stored USD rates
and notionals, and the notionals themselves reproduce from the two measured spot prices
($78,124.575 and $2,456.205 Coinbase): 245.6205, 7812.4575, 390622.875, 122810.25.

**The registered decision rule fires as written, and it is robust.** The MET failure factor of
8.5684× is not close to the 2.0 hurdle and grows under every wider bandwidth and every longer
bootstrap block tried; the MBT clearance of 3.2799× falls only to 3.05× at bandwidth 180 and still
clears; ETH's one-sided p stays below 0.05 at every bandwidth tried.

**The pre-registration ordering holds under git.** Registration commit 04:47:08Z, first fetched byte
04:47:24Z, 16 seconds apart. `REGISTRATION.md` lines 1–528 byte-identical between its only two
commits. The estimator file written 9.5 minutes before the first TASK 6 byte and extended only by
pure append thereafter. The `src/vrp` tree hash identical from `adac707` through the anchor.
`progress.md` append-only across nine commits with zero deletions. The anchor commit, titled
"venue-table corrections", does **not** touch `reports/task3/venue_table.md`: the corrections go to a
new file addressed to a different repository, with an explicit instruction that the other repository
was not and must not be edited.

**The multiplicity handling is correct, and correct in the direction that is harder to get right.**
An intersection-union test of a conjunction takes full nominal α per component; the registration says
so in advance, cites Berger (1982), and applies no correction. Applying one here would have been the
error.

**The capture-level evidence checks out.** Both quoted TASK 3 byte counts and both quoted SHA-256
digests match the files on disk (63,433 B / `ec5a39b737030785…`; 602 B / `eecde3fafbde4090…`). The
Hyperliquid capture holds 232 perpetual instruments and zero options as claimed. The rate-escalation
table (126 requests per endpoint, 2+4+8+16+32+64, zero non-200 across twelve steps) reproduces row by
row, as do the DVOL depth bisection (22 probes per asset, deepest 1,992 days) and the Deribit
half-spread distributions (medians 6.25/5.00/5.00/7.50, round trips 22.50 and 25.00 bps, 96
observations, zero unquoted windows).

**Limitations are disclosed where they exist.** The ETH premium's instability across quarters, the
negative Q3, the absence of any tail measurement, the absence of a simulated sleeve, and the fact
that every cost figure is a strict lower bound because three of five legs are `Absent(not_served)` —
all are stated by the authors in `HYPOTHESES.md:23-24` and `docs/ARTIFACT.md`. None of those is
raised here as a discovery.

**What I would have expected to find if the audit thesis held, and did not find.** No estimator or
parameter was changed after a result was seen — the `src/vrp` tree is fixed from before the data. No
outcome-dependent bandwidth or window: bandwidth 30, tenor 30, α 0.05 and the ±0.10 band are all in
the pre-data registration and in the first version of the estimator file. No selective reporting of
the favourable robustness arm: the non-overlapping check is registered in advance *with* the clause
that a disagreement would be the finding, and it is reported whether or not it helps. No quietly
retired latch: attempt 1's latch is committed and kept, and the amendment records the abort. No
post-hoc verdict edit: the verdict-bearing files have one commit each. No carried figure smuggled
into the arithmetic: the one carried notional is explicitly retired against a measurement, and the
Deribit reference spread is labelled REFERENCE ONLY and enters no verdict.

---

## Could not be checked and why

Four items are recorded as **UNVERIFIABLE** and are not guessed at, plus four gaps in the provenance
chain that no object in the repository can close.

| item | why not | consequence |
|---|---|---|
| The two hourly row counts **47,696** (DVOL) and **47,858** (perpetual) — `HYPOTHESES.md:22`, `progress.md:720-721` | The driver writes them to stdout only (`tools/task6_sealed_run.py:137-140, 182-185`); no artifact stores them, and the spent latch forbids a re-fetch. | **UNVERIFIABLE.** A consistency check only: `ceil(1992/40) = 50` hourly chunks with inclusive endpoints over 1,992 days gives 1992 × 24 + 50 = **47,858**, exactly the stated perpetual figure, and the 7-day-later DVOL start reconciles the 162-row difference. Consistent — but consistency is not verification. Everything else in the same sentence (1,985 / 1,992 / 30 / 1,955 / the span) verifies exactly. |
| **BTCY MER 1.28 %, ETHY MER 1.29 %** — `README.md:79`, `venue_table.md:28` | No machine-readable artifact holds them and the two fund pages were never captured under `data/raw/`. | **UNVERIFIABLE.** Decides nothing: the ETF route is excluded on the registered product-type criterion 3.1(2), not on cost. |
| **"mypy strict clean, ruff clean"** — `README.md:122` | Establishing a pass/fail requires executing the repository's own tooling, which the read-only rule forbids in place; `reports/env_report.json` records versions, not exit status. | **UNVERIFIABLE.** The counts beside it verify statically — **50 tests** (28 + 22 `def test_`) and **17 source files** — and `ba50596..d37cf6d` touches no `.py`, so any clean run at `ba50596` applies to the anchored code. |
| Carried **ORBExperiment / MLCryptoEngine** figures — `venue_table.md:97`, `docs/VENUE_TABLE_UPDATE.md:73-74` (0.076572 / 0.333662 USD per share, n = 550, 11.27×) | The cited sources are in other repositories; nothing under `VRPExperiment/` stores them. | **UNVERIFIABLE inside this repository.** They enter no verdict arithmetic — they appear as narrative precedent for measuring rather than carrying cost. The two carried *notional* figures in the same table are re-derived internally and both drift percentages verify. |
| The **live spot measurement** that fixes the notionals — Coinbase / Kraken, `venue_table.md:9-16` | It wrote no file: `data/raw/task3/` contains no Coinbase or Kraken response. | The one gap in an otherwise complete precedence chain: this fetch **cannot be ordered against the registration from evidence**. Every fetch that *did* leave a file postdates the registration commit. |
| The **400-day timestamp-misalignment probe** that justifies fixing the observation instant at 08:00 UTC — `docs/ACCESS.md:282-289` | No artifact stores it and no committed tool produces it; the five tools in `tools/` write only `deribit_probe.json`, `rate_and_revision_baseline.json`, `reference_spreads_deribit.json`, `env_report.json` and the task6 results. The latch forbids re-fetching. | The *ordering* of the choice is SUPPORTED (§6 of ACCESS.md is in a commit 6.5 s before the latch, and `REGISTRATION.md:141-142` pre-authorised the deferral); the claim that it was made from timestamps alone, which is what makes it outcome-blind, is **unverifiable**. Corroborated indirectly and strongly by `src/vrp/tzguard.py:10` ("Deribit settles at 08:00 UTC") in `8bcc5bf` — before the registration and before any network call — and by the measured expiry `2026-09-25T08:00:00Z`. |
| The **fixture run** — `reports/task6/fixture_result.json` | The synthetic source seeds from the run date (`tools/task6_sealed_run.py:193-198`), so today's stream differs, and re-running the driver is outside the read-only rule. | The stored figures are internally consistent and the bps conversion checks out. The +18.3 % overshoot of the planted 0.08 is 0.66 fixture standard errors and is partly the known downward (Jensen) bias of a 30-observation sample standard deviation on the realized leg. No document states a recovery tolerance, so nothing is contradicted. |
| Whether the **raw series were altered after the anchor**, and every `data/` mtime | `data/` is gitignored; the files carry mtimes, not commit hashes, and mtimes can be rewritten. | Formally **unanchored**. Practically authenticated: an independent recomputation reproduces roughly forty stored figures across two assets to full precision, which altered inputs could not do. This would be settled outright by hashing the raw captures into a committed manifest at capture time — the repository does exactly that for its *code*, via the latch, but not for its data. |

Also recorded: three stored artifacts have **no committed generator** — `reports/task4/
revision_recheck.json` (which carries the contested `gap` string of finding **-2**),
`reports/task5/commission_bps.json` (which carries the deciding 122.140 / 162.853 bps figures) and
`reports/task5/ibkr_ca_commissions.json`. Their inputs are on disk
(`data/raw/task5/commissions-futures.html`, 489,783 B, matching the byte count at
`docs/COSTS.md:33`), and the commission figures were in fact recomputed from those stored rates and
verified; what cannot be re-derived is the automated step from raw capture to stored figure.

Finally, `REGISTRATION.md:559-563`'s claim that "No premium value was observed, printed, or logged,
by the tool or by the operator" during the aborted attempt 1 is a claim about a human, not an object.
Its checkable parts all verify: no result file was ever committed (`git log --all --name-only |
grep real_result` returns nothing), `data/raw/task6/` holds exactly four files all timestamped after
latch 2 was written, and `src/vrp` is unchanged across the abort.

---

## Live-repo access log

Merged from the verification pass, the provenance pass, this consolidation and the
citation-check applier pass. Every access to
`/home/kiros-li/Documents/GitHub/VRPExperiment/` in all three was **read-only**:
`git status --porcelain`, `git rev-parse`, `git log`, `git show`, `git diff`, `git cat-file -p`,
`git ls-tree`, `git grep <commit>`, plus `ls`, `stat`, `find -printf`, `sha256sum`, `wc -l` and
`head` on the gitignored `data/` tree, and `cp` of four ~45 KB JSON files out of the repository into
the work directories. **No file in the repository was opened for writing, no repository script was
executed, and no commit, checkout, stash, reset, branch or clean was performed.** No `.env`,
keystore, session, credential or token file was opened. `data/raw/task4/alt/tardis_api`
(210,602,148 B) was never opened. Scratch work went to
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-vrp-verify/`,
`…/agentC-vrp-prov/` and `…/agentC-vrp-consol/`; nothing was written under the audited repository.

Unanchored reads (untracked / gitignored working-tree data), with UTC read times:

* `data/raw/task6/{dvol,underlying}_{BTC,ETH}_daily.json` — copied and read **2026-09-05T03:57Z**
* `data/raw/task4/alt/cdd_DeriBit_volatility_OHLC_{BTC,ETH}.csv` — line and byte counts, **04:03Z**
* `data/raw/` full mtime listing — **04:05Z** (verification), **04:05:58Z** (provenance),
  **05:52:03Z** (consolidation)
* `data/raw/task3/*.html`, `cme_refusal.json`, `hl_meta.json`, `data/raw/task5/commissions-futures.html`
  — sizes and SHA-256 only, plus the 602-byte CME refusal body in full, **04:05Z**
* `data/raw/task6/` mtimes and `src/vrp/sealed_read.py` mtime (`stat`/`find -printf`, `TZ=UTC`) —
  **2026-09-05T18:14Z** (applier pass, to re-derive the 9.6 min / 8.3 min figures in §Summary and
  §Provenance)

These paths are not in git and may have changed since the 2026-08-30 anchor.

**`git -C /home/kiros-li/Documents/GitHub/VRPExperiment status --porcelain`, BEFORE first access —
2026-09-05T03:56:59Z (provenance pass) and 2026-09-05T03:57:29Z (verification pass):**

```
```

(empty in both — exit 0, working tree clean; `HEAD` = `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`)

**BEFORE first access in this consolidation — 2026-09-05T05:50:22Z:**

```
```

(empty — exit 0, working tree clean; `HEAD` = `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`)

**BEFORE first access in the citation-check applier pass — 2026-09-05T18:13:55Z:**

```
```

(empty — exit 0, working tree clean; `HEAD` = `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`)

**AFTER last access — 2026-09-05T04:08:51Z (verification), 2026-09-05T04:10:21Z (provenance),
2026-09-05T05:53:21Z (consolidation), 2026-09-05T18:18:12Z (citation-check applier):**

```
```

(empty in all four — exit 0, working tree clean; `HEAD` =
`d37cf6d190dfdaef8e613daf099a507fe1a77dcf` at every check)

**No modification was made to the audited repository and none is reported.**
