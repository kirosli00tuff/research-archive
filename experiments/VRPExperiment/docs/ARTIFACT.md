# The BTC and ETH variance risk premium, and whether a British Columbia resident can reach it

**A measurement, 2026-08-30.** Self-contained: nothing else in this repository
needs to be read to use it.

---

## What was asked

Two questions, and the second is the one that has not been answered elsewhere.

1. **Does the option market charge more volatility than BTC and ETH
   subsequently deliver?** — the variance risk premium.
2. **Can anyone resident in British Columbia lawfully harvest it, at a cost
   below the premium, with about $1,000?**

No capital was deployed. No order was placed. No venue was joined. No account
was opened. Every figure below was read from a public endpoint or a published
schedule that required no registration.

---

## The answer in plain words

**The premium is real and large in bitcoin. It is smaller and unreliable in
ether. And the arithmetic that decides reachability is not about the premium at
all — it is about contract size.**

A British Columbia resident *can* lawfully trade crypto options: Interactive
Brokers Canada Inc., a CIRO member, offers CME options on Micro Bitcoin and
Micro Ether futures to Canadian clients. That was the surprise; the expectation
going in was that no reachable venue would offer the product.

But of the two contracts, only **Micro Ether** is small enough that a $1,000
sleeve certainly supports a position — and Micro Ether is so small
(**$245.62** of underlying per contract) that the **broker's commission alone,
at $0.20 a contract, costs 122 basis points of notional over one hedged
round trip.** The ether premium is worth about **119 basis points**. **The
commission is larger than the premium**, before a single cent of bid-ask,
exchange fee or margin is charged.

**Micro Bitcoin** would clear the hurdle comfortably — its notional is 31.8×
larger, so the same style of commission costs only **16 basis points** against a
bitcoin premium worth **198**. But whether $1,000 covers the margin on a short
Micro Bitcoin option **could not be established without a brokerage account**,
and CME refused automated access to its margin schedule, citing its own terms of
use. That refusal was obeyed.

**So: the premium exists, the venue exists, and the one route that is certainly
affordable is the one where the premium does not cover the commission.**

---

## The premium, measured

**Source:** Deribit's public API — the DVOL 30-day model-free implied volatility
index, and Deribit's own perpetual for the underlying. No account. Both series
taken hourly and filtered to **08:00 UTC**, which is Deribit's option settlement
instant.

**Definition, fixed before any data was read:**
`VRP = (30-day implied volatility) − (realized volatility over the following 30
days)`, in annualised volatility points. Realized volatility is close-to-close,
sample standard deviation with `ddof=1`, annualised by `√365`. **Positive means
the option market charged more than the underlying delivered.**

| | **BTC** | **ETH** |
|---|---|---|
| **n** | **1,955 daily observations** | **1,955 daily observations** |
| window | 2021-03-24 → 2026-07-30 | 2021-03-24 → 2026-07-30 |
| **mean premium** | **8.66 volatility points** | **5.20 volatility points** |
| **as basis points of notional** | **198.11 bps** | **119.05 bps** |
| standard error (Newey–West, bandwidth 30) | 0.0147 | 0.0215 |
| **t** | **5.888** | **2.418** |
| **one-sided p** | **2.3 × 10⁻⁹** | **7.9 × 10⁻³** |
| **one-sided 95% CI lower bound** | **142.74 bps** | **38.01 bps** |
| share of observations positive | 73.86% | 64.55% |

**Robustness.** Repeating the test on **66 non-overlapping** 30-day windows —
which removes the overlap-induced autocorrelation entirely at the cost of 96% of
the sample — gives **BTC 220.87 bps, t = 4.568, p = 1.1 × 10⁻⁵** and **ETH
132.79 bps, t = 2.088, p = 0.020**. Both agree with the headline in sign and in
significance.

### Stability: the two assets behave differently, and it matters

Split into four equal quarters of the sample:

| period | n | **BTC** | **ETH** |
|---|---|---|---|
| 2021-03-24 → 2022-07-24 | 488 | **+284.53 bps** (p = 0.00026) | +146.27 bps (**p = 0.146, n.s.**) |
| 2022-07-25 → 2023-11-24 | 488 | **+250.59 bps** (p = 6.8 × 10⁻⁵) | **+291.21 bps** (p = 3.1 × 10⁻⁵) |
| 2023-11-25 → 2025-03-26 | 488 | **+145.13 bps** (p = 0.0046) | **−18.56 bps** (**negative**, p = 0.597) |
| 2025-03-27 → 2026-07-30 | 491 | **+112.72 bps** (p = 0.018) | +57.66 bps (**p = 0.211, n.s.**) |

**BTC is significant in every quarter but decaying monotonically — down 60.4%
across the sample.** A reader planning around this should assume the decay
continues rather than that the average persists.

**ETH is significant in one quarter of four, and is negative in another.** The
full-sample ether result rests heavily on the 2022–2023 window. **It should not
be relied on as a stable property of ether.**

---

## Venue reachability, measured

Every classification below rests on published text recorded with its URL and its
date. **No proxy or VPN was used, and no prohibition was worked around.**

