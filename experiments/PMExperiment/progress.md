# progress.md — PMExperiment session log

Append-only. One entry per sub-stage. Every entry states the ETA given before
the task was armed and the actual elapsed against it, per standing rule 2.
Every figure travels with its n in the same sentence, per standing rule 13.

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
