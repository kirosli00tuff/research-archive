# Stage B.1 Task 0: the price reconciliation

Dated 2026-08-24. Checked 2026-08-24 to 2026-08-25 UTC.

## The discrepancy

A.1 measured the 2026-07-01 width-20 book's median share price at
143.89 from stored adjusted closes, adjustment=all as of the 2026-07-24
pull. A.2 measured the same book's median mid at 103.25 from live
consolidated quotes over sessions 2026-08-19 to 2026-08-21. The ratio
of medians is 0.7176, a 28.2 percent gap. Momentum drift explains some.
A split after the pull date would explain the rest silently, because
the stored series reflects only actions known at pull time. This report
settles which.

## The check

Source: stockanalysis.com, retrieved 2026-08-24, one page per name plus
the 2026 splits calendar. AiTrader's credential path is off limits this
stage and HFExperiment's own Alpaca keys are not yet in .env, so a
public corporate-actions source was used. Each name was checked for
splits in 2026 and for dividends with an ex-date between 2026-07-24 and
2026-08-24. The splits calendar's visible slice covered 2026-08-03 to
2026-08-24 with none of the 20 names present. The per-name pages close
the remaining 2026-07-24 to 2026-08-02 window.

## Result: zero corporate actions in the window

No name in the book split in 2026. No name went ex-dividend between
2026-07-24 and 2026-08-24. Three names pay dividends at all, and every
ex-date misses the window: MU last went ex 2026-07-06 at 0.15 per
share, WDC next goes ex 2026-09-08 at 0.60, STX next goes ex 2026-09-24
at 2.96. The largest of these is 0.37 percent of price, immaterial
against a 28 percent gap even had it landed inside the window.

## The basis cross-check

With zero actions in the window, the pull-time share basis IS the
current share basis, so the two medians already sit on a consistent
basis and differ only by date. Two independent confirmations:

1. Every stored 2026-07-01 close sits inside the name's current-basis
   52-week range. A missed 2:1 split would put the stored close near or
   above twice the displayed high. INTC's stored 139.63 sits within 2
   percent of its displayed high of 142.35. MXL's stored 128.03 sits
   within its displayed high of 128.30.
2. The two names whose July-to-August ratios looked split-shaped were
   checked individually. MXL at ratio 0.518 near one half: no split, no
   dividend, the name halved on market moves and closed 2026-08-24 at
   62.78. WOLF at ratio 0.546: no split, no dividend, closed at 24.76.

## The medians recomputed on the consistent basis

| measure | value | date | basis |
|---|---|---|---|
| median close, A.1 | 143.89 | 2026-07-01 | consistent, confirmed |
| median mid, A.2 | 103.25 | 2026-08-19 to 21 | consistent, confirmed |
| median close, this check | 97.45 | 2026-08-24 | consistent, current |

The third row is the median of the 2026-08-24 closes retrieved during
this check, 19 names plus MU at its 2026-08-21 measured mid because the
MU page fetched was its dividend page. It extends the A.2 measurement
by one more session of decline and sits on the same basis.

Per-name ratios of live mid to stored close run continuously from 0.52
to 1.06 with no isolated split-shaped outlier. That distribution is the
signature of a correlated selloff, not an adjustment artifact. The book
is four correlated sector bets per the Section 4 registered risk, and
it drew down 28 percent at the median between formation and the A.2
measurement.

## Verdict

The gap RECONCILES as market movement. No stale adjustment exists in
the stored series for these 20 names. The bar pipeline may build on the
fresh-query design, which exists so this check never has to be run by
hand again: every daily and formation query re-fetches with
adjustment=all, so an action landing between runs re-enters the store
rather than aging out of it.

What would change this verdict: a corporate action the public source
missed. The pipeline's first formation run re-queries every trailing
window fresh, which would surface exactly that as a discontinuity
against these recorded numbers.
