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

---

## Stage C — the power gate over 91–99c — 2026-08-30

**The verdict, in one sentence: PENDING_ACCESS — Polymarket's Terms of Use,
effective 2026-08-11 and read in full before any repeated fetch, prohibit "data
mining tools, robots, crawlers, or similar data gathering and extraction tools"
with no entity-type qualification, and their scope reaches anyone "connecting
via an API" and data taken "directly or through an API, or any other means,
including on-chain" — so the enumeration was never armed, the power gate did not
fire over 91–99c or anywhere else, and zero market-data requests were sent to
the venue.**

**The finding underneath the verdict is about this repository, not about
Polymarket.** Amendment 1 moved the entire measurement venue here on the stated
ground that Polymarket's data is "public by construction rather than by
permission" and that "standing rule 12 is satisfied here rather than
circumvented." That claim cited no terms document, no clause, no effective date
and no fetch date. It inferred **permission** from the absence of an
**authentication** requirement — and those are different properties. Stage A had
already shown the gap on Kalshi, whose data was equally keyless and equally
prohibited. Amendment 6 retracts the ground; ADR-012 converts the lesson into a
practice, that a claim about what terms permit carries a quoted clause with both
dates or is recorded as unmeasured.

**Polymarket is the same case as Kalshi, not the opposite one.** That sentence
is the result. Two venues, both serving data reachable without a credential,
both publishing terms that withhold the systematic retrieval this measurement
needs absent prior written consent.

**What was measured, and what was deliberately not.** `robots.txt` on
polymarket.com returns HTTP 200 in 35.7 ms with `User-agent: *` and **no
`Disallow` at all** — genuinely more permissive than Kalshi, whose website
served a 429 bot challenge before robots.txt. The three API hosts publish no
crawl directives. The developer documentation publishes rate limits and a
builder program and **zero** occurrences of "terms of use", "license",
"acceptable use" or "public data". Reachability, rate limits and history depth
were **withheld** rather than measured, following ADR-007: standing rule 12
outranks standing rule 4 precisely when the measurement would itself be the
prohibited act.

**The ordering clause of rule 12 earned its keep, and that is worth saying
plainly.** "Record robots.txt and the published terms *before any repeated
fetch*" is what made the withholding possible. Stage A read eleven keyless
Kalshi market requests before its terms position was established and could only
withhold the rate-limit burst afterwards. Stage C read the terms first and sent
**zero** market-data requests. The rule did exactly the work it was written to
do, and it should not be softened.

**Reading the terms took work, and the shortcut would have produced a false
report.** `polymarket.com/tos` returns HTTP 200 but is client-rendered: 217 KB of
body strips to 1,354 characters, and the Next.js payload carries only an app
shell under a route named `(embedded-docs)/tos`. Reporting from either of the
first two reads would have been reporting on a page shell while believing it was
the terms. The document itself is embedded from elsewhere, and it is 59,617
bytes long.

**What is recorded against the finding rather than for it.** Three things cut
the other way and are stated because a verdict that lists only its supports is
not a verdict. robots.txt is fully permissive. The Data clause — the one that
names on-chain access — is **conditional on entity type** and does not bind a
retail researcher, so it is quoted for scope and is not the ground. And the
strongest counterargument is real: the crawlers bullet forbids scraping from
"the Site, any other Interface, or Features", "Interface" is defined as sites
where the Terms are posted, and the Terms are not posted at
`gamma-api.polymarket.com`. Amendment 6 sets that argument out in full and gives
three reasons it is not taken, the governing one being that a venue may not be
held to a looser reading than another because its verdict would be more
convenient.

**Task 1 landed and is not wasted.** Section 1's volume floor — missing since
Stage A never armed the task that would have filled it — is now registered as
Amendment 5 at **total traded volume ≥ $1,000**, imported verbatim from the
benchmark study whose magnitudes set the effect band. A floor chosen by someone
else, before this repository existed, cannot have been tuned to a sample this
repository had not yet seen. **Its cost in sample is unmeasured and is reported
absent, not as zero**, because no enumeration ever ran.

**On what a Polymarket result would and would not have licensed.** The stage was
instructed to state this whatever the verdict, and it holds more sharply now
that there is no result at all: a GO on Polymarket would have licensed a
calibration measurement **on Polymarket**, and nothing whatever about Kalshi.
H1t — transfer — is registered UNTESTED on three grounds, including this
program's own MLCryptoEngine H2 measuring cross-venue transfer at **AUC 0.501**.
No Polymarket figure exists to be misread as evidence about a Canadian-tradeable
venue, and none may be written as one if it ever does.

**What stands.** Stage B's BAND-OPEN verdict over 91–99c held to resolution is
untouched, because it was computed from registered constants and never depended
on venue access. What is now unavailable is the count that would say whether
that region holds contracts in usable numbers — and that remains, as it has been
since Section 0.4, an open question rather than an answered one.

A later correction is a new line, never an edit.

---

## Stage D — three candidate licences, and there is none — 2026-08-30

**The verdict, in one sentence: no candidate returns PERMITTED — Polymarket
publishes contact addresses but every one of them is scoped to someone else, the
leading academic dataset states CC BY 4.0 and documents all four gate inputs
over 1,201,580,990 rows yet fails the evidence standard on two elements, and
Dune's in-force Terms prohibit the tool class outright and gate programmatic
query behind a paid subscription — so the calibration question is unmeasurable
at this house's standard until an authorization is granted, and that is a
terminal state rather than a setback.**

