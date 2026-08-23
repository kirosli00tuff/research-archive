# Predictability without capturability

**A short-horizon directional model scored AUC 0.94 on a real recorded order
book and captured about 0.03 bps per trade.** Those two facts are not in
tension, and the gap between them is the point of this note: high directional
accuracy at short horizons is fully compatible with zero capturable edge. A
result that reports accuracy without also reporting *capture*, the *cost floor*
it must clear, and the *confidence-magnitude structure* underneath it is
reporting half a result — the half that cannot be falsified by a fee schedule.

This is a negative finding from a solo quantitative research project, written up
because the negative half is the half that usually goes unpublished. Nothing
below is a recommendation, and none of it is advice about what to trade.

---

## What was measured

A gradient-boosted-tree classifier (LightGBM) was trained to predict the sign of
the next mid-price move on tick-level order-book data recorded directly from
exchange WebSocket feeds. Sampling is event bars — one sample every 50 book
updates — with 42 microstructure features (order-flow imbalance, depth, book
slope, realised volatility, time since last trade, cross-venue divergence), and
fixed-horizon labels from 100 ms out to 900 s. Evaluation is purged k-fold
cross-validation with an embargo, and every run carries a leakage suite whose
planted-future canary is verified to fire.

Venues: **Kraken spot BTC/USD** and **Coinbase Advanced Trade BTC-USD** (both
self-recorded), and **CME micro bitcoin futures (MBT)** via a Databento
historical feed.

---

## The measured chain

### 1. The accuracy is real, and it reproduces

On six validated days of Kraken BTC/USD (165,075 samples), AUC at the 100 ms
horizon is **0.9432**. That figure is not a fluke of one session: across the
four *full* days in the window it ranges 0.9345 to 0.9389 — a spread of
**0.0044**. Short-horizon directional discrimination on this book is a stable,
reproducible property of the data.

Predictability decays monotonically with horizon: 0.9432 at 100 ms, 0.8876 at
1 s, 0.7132 at 30 s, 0.5401 at 900 s.

### 2. The capture is approximately nothing

Gross capture — the mean signed move the model actually harvests per trade,
before any cost — at those same horizons:

| horizon | AUC | gross capture | Spearman rho (confidence vs \|move\|) | top decile | ratio |
|---|---|---|---|---|---|
| 100 ms | 0.9432 | **0.0291 bps** | **−0.3175** | 0.0720 bps | 2.47× |
| 500 ms | 0.9079 | 0.0576 bps | −0.2407 | 0.2223 bps | 3.86× |
| 1 s | 0.8876 | 0.0850 bps | −0.2150 | 0.2922 bps | 3.44× |
| 5 s | 0.8299 | 0.3053 bps | −0.1572 | 0.6192 bps | 2.03× |
| 30 s | 0.7132 | 0.7237 bps | −0.0465 | 1.3139 bps | 1.82× |
| 900 s | 0.5401 | 0.2093 bps | +0.0606 | 5.0020 bps | 23.9× |

Coinbase BTC-USD, same window (41,780 samples), behaves the same way: rho
−0.3665, −0.3936, −0.3855, −0.2987 at 100 ms / 500 ms / 1 s / 5 s, on AUC
falling 0.8917 (100 ms) → 0.7202 (5 s).

**Where AUC is highest, capture is smallest.** At the horizon where the model
calls direction correctly with AUC 0.94, it wins three hundredths of a basis
point per trade.

### 3. The cost floors that frame those numbers

Basis points, round trip, measured against live venue schedules rather than
assumed:

| venue | maker per side | **round trip** |
|---|---|---|
| Hyperliquid perps, base tier | 1.5 bps | **3.0 bps** |
| Kraken spot, base tier | 25 bps | **50 bps** |
| Coinbase Advanced spot, base tier | 40 bps | **80 bps** |

The AUC 0.9432 / 0.0291 bps pair was measured on **Kraken**, which charges
**50 bps** round trip. Against that, the 100 ms signal misses its own venue's
floor by roughly **1,700×**. Against the cheapest venue reachable from this
operator's jurisdiction at all — Hyperliquid at **3 bps** — it still misses by
roughly **100×**. There is no fee schedule in the reachable set that a 0.03 bps
edge clears.

### 4. The top-confidence decile does not rescue it

The obvious next move is to trade only where the model is most confident. That
was tested against a threshold registered before the numbers existed, and it
fails.

Top-confidence deciles do capture 2–24× the all-sample mean. But the
mechanism is **accuracy, not magnitude**: inside the top decile the model is
almost always right, so capture approaches the mean absolute move there, while
the full sample is diluted by wrong calls. The decile is not finding the big
moves; it is finding the easy ones.

