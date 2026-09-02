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

---

## Note on numbering, recorded 2026-08-29, not repaired

This file carries **two ADR-006 entries and two ADR-007 entries**: the pair
dated 2026-08-29 (PENDING_ACCESS; the withheld rate-limit measurement) and the
pair dated 2026-08-30 (Polymarket; the fee band ordering). The collision is
recorded here rather than fixed, because the file is append-only and renumbering
a committed ADR would silently break the references already pointing at it —
`Makefile:24` and `docs/ACCESS.md:76` both cite "ADR-006/ADR-007" meaning the
2026-08-29 pair. **Cite an ambiguous number with its date.** Numbering continues
at ADR-009.

---

## ADR-009. The effect band is in probability points, and every published magnitude is exploitable only at a high entry price

**Status:** accepted, 2026-08-29.

Section 3 registers the band as "0.02 to 0.08 absolute probability points". That
wording was not taken on trust, because the cited sources lead with **returns**,
and the two units differ by the factor 1/p — an order of magnitude at the tails.
A 60 % loss on a 5c contract is 3 cents of mispricing, not 60.

**How it was established.** Each recorded magnitude was reconstructed both ways
and checked against the numbers the registration itself prints. The identity is
`return = gap ÷ price`.

| recorded figure | as a probability gap | as a return | which reproduces the record |
|---|---|---|---|
| Bürgi's 5c contract winning 3 % | 0.03 − 0.05 = **−0.02**, the recorded "2-point gap" | −0.02 / 0.05 = **−40.0 %**, the recorded "−40 %" | both, consistently |
| Bürgi's 95c contract winning 98 % | 0.98 − 0.95 = **+0.03**, the recorded "3-point gap" | 0.03 / 0.95 = **+3.16 %**, the recorded "+3.1 %" | both, consistently |
| Krause's −0.077 at longshots settling 4.0 % | implies a mean bucket price of 0.040 + 0.077 = **0.117**, coherent for a "below 30c" bucket | implies a mean price of 0.040 / 0.923 = **0.043**, and would make Krause's the *smallest* figure cited | only the probability reading |

The Krause row is decisive on its own: under the return reading, the figure
Section 3 calls "the largest single-category published figure" would be the
smallest of the three. **The band is in probability points. It is not
ambiguous, and no conversion is needed** — the fee is denominated identically,
$0.02 against a $1.00 payout being 0.02 of probability.

**One recorded magnitude that is not usable as an effect size.** Bürgi's
"buyers of contracts under 10c lose over 60 % of their money **after fees**" is
a return, and it is post-fee. Converted, it is 0.030 at 5c and 0.057 at 9.5c —
inside the band — but it already contains the venue's own fee, so using it
against a cost model would charge the fee twice. Section 3 set neither band edge
from it, and this records why.

**The consequential half of the finding: direction.** At longshot prices the
documented miscalibration is *over*pricing, so a buyer of a longshot holds a
negative edge, while break-even requires *under*pricing. On a binary venue the
exploitable expression is the complement. Restated in the underpriced direction,
every registered magnitude sits at a **high** entry price:

| source figure | exploitable side | entry price | underpricing |
|---|---|---|---|
| Bürgi, 5c winning 3 % | NO | **0.95** | 0.02 |
| Bürgi, 95c winning 98 % | YES | **0.95** | 0.03 |
| Krause, sub-30c settling 4.0 % | NO | **0.883** | 0.077 |

**Consequence.** The registered FX is proportional to entry price, so every
exploitable expression of the band is charged FX at 88–95c rather than at
5–12c. The unit determination and the FX treatment are therefore coupled, and
that coupling is what makes ADR-010's turnover question material rather than
academic. Two further facts travel with the band wherever it is used, and
neither is repaired here:

- **A scope mismatch.** The band is registered "in the tail cell (snapshot
  prices 1–10c and 91–99c)". Krause's exploitable complement at 88.3c lands in
  the 81–90 decile, outside that cell. The band is **not narrowed** on this
  ground — narrowing a registered band after seeing the arithmetic is precisely
  what Section 3 forbids — but the mismatch is stated wherever the band's top
  carries a conclusion.