**Nothing was enumerated to reach this.** No contract, price, order book, volume
or resolution was requested from any venue, dataset or platform. Only licences
were read. Zero dollars.

**The stage's first act was to apply its own rule to itself, and the rule
convicted the record.** ADR-012 requires that a claim about what a source
permits carry a quoted clause, an effective date and a fetch date. Written as a
procedure and fired over this repository's own three claims, it returns:
Amendment 1 inadmissible on all three elements, as expected; Stage C's
Polymarket finding admissible on all three; and **Stage A's Kalshi finding
admissible on two of three.** ADR-012 says that finding "met that bar." It did
not — **no tracked document records an effective date for the Kalshi Data Terms
of Use, and the licence read confirmed at source that the document prints none.**
This changes no verdict, because an unmeasured permission and a prohibited one
both mean proceed as if permission were absent. It changes what the record may
claim about its own evidence, and it is recorded because **a procedure that only
ever convicts other people's documents is not a procedure.**

**The most useful thing the stage produced is a distinction it had to enforce
against itself within the hour.** UNMEASURED is not a synonym for PROHIBITED:
same operating posture, different epistemic content, one a measured refusal and
the other an absence. The licence read of Dune declared its current Terms
unreadable behind Cloudflare, quoted every clause from a superseded archive, and
published PROHIBITED anyway. **Bare `curl` returns 403; the same `curl` with
nothing added but a browser User-Agent returns HTTP 200.** The in-force
instrument was one header away, and publishing a prohibition from a document
never read is **Amendment 1's error with the sign reversed** — that amendment
inferred permission from a document it never read. The evidence standard has no
direction-of-travel exemption, and a repository that had just been handed a
pre-blessed no-candidate outcome had every incentive not to notice.

**What each candidate turned out to be.** Polymarket publishes six addresses and
designates none of them for this ask: the data-licensing route opens "If you or
your clients are Capital Markets Entities", the builder programme's published
upgrade path is gated on "Route orders through Polymarket", and the Terms carry
no notices clause and no postal address at all. **Kalshi is the mirror image —
it names prior written authorization as the only key and publishes no address to
present it at, in a document that is itself undated.** Nothing was drafted and
nobody was contacted, so **nothing was refused**; PROHIBITED is the baseline, not
a rejection. The dataset question is genuinely separate from the venue question
and it still fails: `Polymarket-v1` carries everything the gate would need,
including resolution *presence* separable from resolution *value*, and neither
its card nor the CC BY 4.0 legal code prints any date — while the licence's own
Section 1 limits it to rights "the Licensor has authority to license" and
Section 5(a) disclaims title, over a corpus its own card says is unaffiliated
with the venue it came from.

**The adversarial verification earned its cost and is reported as load-bearing.**
Nine lenses across three candidates overturned Dune's central factual claim,
caught two selective quotations already sitting in a draft of the evidence
document — the Polymarket Terms' only affirmative grant, and Kalshi's PERMITTED
USES clause, which grants personal non-commercial access while conditioning
AI/ML training on written consent — refuted the dataset candidate on a second
element its reader had certified "satisfied, and generously", deleted an unsound
leg of a rebuttal rather than softening it, and closed the AI-and-machine-
learning axis that no licence read had searched, on the very clause class that
decided Kalshi. **Every correction made the record narrower or weaker. None
changed a verdict.**

**What the stage did not read is stated, because a sampled space is not an
enumerated one.** Versioned repository deposits — Zenodo, Dataverse, OSF,
figshare — were never fetched, and a DOI landing page prints a licence, a date
and a version *by construction*. The dataset candidate therefore reached
UNMEASURED on the effective-date element **without fetching the one document
class that carries that element by construction.** The direction of that bias is
named: under-sampling biases toward UNMEASURED, which is the fail-closed
direction and the safe one, and it is a bias all the same. **"There is none" is
a verdict over what was read. It is not a proof that no permitted route exists.**

**The honest position, and why it is a terminal state.** The register now carries
BAND-OPEN as a cost finding with **no calibration measurement behind it** —
that sentence is the whole of what this repository has established about prices.
Four stages have produced zero dollars spent, zero contracts enumerated, zero
market-data requests to the measurement venue, and **no statistic anywhere
relating a price to an outcome.** NPDExperiment discovered its answer after 415
days of collection, in the session that read the result. This one discovered,
before collecting anything, that the collection is not permitted. Two venues and
three third-party routes now say the same thing in five documents for four
different reasons, and **that is a result, not the absence of one.**

**No fourth venue is proposed and the standard was not softened to admit a
candidate.** The one candidate excluded on a technicality the rule arguably was
not written for — no Creative Commons legal code prints a date — is recorded
with that tension stated at full strength, escalated to the operator, and left
closed. Curing the date would not open it: the chain of title, the grant's own
limits, and an unrun AI-clause search all survive the fix.

**One thing is uncomfortable and belongs here rather than in a footnote.** Three
reports on permission produced zero coverage figures. That is the stage's
registered scope working exactly as designed — it enumerates nothing. But the
precedent this repository was built against failed on **power**, not on
permission. **If an authorization arrived tomorrow, the power question would
still be unanswered**, and nothing in Stages A through D has moved it.

A later correction is a new line, never an edit.
