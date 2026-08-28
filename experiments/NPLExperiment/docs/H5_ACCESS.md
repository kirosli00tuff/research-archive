# docs/H5_ACCESS.md — what the venue serves on HIP-3 equity-style perps

**Measured 2026-08-28. Two full census passes, 323 requests each, plus a
6-request reconnaissance probe: 652 requests in total, zero dollars, keyless
public endpoints, every one charged to the shared ledger before it was sent.**
Both passes returned **identical** counts on every figure below; the second
is the one recorded (`h5-census-2026-08-28T21:51:54Z`, session tag
`extended`).

This document answers Task 2 of `registrations/H5/REGISTRATION.md`: which
fields the venue serves per instrument, which it does not, and — the
question the operator named as the one that might resolve most of the entry
alone — **whether funding is served on these instruments at all.**

**A note on what is quoted.** Response fragments below are verbatim, with
one exception stated where it occurs: `fundingHistory` rows carry a
`fundingRate`, and H5 reads no funding rate value on any path, so that one
field is shown as `<gated>` and everything else in the row is verbatim.

---

## 1. The headline answers

| question | measured answer |
|---|---|
| Is a **reference** served? | **Yes, on 151 of 151** resolved instruments. `oraclePx` on every one; `indexPx` never needed. `reference_unserved` is **zero**. |
| Is **funding** served? | **Yes.** The `funding` field is present on **151 of 151** asset contexts, and `fundingHistory` returns rows for **94 of 94 live** instruments — every live instrument's last row is inside the last two hours. The 2026-08-27 `no_data` / `caught_up=true` records on `xyz:AAPL`, `xyz:NVDA`, `xyz:META` and `xyz:XYZ100` were **an archive cursor at its end, not an absent field**. |
| Is there a **book**? | Two-sided on **94 of 94 live** instruments; **empty on all 57 delisted** ones. |
| Is there **historical mark-vs-oracle**? | **No.** The venue serves no historical mark and no historical oracle in the same row, anywhere on the info endpoint. A retrospective basis of the registered construction **does not exist** (Amendment H5-1 Change 2). |
| Is there **historical deviation of any kind**? | **Yes, of a different construction**: `premium`, hourly, in the `fundingHistory` row beside its `time`. It is an **impact-price** deviation, so it is a named secondary and may never fire VIABLE. |
| How big is the **contemporaneous basis**? | On the 94 live instruments, one `extended` snapshot: **median absolute 3.72 bp, IQR 0.73–7.31, max 51.4 bp, 8.5 percent over the 18 bp floor, 0.0 percent over the 54 bp bar.** |

## 2. Verbatim response fragments

### `perpDexs` — 11 entries, the first `null` (the main dex)

```json
[null, {"name": "xyz", "fullName": "XYZ", "deployer": "0x88806a71d74ad0a510b350545c9ae490912f0888",
        "oracleUpdater": null, "feeRecipient": "0x9cd0a696c7cbb9d44de99268194cb08e5684e5fe",
        "assetToStreamingOiCap": [["xyz:AAOI", "25000000.0"], ["xyz:AAPL", "150000000.0"], ...]}]
```

### `metaAndAssetCtxs` **accepts a `dex` parameter**

This was not assumed. `{"type": "metaAndAssetCtxs", "dex": "xyz"}` returns
HTTP 200, 53,140 bytes, a two-element list whose universe (117 rows) and
context list (117 rows) are **positionally aligned**. A length mismatch is a
refusal in the parser, never a `zip` that truncates and mislabels.

Universe row, verbatim — note the venue **already carries the dex prefix in
`name`**, so an H5 coin is the served name and nothing is re-prefixed:

```json
{"szDecimals": 4, "name": "xyz:XYZ100", "maxLeverage": 30, "marginTableId": 30,
 "growthMode": "enabled", "lastFeeScaleChangeTime": "2025-11-23T17:37:10.033211662",
 "deployerFeeScale": "1.0"}
```

Asset context, verbatim (`xyz:XYZ100`, same snapshot):

```json
{"funding": "0.00000625", "openInterest": "6361.0196", "prevDayPx": "29582.0",
 "dayNtlVlm": "276647444.2027971148", "premium": "-0.0001018745", "oraclePx": "29448.0",
 "markPx": "29446.0", "midPx": "29445.0", "impactPxs": ["29444.0", "29446.0"],
 "dayBaseVlm": "9360.2656000001"}
```

