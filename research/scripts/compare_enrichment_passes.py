#!/usr/bin/env python3
"""Three-way comparison of the 30-event enrichment pilot: Opus (A1-3), Sonnet (B1-3), direct pass.

Reads data/collection/enrichment/pilot/{A,B}{1,2,3}.json and direct-research.json.
A date counts as evidenced when it has a start year and at least one evidence item.
Two passes agree when their start years differ by at most 3. A date is an A-grade
candidate when at least two passes agree and at least one of the agreeing passes
cites a bibliographic record. Writes pilot/three-way-comparison.json.
"""
import json, itertools
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "data/collection/enrichment/pilot"
KEYS = ("conceptual", "methodological", "institutional")
TOL = 3

def load_pass(prefix):
    out = {}
    for k in (1, 2, 3):
        for r in json.loads((P / f"{prefix}{k}.json").read_text()):
            out[r["pid"]] = r
    return out

passes = {"opus": load_pass("A"), "sonnet": load_pass("B"),
          "direct": {r["pid"]: r for r in json.loads((P / "direct-research.json").read_text())["events"]}}

def cell(rec, key):
    d = (rec.get("dates") or {}).get(key) or {}
    s = d.get("start")
    ev = d.get("evidence") or []
    if s is None or not ev:
        return None
    return {"start": s, "end": d.get("end"), "biblio": any(e.get("kind") == "bibliographic_record" for e in ev),
            "confidence": d.get("confidence")}

pids = sorted(passes["direct"])
rows, summ = [], {k: {"evidenced": {n: 0 for n in passes}, "pairs": {}, "agree3": 0, "a_candidates": 0, "events_with_2plus": 0} for k in KEYS}
for pid in pids:
    name = passes["direct"][pid].get("canonicalName")
    for key in KEYS:
        c = {n: cell(passes[n].get(pid, {}), key) for n in passes}
        for n in passes:
            summ[key]["evidenced"][n] += c[n] is not None
        have = [n for n in passes if c[n]]
        row = {"pid": pid, "name": name, "date": key, "values": {n: (c[n]["start"] if c[n] else None) for n in passes}}
        if len(have) >= 2:
            summ[key]["events_with_2plus"] += 1
        for a, b in itertools.combinations(passes, 2):
            if c[a] and c[b]:
                t = summ[key]["pairs"].setdefault(f"{a}-{b}", [0, 0])
                t[1] += 1
                t[0] += abs(c[a]["start"] - c[b]["start"]) <= TOL
        agree_sets = [set(x) for x in itertools.combinations(have, 2)
                      if abs(c[x[0]]["start"] - c[x[1]]["start"]) <= TOL]
        if len(have) >= 3 and all(abs(c[x]["start"] - c[y]["start"]) <= TOL for x, y in itertools.combinations(have, 2)):
            summ[key]["agree3"] += 1
        row["agreeing_pairs"] = [sorted(s) for s in agree_sets]
        if any(c[n]["biblio"] for s in agree_sets for n in s):
            summ[key]["a_candidates"] += 1
            row["a_candidate"] = True
        spread = [c[n]["start"] for n in have]
        row["spread"] = (max(spread) - min(spread)) if len(spread) > 1 else None
        rows.append(row)

out = {"tolerance_years": TOL, "events": len(pids), "summary": summ, "rows": rows}
(P / "three-way-comparison.json").write_text(json.dumps(out, indent=1))
for k in KEYS:
    s = summ[k]
    print(k, "evidenced", s["evidenced"], "| pair agreement", {a: f"{x}/{y}" for a, (x, y) in s["pairs"].items()},
          "| all-three agree", s["agree3"], "| A-candidates", s["a_candidates"])
big = [r for r in rows if r["spread"] is not None and r["spread"] > TOL]
print(len(big), "date cells where the evidenced passes differ by more than", TOL, "years")
