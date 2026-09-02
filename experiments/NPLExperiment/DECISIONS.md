# DECISIONS.md — append-only ADR log

Read before revisiting a settled question. Each ADR names the decision, the
ground it rests on, and what was measured. Nothing here is edited in place.

## ADR-001: The entry anchor is the second daily close

**Date:** 2026-08-27 · **Status:** accepted · REGISTRATION.md Section 3

The entry is the close of listing day + 1 (the timestamp 00:00:00Z of
listing day + 2). Day-0 and day-1 prices carry the listing pop and the
thinnest books of the instrument's life; entering at the second daily close
prices the hypothesis on a market that has existed for one full UTC day.
The day-1 close is recorded as a descriptive anchor, never verdict-bearing.
Fixed before any census row existed.

## ADR-002: The control rule is same-dex, 180-day age, nearest signed trailing funding

**Date:** 2026-08-27 · **Status:** accepted · Section 6

Matching on the signed trailing 168-hour mean hourly funding at the event
entry separates listing age from generic negative-funding compensation —
the H8 cancellation is the measured reason the control exists. Same dex
keeps fee class and microstructure comparable; 180 days makes the control
unambiguously not-young; with-replacement keeps thin dexs matchable. Ties
break to the older listing, then coin name ascending — both fixed before
any pair existed. Matching reads no row stamped after the event entry
(`npl.controls.PostEntryRead`, pinned by test).

## ADR-003: Cost bands, 9 bp vanilla and 18 bp HIP-3 round trip

**Date:** 2026-08-27 · **Status:** accepted · Section 5

Carried basis: venue base fees 1.5 bp maker / 4.5 bp taker per side → 9 bp
taker round trip central, 3 bp all-maker low bound, 18 bp stress bound.
HIP-3 builder markets default to double fees → 18 (6, 36). The A.1 census
found per-dex meta carries `deployerFeeScale` per instrument — a live
verification input recorded for Stage B's descriptive cost table. Forward
events add a measured touch spread at entry (ADR-008), descriptive only.

## ADR-004: The blindness field lists

**Date:** 2026-08-27 · **Status:** accepted · CLAUDE.md, Section 0

Candle payload fields readable outside sealed writers: `t`, `T`, row count.
fundingHistory fields readable: `time` always, `fundingRate` only where
`time` is at or before the referencing event entry. l2Book `px`/`sz`
readable in `spread.py` only (a registered descriptive cost input, not an
outcome). Enforced structurally: the repo-wide AST guard scans every
subscript and `.get()` key (tests/test_guards.py), the gated reader returns
a coercion-refusing `Absent` for post-entry rates, and the sealed writers
have no parser at all. A text search was rejected — the InsiderExperiment
mutation exercise proved text-level guards pass vacuously on a key left in
a comment.

## ADR-005: Pacing figures are measured per endpoint, operating at half ceiling

**Date:** 2026-08-27 · **Status:** accepted · docs/ACCESS.md Task 2, npl/pacing.py

The solattn Amendment 6 lesson, applied in advance: ceilings are per
endpoint, never per host, and measured never assumed. Measured 2026-08-27:
refusals exist at probe scale only on perpDexs (~79/min) and candleSnapshot
at 5,000 rows (~23/min, sustained clean); the refusal body is the four
bytes `null` with HTTP 429; the documented 1200 weight/min does not
describe admission. Operating paces: meta 0.8 s, metaAndAssetCtxs 0.8 s,
perpDexs 1.6 s, candleSnapshot 5.3 s (endpoint-wide, from the 5,000-row
ceiling), fundingHistory 1.4 s, l2Book 0.5 s — half the measured ceiling
where one was found, half the highest verified-clean rate where not.

## ADR-006: The seal target is the closed day, and the open day is never sealed

**Date:** 2026-08-27 · **Status:** accepted · npl/watcher.py

