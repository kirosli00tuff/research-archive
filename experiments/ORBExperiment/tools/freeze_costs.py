"""A.2 TASK 2 — freeze the cost model, hash it, and record the hash."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from orb.costs_registered import (
    MEASURED_AGAINST_CARRIED,
    MEASURED_ON,
    REGISTERED_COST_MODEL,
)
from orb.ledger import AppendOnlyLedger

ROOT = Path(__file__).resolve().parent.parent


def canonical(model: object) -> str:
    def encode(value: object) -> object:
        if dataclasses.is_dataclass(value) and not isinstance(value, type):
            return {
                f.name: encode(getattr(value, f.name))
                for f in dataclasses.fields(value)
            }
        if isinstance(value, tuple | list):
            return [encode(v) for v in value]
        return value

    return json.dumps(encode(model), sort_keys=True, separators=(",", ":"))


def main() -> int:
    payload = canonical(REGISTERED_COST_MODEL)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    ledger = AppendOnlyLedger(ROOT / "data" / "state" / "cost_model.jsonl")
    ledger.append(
        {
            "kind": "cost_model_freeze",
            "sha256": digest,
            "measured_on": MEASURED_ON.isoformat(),
            "canonical_bytes": len(payload),
            "measured_against_carried": {
                k: {"carried": c, "measured": m, "verdict": v}
                for k, (c, m, v) in MEASURED_AGAINST_CARRIED.items()
            },
        }
    )
    latch = ROOT / "data" / "state" / "cost_model_latch.json"
    latch.parent.mkdir(parents=True, exist_ok=True)
    latch.write_text(
        json.dumps(
            {"sha256": digest, "measured_on": MEASURED_ON.isoformat()},
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    print(f"cost model frozen\n  sha256 {digest}\n  latch  {latch}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
