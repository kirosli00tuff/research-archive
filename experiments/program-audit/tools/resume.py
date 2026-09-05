#!/usr/bin/env python3
"""tools/resume.py — one-command resume for the program audit after a reboot or a session-limit hit.

Everything here is idempotent and read-only on the audited repositories (the only commands run against
them are `git rev-parse` and `git status --porcelain`, via tools/git_status_check.sh).

Default (safe while workflows may still be alive):
  1. verify the persistent scratchpad: 13 snapshots against provenance/snapshot-manifest.json (sha256),
     the recomputation venv, and COMMON_RULES.md (cache copy re-synced from the repo copy if it drifted);
  2. recreate the legacy /tmp scratchpad symlinks (tools/tmp_links.sh);
  3. bank cross-repo leads from every workflow journal into provenance/launch-args/agent{A,B}-leads.json;
  4. print the disk state of every blind pass and anything that needs recovery.

With --runs-dead (after a reboot, or once every workflow has reported):
  5. AFTER cleanliness check for every run in provenance/launch-args/ACTIVE.json, compared with
     DIRT_BASELINE.json (any new porcelain entry is reported loudly), then the run is moved to HISTORY.json;
  6. next args file per unfinished blind pass (run number auto-incremented, leads: []), BEFORE check,
     and the exact Workflow invocation to make; a RUN_LOG stub is appended.

--phase seeded|adjudication|D prints the state and args shape for the later phases instead of step 6.
--commit stages findings/agent{A,B,C}, findings/protocol, provenance, tools, work and RESUME.md (never
findings/independent/) and commits them with a generated message; --session-url adds the trailer.
"""
import argparse, datetime, glob, hashlib, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROV = os.path.join(ROOT, 'provenance')
LA = os.path.join(PROV, 'launch-args')
CACHE = '/home/kiros-li/.cache/program-audit/scratchpad'
SNAP = os.path.join(CACHE, 'snap')
VENV_PY = os.path.join(CACHE, 'venv', 'bin', 'python')
JOURNAL_GLOB = os.path.expanduser('~/.claude/projects/-home-kiros-li-Documents-GitHub-program-audit/*/subagents/workflows/*/journal.jsonl')
MIN_DRAFT_BYTES = 400
AGENTS = {
    'A': dict(outdir='findings/agentA', ledger='reopen', script='findings/protocol/agentA-blind.workflow.js', prefix='01-agentA-blind', leads='agentA-leads.json'),
    'B': dict(outdir='findings/agentB', ledger='positives', script='findings/protocol/agentB-blind.workflow.js', prefix='02-agentB-blind', leads='agentB-leads.json'),
    'C': dict(outdir='findings/agentC', ledger=None, script='findings/protocol/agentC-blind.workflow.js', prefix='03-agentC-blind', leads=None),
}
LATER = {
    'seeded': dict(script='findings/protocol/seeded.workflow.js', note='args = {agent, outdir, blinddir, state}; one launch per agent'),
    'adjudication': dict(script='findings/protocol/agentC-adjudicate.workflow.js', note='args = the state object'),
    'D': dict(script='findings/protocol/agentD-proposals.workflow.js', note='args = the state object'),
}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')


def jload(path, default):
    return json.load(open(path)) if os.path.isfile(path) else default


def sh(*cmd):
    return subprocess.run(list(cmd), capture_output=True, text=True, cwd=ROOT)


def say(msg):
    print(msg, flush=True)


# ---------- 1. persistent scratchpad ----------
def verify_scratchpad():
    problems = []
    man = jload(os.path.join(PROV, 'snapshot-manifest.json'), None)
    if not man:
        problems.append('snapshot-manifest.json missing')
    else:
        for repo, info in sorted(man['repos'].items()):
            bad = 0
            for rel, meta in info['files'].items():
                p = os.path.join(SNAP, repo, rel)
                if meta['sha256'].startswith('symlink:'):
                    ok = os.path.islink(p) and os.readlink(p) == meta['sha256'][8:]
                else:
                    ok = os.path.isfile(p) and hashlib.sha256(open(p, 'rb').read()).hexdigest() == meta['sha256']
                bad += 0 if ok else 1
            extra = sum(len(f) for _, _, f in os.walk(os.path.join(SNAP, repo))) - info['n_files']
            if bad or extra:
                problems.append(f'snapshot {repo}: {bad} files differ or missing, {extra} unexpected')
        if not problems:
            say(f"snapshots: 13 repositories verified against the manifest ({sum(i['n_files'] for i in man['repos'].values())} files, sha256)")
    if not os.access(VENV_PY, os.X_OK):
        problems.append(f'venv python missing: {VENV_PY}')
    repo_rules = os.path.join(ROOT, 'findings', 'protocol', 'COMMON_RULES.md')
    cache_rules = os.path.join(CACHE, 'COMMON_RULES.md')
    if not os.path.isfile(cache_rules) or open(cache_rules).read() != open(repo_rules).read():
        shutil.copyfile(repo_rules, cache_rules)
        say('COMMON_RULES.md: cache copy re-synced from the repository copy')
    for p in problems:
        say('PROBLEM: ' + p)
    return not problems


