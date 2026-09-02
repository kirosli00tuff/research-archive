# progress.md — PMExperiment session log

Append-only. One entry per sub-stage. Every entry states the ETA given before
the task was armed and the actual elapsed against it, per standing rule 2.
Every figure travels with its n in the same sentence, per standing rule 13.

---

## Entry 2.1 — addendum, recorded after the push

Task 4 actual, closing the open cell in Entry 2's table: **~6 min against
the 20-min ETA** (report, ADRs, suite green at 34 tests, commit `98ce2d4`,
pushed to the private `origin/main` at 07:53:11Z). Appended as a new record,
not an edit, per the append-only rule.

---

## Entry 2 — Stage A: access, the permitted subset, and the power gate — 2026-08-29

**Verdict, one sentence: Stage A ends PENDING_ACCESS — the data is
technically open without an account but the recorded terms do not sanction
keyless systematic retrieval or AI-mediated analysis, the governing API
Developer Agreement is unreadable by automated means, and the keyless
settled history reaches only to spring 2024 — so the power gate never fired
and the calibration question stays open, unmeasured.**

### ETA against actual, per task (standing rule 2)

| task | ETA, with its basis | actual |
|---|---|---|
| 0 — register Section 0 | 30 min, from NPD B.2 (55 stated, 41 actual) and the scaffold session as comparable document-heavy work | **14 min** (07:23:51Z → 07:37:33Z) |
| 1 — measure access | probe batch ~2 min from first-request latency (127.6 ms); report phase 25 min from Task 0's measured 14 min | probe + terms retrieval **~11 min** (terms hunting dominated: bot challenges, an archive fetch, one 2-min headless timeout); report phase **~9 min** |
| 2 — register the filter | never armed | — the access gate closed the stage first, as registered |
| 3 — fire the power gate | never armed | — same |
| 4 — report and push | 20 min, from Task 0's document half | recorded at push in this entry's commit |

### The access table (full figures and dates in docs/ACCESS.md)

| quantity | reading, 2026-08-29 |
|---|---|
| keyless reachability | HTTP 200, 99.9–213.8 ms, n = 11 API requests |
| outcome exposure | `result` beside final prices on settled records, 2 of 5 permitted records inspected |
| settled-history depth | earliest retrievable close between 2024-01-01 and 2024-05-31, n = 6 bracketing probes; the published 2021→2025 span is not keylessly reproducible |
| candlesticks | work on a fresh traded market (1 candle); 0 daily candles on the one ≥ 30-day-old market tested — ambiguous, counted ambiguous |
| rate limit | documented claim 200 reads/s (Basic); measurement withheld under standing rule 12, ADR-007 |
| terms | Data Terms of Use prohibit systematic retrieval and AI-mediated use without written authorization; Developer Agreement HTTP 429 bot-challenged to every automated read; robots.txt: API host 404, Website 429 |

### Subset counts and the price-bucket distribution

None exist. The permitted-subset filter was never registered and no bucket
was ever built, because the access gate fired first — reported as absent,
not as zero (standing rule 5). Tasks 2 and 3 are the registered casualties
of the PENDING_ACCESS row, not omissions.

### What held

Section 0 (outcome map, effect band 0.02–0.08 cited to source, cost model
with C(0.95) = 0.0785, outcome blindness) was committed at 07:37:33Z, before
the first request at ~07:44Z. The probe budget was 13 requests, single-shot,
spaced, no retries, no pagination. Guards were verified by mutation, and the
first mutation run caught a real weakness — the bar-enforcement check
accepted a docstring mention; it now requires the `registry.` reference
(test_guards.py records this in its docstring).

**On Stage B:** stated if and only if the gate cleared. It did not clear; no
Stage B is stated. Reopening conditions: REGISTRATION.md Section 15.1.

---

## Entry 0 — Stage A operator prompt, logged verbatim before any other work

**Logged 2026-08-29T07:23:51Z, per standing rule 1. Work follows in later
entries; nothing below this line in this entry is work.**

> BEGIN PROMPT - NEW REPO: PMExperiment, STAGE A — ACCESS, THE PERMITTED
> SUBSET, AND THE POWER GATE
>
> Create a repository at ~/Documents/GitHub/PMExperiment. Read, read-only,
> InsiderExperiment's REGISTRATION.md Sections 0 and 0.1, NPDExperiment's
> closure, solattn's REGISTRATION.md and CLAUDE.md, and MLCryptoEngine's
> CLAUDE.md, as the source of the standing practices this repo inherits. Modify
> none of them. Give a measured ETA per task and write that requirement into
> CLAUDE.md as a standing rule.
>
> What this project is, stated permanently in CLAUDE.md and README from the
> first commit. A measurement-only test of whether prediction-market prices are
> mis-calibrated by enough to survive the costs a Canadian retail participant
> actually pays. It never trades, holds no account, places no order, and has no
> stage in which one is planned. Kalshi market data is public and is read
> without an account. A documented negative is a valid and expected outcome,
> and BLOCKED on power is a cheap and legitimate answer.
>
> Why the power gate exists, quoted into Section 0.1 from the record rather
> than from this prompt. NPDExperiment closed at unresolved-at-achievable-power
> with a realized minimum detectable contrast of 0.0512 against an effect band
> of 0.01 to 0.05, discovered after 415 days in the same session that read the
> result. InsiderExperiment then registered its gate in advance and fired
> BLOCKED at 49.35 bp before spending. This repo follows Insider, not NPD.
>
> Task 0: register Section 0 before any request. First commit.
>
> Register the outcome map: GO, DEGRADED and BLOCKED conditions, each defined
> on counts and dispersion only, never on a first moment relating price to
> outcome. Register the minimum detectable effect computation and the effect
> band it will be judged against, citing the published favourite-longshot
> magnitudes you are testing for. Register the cost model in full before
> measuring anything: two cents per contract per side, the FX schedule, and a
> spread assumption stated as an assumption. Register that no calibration
> statistic is computed until the gate fires.
>
> Task 1: measure access rather than trusting documentation.
>
> Establish, by probing: whether Kalshi market data and settlement history are
> reachable without an account, the rate limits as measured, how far back
> resolved contracts are retrievable, whether resolution outcomes are exposed
> alongside final prices, and what the terms of service permit for automated
> reading from Canada. Report each with its measured figure and the date.
>
> If public data proves unreachable or too shallow, Section 0 reports on access
> rather than pretending to report on the hypothesis, exactly as ORBExperiment
> did, and the stage ends there as a valid outcome.
>
> Task 2: define the Canadian-permitted subset mechanically, before any
> outcome.
>
> From published CIRO and platform rules, register the filter: the three
> permitted categories, the 30-day minimum maturity, and any volume floor you
> choose, with the choice justified before it is applied. Report how many
> resolved contracts fall inside it and how many outside, so the filter's cost
> in sample is visible.
>
> Do not tune the filter to increase the sample. Register it, then report what
> it yields.
>
> Task 3: fire the power gate, without reading an outcome.
>
> Compute the minimum detectable effect from price-bucket counts and dispersion
> alone, for the permitted subset and for the unrestricted Kalshi universe
> separately, and judge both against the registered effect band. Report the
> price distribution across buckets, since the whole question is whether
> extreme-priced contracts exist inside the Canadian filter in usable numbers.
>
> State the verdict in one sentence. If the permitted subset is BLOCKED while
> the unrestricted universe is not, that is itself the finding: the mispricing
> may be real and simply not reachable from Canada, and the note should say so
> plainly rather than treating it as a failure.
>
> Task 4: report. Append a dated progress entry with the access table, the
> subset counts, the price-bucket distribution and the gate verdict. Append
> ADRs for the access findings and the registered filter. State what Stage B
> would be if and only if the gate cleared, without designing it. Run make
> lint, make typecheck, make test. Initialize git, commit, push to a private
> remote.
>
> END PROMPT

One deviation already visible at logging time: the repository, its remote, and
two commits exist, created by the scaffold session recorded in Entry 1, so
"create a repository" and "initialize git" are already satisfied rather than
performed here. The inherited sources named above were read, read-only, before
this entry was written; none was modified.

---

## Entry 1 — scaffold, written before any operator stage prompt existed

**Recorded 2026-08-29.** This repository was scaffolded directly rather than
from a stage prompt, so standing rule 1 has no prompt to reproduce for this
entry. **Entry 0 is reserved** and is filled by the first operator stage prompt,
logged verbatim before any other work, ahead of the first request.

**ETA:** none stated — the scaffold was not an armed task. **Actual:** one
session, no measurement performed.

**State at this entry.** No request has been sent to any endpoint. No contract,
price, resolution, ledger row or coverage figure exists. `REGISTRATION.md`
carries a `NOT YET REGISTERED` banner and an empty Section 0, which must be
committed before the first request goes out.

**What is in place.** `README.md` leading with scope and the power precedent.
`CLAUDE.md` with sixteen standing rules. `REGISTRATION.md` as a scaffold.
`HYPOTHESES.md` with H1 open and unregistered, three candidates closed before
opening, and H2 and H3 parked. `DECISIONS.md` with ADR-001 through ADR-004.
`report.md` empty of claims. Package and test skeletons, MIT license,
`.gitignore` excluding `.env` and session files.

`.env.example` is empty on purpose: Stage A needs no credential, because Kalshi
market data and settlement history are public and read without an account.

**Nine honesty tests, verified by mutation** (standing rule 14): altering the
no-first-moment rule in `CLAUDE.md` fails the suite; restoring it passes. Their
reader folds whitespace, because a hard-wrapped needle failed a literal match on
text that was genuinely present — the fix belongs in the matcher, not in
rewording a document to satisfy it.

**Next:** Stage A Task 0 logs the operator prompt as Entry 0, then writes and
commits Section 0 — the outcome map, the permitted-subset filter, the cost model
and the effect band — before any request goes out.

---

## Entry 3 — amendments 1 to 3: venue, fee band, scope — 2026-08-30

**ETA:** none stated; document work, no measurement armed. **Actual:** one
session, zero requests sent, zero dollars.

**No statistic relating a price to an outcome exists.** Section 15 remains
empty. These amendments were written before any measurement, which is the only
time they can honestly be written.

**Amendment 1.** The measurement venue moves to Polymarket, whose public read
endpoints need no key, authentication or wallet, with settlement on Polygon.
Kalshi's PENDING_ACCESS verdict of 2026-08-29 stands and is not re-litigated.
Transfer between venues is registered **UNTESTED**, on three grounds recorded in
the register, including this program's own MLCryptoEngine H2 at **AUC 0.501**.
The category mismatch is registered before measurement: Polymarket's documented
mispricing concentrates in politics and sports, which the Canadian-permitted
subset excludes.

**Amendment 2.** A fee-versus-edge band fires **before** the power gate. The
Canadian fee is flat at $0.02 per contract per side against a $1.00 payout, so
break-even requires the true probability to exceed the market price by **2.0
percentage points** held to resolution or **4.0** round trip, before spread and
FX. Three verdicts registered: BAND-EMPTY closes the tradeable question on cost,
BAND-NARROW records a split finding, BAND-OPEN passes a named region to the
power gate. Computed once, never recomputed after a result is seen.

