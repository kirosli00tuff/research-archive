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

---

## Stage B — the fee-versus-edge band — 2026-08-29

**The verdict, in one sentence: BAND-OPEN — at entry prices 91–99c held to
resolution, an effect at the top of the registered band would clear the
registered Canadian retail cost, needing 5.85 probability points of
underpricing against a band whose top is 8.00, so the tradeable question is
not closed on cost — but the surviving region is the top 2.15 points of a
6-point band, no cited source places a magnitude there at that price bucket,
and the band's top is set by the one source whose sample size the registration
never recorded.**

**Nothing was read to reach this.** No contract, price, order book or
resolution was requested from Polymarket, Kalshi or anywhere else. The whole
stage is arithmetic over constants registered before it began, so Sections 4
and 10 stand intact and the stage cost nothing.

**The stage's main intellectual risk was a unit, and it was retired first.**
The cited sources lead with realized *returns* while the fee is denominated in
*probability points*, and the two differ by the factor 1/p — an order of
magnitude at the tails. Getting it backwards would have inflated or destroyed
the band. Each recorded magnitude was reconstructed both ways and checked
against the numbers the registration itself prints: Bürgi's 5c contract
winning 3 % is a 2-point gap *and* a −40 % return, and both reproduce exactly.
Krause's −0.077 settles it alone, because under the return reading the figure
Section 3 calls the largest cited would be the smallest. The band is in
probability points, unambiguously, and no conversion was needed.

**The consequential half of that finding was direction, not units.** At
longshot prices the documented miscalibration is *over*pricing, so a buyer of
a longshot holds a negative edge while break-even requires *under*pricing. The
exploitable expression is always the complement. Restated that way, **every
registered magnitude sits at a high entry price** — 88c to 95c — which is
exactly where a price-proportional FX charge bites hardest. That is what made
the FX question material rather than bookkeeping, and it is registered as
Amendment 4: the two candidate models are one formula with a turnover, k = 1
binds because Section 2 forbids revising a cost component toward H1, and the
verdict turns out to be identical under k = 1, k = 12 and FX driven to zero.

**The central arithmetic fact.** The registered cost floor runs **entirely
inside** the registered effect band at every price. It never crosses either
edge anywhere in the tradeable range: the round-trip curve meets the band's
top only at $1.00, a price that cannot be traded. Section 2 predicted this in
advance — C(0.95) = 0.0785 "sits at the top of the published effect band … the
central economic fact this repository exists to test" — and the arithmetic
confirms it to 0.0015.

**The number a reader should keep.** The venue fee and half-spread alone come
to 0.0300 on the held-to-resolution route, before any FX at all, against a
registered band bottom of 0.0200. **No FX treatment, no venue price and no exit
route reaches the bottom of the band.** And at the FX-free limit the held route
requires exactly 0.0300 while Bürgi's favourite-tail gap is exactly 0.0300 — a
dead heat, zero expected profit, at the one bucket where a magnitude is
actually cited.

**So BAND-OPEN is a thin verdict, and it is reported as one.** It fires because
Amendment 2's own rationale asks whether a documented effect *could* survive,
and at the top of the registered band one could. It does not fire because any
cited magnitude survives: the two figures cited at 91–99c are 2.0 and 3.0
points and both fail. The only cited figure large enough is Krause's 7.7
points, whose exploitable entry price is 88.3c — one decile below the tail cell
the band is registered for — and whose n appears nowhere in this repository.
The band's bottom travels with 313,972 contract prices; its top travels with
none.

**What it authorizes, and what it does not.** BAND-OPEN is not evidence that a
tradeable edge exists. It records that cost alone does not close the question,
so the power gate is still worth firing — over entry prices 91–99c held to
resolution, and over no other region. That gate was not designed here.
Amendment 3's labelled-phenomenon-study route is not triggered; it applies only
on BAND-EMPTY.

**Two things are still unmeasured, and are recorded as unmeasured rather than
assumed.** Whether the permitted subset contains 91–99c contracts in usable
numbers is a count this stage may not read, and by registration it is the power
gate's question. And Section 1's volume floor was never registered, because
Stage A's Task 2 never armed — which is why BAND-NARROW's "below usable volume"
clause could not be evaluated at all.

A later correction is a new line, never an edit.
