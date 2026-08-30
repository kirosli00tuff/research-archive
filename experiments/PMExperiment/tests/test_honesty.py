"""Honesty tests.

These assert that the repository's scope statement and its power precedent
stay in the documents a reader arrives at first. They are load-bearing: if a
future session removes one of these sentences, the build fails.

A gate that has never failed is not a gate, so each assertion here names a
specific sentence rather than a vague property.
"""

from pathlib import Path

from pmexperiment import admissibility, band

ROOT = Path(__file__).resolve().parent.parent


def _read(name: str) -> str:
    """Read a document with whitespace folded to single spaces.

    Markdown hard-wraps prose, so a sentence that is genuinely present can
    still fail a literal substring match purely because a line break landed
    mid-phrase. Folding whitespace makes these tests assert on content rather
    than on line-wrap accidents. The fix belongs here, in the reader, not in
    rewording the document to satisfy a brittle matcher.
    """
    raw = (ROOT / name).read_text(encoding="utf-8")
    return " ".join(raw.split())


def test_readme_states_it_never_trades() -> None:
    readme = _read("README.md")
    assert "never trades, holds no account, places no order" in readme
    assert "no stage in which one is planned" in readme


def test_readme_states_a_negative_is_valid() -> None:
    readme = _read("README.md")
    assert "A documented negative is a valid and expected outcome" in readme
    assert "BLOCKED" in readme


def test_readme_carries_the_npd_power_precedent_with_its_figures() -> None:
    readme = _read("README.md")
    assert "0.0512" in readme
    assert "0.01 to 0.05" in readme
    assert "415 days" in readme


def test_readme_carries_the_insider_gate_figure() -> None:
    readme = _read("README.md")
    assert "49.35 bp" in readme


def test_readme_states_the_canadian_doubt_rather_than_hiding_it() -> None:
    readme = _read("README.md")
    assert "30-day minimum maturity" in readme
    assert "not reachable from Canada" in readme


def test_claude_md_carries_the_no_first_moment_rule() -> None:
    claude = _read("CLAUDE.md")
    assert "No first moment before the gate" in claude
    assert "counts and dispersion only" in claude


def test_claude_md_forbids_tuning_the_filter() -> None:
    claude = _read("CLAUDE.md")
    assert "Do not tune a filter to increase a sample" in claude


def test_registration_section_zero_is_registered() -> None:
    """Section 0 was committed in Stage A Task 0, before the first request.

    This replaces the inverted scaffold test in the same commit that removed
    the NOT YET REGISTERED banner, exactly as that test's docstring promised.
    """
    reg = _read("REGISTRATION.md")
    assert "NOT YET REGISTERED" not in reg
    assert "Section 0 registered 2026-08-29" in reg
    assert "0.02 to 0.08" in reg
    assert "The split verdict is registered in advance as a finding" in reg
    assert "no cost can be chosen after seeing a result" in reg


def test_env_example_declares_no_credential() -> None:
    env = _read(".env.example")
    assert "=" not in env, "Stage A needs no credential; .env.example stays empty"


def test_hypotheses_register_carries_h1_state() -> None:
    h = _read("HYPOTHESES.md")
    assert "H1 OPEN, registered, PENDING_ACCESS" in h
    assert "Closed before opening" in h


def test_access_verdict_is_recorded_with_its_evidence() -> None:
    """Stage A ended at the access gate; the record must say so plainly."""
    access = _read("docs/ACCESS.md")
    assert "PENDING_ACCESS" in access
    assert "fails closed" in access
    reg = _read("REGISTRATION.md")
    assert "The power gate never fired" in reg
    assert "no statistic relating a price to an outcome exists" in reg.lower()


def test_registration_carries_the_house_section_set() -> None:
    """Sections 0 through 17, with 17 reserved for amendments."""
    reg = (ROOT / "REGISTRATION.md").read_text(encoding="utf-8")
    for n in range(18):
        assert f"## {n}. " in reg, f"REGISTRATION.md is missing section {n}"
    assert "## 17. Amendments" in reg


