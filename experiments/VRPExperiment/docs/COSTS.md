# TASK 5 — Cost measurement on reachable instruments

**The second deciding measurement.** Measured 2026-08-30, 06:15Z–06:55Z.
Machine-readable evidence in `reports/task5/`.

**Section 4 of `REGISTRATION.md` registered no cost figure from anywhere, and
this document carries none.** Every number below was retrieved live from the
venue or broker that charges it, on the date stated. Where a figure could not be
retrieved, it is recorded `Absent` with its reason and **nothing is
substituted**.

---

## 0. Which venues this applies to

Section 4.1 restricts cost measurement to venues classified **PERMITTED** in
TASK 3. That is exactly two routes, both through the same broker:

| route | product | capital status |
|---|---|---|
| **CME options on Micro Ether futures (MET) via IBKR Canada** | option on 0.10 ETH, notional **$245.62** | **capital-feasible** |
| **CME options on Micro Bitcoin futures (MBT) via IBKR Canada** | option on 0.10 BTC, notional **$7,812.46** | **unresolved** — needs IM ≤ 12.80% of notional |

Deribit is **PROHIBITED** and its cost is therefore **not** a cost of this
experiment. It is measured in §4 as an explicitly labelled **reference**, and is
never substituted for a permitted venue's cost.

---

## 1. Commission — **measured live against the published schedule**

Source: `https://www.interactivebrokers.ca/en/pricing/commissions-futures.php`,
**HTTP 200, 489,783 bytes**, retrieved 2026-08-30T06:20Z. `robots.txt` for
`www.interactivebrokers.ca` does not disallow `/en/pricing/`.

The relevant band for a $1,000 sleeve is the lowest volume tier, **≤ 1,000
contracts per month**, where IBKR's Tiered and Fixed rates coincide.

| product (CME, via IBKR Canada) | ≤ 1,000 /mo | 1,001–10,000 | > 20,000 |
|---|---|---|---|
| **Micro Ether futures & futures options (MET)** | **USD 0.20 /contract** | 0.17 tiered / 0.14 fixed | 0.11 |
| **Micro Bitcoin futures & futures options (MBT)** | **USD 0.85 /contract** | 0.71 tiered / 0.57 fixed | 0.43 |
| Bitcoin futures & futures options (BRR, full size) | USD 5.00 /contract | 4.20 / 3.40 | 2.60 |
| Ether futures & futures options (ETH, ETHUSDRR, full size) | USD 3.00 /contract | 2.55 / 2.10 | 1.65 |
| Spot-Quoted / E-Nano / E-micro futures & futures options (**MES, MNQ, M2K, MGC**, and 25 others) | **USD 0.25 /contract** | 0.20 / 0.15 | 0.10 |

### 1.1 The commission is **not** the all-in cost, and the schedule says so

Verbatim from the same page:

> "Aside from the commission, fees charged to clients by IBKR, including but not
> limited to those referenced on this website, are intended to cover the costs of
> execution, **including exchange fees**. Such fees generally reflect the
> exchange fee structure, but in certain circumstances may be higher or lower
> than the fees charged by the exchange."

> "Subject to note 2 above, **non-member exchange and regulatory fees are
> applied**, unless a client is pre-qualified by IBKR."

**The exchange and regulatory legs are additional, and their magnitudes are
CME's published schedule — which is `Absent(not_served)` because CME refused
automated access citing its own Data Terms of Use (TASK 3).** The refusal is
recorded verbatim in `reports/task3/robots_and_terms.md` and was obeyed.

**Consequence, stated plainly: the commission leg of the cost is measured and
the exchange-fee leg is not, so the all-in round-trip cost on the permitted
venue cannot be completed by this repository.** No exchange fee is estimated
from a rule of thumb, inferred from a third party, or carried from another
repository.

### 1.2 Commission in basis points of notional — **measured**

At the measured spot of **BTC $78,124.575** and **ETH $2,456.205** (TASK 3,
`n = 2` independent sources agreeing to 1.16 and 3.24 bps):

