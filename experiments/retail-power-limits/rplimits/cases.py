"""The extracted evidence: four power cases and three contrast cases.

Nothing here is computed. Every value is a quotation from a closed sibling
repository, carried with the key of the :class:`~rplimits.sources.Source` a
reader can check it against. The type system is doing one job: a figure cannot
enter this file without a source, because the field type is
:class:`Figure` and :class:`Figure` has no default for ``source``.

The ``caveat`` field is load-bearing and is not editorial. Four of the figures
this note was asked to carry are compressed or mis-scoped in the form they were
handed over, and the correction belongs beside the number rather than in a
footnote a later reader will skip.
"""

from __future__ import annotations

from dataclasses import dataclass

from rplimits.sources import SOURCES


@dataclass(frozen=True, slots=True)
class Figure:
    """One quoted value and the source it is quoted from."""

    value: str
    source: str

    def __post_init__(self) -> None:
        if self.source not in SOURCES:
            raise KeyError(f"figure cites an unknown source: {self.source!r}")
        if not self.value.strip():
            raise ValueError("a figure with no value is not a figure")


@dataclass(frozen=True, slots=True)
class PowerCase:
    """One experiment that closed on detectability rather than on a measured null."""

    key: str
    repo: str
    closed: str
    hypothesis: Figure
    effect_band: Figure
    realized_mde: Figure
    sample_achieved: Figure
    sample_required: Figure
    cost: Figure
    closure_language: Figure
    caveat: str

    @property
    def figures(self) -> tuple[Figure, ...]:
        return (
            self.hypothesis,
            self.effect_band,
            self.realized_mde,
            self.sample_achieved,
            self.sample_required,
            self.cost,
            self.closure_language,
        )


@dataclass(frozen=True, slots=True)
class ContrastCase:
    """One closure in the same program that was *not* a power closure."""

    key: str
    repo: str
    closure_type: Figure
    deciding_number: Figure
    why_not_power: str

    @property
    def figures(self) -> tuple[Figure, ...]:
        return (self.closure_type, self.deciding_number)


NPD = PowerCase(
    key="NPD",
    repo="NPDExperiment",
    closed="2026-08-25",
    hypothesis=Figure(
        "Given anonymized per-name numeric feature blocks, a frontier LLM ranks next-window "
        "cross-sectional returns better than cheap mechanical baselines.",
        "npd-registration",
    ),
    effect_band=Figure(
        "Daily rank IC 0.01 to 0.05, the realistic band from the literature, registered in "
        "Section 9.2 before any call went out.",
        "npd-registration",
    ),
    realized_mde=Figure(
        "0.0512 minimum detectable contrast, above the entire 0.01 to 0.05 band, against a "
        "pre-registered projection of 0.026 to 0.047. The realized daily contrast standard "
        "deviation came in at 0.36339 against a registered assumption of at most 0.2626.",
        "npd-progress",
    ),
    sample_achieved=Figure(
        "415 stored daily rankings of 432 eligible window days, 96.1 percent coverage against a "
        "90 percent bar; 404 evaluable days; 125.6 independent-equivalent days after the 3.4 "
        "variance inflation the five-session horizon induces.",
        "npd-progress",
    ),
    sample_required=Figure(
        "Roughly four times the evaluable days, landing near 1,700 trading days of post-cutoff "
        "window. No model has one; the window accrues at about 21 trading days a month.",
        "npd-registration",
    ),
    cost=Figure(
        "6.9378 USD of a 10.00 USD cap across 920 billed gate calls. 411 minutes of recorded "
        "stage time across six stages, of which B.1 collection alone was 194 minutes. One "
        "irrecoverable read of the sealed window.",
        "npd-progress",
    ),
    closure_language=Figure(
        "The numeric-LLM question is unresolved at achievable power. Two serious attempts have "
        "produced zero positives.",
        "npd-registration",
    ),
    caveat=(
        "The phrase carried into InsiderExperiment's Section 0.1 — discovered \"after 415 days "
        'of collection" — means 415 days of *stored rankings*, not 415 days of elapsed '
        "wall-clock. Scaffold, registration, collection, evaluation and closure all ran on "
        "2026-08-25. The elapsed cost was one day; the 415 is the sample."
    ),
)

