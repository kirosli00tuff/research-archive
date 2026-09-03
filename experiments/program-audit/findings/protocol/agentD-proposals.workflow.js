export const meta = {
  name: 'agentD-proposals',
  description: 'Agent D forward proposals: reconstruct the constraint set from the repositories (D1), method improvements grounded in frozen findings (D2), new hypotheses screened against duplication/venue/affordability/power gates (D3), the exhaustion verdict (D4), RECOMMENDATION.md (D5)',
  phases: [
    { title: 'D1 Constraints', detail: 'per-repository extraction, then a merger' },
    { title: 'D2 Method', detail: 'three independent proposers by angle, then a ranker' },
    { title: 'D3 Hypotheses', detail: 'five generators by angle, independent screeners per candidate' },
    { title: 'D4-D5 Verdict', detail: 'exhaustion verdict, recommendation, Phase 3 notes on findings' },
  ],
}

const RULES_PATH = '/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/COMMON_RULES.md'
const SNAP = '/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/snap'
const F = '/home/kiros-li/Documents/GitHub/program-audit/findings'
const OUT = '/home/kiros-li/Documents/GitHub/program-audit/proposals'
const REPOS = ['retail-power-limits','HFExperiment','InsiderExperiment','NPDExperiment','VRPExperiment','ETFExperiment','solclear','PMExperiment','solattn','NPLExperiment','MLCryptoEngine','ORBExperiment','AiTrader']
const BATCH = 3

const ROLE = `
YOU ARE AGENT D. You author forward proposals. You wrote none of the findings and you may not
revise any of them: findings/agentA, agentB, agentC and SUMMARY.md are frozen at the git tag
findings-frozen. If you believe a finding is wrong, record that in ${OUT}/PHASE3_NOTES_ON_FINDINGS.md
(finding ID, what you think is wrong, evidence) and never edit Phase 2. You read the audited
repositories (snapshots under ${SNAP}/, live git and untracked data read-only per the rules) and
the frozen findings (${F}/SUMMARY.md, ${F}/agentC/adjudication/, ${F}/agentA, agentB, agentC
including seeded/). Output only under ${OUT}/. A cheap venue is a necessary condition for a
hypothesis and never a reason for it. A recommendation to open nothing is a complete answer.
`

const D1_SCHEMA = { type: 'object', properties: { repo: { type: 'string' }, venues: { type: 'integer' }, costs: { type: 'integer' }, data_sources: { type: 'integer' }, hypotheses: { type: 'integer' }, notes: { type: 'string' } }, required: ['repo','venues','costs','data_sources','hypotheses','notes'] }

function d1Prompt(repo) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
D1 EXTRACTION for repository ${repo} (${SNAP}/${repo}/). Extract, with repository/file:line and the
figure for every element, whatever this repository establishes about:
 (a) execution venues lawfully reachable by the operator (jurisdiction: British Columbia, Canada,
     per the repositories), and venues found NOT reachable, with the evidence type (measured
     login/API/KYC outcome vs carried terms) and date;
 (b) measured round-trip cost per instrument (fees, spread, slippage, funding, borrow), with the
     measurement method, date and n;
 (c) capital scale per sleeve (stated account sizes, position minimums, sleeve allocations);
 (d) data sources available at zero or low cost with their MEASURED limitations (lags, coverage,
     rate limits, survivorship, vendor tiers) and cost;
 (e) latency capability (measured or stated: collection cadence, order path, colocation, none);
 (f) EVERY hypothesis or entry in this repository: ID, one-line statement, status (open / closed /
     parked / shipped / blocked / registered-not-open / culled-at-registration), closure kind from
     the house taxonomy (cost-bound, signal-absent, unmeasurable-on-available-data,
     untestable-at-achievable-power, source-integrity-blocked, other), closure date, deciding figure
     with n, and registered reopen conditions.
