# HYPOTHESES — VRPExperiment

One hypothesis. One stage. One artifact. **Closed.**

---

## H1 — The BTC/ETH variance risk premium and its reachability from British Columbia

> A variance risk premium exists in BTC and ETH at a 30-day tenor, is positive
> and material, **and** at least one venue lawfully reachable by a British
> Columbia resident permits harvesting it at an all-in round-trip cost below
> that premium by the registered margin.

| | |
|---|---|
| **Status** | **CLOSED — VENUE_BLOCKED** · 2026-08-30 · qualified, see the open route below |
| **Registered expectation** | VENUE_BLOCKED. Assistant prior 0.12 / **0.76** / 0.12 over HARVESTABLE / VENUE_BLOCKED / SIGNAL_ABSENT, recorded 2026-08-30 before any network call. |
| **Registration** | `REGISTRATION.md`, commit `7827592`, **before any network call**. Amendment 1 records an aborted first sealed-read attempt. |
| **The premium — both conjuncts of "positive and material" hold** | **BTC: mean 0.086607 annualised volatility points = 198.111 bps of notional, n = 1,955 daily observations**, Newey–West HAC bandwidth 30, SE 0.014709, **t = 5.888, one-sided p = 2.297 × 10⁻⁹**, one-sided 95% CI lower bound **0.062401 vol points = 142.740 bps**, positive on **73.86%** of observations. **ETH: mean 0.052045 vol points = 119.052 bps, n = 1,955**, SE 0.021528, **t = 2.418, one-sided p = 7.859 × 10⁻³**, CI lower **0.016618 vol points = 38.012 bps**, positive on **64.55%**. |
| **Robustness — the registered non-overlapping check agrees** | **BTC n = 66 non-overlapping windows: 0.096558 vol points = 220.872 bps, t = 4.568, p = 1.128 × 10⁻⁵, CI lower 140.188 bps. ETH n = 66: 0.058053 = 132.793 bps, t = 2.088, p = 0.0203, CI lower 26.688 bps.** Both agree with the primary in **sign and in significance**, so the registered clause "if they disagree, the disagreement is the finding" is not triggered. |
| **The deciding cost comparison, per permitted route** | **MET (ETH), the only unambiguously capital-feasible route: measured commission-only cost 122.140 bps central / 162.853 bps pessimistic per straddle round trip with its hedge — against an ETH premium CI lower bound of 38.012 bps. Required for HARVESTABLE: 2.0 × 162.853 = 325.706 bps. FAILS BY 8.57×.** And the failure does not depend on the margin at all: **the ETH premium's point estimate, 119.052 bps, is below the central commission-only cost of 122.140 bps.** The premium does not cover the commission. **MBT (BTC): commission-only cost 16.320 bps central / 21.760 bps pessimistic, against a BTC premium CI lower bound of 142.740 bps — passes the 2.0× margin by 3.28× on commission alone.** |
| **Sample** | Deribit public API, **no account, no registration, no order**. DVOL index and `BTC/ETH-PERPETUAL`, both taken hourly and filtered to **08:00 UTC** — Deribit's own option settlement instant. **47,696 hourly DVOL rows → 1,985 daily observations per asset; 47,858 hourly perpetual rows → 1,992.** Paired: **1,985 days**, of which **30 dropped for an incomplete 30-day forward window**, leaving **n = 1,955** spanning **2021-03-24 → 2026-07-30**. Implied history begins 2021-03-24, the first date Deribit serves DVOL. |
| **Limitations** | **The ETH premium is not stable and the full-sample result rests on one quarter.** Split into four equal parts: Q1 (2021-03-24→2022-07-24, n=488) **+146.27 bps, p = 0.146, not significant**; Q2 (→2023-11-24, n=488) **+291.21 bps, p = 3.14 × 10⁻⁵**; Q3 (→2025-03-26, n=488) **−18.56 bps, NEGATIVE, p = 0.597**; Q4 (→2026-07-30, n=491) **+57.66 bps, p = 0.211, not significant**. **Only one of four quarters is individually significant and one is negative.** BTC is significant in all four but **decays monotonically**: **284.53 → 250.59 → 145.13 → 112.72 bps**, a **60.4% fall** across the sample — the same shape MLCryptoEngine H5 measured in funding carry. **No tail is measured**: a short-variance position's defining risk is the move absent from a 5.4-year sample, and the premium is compensation for exactly that risk, so this measures the payment and not the liability. **No sleeve is simulated**; there is no equity curve, drawdown or Sharpe anywhere in this repository. |
| **What the cost figure is NOT** | **Three of five cost legs are `Absent(not_served)`** — the option bid-ask, the hedge bid-ask, and the exchange/regulatory fee. **Every figure above is a strict LOWER BOUND on cost**, because every absent leg is non-negative. **The bound is sufficient to decide MET and insufficient to decide MBT**, and that asymmetry is the whole shape of this closure. |
| **Working** | `docs/ARTIFACT.md`; `reports/task6/real_attempt2_result.json`; `docs/COSTS.md`; `reports/task3/venue_table.md`; `docs/ACCESS.md`. Latches: `reports/task6/task6.latch.json` (attempt 1, aborted) and `task6.latch.2.json` (the read, written 2026-08-30T06:58:05.858Z). |
| **What would reopen it** | **Not a better estimator and not more data.** The premium is measured, large and significant on BTC; nothing about the premium side is in doubt at the sample level. Exactly **two figures** would settle the one route left open: **(1)** the CME initial margin for a short MBT option — HARVESTABLE requires it to be **≤ 12.80% of the $7,812.46 notional**, i.e. **≤ $1,000 per contract**; and **(2)** the all-in MBT option and futures bid-ask plus CME exchange and regulatory fees — HARVESTABLE requires their pessimistic total to be **≤ 49.61 bps of notional**, which is the room left between the BTC premium's CI lower bound and twice the measured commission. **Both are obtainable in one session by an operator with an IBKR Canada account, and by nobody without one.** Reopening on the ETH side additionally requires the quarterly instability above to resolve, which more of the same data cannot do. |

