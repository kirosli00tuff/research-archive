# ACCESS.md — measured access, per source, with dates

Written by Stage A Task 1 on 2026-08-29. Every figure below was measured on
that date unless labelled a documented claim. Refusals fail closed: a source
that could not be read is reported unavailable, never assumed permissive.

## Verdict

**PENDING_ACCESS** (REGISTRATION.md Section 0.5). Conditions 1 and 2 pass;
conditions 3 and 4 fail closed as unmeasured or undemonstrated; condition 5
fails closed on the recorded terms. Section 0 therefore reports on access,
not on the hypothesis, and Stage A ends here as a valid outcome.

## The access gate, condition by condition

| # | condition | reading | evidence |
|---|---|---|---|
| 1 | settled markets enumerable over HTTP without credential | **PASS** | `GET /trade-api/v2/markets?status=settled` keyless: HTTP 200 in 127.6 ms, 2 records returned, 2026-08-29 |
| 2 | resolution outcome exposed on the settled record | **PASS** | `result` field present, alongside `last_price_dollars`, `settlement_value_dollars`, `settlement_ts`; verified on 2 records against the registered cap of 5; no statistic computed |
| 3 | ≥ 1,000 settled markets enumerable in total | **NOT MEASURED — fails closed** | counting requires systematic pagination of the full listing, which the recorded terms (condition 5) do not sanction without written authorization; a single page of 20 returned with a continuation cursor, so the count is > 20 and otherwise unknown |
| 4 | price history retrievable to 30 days before close | **NOT DEMONSTRATED — fails closed** | candlesticks endpoint works keylessly on a just-settled traded market (1 candle, fields `price`, `yes_bid`, `yes_ask`, `volume_fp`, `open_interest_fp`); the one ≥ 30-day-old settled market tested (`NASDAQ100-24OCT25-T21499.99`, closed 2024-10-25) returned HTTP 200 and **0 daily candles** over T−40d..T; ambiguous, counted as ambiguous, attributed to nothing |
| 5 | recorded terms and robots.txt do not forbid keyless automated reading | **FAIL — fails closed** | see "The terms, as recorded" below |

## The terms, as recorded (before any repeated fetch, per standing rule 12)

**Kalshi Data Terms of Use** — fetched 2026-08-29 from
`https://kalshi-public-docs.s3.amazonaws.com/kalshi-data-terms-of-service.pdf`.
Scope on its face: content on the kalshi.com Website, defined to include
prices, settlement prices, volumes and related information ("Kalshi Data").
Permitted: "access content only for your personal use for non-commercial
purposes," "only … in the form in which it is presented on the Website."
Prohibited without prior written authorization: "collecting, copying,
reproducing, downloading … compiling (including, without limitation, through
framing or systematic retrieval to create collections, compilations,
databases or directories)"; "use of any … scripts, software, spiders, robots
… to navigate, access, copy in bulk, retrieve, harvest, index, search or
analyze any portion of the Website"; and, in bold in the original: "use of
any Kalshi Data (including associated metadata) in any manner for any machine
learning and/or artificial intelligence … or otherwise for the purposes of
using or in connection with the use of such technologies, tools, or models to
generate any information, material, data, derived works, content, or output
is expressly prohibited."

**API Developer Agreement** — `https://kalshi.com/developer-agreement`,
**unreadable by automated means on 2026-08-29**: curl and server-side fetch
both received HTTP 429 with a Vercel bot-challenge page; a headless-browser
render timed out at the same checkpoint. The Internet Archive capture of
2026-02-14 preserves only the page shell, whose own description reads: "The
terms and conditions for programmatic trading on Kalshi."
`https://docs.kalshi.com/welcome` (fetched 2026-08-29) states: "By continuing
to use or access Kalshi's API, you are agreeing to be bound to our Developer
Agreement." The agreement this project would be bound by could not be read,
and a source that cannot be read is reported unavailable, never assumed
permissive.

