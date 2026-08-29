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