- **An n that does not exist** (standing rule 13). Bürgi carries n = 313,972
  contract prices on 46,282 contracts across 12,403 events, and sets the band's
  bottom. **Krause's n is nowhere in the registration**, and Krause sets the
  band's top. The companion CPI study finding *no* classic bias carries n = 95
  contracts over 12 months. The band's bottom travels with a large n; its top
  travels with none.

---

## ADR-010. FX turnover: k = 1 binds, and it does not decide the verdict

**Status:** accepted, 2026-08-29. Registered as REGISTRATION.md Amendment 4
before the band gate fired.

Section 2 fixes the FX rate and its base but leaves implicit whether the charge
recurs per contract or is paid once per funding and shared across everything
that funding buys. Both readings are one formula with a turnover k —
`FX(p) = 0.03 · p / k` — and Section 2's single-contract participant is exactly
k = 1.

**Decision: k = 1 binds; k > 1 is reported beside it, never substituted.**
Section 2 forbids revising a cost component in the direction that helps H1, and
k > 1 lowers the floor in exactly that direction. Binding k = 1 also means a
surviving band cannot be manufactured by a generous assumption: k = 1
overstates FX for a repeat participant and biases toward BAND-EMPTY.

**Consequence.** `pmexperiment/band.py` takes turnover as a parameter defaulting
to `registry.FX_TURNOVER_REGISTERED = 1.0`, so the registered case binds unless a
caller names another and no registered constant goes unread. `docs/BAND.md`
reports k = 1, k = 12 and the k → ∞ limit side by side. A later stage that wants
k > 1 to bind needs its own numbered amendment carrying a **measured** turnover,
not an assumed one.

**What the decision did not cost.** The band's top clears the requirement at all
ten registered buckets on both exit routes under every k, and the band's bottom
clears at none of them under any k, so the verdict is invariant to the choice.
An assumption that is registered, argued, and then shown not to carry the result
is in the best position an assumption can hold.

**Recorded rather than tidied:** `registry.FX_TURNOVER_REGISTERED` was committed
in `9b4bd4f`, one commit *before* the Amendment 4 text it cites landed in
`4d75f66`. Both sit inside the same task and no verdict fired between them, but
the lag is real and is written down rather than rebased away.

---

## ADR-011. The volume floor is imported from the benchmark, not chosen here

**Status:** accepted, 2026-08-30. Registered as REGISTRATION.md Amendment 5
before Stage C enumerated anything. Numbering continues past the duplicate
ADR-006/ADR-007 pairs recorded above rather than renumbering them.

Section 1 required "a volume floor chosen and justified **before** it is
applied", and Stage A never armed the task that would have filled it in. The
danger in filling it now is plain: this is the one registered parameter whose
value directly moves the count the power gate consumes, and it is being set by
the same session that will go on to read that count.

**Decision: adopt the benchmark study's own floor — total traded volume ≥
$1,000 — verbatim from Section 3's record of Bürgi, Deng and Whelan.** A number
chosen by someone else, before this repository existed, for reasons unrelated to
this sample, cannot have been tuned to this sample; that is the specific failure
standing rule 9 exists to prevent. It also keeps the population comparable to
the one the registered effect band was measured on.

**Consequence.** The floor reduces every count the gate consumes and so biases
toward BLOCKED, against H1; it also removes contracts on which the registered
1-cent half-spread is undefined rather than merely uncertain. Its cost in sample
is reported on both universes as a first-class output. The benchmark's companion
spread filter is **not** adopted, because measuring it needs an order-book read
this stage does not perform, and a filter whose cost in sample cannot be
measured is worse than no filter at all.

**What would change it:** nothing in Stage C. A later stage may register a
different floor only by numbered amendment carrying its own evidence, and the
sample cost of both floors must then be reported side by side.

