"""Save text of all MacTutor history topic pages (agents pick the relevant ones). No model involved."""
import json, re, subprocess, time, html
R = 'data/collection/'
BASE = 'https://mathshistory.st-andrews.ac.uk/'
def get(u):
    return subprocess.run(['curl', '-s', '-m', '30', '-A', 'proofscape-research/0.1', u], capture_output=True, text=True).stdout
idx = get(BASE + 'OtherIndexes/histtopics/')
topics = [(h.replace('../../', BASE), html.unescape(t)) for h, t in re.findall(r'href="([^"]*HistTopics/[^"]+)"[^>]*>([^<]+)<', idx)]
match = {}
pages = {}
for u, t0 in topics:
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', get(u), flags=re.S)
    pages[u] = {'title': t0, 'text': html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)))[:12000]}
    time.sleep(1)
json.dump({'matches': match, 'pages': pages}, open(R + 'enrichment/sources/mactutor-topics.json', 'w'), indent=1)
print(len(match), len(pages))
