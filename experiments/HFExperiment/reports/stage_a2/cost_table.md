## Round-trip table, measured spreads

Spread term: measured book median 12.77 bp, 2026-07-01 width-20 book, consolidated tape, sessions 2026-08-19 to 2026-08-21. Unmeasured names: none. Share counts use the measured median mid 103.25 USD. TAF holds the worst-case one cent floor, UNMEASURED.

| notional | regime | commission/side | binds | spread rt bp | reg bp | total rt bp |
|---|---|---|---|---|---|---|
| 30 | whole_tiered | 0.1500 (50.0 bp) | cap | 12.77 | 3.54 | 116.3 |
| 30 | whole_fixed | 0.3000 (100.0 bp) | cap | 12.77 | 3.54 | 216.3 |
| 30 | fractional | 0.3000 (100.0 bp) | fractional_1pct | 12.77 | 3.54 | 216.3 |
| 45 | whole_tiered | 0.2250 (50.0 bp) | cap | 12.77 | 2.43 | 115.2 |
| 45 | whole_fixed | 0.4500 (100.0 bp) | cap | 12.77 | 2.43 | 215.2 |
| 45 | fractional | 0.4500 (100.0 bp) | fractional_1pct | 12.77 | 2.43 | 215.2 |
| 70 | whole_tiered | 0.3500 (50.0 bp) | minimum | 12.77 | 1.63 | 114.4 |
| 70 | whole_fixed | 0.7000 (100.0 bp) | cap | 12.77 | 1.63 | 214.4 |
| 70 | fractional | 0.7000 (100.0 bp) | fractional_1pct | 12.77 | 1.63 | 214.4 |
| 100 | whole_tiered | 0.3500 (35.0 bp) | minimum | 12.77 | 1.21 | 84.0 |
| 100 | whole_fixed | 1.0000 (100.0 bp) | minimum | 12.77 | 1.21 | 214.0 |
| 100 | fractional | 1.0000 (100.0 bp) | fractional_1pct | 12.77 | 1.21 | 214.0 |
| 180 | whole_tiered | 0.3500 (19.4 bp) | minimum | 12.77 | 0.76 | 52.4 |
| 180 | whole_fixed | 1.0000 (55.6 bp) | minimum | 12.77 | 0.76 | 124.6 |
| 180 | fractional | 1.8000 (100.0 bp) | fractional_1pct | 12.77 | 0.76 | 213.5 |

## Annual deterministic drag at measured churn

| width | churn/mo | fills/mo | regime | commission/yr | reg/yr | total/yr |
|---|---|---|---|---|---|---|
| 20 | 5.2 | 10.4 | whole_tiered | 28.08 | 0.68 | 28.76 |
| 20 | 5.2 | 10.4 | whole_fixed | 56.16 | 0.68 | 56.84 |
| 20 | 5.2 | 10.4 | fractional | 56.16 | 0.68 | 56.84 |
| 5 | 2.0 | 4.0 | whole_tiered | 16.80 | 0.33 | 17.13 |
| 5 | 2.0 | 4.0 | whole_fixed | 48.00 | 0.33 | 48.33 |
| 5 | 2.0 | 4.0 | fractional | 86.40 | 0.33 | 86.73 |

## The registered cost hurdle

Primary width 5, churn 2.0 names per month, per-name notional 180 USD, worst-case fractional regime. Width-5 book measured spread 13.08 bp at median mid 201.91 USD. Round trip 213.84 bp. Hurdle 4.07 bp per day. Registered: 4.07.

## Verdict honest arithmetic

rho tuned for 1600 trading days at alpha 0.05: 0.071641. If the width-5 mean holds at 27.99 bp per day against 418 bp daily noise, the lower bound clears zero at day 2061 and clears the registered hurdle at day 2852.
