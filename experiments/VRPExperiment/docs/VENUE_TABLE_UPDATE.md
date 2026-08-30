# Venue cost table — corrections to carry across to MLCryptoEngine

**Prepared 2026-08-30 by VRPExperiment. For the operator to carry across.**

> **The MLCryptoEngine repository was not edited and must not be edited by this
> repository.** This file exists so the corrections can be applied there
> deliberately, with their provenance attached.

The table in question is `MLCryptoEngine/HYPOTHESES.md` §"venue cost table"
(around line 303), together with the CME per-contract block below it. That block
already carries the right warning — *"Treat these as dated measurements, not
constants"* — and the two corrections below are that warning coming due.

---

## Correction 1 — US single-name equity intraday is the programme's most expensive venue

**Source:** ORBExperiment, re-verified live from its own repository on
2026-08-30 rather than quoted from memory.

> **US single-name equity, intraday, entry: time-weighted half spread, median
> `0.076572` USD per share, 90th percentile `0.333662`, `n = 550` minutes
> served, 0 refused.**

Provenance: `ORBExperiment/README.md:300`, `ORBExperiment/docs/HANDOVER.md:59`,
and the underlying measurement in
`ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json:74`
(`0.07657173002730797`). *(The governing prompt quoted this as `0.0766`; the
measured value is `0.076572` and the measurement is what is recorded.)*

**Converted to the table's units.** A half spread of `0.076572` USD/share is a
round-trip spread cost of `2 × 0.076572 = 0.153144` USD/share. On a typical
share price near **100 USD** that is **≈ 153 bps round trip**.

**Suggested row:**

| venue | per side | **round trip** | verified |
|---|---|---|---|
| US single-name equity, intraday (ORB universe, opening-relative-volume selected) | **7.66 bps** at a 100 USD share price | **≈ 153 bps** | 2026-08-29 (ORB), re-verified 2026-08-30 |

**Why it belongs in the table.** At ≈ 153 bps round trip this is **the most
expensive venue the programme has measured** — roughly **1.9× Coinbase spot's
80 bps**, **3.1× Kraken's 50 bps**, and **51× Hyperliquid's 3 bps**. The table
currently implies crypto spot is the programme's cost ceiling. It is not.

**Two qualifications that must travel with the row, or it will be misread.**

1. **It is a spread, not a fee.** Every other row in that table is a
   *commission* schedule. This one is a measured *touch spread*. They are not
   the same quantity and should not be silently summed. The equity row's own
   commission is additional and is not measured here.
2. **The bps figure is price-dependent and the USD figure is not.** `0.076572`
   USD/share is the measurement; the ≈ 153 bps depends entirely on the share
   price assumed. On a 20 USD share it is ≈ 766 bps; on a 500 USD share, ≈ 31
   bps. **Carry the USD figure as primary and the bps as derived**, or the row
   will drift the way the CME rows did (Correction 2).

---

## Correction 2 — the CME micro notionals are stale, and the bps figures move with them

**Source:** measured live 2026-08-30 by this repository, from Coinbase's public
spot endpoint (BTC **$78,124.575**, ETH **$2,456.205**), corroborated by Kraken
to within **1.16 bps** and **3.24 bps** respectively, `n = 2` sources per asset.

MLCryptoEngine's CME block is dated **2026-07-15**. **Forty-six days later both
crypto notionals have moved by roughly a fifth to a quarter**, and because those
rows are *per-contract fees expressed in basis points of notional*, **the bps
figures moved with them.**

| contract | notional recorded 2026-07-15 | **notional measured 2026-08-30** | drift |
|---|---|---|---|
| **MBT** micro bitcoin (0.10 BTC) | $6,505 | **$7,812.46** | **+20.1%** |
| **MET** micro ether (0.10 ETH) | $191 | **$245.62** | **+28.6%** |

**Both carried figures understate notional, so both carried bps figures
overstate cost.** Mechanically: a higher notional divides the same
per-contract fee, so the cost in bps **falls**.

**Suggested replacement rows**, using this repository's independently measured
IBKR Canada commission schedule (`interactivebrokers.ca/en/pricing/commissions-futures.php`,
retrieved 2026-08-30, lowest volume tier ≤ 1,000 contracts/month):