| product | notional | commission/side | **one side** | **round trip** |
|---|---|---|---|---|
| **MET option** | $245.62 | $0.20 | **8.143 bps** | **16.285 bps** |
| **MBT option** | $7,812.46 | $0.85 | **1.088 bps** | **2.176 bps** |
| BRR option (5 BTC) | $390,622.88 | $5.00 | 0.128 bps | 0.256 bps |
| ETH option (50 ETH) | $122,810.25 | $3.00 | 0.244 bps | 0.489 bps |

A short ATM **straddle** is two option contracts, so a round trip is four
contract fills:

| straddle round trip, **commission only** | cost | as bps of notional |
|---|---|---|
| **MET** | 4 × $0.20 = **$0.80** | **32.571 bps** |
| **MBT** | 4 × $0.85 = **$3.40** | **4.352 bps** |

Each delta-hedge rebalance trades the underlying micro future once:

| one rebalance fill, **commission only** | cost | as bps of notional |
|---|---|---|
| **MET future** | $0.20 | **8.143 bps** |
| **MBT future** | $0.85 | **1.088 bps** |

### 1.3 The central tension of this experiment, in one number

> **The MET straddle's commission is 7.48× more expensive in basis points than
> the MBT straddle's — 32.571 bps against 4.352 — purely because MET's notional
> is 31.8× smaller.**

**MET is the only route that is unambiguously capital-feasible at $1,000, and it
is the expensive one.** This is MLCryptoEngine ADR-023's finding — *notional
decides everything on CME* — arriving as the binding constraint rather than as a
curiosity. The cheap route (MBT at 4.352 bps) is the one whose capital
feasibility turns on a margin figure this repository could not obtain.

---

## 2. Quoted bid-ask on the permitted instruments — **`Absent(not_served)`**

**Section 4.1 requires the quoted bid-ask on the specific option series that
would be traded, sampled across at least 20 distinct observation windows. It
could not be obtained, and nothing is substituted.**

Attempts, all recorded:

| source | result |
|---|---|
| **CME Group** (primary) | **Not attempted for quotes.** Its Data Terms of Use refusal (HTTP 403, recorded verbatim in TASK 3) binds, and fetching stopped on receipt. |
| **IBKR Canada** | Market data requires an account. `index.php?f=quote&symbol=MBT` → **HTTP 200 serving a "404 Page Not Found" body**, 17,301 bytes. |
| **Barchart** | `barchart.com/futures/quotes/MET*0/options` → **HTTP 404**, 535,327 bytes. |
| **Yahoo Finance** | `query1.finance.yahoo.com/v7/finance/options/BTC=F` → **HTTP 401**, verbatim: `{"finance":{"result":null,"error":{"code":"Unauthorized","description":"Invalid Crumb"}}}` |

**No public source serves CME MET or MBT option quotes without an account.**

**Recorded as `Absent(not_served)`.** This repository holds no market-data
subscription and no broker credential, and plans neither. **Guard 1 enforces the
consequence structurally**: the `Absent` refuses `float()`, `int()`, indexing and
every arithmetic path, so no downstream computation can quietly treat the
missing spread as zero.

**What was explicitly NOT done.** A spread band was not carried from Deribit
(§4), not carried from MLCryptoEngine's futures measurements, not modelled from
tick size, and not inferred from a comparable instrument. **That substitution is
the exact defect ORBExperiment found in its own carried QQQ band, where five of
six legs were understated and the resulting shift was 11.27× too small — and one
leg was *over*stated, which is why the answer is not simply "assume worse".**

**Open operator item:** an operator with an IBKR Canada account and CME crypto
market-data permission can sample the ATM 30-day MET and MBT option bid-ask over
≥ 20 windows and complete this figure. The tenor, series selection rule and
distribution statistics are already registered in Section 4.1 and 4.2 and need
no further decisions.

---

## 3. Delta-hedge cost and rebalance count

### 3.1 The per-rebalance cost is measured; its **count** is not measurable here

Section 4.3 registered the hedging rule before any data: **resize whenever the
position delta moves more than ±0.10 from flat, evaluated once per calendar day
at the fixed UTC instant, over the 30-day tenor**, with ±0.05 and ±0.20 swept as
sensitivity.

