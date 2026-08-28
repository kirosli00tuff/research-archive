# docs/ACCESS.md — A.1 access verification, measured live

**Every figure below was measured by this repository on 2026-08-28 UTC, with
its n.** Where a source documents something, the documented text is quoted
verbatim and **labelled `documented`**; under standing rule 3 the measured
figure wins wherever the two meet.

**Terms of service were recorded before the first repeated fetch of any
source.** The `robots.txt` sweep (n = 8 hosts) ran as the first network
activity of this repository, at 2026-08-28T19:57Z, before any data surface was
touched. Request ledger totals at the close of A.1 Task 1: **47 charged
requests** (13 flow, 4 archive, 30 venue), 41 settled 200, 5 settled 404, 1
settled 401. **Zero dollars. No key, token or credential was used or exists.**

---

## 1. Terms of service and robots.txt — recorded before the first repeated fetch

| host | HTTP | verdict | the directive that decides it |
|---|---|---|---|
| `farside.co.uk` | **200**, 33 bytes | **PERMITTED** | names one agent only; no `*` group exists |
| `sosovalue.com` | **200**, 682 bytes | **PERMITTED** for the path used | `*` group disallows query-string and tab patterns; the path used matches none |
| `www.theblock.co` | **200**, 668 bytes | **DISALLOWED for the data endpoint** | `Disallow: /api/` under `User-agent: *` |
| `glassnode.com` | **200**, 152 bytes | **DISALLOWED for the data endpoint** | `Disallow: /api` under `User-agent: *` |
| `api.glassnode.com` | **401** | **NOT KEYLESS** | robots.txt itself is behind auth |
| `archive.org` | **200**, 238 bytes | **PERMITTED** | disallows `/control/` and `/report/` only |
| `web.archive.org` | **404** | **PERMITTED** | no robots.txt is served |
| `api.hyperliquid.xyz` | **404**, 0 bytes | **PERMITTED** | no robots.txt is served |
| `api.kraken.com` | **404** | **PERMITTED** | no robots.txt; the path returns an API error object |

### farside.co.uk/robots.txt — verbatim, in full (33 bytes)

```
User-agent: Twitterbot
Disallow:
```

**Reading, stated because it is load-bearing.** The file contains exactly one
group and that group names `Twitterbot`. There is **no `User-agent: *` group**.
Under RFC 9309 a crawler that matches no specific group and finds no wildcard
group has no applicable rules, so **`robots.txt` places no restriction on this
repository's collector**. `https://farside.co.uk/terms-of-use/` returns **404**
(n = 1); the only legal page linked from the site is
`https://farside.co.uk/privacy-policy/` (**200**, 69,457 bytes), which is a
**GDPR personal-data notice and says nothing about automated collection or
data reuse**. The site footer carries `© 2025 Farside Investors. All rights
reserved.`

**No stated prohibition exists, so collection proceeds. Attribution is carried
in every artifact as `Source: Farside Investors`, which is the attribution the
source itself prints beside the table.**

### www.theblock.co/robots.txt — the clause that closes it

```
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=yes
Disallow: /search
Disallow: /api/
Disallow: /preview/
Disallow: /wp-json/
Disallow: /ping
Disallow: /tbco/prebid.js
```

The rendered page (`/data/crypto-markets/bitcoin-etf`, **200**, 735,287 bytes)
contains **no `<table>` element and no server-rendered daily series**; the
values are fetched at runtime from `https://www.theblock.co/api/tbco`, which
**`Disallow: /api/` forbids**. **The endpoint was therefore never requested.**
TheBlock is recorded **DISALLOWED** and routed out of the candidate set. This
is the HFExperiment Wealthsimple precedent applied: a stated prohibition ends
the enquiry rather than prompting a workaround.

### glassnode.com/robots.txt — the clause that closes it

```
User-agent: *
Allow: /
Disallow: /signals
Disallow: /api
```

`https://glassnode.com/charts` returns **404** (n = 1) and
`https://api.glassnode.com/robots.txt` returns **401** behind Cloudflare, so
the data host is not keyless. **Glassnode is recorded DISALLOWED-and-not-keyless
and routed out.** Its endpoint was never requested.

---

## 2. The flow candidates — what the bytes actually contain

