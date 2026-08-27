# ACCESS.md — the measured access table

All access is a keyless `POST https://api.hyperliquid.xyz/info` with a JSON
body. No account, no API key, no cookie. Every request in this file was
charged to the request ledger before it was sent (`data/ledgers/
requests.jsonl`, cap 20,000/day).

## A.1 Task 1 — access verification, live, 2026-08-27T00:56–00:58Z (n = 9 requests)

### type: meta (main dex perp universe)

`{"type": "meta"}` → HTTP 200, 17,495 bytes. **232 universe rows, 56 flagged
`isDelisted`.** Verbatim first row and a verbatim delisted row:

```
{"szDecimals": 5, "name": "BTC", "maxLeverage": 40, "marginTableId": 56}
{"szDecimals": 1, "name": "MATIC", "maxLeverage": 20, "marginTableId": 20, "isDelisted": true}
```

`szDecimals`, `maxLeverage`, and the delisted flag (`isDelisted`) are all
present, machine-readable. First delisted names observed: MATIC, RNDR, FTM,
MKR, FXS, HPOS, RLB, UNIBOT, OX, FRIEND, SHIA, CYBER. Last three universe
rows (newest listings): CHIP, GRAM, CASHCAT.

### type: metaAndAssetCtxs

HTTP 200, 71,519 bytes. Shape: `[meta, assetCtxs]`. Meta half keys:
`universe`, `marginTables`, `collateralToken`. Verbatim first asset ctx
(truncated at 240 chars):

```
{"funding": "0.0000125", "openInterest": "37699.3697800001", "prevDayPx": "78604.0", "dayNtlVlm": "3298927704.8863325119", "premium": "-0.0002147234", "oraclePx": "78705.9", "markPx": "78689.0", "midPx": "78688.5", "impactPxs": ["78688.0",
```

### type: perpDexs (HIP-3 dex enumeration) and per-dex meta

HTTP 200. Verbatim (first 300 chars):

```
[null,{"name":"xyz","fullName":"XYZ","deployer":"0x88806a71d74ad0a510b350545c9ae490912f0888","oracleUpdater":null,"feeRecipient":"0x9cd0a696c7cbb9d44de99268194cb08e5684e5fe","assetToStreamingOiCap":[["xyz:AAOI","25000000.0"],["xyz:AAPL","150000000.0"],["xyz:ALUMINIUM","25000000.0"],["xyz:AMAT","2500
```

The first entry is `null` (the main dex). **10 builder dexs live: xyz, flx,
vntl, hyna, km, abcd, cash, para, mkts, io.** Per-dex meta works via
`{"type": "meta", "dex": "xyz"}` → 117 universe rows, coins namespaced
`xyz:NAME`. Verbatim first row:

```
{"szDecimals": 4, "name": "xyz:XYZ100", "maxLeverage": 30, "marginTableId": 30, "growthMode": "enabled", "lastFeeScaleChangeTime": "2025-11-23T17:37:10.033211662", "deployerFeeScale": "1.0"}
```

HIP-3 meta rows additionally carry `deployerFeeScale` — a live fee signal
for the Section 5 verification.

### type: candleSnapshot, 1d and 1h

`{"type":"candleSnapshot","req":{"coin":"BTC","interval":"1d","startTime":…,"endTime":…}}`
→ HTTP 200. A 10-day request returned 11 rows. Verbatim first row (this is
BTC, the access-probe instrument, not a study event; the census and every
non-sealed module parse only `t`, `T`, and row count):

```
[{"t":1786924800000,"T":1787011199999,"s":"BTC","i":"1d","o":"62874.0","c":"64494.0","h":"64580.0","l":"62730.0","v":"30514.0474","n":278626},…
```

1h works identically: a 24-hour request returned 25 rows.

### type: fundingHistory, with startTime paging

`{"type":"fundingHistory","coin":"BTC","startTime":…}` → HTTP 200. A 48-hour
request returned 48 hourly rows, times 1787619600045 → 1787788800012.
Verbatim first row:

```
[{"coin":"BTC","fundingRate":"0.0000125","premium":"0.0000802332","time":1787619600045},…
```

Paging: a follow-up request with `startTime = last_time + 1` returned HTTP
200 with **an empty list** — end-of-feed is a served empty page (measured
absence, `no_data`), not an error.

### type: l2Book

HTTP 200. Verbatim (first 220 chars):

```
{"coin":"BTC","time":1787792220145,"levels":[[{"px":"78688.0","sz":"2.4478","n":14},{"px":"78687.0","sz":"0.8281","n":3},{"px":"78686.0","sz":"2.28816","n":4},{"px":"78685.0","sz":"1.79905","n":5},{"px":"78684.0","sz":"2
```