**robots.txt** — `api.elections.kalshi.com/robots.txt`: HTTP 404 in 0.114 s
(no crawl directives published on the API host). `kalshi.com/robots.txt`:
HTTP 429 bot-challenge page in 0.071 s (the Website refuses unauthenticated
automated readers before robots.txt is even served).

**The published research path.** The strongest calibration study of this
venue (Bürgi, Deng and Whelan 2026) states it "registered with Kalshi to get
access to their Application Programming Interface." The sanctioned bulk
research path runs through registration — exactly what ADR-002 registered
this project away from.

## Measured figures beyond the gate

| quantity | measured value | date |
|---|---|---|
| keyless API reachability | HTTP 200, latencies 99.9–213.8 ms across 11 requests | 2026-08-29 |
| settled-history depth | earliest retrievable settled close sits **between 2024-01-01 (empty page) and 2024-05-31 (present)**, bracketed by `max_close_ts` probes at 2021-08-01, 2022-01-01, 2023-01-01, 2024-01-01 (all empty) and 2024-07-01, 2025-01-01 (both non-empty) | 2026-08-29 |
| depth vs the published benchmark | the 2021→Apr 2025 span analyzed by Bürgi-Deng-Whelan is **not reproducible keylessly**: roughly the first three years of settlements are absent from the keyless listing | 2026-08-29 |
| outcome exposure | `result` present on settled records together with final prices | 2026-08-29 |
| rate limit, documented claim | Basic tier 200 reads/s (docs.kalshi.com/getting_started/rate_limits, read 2026-08-29); tiers are defined for API-key holders | claim, not a measurement |
| rate limit, measured | **withheld** — a burst probe imposes load for measurement's sake on a venue whose governing agreement could not be read; standing rule 12 (terms bind) takes precedence over rule 4 (measured beats documented) here, recorded as a deliberate deviation in DECISIONS.md ADR-007 | 2026-08-29 |

## Request log

13 outbound requests total on 2026-08-29, all keyless, single-shot, spaced
≥ 1.5 s where consecutive, no retries: 2 robots.txt fetches (429, 404) and
11 API reads — 2 settled-listing reads (limit 2, which is also the
reachability read, and limit 20), 6 depth brackets at `max_close_ts`
boundaries, and 3 candlestick reads (2 returned zero candles, 1 returned one
candle). The two
terms documents and the rate-limit docs page were read through ordinary
page fetches, not the API. No request enumerated beyond a single page; no
dataset was compiled; the raw probe responses were not retained beyond this
report and the two tickers named above.

---

# Polymarket — measured 2026-08-30 by Stage C

## Verdict

**PENDING_ACCESS.** Section 0.5's condition 5 fails closed: the published terms,
recorded before any repeated fetch, do not sanction the systematic keyless
reading this measurement requires. **Zero market-data requests were sent** — no
contract, price, order book or resolution was requested — and the power gate did
not fire. Amendment 6 records that this also falsifies Amendment 1's stated
ground for moving the venue here.

## robots.txt, on every host this stage would have used

| host | status | latency | content |
|---|---|---|---|
| `polymarket.com` | **200** | 35.7 ms | 73 bytes: `User-agent: *` + `Sitemap: https://polymarket.com/sitemaps/sitemap-index.xml`. **No `Disallow` of any kind.** |
| `gamma-api.polymarket.com` | 404 | 280.1 ms | `404 page not found` — no crawl directives published |
| `clob.polymarket.com` | 404 | 201.4 ms | nginx 404 — no crawl directives published |
| `data-api.polymarket.com` | 404 | 220.9 ms | `404 page not found` — no crawl directives published |

**robots.txt is permissive, and it is not the governing document.** The website
publishes no crawl restriction at all — a genuine contrast with Kalshi, whose
website returned an HTTP 429 bot challenge before robots.txt was even served.
Standing rule 12 requires both robots.txt **and** the published terms; where they
disagree, a permissive robots.txt does not licence what the terms prohibit.