### 2.1 Farside Investors — **selected as the primary flow source**

| probe | result |
|---|---|
| `https://farside.co.uk/btc/` | **200**, 267,010 bytes, `text/html`, server `cloudflare`, 0.53 s |
| `https://farside.co.uk/bitcoin-etf-flow-all-data/` | **200**, **794,472 bytes**, 0.83 s |
| rendering | **server-rendered HTML `<table>`. No JavaScript execution is required.** |
| history served | **676 date rows, 11 Jan 2024 → 28 Aug 2026** |
| **rows on or after 2025-05-01** | **336** (the out-of-sample window) |
| columns | 12 funds + `Total`: IBIT, FBTC, BITB, ARKB, BTCO, EZBC, BRRR, HODL, BTCW, MSBT, GBTC, BTC |
| **the registered five** | **all present** (IBIT, FBTC, GBTC, ARKB, BITB) |
| units | millions of USD; negatives in parentheses; absence as `-` |
| **per-row publication timestamp** | **NOT SERVED. No timestamp column of any kind exists.** |
| keyless structured endpoint | **none** — HTML only; no JSON, no CSV, no documented API |

**The default `/btc/` page serves only the most recent 15 date rows.** The full
history lives at `/bitcoin-etf-flow-all-data/`, linked from `/btc/` as *"To see
an alternative table with all the daily flow data, click here"*.

#### The documented publication convention — measured as ABSENT

The verbatim notes served beside the tables, and the whole of what the source
documents about timing:

> **`/btc/`** — *"Note: The above table is generated automatically. Farside
> Investors is not liable for any errors or inaccuracies in the data."*
>
> **`/bitcoin-etf-flow-all-data/`** — *"Note: The above table is generated
> automatically, in real time. Farside Investors is not liable for any errors
> or inaccuracies in the data."*

**Labelled `documented`. It documents no publication time at all.** The words
"evening" and "night" appear **zero times** across both pages (n = 2 pages
searched). **The evening-and-night convention carried into the brief is
therefore not documented where the data is served, and there is nothing to
record as the documented print time.** Under standing rule 3 the **measured**
lag of A.1 Task 3 is the only figure that will exist, which is the outcome that
rule was written for.

**"generated automatically, in real time" is the whole-file-regeneration
signature** the MLCryptoEngine H11 precedent named. It is recorded here as the
documented basis for treating A.1 Task 4's revision measurement as first-class.

#### The measured hazard that makes the parser load-bearing

**The `Total` column prints `0.0` on a day where every per-fund cell is a
dash.** Measured over the out-of-sample window: **3 of 336 rows carry a dash in
all five registered funds, and all 3 of those 3 print a numeric `0.0` in
`Total`** — 26 May 2025 (Memorial Day), 19 Jun 2025 (Juneteenth), and 28 Aug
2026 (the open day, not yet printed at capture time).

**A source-side synthesized zero is exactly the value standing rule 4
forbids.** Consuming `Total` would have:

1. injected 3 fabricated flat trading days into the census, and
2. — far worse — recorded **`0.0` net flow for the open day on every capture
   taken before the print lands**, which would make the A.1 Task 3 lag
   measurement report that every day prints at 00:00 UTC.

`etf.flow.aggregate` therefore computes the signal from the five per-fund cells
and **returns a recorded absence when any one of them is absent**; the `Total`
column is never read. This was registered at A.0 before the source was
fetched, and the measurement above is what it was registered against.

**Partially-dashed rows in the settled history: 0 of 336.** When the table
prints, it prints all five funds. Whether a fund reports late *within* a day is
not visible in the settled table and can only be measured forward — which is
A.1 Task 3.

### 2.2 SoSoValue — **retained as a cross-check, not as the signal**

| probe | result |
|---|---|
| `https://sosovalue.com/assets/etf/us-btc-spot` | **200**, 1,086,812 bytes, 0.89 s |
| **keyless structured endpoint** | **YES** — a `<script id="__NEXT_DATA__">` JSON payload of 756,748 bytes is embedded in the page |
| history served | `props.pageProps.historyData.list`, **660 daily rows**, 2024-01-10 → 2026-08-27 |
| row shape | `{"dataDate": "2026-08-27 00:00:00", "totalNetInflow": 242238213.36, "totalVolume": …, "cumNetInflow": …, "period": "1d", "market": "US"}` |
| **per-row publication timestamp** | **NOT SERVED.** `dataDate` is the trading day, never the print time. |
| universe | `totalNetInflow` aggregates **all** US spot BTC ETFs, **not the registered five** |

