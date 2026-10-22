"""Build public/field-emergence-explorer.html: one page with the curated events on a time axis, milestone detail, people, links and audit marks.
Sources: catalogue (field-events-merged.json), focused MSC2020 additions (field-map-focused-additions.json), directly checked records (public/field-emergence-milestones.json, status researched),
source-first records (enrichment/sourcefirst/merged/M_*.json), blind second pass (enrichment/second_blind/second_*.json)."""
import re, json, glob, random, copy, sys
sys.path.insert(0, 'scripts')
import chronology as CH
from field_map_curation import SAME_EVENT, audit_near_duplicates, audit_shared_first_statements, audit_shared_roots, audit_visible_aliases, build_relations, merge_events, refocus_solution
from field_map_taxonomy import LANES
E = 'data/collection/enrichment/'
cat = {e['id']: e for e in json.load(open('data/collection/field-events-merged.json'))['events']}
focused = json.load(open('data/collection/field-map-focused-additions.json'))['entries']
for addition in focused:
    event = addition['catalogue']
    if event['id'] in cat:
        raise ValueError(f"Duplicate focused catalogue ID: {event['id']}")
    cat[event['id']] = event
other = {(e.get('pid') or e['eventId']): e for e in json.load(open('public/field-emergence-milestones.json'))['events']}
mine = {e['pid']: e for f in sorted(glob.glob(E + 'sourcefirst/merged/M_*.json')) for e in json.load(open(f))}
dx = {}
for f in glob.glob(E + 'sourcefirst/dx_*.json') + glob.glob(E + 'sourcefirst/app_*.json') + glob.glob(E + 'sourcefirst/app2_*.json'):
    try:
        for x in json.load(open(f)): dx[x['pid']] = x
    except Exception: pass
second = {}
for f in glob.glob(E + 'second_blind/second_*.json'):
    try:
        for e in json.load(open(f)): second[e['pid']] = e
    except Exception: pass
ROLES = ('first_statement', 'first_application', 'naming', 'consolidation', 'institution')
def clean_people(ps):
    return [{'name': p.get('name'), 'role': p.get('role'), 'life': p.get('lifespan'), 'url': p.get('biographyUrl'),
             'works': [{'c': w.get('citation'), 'y': w.get('year'), 'u': w.get('url'), 'w': w.get('whyItMatters')} for w in (p.get('works') or [])]} for p in ps or []]
def clean_ms(ms):
    return [{'r': m.get('role'), 'y': m.get('year'), 'ye': m.get('endYear'), 'p': m.get('precision'), 'l': m.get('label'), 'w': m.get('work'),
             'pe': m.get('people') or [], 'd': m.get('description'), 'ph': m.get('phase'), 'c': m.get('confidence'), 'n': m.get('note'),
             'ev': [{'c': x.get('claim'), 's': x.get('source'), 'u': x.get('url'), 'k': x.get('kind')} for x in m.get('evidence') or []]} for m in ms or []]
