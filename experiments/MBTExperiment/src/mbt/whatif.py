"""The what-if margin read, and the known-answer test that must precede it.

**A new path reproduces a previously measured answer before its output is
trusted.** Before any MBT margin figure is believed, the same code path runs
against a liquid product whose margin is independently checkable, and the
comparison is recorded. A pipeline that has only ever been pointed at the
instrument it was built for has never been checked against anything.

**Where the known answer comes from, and where it does not.** CME refused
automated access to its margin schedule, citing its own Data Terms of Use, and
that refusal was obeyed by VRPExperiment and is obeyed here. The expected value
is therefore an **operator input**, read by a person from the IBKR client portal
or CME's published schedule, and supplied through the environment. This
repository does not scrape it, does not infer it from a third party, and does not
carry one from another repository. With no operator value supplied, the check
records :class:`Absent` and the MBT output stays untrusted.

**Nothing produced here is admissible to any gate.** Every figure carries the
environment measured from the connected account, and :mod:`mbt.gates` refuses a
paper-tagged margin. That refusal is pinned by test.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from mbt.absence import AbsenceReason, Absent, Maybe
from mbt.broker import MarginPreview, is_unset
from mbt.clock import iso_utc, utc_now
from mbt.figures import Figure
from mbt.provenance import Environment, ProvenanceKind


@final
@dataclass(frozen=True, slots=True)
class KnownAnswerCheck:
    """One comparison of a measured margin against an independently known one."""

    product: str
    expected: Maybe[float]
    measured: Maybe[float]
    tolerance_fraction: float
    agrees: bool
    source_of_expected: str
    detail: str
    checked_at: str

    def as_row(self) -> dict[str, object]:
        return {
            "product": self.product,
            "expected": self.expected.as_row()
            if isinstance(self.expected, Absent)
            else self.expected,
            "measured": self.measured.as_row()
            if isinstance(self.measured, Absent)
            else self.measured,
            "tolerance_fraction": self.tolerance_fraction,
            "agrees": self.agrees,
            "source_of_expected": self.source_of_expected,
            "detail": self.detail,
            "checked_at": self.checked_at,
        }


def margin_from_preview(preview: MarginPreview) -> Maybe[float]:
    """Read the initial margin change off a preview, refusing IBKR's sentinel.

    IBKR serves ``1.7976931348623157E308`` for "not computed". Parsing it to a
    float would produce a finite-looking 1e308 that a later comparison would
    treat as an enormous but real margin, and every ceiling test would fail for
    the wrong reason.
    """
    if is_unset(preview.init_margin_change):
        return Absent(
            AbsenceReason.NOT_SERVED,
            "the what-if response carried IBKR's not-computed sentinel for "
            "initMarginChange. A sentinel is not a margin and is never parsed "
            "into one.",
        )
    try:
        return float(preview.init_margin_change)
    except ValueError:
        return Absent(
            AbsenceReason.NOT_SERVED,
            f"initMarginChange {preview.init_margin_change!r} did not parse as a "
            "number and is recorded absent rather than coerced.",
        )


def known_answer_check(
    *,
    product: str,
    expected: Maybe[float],
    preview: MarginPreview,
    tolerance_fraction: float = 0.10,
    source_of_expected: str,
) -> KnownAnswerCheck:
    """Compare a measured margin against an operator-supplied known answer."""
    measured = margin_from_preview(preview)
    stamp = iso_utc(utc_now(), "known_answer_check")

    if isinstance(expected, Absent):
        return KnownAnswerCheck(
            product=product,
            expected=expected,
            measured=measured,
            tolerance_fraction=tolerance_fraction,
            agrees=False,
            source_of_expected=source_of_expected,
            detail=(
                "no operator-supplied expected margin, so the code path has not "
                "been checked against a known answer and its MBT output is not "
                "trusted. This is an absence, not a pass."
            ),
            checked_at=stamp,
        )
    if isinstance(measured, Absent):
        return KnownAnswerCheck(
            product=product,
            expected=expected,
            measured=measured,
            tolerance_fraction=tolerance_fraction,
            agrees=False,
            source_of_expected=source_of_expected,
            detail=f"the preview served no usable margin: {measured.detail}",
            checked_at=stamp,
        )

    magnitude = abs(measured)
    reference = abs(expected)
    agrees = reference > 0 and abs(magnitude - reference) <= tolerance_fraction * reference
    return KnownAnswerCheck(
        product=product,
        expected=expected,
        measured=measured,
        tolerance_fraction=tolerance_fraction,
        agrees=agrees,
        source_of_expected=source_of_expected,
        detail=(
            f"measured {magnitude} against a known {reference}, a relative "
            f"difference of {abs(magnitude - reference) / reference:.4f} against a "
            f"tolerance of {tolerance_fraction:.4f}"
            if reference > 0
            else "the known answer was not positive, so no comparison was made"
        ),
        checked_at=stamp,
    )


def margin_figure(preview: MarginPreview, environment: Environment) -> Maybe[Figure]:
    """Turn a preview into a tagged figure, or record why it is not one.

    The environment is the one measured from the connected account, passed in by
    the caller that built :class:`SessionProvenance`. There is no path here that
    reads it from configuration.
    """
    measured = margin_from_preview(preview)
    if isinstance(measured, Absent):
        return measured
    return Figure.record(
        name="initial_margin_short_mbt_option",
        value=abs(measured),
        unit="USD_per_contract",
        kind=ProvenanceKind.MARGIN,
        environment=environment,
        detail=(
            "initMarginChange from a whatIf preview. A margin is a property of "
            "the ACCOUNT, so a paper one is development evidence and is refused "
            "by every gate."
        ),
    )