def test_progress_reserves_entry_zero_for_the_operator_prompt() -> None:
    p = _read("progress.md")
    assert "Entry 0 is reserved" in p
    assert "logged verbatim before any other work" in p


def test_report_claims_nothing_yet() -> None:
    r = _read("report.md")
    assert "No stage has run" in r
    assert "Nothing is claimed here" in r


def test_transfer_is_registered_untested_and_may_not_be_assumed() -> None:
    """Amendment 1's central guard: Polymarket is not evidence about Kalshi."""
    reg = _read("REGISTRATION.md")
    hyp = _read("HYPOTHESES.md")
    assert "Transfer is registered as UNTESTED and may not be assumed" in reg
    assert "AUC 0.501" in reg and "AUC 0.501" in hyp
    assert "UNTESTED. May not be assumed at any point." in hyp


def test_fee_band_arithmetic_and_verdicts_are_registered() -> None:
    reg = _read("REGISTRATION.md")
    assert "$0.02 per contract per side" in reg
    assert "2.0 percentage points" in reg
    assert "4.0 percentage points" in reg
    for verdict in ("BAND-EMPTY", "BAND-NARROW", "BAND-OPEN"):
        assert verdict in reg


def test_gate_order_is_registered_band_before_power() -> None:
    reg = _read("REGISTRATION.md")
    assert "The fee band of Amendment 2 fires first" in reg
    assert "no bucket may be added to it afterwards" in reg


def test_scope_change_did_not_relax_the_no_execution_rule() -> None:
    """Amendment 3 admits a trading question. It must not admit a trade."""
    reg = _read("REGISTRATION.md")
    assert "No stage in this repository places an order" in reg
    assert "The scope guard in `CLAUDE.md` stands" in reg


def test_category_mismatch_is_registered_before_measurement() -> None:
    reg = _read("REGISTRATION.md")
    assert "concentrates in politics and sports" in reg
    assert "cannot later be offered as an explanation" in reg


# --- Stage B: the fee band fired BAND-OPEN on 2026-08-29 ---------------------
#
# These pin the fired verdict and the figures it rests on. Amendment 2 fixes
# the band as computed once, so a later session that wants a different verdict
# needs a numbered amendment carrying new evidence — not an edit here.


def test_band_verdict_and_its_figures_are_recorded() -> None:
    reg = _read("REGISTRATION.md")
    doc = _read("docs/BAND.md")
    hyp = _read("HYPOTHESES.md")
    assert "The fee-versus-edge band, fired 2026-08-29: BAND-OPEN" in reg
    assert "BAND-OPEN" in doc
    assert "BAND-OPEN" in hyp
    for figure in ("5.85 points", "8.00 points", "0.0785"):
        assert figure in reg, f"{figure} left the fired verdict"
    for figure in ("0.0585", "0.0785", "0.0300"):
        assert figure in hyp, f"{figure} left the hypothesis register"
        assert figure in doc, f"{figure} left the band evidence"


def test_the_band_bottom_is_recorded_as_unreachable_everywhere() -> None:
    """The one decisive figure: a 3.0-point floor beneath a 2.0-point edge."""
    reg = _read("REGISTRATION.md")
    assert "0.0300" in reg
    assert "0.0200" in reg
    assert (
        "No FX treatment, no venue price and no exit route reaches the bottom "
        "of the band" in reg
    )


def test_the_unit_determination_survives_in_the_record() -> None:
    """ADR-009: probability points, not percent return, with its derivation."""
    dec = _read("DECISIONS.md")
    doc = _read("docs/BAND.md")
    assert "The band is in probability points" in dec
    assert "return = gap ÷ price" in dec
    assert "absolute probability points, not percent realized return" in doc
    assert "313,972" in doc


def test_the_fx_treatment_binds_at_turnover_one() -> None:
    """Amendment 4: k = 1 binds, k > 1 is reported and never substituted."""
    reg = _read("REGISTRATION.md")
    assert "k = 1 binds" in reg
    assert "never substituted" in reg
    assert "It does not decide the verdict" in reg


