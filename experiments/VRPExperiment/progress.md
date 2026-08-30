# VRPExperiment — Progress Ledger

Single-stage scoped census. Append-only. Timestamps timezone-aware UTC.

---

## 2026-08-30T04:32:03Z — TASK 0 START — Prompt logged verbatim

The governing prompt is reproduced verbatim below, before any other work, per the
standing rules. This supersedes any earlier VRPExperiment Stage A prompt.

### VERBATIM PROMPT

```text
VRPExperiment, Stage A. Single-stage scoped census. Effort: high. Run autonomously. Commit at every task boundary and push to origin/main after every commit. Never force-push, never amend or rewrite a pushed commit.

Working tree is /home/kiros-li/Documents/GitHub/VRPExperiment, initialized on main with one commit. The remote does not exist yet. Create it with gh repo create kirosli00tuff/VRPExperiment --private --source=. --remote=origin and push. If gh authentication fails, record the failure loudly, continue committing locally, and list the remote as an open operator item.

This supersedes any earlier VRPExperiment Stage A prompt. This repository runs one stage, produces one artifact, and closes. It is not a ladder. No capital is deployed, no order is placed, no venue is joined.

Purpose. Measure the BTC and ETH variance risk premium from public option data, and measure whether any venue lawfully reachable by a British Columbia resident permits harvesting it at a cost below the measured premium. Produce a citable artifact and a register entry that closes the question, whichever way it lands.

Registered expectation, stated before any measurement: VENUE_BLOCKED. Deribit prohibits Canadian residents on its restricted-jurisdictions policy dated 2026-03-19. MLCryptoEngine measured MET micro ether at 101.76 bps and MBT micro bitcoin at $6,505 notional on 2026-07-15, against a sleeve of roughly $1,000. ADR-034 records that Hyperliquid at 3 bps is the cheapest BC-reachable venue and the only one offering a short, and it lists perpetuals rather than options. The artifact is the deliverable, not the answer.

Standing rules, in force throughout.

Log this prompt verbatim to progress.md before any other work.
Measured beats documented. Every carried figure is re-verified live before use, per the ADR-055 pattern. The measurement wins.
Absence is a recorded state. Refusals are loud. Never synthesize a value for an unreachable venue.
Ledgers append-only and fsynced.
Terms of service bind, and jurisdiction binds harder. Record robots.txt and published terms verbatim before any repeated fetch. Do not register at any venue, do not onboard, do not use a proxy or VPN, do not place any order. Reading a public endpoint requiring no account is permitted and is distinct from trading. Where a venue prohibits Canadian residents, that is a measured finding and is never worked around.
Every figure travels with its n in the same sentence.
Spend nothing.
Timestamps timezone-aware in UTC. Option expiries carry their exchange settlement time.
Outcome blindness applies to the premium: the measurement machinery is built against synthetic fixtures with known answers and pointed at real data exactly once, behind a latch, at TASK 6.

TASK 0. Preconditions, remote, and the duplication screen.

Confirm tree and branch. Create and push the remote, or record the failure.

Run the duplication screen across every repo under /home/kiros-li/Documents/GitHub for: variance risk premium, VRP, implied volatility, realized volatility, DVOL, option, straddle, delta hedge, volatility premium. Record output with per-repo hit counts in docs/DUPLICATION.md.

Screen explicitly against three closures and write the reasoning out rather than asserting CLEAR. MLCryptoEngine H5 funding rate carry and H8 cross-sectional funding carry are premium-harvesting on crypto derivatives; state why an implied-minus-realized volatility gap is a different quantity from a funding rate. NPLExperiment H5 measured a HIP-3 basis at 4.14 bps against an 18 bps floor; state why this is a different premium. MLCryptoEngine H2 tested CME micro futures and closed signal-absent at AUC 0.501 on 224,425,675 events; state why a volatility premium on the same venue is a different mechanism from a microstructure edge transfer. If any screen returns ADJACENT, record ADJACENT and carry the qualification into the register entry.

TASK 1. Scaffold and guards.

uv project, package vrp, src layout, Python 3.13+, ruff, mypy strict, pytest, pre-commit, Makefile with install, lint, fmt, typecheck, test, all, guards. Port by shape from ORBExperiment: recorded absence refusing float and int and indexing; append-only fsynced ledger; the call-state enum; a blindness pin refusing any read of an implied or realized volatility value, option price or premium outside a sealed writer; a timezone guard refusing naive datetimes. make all green on an empty tree.

TASK 2. REGISTRATION.md, committed before any network call.

Section 0, the outcome map, three branches judged on reachability and cost and never on returns.

HARVESTABLE: the measured premium is positive at the registered significance, and its magnitude exceeds the measured all-in round-trip cost on at least one lawfully reachable venue by the registered margin. A successor sleeve becomes worth registering, in its own repo, on its own registration. This repo still closes.

VENUE_BLOCKED: the premium is positive and material, and no lawfully reachable venue clears the cost hurdle at the sleeve size. A documented answer and a citable artifact.

SIGNAL_ABSENT: the premium is not distinguishable from zero, or is negative.

Sections 1 through 8, concise. The hypothesis as a joint claim about magnitude and reachability. The measured quantity, with the tenor, the implied-volatility estimator, the realized-volatility estimator named, the sampling frequency, and the sign convention stated explicitly. The venue set and reachability criterion, populated by TASK 3 and not before. The cost model, populated by TASK 5 and not before, with no carried figure registered. The margin by which the premium must exceed cost for HARVESTABLE, justified before any number exists. Inference: a single one-sided test at alpha 0.05 on the premium, with the Berger 1982 note recorded that no multiplicity correction applies to a single endpoint. Power, with effect sizes halved per McLean and Pontiff, and a recorded statement that a strategy-Sharpe endpoint of 1.32 annualized would need roughly 119 weekly observations to reach t equals 2 and roughly 478 at the halved 0.66, which is why the endpoint is the premium and not a strategy return. Epistemic boundary: a positive establishes that a premium existed on this data at this tenor by this estimator and exceeded a cost measured at a point in time on a specific venue, and is never evidence that a sleeve would have been profitable, because no sleeve is simulated here.

Section 9, priors. Assistant prior recorded. Operator slot reserved empty, with a note that it does not block anything in a single-stage census and exists for the calibration ledger. Record the ORBExperiment calibration outcome as context: assistant 0.15 and operator 0.30 both resolved against a NO on H1, and neither had priced the spread.

TASK 3. Venue reachability. The first deciding measurement.

For each candidate venue record the published restricted-jurisdictions policy verbatim with its date and URL, and classify Canada and British Columbia as permitted, prohibited or unclear.

Verify the Deribit policy dated 2026-03-19 is still current and record the retrieval date. Then check at minimum: CME options on Micro Bitcoin and Micro Ether futures through Interactive Brokers Canada, including whether the product is permissioned for Canadian retail clients rather than merely listed on the US site; CME Bitcoin and Ether options at full size; any Canadian-listed covered-call or volatility crypto ETF; any CIRO-registered Canadian venue offering crypto options; and whether Hyperliquid or any BC-reachable perpetual venue has listed an options product since 2026-07.

For each permitted venue record with its n: contract size, minimum order increment, notional at current spot, initial and maintenance margin for a short option position, and the number of positions a $1,000 sleeve supports. A venue supporting fewer than one position is capital-blocked, which is distinct from prohibited, and both are distinct from reachable.

While here, re-verify and record current CME initial and maintenance margin for MES, MNQ, MGC and MBT through IBKR Canada. These are not needed for this hypothesis. They are needed for the program-level venue table and this is the cheapest opportunity to measure them.

TASK 4. Public data access for the premium.

Measure what is served without an account. Deribit publishes a public API and a DVOL index; reading it requires no registration and is permitted under rule 5 even though trading there is not. Probe and record status codes, rate ceilings measured per endpoint by escalation rather than read from documentation, history depth bisected rather than assumed, and refusal payloads verbatim.

Probe alternatives and record each: CryptoDataDownload, Laevitas, Amberdata, Tardis, and any exchange publishing an implied volatility index. For each record whether option-level implied volatility is served or only an index, how far back, at what granularity, and whether values are ever revised after publication. The revision question is mandatory. MLCryptoEngine H11 died on a source that regenerated whole files and revised past rows, and a revised implied-volatility series would silently rewrite this measurement.

TASK 5. Cost measurement on reachable instruments. The second deciding measurement.

Only for venues classified permitted in TASK 3. Measure, never carry: quoted bid-ask on the specific option series that would be traded, sampled across at least 20 distinct observation windows, reported as median, 90th percentile and full distribution with its n; exchange and broker commission verified against the live schedule; the cost of the delta hedge on the reachable futures contract measured the same way; and the number of rebalances a registered hedging rule would require, with the cost of each.

Report all-in round-trip cost as a fraction of notional and as a fraction of premium collected, at both a central and a pessimistic end, with the statistic assigned to each end before anything downstream is computed. This is the ORB lesson: a band carried from a different instrument understated five of six legs by up to 13 times.

If no venue is permitted, record Absent(venue_blocked) with the TASK 3 finding and synthesize nothing.

TASK 6. The premium measurement, single sealed read.

Build the extraction and estimation against synthetic fixtures first, including a planted-premium fixture the canary must fire on, a zero-premium fixture and a negative-premium fixture. Then open the latch once, run against real public data, and record the result with its n. One read only.

Report the premium at the registered tenor for BTC and ETH, its confidence interval, its stability across the sample window, and its magnitude in the same units as the TASK 5 cost so the two are directly comparable.

TASK 7. Fire Section 0.

Record the verdict with every input figure and its n beside it, in HYPOTHESES.md and progress.md. Write the register entry in the house shape with the closure kind, adding venue-blocked as a kind if it is the one that fires.

TASK 8. The artifact and close-out.

Write docs/ARTIFACT.md as the citable deliverable: the measured premium with its n, the venue reachability table with permitted, prohibited, capital-blocked and unclear classifications, the measured cost per permitted venue or Absent with its reason, and the conclusion in plain words. Write it so a reader outside this program can use it without reading anything else.

Write a one-page README with a what-is-measured table carrying every figure and its n. DECISIONS.md with numbered ADRs. docs/HANDOVER.md.

Add one further file, docs/VENUE_TABLE_UPDATE.md, recording two corrections for the program-level venue cost table in MLCryptoEngine: the ORBExperiment measurement of US single-name equity intraday at a median entry half-spread of 0.0766 USD per share, n equals 550, which is roughly 153 bps round trip on a typical share price and makes it the most expensive venue the program has measured; and the re-verified CME margins from TASK 3. Do not edit the MLCryptoEngine repository. Write the update here for the operator to carry across.

make all green. progress.md entries per task with ETA against actual. Final commit and push.

Print an end-state summary: the Section 0 verdict with its inputs, the venue table, the measured cost or its Absent reason, the measured premium with its n, the public data sources with measured depth and revision behaviour, the re-verified CME margins, the remote status, and every open operator item.
```