## The terms, as recorded (before any repeated fetch, per standing rule 12)

**POLYMARKET.COM TERMS OF USE**, effective **2026-08-11**, published by
Adventure One QSS, Inc. Retrieved 2026-08-30, 59,617 bytes.

*How it was retrieved, recorded because it took work:* `polymarket.com/tos`
returns HTTP 200 in 198 ms but is client-rendered — its 217 KB body strips to
1,354 characters of text, and its Next.js flight payload (129 KB) carries only
the app shell, under a route segment named `(embedded-docs)/tos`. The terms are
an embedded document, retrieved from the `docs.google.com` document that payload
references (HTTP 200, 578 ms). **The first two reads did not contain the terms,
and reporting from them would have been reporting on a page shell.**

**Prohibited conduct, quoted verbatim, with no entity-type qualification:**

> Use any data mining tools, robots, crawlers, or similar data gathering and
> extraction tools to scrape or otherwise remove data from the Site, any other
> Interface, or Features;

> Use any manual process to monitor or copy any of the material on the Site, any
> other Interface, or Features or for any other unauthorized purpose without our
> prior written consent;

> Harvest or otherwise collect information from the Site, any other Interface,
> or the Features for any unauthorized purpose;

**Scope, quoted verbatim — the terms reach API and on-chain access by name:**

> BY ACCESSING, INTERACTING WITH OR USING THE SITE, ANY FEATURE OR ANY OTHER
> INTERFACE (INCLUDING BY CONNECTING VIA AN API, LINKING YOUR WALLET, OR
> OTHERWISE CREATING AN IDENTIFIER ON THE SITE) … YOU AGREE … TO BE BOUND BY THE
> TERMS

> Access or use any data, content, or information contained on our Site, any
> Interface or Features directly or through an API, or any other means,
> including on-chain, whether in raw, derived, aggregated, or anonymized form
> (the "Data") if you are (i) a non-retail, professional entity that engages in
> capital markets activities … or (ii) a market data distributor, in each case
> unless otherwise agreed to in writing by us

**The Data clause is conditional and does not bind a retail researcher.** Its
prohibition attaches to capital-market entities and market-data distributors,
and a Canadian retail individual doing measurement-only research is neither. It
is quoted here for its **scope language**, which establishes that the Terms
contemplate and govern API and on-chain access — not as the ground of the
verdict. The ground is the unconditional data-mining and crawlers bullet above.

**Geographic scope, recorded though not the ground:**

> USE OF THE SITE, PLATFORM OR TECHNOLOGY FEATURES FOR TRADING IS NOT PERMITTED
> BY PERSONS OR ENTITIES WHO RESIDE IN … ALBERTA … BRITISH COLUMBIA … ONTARIO …
> QUEBEC …

> If you are in a Restricted Jurisdiction (as defined below), you are only
> permitted to use the Content Features on the Site or any other Interface and
> may not use the Site or any other Interface for any other purpose

Four Canadian provinces are named individually. For a participant in them,
permitted use narrows to the Content Features — "news and information about
global current events" — and no other purpose.

**Clauses that do *not* exist in the document**, checked and recorded as absent
rather than assumed: no occurrence of "spider", "automated", "systematic",
"machine learning", "artificial intelligence", or "Canada" as a country-level
term. The AI-use prohibition that decided Kalshi has **no** counterpart here;
this finding rests on the crawlers bullet alone.

## The developer documentation, measured

`docs.polymarket.com`, HTTP 200 in 268.6 ms, 396 KB. Publishes "Rate Limits —
Cloudflare IP-based request limits for Polymarket APIs", "CLOB Trading Rate
Limits", and a builder program with tiers. Occurrences of "terms of use": **0**.
Of "license"/"licence": **0**. Of "acceptable use": **0**. Of "public data":
**0**. **No separate developer agreement grants what the Terms of Use withhold**,
and no published licence makes the market data free to compile.

