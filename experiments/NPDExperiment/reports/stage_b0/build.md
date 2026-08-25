# Stage B.0. Data, features, baselines, sealed

Built 2026-08-25T17:06:19.142206+00:00.

## Source integrity

Two read-only paths were opened and no others. `news_experiment.db` was never opened.

- `backtest/universe.py` sha256 before the extract: `8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529`
- `backtest/universe.py` sha256 after the extract:  `8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529`
- unchanged: **True**
- re-hashed at report time: `8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529`

The bar store was opened through a SQLite immutable read-only URI, so a write is impossible at the driver level rather than by convention.

## Extract

- daily bars copied: **15,474,106**
- distinct symbols: **18,474**
- every 1day row carries adjustment `all` and venue `alpaca`, verified before the copy

## Universe reproduction

Rule `U-LIQ-500-stk-w60-m40-p5`. The ported machinery rebuilt each formation from bars and was checked against the source own stored membership. A single differing symbol or rank fails the check.

- formations reproduced: **55**
- verified against the source: **55**
- failures: **0**
- members per formation: **500 to 500**
- range: 2022-01-03 through 2026-07-01

## Panel coverage by month, window only

| month | sessions | panels drawn | coverage |
|---|---|---|---|
| 2024-10 | 1 | 1 | 100% |
| 2024-11 | 20 | 20 | 100% |
| 2024-12 | 21 | 21 | 100% |
| 2025-01 | 20 | 20 | 100% |
| 2025-02 | 19 | 19 | 100% |
| 2025-03 | 21 | 21 | 100% |
| 2025-04 | 21 | 21 | 100% |
| 2025-05 | 21 | 21 | 100% |
| 2025-06 | 20 | 20 | 100% |
| 2025-07 | 22 | 22 | 100% |
| 2025-08 | 21 | 21 | 100% |
| 2025-09 | 21 | 21 | 100% |
| 2025-10 | 23 | 23 | 100% |
| 2025-11 | 19 | 19 | 100% |
| 2025-12 | 22 | 22 | 100% |
| 2026-01 | 20 | 20 | 100% |
| 2026-02 | 19 | 19 | 100% |
| 2026-03 | 22 | 22 | 100% |
| 2026-04 | 21 | 21 | 100% |
| 2026-05 | 20 | 20 | 100% |
| 2026-06 | 21 | 21 | 100% |
| 2026-07 | 17 | 17 | 100% |
| **total** | **432** | **432** | **100%** |

## Feature blocks and anonymization

- feature rows stored, fit period and window: **308,610**
- days carrying an anonymization mapping: **432**
- features per name per day: **9**
- every feature cross-sectionally z-scored within the day, across exactly the rows the model sees

## Baseline completion

| baseline | window days ranked |
|---|---|
| `sign_last` | 432 |
| `mom_12_1` | 432 |
| `logistic` | 432 |

The logistic baseline was fitted once on **21322** rows across **711** days, 2022-01-03 through 2024-10-30, strictly before the window start of 2024-10-31. Frozen coefficient digest:

    fe6f60067cb23f5e6daf467b0056817e93d5742e6b6018748ded03b635946043

`load_fit_targets` refuses any date after the guard band end, so the fit cannot reach a window outcome even if the two return stores were ever pointed at one file.

## Sealing

Forward returns are split by date and the split is the seal.

| store | dates | permitted reader |
|---|---|---|
| `var/npd_fit.db` | strictly before the window start | `npd.baselines.logistic` |
| `var/npd_sealed.db` | inside the window | `npd.eval.evaluator` and nothing else |

`npd.data.forward_returns` writes both and has no reader at all. `tests/test_guards.py` walks every source file and fails when another module names the sealed store, calls the sealed reader, or adds a read to the writer.

## Power, recomputed from the built window

- window: 2024-10-31 through 2026-07-24, **432 trading days**
- evaluable at the primary five-session horizon: **427**
- null daily rank IC standard deviation at 30 names: **0.185695**
- registered floor MDE: **0.01787** against a floor of 0.025. Clears it.
- overlap variance inflation at h=5: **3.4000000000000004**, effective days **125.6**

| corr(model, best baseline) | detectable at t 2.0 | powered at 80 percent |
|---|---|---|
| 0.00 | 0.0469 | 0.0666 |
| 0.30 | 0.0392 | 0.0557 |
| 0.50 | 0.0331 | 0.0471 |
| 0.70 | 0.0257 | 0.0365 |

At the middle cell the primary contrast covers the upper part of the registered band 0.01 to 0.05, from 0.0331.

