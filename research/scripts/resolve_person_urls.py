"""For people without a valid biography URL, try MacTutor then Wikipedia page existence (HTTP 200); never invent a URL."""
import json, glob, subprocess, time, unicodedata, re, urllib.parse
B = 'data/collection/enrichment/sourcefirst/'
def ok(u, name):
    r = subprocess.run(['curl', '-s', '-L', '-m', '20', '-A', 'proofscape-research/0.1', u], capture_output=True, text=True)
    time.sleep(0.5)
    m = re.search(r'<title>(.*?)</title>', r.stdout, re.S)
    t = ascii_(m.group(1)).lower() if m else ''
    toks = [w for w in re.sub(r'[^A-Za-z\- ]', '', ascii_(name)).lower().split() if len(w) > 2]
    # same person only if the page title carries the surname and the first given name (a lone initial is not enough)
    return bool(toks) and toks[-1] in t and (len(toks) < 2 or toks[0] in t)
def ascii_(s): return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
cache = {}
for f in sorted(glob.glob(B + 'A_*.json')):
    d = json.load(open(f)); ch = False
    for e in d:
        for p in e['people']:
            u = p.get('biographyUrl')
            if isinstance(u, str) and u.startswith('https://'): continue
            nm = p['name']
            if nm not in cache:
                parts = re.sub(r'[^A-Za-z\- ]', '', ascii_(nm)).split()
                cands = []
                if parts: cands.append('https://mathshistory.st-andrews.ac.uk/Biographies/' + parts[-1] + '/')
                cands.append('https://en.wikipedia.org/wiki/' + urllib.parse.quote(nm.replace(' ', '_')))
                cache[nm] = next((c for c in cands if ok(c, nm)), None)
            if cache[nm]: p['biographyUrl'] = cache[nm]; ch = True
    if ch: json.dump(d, open(f, 'w'), indent=1, ensure_ascii=False)
json.dump(cache, open(B + 'person-url-cache.json', 'w'), indent=1)
print(sum(1 for v in cache.values() if v), len(cache))
