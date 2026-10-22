"""Source-first pass: for each merged event, fetch top Wikipedia search hits with intro text and years. No model involved."""
import json, re, subprocess, sys, time, urllib.parse
ROOT = 'data/collection/'
ev = json.load(open(ROOT + 'field-events-merged.json'))['events']
OUT = ROOT + 'enrichment/sources/wikipedia-leads.json'
try: res = json.load(open(OUT))
except Exception: res = {}
def api(**p):
    url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({**p, 'format': 'json'})
    for _ in range(3):
        r = subprocess.run(['curl', '-s', '-m', '30', '-A', 'proofscape-research/0.1', url], capture_output=True, text=True)
        try: return json.loads(r.stdout)
        except Exception: time.sleep(3)
    return {}
for e in ev:
    if e['id'] in res: continue
    q = re.sub(r'\s*[:(].*$', '', e['name'])  # name before colon/parenthesis
    hits = api(action='query', list='search', srsearch=q, srlimit=3).get('query', {}).get('search', [])
    cands = []
    for h in hits:
        x = api(action='query', prop='extracts', exintro=1, explaintext=1, titles=h['title'], redirects=1)
        page = next(iter(x.get('query', {}).get('pages', {}).values()), {})
        t = page.get('extract', '')[:2500]
        cands.append({'title': h['title'], 'url': 'https://en.wikipedia.org/wiki/' + h['title'].replace(' ', '_'),
                      'years': sorted({int(y) for y in re.findall(r'\b(1[0-9]{3}|20[0-2][0-9])\b', t)}), 'intro': t})
        time.sleep(0.3)
    res[e['id']] = {'name': e['name'], 'query': q, 'candidates': cands}
    json.dump(res, open(OUT, 'w'), indent=1)
print(len(res))