The absolute figures settle it. **The best top-confidence decile anywhere in the
study captures 5.00 bps, against an 80 bps round trip — missing the economic bar
by 16×.** There is no selection filter hiding in the predictions.

A related caution: the probabilities are rank-ordered, not accurate. Worst
calibration gap 0.6086 (Kraken) and 0.4628 (Coinbase), mean Brier 0.163 and
0.181. The model knows which way more often than it knows how sure it is.

### 5. The mechanism: AUC is magnitude-blind

AUC asks one question — do up-moves score higher than down-moves? It never asks
*by how much*. A model that calls the sign of every 0.01 bps flicker while being
useless on the 5 bps moves posts a superb AUC and captures nothing.

The measurement is the Spearman correlation between model confidence
(`|p − 0.5|`) and realised `|move|`. Had that correlation been zero, AUC would
merely be uninformative about size. **It is not zero. It is strongly negative**
— rho ≈ **−0.32** on Kraken and **−0.37** on Coinbase at 100 ms, and most
negative at exactly the horizons where AUC looks best.

Confidence concentrates in the *smallest* moves. The model is surest precisely
where there is least to win. That is a mechanism, not an absence, and it is why
the AUC and the capture can both be honest numbers at the same time.

### 6. The headline number did not survive more data

The hypothesis was originally closed on a different figure: **3.31 bps** gross
capture at 900 s on Coinbase BTC-USD against 80 bps of cost, AUC 0.596, net EV
**−76.69 bps** — a real signal failing the arithmetic by 23×.

That 3.31 bps came from a single day. Across four full days the same measurement
ranges **−2.44 to +3.05 bps**: a draw from a distribution centred near zero, not
a small positive edge. Coinbase's 900 s AUC over the same four days ranges
0.3612 to 0.5931.

This did not reopen the question — it closed it harder. The long-horizon capture
was not merely too small to pay for itself; it was **not reliably positive at
all**. The short-horizon AUC reproduces to 0.0044 and the long-horizon capture
does not reproduce whatsoever, and those are the two ends of the same finding.

### 7. Capacity was not the constraint

Tested once, against a bar written before training: at 900 s, out of sample,
under the same purged CV and embargo, a deep model had to beat the tree by
**AUC + 0.020 AND gross capture + 1.00 bps**. A 2-layer MLP and a single-layer
GRU over a 16-bar window were run on Coinbase BTC-USD, six days, 123,864
samples.

Both scored **below the LightGBM baseline** on both metrics at both 900 s and
1 s — not short of the bar, worse than the baseline. At 900 s both posted AUC
under 0.50 and negative gross capture. The leakage suite passed, and its
planted-future canary reached **AUC 0.9714** on a deliberately planted future
column, so the clean result came from a probe demonstrably capable of firing.

---

## The transfer test: the signal is venue-local microstructure, not information

If the model had learned something about *where bitcoin is going*, that
knowledge should survive a change of venue. It does not.

The identical pipeline was run on **CME micro bitcoin futures (MBT)** —
224,425,675 events over 989 scheduled-open hours across two validated months
(April and May 2026), mbp-10 depth, ordered on `ts_recv`.

| 900 s, maker | round-trip cost | gross capture | AUC | net EV |
|---|---|---|---|---|
| Coinbase BTC-USD | 80.00 bps | 3.31 bps | 0.596 | −76.69 bps |
| **CME MBT** | **5.33 bps** | **0.22 bps** | **0.501** | **−5.11 bps** |

Changing venue cut cost 15×. It cut the gross edge 15× as well. **AUC 0.501 is a
coin flip.** Net EV never crosses zero at any horizon in either cost mode.

Two escape routes were closed. The cross-venue features that ranked near the top
of feature importance were 100% NaN in the CME run — but measured where they
*can* be computed, they are worth **ΔAUC ≤ +0.0044**, immaterial at every
horizon, so their absence did not cause the failure. (Feature importance
measured what the model leaned on, not what it gained — a distinction worth
carrying.) And the one figure clearing rounding noise, +0.215 bps at 900 s,
**reversed to −0.785 bps** on a stride-1 control.

This is the cleanest available evidence that the 0.94 is not information about
price. Same asset, same pipeline, same features, different matching engine — and
the discrimination vanishes. What the model learned is a property of one venue's
book dynamics, and it does not travel.

---

## Scope, stated honestly

Everything above is bounded by what was actually recorded, and the bounds are
narrow enough to matter.

- **Sample window.** The diagnostic rests on **six validated days**,
  2026-07-30 → 2026-08-04, of which two are degraded and named rather than
  averaged in (one has 56 samples from a mid-day recorder start; one is missing
  hours 02–06 on both venues from a host-level outage). The original Phase B
  figures rest on a **single day**, 2026-07-31. The CME leg is two months of one
  contract.
