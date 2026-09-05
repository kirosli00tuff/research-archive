# ETFExperiment — Agent C findings (referee and verifier)

Repository: `ETFExperiment`
Anchored SHA: `4d110027674e7b4cd2861cf4e0e74f975111daf1` (master, 2026-08-28 local = 2026-08-29T02:43:48Z)
— also the live `HEAD`, so the anchor is this repository's last commit and nothing below can be
overtaken by a later commit here.
Agent: **C** (referee; no thesis). Consolidated 2026-09-05.

Inputs merged: `findings/agentC/verification/ETFExperiment.inventory.md` and `.inventory.json`;
`findings/agentC/verification/ETFExperiment.verification.md` and `.claims.json`;
`findings/agentC/provenance/ETFExperiment.md` and `.json`.
Snapshot re-read for this pass: `SNAP/ETFExperiment/` — **every quote below was re-located in the
snapshot at the line cited**, and every load-bearing figure was recomputed first-hand during
consolidation from a fresh copy of the anchored `src/etf` (sha256 of `power.py`
`0fed794c…46bd268`, of `config.py` `78573ddc…f85c0814`). The live repository was re-read read-only
on 2026-09-05T18:05–18:11Z for the two untracked primitives that two findings turn on and for the
Amendment-2 commit objects; see §Live-repo access log. Each finding carries a **Consolidation
check** bullet recording what that re-check found. **Eleven draft findings entered consolidation,
three merges collapsed them to eight, none was dropped.**

**Anchoring caveat that governs part of the record.** `.gitignore` line 2 excludes `data/` in full,
so no raw primitive is in the snapshot. Every figure derived from `data/access/*`,
`data/ledgers/requests.jsonl`, `data/outcomes/*` and `data/snapshots/*` is **UNANCHORED**: read
2026-09-05, it may have changed since the 2026-08-28 anchor. Two of those files demonstrably did
move after the documents were written — the request ledger from 220 to 238 charges and the snapshot
ledger from 2 to 20 captures, both between 2026-08-28T20:40Z and 2026-08-29T02:40Z — and one finding
(**-6**) turns on exactly that movement. Everything tracked *is* anchored: all twelve E1 power cells,
the E2 grid, the census, the archive-density chain and both minimum-N bisections reproduce
bit-for-bit from the anchored source at the anchored seed.

---

## Summary

The tracked half of this repository is unusually reproducible and it holds. Every simulated power
figure, both minimum-N bisections, the whole census partition, the archive-density chain from raw
Wayback timemaps to eleven served values, the retro-revision table and the pre-period derived
quantities reproduce exactly, and the pre-registration ordering is real to the second: five
registration commits land between 08:05:56Z and 08:11:50Z, the first network charge at 08:12:19Z,
and no registered numeric parameter ever moved. What does not hold is a cluster of **labels**: an
accrual rate called "measured" that was never measured and that the repository's own census
contradicts; four statistics presented as a measured *difference* between two fund universes that
are in fact the mean, median, min and max of one universe's *level*; a simulation budget stated for
figures produced at a different one; and a blindness claim contradicted by an artifact timestamped
36 seconds before its own commit. Eight findings survive consolidation; **none of them moves the
`untestable-at-achievable-power` closure**, which rests on an archive-capture density of 11/333
against a 0.60 bar that no window this data admits can rescue. Six items could not be checked at all
— the pre-period raw payloads, the mutation harness/source attribution, the gate outputs and every
carried external statistic — and are recorded as unverifiable rather than guessed at.

---

## Verification scoreboard

### Claims

| Status | Count |
|---|---|
| VERIFIED | **30** |
| CONTRADICTED | **6** |
| UNVERIFIABLE | **2** |
| **Total claim rows audited** | **38** |

Counted separately below and not in that table: **43 derived quantities** (40 VERIFIED, 3
CONTRADICTED — all three are the same two defects as claim rows already counted), **6 intervals**
(5 VERIFIED, 1 CONTRADICTED) and **9 test-statistic-shaped quantities** (4 VERIFIED, 1 CONTRADICTED,
4 UNVERIFIABLE). Across all four kinds: **96 items, 79 VERIFIED, 11 CONTRADICTED, 6 UNVERIFIABLE.**

The six contradicted claim rows are, in order of what rests on them: the "measured forward accrual
rate of 20.8 admissible days per month" (`REGISTRATION.md:981`, finding **-1**); the five-fund vs
all-fund difference statistics (`docs/ACCESS.md:172`, finding **-2**); the E1 minimum-N budget
attribution (`REGISTRATION.md:1011`, finding **-3**); "the 220 charged requests … total lifetime"
(`REGISTRATION.md:1160`, finding **-6**); "572 of 572 post-boundary rows across three pages"
(`REGISTRATION.md:604`, finding **-7**); and the pacing equivalence (`report.md:150`, finding
**-8**). The two unverifiable claim rows are the pre-period primitives at `report.md:296` (the raw
payloads were never written to disk) and "two of the six [mutations] required fixing the harness"
at `report.md:419` (the log records outcome flags only).

**MUST-VERIFY claims (the 8 marked in the inventory), with status:**

| # | Claim | Status |
|---|---|---|
| C01 | "Its archive-capture-density leg is measured at **11 of 333 = 0.0330** against the registered 0.60 bar … **No subsequent measurement can restore it** … **GO is closed.**" (`REGISTRATION.md:863-867`) | **VERIFIED** — 11/333 = 0.033033, 0.60/0.033033 = 18.16×; the raw-timemap rebuild reproduces 37 admissible / 53 too-late / 243 no-capture exactly, and the irreversibility survives every window bound tried (37 at D 20:00Z, 66 at D 08:00Z, 78 at D 00:00Z, 114 at D−1 00:00Z, 112 unbounded — all far under the 200-day bar) |
| C02 | "At the **measured forward accrual rate of 20.8 admissible days per month**: projected achieved N … **2027-03-31: 163**; achieved N = 300 arrives around **2027-10-26**" (`REGISTRATION.md:981-986`) | **SPLIT.** The N = 163 arithmetic **VERIFIED** (11 + round(153 × 333/336) = 163, exact) and the two arrival dates **VERIFIED** conditional on the rate (2027-10-24 and 2027-07-24 recomputed). The rate's label **CONTRADICTED** — finding **-1** |
| C03 | "**The governing minimum N is therefore 300, not 237**" with E1 237 / E2 300 (`REGISTRATION.md:974-978`) | **VERIFIED on the figures** — `minimum_n(0.18, 0.80)` = **237** and the E2 grid 200 → 0.676667, 250 → 0.71, 300 → 0.80 all reproduce bit-identically. The stated **provenance** of 237 is **CONTRADICTED** — finding **-3** |
| C04 | "**BLOCKED does not fire on power** … Measured: **0.6105**. The trigger is not met." (`REGISTRATION.md:869-871`) | **VERIFIED** — `e1_power(163, 0.18)` = **0.6105**, bit-identical, re-run at consolidation; all 12 E1 cells reproduce. The N it is evaluated at is finding **-1** |
| C05 | "**0 of 11** revised / sign flips / threshold crosses; **11 of 11** intact … below the registered minimum of 30" (`REGISTRATION.md:756-769`) | **VERIFIED** — 11 rows `state=stored`, every `delta_usd == 0.0`, `meets_registered_minimum` false. `revised = delta != 0.0` is the tightest possible definition and cannot fail to fire |
| C06 | "**Census: 336 rows, 11 admissible**" with exclusions 53 / 243 / 25 / 3 + 1 (`report.md:260-269`) | **VERIFIED** — 11 + 325 = 336; `by_month` sums to 336 days and 11 admissible over 16 months; 37 = 11 served + 25 served-no-value + 1 fetch-failed; 333 printed + 3 = 336 |
| C07 | "**0.316 times per calendar day** (n = 153 … over 484 calendar days) … **48.37 percent** … in-window … unbounded would reach only **112 of 333 (33.63 percent)**" (`docs/ACCESS.md:380-385`) | **VERIFIED** — 153/484 = 0.31612; 74/153 = 0.48366; 112/333 = 0.336336, all from the untracked timemaps (UNANCHORED). Recorded, not raised: under the *trading-day* reading of the window the middle figure is 57/153 = 37.5 %, because weekend captures land in the clock band but qualify for no trading day |
| C15 | "the registered five-fund aggregate **differs from** the all-fund total by a mean of **47.42M USD** (median 27.20M, range −903.20M to +1,205.20M, n = 333)"; "**315 of 333** … agree within 2 percent" (`docs/ACCESS.md:172-181`) | **SPLIT.** The 315-of-333 cross-check **VERIFIED** exactly, worst day 2026-08-11 7.8M vs 4.886M. The difference statistics **CONTRADICTED** — finding **-2** |

**5 VERIFIED outright, 3 split (verified on the arithmetic, contradicted on a label or a
provenance), 0 wholly unverifiable.** The leg that actually closes the repository — C01's archive
density — is the one that verifies most completely, end to end from raw untracked timemaps through
the repository's own `density()`.

### Intervals

| Metric | Count |
|---|---|
| Intervals audited | **6** |
| Independence doubtful | **0** |
| Recomputed | **6** |
| Conclusion moved | **1** |

**No confidence interval on any estimate is reported anywhere in this repository**, and that is not
an omission: neither co-primary was ever run on data, so there is no estimate to put an interval
around. What exists is three binomial standard errors on *simulated* powers (I1 √(0.8·0.2/300) =
0.023094; I2 √(0.25/300) = 0.0288675; I3 √(0.25/400) = 0.025 — all three reproduce exactly), one
min/max range of archived capture offsets that the authors explicitly refuse to promote to an
interval (I4, served +04:05 … +08:00 on n = 11, dashed −03:38 … +04:29 on n = 23, reproduces), one
set of nearest-rank empirical quantiles (I6, descriptive, reproduces), and I5.

