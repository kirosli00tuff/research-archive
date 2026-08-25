"""The frozen prompt. Built once, hashed, and never edited after B.0b.

The hash is recorded in reports/stage_b0b/mock_run.md and every B.3 replay uses
the same bytes. A prompt that drifts between models turns a replay into a new
experiment.

Nothing identifying reaches this text. No ticker, no date, no absolute price, no
market-level value. tests/test_anonymization.py fails if a real symbol string
appears in a built prompt.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass

from npd.config import CONFIG, Config

SYSTEM = (
    "You rank assets by expected relative future return.\n"
    "You receive a table of anonymized rows. Each row is one asset, identified only "
    "by a random label. Every column is a numeric feature already standardized across "
    "the rows in this table, so a value of 0.00 is the table average and 1.00 is one "
    "standard deviation above it.\n"
    "Return a ranking of every label, best expected relative future return first, "
    "worst last.\n"
    "Reply with JSON only, in exactly this shape:\n"
    '{"ranking": ["<label>", "<label>", ...]}\n'
    "The ranking must contain every label exactly once and nothing else. "
    "Do not include commentary, reasoning, or any field other than ranking."
)

COLUMN_HELP = {
    "ret_1": "return over the last 1 session",
    "ret_5": "return over the last 5 sessions",
    "ret_10": "return over the last 10 sessions",
    "ret_20": "return over the last 20 sessions",
    "ret_60": "return over the last 60 sessions",
    "rvol_20": "realized volatility over 20 sessions",
    "rvol_60": "realized volatility over 60 sessions",
    "dvol_z_60": "dollar volume relative to its own last 60 sessions",
    "vtrend_5_60": "mean volume over 5 sessions divided by mean volume over 60",
}


@dataclass(frozen=True, slots=True)
class Prompt:
    system: str
    user: str
    labels: tuple[str, ...]

    @property
    def digest(self) -> str:
        return hashlib.sha256((self.system + "\x00" + self.user).encode()).hexdigest()


def template_digest(cfg: Config = CONFIG) -> str:
    """Hash of the invariant parts. Changes only when the template changes."""
    payload = SYSTEM + "\x00" + "\x00".join(f"{n}:{COLUMN_HELP[n]}" for n in cfg.feature_names)
    return hashlib.sha256(payload.encode()).hexdigest()


def build(
    labels: Sequence[str],
    z_by_label: dict[str, dict[str, float]],
    cfg: Config = CONFIG,
) -> Prompt:
    """Render one call.

    `labels` is the presentation order, already shuffled by npd.data.anonymize,
    so row position carries no information.
    """
    if len(labels) != cfg.panel_size:
        raise ValueError(f"expected {cfg.panel_size} rows, got {len(labels)}")
    names = list(cfg.feature_names)

    legend = "\n".join(f"  {n}  {COLUMN_HELP[n]}" for n in names)
    header = "label  " + "  ".join(names)
    rows = []
    for lab in labels:
        block = z_by_label[lab]
        rows.append(lab + "  " + "  ".join(f"{block[n]:+.2f}" for n in names))

    user = (
        f"Columns:\n{legend}\n\n"
        f"{len(labels)} rows:\n{header}\n" + "\n".join(rows) + "\n\n"
        "Rank every label, best expected relative future return first. JSON only."
    )
    return Prompt(system=SYSTEM, user=user, labels=tuple(labels))
