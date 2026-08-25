"""The one pre-registered calibration call. Runs before B.1, excluded from the sample.

REGISTRATION.md Section 12.2 permits exactly this call and states what it is for:

  1. confirm which request parameters the endpoint accepts, including whether
     temperature is accepted for this reasoning model
  2. measure actual tokens per call

It then applies the registered decision rule. reasoning_effort takes the highest
value in (low, minimal) whose calibrated projected total spend is at most 80
percent of the remaining cap. If neither qualifies, B.1 does not start.

The call uses a real window panel so the token count is real. Its evidence row is
keyed to the sentinel date `calibration`, never to the window day that supplied
the panel, so the resume logic cannot mistake it for a collected day and the
sample stays clean.

The API key is read from .env and is never printed, logged, or echoed.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from npd.callstate import CallState  # noqa: E402
from npd.collect import prompt as prompt_mod  # noqa: E402
from npd.collect.adapter import (  # noqa: E402
    AuthFault,
    OpenAIAdapter,
    QuotaExhausted,
    TransientFault,
    UnparseableResponse,
    UnsupportedParameter,
)
from npd.collect.collector import load_day  # noqa: E402
from npd.config import CONFIG  # noqa: E402
from npd.data.store import open_store  # noqa: E402
from npd.ledger.evidence import EvidenceLedger  # noqa: E402
from npd.ledger.spend import SpendLedger, cost_of  # noqa: E402
from npd.window import derive_window  # noqa: E402

CALIBRATION_DATE = "calibration"
SAFETY_FRACTION = 0.80
EFFORT_ORDER = ("low", "minimal")


def load_env() -> None:
    """Read .env into the environment. The value is never printed."""
    from npd.env import load_env as _load

    if not _load():
        raise SystemExit(".env is missing")


def main() -> int:
    effort = CONFIG.reasoning_effort
    for i, arg in enumerate(sys.argv):
        if arg == "--effort" and i + 1 < len(sys.argv):
            effort = sys.argv[i + 1]
    cfg = dataclasses.replace(CONFIG, reasoning_effort=effort)
    load_env()
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set")

    with open_store() as con:
        sess = [r[0] for r in con.execute("SELECT date FROM session ORDER BY idx")]
        window = derive_window([dt.date.fromisoformat(d) for d in sess])
        sample_day = window.sessions[0].isoformat()
        payload = load_day(con, sample_day)
    if payload is None:
        raise SystemExit(f"the store cannot serve {sample_day}")

    built = prompt_mod.build(payload.labels, payload.z_by_label)
    spend = SpendLedger()
    evidence = EvidenceLedger()

    results: dict[str, object] = {
        "panel_from": sample_day,
        "prompt_template_digest": prompt_mod.template_digest(),
        "prompt_chars": len(built.system) + len(built.user),
        "model": cfg.gate_model,
        "reasoning_effort": effort,
    }

    adapter = OpenAIAdapter(cfg)
    temperature_accepted = True
    answer = None
    detail = ""
    for attempt in (1, 2):
        try:
            answer = adapter.rank(built)
            break
        except UnsupportedParameter as exc:
            temperature_accepted = False
            detail = str(exc)[:300]
            adapter.disable_temperature()
            continue
        except QuotaExhausted as exc:
            results["outcome"] = "quota_exhausted"
            results["detail"] = str(exc)
            evidence.record(
                date=CALIBRATION_DATE,
                state=CallState.NO_DATA,
                model=CONFIG.gate_model,
                attempt=attempt,
                detail=f"insufficient_quota during calibration: {exc}",
            )
            print(json.dumps(results, indent=2))
            return 2
        except AuthFault as exc:
            results["outcome"] = "auth_fault"
            results["detail"] = str(exc)
            print(json.dumps(results, indent=2))
            return 3
        except (TransientFault, UnparseableResponse) as exc:
            results["outcome"] = "failed"
            results["detail"] = f"{type(exc).__name__}: {exc}"
            evidence.record(
                date=CALIBRATION_DATE,
                state=CallState.MODEL_FAILED,
                model=CONFIG.gate_model,
                attempt=attempt,
                detail=str(exc)[:500],
            )
            print(json.dumps(results, indent=2))
            return 4

    if answer is None:
        results["outcome"] = "failed"
        print(json.dumps(results, indent=2))
        return 4

    cost = cost_of(
        answer.usage.input_tokens, answer.usage.cached_input_tokens, answer.usage.output_tokens, cfg
    )
    spend.record(
        date=CALIBRATION_DATE,
        kind="calibration",
        input_tokens=answer.usage.input_tokens,
        cached_input_tokens=answer.usage.cached_input_tokens,
        output_tokens=answer.usage.output_tokens,
        note=f"panel from {sample_day}, reasoning_effort={effort}, "
        f"temperature_accepted={temperature_accepted}",
    )
    evidence.record(
        date=CALIBRATION_DATE,
        state=CallState.STORED,
        model=CONFIG.gate_model,
        attempt=1,
        input_tokens=answer.usage.input_tokens,
        cached_input_tokens=answer.usage.cached_input_tokens,
        output_tokens=answer.usage.output_tokens,
        reasoning_tokens=answer.usage.reasoning_tokens,
        cost_usd=cost,
        latency_s=answer.latency_s,
        raw_response=answer.raw,
        detail=f"calibration, panel from {sample_day}, excluded from the sample",
    )

    n_days = window.n_days
    remaining = CONFIG.spend_cap_usd - spend.total_usd()
    projected = n_days * cost

    results.update(
        {
            "outcome": "ok",
            "temperature_accepted": temperature_accepted,
            "temperature_detail": detail,
            "reasoning_effort_used": effort,
            "input_tokens": answer.usage.input_tokens,
            "cached_input_tokens": answer.usage.cached_input_tokens,
            "output_tokens": answer.usage.output_tokens,
            "reasoning_tokens": answer.usage.reasoning_tokens,
            "latency_s": round(answer.latency_s, 2),
            "cost_per_call_usd": round(cost, 6),
            "window_days": n_days,
            "projected_total_usd": round(projected, 4),
            "remaining_cap_usd": round(remaining, 4),
            "safety_budget_usd": round(SAFETY_FRACTION * remaining, 4),
            "registered_estimate_usd": round(cost_of(1600, 0, 1150, cfg), 6),
            "ranking_parsed": len(answer.ranking) == CONFIG.panel_size,
        }
    )
    results["decision_rule"] = (
        f"reasoning_effort {effort} is admissible when "
        f"{projected:.4f} <= {SAFETY_FRACTION * remaining:.4f}"
    )
    results["clears_safety_budget"] = projected <= SAFETY_FRACTION * remaining

    out = ROOT / "reports" / "stage_b1"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"calibration_{effort}.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