**Independence: doubtful in none.** The three binomial SEs are computed on genuinely i.i.d.
replications of a seeded simulator, which is the correct assumption; the only shared structure is
one `random.Random(20260828)` stream, which does not correlate replications. **No standard error,
interval or test anywhere in this repository is computed on a time series, a panel or any
repeated-within-day structure**, because no outcome was ever read — so the usual hazard of treating
serially dependent daily returns as i.i.d. never arises here. The one quantity with a genuinely
awkward structure (I4, capture times censored by a crawl schedule the project did not choose) is
the one the record refuses to promote, at `report.md:239-242` and `REGISTRATION.md:786-793`.

**The one moved conclusion is I5**, the "mean 47.42M / median 27.20M / range −903.20M to +1,205.20M,
n = 333" range at `REGISTRATION.md:622-623`, `docs/ACCESS.md:174-175` and `report.md:65`. Recomputed
first-hand at consolidation: those four numbers are the mean, median, min and max of the Farside
all-fund `Total` **level**, not of any difference. The actual difference is mean −7.44M, median
−3.00M, range −150.40M to +363.00M, and it exceeds the registered 100M threshold on 6 of 333 days.
The stated inference — "large against the registered 100M threshold … not interchangeable" — does
not follow from the measurement. Finding **-2**.

### Tests

| Metric | Count |
|---|---|
| Test-statistic-shaped quantities audited | **9** |
| Tail mismatch | **0** |
| Degrees-of-freedom issue | **0** |
| Multiplicity-correction mismatch | **1** |

**Tail: 0 mismatches.** Both co-primaries are registered one-sided positive and both are implemented
upper-tail: E1 rejects on `spearman(xs, ys) > critical` (`src/etf/power.py:70-104`), E2 on
`perm_edge/traded − cost ≥ observed` with the exact-valid `(exceed + 1)/(draws + 1)` Monte-Carlo
p-value (`src/etf/power.py:119-166`). Both match `REGISTRATION.md:290-293` and `:302-306`.

**Degrees of freedom: 0 issues, and none is possible.** Every in-repo test is distribution-free —
a permutation null over ranks for E1 and over signed position labels for E2 — so no dof enters
anywhere. The critical value is a Monte-Carlo quantile, `index = ceil((1 − α)·draws) − 1`.

**Both engines are correctly sized**, which was checked rather than assumed: E1's empirical size at
the registered α is 0.0265 / 0.0270 / 0.0295 at n = 163 across three seeds and 0.0220 at n = 300
(MC SE 0.0035); E2's at ρ = 0, n = 163 is 0.0225. The repository's own calibration tests
(`tests/test_power.py:59-65`, `:75-78`) were re-run verbatim and pass: permutation cut 0.11530
against the 1/√(n−1) asymptotic 0.11660, |diff| 0.00130 < 0.02; size 0.05375 inside the asserted
(0.02, 0.09).

**The one correction mismatch is the Šidák adjustment itself.** `α_adj = 1 − 0.95^(1/2) =
0.0253205655` is a **union-type** correction, attached to a decision rule that is a **conjunction**:
"Both must pass for the Stage B GO row" (`REGISTRATION.md:285-286`), "both co-primaries at or above
80 percent power" (`REGISTRATION.md:394`), `src/etf/section0.py:139`. An intersection–union test has
size bounded by the largest component level, so each component may be tested at the full 0.05.
Finding **-5** — recomputed, and the closure survives it. The contrast case is instructive and is
recorded as correct: the four-cell threshold-sensitivity **secondary** (`REGISTRATION.md:315-316`)
has no conjunction attached and is the one place Šidák is used properly.

Four test rows are UNVERIFIABLE and all four are external: the carried Newey–West t 3.12 (n = 313),
t 8.99, IV F 21.58, Granger β 0.47 / t 9.75, reversal t −2.42..−3.99, 10-day t 4.49 (T7); the
carried IV t 2.65 on 563 days (T8); the 90-day rolling 0.16 "indistinguishable from zero", reported
with no standard error on either side (T9); and the four-cell secondary, which was never run (T6).
Only t 3.12 propagates into a registered bar, via ρ ≈ 0.176 → the registered 0.09, and **that
propagation arithmetic is checked**: inverting the printed formula gives 0.17421 and t/√n gives
0.17641, which is the printed 0.176 within its own "≈".

### Provenance

| Status | Count |
|---|---|
| SUPPORTED | **20** |
| NOT_SUPPORTED | **5** |
| PARTIAL | **9** |
| UNVERIFIABLE | **0** |
| **Total provenance items audited** | **34** |

Split by kind: **22 registration claims** — 11 SUPPORTED, 7 PARTIAL, 4 NOT_SUPPORTED — and **12
parameter or budget changes after data existed** — 9 SUPPORTED, 2 PARTIAL, 1 NOT_SUPPORTED. No row
is UNVERIFIABLE: every provenance claim raised had a git object, an artifact timestamp or a ledger
row to test it against. The questions that genuinely cannot be answered are not status rows but
limits, and they are listed in §Could not be checked and why.

**The pre-registration guarantee verifies, and it is the strongest thing in this repository.** Five
commits carrying the scaffold, the five standing guards, `CLAUDE.md`, `REGISTRATION.md` Sections
0–14 and `HYPOTHESES.md` land at 08:05:56 / 08:07:59 / 08:09:26 / 08:11:17 / 08:11:50Z; the first
network charge in `data/ledgers/requests.jsonl` is stamped **08:12:19Z**, 29 seconds after the last
of them, and `reports/stage_a1/robots_and_terms.json` carries the same 08:12:19–08:12:54Z instants
independently. `git ls-tree -r 44567f6` lists 44 paths and not one data artifact. `git show
44567f6:REGISTRATION.md` is 86 lines and is **byte-identical** to lines 1–86 of the anchored file,
so the Section 0 DEGRADED expectation is pre-data to the byte. **`REGISTRATION.md` is genuinely
append-only**: all six post-data commits touching it are `+N / −0` and every hunk header is an
end-append (`@@ -594,0 +595,102 @@`, `@@ -696,0 +697,121 @@`, `@@ -817,0 +818,128 @@`,
`@@ -945,0 +946,46 @@`, `@@ -991,0 +992,103 @@`, `@@ -1094,0 +1095,67 @@`). **No registered numeric
parameter ever moved**: `git diff 815f888 4d11002 -- src/etf/config.py` is 12 insertions and 0
deletions, all three flow-source strings and their comments; every bar, floor, threshold, horizon,
alpha, deadline and cap is byte-identical to the version committed 2 m 23 s before the first
request.

