export const meta = {
  name: 'agentB-blind',
  description: 'Agent B blind pass: thesis "claimed more than it earned" over 13 repos, per-repo readers, consolidation, citation verification, cross-repo standards pass',
  phases: [
    { title: 'Read', detail: 'sceptic readers per repository (large repos split by document set)' },
    { title: 'Consolidate', detail: 'one consolidator per repository assigns IDs, writes md + json' },
    { title: 'Verify', detail: 'two independent citation verifiers per repository' },
    { title: 'Apply', detail: 'apply verifier verdicts: keep / correct / drop' },
    { title: 'Cross-repo', detail: 'standards applied unevenly across repositories; shipped artifacts' },
  ],
}

const RULES_PATH = '/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/COMMON_RULES.md'
const SNAP = '/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/snap'
const OUT = '/home/kiros-li/Documents/GitHub/program-audit/findings/agentB'

const THESIS = `
YOU ARE AGENT B. Your thesis: this program claimed more than it earned.
Build the strongest HONEST case that conclusions outran evidence. You are a sceptic, not a neutral
reviewer, but you may not invent evidence and you may not misquote. Apply MAXIMUM scrutiny to every
positive, qualified positive, shipped artifact and open hypothesis: a positive inside a corpus of
negatives is the one thing that would be acted on, so it earns more scrutiny than the negatives,
not less. Negatives are not exempt: a negative reached by a process that would also have produced a
positive on noise is a claim that outran its evidence.

Hunt specifically for:
 1. A positive that does not survive the correction the negatives received (multiplicity, cost
    model, fill model, survivorship, look-ahead, clustering) — compare the standard applied to each
    positive with the standard the same repository applied to its negatives.
 2. A bar lowered, widened or re-specified after data existed (compare amendment dates and the
    amendment's own statement of what data existed against progress.md, git history and stored
    artifact timestamps).
 3. An amendment that rescued a verdict rather than recording a falsification.
 4. A limitation disclosed in one field (a footnote, an epistemic-boundary section, a progress
    entry) and absent from the conclusion, the README, the register entry or the shipped artifact's
    framing.
 5. A selection or screen preceding a test and uncorrected (universe filters, venue selection,
    date-range choice, parameter picks, "culled at registration" candidates that informed the
    survivor).
 6. An open hypothesis that should already have closed on its own registered rule.
 7. A shipped artifact (a tool, a detector, a table, a dataset, a "power limit", a cost table)
    whose support is weaker than its framing.
 8. A power figure resting on an assumption the repository elsewhere calls falsified or
    unmeasured (effect size, dispersion, base rate, independence, fill rate, cost).

For each candidate, extract the claim verbatim, the deciding numbers with n, and the standard the
repository set for itself (its own registration, guard set or decision rule). Where the claim rests
on arithmetic, recompute it with the Python provided and show your working with file:line for every
input. Where git history is needed to date a change against data existence, use the live
repository's git log/show/blame read-only and cite the commits.

Also produce a POSITIVES LEDGER for the repository: every positive, qualified positive, shipped
artifact, open hypothesis, and every negative whose verdict rested on a threshold. For each: the
claim as stated (file:line), the deciding figures with n, the bar and its registration date, any
amendment touching the bar with date and what data existed, the corrections applied, and the
framing used in README/report/register. This ledger is factual, not advocacy; it feeds the
cross-repository pass.
`

