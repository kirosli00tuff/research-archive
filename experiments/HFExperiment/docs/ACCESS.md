# Broker access, measured

Stage A.1 Task 2. Every figure carries its source and retrieval date. All
retrievals 2026-08-23 unless marked. Claims from the stage prompt were
re-verified rather than inherited.

## Broker table

| broker | Canadian residents | US equities | order-placing API | fractional through API | account minimum | commission (US stocks) | inactivity or maintenance fees | cash account |
|---|---|---|---|---|---|---|---|---|
| IBKR Canada | yes [1] | yes [1] | yes, TWS API and Web API [1] | UNVERIFIED, settled by test in Task 3 | none [2] | Pro Tiered 0.0035/sh, min 0.35, cap 0.5 pct. Pro Fixed 0.005/sh, min 1.00, cap 1 pct. Fractional orders: greater of 1 pct of value or 0.01 [2] | none found on the .ca Other Fees page [3] | yes, and sub-2,000 USD forces one [8] |
| Alpaca | NO [4] | yes | yes | yes | none | zero commission | none | yes |
| Questrade | yes | yes | NO for customers, partner developers only [5] | n/a | none | n/a | none | yes |
| Wealthsimple | yes | yes | NO official API, ToS prohibits API trading [6] | n/a | none | zero commission, 1.5 pct FX [7] | none | yes |

Verdict: IBKR Canada is the only reachable broker that clears residency,
US equities, and an order-placing API at once. Alpaca excludes Canadian
residents today. Its careers page advertises a Canadian broker-dealer
controller role, so the exclusion may lift. Recheck at stage C if Task 3
resolves badly.

Sources:

1. https://www.interactivebrokers.ca/en/pricing/commissions-stocks.php and
   https://www.interactivebrokers.ca/en/trading/fractional-trading.php
   (.ca pages, RRSP and TFSA menus present, Canadian entity)
2. https://www.interactivebrokers.ca/en/pricing/commissions-stocks.php
   ("no added spreads, ticket charges, platform fees, or account minimums")
3. https://www.interactivebrokers.ca/en/pricing/other-fees.php
   (no inactivity line item anywhere on the page)
4. https://alpaca.markets/support/countries-alpaca-is-available
   ("Residents of Canada are not currently eligible")
5. https://www.questrade.com/api ("Executing trades using the API is
   available to Questrade partner developers only")
6. https://github.com/MarkGalloway/wealthsimple-trade (unofficial docs,
   notes ToS prohibition and enforcement warnings)
7. https://www.interactivebrokers.ca/en/trading/us-stock-trading-costs-for-canadian-resi.php
   (IBKR comparison table quoting Wealthsimple 1.50 pct FX, as of
   2026-04-29 per the page)
8. FINRA margin rules require 2,000 USD minimum equity for a margin
   account, so a 1,000 USD account is a cash account and long-only by
   construction.

## IBKR Lite

Lite is US-resident only. A Canadian applicant gets Pro. Sources:
https://www.interactivebrokers.com/en/trading/why-ibkr-lite.php and
https://www.elitetrader.com/et/threads/is-ibkr-lite-only-for-us-residents.346306/

## The cap rule, in IBKR's own words

From the .ca commissions page disclosures, retrieved 2026-08-23:

> In the event the calculated maximum per order is less than the minimum
> per order, the maximum per order will be assessed. For example, a
> purchase to buy 10 shares of a $0.20 stock will be charged $0.02
> (10 shares x 0.005/share = 0.05 commission, minimum 1.00 per Order,
> capped at 10 shares x 0.20 x 1% = 0.02).

The US stocks table lists maximum per order as 1 pct of trade value for
both plans, and a separate disclosure line narrows Tiered:

> Tiered commissions will be capped at 0.5% of trade value

Confirmed: Tiered cap 0.5 pct, min 0.35. Fixed cap 1 pct, min 1.00.
Derived crossovers confirmed: cap equals minimum at 70 USD Tiered and
100 USD Fixed. Below those figures every whole-share order pays the cap.

## The fractional-order schedule, a finding