The five NOT_SUPPORTED rows are P06 (Amendment 2's "No power number existed", finding **-4**), P13
(the 220 lifetime figure, finding **-6**), P17 (the pre-registration rule against registering an
unmeasured accrual figure, finding **-1**), P21 (the "1,200 draws, 300 sims/cell" label on E1's 237,
finding **-3**) and C08 (the E1 minimum-N budget change carrying no amendment, also finding **-3**).
The nine PARTIAL rows split into three that became findings (P08 → **-7**, P20/P22 → **-3**) and six
that did not and are recorded in §Sound as small, disclosed or immaterial: the "one-ULP steps" that
are actually `1e-12` (P03), the "143 charged requests" that was 145 at the commit instant (P05), the
`.env.example` "empty on purpose" that is a 200-byte comment block whose first line reads
"# Deliberately empty" (P10), ADR-003's undated 12 h 25 m gap between a §8 registration and the
figure quoted in it (P19), the two one-shot `meta.*` endpoints added at a conservative pace with no
amendment line (C04), and the E2 budget reduction that is disclosed one amendment late (C07).

### Merge and de-duplication record

| Draft | Origin | Disposition |
|---|---|---|
| DRAFT-V-1 | verification §5 | **merged** with DRAFT-P-4 → **AUDIT-C-ETFExperiment-1** |
| DRAFT-P-4 | provenance §3 | **merged** with DRAFT-V-1 → **-1** |
| DRAFT-V-2 | verification §5 | → **-2**, unchanged in substance |
| DRAFT-P-1 | provenance §3 | **merged** with DRAFT-P-2 and DRAFT-V-3's budget half → **-3** |
| DRAFT-P-2 | provenance §3 | **merged** into **-3** |
| DRAFT-V-3 (budget half, claim `ETF-C03b`) | verification §5 | **merged** into **-3** |
| DRAFT-P-3 | provenance §3 | → **-4**, unchanged |
| DRAFT-V-3 (Šidák half) | verification §5 | → **-5**, budget evidence moved out to **-3** |
| DRAFT-V-4 | verification §5 | **merged** with DRAFT-P-5 → **-6** |
| DRAFT-P-5 | provenance §3 | **merged** with DRAFT-V-4 → **-6** |
| DRAFT-V-5 | verification §5 | → **-7**, provenance P08 folded in as corroboration |
| DRAFT-V-6 | verification §5 | → **-8**, unchanged |

**Eleven drafts in, three merges, eight findings out. Nothing was dropped.** All eleven carry a
verbatim quote that re-locates in `SNAP/ETFExperiment/` at the line cited, and all eleven carry a
figure that recomputed in this pass. The three merges were genuine duplicates or near-duplicates:
the verification pass and the provenance pass found the 20.8 accrual defect and the 220-request
staleness independently from different evidence, and the three budget mis-attributions are one
defect (a stated simulation budget that did not produce the figures it is attached to) stated in
three places.

Three reconciliations were required.

* **Severity of -6** (the 220 lifetime figure). The verification draft graded it **S4**, the
  provenance draft **S3**. Resolved to **S4**. The severity ladder reserves S3 for a stale
  *blocker* or *external* figure; the request count is neither. No measurement, bar, floor or
  verdict path reads it, which the verification draft states and I confirmed by grep. It is a
  closing-statement hygiene defect, correctly recorded and correctly small.
* **Class of -1** (the 20.8 accrual rate). The verification draft filed it UNSUPPORTED_POSITIVE, the
  provenance draft PROVENANCE. Resolved to **UNSUPPORTED_POSITIVE**: the defect is not that the
  figure's origin is undocumented but that a quantity presented as measured has no measurement
  behind it and is contradicted by the repository's own census, and something material — the Section
  0 power row — rests on it.
* **Direction of -1.** The verification draft said B (claimed too much), the provenance draft A
  (closed too early). Resolved to **B**. The sentence claims a measurement that was not made; the
  closure that follows is, if anything, more secure at the measured rate than at the stated one, so
  "closed too early" is the wrong axis.

One draft figure was corrected. DRAFT-V-1 put E1's power at the repository's measured admissible
rate (N ≈ 16) at "≈ 0.08"; re-run at consolidation, `e1_power(16, 0.18)` = **0.0955**. The
substantive point — that it is far under the 0.50 BLOCKED floor — is unchanged.

---

## Findings

Eight. Ordered by descending severity. **None of them changes the registered verdict**, and each
says so explicitly.

### AUDIT-C-ETFExperiment-1
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** H1's closure at `untestable-at-achievable-power` — the projected
  achieved N of 163, the Section 0 finding that BLOCKED does not fire on power, and the two arrival
  dates the deadline finding is stated with
- **Direction:** B (claimed too much)
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2 — the label "measured" contradicts the repository's own census
- **Label:** DERIVED (stored artifacts, the repository's own code, and a bit-exact rerun of its
  power function)
- **Claim challenged (verbatim):** "**The deadline finding, restated at the governing figure.** At
  the measured / forward accrual rate of 20.8 admissible days per month:" —
  ETFExperiment/REGISTRATION.md:981-982. And, under a table column literally headed `measured`:
  "| projected achieved N at the registered deadline | **163** | forward accrual 20.8 admissible
  days/month |" — ETFExperiment/REGISTRATION.md:1010
- **Evidence:**
  - **The figure exists in no artifact and in no line of code.** `grep -rn "20\.8"` over
    `reports/`, `src/` and `scripts/` at the anchor returns nothing. Its only occurrences are 14
    prose citations across six documents: ETFExperiment/REGISTRATION.md:982, :1010, :1129;
    ETFExperiment/report.md:360, :447, :506; ETFExperiment/HYPOTHESES.md:70, :82, :84;
    ETFExperiment/progress.md:493, :533, :581; ETFExperiment/DECISIONS.md:555, :596.
  - **What the code actually computes is a different rate.** ETFExperiment/scripts/power_gate.py:71
    sets `printed_rate = 333 / 336` and applies it to a calendar weekday count
    (`trading_days_between`, ETFExperiment/scripts/power_gate.py:29-43). 21 weekdays/month ×
    333/336 = **20.8125**. That is the rate at which the **source prints a value**, applied as
    though every future printed day were **admissible**.
  - **The repository measured the admissible rate, and it is not 20.8.**
    ETFExperiment/reports/stage_a2/census.json `by_month` records **11 admissible days across 16
    months = 0.6875 per month** (336 days summed, 11 admissible summed — both re-verified).
  - **Forward accrual was measured and it was zero.** `census.json` `admissible_forward_capture` =
    **0**; `power.json` `scenarios.achieved_forward_only` = **0**; ETFExperiment/report.md:264
    prints "**admissible** (all retro-archive; forward-capture 0) | **11**". The untracked snapshot
    ledger `data/snapshots/flow_snapshots.jsonl` holds 20 captures over one trade date, every one
    with `signal_usd: null`.
  - **The registration forbids exactly this, in a pre-data commit.** "**Therefore: no accrual,
    coverage, lag, retention, revision, or capture-density figure in this repository is registered
    before it is measured.** Every such figure is named as an A.1 or A.2 **measurement target**,
    never as an input" — ETFExperiment/REGISTRATION.md:571-573, committed at `38b9397`
    2026-08-28T08:11:17Z, 62 seconds before the first network request — with "admissible days per
    month and the trailing rate" named as an A.2 Task 1 target at ETFExperiment/REGISTRATION.md:584.
  - **20.8 does not even reproduce the 163 it is printed beside.** 7.064 months × 20.8 + 11 =
    **157.9**, against the stated 163, because 163 came from the weekday method and 20.8 from a
    calendar-month convention. The two methods disagree by 5 days at the deadline and by 12 days at
    Amendment 6's 2027-10-31 horizon (20.8 × 14.094 = 293.2 forward, against the weekday method's
    303).
  - **What turns on it:** "**BLOCKED does not fire on power.** Its power trigger is E1 under 0.50 at
    the published-magnitude assumption at the achievable count by 2027-03-31. Measured: **0.6105**.
    The trigger is not met." — ETFExperiment/REGISTRATION.md:869-871, enforced at
    ETFExperiment/src/etf/section0.py:125-136.
- **Recomputation:** Inputs — `reports/stage_a2/power.json` (weekdays_to_deadline 153,
  printed_day_rate 0.9910714285714286, scenarios), `reports/stage_a2/census.json` (admissible 11,
  admissible_forward_capture 0, by_month), `src/etf/power.py` and `src/etf/config.py` copied from
  `SNAP` into `work/agentC-etf-consol/`. Method — re-run the anchored `e1_power` over a grid of N at
  ρ = 0.18 to locate the 0.50 BLOCKED floor, then invert the repository's own projection identity
  N = 11 + rate × (2026-08-28 → 2027-03-31 = 7.064 months) to get the accrual rate at which the
  trigger fires. Result — N = 163 reproduces exactly (11 + round(153 × 333/336)); E1 power
  **0.4475** at n = 100, **0.4755** at 110, **0.5110** at 115, 0.5025 at 120, 0.5275 at 125, 0.5870
  at 140, **0.6105** at 163, so the floor is crossed at **n ≈ 113–120**, i.e. at an accrual rate of
  **≈ 14.4–15.4 admissible days per month**. At the repository's only measured admissible rate
  (0.6875/month) the achievable N is **16** and `e1_power(16, 0.18)` = **0.0955**, far under the
  floor. Tolerance: bit-exact on the reproduced powers; the crossing is located to ±5 in n by the
  0.0112 Monte-Carlo SE at 2,000 simulations.
- **What would resolve it:** either (a) an artifact measuring a forward admissible-day rate — which
  needs the forward collector to run past at least one completed print, and it was disarmed
  2026-08-29T02:43:48Z before that happened; or (b) relabelling 20.8 as a **projection under the
  assumption that the repository's own capture would make every printed day admissible**, stating
  that assumption, and reporting the Section 0 power row's sensitivity to it. The underlying
  question is genuinely open: the served-capture offsets the repository itself measured run up to
  **+07:59:42**, eighteen seconds inside the 08:00Z anchor.
- **Confidence:** HIGH that 20.8 is a printed-day rate and not a measured admissible rate — it is
  readable directly from `scripts/power_gate.py:69-71` and from the census's own `by_month` block,
  and the power sensitivity is a bit-exact rerun of the repository's own function. MEDIUM only on
  the counterfactual rate a working snapshotter would have achieved, which no data settles.
- **Invalidated by later commits?:** no — `4d11002` is the last commit on master, the collectors are
  disarmed, and the census and power artifacts are tracked and anchored.
- **Disclosed by the authors?:** **partly, and only in code and in a table cell.** The substitution
  is stated in a source comment — "The forward cohort accrues at the measured **printed-day** rate:
  the census measured 333 printed days in 336 weekday rows over the window",
  ETFExperiment/scripts/power_gate.py:69-71 — and the forward-capture count of 0 is printed at
  ETFExperiment/report.md:264 and README.md:37. **No document anywhere qualifies the word
  "measured"**, and it is attached to the figure in all 14 prose citations and in a table column
  headed `measured`. The disclosure covers the mechanism; it does not cover the label, which is what
  this finding challenges. The finding therefore stays DERIVED and S2 rather than being capped as a
  disclosed limitation.
- **Consolidation check:** verified. Quotes EXACT at `REGISTRATION.md:981-982` and `:1010` in SNAP.
  Re-run first-hand at consolidation: `e1_power(163, 0.18)` = 0.6105; the n-scan reproduces
  0.4475 / 0.4755 / 0.5110 / 0.5025 / 0.5275 / 0.5870; `census.json` `by_month` sums to 336 days and
  11 admissible over 16 months; `admissible_forward_capture` = 0; `grep -rn "20\.8"` over
  `reports/ src/ scripts/` returns nothing while returning 14 prose lines. One draft figure
  corrected: E1 power at N = 16 is **0.0955**, not the draft's "≈ 0.08". Kept otherwise unchanged.

### AUDIT-C-ETFExperiment-2
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** A.1 Task 1 source selection — the SoSoValue cross-check and the
  justification for keeping the registered five-fund universe rather than the all-fund total
- **Direction:** A (closed too early — the question of using the second publisher was closed on a
  statistic that measures something else)
- **Class:** ARITHMETIC
- **Severity:** S2 — a stated measurement is of a different quantity than its sentence says
- **Label:** DERIVED (recomputed from the two stored source captures)
- **Claim challenged (verbatim):** "Measured over the 333 overlapping out-of-sample days, **the
  registered five-fund aggregate differs from the all-fund total by a mean of 47.42M USD (median
  27.20M, range −903.20M to +1,205.20M, n = 333)** — large against the registered 100M USD
  threshold. The two are **not interchangeable**, and Section 2 names five funds because the source
  study does." — ETFExperiment/docs/ACCESS.md:172-177. Repeated
  at ETFExperiment/REGISTRATION.md:620-623 and ETFExperiment/report.md:65.
