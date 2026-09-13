"""The paper margin is inadmissible, pinned against the MEASURED figure.

Stage B pinned this against a synthetic 880.0. That test could pass while never
having seen a real margin. **These pin it against figures the venue actually
returned on 2026-09-03**, so the refusal is demonstrated on the number it would
really be handed.

The distinction matters more here than usual. Every measured paper margin sits
far ABOVE the registered ceiling, so a paper figure promoted into the gate would
produce a confident FAIL. A wrong verdict that points the same way as the truth
is still a wrong verdict, and it is the harder kind to notice.
"""

from __future__ import annotations

import pytest

from mbt.absence import AbsenceReason, Absent
from mbt.figures import Figure
from mbt.gates import (
    GateName,
    GateOutcome,
    PaperFigureInadmissibleError,
    fire,
    require_admissible,
)
from mbt.provenance import Environment, ProvenanceKind
from mbt.registry import MARGIN_CEILING_USD_PER_CONTRACT

#: Measured on this operator's paper session, 2026-09-03, n = 18 previews across
#: 9 listed strikes of the W1E 20261002 series and both rights.
MEASURED_PAPER_MARGINS_USD = (3441.42, 3903.26, 3972.65, 4028.53, 4599.07)


def _paper_margin(value: float) -> Figure:
    return Figure.record(
        name="initial_margin_short_mbt_option",
        value=value,
        unit="USD_per_contract",
        kind=ProvenanceKind.MARGIN,
        environment=Environment.PAPER,
        detail="measured by whatIf preview on a paper session, 2026-09-03",
    )


@pytest.mark.parametrize("value", MEASURED_PAPER_MARGINS_USD)
def test_a_measured_paper_margin_reaching_the_gate_raises(value: float) -> None:
    with pytest.raises(PaperFigureInadmissibleError):
        require_admissible(_paper_margin(value), GateName.MARGIN)


@pytest.mark.parametrize("value", MEASURED_PAPER_MARGINS_USD)
def test_firing_the_margin_gate_from_a_measured_paper_figure_raises(value: float) -> None:
    """The refusal happens at the gate, not merely at an admissibility helper."""
    with pytest.raises(PaperFigureInadmissibleError):
        fire(
            GateName.MARGIN,
            _paper_margin(value),
            ceiling=MARGIN_CEILING_USD_PER_CONTRACT,
            unit="USD_per_contract",
        )


def test_every_measured_paper_margin_sits_above_the_registered_ceiling() -> None:
    """Why promoting one would be dangerous rather than merely irregular.

    A paper figure admitted here would produce a FAIL that happens to point the
    same way the live answer might. A verdict that is right by accident is not a
    result, and the gate refuses it for provenance rather than for its value.
    """
    assert all(v > MARGIN_CEILING_USD_PER_CONTRACT for v in MEASURED_PAPER_MARGINS_USD)


def test_the_margin_gate_stays_absent_with_its_reason() -> None:
    result = fire(
        GateName.MARGIN,
        Absent(AbsenceReason.NO_LIVE_SESSION, "the paper-only clause is in force"),
        ceiling=MARGIN_CEILING_USD_PER_CONTRACT,
        unit="USD_per_contract",
    )
    assert result.outcome is GateOutcome.ABSENT
    assert result.measured is None
    assert "no_live_session" in result.reason