Main-dex context for comparison (`BTC`, same pass) — the arithmetic that
identified `premium`'s construction:

```json
{"funding": "0.0000125", "openInterest": "37943.37328", "prevDayPx": "79994.0",
 "dayNtlVlm": "4615527344.0638856888", "premium": "-0.0003482613", "oraclePx": "77528.0",
 "markPx": "77492.2", "midPx": "77500.5", "impactPxs": ["77500.0", "77501.0"],
 "dayBaseVlm": "58365.4670299997"}
```

`(77501.0 − 77528.0) / 77528.0 = −0.00034826…`, which is the served
`premium` to every digit shown, where `77501.0` is the served impact ask.
**`premium` is an impact-price deviation, not mark against oracle** — a
different construction, hence a named secondary.

### `fundingHistory` — rows served, `fundingRate` gated in this document

Key set, verbatim: `["coin", "fundingRate", "premium", "time"]`. One row,
verbatim except the gated field:

```json
{"coin": "xyz:AAPL", "fundingRate": "<gated>", "premium": "<gated>", "time": 1763737200047}
```

A page returns at most **500 rows**, hourly. `xyz:AAPL`'s archive reaches
back to `1763737200047` = **2025-11-21T15:00Z**.

### `l2Book` — 20 levels per side on a live instrument

```json
{"coin": "xyz:GOOGL", "levels": [[{"px": "345.94", "sz": "2.891", "n": 1}, ...],
                                 [{"px": "345.95", "sz": "4.004", "n": 1}, ...]],
 "time": ...}
```

On a delisted instrument one side comes back empty, which the registered l2
reader records as a refusal rather than a spread — `no_data`, 57 of 57.

## 3. The served-field matrix

**Every one of the 151 resolved instruments serves exactly the same ten
context fields.** There is no variation to report, on any dex, live or
delisted — which is itself the finding: the venue's context shape does not
distinguish a market with 1.2 million dollars of daily volume from one with
zero.

| field | served on | H5 uses it as |
|---|---|---|
| `markPx` | 151 / 151 | the perp mark (registered) |
| `oraclePx` | 151 / 151 | **the reference** (registered, first choice) |
| `indexPx` | 0 / 151 | registered fallback reference; never needed |
| `midPx` | 151 / 151 | **registered non-reference** — book state |
| `prevDayPx` | 151 / 151 | **registered non-reference** |
| `impactPxs` | 151 / 151 | **registered non-reference**; identifies `premium`'s construction |
| `premium` | 151 / 151 | the named secondary deviation (contemporaneous and historical) |
| `funding` | 151 / 151 | **service only** — H5 never reads the value |
| `openInterest` | 151 / 151 | descriptive; part of the three-field listing rule |
| `dayNtlVlm` | 151 / 151 | descriptive; part of the three-field listing rule |
| `dayBaseVlm` | 151 / 151 | not used |

## 4. Resolution and the universe, by dex

The mapping (`npl.h5.resolution`) was committed **before any price was
read**. 198 registered ticker strings; applied to the live enumeration:

| dex | instruments | resolved | live | delisted | non-equity | unresolvable |
|---|---:|---:|---:|---:|---:|---:|
| `abcd` | 1 | 1 | 0 | 1 | 0 | 0 |
| `cash` | 17 | 12 | 0 | 12 | 5 | 0 |
| `flx` | 16 | 6 | 0 | 6 | 10 | 0 |
| `hyna` | 25 | 0 | 0 | 0 | 25 | 0 |
| `io` | 6 | 4 | 2 | 2 | 0 | 2 |
| `km` | 23 | 15 | 0 | 15 | 5 | 3 |
| `mkts` | 23 | 15 | 3 | 12 | 5 | 3 |
| `para` | 30 | 20 | 16 | 4 | 7 | 3 |
| `vntl` | 15 | 0 | 0 | 0 | 4 | 11 |
| `xyz` | 117 | 78 | 73 | 5 | 19 | 20 |
| **total** | **273** | **151** | **94** | **57** | **80** | **42** |