The solattn ADR-019 defect, avoided by construction: the 01:40Z daily pass
seals yesterday's births manifest, `seal_closed_day` refuses `day >= today`
loudly, a closed day without a seal refuses to read (a missing attestation
is an error, never a pass), and a sealed manifest that grew raises rather
than being re-attested. The seal lands first in the daily pass, so a failed
attestation stops the pass before anything else runs.

## ADR-007: Checkpoint days are +2, +32, +92 with a 5-day catch-up window

**Date:** 2026-08-27 · **Status:** accepted · Section 12 / npl/checkpoints.py

+2 captures the entry row the day it exists; +32 and +92 give the 30- and
90-day windows one full day of slack for the venue to publish the final
candle. The catch-up window is 5 days; a window that closes unsatisfied
writes a loud `expired` record — a permanent hole is a recorded outcome,
never a silent one (the solattn Amendment 6 lesson).

## ADR-008: The entry-anchor spread snapshot rides the hourly watcher at :05

**Date:** 2026-08-27 · **Status:** accepted · npl/spread.py, ops/systemd

The registered window is 30 minutes after the 00:00Z entry close. The
watcher timer fires at :05 every hour, so the 00:05Z pass falls inside the
window; a pass arriving later than 30 minutes writes a loud expired record
and the spread is never backfilled — a stale spread is not a spread.

## ADR-009: The event date cross-check, epoch censoring, and the mechanical hyperp tag

**Date:** 2026-08-27 · **Status:** accepted · REGISTRATION.md Amendment 1

Measured: the venue index-backfills 1d candles to 2020 while its funding
archive begins 2023-05-12T00:00Z exactly (5 of 5 launch-era instruments),
and every post-epoch listing probed (7 of 7) has candle and funding starts
on the same UTC day. UNIBOT (+49 days) and CYBER (+10) show the pre-vanilla
signature. Consequences: the event date requires candle-vs-funding
agreement within ±1 day; epoch-touching instruments are censored as events
and remain controls; funding-later-than-candles beyond tolerance tags
`hyperp_conversion` mechanically with the event at the funded phase start.
The documentation-based hyperp source was probed and found not
machine-readable; the mechanical signature cannot be fitted to outcomes
because it reads timestamps only.

## ADR-010: The funding archive is per-instrument, sealed raw, cursor-resumable

**Date:** 2026-08-27 · **Status:** accepted · npl/archive.py

Control assignment needs candidates' trailing funding at each event entry;
fetching per (event, candidate) is quadratic in requests. One full archive
per instrument (500-row sealed pages, cursor derived from the sealed pages'
own timestamps) makes assignment and the retro windows local reads under
the blindness gate. The daily pass advances it under a 15,000-request soft
budget, leaving 5,000 headroom under the registered 20,000 cap.

## ADR-011: The config-enforcement guard walks the parse tree, with a named pending list

**Date:** 2026-08-27 · **Status:** accepted · tests/test_guards.py

Ported from InsiderExperiment ADR-012's correction: the guard reads
identifiers from the AST, never text. The Stage A addition: a
PENDING_ENFORCEMENT list named each not-yet-consumed field with the task
that lands its consumer, the test pinned unread == pending in both
directions, and the list reached empty at the end of Stage A.3 — a field
enforced nowhere is decoration, and a pending entry that outlived its task
would have failed the build.

## ADR-012: The 60-minute watcher cadence and the 01:40 UTC daily pass

**Date:** 2026-08-27 · **Status:** accepted · ops/systemd

60 minutes resolves a listing to the hour — the registered listing-day
tolerance is a day, so the poll is 24× finer than the quantity it feeds,
and one poll costs ~12 requests against a measured meta ceiling of
160+/min. 01:40 UTC clears solattn's 00:40 pass and AiTrader's 22:30
collection (both verified present and untouched on 2026-08-27), and lands
after the venue's 00:00Z daily close with 100 minutes of slack.

## ADR-013: The register architecture and the familywise fixed-point cull

**Date:** 2026-08-28 · **Status:** accepted · HYPOTHESES.md, npl/register/cull.py

