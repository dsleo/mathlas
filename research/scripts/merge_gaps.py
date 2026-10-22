"""Append gap-filling results (gaps_*.json) to sourcefirst/merged/M_NN.json: new milestones and people, then re-sort, cap at 8 milestones, recompute derived dates."""
import json, glob
B = 'data/collection/enrichment/sourcefirst/'
gaps = {x['pid']: x for f in sorted(glob.glob(B + 'gaps_*.json')) for x in json.load(open(f))}
RULE = (('conceptual', ('first_statement',)), ('methodological', ('first_application',)), ('institutional', ('naming', 'consolidation', 'institution')))
conf = {'low': 0, 'medium': 1, 'high': 2}
def ok_url(u): return isinstance(u, str) and u.startswith('https://')
nm = npp = 0
for f in sorted(glob.glob(B + 'merged/M_*.json')):
    d = json.load(open(f)); ch = False
    for e in d:
        g = gaps.get(e['pid'])
        if not g: continue
        have = {(m['role'], m.get('year')) for m in e['milestones']}
        for m in g.get('milestones') or []:
            if (m.get('role'), m.get('year')) in have or not m.get('evidence') or not all(ok_url(x.get('url')) for x in m['evidence']): continue
            m.setdefault('phase', None); m.setdefault('endYear', None)
            e['milestones'].append(m); nm += 1; ch = True
        names = {p['name'] for p in e['people']}
        for p in g.get('people') or []:
            if p.get('name') in names or len(e['people']) >= 6 or not ok_url(p.get('biographyUrl')): continue
            ws = [w for w in p.get('works') or [] if ok_url(w.get('url')) and isinstance(w.get('year'), int)][:3]
            if not ws: continue
            e['people'].append({'name': p['name'], 'role': p.get('role') if p.get('role') in ('originator', 'developer', 'systematiser', 'popularizer') else 'developer', 'lifespan': p.get('lifespan'), 'biographyUrl': p['biographyUrl'], 'works': ws}); npp += 1; ch = True
        e['milestones'].sort(key=lambda m: (m.get('year') is None, m.get('year') or 0))
        dropped = []
        while len(e['milestones']) > 8:
            ms = e['milestones']
            c = [m for m in ms if m['role'] == 'recognition'] or [m for m in ms if m['role'] == 'precursor'][1:]
            if not c:
                seen = {}
                for m in sorted(ms, key=lambda m: conf.get(m.get('confidence'), 1)):
                    k = (m['role'], m.get('year'))
                    if k in seen: c = [m]; break
                    seen[k] = m
            if not c: c = sorted([m for m in ms if m['role'] == 'key_development'], key=lambda m: (conf.get(m.get('confidence'), 1), -(m.get('year') or 0)))[:1]
            if not c: break
            ms.remove(c[0]); dropped.append(f"{c[0]['role']} {c[0].get('year')} {c[0].get('label')}")
        if dropped: e['notes'] = (e['notes'] if isinstance(e['notes'], str) else ' '.join(map(str, e['notes']))) + ' Milestones omitted to respect the 8-milestone cap: ' + '; '.join(dropped) + '.'
        e['phases'] = list(dict.fromkeys(list(e.get('phases') or []) + [m['phase'] for m in e['milestones'] if m.get('phase')]))
        for k, roles in RULE:
            ys = [m['year'] for m in e['milestones'] if m['role'] in roles and m.get('year') is not None]
            e['derivedDates'][k] = min(ys) if ys else None
    if ch: json.dump(d, open(f, 'w'), indent=1, ensure_ascii=False)
print('milestones added', nm, 'people added', npp)