The same disclosures carry a separate schedule for fractional orders:

> Fractional share trades are subject to the same commission rates as
> whole share trades, with a minimum commission of USD 0.01. For each
> fractional share trade, you will be charged the greater of 1% of the
> trade value or USD 0.01.

The page's own examples bill pure sub-share trades at 1 pct of value, not
at the plan cap. If that schedule applies to any order with a fractional
quantity, a 45 USD fractional order pays 100 bp per side, not the 50 bp
the settled sizing assumed, on either plan. Whether a mixed
integer-plus-fraction order bills whole on this schedule or splits is not
determinable from the page. This does not touch the slippage measurement,
because commission is deterministic and subtracts exactly. It doubles the
projected commission drag. The A.2 cost model must carry the fractional
row until a paper fill measures the real billing. Task 3 gains a sub-test
for it.

## Regulatory rates

| fee | rate | source |
|---|---|---|
| SEC Section 31 | 20.60 USD per million of sale proceeds, effective 2026-04-04 | https://www.sec.gov/rules-regulations/fee-rate-advisories/2026-2 and https://www.finra.org/rules-guidance/notices/information-notice-20260317 |
| FINRA TAF | 0.000195 USD per share sold, max 9.79 per trade, effective 2026-01-01 | FINRA information notice 2026-03-17 above, matching the IBKR .ca commissions page pass-through line |
| FINRA CAT | 0.000003 USD per share | IBKR .ca commissions page |
| NSCC and DTC clearing | 0.0002 USD per share, Tiered pass-through | IBKR .ca commissions page |

The one cent TAF floor the settled design assumed is CONFIRMED NOWHERE.
FINRA's schedule has no per-trade minimum and IBKR's page states none.
Exact TAF on a one-share sell is 0.0195 cents. The cost model holds the
one cent floor as a worst-case bound on billing granularity until a real
fill statement settles it. The gap is 0 to 2.2 bp at 45 USD.

The FINRA rulebook page still serves the pre-2026 text (0.000166, max
8.30, eff. 2024). The 2026-03-17 information notice and IBKR's live page
agree on the new rate. Recorded as rulebook lag.

## A resolvable discrepancy, resolved and immaterial

