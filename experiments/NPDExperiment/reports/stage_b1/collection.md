# Stage B.1. The live gate collection

Completed 2026-08-25T19:47:12.959961+00:00.

Gate model `gpt-5-2025-08-07`, reasoning effort `minimal`, temperature not sent (Amendment 1).

Prompt template digest `7e6f3d6801506bd7b158d7937b8fc3bae82c8fffac6770acaeb924bc4391c7fb`.

## Window

- 2024-10-31 through 2026-07-24
- **432 trading days**, derived from the verified cutoff 2024-09-30 plus a one month guard band
- clears the registered 200 day floor: **True**

## Per-state counts

The five states are never merged.

| state | days | class |
|---|---|---|
| `stored` | 415 | sample |
| `no_data` | 0 | sample composition |
| `model_failed` | 17 | **operational health** |
| `excluded_pre_cutoff` | 0 | **sample composition** |
| `source_failed` | 0 | operational health |
| **total** | **432** | |

## Coverage against the Section 0 bars

- eligible days, `excluded_pre_cutoff` removed from the denominator: **432**
- days carrying a stored, parseable ranking: **415**
- days carrying a full 30 name ranking in the store: **415**
- coverage: **96.1%**

| bar | threshold | met |
|---|---|---|
| GO | at least 90% | yes |
| DEGRADED | 70% to 90% | no |
| BLOCKED | under 70%, or the window under the power floor | no |

## Section 0 verdict: **GO**

96.1% of eligible days carry a stored, parseable ranking, at or above the 90% bar.

## Spend

- gate calls billed: **920**
- calibration calls, excluded from the sample: **2**
- total spent: **6.9378 USD** of a 10.00 USD cap
- remaining: **3.0622 USD**
- measured cost per gate call: **0.007508 USD**
- input tokens: 3,514,278
- output tokens: 361,641, of which reasoning 217,728

## Stored ranking integrity

Structural only. No forward return was read and no output was joined to any
outcome.

| check | days |
|---|---|
| days with a ranking in the store | 415 |
| ranks are exactly 1 to 30 | 415 |
| labels match that day mapping | 415 |
| symbols match that day panel | 415 |
| label to symbol is consistent | 415 |

## Operational health

- attempts under the current procedure: **883**, across 432 days, 2.04 per day
- days needing more than one attempt: **175**
- attempts by reasoning effort: **{'minimal': 813, 'low': 70}**
- superseded attempts, kept in the ledger and excluded from these counts: **74**
- calibration calls, excluded from the sample: **2**
- days whose stored answer came from `low` after an escalation: **53**

| date | attempts |
|---|---|
| 2024-11-06 | 3 |
| 2024-11-12 | 5 |
| 2024-11-18 | 2 |
| 2024-11-20 | 2 |
| 2024-12-02 | 2 |
| 2024-12-06 | 5 |
| 2024-12-09 | 5 |
| 2024-12-11 | 5 |
| 2024-12-16 | 5 |
| 2024-12-17 | 4 |
| 2024-12-20 | 5 |
| 2024-12-23 | 5 |
| 2024-12-26 | 3 |
| 2024-12-30 | 3 |
| 2025-01-02 | 4 |
| 2025-01-03 | 5 |
| 2025-01-10 | 5 |
| 2025-01-14 | 2 |
| 2025-01-16 | 2 |
| 2025-01-17 | 3 |

## What this stage did not do

It computed no rank IC, read no outcome against any output, and fired no
hypothesis verdict. The Section 0 verdict above is fired on coverage alone.
B.2 runs once, later, and only after the operator writes his registered prior
into REGISTRATION.md Section 13.
