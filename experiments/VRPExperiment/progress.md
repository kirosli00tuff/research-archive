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
