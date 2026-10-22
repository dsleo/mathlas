"""Normalise the source-first batches (scale/A_batchNN.json) to the strict milestone schema without inventing facts.
Fixes: people roles mapped to the controlled vocabulary (original text kept in roleNote), milestones sorted (undated last),
null-year precision -> unknown, phases listed, missing notes, confidence 'medium-high' -> 'medium'. Writes sourcefirst/A_NN.json."""
import json, glob, re
B = 'data/collection/enrichment/'
def role(t):
    s = (t or '').lower()
    if s in ('originator', 'developer', 'systematiser', 'popularizer'): return s
    if re.search(r'popular|expos|lectur|survey|teacher|translator', s): return 'popularizer'
    if re.search(r'systemat|textbook|monograph|consolid|codif|axiomati|formaliz', s): return 'systematiser'
    if re.search(r'origin|found|inventor|invent|introduc|first|discover|proposed|creator|pioneer|coined', s): return 'originator'
    return 'developer'
for f in sorted(glob.glob(B + 'scale/A_batch*.json')):
    n = f[-7:-5]; d = json.load(open(f))
    for e in d:
        for p in e.get('people', []):
            if p.get('role') not in ('originator', 'developer', 'systematiser', 'popularizer'):
                p['roleNote'] = p.get('role'); p['role'] = role(p.get('role'))
        ms = e['milestones']
        for m in ms:
            if m.get('year') is None: m['precision'] = 'unknown'
            if m.get('confidence') not in ('high', 'medium', 'low'): m['confidence'] = 'medium'
        ms.sort(key=lambda m: (m.get('year') is None, m.get('year') or 0))
        ph = list(e.get('phases') or [])
        for m in ms:
            if m.get('phase') and m['phase'] not in ph: ph.append(m['phase'])
        e['phases'] = ph
        if not str(e.get('notes') or '').strip(): e['notes'] = 'No further notes recorded by the source-first pass.'
        e['pass'] = 'source-first (Sonnet/Haiku), unadjudicated'
    json.dump(d, open(B + f'sourcefirst/A_{n}.json', 'w'), indent=1, ensure_ascii=False)
print('ok')
