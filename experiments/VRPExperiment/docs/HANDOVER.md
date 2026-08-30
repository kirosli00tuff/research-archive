# HANDOVER — VRPExperiment

**Repository status: CLOSED, 2026-08-30. Verdict VENUE_BLOCKED**, qualified.
One stage, one artifact, no successor here.

**Remote: `https://github.com/kirosli00tuff/VRPExperiment` (private). Created
and pushed successfully. `gh` authentication did not fail. There is no open
operator item on the remote.**

---

## Open operator items, in priority order

### 1. Settle the one open route — MBT — with two figures **(the only item that changes a verdict)**

Everything else in this repository is closed. **CME options on Micro Bitcoin
futures, via Interactive Brokers Canada, is the one route left open**, and it is
open on exactly two figures. Both are visible in an IBKR Canada client portal in
a single session; neither is obtainable without an account.

| figure needed | threshold it must clear | why that number |
|---|---|---|
| **Initial margin on a short MBT option** | **≤ 12.80% of the $7,812.46 notional, i.e. ≤ $1,000 per contract** | Below this a $1,000 sleeve holds fewer than one position and the route is **capital-blocked** |
| **All-in MBT option + futures bid-ask, plus CME exchange and regulatory fees**, at the pessimistic (90th-percentile) end | **≤ 49.61 bps of notional** | The room between the BTC premium's one-sided 95% lower bound (142.740 bps) and twice the measured commission-only pessimistic cost (2 × 21.760 = 43.520 bps) |

**If both clear, the honest reading is that the registered HARVESTABLE
condition was met on MBT** — and per Section 0 that makes a successor sleeve
worth registering **in its own repository, on its own registration**. *This
repository still closes either way.*

**If either fails, VENUE_BLOCKED is unqualified** and the question is finished.

**Sampling instructions are already registered and need no further decisions:**
Section 4.1 (≥ 20 distinct observation windows on the ATM 30-day series, median
and 90th percentile with `n`), Section 4.2 (central = median, pessimistic = p90,
assignment fixed before anything downstream), Section 4.3 (±0.10 delta band
evaluated daily, swept at ±0.05 and ±0.20).

### 2. Carry the venue-table corrections across to MLCryptoEngine

`docs/VENUE_TABLE_UPDATE.md` holds three corrections and a set of recorded
absences, with provenance. **This repository did not and must not edit
MLCryptoEngine.** The unambiguous part is the notional column: **MBT
$6,505 → $7,812.46 (+20.1%)** and **MET $191 → $245.62 (+28.6%)**, both direct
measurements corroborated by a second public source. The fee-side rows are
**commission-only lower bounds** and must be labelled as such rather than
silently replacing the existing all-in figures.

### 3. Record an operator prior, if the calibration ledger is wanted

**The Section 9.2 operator slot is empty.** It blocked nothing in a single-stage
census, by design. The assistant's prior (**0.12 / 0.76 / 0.12** over
HARVESTABLE / VENUE_BLOCKED / SIGNAL_ABSENT) resolved in favour of the branch it
weighted — **but for a partly wrong reason**, and `HYPOTHESES.md` records that
in full. If the calibration ledger is to score this stage, note that a prior
which gets the branch right through a wrong mechanism should not be scored as a
clean hit.

### 4. `Absent(not_served)`: CME margins for MES, MNQ, MGC, MBT

Sought for the programme venue table, not for this hypothesis. **Not obtainable
without an account**, and CME's own Data Terms of Use refusal was obeyed rather
than worked around. Details and the reasoning in `docs/VENUE_TABLE_UPDATE.md`.

---

## Things a successor must not do

- **Do not re-run the TASK 6 real read.** The latch is spent. `--mode real`
  raises `LatchAlreadySpentError`, and a second read of the window voids the
  hypothesis. Both latches — attempt 1 (aborted) and attempt 2 (the read) — are
  committed and must stay.
- **Do not substitute Deribit's spread for a CME spread.** It is measured and
  labelled REFERENCE ONLY for exactly this reason. See ADR-008 and the
  ORBExperiment precedent it cites: a carried band understated five of six legs
  and produced a shift 11.27× too small, while overstating a sixth.
- **Do not treat the premium as a return.** No sleeve was simulated. The tail —
  the move absent from a 5.4-year sample, which is the entire risk a variance
  seller bears — is unmeasured. **This measured the payment, not the liability.**
- **Do not rely on the ETH premium.** One of four quarters is individually
  significant and one is **negative**; the full-sample result rests on 2022–2023.
- **Do not read the BTC premium as stationary.** It decays monotonically across
  the sample, **284.53 → 250.59 → 145.13 → 112.72 bps**, a 60.4% fall.
- **Do not re-verify a revision by comparing whole HTTP responses.** Deribit's
  envelope carries `usIn`/`usOut`/`usDiff` timing fields that change every call.
  Compare the canonicalised `result.data` array. See ADR-009.

---

## Where the evidence is

| question | file |
|---|---|
| the deliverable, self-contained | **`docs/ARTIFACT.md`** |
| what was registered, and when | `REGISTRATION.md` (commit `7827592`, before any network call) + Amendment 1 |
| the verdict and its inputs | `HYPOTHESES.md` |
| why this is not a duplicate of three prior closures | `docs/DUPLICATION.md` |
| venue policies, verbatim, with dates | `reports/task3/deribit_restricted_jurisdictions_verbatim.md`, `reports/task3/venue_table.md` |
| robots.txt and the CME refusal, verbatim | `reports/task3/robots_and_terms.md` |
| what the public endpoints serve and refuse | `docs/ACCESS.md`, `reports/task4/` |
| cost, and the three absent legs | `docs/COSTS.md`, `reports/task5/` |
| the sealed read | `reports/task6/real_attempt2_result.json`, latches alongside |
| decisions and their reasoning | `DECISIONS.md` |
| the run log, ETA against actual | `progress.md` |

## Reproducing

```bash
make install && make all
```

**`make all` green: ruff clean, mypy strict clean, 50 tests passed.** Python
3.13.14, ruff 0.16.5, mypy 2.3.1, pytest 9.1.1; full provenance in
`reports/env_report.json`.

`python tools/task6_sealed_run.py --mode fixture` re-runs the entire estimation
pipeline against synthetic data with a known planted premium, touching no latch
and reading no real data. It is the honest way to inspect the machinery now that
the real read is spent.
