export const meta = {
  name: 'agentA-blind',
  description: 'Agent A blind pass: thesis "closed too early" over 13 repos, per-repo readers, consolidation, citation verification, cross-repo reopen triggers',
  phases: [
    { title: 'Read', detail: 'advocate readers per repository (large repos split by document set)' },
    { title: 'Consolidate', detail: 'one consolidator per repository assigns IDs, writes md + json' },
    { title: 'Verify', detail: 'two independent citation verifiers per repository' },
    { title: 'Apply', detail: 'apply verifier verdicts: keep / correct / drop' },
    { title: 'Cross-repo', detail: 'reopen conditions met by later work in other repositories' },
  ],
}

const RULES_PATH = '/home/kiros-li/.cache/program-audit/scratchpad/COMMON_RULES.md'
const SNAP = '/home/kiros-li/.cache/program-audit/scratchpad/snap'
const OUT = '/home/kiros-li/Documents/GitHub/program-audit/findings/agentA'

const THESIS = `
YOU ARE AGENT A. Your thesis: this program closed hypotheses too early or too hard.
Build the strongest HONEST case that work was abandoned prematurely. You are an advocate, not a
neutral reviewer, but you may not invent evidence and you may not misquote. Most entries in these
repositories are negative results; agreeing with a negative result is free, so your job is to find
where the negative was reached on weaker grounds than its label implies.

Hunt specifically for:
 1. A closure resting on a variant never tested (a parameterisation, horizon, universe, venue,
    endpoint or estimator that the registration or discussion names but that was never run).
 2. A stated blocker that has since expired (an access, licence, data, account, jurisdiction, cost
    or tooling blocker that a later dated entry in THIS repository shows was lifted, measured
    differently, or superseded), where the closure label was not revisited.
 3. A reopening condition whose trigger has already been met (compare each registered reopen
    condition against later entries in the same repository; note any that might be met by work in
    a DIFFERENT repository and list them separately for the cross-repo pass).
 4. A sample dismissed as too thin where the arithmetic does not support the dismissal (recompute:
    with the stated n, effect and dispersion, what power or interval actually results?).
 5. A closure label harsher than its own deciding number (e.g. "signal-absent" where the point
    estimate is on the hypothesis side and the interval is wide; "falsified" where the bar was
    missed narrowly; "BLOCKED" where a cheaper path was named and not tried).
 6. An untestable-at-achievable-power verdict where a different endpoint with better
    signal-to-noise was available in the same design and not considered.
 7. A data-availability closure where an alternative source exists (named anywhere in this
    repository, or known to you with a concrete citation you can state).

For each candidate, extract the deciding number and its n from the document, and the closure
kind/label. Where the closure rests on arithmetic, recompute it (power, interval, ratio) with the
Python provided and show your working with file:line for every input.

Also produce a REOPEN LEDGER for the repository: every hypothesis/entry with its status
(open/closed/parked/shipped/blocked), closure kind, closure date, the deciding figure with n and
file:line, every stated blocker with file:line, and every registered reopen condition with
file:line. This ledger is factual, not advocacy; it feeds the cross-repository pass.
`

const FINDING_BLOCK = `
Write each finding as a markdown block with EXACTLY these field lines, in this order:
### <ID>
- **Repository / SHA:** <repo> / <sha>
- **Hypothesis or artifact:** ...
- **Direction:** A
- **Class:** ...
- **Severity:** S1|S2|S3|S4
- **Label:** DERIVED|READ
- **Claim challenged (verbatim quote):** "..." — <repo>/<path>:<line>
- **Evidence:** ... (figures with n, each with <repo>/<path>:<line> or data path + UTC read time)
- **Recomputation (if any):** inputs with file:line, method, result
- **What would resolve it:** ...
- **Confidence:** HIGH|MEDIUM|LOW — <one sentence>
- **Invalidated by later commits?:** yes|no — <why>
- **Disclosed by authors?:** yes (<file:line>)|no — <one sentence>
`

