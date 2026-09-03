export const meta = {
  name: 'agentC-blind',
  description: 'Agent C referee blind pass: numeric-claim verification against code and data, inference audit (CIs and test statistics), git provenance of registration claims, per repository',
  phases: [
    { title: 'Locate', detail: 'per repository: inventory analysis code, ledgers, manifests, JSON/CSV artifacts and the numeric claims that rest on them' },
    { title: 'Verify', detail: 'per repository: claims vs code/data, derived quantities recomputed, every CI and test statistic audited' },
    { title: 'Provenance', detail: 'per repository: git show on every registration-before-data claim' },
    { title: 'Consolidate', detail: 'per repository: findings register with IDs, md + json' },
    { title: 'Check', detail: 'citation verifier + applier per repository' },
  ],
}

const RULES_PATH = '/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/COMMON_RULES.md'
const SNAP = '/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/snap'
const OUT = '/home/kiros-li/Documents/GitHub/program-audit/findings/agentC'
const LIVE = '/home/kiros-li/Documents/GitHub'
const REPOS = ['retail-power-limits','HFExperiment','InsiderExperiment','NPDExperiment','VRPExperiment','ETFExperiment','solclear','PMExperiment','solattn','NPLExperiment','MLCryptoEngine','ORBExperiment','AiTrader']
const BATCH = 2

const ROLE = `
YOU ARE AGENT C, the referee and verifier. You have NO thesis. You do not argue that the program
closed too early or claimed too much; you establish what the numbers, the code, the stored data and
the git objects actually support. Unverifiable is a legitimate result and must never be guessed at.
Where a claim verifies, say so plainly: a verified claim is as important a result as a contradicted
one. You have not read, and must not read, anything under findings/agentA or findings/agentB.
`

const FINDING_BLOCK = `
Findings (only where verification CONTRADICTS a claim, or a stated estimator/correction/provenance
does not match what was done) use the standard block format from the rules file:
### <ID>
- **Repository / SHA:** <repo> / <sha>
- **Hypothesis or artifact:** ...
- **Direction:** A|B  (the direction the discrepancy cuts: A if it makes a closure weaker than labelled, B if it makes a positive or a power figure weaker than claimed; write "neutral" only for pure hygiene)
- **Class:** ...
- **Severity:** S1|S2|S3|S4
- **Label:** DERIVED|READ
- **Claim challenged (verbatim quote):** "..." — <repo>/<path>:<line>
- **Evidence:** ... (figures with n, each with <repo>/<path>:<line> or data path + UTC read time)
- **Recomputation (if any):** inputs with file:line, method, result, tolerance
- **What would resolve it:** ...
- **Confidence:** HIGH|MEDIUM|LOW — <one sentence>
- **Invalidated by later commits?:** yes|no — <why>
- **Disclosed by authors?:** yes (<file:line>)|no — <one sentence>
`

const LOCATE_SCHEMA = { type: 'object', properties: {
  repo: { type: 'string' }, n_artifacts: { type: 'integer' }, n_code_files: { type: 'integer' }, n_claims_listed: { type: 'integer' },
  top_claims: { type: 'array', items: { type: 'string' } }, has_untracked_data: { type: 'boolean' }, notes: { type: 'string' } },
  required: ['repo','n_artifacts','n_code_files','n_claims_listed','top_claims','has_untracked_data','notes'] }