const FINDING_BLOCK = `
Write each finding as a markdown block with EXACTLY these field lines, in this order:
### <ID>
- **Repository / SHA:** <repo> / <sha>
- **Hypothesis or artifact:** ...
- **Direction:** B
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
headers only). Grep the rest of the repository for the claims, bars, amendments and artifacts you
encounter. Where analysis code or stored artifacts exist in the snapshot, open them: a claim that
the code contradicts is the strongest kind of finding (DERIVED).

OUTPUT (write these two files; create the directory):
 1. ${OUT}/_drafts/${repo}/${part}.md — your draft findings. Use temporary IDs DRAFT-${part}-<k>.
    ${FINDING_BLOCK}
    After the findings, add a section "## What I checked and found sound" listing what you examined
    where the thesis did NOT hold, with file references. If you found no findings at all, say so
    plainly and give that list in full.
    Add a section "## Live-repo access log" with the before/after git status --porcelain outputs if
    you touched the live repo, or "none" if you did not.
 2. ${OUT}/_drafts/${repo}/${part}.positives.md — the POSITIVES LEDGER for the entries covered by
    your documents (table or list: claim | kind (positive / qualified positive / shipped / open /
    thresholded negative) | deciding figures (n) | file:line | bar + registration date | amendments
    touching the bar (date, data existed?) | corrections applied | framing in README/report).

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
You are the CONSOLIDATOR for Agent B on repository ${repo}. Agent B's thesis: the program claimed
more than it earned. You are still Agent B: an honest sceptic.

INPUT: the draft files ${parts.map(p => `${OUT}/_drafts/${repo}/${p}.md`).join(', ')} and the positives
ledgers ${parts.map(p => `${OUT}/_drafts/${repo}/${p}.positives.md`).join(', ')}. Read them all.
You have access to ${SNAP}/${repo}/ to check anything.

TASKS:
 1. Merge duplicates (same claim challenged on the same grounds) into one finding, keeping the
    strongest evidence and every distinct file:line.
 2. Assign stable IDs AUDIT-B-${repo}-1, -2, ... in descending severity order (S1 first).
 3. Enforce the format: every field present; verbatim quote with file:line; figures with n;
    Label DERIVED only if the evidence came from data, code, or a git object (a recomputation from
    numbers printed in a document is READ unless the inputs were taken from stored data/code);
    "Disclosed by authors?" honest — if disclosed, severity capped at S3 and the text says so.
 4. Drop anything that lacks a locatable quote, a figure, or an n; record what you dropped and why
    in a "## Dropped at consolidation" section.
 5. Write ${OUT}/${repo}.md with: a 3-6 line summary of the strongest case for the thesis in this
    repository; the findings in the standard block format; "## What Agent B checked and found
    sound"; "## Dropped at consolidation"; "## Live-repo access log" (merged from drafts).
 6. Write ${OUT}/${repo}.positives.md: the merged, de-duplicated POSITIVES LEDGER, with a final
    section "## Leads for the cross-repository pass": positives or artifacts here that another
    repository relies on, and standards applied here that look laxer or stricter than the house
    norm, with your best guess of the comparison repository.
 7. Write ${OUT}/${repo}.json: a JSON array, one object per finding, keys exactly:
    id, repo, sha, agent ("B"), direction ("B"), hypothesis_or_artifact, class, severity, label,
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
    ? 'Your lens: CITATION FIDELITY. For every finding, grep the snapshot for the quoted text; confirm the file and that the line number is right (within 3 lines counts as NEAR). Confirm every figure and n cited in the evidence actually appears at the cited location, and that any git commit cited exists in the live repository (git -C <live> cat-file -t <sha>, read-only). Any quote that cannot be found, or any figure that differs from the source, is a DROP or CORRECT.'
    : 'Your lens: DISCLOSURE AND LABELLING. For every finding, search the repository (grep the snapshot, especially DECISIONS.md, REGISTRATION.md, HYPOTHESES.md, progress.md, report.md, FINDINGS.md, docs/) for whether the authors themselves already disclose the limitation the finding raises, in the same place the claim is made or in a linked section. If they do, the finding must be labelled READ, capped at S3, and must say so; if it does not, recommend CORRECT with the disclosure_ref. A limitation disclosed in a footnote but absent from the conclusion or the framing is NOT a full disclosure for a finding about the framing; say which case applies. Also check that DERIVED is only used where the evidence came from data, code or a git object, and that severity matches the definitions (S1 conclusion wrong/unsupported; S2 label contradicts its own evidence; S3 stale blocker or figure; S4 hygiene).'
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
You are an independent VERIFIER inside Agent B for repository ${repo}. You do not judge whether
Agent B's thesis is right; you check that each finding in ${OUT}/${repo}.md (and ${OUT}/${repo}.json)
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
You are the APPLIER inside Agent B for repository ${repo}. Two independent verifiers reviewed
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
 - KEEP: append "- **Citation check:** verified (quote EXACT|NEAR, figures YES|PARTIAL)".
 - If the verifiers disagree, check the source yourself and record which you followed and why in
   the Citation check line.
Keep the json in sync with the md. Return the counts and the final list of IDs.`
}