| contract | notional | commission/side | round turn | **cost bps** |
|---|---|---|---|---|
| MBT micro bitcoin | **$7,812.46** | **$0.85** | $1.70 | **2.176** |
| MET micro ether | **$245.62** | **$0.20** | $0.40 | **16.285** |

**These are NOT directly comparable to the recorded 6.211 and 101.762 bps, and
the difference must not be read as a cost reduction.** Three things differ:

1. **The commission source differs.** MLCryptoEngine's round turns ($4.04 for
   MBT, $1.94 for MET) are larger than IBKR Canada's commission alone ($1.70 and
   $0.40). The most likely reason is that the recorded figures are **all-in**,
   including CME exchange and regulatory fees, while the figures above are
   **commission only**.
2. **This repository could not measure the exchange-fee component.** CME Group
   refused automated access citing its own Data Terms of Use (HTTP 403, refusal
   recorded verbatim in `reports/task3/robots_and_terms.md`), and the refusal was
   obeyed. **The exchange and regulatory legs are `Absent(not_served)` here.**
   IBKR's own schedule states them to be additional to the commission:
   *"non-member exchange and regulatory fees are applied."*
3. **Therefore the rows above are LOWER BOUNDS on cost, and the recorded rows
   are not.** They should be added as a **separate, clearly labelled
   commission-only pair**, or the notionals alone should be corrected while the
   all-in bps figures are re-measured at source. **They should not silently
   replace the existing rows.**

**The stable, unambiguous correction is the notional column.** $6,505 → $7,812.46
and $191 → $245.62 are direct measurements from a public endpoint, corroborated
by a second, and they are correct regardless of how the fee side is resolved.

---

## Correction 3, offered — a structural note the table would benefit from

MLCryptoEngine's table already says **"the cheapest venue reachable from British
Columbia is Hyperliquid at 3 bps, and it is also the only one offering a
short"** (ADR-034). **The first half is confirmed; the second half is now
incomplete for options.**

Measured 2026-08-30: **Interactive Brokers Canada Inc., a CIRO member with a
registered office in Montreal, offers CME options on Micro Bitcoin and Micro
Ether futures to Canadian clients**, on its own `.ca` domain, with the verbatim
call to action *"If you already have Options trading permission, you can begin
trading CME Group Options on Micro Bitcoin and Micro Ether Futures."* A short
option position is a short. Separately, Hyperliquid's own API enumerates **232
perpetuals and zero options**, with three options-endpoint probes each returning
HTTP 422 — so ADR-034's description of Hyperliquid remains exactly right.

**Suggested amendment to the standing note:** Hyperliquid is the cheapest
BC-reachable venue **for perpetuals** and the only BC-reachable short **in that
instrument class**; **for options the BC-reachable route is IBKR Canada → CME**,
at a commission cost that depends entirely on which contract is used —
**2.176 bps on MBT against 16.285 bps on MET, a 7.5× spread on the same
schedule, purely from notional.** That is ADR-023's finding arriving as a
binding constraint rather than a curiosity.

---

## Recorded absences the programme table should carry

**`Absent(not_served)`: CME initial and maintenance margin for MES, MNQ, MGC and
MBT, and short-option margin for MBT and MET.** These were sought specifically
for the programme venue table, since this was the cheapest opportunity to
measure them. They could not be obtained:

1. CME Group refused automated access, citing its own Data Terms of Use; fetching
   stopped on receipt and was not worked around.
2. Interactive Brokers Canada does not publish per-contract margin publicly —
   both margin pages (HTTP 200, 275,624 bytes) serve a wizard and a table-view
   chooser rather than values; the figures sit behind Client Portal.
3. MLCryptoEngine holds no margin figure to carry: a grep for "initial margin",
   "maintenance margin" and "SPAN margin" across its markdown and
   `config/venues.yaml` returns **zero** rows.

**Nothing was synthesized.** An operator with an IBKR Canada login can read all
six figures in one session, and the one that decides an open question in this
repository is: **the initial margin on a short MBT option must be ≤ 12.80% of
the $7,812.46 notional, i.e. ≤ $1,000 per contract**, for a $1,000 sleeve to
hold one position.
