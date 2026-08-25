"""Write the B.2 evaluation report.

This module holds no outcome of its own. It renders what the evaluator returns.
The order is fixed: the validity gate, then the primary contrast, then the
permutation null, then the verdict. Secondaries and descriptives come after the
verdict and never before it, because a reader who meets them first will read the
verdict through them.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import TYPE_CHECKING

from npd.config import CONFIG, Config
from npd.paths import REPORTS

if TYPE_CHECKING:
    from npd.eval.evaluator import B2Result

REGISTERED_PROJECTION = "0.026 to 0.047"


def _pct(x: float) -> str:
    return f"{x:+.4f}"


def write_report(result: B2Result, cfg: Config = CONFIG) -> Path:
    out = REPORTS / "stage_b2"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "evaluation.md"
    lines: list[str] = []
    a = lines.append

    a("# Stage B.2. The one-shot evaluation")
    a("")
    a(f"Run {dt.datetime.now(dt.UTC).isoformat()}. Once.")
    a("")
    a(f"Gate model `{cfg.gate_model}`. Sealed store read one time, by one module.")
    a("")
    a("---")
    a("")

    # ---- Task 1 ----------------------------------------------------------
    a("## Amendment 0, recorded before any outcome was read")
    a("")
    a(f"Operator prior: **{result.amendment_zero_prior}**")
    a("")
    a("The operator adopted the assistant prior of 0.05 rather than forming an")
    a("independent one. The calibration ledger shows it as **adopted, not")
    a("independent**, because an adopted prior carries no information about the")
    a("operator own judgment and would corrupt the calibration record if logged as")
    a("his.")
    a("")
    a("**This experiment yields no evidence about the operator calibration.** One")
    a("prior was recorded, not two.")
    a("")
    a("---")
    a("")

    # ---- Task 2 ----------------------------------------------------------
    g = result.gate
    if g is None:
        raise RuntimeError("the evaluator returned no validity gate result")
    a("## Task 2. The pipeline validity gate")
    a("")
    a("The registered negative control. Stored rankings shuffled within each day,")
    a(f"{g.draws:,} draws, scored against the sealed forward returns.")
    a("")
    a("**This detects pipeline defects, not model contamination.** A non-zero")
    a("shuffled IC means the scorer, the join, or the label mapping is wrong, and")
    a("every downstream number would be an artifact. It is not a contamination")
    a("clearance and a later reader must not read it as one.")
    a("")
    a("| quantity | value |")
    a("|---|---|")
    a(f"| shuffled mean daily rank IC | **{_pct(g.grand_mean)}** |")
    a(f"| Monte Carlo 95 percent interval on that mean | {_pct(g.mc_low)} to {_pct(g.mc_high)} |")
    a(f"| spread of the null distribution, sd | {g.sd:.5f} |")
    a(f"| null distribution 2.5 to 97.5 percentile | {_pct(g.p2_5)} to {_pct(g.p97_5)} |")
    a(f"| registered tolerance | {CONTROL_TOLERANCE_TEXT} |")
    a("")
    if result.gate_passed:
        a("**Gate verdict: PASS.** The shuffled mean sits inside the registered")
        a("tolerance of zero. The scorer, the join, and the label mapping behave as a")
        a("valid pipeline must under randomization, so the numbers below are")
        a("computed on a pipeline that has been shown to produce zero when it should.")
    else:
        a("**Gate verdict: FAIL. Everything stopped here.**")
        a("")
        a(result.stopped_reason)
        _flush(path, lines)
        return path
    a("")
    a("---")
    a("")

    p = result.primary
    n = result.permutation_null
    sec = result.secondary
    if p is None or n is None or sec is None:
        raise RuntimeError("the gate passed but a horizon result is missing")
    # ---- Task 3 ----------------------------------------------------------
    a("## Task 3. The primary contrast")
    a("")
    a(f"Primary horizon, next-{p.horizon}-session return. **{p.n_days} evaluable days.**")
    a(f"{p.n_dropped_incomplete} days dropped because a name in the panel carried no")
    a("realized return. The absence is recorded and the day is dropped, never filled.")
    a("")
    a("### Mean daily rank IC")
    a("")
    a("| series | mean daily rank IC |")
    a("|---|---|")
    a(f"| **model**, `{cfg.gate_model}` | **{_pct(p.model_mean_ic)}** |")
    for name, value in sorted(p.baseline_mean_ic.items(), key=lambda kv: -kv[1]):
        mark = " &larr; best" if name == p.best_baseline else ""
        a(f"| baseline `{name}` | {_pct(value)}{mark} |")
    a("")
    a(f"**Best baseline: `{p.best_baseline}`.** It was designated after the fact, as")
    a("the baseline with the highest mean daily rank IC in the window. Selecting it")
    a("this way is **conservative**, because it picks the hardest of the three")
    a("baselines for the model to clear rather than the easiest. It raises the bar,")
    a("it never lowers it. Recorded as ADR-010.")
    a("")
    a("### The contrast")
    a("")
    a("Model mean daily rank IC minus best-baseline mean daily rank IC.")
    a(f"Day-clustered moving-block bootstrap, {cfg.bootstrap_resamples:,} resamples,")
    a(f"block length {2 * cfg.primary_horizon_sessions}, two-sided at t {cfg.t_critical}.")
    a("")
    a("| quantity | value |")
    a("|---|---|")
    a(f"| **primary contrast** | **{_pct(p.contrast_point)}** |")
    a(f"| interval | {_pct(p.contrast_interval.low)} to {_pct(p.contrast_interval.high)} |")
    a(f"| excludes zero | **{p.contrast_interval.excludes_zero()}** |")
    a(f"| bootstrap standard error | {p.bootstrap_se:.5f} |")
    a(f"| daily contrast sd | {p.contrast_sd_daily:.5f} |")
    a("")
    a("No family correction applies. This is one pre-registered contrast on one")
    a("pre-registered model, and the registration states why: the hypothesis was not")
    a("selected from a sweep. It was written before any output existed.")
    a("")
    a("### Power that actually existed")
    a("")
    a("| quantity | value |")
    a("|---|---|")
    a(f"| achieved effective sample size | **{p.effective_n:.1f}** independent-equivalent days |")
    a(f"| realized minimum detectable contrast | **{p.realized_mde:.4f}** |")
    a(f"| registered projection | {REGISTERED_PROJECTION} |")
    a("")
    a("The result is read against the power that existed, not the power that was")
    a("hoped for.")
    a("")
    a("---")
    a("")

    # ---- Task 4 ----------------------------------------------------------
    a("## Task 4. The permutation null")
    a("")
    a(f"Within-day permutation of the model outputs, {n.draws:,} resamples, drawn")
    a("independently of the gate in Task 2 so the two questions do not share a")
    a("sample.")
    a("")
    a("| quantity | value |")
    a("|---|---|")
    a(f"| observed model mean daily rank IC | **{_pct(p.model_mean_ic)}** |")
    a(f"| null mean | {_pct(n.grand_mean)} |")
    a(f"| null sd | {n.sd:.5f} |")
    a(f"| null 2.5 to 97.5 percentile | {_pct(n.p2_5)} to {_pct(n.p97_5)} |")
    a(f"| **two-sided p** | **{result.permutation_p:.4f}** |")
    a("")
    a("---")
    a("")

    # ---- Task 6, before the secondaries ----------------------------------
    a("## Task 6. The verdict, fired once")
    a("")
    a("| registered row | fired |")
    a("|---|---|")
    a(f"| beats coin and beats every baseline | {'**YES**' if result.c1_authorized else 'no'} |")
    a(
        "| beats coin, does not beat the baselines | "
        f"{'**YES**' if (p.beats_coin and not p.beats_best_baseline) else 'no'} |"
    )
    a(f"| does not beat coin | {'**YES**' if not p.beats_coin else 'no'} |")
    a("")
    a(f"### Verdict: {result.verdict_row}")
    a("")
    a(f"**{result.verdict_text}**")
    a("")
    a("Supporting tests:")
    a("")
    a("| test | result |")
    a("|---|---|")
    a(
        f"| model IC above zero | {_pct(p.model_mean_ic)}, interval "
        f"{_pct(p.model_interval.low)} to {_pct(p.model_interval.high)}, "
        f"significant: **{p.beats_coin}** |"
    )
    a(
        f"| contrast above zero | {_pct(p.contrast_point)}, interval "
        f"{_pct(p.contrast_interval.low)} to {_pct(p.contrast_interval.high)}, "
        f"significant: **{p.beats_best_baseline}** |"
    )
    a("")
    if not p.beats_coin:
        tight = abs(p.model_interval.high) < 0.02 and abs(p.model_interval.low) < 0.02
        a("**Which kind of null is this.** The verdict row is as registered. Read")
        a("descriptively against the realized power:")
        a("")
        if tight:
            a(f"This is a **tight null**. The model IC interval, {_pct(p.model_interval.low)}")
            a(f"to {_pct(p.model_interval.high)}, is narrow enough to exclude effects across")
            a("most of the realistic band 0.01 to 0.05. The sample had the resolution to")
            a("find an effect of the size the literature reports and did not find one.")
        else:
            a("This is an **underpowered unresolved**, not a tight null. The realized")
            a(f"minimum detectable contrast is {p.realized_mde:.4f}, so effects below that")
            a("magnitude were never distinguishable from zero by this design.")
        a("")
        if p.model_mean_ic < 0 and p.model_interval.high < 0:
            a("**The model IC is significantly negative.** The verdict row is unchanged.")
            a("The negative sign is reported here descriptively and is not a separate")
            a("finding, because no registered test asks whether the model ranks worse")
            a("than chance.")
        a("")
    a("### The epistemic boundary, verbatim")
    a("")
    a("> A positive supports the claim the pipeline predicts, never the claim the")
    a("> model understands.")
    a("")
    a("---")
    a("")

    # ---- Task 5, after the verdict ---------------------------------------
    a("## Task 5. Secondaries and descriptives")
    a("")
    a("**Everything in this section is subordinate. None of it changed the verdict")
    a("above and none of it may be read as changing it.**")
    a("")
    a(f"### Secondary horizon, next-{sec.horizon}-session return")
    a("")
    a("| series (SECONDARY) | mean daily rank IC |")
    a("|---|---|")
    a(f"| model, SECONDARY | {_pct(sec.model_mean_ic)} |")
    for name, value in sorted(sec.baseline_mean_ic.items(), key=lambda kv: -kv[1]):
        a(f"| baseline `{name}`, SECONDARY | {_pct(value)} |")
    a("")
    a("| quantity (SECONDARY) | value |")
    a("|---|---|")
    a(f"| evaluable days | {sec.n_days} |")
    a(f"| best baseline | `{sec.best_baseline}` |")
    a(f"| contrast | {_pct(sec.contrast_point)} |")
    a(f"| interval | {_pct(sec.contrast_interval.low)} to {_pct(sec.contrast_interval.high)} |")
    a(f"| excludes zero | {sec.contrast_interval.excludes_zero()} |")
    a(f"| model IC excludes zero | {sec.beats_coin} |")
    a(f"| realized minimum detectable contrast | {sec.realized_mde:.4f} |")
    a("")
    a("### Descriptive. Window halves")
    a("")
    a("Residual knowledge just past a cutoff would show as early-window strength")
    a("decaying later. **This is a diagnostic and not a verdict input.** A difference")
    a("here is a flag for a future registered test, never a finding.")
    a("")
    a("| half | days | model mean daily rank IC |")
    a("|---|---|---|")
    a(f"| first | {result.first_half_days} | {_pct(result.first_half_ic)} |")
    a(f"| second | {result.second_half_days} | {_pct(result.second_half_ic)} |")
    a(
        f"| difference, first minus second | | {_pct(result.first_half_ic - result.second_half_ic)} |"
    )
    a("")
    a("### Descriptive. Model against a coin, independent of the baselines")
    a("")
    a("| quantity | value |")
    a("|---|---|")
    a(f"| model mean daily rank IC | {_pct(p.model_mean_ic)} |")
    a(f"| interval | {_pct(p.model_interval.low)} to {_pct(p.model_interval.high)} |")
    a(f"| beats a coin | **{p.beats_coin}** |")
    a("")
    a("---")
    a("")
    a("## What this evaluation did not do")
    a("")
    a("It read the sealed store one time. It added no horizon, no baseline, no model,")
    a("and no robustness variant that the registration does not already name. It did")
    a("not modify the sealed store, the stored rankings, the frozen prompt digest,")
    a("the baselines, or any registered parameter.")
    a("")
    a("**The limitation carried forward from Amendment 2.** The gate ran at `minimal`")
    a("reasoning effort on the large majority of attempts. Every statement above is a")
    a("statement about gpt-5-2025-08-07 at minimal reasoning effort, not about the")
    a("model at its best.")
    a("")

    _flush(path, lines)
    return path


CONTROL_TOLERANCE_TEXT = "0.02"


def _flush(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