---

## ADR-012. Polymarket fails the access gate on the same clause class as Kalshi, and a claim about terms now requires a quotation

**Status:** accepted, 2026-08-30. Recorded as REGISTRATION.md Amendment 6 and
Section 15.3, with the evidence in `docs/ACCESS.md`.

Stage C read Polymarket's `robots.txt` on four hosts and its Terms of Use in
full before any repeated fetch. The terms prohibit "data mining tools, robots,
crawlers, or similar data gathering and extraction tools to scrape or otherwise
remove data", with no entity-type qualification, and their scope reaches anyone
"CONNECTING VIA AN API" and data taken "directly or through an API, or any other
means, including on-chain". The enumeration Stage C was to perform is that tool
class. **PENDING_ACCESS, zero market-data requests sent.**

**The decision this ADR exists to record is not the verdict. It is why the
verdict was a surprise.** Amendment 1 moved the entire measurement venue to
Polymarket on the stated ground that "the data is public by construction rather
than by permission" and that "standing rule 12 is satisfied here rather than
circumvented" — citing no terms document, no clause, no effective date and no
fetch date. It inferred **permission** from the absence of an **authentication**
requirement. Those are different properties, and the second does not imply the
first. Stage A had already demonstrated the gap on Kalshi, whose data was also
keyless and also prohibited.

**Registered practice, extending standing rule 12.** A claim in this repository
about what a venue's terms permit carries **a quoted clause, the document's
effective date, and the date it was fetched** — or it is recorded as unmeasured
and the stage proceeds as if permission were absent. Stage A's Kalshi finding
met that bar. Amendment 1 did not, and its ground is retracted by Amendment 6.
An operator who wants this in `CLAUDE.md`'s numbered rules should add it there;
it is recorded here so the practice binds regardless.

**Consequence, and what is deliberately not concluded.** Reachability, rate
limits and history depth were **withheld**, following ADR-007's precedence of
rule 12 over rule 4, because measuring them would itself be the prohibited act.
Whether a Polygon read through infrastructure that is not a Polymarket Interface
falls outside these terms is a **live question this repository has not
answered**, and it is recorded as a reopening path rather than taken as a
workaround. The counterargument that the API hosts may not be "Interfaces" as
defined is set out in full in Amendment 6 with three reasons it is not adopted;
the governing one is that a venue may not be held to a looser reading than
another because its verdict would be more convenient.

**The ordering clause earned its place.** Rule 12's "before any repeated fetch"
is what made the withholding possible: Stage A read 11 keyless market requests
before its terms position was established, Stage C read the terms first and sent
zero. That clause should not be softened.

---

## ADR-013. The Polymarket written-authorization route exists, is addressed to someone else, and the baseline stays PROHIBITED

**Status:** accepted, 2026-08-30. Evidence in `docs/LICENCES.md`. Numbering
continues past the duplicate ADR-006/ADR-007 pairs recorded above rather than
renumbering them.

Stage D asked whether a contact route exists through which a researcher could
request the written authorization both venues' terms name. **It does, and none
of the published routes is addressed to this asker.** `data-licensing@polymarket.com`
is the closest in subject matter and its own sentence opens "If you or your
clients are **Capital Markets Entities**"; the builder program's published
upgrade path is gated on "Route orders through Polymarket and demonstrate
consistent usage", which a repository that will never trade cannot pass; the
Terms' only Contact Us clause is scoped to "questions, complaints, or claims
concerning the Features"; and the Terms contain **no notices clause and no
postal address** — `Notices` 0 occurrences, `authorization` 0 occurrences across
58,830 characters.

**Decision: the candidate is recorded PROHIBITED as a baseline, and nothing is
drafted or sent.** The in-force Terms, effective 2026-08-11 under a genuine
`Effective as of` label and read in full as 14 contiguous chunks, prohibit the
tool class with no entity-type qualification and no consent proviso — the
proviso in the adjacent bullet attaches to *manual* processes, so even a granted
consent under it would not unlock automated collection.

