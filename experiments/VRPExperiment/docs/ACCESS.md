# TASK 4 — Public data access for the premium

**Measured 2026-08-30, 05:45Z–06:10Z.** Machine-readable evidence in
`reports/task4/deribit_probe.json` and `reports/task4/rate_and_revision_baseline.json`.

**Nothing here registers, onboards, or places an order.** Reading a public
endpoint that requires no account is permitted under standing rule 5 and is
distinct from trading. Deribit's *private* endpoint was probed exactly once, to
confirm the public/private split is real, and it refused as it should:

```json
{"jsonrpc":"2.0","error":{"code":13009,"data":{"reason":"invalid_token"},"message":"unauthorized"},"testnet":false}
```
`GET /api/v2/private/get_account_summary?currency=BTC` → **HTTP 400**. No
credential was sent, none is held, and none is planned.

**Blindness holds throughout.** The probe tools read no volatility value. They
extract HTTP status, byte count, row count, **index-0 timestamps**, and SHA-256
digests. The revision question is answered by comparing digests, which needs no
value at all.

---

## 1. Deribit — the registered primary source

`robots.txt` at `www.deribit.com` returns **HTTP 404** (25,049 bytes of HTML
error page): **no crawl directives are published at that path**.
`support.deribit.com/robots.txt` is served and does not disallow the article
path used in TASK 3.

### 1.1 Endpoint status, `n = 11` probes

| endpoint | params | HTTP | rows | bytes |
|---|---|---|---|---|
| `get_time` | — | **200** | — | 117 |
| `status` | — | **200** | — | 124 |
| `get_index_price` | `btc_usd` | **200** | — | 165 |
| `get_index_price` | `eth_usd` | **200** | — | 163 |
| `get_volatility_index_data` | BTC, 2 d, 3600 s | **200** | **49** | 2,064 |
| `get_volatility_index_data` | ETH, 2 d, 3600 s | **200** | **49** | 2,077 |
| `get_instruments` | BTC, kind=option | **200** | **1,026** | 895,883 |
| `get_instruments` | ETH, kind=option | **200** | **876** | 763,918 |
| `get_currencies` | — | **200** | 50 | 22,442 |
| `get_volatility_index_data` | **currency=DOGE** | **400** | — | 206 |
| `get_index_price` | **invalid index** | **400** | — | 200 |

**Every endpoint this measurement needs is served with no account.** Live
instrument counts: **1,026 BTC option instruments and 876 ETH option
instruments**, `n = 1` enumeration each.

### 1.2 Refusal payloads, recorded verbatim

Unsupported resolution (`300`, `900`, `21600` all identical), **HTTP 400**:
```json
{"code":-32602,"data":{"reason":"unsupported resolution","param":"resolution"},"message":"Invalid params"}
```
Invalid index name, **HTTP 400**:
```json
{"code":-32602,"data":{"reason":"invalid index","param":"index_name"},"message":"Invalid params"}
```

**Supported DVOL resolutions, measured by trying them: `60`, `3600`, `43200`,
`1D`.** Read from the endpoint, not from documentation. *(`1D` was found on a
later probe during TASK 6 preparation and is appended here rather than silently
folded into the original list: the first list was incomplete because it tested
only numeric-seconds values.)*

### 1.3 A refusal that does not look like one — recorded loudly

`get_volatility_index_data?currency=DOGE&resolution=3600` returns **HTTP 200**:
```json
{"jsonrpc":"2.0","result":{"data":[],"continuation":null},"testnet":false}
```

**An unsupported currency returns a successful, empty response, not an error.**
A caller that reads "empty" as "no volatility" would synthesize a value for an
instrument that does not exist. This is precisely the failure Guard 4 exists to
prevent: `NO_DATA` is a health state and is **never** merged with a
composition or venue fact. *(Note the inconsistency in Deribit's own API: the
same currency returns HTTP 400 when `resolution` is omitted and HTTP 200 with an
empty array when it is supplied. The status code alone is not a reliable
discriminator, and this repository does not treat it as one.)*