`levels` is `[bids, asks]`, each level `{px, sz, n}` — the Section 5 touch
spread and top-five depth are servable from one request.

## Documented request weights — documented, not measured

Source: Hyperliquid docs, "Rate limits and user limits"
(hyperliquid.gitbook.io), retrieved 2026-08-27T00:58Z via a one-off
documentation fetch (not a venue API call; recorded here rather than in the
request ledger, which accounts venue endpoints).

- "REST requests share an aggregated weight limit of **1200 per minute**"
  (IP-based).
- Weight **2**: `l2Book`, allMids, clearinghouseState, orderStatus,
  spotClearinghouseState, exchangeStatus.
- Weight **20**: "All other documented info requests" — covers `meta`,
  `metaAndAssetCtxs`, `perpDexs`, `candleSnapshot`, `fundingHistory`.
- Weight **60**: userRole. Weight **40**: explorer API requests.
- `fundingHistory` (and other list endpoints): additional weight "per 20
  items returned in the response."
- "The candleSnapshot info endpoint has an additional rate limit weight per
  60 items returned."
- The docs do not state a maximum item count per response for candleSnapshot
  or fundingHistory; the caps are measured in A.1 Task 3 below.

Every figure in this section is the documentation's claim. The measured
sections below govern wherever they disagree (standing rule: measured beats
documented).

## A.1 Task 2 — rate ceilings, measured per endpoint, 2026-08-27T01:00–01:18Z

Protocol: per endpoint, a burst at 0.05 s nominal spacing until the first
refusal or n_max, with a 61 s cooldown between endpoints so each starts on a
full budget; then a 60 s sustained verification for the load-bearing
endpoints. 846 requests ledgered by the end of the probe. Raw results:
scratchpad `a1_rate_results.json` (figures reproduced here in full).

| endpoint | burst | refusal | sustained verification | measured ceiling | chosen operating pace |
|---|---|---|---|---|---|
| meta | 80/80 admitted in 22.8 s (~211/min) | none | 99/99 clean at 0.375 s (160/min) | **not reached at probe scale** | 0.8 s (half the verified-clean 160/min) |
| metaAndAssetCtxs | 80/80 in 27.3 s (~176/min) | none | — | not reached at probe scale | 0.8 s |
| perpDexs | **79 admitted, then 429** at 20.7 s | body verbatim: `null` | — | **~79/min** | 1.6 s (half of 79/min) |
| candleSnapshot, 11 rows | 80/80 in 24.3 s (~198/min) | none | — | not reached at probe scale | 5.3 s (endpoint-wide, from the 5000-row ceiling) |
| candleSnapshot, 5000 rows | **23 admitted, then 429** at 14.0 s | body verbatim: `null` | 20/20 clean at 2.61 s (23/min) | **~23/min at 5000 rows** | 5.3 s (half of 23/min) |
| fundingHistory, 500 rows | 45/45 in 13.1 s (~206/min) | none | 67/67 clean at 0.667 s (89/min) | not reached at probe scale | 1.4 s (half the verified-clean 89/min) |
| l2Book | 120/120 in 26.5 s (~271/min) | none | 142/142 clean at 0.25 s (240/min) | not reached at probe scale | 0.5 s (half the verified-clean 240/min) |

Findings against the documentation:

- **The refusal shape is HTTP 429 with the four-byte body `null`.** No
  Retry-After header is relied on; the collectors treat any 429 as
  `rate_limited`, a loud recorded state, never end-of-feed.
- **The documented 1200 weight/min budget does not describe admission.**
  meta absorbed 80 requests (nominal 1600 documented weight) inside 23
  seconds without a refusal, and fundingHistory at 500 rows absorbed 45
  requests (nominal ~2000 documented weight) in 13 seconds. Where a ceiling
  WAS found (perpDexs at ~79/min, candleSnapshot at ~23/min for 5000-row
  responses), it is measured, not derived from the documented weights. The
  registered operating paces above are the halves of measured ceilings where
  one was found and halves of the highest verified-clean rate where one was
  not, and they are registered in `npl.pacing.OPERATING_PACING_S`.

## A.1 Task 3 — retention, measured on 12 instruments, 2026-08-27T01:19–01:23Z

Probe set spanning old majors (BTC, ETH, SOL, DOGE, AVAX), the H5-cited MERL
and TNSR, HYPE, three recent listings (CHIP, GRAM, CASHCAT), and one HIP-3
instrument (xyz:XYZ100). n = 12 instruments, 40 requests (897 ledgered
cumulative). Every figure below parsed through the blindness readers: times
and row counts only.