**The label is deliberately precise. Nothing was requested, so nothing was
refused.** PROHIBITED here is what the Terms permit today absent authorization;
it is not a record that Polymarket declined. A later reader may not convert this
row into a refusal.

**Consequence, and the part that cuts against the verdict.** The verification
pass established three limits on how far this reaches: the load-bearing clause
was quoted **without its defined terms**, so its boundary is asserted rather
than measured; the bullet is scoped to "the Site, any other Interface, or
Features", and **a public Polygon ledger is none of the three on its face**, so
Amendment 6's Polygon question stays open rather than being closed here; and the
AI/ML axis is now **measured as a null** — `artificial intelligence` 0,
`machine learning` 0 across the Polymarket Terms. **Polymarket has no AI clause
where Kalshi has one**, and that asymmetry is recorded because it was unchecked
until the verification ran it, on the very clause class that decided Kalshi.

**Two corrections to this repository's own record, made here rather than left.**
First, **the Kalshi Data Terms of Use print no date at all** — `Effective` 0,
`Last Updated` 0 — so ADR-012's statement that "Stage A's Kalshi finding met
that bar" overstates it by one element: the finding met two of three. **This
changes no verdict**, because UNMEASURED and PROHIBITED both mean proceed as if
permission were absent, and it is recorded because a procedure that only ever
convicts other people's documents is not a procedure. Second, **Kalshi's Section
I PERMITTED USES was never disclosed here** and cuts both ways: it grants
personal, non-commercial access while conditioning AI/ML training and cached
data sets on prior written consent. Quoting only the prohibitions made the
framing one-sided.

---

## ADR-014. A dataset's licence is a separate question from its venue's, and the leading dataset fails ADR-012 on two elements

**Status:** accepted, 2026-08-30. Evidence in `docs/LICENCES.md`.

The premise Stage D was given is correct and is affirmed: **a dataset released
under a research licence may permit what the venue's terms do not, and the two
questions are separate.** The sweep found seven released corpora. The leading
one, `TimeSeventeen/Polymarket-v1`, states CC BY 4.0 three times, documents all
four inputs the power gate needs — entry price, category, maturity, and
resolution *presence* separable from resolution *value*, which is what standing
rule 8 requires — over 1,201,580,990 rows spanning 2022-11-21 to 2026-04-28.

**Decision: UNMEASURED, on ADR-012 elements (1) and (2).**

Element (2) fails because **neither the dataset card nor the CC BY 4.0 legal
code prints any date**, and there is no third document to fall back to. Element
(1) fails because the licence read quoted the two clauses of CC BY 4.0 that
grant and passed over the two in the same document that limit — Section 1
capping Licensed Rights to what "the Licensor has authority to license", and
Section 5(a) disclaiming warranties of title and non-infringement. **Element (1)
is measured as text present, not as an effective grant.**

**The tension this raises is registered rather than resolved.** ADR-012's
effective-date requirement was written against a mutable terms page a venue can
silently rewrite. Applied literally it makes it impossible for **any**
CC-licensed dataset ever to be recorded PERMITTED, because no Creative Commons
legal code prints a date. That is a serious argument and it is recorded at full
strength. It is not acted on: softening an evidence standard at the precise
moment it excludes the one attractive candidate, having applied it without
complaint to Kalshi and Polymarket when it excluded them, is what standing rule
9 exists to prevent. **The strongest form of the argument also fails on its own
document** — the legal code's footer points to an errata page carrying "the date
of change", so "the text does not drift" is contradicted by the text.

**Consequence: curing the date would not open this candidate, and no reader
should think it would.** Three gaps survive it. The chain of title is
unestablished — a third-party republisher's CC BY tag over a corpus derived from
another venue's platform is not a measurement that the republisher held the
rights to grant it. The AI/ML clause search, the class that closed Kalshi, is
**unrun** on the dataset LICENSE bodies and on Manifold's Terms of Service.
And whether a venue's terms reach a downstream on-chain-derived corpus is a
question Amendment 6 registered as **open**; "neither venue's terms govern this
candidate" is itself a positive claim about a document's reach, carrying no
clause and no date, and is restated as UNRESOLVED.