One repo, one substrate, many hypotheses: H1 closed, H2/H3/H4 co-registered
on fresh data under one familywise budget (alpha_h = 1 − 0.95^(1/k)). The
cull runs to a k/alpha fixed point with simultaneous removal per pass:
any hypothesis under 0.50 required power at the current alpha_h drops, and
alpha_h recomputes. Power weakly grows as k falls, so removal is final and
the iteration terminates. Measured sensitivity, recorded plainly: under
the flat pair projection H2 would have dropped in pass 1 alongside H3/H4
(k = 0) — the simultaneous-drop semantics can cull a hypothesis that
would survive alone. A future register weighing sequential (worst-first)
removal should decide BEFORE any projection exists; this one registered
simultaneous-drop at A.0 and applied it unchanged.

## ADR-014: The quarantine is structural — string pin, import isolation, recorded sample

**Date:** 2026-08-28 · **Status:** accepted · tests/test_guards.py, npl/register/generating_sample.py

The spent H1 read is quarantined by three mechanisms, each with its
refusal produced by test: an AST string pin holding the reachable stage_b
surface at exactly the two H1 modules (scanned on synthetic offenders,
not just asserted clean); import isolation of the npl.stageb package; and
the 312 generating-sample event IDs recorded write-once in
data/state/generating_sample.json, refused by every successor view. The
sample is usable for power assumptions, labelled so wherever carried,
never admissible to a successor verdict.

## ADR-015: Fresh means the complement of the generating sample

**Date:** 2026-08-28 · **Status:** accepted · npl/register/fresh.py

No clock defines the fresh cohort — the recorded generating-sample set
does. Fresh = every Amendment-1-resolved event not in the sample and not
dead before entry. On the sealed census this reproduces the registered 62
pending-at-closure exactly (pinned), and census refresh rows extend it
without a boundary rule that could drift.

## ADR-016: The by-dex pair projection governs; the flat summary rides beside

**Date:** 2026-08-28 · **Status:** accepted · registrations/H2 Amendment H2-1

Pairability on this venue is a deterministic function of measured dex age
(xyz measured 36/36 pairable; young dexs cross the 180-day candidate age
on known dates), so projecting pairs as per-dex accrual × onset windows
is the faithful application of the A.1 measurement. The flat share
(0.613 × forward events) is a knowingly-wrong stationary summary and is
reported beside as sensitivity — including that it would have culled
everything. Both projections use only A.1-measured quantities committed
before any cull arithmetic ran.

## ADR-017: Generating-sample figures govern every honest range

**Date:** 2026-08-28 · **Status:** accepted · registrations/H3 §8, H4 §8

Where a subset figure is unknown (H3's magnitude leg, H4's conditional
share), power computes at both ends of the honest range and the
generating-sample-derived end governs the cull — adopting the optimistic
end after seeing the pessimistic one would be outcome-fitting, and
assuming the conditional share exceeds the unconditional one would assume
H4's conclusion. Both ends are always reported.

## ADR-018: Candidate trailing windows — trail files on the main dex, archive extension on hip3

**Date:** 2026-08-28 · **Status:** accepted · npl/register/forward.py, docs/ACCESS.md

Assignment needs each candidate's (entry−168h, entry] funding. Main-dex
candidates (~173) needed one page each for two nearby entries → sealed
raw trail files (trail-*.raw, outside the page-* cursor globs, so the
contiguous archive discipline of ADR-010 is untouched). xyz candidates
overlapped 36 entries spanning 90 days → contiguous archive extension.
380 pages total against ~905 for blanket extension.

## ADR-019: The fresh cohort seals at maturity; checkpoints are forward-only; pair legs ride the event schedule

**Date:** 2026-08-28 · **Status:** accepted · npl/cli.py, registrations/H2 Amendment H2-2

The 62 backfillable events' candle windows seal once, at entry+92d, under
the fresh plan (the H1 retro-backfill shape) — a write-once seal of a
partial window would block its own completion, and 1d retention is
measured-full so nothing ages out. Checkpoints (+2/+32/+92, unchanged
bars) run for forward births, with the pair's elder leg checkpointing on
its event's schedule; H2 coverage requires both legs.