**Amendment 3.** The terminal question now admits whether a tradeable edge
exists. **The repository still never trades**: no stage places an order, holds a
position, connects to a broker, or stores a trading credential, and the
`CLAUDE.md` scope guard is unaltered.

**Five new honesty tests, verified by mutation** (standing rule 14): weakening
the transfer guard to "Transfer is probably fine" fails the suite; restoring it
passes. 39 tests green, lint and typecheck clean.

**Open action, no assumed outcome:** the written-authorization request to Kalshi
is the only registered path that reopens measurement on a Canadian-tradeable
venue.

**Next:** compute the fee band. It reads published effect magnitudes and the fee
schedule only, so it needs no venue access and spends nothing.

---

## Entry 4 — Stage B operator prompt, logged verbatim before any other work

**Logged 2026-08-29T19:08Z, per standing rule 1. Work follows in later entries;
nothing below this line in this entry is work.**

> BEGIN PROMPT - PMEXPERIMENT STAGE B: THE FEE-VERSUS-EDGE BAND
>
> Read CLAUDE.md, REGISTRATION.md in full including Amendments 1 to 3,
> HYPOTHESES.md, DECISIONS.md, progress.md and report.md first. Per standing
> rule 1, log this prompt verbatim to progress.md before any other work. Per
> standing rule 2, state an ETA before arming each task and record actual
> against it.
>
> This stage reads no venue. No contract, no price, no order book, no
> resolution, from Polymarket, Kalshi or anywhere else. It computes arithmetic
> over inputs already registered. Sending a request would violate Section 4 and
> Section 10.
>
> Task 1: reconstruct the registered inputs from the registration, not from this
> prompt.
>
> Quote verbatim from REGISTRATION.md: the effect band from Section 3 with its
> citation, the cost model from Section 2 including the fee, the FX schedule and
> the spread assumption, and the three verdict definitions from Amendment 2. If
> any input this stage needs is absent or ambiguous, stop and report that rather
> than supplying it.
>
> Task 2: verify the effect band's units before computing anything with it. This
> is the stage's main intellectual risk.
>
> The registered band is expressed as a magnitude. Establish from the cited
> source whether it is percentage points of probability mispricing or percent
> realized return, because they are not interchangeable and the fee is
> denominated in the first. A 60 percent realized loss on a five cent contract
> is three cents of mispricing, not sixty. Getting this backwards inflates or
> destroys the band by an order of magnitude.
>
> Report which unit the source uses, how you established it, and the conversion
> if one is needed. If the source is ambiguous on the point, say so and carry
> both readings through Task 3 as separate columns rather than choosing.
>
> Task 3: resolve the FX treatment honestly, and register the choice.
>
> The schedule charges 1.5 percent under $10,000 CAD. Whether that is a
> per-contract cost or an amortized funding cost changes the answer materially:
> 1.5 percent on a 90 cent contract is 1.35 cents against an edge measured in
> single cents, but a single conversion spread across many contracts is close to
> negligible per contract.
>
> Decide which model applies, state the reasoning, and register it as an
> amendment before using it. Report the band under both treatments so the choice
> is visible rather than buried. Name the direction each treatment biases the
> verdict.
>
> Task 4: compute the band across price buckets.
>
> For each price bucket across the full range, compute the minimum underpricing
> required to break even, net of fee, spread and FX, for both exit routes: held
> to resolution at one fee, and exited before resolution at two. Compare each
> against the registered effect band.
>
> Report it as a table with the required underpricing beside the registered
> effect magnitude at that bucket, so a reader can see where they cross. State
> the crossing points explicitly rather than leaving them to be inferred from the
> table.
>
> Then apply the Canadian filter as a second pass: which surviving buckets, if
> any, fall inside the permitted categories of economic indicators, financial
> markets and climate at a 30-day minimum maturity. Report the two passes
> separately.
>
> Task 5: fire the verdict, and stop.
>
> State BAND-EMPTY, BAND-NARROW or BAND-OPEN in one sentence at the top of the
> entry, against the definitions quoted in Task 1 and without adjusting them.
>
> If BAND-EMPTY, the tradeable question closes on cost. Record it in
> HYPOTHESES.md with the figures that closed it, and state that the calibration
> work may continue only as a labelled phenomenon study.
>
> If BAND-NARROW or BAND-OPEN, name the surviving region precisely and record
> that the power gate fires next over that region and no other. Do not design the
> power gate here.
>
> Do not propose a different fee assumption, a different effect band, or a
> different venue to rescue an empty band. If the arithmetic closes it, that is
> the finding.
>
> Task 6: report. Append the entry with the unit determination, the FX treatment
> and its amendment, the band table, both passes and the verdict. Append ADRs for
> the unit finding and the FX treatment. Extend the honesty tests to pin the
> verdict and its figures. Update report.md with a section written for the moment
> it landed. Run make lint, make typecheck, make test. Commit at each task
> boundary and push.
>
> END PROMPT

**ETAs stated before arming, per standing rule 2**, each derived from measured
work in Entry 2 and Entry 2.1 rather than guessed: Task 0 **4 min** (Entry 2's
Task 0 registered Section 0 in a measured 14 min; this is roughly a fifth of
that document volume), Task 1 **7 min** (Entry 2 Task 1's report phase measured
9 min, less its probe half), Task 2 **10 min**, Task 3 **10 min**, Task 4
**18 min** (Entry 2.1 measured 6 min for report + ADRs + a 34-test suite + push;
this adds a module and its tests), Task 5 **6 min**, Task 6 **20 min** (Entry
2.1's Task 4 measured 6 min for the same shape, plus mutation verification of
the new guards). **Total 75 min.** Actuals land in Entry 5.

**One deviation visible at logging time:** the six binding documents named in
the prompt were read, read-only, before this entry was written, exactly as
Entry 0 recorded for Stage A. No other work has been done and no request has
been sent to any endpoint.

---

## Entry 5 — Stage B: the fee-versus-edge band — 2026-08-29

**Verdict, one sentence: the band gate fires BAND-OPEN — at entry prices
91–99c held to resolution an effect at the top of the registered band would
clear the registered cost, needing 5.85 probability points against a band top
of 8.00, so the tradeable question is not closed on cost — but the surviving
region is the top 2.15 points of a 6-point band, no cited source places a
magnitude there at that bucket, and the band's top is set by the one source
whose n the registration never recorded.**

**Zero requests sent. Zero dollars. No contract, price, order book or
resolution was read from any venue**, so Sections 4 and 10 stand intact.

### ETA against actual, per task (standing rule 2)

Tasks 1, 2 and 4 were **not separable in execution**: the band arithmetic is
simultaneously the reconstruction of the registered inputs, the unit check and
the table. They are reported against the commit boundaries actually made,
rather than split after the fact into the shape the ETA assumed.

| task | ETA, with its basis | actual |
|---|---|---|
| 0 — log the prompt verbatim | 4 min, from Entry 2 Task 0's measured 14 min scaled by document volume | **1.7 min** (19:05:53Z → 19:07:37Z, `e2d8f10`) |
| 1, 2, 4 — inputs, unit, band table | 35 min combined (7 + 10 + 18) | **13.7 min** combined: arithmetic and guards 8.3 min (`9b4bd4f`), documents 5.4 min (`34307b6`) |
| 3 — FX treatment and its amendment | 10 min, from Entry 3's three-amendment session | **1.4 min** (`4d75f66`) |
| 5 — fire the verdict | 6 min | **1.4 min** (`32dc10a`) |
| 6 — tests, mutation, report, push | 20 min, from Entry 2.1's measured 6 min plus mutation runs | recorded at push in this entry's commit |

**The ETAs ran long by roughly a factor of two.** The named cause: every ETA
was derived from Stage A's document-writing rate, and Stage B's document half
was smaller than Stage A's while its arithmetic half was already pinned in
tests before the prose was written. Recorded so the next stage's estimates
start from Stage B's rate rather than Stage A's.

### The unit determination (Task 2), and why it was the stage's real risk

**The band is in absolute probability points, not percent realized return.**
Established by reconstructing each cited magnitude both ways and checking it
against the numbers the registration itself prints, using `return = gap ÷
price`. Bürgi's 5c contract winning 3 % is a 2-point gap *and* a −40 % return;
his 95c contract winning 98 % is a 3-point gap *and* a +3.16 % return; both
reproduce the record exactly, n = 313,972 contract prices on 46,282 contracts
across 12,403 events. Krause's −0.077 settles it alone: read as a probability
difference it implies a mean bucket price of 0.117, coherent for a "below 30c"
bucket, while read as a return it implies 0.043 and would make the figure
Section 3 calls "the largest single-category published figure" the smallest of
the three. The fee is denominated identically, so no conversion was needed.
ADR-009.

**The half of that finding that changed the answer was direction.** At longshot
prices the documented miscalibration is *over*pricing, so a longshot buyer has
a negative edge while break-even needs *under*pricing; the exploitable
expression is always the complement. Restated that way every registered
magnitude sits at a **high** entry price — 0.883 to 0.95 — which is exactly
where a price-proportional FX charge is largest.

### The FX treatment (Task 3), registered as Amendment 4 before use

Both candidate models are one formula with a turnover: `FX(p) = 0.03·p/k`.
Section 2's participant is exactly k = 1. **k = 1 binds; k > 1 is reported
beside it and never substituted**, because Section 2 forbids revising a cost
component in the direction that helps H1, and because k = 1 biases toward
BAND-EMPTY so a surviving band cannot be its artifact. **The verdict is
invariant to the choice**, which is the best position a contested assumption
can hold. ADR-010.

Recorded rather than supplied: the prompt's "$10,000 CAD" FX tier is
**registered nowhere** and was not used; Section 2 registers a flat 1.5 % per
direction with no size break.

### The band (Task 4, Pass 1) — full table in `docs/BAND.md`

Required underpricing in probability points, held to resolution (R_H, one fee)
and exited before resolution (R_X, two):

| bucket | mid p | R_H k=1 | R_X k=1 | R_H k→∞ | registered magnitude |
|---|---|---|---|---|---|
| 1–10c | 0.055 | 0.0316 | 0.0517 | 0.0300 | 0.02–0.08, but *overpriced* — a buy has the wrong sign |
| 41–50c | 0.455 | 0.0437 | 0.0636 | 0.0300 | not registered |
| 81–90c | 0.855 | 0.0556 | 0.0756 | 0.0300 | not registered — Krause's complement lands here at 0.883 |
| 91–99c | 0.950 | **0.0585** | **0.0785** | 0.0300 | 0.02–0.08; cited here: Bürgi's **0.020** and **0.030** |

**The crossing points, stated rather than inferred: there are none inside the
tradeable range.** R_H(p) = 0.03 + 0.03p meets the band bottom at p = −0.3333
and the band top at p = +1.6667; R_X(p) = 0.05 + 0.03p meets them at −1.0000
and at exactly +1.0000, a price that cannot be traded. **The registered cost
floor runs entirely inside the registered effect band at every price** — which
is what Section 2 predicted before any measurement, confirmed here to 0.0015.