**`hyna` and `vntl` resolve to nothing**: `hyna` is a wholly crypto dex, and
`vntl` lists private issuers and unnamed thematic baskets. Neither
contributes an instrument to this entry.

**The live equity-style family is concentrated in two dexs**: `xyz` (73) and
`para` (16) hold **89 of the 94** live instruments; `mkts` holds 3 and `io`
2. Four dexs — `abcd`, `cash`, `flx`, `km` — are **entirely delisted** on
their equity-style instruments: 34 instruments, zero live.

### Resolution reasons, with their n

| state | reason | n |
|---|---|---:|
| `resolved` | `equity` | 118 |
| `resolved` | `etf` | 15 |
| `resolved` | `index` | 18 |
| `excluded_non_equity` | `commodity` | 37 |
| `excluded_non_equity` | `crypto` | 28 |
| `excluded_non_equity` | `crypto_index` | 3 |
| `excluded_non_equity` | `fx` | 7 |
| `excluded_non_equity` | `rate` | 5 |
| `excluded_unresolvable` | `ambiguous_ticker` | 15 |
| `excluded_unresolvable` | `basket_no_named_reference` | 14 |
| `excluded_unresolvable` | `not_in_registered_mapping` | 1 |
| `excluded_unresolvable` | `private_no_public_underlying` | 11 |
| `excluded_unresolvable` | `venue_house_index` | 1 |


One instrument — `para:IGV`, born 2026-08-28 and already delisted — carries
a ticker the registered mapping has never seen. It is recorded as
`excluded_unresolvable / not_in_registered_mapping` and counted. **It is not
being added**: the mapping was registered before any price was read, and
extending it after a census is how a universe gets fitted.

## 5. The delisted stratum, and why it is excluded

**57 of the 151 resolved instruments are delisted**, and the three fields
agree unanimously: every one carries `isDelisted: true`, `openInterest`
exactly `0`, and `dayNtlVlm` exactly `0`. **Zero conflicting cases.** None
of the 94 live instruments carries any of the three.

Their contemporaneous basis is not small:

| stratum | n | median abs basis | IQR | max | share > 18 bp | share > 54 bp |
|---|---:|---:|---:|---:|---:|---:|
| **live** | **94** | **3.72 bp** | 0.73 – 7.31 | 51.4 bp | 8.5 % | **0.0 %** |
| delisted | 57 | 30.52 bp | 0.00 – 210.79 | 2,481 bp | 54.4 % | **45.6 %** |
| all resolved | 151 | 4.14 bp | 0.00 – 18.13 | 2,481 bp | 25.8 % | 17.2 % |

**Every observation above the 54 bp VIABLE bar lives in the delisted
stratum.** A dead market's mark is a frozen last value while its oracle goes
on updating; the gap between them is the delisting, not a deviation anyone
could have observed as a market. Amendment H5-2 excludes them from the
contemporaneous universe and keeps them here as the sharpest available
evidence for the registration's own honesty clause.

**One further observation, which belongs in this document more than
anywhere else.** Of the 57 delisted instruments, **32 are still being served
an unbroken hourly funding series** — 168 rows each, the most recent stamped
`2026-08-28T21:00Z`, on markets with zero open interest, zero volume and no
book. The venue is accruing funding on instruments where nothing trades.
Nothing states Section 4's point more plainly: **these fields are the
venue's bookkeeping, and bookkeeping continues after the market stops.**

## 6. The funding-service answer, per instrument

`funding field` is the presence of the `funding` key on the asset context.
`fundingHistory (7d)` is the terminal call state of a one-page probe over the
last seven days, and `rows` its row count. **No funding rate value is read on
any H5 path**; these are counts, states and timestamps only.