## ADR-020: Pair costs are per-leg centrals with half/double bands; E2's floor is per pair

**Date:** 2026-08-28 · **Status:** accepted · npl/register/pairs.py, registrations/H2 §5, §8

Pair central = sum of the legs' H1 centrals (18/27/36 bp); bands half and
double per the register prompt (unlike H1's third/double single-leg
bands — recorded to prevent silent reconciliation). E2's economic floor
is 2× the pair's own central cost, so a mixed pair is held to its own
bar, not a family average. Requirement modes registered: H2/H3 all-legs,
H4 best-cell.

## ADR-021: Collectors take their write roots as parameters

**Date:** 2026-08-28 · **Status:** accepted · npl/register/forward.py, registrations/H2 Amendment H2-2

A test drove the trail fetcher into the real data/funding store through a
default-parameter root (7.2M fake-coin seal files before the run was
stopped; verified test-only and removed). The lesson generalizes: any
function that writes a store takes the root explicitly, the test pins
that artifacts land in the given root and nowhere else, and unbounded
fetch loops carry a loud cap. Defect recorded in Amendment H2-2 and
progress.md rather than smoothed over.

## ADR-022: The control falls back to the main dex where the event's own dex has no eligible elder

**Date:** 2026-08-28 · **Status:** accepted · npl/controls.py, npl/register/fallback.py, registrations/H2 Amendment H2-3 Change 1

**Made before any outcome existed.** At the moment this was decided the H2
pair reader had seen only synthetic fixtures, no pair net return had been
computed, and both per-look latches were absent.

The A.2 measurement was unambiguous: 24 of the 62 fresh events sat on dexs
whose oldest instrument was younger than the registered 180 days (para 18,
mkts 4, io 2), so the same-dex rule could not pair them at all, and their
dexs cross the age threshold only on deterministic future dates
(2026-09-26, 2026-12-26, 2027-02-13). Waiting was the alternative, and
waiting is what pushed H2's earliest read past its own deadline.

The fallback is consulted **only** where the same-dex candidate set is
empty after both the 180-day and coverage conditions; a same-dex candidate
always wins, and the distance, tie-break, and replacement rules are
identical. Every pair carries `pair_type`, and **the tag never filters a
primary statistic** — it names a stratum. The `same_dex` subset is reported
beside every primary figure at every look, because a cross-dex pair matches
funding but not venue microstructure and a reader must be able to see
whether the primary rests on it.

Recorded plainly: this is a **relaxation**, admitting pairs the registered
rule refused. It changed no bar, no alpha, and no outcome definition. It
took the backfillable cohort's match rate from 0.613 to 1.000 (62/62), and
it collapsed the by-dex and flat projection models into one, because
pairability stopped being a function of the event's own dex age.

Rows written before the amendment carry no `pair_type`. They are
`same_dex` **by the registered rule that produced them**, not by imputation
of a missing value — the rule in force admitted same-dex candidates only.
`pair_type_of_row` encodes exactly that, and refuses an unregistered tag.

## ADR-023: E2's economic floor moves from 2× to 1× the pair's central cost

**Date:** 2026-08-28 · **Status:** accepted · npl/config.py, npl/register/pairs.py, registrations/H2 Amendment H2-3 Change 2

**Made before any outcome existed**, on the same evidence as ADR-022:
counts, tags, and timestamps.

**This is a weakening, and it is recorded as one.** A pair returning between
one and two times its own execution cost now counts as a success where it
did not. The bar still requires each pair to clear its own round trip (18,
27, or 36 bp by class), so E2 remains an economic test and not a
restatement of E1's sign test; what it no longer requires is a doubling.

