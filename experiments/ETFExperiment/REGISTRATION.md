# REGISTRATION.md — the pre-registration

> **STATUS: SECTION 0 REGISTERED 2026-08-28, BEFORE ANY NETWORK CALL.**
>
> At the moment this document was first committed, **this repository had sent
> no request to any endpoint, held no flow value, no price, no funding row, and
> no census row of any kind.** The request ledger did not exist. That ordering
> is what makes this a pre-registration rather than a description.
>
> **From this point the specification is closed.** Where the specification and
> reality disagree, the session reports and stops rather than choosing.
> Changing anything here requires a **new dated amendment** appended at the
> bottom, with its reason and a statement of exactly what data existed at the
> time it was made. Nothing above an amendment line is ever edited.
>
> **Disclosure.** NPLExperiment (REGISTRATION.md, HYPOTHESES.md, progress.md),
> MLCryptoEngine (HYPOTHESES.md H11, report.md line 2734, DECISIONS.md
> ADR-055), solattn (DECISIONS.md ADR-019/021/022) and InsiderExperiment
> (progress.md) were read before this was written, and their measured figures
> are carried below with their sources. The external figures of Section 14 were
> supplied by the operator with their sources named and **none of them was
> measured by this repository**; each is labelled where it is used. No
> ETFExperiment data of any kind existed.

---

## 0. The outcome map — it judges collection feasibility and detectability, never returns

The Section 0 verdict fires in Stage A.2 Task 5 from the admissible-day census,
the power computation, and the Stage A.1 access, lag and observability
findings. **It reads no outcome value: every input is a count-derived power, a
measured share, or an operational verdict.**

- **GO:** **both** co-primaries of Section 8 reach **at least 80 percent power
  at alpha_adj** under the **registered effect assumption** of Section 9 (rank
  correlation 0.09), at the achievable admissible-day count by **2027-03-31**,
  **and** the as-printed observability test of A.1 Task 4 **passes in full**.
- **DEGRADED:** E1 reaches at least 80 percent power at the **published-
  magnitude** assumption (rank correlation 0.18) but under 80 percent at the
  registered assumption, **or** as-printed observability **passes partially**.
  Collection proceeds. Recomputed power is stated beside the registered target.

  **The verdict scope narrows, and the narrowing is stated here in plain words
  before any data exists: under DEGRADED a Stage B FAIL establishes that the
  effect is not present at its published magnitude, and cannot distinguish a
  decayed effect from no effect at all.**
- **BLOCKED:** E1 under **50 percent** power at the published-magnitude
  assumption at the achievable count by 2027-03-31, **or** as-printed
  observability **FAIL**, **or** a measured revision rate high enough that **no
  stable as-printed value exists before the entry anchor on a majority of
  days**. Nothing armed beyond the census.

**The residual band, registered rather than left as a gap.** The three clauses
above leave one case unnamed: E1 power at the published magnitude between the
0.50 BLOCKED floor and the 0.80 GO floor, with observability passing in full.
It is registered here as **DEGRADED** — it sits above the floor that stops
collection, so collection proceeds under the DEGRADED narrowing above. Naming
it now is cheaper than discovering the gap while holding a number.

**Precedence, fixed.** The three BLOCKED triggers are evaluated first and in
the order written; GO second; DEGRADED is the residual. A BLOCKED trigger fires
even at perfect power, because a design that cannot observe its own signal at
the anchor is not rescued by sample size.

Enforced by `etf.section0.fire_section0`, committed with this document and
pinned by `tests/test_section0.py`, with every boundary fixture sitting exactly
on the registered boundary: 0.80 and 0.50 on the power floors, 0.50 on the
majority share, and one-ULP steps across each. The observability verdict itself
is fired by `etf.observability.fire_observability`, pinned by
`tests/test_observability.py` with fixtures exactly on the 0.60 and 0.90 bars.

### Registered expectation, stated now so the verdict reads as a documented answer

**The Section 9 arithmetic and the decay evidence of Section 14 point to
DEGRADED.** The registered assumption is a rank correlation of 0.09; a
threshold-free permutation test needs several hundred admissible days to reach
80 percent power against it, and the achievable admissible-day count by
2027-03-31 is bounded by roughly 250 US trading days of out-of-sample history
plus forward accrual. The published-magnitude figure of 0.18 is reachable on
that sample; the registered half is likely not.

This is stated **before the census exists** so that the verdict, when it fires,
reads as a documented answer rather than a disappointment. **A DEGRADED here
narrows a question rather than abandoning it, and a BLOCKED is a documented
answer, not a failure of process.** InsiderExperiment closed BLOCKED before
measurement and that closure is the cheapest finding in the house record.