---

## Section 0 — the verdict, fired

### The branch that fires: **VENUE_BLOCKED**

**Registered text:** *"The premium is positive and material, and no lawfully
reachable venue clears the cost hurdle at the sleeve size."*

**SIGNAL_ABSENT does not fire.** Both assets reject H₀: mean(VRP) ≤ 0 at the
registered one-sided α = 0.05 with the registered HAC bandwidth 30 — **BTC
p = 2.297 × 10⁻⁹ (n = 1,955), ETH p = 7.859 × 10⁻³ (n = 1,955)** — and the
registered non-overlapping robustness check agrees on both.

**HARVESTABLE cannot fire, and the reason is structural rather than
arithmetic.** It requires the premium's CI lower bound to exceed **2.0 × the
measured pessimistic cost** on a lawfully reachable venue. **The pessimistic
cost is `Absent(not_served)` on both permitted routes**, because the option
bid-ask, the hedge bid-ask and the CME exchange fee could not be obtained
without an account or in the face of CME's Data Terms of Use refusal. **A branch
conditioned on a measured cost cannot fire on an absent one**, and Guard 1
enforces this structurally rather than by discipline.

**VENUE_BLOCKED fires, on four routes established and one left open:**

| route | classification | why |
|---|---|---|
| **Deribit** | **PROHIBITED** | Restricted-jurisdictions policy stamped `2026-03-19T16:49:36Z`; "Canada" listed bare, with none of the narrowing qualifiers five other entries carry. |
| **CME MET options via IBKR Canada** | **COST-EXCEEDED — established** | Commission-only cost **162.853 bps pessimistic** vs premium CI lower **38.012 bps**; required 325.706 bps. **Fails by 8.57×, at a strict lower bound, so cost can only make it worse.** The point estimate (119.052 bps) does not cover the central commission (122.140 bps). |
| **CME BTC options (full, 5 BTC)** | **CAPITAL_BLOCKED** | $390,622.88 notional = **390.6×** the $1,000 sleeve. |
| **CME ETH options (full, 50 ETH)** | **CAPITAL_BLOCKED** | $122,810.25 notional = **122.8×** the sleeve. |
| **Hyperliquid** | **NO_PRODUCT** | 232 perpetuals, **zero options**; three options-endpoint probes each HTTP 422. |
| **Canadian covered-call crypto ETFs** | **NOT AN OPTION PRODUCT** | Fails registered criterion 3.1(2): the resident buys a fund unit, not an option. BTCY MER 1.28%, ETHY MER 1.29%. |
| **CIRO-registered crypto venues** | **NO_PRODUCT** | Spot only. The CIRO route to crypto options *is* IBKR Canada → CME. |
| **CME MBT options via IBKR Canada** | **⚠ OPEN — the one route not closed** | Permitted and commission-cheap (passes the margin by 3.28× on commission alone, **at any rebalance count up to the daily maximum of 29**). **Unresolved on two named figures**: initial margin ≤ 12.80% of notional, and absent cost legs ≤ 49.61 bps. |