### 1.4 History depth — **bisected, not assumed**

Method: exponential bracket then bisection on a 7-day window at
`resolution=43200`, `n = 22` probes per asset.

| asset | deepest served | first empty | approximate earliest served |
|---|---|---|---|
| **BTC** | **1,992 days back** | 1,993 days back | **2021-03-17T06:23:58Z** |
| **ETH** | **1,992 days back** | 1,993 days back | **2021-03-17T06:24:06Z** |

**Corroborated independently:** the CryptoDataDownload DVOL CSV (§2.1) has its
oldest row at **2021-03-24**, one week later, which is consistent with a series
beginning in the second half of March 2021.

**1,992 days is 2.73× the registered minimum depth of 730 daily observations
(Section 2.5).** Depth is not a binding constraint on this measurement.

### 1.5 Page size and pagination — measured

A request for 30 days at `resolution=60` returns **exactly 1,000 rows** and a
**`continuation` token**, covering only **0.69 days** of the 30 requested.
Following the token once returned a further **1,000 rows** covering
`2026-08-28T21:09Z → 2026-08-29T13:48Z`, **contiguous** with page 1
(`2026-08-29T13:49Z → 2026-08-30T06:28Z`), and a further token.

**The 1,000-row cap is a page size, not a depth limit.** Fine-resolution deep
history is reachable by paging. Recorded so a later reader does not mistake a
truncated first page for the end of the series — that mistake would silently
shorten every window in the analysis.

### 1.6 Rate ceiling — **measured by escalation, not read from documentation**

Two passes, because the first one measured the wrong thing and the correction is
recorded rather than silently applied.

**Pass 1 (superseded).** Sixty *sequential* requests to `get_index_price`
achieved **3.64 req/s** and drew **no refusal**. This measured round-trip
latency, not the venue's limit.

**Pass 2, concurrent escalation**, doubling concurrency from 2 until a non-200
status is drawn or a registered ceiling of 64 concurrent requests is reached:

| concurrency | `get_index_price` | `get_volatility_index_data` |
|---|---|---|
| 2 | 11.99 req/s · all 200 | 10.01 req/s · all 200 |
| 4 | 21.43 req/s · all 200 | 23.82 req/s · all 200 |
| 8 | 44.96 req/s · all 200 | 37.88 req/s · all 200 |
| 16 | 87.60 req/s · all 200 | 68.95 req/s · all 200 |
| 32 | 56.62 req/s · all 200 | 120.45 req/s · all 200 |
| 64 | **126.76 req/s · all 200** | 113.08 req/s · all 200 |

**No refusal was drawn on either endpoint, `n = 126` requests each.** The
honest statement is **"no rate refusal at or below 126.76 req/s"** — an
**upper bound that was not reached**, not a measured ceiling. The escalation
stopped at the registered ceiling of 64 concurrent rather than climbing against
a venue that has not refused; hammering a public endpoint until it breaks is not
a measurement this repository is entitled to take.

### 1.7 Revision behaviour — **the mandatory question**

MLCryptoEngine H11 died on a source that regenerated whole files and revised
past rows. A revised implied-volatility series would silently rewrite this
measurement.

**First attempt returned a false positive, and the correction is recorded.**
Fetching a fixed, closed 7-day window 45 days in the past twice, 5 seconds
apart, produced **different whole-response SHA-256 digests**. Diagnosis: the
JSON-RPC envelope carries `usIn`, `usOut` and `usDiff` server-timing fields that
change on every call. With those excluded, the **169 data rows were
byte-identical**:

```
data-only SHA-256, fetch A: fa63b50d8879cc74db37488c4082120725182ff6a855ec183947a39d5e2be8ef
data-only SHA-256, fetch B: fa63b50d8879cc74db37488c4082120725182ff6a855ec183947a39d5e2be8ef
```

**A whole-response digest is the wrong instrument for this question and would
have reported a revision that did not happen.**

