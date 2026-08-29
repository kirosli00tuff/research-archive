# retail-power-limits

**Across four independent pre-registered experiments, the binding constraint was
not whether a published effect exists but whether an achievable sample could
detect an effect of the reported size.** Each closed at *unresolved at
achievable power*, at *untestable at achievable power*, or *BLOCKED* on a power
gate — never on a measured null. In two of the four the outcome variable was
never read at all, and a third closed with its own forward series never started.

**This is not evidence that those anomalies are absent, and four cases are four
cases rather than a survey; the note claims a detectability result about
retail-scale replication and nothing more.**

Read the note: **[docs/the-power-limit.md](docs/the-power-limit.md)**.

## The four cases

| experiment | measured detectability | against | closed at |
|---|---|---|---|
| NPDExperiment | minimum detectable contrast **0.0512** | an effect band of **0.01 to 0.05** | unresolved at achievable power |
| InsiderExperiment | minimum detectable effect **49.35 bp per month** | 30 to 40 bp gross, 13.3 to 34.7 net, BLOCKED floor 40 | **BLOCKED** on the power gate |
| ETFExperiment | **163** admissible days projected at its deadline | a governing minimum of **300**; **845** for E1 and **above 1,200** for E2 at the registered assumption, against about **302** reachable by 2027-10-31 | untestable at achievable power |
| HFExperiment | **z 1.668** against a corrected bar of **2.50** | 104.0 %/yr of excess needed, 70.5 delivered | resolved on statistical power, not absent signal |

Full extraction, every figure with its repository, file and commit:
**[SOURCES.md](SOURCES.md)**.

## What the note argues

1. **The claim and its scope limit**, stated before the evidence.
2. **The four cases**, with their measured detectability against their effect
   bands — and four figures corrected against the record.
3. **The progression**, which is the spine: NPDExperiment discovered the problem
   after collecting, spending **6.9378 USD** and opening its one-shot sealed
   store; InsiderExperiment then registered a power gate in its Section 0
   *because of it*, quoting NPDExperiment by name, and fired BLOCKED at zero
   dollars with its alpha still sealed. That progression from expensive
   discovery to cheap refusal is the transferable output, and it matters more
   than any individual closure.
4. **The contrast cases** — MLCryptoEngine, solattn, solclear — because not
   every closure in this program was a power closure, and naming them dates the
   shift.
5. **The practice**, stated so someone else could adopt it: compute the minimum
   detectable effect from dispersion and sample size alone before any first
   moment is read; fix the effect band from the published record and derive the
   bars from it; commit the gate before the measurement it judges; and treat
   BLOCKED as a cheap and legitimate outcome rather than a failure.
6. **What would change the conclusion**: a domain whose effects are large
   relative to achievable samples, not a better estimator on the same ones.

## What this repository is not

It holds no market data, opens no data source, computes no statistic, and makes
no claim about any market. It has no execution path and never had one. It is a
note plus the machinery that keeps the note's figures pinned to their sources.

## Layout

    README.md                  this file: the claim and the scope limit
    docs/the-power-limit.md    the note
    SOURCES.md                 every figure mapped to repository, file and commit
    DECISIONS.md               ADRs, including why this lives in its own repository
    progress.md                append-only stage record, ETA against actual
    rplimits/                  the sourced figures, and the renderers for the
                               generated blocks in the documents
    tests/                     honesty tests, drift tests, credential scan

## Running it

    make install     create the venv and install
    make check       lint, typecheck, test      # the gate
    make tables      print the generated blocks
    uv run python -m rplimits --write           # regenerate the blocks in place

## The honesty tests

`tests/test_honesty.py` fails the build if the scope-limit sentence is deleted
from this file or from the note, or if any headline figure — `0.0512`,
`0.01 to 0.05`, `49.35 bp per month`, `845`, `above 1,200`, `302`, `z 1.668`,
`2.50`, `6.9378 USD` — stops being reported. A separate test scans every tracked
file for credential-shaped strings, and each detector has a canary asserting it
actually fires. A future session cannot quietly soften the scope limit or drop
an inconvenient number.

## Licence

MIT. See [LICENSE](LICENSE).