def test_band_open_is_never_claimed_as_an_edge() -> None:
    """Cost failing to close a question is not evidence that an edge exists."""
    reg = _read("REGISTRATION.md")
    hyp = _read("HYPOTHESES.md")
    assert "BAND-OPEN is not a finding that an edge exists" in reg
    assert "**not** evidence that a tradeable edge exists" in hyp


def test_the_band_top_is_recorded_as_carrying_no_n() -> None:
    """Standing rule 13, applied to the figure the verdict actually rests on."""
    reg = _read("REGISTRATION.md")
    assert "The band's top carries no n" in reg
    assert "313,972 contract prices on 46,282 contracts" in reg


def test_stage_b_records_that_it_read_no_venue() -> None:
    doc = _read("docs/BAND.md")
    assert "No venue was read" in doc
    assert "Zero dollars spent" in doc


def test_the_surviving_region_is_named_and_closed_to_everything_else() -> None:
    reg = _read("REGISTRATION.md")
    hyp = _read("HYPOTHESES.md")
    assert "the only region the power gate may fire over" in reg
    assert "held to resolution" in reg
    assert "and no other region" in hyp


def test_the_verdict_strings_in_code_match_the_registration() -> None:
    """A verdict the code spells differently from the document is a drift bug."""
    reg = _read("REGISTRATION.md")
    for verdict in band.BandVerdict:
        assert verdict.value in reg


# --- Stage C: Polymarket fired PENDING_ACCESS on 2026-08-30 ------------------
#
# The load-bearing one is the retraction. Amendment 1 moved the whole
# measurement venue on an unmeasured claim about terms; if that retraction ever
# leaves the record, the same mistake is available to be made a third time.


def test_polymarket_access_verdict_is_recorded_with_its_clause() -> None:
    reg = _read("REGISTRATION.md")
    access = _read("docs/ACCESS.md")
    assert "The Polymarket access gate, fired 2026-08-30: PENDING_ACCESS" in reg
    assert "fails closed" in access
    for clause in ("data mining tools, robots, crawlers", "including on-chain"):
        assert clause in reg, f"the deciding clause left the record: {clause}"
        assert clause in access
    assert "2026-08-11" in reg, "the terms' effective date must travel with them"
    assert "59,617" in access, "the size of the document actually read"


def test_amendment_one_premise_is_retracted_not_quietly_dropped() -> None:
    """The stage's real finding: this repository's own unmeasured claim."""
    reg = _read("REGISTRATION.md")
    assert "That claim was never measured" in reg
    assert "Polymarket is the same case as Kalshi, not the opposite one" in reg
    assert "public by construction rather than by permission" in reg, (
        "the retracted claim must stay quoted, not paraphrased away"
    )


def test_the_terms_claim_practice_is_registered() -> None:
    """ADR-012 turns the failure into a rule, or it will simply recur."""
    dec = _read("DECISIONS.md")
    assert (
        "a quoted clause, the document's effective date, and the date it was "
        "fetched" in dec
    )
    hyp = _read("HYPOTHESES.md")
    assert "Keyless is not the same as permitted" in hyp


def test_stage_c_sent_no_market_data_requests() -> None:
    """Reading terms first is what made this possible; it must stay provable."""
    access = _read("docs/ACCESS.md")
    reg = _read("REGISTRATION.md")
    assert "Zero market-data requests were sent" in access
    assert "sent **zero market-data requests**" in reg
    assert "WITHHELD" in reg


def test_the_counterargument_to_the_access_verdict_is_recorded() -> None:
    """A verdict that lists only its supports is not a verdict."""
    reg = _read("REGISTRATION.md")
    assert "recorded rather than suppressed" in reg
    assert (
        "A venue may not be held to a looser reading than another because its "
        "verdict would be more convenient" in reg
    )


def test_volume_floor_cost_in_sample_is_reported_absent_not_zero() -> None:
    """Standing rule 5 applied to a filter that was registered but never ran."""
    p = _read("progress.md")
    assert "Its cost in sample: not measured" in p
    assert "never as zero" in p


def test_transfer_statement_holds_even_with_no_polymarket_result() -> None:
    """Task 4 stands whatever the verdict, so it must not depend on one."""
    p = _read("progress.md")
    r = _read("report.md")
    assert "and nothing whatever about Kalshi" in p
    assert "and nothing whatever about Kalshi" in r
    assert "AUC 0.501" in p


