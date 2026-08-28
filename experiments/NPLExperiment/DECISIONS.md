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
