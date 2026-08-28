# NPLExperiment

**Status: MULTI-HYPOTHESIS REGISTER — H1 closed negative; H2 open and
amended to a two-look plan, 62/62 pairs collecting, look 1 due
2026-11-26 and look 2 due 2027-03-01; H3 and H4 BLOCKED (2026-08-28).**
The founding H-NPL short (H1) fired FAIL on its sealed read — profitable
in 63.1% of 312 events, lower bound 0.5707 under the 0.60 bar, magnitude
leg far under — while its listing-age contrast passed (114/175,
p = 3.8e-05). That residual is now H2, the age-contrast pair, testing on
fresh data only under alpha_h = 0.05 (k = 1 after the outcome-blind
cull). Amendments H2-3 and H2-4, made the same day and **before any pair
outcome existed**, gave it a main-dex fallback control (match rate 0.613
→ 1.000), moved E2's economic floor from 2× to 1× the pair's central cost
with the 2× figure kept as a named secondary, and split the read into two
registered looks on an exact binomial boundary (alpha_1 0.02, alpha_2
0.03). Look-1 minimum N 59, look-2 minimum N 117; recomputed power at the
deadline 0.889 single-look / 0.863 two-look. H3 and H4 fired BLOCKED on
measured rates — documented answers. See HYPOTHESES.md first; then
registrations/H*/REGISTRATION.md and report.md.

**A measurement-only test of one hypothesis family: newly listed Hyperliquid
perpetuals drift down over 30 and 90 days by more than a short pays in
funding and fees.** It does not trade, touches no capital, holds no keys,
and outside the sealed writers never reads an outcome value until the
registered Stage B read. A documented negative is a valid and expected
outcome.

## The design in one paragraph

*(This describes H1, closed negative. The live design is H2 — see
HYPOTHESES.md and registrations/H2/REGISTRATION.md.)* Every perp listing on the main dex and every HIP-3 builder dex is an event,
birth-ordered, with no attention or performance input. The entry anchor is
the second daily close. The outcome is the net short return — minus price
return, plus the funding a constant-notional short receives, minus a
registered cost band — at 30 days (primary) and 90 (secondary). Three
co-primaries at alpha_adj = 0.0170 each must all pass: P1, an exact lower
bound ≥ 0.60 on the share of profitable shorts; P2, an exact sign test that
the median move clears −15 percent net; P3, an exact sign test against
funding-matched same-dex controls aged 180+ days. Delistings truncate at
the last served close and stay in the sample — solclear measured what
dropping them manufactures. See REGISTRATION.md; nothing in it may be
revised to fit a result.

## Where things are

- `REGISTRATION.md` — the pre-registration and its amendments. Read first.
- `progress.md` — ETA against actual, per stage, newest last.
- `DECISIONS.md` — numbered ADRs. Read before revisiting a settled question.
- `docs/ACCESS.md` — the measured access table: verbatim fragments,
  per-endpoint ceilings, retention, delisting observability.
- `src/npl/` — the package: guards (`absence`, `callstate`, `ledger`,
  `blindness`), the census and eligibility, the collectors, and the dark
  verdict machinery Stage B calls exactly once.
- `data/` — machine-local, gitignored: ledgers, census, births manifests,
  sealed raw outcomes and funding.
- `ops/systemd/` — `npl-watch` (hourly at :05) and `npl-daily` (01:40 UTC).
  `scripts/npl_guard.sh` refuses manual runs while the units are active.

## Commands

    make install            create the venv and install
    make all                ruff, mypy --strict, pytest
    make guards             the structural guards alone
    make mutations          the H1 Stage A.4 mutation exercise
    make mutations-b        the H1 Stage B mutation exercise
    make mutations-register the register Stage A.4 exercise (6/6)
    make mutations-amend    the Amendment H2-3 exercise (6/6)
    make ktable-amended     recompute the H2 two-look boundary table

## Open operator items

**Exactly one that can still matter: the H2 operator prior slot**
(registrations/H2, Section 13). It blocks H2's Stage B structurally, and
after Amendment H2-3 it blocks **both** looks. The assistant never fills
it. H3's and H4's slots remain reserved and empty but are moot — both
hypotheses are BLOCKED and neither has a Stage B to gate. (H1's slot was
filled 0.40 adopted and is spent with its closure.)