| venue / route | product | Canada / BC | classification |
|---|---|---|---|
| **Deribit** | BTC & ETH options, deepest book | **prohibited** | **PROHIBITED** |
| **CME Micro Ether options** via IBKR Canada | option on **0.10 ETH**, $245.62 notional | permitted | **PERMITTED, capital-feasible — and cost-exceeded** |
| **CME Micro Bitcoin options** via IBKR Canada | option on **0.10 BTC**, $7,812.46 notional | permitted | **PERMITTED — capital status UNRESOLVED** |
| CME Bitcoin options, full size | 5 BTC, **$390,622.88** | permitted | **CAPITAL-BLOCKED** (390.6× the sleeve) |
| CME Ether options, full size | 50 ETH, **$122,810.25** | permitted | **CAPITAL-BLOCKED** (122.8× the sleeve) |
| **Hyperliquid** | **232 perpetuals, 0 options** | permitted | **NO PRODUCT** |
| Canadian covered-call crypto ETFs (BTCY, ETHY, BCCL) | TSX fund units | permitted | **NOT AN OPTION PRODUCT** — the buyer holds a fund, not an option. BTCY MER **1.28%**, ETHY MER **1.29%** |
| CIRO-registered crypto venues (e.g. Webull Canada, approved 2026-06-30) | **spot only** | permitted | **NO PRODUCT** |

**Deribit.** Its Restricted Jurisdictions page, stamped
`2026-03-19T16:49:36Z` and still current on retrieval, states: *"The access and
use of our platform, and the services we offer, are not allowed if you are
located, incorporated or otherwise established in, or a resident of, any of the
jurisdictions in the overview below"*, and lists **"Canada"**. Five other
entries carry narrowing qualifiers — Belarus and Russia exempt EEA and Swiss
nationals; Panama and the UAE restrict only *Retail Investors* and only to
*spot*; the UK only *Retail Clients*; Ukraine only three named regions.
**Canada carries none.** It is an unconditional whole-country prohibition.

**Hyperliquid.** Measured, not assumed: its public API enumerates **232
perpetual instruments and zero options**, and three separate options-endpoint
probes each returned HTTP 422. No options product has listed there.

**The sleeve arithmetic**, at measured spot (BTC **$78,124.575**, ETH
**$2,456.205**, two independent public sources agreeing to 1.16 and 3.24 basis
points):

| contract | notional | $1,000 sleeve ÷ notional | supported iff initial margin ≤ |
|---|---|---|---|
| **Micro Ether option** | **$245.62** | **4.07×** | **407.1% of notional** — no margin regime is near this, so **not capital-blocked** |
| **Micro Bitcoin option** | **$7,812.46** | **0.128×** | **12.80% of notional** — **unresolved; see below** |

---

## Cost, measured — and what could not be measured

**Commission, from Interactive Brokers Canada's live published schedule
(retrieved 2026-08-30), lowest volume tier:**

| contract | commission per contract |
|---|---|
| **CME Micro Ether futures & futures options (MET)** | **USD 0.20** |
| **CME Micro Bitcoin futures & futures options (MBT)** | **USD 0.85** |
| CME Bitcoin, full size (BRR) | USD 5.00 |
| CME Ether, full size | USD 3.00 |
| CME micro equity/metal futures & options (MES, MNQ, M2K, MGC and 25 others) | USD 0.25 |

**In basis points of notional**, for one hedged short straddle round trip — two
option contracts opened and closed, plus the delta hedges the registered rule
requires (median **11** rebalances, 90th percentile **16**, measured over
**1,955** paths):

| | **Micro Ether (MET)** | **Micro Bitcoin (MBT)** |
|---|---|---|
| straddle round trip | **32.57 bps** | **4.35 bps** |
| delta hedge, central (11 rebalances) | 89.57 bps | 11.97 bps |
| delta hedge, pessimistic (16 rebalances) | 130.28 bps | 17.41 bps |
| **total, central** | **122.14 bps** | **16.32 bps** |
| **total, pessimistic** | **162.85 bps** | **21.76 bps** |
| **premium available (CI lower bound)** | **38.01 bps** | **142.74 bps** |

> **Every cost figure above is a strict LOWER BOUND. Three of five cost legs
> could not be measured, and each of them is non-negative, so the true cost is
> higher — possibly much higher.**

**What could not be measured, and why:**

| missing leg | why |
|---|---|
| **CME exchange and regulatory fees** | CME Group refused automated access, citing its **own Data Terms of Use**: *"This IP address is blocked due to suspected web scraping activity… Use of scripts, software, spiders, robots… is strictly prohibited by CME Group's website Data Terms of Use."* Fetching stopped on receipt and was not worked around. IBKR's schedule states these fees are **additional** to the commission. |
| **Option bid-ask on MET and MBT** | No public source serves CME crypto option quotes without an account. IBKR's quote page returns a 404 body, Barchart 404, Yahoo Finance HTTP 401. |
| **Delta-hedge bid-ask** | Same. |
| *(also)* **IBKR's daily "Exposure Fee"** | The broker states it charges one on risky accounts and that *"short positions in low-priced options generate the largest exposures relative to the amount of capital."* Account-specific; not obtainable. |

