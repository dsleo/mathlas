"""Check milestone files: JSON validity, pids match the batch input, roles, evidence, derived dates follow the schema rule."""
import json, glob, sys
ROLES = {'precursor','first_statement','first_application','key_development','consolidation','naming','institution','recognition'}
for f in sorted(glob.glob('data/collection/enrichment/scale/A_batch*.json')):
    n = f[-7:-5]
    try: out = json.load(open(f)); inp = json.load(open(f'data/collection/enrichment/scale/batch{n}.json'))
    except Exception as ex: print(n, 'ERR', ex); continue
    inp = inp if isinstance(inp, list) else inp.get('events', [])
    bad = []
    if {e['pid'] for e in out} != {e['pid'] for e in inp}: bad.append('pid mismatch')
    for e in out:
        ms = e.get('milestones', [])
        if not 3 <= len(ms) <= 8: bad.append(f"{e['pid']}: {len(ms)} milestones")
        for m in ms:
            if m.get('role') not in ROLES: bad.append(f"{e['pid']}: role {m.get('role')}")
            if m.get('year') is not None and not m.get('evidence'): bad.append(f"{e['pid']}: dated milestone without evidence")
        for key, roles in (('conceptual', ['first_statement']), ('methodological', ['first_application']), ('institutional', ['naming','consolidation','institution'])):
            ys = [m['year'] for m in ms if m.get('role') in roles and m.get('year') is not None]
            if (min(ys) if ys else None) != e.get('derivedDates', {}).get(key): bad.append(f"{e['pid']}: derived {key}")
    print(n, len(out), 'OK' if not bad else bad)