const REPO_PARTS = [
  { repo: 'AiTrader', parts: [
    { part: 'p1-experiment', docs: 'EXPERIMENT.md, AUDIT.md, AUDIT-2026-07-29.md, DATA_AUDIT.md, LIVE_READINESS.md, COLLECTION_LOG.md, WEEKLOG.md, docs/' },
    { part: 'p2-return', docs: 'RETURN.md (7991 lines; read all of it in chunks)' },
    { part: 'p3-progress', docs: 'PROGRESS.md, CONTEXT.md, README.md (Market AI Lab), news_experiment/, research_satellite/, and any stored ledgers or JSON/CSV under the snapshot' },
  ]},
  { repo: 'ETFExperiment', parts: [ { part: 'all', docs: 'every markdown file, reports/, scripts/, src/ as needed' } ] },
  { repo: 'HFExperiment', parts: [ { part: 'all', docs: 'every markdown file, reports/, scripts/, src/ as needed' } ] },
  { repo: 'InsiderExperiment', parts: [ { part: 'all', docs: 'every markdown file, reports/, scripts/, src/ as needed' } ] },
  { repo: 'MLCryptoEngine', parts: [
    { part: 'p1-report', docs: 'report.md (5190 lines; read all of it in chunks), README.md' },
    { part: 'p2-register', docs: 'HYPOTHESES.md, DECISIONS.md (2701 lines), AUDIT.md, docs/notes/, audit/' },
    { part: 'p3-progress', docs: 'progress.md (2977 lines), research/ (notebooks, docs, stored artifacts), backtest/' },
  ]},
  { repo: 'NPDExperiment', parts: [ { part: 'all', docs: 'every markdown file, reports/, scripts/, src/ as needed' } ] },
  { repo: 'NPLExperiment', parts: [
    { part: 'p1-registrations', docs: 'REGISTRATION.md, registrations/H2..H5/REGISTRATION.md, HYPOTHESES.md, report.md, README.md' },
    { part: 'p2-progress', docs: 'DECISIONS.md, progress.md (1556 lines), docs/ (ACCESS, H5_ACCESS, PAIR_FEASIBILITY, STAGES, SUBSTRATE), reports/' },
  ]},
  { repo: 'ORBExperiment', parts: [
    { part: 'p1-registration', docs: 'REGISTRATION.md (4193 lines; read all of it in chunks), HYPOTHESES.md, report.md' },
    { part: 'p2-decisions', docs: 'DECISIONS.md, README.md, docs/ (ACCESS, DUPLICATION, HANDOVER, STAGES, STAGE_A_PROMPT), reports/*.md' },
    { part: 'p3-progress', docs: 'progress.md (3737 lines; read all of it in chunks), reports/ artifacts (json/csv), tools/' },
  ]},
  { repo: 'PMExperiment', parts: [
    { part: 'p1-register', docs: 'REGISTRATION.md, HYPOTHESES.md, DECISIONS.md, report.md, README.md' },
    { part: 'p2-progress', docs: 'progress.md (1651 lines), docs/ (ACCESS, BAND, LICENCES), pmexperiment/, data/' },
  ]},
  { repo: 'VRPExperiment', parts: [ { part: 'all', docs: 'every markdown file, docs/, reports/, tools/, src/ as needed' } ] },
  { repo: 'retail-power-limits', parts: [ { part: 'all', docs: 'every markdown file, docs/, rplimits/' } ] },
  { repo: 'solattn', parts: [
    { part: 'p1-register', docs: 'REGISTRATION.md, FINDINGS.md, DECISIONS.md, README.md, docs/*.md' },
    { part: 'p2-progress', docs: 'progress.md (2936 lines; read all of it in chunks), docs/ non-md artifacts, ops/, solattn/ code as needed' },
  ]},
  { repo: 'solclear', parts: [
    { part: 'p1-findings', docs: 'FINDINGS.md, README.md, METHOD_B.md, DECISIONS.md' },
    { part: 'p2-progress', docs: 'progress.md (1849 lines), data/, scripts/, solclear/ code as needed' },
  ]},
]

