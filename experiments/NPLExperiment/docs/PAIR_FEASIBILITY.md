# Pair feasibility memo — H2, the age-contrast pair

**Analysis only. No capital, no orders, no execution path exists in this
repository.** This memo sizes whether the registered H2 pair could be held
at all on the venue's mechanics, because a design that cannot be held is
not worth measuring. Every figure is either registered (costs, horizons),
measured this stage (accrual, match rate), or arithmetic on the venue's
published margin mechanics (labelled as such). Written 2026-08-28 at
register Stage A.3 Task 6.

## The position, restated

One pair = **short the young listing + long its funding-matched elder, on
the same dex, equal constant notional N per leg, held 30 days**, entered
at the second daily close, exited at entry + 30d. Four fills. Registered
pair costs: 18 bp both-vanilla / 27 mixed / 36 both-HIP-3 central.

## Isolated margin on both legs

Both legs sit in **isolated margin**, deliberately: cross margin would let
a squeeze on the young short drain the elder long's collateral, coupling
exactly the two books the design wants separated. Isolated margin makes
each leg's worst case its posted margin and nothing else.

- **Young short leg:** posted margin M_s. A price rise of x wipes
  M_s − maintenance at x ≈ M_s/N (the venue liquidates at the maintenance
  floor, roughly half the initial-margin fraction at the instrument's max
  leverage — arithmetic below sizes past it).
- **Elder long leg:** posted margin M_l; worst case is the instrument
  going to zero, loss hard-capped at M_l.

## The 100-percent-adverse-move cap arithmetic (squeeze exposure)

Young listings are squeeze-prone — thin books, no borrow, reflexive
flows. The registered sizing question: **what margin survives a +100
percent move against the short leg?**

Liquidation on an isolated short at notional N with posted margin M_s
arrives near x_liq ≈ (M_s − m·N)/N, where m is the maintenance fraction
(venue: half of 1/maxLeverage; young HIP-3 listings commonly cap at 3–10x
leverage, so m ≈ 0.05–0.17). To keep x_liq ≥ 1.0 (a full doubling):

    M_s ≥ N × (1 + m)  →  M_s ≈ 1.05N to 1.17N

**Sized rule: post ~1.2N on the young short leg.** Then a +100 percent
move does not liquidate; beyond it, the isolated wall caps the loss at
1.2N regardless of how far the squeeze runs — the loss is capped by
construction, not by hope. The elder long posts 1.0N (its worst case is
−N at zero, already capped). **Capital per pair ≈ 2.2N.**

The elder does not hedge a young-specific squeeze — the pair's price legs
are hedged only against market-wide moves. The squeeze is the pair's tail
risk, it lives entirely on the young leg, and the cap arithmetic above is
what bounds it.

## Venue minimum notionals and maximum concurrent pairs at $1,000

Venue minimum order notional is **near $10** (carried figure, register
prompt). Size-decimal rounding on high-priced elders can lift the
effective minimum slightly; at the $10–25/leg range every instrument
probed this stage quotes fine steps (descriptive spread snapshots,
data/spreads/pair_spreads.jsonl, n = 78 legs).

- Capital per pair at minimum notional (N = $10/leg): ≈ **$22**.
- Concurrent pairs in steady state = accrual × hold: **18.57
  events/month × (32/30.44) months ≈ 19–20 open pairs** (measured
  accrual; entry+30d hold plus fill slack) — of which the pairable share
  (~0.61 measured, rising as young dexs age) gives **~12–14 open pairs
  today, rising toward ~19**.
- Capital needed in steady state at minimum notional: 14–20 pairs ×
  $22 ≈ **$310–$440**, against the $1,000 sleeve — headroom ≈ 2.3–3.2x,
  or equivalently **notional up to ~$22–25 per leg** with every measured
  pair held simultaneously.
- Hard cap at $1,000: **floor(1000 / 22) = 45 concurrent pairs at
  minimum notional** — above any accrual this venue has measured.

**The sleeve is feasible at the venue minimum with margin to spare; the
binding constraint is accrual, not capital.**

## Funding-flip behavior of the hedged pair

The pair's hourly funding P&L is the **differential**: the young short
receives r_young, the elder long pays r_elder, so the pair earns
(r_young − r_elder) per hour on N. The Section 6 match (nearest signed
trailing 168h mean) starts this differential near zero by construction —
the pair is funding-hedged at entry, which is the entire point of the
matched design.

The risk is **divergence after entry**:

- If the young's funding flips deeply negative while the elder's holds
  (the H8 shape: the market pricing decline into funding), the pair
  *pays* the differential — the young short bleeds funding faster than
  the elder long collects it. On the generating sample the mean paired
  funding differential over 30 days was **+0.88 points in the pair's
  favor** (n = 175, generating-sample figure, assumption not verdict) —
  small beside the +6.43-point price differential, which is what the
  pair exists to capture.
- The flip is bounded economically, not mechanically: funding cannot
  liquidate an adequately margined leg by itself at these magnitudes
  (even −100 %/yr on one leg costs ~8.2 points over 30 days on N,
  against the 1.2N wall), so a funding flip degrades the pair's net —
  it does not blow it up.
- A future execution stage (none is registered) would need a
  funding-flip kill criterion; for the measurement, the flip is simply
  part of the measured pair net, which is the honest place for it.

## What this memo does not do

It does not authorize execution, does not model fills, does not estimate
capacity beyond the venue-minimum arithmetic above, and does not touch an
outcome value. If H2's Stage B ever fires its positive row, an execution
design is a **new registration** with its own gates; this memo is the
feasibility footnote that says such a registration would not be absurd on
its face.