| instrument | underlying | kind | listing | reference | funding field | fundingHistory (7d) | rows | l2Book | touch bp |
|---|---|---|---|---|---|---|---:|---|---:|
| `io:NBIS` | NBIS | equity | live | `oraclePx` | yes | `stored` | 8 | `stored` | 1.44 |
| `io:SNDK` | SNDK | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.68 |
| `mkts:SMALL2000` | RUT | index | live | `oraclePx` | yes | `stored` | 55 | `stored` | 22.32 |
| `mkts:US500` | SPX | index | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.52 |
| `mkts:USTECH` | NDX | index | live | `oraclePx` | yes | `stored` | 168 | `stored` | 3.07 |
| `para:AAOI` | AAOI | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 57.11 |
| `para:AVGO` | AVGO | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 33.35 |
| `para:CIEN` | CIEN | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 57.84 |
| `para:COHR` | COHR | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 3.22 |
| `para:CRDO` | CRDO | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 9.45 |
| `para:CRWD` | CRWD | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 45.77 |
| `para:GLW` | GLW | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 33.63 |
| `para:IREN` | IREN | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 5.33 |
| `para:LRCX` | LRCX | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.98 |
| `para:MELI` | MELI | equity | live | `oraclePx` | yes | `stored` | 105 | `stored` | 58.02 |
| `para:NET` | NET | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 57.97 |
| `para:RDDT` | RDDT | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 6.52 |
| `para:SMCI` | SMCI | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 57.96 |
| `para:STX` | STX | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 14.23 |
| `para:TER` | TER | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 35.92 |
| `para:VST` | VST | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 27.63 |
| `xyz:AAOI` | AAOI | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.88 |
| `xyz:AAPL` | AAPL | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.63 |
| `xyz:AMAT` | AMAT | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 4.97 |
| `xyz:AMD` | AMD | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.64 |
| `xyz:AMZN` | AMZN | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.50 |
| `xyz:ARM` | ARM | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.25 |
| `xyz:ASML` | ASML | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.76 |
| `xyz:AVGO` | AVGO | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 2.44 |
| `xyz:BABA` | BABA | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.68 |
| `xyz:BB` | BB | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 11.27 |
| `xyz:BE` | BE | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.95 |
| `xyz:BX` | BX | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 16.16 |
| `xyz:COIN` | COIN | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.56 |
| `xyz:COST` | COST | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 10.47 |
| `xyz:CRCL` | CRCL | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.15 |
| `xyz:CRWD` | CRWD | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 4.58 |
| `xyz:CRWV` | CRWV | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.07 |
| `xyz:DELL` | DELL | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 2.41 |
| `xyz:DKNG` | DKNG | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 20.97 |
| `xyz:EBAY` | EBAY | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 18.91 |
| `xyz:EWJ` | EWJ | etf | live | `oraclePx` | yes | `stored` | 168 | `stored` | 5.64 |
| `xyz:EWT` | EWT | etf | live | `oraclePx` | yes | `stored` | 168 | `stored` | 3.72 |
| `xyz:EWY` | EWY | etf | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.11 |
| `xyz:EWZ` | EWZ | etf | live | `oraclePx` | yes | `stored` | 168 | `stored` | 3.10 |
| `xyz:GEV` | GEV | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 8.09 |
| `xyz:GIGADEV` | SSE:603986 | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 7.34 |
| `xyz:GME` | GME | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 2.23 |
| `xyz:GOOGL` | GOOGL | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.87 |
| `xyz:HIMS` | HIMS | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 12.11 |
| `xyz:HOOD` | HOOD | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.92 |
| `xyz:HYUNDAI` | KRX:005380 | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 5.52 |
| `xyz:IBM` | IBM | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 3.82 |
| `xyz:INTC` | INTC | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.34 |
| `xyz:IREN` | IREN | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 2.25 |
| `xyz:JP225` | NI225 | index | live | `oraclePx` | yes | `stored` | 168 | `stored` | 8.06 |
| `xyz:KIOXIA` | TSE:285A | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 10.25 |
| `xyz:KORU` | KORU | etf | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.93 |
| `xyz:KR200` | KOSPI200 | index | live | `oraclePx` | yes | `stored` | 168 | `stored` | 12.27 |
| `xyz:LITE` | LITE | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 2.34 |
| `xyz:LLY` | LLY | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 4.26 |
| `xyz:MAGS` | MAGS | etf | live | `oraclePx` | yes | `stored` | 168 | `stored` | 17.79 |
| `xyz:META` | META | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.52 |
| `xyz:MRNA` | MRNA | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 6.56 |
| `xyz:MRVL` | MRVL | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.46 |
| `xyz:MSFT` | MSFT | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.37 |
| `xyz:MSTR` | MSTR | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.79 |
| `xyz:MU` | MU | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.64 |
| `xyz:NBIS` | NBIS | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.44 |
| `xyz:NET` | NET | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 3.00 |
| `xyz:NFLX` | NFLX | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 2.45 |
| `xyz:NOK` | NOK | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 8.82 |
| `xyz:NOW` | NOW | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 5.59 |
| `xyz:NVDA` | NVDA | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.46 |
| `xyz:ORCL` | ORCL | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.66 |
| `xyz:PLTR` | PLTR | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.08 |
| `xyz:QCOM` | QCOM | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.22 |
| `xyz:RDDT` | RDDT | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 20.87 |
| `xyz:RIVN` | RIVN | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 13.74 |
| `xyz:RKLB` | RKLB | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 2.94 |
| `xyz:SMH` | SMH | etf | live | `oraclePx` | yes | `stored` | 168 | `stored` | 7.58 |
| `xyz:SMSN` | SMSN | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.07 |
| `xyz:SNDK` | SNDK | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.68 |
| `xyz:SOFTBANK` | TSE:9984 | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 60.64 |
| `xyz:SOXL` | SOXL | etf | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.89 |
| `xyz:SP500` | SPX | index | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.13 |
| `xyz:TSLA` | TSLA | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 0.29 |
| `xyz:TSM` | TSM | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 1.19 |
| `xyz:URNM` | URNM | etf | live | `oraclePx` | yes | `stored` | 168 | `stored` | 4.72 |
| `xyz:USAR` | USAR | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 6.64 |
| `xyz:WDC` | WDC | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 2.82 |
| `xyz:XBI` | XBI | etf | live | `oraclePx` | yes | `stored` | 31 | `stored` | 20.90 |
| `xyz:XLE` | XLE | etf | live | `oraclePx` | yes | `stored` | 168 | `stored` | 8.77 |
| `xyz:ZM` | ZM | equity | live | `oraclePx` | yes | `stored` | 168 | `stored` | 9.93 |
| `abcd:USA500` | SPX | index | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `cash:AMZN` | AMZN | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:CAR` | CAR | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:EWY` | EWY | etf | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:GOOGL` | GOOGL | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:HOOD` | HOOD | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:INTC` | INTC | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:KWEB` | KWEB | etf | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:META` | META | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:MSFT` | MSFT | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:NVDA` | NVDA | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:TSLA` | TSLA | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `cash:USA500` | SPX | index | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `flx:COIN` | COIN | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `flx:CRCL` | CRCL | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `flx:NVDA` | NVDA | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `flx:TSLA` | TSLA | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `flx:USA100` | NDX | index | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `flx:USA500` | SPX | index | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `io:EWY` | EWY | etf | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `io:IONQ` | IONQ | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `km:AAPL` | AAPL | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:BABA` | BABA | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:BMNR` | BMNR | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:GOOGL` | GOOGL | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:JPN225` | NI225 | index | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `km:MU` | MU | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:NVDA` | NVDA | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:PLTR` | PLTR | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:RTX` | RTX | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:SMALL2000` | RUT | index | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:TENCENT` | HKEX:0700 | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:TSLA` | TSLA | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:US500` | SPX | index | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:USTECH` | NDX | index | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `km:XIAOMI` | HKEX:1810 | equity | delisted | `oraclePx` | yes | `stored` | 168 | `no_data` | — |
| `mkts:AAPL` | AAPL | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:BABA` | BABA | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:BMNR` | BMNR | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:GOOGL` | GOOGL | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:JPN225` | NI225 | index | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:MU` | MU | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:NVDA` | NVDA | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:PLTR` | PLTR | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:RTX` | RTX | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:TENCENT` | HKEX:0700 | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:TSLA` | TSLA | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `mkts:XIAOMI` | HKEX:1810 | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `para:CAMBRICON` | SSE:688256 | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `para:INNOLIGHT` | SZSE:300308 | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `para:NAVER` | KRX:035420 | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `para:TENCENT` | HKEX:0700 | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `xyz:IBIDEN` | TSE:4062 | equity | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `xyz:IBOV` | IBOV | index | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `xyz:KSTR` | KSTR | etf | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `xyz:NIFTY` | NIFTY50 | index | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
| `xyz:VIX` | VIX | index | delisted | `oraclePx` | yes | `no_data` | 0 | `no_data` | — |