Write ${OUT}/D1_constraints/${repo}.md (six sections a-f, tables) and ${OUT}/D1_constraints/${repo}.json
with keys venues, costs, capital, data_sources, latency, hypotheses (arrays of objects with fields
value, source_file, source_line, date, measured_or_carried, notes as applicable; hypotheses carry id,
statement, status, closure_kind, closure_date, deciding_figure, n, reopen_conditions, source_file,
source_line). Return counts.`
}

const D1_MERGE = `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
D1 MERGE. Read every ${OUT}/D1_constraints/*.md and *.json. Write ${OUT}/D1_CONSTRAINTS.md: the
reconstructed constraint set, one section per element (a) venues reachable / not reachable, (b)
measured round-trip cost per instrument, (c) capital scale per sleeve, (d) data sources with
measured limitations, (e) latency capability, (f) the COMPLETE hypothesis register across all
thirteen repositories (closed / open / parked / shipped / blocked, with closure kinds). Every row
carries repository, file:line and figure. Where repositories disagree on a figure, show both and
the dates; consult ${F}/agentC/seeded/CONCORDANCE.md and ${F}/SUMMARY.md for the adjudicated view
and cite them. Also write ${OUT}/D1_CONSTRAINTS.json (same structure, machine-readable) and end the
md with "## What the constraint set does not tell us" (gaps). Return a plain summary.`

function d2Prompt(angle) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
D2 METHOD PROPOSER, angle: ${angle}. Read ${F}/SUMMARY.md, ${F}/METHOD.md, ${F}/agentC/adjudication/*.md,
and the seeded outputs ${F}/agentA/seeded/, ${F}/agentB/seeded/, ${F}/agentC/seeded/ (especially
CHECK1, CHECK2, CHECK3, CHECK5, CHECK6/CONCORDANCE). Open the repositories' own templates
(REGISTRATION.md sections, HYPOTHESES.md rules, DECISIONS.md ADR format, CLAUDE.md) in ${SNAP}/.
Propose improvements to METHOD before any new hypothesis: the registration template, guard set,
closure taxonomy, power conventions, interval conventions, calibration ledger, amendment discipline,
carried-vs-measured discipline, and the audit process itself. EVERY proposal must cite a specific
frozen finding ID (or an adjudication ruling) that motivates it, state the concrete change (what
text or rule changes in which template file), its expected value (which class of error it prevents
and how often that error appeared across the thirteen repositories, with counts from the findings),
and its implementation cost (hours, and whether existing registrations must be amended). Write
${OUT}/D2_method/${angle.replace(/[^a-z0-9]+/gi,'_').toLowerCase()}.md with 5-10 proposals in a fixed
block format (Title / Motivating finding IDs / Change / Expected value / Cost / Risk of the change
itself). Return the list of titles.`
}

const D2_RANK = `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
D2 RANKER. Read every ${OUT}/D2_method/*.md. Merge duplicates, keep the strongest statement of each,
verify each cited finding ID exists in ${F}/SUMMARY.md or the agent files (drop any proposal whose
motivating finding does not exist or was ruled NOT_UPHELD without a surviving alternative), and
rank by expected value against implementation cost. Write ${OUT}/D2_METHOD.md: the ranked list with
the full block for each, a table (rank, title, motivating IDs, EV, cost, ratio), and a short section
"Proposals considered and dropped" with reasons. Return the top five titles.`

function d3GenPrompt(angle) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
D3 HYPOTHESIS GENERATOR, angle: ${angle}. Read ${OUT}/D1_CONSTRAINTS.md and .json first: the
reachable venues, measured costs, capital scale, data sources, latency and the COMPLETE list of
closed/open/parked/shipped hypotheses. Read ${F}/SUMMARY.md for the three most consequential findings
and the frozen findings that name untested variants, expired blockers or alternative endpoints.
Generate 4-6 candidate hypotheses from your angle. For EACH, fill every field:
 1. Falsifiable one-sentence statement (with the endpoint, the bar and the horizon).
 2. Mechanism, stated independently of venue cost (why the effect should exist at all).
 3. Primary evidence: citations (papers, public datasets, or repository measurements) with sample
    periods and effect sizes; say when a citation is from memory and must be checked.
 4. Duplication verdict against EVERY entry in D1 section (f): CLEAR, ADJACENT or DUPLICATE, naming
    the entries compared and why.
 5. Reachable venue and the MEASURED cost hurdle on the specific instrument (cite D1; if the cost
    was never measured, say "unmeasured" and name what measuring it would take).
 6. Whether a sleeve at the stated capital scale supports at least one position (minimum size vs
    sleeve capital, from D1).
 7. Power estimate at HALF the cited effect size: the test, alpha, the observation count needed
    for 80 percent power, and the calendar time to reach it at the data cadence available (show
    the arithmetic; use the venv).
 8. The single biggest reason it would fail.
 9. The frozen finding ID that motivated it, or the word NOVEL.
Write ${OUT}/D3_candidates/${angle.replace(/[^a-z0-9]+/gi,'_').toLowerCase()}.md and a json array
${OUT}/D3_candidates/${angle.replace(/[^a-z0-9]+/gi,'_').toLowerCase()}.json with keys id
(D3-<angle-slug>-<k>), statement, mechanism, evidence, duplication_verdict, duplication_against,
venue, instrument, cost_hurdle, cost_measured, affordability, power_n, power_calendar_time,
power_arithmetic, biggest_failure_reason, motivating_finding. Return the list of ids and statements.`
}

const SCREEN_SCHEMA = { type: 'object', properties: { id: { type: 'string' }, duplication: { type: 'string', enum: ['CLEAR','ADJACENT','DUPLICATE'] }, venue: { type: 'string', enum: ['PASS','FAIL','UNMEASURED'] }, affordability: { type: 'string', enum: ['PASS','FAIL','UNKNOWN'] }, power: { type: 'string', enum: ['PASS','FAIL','UNKNOWN'] }, overall: { type: 'string', enum: ['SURVIVES','SCREENED_OUT'] }, failing_gate: { type: 'string' }, reasoning: { type: 'string' } }, required: ['id','duplication','venue','affordability','power','overall','failing_gate','reasoning'] }

function screenPrompt(cand) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
D3 INDEPENDENT SCREENER for candidate ${cand.id}: "${cand.statement}". Read the full candidate block
in ${cand.file} and ${OUT}/D1_CONSTRAINTS.md/.json. Re-run each gate yourself, do not trust the
generator's self-assessment:
 - DUPLICATION: compare against EVERY entry in D1 section (f) and against the closed-before-opening
   and parked lists in each repository's HYPOTHESES.md (grep ${SNAP}/*/HYPOTHESES.md). DUPLICATE
   fails; ADJACENT passes only if the candidate names what is different and why the prior closure
   does not already answer it.
 - VENUE: is the venue lawfully reachable per D1 (measured, not carried)? Is the cost hurdle on the
   specific instrument measured? UNMEASURED does not fail by itself but must be recorded.
 - AFFORDABILITY: does a sleeve at the stated capital support at least one position?
 - POWER: recompute the power arithmetic at half the cited effect with the venv; does the observation
   count arrive within a calendar time the program could plausibly wait (state the threshold you
   used and why)?
