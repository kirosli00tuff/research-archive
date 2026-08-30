# VRPExperiment

**A single-stage census of the BTC and ETH variance risk premium, and whether a
British Columbia resident can lawfully harvest it below cost.**

**Status: CLOSED, 2026-08-30. Verdict: VENUE_BLOCKED**, qualified — one route
open on two named figures. One stage, one artifact, no successor in this
repository.

**No capital was deployed. No order was placed. No venue was joined. No account
was opened. No proxy or VPN was used.**

> **Read [`docs/ARTIFACT.md`](docs/ARTIFACT.md).** It is the deliverable and is
> self-contained.

---

## The verdict in one sentence

> A large, significant variance risk premium exists in BTC (**198.11 bps of
> notional, n = 1,955, p = 2.3 × 10⁻⁹**) and a smaller, unstable one in ETH
> (**119.05 bps, n = 1,955, p = 7.9 × 10⁻³**); the only lawfully reachable venue
> that is unambiguously affordable at $1,000 charges **more in commission alone
> (122.14 bps) than the ETH premium is worth**; and the one route that would
> clear the hurdle cannot be settled without a brokerage account this repository
> does not have and will not open.

---

## What is measured — every figure with its n

### The premium

| figure | value | n |
|---|---|---|
| BTC premium, mean | **0.086607 vol points = 198.111 bps of notional** | **1,955 daily observations** |
| BTC HAC standard error (Newey–West, bandwidth 30) | 0.014709 | 1,955 |
| BTC t / one-sided p | **5.888 / 2.297 × 10⁻⁹** | 1,955 |
| BTC one-sided 95% CI lower bound | **142.740 bps** | 1,955 |
| BTC share of observations positive | 0.7386 | 1,955 |
| ETH premium, mean | **0.052045 vol points = 119.052 bps** | **1,955** |
| ETH HAC standard error | 0.021528 | 1,955 |
| ETH t / one-sided p | **2.418 / 7.859 × 10⁻³** | 1,955 |
| ETH one-sided 95% CI lower bound | **38.012 bps** | 1,955 |
| ETH share of observations positive | 0.6455 | 1,955 |
| BTC non-overlapping robustness | 220.872 bps, t 4.568, p 1.128 × 10⁻⁵ | **66 windows** |
| ETH non-overlapping robustness | 132.793 bps, t 2.088, p 0.0203 | **66 windows** |
| BTC quarterly means (decay 60.4%) | +284.53 / +250.59 / +145.13 / +112.72 bps | 488 / 488 / 488 / 491 |
| ETH quarterly means (**one significant, one negative**) | +146.27 (n.s.) / +291.21 / **−18.56** / +57.66 bps | 488 / 488 / 488 / 491 |
| conversion, registered before any data | **1 volatility point = 22.875 bps of notional** | — |

### Cost — every figure a strict lower bound

| figure | value | n |
|---|---|---|
| MET commission | **USD 0.20 / contract** | 1 published schedule, 2026-08-30 |
| MBT commission | **USD 0.85 / contract** | 1 published schedule, 2026-08-30 |
| MES / MNQ / M2K / MGC commission | **USD 0.25 / contract** | 1 published schedule |
| MET straddle round trip | **32.571 bps** | — |
| MBT straddle round trip | **4.352 bps** | — |
| rebalances, registered ±0.10 band, 30-day tenor | **median 11, p90 16** (BTC max 20, ETH max 22) | **1,955 paths per asset** |
| rebalances at ±0.05 / ±0.20 (swept, not chosen) | median 17 / median 5 | 1,955 each |
| **MET total, central / pessimistic** | **122.140 / 162.853 bps** | — |
| **MBT total, central / pessimistic** | **16.320 / 21.760 bps** | — |
| CME exchange & regulatory fees | **`Absent(not_served)`** — CME's Data Terms of Use refusal | — |
| MET / MBT option and hedge bid-ask | **`Absent(not_served)`** — no public source | — |
| Deribit reference straddle spread (**not a cost input**) | BTC **22.50 bps**, ETH **25.00 bps** round trip | **24 windows/leg, 96 observations, 0 unquoted** |

### Venue reachability

| figure | value | n |
|---|---|---|
| BTC spot / ETH spot | **$78,124.575 / $2,456.205** (Kraken agrees to 1.16 / 3.24 bps) | 2 sources each |
| MET option notional | **$245.62** — sleeve buys **4.07×** | — |
| MBT option notional | **$7,812.46** — sleeve buys **0.128×**; needs IM ≤ **12.80%** | — |
| CME full-size BTC / ETH option notional | $390,622.88 / $122,810.25 — **390.6× / 122.8×** the sleeve | — |
| Deribit policy | **Canada PROHIBITED**, stamped `2026-03-19T16:49:36Z` | 1 page, verbatim |
| Hyperliquid options | **zero**, alongside 232 perpetuals | 232 instruments enumerated |
| Canadian covered-call crypto ETF fees | BTCY MER **1.28%**, ETHY MER **1.29%** | 2 funds |
| **CME margins (MES, MNQ, MGC, MBT)** | **`Absent(not_served)`** — open operator item | — |

### Data access

| figure | value | n |
|---|---|---|
| Deribit public endpoints served without an account | **9 of 9 valid, HTTP 200** | 11 probes |
| DVOL history depth, **bisected** | **1,992 days** (≈ 2021-03-17) | 22 probes/asset |
| live option instruments | **1,026 BTC, 876 ETH** | 1 enumeration each |
| rate refusal | **none drawn at or below 126.76 req/s** — an upper bound *not reached* | 126 requests/endpoint |
| page size | **1,000 rows**, with a `continuation` token; pagination verified contiguous | 2 pages |
| **revision** | **all six fixed windows byte-identical after ≈ 70 minutes** | 6 windows × 169 rows |
| sources requiring an account (refused) | **Laevitas, Amberdata** | 2 |
| sources serving option-level IV but **snapshot only** | OKX, Bybit, Binance | 3 |

---

## Repository map

| file | what it holds |
|---|---|
| **`docs/ARTIFACT.md`** | **the deliverable — self-contained, citable** |
| `REGISTRATION.md` | Sections 0–9, committed **before any network call**; Amendment 1 |
| `HYPOTHESES.md` | H1, the fired verdict, and prior calibration |
| `DECISIONS.md` | numbered ADRs |
| `docs/DUPLICATION.md` | the duplication screen and the three-closure reasoning |
| `docs/ACCESS.md` | TASK 4 — what the public endpoints serve, and refuse |
| `docs/COSTS.md` | TASK 5 — cost, and the three legs that are `Absent` |
| `docs/HANDOVER.md` | open operator items |
| `docs/VENUE_TABLE_UPDATE.md` | corrections for MLCryptoEngine's programme venue table |
| `progress.md` | append-only ledger, one entry per task, ETA against actual |
| `reports/` | machine-readable evidence, including both TASK 6 latches |
| `src/vrp/` | five structural guards and the sealed reader |

## Running it

```bash
make install      # uv venv on Python 3.13, dev extras
make all          # ruff format + check, mypy strict, pytest
make guards       # the structural guards alone, verbosely
```

**`make all` is green: 50 tests, mypy strict clean, ruff clean.**

**The TASK 6 latch is spent and is not re-runnable.** `--mode real` raises
`LatchAlreadySpentError`. `--mode fixture` runs the identical pipeline against
synthetic data with a known planted premium and touches no latch.
