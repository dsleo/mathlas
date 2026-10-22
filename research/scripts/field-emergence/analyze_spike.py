import json, math, statistics as st

rows = {}
for l in open("zbmath_counts.jsonl"):
    r = json.loads(l)
    if r["n"] is not None:
        rows[r["q"]] = r["n"]
meta = json.load(open("zb_spike_meta.json"))
W = [tuple(w) for w in meta["windows"]]
label = lambda w: f"{w[0]}-{w[1]}"

def N(w): return rows.get(f"py:{w[0]}-{w[1]}")
def n1(s, w): return rows.get(f"cc:{s} py:{w[0]}-{w[1]}")
def n2(a, b, w): return rows.get(f"cc:{a} cc:{b} py:{w[0]}-{w[1]}")

def series(a, b):
    out = []
    for w in W:
        t, na, nb, nab = N(w), n1(a, w), n1(b, w), n2(a, b, w)
        if None in (t, na, nb, nab) or na == 0 or nb == 0:
            out.append(None); continue
        lift = nab * t / (na * nb)
        out.append({"w": label(w), "n_ab": nab, "n_a": na, "n_b": nb, "N": t, "lift": lift,
                    "share_of_smaller": nab / min(na, nb)})
    return out

# seed events -> (pair, year the event is dated)
EV = {
 "E38 Furstenberg ergodic Szemeredi (1977)": ("11", "37", 1977),
 "E50 Green-Tao (2004)": ("05", "11", 2004),
 "E50 Green-Tao ergodic route (2004)": ("11", "37", 2004),
 "E41 Donaldson gauge theory (1983)": ("57", "81", 1983),
 "E41 Donaldson gauge theory (1983) 58x81": ("58", "81", 1983),
 "E42 Jones polynomial (1985)": ("46", "57", 1985),
 "E44 moonshine / vertex algebras (1988)": ("17", "81", 1988),
 "E47 mirror symmetry (1991)": ("14", "81", 1991),
 "E49 SLE (2000)": ("60", "81", 2000),
 "E49 SLE (2000) 30x60": ("30", "60", 2000),
 "E52 expansion in groups (2008)": ("05", "20", 2008),
 "E51 polynomial method (2008)": ("05", "14", 2008),
 "E56 Huh Hodge theory (2012)": ("05", "14", 2012),
 "E57 regularity structures (2014)": ("35", "60", 2014),
 "E59 PFR entropy (2023)": ("05", "94", 2023),
 "E73 computer proof (1976)": ("05", "68", 1976),
 "E36 topological combinatorics (1978)": ("05", "55", 1978),
 "E33 index theorem (1963)": ("55", "58", 1963),
 "B13 arithmetic QUE (2006)": ("11", "37", 2006),
 "B17 entropy (1958)": ("37", "94", 1958),
 "B18 wavelets (1988)": ("42", "94", 1988),
 "B24 D-modules (1984)": ("32", "35", 1984),
 "E34/E65 Langlands (1967)": ("11", "22", 1967),
}

def jump(s, i):
    """ratio of lift in window i to lift in window i-1, if both defined and n_ab>=10 in window i"""
    if i == 0 or s[i] is None or s[i - 1] is None: return None
    if s[i]["n_ab"] < 10 or s[i - 1]["lift"] == 0: return None
    return s[i]["lift"] / s[i - 1]["lift"]

def win_index(year):
    for i, w in enumerate(W):
        if w[0] <= year <= w[1]: return i
    return None

print("== seed event pairs: lift per window ==")
tested = 0; hit = 0; res = []
for name, (a, b, y) in EV.items():
    s = series(a, b)
    i = win_index(y)
    j = jump(s, i) if i is not None else None
    # allow the following window too (signal may lag an event dated late in its decade)
    j2 = jump(s, i + 1) if i is not None and i + 1 < len(W) else None
    best = max([x for x in (j, j2) if x is not None], default=None)
    tested += best is not None
    hit += (best is not None and best >= 1.5)
    res.append((name, a, b, y, best))
    print(f"{name:48s} {a}x{b} lifts:", " ".join("-" if x is None else f"{x['lift']:.1f}" for x in s), f"| jump={None if best is None else round(best,2)}")

print("\n== controls: all consecutive-window jumps ==")
cj = []
for a, b in meta["control"]:
    s = series(a, b)
    for i in range(1, len(W)):
        j = jump(s, i)
        if j is not None: cj.append(j)
print("n control transitions:", len(cj), "share with jump >= 1.5:", round(sum(1 for x in cj if x >= 1.5) / max(1, len(cj)), 3),
      "median", round(st.median(cj), 2) if cj else None)
# the same for all non-event listed pairs (background): all pairs in meta['pairs']
bj = []
for a, b in meta["pairs"]:
    s = series(a, b)
    for i in range(1, len(W)):
        j = jump(s, i)
        if j is not None: bj.append(j)
print("n listed-pair transitions:", len(bj), "share >=1.5:", round(sum(1 for x in bj if x >= 1.5) / max(1, len(bj)), 3))
print("event-pair tests with data:", tested, "with jump >= 1.5 in event window or next:", hit)

out = {
 "note": "Channel B spike: counts of zbMATH Open documents by MSC two-digit section pair and window, from api.zbmath.org/v1/document/_search (count = nr_total_results). Lift = n_ab * N / (n_a * n_b). Retrieved 2026-10-16.",
 "windows": [label(w) for w in W],
 "pairs": meta["pairs"], "control": meta["control"],
 "series": {f"{a}-{b}": series(a, b) for a, b in meta["pairs"] + meta["control"]},
 "event_tests": [{"event": n, "pair": [a, b], "year": y, "max_jump_in_window_or_next": None if j is None else round(j, 3)} for n, a, b, y, j in res],
 "control_transitions": {"n": len(cj), "share_jump_ge_1_5": round(sum(1 for x in cj if x >= 1.5) / max(1, len(cj)), 3)},
 "listed_pair_transitions": {"n": len(bj), "share_jump_ge_1_5": round(sum(1 for x in bj if x >= 1.5) / max(1, len(bj)), 3)},
}
json.dump(out, open("channel_b_spike.json", "w"), ensure_ascii=False, indent=1)
