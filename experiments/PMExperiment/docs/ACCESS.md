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
