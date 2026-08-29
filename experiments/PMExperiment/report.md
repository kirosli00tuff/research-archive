# report.md — PMExperiment, stage by stage

Each section is written for the moment it landed and is not revised afterwards.
A later correction is a new line, never an edit.

---

## Scaffold — 2026-08-29

**No stage has run.** No request has been sent to any endpoint, no contract,
price, resolution or ledger row exists, and `REGISTRATION.md` Section 0 is not
written.

Structure only: the seven binding documents, the package and test skeletons,
the sixteen standing rules, and four ADRs. Nine honesty tests pin the scope
statement and the power figures into `README.md` and `CLAUDE.md`, verified by
mutation — altering the no-first-moment rule fails the suite, restoring it
passes.

**Nothing is claimed here.** The first substantive section of this file is
written when Stage A Task 1 reports measured access.

---

## Stage A — access, the permitted subset, and the power gate — 2026-08-29

**The verdict, in one sentence: Stage A ends PENDING_ACCESS — Kalshi's
public data is technically reachable without an account (HTTP 200 at
100–214 ms across 11 keyless requests) with resolution outcomes exposed
beside final prices, but the recorded terms do not sanction the systematic
keyless retrieval this measurement needs, the API Developer Agreement that
governs programmatic access cannot be read by automated means, and the
keyless settled history is in any case too shallow (reaching only to between
2024-01-01 and 2024-05-31, n = 6 bracketing probes) — so the power gate
never fired and the calibration question stays open, unmeasured.**

Section 0 was registered first, in full, before any request: the outcome map
on counts and dispersion only, the effect band 0.02 to 0.08 cited to
Bürgi-Deng-Whelan (2026), Krause (2026) and Page-Clemen (2013), the cost
model (4c fees + 1c half-spread assumption + 3 % FX, a cost floor of 0.0785
at the 95c tail), and outcome blindness with mutation-verified guards. That
registration held: no price bucket was built and no outcome was joined to
any price.

The access gate failed closed on three of five registered conditions
(REGISTRATION.md Section 15.1, evidence in docs/ACCESS.md). The Canadian
permitted-subset filter was therefore never registered, no subset count
exists, and no price-bucket distribution exists — reported as absent, not as
zero. Tasks 2 and 3 never armed, exactly as the registration's
PENDING_ACCESS row prescribes.

**On Stage B:** the operator prompt asks what Stage B would be if and only
if the gate cleared. The gate did not clear, so no Stage B is stated.

A later correction is a new line, never an edit.