**What would change it:** a numbered amendment on version-identity-in-place-of-
date, registered *before* the measurement it governs and only alongside closing
element (1), the chain of title, and the AI-clause search.

---

## ADR-015. A third party's convenience is not permission, and PROHIBITED on an unread instrument is Amendment 1's error reversed

**Status:** accepted, 2026-08-30. Evidence in `docs/LICENCES.md`.

**Decision: PROHIBITED for Dune, the one in-scope platform measured; UNMEASURED
for Flipside, Allium, Nansen and Sim, whose governing documents were not
retrieved.**

Dune's in-force Terms of Service, labelled `Last updated on: June 3rd, 2026` —
a last-updated label, and the substitution for an effective label is disclosed
rather than smuggled — bind anyone "REGARDLESS OF WHETHER YOU HAVE REGISTERED
WITH DUNE AS A USER", prohibit "bots, crawlers, scrapers, or other automated
means" and any "mean other than Dune's provided interface", retain "all rights
to all elements of the Service", and grant only a **non-sublicensable**,
revocable right to use the *Services* — a right in a service, not in data.
Permission was searched for affirmatively rather than inferred from silence:
`aggregate`, `derived`, `redistribute`, `republish`, `resell`, `commercial use`,
`creative commons`, `open source`, `public domain` — **zero occurrences each**.
Programmatic query is account-gated with no keyless path, the API key issuing
only "After the User's subscription to a Subscription Plan", and the tier price
is recorded **UNMEASURED** because the pricing page is a client-rendered shell
at 0.14–0.40 % text and the figures a search summary offered came from no
document that was read.

**The decision this ADR exists to record is not the verdict. It is the error
the verification caught on the way to it.** The licence read declared Dune's
current Terms **unreadable** — "Cloudflare is fingerprinting the TLS/client, not
the headers" — quoted every clause from a superseded May 2025 archive, and
published PROHIBITED anyway. Both halves were wrong. Bare `curl` returns 403;
the same `curl` with nothing added but a browser `User-Agent` returns **HTTP
200**, and the in-force instruments were one header away. And **PROHIBITED on an
instrument that was never read is a synthesized value** — standing rule 5
forbids exactly that, and **ADR-012 has no direction-of-travel exemption**.

**This is Amendment 1's error with the sign reversed.** Amendment 1 inferred
*permission* from a document it never read; this read inferred *prohibition*
from a document it never read. The convenience rule of Amendment 6 — "a venue
may not be held to a looser reading than another because its verdict would be
more convenient" — is **symmetric**, and with a no-candidate outcome pre-blessed
as legitimate, an over-strict reading had become the convenient one. The verdict
above stands only because the in-force instrument was subsequently retrieved and
independently re-extracted; it does not stand on the archive.

**Consequence, independent of every clause above: Dune's terms nowhere establish
that Dune holds redistributable rights in the third-party prediction-market data
it surfaces.** Routing through a third-party platform cannot cure an upstream
position that has already fired PENDING_ACCESS. A third party's convenience is
not permission, and a platform that hosts a table is not thereby able to license
it onward.

---

## ADR-016. Kalshi's institutional desk did not decline on the merits, and the gate moves from permission to standing

**Status:** accepted, 2026-09-02, on correspondence received 2026-09-01.
Evidence in `docs/ACCESS.md`, "Kalshi — the institutional desk reply". Numbering
continues past the duplicate ADR-006/ADR-007 pairs recorded above rather than
renumbering, per the note of 2026-08-29.

**Decision: the Kalshi Internal Use route is recorded as EXISTS-AND-UNTRAVELLED,
and the claim that the use fits it is recorded UNMEASURED under ADR-012.** Both
labels are deliberate and neither is PERMITTED.