**Six data-only baselines were then recorded** for re-checking after a
meaningful interval (`reports/task4/rate_and_revision_baseline.json`), each a
closed 7-day window at `resolution=3600`, `169 rows` each:

| asset | days back | rows | data-only SHA-256 (first 16) |
|---|---|---|---|
| BTC | 45 | 169 | `fa63b50d8879cc74` |
| BTC | 365 | 169 | `8c3f100adf973a43` |
| BTC | 900 | 169 | `dbe71688a237c845` |
| ETH | 45 | 169 | `14b42a8bc42fab6b` |
| ETH | 365 | 169 | `f7ec7c9a195a2fe3` |
| ETH | 900 | 169 | `2647860f242c4b1a` |

**These are re-checked at TASK 8 and the result recorded there.** A 5-second
gap tests nothing; the TASK 8 re-check spans the working session.

---

## 2. Alternatives, each probed

| source | served without an account? | option-level IV, or an index only? | history depth | granularity | revision risk |
|---|---|---|---|---|---|
| **Deribit** | **yes**, HTTP 200 on all 9 valid endpoints | **both** — the DVOL index *and* 1,026 BTC / 876 ETH option instruments | **1,992 days**, bisected | 60 s / 3600 s / 43200 s | baselines recorded; §1.7 |
| **CryptoDataDownload** | **yes**, HTTP 200, no key | **index only** (DVOL OHLC), and **derived from Deribit** | **1,986 daily rows**, 2021-03-24 → 2026-08-30 | **daily only** | **HIGH — see §2.1** |
| **Laevitas** | **NO — refused** | — | — | — | — |
| **Amberdata** | **NO — refused** | — | — | — | — |
| **Tardis** | metadata yes; history **paid** | lists a `deribit_volatility_index` channel, `availableSince 2019-03-30` | not measured | not measured | not pursued — **spend nothing** |
| **OKX** | **yes**, HTTP 200, 868,306 B | **option-level** (`askVol`, `bidVol`, `delta`, `gamma`, `fwdPx`) | **none — live snapshot only** | snapshot | n/a |
| **Bybit** | **yes**, HTTP 200, 427,630 B | **option-level** (`bid1Iv`, `ask1Iv`) | **none — live snapshot only** | snapshot | n/a |
| **Binance eoptions** | **yes**, HTTP 200 | **option-level** (`bidIV`, `askIV`, `markIV`, full greeks) | **none — live snapshot only** | snapshot | n/a |
| **Volmex** | **not located** | — | — | — | — |

### Refusals, verbatim

**Laevitas**, `GET api.laevitas.ch/analytics/options/atm_iv?currency=BTC` → **HTTP 400**:
```json
{"status":400,"message":"Api Key is Required"}
```
**Amberdata**, `GET web3api.io/api/v2/market/options/exchanges/information` → **HTTP 403**:
```json
{"message":"Forbidden"}
```
Both **require an account**. Neither was pursued: this repository registers
nowhere and spends nothing. **`Absent(not_served)` for both. No value from
either is estimated, substituted, or inferred.**

**Volmex**: two candidate paths (`/v1/indices/BVIV`, `/v2/public/indices`) both
returned `{"name":"NotFoundError","code":404}`. The endpoint was **not
located**, which is recorded as *not located* and **not** as *does not exist* —
the difference matters and this repository did not establish the stronger claim.

### 2.1 CryptoDataDownload — the H11 risk, named

CDD publishes `DeriBit_volatility_OHLC_BTC.csv` (**76,979 bytes**, SHA-256
`a32533bee1406df578021749…`) and `DeriBit_volatility_OHLC_ETH.csv`
(**78,058 bytes**, SHA-256 `0c911fc282aa19cb298cbcae…`), each with header
`date,symbol,open,high,low,close` and **1,986 daily rows** spanning
**2021-03-24 → 2026-08-30**.

**Two disqualifying properties, both measured:**

1. **It is not an independent source.** The filename says so and the content
   confirms it: this is Deribit's own DVOL index, redistributed. Using it
   alongside Deribit would be counting one source twice.
