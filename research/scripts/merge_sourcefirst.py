"""Merge sourcefirst/A_NN.json with thin_*.json (replacements), naming_*.json and firststmt.json (added milestones).
Writes sourcefirst/merged/M_NN.json with milestones sorted and derivedDates recomputed by the schema rule."""
import json, glob, os
B = 'data/collection/enrichment/sourcefirst/'
os.makedirs(B + 'merged', exist_ok=True)
thin = {e['pid']: e for f in glob.glob(B + 'thin_*.json') for e in json.load(open(f))}
extra = {}
for f in glob.glob(B + 'naming_*.json'):
    for x in json.load(open(f)): extra.setdefault(x['pid'], []).extend(x.get('milestones') or [])
for x in json.load(open(B + 'firststmt.json')):
    if x.get('milestone'): extra.setdefault(x['pid'], []).append(x['milestone'])
RULE = (('conceptual', ('first_statement',)), ('methodological', ('first_application',)), ('institutional', ('naming', 'consolidation', 'institution')))
nrep = nadd = 0
for f in sorted(glob.glob(B + 'A_*.json')):
    d = json.load(open(f))
    for i, e in enumerate(d):
        if e['pid'] in thin:
            d[i] = e = thin[e['pid']]; nrep += 1
        have = {(m['role'], m.get('year'), m.get('label')) for m in e['milestones']}
        for m in extra.get(e['pid'], []):
            if (m['role'], m.get('year'), m.get('label')) in have: continue
            m.setdefault('phase', None); m.setdefault('endYear', None)
            e['milestones'].append(m); nadd += 1
        e['milestones'].sort(key=lambda m: (m.get('year') is None, m.get('year') or 0))
        # over the 8-milestone cap: drop recognition, extra precursors, same-role-same-year duplicates, then weakest key_development; list what was dropped in notes
        conf = {'low': 0, 'medium': 1, 'high': 2}
        dropped = []
        def drop(m): e['milestones'].remove(m); dropped.append(f"{m['role']} {m.get('year')} {m.get('label')}")
        while len(e['milestones']) > 8:
            ms = e['milestones']
            c = [m for m in ms if m['role'] == 'recognition']
            if not c:
                pre = [m for m in ms if m['role'] == 'precursor']; c = pre[1:]
            if not c:
                seen = {}
                for m in sorted(ms, key=lambda m: conf.get(m.get('confidence'), 1)):
                    k = (m['role'], m.get('year'))
                    if k in seen: c = [m]; break
                    seen[k] = m
            if not c: c = sorted([m for m in ms if m['role'] == 'key_development'], key=lambda m: (conf.get(m.get('confidence'), 1), -(m.get('year') or 0)))[:1]
            if not c: break
            drop(c[0])
        if dropped:
            n = e['notes'] if isinstance(e['notes'], str) else ' '.join(map(str, e['notes']))
            e['notes'] = n + ' Milestones omitted to respect the 8-milestone cap: ' + '; '.join(dropped) + '.'
        e['phases'] = list(dict.fromkeys(list(e.get('phases') or []) + [m['phase'] for m in e['milestones'] if m.get('phase')]))
        for k, roles in RULE:
            ys = [m['year'] for m in e['milestones'] if m['role'] in roles and m.get('year') is not None]
            e['derivedDates'][k] = min(ys) if ys else None
    json.dump(d, open(B + 'merged/M_' + f[-7:-5] + '.json', 'w'), indent=1, ensure_ascii=False)
print('replaced', nrep, 'added milestones', nadd)