The reply reports three things. The use as described **fits Kalshi's Internal
Use data licence** — so it was **not declined on the merits**, and no merits
objection was raised at all. Applying requires **an established legal entity**
with formation documents and beneficial-owner verification. And the **2021
historical depth is available through historical endpoints** on the appropriate
licence, which are not subject to the live-data cutoff Stage A measured at
roughly spring 2024.

**The decision this ADR exists to record is not the label. It is that Stage D
was wrong in the exact way Stage D said it might be.** Stage D published "no
candidate returns PERMITTED" and "there is none" as a terminal state on
2026-08-30, and attached its own limit in the same document: the candidate space
was **sampled, not enumerated**, and *"there is none" is a verdict over what was
read.* **Two days later a route surfaced that Stage D had not read.** The limit
clause was not decoration and it was not modesty; it was correct, and it earned
its place in a way no test could have forced. **A completeness caveat that turns
out to be load-bearing within the week is the strongest argument in this
repository for writing them at all.**

**Admissibility, stated rather than glossed, because the prompt is right that it
is the interesting part.** Correspondence carries a **received date, not an
effective date** — a letter has no commencement clause and there is no second
document to fall back to. Fired through `pmexperiment.admissibility`, the claim
returns **UNMEASURED on element (2)**. The argument that a received date *is* the
effective date for an instrument that has no other is a good one, is recorded at
full strength in `docs/ACCESS.md`, and is **not adopted** — not because it is
weak, but because element (2) was written against a mutable page a venue can
silently rewrite, and amending it at closure to govern a measurement that will
never be made is worse than leaving the question open.

**And the honest asymmetry against ADR-014, which this ADR will not claim credit
for.** ADR-014 held this standard when holding it excluded the one attractive
candidate, at real cost. **Here holding it costs nothing**, because the entity
requirement closes the route whichever way admissibility falls. Applying a rule
when it is free is not evidence that the rule is being applied.

**A second gap, and it is the larger one.** Element (1) requires **a quoted
clause**, and what this repository holds is **the operator's summary of the
reply, not its text**. No sentence of the correspondence is quoted anywhere
here. **Firing the procedure over it exposed a blind spot in the procedure**:
`missing_elements()` checks only that `clause` is non-empty, so it would score a
paraphrase as satisfying element (1) when ADR-012 plainly does not. **The check
is weaker than the ADR it implements, and this is the first claim that showed
it** — every earlier claim was fired over a document this repository had itself
fetched, where the distinction never arose. It is **recorded and deliberately not
repaired**: adding a detector at closure, to a gate governing measurements that
will never run, is scope in the wrong direction, and no honest detector exists —
quotation marks are not evidence of quotation.

**What the reply does not establish, because finding 1 will otherwise be read as
a green light.** Nothing was applied for, so **nothing was granted and nothing
was refused**. The fee is **UNMEASURED**. Whether an Internal Use licence permits
**publishing** a calibration result is **UNRESOLVED** and is the sharpest of
these — the licence is named for internal use, this repository exists to publish,
and the instrument was never read. Whether it carries the **AI/ML written
consent** that Kalshi's Section I conditions separately — the clause class that
closed Kalshi in Stage A — is **UNRESOLVED**. **An established legal entity is a
necessary step on this route, not a sufficient one.**

**Consequence for Stage A, recorded because it is the good kind of surprise.**
Finding 3 does not touch Stage A's measurement. Stage A wrote that the
2021→Apr 2025 span is *"not reproducible keylessly"* — a claim about the keyless
surface, not about the archive — and that phrasing is exactly right under the
reply. **Had it been written as "the history does not reach 2021" it would now
be false.** The depth finding is an input to power that is now known to be
obtainable on a route this repository will not travel; **no count, bucket or
dispersion exists for any Kalshi universe**, so nothing whatever follows from it
for the power gate, which has still never fired.

---

## ADR-017. The entity path is declined by the operator, and a declined cost is not a finding