function readerPrompt(repo, part, docs, allParts) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${THESIS}
YOUR ASSIGNMENT: repository ${repo}, part "${part}". Read from ${SNAP}/${repo}/ only (plus the live
repo's git history and untracked data, read-only, per the rules). Your PRIMARY documents: ${docs}.
${allParts > 1 ? `This repository is split across ${allParts} readers by document set. Other readers cover the other documents. You MAY read any file in the snapshot for context, but raise findings whose primary evidence lies in your assigned documents; if you notice a strong candidate in another reader's documents, still record it (dedup happens later) but mark it "primary evidence outside my assignment".` : 'You are the only reader for this repository; read everything relevant.'}
Read the primary documents COMPLETELY (use sed -n or the Read tool in chunks; do not skim
headers only). Grep the rest of the repository for the hypotheses, blockers and reopen conditions
you encounter.

OUTPUT (write these two files; create the directory):
 1. ${OUT}/_drafts/${repo}/${part}.md — your draft findings. Use temporary IDs DRAFT-${part}-<k>.
    ${FINDING_BLOCK}
    After the findings, add a section "## What I checked and found sound" listing what you examined
    where the thesis did NOT hold, with file references. If you found no findings at all, say so
    plainly and give that list in full.
    Add a section "## Live-repo access log" with the before/after git status --porcelain outputs if
    you touched the live repo, or "none" if you did not.
 2. ${OUT}/_drafts/${repo}/${part}.reopen.md — the REOPEN LEDGER for the entries covered by your
    documents (table or list: entry | status | closure kind | closure date | deciding figure (n) |
    file:line | blockers (file:line) | reopen conditions (file:line) | possibly-met-by-other-repo?).

Your final message: a short plain-text summary: number of draft findings by severity, and one line
per finding (temporary ID, class, severity, one-sentence claim).`
}

const CONSOLIDATOR_SCHEMA = {
  type: 'object',
  properties: {
    repo: { type: 'string' },
    n_findings: { type: 'integer' },
    findings: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, class: { type: 'string' }, severity: { type: 'string' }, label: { type: 'string' }, one_line: { type: 'string' }
    }, required: ['id','class','severity','label','one_line'] } },
    sound_areas: { type: 'array', items: { type: 'string' } },
    cross_repo_leads: { type: 'array', items: { type: 'string' } },
  },
  required: ['repo','n_findings','findings','sound_areas','cross_repo_leads'],
}

function consolidatorPrompt(repo, parts) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
You are the CONSOLIDATOR for Agent A on repository ${repo}. Agent A's thesis: the program closed
hypotheses too early or too hard. You are still Agent A: an honest advocate.

INPUT: the draft files ${parts.map(p => `${OUT}/_drafts/${repo}/${p}.md`).join(', ')} and the reopen
ledgers ${parts.map(p => `${OUT}/_drafts/${repo}/${p}.reopen.md`).join(', ')}. Read them all.
You have access to ${SNAP}/${repo}/ to check anything.

TASKS:
 1. Merge duplicates (same claim challenged, or same closure attacked on the same grounds) into
    one finding, keeping the strongest evidence and every distinct file:line.
 2. Assign stable IDs AUDIT-A-${repo}-1, -2, ... in descending severity order (S1 first).
 3. Enforce the format: every field present; verbatim quote with file:line; figures with n;
    Label DERIVED only if the evidence came from data, code, or a git object (a recomputation from
    numbers printed in a document is READ unless the inputs were taken from stored data/code);
    "Disclosed by authors?" honest — if disclosed, severity capped at S3 and the text says so.
 4. Drop anything that lacks a locatable quote, a figure, or an n; record what you dropped and why
    in a "## Dropped at consolidation" section.
 5. Write ${OUT}/${repo}.md with: a 3-6 line summary of the strongest case for the thesis in this
    repository; the findings in the standard block format; "## What Agent A checked and found
    sound"; "## Dropped at consolidation"; "## Live-repo access log" (merged from drafts).
 6. Write ${OUT}/${repo}.reopen.md: the merged, de-duplicated REOPEN LEDGER, with a final section
    "## Leads for the cross-repository pass" listing every blocker or reopen condition that might be
    satisfied by work in another repository, with your best guess of which repository.
 7. Write ${OUT}/${repo}.json: a JSON array, one object per finding, keys exactly:
    id, repo, sha, agent ("A"), direction ("A"), hypothesis_or_artifact, class, severity, label,
    claim_quote, claim_file, claim_line, evidence_summary, evidence_refs (array of "repo/path:line"
    strings), recomputation (string or null), would_resolve, confidence, confidence_why,
    invalidated_by_later_commits (bool), invalidation_note, disclosed_by_authors (bool),
    disclosure_ref (string or null).
Return the structured summary.`
}

