export const meta = {
  name: 'seeded-checks',
  description: 'Six seeded checks (multiplicity, endpoint independence, interval assumptions, carried vs measured, calibration, cross-repo propagation) run for one agent after its blind pass',
  phases: [
    { title: 'Triage', detail: 'per-repository extraction of every correction, co-primary endpoint, CI, carried figure and prior' },
    { title: 'Checks', detail: 'checks 1, 2, 4, 5 cross-repository; check 3 per repository' },
    { title: 'Propagation', detail: 'check 6: template-error propagation and figure concordance' },
  ],
}

const AGENT = args.agent            // 'A' | 'B' | 'C'
const OUT = args.outdir             // .../findings/agentX/seeded
const BLIND = args.blinddir         // .../findings/agentX  (own blind output; may be read)
const RULES_PATH = '/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/COMMON_RULES.md'
const SNAP = '/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/snap'
const REPOS = ['retail-power-limits','HFExperiment','InsiderExperiment','NPDExperiment','VRPExperiment','ETFExperiment','solclear','PMExperiment','solattn','NPLExperiment','MLCryptoEngine','ORBExperiment','AiTrader']
const BATCH = 3

const ROLE = AGENT === 'A'
  ? 'You are part of Agent A (thesis: the program closed hypotheses too early or too hard). For the seeded checks you follow the check procedure exactly and report what the numbers say; assign each finding the Direction its consequence actually cuts (A if the error made closure easier or power look worse than it was; B if it made a positive or a power figure look better than it was).'
  : AGENT === 'B'
  ? 'You are part of Agent B (thesis: the program claimed more than it earned). For the seeded checks you follow the check procedure exactly and report what the numbers say; assign each finding the Direction its consequence actually cuts (A if the error made closure easier or power look worse than it was; B if it made a positive or a power figure look better than it was).'
  : 'You are part of Agent C, the referee and verifier. You have no thesis. Follow the check procedure exactly and report what the numbers say; assign each finding the Direction its consequence actually cuts (A if the error made closure easier or power look worse than it was; B if it made a positive or a power figure look better than it was).'

const ID_RULE = `ID convention for seeded findings: AUDIT-${AGENT}-<REPO>-<n> with n = 100*k + i for check k (so check 1 findings are 101, 102, ...; check 6 are 601, 602, ...). This keeps the stable-ID form and cannot collide with blind-pass IDs. Seeded findings are written ONLY under ${OUT}; never edit anything under ${BLIND} outside seeded/.`

const FORMAT = `Every finding uses the standard block format from the rules file (all fields, verbatim quote with file:line, figures with n, Label, Severity, Direction, Confidence, Invalidated-by-later-commits, Disclosed-by-authors). Also write a JSON array file next to each md with keys: id, repo, sha, agent, direction, hypothesis_or_artifact, class, severity, label, claim_quote, claim_file, claim_line, evidence_summary, evidence_refs, recomputation, would_resolve, confidence, confidence_why, invalidated_by_later_commits, invalidation_note, disclosed_by_authors, disclosure_ref, check (integer 1-6). Report where you found nothing: a check that finds no instance in a repository says so with what was searched.`

const TRIAGE_SCHEMA = { type: 'object', properties: {
  repo: { type: 'string' },
  corrections: { type: 'integer' }, co_primary_declarations: { type: 'integer' }, confidence_intervals: { type: 'integer' },
  carried_figures: { type: 'integer' }, prior_records: { type: 'integer' }, calibration_ledger_exists: { type: 'boolean' },
  notes: { type: 'string' } }, required: ['repo','corrections','co_primary_declarations','confidence_intervals','carried_figures','prior_records','calibration_ledger_exists','notes'] }