Two guards travel with it. First, **the 2× figure is retained as a named
secondary computed at every look**, so the cost of the weakening sits in the
same artifact as its benefit. Second, the registered power assumption had to
move with the floor — E2's 0.60 was itself a judgment discount from E1's
0.651, not a measurement — and the new figure is set by **linear
interpolation in the floor multiple** between multiple 0 (E1's 0.65) and
multiple 2 (0.60), giving 0.625 at multiple 1. Linear is the neutral choice,
not a claim about a distribution nobody has measured. Because it is a choice,
**every minimum N is reported twice**, at 0.625 and at the unchanged 0.60:
117/59 against 184/92. A reader who rejects the interpolation can read the
second row and see that the design does not reach 0.80 by the deadline.

The alternative considered and declined: keep 2× and accept a 169-pair
single-look minimum reached near 2027-05/06, past the registered deadline.
That is not a stricter experiment, it is an experiment that never reports.

## ADR-024: H2 is decided at two looks, on an exact binomial boundary, with the split fixed in advance

**Date:** 2026-08-28 · **Status:** accepted · npl/register/sequential.py, npl/register/pairs.py, npl/register/latches.py, registrations/H2 Amendment H2-3 Change 3 and H2-4

**Made before any outcome existed.**

A single look at the deadline is one chance to learn anything; a second,
earlier look costs alpha but buys a date. The split is **alpha_1 = 0.02,
alpha_2 = 0.03**, fixed at registration and confirmed by the Task 3
arithmetic against a two-clause materiality test written before it was
applied: a replacement must gain ≥ 0.01 governing power **and** must not cut
the look-1 firing probability by more than 0.05. Two candidates —
(0.01, 0.04) and (0.005, 0.045) — gain +0.027 and +0.026 power and fail
clause (b) by cutting the interim's firing probability 0.193 and 0.277.
**Clause (b) exists because a split that makes look 1 nearly inert has not
improved a two-look design, it has deleted one of its looks.**

The boundary is exact, not asymptotic: k₁ from alpha_1 alone, k₂ from the
spend **conditional on not having rejected at look 1**, over the independent
increment. Total type-I is at most alpha_1 + alpha_2 = 0.05 by construction
and in practice lands under it (0.0422 at the look-2 minimum). Validity
rests on n₁ and n₂ being fixed by outcome-blind quantities — pair counts and
the calendar — which is a property of the substrate, so the substrate says
so and a test pins it.

Consequences accepted deliberately: Section 10's "exactly once" becomes
**exactly twice**, one open per look, each behind a write-once fsynced
latch, with look 2 structurally unable to run before look 1's latch exists.
Futility may stop the trial early, but **only** on the registered boundary —
conditional power under 0.10 at the registered true share — never on
inspection.

## ADR-025: A defect in ADR-024's own wording, corrected before any data existed

**Date:** 2026-08-28 · **Status:** accepted · registrations/H2 Amendment H2-4 §7, npl/register/pairs.py

Amendment H2-3 wrote the look-2 GO condition as "both reject at k₂", with
the look-2 rejection event defined as `S₁ < k₁ and S₂ ≥ k₂`. Read literally,
a co-primary whose look-1 count had already crossed k₁ — while the other had
not, so the trial correctly continued — could never satisfy `S₁ < k₁` at
look 2, and the design would fire **FAIL because the early evidence was too
strong**. The defect surfaced while writing the look-aware reader, was
recorded rather than smoothed over, and was corrected in the same session,
**before any outcome value existed and while the reader had still seen only
synthetic fixtures**.

Corrected rule: a co-primary passes at look 2 when the procedure has
rejected its null **by** look 2 — `S₁ ≥ k₁` or `S₂ ≥ k₂`. This is the union
of the two registered rejection regions, so the exact spend and every number
in the boundary table are unchanged, and the familywise error is untouched.
`S₁ < k₁ and S₂ ≥ k₂` remains the definition of the look-2 rejection *event*
used to compute that spend. The known-answer test for exactly this case —
E1 crossed at look 1, E2 crosses k₂ = 69 at look 2, row is GO — is the pin.

The general lesson, third time in this project: a registration written in
prose and a reader written in code disagree in the corners, and the
disagreement is only visible when the code is written. Write the reader
inside the same session as the amendment, and correct the amendment while
the correction is still free.

## ADR-026: The H5 ticker-to-underlying mapping is an exact-string table, written before any price was read

**Date:** 2026-08-28 · **Status:** accepted · registrations/H5 Section 2, npl/h5/resolution.py

The H5 universe is "every HIP-3 instrument whose ticker resolves to an
identifiable equity, ETF or index underlying". Resolving a ticker is where a
universe gets fitted: the temptation is to decide, after seeing which
instruments are interesting, that `GIGADEV` obviously means GigaDevice and
`STRC` obviously means whatever is convenient. So the mapping is a **table of
exact strings, committed before the first price read** — 198 entries, in
three disjoint tables whose disjointness is checked at import.

The admission criterion is stated once and applied mechanically: a ticker is
`resolved` only where it is **(a) an exact listed ticker symbol on a major
exchange** or **(b) an unambiguous name or standard abbreviation of exactly
one listed issuer or one named public index**. Everything failing both is
excluded with a recorded reason — `ambiguous_ticker`, `private_no_public_underlying`,
`basket_no_named_reference`, `venue_house_index`, `not_in_registered_mapping`
— and counted. Several exclusions are tickers whose likely meaning a reader
can guess (`QNT`, `STRC`, `SKHX`, `SKHY`, `CL`). **A likely meaning is a
guess, and refusing it is the whole point of the table.**

Measured: the 198 entries covered the enumerated census exactly — no unmapped
ticker and no dead entry — until `para:IGV` was born mid-stage and recorded as
`not_in_registered_mapping`. **It was not added.** Extending the table after a
census is how a universe gets fitted; a later amendment may add it.

Alternative rejected: fuzzy or prefix matching. It would have resolved
`GIGADEV` and `SKHX` alike, and there is no way to audit afterwards which
matches were right.

## ADR-027: The reference is the venue's own oracle, and the honesty clause is a first-class part of the design

**Date:** 2026-08-28 · **Status:** accepted · registrations/H5 Section 4, npl/h5/basis.py

H5 reads **no external equity price feed**: zero dollars, keyless endpoints,
one venue. Every reference is therefore the venue's own — `oraclePx`, with
`indexPx` as a registered fallback that measurement showed was never needed
(served on 151 of 151). `midPx`, `prevDayPx` and `impactPxs` are **registered
non-references**, because substituting a book field for an unserved oracle is
exactly how a basis becomes an artefact.

The consequence is not a caveat at the end of the document; it is the
design's boundary. A basis computed against a venue-internal reference
measures **the venue's bookkeeping, not a tradable gap**. The registration
states this three ways and pre-registers the expectation that a near-zero
basis is the likely measurement — so a small number cannot later be sold as
a surprise, and a large one cannot be sold as a discovery this data can
make. A VIABLE row authorizes exactly one thing: a registration in a
different repository, against an independent feed. It authorizes no capital,
and the closed-and-carried IBKR economics (40–100 bp whole-share round trips,
fractional orders refused at error 10243) mean no cross-venue pair is
registrable here even if the deviation were real.

The measurement supplied its own demonstration: **32 delisted instruments —
zero open interest, zero volume, no book — are still served an unbroken
hourly funding series.** Bookkeeping continues after the market stops.

## ADR-028: Every observation is tagged by underlying-market session, against a calendar written out by date

**Date:** 2026-08-28 · **Status:** accepted · registrations/H5 Section 5, npl/h5/calendar.py

A perpetual on a closed underlying has no reference market at all. Pooling a
Saturday snapshot with a Tuesday-morning one is the fastest way to
manufacture a basis that is really a stale reference, so **deviation is
characterized within each session tag separately** and every figure carries
its tag and its n.

Four tags, in `America/New_York`: `regular` (09:30 to the day's close),
`extended` (04:00–09:30 and close to 20:00), `closed_weekday`, `weekend`.
The NYSE full-closure and 13:00-close tables are **written out by date for
2024–2027 rather than derived**, so a rule change in a later year is an
amendment and not a silent recomputation, and a timestamp in an uncovered
year is a **loud refusal** rather than a default to "open". Sixteen fixtures
sit exactly on the boundaries — 09:30, 16:00, 13:00 on an early close, 20:00,
Saturday 00:00, Monday 00:00, and an EST/EDT crossing — because a fixture
comfortably inside its boundary lets a moved threshold pass unnoticed.

Alternative rejected: deriving the calendar from weekday arithmetic plus a
holiday library. It would have added a dependency to a zero-dependency
project and made the registered calendar unauditable at the point of use.

## ADR-029: The VIABLE bar is 54 bp, and it is arithmetic on the registered cost band

**Date:** 2026-08-28 · **Status:** accepted · registrations/H5 Section 6, npl/h5/outcome.py

The bar is not a number someone liked. HIP-3 builder markets default to
**double** the venue's native fees — 3 bp maker and 9 bp taker per side — so
a taker round trip is **18 bp central**, with the registered band at 6 and 36
(ADR-003, `CONFIG.hip3_round_trip_bp = (6.0, 18.0, 36.0)`). The floor is that
central figure; the VIABLE bar is `h5_viable_basis_multiple` × floor:

    floor  = hip3_round_trip_bp[1]      = 18 bp
    bar    = 3.0 x 18 bp                = 54 bp

Three times the cost floor, so a deviation that clears it is not merely
larger than the cost of crossing — it is large enough that a **third** of it
could be spent on execution and something would remain to investigate. The
multiple lives in config and the arithmetic is recomputed at every firing;
neither 18 nor 54 is written as a literal anywhere in the map.

Boundary conventions, fixed before data and each with a fixture sitting
exactly on it: VIABLE is **strictly greater** than 54 (exactly 54.00 is
INDETERMINATE); CLOSED needs **strictly under** 18 in *every* tag (exactly
18.00 anywhere is not CLOSED); funding clears at **at least** one half (10 of
20 passes, 9 of 20 closes); the instrument bar is **at least** 20.

## ADR-030: A delisted instrument is excluded on three fields agreeing, not on a flag

**Date:** 2026-08-28 · **Status:** accepted · registrations/H5 Amendment H5-2, npl/h5/listing.py

Section 2 as written admitted every resolved instrument, trading or not. A
delisted perpetual has **no market**: its mark is a frozen last value while
its oracle goes on updating, so the gap between them is the delisting. The
census measured what that costs: the delisted stratum's median absolute basis
is **30.5 bp with 45.6 percent over the 54 bp bar**, against **3.72 bp and
0.0 percent** for live instruments in the same snapshot. **Every observation
above the bar lived in dead markets.**

The exclusion is **conjunctive**: `isDelisted` true **and** `openInterest`
exactly zero **and** `dayNtlVlm` exactly zero. A one-flag rule trusts a single
field; three independent fields agreeing — plus the venue's own empty book —
is a measurement. Any other combination is `conflicting` and is reported
loudly, never resolved by the rule. Measured: 57 of 57 delisted instruments
satisfied all three, 0 of 94 live ones satisfied any, zero conflicting. An
**absent** field is never read as a zero.

The amendment was made with the census in hand, which is disclosed in full in
its own text. Its direction is the check: it makes VIABLE **strictly harder**
and deleted this entry's only route to it. The argument stands without the
numbers — a market with no participants cannot deviate — and would have been
in Section 2 had the omission been noticed.

## ADR-031: H5 writes only under data/h5/, reads no candle and no funding rate, and gates its retrospective read

**Date:** 2026-08-28 · **Status:** accepted · registrations/H5 Section 0, npl/h5/stores.py, npl/h5/gate.py

Three structural rules, each enforced rather than intended, because the
obvious implementation of "measure the basis" breaks all three.

**Writes.** Every H5 write goes through `npl.h5.stores.h5_store`, which
resolves the target and refuses anything outside `data/h5/`. The refusal is
**produced by a test against the real path** `data/controls/h2_pairs.jsonl`,
and an AST guard pins that no H5 module constructs a ledger or opens a file
in a write mode outside that one module. Reading is deliberately allowed and
routed through a read-only helper: the cohort ledgers must be read for the
quarantine to be honoured, and reading them is the mechanism, not a breach.

**Candles and funding rates.** A candle read blind carries `t`, `T` and a row
count, which is not a price; a candle read with a price violates standing
rule 7. So **no retrospective basis can come from `candleSnapshot`**, and that
consequence was registered before measurement rather than discovered after.
Funding is recorded as **service** — field presence, row counts, timestamps —
so the operator's first question is answered without reading a single rate.

**The retrospective gate.** The venue serves `premium` hourly, which is a
near-deterministic function of the funding rate: reading it across a
registered event's open outcome window would be a post-entry funding read
wearing a different field name. So the historical read alone is gated to
coins outside the generating sample, the fresh plan, and both legs of every
assigned H2 pair, and the gate is the **first statement of the fetch
function** — structurally in the path, not left to the caller — with an AST
pin on that position. It cost the entry its retrospective sample (27 of 151
eligible, 39 usable observations) and was kept anyway: a gate relaxed after
it turns out to be expensive is not a gate.


## ADR-032: A bounded network wait before each collector pass

Four watcher sweeps between 2026-08-31T21:23Z and 2026-09-02T09:10Z polled
zero dexs and recorded `source_failed` on both `meta:main` and `perpDexs`
with a null http_status, meaning the request never reached the wire. Every
one sat at a boot or resume boundary (21:23Z, 06:04Z, 01:52Z, 09:10Z) and
the sweep that followed each recovered cleanly at 11 dexs polled. A direct
probe of the endpoint during the investigation returned http 200 in 0.15s,
so the venue was never the cause.

Both units already carried `After=network-online.target` and
`Wants=network-online.target`. That is close to a no-op here for two
reasons: `network-online.target` belongs to the system manager and a
`--user` unit ordering against it orders against the user manager's own
target, which nothing reaches; and the target is not re-evaluated after a
suspend, which is the other half of the observed boundary set.

Decided. `scripts/wait_for_net.sh` runs as `ExecStartPre` on both
`npl-watch.service` and `npl-daily.service`. It polls DNS for
`api.hyperliquid.xyz` every 3 seconds up to a 60 second deadline, then
proceeds either way.

Two properties are load-bearing and both are tested.

It charges nothing. Resolution only, never a venue request, so the
registered request ledger and its daily cap stay the single authority on
spend. A connectivity probe that charged the venue would have made the
ledger a partial record.

It never suppresses a real outage. On timeout it exits 0 and the pass runs
and records `source_failed` loudly, per the standing rule that a refusal is
loud and an absence is a recorded state. A wait that failed the unit would
have converted a recorded absence into a silent skip, which is the failure
this project is built to refuse. Verified by test: bogus host at a 6 second
deadline exits 0 and writes the timeout line to stderr for the journal.

What this does not do, stated so nobody reads it as more than it is. It
changes no registered design: not the universe, not the entry anchor, not
eligibility, not coverage bars, not any outcome path. The H2 reader stays
dark and all three latches stay absent. It is infrastructure hardening on a
collector, recorded as an ADR rather than a registration amendment for that
reason.

The honest cost-benefit. Data integrity was not at risk: the guard behaved
correctly at every failure, the next hourly sweep recovered, the daily pass
catches up regardless, and forward listing dates are cross-checked against
first-candle and funding evidence rather than resting on sighting time. Two
narrow gains justify the change. A birth in the final hour of a UTC day
whose sighting slipped past midnight could have shifted an inferred date by
a day. And four benign markers in the log make a genuine venue outage
harder to see, which is the more valuable of the two.

Live units and `ops/systemd/` copies verified identical after the edit.
`daemon-reload` clean, both timers still active, next fire times unchanged.