INSIDER = PowerCase(
    key="Insider",
    repo="InsiderExperiment",
    closed="2026-08-25",
    hypothesis=Figure(
        "Opportunistic and cluster insider purchases, disclosed on Form 4, predict positive "
        "abnormal returns that survive the operator's measured cost band at achievable size.",
        "insider-registration",
    ),
    effect_band=Figure(
        "30 to 40 bp per month decayed gross — Cohen, Malloy and Pomorski's 82 bp per month over "
        "1989 to 2007, decayed 60 to 70 percent on 2008 to 2024 data — and 13.3 to 34.7 bp per "
        "month net at the registered six-month hold.",
        "insider-registration",
    ),
    realized_mde=Figure(
        "49.35 bp per month, above the whole gross band and the whole net band, against a "
        "registered BLOCKED floor of 40 bp committed before the measurement existed. Stable "
        "across Newey-West bandwidths: 50.19 at lag 5, 49.11 at lag 63, 49.53 at lag 126.",
        "insider-gate",
    ),
    sample_achieved=Figure(
        "4,585 qualifying events against a registered floor of 1,000; 2,581 sessions at 99.5 "
        "percent coverage against a floor of 80 percent; 2,869.9 effective independent periods, "
        "which exceeds the raw session count because the variance inflation of 0.899 is below one.",
        "insider-registration",
    ),
    sample_required=Figure(
        "Not a sample requirement. Section 0.4 required about 23 effective names to stay out of "
        "BLOCKED; the value-weighted book held 71.9 names behaving like 29.7 effective names, top "
        "name 14.9 percent and top five 33.8 percent. The 9.993 percent annualized tracking error "
        "is the whole of the 49.35.",
        "insider-registration",
    ),
    cost=Figure(
        "Zero dollars. No paid API was used. 214 wire requests totalling 2.78 GB with zero "
        "non-200 responses. About 51 minutes for Stage A.1 and 20 for Z.1 by the commit record. "
        "The realized alpha was never read and sits sealed.",
        "insider-registration",
    ),
    closure_language=Figure(
        "The registered primary design cannot resolve the effect at achievable power. The minimum "
        "detectable effect is 49.35 bp per month against a registered BLOCKED floor of 40 and "
        "against a decayed literature band of 30 to 40 bp per month gross and 13 to 35 bp per "
        "month net at the six-month hold. Stage B is never written. The repo closes on the finding.",
        "insider-registration",
    ),
    caveat=(
        "The corpus is explicitly not the cause: it cleared its floor by a factor of four and a "
        "half. The finding is also scoped by universe — 94.2 percent of qualifying-shaped insider "
        "purchases happen outside the liquid-500 band this design could trade — so it does not "
        "refute the literature it tested against."
    ),
)

ETF = PowerCase(
    key="ETF",
    repo="ETFExperiment",
    closed="2026-08-28",
    hypothesis=Figure(
        "US spot Bitcoin ETF net flow prints predict the next day's BTC return, out of sample, by "
        "enough to clear a round trip on Hyperliquid perps.",
        "etf-readme",
    ),
    effect_band=Figure(
        "Rank correlation 0.09 registered, against a published magnitude of 0.18; powers were "
        "also computed at a quartered 0.045 and reported beside the registered figure.",
        "etf-registration",
    ),
    realized_mde=Figure(
        "Expressed as a required N rather than an effect size. E1 needs 237 admissible days at "
        "the published 0.18 and 845 at the registered 0.09; E2 needs 300 at 0.18 and above 1,200 "
        "at 0.09. Section 10 requires both co-primaries, so the governing minimum is 300 at the "
        "published magnitude and above 1,200 at the registered one.",
        "etf-registration",
    ),
    sample_achieved=Figure(
        "11 admissible days at closure, from a 336-row census — 53 capture-too-late, 243 "
        "no-capture, 25 capture-served-no-value, 3 no-printed-value, 1 archive-fetch-failed. "
        "163 projected at the registered 2027-03-31 deadline at the measured forward accrual of "
        "20.8 admissible days per month.",
        "etf-registration",
    ),
    sample_required=Figure(
        "300 governing at the published magnitude, above 1,200 at the registered one. The "
        "shortfall at the deadline is 137 days against the governing figure, and 74 days against "
        "E1's 237, the most favourable figure anywhere on the record.",
        "etf-registration",
    ),
    cost=Figure(
        "Zero dollars, no capital and no credential at any point. 220 charged requests over the "
        "repository's lifetime. No outcome value was ever read.",
        "etf-registration",
    ),
    closure_language=Figure(
        "H1 closes at untestable-at-achievable-power. The registered design cannot resolve the "
        "effect at the sample size reachable by the registered deadline of 2027-03-31. The signal "
        "was never read and this closure is not evidence about it.",
        "etf-close",
    ),
    caveat=(
        "The 845 / above-1,200 / about-302 triple is real but does not belong to the closure "
        "firing. Those are Amendment 6's numbers for what fourteen further months of forward "
        "collection would buy: about 302 admissible days by 2027-10-31, which clears the "
        "governing 300 at the published 0.18 by two days and clears nothing at the registered "
        "0.09. The closure itself fired on 163 projected against 300 governing at the "
        "2027-03-31 deadline."
    ),
)