- **Evidence:**
  - **The four printed numbers are the mean, median, minimum and maximum of the Farside all-fund
    `Total` column itself**, over the same 333 days: recomputed **47.42M / 27.20M / −903.20M /
    +1,205.20M**, matching every printed digit.
  - **The actual difference between the two universes** over those days is mean **−7.44M**, median
    **−3.00M**, range **−150.40M to +363.00M**; |difference| mean 17.61M, median 9.70M.
  - **|five-fund − all-fund| ≥ 100M on 6 of 333 days (1.8 %)**, which is the opposite of "large
    against the registered 100M USD threshold".
  - For completeness, the five-fund series' own level statistics are 39.98M / 27.40M / −860.90M /
    +1,142.40M — exactly `census.json`'s stored `signal_distribution_live_descriptive`.
  - Registered universe: ETFExperiment/src/etf/config.py:141,
    `flow_universe_tickers=("IBIT","FBTC","GBTC","ARKB","BITB")`.
  - **The companion claim in the same paragraph does verify**: "**315 of 333** out-of-sample days
    agree within 2 percent" (ETFExperiment/docs/ACCESS.md:179-181) reproduces exactly, and the named
    worst day 2026-08-11 reproduces as 7.8M against 4.886M.
  - No script under `scripts/` computes this cross-check and no module names sosovalue, so the
    figure has no committed code path and no stored artifact.
- **Recomputation:** Inputs — `data/access/farside_all_parsed.json` (676 rows, 14-column header) and
  `data/access/sosovalue-btc.html` (`__NEXT_DATA__` → `props.pageProps.historyData.list[*]`), both
  read read-only **2026-09-05T18:09Z** (untracked, **UNANCHORED**). Method — parse cells by the
  repository's own conventions (`src/etf/flow.py:parse_cell`: dash → absent, parentheses →
  negative, millions → USD), filter to `d >= CONFIG.oos_start_date`, form the five-fund aggregate
  with `aggregate`'s strict rule (absent if any registered fund cell is a dash), and compute the
  level statistics of each series and the per-day difference. Result — 676 rows, 336 on or after
  2025-05-01, **333** with all five funds and a `Total` printed; Farside `Total` level mean 47.42M,
  median 27.20M, min −903.20M, max 1205.20M; difference mean −7.44M, median −3.00M, min −150.40M,
  max 363.00M; |difference| ≥ 100M on **6 of 333**. Tolerance exact to the printed 0.01M.
- **What would resolve it:** replacing the sentence's four numbers with the difference statistics
  actually measured (mean −7.44M, median −3.00M, range −150.40M..+363.00M, |diff| ≥ 100M on 6 of 333
  days) and restating the inference that follows from them. If the intent was to report the *scale
  of the flow series* rather than the *difference between universes*, the sentence needs a different
  verb — and the "not interchangeable" conclusion then has no measured support anywhere in the
  record.
- **Confidence:** HIGH on the recomputation — the four stated numbers reproduce exactly as the level
  statistics of a different series, which no rounding difference could produce, and the check was
  run twice from independent scripts. MEDIUM on the consequence: a near-interchangeable second
  publisher matters to reopen threshold (b) at ETFExperiment/HYPOTHESES.md:84, because SoSoValue's
  archive-capture density over the test window was never measured and this figure is what closed the
  question of using it.
- **Invalidated by later commits?:** no. `4d11002` is the last commit and both data files carry
  mtimes of 2026-08-28, before the anchor's documents were finalised. The figure could move if
  either publisher revised its history after 2026-08-28; that would change the difference statistics
  but could not convert a difference into a level.
- **Disclosed by the authors?:** **no.** The figure is presented as measured, with its n, in three
  documents, and nothing anywhere flags it as a level rather than a difference. It does **not**
  reopen the closure: SoSoValue serves no per-row publication timestamp either
  (ETFExperiment/docs/ACCESS.md:169), so reopen threshold (a) is untouched.
- **Consolidation check:** verified and re-derived from scratch. Quote EXACT at
  `docs/ACCESS.md:172-177` in SNAP. My own independent parse of the untracked Farside capture
  (`work/agentC-etf-consol/recheck3.py`, read 2026-09-05T18:09Z) returns 676 rows → 336 → 333, level
  mean 47.42M / median 27.20M / min −903.20M / max 1205.20M, difference mean −7.44M / median −3.00M
  / min −150.40M / max +363.00M, |diff| ≥ 100M on 6 of 333 — every figure in the draft reproduced.
  Kept unchanged.

### AUDIT-C-ETFExperiment-3
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** the E1 minimum-N figures (237 at ρ 0.18, 845 at ρ 0.09, 3,776 at
  ρ 0.045) in Amendment 3 §1 and Amendment 5's closing table, and
  `reports/stage_a2/power.json:minimum_n_for_e1`
- **Direction:** A — the closure's figures were not produced by the method the register states for
  them, so their provenance is looser than labelled
- **Class:** PROVENANCE
- **Severity:** S2 — a stated budget contradicts the code that produced the figures, and one stated
  figure does not reproduce at the stated budget