### END VERBATIM PROMPT

---

## 2026-08-30T04:38Z — TASK 0 COMPLETE — preconditions, remote, duplication screen

**ETA 20 min · actual ~6 min.**

| item | result |
|---|---|
| Working tree | `/home/kiros-li/Documents/GitHub/VRPExperiment`, clean, branch `main` |
| Commit at start | `eda2d65` "Repo init: VRPExperiment scaffold placeholder", **1 commit** |
| Toolchain | uv 0.12.0, python3 3.14.4, gh authenticated as `kirosli00tuff` |
| Remote | **CREATED AND PUSHED.** `https://github.com/kirosli00tuff/VRPExperiment` (private). `gh repo create` exit 0. `git push -u origin main` exit 0; local HEAD `31c9345` equals `origin/main`. **No gh authentication failure. No open operator item on the remote.** |
| Duplication screen | 14 repos × 9 terms. Recorded in `docs/DUPLICATION.md`. |

**Duplication screen result: CLEAR, no ADJACENT.**

- `variance risk premium`, `implied volatility`, `volatility premium`,
  `delta hedge`: **0 lines** in all 13 non-control repositories.
- `VRP`: raw substring counts up to 4,154 (solattn) are **entirely artifacts** —
  **0** word-boundary hits anywhere outside this repo; matches sit inside
  Bluesky DIDs and base58 Solana addresses.
- `DVOL`: **0** word-boundary hits in the entire tree outside this repo.
- `realized volatility`: 10 lines, all of it used as an **input feature or
  regime switch** (AiTrader ADX regime detector; MLCryptoEngine triple-barrier
  width scaling; NPDExperiment `rvol_20`/`rvol_60` feature names). **Not one
  line compares realized to implied.**