const VERIFIER_SCHEMA = {
  type: 'object',
  properties: {
    repo: { type: 'string' },
    verdicts: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' },
      quote_found: { type: 'string', enum: ['EXACT','NEAR','NOT_FOUND'] },
      quote_line_ok: { type: 'boolean' },
      figures_ok: { type: 'string', enum: ['YES','PARTIAL','NO','NA'] },
      n_present: { type: 'boolean' },
      label_ok: { type: 'boolean' },
      disclosed_by_authors: { type: 'boolean' },
      disclosure_ref: { type: 'string' },
      severity_ok: { type: 'boolean' },
      recommendation: { type: 'string', enum: ['KEEP','CORRECT','DROP'] },
      notes: { type: 'string' },
    }, required: ['id','quote_found','quote_line_ok','figures_ok','n_present','label_ok','disclosed_by_authors','severity_ok','recommendation','notes'] } },
  },
  required: ['repo','verdicts'],
}

function verifierPrompt(repo, k) {
  const lens = k === 1
    ? 'Your lens: CITATION FIDELITY. For every finding, grep the snapshot for the quoted text; confirm the file and that the line number is right (within 3 lines counts as NEAR). Confirm every figure and n cited in the evidence actually appears at the cited location. Any quote that cannot be found, or any figure that differs from the source, is a DROP or CORRECT.'
    : 'Your lens: DISCLOSURE AND LABELLING. For every finding, search the repository (grep the snapshot, especially DECISIONS.md, REGISTRATION.md, HYPOTHESES.md, progress.md, report.md, docs/) for whether the authors themselves already disclose the limitation the finding raises. If they do, the finding must be labelled READ, capped at S3, and must say so; if it does not, recommend CORRECT with the disclosure_ref. Also check that DERIVED is only used where the evidence came from data, code or a git object, and that severity matches the definitions (S1 conclusion wrong/unsupported; S2 label contradicts its own evidence; S3 stale blocker or figure; S4 hygiene).'
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
You are an independent VERIFIER inside Agent A for repository ${repo}. You do not judge whether
Agent A's thesis is right; you check that each finding in ${OUT}/${repo}.md (and ${OUT}/${repo}.json)
is honestly cited and honestly labelled. ${lens}
Read the findings file, then check every finding against ${SNAP}/${repo}/ (read-only). Do not
write any file. Return one verdict per finding ID. Default to CORRECT rather than DROP when the
substance is real but a detail is off; DROP only when the quote cannot be found, the figure is
wrong in a way that removes the basis, or no n exists anywhere for the figure. Put the specific
correction text in notes.`
}

const APPLIER_SCHEMA = {
  type: 'object',
  properties: { repo: { type: 'string' }, kept: { type: 'integer' }, corrected: { type: 'integer' }, dropped: { type: 'integer' }, final_ids: { type: 'array', items: { type: 'string' } } },
  required: ['repo','kept','corrected','dropped','final_ids'],
}

function applierPrompt(repo, v1, v2) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
You are the APPLIER inside Agent A for repository ${repo}. Two independent verifiers reviewed
${OUT}/${repo}.md. Their verdicts (JSON):
VERIFIER 1 (citation fidelity): ${JSON.stringify(v1)}
VERIFIER 2 (disclosure and labelling): ${JSON.stringify(v2)}
Apply them to ${OUT}/${repo}.md and ${OUT}/${repo}.json, checking each correction yourself against
${SNAP}/${repo}/ before applying it:
 - DROP if either verifier found the quote NOT_FOUND or figures NO and you confirm it; move the
   finding's full text to a "## Dropped after verification" section at the end of the md with the
   reason, and remove it from the json. Do NOT renumber remaining IDs.
 - CORRECT: fix the line number, quote, figure, label, severity or disclosure field as indicated,
   and append a field line "- **Citation check:** corrected — <what changed>" to the finding.
 - KEEP: append "- **Citation check:** verified (quote ${'EXACT|NEAR'}, figures ${'YES|PARTIAL'})".
 - If the verifiers disagree, check the source yourself and record which you followed and why in
   the Citation check line.
Keep the json in sync with the md. Return the counts and the final list of IDs.`
}

