"""Every config field must have a consumption site outside config.py.

Borrowed shape from AiTrader: a config value nothing reads is decoration,
and decoration drifts. The test fails when a field name appears nowhere in
the package or scripts outside its own definition.
"""
from dataclasses import fields
from pathlib import Path

from hfexperiment.config import StageAConfig

ROOT = Path(__file__).resolve().parent.parent
SEARCH_DIRS = (ROOT / "src/hfexperiment", ROOT / "scripts")


def test_every_config_field_is_consumed_somewhere() -> None:
    sources = []
    for directory in SEARCH_DIRS:
        for path in directory.rglob("*.py"):
            if path.name == "config.py":
                continue
            sources.append(path.read_text())
    corpus = "\n".join(sources)
    unenforced = [
        f.name for f in fields(StageAConfig) if f.name not in corpus
    ]
    assert not unenforced, (
        f"config fields with no consumption site: {unenforced}"
    )
