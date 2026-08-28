"""Every config and threshold field needs a consumption site elsewhere.

Borrowed shape from AiTrader: a config value nothing reads is decoration,
and decoration drifts. The test fails when a field name appears nowhere in
the package or scripts outside its own definition. Stage A.2 extends the
guard to the registered thresholds, which is what makes a registered
number an enforced number.
"""
from dataclasses import fields
from pathlib import Path

from hfexperiment.config import StageAConfig
from hfexperiment.registered import RegisteredThresholds

ROOT = Path(__file__).resolve().parent.parent
SEARCH_DIRS = (ROOT / "src/hfexperiment", ROOT / "scripts")


def corpus_excluding(definition_file: str) -> str:
    sources = []
    for directory in SEARCH_DIRS:
        for path in directory.rglob("*.py"):
            if path.name == definition_file:
                continue
            sources.append(path.read_text())
    return "\n".join(sources)


def test_every_config_field_is_consumed_somewhere() -> None:
    corpus = corpus_excluding("config.py")
    unenforced = [
        f.name for f in fields(StageAConfig) if f.name not in corpus
    ]
    assert not unenforced, (
        f"config fields with no consumption site: {unenforced}"
    )


def test_every_registered_threshold_has_an_enforcement_site() -> None:
    corpus = corpus_excluding("registered.py")
    unenforced = [
        f.name for f in fields(RegisteredThresholds) if f.name not in corpus
    ]
    assert not unenforced, (
        f"registered thresholds with no enforcement site: {unenforced}"
    )