function locatePrompt(repo) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
LOCATE task for repository ${repo}. Snapshot: ${SNAP}/${repo}/. Live repo (read-only, git and
untracked data only): ${LIVE}/${repo}/.
 1. INVENTORY every place a number could be verified: analysis code (src/, scripts/, tools/,
    research/, *.py), stored ledgers, manifests, JSON/CSV/parquet artifacts under reports/, data/,
    audit/, docs/, and untracked data in the live working tree (ls -la only; note sizes and mtimes;
    do not open large binaries). For each artifact: path, what it holds, which document figures it
    appears to back, whether it is tracked (anchored) or untracked (unanchored).
 2. LIST THE NUMERIC CLAIMS: read REGISTRATION.md (and registrations/*), HYPOTHESES.md, report.md,
    FINDINGS.md, README.md, DECISIONS.md verdict entries, and reports/*.md. Extract every numeric
    claim that a verdict, closure, power figure, cost hurdle or shipped artifact rests on: the
    claim verbatim, file:line, the figure(s) and n, and the artifact or code you believe produced
    it. Rank them by how much rests on them (a closure's deciding number ranks first). Mark at
    least the top five as MUST-VERIFY (the brief demands at least three per repository).
 3. LIST EVERY CONFIDENCE INTERVAL and EVERY TEST STATISTIC or p-value reported anywhere in the
    documents, with file:line, the stated estimator or test, n, and the data structure.
 4. LIST EVERY PROVENANCE CLAIM: statements that bars, parameters, outcome maps, priors or decision
    rules were fixed in a named commit or before data existed (grep for commit hashes, "registered
    before", "before any data", "sealed", "frozen", "no data existed", "accepted before"). Record
    the claim verbatim, file:line, the commit named (if any), and what would have to be true.
OUTPUT: ${OUT}/verification/${repo}.inventory.md with four sections (Artifacts, Numeric claims
ranked with MUST-VERIFY marks, Intervals and tests, Provenance claims), and
${OUT}/verification/${repo}.inventory.json with keys artifacts, claims, intervals, tests,
provenance_claims (arrays of objects with the fields above). Live-repo access log at the end of the
md. Return the counts and the top claims.`
}

function verifyPrompt(repo, inv) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
VERIFY task for repository ${repo}. Read ${OUT}/verification/${repo}.inventory.md and .json first
(your own agent's inventory). Snapshot: ${SNAP}/${repo}/. Live repo (read-only): ${LIVE}/${repo}/.
Python venv and work dir per the rules. Inventory summary: ${JSON.stringify(inv).slice(0, 1500)}

 A. NUMERIC CLAIMS. For every MUST-VERIFY claim (at least the three highest-severity, preferably
    all listed), verify the number against the code or data that produced it: open the artifact,
    recompute the figure from stored primitives (counts, sums, per-unit rows) with your own short
    script, and compare. Where the code that produced it exists, read it and confirm the formula,
    the filters, the sample window and the n; run a copy in your work dir only if inputs are
    available read-only. Record for EACH claim: stated value, source of truth used, recomputed
    value, tolerance, and status VERIFIED / CONTRADICTED / UNVERIFIABLE (with the exact reason:
    artifact missing, data not served, code absent, inputs unanchored, etc.). Also recompute every
    DERIVED quantity you can from stored primitives (rates from counts, means from sums, power from
    stated inputs, cost hurdles from fee components, intervals from stored rows) and check agreement.
 B. INTERVALS. For EVERY confidence interval in the inventory: identify the estimator actually used
    (from code if it exists, else from the document), whether independence was assumed, whether the
    data structure (time series, panel, repeated within day/instrument) makes that assumption
    doubtful, and whether the interval reproduces from stored data. Record a table row per interval.
 C. TEST STATISTICS. For EVERY test statistic or p-value: check the tail (one- vs two-sided against
    the registered direction), the degrees of freedom or the exact distribution, whether the
    multiplicity correction applied matches the decision rule it feeds (a union-type correction
    such as Šidák or Bonferroni on a conjunction / all-must-pass rule is a mismatch; an
    intersection-union rule needs no correction per component), and whether the statistic
    reproduces. Record a table row per test.
Every status must be one of VERIFIED, CONTRADICTED, UNVERIFIABLE. Never guess. If a claim is
UNVERIFIABLE because the data is unanchored or absent, say exactly what is missing.
${FINDING_BLOCK}
Raise findings ONLY for CONTRADICTED claims, mismatched estimators/tails/dof/corrections, or
intervals whose independence assumption is violated in a way that changes a stated comparison
(recompute clustered/block where data allows and report whether the conclusion moves). Use
temporary IDs DRAFT-V-<k>; the consolidator assigns final IDs.
OUTPUT: ${OUT}/verification/${repo}.verification.md (sections: Claims table, Derived quantities
table, Intervals table, Tests table, Draft findings, What could not be checked and why, Live-repo
access log) and ${OUT}/verification/${repo}.claims.json: a JSON array with one object per claim,
interval and test, keys: kind (claim|derived|interval|test), claim_text, file, line, stated_value,
source_of_truth, recomputed_value, tolerance, status (VERIFIED|CONTRADICTED|UNVERIFIABLE), reason,
estimator (intervals/tests), independence_assumed (bool or null), data_structure, tail, dof,
correction_applied, decision_rule_type (conjunction|union|single|null), correction_matches_rule
(bool or null), unanchored (bool), notes. Return a plain summary: counts by status and one line per
CONTRADICTED item.`
}

function provenancePrompt(repo, inv) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
PROVENANCE task for repository ${repo}. Read ${OUT}/verification/${repo}.inventory.md and .json
(section Provenance claims). Live repo git history (read-only: git -C ${LIVE}/${repo} log|show|diff|
blame|rev-parse|cat-file|ls-tree only). Snapshot for document text: ${SNAP}/${repo}/.
For EVERY claim that bars, parameters, an outcome map, priors or a decision rule were fixed in a
named commit or before data existed:
 1. If a commit is named: run git show <commit> --stat and git show <commit>:<path> for the file(s)
    the claim concerns; confirm the commit exists, its author date, and that the bar/parameter/map
    as claimed is present in that commit's version of the file. Quote the relevant lines from the
    commit's version. Status SUPPORTED / NOT_SUPPORTED / PARTIAL (say what differs).
 2. If no commit is named: use git log --follow -p on the file and git log -S "<figure>" to find
    the first commit introducing the bar/parameter and its date; then establish when data first
    existed (first commit adding data artifacts, first progress.md entry recording a measurement,
    stored artifact timestamps, ledger first rows). Compare the dates. Status as above, with the
    commits and dates cited.
 3. For EVERY parameter, bar or rule that CHANGED after data existed (git log -p on the
    registration files; look for edits to figures, thresholds, horizons, universes, alpha, n
    targets, cost figures), check whether a dated amendment records the change with its reason and
    the data that existed. A change without a dated amendment is a finding (PROVENANCE, S2 if it
    touches a verdict-relevant figure, else S3). Include the git diff hunk (trimmed) as evidence.
 4. Record every claim and every changed parameter in a table, whether or not it is a finding.
${FINDING_BLOCK}
Use temporary IDs DRAFT-P-<k>. Every finding here is DERIVED (git objects) unless it rests only on
document text.
OUTPUT: ${OUT}/provenance/${repo}.md (sections: Registration claims table, Parameter changes after
data table, Draft findings, What could not be checked and why, Live-repo access log with the
before/after git status --porcelain) and ${OUT}/provenance/${repo}.json: array of objects with
keys kind (registration_claim|parameter_change), claim_text, file, line, commit_named,
commit_found, commit_date, data_first_existed (date + evidence), status
(SUPPORTED|NOT_SUPPORTED|PARTIAL|UNVERIFIABLE), amendment_recorded (bool or null),
amendment_ref, evidence, notes. Return a plain summary: counts by status and one line per
NOT_SUPPORTED or unamended change.`
}

const CONSOLIDATOR_SCHEMA = { type: 'object', properties: {
  repo: { type: 'string' }, n_findings: { type: 'integer' },
  claims_verified: { type: 'integer' }, claims_contradicted: { type: 'integer' }, claims_unverifiable: { type: 'integer' },
  provenance_supported: { type: 'integer' }, provenance_not_supported: { type: 'integer' }, provenance_partial: { type: 'integer' }, provenance_unverifiable: { type: 'integer' },
  findings: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, class: { type: 'string' }, severity: { type: 'string' }, label: { type: 'string' }, one_line: { type: 'string' } }, required: ['id','class','severity','label','one_line'] } } },
  required: ['repo','n_findings','claims_verified','claims_contradicted','claims_unverifiable','provenance_supported','provenance_not_supported','provenance_partial','provenance_unverifiable','findings'] }

function consolidatorPrompt(repo) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
CONSOLIDATOR for Agent C, repository ${repo}. Inputs (own agent's output): ${OUT}/verification/${repo}.inventory.md,
${OUT}/verification/${repo}.verification.md and .claims.json, ${OUT}/provenance/${repo}.md and .json.
Snapshot for checks: ${SNAP}/${repo}/.
 1. Merge the draft findings from verification and provenance; de-duplicate; drop any without a
    locatable quote and figure (record drops).
 2. Assign IDs AUDIT-C-${repo}-1, -2, ... in descending severity.
 3. Enforce the format and honest labelling (DERIVED only for data/code/git evidence; disclosed
    limitations READ and capped at S3 with the disclosure cited).
 4. Write ${OUT}/${repo}.md: a 3-8 line neutral summary of what verified, what did not, and what
    could not be checked; a "## Verification scoreboard" (claims VERIFIED / CONTRADICTED /
    UNVERIFIABLE with counts and the list of MUST-VERIFY claims with their status; intervals audited
    with estimator/independence summary; tests audited with tail/dof/correction summary; provenance
    SUPPORTED / NOT_SUPPORTED / PARTIAL / UNVERIFIABLE); the findings in standard block format;
    "## Sound" (what verified cleanly); "## Could not be checked and why"; "## Live-repo access
    log" merged.
 5. Write ${OUT}/${repo}.json: JSON array of findings with keys exactly: id, repo, sha, agent
    ("C"), direction, hypothesis_or_artifact, class, severity, label, claim_quote, claim_file,
    claim_line, evidence_summary, evidence_refs, recomputation, would_resolve, confidence,
    confidence_why, invalidated_by_later_commits, invalidation_note, disclosed_by_authors,
    disclosure_ref.
 6. Write ${OUT}/${repo}.scoreboard.json: {repo, claims: {verified, contradicted, unverifiable,
    must_verify: [{claim, status}]}, intervals: {audited, independence_doubtful, recomputed,
    conclusion_moved}, tests: {audited, tail_mismatch, dof_issue, correction_mismatch}, provenance:
    {supported, not_supported, partial, unverifiable}}.
Return the structured summary.`
}

const VERIFIER_SCHEMA = { type: 'object', properties: { repo: { type: 'string' }, verdicts: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, quote_found: { type: 'string', enum: ['EXACT','NEAR','NOT_FOUND'] }, quote_line_ok: { type: 'boolean' },
  figures_ok: { type: 'string', enum: ['YES','PARTIAL','NO','NA'] }, recomputation_reproduced: { type: 'string', enum: ['YES','NO','NOT_ATTEMPTED','NA'] },
  label_ok: { type: 'boolean' }, disclosed_by_authors: { type: 'boolean' }, disclosure_ref: { type: 'string' }, severity_ok: { type: 'boolean' },
  recommendation: { type: 'string', enum: ['KEEP','CORRECT','DROP'] }, notes: { type: 'string' } },
  required: ['id','quote_found','quote_line_ok','figures_ok','recomputation_reproduced','label_ok','disclosed_by_authors','severity_ok','recommendation','notes'] } } }, required: ['repo','verdicts'] }

function verifierPrompt(repo) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
Independent CITATION AND REPRODUCTION checker inside Agent C for repository ${repo}. Read
${OUT}/${repo}.md and .json. For every finding: grep the snapshot for the quote (EXACT / NEAR within
3 lines / NOT_FOUND); confirm the figures and n at the cited locations; where a recomputation is
given, re-run it independently from the stated inputs (venv, your own work dir) and report whether
you reproduce it; check DERIVED/READ labelling and whether the authors disclosed the point (grep
DECISIONS.md, REGISTRATION.md, progress.md, report.md, FINDINGS.md, docs/); check severity against
the definitions. Do not write files. Return one verdict per ID with specific correction text in
notes. DROP only when the quote cannot be found or the basis figure is wrong.`
}

const APPLIER_SCHEMA = { type: 'object', properties: { repo: { type: 'string' }, kept: { type: 'integer' }, corrected: { type: 'integer' }, dropped: { type: 'integer' }, final_ids: { type: 'array', items: { type: 'string' } } }, required: ['repo','kept','corrected','dropped','final_ids'] }

function applierPrompt(repo, v) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
APPLIER inside Agent C for repository ${repo}. Checker verdicts (JSON): ${JSON.stringify(v)}
Apply to ${OUT}/${repo}.md and ${OUT}/${repo}.json after confirming each correction yourself against
${SNAP}/${repo}/: DROP → move the finding's text to "## Dropped after verification" with the reason
and remove from json (do not renumber); CORRECT → fix the field and append "- **Citation check:**
corrected — <what changed>"; KEEP → append "- **Citation check:** verified (quote ..., figures ...,
recomputation ...)". Keep json in sync. Return counts and final IDs.`
}

async function repoChain(repo) {
  const inv = await agent(locatePrompt(repo), { model: 'opus', label: `C-locate:${repo}`, phase: 'Locate', schema: LOCATE_SCHEMA })
  if (!inv) return { repo, stage: 'locate-failed' }
  const [ver, prov] = await parallel([
    () => agent(verifyPrompt(repo, inv), { label: `C-verify:${repo}`, phase: 'Verify' }),
    () => agent(provenancePrompt(repo, inv), { label: `C-provenance:${repo}`, phase: 'Provenance' }),
  ])
  if (!ver || !prov) return { repo, stage: 'verify-or-provenance-failed', ver: !!ver, prov: !!prov }
  const c = await agent(consolidatorPrompt(repo), { model: 'opus', label: `C-consolidate:${repo}`, phase: 'Consolidate', schema: CONSOLIDATOR_SCHEMA })
  if (!c) return { repo, stage: 'consolidate-failed' }
  if (c.n_findings === 0) { log(`${repo}: no C findings to check`); return { repo, stage: 'done', consolidated: c, applied: null } }
  const v = await agent(verifierPrompt(repo), { model: 'opus', label: `C-check:${repo}`, phase: 'Check', schema: VERIFIER_SCHEMA })
  if (!v) return { repo, stage: 'check-failed', consolidated: c }
  const a = await agent(applierPrompt(repo, v), { model: 'opus', label: `C-apply:${repo}`, phase: 'Check', schema: APPLIER_SCHEMA })
  return { repo, stage: a ? 'done' : 'apply-failed', consolidated: c, applied: a }
}

phase('Locate')
const results = []
for (let i = 0; i < REPOS.length; i += BATCH) {
  const batch = REPOS.slice(i, i + BATCH)
  log(`batch ${i / BATCH + 1}: ${batch.join(', ')}`)
  const res = await parallel(batch.map(r => () => repoChain(r)))
  results.push(...res.filter(Boolean))
}
const incomplete = results.filter(r => r.stage !== 'done').map(r => `${r.repo}:${r.stage}`)
if (incomplete.length) log(`incomplete: ${incomplete.join(', ')}; resume after the limit resets`)
return results.map(r => ({ repo: r.repo, stage: r.stage, consolidated: r.consolidated || null, applied: r.applied || null }))