- **One regime.** Six days is not six regimes. The CME window covers BTC running
  65,850 → 83,195 (+26%) with no sustained drawdown: a rising market, sampled
  once — **distinct volatility conditions genuinely covered: one.** Under this
  project's own research-honesty rule, every figure above is pipeline validation
  rather than evidence of a durable edge, and a signal fitted on a few days is
  fitted on those days' regime.
- **The venue set is three books.** Kraken spot, Coinbase Advanced spot, CME
  MBT. Nothing here shows that no edge exists at fee tiers this project cannot
  reach, at latency it does not have, or on instruments it did not survey.
- **Coverage that was not run.** The ETH pair on both spot venues was not run;
  the six-day sweep ran at stride 3, every third retained event bar. CME was not
  re-run after the diagnostic.
- **Independent checking.** An adversarial external audit was performed on this
  repository. It covered a *different* hypothesis chain. Of the closure
  described here it states: *"the Phase-B and detection-track hypotheses (H1,
  H2, H4, H5, H8–H11) could not be independently re-derived within this audit —
  their inputs are not all present in the clone. I read their register entries;
  each cites a measured number and a reopening condition. They are
  **unaudited**, not clean."* **This closure was read, not executed, by the
  external audit**, and under that audit's own labelling convention that is
  worth considerably less than a re-derived result.
- **One interpretation that is not measured here.** A natural microstructure
  reading of §5 is that a direction-trained model is largely learning the
  bid-ask bounce — the most predictable and the smallest component of
  short-horizon price motion. That reading is consistent with every number
  above, but this project did not decompose the signal to test it, and it should
  be read as an unverified interpretation rather than as one of the measured
  findings. What was measured is the magnitude-blindness itself: rho −0.32 to
  −0.37, strongest where AUC is highest.

---

## What outside evidence says

Folded in from an external literature audit of the project's closures, and
reproduced here without extension:

> **Directional prediction (H1, H2) — the order-book-ML literature does not
> reproduce.** Deep-learning limit-order-book predictors overfit the FI-2010
> benchmark and drop sharply on unseen data; DeepLOB's own authors report 62–70%
> on a real one-year LSE set against the benchmark's inflated figure, and
> surveys find "all models exhibit a significant performance drop when exposed
> to new data" ([Prata et al., *Deep limit order book forecasting*, Quant.
> Finance 2025](https://www.tandfonline.com/doi/full/10.1080/14697688.2025.2522911);
> [LOB DL benchmark study, *AI Review*
> 2024](https://link.springer.com/article/10.1007/s10462-024-10715-4)).

Reconciled against this closure: it corroborates that microstructure-ML
directional edges do not generalize, consistent with the AUC 0.501 transfer
failure and with the real-but-tiny spot edge at AUC 0.596. It contradicts no
part of the reopening condition below; it strengthens the prior against
relitigating on a better model.

---

## The registered reopening condition, verbatim

This hypothesis was closed as **cost-bound** — a real signal smaller than the
cost of capturing it — on 2026-08-03, and the condition under which it reopens
was registered with the closure. It is quoted here in full rather than
paraphrased. (The source is a table cell; its one `<br><br>` line break is
rendered below as a paragraph break. The text is otherwise unaltered.)

> A round-trip cost below roughly **3 bps**, i.e. under 1.5 bps per side. On Coinbase that is the 0 bps maker tier requiring **$250M trailing 30-day volume**; on Kraken, the 0 bps maker tier at **$10M**. Neither is reachable at this project's capital. **Reopens on cost, not on modelling** — AUC 0.596 says there is signal there, so a better model is worth building *only after* a venue at that fee level exists. It does not reopen on more data at the same venues.
>
> **C.14 strengthened this closure in three ways.** (1) **The mechanism is named: AUC is magnitude-blind.** Confidence is *anti*-correlated with realised move size — Spearman **rho = −0.32** (Kraken) and **−0.37** (Coinbase) at 100 ms — so the model is surest exactly where there is least to win. (2) **There is no hidden selection filter.** Top-confidence deciles do capture 2–24× the all-sample mean, but through accuracy rather than magnitude, and the best decile in the study captures **5.00 bps against 80 bps** — missing the economic bar by 16×. (3) **Capacity is not the constraint.** An MLP and a GRU both score *worse* than LightGBM on AUC and on capture, at 900 s and at 1 s, with the leakage suite passing and its planted-future canary firing at AUC 0.9714. Reopening now additionally requires the top-confidence decile to clear a round trip somewhere, which it does not.

Note what the condition is scoped to. It is a threshold on **cost**, not an
invitation to try a stronger learner. AUC 0.596 says there is something there;
the deep-learning result says capacity is not what stands between it and a
profit; the cost table says what does.

---

## The claim, restated

An AUC of 0.94 is a real measurement and it means less than it appears to. It
survives replication across days to within 0.0044 and it does not survive
contact with a fee schedule, because the quantity it scores is uncorrelated —
in fact anti-correlated — with the quantity that pays.

A directional result on limit-order-book data is not interpretable without four
numbers reported together:

1. **accuracy** (AUC, hit rate) — how often the sign is right;
2. **gross capture** in basis points per trade — how much the sign is worth;
3. **the round-trip cost floor** at a venue the author can actually reach; and
4. **the confidence-magnitude correlation** — whether the model's certainty
   tracks the size of what it is certain about.

Report the first alone and a null result is indistinguishable from a discovery.
All four were reported here, and they close the question.

---

## Sources

Every figure above traces to a section of this project's `report.md` — or,
where a figure is stated only in the register, to that entry — and to the commit
that produced it. Commits are in `main`.

| figure(s) | `report.md` section | commit |
|---|---|---|
| The whole per-horizon table (AUC 0.9432 / 0.9079 / 0.8876 / 0.8299 / 0.7132 / 0.5401; capture 0.0291 → 0.2093 bps; rho −0.3175 → +0.0606; top-decile 0.0720 → 5.0020 bps; ratios 2.47× → 23.9×); Coinbase rho −0.3665 / −0.3936 / −0.3855 / −0.2987 on AUC 0.8917 → 0.7202; sample counts 165,075 (Kraken), 41,780 (Coinbase), 123,864 (deep, 900 s); six validated days 2026-07-30 → 2026-08-04 at stride 3; the two degraded days (56 samples; hours 02–06 missing); four-day AUC range 0.0044 and 900 s capture −2.44 to +3.05 bps; Coinbase four-day 900 s AUC 0.3612–0.5931; calibration gaps 0.6086 / 0.4628 and mean Brier 0.163 / 0.181; cross-venue ΔAUC ≤ +0.0044; the MLP/GRU bar (+0.020 AUC and +1.00 bps) and both models falling below baseline; canary AUC 0.9714; the "2–24×", "5.00 bps against 80 bps" and "16×" framings | §Stage C.14 — diagnosing the directional prediction failure (2026-08-05) | `ddf525d` (bars pre-registered in `a2d7466`; rho sign gate corrected in `5430eba`) |
| AUC 0.596 @ 900 s and net EV −76.69 bps, Coinbase BTC-USD; the 42-feature / event-bar / horizon setup; the leakage suite | §Phase B research run — 2026-08-02 01:05 UTC | `03c99f9` (research layer in `b9c07a4`; framing in `26d2626`) |
| 3.31 bps gross capture @ 900 s; CME MBT AUC 0.501, 0.22 bps capture, 5.33 bps cost, −5.11 bps net EV, never crossing zero at any horizon in either cost mode; the 15× cost cut matched by a 15× edge cut; the +0.215 → −0.785 bps stride-1 control; BTC 65,850 → 83,195 (+26%) and "distinct volatility conditions genuinely covered: one" | §Stage C.8 — does the Phase B edge transfer to CME? (2026-08-03) | `16b3fa4` |
| CME sample size: 224,425,675 events over 989 scheduled-open hours, two validated MBT months, mbp-10 depth, ordering clock `ts_recv` | `HYPOTHESES.md` §H2 — Transfer of that edge to CME micro futures (**Sample** row; not restated in `report.md`) | `fd18ba2` |
| Hyperliquid maker round trip 3.00 bps (1.5 bps/leg, verified 2026-08-01) | §Stage C.9 — spread-to-cost survey and adverse selection (2026-08-03) | `c74257e` |
| Kraken base tier corrected to 25 bps maker / 50 bps round trip (live schedule, retrieved 2026-08-08); Coinbase Advanced 40 bps maker / 80 bps round trip | `DECISIONS.md` ADR-055; `HYPOTHESES.md` §The measured venue cost landscape | `81e456e` (Kraken tier first corrected in `2299c7f`) |
| The deep-LOB reproducibility citations | `HYPOTHESES.md` §External corroboration (folded in at C.27) | `81e456e` |
| The registered reopening condition, quoted verbatim; the closure date 2026-08-03; the "fails by 23×" framing of the original deciding number | `HYPOTHESES.md` §H1 — Short-horizon directional prediction on crypto spot | `fd18ba2` (C.14 addendum in `ddf525d`) |
| "Unaudited, not clean" scope statement | `AUDIT.md` §C (Priority-three sweep) and §E (Verdict) | `fb296cb` |

The register entry this note summarises is **H1** in `HYPOTHESES.md`; the
transfer result is **H2**. Both are closed. `AUDIT.md` records what has and has
not been independently checked.