def notes_text(n): return n if isinstance(n, str) else ' '.join(map(str, n or []))
out = []
for pid, o in other.items():
    c = cat.get(o['eventId'], {})
    rec = None; tier = 'catalogue'
    if o.get('researchStatus') == 'researched' and o.get('milestones'): rec, tier = o, 'direct'
    elif pid in mine: rec, tier = mine[pid], 'source-first'
    cd = (c.get('dates') or [None])[0]
    cy = (cd[0] if isinstance(cd, (list, tuple)) else (int(m.group()) if (m := re.search(r'-?\d+', str(cd))) else None)) if cd else None
    if rec is not None and tier == 'direct': rec = copy.deepcopy(rec)
    ms = (rec or {}).get('milestones') or []
    if rec is not None and pid in dx:
        have = {(m['role'], m.get('year')) for m in rec['milestones']}
        for m in dx[pid].get('milestones') or []:
            if (m.get('role'), m.get('year')) in have or not m.get('evidence') or not all(str(x.get('url', '')).startswith('https://') for x in m['evidence']): continue
            rec['milestones'].append(m)
    if rec is not None: CH.normalize(rec); ms = rec['milestones']; ms.sort(key=lambda m: (m.get('year') is None, m.get('year') or 0))
    raw = (rec or {}).get('derivedDates') or {}
    dd = {k: (v.get('start') if isinstance(v, dict) else v) for k, v in raw.items()}
    grades = {k: v.get('grade') for k, v in raw.items() if isinstance(v, dict) and v.get('grade')}
    shown = CH.shown(ms) if ms else None
    y = shown['conceptual']['y'] if shown else None
    approx = False
    if y is None: y, approx = cy, True
    sec = None
    if pid in second:
        s = second[pid]; sd = {k: min([m['year'] for m in s.get('milestones') or [] if m.get('role') in r and m.get('year') is not None] or [None]) for k, r in (('conceptual', ('first_statement',)), ('methodological', ('first_application',)), ('institutional', ('naming', 'consolidation', 'institution')))}
        sec = {'derived': sd, 'took': CH.took_hold([{'role': m.get('role'), 'year': m.get('year'), 'label': m.get('label')} for m in s.get('milestones') or []], sd.get('conceptual')), 'n': len(s.get('milestones') or []), 'people': [p.get('name') for p in s.get('people') or []],
               'ms': [{'r': m.get('role'), 'y': m.get('year'), 'l': m.get('label')} for m in s.get('milestones') or []]}
    out.append({'pid': pid, 'id': o['eventId'], 'name': (rec or o).get('canonicalName') or o['canonicalName'], 'aliases': (rec or o).get('aliases') or [],
                'type': c.get('type'), 'from': c.get('from') or [], 'to': c.get('to') or [], 'product': c.get('product'), 'why': c.get('why'), 'cat': c.get('src'),
                'tier': tier, 'grade': grades, 'shown': shown, 'took': CH.took_hold(ms, shown['conceptual']['y'] if shown else None) if ms else None, 'y': y, 'approx': approx, 'derived': dd, 'phases': (rec or {}).get('phases') or [],
                'ms': clean_ms(ms), 'people': clean_people((rec or {}).get('people')), 'notes': notes_text((rec or {}).get('notes')) if rec else notes_text(o.get('notes')),
                'catalogueDates': c.get('dates'), 'second': sec})
audit_shared_roots(out)
audit_near_duplicates(out)
out = merge_events(out)
for e in out:
    refocused = refocus_solution(e)
    if e['mergedPids'] or refocused:
        merged_ms = [{'role': m['r'], 'year': m['y'], 'label': m['l']} for m in e['ms']]
        e['shown'] = CH.shown(merged_ms)
        e['derived'] = CH.strict(merged_ms)
        e['took'] = CH.took_hold(merged_ms, e['shown']['conceptual']['y'])
        if e['shown']['conceptual']['y'] is not None:
            e['y'] = e['shown']['conceptual']['y']
            e['approx'] = e['shown']['conceptual']['basis'] != 'first statement'
audit_shared_first_statements(out)
audit_visible_aliases(out)
out = [e for e in out if e['y'] is not None] + [e for e in out if e['y'] is None]
EDGES = build_relations(out)
rnd = random.Random(20261019); ids = [e['pid'] for e in out]; rnd.shuffle(ids)
sample = set(ids[:56])
for e in out: e['sample'] = e['pid'] in sample
method = open('scripts/field_explorer_method.html').read()
nms = sum(len(e['ms']) for e in out); npp = sum(len(e['people']) for e in out); nev = sum(len(m['ev']) for e in out for m in e['ms'])
for k, v in {'N': len(out), 'MS': f'{nms:,}', 'PEOPLE': f'{npp:,}', 'EV': f'{nev:,}', 'DIRECT': sum(1 for e in out if e['tier'] == 'direct'), 'SF': sum(1 for e in out if e['tier'] == 'source-first')}.items():
    method = method.replace('{{' + k + '}}', str(v))
html = open('scripts/field_explorer_template.html').read().replace('<!--METHOD-->', method).replace('{{N}}', str(len(out))).replace('/*DATA*/[]', json.dumps(out, ensure_ascii=False, separators=(',', ':'))).replace('/*EDGES*/[]', json.dumps(EDGES)).replace('/*REDIRECTS*/{}', json.dumps(SAME_EVENT)).replace('/*MAP_LANES*/[]', json.dumps(LANES))
open('public/field-emergence-explorer.html', 'w').write('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + html)
import sys
if len(sys.argv) > 1: open(sys.argv[1], 'w').write(html)  # fragment for artifact publishing
from collections import Counter
print(len(out), Counter(e['tier'] for e in out), 'second', len(second), 'undated', sum(1 for e in out if e['y'] is None))