// ---- Phase 1-4: per-repository chain, THROTTLED ----
// Account usage limits killed two full-parallel runs with nothing banked. Run at most BATCH
// repositories at a time, smallest first, so completed agents are cached and survive a limit hit.
const ORDER = ['retail-power-limits','HFExperiment','InsiderExperiment','NPDExperiment','VRPExperiment','ETFExperiment','solclear','PMExperiment','solattn','NPLExperiment','MLCryptoEngine','ORBExperiment','AiTrader']
const BATCH = 2
const byName = Object.fromEntries(REPO_PARTS.map(rp => [rp.repo, rp]))
// Disk-state driven skipping. The runtime's resume cache is positional (longest unchanged prefix
// of agent() calls); with two chains interleaving and partial failures the order shifts and
// completed agents re-run, overwriting verified output. tools/agent_state.py scans the output
// directory and passes {done_repos, done_parts, leads} as args; every launch is fresh.
const STATE = args || {}
const DONE_REPOS = new Set(STATE.done_repos || [])
const DONE_PARTS = STATE.done_parts || {}
const DISK_LEADS = STATE.leads || []
const LEADS_FILE = STATE.leads_file || '/home/kiros-li/Documents/GitHub/program-audit/provenance/launch-args/agentA-leads.json'
const CONSOLIDATED = STATE.consolidated || {}   // repo -> n_findings, consolidator done but verify/apply not
async function repoChain(rp) {
  const parts = rp.parts.map(p => p.part)
  if (DONE_REPOS.has(rp.repo)) {
    log(`${rp.repo}: complete on disk, skipped`)
    return { repo: rp.repo, parts, drafts: parts.length, consolidated: { n_findings: -1, cross_repo_leads: [] }, applied: 'on-disk', skipped: true }
  }
  const partsDone = new Set(DONE_PARTS[rp.repo] || [])
  if (partsDone.size) log(`${rp.repo}: reader draft(s) on disk for ${[...partsDone].join(', ')}, skipped`)
  const drafts = await parallel(rp.parts.map(p => () => partsDone.has(p.part)
    ? Promise.resolve('on-disk')
    : agent(readerPrompt(rp.repo, p.part, p.docs, rp.parts.length), { model: 'opus', label: `A-read:${rp.repo}:${p.part}`, phase: 'Read' })))
  const r = { repo: rp.repo, parts, drafts: drafts.filter(Boolean).length }
  if (r.drafts < rp.parts.length) { log(`${rp.repo}: ${r.drafts}/${rp.parts.length} readers completed; consolidation deferred to a resume`); return { ...r, consolidated: null, applied: null } }
  if (r.repo in CONSOLIDATED) log(`${r.repo}: consolidated output on disk (${CONSOLIDATED[r.repo]} findings), consolidate skipped`)
  const c = (r.repo in CONSOLIDATED)
    ? { n_findings: CONSOLIDATED[r.repo], cross_repo_leads: [], on_disk: true }
    : await agent(consolidatorPrompt(r.repo, r.parts), { model: 'opus', label: `A-consolidate:${r.repo}`, phase: 'Consolidate', schema: CONSOLIDATOR_SCHEMA })
  if (!c) return { ...r, consolidated: null, applied: null }
  if (c.n_findings === 0) { log(`${r.repo}: no findings to verify`); return { ...r, consolidated: c, applied: null } }
  const [v1, v2] = await parallel([
    () => agent(verifierPrompt(r.repo, 1), { model: 'opus', label: `A-verify1:${r.repo}`, phase: 'Verify', schema: VERIFIER_SCHEMA }),
    () => agent(verifierPrompt(r.repo, 2), { model: 'opus', label: `A-verify2:${r.repo}`, phase: 'Verify', schema: VERIFIER_SCHEMA }),
  ])
  if (!v1 && !v2) return { ...r, consolidated: c, applied: null }
  const a = await agent(applierPrompt(r.repo, v1, v2), { model: 'opus', label: `A-apply:${r.repo}`, phase: 'Apply', schema: APPLIER_SCHEMA })
  return { ...r, consolidated: c, applied: a }
}
phase('Read')
const perRepo = []
for (let i = 0; i < ORDER.length; i += BATCH) {
  const batch = ORDER.slice(i, i + BATCH).map(n => byName[n])
  log(`batch ${i / BATCH + 1}: ${batch.map(b => b.repo).join(', ')}`)
  const res = await parallel(batch.map(rp => () => repoChain(rp)))
  perRepo.push(...res.filter(Boolean))
}