## Reachability, rate limits and history depth — withheld, not measured

**Deliberately not measured, following ADR-007's precedent of 2026-08-29.** Each
of those figures requires sending market-data requests to a venue whose recorded
terms prohibit the tool class that sends them. Standing rule 12 outranks
standing rule 4 exactly here: measuring would itself be the prohibited act.
Reported as withheld — never as zero, and never as unknown-therefore-fine.

**The ordering did the work.** Rule 12 requires the terms be recorded *before any
repeated fetch*. Stage A read 11 keyless Kalshi market requests before its terms
position was established; Stage C read robots.txt and the terms first and sent
**zero** market-data requests to Polymarket.

## Request log

**7 requests to Polymarket hosts on 2026-08-30**, all single-shot, spaced ~2 s,
no retries, no pagination: 4 `robots.txt` (200, 404, 404, 404), 1 `/tos` page
(200, 198 ms), 1 `docs.polymarket.com` (200, 269 ms), 1 rendered read of `/tos`.
Plus 1 request to `docs.google.com` for the embedded terms document (200,
578 ms). **No request asked for a contract, a price, an order book, a resolution
or a listing of any kind. No dataset was compiled, and `data/raw/` is empty for
this venue.**

---

# Kalshi — the institutional desk reply, received 2026-09-01, recorded by Stage E

## Verdict

**EXISTS-AND-UNTRAVELLED.** A route exists and was **not declined on the
merits**; it is gated on an established legal entity, and **nothing was applied
for, so nothing was granted and nothing was refused**. The claim itself is
recorded **UNMEASURED** under ADR-012 — correspondence carries a **received
date, not an effective date** — and UNMEASURED here means *not checkable in the
required form*, never *doubted* and never *PROHIBITED*.

**This section records correspondence, not a probe.** Stage E sent no request to
any Kalshi endpoint and to no other host. The reply reached the operator and was
read here. **Zero market-data requests, zero contracts, zero dollars**, and no
contract, price, order book or resolution was asked for or received.

**It is recorded because it changes the register.** Stage D closed on 2026-08-30
with "no candidate returns PERMITTED" and wrote it as terminal, while attaching
its own limit: *"There is none" is a verdict over what was read, and it is not a
proof that no permitted route exists.* **That limit was vindicated in two days.**
A route exists, and Stage D had not read it.

## What the reply reports

Three findings, each **as reported by the operator** and none of them verified by
this repository against a published instrument:

| # | finding | what it changes |
|---|---|---|
| 1 | the use as described **fits Kalshi's Internal Use data licence** | **the route was not declined on the merits.** No merits objection was raised at all |
| 2 | applying requires **an established legal entity**, with formation documents and beneficial-owner verification | the gate moves from *permission* to *standing*. An individual undergraduate holds no such entity |
| 3 | the **2021 historical depth is available through historical endpoints** on the appropriate licence, which are **not** subject to the live-data cutoff | Stage A's keyless cutoff at roughly spring 2024 is a property of **the keyless surface**, not of the archive |

## The date this carries, and what it does to admissibility under ADR-012

**Received 2026-09-01. It carries no effective date, because correspondence has
none** — a letter is not a published instrument with a commencement clause, and
there is no second document to fall back to. This is stated rather than glossed,
because the whole of ADR-012 is that a claim about permission must be checkable
by someone who was not there.

**Fired through `pmexperiment.admissibility` as a claim, it returns UNMEASURED.**
Element (2), the effective date, is absent and no substitute is registered.
That verdict does **not** mean the reply is doubted; UNMEASURED is not a synonym
for PROHIBITED, and it is emphatically not a synonym for untrue. It means the
claim is not checkable in the form ADR-012 requires.

