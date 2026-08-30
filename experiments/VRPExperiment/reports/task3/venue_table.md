# TASK 3 — Venue reachability. The first deciding measurement.

**Measured 2026-08-30, 04:32Z–05:35Z.** Every classification below is evidenced
by published text recorded with its URL and its date. **No venue was joined, no
account was opened, no order was placed, no proxy or VPN was used.**

## Reference spot, measured live from two independent public endpoints

| asset | Coinbase `api.coinbase.com/v2/prices/{}/spot` | Kraken `api.kraken.com/0/public/Ticker` (last) | disagreement |
|---|---|---|---|
| BTC-USD | **$78,124.575** | $78,115.50 | **1.16 bps** |
| ETH-USD | **$2,456.205** | $2,455.41 | **3.24 bps** |

Both endpoints served HTTP 200 and require no account. **The Coinbase figure is
used downstream**, registered here before use; Kraken is the corroborating
second source and the two agree to within 3.24 bps, `n = 2` sources per asset.

## The venue table

| # | venue / route | product | Canada | British Columbia | classification | evidence |
|---|---|---|---|---|---|---|
| 1 | **Deribit** | BTC/ETH options, DVOL futures | **prohibited** | **prohibited** | **PROHIBITED** | Restricted Jurisdictions, stamped `2026-03-19T16:49:36Z`, retrieved 2026-08-30. "Canada" listed bare, with **no** exemption or partial-restriction qualifier, unlike 5 other entries. |
| 2 | **CME options on Micro Ether futures (MET) via Interactive Brokers Canada Inc.** | option on 1 MET future = **0.10 ETH** | permitted | permitted | **PERMITTED** | IBKR **Canada Inc.** publishes a dedicated product page; CIRO member; registered office Montreal, Quebec. |
| 3 | **CME options on Micro Bitcoin futures (MBT) via Interactive Brokers Canada Inc.** | option on 1 MBT future = **0.10 BTC** | permitted | permitted | **PERMITTED, capital status UNRESOLVED** | Same page. Capital feasibility turns on an initial margin that is `Absent(not_served)` — see below. |
| 4 | **CME Bitcoin options (full size)** | option on 1 BTC future = **5 BTC** | permitted | permitted | **CAPITAL_BLOCKED** | Notional **$390,622.88** = **390.6×** the $1,000 sleeve. Blocked at any margin above 0.26% of notional. |
| 5 | **CME Ether options (full size)** | option on 1 ETH future = **50 ETH** | permitted | permitted | **CAPITAL_BLOCKED** | Notional **$122,810.25** = **122.8×** the sleeve. Blocked at any margin above 0.81% of notional. |
| 6 | **Hyperliquid** | 232 perpetuals | permitted | permitted | **NO_PRODUCT** | Measured: `POST /info {"type":"meta"}` → HTTP 200, 17,495 bytes, **universe n = 232**, **zero** instrument names matching a call/put/strike pattern. Three options-endpoint probes (`optionMeta`, `optionsMeta`, `metaOptions`) each returned **HTTP 422 "Failed to deserialize the JSON body into the target type"**. |
| 7 | **Canadian-listed covered-call crypto ETFs** (Purpose BTCY, Purpose ETHY, Global X BCCL) | fund units on TSX | permitted | permitted | **NOT AN OPTION PRODUCT** — fails registered criterion 3.1(2) | These are packaged funds that write calls internally. The resident buys a unit, not an option. Costs measured: **BTCY MER 1.28%**; **ETHY management fee 1.10%, MER 1.29%, MER capped 1.48%**. |
| 8 | **CIRO-registered Canadian crypto venues** (e.g. Webull Canada Crypto Ltd., CIRO approval 2026-06-30) | **spot only** — BTC, ETH, SOL, XRP, ADA, LTC | permitted | permitted | **NO_PRODUCT** | No CIRO-registered venue was found offering crypto **options** directly. **The CIRO-registered route to crypto options is row 2/3 itself**: IBKR Canada Inc. is a CIRO member. |

## Row 2 and 3 — the permissioning question the prompt asked, answered

The prompt asks whether CME micro crypto options are "**permissioned for Canadian
retail clients rather than merely listed on the US site**." **They are
permissioned.** The evidence is that the page is served by the *Canadian entity's
own domain* and signed by the Canadian entity:

- URL: `https://www.interactivebrokers.ca/en/trading/cme-micro-bitcoin-ether-options.php` — **HTTP 200, 123,443 bytes**, retrieved 2026-08-30T05:15Z.
- Page title, verbatim: **"CME Group Micro Bitcoin and Micro Ether Options | Interactive Brokers Canada Inc."**
- Footer, verbatim: **"Interactive Brokers Canada Inc. Is a member of the Canadian Investment Regulatory Organization (CIRO) and Member - Canadian Investor Protection Fund. Registered Office: 1800 McGill College Avenue, Suite 2106, Montreal, Quebec, H3A 3J6, Canada."**
- Call to action, verbatim: **"If you already have Options trading permission, you can begin trading CME Group Options on Micro Bitcoin and Micro Ether Futures. If you do not already have Options trading permission, log in to Client Portal and request Options trading permission via the Settings > Account Settings > Trading Experience & Permissions menu item. Trading permission requests are typically approved overnight."**
- Risk statement, verbatim: **"TRADING OPTIONS ON CME MICRO BITCOIN AND MICRO ETHER FUTURES IS ESPECIALLY RISKY AND IS ONLY FOR CLIENTS WITH A HIGH RISK TOLERANCE AND THE FINANCIAL ABILITY TO SUSTAIN LOSSES."**

There is no jurisdictional carve-out anywhere on the Canadian page excluding
British Columbia or any province. The corresponding **futures**-only page
(`cme-micro-bitcoin.php`, HTTP 200, 120,250 bytes) is also served by the Canadian
entity, so the options offering is not an artifact of a shared template that only
covers futures in Canada.

**This contradicts the registered expectation.** Section 9.1 priced
VENUE_BLOCKED at 0.76 largely on the assumption that no reachable venue would
offer an option product. **At least one does.**

## Contract specifications, measured, each with its `n`

Source: the IBKR Canada product page above, `n = 1` published specification page
per product, retrieved 2026-08-30.

| item | Options on **MBT** | Options on **MET** |
|---|---|---|
| underlying | **One Micro Bitcoin futures contract (= 0.10 bitcoin)** | **One Micro Ether futures contract (= 0.10 ether)** |
| minimum price increment | **$5.00 per bitcoin = $0.50 per contract** for premium above $25.00 per bitcoin; **$1.00 per bitcoin = $0.10 per contract** for premium ≤ $25.00 per bitcoin | **$0.50 per ether = $0.05 per contract** |
| listed expiries | One nearest Monday · one nearest Wednesday · **four nearest weekly Friday contracts (Weeks 1, 2, 3, 4)** · **two nearest Monthly contracts** | same |
| **notional at measured spot** | **$7,812.46** | **$245.62** |
| settlement | into the underlying micro future | into the underlying micro future |

The **two nearest Monthly contracts** are what the registered 30-day tenor of
Section 2.1 trades. The weekly Fridays bracket 30 days and are what the
Section 2.2 fallback would interpolate across.

## The $1,000 sleeve, and the capital-blocked determination

The registered criterion: a venue supporting **fewer than one position** at
$1,000 is CAPITAL_BLOCKED, which is distinct from prohibited and both are
distinct from reachable.

| product | notional | sleeve ÷ notional | one short option is supported iff | determination |
|---|---|---|---|---|
| **MET option** | **$245.62** | **4.07×** | initial margin ≤ **407.1%** of notional | **NOT capital-blocked.** No margin regime charges four times notional on a short option. The sleeve constraint **is not binding on MET at any initial margin below $1,000 per contract.** |
| **MBT option** | **$7,812.46** | **0.128×** | initial margin ≤ **12.80%** of notional | **UNRESOLVED.** Turns entirely on a figure that is `Absent(not_served)`. Not recorded as capital-blocked, and not recorded as clear. |
| **BTC option (full)** | **$390,622.88** | **0.0026×** | IM ≤ **0.26%** of notional | **CAPITAL_BLOCKED** |
| **ETH option (full)** | **$122,810.25** | **0.0081×** | IM ≤ **0.81%** of notional | **CAPITAL_BLOCKED** |

**The MET row is the finding that moves the experiment.** It is a lawfully
reachable, capital-feasible venue for a short option position at the registered
sleeve size, reached through a CIRO-regulated Canadian dealer.

## Re-verification of carried figures — the measurement wins

Per ADR-055 and Section 3.4, carried figures are re-verified live before use.
**Two disagree, and both disagreements are recorded.**