HF = PowerCase(
    key="HF",
    repo="HFExperiment",
    closed="2026-08-26",
    hypothesis=Figure(
        "The equal-weighted top five names by 12-1 momentum with a skip month in the U-LIQ-500 "
        "universe, re-formed on the first trading session of each month, earn positive daily "
        "excess return over the equal-weighted universe.",
        "hf-registration",
    ),
    effect_band=Figure(
        "27.99 bp per day, measured on the already-spent AiTrader holdout, against daily noise "
        "near 418 bp implied by 66.4 percent annualized tracking error. The band is the "
        "measurement, not a literature range: this design tested its own prior estimate.",
        "hf-registration",
    ),
    realized_mde=Figure(
        "z 1.668 against a corrected bar of 2.50 over a 2.55-year holdout, interval -4.9 to "
        "+60.9. Clearing the bar needed 104.0 percent per year of excess; the book delivered "
        "70.5, a shortfall of 1.5x. Widening 5 names to 50 halves tracking error (66.4 to 31.7 "
        "percent) and cuts excess proportionally (27.99 to 10.04 bp per day), so z moves only "
        "1.668 to 1.455 and neither width clears.",
        "aitrader-return",
    ),
    sample_achieved=Figure(
        "One 2.55-year holdout, touched once at commit a0a9ef6. Zero forward shadow observations: "
        "the series was disarmed before its first accrual and the verdict was never computed.",
        "hf-progress",
    ),
    sample_required=Figure(
        "Under the frozen confidence sequence, with the sample mean holding at 27.99 bp per day, "
        "the lower bound clears zero at day 2,061 and clears the measured 4.07 bp per day cost "
        "hurdle at day 2,852. Eight to eleven years.",
        "hf-registration",
    ),
    cost=Figure(
        "Zero dollars deployed and zero capital; the live track was never funded. The cost already "
        "sunk is the 2.55-year holdout, spent once and not repeatable, plus four stages of "
        "instrument build across 2026-08-23 to 2026-08-25.",
        "hf-progress",
    ),
    closure_language=Figure(
        "H-F is 12-1 cross-sectional momentum, tested once in the AiTrader cross-sectional round "
        "of 2026-07-26 and resolved on statistical power rather than absent signal.",
        "hf-readme",
    ),
    caveat=(
        "HFExperiment is a power case by inheritance and by its own registered forward "
        "arithmetic, not by a power gate firing inside it. Its own Section 0 fired BLOCKED on the "
        "*broker* — IBKR refused fractional quantities through the API, errors 10243 and 10244 — "
        "and the repository then closed by operator decision on 2026-08-26 with the shadow series "
        "never started. The power resolution belongs to the AiTrader round of 2026-07-26, which "
        "HFExperiment's README states in its first sentence and its Section 11 prices at eight to "
        "eleven years."
    ),
)

POWER_CASES: tuple[PowerCase, ...] = (NPD, INSIDER, ETF, HF)


MLCRYPTO = ContrastCase(
    key="MLCryptoEngine",
    repo="MLCryptoEngine",
    closure_type=Figure(
        "Eleven hypotheses, nine tested and closed, and not one closed on power. The register's "
        "own two-way split is cost-bound versus signal-absent: H1 and H3 cost-bound, H2 and H4 "
        "signal-absent, H5 decayed, H8 signal present and cancelled by its own hedge, H9 "
        "insignificant after deflation, H10 unidentifiable in available data, H11 failing all six "
        "registered bars, H7 closed by decision, H6 negative under an order-lifecycle fill model.",
        "mlc-hypotheses",
    ),
    deciding_number=Figure(
        "A short-horizon model scored AUC 0.9432 at 100 ms and captured 0.0291 bps per trade on "
        "Kraken BTC/USD, which charges 50 bps round trip — a miss of roughly 1,700x. Against the "
        "cheapest venue reachable from the operator's jurisdiction at all, Hyperliquid at 3 bps, "
        "it still misses by roughly 100x. Separately, H4 cointegration break-even transaction "
        "costs ran 300 to 550 bps against that same 3 bps actual, a margin of 100 to 180x.",
        "mlc-h1note",
    ),
    why_not_power=(
        "The samples were large and the discrimination was real. AUC 0.94 is not an underpowered "
        "measurement; it is a well-measured quantity that turns out not to be the quantity that "
        "pays. These closures reopen on a fee schedule or not at all, and the register says so in "
        "the field it calls 'what would reopen it'."
    ),
)