**The per-rebalance commission is measured** (§1.2: MET $0.20 = 8.143 bps, MBT
$0.85 = 1.088 bps, plus an unmeasured spread and an unmeasured exchange fee).

**The rebalance count cannot be computed at TASK 5, and the reason is
structural, not practical.** A straddle's delta is `2·N(d₁) − 1`, and `d₁`
requires an implied volatility. **Implied volatility is a blind field.**
Computing the rebalance count therefore requires the sealed read, and is
performed inside TASK 6 rather than here.

**This decomposition is recorded rather than assumed:** TASK 5 measures the
*price per rebalance*, TASK 6 measures the *number of rebalances*, and the two
multiply only after the latch is spent. Doing it any other way would have
required reading an implied volatility before the latch, which is precisely what
the blindness pin exists to prevent.

### 3.2 The hedge instrument is reachable, which is worth stating

The delta hedge is the **MET or MBT future itself**, and TASK 3 established both
are permissioned for Canadian clients through IBKR Canada at the commissions in
§1. Unlike MLCryptoEngine ADR-034's carry trade — where the long leg sat on a
40 bps venue and the short on a 1.5 bps venue, a 27× asymmetry across two sets of
credentials — **both legs here sit on one venue, in one account, at one
commission schedule.** That is a genuine structural advantage of this route and
it did not have to be true.

---

## 4. Reference spread on Deribit — **NOT a cost input**

> **This section measures a venue British Columbia residents may not use.** It
> is recorded because a reader will ask what a liquid crypto option book costs,
> and because the answer turns out to be part of the finding. **It is never
> substituted for a permitted venue's cost, and no verdict in this repository
> reads it.**

Method: the ATM strike at the listed expiry nearest 30 days, for BTC and ETH,
call and put, sampled across **24 registered observation windows** spaced 20
seconds apart. The tool emits **differences only** — spread, half-spread, and
half-spread as a fraction of notional — and never a mid-price, mark price or
premium level, because those are blind until TASK 6. Deribit option contracts
are one coin of underlying quoted in coin units, so **a spread in coin units is
directly a fraction of notional**.

### 4.1 The measured series

| | BTC | ETH |
|---|---|---|
| expiry selected | **2026-09-25T08:00:00Z** | **2026-09-25T08:00:00Z** |
| settlement rule | 08:00 UTC on the expiry date | 08:00 UTC on the expiry date |
| days to expiry at selection | **26.06** | **26.06** |
| ATM strike chosen | **78,000** | **2,500** |
| index level at selection | 78,178.25 | 2,457.21 |
| strikes listed at that expiry | 65 | 64 |
| expiries listed | 13 | 13 |

The registered tenor is 30 days and the nearest listed expiry is **26.06 days**.
Recorded as measured, not adjusted: Deribit lists 13 expiries and none sits
closer to 30 days than this one.

### 4.2 Half-spread as a fraction of notional, `n = 24` windows per leg

**Zero unquoted windows on any leg: 24 of 24 quoted, four legs, 96 observations.**

| leg | n quoted | n unquoted | **median** | **p90** | min | max | full distribution |
|---|---|---|---|---|---|---|---|
| **BTC call** | **24** | 0 | **6.25 bps** | **7.50 bps** | 5.0 | 10.0 | 5.0 ×12, 7.5 ×11, 10.0 ×1 |
| **BTC put** | **24** | 0 | **5.00 bps** | **7.50 bps** | 5.0 | 7.5 | 5.0 ×19, 7.5 ×5 |
| **ETH call** | **24** | 0 | **5.00 bps** | **7.50 bps** | 5.0 | 7.5 | 5.0 ×15, 7.5 ×9 |
| **ETH put** | **24** | 0 | **7.50 bps** | **10.00 bps** | 5.0 | 12.5 | 5.0 ×11, 7.5 ×6, 10.0 ×6, 12.5 ×1 |

### 4.3 The spread is tick-bound, and that is the finding

