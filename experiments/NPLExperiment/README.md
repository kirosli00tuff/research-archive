# NPLExperiment

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

## The operator's one open item

REGISTRATION.md Section 13 reserves the operator prior slot, empty. The
assistant priors recorded beside it are not the operator's number, and the
empty slot blocks Stage B structurally.
