# Duplication screen — VRPExperiment Stage A

**Run:** 2026-08-30T04:33Z · **Scope:** every repository under
`/home/kiros-li/Documents/GitHub` (14 repositories, VRPExperiment included as
the control row) · **Method:** `grep -rniI`, case-insensitive, binary files
skipped, excluding `.git`, `node_modules`, `.venv`, `__pycache__`, and the four
tool caches. Counts are **matching lines**, not matching files.

The screen is reported in two passes because the first pass is misleading and
saying so is the point. Pass 1 is the raw substring count the prompt asked for.
Pass 2 re-runs the two acronyms under `grep -w` word boundaries, because an
acronym of three or four characters collides with base58 addresses, Bluesky
DIDs and hex digests at a rate that makes the raw count uninterpretable.

---

## Pass 1 — raw substring hit counts, per repo, per term

| repo | variance risk premium | VRP | implied volatility | realized volatility | DVOL | option | straddle | delta hedge | volatility premium |
|---|---|---|---|---|---|---|---|---|---|
| AiTrader | 0 | 0 | 0 | 4 | 0 | 358 | 0 | 0 | 0 |
| ETFExperiment | 0 | 0 | 1 | 0 | 5 | 85 | 4 | 0 | 0 |
| HFExperiment | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| InsiderExperiment | 0 | 4 | 0 | 0 | 40 | 1218 | 2 | 0 | 1 |
| [personal repo, name removed] | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MLCryptoEngine | 0 | 804 | 0 | 1 | 15 | 218 | 2 | 0 | 0 |
| NPDExperiment | 0 | 0 | 0 | 5 | 7 | 4 | 0 | 0 | 0 |
| NPLExperiment | 0 | 0 | 0 | 0 | 0 | 16 | 0 | 0 | 0 |
| ORBExperiment | 0 | 3 | 0 | 0 | 0 | 36 | 4 | 0 | 0 |
| PMExperiment | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| retail-power-limits | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| solattn | 0 | 4154 | 0 | 0 | 22 | 49 | 0 | 0 | 0 |
| solclear | 0 | 7 | 0 | 0 | 0 | 3 | 1 | 0 | 0 |
| **VRPExperiment** *(control)* | 3 | 8 | 2 | 3 | 2 | 10 | 1 | 2 | 2 |

## Pass 2 — the same acronyms under word boundaries (`grep -w`)

| repo | `VRP` word-boundary | `DVOL` word-boundary |
|---|---|---|
| solattn | **0** (raw 4154) | **0** (raw 22) |
| MLCryptoEngine | **0** (raw 804) | **0** (raw 15) |
| InsiderExperiment | **0** (raw 4) | **0** (raw 40) |
| solclear | **0** (raw 7) | — |
| ORBExperiment | **0** (raw 3) | — |
| NPDExperiment | — | **0** (raw 7) |
| ETFExperiment | — | **0** (raw 5) |

**Every VRP and DVOL hit outside this repository is a substring artifact.**
Sampled directly: `solattn/data/attention/mentions-2026-08-23.jsonl` matches
`VRP` inside Bluesky DIDs such as `did:plc:...`;
`MLCryptoEngine/data/vendor/archive/solrpds/2021.csv` matches inside base58
Solana addresses (`...djQm82RpHmE3SuVrPGtZ...`) and
`features_c23.csv` inside `...9XvrpY3shy...`. `DVOL` returns **zero
word-boundary hits in the entire tree** outside this repository. There is no
implied-volatility index anywhere in the program.

## Pass 3 — the substantive phrases, read line by line

`variance risk premium`, `implied volatility`, `volatility premium` and
`delta hedge` return **zero hits in every repository except this one**. The two
remaining phrases were read rather than counted:

**`realized volatility` — 10 lines, none of them an endpoint.** All ten are
realized volatility used as an *input feature* or a *regime switch*:
`AiTrader/config/default_config.yaml:212` and `config.hpp:270` are an
"ADX + realized volatility" regime detector threshold;
`MLCryptoEngine/research/labels/triple_barrier.py:6` uses it to *scale barrier
widths* for labelling; `NPDExperiment` registers `rvol_20` and `rvol_60` as two
of a feature list in `REGISTRATION.md:124-125`, `DECISIONS.md:108` and
`src/npd/collect/prompt.py:49-50`. **Not one line compares a realized
volatility to an implied volatility.** Realized volatility as a covariate is a
different object from realized volatility as the subtrahend in a premium.