Raw spreads take only the values **0.0010, 0.0015, 0.0020, 0.0025 coin** —
**every one an exact multiple of the 0.0005-coin tick, which is 5 bps of a
one-coin notional.** The touch sits at **two ticks in the modal case** and never
exceeded five.

This is the same structure MLCryptoEngine found on PUMP, where the spread was
pinned at one tick for 85.5% of a quoted week: **a tick-bound spread cannot
compress**, so competition lengthens the queue rather than narrowing the margin.
Recorded because it means these figures are **stable rather than lucky** — a
24-window sample of a tick-bound quantity is a much better estimate of its
central tendency than 24 windows of a freely-moving one.

Depth at the touch was real, not nominal: BTC call bid sizes 1.5–32.1 and ask
sizes 0.2–16.7; ETH put bid sizes 18–395 and ask sizes 18–764.

### 4.4 The comparison a reader will want, with its warning

A short ATM **straddle** pays the call half-spread plus the put half-spread on
entry and again on exit:

| | one way | **round trip** |
|---|---|---|
| **BTC straddle, Deribit, medians** | 6.25 + 5.00 = **11.25 bps** | **22.50 bps of notional** |
| **ETH straddle, Deribit, medians** | 5.00 + 7.50 = **12.50 bps** | **25.00 bps of notional** |

> **The finding this produces, stated carefully.** The **commission alone** on
> the capital-feasible permitted route — **MET at 32.571 bps round trip, with its
> spread and exchange fee still `Absent`** — already exceeds the **entire quoted
> spread cost** of the same trade on Deribit (**22.50 bps BTC, 25.00 bps ETH**).
>
> **This is a comparison, not a substitution.** It does not give MET a spread,
> it does not complete MET's cost, and it does not enter any verdict. What it
> shows is a *structural* fact about which this repository is entitled to speak:
> **the venue where this trade is cheap is the venue a British Columbia resident
> may not use, and the venue they may use is more expensive in commission alone
> than the other is in total spread.** That statement needs no substituted
> figure to be true.

---

## 5. What Section 4.2 requires, and what can be filled

| Section 4.2 requirement | central end | pessimistic end | status |
|---|---|---|---|
| option leg half-spread | median | 90th percentile | **`Absent(not_served)`** on both permitted venues |
| hedge leg half-spread | median | 90th percentile | **`Absent(not_served)`** on both permitted venues |
| commission | live schedule | live schedule | **MEASURED** — MET $0.20, MBT $0.85 per contract |
| exchange & regulatory fee | live schedule | live schedule | **`Absent(not_served)`** — CME's terms bind |
| rebalance count | rule's median | rule's 90th percentile | **deferred to TASK 6** — requires a blind field |
| **all-in round-trip, fraction of notional** | — | — | **`Absent` — three of five legs are absent** |
| **all-in round-trip, fraction of premium collected** | — | — | **`Absent` — and additionally requires the TASK 6 premium level** |

**The all-in cost is `Absent`, and the honest floor is not zero.** What *is*
measured is a **strict lower bound** on the cost, since every absent leg is
non-negative:

| route | measured lower bound on straddle round-trip cost (commission only) |
|---|---|
| **MET** | **≥ 32.571 bps of notional**, plus rebalance commissions at 8.143 bps each |
| **MBT** | **≥ 4.352 bps of notional**, plus rebalance commissions at 1.088 bps each |

A lower bound is a real constraint and is used as one in TASK 7. **It is never
reported as the cost.**

---

## 6. One further cost that is measured only in its existence

TASK 3 recorded, verbatim from IBKR: *"Interactive Brokers calculates and
charges a daily **'Exposure Fee'** … **Closing out short option positions may
also reduce or eliminate the Exposure Fee. Testing has indicated that short
positions in low-priced options generate the largest exposures relative to the
amount of capital.**"*

A short option book at this broker can attract a **daily** charge that is neither
commission nor spread, and the broker names short options as its largest
generator. **Its magnitude is account-specific and is `Absent(not_served)`.** It
is recorded because it means the lower bounds in §5 are lower bounds **in one
more known direction** than the missing spread and exchange fee alone.
