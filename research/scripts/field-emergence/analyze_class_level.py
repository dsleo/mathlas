#!/usr/bin/env python3
"""Class-level run: apply detect.py to the MSC class-pair matrix and grade against the seed events.

  python3 -I analyze_class_level.py matrix MATRIX.jsonl OUT.json [--window 5]

MATRIX.jsonl is the output of the `matrix` route (one line per review year, keys 'A|B' for pairs
and 'A|A' for single-class totals, plus classified_docs). Windows are `--window` years wide
(default 5) and must be fully covered by fetched years. Counts are by zbMATH REVIEW year (0-11
years after publication), so onsets lag publication; an onset is accepted for an event if it falls
from the start of the expected decade to the end of the following decade.

No threshold is tuned on the seed events: detect.Params defaults are used (kappa='mass').
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from detect import detect, Params

CONS = os.path.join(HERE, "..", "..", "data", "collection", "event-msc-map-consensus.json")


def load_matrix(path, width):
    rows = {}
    for l in open(path):
        r = json.loads(l)
        rows[r["year"]] = r
    years = sorted(rows)
    wins = []
    y = years[0]
    while y + width - 1 <= years[-1]:
        if all(yy in rows for yy in range(y, y + width)):
            wins.append((y, y + width - 1))
        y += width
    return rows, wins


def build(rows, wins, min_total):
    classes, pair_acc = {}, {}
    T = len(wins)
    N = np.zeros(T)
    for t, (y0, y1) in enumerate(wins):
        for y in range(y0, y1 + 1):
            r = rows[y]
            N[t] += r.get("classified_docs") or 0
            for k, n in r["pairs"].items():
                a, b = k.split("|")
                if a == b:
                    classes.setdefault(a, np.zeros(T))[t] += n
                else:
                    pair_acc.setdefault((a, b), np.zeros(T))[t] += n
    cl = sorted(classes)
    ci = {c: i for i, c in enumerate(cl)}
    nc = np.array([classes[c] for c in cl])
    keep = [p for p, v in pair_acc.items() if v.sum() >= min_total and p[0] in ci and p[1] in ci]
    keep.sort()
    n_ab = np.array([pair_acc[p] for p in keep])
    pidx = np.array([[ci[a], ci[b]] for a, b in keep])
    return cl, nc, keep, n_ab, pidx, N


def decade_range(s):
    y = int(s[:4])
    return y, y + 9


def main():
    mode, path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    width = int(sys.argv[sys.argv.index("--window") + 1]) if "--window" in sys.argv else 5
    min_total = 30
    rows, wins = load_matrix(path, width)
    cl, nc, pairs, n_ab, pidx, N = build(rows, wins, min_total)
    T = len(wins)
    prm = Params(kappa="mass", n_neighbors=400)
    t0 = time.time()
    res = detect(n_ab, nc, nc, N, pair_index=pidx, params=prm)
    print(f"{len(pairs)} pairs x {T} windows, detect {time.time() - t0:.0f}s", file=sys.stderr)

    onset = res["onset"]
    q = res["q_final"]
    flagged = (q <= prm.fdr) & (onset >= 0)
    E = res["E"]
    big = np.nanmax(E, axis=1) >= 10
    pi = {p: i for i, p in enumerate(pairs)}
    Sfree = np.nanmax(np.where(np.isfinite(res["scan"]["S_raw"]), res["scan"]["S_raw"], -1), axis=1)
    logE = np.log10(np.maximum(np.nanmax(E, axis=1), 1e-3))
    order_E = np.argsort(logE)
    logE_sorted = logE[order_E]
    S_sorted_by_E = Sfree[order_E]

    def pct(i):
        """(global percentile, size-matched percentile) of the pair's ungated evidence S_free;
        size-matched = among pairs whose largest expected count is within a factor 10^0.25."""
        g = float((Sfree <= Sfree[i]).mean())
        lo_i = np.searchsorted(logE_sorted, logE[i] - 0.25, side="left")
        hi_i = np.searchsorted(logE_sorted, logE[i] + 0.25, side="right")
        seg = S_sorted_by_E[lo_i:hi_i]
        return g, float((seg <= Sfree[i]).mean())

    # event grading: pairs from the consensus file (first mapper + blind AI pass)
    cons = json.load(open(CONS))["events"]

    def eval_pairs(pairlist, lo, hi):
        best = None
        top_pct = -1.0
        order = {"hit": 0, "early": 1, "late": 2, "not flagged": 3}
        for a, b in pairlist:
            k = tuple(sorted((a, b)))
            i = pi.get(k)
            if i is None:
                st = {"pair": list(k), "status": "not in matrix (fewer than %d documents)" % min_total}
            else:
                o = int(onset[i])
                g_pct, m_pct = pct(i)
                st = {"pair": list(k), "q_final": float(q[i]), "p_final": float(res["p_final"][i]),
                      "evidence_percentile_global": round(g_pct, 4), "evidence_percentile_size_matched": round(m_pct, 4),
                      "onset_window": None if o < 0 else f"{wins[o][0]}-{wins[o][1]}",
                      "max_expected": float(np.nanmax(E[i])), "total_docs": int(n_ab[i].sum())}
                if flagged[i]:
                    st["status"] = "hit" if lo <= wins[o][0] <= hi else ("early" if wins[o][0] < lo else "late")
                else:
                    st["status"] = "not flagged"
            if best is None or order.get(st["status"], 4) < order.get(best["status"], 4):
                best = st
            if "evidence_percentile_size_matched" in st:
                top_pct = max(top_pct, st["evidence_percentile_size_matched"])
        if best is not None:
            best = dict(best)
            best["best_size_matched_percentile_over_pairs"] = top_pct if top_pct >= 0 else None
        return best

    table = []
    for e in cons:
        if e["detectability"] == "none" or not e["expectedWindow"]:
            continue
        lo = decade_range(e["expectedWindow"][0])[0]
        hi = decade_range(e["expectedWindow"][-1])[1] + 10   # review-year lag allowance: through the next decade
        allp = [tuple(p) for p in e["consensusPairs"] + e["onlyInMap"] + e["onlyInBlind"]]
        consp = [tuple(p) for p in e["consensusPairs"]]
        if not allp:
            continue
        table.append({"id": e["id"], "set": e["set"], "name": e["name"], "detectability": e["detectability"],
                      "agreement": e["agreement"], "expectedWindow": e["expectedWindow"],
                      "n_pairs_in_matrix": sum(1 for p in allp if tuple(sorted(p)) in pi),
                      "best_pair": eval_pairs(allp, lo, hi),
                      "best_consensus_pair": eval_pairs(consp, lo, hi) if consp else None})

    # base rate: share of all big pairs flagged with an onset in the accepted range, per expected window
    def base_rate(lo, hi):
        ok = flagged & big
        starts = np.array([w[0] for w in wins])
        sel = np.array([lo <= starts[o] <= hi if o >= 0 else False for o in onset])
        return float((ok & sel).sum() / max(1, big.sum()))

    summary = {
        "windows": [f"{a}-{b}" for a, b in wins], "n_classes": len(cl), "n_pairs_tested": len(pairs),
        "pairs_with_max_expected_ge_10": int(big.sum()),
        "flagged_q_le_0.05": int(flagged.sum()), "flagged_among_ge_10": int((flagged & big).sum()),
        "nu": float(res["nu"]), "psi": float(res["psi"]),
        "kappa": [round(float(k), 3) for k in res["kappa"]],
    }
    status_counts = {}
    for t in table:
        s = t["best_pair"]["status"]
        status_counts[s] = status_counts.get(s, 0) + 1
    summary["event_status_counts"] = status_counts
    cc2 = {}
    for t in table:
        if t["best_consensus_pair"]:
            k = t["best_consensus_pair"]["status"]
            cc2[k] = cc2.get(k, 0) + 1
    summary["event_status_counts_consensus_pairs_only"] = cc2
    use = [t for t in table if t["best_pair"] and t["best_pair"].get("best_size_matched_percentile_over_pairs") is not None]
    pcts = [t["best_pair"]["best_size_matched_percentile_over_pairs"] for t in use]
    ks = [max(1, t["n_pairs_in_matrix"]) for t in use]
    screen = {"n_events_with_pair": len(use)}
    for c in (0.8, 0.9, 0.95, 0.99):
        top = round(100 * (1 - c))
        obs = sum(1 for p in pcts if p >= c) / max(1, len(pcts))
        chance = sum(1 - c ** k for k in ks) / max(1, len(ks))   # P(at least one of k pairs lands in the top X%) if ranks were uniform
        screen[f"top_{top}pct"] = {"observed": round(obs, 3), "chance": round(chance, 3)}
    screen["note"] = ("share of events whose best pair ranks in the top X% of size-matched pairs by ungated evidence, "
                      "against the share expected if ranks were uniform given each event's number of pairs")
    summary["screen_recall_size_matched"] = screen
    hits_by_det = {}
    for t in table:
        d = t["detectability"]
        hits_by_det.setdefault(d, {"n": 0, "hit": 0})
        hits_by_det[d]["n"] += 1
        hits_by_det[d]["hit"] += t["best_pair"]["status"] == "hit"
    summary["hits_by_detectability"] = hits_by_det
    # base rate for a typical expected window (decade 2000s plus next) as a reference
    summary["base_rate_flagged_onset_in_window"] = {
        f"{a}-{b}": round(base_rate(a, b), 4) for a, b in [(1970, 1989), (1980, 1999), (1990, 2009), (2000, 2019)]}

    order = np.argsort(q)
    top = []
    for i in order[:300]:
        if not flagged[i]:
            continue
        top.append({"pair": list(pairs[i]), "onset": f"{wins[onset[i]][0]}-{wins[onset[i]][1]}", "q": float(q[i]),
                    "total_docs": int(n_ab[i].sum())})
    json.dump({"note": "class-level run by zbMATH review year (SPARQL matrix); see FIELD_EMERGENCE_CLASSLEVEL.md",
               "summary": summary, "events": table, "top_flagged": top}, open(out, "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