def test_the_gate_did_not_fire_and_both_passes_are_absent() -> None:
    p = _read("progress.md")
    assert "the power gate did not fire" in p
    assert "absent, not zero" in p
    assert "The scope fixed by Stage B was not widened" in p


# --- Stage D: three candidate licences, none PERMITTED — 2026-08-30 ---------
#
# The load-bearing one is the transfer statement. Stage D read licences that
# would, if one had been granted, have put Polymarket-derived records within
# reach — and a licence changes only who may read the records, never which
# venue they describe. If that sentence ever leaves the record, a later session
# has a corpus and no reason left not to call it evidence about Kalshi.


def test_a_dataset_licence_changes_the_permission_never_the_venue() -> None:
    """Task 3's transfer statement, which holds whatever the verdicts were."""
    lic = _read("docs/LICENCES.md")
    assert "A dataset licence changes the permission, never the venue" in lic
    assert (
        "licenses a statement about Polymarket and nothing whatever about Kalshi" in lic
    )
    assert "AUC 0.501" in lic, "the transfer ground must travel with the statement"
    assert "UNTESTED" in lic


def test_no_candidate_returns_permitted_and_each_verdict_is_recorded() -> None:
    """The three verdicts, with the document and date each rests on."""
    lic = _read("docs/LICENCES.md")
    assert "No candidate returns PERMITTED" in lic
    for verdict in admissibility.CandidateVerdict:
        assert verdict.value in lic, f"{verdict.value} left the evidence document"
    assert "2026-08-11" in lic, "candidate 1's effective date must travel with it"
    assert "Last updated on: June 3rd, 2026" in lic, "candidate 3's in-force label"
    assert "cc-by-4.0" in lic, "candidate 2's stated licence"


def test_unmeasured_is_never_written_as_a_synonym_for_prohibited() -> None:
    """The distinction the code enforces must survive in the prose too.

    Collapsing the two is what let a licence read publish PROHIBITED from an
    instrument it had never opened — Amendment 1's error with the sign
    reversed. If this sentence goes, the next session has no reason not to.
    """
    lic = _read("docs/LICENCES.md")
    assert "UNMEASURED is not a synonym for PROHIBITED" in lic
    assert "Amendment 1's error with the sign reversed" in lic
    assert "ADR-012 has no direction-of-travel exemption" in lic


def test_the_kalshi_effective_date_gap_is_recorded_against_our_own_record() -> None:
    """ADR-012 applied to itself. It must keep convicting the record, not others."""
    lic = _read("docs/LICENCES.md")
    dec = _read("DECISIONS.md")
    p = _read("progress.md")
    assert "It met two elements of three" in lic
    assert "overstates it by one element" in dec
    assert "only ever convicts other people's documents is not a procedure" in p


def test_nothing_was_requested_so_nothing_was_refused() -> None:
    """Candidate 1's label must not be readable as a refusal by the venue."""
    lic = _read("docs/LICENCES.md")
    assert "Nothing was requested, so nothing was refused" in lic
    assert "a record that authorization was sought and refused" in lic


def test_the_unread_candidate_space_is_recorded_as_a_limit_on_the_verdict() -> None:
    """A sampled space is not an enumerated one, and the bias has a direction."""
    lic = _read("docs/LICENCES.md")
    p = _read("progress.md")
    assert "the candidate space was sampled, not enumerated" in lic
    assert "is not a proof that no permitted route exists" in lic
    assert "Zenodo" in lic, "the unread deposit family must stay named"
    assert "the power question would still be unanswered" in p


def test_band_open_is_carried_as_a_cost_finding_with_nothing_behind_it() -> None:
    """Task 4's registered consequence, in the words it was registered in."""
    lic = _read("docs/LICENCES.md")
    r = _read("report.md")
    assert "cost finding with no calibration measurement behind it" in lic
    assert "cost finding with **no calibration measurement behind it**" in r
    assert "No fourth venue is proposed" in lic