**`straddle` — 15 lines, every one the English verb.** `ETFExperiment` ×4
("the print window straddles midnight UTC", "chosen to straddle the boundary"),
`MLCryptoEngine` ×2 ("straddles span start"), `ORBExperiment` ×4 ("Noise
straddles 1.0"), `solclear` ×1 ("straddles the threshold"). **Zero option
straddles.** The collision is with the verb *to span*, and it is total.

**`option` — 1,993 lines, all CLI and API vocabulary.** The dominant sources are
argparse/CLI `options`, HTTP request `options`, and config `options`. There is
no options *contract* anywhere in the program.

---

# Screen against the three named closures

The prompt requires reasoning, not an assertion of CLEAR. Each closure is
stated from its own repository's record, then distinguished.

## Closure 1 — MLCryptoEngine H5 (funding rate carry) and H8 (cross-sectional funding carry)

**What they measured.** H5, closed 2026-08-04 as *decayed, not disproved*: a
delta-neutral long-spot/short-perp book collecting funding, historically
**8.07 % (ETH) and 8.00 % (BTC)** net annualised on deployed capital, decayed
~85 % — Binance BTC funding annualised **30.61 % (2021) → 1.94 % (2026)** —
sampled on Hyperliquid hourly funding 2023-05-12 → 2026-08-04, **27,761 rows for
BTC** across 12 perps. H8, closed 2026-08-05 as *signal present, cancelled by
its own hedge*: funding income **+43.68 %/yr**, price return **−42.91 %**, net
**+0.11 %** against a 4 % risk-free rate, on **4,411,046 hourly funding
observations** over 231 usable perps.

**Why an implied-minus-realized volatility gap is a different quantity from a
funding rate.** Three separations, and the first is sufficient on its own.

1. **They are premia on different state variables.** A funding rate is the
   price of *the perpetual's deviation from spot* — a level, a first moment. It
   is an explicit, contractually specified periodic payment that one side pays
   the other so the perp tracks the index, and it is *observable directly as a
   number the venue publishes*. A variance risk premium is the price of *the
   second moment* — the gap between the volatility the option market charges
   and the volatility the underlying subsequently delivers. It is never
   published; it is a *difference of two estimators*, one forward-looking and
   implied out of a price by an inversion, one backward-looking and computed
   from returns. No arithmetic converts one into the other. A funding rate can
   be zero while the variance premium is 5 vol points, and the reverse.
2. **They are compensations for different risks.** Funding compensates for
   carrying inventory against a directional crowd — the record proves it, since
   H5 measured funding correlating **0.5+ with trailing price trend** (BTC pays
   5.77 bps/day in uptrends against 1.87 in downtrends), which is why H5's
   reopening condition is about *the funding level* and its qualifier is that it
   is "a bull-market income stream wearing a delta-neutral label". A variance
   premium, if it exists, compensates for bearing *gamma* — the risk of a
   realized move larger than the one priced — and its sign is set by the
   convexity demand of hedgers, not by trend-following flow.
3. **They live on different instruments and therefore different venues.**
   Funding is a perpetual-swap mechanic. There is no funding rate on an option.
   The variance premium is only measurable where options trade, which is exactly
   the reachability question this repository exists to answer, and which H5 and
   H8 never had to ask because Hyperliquid perps were reachable at 3 bps.

**Verdict: CLEAR.** H5 and H8 are first-moment carry on perpetuals; this is a
second-moment premium on options. Different quantity, different risk
compensation, different instrument. Note however that H5 and H8 supply the
*reachability precedent* — they are the reason ADR-034's claim that Hyperliquid
is the only BC-reachable venue offering a short is load-bearing here, and TASK 3
re-verifies it rather than carrying it.

## Closure 2 — NPLExperiment H5 (HIP-3 basis, 4.14 bp against an 18 bp floor)

**What it measured.** Two snapshots, **188 observations, 0 absent**, session tag
`extended`: **median absolute basis 4.14 bp**, IQR 0.71–9.15, with **9.57 %** of
observations over the 18 bp floor and **1.60 %** over the 54 bp bar.

**Why this is a different premium.** The HIP-3 basis is a *cross-instrument
price dislocation*: the gap between a HIP-3 deployed market's price and the
served reference for the same underlying, at the same instant. Its economic
content is an arbitrage relation — two claims on one underlying that should
converge, and the basis is the cost of not converging. It is measured as
`|price_A − price_B| / price` on simultaneous quotes, requires no time series
to compute a single observation, and has no horizon.

A variance risk premium is not a dislocation between two prices for one thing.
It is a wedge between a *price* and a *subsequent realization* — the option
market's forward-looking volatility charge against the volatility the
underlying actually delivers over a stated tenor. It cannot be observed at an
instant; it requires the tenor to elapse before the realized leg exists. There
is no convergence relation to arbitrage: the implied and realized legs are not
two prices for the same claim, and nothing forces them together. A trader who
sells the premium is short gamma and can lose without any mispricing having
existed.

The floors also differ in kind. NPL's 18 bp floor is a *transaction-cost floor
on an arbitrage* — the basis must exceed round-trip cost or the convergence
trade is not takeable. This repository's cost hurdle is a floor on a *risk
premium*, which does not converge and which is compensation for a variance a
seller genuinely bears. Clearing NPL's floor means an arbitrage is free money;
clearing this one means a risk is paid for above its cost of access.

**Verdict: CLEAR.** Instantaneous cross-price dislocation with a convergence
relation, versus a price-versus-realization wedge over a tenor with no
convergence relation.

## Closure 3 — MLCryptoEngine H2 (CME micro futures, AUC 0.501 on 224,425,675 events)

**What it measured.** Closed *signal-absent* 2026-08-03: **AUC 0.501** at every
horizon, **0.22 bps** gross capture against **5.33 bps** cost, best net EV
**−5.11 bps**, on **224,425,675 events** over 989 scheduled-open hours across two
validated MBT months (2026-04, 2026-05), mbp-10 depth, ordering clock `ts_recv`.
The closure note is explicit that the cost problem *was solved* — 5.33 bps
against crypto spot's 80 — and the signal vanished anyway, and that H2 reopens
only "on evidence of measurable AUC on a *different* instrument or feature
class", never on a re-run against the same contract.

**Why a volatility premium on the same venue is a different mechanism from a
microstructure edge transfer.** The overlap here is venue and underlying only.
CME is the venue in both; the underlying is bitcoin in both. Everything that
decides the outcome differs.

1. **Direction of the claim.** H2 is a *prediction* claim: that a learned
   feature map assigns above-chance probability to the sign of the next price
   move. Its endpoint is AUC, and a coin-flip AUC ends it. This repository makes
   *no prediction claim at all*. The variance premium is a claim that a
   *systematic wedge* exists between two measurable quantities — implied and
   subsequent realized volatility — which is true or false as a matter of
   historical fact regardless of whether anything is forecastable. A market can
   be perfectly efficient in H2's sense, AUC exactly 0.500 at every horizon, and
   still pay a large variance risk premium; indeed efficiency is the *standard
   explanation* for why a variance premium persists, because it is a risk
   compensation rather than a mispricing.
2. **What the counterparty is paying for.** H2's edge, had it existed, would be
   a *transfer* — one participant's information advantage extracted from
   another's uninformed order flow. It is zero-sum before costs, which is why
   adverse selection and queue position dominate its accounting. A variance risk
   premium is *not a transfer*. It is a premium paid by hedgers who want
   convexity to sellers who supply it, and the seller earns it by bearing
   realized variance. A seller of variance loses in exactly the states hedgers
   are buying protection against. That is a risk-bearing return, not an edge.
3. **Instrument class.** H2 traded the MBT *future*, a linear delta-one claim.
   This measures the *option* on the underlying, a convex claim. That the two
   are listed by the same exchange under adjacent product codes is a fact about
   the exchange, not about the mechanism.
4. **What the closure would have to say to bind.** H2's own reopening clause
   scopes it to "a *different* instrument or feature class" and to AUC. A
   variance premium is neither a feature class nor an AUC. H2 constrains
   *this repository's cost side* — its 5.33 bps MBT round-turn and its
   224,425,675-event depth are the best evidence in the program that CME micro
   bitcoin is cheap per notional — and constrains nothing on the premium side.

**Verdict: CLEAR on the mechanism, with a carried input.** H2 does not overlap
this hypothesis, but its measured MBT cost structure is a *live input* to TASK 3
and TASK 5, and per the standing rule it is re-verified rather than carried.

---

## Screen result

**CLEAR on all three named closures, and CLEAR on the corpus screen.** No
repository in this program has ever computed an implied volatility, an
implied-minus-realized gap, or a variance risk premium; `implied volatility`,
`volatility premium`, `delta hedge` and `variance risk premium` each return
**zero lines** across all thirteen non-control repositories.

**No ADJACENT is recorded.** The three closures are adjacent in *venue and
underlying* — CME and Hyperliquid, BTC and ETH — but not in *measured quantity*,
which is the axis the screen tests. The qualification carried into the register
entry is therefore not a duplication qualification but a dependency one:

> **Carried qualification.** This hypothesis inherits its venue-reachability
> priors from MLCryptoEngine ADR-034 and its CME cost priors from
> MLCryptoEngine H2. Both are dated measurements, not constants, and both are
> re-verified live in TASK 3 and TASK 5 before use. If re-verification
> disagrees with the carried figure, the measurement wins and the disagreement
> is recorded.