// ---- Phase 5: cross-repository pass (needs every reopen ledger) ----
phase('Cross-repo')
const done = perRepo.filter(Boolean)
const incomplete = ORDER.filter(n => !done.find(d => d.repo === n && d.consolidated && (d.consolidated.n_findings === 0 || d.applied)))
if (incomplete.length) { log(`cross-repo pass deferred; incomplete: ${incomplete.join(', ')}`); return { repos: done, incomplete } }
const leads = [...DISK_LEADS, ...done.flatMap(r => (r.consolidated && r.consolidated.cross_repo_leads) ? r.consolidated.cross_repo_leads.map(l => `${r.repo}: ${l}`) : [])]
const cross = await agent(`First run: cat ${RULES_PATH}   and follow every rule in it.
${THESIS}
You are Agent A's CROSS-REPOSITORY reader. All thirteen per-repository passes are complete. Read
every reopen ledger ${OUT}/*.reopen.md and every findings file ${OUT}/*.md (these are Agent A's own
output; you may read them). The consolidators flagged these leads:
${leads.length ? leads.map(l => ' - ' + l).join('\n') : ' (none flagged; build your own list from the ledgers)'}
Also read ${LEADS_FILE}: a JSON array of lead strings accumulated from every consolidator across all runs of this pass; treat it as part of the same list and cover every lead in it.

TASK: for every stated blocker and every registered reopen condition in any repository, determine
whether a DIFFERENT repository's later, dated work has already met it (an access obtained, a venue
measured reachable, a cost measured below a hurdle, a data source found, a licence or jurisdiction
question resolved, a tool built, a vendor tier confirmed). Read the relevant snapshot files in both
repositories and cite both sides with file:line and dates. Also look for data-availability closures
in one repository where another repository actually obtained or measured that data.
Only raise a finding where the trigger is concretely met on the evidence, not merely plausible.
Distinguish: (a) trigger met and closure not revisited; (b) trigger met and the repository noticed
(then it is not a finding, but record it in a "## Triggers met and already handled" section);
(c) trigger partially met (record under "## Partial", not as findings).

OUTPUT: ${OUT}/CROSS_REPO.md with findings in the standard block format. IDs continue each target
repository's numbering: read ${OUT}/<repo>.json to find the highest n for that repository and start
at n+1 (the target repository is the one whose closure is challenged). Class is usually
CROSS_REPO_INCONSISTENCY or OVER_CLOSED. Also write ${OUT}/CROSS_REPO.json in the same JSON
shape as the per-repository json files (keys: id, repo, sha, agent, direction,
hypothesis_or_artifact, class, severity, label, claim_quote, claim_file, claim_line,
evidence_summary, evidence_refs, recomputation, would_resolve, confidence, confidence_why,
invalidated_by_later_commits, invalidation_note, disclosed_by_authors, disclosure_ref), adding a
key "other_repo_refs" (array of "repo/path:line"). Include the "Triggers met and already handled"
and "Partial" sections in the md. Return a plain summary of counts and one line per finding.`,
  { label: 'A-cross-repo', phase: 'Cross-repo' })

return {
  repos: done.map(r => ({ repo: r.repo, drafts: r.drafts, n: r.consolidated ? r.consolidated.n_findings : null, applied: r.applied })),
  cross: typeof cross === 'string' ? cross.slice(0, 4000) : cross,
}