# DECISIONS

Architecture decision records. Each records a deliberate departure from a
default, or a choice that a later reader would otherwise have to reverse
engineer. Append only.

---

## ADR-001. This is a separate repository

**Status:** accepted, 2026-08-29.

The prediction-market hypothesis shares no universe, no venue, no cost model
and no data source with any existing repository in this program. Folding it
into one of them would mix two registers and two multiplicity accounts.

**Consequence:** its own register, its own trial accounting, its own ledger. No
result here is evidence in another repository's family, and no result there is
evidence here.

---

## ADR-002. Stage A holds no account, on either side of the border

**Status:** accepted, 2026-08-29.

Kalshi market data and settlement history are public. Canadians cannot trade
there, but nothing prevents measuring it. The measurement half of this project
therefore needs no broker, no credential and no capital.

**Consequence:** `.env.example` is empty on purpose. Zero dollars spent in
Stage A. The Canadian-permitted filter is a registered analysis step, not a
trading plan.

---

## ADR-003. The power gate is committed before the measurement it judges

**Status:** accepted, 2026-08-29.

NPDExperiment closed at unresolved-at-achievable-power, MDE 0.0512 against an
effect band of 0.01 to 0.05, discovered after 415 days in the session that read
the result. InsiderExperiment registered its gate first and fired BLOCKED at
49.35 bp before spending.

**Consequence:** no statistic relating a price to an outcome is computed until
the gate fires. The gate reads bucket counts and dispersion only.

---

## ADR-004. A split verdict is a finding, not a failure

**Status:** accepted, 2026-08-29.

The unrestricted universe and the Canadian-permitted subset are judged
separately.

**Consequence:** if the unrestricted universe clears and the permitted subset
is BLOCKED, the registered reading is "the mispricing may be real and not
reachable from Canada." That is reported as a result.

---

## ADR-005. The document set follows ORBExperiment, the current house shape

**Status:** accepted, 2026-08-29.

The scaffold was first written with five markdown files, `## Section N`
registration headers, and a progress log in stage-entry form. That diverged
from ORBExperiment, which opened the same day and is the current shape:
seven binding documents, `## N.` registration headers numbered 0 through 17
with 17 reserved for amendments, a `HYPOTHESES.md` register, a `report.md`
written per stage and never revised, and a `progress.md` session log whose
Entry 0 is the operator prompt logged verbatim before any other work.

**Consequence:** the divergence is corrected before any measurement, so no
record is rewritten later. `HYPOTHESES.md` and `report.md` are added, the
registration is renumbered to the house shape with sections 5 through 16
stubbed, `progress.md` becomes a session log with Entry 0 reserved, and
CLAUDE.md carries sixteen numbered standing rules that later entries cite by
number. Four tests pin the shape so it cannot drift back.

---

## ADR-006. Stage A fires PENDING_ACCESS on the recorded terms, and the filter is never registered

**Status:** accepted, 2026-08-29.

The access gate (REGISTRATION.md Section 0.5) failed closed on three of five
conditions. The decisive one is condition 5: the Kalshi Data Terms of Use,
recorded before any repeated fetch, prohibit systematic retrieval into
datasets and expressly prohibit use of Kalshi Data in connection with AI
tools to generate output, absent prior written authorization; the API
Developer Agreement that would govern programmatic access returned an HTTP
429 bot challenge to every automated read attempted, and a source that
cannot be read is reported unavailable, never assumed permissive (standing
rule 5). The published benchmark study reached this data by registering an
account — the path ADR-002 excludes.

Technical reachability was fine — keyless HTTP 200 at ~100–214 ms across 11
single-shot requests — and the settled record exposes `result` beside final
prices. Access failed on permission and depth, not on plumbing: the keyless
settled listing reaches back only to between 2024-01-01 and 2024-05-31
(n = 6 bracketing probes), missing roughly the first three years of the
published benchmark's span.

**Consequence:** Section 0 reports on access, exactly as registered. Tasks 2
and 3 never ran: the Canadian-permitted filter was **not registered** and no
price bucket, dispersion, or power verdict exists. The registered sampling
machinery (seed 20260829, Wilson bound, buckets) stays registered and
unarmed. H1 remains OPEN at PENDING_ACCESS. Reopening paths are recorded in
REGISTRATION.md Section 15.1 and require either written authorization, a
sanctioned keyless bulk channel, or an operator reversal of ADR-002 by
numbered amendment.

---

## ADR-007. The rate-limit burst measurement is withheld: rule 12 outranks rule 4 here

**Status:** accepted, 2026-08-29.

Standing rule 4 says measured beats documented, and the stage prompt asked
for "the rate limits as measured." A rate limit is measured by driving
request pace until the venue pushes back — deliberately imposed load. With
the governing Developer Agreement unreadable and the readable terms
prohibiting bulk automated access, imposing probe load for measurement's own
sake is exactly what standing rule 12 (terms bind) exists to stop.

**Consequence:** the access table records the documented claim — Basic tier
200 reads/s, read from docs.kalshi.com on 2026-08-29 — labelled a claim, not
a measurement, with this ADR as the named deviation. The whole probe budget
was 13 requests, single-shot, spaced, no retries, no pagination beyond one
page. If access ever reopens under written authorization, the rate limit is
measured then, inside whatever pace that authorization names.

---

## ADR-006. Polymarket measures the phenomenon; transfer to a tradeable venue is a separate, untested hypothesis

**Status:** accepted, 2026-08-30.

Kalshi fired PENDING_ACCESS on terms rather than technology. Polymarket's public
read endpoints need no key, no authentication and no wallet, and settlement sits
on Polygon, so its data is public by construction rather than by permission.
Moving the measurement there satisfies standing rule 12 instead of circumventing
it.

**Consequence:** the measurement answers whether mispricing exists, not whether
it is reachable from Canada. Transfer is registered UNTESTED and may not be
assumed, on three grounds: a documented Kalshi bias reported not to replicate on
Polymarket, the largest Polymarket study finding no general longshot bias where
other work finds one on Kalshi, and MLCryptoEngine's H2 measuring cross-venue
transfer at AUC 0.501. Polymarket's documented mispricing also concentrates in
politics and sports, the two categories the Canadian-permitted subset excludes.

---

## ADR-007. The fee band fires before the power gate

**Status:** accepted, 2026-08-30.

Eleven MLCryptoEngine hypotheses closed on cost rather than signal, several after
data had been collected. The Canadian fee is flat at $0.02 per contract per side
against a $1.00 payout, so break-even requires the true probability to exceed the
market price by 2.0 points held to resolution, or 4.0 points round trip, before
spread and FX. Because the fee is flat in cents while the exploitable edge at
favourites is also small in cents, the requirement bites hardest exactly where
the documented bias lives.

**Consequence:** the band is computed from published effect magnitudes and the
fee schedule alone, reads no contract or outcome from any venue, and fires ahead
of the power gate. BAND-EMPTY closes the tradeable question on arithmetic before
a single contract is enumerated. The band is registered once and never recomputed
after a calibration result is seen.

---

## ADR-008. The terminal question admits a trade; the repository does not

**Status:** accepted, 2026-08-30.

The operator's goal has moved from measurement to finding a tradeable strategy,
and account creation is acceptable to him. Recording that as an amendment rather
than letting it drift keeps the register honest.

**Consequence:** no stage here places an order, holds a position, connects to a
broker, or stores a trading credential. The `CLAUDE.md` scope guard stands
unaltered and its test still passes. A tradeable finding is a finding; execution
is a separate decision with its own record. If the band closes the tradeable
question, the calibration work may continue only as a labelled phenomenon study
and may not be converted into a strategy.