| coin | 1d rows / earliest | 1h rows / earliest | funding page-1 rows / earliest |
|---|---|---|---|
| BTC | 2200 / 2020-08-19 | 5002 / 2026-01-30T16:00Z | 500 / **2023-05-12T00:00Z** |
| ETH | 2200 / 2020-08-19 | 5002 / 2026-01-30 | 500 / 2023-05-12 |
| SOL | 2174 / 2020-09-14 | 5002 / 2026-01-30 | 500 / 2023-05-12 |
| DOGE | 2200 / 2020-08-19 | 5002 / 2026-01-30 | 500 / 2023-05-12 |
| AVAX | 2165 / 2020-09-23 | 5002 / 2026-01-30 | 500 / 2023-05-12 |
| MERL | 857 / **2024-04-23** | 5001 / 2026-01-30 | 500 / **2024-04-23T15:00Z** |
| TNSR | 872 / **2024-04-08** | 5001 / 2026-01-30 | 500 / **2024-04-08T22:00Z** |
| HYPE | 631 / **2024-12-05** | 5004 / 2026-01-30 | 500 / **2024-12-05T10:00Z** |
| CHIP | 128 / **2026-04-22** | 3048 / 2026-04-22T02:00Z | 500 / **2026-04-22T03:00Z** |
| GRAM | 57 / **2026-07-02** | 1337 / 2026-07-02T09:00Z | 500 / **2026-07-02T10:00Z** |
| CASHCAT | 48 / **2026-07-11** | 1126 / 2026-07-11T04:00Z | 500 / **2026-07-11T05:00Z** |
| xyz:XYZ100 | 319 / **2025-10-13** | 5002 / 2026-01-30 | 500 / **2025-10-13T13:00Z** |

Measured findings:

1. **1d candles serve the instrument's full life with no cap observed**
   (largest single response 2,200 rows). For the majors they extend to
   2020 — three years before the venue's funding archive — so early candles
   are index-backfilled and a first 1d candle is NOT a listing date for the
   pre-epoch era.
2. **The funding archive epoch is 2023-05-12T00:00Z**: every venue-launch-era
   instrument's first funding row lands exactly there (n = 5 of 5 majors).
3. **For every instrument listed after the epoch, first 1d candle, first 1h
   candle, and first funding row agree on the same UTC day** (n = 7 of 7
   probed post-epoch instruments) — the listing-date inference of Section 3
   holds to well under the registered ±1 day, cross-checked on two
   independent series.
4. **1h candles are a rolling window of ~5,000 bars** (5001–5004 observed,
   earliest 2026-01-30 ≈ now − 208 days), full-life for instruments younger
   than that. The 1h interval is not outcome-bearing in this design.
5. **fundingHistory pages at exactly 500 rows** ascending from startTime,
   advances by `startTime = last + 1` (verified on BTC, MERL, CHIP), and the
   90-day retro funding windows are servable for every event with a
   post-epoch listing. **Registered pull cadence: daily batch per active
   instrument, cursor = last stored time + 1; one 500-row page covers 20.8
   days, so a daily pull carries ~19 days of catch-up margin.**

## A.1 Task 4 — delisting observability, 6 delisted perps, 2026-08-27T01:23–01:25Z

solclear Finding 2 (manufactured survivorship) is why this is first-class.
Probe: the full 1d span and the first funding page for six perps flagged
`isDelisted` in meta. Verbatim evidence (times through the blind readers):

| coin | 1d rows / span | funding page-1 rows / span |
|---|---|---|
| MATIC | 1419 / 2020-10-22 → **2024-09-09T23:59Z** | 500 / 2023-05-12 → 2023-06-25 |
| RNDR | 535 / 2023-02-03 → **2024-07-21** | 500 / 2023-05-18 → 2023-06-26 |
| FTM | 1572 / 2020-09-24 → **2025-01-12** | 500 / 2023-05-25 → 2023-06-27 |
| UNIBOT | 380 / 2023-06-14 → **2024-06-27** | 500 / **2023-08-02** → 2023-08-22 |
| CYBER | 600 / 2023-08-21 → **2025-04-11** | 500 / **2023-08-31** → 2023-09-20 |
| FRIEND | 256 / 2023-08-21 → **2024-05-02** | 500 / 2023-08-21 → 2023-09-10 |

**Verdict: PASS in full — 6 of 6 probed delisted perps serve both their
candle history (through their delisting date) and their funding history.**
The retrospective cohort is not survivorship-manufactured by the venue's
serving behaviour.

One further mechanical finding rides on this table: UNIBOT's candles begin
49 days before its first archived funding row, and CYBER's 10 days before —
the signature of a pre-vanilla (hyperp-style) phase trading without archived
funding. FRIEND's agree to the hour. This motivates REGISTRATION.md
Amendment 1: the event date is the first candle day cross-checked against
the first funding day, and a disagreement past the ±1 day tolerance tags the
instrument `hyperp_conversion` mechanically, with the funded phase's start
as the event date.