# ---------- 2. /tmp symlinks ----------
def tmp_links():
    r = sh('bash', os.path.join(ROOT, 'tools', 'tmp_links.sh'))
    say('tmp links: ' + ('; '.join(l.split(' -> ')[0].replace('ok /tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/', '') for l in r.stdout.splitlines() if l.startswith('ok ')) or r.stdout.strip() or r.stderr.strip()))


# ---------- 3. leads from journals ----------
def bank_leads():
    added = {'A': 0, 'B': 0}
    files = {a: os.path.join(LA, AGENTS[a]['leads']) for a in ('A', 'B')}
    cur = {a: jload(files[a], []) for a in files}
    for jp in sorted(glob.glob(JOURNAL_GLOB)):
        for line in open(jp):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            r = e.get('result')
            if not isinstance(r, dict) or not r.get('cross_repo_leads') or not r.get('repo'):
                continue
            ids = [f.get('id', '') for f in r.get('findings', []) if isinstance(f, dict)]
            agent = 'A' if any(i.startswith('AUDIT-A-') for i in ids) else 'B' if any(i.startswith('AUDIT-B-') for i in ids) else None
            if agent is None:
                continue
            for l in r['cross_repo_leads']:
                s = str(l) if str(l).startswith(r['repo']) else f"{r['repo']}: {l}"
                if s not in cur[agent]:
                    cur[agent].append(s)
                    added[agent] += 1
    added['A'] += reopen_note_leads(cur['A'])
    for a in files:
        json.dump(cur[a], open(files[a], 'w'), indent=1, ensure_ascii=False)
    say(f"leads: A {len(cur['A'])} (+{added['A']} new), B {len(cur['B'])} (+{added['B']} new)")


def reopen_note_leads(bank):
    """Agent A consolidators write <repo>.reopen.md with a 'Leads for the cross-repository pass' table.
    When a consolidator dies before returning, its leads exist only there; bank them in the journal format."""
    n = 0
    for path in sorted(glob.glob(os.path.join(ROOT, AGENTS['A']['outdir'], '*.reopen.md'))):
        repo = os.path.basename(path)[:-len('.reopen.md')]
        parts = open(path, encoding='utf-8').read().split('Leads for the cross-repository pass', 1)
        if len(parts) < 2:
            continue
        for line in parts[1].splitlines():
            m = re.match(r'\|\s*\*\*L(\d+)\*\*\s*\|(.*)\|\s*$', line)
            if not m:
                continue
            cells = [c.strip().replace('**', '') for c in m.group(2).split('|')]
            if len(cells) < 3:
                continue
            what, cond, where = cells[0], cells[1], cells[-1]
            first = re.split(r'[\s,;(]', where.replace('`', ''), maxsplit=1)[0]
            s = f"{repo}: L{m.group(1)} ({first}): {what} - {cond} [where: {where}]"
            if s not in bank:
                bank.append(s)
                n += 1
    return n


# ---------- 4. state + recovery ----------
def agent_state(agent):
    a = AGENTS[agent]
    args = [a['outdir'], '--agent', 'C'] if agent == 'C' else [a['outdir'], '--ledger', a['ledger']]
    r = sh('python3', os.path.join(ROOT, 'tools', 'agent_state.py'), *args)
    if r.returncode:
        sys.exit('agent_state failed: ' + r.stderr)
    return json.loads(r.stdout)


def blind_complete(agent):
    out = os.path.join(ROOT, AGENTS[agent]['outdir'])
    return any('cross' in f.lower() for f in os.listdir(out) if os.path.isfile(os.path.join(out, f)))


