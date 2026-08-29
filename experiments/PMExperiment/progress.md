# progress.md — PMExperiment session log

Append-only. One entry per sub-stage. Every entry states the ETA given before
the task was armed and the actual elapsed against it, per standing rule 2.
Every figure travels with its n in the same sentence, per standing rule 13.

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