- `straddle`: 15 lines, **every one the English verb** ("straddles midnight
  UTC", "Noise straddles 1.0"). Zero option straddles.
- `option`: 1,993 lines, all CLI/API/config vocabulary. Zero option contracts.

**Three named closures, reasoned rather than asserted — all CLEAR.**

1. **MLCryptoEngine H5 / H8 (funding carry).** A funding rate prices the
   perpetual's deviation from spot — a **first moment**, contractually specified
   and **published directly by the venue**. A variance premium is a **difference
   of two estimators** on the **second moment**, never published, one implied by
   inversion from a price and one computed from subsequent returns. Funding
   compensates carrying inventory against a directional crowd (H5 measured it
   correlating **0.5+ with trailing trend**: BTC pays 5.77 bps/day in uptrends
   vs 1.87 in downtrends); a variance premium compensates bearing **gamma**.
   There is no funding rate on an option. Different quantity, different risk,
   different instrument.
2. **NPLExperiment H5 (HIP-3 basis 4.14 bp, n = 188, 18 bp floor).** A basis is
   an **instantaneous cross-price dislocation** between two claims on one
   underlying, with a **convergence relation** to arbitrage, computable from a
   single simultaneous quote pair. A variance premium is a wedge between a
   **price and a subsequent realization** over a stated tenor, with **no
   convergence relation** — nothing forces implied and realized together, and a
   seller is short gamma and can lose with no mispricing having existed. NPL's
   18 bp floor is a cost floor on an arbitrage; this repository's hurdle is a
   floor on a **risk premium**.
3. **MLCryptoEngine H2 (CME micro futures, AUC 0.501, n = 224,425,675 events).**
   H2 is a **prediction** claim with an AUC endpoint; this makes **no prediction
   claim**. A market can be exactly AUC 0.500 and still pay a large variance
   premium — efficiency is the standard *explanation* for the premium, not a
   refutation. H2's edge would have been a **zero-sum transfer** from uninformed
   flow; a variance premium is **risk-bearing compensation** paid by hedgers for
   convexity. H2 traded the **linear** MBT future; this measures the **convex**
   option. H2's own reopening clause scopes it to a different instrument or
   feature class and to AUC; a variance premium is neither.

**Carried qualification into the register entry** (a dependency, not a
duplication): venue-reachability priors come from MLCryptoEngine ADR-034 and CME
cost priors from MLCryptoEngine H2. Both are dated measurements. Both are
re-verified live in TASK 3 and TASK 5 before use; if re-verification disagrees,
the measurement wins and the disagreement is recorded.

**Re-verification already performed at TASK 0** (measured beats documented):

| carried figure | prompt states | measured live from source | source |
|---|---|---|---|
| ORB entry half spread | 0.0766 USD/share, n = 550 | **0.076572** median, **0.333662** p90, **n = 550 minutes served, 0 refused** | `ORBExperiment/README.md:300`, `docs/HANDOVER.md:59`, `reports/stage_a3rescue/task2_slippage_band.json:74` (0.07657173002730797) |
| MET micro ether cost | 101.76 bps | **101.762 bps**, notional **$191**, round turn $1.94 | `MLCryptoEngine/report.md:1165` |
| MBT micro bitcoin | $6,505 notional | **$6,505** notional, round turn **$4.04**, **6.211 bps** | `MLCryptoEngine/report.md:1164` |
| ADR-034 Hyperliquid | 3 bps, cheapest BC-reachable, only short | Confirmed verbatim: "the only reachable venue offering a short is Hyperliquid perps", Hyperliquid perps base tier **1.5 bps/side = 3.0 bps round trip**, verified 2026-08-01 | `MLCryptoEngine/DECISIONS.md:1480`, `HYPOTHESES.md:305` |

All four carried figures agree with source to rounding. **No disagreement to
record at TASK 0.** The venue figures are dated 2026-07-15 / 2026-08-01 and are
re-measured live in TASK 3 regardless.

---

## 2026-08-30T04:52Z — TASK 1 COMPLETE — scaffold and guards

**ETA 45 min · actual ~14 min.**

`uv` project, package `vrp`, src layout, **Python 3.13.14** (pinned by
`uv venv --python 3.13`; the machine's system interpreter is 3.14.4 and is not
used). ruff 0.16.5, mypy 2.3.1 strict, pytest 9.1.1, pre-commit 4.6.2.
Makefile targets `install lint fmt typecheck test all guards clean`.

**`make all` is green on an empty tree: ruff format + check clean, mypy strict
`Success: no issues found in 11 source files`, `28 passed`.**

Five guards ported by shape from ORBExperiment, each named to the standing rule
it pins.

| guard | module | what it refuses |
|---|---|---|
| 1 · recorded absence | `src/vrp/absence.py` | `float()`, `int()`, `__index__`, every arithmetic operator both ways, ordering, `bool()`, `len()`, iteration, indexing. **10 absence reasons**, including the four the prompt distinguishes: `venue_blocked`, `venue_capital_blocked`, `venue_unclear`, `latch_unspent`. |
| 2 · timezone | `src/vrp/tzguard.py` | naive datetimes at every boundary, **and non-UTC aware datetimes, which it refuses rather than converts** — a silent conversion hides which side was wrong. `ExchangeExpiry` cannot be constructed without a settlement instant, an exchange, and the published settlement rule verbatim. |
| 3 · append-only ledger | `src/vrp/ledger.py` | non-durable writes (`O_APPEND` + `fsync` per line, short-write detected), and silent repair — a damaged line comes back as `TruncatedLedgerLine` and is excluded from `row_count()` rather than dropped. Rows are credential-redacted before serialisation. |
| 4 · call-state enum | `src/vrp/callstate.py` | merging **operational health** (5 states) with **venue classification** (5 states). `combined_total()` raises structurally. **A 403 is `access_refused`, an operational fact; a jurisdiction finding comes only from published policy text.** |
| 5 · blindness pin | `src/vrp/fields.py`, `src/vrp/seal.py`, AST walk in `tests/test_guards.py` | any module outside `{vrp/fields.py, vrp/seal.py, vrp/sealed_read.py}` naming any of **38 blind fields** — implied vol (`mark_iv`, `dvol`, …), realized vol, option price, premium — as a string literal, attribute, name, or parameter. |

Plus the **TASK 6 latch** (`src/vrp/latch.py`): written before the read, records
the SHA-256 of every participating module, refuses a second write with
`LatchAlreadySpentError`, and exposes `verify_modules()` so post-read module
drift is visible rather than silent.

**Two design decisions recorded rather than assumed.**

1. **Cost and reachability fields are deliberately READABLE, not blind.**
   `bid`, `ask`, `initial_margin`, `commission`, `policy_text` and 25 others sit
   in `READABLE_FIELDS`. Blinding them would blind the wrong half of the
   experiment: TASK 3 and TASK 5 are the two *deciding* measurements and must be
   readable to decide anything. Only the premium and its two estimator legs are
   blind. The two registries are asserted disjoint at import.
2. **The `open()` guard is narrowed to text handles, and the narrowing is
   stated.** `os.open` / `os.fdopen` are exempt because they return a raw file
   descriptor and are the only way Guard 3 gets `O_APPEND` plus `fsync`. Builtin
   `open` and `Path.open` stay forbidden — those are the calls that would let a
   module read and parse a served payload. **The guard fired on its first run
   against `vrp/ledger.py:74`**, which is the evidence it binds on real modules
   and not only on fixtures.

**Both AST guards carry a canary that demonstrably fires.**
`test_the_blindness_pin_actually_fires_on_a_planted_violation` plants
`payload["mark_iv"]` and asserts the walk returns it;
`test_the_open_guard_fires_on_a_planted_path_open` plants a builtin `open`, a
`Path.open` and an `os.open` and asserts exactly the first two are caught. A pin
that cannot fire proves nothing.

Toolchain provenance recorded to `reports/env_report.json` by `tools/env_report.py`.

---

## 2026-08-30T05:04Z — TASK 2 COMPLETE — REGISTRATION.md, before any network call

**ETA 40 min · actual ~12 min.** `REGISTRATION.md`, 533 lines. **No network call
has been made by this repository at any point up to this commit.** The last
commit before registration is `8bcc5bf`.

**Section 0** registers three branches judged on reachability and cost, never on
returns, with an explicit precedence rule: if the premium fails Section 6,
SIGNAL_ABSENT fires **regardless of the venue finding**. VENUE_BLOCKED
sub-classifies into *prohibited*, *capital-blocked*, *no-product* and
*cost-exceeded*, because they are four different findings and only the first is a
jurisdiction fact.

**Section 2** fixes the measured quantity before any data:

| element | registered value |
|---|---|
| tenor | **30 calendar days**, one tenor, both assets, no sweep |
| implied estimator | **exchange-published 30-day model-free IV index (Deribit DVOL)**, annualised vol points; a fallback to ATM-forward option-level mark IV, interpolated **linearly in total variance**, is registered now and recorded as used-or-not, never blended |
| realized estimator | **close-to-close, `ddof=1`, annualised by √365**, over the 30 days **following** the implied observation. Not Parkinson, not Garman-Klass, not Yang-Zhang, not intraday realized variance |
| sampling | daily, at a **fixed UTC instant** set at first read and never moved |
| sign | **`VRP_t = IV_t − RV_{t→t+30}`. Positive means the option market charged more than the underlying delivered — a seller of variance was paid.** |
| depth | registered minimum **730 daily observations per asset**; **60** is the floor below which `Absent(insufficient_sample)` is recorded and no number printed |

The **forward-looking** direction of the realized leg is pinned explicitly: RV
over the 30 days *preceding* `t` is a different quantity and is not the
subtrahend. This is the most common way the measurement is got wrong.

**Section 2.6 registers the one conversion that makes premium and cost
comparable, before any number exists**, with its arithmetic verified:
`edge_bps = √(2/π)·√T·(IV−RV)·10,000`; at `T = 30/365 = 0.082192`,
`√T = 0.286691`, `√(2/π) = 0.797885`, so **one volatility point of premium is
22.875 bps of notional**. Its three limitations — continuous-hedging assumption,
ATM-straddle-only, first-order — are registered as limitations rather than
discovered later.

**Section 3 registers the reachability criterion and no venue.** Permitted
requires published text recorded verbatim with URL and date, an option product
listed, and **no proxy, no VPN, no misrepresentation of residence**. **UNCLEAR is
never read as permission and cannot support HARVESTABLE.** The two carried claims
— ADR-034's Hyperliquid-only-short finding and Deribit's 2026-03-19 policy — are
registered **as claims to be tested, not as findings**.

**Section 4 registers the cost model and carries no figure from anywhere.**
Central end takes the **median** half-spread on both legs and the registered
rule's **median** rebalance count; pessimistic takes the **90th percentile** of
each. **The assignment is registered here, before anything downstream is
computed.** The hedging rule is registered as **±0.10 delta, evaluated daily at
the fixed UTC instant**, with ±0.05 and ±0.20 swept as sensitivity — per ADR-034
a rebalance band is a trade-off and is swept and reported, never chosen. If no
venue is permitted: **`Absent(venue_blocked)`, synthesize nothing** — enforced
structurally by Guard 1.

**Section 5 registers the margin as 2.0× against the pessimistic end**, justified
before any number exists by three named, unmeasured error sources all pushing the
same way: quoted spread is not effected spread (H3 measured adverse selection
**positive on all 28 instruments, +0.06 to +0.68 bps**); the rebalance count is a
rule not an observed path; and the Section 2.6 conversion assumes continuous
hedging, making the premium an **upper bound**. 2.0 is deliberately modest against
ORB's measured **11.27×** — because ORB's was a *carry* error and this repository
carries nothing.

**Section 6** registers **one one-sided t-test at α = 0.05**, H₀ `mean(VRP) ≤ 0`,
with **Newey–West HAC at bandwidth 30** registered *before any data* because the
overlapping 30-day forward windows induce serial correlation by construction —
the same defect ORB's audit A3 found after the fact, where independence made
intervals **2–17× too narrow**. Non-overlapping windows are registered as
robustness, and **if the two disagree in sign or significance the disagreement is
the finding and neither is suppressed**. The **Berger 1982** note is recorded: the
hypothesis is a **conjunction**, an intersection-union test gets the **full
nominal level per component**, and no multiplicity correction applies.

**Section 7** halves every effect size per **McLean and Pontiff (2016)** and
records the arithmetic that decides the endpoint: a strategy-Sharpe endpoint of
**1.32 annualised needs ≈ 119 weekly observations** to reach t = 2
(`(2/1.32)² = 2.2957 yr × 52 = 119.4`), and **≈ 478 at the halved 0.66**
(`(2/0.66)² = 9.1827 yr × 52 = 477.5`, more than nine years). **That is why the
endpoint is the premium and not a strategy return.** Section 7.3 registers the
design's own weakness before seeing data: at 730 daily observations with
bandwidth 30 the effective independent sample is ≈ 24, detecting `d ≈ 0.508`, and
**the halved-effect design is powered only if the premium is large**.

**Section 8** states the epistemic boundary, including the one this repository
most needs a reader to see: **a short-variance position's defining risk is the
move that does not appear in a two-year sample, and the premium is compensation
for exactly that risk — so measuring the premium without the tail measures the
payment and not the liability.**

**Section 9** records the assistant prior **HARVESTABLE 0.12 / VENUE_BLOCKED 0.76
/ SIGNAL_ABSENT 0.12** with its reasoning, reserves the operator slot **empty**
with a note that it blocks nothing in a single-stage census, and records the
ORBExperiment calibration outcome: **assistant 0.15 and operator 0.30 both
resolved against a NO on H1, and neither had priced the spread** — the closure
came from a measured **0.076572 USD/share** entry half spread (**n = 550 minutes
served, 0 refused**) against a carried QQQ band **11.27×** too small.

---

## 2026-08-30T05:40Z — TASK 3 COMPLETE — venue reachability, the first deciding measurement

**ETA 60 min · actual ~36 min.** Full record in `reports/task3/venue_table.md`,
`reports/task3/deribit_restricted_jurisdictions_verbatim.md`,
`reports/task3/robots_and_terms.md`.

**No venue was joined, no account opened, no order placed, no proxy or VPN used.**
robots.txt recorded verbatim with SHA-256 for all 8 domains before any repeated
fetch.

### The headline: the registered expectation is contradicted

**Section 9.1 priced VENUE_BLOCKED at 0.76 largely on the belief that no
BC-reachable venue would offer an option product. At least one does.**

**Interactive Brokers Canada Inc. — a CIRO member with a registered office at
1800 McGill College Avenue, Suite 2106, Montreal, Quebec — publishes a dedicated
product page on its own `.ca` domain offering CME Group Options on Micro Bitcoin
and Micro Ether Futures**, with the verbatim call to action *"If you already have
Options trading permission, you can begin trading CME Group Options on Micro
Bitcoin and Micro Ether Futures."* This answers the prompt's precise question —
permissioned for Canadian retail clients, **not** merely listed on the US site.
HTTP 200, 123,443 bytes, retrieved 2026-08-30T05:15Z.

### Live reference spot, two independent public endpoints, no account

**BTC $78,124.575** (Coinbase) vs **$78,115.50** (Kraken), disagreeing by
**1.16 bps**, `n = 2` sources. **ETH $2,456.205** vs **$2,455.41**, **3.24 bps**,
`n = 2`. Coinbase used downstream, registered before use.

### The venue table

| venue / route | product | classification |
|---|---|---|
| **Deribit** | BTC/ETH options | **PROHIBITED** |
| **CME MET options via IBKR Canada** | option on 0.10 ETH | **PERMITTED, capital-feasible** |
| **CME MBT options via IBKR Canada** | option on 0.10 BTC | **PERMITTED, capital status UNRESOLVED** |
| **CME BTC options (full, 5 BTC)** | $390,622.88 notional | **CAPITAL_BLOCKED, 390.6× the sleeve** |
| **CME ETH options (full, 50 ETH)** | $122,810.25 notional | **CAPITAL_BLOCKED, 122.8× the sleeve** |
| **Hyperliquid** | 232 perps, **0 options** | **NO_PRODUCT** |
| **Canadian covered-call crypto ETFs** | TSX fund units | **NOT AN OPTION PRODUCT** (fails registered criterion 3.1(2)) |
| **CIRO-registered crypto venues** (Webull Canada, approved 2026-06-30) | **spot only** | **NO_PRODUCT** |

**Deribit: PROHIBITED, verified and dated.** The page's own machine-readable
stamp is `2026-03-19T16:49:36Z` — **the registered 2026-03-19 date is confirmed
exactly**, with the time of day added, and the policy is still current at
retrieval. **"Canada" is listed bare.** Five other entries carry qualifiers that
narrow the prohibition (Belarus and Russia have EEA/Switzerland nationality
exemptions; Panama and the UAE restrict only *Retail Investors* and only to
*spot*; the UK only *Retail Clients*; Ukraine only three named regions). **Canada
carries no qualifier of any kind** — an unconditional whole-country prohibition
over location, incorporation, establishment and residence. Not worked around.

**Hyperliquid: NO_PRODUCT, measured not assumed.** `POST /info {"type":"meta"}`
→ HTTP 200, 17,495 bytes, **universe n = 232**, and **zero** instrument names
match any call/put/strike pattern. Three options-endpoint probes (`optionMeta`,
`optionsMeta`, `metaOptions`) each returned **HTTP 422 "Failed to deserialize the
JSON body into the target type"**. **No options product has listed since
2026-07.** ADR-034's description is confirmed; its *implication* — that no
BC-reachable venue offers a short in this asset class — **is now false for
options.**

### The $1,000 sleeve, and the capital determination

| product | notional | sleeve ÷ notional | supported iff IM ≤ | determination |
|---|---|---|---|---|
| **MET option** | **$245.62** | **4.07×** | **407.1%** of notional | **NOT capital-blocked** — no margin regime charges four times notional; **the sleeve constraint is not binding at any IM below $1,000/contract** |
| **MBT option** | **$7,812.46** | **0.128×** | **12.80%** of notional | **UNRESOLVED** — turns entirely on a figure that is `Absent(not_served)` |
| BTC full | $390,622.88 | 0.0026× | 0.26% | **CAPITAL_BLOCKED** |
| ETH full | $122,810.25 | 0.0081× | 0.81% | **CAPITAL_BLOCKED** |

### Re-verification: two carried figures disagreed, and the measurement won

| carried | source | re-measured | drift |
|---|---|---|---|
| MBT notional **$6,505** | MLCryptoEngine 2026-07-15 | **$7,812.46** | **+20.1%** |
| MET notional **$191** | MLCryptoEngine 2026-07-15 | **$245.62** | **+28.6%** |

Both carried figures are 46 days stale and **understate notional**. Every sleeve
calculation above uses the re-measured values. This is the ADR-055 pattern doing
its job on the first opportunity it had.

### Recorded absences — CME margins, and why

**`Absent(not_served)` for MES, MNQ, MGC, MBT initial and maintenance margin, and
for short-option margin on MBT and MET.** Three reasons, all recorded:

1. **CME Group refused, citing its own Data Terms of Use, and the refusal is
   recorded verbatim** (HTTP 403, 602 bytes, SHA-256 `eecde3fa…a4f7e`): *"This IP
   address is blocked due to suspected web scraping activity … Use of scripts,
   software, spiders, robots, avatars, agents, tools or other scraping mechanisms
   is strictly prohibited by CME Group's website Data Terms of Use."* **All
   fetching of cmegroup.com stopped on receipt. No user-agent rotation, no proxy,
   no retry loop, no third-party mirror substituted.** Terms bind.
2. **IBKR Canada does not publish per-contract margin without a login.** Both
   margin pages (HTTP 200, 275,624 bytes) serve a wizard and a table-view chooser,
   not values. The legacy `index.php?f=marginnew&p=fut` endpoint (17,299 bytes)
   contains no MBT/MES/MNQ/MGC margin row.
3. **MLCryptoEngine holds no CME margin figure to carry** — grep for "initial
   margin", "maintenance margin", "SPAN margin" across its markdown and
   `config/venues.yaml` returns **zero** rows. These would have been new
   measurements, not re-verifications.

**Nothing is synthesized.** Open operator item: an operator with an IBKR Canada
login can read all six figures in Client Portal and settle the MBT question
against the measured threshold **IM ≤ 12.80% of $7,812.46 = $1,000.00**.

### One further measured cost datum, recorded because it binds on TASK 5

Verbatim from IBKR: *"Interactive Brokers calculates and charges a daily
**'Exposure Fee'** … **Closing out short option positions may also reduce or
eliminate the Exposure Fee. Testing has indicated that short positions in
low-priced options generate the largest exposures relative to the amount of
capital.**"* A short option book at this broker can attract a **daily** charge
that is neither commission nor spread, and the broker names short options as the
position type that generates it. Magnitude is account-specific and
`Absent(not_served)`. **TASK 5's cost is therefore incomplete in a known
direction and must never be read as complete.**

### Canadian covered-call crypto ETFs — reachable, but not an option product

Purpose **BTCY** (MER **1.28%**), Purpose **ETHY** (management fee **1.10%**, MER
**1.29%**, MER capped **1.48%**), Global X **BCCL**. All TSX-listed and
BC-reachable. **They fail registered criterion 3.1(2): the resident buys a fund
unit, not an option.** Recorded as a distinct classification with its measured
fee, because it is the honest comparison a reader will want — but it cannot
support HARVESTABLE under the criterion registered before measurement.

---

## 2026-08-30T06:12Z — TASK 4 COMPLETE — public data access

**ETA 50 min · actual ~32 min.** Full record in `docs/ACCESS.md`,
`reports/task4/deribit_probe.json`, `reports/task4/rate_and_revision_baseline.json`.

**No registration, no onboarding, no order.** Deribit's *private* endpoint was
probed once to confirm the public/private split is real; it refused correctly
with `{"code":13009,"data":{"reason":"invalid_token"},"message":"unauthorized"}`,
HTTP 400. No credential was sent and none is held. **Blindness held: the probe
tools read status codes, byte counts, row counts, index-0 timestamps and SHA-256
digests, and no volatility value.**

### Deribit, the registered primary — every requirement met

- **All 9 valid public endpoints HTTP 200 with no account**, `n = 11` probes.
  Live: **1,026 BTC option instruments, 876 ETH option instruments.**
- **History depth bisected, not assumed: 1,992 days back for both assets**
  (~2021-03-17), `n = 22` probes per asset. **2.73× the registered 730-day
  minimum.** Corroborated independently by CryptoDataDownload's oldest DVOL row
  at 2021-03-24.
- **Supported resolutions measured by trying them: 60, 3600, 43200 s.** 300, 900
  and 21600 refuse with, verbatim, `{"code":-32602,"data":{"reason":"unsupported
  resolution","param":"resolution"},"message":"Invalid params"}`.
- **The 1,000-row cap is a page size, not a depth limit.** A 30-day request at
  `resolution=60` returned exactly 1,000 rows covering **0.69 days** plus a
  `continuation` token; following it once returned 1,000 more rows, **contiguous**
  with page 1. Recorded because mistaking a truncated first page for the end of
  the series would silently shorten every window in the analysis.

### Two self-corrections, recorded rather than silently applied

**1. The revision test's first result was a false positive.** Fetching a fixed
closed 7-day window twice, 5 s apart, produced different whole-response digests.
Cause: the JSON-RPC envelope carries `usIn`/`usOut`/`usDiff` server-timing fields
that change every call. **With those excluded the 169 data rows were
byte-identical** — data-only SHA-256
`fa63b50d8879cc74db37488c4082120725182ff6a855ec183947a39d5e2be8ef` on both
fetches. A whole-response digest is the wrong instrument for this question and
would have reported a revision that did not happen. **Six data-only baselines
recorded** (BTC and ETH at 45, 365 and 900 days back, 169 rows each) for
re-checking at TASK 8 across a real interval.

**2. The rate ceiling was not found by a sequential burst.** 60 sequential
requests achieved **3.64 req/s** and drew no refusal — that measured round-trip
latency. Re-run as a **concurrent escalation** doubling from 2 to 64:
**no refusal on either endpoint, `n = 126` requests each**, peaking at
**126.76 req/s** (`get_index_price`) and **120.45 req/s**
(`get_volatility_index_data`). The honest statement is **"no rate refusal at or
below 126.76 req/s" — an upper bound that was not reached, not a measured
ceiling.** The escalation stopped at the registered 64-concurrent ceiling rather
than hammering a public endpoint until it broke.

### A refusal that does not look like one

`get_volatility_index_data?currency=DOGE&resolution=3600` returns **HTTP 200**
with `{"result":{"data":[],"continuation":null}}`. **An unsupported currency
returns a successful empty response, not an error**, and a caller reading "empty"
as "no volatility" would synthesize a value for an instrument that does not
exist. Guard 4's separation of `NO_DATA` from every composition fact is exactly
what stops this. Deribit's own status code is inconsistent here — HTTP 400 when
`resolution` is omitted, HTTP 200 with an empty array when it is supplied — so
the status code alone is not a reliable discriminator and is not treated as one.

### The eight alternatives, and the structural finding

| source | account? | option-level IV or index? | history | revision risk |
|---|---|---|---|---|
| **Deribit** | **no** | **both** | **1,992 days** | baselines recorded |
| CryptoDataDownload | no | index only, **derived from Deribit** | 1,986 daily rows, 2021-03-24→2026-08-30 | **HIGH** |
| **Laevitas** | **YES — refused** | — | — | — |
| **Amberdata** | **YES — refused** | — | — | — |
| Tardis | history **paid** | lists a `deribit_volatility_index` channel | not measured | not pursued — spend nothing |
| OKX | no | **option-level** + greeks | **snapshot only** | n/a |
| Bybit | no | **option-level** | **snapshot only** | n/a |
| Binance eoptions | no | **option-level** + greeks | **snapshot only** | n/a |

Refusals verbatim: Laevitas `{"status":400,"message":"Api Key is Required"}`;
Amberdata `{"message":"Forbidden"}` HTTP 403. **`Absent(not_served)` for both;
nothing estimated or substituted.** Volmex: two candidate paths both 404 — recorded
as **not located**, deliberately *not* as *does not exist*.

**The structural finding that decides the source choice: only two of the eight
sources serve history at all, and one of them is a mirror of the other.** OKX,
Bybit and Binance each serve *richer* data than Deribit's index — full
option-level bid/ask IV with greeks, publicly, no account — and **all three serve
a live snapshot only**. They cannot supply a 730-day series unless this
repository had been recording daily for two years, which it has not. **This is
why Section 2.2's fallback was registered *within* Deribit rather than across
venues, and that registration was made before any of this was measured.**

**CryptoDataDownload carries the H11 risk by construction.** It is a single CSV
containing today's row, so it is rebuilt on every publication — the exact shape
that killed MLCryptoEngine H11, a source that regenerates whole files and can
revise past rows with no signal. It is also not independent: the filename
`DeriBit_volatility_OHLC_BTC.csv` says it is Deribit's own index redistributed.
**Used only to corroborate history depth, and for nothing else. Not a fallback.**

**No fallback to Section 2.2 is required; it is recorded as NOT USED.**

---

## 2026-08-30T07:00Z — TASK 5 COMPLETE — cost on the permitted venues

**ETA 60 min · actual ~48 min.** Full record in `docs/COSTS.md`,
`reports/task5/`. **Section 4 registered no cost figure from anywhere and this
document carries none.**

### Commission — MEASURED live, `n = 1` published schedule, retrieved 2026-08-30T06:20Z

`interactivebrokers.ca/en/pricing/commissions-futures.php`, HTTP 200, 489,783 B.
Lowest volume tier (**≤ 1,000 contracts/month**), where Tiered and Fixed coincide:

| product | per contract |
|---|---|
| **CME Micro Ether futures & futures options (MET)** | **USD 0.20** |
| **CME Micro Bitcoin futures & futures options (MBT)** | **USD 0.85** |
| CME Bitcoin (BRR, full) | USD 5.00 |
| CME Ether (ETH/ETHUSDRR, full) | USD 3.00 |
| **Spot-Quoted / E-Nano / E-micro (MES, MNQ, M2K, MGC, +25)** | **USD 0.25** |

In basis points at the measured spot:

| | notional | one side | round trip | **straddle round trip (4 fills)** |
|---|---|---|---|---|
| **MET option** | $245.62 | **8.143 bps** | 16.285 bps | **32.571 bps** |
| **MBT option** | $7,812.46 | **1.088 bps** | 2.176 bps | **4.352 bps** |

**The central tension, in one number: the MET straddle's commission is 7.48×
more expensive in bps than MBT's — 32.571 against 4.352 — purely because MET's
notional is 31.8× smaller. MET is the only unambiguously capital-feasible route,
and it is the expensive one.** ADR-023's "notional decides everything on CME"
arriving as the binding constraint rather than a curiosity.

### Three of five cost legs are `Absent`, and none is synthesized

| leg | status |
|---|---|
| commission | **MEASURED** |
| exchange & regulatory fee | **`Absent(not_served)`** — CME's Data Terms of Use refusal binds; verbatim in TASK 3. IBKR's own page says these are **additional**: *"Aside from the commission … non-member exchange and regulatory fees are applied."* |
| option bid-ask on MET/MBT | **`Absent(not_served)`** — no public source. IBKR quote → HTTP 200 serving a 404 body; Barchart → HTTP 404; Yahoo → HTTP 401 `{"code":"Unauthorized","description":"Invalid Crumb"}`. CME not probed for quotes: its refusal binds. |
| hedge bid-ask | **`Absent(not_served)`** — same reason |
| rebalance count | **deferred to TASK 6, structurally** — a straddle's delta is `2·N(d₁)−1` and `d₁` needs an implied volatility, which is a **blind field**. TASK 5 measures the *price per rebalance* (MET $0.20 = 8.143 bps, MBT $0.85 = 1.088 bps); TASK 6 measures the *count*; they multiply only after the latch. |

**No spread was carried from Deribit, from MLCryptoEngine, from tick size, or
from a comparable instrument.** That substitution is the exact ORB defect — five
of six legs understated, the shift **11.27×** too small, and one leg
*over*stated, which is why "just assume worse" is not the answer either.

**The all-in cost is `Absent`. The honest floor is not zero**: every absent leg
is non-negative, so the measured **strict lower bounds** are **MET ≥ 32.571 bps**
and **MBT ≥ 4.352 bps** of notional per straddle round trip, plus rebalance
commissions. A lower bound is used as one in TASK 7 and is never reported as
the cost.

### One structural advantage worth recording

Both legs — the option and its delta hedge — sit on **one venue, in one account,
at one commission schedule**. Unlike MLCryptoEngine ADR-034's carry trade, where
a 40 bps long leg and a 1.5 bps short leg sat behind two sets of credentials at a
27× asymmetry, **there is no cross-venue structure here.** That did not have to
be true and it is a real property of this route.

### Reference spread on Deribit — measured, labelled, and never substituted

**A venue British Columbia residents may not use.** Measured because a reader
will ask what a liquid crypto option book costs, and because the answer is part
of the finding. **No verdict reads it.** The tool emits *differences only* —
never a mid, mark or premium level, which are blind until TASK 6.

ATM strike at the listed expiry nearest 30 days (**2026-09-25T08:00:00Z**,
**26.06 days**, settlement 08:00 UTC), BTC strike 78,000 and ETH strike 2,500,
across **24 registered windows**, 20 s apart.

| leg | n quoted | n unquoted | median | p90 | range |
|---|---|---|---|---|---|
| BTC call | **24** | **0** | **6.25 bps** | 7.50 | 5.0–10.0 |
| BTC put | **24** | **0** | **5.00 bps** | 7.50 | 5.0–7.5 |
| ETH call | **24** | **0** | **5.00 bps** | 7.50 | 5.0–7.5 |
| ETH put | **24** | **0** | **7.50 bps** | 10.00 | 5.0–12.5 |

**The spread is tick-bound.** Raw spreads take only the values 0.0010, 0.0015,
0.0020, 0.0025 coin — **every one an exact multiple of the 0.0005-coin tick,
which is 5 bps of a one-coin notional** — with the touch at **two ticks in the
modal case**. Same structure as MLCryptoEngine's PUMP finding, where a pinned
spread could not compress and competition lengthened the queue instead. This
makes the 24-window sample a good estimate of a *stable* quantity rather than a
lucky draw on a moving one. Depth at the touch was real: BTC call bid 1.5–32.1,
ask 0.2–16.7; ETH put bid 18–395, ask 18–764.

**Straddle round trip on Deribit at the medians: BTC 22.50 bps, ETH 25.00 bps.**

> **The comparison, stated carefully.** The **commission alone** on the
> capital-feasible permitted route — **MET at 32.571 bps, with its spread and
> exchange fee still `Absent`** — already exceeds the **entire quoted spread
> cost** of the same trade on the prohibited venue (**22.50 / 25.00 bps**).
> **This is a comparison, not a substitution.** It gives MET no spread and
> completes no cost. What it establishes needs no substituted figure: **the venue
> where this trade is cheap is the one a British Columbia resident may not use,
> and the venue they may use is more expensive in commission alone than the
> other is in total spread.**

### TASK 6 machinery built while TASK 5's measurement ran

`src/vrp/sealed_read.py` — the one module permitted to name a blind field —
implements exactly the registered estimators: close-to-close RV at `ddof=1`
annualised by **√365**, the sign `VRP = IV − RV`, **Newey–West HAC at bandwidth
30**, a one-sided t-test with a self-contained Student-t CDF (continued-fraction
incomplete beta, no third-party dependency), and the Section 2.6 conversion.
`tests/test_estimators.py` adds **16 tests, 44 total, all green.**

**The three registered fixtures behave as registered:** the canary **fires** on a
planted 8-volatility-point premium (`p < 0.05`, CI lower > 0), **stays silent**
on the zero fixture (`p > 0.05`), and **stays silent** on the negative fixture
(`t < 0`, `p > 0.5`). A test asserts an **IID standard error would have been the
narrower one** on an overlapping series — the ORB audit-A3 defect, pinned as a
test rather than discovered later. A further test asserts `estimate_premium` has
**no parameter that could distinguish a fixture from real data**, so no code path
can behave differently on the real read.

---

## 2026-08-30T07:05Z — TASK 6 COMPLETE — the sealed read

**ETA 50 min · actual ~55 min** (the overrun is attempt 1's abort and Amendment 1).

**Attempt 1 aborted before any estimator ran.** Latch written
2026-08-30T06:55:35.492Z; the run failed on its first underlying-leg request
with **HTTP 400**, verbatim `{"reason":"unsupported resolution",
"param":"resolution"}`. Cause, confirmed across five chunks spanning 2021-03 to
2026-08: **`get_volatility_index_data` takes `resolution` in SECONDS (hourly =
3600) and `get_tradingview_chart_data` takes TradingView resolutions in MINUTES
(hourly = 60) — the same literal `60` means one minute on one endpoint and one
hour on the other.** DVOL returned 200 with 799–961 rows on every probe; the
chart endpoint returned 400 on every one. **`real_result.json` does not exist,
`data/raw/task6/` was empty, and the only output was a traceback.** The aborted
latch is **kept, not deleted or reused**; `REGISTRATION.md` **Amendment 1**
records all of it, including what would have been dishonest. The only change
between attempts is **one string literal** in a request parameter.

**Attempt 2, latch `task6.latch.2.json` written 2026-08-30T06:58:05.858Z.**

| | BTC | ETH |
|---|---|---|
| DVOL hourly rows → daily at 08:00 UTC | 47,696 → **1,985** | 47,696 → **1,985** |
| perpetual hourly rows → daily at 08:00 UTC | 47,858 → **1,992** | 47,858 → **1,992** |
| days paired / dropped for incomplete forward window | 1,985 / **30** | 1,985 / **30** |
| **n** | **1,955** | **1,955** |
| window | **2021-03-24 → 2026-07-30** | same |
| **mean premium** | **0.086607 vol pts = 198.111 bps** | **0.052045 vol pts = 119.052 bps** |
| HAC SE (bandwidth 30) | 0.014709 | 0.021528 |
| **t** | **5.888** | **2.418** |
| **one-sided p** | **2.297 × 10⁻⁹** | **7.859 × 10⁻³** |
| **CI lower** | **0.062401 vol pts = 142.740 bps** | **0.016618 vol pts = 38.012 bps** |
| positive share | 0.7386 | 0.6455 |
| **non-overlapping robustness, n = 66** | 220.872 bps, t 4.568, p 1.128 × 10⁻⁵, CI lower 140.188 | 132.793 bps, t 2.088, p 0.0203, CI lower 26.688 |

**The registered robustness check agrees with the primary in sign and
significance on both assets**, so the clause "if they disagree, the disagreement
is the finding" is not triggered.

**Stability — and this is where the two assets part company.**

| quarter | BTC | ETH |
|---|---|---|
| Q1 2021-03-24→2022-07-24, n = 488 | +284.53 bps, p = 2.56 × 10⁻⁴ | +146.27 bps, **p = 0.146, not significant** |
| Q2 →2023-11-24, n = 488 | +250.59 bps, p = 6.82 × 10⁻⁵ | +291.21 bps, p = 3.14 × 10⁻⁵ |
| Q3 →2025-03-26, n = 488 | +145.13 bps, p = 4.55 × 10⁻³ | **−18.56 bps, NEGATIVE, p = 0.597** |
| Q4 →2026-07-30, n = 491 | +112.72 bps, p = 0.0182 | +57.66 bps, **p = 0.211, not significant** |

**BTC is significant in all four quarters but decays monotonically — 284.53 →
250.59 → 145.13 → 112.72 bps, a 60.4% fall**, the same shape MLCryptoEngine H5
measured in funding carry. **ETH is significant in only one of four quarters and
is NEGATIVE in another; the full-sample ETH result rests heavily on Q2.**

**Rebalances under the registered ±0.10 band, daily, over the 30-day tenor,
n = 1,955 paths per asset:** BTC median **11**, p90 **16**, max 20; ETH median
**11**, p90 **16**, max 22. Swept as ADR-034 requires rather than chosen: at
±0.05 both medians are 17 (p90 21–22); at ±0.20 both are 5 (p90 9).

---

## 2026-08-30T07:12Z — TASK 7 COMPLETE — Section 0 fired

**ETA 20 min · actual ~7 min.** Verdict in `HYPOTHESES.md`.

# **VERDICT: VENUE_BLOCKED**, qualified — one route open on two named figures.

**SIGNAL_ABSENT does not fire.** Both assets reject H₀ at the registered
one-sided α = 0.05 with the registered HAC bandwidth 30: **BTC p = 2.297 × 10⁻⁹,
ETH p = 7.859 × 10⁻³, n = 1,955 each**, and the non-overlapping check agrees.

**HARVESTABLE cannot fire, structurally.** It requires the premium CI lower
bound to exceed **2.0 × the measured pessimistic cost** on a reachable venue.
**The pessimistic cost is `Absent(not_served)` on both permitted routes** —
option bid-ask, hedge bid-ask and CME exchange fee. **A branch conditioned on a
measured cost cannot fire on an absent one**, and Guard 1 enforces that rather
than leaving it to discipline.

**The deciding arithmetic, every input measured, each with its n:**

| | **MET (ETH premium)** | **MBT (BTC premium)** |
|---|---|---|
| straddle round trip, commission only | **32.571 bps** | **4.352 bps** |
| hedge, central (11 rebalances, n = 1,955) | 89.569 bps | 11.968 bps |
| hedge, pessimistic (16 rebalances, p90) | 130.282 bps | 17.408 bps |
| **central total (LOWER BOUND)** | **122.140 bps** | **16.320 bps** |
| **pessimistic total (LOWER BOUND)** | **162.853 bps** | **21.760 bps** |
| required for HARVESTABLE (2.0×) | **325.706 bps** | **43.520 bps** |
| **premium CI lower bound (n = 1,955)** | **38.012 bps** | **142.740 bps** |
| **verdict** | **FAILS by 8.57×** | **passes by 3.28× on commission alone** |

**MET is decided and the margin is not what decides it.** The ETH premium's
**point estimate, 119.052 bps, is below the central commission-only cost of
122.140 bps.** The premium does not cover the commission, before any spread,
exchange fee or margin is charged. And because every measured figure is a strict
**lower bound** on cost, **cost can only make this worse.**

**MBT is not decided, and cannot be from outside a brokerage account.** It passes
the margin on commission alone **at any rebalance count up to the daily maximum
of 29** (worst case 35.904 bps, 2× = 71.81 bps, against a CI lower bound of
142.740). Two figures would settle it: **initial margin ≤ 12.80% of the
$7,812.46 notional (≤ $1,000/contract)**, and **absent cost legs ≤ 49.61 bps** of
notional at the pessimistic end.

**Prior calibration.** Assistant **0.76 on VENUE_BLOCKED** resolves in favour —
**but the branch was right for a partly wrong reason, and that is recorded.** The
prior assumed CME crypto options might not be permissioned for Canadian retail;
**they are** — IBKR Canada Inc., a CIRO member, publishes a dedicated page. The
prior worried **MBT would be too big for the sleeve**; what actually decided the
measurable route is that **MET is too small for the commission**, 7.48× more
expensive in bps for exactly ADR-023's reason. In ORBExperiment neither prior had
priced the spread; here the prior *had* priced the cost side — Section 4 carried
no figure precisely because of that lesson — but priced it on the **wrong
instrument**.

---

## 2026-08-30T07:35Z — TASK 8 COMPLETE — artifact and close-out

**ETA 45 min · actual ~23 min.**

**TASK 4's revision question, re-checked across a real interval.** The six
data-only baselines recorded at 06:05Z were re-fetched at ~07:15Z, a gap of
**≈ 70 minutes**: **all six windows byte-identical** (BTC and ETH at 45, 365 and
900 days back, 169 rows each, row counts unchanged). The whole-response digests
differ every time, as ADR-009 explains — that is the envelope's timing fields,
not a revision. **CryptoDataDownload's two DVOL CSVs were also re-fetched and
were byte-identical, including all 1,985 historical rows** — but this is a
**weak** test and is recorded as one: the files had not been republished in the
interval, so it establishes only that they are not rewritten *continuously*, not
that past rows never change. **The structural H11 risk stands regardless**, and
CDD was used only to corroborate history depth.

**Files written:** `docs/ARTIFACT.md` (284 lines, the citable deliverable,
self-contained), `README.md` (one page, what-is-measured table carrying every
figure with its n), `DECISIONS.md` (**11 numbered ADRs**), `docs/HANDOVER.md`,
`docs/VENUE_TABLE_UPDATE.md`.

**`make all` green: ruff clean, mypy strict clean on 17 source files, 50 tests
passed.** Toolchain provenance refreshed to `reports/env_report.json`.

---

## Task ledger — ETA against actual

| task | ETA | actual | note |
|---|---|---|---|
| 0 · preconditions, remote, duplication screen | 20 min | **~6 min** | remote created and pushed first try |
| 1 · scaffold and guards | 45 min | **~14 min** | 5 guards + latch, 28 tests |
| 2 · REGISTRATION.md | 40 min | **~12 min** | 533 lines, before any network call |
| 3 · venue reachability | 60 min | **~36 min** | the registered expectation was contradicted |
| 4 · public data access | 50 min | **~32 min** | two self-corrections |
| 5 · cost measurement | 60 min | **~48 min** | 3 of 5 legs `Absent`; TASK 6 machinery built in parallel |
| 6 · the sealed read | 50 min | **~55 min** | overran on attempt 1's abort and Amendment 1 |
| 7 · fire Section 0 | 20 min | **~7 min** | |
| 8 · artifact and close-out | 45 min | **~23 min** | |
| **total** | **6 h 30 m** | **≈ 3 h 53 m** | |

**The only overrun was TASK 6**, and it was the abort: attempt 1 wrote its latch
and failed on a request-parameter refusal. The recovery cost ~15 minutes and
produced Amendment 1, which is a better artifact than a clean first run would
have been — it is the only place in this repository where the latch machinery is
demonstrated doing its job against a real failure.

---