**Why it is a cross-check and not the signal: the universe differs.** Measured
over the 333 overlapping out-of-sample days, **the registered five-fund
aggregate differs from the all-fund total by a mean of 47.42M USD (median
27.20M, range −903.20M to +1,205.20M, n = 333)** — large against the registered
100M USD threshold. The two are **not interchangeable**, and Section 2 names
five funds because the source study does.

**The cross-check itself passes: 315 of 333 out-of-sample days agree within 2
percent** between Farside's all-fund `Total` and SoSoValue's `totalNetInflow`
(n = 333). The 18 that do not are dominated by near-zero days where a relative
test is unforgiving (worst: 2026-08-11, 7.8M against 4.89M). **Two
independently operated sources agreeing on 315 of 333 days is the strongest
available evidence that the served flow surface is not idiosyncratic to one
publisher.**

### 2.3 The candidate set, resolved

| candidate | verdict |
|---|---|
| **Farside Investors** | **SELECTED — primary.** Keyless, server-rendered, per-fund, 676 rows, no prohibition. |
| **SoSoValue** | **RETAINED — cross-check only.** Keyless structured payload; different universe. |
| TheBlock | **OUT — automated collection of the data endpoint is disallowed by robots.txt.** |
| Glassnode | **OUT — data endpoint disallowed and not keyless (401).** |

**Neither selected source serves a per-row publication timestamp (n = 2 of 2).
The capture timestamp this repository stamps is therefore the only print-time
evidence that will ever exist, which is precisely why A.1 Task 3 is the
experiment.**

---

## 3. The venue — Hyperliquid `POST https://api.hyperliquid.xyz/info`

All probes **HTTP 200**. Every figure below came through the blindness readers,
which see `t`, `T`, row counts and `time`, and are structurally incapable of
returning a price.

| probe | result |
|---|---|
| `type: meta` | 200, 17,495 bytes, 0.15 s; BTC present in `universe` |
| `candleSnapshot` `1d`, 30-day window from 2025-05-15 | 200, 4,525 bytes, **31 rows** |
| `candleSnapshot` `1h`, 7-day window from 2025-05-15 | **200, 2 bytes, `[]`, 0 rows** |
| `fundingHistory` from 2025-04-01 | 200, **72 rows**, **0 gated**, 2025-04-01T00:00Z → 2025-04-04T19:00Z |
| `fundingHistory` from 2025-05-15 | 200, **72 rows**, **72 of 72 gated by the pre-period pin** |
| `fundingHistory` paging | **500 rows per page**, measured on 3 pages |
| `fundingHistory` depth | reaches **2023-05-13** at least (500 rows served from that start) |

### 3.1 The pre-period pin, demonstrated live rather than only on fixtures

The two `fundingHistory` probes were chosen to straddle the registered
2025-05-01 boundary. **The pre-period page returned 72 readable rates and 0
gated; the post-period page returned 0 readable and 72 of 72 gated
(`Absent(pre_period_gated)`), and a third page from 2025-05-01 gated 500 of
500.** The guard is exercised against production payloads, not only against
`tests/test_preperiod.py`.

### 3.2 **The finding that constrains the retro cohort: `candleSnapshot` serves a rolling 5,001-row window**

Measured by bisection (n = 17 probes across two intervals):

| interval | rows returned on a maximal request | earliest served open |
|---|---|---|
| **`1h`** | **5,001** | **2026-02-01T11:00:00Z** |
| `1d` | 2,201 | 2020-08-19T00:00:00Z (index backfill) |

**5,001 hourly candles is 208.4 days, and 2026-08-28 minus 208.4 days is
2026-02-01T11:00Z — the served start to the hour.** The window is therefore not
an archive epoch but a **rolling cap that slides forward one hour per hour**.
Probes at 730, 550, 400, 300, 250 and 225 days back returned **0 rows**; probes
at 212, 206, 203, 201, 200, 100 and 30 days back returned rows.