**Status:** accepted, 2026-09-02. Recorded as REGISTRATION.md Amendment 7, with
the route it declines recorded in Section 15.4 and ADR-016.

**Decision: both routes to the established legal entity that a Kalshi Internal
Use application requires are declined by the operator.** Institutional
sponsorship through the university was consulted and judged **not achievable
within the time available**, with fourth-year term starting. Forming a personal
legal entity was judged **disproportionate** to a stated prior of **5 to 8
percent** against a band verdict already recorded as thin — the surviving region
being the top **2.15 of 6.0 points** at 95c, requiring **5.85 points** at k = 1
against a band top of **8.00**, with every magnitude cited inside that bucket
failing the **0.0300** cost floor.

**The decision this ADR exists to record is the category, not the outcome.**
This is **the operator declining a cost. It is not a discovery, and it is not
evidence about H1.** Every prior closure in this repository — PENDING_ACCESS
twice, three licence verdicts, BAND-OPEN — rests on a document or on arithmetic
over registered constants. **This one rests on a person's judgement about their
own time and money**, and it is filed in a different category deliberately so
that no later reader collapses the two.

**Why the distinction is worth an ADR rather than a sentence.** A repository
that closes on access and a repository that closes because its operator stopped
paying look identical from the outside — both end with no measurement. They are
not the same finding, and only one of them is a finding at all. **Recording the
difference is the only thing that keeps the access verdicts meaning what they
say.** If this ADR were folded into the closure verdict, a later session could
read the whole project as "the data was unreachable" when the accurate reading is
"the data was unreachable on the routes read, one route opened, and the operator
declined the cost of standing up to it."

**The prior is recorded and is explicitly not pre-registered.** Section 13 was
never filled and is left empty permanently; the 5-to-8-percent figure arrives at
closure, **after** two gates had fired, and Amendment 7 records that it may never
be described as pre-registered. **The empty Section 13 is a truer record than a
filled one**, and this repository would rather carry a visible gap than a
plausible-looking backfill. It is recorded at all because a cost decision whose
input is unrecorded cannot be audited — and because a prior of 5 to 8 percent
makes **a null the modal expected outcome**, which is the frame the closure
should be read in.

**Consequence: Kalshi did not refuse.** The desk raised no merits objection.
**This repository declined**, and Section 15.4's label stays
EXISTS-AND-UNTRAVELLED rather than becoming anything that reads as a refusal —
the same discipline ADR-013 applied to Polymarket, where nothing was requested
so nothing was refused. Here something was answered and nothing was applied for.

---

## ADR-018. The project closes on access and standing, and the closure is filed as a terminal state rather than a result about H1

**Status:** accepted, 2026-09-02. The closing decision. Recorded as
REGISTRATION.md Section 15.5 and Amendment 8, with the register updated in
HYPOTHESES.md and the stage reported in `report.md`.

**Decision: PMExperiment closes. H1 is unmeasurable at this house's standard —
not disproven, not unlikely, unmeasurable.** Both venues closed on their own
terms, all three licence candidates failed, and the one route that exists was not
declined on the merits but is gated on an established legal entity the operator
does not hold and has decided not to create (ADR-016, ADR-017).

**The decision this ADR exists to record is the category of the ending.** Five
stages produced **no contract, no price bucket, no dispersion and no statistic
relating a price to an outcome.** An ending with no measurement in it can be
filed two ways, and only one of them is honest here:

| filing | what it would claim | why it is wrong |
|---|---|---|
| **a result about H1** | the effect is absent, or small, or not worth pursuing | **nothing was ever measured against H1.** No such claim has any support in this repository |
| **a terminal access finding** | the question could not be reached at this house's evidence standard, by this operator, on the routes read | what actually happened |

