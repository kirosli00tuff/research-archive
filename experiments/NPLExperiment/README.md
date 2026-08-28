# NPLExperiment

**Status: MULTI-HYPOTHESIS REGISTER — H1 closed negative; H2 open
(DEGRADED, collectors armed); H3 and H4 BLOCKED (2026-08-28).** The
founding H-NPL short (H1) fired FAIL on its sealed read — profitable in
63.1% of 312 events, lower bound 0.5707 under the 0.60 bar, magnitude
leg far under — while its listing-age contrast passed (114/175,
p = 3.8e-05). That residual is now H2, the age-contrast pair, testing on
fresh data only under alpha_h = 0.05 (k = 1 after the outcome-blind
cull; E1/E2 deadline powers 0.974/0.760; earliest Stage B ≈ mid-2027).
H3 and H4 fired BLOCKED on measured rates — documented answers. See
HYPOTHESES.md first; then registrations/H*/REGISTRATION.md and
report.md.

**A measurement-only test of one hypothesis family: newly listed Hyperliquid
perpetuals drift down over 30 and 90 days by more than a short pays in
funding and fees.** It does not trade, touches no capital, holds no keys,
and outside the sealed writers never reads an outcome value until the
registered Stage B read. A documented negative is a valid and expected
outcome.

## The design in one paragraph

Every perp listing on the main dex and every HIP-3 builder dex is an event,
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

    make install     create the venv and install
    make all         ruff, mypy --strict, pytest
    make guards      the structural guards alone
    make mutations   the registered mutation exercise (Stage A.4)

## Open operator items

Exactly the three reserved operator prior slots (registrations/H2, H3,
H4, Section 13 analogs), and nothing else. H2's is the one that will
matter — its Stage B cannot run without it. The assistant fills none of
them. (H1's slot was filled 0.40 adopted and is spent with its closure.)