**Consequence, stated plainly and routed rather than worked around.** Section 5
defines the outcome as the perp return from the 08:00 UTC anchor to the anchor
plus 24 hours. **That return is not computable from 1d candles, whose
boundaries are 00:00 UTC.** So hourly candles are structurally required, and
**hourly candles do not exist for out-of-sample days older than roughly 208
days**. Of the 333 printed out-of-sample rows, **roughly 190 fall before
2026-02-01 and are already outside the servable 1h window; the boundary
consumes one further day every day.**

**Three things follow, none of them a change to the registration:**

1. **A retro day older than the rolling window is `underpowered` under the
   Section 12 coverage bar — a recorded absence, never a return.** No
   substitution of a 1d return for an hourly one is permitted, because it would
   silently redefine the anchor the whole design turns on.
2. **The sealed collection of A.2 Task 3 is urgent in a way the brief did not
   anticipate.** Every day of delay permanently destroys one day of retro 1h
   coverage. This is the same durability argument the brief makes for the
   forward flow ledger, and it binds harder here because no archive exists.
3. **This is an input to the A.1 Task 4 verdict and to Section 0**, and it
   pushes toward the forward cohort carrying more of the weight.

Recorded as **ADR-013**.

### 3.3 Kraken, cross-check only

`GET https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=1440` → **200**,
62,272 bytes, `application/json`, 0.28 s, response keyed `XXBTZUSD`. Keyless.
Retained as a **descriptive cross-check source only**; it is not the instrument
Section 2 names and no verdict reads it.

---

## 4. The archive — Wayback

| probe | result |
|---|---|
| `GET https://archive.org/wayback/available?url=farside.co.uk/bitcoin-etf-flow-all-data/&timestamp=20250601` | **200**, 281 bytes, `application/json`, 0.36 s |
| `GET https://web.archive.org/web/timemap/link/https://farside.co.uk/bitcoin-etf-flow-all-data/` | **200**, 16,300 bytes, `application/link-format`, 0.58 s |

Availability response, verbatim head:

```
{"url": "farside.co.uk/bitcoin-etf-flow-all-data/", "archived_snapshots": {"closest": {"status": "200", "available": true, "url": "http://web.archive.org/web/20250518185537/https://farside.co.uk/bitco…
```

Timemap response, verbatim head:

```
<https://farside.co.uk/bitcoin-etf-flow-all-data/>; rel="original",
<https://web.archive.org/web/timemap/link/https://farside.co.uk/bitcoin-etf-flow-all-data/>; rel="self"; type="application/link-form…
```

**Both endpoints serve, keyless, and the full-history flow page is archived.**
The per-day capture density — the figure that decides whether a retro cohort
exists at all — **is not asserted here. It is measured at A.1 Task 4.**

---

## 5. A defect found and fixed inside A.1 Task 1

**Pacing state lived in the client instance, so it paced nothing across
processes.** The first attempt to space two flow fetches revealed it: each
script invocation built a fresh `PacedClient` with an empty last-sent map, so
the registered 30 s spacing was enforced only within a single run. **The
collectors of A.3 fire as separate systemd invocations, so the limiter would
have paced nothing at all in production.**

`PacedClient._pace` now takes the **longer** of two waits: the in-process
monotonic gap and the gap since the endpoint's last **charge row in the request
ledger**, which is the only state shared across processes. Pinned by
`tests/test_pacing.py::test_the_pace_survives_process_death_by_reading_the_ledger`.
Recorded as **ADR-014**.

---

## 6. Pacing figures in force at the close of A.1 Task 1

**Provisional, registered at A.0 before any measurement, and replaced by
amendment from the A.1 Task 2 measurement.** An endpoint with no registered
pace is **refused, not defaulted fast** (`etf.pacing.PacingUnknown`).

| endpoint | provisional min spacing |
|---|---|
| `meta.robots`, `meta.terms` | 5.0 s |
| `flow.table` | 30.0 s |
| `archive.availability`, `archive.timemap`, `archive.snapshot` | 10.0 s |
| `venue.candleSnapshot`, `venue.fundingHistory`, `venue.meta` | 5.0 s |
| `kraken.ohlc` | 5.0 s |