2. **It is a whole-file regeneration.** The file is a single CSV that includes
   *today's* row, so it is rebuilt on every publication. **This is exactly the
   shape that killed MLCryptoEngine H11** — a source that regenerates whole
   files and can revise past rows without any signal that it has. Its digests
   are recorded above and re-checked at TASK 8, but **the structural risk is
   present regardless of what a single re-check finds**: one unchanged
   observation does not establish that rows never change.

**Disposition: CDD is used as a corroborating check on Deribit's history depth
(§1.4) and for nothing else. It is not a fallback for the primary series.**

### 2.2 The structural finding that decides the source choice

**Only two of the eight probed sources serve *history* at all, and one of them
is a mirror of the other.**

OKX, Bybit and Binance each serve **richer** data than Deribit's index — full
option-level bid/ask implied volatility with greeks, publicly and without an
account. **All three serve a live snapshot only.** They cannot supply a 730-day
series unless this repository had been recording daily for two years, which it
has not, and no amount of engineering changes that.

This is the reason the Section 2.2 fallback was registered **within Deribit**
(option-level mark IV at the bracketing expiries) rather than **across venues**.
That registration was made before any of this was measured, and the measurement
supports it. **Recorded here because it is the kind of design choice that looks
arbitrary in a registration and turns out to be load-bearing.**

---

## 3. What this means for TASK 6

| requirement (Section 2.5) | registered | measured | status |
|---|---|---|---|
| implied estimator served | DVOL index, both assets | **HTTP 200, no account, 1,992 days** | **met** |
| minimum depth | 730 daily observations per asset | **1,992 days available** | **met, 2.73×** |
| minimum for any figure | 60 observations | far exceeded | **met** |
| sampling frequency | daily at a fixed UTC instant | **08:00 UTC**, taken hourly and filtered — see below | **met** |
| revision behaviour | must be established | baselines recorded, re-checked at TASK 8 | **pending TASK 8** |
| underlying closes for the realized leg | daily, same UTC instant | `get_index_price` served, HTTP 200 | **met** |

**No fallback to Section 2.2's option-level construction is required.** It is
recorded as **not used**, per the registration's instruction that the fallback
be recorded as used or not used and never blended.


---

## 6. The fixed UTC instant, chosen before the latch

Section 2.5 registered "one observation per calendar day, at a **fixed UTC
instant**. The instant is fixed at the first read and never moved." **The
instant is fixed here, before the TASK 6 latch, at 08:00 UTC**, and the reason
is a measured misalignment rather than a preference.

Measured on a 400-day window, timestamps only, no value read:

| series | endpoint | `resolution=1D` bucket stamp |
|---|---|---|
| implied leg | `get_volatility_index_data` | **00:00 UTC** (n = 401 rows, all `hour == 0, minute == 0`) |
| underlying leg | `get_tradingview_chart_data`, `BTC-PERPETUAL` | **08:00 UTC** (n = 401 rows, all `hour == 8, minute == 0`) |

**The two endpoints bucket their daily bars eight hours apart**, so pairing them
at `resolution=1D` would have silently offset the implied leg from the realized
leg by eight hours on every one of ~1,900 observations. Daily bars cannot fix
this; **both series are therefore taken at `resolution=3600` and filtered to the
08:00 UTC observation**, which makes them exactly simultaneous.

**08:00 UTC is also the right instant on the merits, not merely the convenient
one: it is Deribit's option settlement time**, measured in TASK 5 on the live
series (`BTC-25SEP26-78000-C` and its put, settlement `2026-09-25T08:00:00Z`).
A 30-day tenor measured 08:00 → 08:00 is exactly the interval an option spans,
which is what the standing rule *"option expiries carry their exchange
settlement time"* points at.

Requests are chunked at **40 days = 960 hourly rows**, under the 1,000-row page
cap of §1.5, and the run **raises rather than continues** if any chunk returns
≥ 1,000 rows. A silent truncation would shorten the series without any signal.