Return the structured verdict; the reasoning must cite D1 rows and repository file:line.`
}

const D4_D5 = `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
D4 and D5. Inputs: ${OUT}/D1_CONSTRAINTS.md, ${OUT}/D2_METHOD.md, every ${OUT}/D3_candidates/*.md and
${OUT}/D3_screening.json (screener verdicts), ${F}/SUMMARY.md.
D4: state plainly whether ANY new hypothesis is warranted. If the constraint set implies the reachable
space (venues × instruments × data × capital × latency) is exhausted or nearly so, say so and defend
it with the D1 rows; if survivors exist, say why they are not already answered by a closure. A
recommendation to open nothing, with reasoning, is acceptable and complete.
D5: write ${OUT}/RECOMMENDATION.md with: (1) the constraint set with its sources (condensed from D1,
every row cited); (2) the ranked method improvements (from D2); (3) the surviving hypotheses in
priority order with all nine fields; (4) the screened-out list with the failing gate named for each;
(5) the D4 verdict; (6) the single next action you would take, with reasons. Also write
${OUT}/D3_HYPOTHESES.md (survivors + screened-out, full blocks) and ${OUT}/D4_VERDICT.md. If at any
point you concluded a frozen finding is wrong, append it to ${OUT}/PHASE3_NOTES_ON_FINDINGS.md
(create it; if you have no such notes, create it saying so). Return a plain summary: D4 verdict,
number of survivors, top three method improvements, next action.`

async function batched(items, fn) { const out = []; for (let i = 0; i < items.length; i += BATCH) { const res = await parallel(items.slice(i, i + BATCH).map(it => () => fn(it))); out.push(...res) } return out }

phase('D1 Constraints')
const d1 = await batched(REPOS, r => agent(d1Prompt(r), { label: `D1:${r}`, phase: 'D1 Constraints', schema: D1_SCHEMA }))
if (d1.filter(Boolean).length < REPOS.length) { log('D1 extraction incomplete; resume after the limit resets'); return { incomplete: 'D1' } }
const d1m = await agent(D1_MERGE, { label: 'D1-merge', phase: 'D1 Constraints' })
if (!d1m) return { incomplete: 'D1-merge' }

phase('D2 Method')
const angles2 = ['registration template and guard set', 'statistics, power and interval conventions', 'process, amendments, calibration and audit']
const d2 = await batched(angles2, a => agent(d2Prompt(a), { label: `D2:${a.slice(0, 20)}`, phase: 'D2 Method' }))
if (d2.filter(Boolean).length < angles2.length) return { incomplete: 'D2' }
const d2r = await agent(D2_RANK, { label: 'D2-rank', phase: 'D2 Method' })
if (!d2r) return { incomplete: 'D2-rank' }

phase('D3 Hypotheses')
const angles3 = ['microstructure and cost-structure driven', 'calendar, event and announcement driven', 'cross-asset, basis and funding driven', 'data-availability driven (what the program can measure that others cannot)', 'findings-motivated (untested variants, expired blockers, alternative endpoints named in the frozen findings)']
const gens = await batched(angles3, a => agent(d3GenPrompt(a), { label: `D3-gen:${a.slice(0, 20)}`, phase: 'D3 Hypotheses' }))
if (gens.filter(Boolean).length < angles3.length) return { incomplete: 'D3-gen' }
// collect candidate ids from the json files via a small agent (script has no fs access)
const CAND_SCHEMA = { type: 'object', properties: { candidates: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, statement: { type: 'string' }, file: { type: 'string' } }, required: ['id','statement','file'] } } }, required: ['candidates'] }
const cl = await agent(`Read every json file under ${OUT}/D3_candidates/ and return the list of candidates: id, statement, and the md file path that holds the full block (same basename, .md). Do not write anything.`, { label: 'D3-collect', phase: 'D3 Hypotheses', schema: CAND_SCHEMA })
if (!cl) return { incomplete: 'D3-collect' }
const screens = await batched(cl.candidates, c => agent(screenPrompt(c), { label: `D3-screen:${c.id}`, phase: 'D3 Hypotheses', schema: SCREEN_SCHEMA }))
const sv = screens.filter(Boolean)
const writer = await agent(`Write ${OUT}/D3_screening.json containing exactly this JSON array (verbatim) and return "ok": ${JSON.stringify(sv)}`, { label: 'D3-screen-write', phase: 'D3 Hypotheses' })
if (!writer) return { incomplete: 'D3-screen-write' }

phase('D4-D5 Verdict')
const d45 = await agent(D4_D5, { label: 'D4-D5', phase: 'D4-D5 Verdict' })
return { d1: d1.filter(Boolean).length, d2: typeof d2r === 'string' ? d2r.slice(0, 1500) : d2r, candidates: cl.candidates.length, survivors: sv.filter(s => s.overall === 'SURVIVES').map(s => s.id), screened_out: sv.filter(s => s.overall !== 'SURVIVES').map(s => `${s.id}:${s.failing_gate}`), d45: typeof d45 === 'string' ? d45.slice(0, 3000) : d45 }