The IBKR .ca US-stock-costs page and commissions page both quote Tiered
tier one at 0.0035 per share. A Canadian broker review
(https://www.brokerguide.ca/blog/interactivebrokers-canada-fees-2026)
quotes 0.006. The .ca commissions page lists 0.006 as tier one for USD
DENOMINATED CANADIAN listings, which is the likely source of the review's
figure. At four to five shares neither rate binds, because the cap or the
0.35 minimum dominates both. No figure in the table below moves.

## Cost arithmetic

Assumed share price 45 USD for share counts. Regulatory drag uses the
worst-case one cent TAF floor. CAT and clearing pass-throughs are below
0.1 bp at these sizes and are omitted from the table. Generated by
scripts/cost_table.py from src/hfexperiment/commission.py.

| notional | plan | commission/side | binds | reg drag sell side | round trip |
|---|---|---|---|---|---|
| 30 | tiered | 0.1500 (50.0 bp) | cap | 0.0106 (3.54 bp) | 0.3106 (103.5 bp) |
| 30 | fixed | 0.3000 (100.0 bp) | cap | 0.0106 (3.54 bp) | 0.6106 (203.5 bp) |
| 30 | fractional | 0.3000 (100.0 bp) | 1pct floor | 0.0106 (3.54 bp) | 0.6106 (203.5 bp) |
| 45 | tiered | 0.2250 (50.0 bp) | cap | 0.0109 (2.43 bp) | 0.4609 (102.4 bp) |
| 45 | fixed | 0.4500 (100.0 bp) | cap | 0.0109 (2.43 bp) | 0.9109 (202.4 bp) |
| 45 | fractional | 0.4500 (100.0 bp) | 1pct floor | 0.0109 (2.43 bp) | 0.9109 (202.4 bp) |
| 70 | tiered | 0.3500 (50.0 bp) | minimum | 0.0114 (1.63 bp) | 0.7114 (101.6 bp) |
| 70 | fixed | 0.7000 (100.0 bp) | cap | 0.0114 (1.63 bp) | 1.4114 (201.6 bp) |
| 70 | fractional | 0.7000 (100.0 bp) | 1pct floor | 0.0114 (1.63 bp) | 1.4114 (201.6 bp) |
| 100 | tiered | 0.3500 (35.0 bp) | minimum | 0.0121 (1.21 bp) | 0.7121 (71.2 bp) |
| 100 | fixed | 1.0000 (100.0 bp) | minimum | 0.0121 (1.21 bp) | 2.0121 (201.2 bp) |
| 100 | fractional | 1.0000 (100.0 bp) | 1pct floor | 0.0121 (1.21 bp) | 2.0121 (201.2 bp) |
| 180 | tiered | 0.3500 (19.4 bp) | minimum | 0.0137 (0.76 bp) | 0.7137 (39.7 bp) |
| 180 | fixed | 1.0000 (55.6 bp) | minimum | 0.0137 (0.76 bp) | 2.0137 (111.9 bp) |
| 180 | fractional | 1.8000 (100.0 bp) | 1pct floor | 0.0137 (0.76 bp) | 3.6137 (200.8 bp) |

The 70 USD Tiered row sits exactly on the crossover, where the cap equals
the minimum and either label prices the same 0.35. Below 70 the Tiered
cap binds. Below 100 the Fixed cap binds. The fractional schedule is flat
at 100 bp per side at every notional in range, so under fractional
billing there is no size relief anywhere.

The whole-share Tiered claim from the settled design is confirmed: 30 and
69 cost the same 50 bp rate, and 45 deploys the full stake at that rate.
The claim held only for whole-share billing. The fractional schedule was
not in the settled design and is the one new material fact this
measurement produced.

## Currency conversion

Funding is CAD into USD once. IBKR spot FX carries a 2.00 USD minimum
commission (us-stock-costs page comparison table, note 6). About 20 bp
one time on 1,000 USD. Not part of the round-trip arithmetic.

## The API routing constraint, in IBKR's own words

From the .ca commissions page disclosures:

> Please note that directed API orders cannot use the Tiered fee
> structure. SmartRouted API orders can use either the Tiered or Fixed
> structure.

SmartRouting is therefore a registered constraint on the order path. A
directly routed API order forfeits Tiered pricing. Stage C.1's order gate
must refuse non-SmartRouted orders.

## Task 3: fractional through the API, BLOCKED-ON-OPERATOR

The operator holds no IBKR account. Every sub-test below is blocked until
one exists, live, with the Trade in Fractions permission enabled in
Client Portal, because a paper account inherits the live account's
permissions. No sub-test was resolved by reading documentation.

| sub-test | status | what must be true to run |
|---|---|---|
| decimal totalQuantity order on a liquid tier-1 name, paper gateway | BLOCKED-ON-OPERATOR | live account exists, Trade in Fractions enabled, paper gateway reachable |
| cashQty order on the same name | BLOCKED-ON-OPERATOR | same |
| decimal order via SmartRouting and direct, compared | BLOCKED-ON-OPERATOR | same |
| MinSize and SizeIncrement from reqContractDetails on the same symbol | BLOCKED-ON-OPERATOR | same |
| billing plan of a SmartRouted API order confirmed on a real paper fill | BLOCKED-ON-OPERATOR | same |
| billing of a mixed integer-plus-fraction order against the fractional schedule | BLOCKED-ON-OPERATOR | same, added by the fractional-schedule finding above |

The documentation conflict stands unresolved on purpose: IBKR staff wrote
in June 2026 that the API does not support cash-quantity orders outside
crypto, a third-party guide from March 2026 claims the opposite, and an
Elite Trader thread reports cashQty rounding down to whole shares through
the Web API. The likely resolution is that cashQty is unsupported while
decimal share quantities work, which the quote-first-divide-then-submit
path handles. Likely is not measured. The verdict waits for the test.
