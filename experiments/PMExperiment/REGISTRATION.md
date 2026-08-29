# Binding registration — PMExperiment

**NOT YET REGISTERED. This file is a scaffold.**

Section 0 must be written and committed **before the first request goes out**.
Until that commit exists, no request may be sent and no statistic may be
computed. Once Section 0 is committed, changing any registered value requires a
numbered amendment appended to Section 17. Nothing edits in place.

Every number in this document must be **derived or measured, not assumed**. An
assumption is labelled as one, with its direction of bias named.

---

## Section 0. The gates

*To be written in Stage A Task 0, before any request.*

Two things fire here, and neither reads a first moment relating price to
outcome.

- **The access gate** reads whether the data is reachable at all.
- **The power gate** reads a minimum detectable effect, built from a dispersion
  and a bucket count and from nothing else.

### 0.1 Why this section exists

NPDExperiment closed at *unresolved-at-achievable-power*. Its realized minimum
detectable contrast came in at **0.0512** against a realistic effect band of
**0.01 to 0.05**, so the design could not have detected an effect anywhere in
the range the literature reports. That was discovered after **415 days** of
collection, in the same session that read the result. Its ADR-007 had
registered the risk in advance and the arithmetic still landed too late.

InsiderExperiment registered its power gate before spending and fired
**BLOCKED at 49.35 bp**.

This repository follows Insider. The gate is committed before the measurement
it judges, so the answer cannot be read against a threshold its own measurement
could see.

### 0.2 Outcome map

*To be registered. Conditions defined on counts and dispersion only.*

| verdict | condition | consequence |
|---|---|---|
| GO | *to be registered* | Stage B proceeds against the registered target |
| DEGRADED | *to be registered* | proceeds with the achieved sample, recomputed power stated beside the registered target |
| BLOCKED | *to be registered* | no verdict claimed; artifacts preserved |
| PENDING_ACCESS | public data unreachable or too shallow to compute the gate | Section 0 reports on **access**, not on the hypothesis |

**A split verdict is legitimate and must be reported as such:** the
unrestricted universe may clear while the Canadian-permitted subset is BLOCKED.
That finding is "the mispricing may be real and not reachable from Canada," and
it is a result rather than a failure.

---

## Section 1. Universe and the permitted subset

*To be registered before any outcome is read.*

Two universes, reported separately and never pooled:

- **Unrestricted.** All resolved contracts retrievable from the public source.
- **Canadian-permitted.** The registered filter: the three permitted
  categories (economic indicators, financial markets, climate), the 30-day
  minimum maturity, and a volume floor chosen and justified **before** it is
  applied.

The filter is registered, then reported on. **It is not tuned to increase the
sample.** The sample it costs is a first-class output.

---

## Section 2. The cost model

*To be registered in full before anything is measured.*

Registered before measurement so no cost can be chosen after seeing a result:
per-contract fee per side, the FX schedule, and a spread assumption **stated as
an assumption** with its direction of bias named.

---

## Section 3. The effect band under test

*To be registered.* The published favourite-longshot magnitudes this design is
powered against, cited to source, so the minimum detectable effect is judged
against a number fixed in advance.

---

## Section 4. What is never computed before the gate

No calibration curve. No realized return by price bucket. No contract-level
outcome join. No statistic of any kind relating a price to a resolution.

The gate reads bucket counts and dispersion. Nothing else.

---

## Section 17. Amendments

Amendments append here, numbered, each carrying its own evidence and the date
it was made. Nothing above this line is edited after Section 0 is committed.

*(empty)*