**It is filed as the second, and the guard is a test.** The terminal verdict, the
BAND-OPEN caveat and the three reopening conditions are now pinned in
`README.md`, `REGISTRATION.md` and `HYPOTHESES.md`, verified by **fourteen
mutations, all fourteen load-bearing** — the suite fails when the verdict is
softened to "unlikely", when the BAND-OPEN caveat is stripped, when a reopening
condition is dropped, when the no-fourth-venue guard is removed, when a pending
reply is promoted into a reopening, when the route is rewritten as a refusal by
Kalshi, when the entity decline is reframed as evidence about H1, when the prior
is described as pre-registered, when Section 13 is backfilled, when the closure
is passed off as Section 16's registered closure, when the price reading is
rounded to "never", when Stage D's vindicated caveat is deleted, when the
procedure's blind spot is concealed, and when the correspondence is promoted to
an effective-dated instrument.

**The registered closure conditions were never met, and the closure does not
pretend otherwise.** Section 16 provides for H1 to close when **both verdict
cells fire BLOCKED**, with realized MDEs and their n beside them. **Neither cell
ever fired.** There is no realized MDE because there is no enumeration to compute
one from. **H1 does not close under Section 16 at all**; it terminates on access
and standing, an ending Section 16 did not contemplate. Section 16 is annotated
to say so and is otherwise left exactly as registered on 2026-08-29, so a reader
can see the gap between what the design provided for and what happened.

**Consequence for the one number this repository produced.** **BAND-OPEN is a
cost finding computed from registered constants with no calibration measurement
behind it, and it must not be written anywhere as evidence that an edge exists.**
Amendment 2 fixed the band as computed once; no reopening recomputes it, adds a
bucket to it, or converts it into a result. A reopened measurement starts at the
power gate over 91–99c held to resolution and nowhere else.

**And the closing observation, which is not comfortable.** This repository was
built against NPDExperiment's failure, which was a failure of **power** — a
design that could not have detected an effect anywhere in the range it was
testing, discovered after 415 days. Five stages here produced **zero coverage
figures**: no bucket count, no dispersion, from any route. **If an authorization
arrived tomorrow, the power question would still be unanswered.** Following
Insider rather than NPD saved 415 days and every dollar; it did not answer the
question the whole design was built to answer, and nothing in this repository
should be read as though it had.

---

## ADR-019. Trading access and data permission are separate instruments

**Status:** accepted, 2026-09-02.

Raised after closure: would Polymarket becoming available to Canadians reopen
H1? No tracked document answered it, and the inference is one a careful reader
would make in good faith.

Stage C closed Polymarket on its data terms. The crawler prohibition carries no
entity-type qualification and the data clause reaches material taken directly,
through an API, or by any other means including on-chain. A CIRO authorization
governs who may trade, not who may extract.

**Consequence:** registered as a general rule under ADR-012 rather than as a
Polymarket fact — a regulatory change to trading access is not evidence about
data permission, and the two are measured separately. A Polymarket data licence
is added as a fourth reopening condition, with Canadian trading access recorded
as neither necessary nor sufficient for it.

---

## ADR-020. A shared test reader is not the place to fix one test's problem

**Status:** accepted, 2026-09-02.

Three new assertions failed on bold markers inside the sentences they checked.
Stripping `*` in the shared `_read` fixed them and silently changed what four
pre-existing assertions were checking, since those had been matching text that
includes the markers.

**Consequence:** normalization is scoped to the tests that need it.
`_read_unstyled` exists for content assertions; `_read` is unchanged for the
tests written against it. Widening a shared fixture to fix a local failure is a
silent rewrite of every test that depends on it.

---

## ADR-021. A mutation must be proven to have mutated

**Status:** accepted, 2026-09-02.

Two mutation attempts targeted a phrase hard-wrapped across a line. Neither
`sed` nor a literal `str.replace` matched, the document was never altered, and
the passing suite briefly read as a green mutation result. This is Entry 7.1's
fault in a third form and the second time this repository has caught it.

**Consequence:** a mutation run reports whether the document changed, and a
mutation that fails to alter its target is reported as inconclusive rather than
counted. Patterns are whitespace-tolerant, because the documents hard-wrap.