**Two figures carry the stage.** The fee and half-spread alone total **0.0300**
before any FX, against a band bottom of **0.0200**: no FX treatment, no venue
price and no exit route reaches the bottom of the band. And at the FX-free
limit the held route requires exactly 0.0300 while Bürgi's favourite-tail gap
is exactly 0.0300 — a dead heat at the one bucket where a magnitude is cited.

Both quantifier readings of Amendment 2 are reported: existential (registered,
per the amendment's own "could survive") gives 10/10 buckets surviving on both
routes at every k; strict gives 0/10 at every k. The existential reading is the
registered one and is the one used.

### The Canadian filter (Task 4, Pass 2), reported separately

**The filter's axes are category, maturity and volume; price is not one of
them**, so no price bucket is excluded by its construction. What it can do is
leave a bucket empty of contracts — a **count** this stage may not read, and
one Section 0.4 assigns to the power gate in as many words. Two registered
inputs point toward a populated region (Krause's 7.7 points is inside a
permitted economic-indicator series; Page-Clemen puts the 30-day rule where the
bias is larger), two point against (the CPI companion finds no classic bias at
n = 95 contracts over 12 months; Amendment 1 registers that Polymarket's
mispricing concentrates in the excluded categories, as a risk not a
measurement), and one is **absent**: Section 1's volume floor was never
registered because Stage A Task 2 never armed, so BAND-NARROW's "below usable
volume" clause could not be evaluated at all.

### The verdict (Task 5)

**BAND-OPEN**, against Amendment 2's definitions unadjusted. Not BAND-EMPTY,
because the band exceeds the requirement at 10 of 10 buckets under every
treatment. Not BAND-NARROW, because its category clause is contradicted by
Krause's permitted-category attribution and its volume clause cannot be
evaluated. **The surviving region: entry prices 91–99c, held to resolution,
either side of the book, above 5.85 points at k = 1.** The 1–10c half is out on
sign, the eight non-tail deciles are out because no magnitude is registered
there, and the round-trip route is out because its 0.0015 margin at 95c is
thinner than the 0.00195 by which Section 2's FX base understates cost.

**BAND-OPEN is not evidence that an edge exists.** It records that cost alone
does not close the question. Amendment 3's phenomenon-study route is not
triggered; it applies only on BAND-EMPTY.

### What held

`pmexperiment/band.py` was written against `tests/test_band.py`, which existed
first and failed on import before the module did. Its load-bearing cross-check
is that the round-trip route at k = 1 reproduces `power.cost_floor` exactly and
lands on Section 11's stated C(0.95) = 0.0785 and C(0.05) = 0.0515 — a band
module that could not reproduce the registered floor would be computing
something unregistered. BAND-NARROW and BAND-OPEN are deliberately **not**
derived in code, because they turn on a count this stage may not read, and
encoding that judgement as arithmetic would dress it up as a measurement.

**Nine new honesty tests, five verified by mutation** (standing rule 14): the
suite fails when the no-edge-claimed sentence is weakened to "BAND-OPEN shows a
tradeable edge exists", when the missing-n disclosure is softened, when the FX
amendment is flipped to k = 12, when the band gate references an outcome field,
and when the registered turnover loses its enforcement site. All five restore
green. **63 tests, lint and typecheck clean.**

### Recorded, not repaired

DECISIONS.md already carried **two ADR-006 and two ADR-007 entries** from the
2026-08-29 and 2026-08-30 sessions. Renumbering a committed ADR would silently
break `Makefile:24` and `docs/ACCESS.md:76`, which cite the earlier pair, so the
collision is written down with the instruction to cite an ambiguous number with
its date. Numbering continued at ADR-009. Separately,
`registry.FX_TURNOVER_REGISTERED` was committed one commit *before* the
Amendment 4 text it cites; both sit inside the same task and no verdict fired
between them, but the lag is recorded rather than rebased away.

**Next:** the power gate, over 91–99c held to resolution and no other region.
It was not designed here. It still needs a venue whose terms permit the read —
Kalshi remains PENDING_ACCESS and the written-authorization request remains an
open action with no assumed outcome.

---

## Entry 5.1 — addendum, recorded after the push

Task 6 actual, closing the open cell in Entry 5's table: **4.6 min against the
20-min ETA** (report, Entry 5, nine honesty tests, five mutation runs, suite
green at 63 tests, commit `ebdc116`, pushed to the private `origin/main` at
19:28:45Z). Appended as a new record, not an edit, per the append-only rule.

**Stage B total: 22.9 min against a 75-min stated ETA** (19:05:53Z →
19:28:45Z), overrun by a factor of 3.3 in the safe direction. The cause named
in Entry 5 holds across every task, so the next stage should estimate
document-and-arithmetic work from **Stage B's** measured rate rather than
Stage A's: no task here exceeded its ETA, and the largest single block — the
band arithmetic with its tests and guards — took 8.3 min.

---

## Entry 6 — Stage C operator prompt, logged verbatim before any other work

**Logged 2026-08-29T19:32Z, per standing rule 1. Work follows in later entries;
nothing below this line in this entry is work.**

> BEGIN PROMPT - PMEXPERIMENT STAGE C: THE POWER GATE OVER 91-99c
>
> Read CLAUDE.md, REGISTRATION.md in full including Amendments 1 to 4,
> HYPOTHESES.md, DECISIONS.md, progress.md, report.md and docs/BAND.md first.
> Per standing rule 1, log this prompt verbatim to progress.md before any other
> work. Per standing rule 2, state an ETA before arming each task and record
> actual against it, and note that Entry 5 found Stage A's rate overestimated
> Stage B by roughly a factor of two.
>
> Scope, fixed by Stage B and not reopenable here. The gate fires over entry
> prices 91 to 99 cents, held to resolution, either side of the book, and no
> other region. The 1 to 10 cent half is out on sign, the eight non-tail deciles
> are out because no magnitude is registered there, and the round-trip route is
> out on a margin thinner than the FX base understates cost. Do not widen the
> region to improve the count.
>
> Task 1: register Section 1's missing volume floor before enumerating anything.
>
> Stage A Task 2 never armed, so the floor was never registered, and Entry 5
> records that this is why BAND-NARROW's volume clause could not be evaluated.
> Register it now, justified before it is applied, per standing rule 9. State
> what it costs in sample as a first-class output rather than choosing it to
> preserve one.
>
> Task 2: enumerate the Polymarket universe, reading no outcome.
>
> Public read endpoints require no key, no authentication and no wallet. Measure
> the access properties rather than trusting them: reachability, rate limits, and
> how deep resolved history goes. Record robots.txt and the published terms
> before any repeated fetch, per standing rule 12, and report what they permit.
> If the terms do not sanction this read, stop and report on access, as Stage A
> did for Kalshi.
>
> Enumerate resolved contracts and record, per contract, the fields the gate
> needs and nothing more: identifier, category, entry-price bucket, and whether a
> resolution exists. Do not read the resolution value. Section 4 and Section 10
> stand, and the gate reads bucket counts and dispersion only.
>
> Task 3: fire the gate.
>
> Compute the minimum detectable effect over the 91 to 99 cent region from bucket
> counts and dispersion alone, and judge it against the registered effect band
> and against the 5.85 probability points the band requires at k equals 1.
>
> Report the MDE beside the requirement in the same sentence, with its n, per
> standing rule 13. State GO, DEGRADED or BLOCKED against Section 0.2's
> registered conditions without adjusting them.
>
> Then report the same computation restricted to the Canadian-permitted
> categories of economic indicators, financial markets and climate at a 30-day
> minimum maturity, as a separate pass. Amendment 1 registered in advance that
> Polymarket's mispricing concentrates in politics and sports, which this filter
> excludes, so a split verdict is expected and is a legitimate finding rather
> than a failure.
>
> Task 4: state what the verdict does and does not license.
>
> A GO on Polymarket licenses a calibration measurement on Polymarket. It
> licenses nothing about Kalshi, because H1t transfer is registered UNTESTED on
> three grounds including MLCryptoEngine's H2 at AUC 0.501. Say so explicitly in
> the entry, and do not let a Polymarket GO be written anywhere as evidence about
> a Canadian-tradeable venue.
>
> Task 5: report. Append the entry with the registered floor and its sample cost,
> the measured access table, the gate verdict on both passes, and the transfer
> statement. Append ADRs for the volume floor and the access findings. Extend the
> honesty tests to pin the verdict, its figures and the transfer statement,
> verified by mutation. Update report.md with a section written for the moment it
> landed. Note the ADR numbering collision Entry 5 recorded and continue past it
> rather than renumbering. Run make lint, make typecheck, make test. Commit at
> each task boundary and push.
>
> END PROMPT

**ETAs stated before arming, per standing rule 2.** The prompt directs that
Entry 5's calibration finding be carried: Stage A's rate overestimated Stage B
by roughly a factor of two per task, and Entry 5.1 measured the whole stage at
22.9 min against 75 stated. These ETAs therefore derive from **Stage B's**
measured rate, not Stage A's.

| task | ETA | basis (measured) |
|---|---|---|
| 0 — log the prompt | 2 min | Stage B Task 0 measured **1.7 min** on a prompt of comparable length |
| 1 — register the volume floor | 8 min | Stage B's Amendment 4 measured **1.4 min**; this needs its justification researched first |
| 2a — access, terms, robots.txt | 12 min | Stage A's probe-and-terms phase measured **11 min**, and terms hunting dominated it |
| 2b — enumeration | **not yet stated** | cannot be derived honestly before 2a measures request latency and history depth. Stated before 2b is armed, from the probe, exactly as Entry 2 derived its probe ETA from a measured 127.6 ms |
| 3 — fire the gate | 10 min | Stage B's band arithmetic with tests and guards measured **8.3 min** |
| 4 — the transfer statement | 3 min | a short document block at Stage B's measured rate |
| 5 — report, ADRs, tests, push | 15 min | Stage B's Task 6 measured **4.6 min**; this stage has an access table and two gate passes to report |

**Total stated so far: 50 min plus enumeration.** Actuals land in Entry 7.

**Scope carried in from Stage B and not reopenable here**, per the prompt: the
gate fires over 91–99c held to resolution, either side of the book, and no
other region. **The region is not widened to improve a count.** If the count is
short, that is the finding, exactly as standing rule 9 requires for a filter.

**One thing recorded before any request goes out:** Stage A ended
PENDING_ACCESS on Kalshi's terms, not on its plumbing. The same test is applied
to Polymarket first, before any repeated fetch, and if the recorded terms do
not sanction this read the stage stops and reports on access.

---

## Entry 6.1 — correction to Entry 6's logging timestamp

**Entry 6 states it was logged at 2026-08-29T19:32Z. That figure is wrong.**
It was extrapolated from Entry 5.1's measured 19:28:45Z rather than read from
the clock. The measured logging time is **2026-08-30T03:31Z** — the session
resumed after a gap of roughly eight hours, and the calendar date had rolled
over.

Recorded as a new line rather than an edit, per the append-only rule. The
substantive point is standing rule 4's, and it applies to this repository's own
records as much as to a venue's documentation: **a timestamp inferred from a
previous timestamp is documented, not measured.** Every subsequent time in
Stage C is read from `date -u` at the moment it is recorded. Stage C's elapsed
figures in Entry 7 are computed from 03:31:03Z, the first measured Stage C
timestamp, not from the erroneous 19:32Z.

---

## Entry 7 — Stage C: the power gate over 91–99c — 2026-08-30

**Verdict, one sentence: PENDING_ACCESS — Polymarket's Terms of Use, effective
2026-08-11 and read in full before any repeated fetch, prohibit "data mining
tools, robots, crawlers, or similar data gathering and extraction tools" with no
entity-type qualification, and reach anyone "connecting via an API" and data
taken "directly or through an API, or any other means, including on-chain", so
the enumeration was never armed and the power gate did not fire over 91–99c or
anywhere else.**

**Zero market-data requests were sent to Polymarket. Zero contracts enumerated.
Zero dollars.** No price bucket was built, no dispersion computed, and no
statistic relating a price to an outcome exists in this repository.

### ETA against actual, per task (standing rule 2)

| task | ETA, with its basis | actual |
|---|---|---|
| 0 — log the prompt | 2 min, from Stage B Task 0's measured 1.7 min | **not separately measured**; its commit is the first measured Stage C timestamp, 03:31:03Z (`84f7b92`) |
| 1 — register the volume floor | 8 min | **3.0 min** (03:31:03Z → 03:34:00Z, `f789079`) |
| 2a — access, terms, robots.txt | 12 min, from Stage A's measured 11-min probe-and-terms phase | **6.9 min** (03:34:00Z → 03:40:52Z, `1b3124e`) |
| 2b — enumeration | **never stated, never armed** | the terms closed it before it could be armed |
| 3 — fire the gate | 10 min | **did not fire** — PENDING_ACCESS, exactly as Section 0.3's registered row prescribes |
| 4 — the transfer statement | 3 min | folded into this entry and report.md |
| 5 — report, ADRs, tests, push | 15 min | recorded at push in this entry's commit |

**Deferring 2b's ETA was the right call and is worth recording as practice.**
Standing rule 2 requires an ETA "derived from a probe or from comparable measured
work, never guessed". The enumeration had no comparable measured work, so its
estimate was deliberately withheld until the probe could supply one. The probe
instead closed the task. **No fictional estimate was ever recorded against work
that never ran** — which is what would have happened had the ETA been guessed at
arming time to fill the cell.

### Task 1 — the volume floor, registered and unexercised

Registered as **Amendment 5**: total traded volume **≥ $1,000** per contract,
imported verbatim from the benchmark study whose magnitudes set the registered
effect band (Section 3 records Bürgi, Deng and Whelan filtering to "total staked
≥ $1,000"). The point is provenance, not the number: **a floor chosen by someone
else, before this repository existed, cannot have been tuned to a sample this
repository had not yet seen**, which is the exact failure standing rule 9 exists
to prevent. ADR-011.

**Its cost in sample: not measured.** No enumeration ran, so the floor has never
been exercised on a real contract. Reported absent, never as zero (standing
rule 5). The benchmark's companion spread filter was deliberately **not** adopted,
because measuring it needs an order-book read this stage does not perform, and a
filter whose sample cost cannot be measured is worse than no filter.

### Task 2 — the access table (full evidence in `docs/ACCESS.md`)

| quantity | reading, 2026-08-30 |
|---|---|
| `robots.txt`, polymarket.com | **HTTP 200, 35.7 ms**, 73 bytes: `User-agent: *`, a sitemap line, **no `Disallow` of any kind** |
| `robots.txt`, gamma-api / clob / data-api | **404** in 280.1 / 201.4 / 220.9 ms — no crawl directives on any API host |
| Terms of Use | read **in full**, 59,617 bytes, effective **2026-08-11**, Adventure One QSS, Inc. |
| the deciding clause | prohibits "data mining tools, robots, crawlers, or similar data gathering and extraction tools", **unconditional on entity type** |
| its scope | binding notice reaches "CONNECTING VIA AN API"; Data clause reaches data taken "directly or through an API, or any other means, **including on-chain**" |
| developer docs | rate limits and builder tiers published; occurrences of "terms of use" **0**, "license" **0**, "acceptable use" **0**, "public data" **0** |
| reachability, rate limits, history depth | **WITHHELD**, following ADR-007 — measuring would itself be the prohibited act |
| requests to Polymarket hosts | **7**, all single-shot: 4 robots.txt, 2 page fetches, 1 rendered read. **None asked for a contract, price, order book or resolution.** |

**Reading the terms took work, and the shortcut would have produced a false
report.** `polymarket.com/tos` returns HTTP 200 but is client-rendered: its
217 KB body strips to **1,354 characters**, and its 129 KB Next.js payload
carries only an app shell under a route named `(embedded-docs)/tos`. Reporting
from either of the first two reads would have been reporting on a page shell
while believing it was the terms.

**The ordering clause of rule 12 did the work it was written to do.** Stage A
read **11** keyless Kalshi market requests before its terms position was
established and could withhold only the rate-limit burst afterwards. Stage C read
robots.txt and the terms **first** and sent **zero** market-data requests.

### What is recorded against the verdict, not only for it

robots.txt is **fully permissive** — a real contrast with Kalshi. The Data clause
that names on-chain access is **conditional on entity type** and does not bind a
retail researcher, so it is cited for scope and is **not** the ground. And the
strongest counterargument is real and is set out in full in Amendment 6: the
crawlers bullet forbids scraping from "the Site, any other Interface, or
Features", "Interface" means sites where the Terms are posted, and the Terms are
not posted at `gamma-api.polymarket.com`. Three reasons it is not taken, the
governing one being that **a venue may not be held to a looser reading than
another because its verdict would be more convenient.**

### Task 3 — the gate did not fire, on either pass

Both passes are **absent, not zero**. The unrestricted 91–99c pass and the
Canadian-permitted pass (economic indicators, financial markets, climate, at a
30-day minimum maturity) each require a bucket count and a dispersion, and
neither exists. No MDE was computed, so none is reported against the registered
band or against Stage B's 5.85-point requirement. Section 0.3's PENDING_ACCESS
row prescribes exactly this: Section 0 reports on access, not on the hypothesis,
and the stage ends there as a valid outcome.

**The scope fixed by Stage B was not widened.** The prompt forbade widening the
region to improve a count, and no count existed to be improved. Recorded because
the temptation is real and the record should show it was not taken.

### Task 4 — what a Polymarket verdict would and would not license

Stated whatever the verdict, as instructed, and it holds more sharply now that
there is no verdict to transfer: **a GO on Polymarket would have licensed a
calibration measurement on Polymarket and nothing whatever about Kalshi.** H1t
is registered **UNTESTED** on three grounds, including this program's own
MLCryptoEngine H2 measuring cross-venue transfer at **AUC 0.501**. **No
Polymarket figure exists, and none may ever be written anywhere as evidence
about a Canadian-tradeable venue.**

### The finding underneath the verdict

**Amendment 1's premise did not survive measurement, and it was this
repository's own.** It moved the venue here on the ground that Polymarket's data
is "public by construction rather than by permission" and that "standing rule 12
is satisfied here rather than circumvented" — citing no clause, no effective
date and no fetch date, where Stage A's Kalshi finding quoted its terms verbatim
with the date retrieved. It inferred **permission** from the absence of an
**authentication** requirement. Amendment 6 retracts the ground; Amendment 1
itself stands as the record of what was decided and why.

**ADR-012 converts it into a practice:** a claim about what a venue's terms
permit carries a quoted clause, the document's effective date and the date it
was fetched — or it is recorded as unmeasured and the stage proceeds as if
permission were absent. **Keyless is not permitted.** The register now carries
that mistake twice so it is not made a third time.

**What stands:** Stage B's BAND-OPEN over 91–99c held to resolution, computed
from registered constants, never dependent on venue access, and unaffected by
this verdict.

---

## Entry 7.1 — addendum: a fault in the mutation harness, and the Task 5 actual

**Six mutations, all six load-bearing** (standing rule 14). The suite fails when
Amendment 1's retraction is un-written to "That claim was well supported", when
the counterargument's conclusion is gutted, when its "recorded rather than
suppressed" framing is deleted, when the zero-request record is changed to
"sent several market-data requests", when the transfer statement becomes "and
plausibly something about Kalshi too", and when the unexercised floor's sample
cost is reported as zero instead of not measured. All six restore green at
**72 tests**.

**The first run reported one of those six as passing, and that was wrong.** The
counterargument mutation appeared not to break anything. It had not broken
anything because **it had never been applied**: `sed` is line-based, the target
sentence is hard-wrapped across two lines in the source, and the pattern
therefore matched nothing. The suite passed because the document was unchanged.

**A mutation that does not mutate is not evidence, and the harness now proves it
changed the file before it trusts the result** — `git diff --quiet` on the
target, with a no-op reported as a harness fault rather than counted as a guard
result. Re-run under that check with single-line patterns, both counterargument
mutations fail the suite as required.

This is the mirror image of the fault Entry 1 recorded, and the same root cause:
**the test reader folds whitespace and the mutation tool does not.** Entry 1's
version had a hard-wrapped needle failing a literal match on text that was
genuinely present, and the fix belonged in the reader. This version had a
hard-wrapped needle silently *not* removing text, and the fix belongs in the
harness. Recorded so the next session verifies the change rather than the
absence of a failure.

**Task 5 actual: ~6 min against the 15-min ETA** (03:40:52Z → the commit
carrying this entry). **Stage C total: ~17 min against 50 min stated**, with the
enumeration ETA never stated because the enumeration was never armed. Stage B's
rate, used as the basis here, again ran roughly two to three times long — but in
the safe direction, and the dominant reason this stage came in short is that the
terms closed it before its largest task began.

---

## Entry 8 — Stage D operator prompt, logged verbatim before any other work

**Logged 2026-08-30T04:18:14Z, read from `date -u` at the moment of recording
and not extrapolated from a previous timestamp (Entry 6.1). Per standing rule 1.
Work follows in later entries; nothing below this line in this entry is work.**

> BEGIN PROMPT - PMEXPERIMENT STAGE D: READ THREE CANDIDATE LICENSES, ENUMERATE NOTHING
>
> Read CLAUDE.md, REGISTRATION.md in full including Amendments 1 to 6, HYPOTHESES.md, DECISIONS.md including ADR-012, progress.md, report.md, docs/ACCESS.md and docs/BAND.md first. Per standing rule 1, log this prompt verbatim to progress.md before any other work. Per standing rule 2, state an ETA before arming each task and record actual against it; Entry 5 records that Stage A's rate overestimated Stage B by roughly a factor of two, and Entry 7's estimates ran high again.
>
> This stage enumerates nothing and measures no market. It reads licences and reports what they permit. No contract, price, order book, bucket count or dispersion may be produced by any task here. Sections 4 and 10 stand, and the Stage B region of 91 to 99 cents held to resolution is not reopened.
>
> Both venues are now closed on terms. Kalshi fired PENDING_ACCESS on 2026-08-29 and Polymarket on 2026-08-30, and Amendment 6 retracts the ground on which Amendment 1 moved the venue. ADR-012 governs every claim in this stage: a statement about what a source permits carries a quoted clause, the document's effective date, and the date it was fetched, or it is recorded as unmeasured and the stage proceeds as if permission were absent. Keyless is not permitted, and neither is open access, an academic framing, or a third party's convenience.
>
> Task 1: apply ADR-012 to itself before applying it to anything else.
>
> Write the check as a reusable procedure in pmexperiment/ with a test: a permission claim is admissible only when it carries clause text, an effective date and a fetch date. A claim missing any of the three is recorded as unmeasured. Verify by mutation that a claim stripped of its effective date fails.
>
> Note before fetching anything that a terms page may return HTTP 200 and be client-rendered, as Polymarket's did at 1,354 characters stripped from a 217 KB body. Establish that the document you read is the document, and report the byte counts you used to decide.
>
> Task 2: the three candidates, each read terms-first and reported independently.
>
> For each, report reachability, the governing document with its effective date, the clause bearing on this use quoted verbatim, and a verdict of PERMITTED, PROHIBITED or UNMEASURED. Do not fetch any data from any of them, only their licences.
>
> First, a Polymarket written-authorization request. Determine whether a contact route exists for research data access, as Kalshi's terms name written authorization. Report the route and the evidence for it, and draft nothing.
>
> Second, published academic datasets of prediction-market records. The large Polymarket trading corpus and any comparable released dataset. The question here is a licence question about the dataset, not about the venue, and the two are separate: a dataset released under a research licence may permit what the venue's terms do not. Establish the licence, its terms on derivative analysis and publication, and whether the records carry what the gate needs, which is entry price, category, maturity and resolution presence. Report depth and coverage from the dataset's own documentation rather than by inspecting records.
>
> Third, third-party data platforms carrying prediction-market tables, Dune among them. Their licensing position is their own and must be read as such. Report whether their terms permit programmatic query and republication of aggregates, and what tier that requires.
>
> Task 3: report what each candidate would and would not license, in the register's terms.
>
> For any candidate returning PERMITTED, state which universe it makes measurable, whether the Stage B region is reachable within it, and whether the Canadian-permitted filter of economic indicators, financial markets and climate at a 30-day minimum maturity can be applied to its records at all.
>
> Restate, whatever the outcome, that any measurement on Polymarket records licenses a statement about Polymarket and nothing about Kalshi, since H1t remains UNTESTED on three grounds including MLCryptoEngine's H2 at AUC 0.501. Pin that with a mutation-verified test.
>
> Task 4: state the honest position, including the possibility that there is none.
>
> If no candidate returns PERMITTED, say so plainly and record the consequence: the calibration question is unmeasurable at this house's standard until an authorization is granted, and the register carries BAND-OPEN as a cost finding with no calibration measurement behind it. That is a legitimate terminal state and should be written as one rather than as a setback.
>
> Do not propose a fourth venue to rescue an empty result, and do not soften ADR-012 to admit a candidate.
>
> Task 5: report. Append the entry with the three candidate tables, the admissibility procedure and its mutation result, and the honest position. Append ADRs for each candidate verdict. Extend the honesty tests to pin the verdicts and the transfer statement. Update report.md with a section written for the moment it landed. Continue ADR numbering past the recorded collision rather than renumbering. Run make lint, make typecheck, make test. Commit at each task boundary and push.
>
> END PROMPT

**ETAs stated before arming, per standing rule 2.** The prompt directs that the
overestimation findings be carried: Entry 5 measured Stage A's rate running
roughly two times long against Stage B, and Entry 7.1 measured Stage C at ~17 min
against 50 stated. These ETAs therefore derive from **Stage C's** measured rate
where Stage C did comparable work, and from Stage B's where it did not.

| task | ETA | basis (measured) |
|---|---|---|
| 0 — log the prompt | 2 min | Stage B Task 0 measured **1.7 min**; Stage C's Task 0 was not separately measured |
| 1 — the admissibility procedure, its test and its mutation | 8 min | Stage B's band arithmetic with tests and guards measured **8.3 min**; this module is smaller but carries a mutation run |
| 2 — three candidate licences, read terms-first | 20 min | Stage C's Task 2a measured **6.9 min** for one venue's robots.txt plus terms, including the client-rendered detour; three candidates at that rate is 20.7 min |
| 3 — what each would and would not license, plus the transfer test | 8 min | Stage B's Task 5 verdict measured **1.4 min**; Stage C's transfer statement was folded into its entry; this adds a mutation-verified test |
| 4 — the honest position | 5 min | a document block at Stage C's measured rate |
| 5 — report, three ADRs, honesty tests, push | 12 min | Stage C's Task 5 measured **~6 min** for report, ADRs and six mutation runs; this carries three candidate tables and three ADRs |

**Total stated: 55 min.** Actuals land in Entry 9.

**Scope carried in and not reopenable here**, per the prompt: this stage
enumerates nothing and measures no market. No contract, price, order book,
bucket count or dispersion may be produced by any task. The Stage B region of
91–99c held to resolution is not reopened, and no fourth venue is proposed to
rescue an empty result.

**One deviation visible at logging time:** the eight binding documents named in
the prompt were read, read-only, before this entry was written, exactly as
Entries 0, 4 and 6 recorded for Stages A, B and C. No other work has been done
and no request has been sent to any endpoint.

---

## Entry 9 — Stage D: three candidate licences, and there is none — 2026-08-30

**Verdict, one sentence: no candidate returns PERMITTED — a Polymarket
written-authorization route exists but every published address is scoped to
someone else, the leading academic dataset states CC BY 4.0 and documents all
four gate inputs over 1,201,580,990 rows yet fails ADR-012 on elements (1) and
(2) alike, and Dune's in-force Terms prohibit the tool class and gate
programmatic query behind a paid subscription — so the calibration question is
unmeasurable at this house's standard until an authorization is granted, and
that is a terminal state rather than a setback.**

**Zero contracts enumerated. Zero market-data requests. Zero dollars.** No
price bucket was built, no dispersion computed, and no statistic relating a
price to an outcome exists in this repository. Sections 4 and 10 stand intact,
and the Stage B region of 91–99c held to resolution was not reopened.

### ETA against actual, per task (standing rule 2)

| task | ETA, with its basis | actual |
|---|---|---|
| 0 — log the prompt | 2 min, from Stage B Task 0's measured 1.7 min | **1.45 min** (04:18:14Z → 04:19:41Z, `aa37749`) |
| 1 — the admissibility procedure, its test and its mutation | 8 min, from Stage B's measured 8.3 min for arithmetic with tests and guards | **~9 min** (04:19:41Z → 04:28:05Z `b67fc84`, plus five source-level mutation runs) |
| 2 — three candidate licences, read terms-first | 20 min, from Stage C Task 2a's measured 6.9 min for one venue, scaled by three | **~111 min** (04:31:37Z → 06:22:49Z `7b5a751`), plus **2.9 min** folding in the verification's corrections (`3204e5a`) |
| 3 — the transfer statement and its mutation-verified test | 8 min | **0.8 min** (06:25:40Z → 06:26:28Z, `80b9b9d`) |
| 4 — the honest position | 5 min | **0.8 min** (06:26:28Z → 06:27:18Z, `e6f6f3c`) |
| 5 — report, three ADRs, honesty tests, push | 12 min, from Stage C Task 5's measured ~6 min | recorded at push in this entry's commit |

**Total stated 55 min. Task 1 is the first task in this repository's history to
exceed its ETA, and Task 2 exceeded it by a factor of 5.5.** Both are recorded
rather than explained away, and the cause of the second is worth more than the
number.

**The named cause: the Task 2 ETA was scaled from work of a different kind, not
merely a different size.** Stage C's measured 6.9 minutes covered reading
`robots.txt` and one terms document on one host, where the question was already
known and the answer was in one place. Stage D read **thirty-odd documents
across three candidate families**, each requiring the real instrument to be
located behind a client-rendered shell, followed by an adversarial verification
pass that independently re-fetched and re-extracted every one of them —
**13 agents, ~2.1 M subagent tokens and 454 tool uses across two passes**, four
of which died on a session limit and had to be resumed. **Standing rule 2 asks
for an ETA derived from "comparable measured work", and this work was not
comparable.** An estimate scaled linearly from a different activity is a guess
wearing a measurement's clothes. This is Entry 5's lesson in a new form: there
the basis was the right activity at the wrong rate, here it was the wrong
activity entirely.

### Task 1 — ADR-012 applied to itself, and it does not flatter the record

`pmexperiment/admissibility.py` is ADR-012's sentence as a procedure: a claim
about what a source permits is admissible only when it carries **clause text, an
effective date and a fetch date**, and a claim missing any one of the three is
recorded **UNMEASURED**. It judges the *form* of a claim and never its merits —
a procedure that scored the persuasiveness of a clause would be dressing a
judgement up as a measurement.

**UNMEASURED is not a synonym for PROHIBITED**, and the code enforces the
distinction: the same operational consequence — proceed as if permission were
absent — and different epistemic content, one a measured refusal and the other
an absence. That distinction stopped being academic within the hour; see Task 2,
candidate 3.

**The mutation result: five source-level mutations, all five load-bearing.** The
suite fails when the effective-date check is stripped (the mutation Task 1 names
by hand), when the clause check is stripped, when the fetch-date check is
stripped, when `permits()` is allowed to read UNMEASURED as permission, and when
the client-rendered-shell detector is disabled. All five restore green at 89
tests. Each of the three elements is separately verified load-bearing at runtime
in `tests/test_guards.py`, blanked one at a time, because a procedure requiring
only two of three would pass a test that blanked all three at once.

**The harness failed first, and the failure was Entry 7.1's lesson in a new
form.** The first run reported HARNESS FAULT rather than a result: `git diff
--quiet` cannot see a change to a file git does not know about, and
`admissibility.py` was still untracked, so the change-proof mechanism gave a
false negative and `git checkout --` could not restore the mutated file. **The
harness refused to count the result, which is exactly what Entry 7.1 rebuilt it
to do.** Re-run against a committed baseline, all five mutations bite.

**Fired over this repository's own three claims, one comes out against the
record.** ADR-012 states that "Stage A's Kalshi finding met that bar." **It met
two elements of three.** `docs/ACCESS.md` quotes the Kalshi prohibitions
verbatim and records the fetch date of 2026-08-29, and **no tracked document
records an effective date for the Kalshi Data Terms of Use** — the only
effective date anywhere in this repository is Polymarket's 2026-08-11. The
licence read confirmed it at source: across the extracted PDF, `Effective` **0
occurrences**, `Last Updated` **0**. **This changes no verdict**, because
UNMEASURED and PROHIBITED both mean proceed as if permission were absent. What
it changes is the strength the record claims for itself, and it is recorded
because a procedure that only ever convicts other people's documents is not a
procedure.

Amendment 1's claim, judged by the rule its own failure produced, is
inadmissible on **all three** elements.

### Task 2 — the three candidates (full evidence in `docs/LICENCES.md`)

| # | candidate | verdict | governing document | effective date | the clause |
|---|---|---|---|---|---|
| 1 | Polymarket written-authorization request | **PROHIBITED** | POLYMARKET.COM TERMS OF USE | **2026-08-11**, `Effective as of` label on the masthead | "Use any data mining tools, robots, crawlers, or similar data gathering and extraction tools to scrape or otherwise remove data…" |
| 2 | published academic datasets | **UNMEASURED** | `TimeSeventeen/Polymarket-v1` card + CC BY 4.0 legal code | **ABSENT on both** | "Released under **CC-BY-4.0**. You may share and adapt the material for any purpose…" |
| 3 | third-party platforms (Dune) | **PROHIBITED** (Dune) / **UNMEASURED** (the rest) | Dune Terms of Service + SQL API Addendum | `Last updated on: June 3rd, 2026` (a last-updated label, substitution disclosed) | "bots, crawlers, scrapers, or other automated means" |

**Candidate 1. A route to ask exists; none of them is addressed to this asker.**
`data-licensing@polymarket.com` is the closest in subject matter and its own
sentence opens "If you or your clients are **Capital Markets Entities**". The
builder program's published upgrade path is gated on "Route orders through
Polymarket and demonstrate consistent usage" — a gate a repository that will
never trade cannot pass. The Terms' only Contact Us clause is scoped to
"questions, complaints, or claims concerning the Features", and the document
contains **no notices clause and no postal address**: `Notices` 0 occurrences,
`authorization` 0 occurrences across 58,830 characters. **Kalshi is the mirror
image — it names the ask and publishes no address at all**: `@` 0 occurrences,
`contact` 0, in a document that is itself undated. **Nothing was drafted, sent,
or requested, so nothing was refused.** PROHIBITED is the baseline absent
authorization, not a record that Polymarket declined.

**Candidate 2. The dataset question is genuinely separate from the venue
question, and it still fails.** `TimeSeventeen/Polymarket-v1` states CC BY 4.0
three times and documents all four gate inputs — `price` with `block_timestamp`,
`category`, `opens_at`/`close_at`, and `resolution_status`, which establishes
resolution **presence** separably from **value**, exactly as standing rule 8
requires — over **1,201,580,990 rows spanning 2022-11-21 to 2026-04-28**, read
from the card's published schema table with **no record inspected**. It fails
element (2) because neither the card nor the CC BY 4.0 legal code prints any
date, and element (1) because the read quoted the two clauses that grant and
passed over the two in the same document that limit: Section 1 caps Licensed
Rights to what "the Licensor has authority to license", and Section 5(a)
disclaims warranties of title and non-infringement.

**Candidate 3. The in-force instrument was read only because the verification
caught that it had not been.** The licence read declared Dune's current Terms
unreadable — "Cloudflare is fingerprinting the TLS/client, not the headers" —
quoted every clause from a superseded May 2025 archive, and published PROHIBITED
anyway. **Bare `curl` returns 403; the same `curl` with nothing added but a
browser `User-Agent` returns HTTP 200.** The in-force Terms were one header
away, and this session independently re-extracted them from the retained
172,750-byte body: the printed label and every load-bearing clause are present,
and `aggregat`, `derived`, `redistribut`, `republish`, `resell` are **zero
occurrences each** in the current text too.

**Publishing PROHIBITED from an unread instrument is Amendment 1's error with
the sign reversed** — Amendment 1 inferred *permission* from a document it never
read. **ADR-012 has no direction-of-travel exemption**, and Amendment 6's
convenience rule is symmetric: with a no-candidate outcome pre-blessed as
legitimate, an over-strict reading had become the convenient one. ADR-015.

### What the adversarial verification changed, reported as load-bearing

Nine lenses across three candidates, all of them run after four agents died on a
session limit and the run was resumed. **Every correction narrowed or weakened
the record, and none changed a verdict** — which is the pattern a verification
should produce when the verdicts are right and the reasoning is not yet.

- It **overturned** candidate 3's central factual claim with one HTTP header.
- It caught **two selective quotations** already in a draft of `docs/LICENCES.md`:
  the Polymarket Terms' only affirmative grant, and Kalshi's Section I PERMITTED
  USES, which grants personal non-commercial access while conditioning AI/ML
  training on prior written consent. Quoting only prohibitions had made the
  Kalshi framing one-sided.
- It **refuted candidate 2 on element (1)**, which the read had certified
  "satisfied, and generously".
- It **deleted a leg** of candidate 1's rebuttal: the Institute guide was still
  live when fetched, so it is a standing representation, not a superseded prior
  one. An argument that fails is deleted, not softened.
- It **closed the AI/ML axis**, unsearched by every licence read, on the very
  clause class that decided Kalshi — and found a **measured null**:
  `artificial intelligence` 0, `machine learning` 0 across the Polymarket Terms.
  **Polymarket has no AI clause where Kalshi has one.**
- It found that the on-chain path is **narrower** than claimed: the bullet is
  scoped to "the Site, any other Interface, or Features", and a public Polygon
  ledger is none of the three on its face. Amendment 6's Polygon question stays
  **open**, neither closed nor opened here.

### What was not read, recorded so it is not mistaken for absence

A completeness pass established that **the candidate space was sampled, not
enumerated**. The sharpest gap: **versioned repository deposits — Zenodo,
Dataverse, OSF, figshare — were never fetched**, and a DOI landing page prints a
licence, a publication date and a version *by construction*. Candidate 2 reached
UNMEASURED on the effective-date element **without fetching the one document
class that carries that element by construction**. Also unread: the CC BY 4.0
errata page named in the legal code's own footer, Manifold's Terms of Service,
six Dune addenda incorporated by reference, Token Terminal's Subscription
Agreement, ICE's terms, Kalshi's non-PDF surface, and any regulatory disclosure
route for a CFTC-designated contract market. Full list in `docs/LICENCES.md`.

**The direction of bias is named: an under-sampled space biases toward
UNMEASURED, the fail-closed direction.** It is still a bias. **"There is none"
is a verdict over what was read, and it is not a proof that no permitted route
exists.**

**And one observation that is uncomfortable and correct:** three reports on
permission produced **zero coverage figures** — no bucket count, no dispersion,
from any route. That is this stage's registered scope working as designed. But
NPDExperiment failed on **power**, not on permission. **Even if an authorization
were granted tomorrow, the power question would still be unanswered**, and
nothing in Stages A through D has moved it.

### Task 3 — what each candidate would and would not license

**No candidate returns PERMITTED, so the registered questions are not reached
for any of them** — which universe becomes measurable, whether the Stage B
region of 91–99c is reachable inside it, and whether the Canadian-permitted
filter can be applied. They are recorded as **not reached**, not as answered in
the negative.

The one that came closest is recorded with what it *would* have offered, so a
later session need not rediscover it: `Polymarket-v1` would on its documentation
make the unrestricted Polymarket universe measurable, and carries the `category`,
`opens_at` and `close_at` fields the permitted filter of economic indicators,
financial markets and climate at a 30-day minimum maturity would need. **It
documents no order-book depth, so Amendment 5's volume floor could be applied
but the registered 1-cent half-spread could not be checked.**

**The transfer statement, which holds whatever the outcome and is now pinned by
a mutation-verified test:** any measurement on Polymarket records — from the
venue, from a dataset, or from a third-party platform — **licenses a statement
about Polymarket and nothing whatever about Kalshi.** H1t remains **UNTESTED**
on three grounds including MLCryptoEngine's H2 at **AUC 0.501**. **A dataset
licence changes the permission, never the venue.** Rewriting that sentence to
"arguably settles the venue question too" fails the suite; restoring it passes.

### Task 4 — the honest position

**There is none, and that is a legitimate terminal state.**

The calibration question is **unmeasurable at this house's standard until an
authorization is granted** — not in principle, and not because the arithmetic
came out badly. The power gate has still never fired on any venue over any
region. It is unmeasurable because every route this stage read either prohibits
the reading or cannot show it is permitted, **and this repository does not
proceed on the second any more than on the first.**

**The register carries BAND-OPEN as a cost finding with no calibration
measurement behind it**, and that sentence is the whole of what this repository
has established about prices. It records that cost alone does not close the
question. **It is not evidence that an edge exists** — every magnitude any cited
source places inside its surviving bucket, Bürgi's 2.0 and 3.0 points, **fails**
the cost floor, and the band survives on its registered top, set by the one
source whose n the registration never recorded.

**Why this is written as a terminal state and not a setback.** It is the outcome
the design was built to reach cheaply, and it reached it cheaply: four stages,
**zero dollars, zero contracts enumerated, zero market-data requests to
Polymarket, and no statistic relating a price to an outcome anywhere in this
repository.** NPDExperiment discovered its answer after **415 days** of
collection in the session that read the result; this one discovered, before
collecting anything, that the collection is not permitted. **Two venues and
three third-party routes now say the same thing, in five documents, for four
different reasons. That is a result.**

**No fourth venue is proposed.** The sequence Kalshi → Polymarket → datasets →
platforms has already produced one retracted amendment from exactly that move,
and proposing a fifth route after four close is how a measurement-only project
turns into a search for someone who will say yes. **ADR-012 was not softened to
admit a candidate**, and the one candidate it excludes on a technicality it
arguably was not written for is recorded with that tension stated in full,
escalated to the operator, and left closed.

**What would change it**, each an operator decision rather than a measurement:
written authorization from Adventure One QSS, Inc. or from Kalshi — still the
only path that reopens a **Canadian-tradeable** venue; a numbered amendment on
whether an immutable named public licence satisfies element (2) by version
identity, registered *before* the measurement it governs and only alongside
closing element (1), the chain of title and the AI-clause search; or a paid
third-party tier, which needs an account, an acceptance of terms and a payment,
all outside standing rule 11 absent an explicit operator instruction — and which
still would not establish that the platform holds redistributable rights in the
underlying records.

**None of these is a second look, because no outcome has ever been read.**

### What stands

Stage B's **BAND-OPEN** over 91–99c held to resolution, computed from registered
constants, never dependent on venue access, and untouched by any of this.

---

## Entry 9.1 — addendum: thirteen mutations, and the mutation harness lost work

**Thirteen mutations, all thirteen load-bearing** (standing rule 14). Five at
source level over `pmexperiment/admissibility.py`: the suite fails when the
effective-date check is stripped — the mutation Task 1 names by hand — and
equally when the clause check is stripped, when the fetch-date check is
stripped, when `permits()` is allowed to read UNMEASURED as permission, and when
the client-rendered-shell detector is disabled. Eight over the documents: the
suite fails when a candidate is admitted as PERMITTED, when UNMEASURED is
collapsed into PROHIBITED, when the record is allowed to say the Kalshi finding
met the bar in full, when a refusal is invented that never happened, when the
unread candidate space is described as exhaustively enumerated, when BAND-OPEN
gains a calibration measurement it does not have, when the transfer statement is
softened, and when the self-conviction sentence is dropped. All thirteen restore
green at **95 tests**.

### The harness lost work, and the fault is recorded rather than repaired quietly

**The mutation harness destroyed uncommitted edits to `docs/LICENCES.md`.** Its
restore step is `git checkout -- <target>`, which restores the *last committed*
state. The target held two uncommitted Task 5 edits — the CC BY errata
correction and the whole "what this stage did not read" section — and the first
mutation's restore discarded both. They were rewritten from the session record
and the suite is green, so nothing is missing from the repository; what was lost
was the work of writing them twice.

**Two fixes, and the second is the one that matters.** The harness now refuses to
run on a dirty target — a checkout that could discard uncommitted work is a
harness fault, not a restore — and Task 5's work was committed before the
mutations were re-run. **A tool whose recovery path is `git checkout` may only be
pointed at a clean tree.**

**And the hard-wrap fault appeared for the third time, in its third form.** Three
of the eight document mutations first reported HARNESS FAULT — pattern absent —
because the needles are hard-wrapped in the source and the harness matched
literally. This is the same root cause Entry 1 and Entry 7.1 both recorded: **the
test reader folds whitespace and the mutation tool does not.** Entry 1's fault
was a reader failing to match text that was present, and the fix belonged in the
reader. Entry 7.1's was a `sed` silently *not* removing text, and the fix
belonged in the harness. This one is Entry 7.1's again, and the fix is the same
place: the harness now joins the needle's words with `\s+` before matching, so a
line break cannot hide a target from it.

**The harness reported all three as faults rather than as passing guards**, which
is precisely what Entry 7.1 rebuilt it to do. **A mutation that does not mutate
is still not evidence, and the machinery that says so has now earned its place
twice.** Re-run fold-tolerant against a clean tree, all three bite.

### Task 5 actual, and the stage total

**Task 5: ~14 min against the 12-min ETA** (06:27:18Z → the commit carrying this
entry), covering Entry 9, the Stage D section of `report.md`, the HYPOTHESES.md
amendment, ADR-013 to ADR-015, six new honesty tests, thirteen mutation runs and
one harness repair.

**Stage D total: ~2 h 15 min against 55 min stated** (04:18:14Z → push),
overrunning by a factor of 2.5 — **the first stage in this repository to run long
rather than short.** Stages B and C each came in at roughly a third of their
estimates and Entry 7.1 predicted the same again. **The prediction was wrong, and
the reason is Task 2**: every prior stage's estimate was scaled from
document-writing or arithmetic, and Task 2 was neither. It was an adversarially
verified read of a candidate space, and it took 111 minutes against 20.

**The lesson for the next stage's estimates, stated so it is not rediscovered:**
Stage B taught that a rate can be wrong, and Stage D teaches that **an activity
can be wrong**. Standing rule 2 requires an ETA "derived from a probe or from
comparable measured work" — and when no comparable work exists, Entry 7's
practice of **deferring the estimate until a probe can supply one** is better
than scaling a different activity to fill the cell. Stage C deferred its
enumeration ETA and recorded no fictional number. Stage D should have deferred
Task 2's.

---

## Entry 10 — Stage E operator prompt, logged verbatim before any other work

**Logged 2026-09-02T09:22:59Z, read from `date -u` at the moment of recording and
not extrapolated from a previous timestamp (Entry 6.1). Per standing rule 1.
Work follows in later entries; nothing below this line in this entry is work.**

> BEGIN PROMPT - PMEXPERIMENT STAGE E: CLOSE THE PROJECT AS A TERMINAL ACCESS FINDING
>
> Read CLAUDE.md, REGISTRATION.md with all amendments, HYPOTHESES.md, DECISIONS.md through ADR-015, progress.md, report.md, docs/ACCESS.md, docs/BAND.md and docs/LICENCES.md first. Per standing rule 1, log this prompt verbatim before any other work. Per standing rule 2, state an ETA per task and record actual against it.
>
> This stage closes the project. It reads no venue, enumerates nothing, and computes no calibration statistic. Sections 4 and 10 stand to the end.
>
> Task 1: record the Kalshi reply as a measured access finding, since it changes the register.
>
> Stage D concluded no candidate permitted and wrote it as terminal. Kalshi's institutional desk has since replied, and the position is materially different from what the register holds. Record, in the ADR-012 shape with the date received: that the described use fits their Internal Use data licence, so it was not declined on the merits; that applying requires an established legal entity with formation documents and beneficial owner verification, which an individual undergraduate does not have; and that the 2021 historical depth is available through historical endpoints on the appropriate licence, since those are not subject to the live-data cutoff measured at roughly spring 2024.
>
> Note plainly that this is correspondence rather than a published instrument, so it carries a received date rather than an effective date, and say what that does to its admissibility under ADR-012 rather than glossing it.
>
> Task 2: record the entity path as closed by operator decision, with the reason.
>
> The operator consulted the university and judged institutional sponsorship not achievable within the time available, with fourth-year term starting. Forming a personal legal entity was judged disproportionate to a registered prior of 5 to 8 percent against a band verdict already recorded as thin.
>
> Record this as a decision rather than a discovery. It is the operator declining a cost, not evidence about the hypothesis.
>
> Task 3: state the terminal position.
>
> H1 is unmeasurable at this house's standard. Not disproven, not unlikely, unmeasurable: both venues closed on terms, all three licence candidates failed, and the one route that exists is gated on an entity the operator does not hold and has decided not to create.
>
> BAND-OPEN stands as what it always was, a cost finding computed from registered constants with no calibration measurement behind it. It must not be written anywhere as evidence that an edge exists.
>
> Record the reopening condition precisely: an established legal entity applying for Internal Use, or an academic tier offered by Kalshi if one is, or a licensed dataset whose licensor held authority to license. Note that a reply to the pending academic-tier question, if one arrives, is a one-line register update and not a reopening.
>
> Task 4: rewrite README.md for a cold reader.
>
> Lead with the question, the answer and the reason. Put the transferable output high, because it is the contribution: ADR-012 as a procedure, ADR-015 on the symmetry of convenience, the self-audit that convicted this repository's own Stage A finding at two of three elements, and Stage B's direction correction placing every registered magnitude at high entry prices where proportional FX is largest.
>
> State the registered prior and that a null was the modal expected outcome, so the closure reads as the method working rather than as a disappointment. State that no market price was ever read.
>
> Task 5: pin and close.
>
> Extend the honesty tests so the terminal verdict, the BAND-OPEN caveat and the reopening condition must be present, verified by mutation. Confirm the licence, that no credential-shaped string sits in any tracked file or in git history, and that .env.example is still empty. Append the final dated entry, an ADR for the closure, and a report.md section written for the moment it landed. Continue past the recorded ADR numbering collision rather than renumbering. Run make lint, make typecheck, make test. Push.
>
> END PROMPT

**ETAs stated before arming, per standing rule 2.** Entry 9 measured the lesson
these are built on: Stage D overran by a factor of 2.5 because Task 2's estimate
was scaled from **a different activity**, not merely a different rate, and its
closing instruction was to defer an estimate rather than fabricate a basis.
Stage E is document work end to end — it fetches nothing — so every cell below
derives from Stage D's *measured document* work, and the one cell with no
comparable is named as such rather than dressed up.

| task | ETA | basis (measured) |
|---|---|---|
| 0 — log the prompt | 2 min | Entry 9 measured **1.45 min** for exactly this act |
| 1 — the Kalshi reply as a measured access finding | 8 min | Stage D Task 5's non-mutation half — Entry 9, a report section, a HYPOTHESES amendment and three ADRs — occupied roughly **8 of its measured 14 min**; Task 1 here writes one ADR, one amendment and two evidence-document sections |
| 2 — the entity path closed by operator decision | 4 min | Stage D Task 4 measured **0.8 min** for a single document block; this carries an ADR and a register row beside it |
| 3 — the terminal position | 8 min | Task 1's basis, applied over Section 15.4, Section 16, the unfilled Section 13 and a HYPOTHESES amendment |
| 4 — rewrite README.md for a cold reader | 8 min | **no comparable measured work exists** — this repository has never timed a whole-file rewrite. Scaled from Task 1's basis by length and **flagged here as the weakest cell in the table**, for precisely the reason Entry 9 recorded |
| 5 — pin and close | 20 min | Stage D Task 5 measured **~14 min** for a report section, three ADRs, six honesty tests and thirteen mutation runs; this adds a licence and git-history audit and the push |

**Total stated: 50 min.** Actuals land in Entry 11.

**Scope carried in and not reopenable here**, per the prompt: this stage closes
the project. It reads no venue, enumerates nothing, and computes no calibration
statistic. **Sections 4 and 10 stand to the end.** The Stage B region of 91–99c
held to resolution is not reopened, no fourth venue is proposed, and the ADR
numbering collision recorded on 2026-08-29 is continued past rather than
renumbered.

**One thing visible at logging time that the prompt's own framing does not
carry, recorded now rather than at the point it becomes convenient.** The prompt
refers to "a registered prior of 5 to 8 percent". **Section 13, `The operator
prior`, is empty** — it reads "*To be filled by the operator before the gate
fires*" and has read that since Section 0 was committed on 2026-08-29. The
figure is therefore being supplied **at closure, after the band gate has fired**,
and Task 3 records it as such rather than as something the register already
held. This is noted in the prompt log so the sequence is fixed before any
document is written about it.

**One deviation visible at logging time:** the nine binding documents named in
the prompt were read, read-only, before this entry was written, exactly as
Entries 0, 4, 6 and 8 recorded for Stages A through D. No other work has been
done and no request has been sent to any endpoint.

---

## Entry 11 — Stage E: the project closes as a terminal access finding — 2026-09-02

**Verdict, one sentence: H1 is unmeasurable at this house's standard — not
disproven, not unlikely, unmeasurable — because both venues closed on their own
terms, all three licence candidates failed, and the one route that does exist was
found not to have been declined on the merits but to be gated on an established
legal entity the operator does not hold and has decided not to create.**

**Zero requests sent to any host in this stage. Zero contracts enumerated. Zero
dollars.** No price bucket was built, no dispersion computed, and **no statistic
relating a price to an outcome exists in this repository.** Sections 4 and 10
stand intact to the last commit.

### ETA against actual, per task (standing rule 2)

| task | ETA, with its basis | actual |
|---|---|---|
| 0 — log the prompt | 2 min, from Entry 9's measured 1.45 min for the same act | **0.7 min** (09:22:59Z → 09:23:41Z, `2006ae6`) |
| 1 — the Kalshi reply as a measured access finding | 8 min, from Stage D Task 5's non-mutation half at ~8 of its measured 14 min | **7.8 min** (09:23:41Z → 09:31:26Z, `17dfebd`) |
| 2 — the entity path closed by operator decision | 4 min, from Stage D Task 4's measured 0.8 min scaled for an ADR and a register row | **0.9 min** (09:31:26Z → 09:32:22Z, `fe7e6b9`) |
| 3 — the terminal position | 8 min, Task 1's basis over Section 15.5, Section 16, Section 13 and a HYPOTHESES amendment | **1.7 min** (09:32:22Z → 09:34:01Z, `f8128b2`) |
| 4 — rewrite README.md | 8 min, **flagged in Entry 10 as the weakest cell**: no comparable measured work exists | **2.5 min** (09:34:01Z → 09:36:29Z, `1ba50aa`) |
| 5 — pin and close | 20 min, from Stage D Task 5's measured ~14 min plus a licence and git-history audit | recorded at push in this entry's commit |

**Total stated 50 min.** Tasks 0 through 4 stated 30 min and ran **13.6 min**,
coming in at 45 % of estimate — and the distribution is more useful than the
total.

**The closing lesson on estimates, which is not the one Entry 10 expected.**
Entry 9 taught that **an activity can be wrong**: Stage D's Task 2 was scaled
from work of a different kind and overran by a factor of 5.5. Entry 10 applied
that lesson by deriving every cell from Stage D's *measured document* work and
by **naming Task 4 as the weakest cell**, having no comparable. The results:

- **Task 1, the one cell with a genuine same-activity comparable, landed within
  3 %** — 7.8 min against 8.
- **Every cell scaled from that basis *by length* rather than by activity came
  in at a fifth to a third of estimate.** Scaling by size is the same error as
  scaling by activity, in miniature.
- **Task 4, the cell explicitly flagged as weak, missed by a factor of 3.2.**

**So the flag was right that the estimate was unreliable and told nobody
anything about which way.** Labelling an estimate as weak is not a correction to
it; it is a guess wearing a warning label. The thing that actually predicted
accuracy in this stage was **whether a same-activity measurement existed** —
one cell had one and hit; five did not and missed. Entry 9's remedy stands and is
sharpened: **defer the estimate until a probe can supply one**, and prefer no
number to a flagged one.

### Task 1 — the reply, and what a two-day-old caveat turned out to be worth

Kalshi's institutional desk replied on **2026-09-01**. The use as described
**fits their Internal Use data licence** — **not declined on the merits**, no
merits objection raised at all. Applying requires **an established legal entity**
with formation documents and beneficial-owner verification. The **2021 historical
depth is available through historical endpoints** on that licence, outside the
live-data cutoff Stage A measured at roughly spring 2024.

**The received date was not in the prompt and was not synthesized.** Standing
rule 5 forbids exactly that, so it was asked for and supplied: **2026-09-01**.

**Admissibility, stated rather than glossed.** Correspondence carries a
**received date, not an effective date**. Fired through
`pmexperiment.admissibility` the claim returns **UNMEASURED on element (2)**, and
separately what this repository holds is **the operator's summary rather than the
reply's text**, so element (1) is unmet in substance too. The argument that a
received date *is* the effective date for an instrument that has no other is
recorded at full strength and **not adopted** — amending a general standard at
closure, to govern a measurement that will never be made, is worse than leaving
it open. **The asymmetry against ADR-014 is stated rather than claimed as
credit: there, holding the standard cost the one attractive candidate; here it
costs nothing, because the entity requirement closes the route either way.**

**Firing the procedure over correspondence found a blind spot in the
procedure.** `missing_elements()` checks only that a clause is non-empty and
**cannot tell a quotation from a paraphrase**. **The check is weaker than the ADR
it implements**, and this is the first claim in five stages that showed it —
every earlier one was fired over a document this repository had itself fetched.
**Recorded, deliberately not repaired**: no honest detector exists, and quotation
marks are not evidence of quotation.

**And the finding that is worth more than the reply.** Stage D published "there
is none" as terminal on 2026-08-30 **while recording in the same document that
its candidate space was sampled rather than enumerated**, and that *"there is
none" is a verdict over what was read.* **A route surfaced two days later.** The
caveat cost one paragraph and was load-bearing inside a week. **That is the
strongest argument this repository can make for writing completeness limits at
all**, and it is recorded in ADR-016, in `docs/LICENCES.md` and in `README.md`
so it is not lost.

**One correction to Stage A that did not need making, recorded because it is the
good kind of surprise.** Stage A wrote that the 2021→Apr 2025 span is *"not
reproducible keylessly"* — a claim about the keyless surface, not the archive.
Finding 3 confirms the archive exists behind the licence. **Had that sentence
been written as "the history does not reach 2021", it would now be false.** The
careful phrasing was load-bearing and it held.

### Task 2 — the decision, filed in its own category

The operator consulted the university and judged **institutional sponsorship not
achievable within the time available**, with fourth-year term starting. Forming a
**personal legal entity** was judged **disproportionate** to a stated prior of
5 to 8 percent against a band already thin — the top **2.15 of 6.0 points** at
95c, requiring **5.85 points** at k = 1 against a band top of **8.00**, with
Bürgi's **2.0** and **3.0** both failing the **0.0300** floor.

**This is the operator declining a cost. It is not a discovery and it is not
evidence about H1 in either direction.** Filed as ADR-017 in its own category
because **a project that closes on access and a project whose operator stopped
paying look identical from outside, and only one of them is a finding.**
**Kalshi did not refuse**; nothing was applied for, so nothing was granted and
nothing was refused, and the label stays **EXISTS-AND-UNTRAVELLED**.

### Task 3 — the terminal position, and one thing the prompt's framing got wrong

**H1 is unmeasurable at this house's standard.** Section 15.5 and Amendment 8.

**The prompt referred to "a registered prior of 5 to 8 percent". Section 13,
`The operator prior`, is empty and has been since 2026-08-29.** The figure
arrives **at closure, after the band gate and both access gates had fired**. It
is recorded in Amendment 7 and **may never be described as pre-registered**;
Section 13 is **left empty permanently**, because a visible gap is a truer record
than a plausible-looking backfill, and a test now fails if it is filled.
Recorded because it reframes the closure rather than because it flatters it: at
5 to 8 percent, **a null was the modal expected outcome from the beginning.**

**The registered closure conditions were never met.** Section 16 provides for H1
to close when both verdict cells fire BLOCKED with realized MDEs beside them.
**Neither fired; no MDE exists.** H1 does **not** close under Section 16 at all.
That is annotated in Section 16, which is otherwise left exactly as registered.

### Task 4 — README.md, and two corrections to the prompt's framing

Rewritten for a cold reader, leading with the question, the answer and the
reason, with the transferable output moved to the top: **ADR-012 as a procedure**
(now with its blind spot disclosed), **ADR-015's symmetry of convenience**, **the
self-audit that convicted this repository's own Stage A finding at two of three
elements**, and **Stage B's direction correction** placing every registered
magnitude at 88–95c, where proportional FX is largest.

**Two claims the prompt asked for were not written as asked, and the reasons are
recorded rather than the claims quietly adjusted:**

1. **"the registered prior"** — it is not registered. The README says **"stated,
   not pre-registered"** and explains why, as above.
2. **"no market price was ever read"** — **not accurate.** Stage A's 11 keyless
   probe requests received **two settled records carrying `last_price_dollars`
   and `result`**, recorded in `docs/ACCESS.md` since 2026-08-29. The README
   states that exactly and says instead that **no price series was ever collected
   and no statistic relating a price to an outcome was ever computed**, which is
   true. Rounding the first to the second is precisely the class of claim this
   repository exists to refuse, and doing it in the README would have been the
   worst possible place.

### Task 5 — pinned, audited, closed

**Thirteen new honesty tests; fourteen mutations, all fourteen load-bearing.**
The suite fails when the terminal verdict is softened to "unlikely", when the
BAND-OPEN caveat is stripped, when a reopening condition is dropped, when the
no-fourth-venue guard is removed, when a pending reply is promoted into a
reopening, when the route is rewritten as a refusal by Kalshi, when the entity
decline is reframed as evidence about H1, when the prior is called
pre-registered, when Section 13 is backfilled, when the closure is passed off as
Section 16's registered closure, when the price reading is rounded to "never",
when Stage D's vindicated caveat is deleted, when the procedure's blind spot is
concealed, and when the correspondence is promoted to an effective-dated
instrument. All fourteen restore green at **108 tests**.

**The harness ran clean on its first pass, which has not happened before.** Both
of Entry 9.1's fixes were carried in from the start — it refuses a dirty target,
and it folds whitespace in the needle before matching — and **zero harness
faults** were reported against fourteen mutations, where Stage D's first passes
reported faults on three of eight and then on all five source mutations. The
hard-wrap fault that appeared three times across Entries 1, 7.1 and 9.1 **did not
appear a fourth time.** It was fixed in the right place.

**The audit, run over the whole history rather than the working tree.** **32
commits, 189 reachable objects, every blob decompressed and scanned: zero
credential-shaped strings.** The only env-shaped path ever added to this
repository is `.env.example`, which is **294 bytes, five comment lines, and
contains no `=` at all** — pinned by a test since the scaffold. `LICENSE` is MIT,
17 lines, `Copyright (c) 2026 kirosli00tuff`. `.gitignore` covers `.env`,
`.env.*` with `!.env.example`, `*.session`, `data/raw/` and `data/vendor/`.

### What this repository is at the end

**Five stages. Zero dollars. Zero contracts enumerated. Zero market-data requests
to Polymarket. Zero requests of any kind in Stage E. No price bucket, no
dispersion, and no statistic relating a price to an outcome, anywhere, ever.**

**BAND-OPEN stands as a cost finding computed from registered constants with no
calibration measurement behind it, and it must not be written anywhere as
evidence that an edge exists.** **H1t remains UNTESTED** on three grounds
including MLCryptoEngine's H2 at **AUC 0.501**.

**And the uncomfortable one, kept in the entry rather than a footnote.** This
repository was built against NPDExperiment's failure, which was a failure of
**power**. Five stages here produced **zero coverage figures** — no bucket count,
no dispersion, from any route. **If an authorization arrived tomorrow the power
question would still be unanswered.** Following Insider rather than NPD saved 415
days and every dollar. It did not answer the question the design was built to
answer, and nothing here should be read as though it had.

---

## Entry 11.1 — addendum, recorded after the push: the closing actuals

**Task 5 actual: ~7.9 min against the 20-min ETA** (09:36:29Z → 09:44:22Z,
commit `905d552` pushed to `origin/main`), covering thirteen honesty tests,
fourteen mutation runs, the whole-history credential audit, ADR-018, the
`report.md` section, Entry 11, and the three make targets.

**Stage E total: ~21.4 min against 50 min stated** (09:22:59Z → 09:44:22Z),
coming in at **43 % of estimate**. Stages B and C ran at roughly a third of
theirs, Stage D overran by 2.5, and this one is back under. **Four stages short,
one long, and the one that ran long is still the only one whose estimate was
scaled from the wrong activity.**

**One correctness note on the make targets, recorded rather than left in the
shell history.** `make lint` failed on the first run: `ruff format` reflowed one
assertion, and after reformatting `ruff check` raised **E501 at 90 > 88** on a
test function name long enough to break the line. It was renamed to
`test_terminal_verdict_is_unmeasurable_not_disproven_not_unlikely`, the mutation
harness's reference was updated with it, and **all fourteen mutations were
re-run against the committed tree afterwards — 14 killed, 0 survived, 0 harness
faults**, so the rename is proved not to have quietly disarmed the guard it
names. Lint, typecheck and test are green at **108 tests**.

**The last figure in this repository, and it is the right one to end on.** Five
stages, **zero dollars, zero contracts enumerated, zero statistics relating a
price to an outcome**, and a power gate that never fired. **The question is not
answered.** It is closed.