- **Label:** DERIVED (git objects plus exact reruns of the repository's own seeded code)
- **Claim challenged (verbatim):** "Simulation budget stated: E1 at 20,000 permutation draws / and
  2,000 simulations; E2 at 1,500 draws and 400 simulations, whose simulation / error near a power of
  one half is about 0.025 — both registered floors sit far / from these values." —
  ETFExperiment/REGISTRATION.md:856-859. And: "| E1 minimum N at the published 0.18 | **237** |
  1,200 draws, 300 sims/cell |" — ETFExperiment/REGISTRATION.md:1011. And: "Simulation budgets are
  stated rather than implied: E1 at 20,000 permutation draws and 2,000 simulations" —
  ETFExperiment/report.md:329-330.
- **Evidence:**
  - **Three statements, three different budgets, none of them the one that ran.** The code that
    produced 237 / 845 / 3,776 is `minimum_n(rho_true, target, *, lo=20, hi=4000,
    alpha=CONFIG.alpha_adj, draws=4_000, simulations=600, seed=20260828)` —
    ETFExperiment/src/etf/power.py:225-234 — called with **no override** at
    ETFExperiment/scripts/power_gate.py:104-106.
  - **`REGISTRATION.md:856-859` sits directly beneath two tables**, the minimum-N table at
    ETFExperiment/REGISTRATION.md:834-838 and the power table at :846-851, and its stated E1 budget
    is correct only for the second. `e1_power` does default to `CONFIG.permutation_draws` (20,000)
    and `CONFIG.power_simulations` (2,000) — ETFExperiment/src/etf/power.py:91-92 — so all twelve
    power cells reproduce bit-for-bit at the stated budget.
  - **At the stated budget one of the three stated minimums changes.** `minimum_n(0.09, 0.80)` is
    **845** at the as-run 4,000/600 and **1,016** at the stated 20,000/2,000 — a 20.2 % difference.
    `minimum_n(0.18, 0.80)` is 237 at both.
  - **`REGISTRATION.md:1011`'s "1,200 draws, 300 sims/cell" is Amendment 4's E2 grid budget** —
    ETFExperiment/scripts/e2_minimum.py:42, `e2_power(n, rho, inputs, draws=1200, simulations=300)`.
    The next row of the same table, "| E2 minimum N at the published 0.18 | **300** | 1,200 draws,
    300 sims/cell |" (:1012), is correct: the label was carried up one row onto a figure it does not
    describe.
  - **The row matters.** ETFExperiment/REGISTRATION.md:1015 and ETFExperiment/report.md:456-463 rest
    the closure's most conservative statement on "E1's 237 … the smallest minimum on the record",
    explicitly to make it robust to the E2 figure.
  - **`power.json` repeats the wrong budget for the whole file.**
    ETFExperiment/reports/stage_a2/power.json records `"permutation_draws": 20000,
    "power_simulations": 2000`, written unconditionally from CONFIG at
    ETFExperiment/scripts/power_gate.py:115-116, although the same file's E2 cells ran at 1,500/400
    and its `minimum_n_for_e1` block ran at 4,000/600.
  - **The change carries no amendment.** `minimum_n`'s defaults were introduced at `5fa460a`
    2026-08-28T20:27:29Z, after data existed (08:12:19Z), and no amendment line anywhere records a
    departure from the registered 20,000/2,000 for E1. This is the only post-data deviation from a
    registered figure in the repository with no dated amendment; the E2 equivalent (C07) does have
    one, one amendment late.
  - Recorded and not separately raised: `minimum_n` bisects a **noisy simulated** power curve
    (ETFExperiment/src/etf/power.py:242-252), so its output is a random variable rather than a
    well-defined minimum. The register acknowledges the analogous point for E2's grid at
    ETFExperiment/REGISTRATION.md:966-972 but not for E1's bisection.
- **Recomputation:** Inputs — `src/etf/power.py` and `src/etf/config.py` copied verbatim from `SNAP`
  into `work/agentC-etf-consol/` (sha256 verified) and driven by my own scripts. Method — call the
  repository's own `minimum_n` and `e1_power` at the as-run and the stated budgets, same seed
  20260828. Result — `minimum_n(0.18, 0.80)` = **237** at 4,000/600 and **237** at 20,000/2,000;
  `minimum_n(0.09, 0.80)` = **845** at 4,000/600 and **1,016** at 20,000/2,000; `e1_power(163,
  0.18)` = **0.6105** at the CONFIG defaults. Tolerance: exact equality — these are seeded
  deterministic integer-count ratios.
- **What would resolve it:** a dated amendment recording that the minimum-N bisection ran at 4,000
  draws / 600 simulations, and a correction of the `1,200 draws, 300 sims/cell` cell at
  `REGISTRATION.md:1011`; or a rerun at the registered 20,000/2,000 with the ρ = 0.09 figure
  restated as 1,016. **No stated conclusion changes either way**: 1,016 still sits inside Section 9's
  pre-data qualitative anchor of "high hundreds to low thousands" (ETFExperiment/REGISTRATION.md:382),
  and the direction of the error understates how much data E1 would need, which if anything
  strengthens the closure.
- **Confidence:** HIGH — both budgets are readable in the repository's own scripts, only one of them
  can have produced 237, and both were run to completion at consolidation with exactly reproducing
  results.
- **Invalidated by later commits?:** no — `4d11002` is the last commit and `power.py` has not
  changed since `5fa460a`.
- **Disclosed by the authors?:** **no.** The E2 departure *is* disclosed, in the same sentence
  (ETFExperiment/REGISTRATION.md:856-857). The E1 minimum-N departure is disclosed nowhere: the
  register, the report and `power.json` all state a single E1 budget covering the whole section.
- **Consolidation check:** verified. All three quotes EXACT in SNAP at `REGISTRATION.md:856-859`,
  `:1011` and `report.md:329-330`. Re-run first-hand at consolidation from fresh SNAP copies:
  `minimum_n(0.09, 0.80)` = **845** (4,000/600) and **1,016** (20,000/2,000); `minimum_n(0.18,
  0.80)` = **237**; `e2_minimum.py:42` reads `draws=1200, simulations=300` and `power_gate.py:105`
  calls `minimum_n(rho, TARGET)` with no override; `power.json` carries `"permutation_draws": 20000,
  "power_simulations": 2000` beside `minimum_n_for_e1 = {0.18: 237, 0.09: 845, 0.045: 3776}`. Three
  drafts merged into one finding; no figure changed.

### AUDIT-C-ETFExperiment-4
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** Amendment 2's statement of what data existed when it was made — a
  blindness claim, and one of the record's own guarantees of outcome-blind amendment
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S2 — a blindness claim contradicted by an artifact inside the amendment's own commit
- **Label:** DERIVED (git objects, an artifact timestamp, and exact reproduction)
- **Claim challenged (verbatim):** "No power / number existed when this amendment was written." —
  ETFExperiment/REGISTRATION.md:708-709
- **Evidence:**
  - Amendment 2 is commit `41351a9`, author and commit date 2026-08-28 13:36:13 −0700 =
    **2026-08-28T20:36:13Z**.
  - `reports/stage_a2/power.json` carries `"computed_at": "2026-08-28T20:35:37Z"` — **36 seconds
    earlier** (ETFExperiment/reports/stage_a2/power.json:8). The same value is in the blob first
    committed at `fe60a22`, so it is not a later overwrite.
  - The preceding commit is `66a0c81` at 20:35:28Z, so the entire authoring window for Amendment 2
    is 45 seconds wide and the power run lands 9 seconds into it.
  - **`41351a9` itself contains the edit that produced that file.** `git diff 41351a9^ 41351a9 --
    scripts/power_gate.py` replaces `e2 = e2_power(n, rho, inputs)` with `e2 = e2_power(n, rho,
    inputs, draws=1500, simulations=400)` and adds the justifying comment "E2's inner permutation is
    O(draws x n) per simulation, so the gate runs it at a smaller but stated budget. The simulation
    error on a power near one half is about 0.025 at 400 simulations" — a comment that can only be
    written after observing the gate's cost.
  - Reproduction confirms `power.json` was produced by the **post-edit** script: `e2_power(11, 0.18,
    …, draws=1500, simulations=400)` = 0.0600 = stored, while `draws=2000` gives 0.0725;
    `e2_power(11, 0.09, …)` 1,500 → 0.0375 = stored, 2,000 → 0.0475; `e2_power(88, 0.18, …)` 1,500 →
    0.3325 = stored, 2,000 → 0.3800. Three for three at 1,500, none at 2,000.
  - Amendment 3 (ETFExperiment/REGISTRATION.md:821-824) correctly lists "the completed power
    computation" among the data that existed by then — for a moment 4 m 45 s later.
- **Recomputation:** Inputs — the `economic_inputs` block of `reports/stage_a2/power.json`
  (daily_sd 0.027430504889517645, daily_funding_sum 0.0005343574667950626, round_trip_cost_bp 9.0,
  trade_share 0.7567567567567568) fed to `src/etf/power.py:119` `e2_power` copied from `SNAP`.
  Method — reproduce the stored cells at each candidate budget and compare the artifact timestamp
  with the raw commit object. Result — exact match at 1,500/400 only; `computed_at` 20:35:37Z
  against commit 20:36:13Z. Tolerance: exact equality (seeded).
- **What would resolve it:** a shell or session record fixing the moment the amendment text was
  composed relative to 20:35:37Z. Nothing in the repository can settle it: git records only the
  commit instant, and the request ledger has no row between 20:32:17Z and 20:40:46Z. If "written"
  means "committed", the claim is false; if it means "drafted before the gate was run", it is
  unverifiable and the amendment does not say so.
- **Confidence:** MEDIUM — the artifact ordering is certain and the co-committed `power_gate.py`
  edit is strong circumstantial evidence that the gate had been run and its cost inspected, but the
  word "written" leaves a nine-second window in which the sentence could be literally true.
- **Invalidated by later commits?:** no — Amendment 2 stands unedited at the anchor, as the
  append-only rule requires, and `4d11002` is the last commit.
- **Disclosed by the authors?:** no.
- **Consolidation check:** verified. Quote EXACT at `REGISTRATION.md:708-709` in SNAP. Re-read at
  consolidation from live git objects: `41351a9` = 2026-08-28 20:36:13 +0000, `66a0c81` =
  20:35:28 +0000, `power.json:8` `computed_at` 20:35:37Z, and `git diff 41351a9^ 41351a9 --
  scripts/power_gate.py` shows the `draws=1500, simulations=400` edit with its cost comment inside
  the amendment commit. The E2 cell reproductions were carried from the provenance pass and not
  re-run (an `e2_power` sweep is ~10^8 pure-Python operations); everything else re-verified. Kept
  unchanged.

### AUDIT-C-ETFExperiment-5
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** Section 8's inference frame — every power figure, both minimum Ns, and
  the shortfall magnitudes the closure is stated with
- **Direction:** A (closed too early — the conservative α understates the power available)
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED (rerun of the repository's own functions at the two levels)
- **Claim challenged (verbatim):** "**Two co-primaries, distribution-free, one-sided, at
  `alpha_adj = 1 − 0.95^(1/2) = 0.0253205655` each. Both must pass for the Stage B GO row.**" —
  ETFExperiment/REGISTRATION.md:284-286; with the code comment "alpha_adj = 1 - 0.95 ** (1/2): two
  co-primaries, family-wise 0.05, Sidak." — ETFExperiment/src/etf/config.py:25; and Section 10's
  "**both co-primaries at or above 80 percent power at achieved admissible N**" —
  ETFExperiment/REGISTRATION.md:394.
- **Evidence:**
  - Šidák is a **union-type** correction: it controls P(at least one false rejection) when a family
    of tests is read disjunctively. The rule it is attached to here is a **conjunction** — both
    co-primaries must reject before the Stage B GO row fires. That is an intersection–union test,
    whose size is bounded by the **largest** component level, so each component may be tested at the
    full nominal 0.05 with the overall type-I error still at 0.05. Applying Šidák costs power and
    buys nothing.
  - The rule is a conjunction in all three places it is written: ETFExperiment/REGISTRATION.md:285-286,
    :392-395, and ETFExperiment/src/etf/section0.py:139. The only disjunctive use of Šidák in the
    registration is the four-cell threshold-sensitivity **secondary**
    (ETFExperiment/REGISTRATION.md:315-316), where it is correct.
  - The mismatch is load-bearing on magnitudes: the closure is stated as a shortfall between an
    achievable N of 163 and a governing minimum N of 300, at ETFExperiment/REGISTRATION.md:1008-1015
    — "| shortfall at the deadline, governing figure | **137 days** |" and "| shortfall at the
    deadline, **most favourable figure on the record** | **74 days** |".
  - **Both engines are correctly sized at whatever α they are given**, verified rather than assumed:
    E1's empirical size at the registered α is 0.0265 / 0.0270 / 0.0295 at n = 163 across three
    seeds and 0.0220 at n = 300 (MC SE 0.0035); E2's at ρ = 0, n = 163 is 0.0225. The defect is the
    choice of α, not the implementation.
- **Recomputation:** Inputs — anchored `src/etf/power.py`, `src/etf/config.py`,
  `reports/stage_a2/census.json`, `reports/stage_a2/preperiod_inputs.json`, costs from
  `src/etf/costs.py` (9 bp central). Method — re-run the repository's own `e1_power`, `e2_power` and
  `minimum_n` unmodified, first at the registered `α_adj` (to establish bit-exact reproduction) and
  then at α = 0.05, the level an intersection–union rule permits per component. Result — **E1 power
  at N = 163, ρ = 0.18: 0.6105 → 0.7320**; **E1 minimum N at ρ = 0.18: 237 → 207**; at ρ = 0.09:
  845 → 748; **E2 power at n = 300: 0.8000 → 0.8967**, at 250: 0.7100 → 0.7800, at 200: 0.6767 →
  0.7767, so E2's reported minimum stays 300 at the registered grid resolution of 50 while the true
  minimum moves into (250, 300). **The closure does not move**: 163 still falls short of 207 and of
  300, E1's power at achievable N is still under the 0.80 GO floor and still over the 0.50 BLOCKED
  floor, and the Section 0 verdict is unchanged. What moves is magnitude — the "most favourable
  figure on the record" shortfall of 74 days becomes 44, and the reported power at achievable N
  rises by 0.12. Tolerance: bit-exact at `α_adj`; the α = 0.05 figures carry the same 0.0112 (E1)
  and 0.023–0.029 (E2) Monte-Carlo SE as the originals.
- **What would resolve it:** either (a) an amendment recording that Section 8's rule is an
  intersection–union test and that each co-primary is therefore tested at 0.05, with the power table
  and both minimums recomputed; or (b) a stated reason for keeping the conservative level — for
  example a decision rule elsewhere that reads the co-primaries disjunctively. I found none.
- **Confidence:** HIGH on the mismatch — the decision rule is quoted verbatim in the same sentence
  as the correction, and the IUT result is standard. HIGH on the recomputed magnitudes, which are
  reruns of the repository's own functions. HIGH that the closure survives.
- **Invalidated by later commits?:** no — Section 8 sits above every amendment line and is unedited,
  and `ALPHA_ADJ` is a frozen pre-data constant in `config.py`, which has 12 insertions and 0
  deletions across the whole history.
- **Disclosed by the authors?:** no. The registration states the Šidák rationale and the conjunction
  rule in the same breath without noticing that they pull against each other.
- **Consolidation check:** verified. Quotes EXACT at `REGISTRATION.md:283-286` and `:394` in SNAP.
  Re-run first-hand at consolidation: `e1_power(163, 0.18)` = **0.6105** at `α_adj` and **0.7320** at
  α = 0.05; `minimum_n(0.18, 0.80)` = **237** at `α_adj` and **207** at α = 0.05 — both draft
  figures reproduced exactly. The E2 figures and the empirical-size measurements were carried from
  the verification pass and not re-run at consolidation (cost). Budget evidence that the
  verification draft had folded in here was moved out to finding **-3**, where it belongs.

### AUDIT-C-ETFExperiment-6
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** Amendment 6 §4, the closing network-cost record
- **Direction:** neutral (hygiene)
- **Class:** STALE_FIGURE
- **Severity:** S4 — hygiene. The provenance draft graded it S3; resolved down because the severity
  ladder reserves S3 for a stale *blocker* or *external* figure, and no measurement, bar, floor or
  verdict path reads the request count
- **Label:** DERIVED (an append-only ledger against a git commit timestamp)
- **Claim challenged (verbatim):** "- The **220 charged requests** stand as the total lifetime
  network cost. Zero / dollars, no capital, no credential, at any point." —
  ETFExperiment/REGISTRATION.md:1160-1161. Same figure at ETFExperiment/progress.md:514-516, :564,
  :602.
- **Evidence:**
  - `data/ledgers/requests.jsonl` (untracked, 476 lines, mtime 2026-08-29T02:40:42Z, read read-only
    **2026-09-05T18:10Z**, **UNANCHORED**) holds **238 charge rows and 238 settle rows**, first
    charge 2026-08-28T08:12:19Z, last charge **2026-08-29T02:40:32Z**.
  - Charge **#220** is stamped 2026-08-28T20:40:46Z, and at that instant the split is exactly **flow
    33 / archive 79 / venue 108** and the settles are **213 × 200, 5 × 404, 1 × 401, 1 × 403** —
    every figure the documents print is correct *as of 20:40:46Z*, and matches
    ETFExperiment/progress.md:564-565 digit for digit.
  - Amendment 6 is the anchored commit `4d11002`, stamped **2026-08-29T02:43:48Z**, three minutes
    and sixteen seconds after the ledger's last charge. Lifetime totals at that moment: **238
    charges**, split **flow 51 / archive 79 / venue 108**, settling **231 × 200**, 5 × 404, 1 × 401,
    1 × 403.
  - The 18 extra charges are all `flow.table`, taken at a 20-minute cadence from 21:00:36Z to
    02:40:32Z by the `etf-snap` collector that **Amendment 6 itself disarms** three lines earlier
    (ETFExperiment/REGISTRATION.md:1157).
  - Ledger counts at each amendment instant: 145 at Amendment 1, 219 at Amendment 2, 220 at
    Amendments 3 and 4, 228 at Amendment 5, **238 at Amendment 6**.
- **Recomputation:** Inputs — `data/ledgers/requests.jsonl` rows filtered on `kind == "charge"`, and
  `git -C <live> log -1 --date=iso-local 4d11002`. Method — count charge rows, take the prefix of
  length 220, tabulate `source` and the settle `http_status`, and compare against the commit
  instant. Result as above; tolerance exact (integer counts).
- **What would resolve it:** an amendment line recording 238 as the lifetime figure, or restating
  220 as "at the Stage A close-out", where it was true.
- **Confidence:** HIGH — integer counts from an append-only ledger against a raw git commit
  timestamp, re-derived independently at consolidation.
- **Invalidated by later commits?:** no. `4d11002` is the last commit, the ledger has not been
  written since 2026-08-29T02:40:42Z, and both timers are `disabled` and `inactive`.
- **Disclosed by the authors?:** **no** as to the total. Amendment 5 does disclose the mechanism —
  `etf-snap` "costs roughly 33 requests per day" (ETFExperiment/REGISTRATION.md:1084) — but no
  document revises the count, and the sentence says "total lifetime", not "at the time of writing".
- **Consolidation check:** verified and re-derived. Quote EXACT at `REGISTRATION.md:1160-1161` in
  SNAP. Re-read at consolidation: 476 lines, **238** charges, **238** settles, first 08:12:19Z, last
  2026-08-29T02:40:32Z; split at 220 = flow 33 / archive 79 / venue 108 and settles 213/5/1/1;
  lifetime split flow 51 / archive 79 / venue 108 and settles 231/5/1/1; file mtime
  2026-08-29T02:40:42Z; `4d11002` dated 2026-08-29 02:43:48 +0000. Two drafts merged; severity
  reconciled down to S4.

### AUDIT-C-ETFExperiment-7
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** Amendment 1's pre-period blindness statement
- **Direction:** neutral (hygiene)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED (two anchored artifacts)
- **Claim challenged (verbatim):** "every funding rate stamped at or after 2025-05-01 that has
  passed through a reader has been gated — measured live at **572 of 572 post-boundary rows across
  three pages**." — ETFExperiment/REGISTRATION.md:604-606
- **Evidence:**
  - ETFExperiment/reports/stage_a1/venue_and_archive.json: probe `funding_post_period`, `row_count`
    72, `gated_rows` **72**, `readable_rows` 0.
  - ETFExperiment/reports/stage_a1/depth.json: probe `funding_2025_05_page`, `row_count` 500,
    `gated_rows` **500**.
  - 72 + 500 = **572 of 572** — the count is right, and it comes from **two** pages, not three.
  - The other three funding pages that passed a reader are entirely **pre**-boundary and have
    `gated_rows` 0: `funding_pre_period` (72 rows), `funding_2024_01` (500) and `funding_2023_05`
    (500). Five funding pages were probed in all, three of them pre-boundary.
  - **The blindness claim itself is unaffected**: every post-boundary row that passed a reader was
    gated, which is what the sentence is for.
- **Recomputation:** Inputs — `reports/stage_a1/venue_and_archive.json` and
  `reports/stage_a1/depth.json` at the anchor. Method — sum `gated_rows` and `row_count` over every
  funding probe and count the distinct pages carrying post-boundary rows. Result — 572 of 572 over
  **2** pages; tolerance exact.
- **What would resolve it:** "across two pages", or a third post-boundary funding probe if one
  exists outside these two artifacts. I found none.
- **Confidence:** HIGH — a direct read of two anchored artifacts.
- **Invalidated by later commits?:** no.
- **Disclosed by the authors?:** no.
- **Consolidation check:** verified. Quote EXACT at `REGISTRATION.md:603-606` in SNAP. Re-read at
  consolidation: `venue_and_archive.json` holds `funding_pre_period` 72 rows / 0 gated and
  `funding_post_period` 72 rows / **72** gated; `depth.json` holds `funding_2024_01` 500/0,
  `funding_2023_05` 500/0 and `funding_2025_05_page` 500/**500**. 72 + 500 = 572 across two pages,
  exactly as drafted. The provenance pass's P08 is the same defect found independently and is folded
  in here as corroboration.

### AUDIT-C-ETFExperiment-8
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** the Stage A.1 Task 2 pacing rule, as restated after Amendment 1
  substituted it for the registered "half the measured ceiling"
- **Direction:** neutral (hygiene)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED (arithmetic on one anchored artifact)
- **Claim challenged (verbatim):** "Paces are set at **twice the fastest verified-clean spacing** —
  half the highest verified-clean *rate*, because there is no ceiling to halve." —
  ETFExperiment/report.md:150-151
- **Evidence:**
  - The sentence asserts that the two formulations are the same rule. For `archive.timemap` they are
    not. ETFExperiment/reports/stage_a1/rate_ceilings.json records rungs at 5.0 s (5.78/min), 2.0 s
    (**21.28/min**) and 1.0 s (**12.29/min**), all HTTP 200, with
    `highest_verified_clean_rate_per_min` 21.28 and `operating_min_spacing_s` **2.0**.
  - Twice the fastest verified-clean spacing = 2 × 1.0 s = **2.0 s** — the operating value.
  - Half the highest verified-clean rate = 21.28/2 = 10.64/min = **5.64 s** — 2.8× slower than the
    operating value.
  - The divergence exists because this endpoint's observed rate **fell** at the tighter rung
    (12.29/min at 1.0 s against 21.28/min at 2.0 s), so rate and spacing are not monotone for it.
    The two formulations agree, to rounding, on the other five endpoints: flow.table 10.00 s vs
    9.86 s; archive.availability 2.00 vs 2.00; venue.candleSnapshot 2.00 vs 2.00;
    venue.fundingHistory 2.00 vs 2.00; kraken.ohlc 2.00 vs 2.04.
  - The table this sentence sits under (ETFExperiment/report.md:141-148) prints `archive.timemap |
    21.28/min (n = 18) | 2.0 s`, so both halves of the contradiction are on the same page.
- **Recomputation:** Inputs — `reports/stage_a1/rate_ceilings.json` (6 endpoints, 16 rungs, 96
  requests). Method — for each endpoint compute 2 × (fastest all-200 spacing) and
  60/(highest_verified_clean_rate/2), and compare both to `operating_min_spacing_s`. Result as
  above; tolerance exact to 0.01 s.
- **What would resolve it:** naming one of the two formulations as the rule and deriving the other,
  or recording that they diverge for `archive.timemap` and which one the operating pace follows.
  Nothing scientific turns on it — this is a courtesy-pacing statement and the operating pace is
  2.0 s against a probed floor of 1.0 s either way.
- **Confidence:** HIGH — arithmetic on one anchored artifact, re-derived at consolidation.
- **Invalidated by later commits?:** no.
- **Disclosed by the authors?:** no — though the neighbouring sentence discloses the related
  limitation that "**The figures are bounded by what was probed, not by what the server would
  refuse**, and the record says so rather than implying a measured ceiling exists"
  (ETFExperiment/report.md:155-156). That disclosure covers the ceiling's absence, not the
  inequivalence of the two formulations, so the finding is not capped by it.
- **Consolidation check:** verified. Quote EXACT at `report.md:149-151` in SNAP. Re-derived at
  consolidation across all six endpoints: 96 requests over 16 rungs, every rung all-200;
  archive.timemap 2 × fastest clean spacing = 2.00 s against half-the-rate = 5.64 s (operating 2.0);
  the other five agree at 10.00/9.86, 2.00/2.00, 2.00/2.00, 2.00/2.00 and 2.00/2.04. Kept unchanged.

---

## Sound

What verified cleanly. A verified claim is a result, and in this repository most of them are.

**The closure's own leg is the strongest-verified thing in it.** The archive-capture density of
**11 of 333 = 0.0330** against the registered 0.60 bar rebuilds end-to-end from the raw untracked
Wayback timemaps through the repository's own `src/etf/archive.py`: 451 mementos → 37 admissible
days (32 from `timemap-recent` ∪ 10 from `timemap-all_data`, set-identical to the stored artifact)
→ 11 that served a value. The shortfall factor of 18 is 18.164 and the falsification factor of 3.4
is 3.3636. **The irreversibility claim survives every window bound the data admits**: 37 admissible
at the registered lower bound of D 20:00Z, 66 at D 08:00Z, 78 at D 00:00Z, 114 at D−1 00:00Z, and
112 with no lower bound at all — against a 0.60 bar that needs 200. The authors state and quantify
that ceiling themselves at `docs/ACCESS.md:384-385`. This is why no finding above moves the verdict.

**Every simulated power figure reproduces bit-for-bit** from the anchored source at the anchored
seed 20260828: all 12 E1 cells and all 12 E2 cells of `power.json`, all 8 cells of the E2
minimum-N grid, and all three E1 minimum-N bisections (237 / 845 / 3,776). The RNG is stdlib
`random.Random` with no third-party dependency, so "reproduces" means identical to the last digit.

**The census reconciles exactly, three ways.** 11 admissible + 53 too-late + 243 no-capture + 25
served-no-value + 3 no-printed-value + 1 fetch-failed = **336**; `by_month` over 16 months sums to
336 days and 11 admissible; 37 timemap-admissible = 11 + 25 + 1; 333 printed + 3 = 336. The
derived shares follow: live trade share (138 + 114)/333 = 0.7567568, admissible trade share
(5 + 3)/11 = 0.7272727, inside-band share 81/333 = 0.243243.

**The retro-revision table is honest, including in its definition.** All 11 stored rows have
`delta_usd == 0.0` and `as_printed_usd == current_usd`, zero sign flips, zero threshold crosses,
`meets_registered_minimum` false against the registered 30 — and `revised = delta != 0.0`
(`scripts/retro_revision.py:108-124`) is the **tightest possible** definition, so the 0-of-11 result
cannot be an artefact of a loose test. The record then declines to promote it, repeatedly.

**The pre-registration ordering is real to the second** (see §Verification scoreboard → Provenance):
five registration commits, the last 29 seconds before the first network charge; Section 0
byte-identical from `44567f6` to the anchor; `REGISTRATION.md` append-only across all six post-data
commits; `config.py` +12/−0 across the whole history with every registered bar, floor, threshold,
horizon, alpha, deadline and cap untouched. **If the thesis had been that this repository back-dated
its registration, edited a bar after seeing data, or moved a threshold to reach a verdict, the
evidence would have shown it and it does not.**

**Two amendments that did move a figure were both properly handled.** The archive-density
falsification (0.1111 → 0.0330) is recorded as *falsified* in Amendment 2 with Amendment 1 left
standing above it, and the census code change that caused it landed 45 seconds earlier. The
governing minimum N (237 → 300) is recorded in Amendment 4, whose stated input — `e2_minimum_n.json`,
`computed_at` 20:40:00Z — genuinely predates it. Amendment 6 corrects Amendment 5 by appending a
correction rather than editing it.

**The pacing amendment is a model of a well-handled post-data substitution.** The registered rule
("half the measured ceiling") could not be applied because no ceiling was found; Amendment 1
substitutes an explicit alternative, names its precedent, records that the figures are bounded by
what was probed rather than by what the server would refuse, and leaves the two unmeasured endpoints
on their slower pre-measurement figures rather than letting them inherit a sibling's. The 96 probe
requests across 6 endpoints, every one HTTP 200, verify exactly.

**Also verified, each exactly:** the 5,001-row `candleSnapshot` cap over 17 bisection probes with
zero-row probes at exactly {730, 550, 400, 300, 250, 225} and a first open of 2026-02-01T11:00:00Z
(5,001 hours to 20:00Z on 2026-08-28); the 5,002 sealed unique hourly opens with no duplicates and
no gaps, and the one-row difference from the depth probe resolved as the window sliding, not a
duplicate; 142 of 333 days at ≥ 0.95 candle and funding coverage; the pre-period derived chain
(mean hourly funding × 24 = 0.00053436, × 365 × 100 = 19.504 %/yr, 476 closes → 475 returns,
22 × 500 + 423 = 11,423 over 23 pages); a 9 bp round trip as 0.032810 of one daily σ; the binomial
SE 0.023094 at m = 300; the Šidák constant 0.025320565519103666; 676 date rows → 336 out-of-sample
→ 333 printed with exactly 3 all-dash rows; 153 mementos over 484 calendar days = 0.31612/day;
74/153 = 48.37 % in the clock band; 112/333 = 33.63 % unbounded; 315 of 333 days agreeing within
2 %; zero whole-word occurrences of "evening" or "night" across both Farside pages; the retro cohort
of exactly 8 trading days with all eight dates matching; all six mutations caught and restored
green, with the earlier run's failures disclosed by the authors at `report.md:417-421`; 76 files
under `mypy strict` per `pyproject.toml:44` (34 src + 26 tests + 16 scripts); `verdict.py` imported
by nothing but its own test, which itself asserts that no Stage A module imports it; `data/state/`
absent; both collectors `disabled` and `inactive`; and no credential anywhere in any reachable
commit.

**Recorded and not raised**, because each is either immaterial or already disclosed: the "one-ULP
steps" of the Section 0 boundary fixtures are `1e-12`, roughly 9,000 ULPs at 0.8, though the
property being tested — strict-versus-non-strict comparison exactly on 0.80 / 0.50 / 0.50 — is
genuinely pinned; "the request ledger (143 charged requests)" at `REGISTRATION.md:601` was 145 at
the commit instant, the two extra rows being the `archive.timemap` fetches whose measurement the
same amendment registers; `.env.example` is a 200-byte comment block whose first line reads
"# Deliberately empty" rather than a byte-empty file; `src/etf/pacing.py:20-24`'s comment says "96
requests across 8 endpoints" where the register correctly says 6, and the per-endpoint counts in
that same comment sum to 96; ADR-003's "81 of 333 days (24.3 percent)" postdates the §8 registration
it documents by 12 h 25 m, though §8 as registered carried the same rationale qualitatively and the
ADR labels the figure "measured" and carries its n; the two one-shot `meta.*` endpoints were added
to the pacing map with no amendment line but at a conservative 5.0 s; the E2 budget reduction is
disclosed one amendment late; `docs/ACCESS.md:382`'s 48.37 % is a clock-band share, and under the
stricter trading-day reading the figure would be 57/153 = 37.5 %, but the sentence says "fall inside
the registered 20:00–08:00 UTC window", which is the clock reading, and the inference it supports is
sound on that reading; and `newey_west`-style estimator conventions do not arise here at all,
because nothing was estimated on a time series.

**What I would have expected to find if a "claimed too much" thesis held, and did not find:** a
power figure that does not reproduce (all 32 do); a bar or floor edited after data existed (none of
the 24 registered constants moved); an amendment that edits text above its own line (all six are
pure appends); a verdict fired on a leg that was not measured (the density leg is measured
end-to-end and is the one that closes it); an outcome value read before the seal (the guard test
walks the parse tree for ten price-field names across `src/` and `scripts/` with an empty exempt
list, `data/state/` is absent, and `verdict.py` is imported by nothing); or a secret in history
(none). The defects that do exist are labelling defects in the surrounding prose, not defects in the
machinery.

---

## Could not be checked and why

| Item | Why not | What is missing |
|---|---|---|
| **Pre-period daily sd 0.027431 (n = 475) and mean hourly funding 0.00002226 (n = 11,423 over 23 pages)** at the primitive level (`report.md:296-299`) | `scripts/preperiod_inputs.py` writes only the summary; the 1d candle payload and the 23 funding pages were never written to disk and are absent from `data/`. Every quantity derivable *from* the summary does check — 24-hour sum, annualisation, 476 closes → 475 returns, 22 × 500 + 423 = 11,423 | the raw payloads. Irrecoverable without refetching the venue, which is out of scope and which the repository's own closure forbids |
| **"Two of the six [mutations] required fixing the harness rather than the source"** (`report.md:419`) | `reports/stage_a4/mutations.log` records outcome flags only — no diff, no failing test id, no harness-vs-source attribution. The six *outcomes* verify (all `caught=True restored_green=True`) | a per-mutation record naming the failure site |
| **"`make lint`, `make typecheck` and `make test` are green: ruff clean, mypy strict clean"** (`report.md:401-403`) | no gate output is stored anywhere in the repository. The **76**-file count verifies exactly against `pyproject.toml:44`; "green" does not, and re-running the repository's own gates is outside a read-only audit | a stored lint/typecheck/test report, or a CI log |
| **Every carried external statistic** — Newey–West t 3.12 (n = 313), t 8.99, IV F 21.58, Granger β 0.47 / t 9.75, reversal t −2.42..−3.99, 10-day t 4.49, IV t 2.65 (n = 563), the 90-day rolling 0.16 vs 0.68 | measured by other authors on data this repository does not hold, and **explicitly labelled carried** at `REGISTRATION.md:482-485`. Only t 3.12 propagates into a bar, and **that propagation is checked** (ρ = 0.176 → registered 0.09) | the source studies' data |
| **The Section 0 verdict object and the as-printed observability verdict as computed objects** | `src/etf/section0.py:fire_section0` and `src/etf/observability.py:fire_observability` are called by nothing outside their own tests, and no verdict artifact exists under `reports/`. I verified instead that every input the prose verdict cites reproduces, and that the prose verdict is what those functions would return on those inputs (density 0.0330 < 0.60 → `density_ok` False; `fire_observability` **raises** on `revision_days = 0`, so the forward leg genuinely cannot be evaluated — which is what the documents say) | a stored verdict object, or a script that fires the gate and writes its output |
| **Whether a working forward snapshotter would have made every printed day admissible** — the counterfactual behind finding **-1** | the collector ran ~6 h over a single trade date, was disarmed 2026-08-29T02:43:48Z, and produced 0 admissible days from 0 completed forward days | at least one completed forward print inside the qualifying window. The retro evidence cuts both ways: served captures run +04:05 to **+07:59:42**, i.e. right up against the 08:00Z anchor |
| **Whether any network request was made before 2026-08-28T08:12:19Z** | the ordering claim rests on the ledger's own first row plus `reports/stage_a1/robots_and_terms.json`, both written by the same code path (`etf.ledger.requests`). A request sent outside that path would leave no trace. `data/` is gitignored, so the tree at `44567f6` can only show that no data artifact was *tracked* | an independent network log. The claim is supported by everything available and cannot be closed beyond that |
| **When Amendment 2 was "written" as opposed to committed** (finding **-4**) | git records commit instants only; no shell history, editor state or session log is in the repository, and the request ledger has no row between 20:32:17Z and 20:40:46Z | a session or shell record |
| **Whether the A.1 Task 1 probe code that ran at 08:12Z is the code committed at 20:04:41Z** | the probes ran twelve hours before their commit, and `meta.robots` — the first ledger endpoint — was only added to the pacing map in that commit, so the working tree at run time held uncommitted code. This does not touch the pre-registration ordering (all registration commits precede 08:12:19Z) but the *probe* code cannot be pinned to a commit predating its own run | a commit of the probe code before its run, or a hash recorded in the artifact |
| **Whether the sealed outcome store was ever opened outside the repository's own code paths** | the structural guards, the absence of `data/state/` and the import graph were all verified; an out-of-band read from a REPL or notebook would leave no trace. Stated as a limit, not as a doubt | nothing that any read-only audit could supply |
| **The E2 minimum-N grid, independently re-run** | `e2_power` at n = 300 with 1,200 draws and 300 simulations is order 10⁸ inner operations in pure Python. The budget claim for that grid was verified by reading `scripts/e2_minimum.py:42` against `e2_minimum_n.json`, and the grid's three published cells reproduce at the stated budget in the verification pass, but the full grid was not re-run at consolidation | compute time only |
| **Everything under `data/` as an anchored fact** | `.gitignore` line 2 excludes `data/` in full, so no raw primitive is in the snapshot. Eight claim rows could only be checked against untracked files | nothing for the check itself — the files exist and reproduce — but every figure derived from them is **UNANCHORED**, carries its read time, and may have changed after the anchor. Two files demonstrably did (the request ledger 220 → 238, the snapshot ledger 2 → 20), and finding **-6** turns on exactly that |

---

## Live-repo access log

Per COMMON_RULES, `git status --porcelain` was run on the live repository before the first access
and after the last, in **all three** access windows (the provenance pass, the verification pass, and
this consolidation). All six outputs are recorded verbatim. `HEAD` matched the anchored SHA every
time.

**Window 1 — provenance pass, 2026-09-05T03:58:55Z to 04:15:27Z**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
(no output — clean, exit 0)
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```
…and identically at 04:15:27Z.

Operations: `git log --all --date=iso-strict`, `git log --reverse --name-status`,
`git ls-tree -r 44567f6`, `git diff --numstat` and hunk headers for the six `REGISTRATION.md`
commits, `git log --follow -p -- src/etf/config.py`, `git diff 41351a9^ 41351a9 --
scripts/power_gate.py`, `git show fe60a22:reports/stage_a2/power.json`, `git log -S "220 charged"`,
`git log -S "20.8"`, `git remote -v` / `for-each-ref` / `reflog show refs/remotes/origin/master`,
`git show <c>:REGISTRATION.md` for seven commits, `git grep` history-wide secret scan,
`ls -la data/` and reads of `data/ledgers/requests.jsonl`, and `systemctl --user` timer checks (not
a repository access).

**Window 2 — provenance re-verification, 2026-09-05T05:48:20Z to 06:06:02Z**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
(no output — clean, exit 0)
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```
…and identically at 06:06:02Z. The whole provenance report was re-derived rather than carried
forward: every git fact re-run, every recomputation re-run from a fresh `SNAP` copy. Two items
improved (the `solattn-daily` timer, found via `list-unit-files` because disabled units do not
appear in `list-timers`; and a `report.md` wording note); nothing was overturned.

**Window 3 — verification pass, 2026-09-05T05:48:34Z to 06:04:15Z**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
(no output — clean, exit 0)
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```
…and identically at 06:04:15Z.

| time (UTC) | operation | purpose |
|---|---|---|
| 05:52 | `ls -la data/access/`; read `timemap-recent.txt`, `timemap-all_data.txt`, `farside_all_parsed.json` | C07a-c, C14 |
| 05:52 | read `data/snapshots/flow_snapshots.jsonl` row count and open-day state | finding **-1** |
| 05:56 | read `data/access/sosovalue-btc.html` (`__NEXT_DATA__` payload only) | C15a-b |
| 05:57 | read `data/outcomes/btc-1h-servable-window.json` — **`t` timestamps only, for row-count, duplicate and gap checks; no price field was extracted or retained** | C10, C13 |
| 05:58 | read `data/ledgers/requests.jsonl` (476 lines) | C17 / finding **-6** |
| 05:59 | `grep -cwiE 'evening\|night'` over the three captured HTML pages | C28 |
| 06:00 | `git log --date=iso-strict -12`, `git log -1 4d11002` | Amendment 6 commit time |

**Window 4 — this consolidation, 2026-09-05T18:05:17Z to 18:10:55Z**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
(no output — clean, exit 0)
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain     # 18:10:55Z
(no output — clean, exit 0)
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```

| time (UTC) | operation | purpose |
|---|---|---|
| 18:05:17 | `git status --porcelain`, `git rev-parse HEAD` | pre-access record |
| 18:09 | read `data/access/farside_all_parsed.json` (676 rows) read-only | re-derive finding **-2** from scratch |
| 18:10 | read `data/ledgers/requests.jsonl` (476 lines); `TZ=UTC stat` on it | re-derive finding **-6** |
| 18:10 | `TZ=UTC git log -1 --date=iso-local` on `4d11002`, `41351a9`, `66a0c81`; `git diff 41351a9^ 41351a9 -- scripts/power_gate.py` | findings **-4**, **-6** |
| 18:10:55 | `git status --porcelain`, `git rev-parse HEAD` | post-access record |

Everything else in this consolidation was computed from `SNAP/ETFExperiment/` and from copies of
`src/etf` taken from `SNAP` into
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-etf-consol/`.

**Nothing in the audited repository was modified in any window, and no repository script was
executed in place.** No `.env`, keystore, session or credential file was opened. One untracked
working-tree entry does not appear in `status` and is reported here as COMMON_RULES requires:
`_CLOSED_DO_NOT_RUN_HERE` (747 B, mtime 2026-09-02 22:38 local), hidden from `status` by
`.git/info/exclude` line 7. It is an owner-written closure marker dated three days before this
audit, **it is not mine**, and it was never opened beyond `ls`.

**Anchoring caveat.** Every figure derived from `data/` is UNANCHORED and carries its read time
above. The live tree stands clean at the anchored SHA, but `data/` moved after the anchor's
documents were written — the request ledger from 220 to 238 charges and the snapshot ledger from 2
to 20 captures, both between 2026-08-28T20:40Z and 2026-08-29T02:40Z. Finding **-6** turns on
exactly that movement. Nothing has been written to `data/` since 2026-08-29T02:40:42Z.
