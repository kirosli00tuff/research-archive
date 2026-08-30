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
