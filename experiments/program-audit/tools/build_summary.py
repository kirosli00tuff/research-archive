#!/usr/bin/env python3
"""Aggregate every agent's JSON output into the tables SUMMARY.md needs.

Usage: tools/build_summary.py [--write findings/_summary_tables.md]

Reads (all optional; missing pieces are reported, never invented):
  findings/agent{A,B,C}/<repo>.json, CROSS_REPO.json, seeded/*.json, seeded/CHECK3_intervals/*.json
  findings/agentC/adjudication/<repo>.json          (rulings with contradicts / agrees_with)
  findings/agentC/verification/<repo>.claims.json   (VERIFIED / CONTRADICTED / UNVERIFIABLE)
  findings/agentC/provenance/<repo>.json            (SUPPORTED / NOT_SUPPORTED / PARTIAL / UNVERIFIABLE)
Prints Markdown tables. The orchestrator writes the narrative parts of SUMMARY.md by hand.
"""
import glob, json, os, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, 'findings')
REPOS = ['AiTrader', 'ETFExperiment', 'HFExperiment', 'InsiderExperiment', 'MLCryptoEngine', 'NPDExperiment',
         'NPLExperiment', 'ORBExperiment', 'PMExperiment', 'VRPExperiment', 'retail-power-limits', 'solattn', 'solclear']
SEV = ['S1', 'S2', 'S3', 'S4']
RULINGS = ['UPHELD', 'UPHELD_WITH_CORRECTION', 'NOT_UPHELD', 'UNRESOLVABLE_ON_AVAILABLE_EVIDENCE']


def load(path):
    if not os.path.isfile(path):
        return []  # not produced (yet); the narrative reports gaps explicitly
    try:
        with open(path, encoding='utf-8') as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except (OSError, ValueError) as e:
        print(f'WARN cannot read {os.path.relpath(path, ROOT)}: {e}', file=sys.stderr)
        return []


def findings_for(agent):
    d = os.path.join(F, f'agent{agent}')
    out = []
    for r in REPOS:
        for f in load(os.path.join(d, f'{r}.json')):
            out.append({**f, '_source': 'blind'})
    for f in load(os.path.join(d, 'CROSS_REPO.json')):
        out.append({**f, '_source': 'cross_repo'})
    for p in sorted(glob.glob(os.path.join(d, 'seeded', '*.json')) + glob.glob(os.path.join(d, 'seeded', 'CHECK3_intervals', '*.json'))):
        if os.path.basename(p).startswith('CHECK3_intervals.json'):
            continue  # merged copy of the per-repo check-3 files
        for f in load(p):
            out.append({**f, '_source': 'seeded'})
    seen, uniq = set(), []
    for f in out:
        if f.get('id') in seen:
            continue
        seen.add(f.get('id')); uniq.append(f)
    return uniq


def rulings():
    d = os.path.join(F, 'agentC', 'adjudication')
    out = {}
    for r in REPOS:
        for x in load(os.path.join(d, f'{r}.json')):
            if x.get('finding_id'):
                out[x['finding_id']] = x
    return out


def claims():
    out = defaultdict(list)
    for r in REPOS:
        for c in load(os.path.join(F, 'agentC', 'verification', f'{r}.claims.json')):
            out[r].append(c)
    return out


def provenance():
    out = defaultdict(list)
    for r in REPOS:
        for c in load(os.path.join(F, 'agentC', 'provenance', f'{r}.json')):
            out[r].append(c)
    return out


def table(headers, rows):
    lines = ['| ' + ' | '.join(headers) + ' |', '|' + '|'.join('---' for _ in headers) + '|']
    lines += ['| ' + ' | '.join(str(c).replace('|', '\\|').replace('\n', ' ') for c in row) + ' |' for row in rows]
    return '\n'.join(lines)