### The verdict in one sentence

> **A large, statistically significant variance risk premium exists in BTC
> (198.111 bps of notional, n = 1,955, p = 2.3 × 10⁻⁹) and a smaller and
> distinctly unstable one in ETH (119.052 bps, n = 1,955, p = 7.9 × 10⁻³); the
> only venue a British Columbia resident can lawfully reach that is
> unambiguously capital-feasible at $1,000 charges more in commission alone than
> the ETH premium is worth; and the one route that would clear the hurdle on
> commission cannot be settled without a broker account this repository does not
> have and will not open.**

### The qualification, stated rather than buried

**This is not a clean VENUE_BLOCKED.** The registered branch says *no* lawfully
reachable venue clears the hurdle, and **MBT is not shown to fail** — it is shown
to be **unmeasurable from outside a brokerage account**. VENUE_BLOCKED is fired
because HARVESTABLE demonstrably cannot be established from anything measurable
without opening an account, and SIGNAL_ABSENT is refuted; but the honest
statement of the residual is that **one route is open on exactly two figures, and
both are named above with the thresholds they must clear.**

---

## Prior calibration

| | HARVESTABLE | VENUE_BLOCKED | SIGNAL_ABSENT | outcome |
|---|---|---|---|---|
| **Assistant, recorded pre-measurement** | 0.12 | **0.76** | 0.12 | **VENUE_BLOCKED — resolved in favour** |
| **Operator** | — | — | — | **Slot reserved empty.** Does not block anything in a single-stage census. |

**The prior was right on the branch and wrong on the mechanism, and that is the
part worth recording.** Section 9.1 reasoned that VENUE_BLOCKED would fire
because *"Deribit is the venue with the option book and is believed to prohibit
Canadian residents; CME lists MBT and MET options but a $1,000 sleeve against a
$6,505 MBT notional is unlikely to support one short-option position ... and
Hyperliquid ... lists perpetuals rather than options."*

Two of those three legs held. **The third was wrong in a way that mattered:** the
prior assumed CME crypto options might not be *permissioned* for Canadian retail
at all, and they are — Interactive Brokers **Canada** Inc., a CIRO member,
publishes a dedicated product page for them. **The route was open; it was the
notional arithmetic that closed it**, and on the opposite asset from the one the
prior worried about. The prior worried MBT would be too big for the sleeve; what
actually decided the measurable route was that **MET is too small for the
commission** — 7.48× more expensive in basis points than MBT for exactly the
reason ADR-023 recorded, that notional decides everything on CME.

**This repeats the ORBExperiment lesson in a new place.** There, assistant 0.15
and operator 0.30 both resolved correctly against a NO on H1, and *neither had
priced the spread*. Here the prior resolved correctly again and **had** priced
the cost side — Section 4 was registered as a measurement obligation carrying no
figure precisely because of that lesson — but priced it on the **wrong
instrument**. Getting the branch right for a partly wrong reason is a weaker
result than the 0.76 makes it look, and it is recorded that way.