function triagePrompt(repo) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
You are the TRIAGE extractor for repository ${repo}, reading ${SNAP}/${repo}/ (read-only) and, where
needed, the live repository's git history and untracked data (read-only, per the rules). Read
REGISTRATION.md (and registrations/*/REGISTRATION.md), HYPOTHESES.md, DECISIONS.md, report.md,
FINDINGS.md, README.md, docs/, reports/*.md, progress.md and the analysis code COMPLETELY enough to
extract EVERY instance of the following. Be exhaustive; later check agents work only from your lists.

 T1 MULTIPLICITY: every place a multiple-comparison correction (Šidák, Bonferroni, Holm, BH, or a
    stated alpha split) is applied or declared. Record: the correction, the number of components m,
    the alpha used, the DECISION RULE text verbatim (does the verdict require ALL components to pass
    = conjunction / intersection-union, or ANY = union?), the power figure that rests on it, and
    file:line for each. Include the analysis code path that implements it if one exists.
 T2 CO-PRIMARY ENDPOINTS: every declaration of two or more co-primary (or joint primary) endpoints.
    Record each endpoint's exact definition/formula, the assumptions and horizons used in power
    calculations, the power figures for each component, where the power code lives, file:line.
 T3 CONFIDENCE INTERVALS: EVERY reported confidence interval or standard error (registration,
    report, FINDINGS, progress, reports/*.md, stored JSON/CSV). Record: quantity, point estimate,
    lower, upper (or halfwidth), n, the sd or dispersion if stated, the estimator named (normal,
    Wilson, exact binomial, bootstrap, clustered, HAC/Newey-West, block bootstrap...), the data
    structure (iid, time series, panel, repeated within day/instrument), the file:line, and the
    path to the underlying data or artifact if it exists (snapshot path or live untracked path).
 T4 CARRIED VS MEASURED: every externally sourced figure the repository registers or relies on:
    fee schedules, venue terms, jurisdiction/licence policies, vendor tiers and limits, margin
    requirements, contract specifications, rate limits, publication lags, minimum sizes. Record the
    value, the stated source, whether it was MEASURED live (how, when) or CARRIED from
    documentation, its date, and file:line.
 T5 CALIBRATION: every recorded prior (assistant prior, operator prior, probability of outcome
    map states), its date, whether it precedes the outcome (compare to the verdict date and to git
    history where needed), whether a calibration ledger or Brier record exists, and whether each
    resolved hypothesis was scored against its prior. file:line for each.

OUTPUT: ${OUT}/_triage/${repo}.md with five sections T1..T5 as tables or lists (every row with
file:line), and ${OUT}/_triage/${repo}.json with keys t1_corrections, t2_co_primary, t3_intervals,
t4_carried, t5_priors, each an array of objects carrying the fields above (use null where a field is
absent). Live-repo access log at the end of the md if you touched the live repo. Return the counts.`
}

function checkPrompt(k, title, body) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
${ID_RULE}
${FORMAT}
You run SEEDED CHECK ${k}: ${title}. Inputs: every triage file ${OUT}/_triage/*.md and *.json
(all thirteen repositories), the snapshots under ${SNAP}/, live git history and untracked data
read-only where needed, and the Python venv for computation (write scripts only under your work
dir). You may read ${BLIND}/*.md for context on what the blind pass already raised, but seeded
findings are recorded ONLY under ${OUT} and never backfilled into the blind output.
${body}
OUTPUT: ${OUT}/CHECK${k}_${title.replace(/[^a-z0-9]+/gi,'_').toLowerCase()}.md and the matching .json array
(possibly empty). The md must have: Method (what you did, exactly), a per-repository table of every
instance examined with its result (including "no instance" rows), the findings in standard block
format, and "What could not be checked and why". Return a plain summary: per repository, instances
examined and findings raised.`
}

const CHECK1 = `For every registration applying a multiple-comparison correction (from T1), determine whether
the decision rule is a CONJUNCTION (all components must pass; intersection-union test) or a UNION
(any component passing suffices). Šidák and Bonferroni control the union case. Under an
intersection-union rule each component may run at the full nominal alpha and overall size is still
preserved (Berger 1982). Report every union-type correction applied to a conjunction rule, quote
the rule and the correction verbatim with file:line, and RECOMPUTE the power of each component and
of the conjunction at the proper alpha using the repository's own stated effect size, dispersion
and n (cite each input with file:line; show the code you ran). State whether the corrected power
changes any registered verdict, power floor, or "untestable-at-achievable-power" closure. Where the
correction is correctly matched to a union rule, say so and list it under sound. Where the
repository itself noticed the mismatch (search for Berger, intersection-union, conjunction), say so
and cite it; such a finding is READ and capped at S3.`

const CHECK2 = `For every declaration of two or more co-primary endpoints (from T2), test NUMERICALLY whether
they are algebraically related. Reconstruct each endpoint from its registered definition.
Compute both component powers across AT LEAST SIX assumption-and-horizon combinations (vary the
effect size, dispersion, n, horizon, base rate or whatever the registration parameterises) using
the repository's own power method where it is specified (copy any power script to your work dir and
run it there; otherwise reimplement from the registered formula and say so). Report the maximum
absolute difference in power between the components across all cells. Agreement better than 1e-3
in every cell means the endpoints are coupled and the design is one test wearing two labels.
Report whether the repository detected this itself (cite). Show the table of cells and the code.
If no repository declares co-primary endpoints, say so per repository with what you searched.`

function check3Prompt(repo) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
${ID_RULE}
${FORMAT}
You run SEEDED CHECK 3 (interval assumptions) for repository ${repo}. Inputs: ${OUT}/_triage/${repo}.md
and .json (section T3), the snapshot ${SNAP}/${repo}/, live git history and untracked data
read-only, and the Python venv (scripts only under your work dir). You may read ${BLIND}/${repo}.md
for context; record findings ONLY under ${OUT}.
For EVERY reported confidence interval in T3: compute halfwidth × sqrt(n) / sd (use the reported sd;
if only the interval and n are reported, back out the implied sd under the stated estimator and say
so; for proportions use sqrt(p(1-p))). A value at or near 1.96 (or 1.645 / 2.576 for other
levels) across every unit in a panel indicates a flat normal interval with no clustering,
autocorrelation or block adjustment. Tabulate every interval with the ratio. Then for each interval
whose data is time series, panel, or repeated within days or instruments, determine whether the
independence assumption is plausibly violated (state why). Where the underlying data exists (stored
JSON/CSV/parquet in the snapshot, or untracked data in the live repo, read-only), RECOMPUTE the
interval with a clustered (by day / instrument / whichever unit the registration implies) or
moving-block-bootstrap estimator, and report whether any stated conclusion, bar comparison or
verdict moves. Where data does not allow recomputation, say exactly what is missing. Report
intervals that are already correctly adjusted as sound.
OUTPUT: ${OUT}/CHECK3_intervals/${repo}.md and ${OUT}/CHECK3_intervals/${repo}.json (array, possibly
empty). Return a plain summary: intervals examined, ratio distribution, recomputed count, conclusions
moved.`
}

const CHECK4 = `Identify every figure currently registered or relied upon that is CARRIED from documentation
rather than measured live, and every MEASURED figure old enough to have plausibly moved (state the
measurement date and the age at the anchor date 2026-09-02). Fee schedules, venue terms,
jurisdiction policies, vendor tiers, margin requirements, contract specifications, rate limits and
publication lags are the likely cases. Use T4 from every repository. For each: repository, figure,
value, source, measured/carried, date, age, which registered decision or hurdle depends on it, and
file:line. Then check whether a DIFFERENT repository measured the same figure (this overlaps with
check 6; here just note it). A finding is STALE_FIGURE, usually S3; it is S2 or S1 only if a
verdict or hurdle depends on the figure and the repository states the figure must be measured
(cite that rule). Where a repository documents its carried-vs-measured discipline and applies it,
report it sound.`

const CHECK5 = `Determine, per repository: whether forecast priors are recorded BEFORE outcomes (compare the
prior's date and git commit to the verdict's date and commit; use git log -S or git blame on the
live repository read-only where the document dates are ambiguous); whether a calibration ledger
exists (a place where priors are scored against outcomes, Brier or log score or a simple hit
table); whether every RESOLVED hypothesis has actually been scored against its prior; and whether
unresolved priors are tracked. "Priors recorded but never scored" is a finding (PROCESS, S3 or S4).
"Prior recorded after the outcome existed" is a finding (PROVENANCE, S2). Where a repository
scores its priors properly, report it sound and cite the ledger. Use T5 from every repository and
verify each claimed ledger by opening it.`

const CHECK6 = `These repositories share a house format (REGISTRATION.md with an outcome map, power section,
inference section, priors; HYPOTHESES.md register; DECISIONS.md ADRs; amendment logs), so a
template error in one registration is likely present in several.
PART 1 PROPAGATION: read every check output under ${OUT}/CHECK*.md and CHECK3_intervals/*.md and
every blind finding under ${BLIND}/*.md (own agent's output). For EVERY statistical or procedural
error found anywhere, check EVERY OTHER repository for the same pattern (grep the snapshots for the
same phrasing, the same section structure, the same formula, the same estimator; open the
registrations). Record a matrix: error pattern × repository → present / absent / not applicable,
with file:line for each present cell. Each newly found instance is a finding with its own ID under
this check (class as appropriate, e.g. STATISTICAL or PROCESS); an instance already raised under
another check or in the blind pass is cross-referenced, not duplicated.
PART 2 FIGURE CONCORDANCE: build a table of every externally sourced or measured figure that appears
in more than one repository (fees, venue terms, jurisdiction rules, vendor tiers, publication lags,
margin, contract specs, cost hurdles, round-trip costs, minimum sizes, rate limits). For each:
figure, each repository's stated value, each measurement or citation date, whether they agree, and
which repositories carry it unmeasured while another measured it. Use ${OUT}/CHECK4_*.md and the
triage T4 sections as the starting inventory, then grep all snapshots to complete it. Flag every
disagreement and every carried-while-measured-elsewhere case as a finding (CROSS_REPO_INCONSISTENCY
or STALE_FIGURE).
OUTPUT: the standard CHECK6 md and json PLUS ${OUT}/CONCORDANCE.md holding the figure concordance
table and the propagation matrix.`

async function batched(items, fn) {
  const out = []
  for (let i = 0; i < items.length; i += BATCH) {
    const res = await parallel(items.slice(i, i + BATCH).map(it => () => fn(it)))
    out.push(...res)
  }
  return out
}

// Disk-state driven skipping (see agentA-blind.workflow.js): tools/agent_state.py <out> --seeded
// passes {triage_done, check3_done, checks_done, c3merge_done} as args.state; every launch is fresh.
const ST = (args && args.state) || {}
const TRIAGE_DONE = new Set(ST.triage_done || [])
const CHECK3_DONE = new Set(ST.check3_done || [])
const CHECKS_DONE = new Set(ST.checks_done || [])
const onDisk = (label) => { log(`${label}: on disk, skipped`); return Promise.resolve({ on_disk: true }) }
phase('Triage')
const triage = await batched(REPOS, r => TRIAGE_DONE.has(r) ? onDisk(`triage:${r}`).then(o => ({ ...o, repo: r })) : agent(triagePrompt(r), { model: 'opus', label: `${AGENT}-triage:${r}`, phase: 'Triage', schema: TRIAGE_SCHEMA }))
const tri = triage.filter(Boolean)
log(`triage done for ${tri.length}/13 repos`)
if (tri.length < REPOS.length) { log('triage incomplete; stop here and resume after the limit resets'); return { triage: tri, incomplete: true } }

phase('Checks')
const c3 = await batched(REPOS, r => CHECK3_DONE.has(r) ? onDisk(`check3:${r}`) : agent(check3Prompt(r), { model: 'opus', label: `${AGENT}-check3:${r}`, phase: 'Checks' }))
const c12 = await parallel([
  () => CHECKS_DONE.has(1) ? onDisk('check1') : agent(checkPrompt(1, 'multiplicity', CHECK1), { model: 'opus', label: `${AGENT}-check1`, phase: 'Checks' }),
  () => CHECKS_DONE.has(2) ? onDisk('check2') : agent(checkPrompt(2, 'endpoint independence', CHECK2), { model: 'opus', label: `${AGENT}-check2`, phase: 'Checks' }),
])
const c45 = await parallel([
  () => CHECKS_DONE.has(4) ? onDisk('check4') : agent(checkPrompt(4, 'carried vs measured', CHECK4), { model: 'opus', label: `${AGENT}-check4`, phase: 'Checks' }),
  () => CHECKS_DONE.has(5) ? onDisk('check5') : agent(checkPrompt(5, 'calibration', CHECK5), { model: 'opus', label: `${AGENT}-check5`, phase: 'Checks' }),
])
const c3merge = ST.c3merge_done ? await onDisk('check3-merge') : await agent(`First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
Mechanical merge task. Read every file under ${OUT}/CHECK3_intervals/ (thirteen md + json). Write
${OUT}/CHECK3_intervals.md: a method paragraph, a single table of EVERY interval examined across all
repositories (repo, quantity, estimate, CI, n, ratio halfwidth·√n/sd, estimator, data structure,
independence plausible?, recomputed?, conclusion moved?), then the findings from all per-repository
files reproduced verbatim (do not renumber), then a merged "What could not be checked". Write
${OUT}/CHECK3_intervals.json as the concatenation of the per-repository json arrays (validate JSON).
Do not change any finding's substance. Return counts.`, { model: 'opus', label: `${AGENT}-check3-merge`, phase: 'Checks' })
const missing = [c3.filter(Boolean).length < REPOS.length ? 'check3' : null, c12[0] ? null : 'check1', c12[1] ? null : 'check2', c45[0] ? null : 'check4', c45[1] ? null : 'check5', c3merge ? null : 'check3-merge'].filter(Boolean)
if (missing.length) { log(`checks incomplete: ${missing.join(', ')}; resume after the limit resets`); return { incomplete: true, missing } }

phase('Propagation')
const c6 = CHECKS_DONE.has(6) ? await onDisk('check6') : await agent(checkPrompt(6, 'cross repository propagation', CHECK6), { model: 'opus', label: `${AGENT}-check6`, phase: 'Propagation' })

return {
  triage: tri.map(t => ({ repo: t.repo, ci: t.confidence_intervals, corr: t.corrections, coprim: t.co_primary_declarations, carried: t.carried_figures, priors: t.prior_records, ledger: t.calibration_ledger_exists })),
  checks: [...c12, ...c45].map(r => typeof r === 'string' ? r.slice(0, 1500) : r),
  c3: c3.map(r => typeof r === 'string' ? r.slice(0, 400) : r),
  c6: typeof c6 === 'string' ? c6.slice(0, 3000) : c6,
}