// ---- per-repository chain, THROTTLED (two repositories at a time, smallest first) ----
const ORDER = ['retail-power-limits','HFExperiment','InsiderExperiment','NPDExperiment','VRPExperiment','ETFExperiment','solclear','PMExperiment','solattn','NPLExperiment','MLCryptoEngine','ORBExperiment','AiTrader']
const BATCH = 2
const byName = Object.fromEntries(REPO_PARTS.map(rp => [rp.repo, rp]))
async function repoChain(rp) {
  const drafts = await parallel(rp.parts.map(p => () =>
    agent(readerPrompt(rp.repo, p.part, p.docs, rp.parts.length), { label: `B-read:${rp.repo}:${p.part}`, phase: 'Read' })))
  const r = { repo: rp.repo, parts: rp.parts.map(p => p.part), drafts: drafts.filter(Boolean).length }
  if (r.drafts < rp.parts.length) { log(`${rp.repo}: ${r.drafts}/${rp.parts.length} readers completed; consolidation deferred to a resume`); return { ...r, consolidated: null, applied: null } }
  const c = await agent(consolidatorPrompt(r.repo, r.parts), { model: 'opus', label: `B-consolidate:${r.repo}`, phase: 'Consolidate', schema: CONSOLIDATOR_SCHEMA })
  if (!c) return { ...r, consolidated: null, applied: null }
  if (c.n_findings === 0) { log(`${r.repo}: no findings to verify`); return { ...r, consolidated: c, applied: null } }
  const [v1, v2] = await parallel([
    () => agent(verifierPrompt(r.repo, 1), { model: 'opus', label: `B-verify1:${r.repo}`, phase: 'Verify', schema: VERIFIER_SCHEMA }),
    () => agent(verifierPrompt(r.repo, 2), { model: 'opus', label: `B-verify2:${r.repo}`, phase: 'Verify', schema: VERIFIER_SCHEMA }),
  ])
  if (!v1 && !v2) return { ...r, consolidated: c, applied: null }
  const a = await agent(applierPrompt(r.repo, v1, v2), { model: 'opus', label: `B-apply:${r.repo}`, phase: 'Apply', schema: APPLIER_SCHEMA })
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

phase('Cross-repo')
const done = perRepo.filter(Boolean)
const incomplete = ORDER.filter(n => !done.find(d => d.repo === n && d.consolidated && (d.consolidated.n_findings === 0 || d.applied)))
if (incomplete.length) { log(`cross-repo pass deferred; incomplete: ${incomplete.join(', ')}`); return { repos: done, incomplete } }
const leads = done.flatMap(r => (r.consolidated && r.consolidated.cross_repo_leads) ? r.consolidated.cross_repo_leads.map(l => `${r.repo}: ${l}`) : [])
const cross = await agent(`First run: cat ${RULES_PATH}   and follow every rule in it.
${THESIS}
You are Agent B's CROSS-REPOSITORY reader. All thirteen per-repository passes are complete. Read
every positives ledger ${OUT}/*.positives.md and every findings file ${OUT}/*.md (Agent B's own
output; you may read them). The consolidators flagged these leads:
${leads.length ? leads.map(l => ' - ' + l).join('\n') : ' (none flagged; build your own list from the ledgers)'}

TASKS:
 (a) STANDARDS CONSISTENCY: the repositories share a house method (outcome maps, halved effect
     sizes, cost hurdles, guard sets, closure kinds). Compare the standard each positive, qualified
     positive or shipped artifact was held to against the standard the SAME house applied to
     negatives in other repositories (cost model, fill model, multiplicity, clustering, halved
     effect, measured-not-carried costs). A positive that would have failed under a standard the
     house applied elsewhere is a finding against the repository holding the positive.
 (b) SHIPPED ARTIFACTS RELIED ON ELSEWHERE: where repository X relies on an artifact, table, figure
     or closure produced by repository Y (a power limit, a cost table, a venue table, a detector, a
     calibration outcome), check that Y's support matches the framing X gives it. A downstream use
     that overstates the upstream support is a finding against X; an upstream artifact whose own
     framing exceeds its support is a finding against Y.
 (c) POWER ASSUMPTIONS FALSIFIED ELSEWHERE: a power figure in one repository resting on an
     assumption (effect size, dispersion, cost, fill rate, base rate) that another repository
     measured and found different.
Only raise a finding where the evidence is concrete on both sides; cite both with file:line and
dates. Record near-misses under "## Examined and not raised".

OUTPUT: ${OUT}/CROSS_REPO.md with findings in the standard block format. IDs continue each target
repository's numbering: read ${OUT}/<repo>.json to find the highest n for that repository and start
at n+1 (the target repository is the one whose claim is challenged). Class is usually
CROSS_REPO_INCONSISTENCY, UNSUPPORTED_POSITIVE or STATISTICAL. Also write ${OUT}/CROSS_REPO.json
in the same JSON shape as the per-repository json files, adding a key "other_repo_refs" (array of
"repo/path:line"). Return a plain summary of counts and one line per finding.`,
  { label: 'B-cross-repo', phase: 'Cross-repo' })

return {
  repos: done.map(r => ({ repo: r.repo, drafts: r.drafts, n: r.consolidated ? r.consolidated.n_findings : null, applied: r.applied })),
  cross: typeof cross === 'string' ? cross.slice(0, 4000) : cross,
}