SOLATTN = ContrastCase(
    key="solattn",
    repo="solattn",
    closure_type=Figure(
        "A powered null. Kill criterion K1 fired at 100.0 percent outcome coverage on every "
        "analysed cohort, and all 120 computable cells carry a negative point lift with none "
        "positive at any significance level.",
        "solattn-findings",
    ),
    deciding_number=Figure(
        "Primary trial lift −1.0779 net of the central 450 bps cost band, 95 percent "
        "day-clustered bootstrap interval [−3.3354, +0.0204], n = 12,798 amm pools over three "
        "birth days, 2,107 measurable at the d0+2 anchor, Q5 cell n = 412.",
        "solattn-findings",
    ),
    why_not_power=(
        "The design measured what it set out to measure, at full outcome coverage, and the answer "
        "was no. This is what a closure looks like when detectability is not the binding term, and "
        "it is the reason the four power cases cannot be read as though every negative in this "
        "program were a power negative."
    ),
)

SOLCLEAR = ContrastCase(
    key="solclear",
    repo="solclear",
    closure_type=Figure(
        "Mixed, and the earliest power-shaped refusal in the program. The Stage E outcome study "
        "fired a registered underpowered rule — 18 cleared against a floor of 20 at 30 days, and "
        "4 at 90 days — so no significance was claimed in either direction. Its other closures "
        "are selection and cost: the confirming measurement is priced out at 4,695,489 weighted "
        "credits, 37.6x the stale 124,764 estimate.",
        "solclear-findings",
    ),
    deciding_number=Figure(
        "Every one of the 18 cleared pools realized −100 percent net at 30 days, and all 4 with a "
        "realized 90-day horizon did the same; share ever above entry 0 percent of 18. Separately, "
        "the transferable result: archived-page sampling manufactures survivorship by 60 points at "
        "30 days and 79 at 90, 97.5 percent death on 40 birth-ordered pools against 18.75 percent "
        "on 16 attention-crawled ones.",
        "solclear-findings",
    ),
    why_not_power=(
        "solclear matters here for the date rather than the type. Its underpowered rule was "
        "registered before the measurement and fired on 2026-08-14, eleven days before "
        "NPDExperiment. So the ingredient existed already; what it did was refuse an inference "
        "after the measurement had been made, not refuse the measurement."
    ),
)

CONTRAST_CASES: tuple[ContrastCase, ...] = (MLCRYPTO, SOLATTN, SOLCLEAR)


@dataclass(frozen=True, slots=True)
class Headline:
    """The one-line compression of a power case, for the note's summary table.

    Each field compresses a :class:`Figure` recorded above; ``source`` names
    where the compressed values are checkable. ``tests/test_cases.py`` asserts
    that every :class:`PowerCase` has exactly one headline and no headline is
    orphaned, so the table cannot drift out of step with the record.
    """

    case: str
    band: str
    detectability: str
    verdict: str
    source: str

    def __post_init__(self) -> None:
        if self.source not in SOURCES:
            raise KeyError(f"headline cites an unknown source: {self.source!r}")


HEADLINES: tuple[Headline, ...] = (
    Headline(
        case="NPDExperiment",
        band="daily rank IC 0.01 to 0.05",
        detectability="realized MDE **0.0512** — above the whole band",
        verdict="unresolved at achievable power",
        source="npd-registration",
    ),
    Headline(
        case="InsiderExperiment",
        band="30 to 40 bp/month gross; 13.3 to 34.7 net",
        detectability="realized MDE **49.35 bp/month** — above both bands",
        verdict="BLOCKED on the power gate, verdict row V7",
        source="insider-gate",
    ),
    Headline(
        case="ETFExperiment",
        band="rank correlation 0.09 registered, 0.18 published",
        detectability="needs **N = 300** governing; **163** projected at the deadline",
        verdict="untestable at achievable power",
        source="etf-registration",
    ),
    Headline(
        case="HFExperiment",
        band="27.99 bp/day against ~418 bp/day of noise",
        detectability="**z 1.668** against a 2.50 bar; needed 104.0 %/yr of excess, delivered 70.5",
        verdict="resolved on statistical power, not absent signal",
        source="aitrader-return",
    ),
)