**The argument for admitting it, stated at full strength.** Correspondence takes
effect on receipt. The received date is functionally the effective date for an
instrument that has no other, and ADR-012's effective-date element was written
against **a mutable terms page a venue can silently rewrite** — a hazard a dated
private reply does not have. On that reading element (2) is satisfied by the
received date and the claim is ADMISSIBLE. It is a good argument and it is not
adopted here.

**Why it is not adopted, and the reason is not the one that would flatter this
procedure.** ADR-014 refused to soften this standard when strictness excluded
the one attractive candidate, at real cost. **Here strictness costs nothing** —
finding 2 closes the route whichever way admissibility falls, so applying the
rule strictly buys no protection and earns the procedure no credit. It is
applied strictly anyway, for consistency and for one substantive reason: a
version-identity or receipt-date amendment to element (2) would be a **general**
change to the standard, and registering a general change at closure, to govern
a measurement that will never be made, is worse than leaving it open.

**A second gap, larger than the first, and this one is not curable by
amendment.** Element (1) requires **a quoted clause**. What this repository
holds is **the operator's summary of the reply, not its text.** The three
findings above are a paraphrase; no sentence of the correspondence is quoted
anywhere in this repository.

**And firing the procedure exposed a blind spot in the procedure itself.**
`missing_elements()` tests that `clause` is non-empty. It cannot tell a
quotation from a summary, so it would score the paraphrase above as satisfying
element (1) when ADR-012 plainly does not. **The check is weaker than the ADR it
implements, and this is the first claim that showed it** — every earlier claim
was fired over a document the repository had itself fetched, where the
distinction never arose. **It is recorded and deliberately not repaired.**
Adding a quotation detector at closure would be a change to a gate written for
measurements that will never run, and no honest detector exists anyway: quotation
marks are not evidence of quotation.

## What the reply does not establish, reported absent rather than as zero

| question | state |
|---|---|
| is a licence granted? | **No. Nothing was applied for, so nothing was granted and nothing was refused.** The reply describes a route; it is not the route travelled |
| the fee, if any, for an Internal Use licence | **UNMEASURED.** No figure was reported and none is assumed |
| does Internal Use permit **publishing** a calibration result? | **UNRESOLVED, and it is the sharpest of these.** The licence is named for internal use; this repository exists to publish a public report. The instrument was never read, and a name is not a clause |
| does an Internal Use licence carry the **AI/ML written consent** Kalshi's Section I PERMITTED USES conditions separately? | **UNRESOLVED.** That clause class is what closed Kalshi in Stage A; whether this licence satisfies it is unread |
| what the historical endpoints actually return, at what depth and coverage | **UNMEASURED — never requested.** No count, no bucket, no dispersion exists for any Kalshi universe |

**The consequence of the last two rows, stated so no reader mistakes finding 1
for a green light: an established legal entity is a necessary step on this
route, not a sufficient one.** Three further documents would have to be read
after it, and none of them has been.

## What this does to Stage A's measured finding

**Nothing, and that is worth recording.** Stage A measured the earliest
retrievable settled close as sitting between 2024-01-01 and 2024-05-31 (n = 6
bracketing probes) and wrote the consequence as **"the 2021→Apr 2025 span
analyzed by Bürgi-Deng-Whelan is *not reproducible keylessly*."** Finding 3 says
the archive exists behind the licence. **The measurement stands and so does its
phrasing** — it reported a property of the keyless surface and claimed nothing
about the archive. Had it been written as "the history does not reach 2021", it
would now be false. **The careful phrasing was load-bearing and it held.**

**What finding 3 does change is a power input, and only in principle.** A
2021-onward settled history is a larger sample than a 2024-onward one. **No
count exists for either**, no bucket was ever built, and no dispersion was ever
computed, so nothing follows from this for the power gate — which has still
never fired. Recorded as an input that is now known to be **obtainable on a
route this repository will not travel**, never as a number.