def recovery_items(agent, st):
    items = []
    a = AGENTS[agent]
    drafts = os.path.join(ROOT, a['outdir'], '_drafts')
    if a['ledger'] and os.path.isdir(drafts):
        for repo in sorted(os.listdir(drafts)):
            if repo in st['done_repos']:
                continue
            d = os.path.join(drafts, repo)
            for f in sorted(os.listdir(d)):
                if not f.endswith('.md') or f.endswith(f".{a['ledger']}.md"):
                    continue
                part = f[:-3]
                if os.path.getsize(os.path.join(d, f)) >= MIN_DRAFT_BYTES and not os.path.isfile(os.path.join(d, f"{part}.{a['ledger']}.md")):
                    items.append(f"{agent} {repo}/{part}: draft present ({os.path.getsize(os.path.join(d, f))} bytes) but no {a['ledger']} ledger — check its closing sections; either run a ledger-recovery agent (see RUN_LOG 2026-09-04 18:5x) or let the reader rerun")
    for repo in st.get('consolidated', {}):
        items.append(f"{agent} {repo}: consolidated ({st['consolidated'][repo]} findings), verify/apply pending — handled by the next launch")
    if agent == 'C':
        for repo, s in st.get('stages', {}).items():
            items.append(f"C {repo}: inventory={s['inventory']} verification={s['verification']} provenance={s['provenance']} consolidated={s['consolidated']} — handled by the next launch")
    return items


def report_states():
    states = {}
    for agent in AGENTS:
        st = agent_state(agent)
        states[agent] = st
        done = st['done_repos']
        say(f"agent {agent}: {len(done)}/13 repositories done{' + cross-repo pass written' if blind_complete(agent) else ''}: {', '.join(done) or '-'}")
        for it in recovery_items(agent, st):
            say('   ' + it)
    return states


# ---------- 5. AFTER checks ----------
def parse_check(block):
    out, repo = {}, None
    for line in block.splitlines():
        m = re.match(r'^=== (\S+)\s+HEAD=', line)
        if m:
            repo = m.group(1)
            out[repo] = []
        elif repo and line.startswith('    '):
            out[repo].append(line[4:])
    return out


def status_check(label):
    r = sh('bash', os.path.join(ROOT, 'tools', 'git_status_check.sh'), label)
    if r.returncode:
        sys.exit('git_status_check failed: ' + r.stderr)
    baseline = jload(os.path.join(LA, 'DIRT_BASELINE.json'), {})
    loud = []
    for repo, entries in parse_check(r.stdout).items():
        base = baseline.get(repo, [])
        new = [e for e in entries if e not in base]
        gone = [e for e in base if e not in entries]
        if new or gone:
            loud.append(f"{repo}: new={new} gone={gone}")
    if loud:
        say(f"!!!!! {label}: WORKING TREE OF AN AUDITED REPOSITORY DIFFERS FROM THE BASELINE — report this, never revert: " + ' | '.join(loud))
    else:
        say(f"check {label}: only the pre-existing dirt")
    return loud


def after_checks():
    active = jload(os.path.join(LA, 'ACTIVE.json'), [])
    if not active:
        say('no active runs recorded')
        return []
    log = open(os.path.join(PROV, 'git-status-checks.log')).read()
    history = jload(os.path.join(LA, 'HISTORY.json'), [])
    findings = []
    for e in active:
        label = e['label'] + '-AFTER'
        if f'CHECK: {label} ' in log:
            say(f"check {label}: already recorded")
        else:
            findings += status_check(label)
        history.append(dict(e, after=now()))
    json.dump(history, open(os.path.join(LA, 'HISTORY.json'), 'w'), indent=1)
    json.dump([], open(os.path.join(LA, 'ACTIVE.json'), 'w'), indent=1)
    return findings


# ---------- 6. next runs ----------
def next_run_number(agent):
    nums = [int(m.group(1)) for f in os.listdir(LA) for m in [re.match(rf'agent{agent}-run(\d+)\.args\.json$', f)] if m]
    return (max(nums) if nums else 0) + 1


def prepare_blind(states):
    launches = []
    for agent, st in states.items():
        if blind_complete(agent):
            say(f"agent {agent}: blind pass complete, nothing to launch")
            continue
        n = next_run_number(agent)
        args = dict(st)
        if agent != 'C':
            args['leads'] = []
        path = os.path.join(LA, f'agent{agent}-run{n}.args.json')
        json.dump(args, open(path, 'w'), indent=1)
        label = f"{AGENTS[agent]['prefix']}-run{n}-BEFORE"
        status_check(label)
        launches.append(dict(agent=agent, run=n, script=os.path.join(ROOT, AGENTS[agent]['script']), args=args, args_file=os.path.relpath(path, ROOT)))
    return launches