| carried figure | source and date | re-measured 2026-08-30 | drift | disposition |
|---|---|---|---|---|
| MBT micro bitcoin notional **$6,505** | MLCryptoEngine `report.md:1164`, measured 2026-07-15 | **$7,812.46** (0.10 × $78,124.575) | **+20.1%** | **The measurement wins.** The carried figure is 46 days stale and understates notional by a fifth. Every sleeve calculation above uses $7,812.46. |
| MET micro ether notional **$191** | MLCryptoEngine `report.md:1165`, measured 2026-07-15 | **$245.62** (0.10 × $2,456.205) | **+28.6%** | **The measurement wins.** Used above. |
| MET cost **101.76 bps**, MBT **6.21 bps** (futures round turn) | MLCryptoEngine, 2026-07-15 | not re-measured here — these are **futures** commission-per-notional figures, and TASK 5 measures the **option** leg | — | Carried forward only as context, never as an input. Recorded in `docs/VENUE_TABLE_UPDATE.md` with the notional correction that changes them. |
| **ADR-034**: "Hyperliquid at 3 bps is the cheapest BC-reachable venue and the only one offering a short, and it lists perpetuals rather than options" | MLCryptoEngine `DECISIONS.md:1480`, 2026-08-04 | **Confirmed on the options half.** Hyperliquid's own API returns **232 perpetuals and zero options**, `n = 232` instruments enumerated; three options-endpoint probes all HTTP 422. **No options product has listed since 2026-07.** | — | **Confirmed.** But the *implication* ADR-034 carried — that no BC-reachable venue offers a short in this asset class — **is now false for options**: IBKR Canada → CME MET does. |

## Recorded absences — CME margins

**The prompt required current CME initial and maintenance margin for MES, MNQ,
MGC and MBT through IBKR Canada.** These are not needed for this hypothesis; they
were sought for the program-level venue table.

**Result: `Absent(not_served)` for all four, and for the short-option margin on
MBT and MET.** The reason is recorded and is not a failure of effort:

1. **CME Group is the primary source and it refused, citing its own Data Terms
   of Use.** The refusal is recorded verbatim in `reports/task3/robots_and_terms.md`.
   Fetching stopped on receipt. Terms bind.
2. **Interactive Brokers Canada does not publish per-contract margin publicly.**
   `https://www.interactivebrokers.ca/en/trading/margin-futures-fops.php`
   (HTTP 200, 275,624 bytes) and `.../margin-requirements.php` (HTTP 200,
   275,624 bytes) both serve a **wizard and a table-view chooser**, not values;
   the margin figures sit behind Client Portal. Verbatim from the page:
   **"Margin Requirements [Wizard View] — Your Margin Requirements are based on
   the following: ... After making your selection in Step 3 below, you will
   automatically be taken to the margin requirements page."** The legacy endpoint
   `index.php?f=marginnew&p=fut` returns 17,299 bytes containing **no MBT, MES,
   MNQ or MGC margin row** (the apparent "mes" matches are substrings of
   ordinary words such as "times" and "names").
3. **MLCryptoEngine holds no CME margin figure to carry.** A grep across its
   markdown and `config/venues.yaml` for "initial margin", "maintenance margin"
   and "SPAN margin" returns **zero** rows. There was never a carried figure
   here; these would have been new measurements.

**No margin value is synthesized, estimated from a rule of thumb, or taken from a
third-party aggregator.** A figure obtained by working around CME's refusal would
be a measurement of someone's copy of the schedule, not of the schedule.

**Open operator item, carried to `docs/HANDOVER.md`:** an operator holding an
IBKR Canada account can read initial and maintenance margin for MES, MNQ, MGC,
MBT and for short MBT/MET options directly in Client Portal or TWS, and can
settle the MBT capital question against the measured threshold **IM ≤ 12.80% of
$7,812.46 = $1,000.00**. This repository holds no broker credential and none is
planned.

## One measured cost datum found while here, recorded because it binds on TASK 5

Verbatim from `interactivebrokers.ca/en/trading/margin-futures-fops.php`:

> "Interactive Brokers calculates and charges a daily **'Exposure Fee'** to
> customer accounts that are deemed to have significant risk exposure. ...
> **Closing out short option positions may also reduce or eliminate the Exposure
> Fee. Testing has indicated that short positions in low-priced options generate
> the largest exposures relative to the amount of capital.**"

A short option book at this broker can attract a **daily** charge that is not a
commission and not a spread, and the broker names short options as the position
type that generates it. Its magnitude is account-specific and is
`Absent(not_served)`. It is recorded here so TASK 5's cost figure is read as
**incomplete in a known direction**, never as complete.