def main():
    all_f = {a: findings_for(a) for a in 'ABC'}
    rul = rulings()
    cl = claims()
    pv = provenance()
    flat = [f for a in 'ABC' for f in all_f[a]]
    out = []

    out.append('## Counts\n')
    out.append(table(['Agent', 'Findings', 'S1', 'S2', 'S3', 'S4', 'DERIVED', 'READ', 'blind', 'cross-repo', 'seeded'],
                     [[a, len(all_f[a])] + [sum(1 for f in all_f[a] if f.get('severity') == s) for s in SEV]
                      + [sum(1 for f in all_f[a] if f.get('label') == l) for l in ('DERIVED', 'READ')]
                      + [sum(1 for f in all_f[a] if f['_source'] == s) for s in ('blind', 'cross_repo', 'seeded')] for a in 'ABC']
                     + [['all', len(flat)] + [sum(1 for f in flat if f.get('severity') == s) for s in SEV]
                        + [sum(1 for f in flat if f.get('label') == l) for l in ('DERIVED', 'READ')]
                        + [sum(1 for f in flat if f['_source'] == s) for s in ('blind', 'cross_repo', 'seeded')]]))
    out.append('\n### By direction\n')
    out.append(table(['Direction', 'A', 'B', 'C', 'all'], [[d] + [sum(1 for f in all_f[a] if f.get('direction') == d) for a in 'ABC'] + [sum(1 for f in flat if f.get('direction') == d)] for d in ('A', 'B')]))
    out.append('\n### By class\n')
    classes = sorted({f.get('class') for f in flat if f.get('class')})
    out.append(table(['Class', 'A', 'B', 'C', 'all'], [[c] + [sum(1 for f in all_f[a] if f.get('class') == c) for a in 'ABC'] + [sum(1 for f in flat if f.get('class') == c)] for c in classes]))
    out.append('\n### By repository\n')
    out.append(table(['Repository', 'A', 'B', 'C', 'all', 'S1', 'S2', 'highest'],
                     [[r] + [sum(1 for f in all_f[a] if f.get('repo') == r) for a in 'ABC'] + [sum(1 for f in flat if f.get('repo') == r),
                      sum(1 for f in flat if f.get('repo') == r and f.get('severity') == 'S1'), sum(1 for f in flat if f.get('repo') == r and f.get('severity') == 'S2'),
                      min([f.get('severity', 'S4') for f in flat if f.get('repo') == r] or ['none'])] for r in REPOS]))

    out.append('\n## Adjudication (Agent C rulings on A and B findings)\n')
    ab = [f for a in 'AB' for f in all_f[a]]
    ruled = [f for f in ab if f.get('id') in rul]
    out.append(f'A and B findings: {len(ab)}; ruled: {len(ruled)}; unruled: {len(ab) - len(ruled)}\n')
    out.append(table(['Ruling', 'on A', 'on B', 'total'],
                     [[k] + [sum(1 for f in all_f[a] if rul.get(f.get('id'), {}).get('ruling') == k) for a in 'AB'] + [sum(1 for f in ab if rul.get(f.get('id'), {}).get('ruling') == k)] for k in RULINGS]))
    out.append('\n### Agreement matrix (per repository)\n')
    rows = []
    for r in REPOS:
        rr = [x for x in rul.values() if x.get('repo') == r]
        agree = {tuple(sorted((x['finding_id'], y))) for x in rr for y in (x.get('agrees_with') or [])}
        contra = {tuple(sorted((x['finding_id'], y))) for x in rr for y in (x.get('contradicts') or [])}
        rows.append([r] + [sum(1 for f in all_f[a] if f.get('repo') == r) for a in 'ABC'] + [len(agree), len(contra)]
                    + [sum(1 for x in rr if x.get('ruling') == k) for k in RULINGS])
    out.append(table(['Repository', 'A', 'B', 'C', 'agreements', 'contradictions', 'UPHELD', 'UPHELD_WITH_CORRECTION', 'NOT_UPHELD', 'UNRESOLVABLE'], rows))
    agree_all = {tuple(sorted((x['finding_id'], y))) for x in rul.values() for y in (x.get('agrees_with') or [])}
    contra_all = {tuple(sorted((x['finding_id'], y))) for x in rul.values() for y in (x.get('contradicts') or [])}
    out.append(f'\nAgreement pairs (unique): {len(agree_all)}; contradiction pairs (unique): {len(contra_all)}\n')
    if contra_all:
        out.append('\n### Contradiction pairs\n')
        out.append('\n'.join(f'- {a} vs {b}' for a, b in sorted(contra_all)))

    out.append('\n## Agent C claim verification\n')
    rows, tot = [], Counter()
    for r in REPOS:
        c = Counter(x.get('status') for x in cl.get(r, []))
        tot.update(c)
        rows.append([r, len(cl.get(r, []))] + [c.get(s, 0) for s in ('VERIFIED', 'CONTRADICTED', 'UNVERIFIABLE')])
    rows.append(['all', sum(tot.values())] + [tot.get(s, 0) for s in ('VERIFIED', 'CONTRADICTED', 'UNVERIFIABLE')])
    out.append(table(['Repository', 'claims', 'VERIFIED', 'CONTRADICTED', 'UNVERIFIABLE'], rows))
    contradicted = [(r, x) for r in REPOS for x in cl.get(r, []) if x.get('status') == 'CONTRADICTED']
    if contradicted:
        out.append('\n### Contradicted claims\n')
        out.append(table(['Repository', 'claim', 'file:line', 'stated', 'recomputed'],
                         [[r, (x.get('claim_text') or '')[:120], f"{x.get('file')}:{x.get('line')}", x.get('stated_value'), x.get('recomputed_value')] for r, x in contradicted]))
    out.append('\n## Agent C provenance\n')
    rows, tot = [], Counter()
    for r in REPOS:
        c = Counter(x.get('status') for x in pv.get(r, []))
        tot.update(c)
        rows.append([r, len(pv.get(r, []))] + [c.get(s, 0) for s in ('SUPPORTED', 'PARTIAL', 'NOT_SUPPORTED', 'UNVERIFIABLE')])
    rows.append(['all', sum(tot.values())] + [tot.get(s, 0) for s in ('SUPPORTED', 'PARTIAL', 'NOT_SUPPORTED', 'UNVERIFIABLE')])
    out.append(table(['Repository', 'items', 'SUPPORTED', 'PARTIAL', 'NOT_SUPPORTED', 'UNVERIFIABLE'], rows))

    out.append('\n## Severity-ranked register\n')
    order = {s: i for i, s in enumerate(SEV)}
    reg = sorted(flat, key=lambda f: (order.get(f.get('severity'), 9), f.get('repo', ''), f.get('id', '')))
    out.append(table(['ID', 'Sev', 'Dir', 'Class', 'Label', 'Repo', 'Source', 'C ruling', 'Corrected sev', 'One line'],
                     [[f.get('id'), f.get('severity'), f.get('direction'), f.get('class'), f.get('label'), f.get('repo'), f['_source'],
                       rul.get(f.get('id'), {}).get('ruling', '—' if f.get('agent') != 'C' else 'n/a'),
                       rul.get(f.get('id'), {}).get('corrected_severity') or '',
                       (f.get('one_line') or f.get('evidence_summary') or f.get('hypothesis_or_artifact') or '')[:160]] for f in reg]))

    out.append('\n## Candidate sound repositories (no S1/S2 from any agent, no CONTRADICTED claim, no NOT_SUPPORTED provenance)\n')
    sound = [r for r in REPOS if not any(f.get('repo') == r and f.get('severity') in ('S1', 'S2') for f in flat)
             and not any(x.get('status') == 'CONTRADICTED' for x in cl.get(r, []))
             and not any(x.get('status') == 'NOT_SUPPORTED' for x in pv.get(r, []))]
    out.append(', '.join(sound) if sound else '(none)')
    text = '\n'.join(out) + '\n'
    if len(sys.argv) > 2 and sys.argv[1] == '--write':
        with open(sys.argv[2], 'w', encoding='utf-8') as fh:
            fh.write(text)
        print(f'wrote {sys.argv[2]}')
    else:
        print(text)


if __name__ == '__main__':
    main()