def print_launches(launches):
    if not launches:
        return
    say('\n==== LAUNCH (Workflow tool; then tools/mark_launched.py <agent> <run> <task-id> <workflow-id>) ====')
    for l in launches:
        say(f"Agent {l['agent']} run {l['run']}  scriptPath: {l['script']}")
        say(f"   args: {json.dumps(l['args'], separators=(',', ':'))}")


def later_phase(phase):
    tool = os.path.join(ROOT, 'tools', 'agent_state.py')
    say(f"\n==== {phase}: {LATER[phase]['note']}; scriptPath {os.path.join(ROOT, LATER[phase]['script'])} ====")
    if phase == 'seeded':
        for agent in AGENTS:
            out = os.path.join(ROOT, AGENTS[agent]['outdir'], 'seeded')
            st = json.loads(sh('python3', tool, out, '--seeded').stdout or '{}')
            say(json.dumps({'agent': agent, 'outdir': out, 'blinddir': os.path.join(ROOT, AGENTS[agent]['outdir']), 'state': st}, separators=(',', ':')))
    elif phase == 'adjudication':
        say(sh('python3', tool, os.path.join(ROOT, 'findings', 'agentC', 'adjudication'), '--adjudication').stdout.strip())
    else:
        say(sh('python3', tool, os.path.join(ROOT, 'proposals'), '--agent', 'D').stdout.strip())


# ---------- 7. RUN_LOG + commit ----------
def run_log(lines):
    with open(os.path.join(PROV, 'RUN_LOG.md'), 'a') as f:
        f.write(f"\n## {now()} — tools/resume.py\n" + '\n'.join(lines) + '\n')


def commit(states, launches, session_url):
    paths = [p for p in ('findings/agentA', 'findings/agentB', 'findings/agentC', 'findings/protocol', 'provenance', 'tools', 'work', 'RESUME.md') if os.path.exists(os.path.join(ROOT, p))]
    sh('git', 'add', '--', *paths)
    if not sh('git', 'diff', '--cached', '--quiet').returncode:
        say('commit: nothing staged')
        return
    summary = '; '.join(f"{a} {len(s['done_repos'])}/13" for a, s in states.items())
    launched = ', '.join(f"{l['agent']} run {l['run']}" for l in launches)
    msg = f"bank: {summary}" + (f"; prepared {launched}" if launched else '') + "\n\nBanked by tools/resume.py.\n\nCo-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>\n"
    if session_url:
        msg += f"Claude-Session: {session_url}\n"
    r = subprocess.run(['git', 'commit', '-q', '-F', '-'], input=msg, capture_output=True, text=True, cwd=ROOT)
    say('commit: ' + (sh('git', 'log', '--oneline', '-1').stdout.strip() if not r.returncode else 'FAILED ' + r.stderr))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--runs-dead', action='store_true', help='the runs in ACTIVE.json are dead (reboot / all reported): AFTER checks, next args, BEFORE checks')
    ap.add_argument('--phase', choices=['blind', 'seeded', 'adjudication', 'D'], default='blind')
    ap.add_argument('--commit', action='store_true')
    ap.add_argument('--session-url', default='')
    a = ap.parse_args()
    say(f"resume.py @ {now()}  root={ROOT}")
    verify_scratchpad()
    tmp_links()
    bank_leads()
    states = report_states()
    lines = [f"agent {ag}: {len(st['done_repos'])}/13 done" for ag, st in states.items()]
    launches = []
    if a.runs_dead:
        loud = after_checks()
        lines += ['AFTER checks: ' + ('LOUD: ' + ' | '.join(loud) if loud else 'pre-existing dirt only')]
        if a.phase == 'blind':
            launches = prepare_blind(states)
            lines += [f"prepared {l['agent']} run {l['run']} ({l['args_file']})" for l in launches]
        else:
            later_phase(a.phase)
        run_log(lines)
    elif a.phase != 'blind':
        later_phase(a.phase)
    if a.commit:
        commit(states, launches, a.session_url)
    print_launches(launches)


if __name__ == '__main__':
    main()
