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