**No figure was substituted for any of these.** In particular, no spread was
carried from another instrument or another venue. That substitution is a known
way to get this kind of measurement badly wrong: a sibling study in this
programme carried a slippage band from an index ETF onto single stocks, and when
finally measured on the traded instrument, **five of six legs were understated
and the resulting adjustment was 11.27× larger** than the carried one — while a
sixth was *over*stated, so "assume worse" would not have rescued it either.

**For reference only — not a substitute, and not used in any conclusion.** On
Deribit, the venue British Columbia residents may *not* use, the same 30-day ATM
straddle's quoted round-trip spread was measured across **24 observation windows
per leg, 96 observations, zero unquoted**: **BTC 22.50 bps, ETH 25.00 bps** at
the medians. Spreads were tick-bound — every observed value an exact multiple of
the 0.0005-coin tick, with the touch at two ticks in the modal case.

> This permits one comparison that needs no substituted figure:
> **the commission alone on the affordable permitted route (32.57 bps for the
> straddle, 122.14 bps with its hedge) already exceeds the entire quoted spread
> cost of the same trade on the prohibited venue (22.50 / 25.00 bps).**

---

## The conclusion

**Micro Ether — decided, and not by a close margin.**
The ether premium's point estimate is **119.05 bps**. The **central,
commission-only, lower-bound cost is 122.14 bps**. **The premium does not cover
the commission.** Against the pre-registered requirement that the premium's
lower confidence bound exceed twice the pessimistic cost, it **fails by 8.6×**.
Because every cost input is a lower bound, no further measurement can reverse
this — additional cost data can only widen the gap.

**Micro Bitcoin — not decided, and not decidable from outside a brokerage
account.**
The bitcoin premium's lower confidence bound is **142.74 bps** against a
commission-only pessimistic cost of **21.76 bps** — it clears the registered 2×
hurdle by **3.28×**, and would still clear it at the maximum possible **29**
rebalances. **Two figures would settle it, and only two:**

1. **The initial margin on a short Micro Bitcoin option.** It must be **≤ 12.80%
   of the $7,812.46 notional — that is, ≤ $1,000 per contract** — for a $1,000
   sleeve to hold one position at all.
2. **The all-in bid-ask plus CME exchange and regulatory fees.** At the
   pessimistic end these must total **≤ 49.61 bps of notional**, which is the
   room between the premium's lower bound and twice the measured commission.

Both are visible in an Interactive Brokers Canada client portal in a single
session. Neither is obtainable without one.

**The registered verdict: VENUE_BLOCKED**, on the routes that could be resolved,
with Micro Bitcoin recorded as open on exactly those two figures.

---

## What this does **not** establish

Stated plainly, because the figures above are easy to misread as a trading case.

- **No strategy was simulated.** There is no backtest, no equity curve, no
  drawdown and no Sharpe ratio anywhere behind this document. A premium is not a
  return.
- **No fill was modelled.** The costs are quoted commissions and, where absent,
  bounds. Queue position, partial fills and market impact are not measured.
- **The tail is not measured, and it is the whole risk.** Selling variance pays
  a premium precisely because the seller absorbs the move that does not appear in
  a 5.4-year sample. **This measures the payment and not the liability.** A
  reader who takes 198 bps as an expected return has read it wrong.
- **The ether premium is not stable** — one significant quarter of four, one
  negative — and the bitcoin premium is **decaying 60% across the sample**.
- **Cost and policy are dated measurements, not constants.** Fee schedules,
  margins and jurisdiction policies change. Everything here is true as of
  **2026-08-30** and of no later date.
- **Nothing here is advice**, and no part of it should be acted on without
  independent verification against a live account.

---

## Reproducing it

Everything above came from endpoints requiring no account:

| what | where |
|---|---|
| implied volatility, 30-day, BTC & ETH | Deribit `public/get_volatility_index_data`, resolution `3600` (**seconds**) |
| underlying daily closes | Deribit `public/get_tradingview_chart_data`, `BTC/ETH-PERPETUAL`, resolution `60` (**minutes** — the two endpoints use different units) |
| history available | **1,992 days**, established by bisection, ≈ 2021-03-17 |
| reference option quotes | Deribit `public/get_order_book` |
| commissions | `interactivebrokers.ca/en/pricing/commissions-futures.php` |
| venue policy | `support.deribit.com/hc/en-us/articles/25944487427741-Restricted-Jurisdictions` |
| spot | Coinbase `api.coinbase.com/v2/prices/{}/spot`, corroborated by Kraken |

**Data revision was checked, because a silently revised series would rewrite the
measurement.** Six fixed historical windows (BTC and ETH at 45, 365 and 900 days
back, 169 rows each) were digested and re-fetched ≈ 70 minutes later: **all six
byte-identical.** Note that the whole HTTP response digest **does** change
between calls — Deribit's envelope carries per-request timing fields — so the
comparison must be made on the data array alone. Comparing whole responses
reports a revision that did not occur.
