#!/usr/bin/env python3
"""Place the fields of the time-lapse map so that total bridge length is minimal without any overlap.

Objective: minimise sum over field pairs of sqrt(number of links between them) x (distance between their centres),
subject to every island, drawn at its final size, staying clear of every other island (ellipse-aware, with a gap).
Many random restarts, a penalty continuation, and the best feasible layout is written to
data/field-film-layout.json. Needs numpy and scipy; build_field_film.py only reads the result.
"""

import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
FILM = ROOT / "data/field-film.json"
OUT = ROOT / "data/field-film-layout.json"
BOX = (1500.0, 1080.0)
GAP = 18.0
RESTARTS = 24


def island_radius(count):
    """World-pixel radius of a field holding `count` events (the page uses the same formula)."""
    return 4.6 * (3 + 2.3 * np.sqrt(count))


def main():
    film = json.loads(FILM.read_text())
    fields = film["fields"]
    names = [f["id"] for f in fields]
    idx = {n: i for i, n in enumerate(names)}
    n = len(names)
    count = np.array([f["events"] for f in fields], float)
    r = island_radius(count)
    rx, ry = 1.34 * r, 1.02 * r  # islands are wider than tall
    weight = np.zeros((n, n))
    for link in film["links"]:
        a, b = idx.get(link["from"]), idx.get(link["to"])
        if a is not None and b is not None and a != b:
            weight[a, b] += 1
            weight[b, a] += 1
    I, J = np.triu_indices(n, 1)
    w = np.sqrt(weight[I, J])  # a pair with 100 links pulls 10x as hard as a pair with one, not 100x

    def radius_along(i, ang):
        return rx[i] * ry[i] / np.sqrt((ry[i] * np.cos(ang)) ** 2 + (rx[i] * np.sin(ang)) ** 2)

    def parts(x):
        p = x.reshape(n, 2)
        dx, dy = p[I, 0] - p[J, 0], p[I, 1] - p[J, 1]
        dist = np.sqrt(dx * dx + dy * dy + 1e-6)
        ang = np.arctan2(dy, dx)
        overlap = np.maximum(0, radius_along(I, ang) + radius_along(J, ang) + GAP - dist)
        return p, dist, overlap

    def energy(x, lam):
        p, dist, overlap = parts(x)
        e = (w * dist).sum() / 100 + lam * (overlap ** 2).sum()
        lo = np.maximum(0, np.column_stack([rx, ry]) - p)
        hi = np.maximum(0, p + np.column_stack([rx, ry]) - np.array(BOX))
        return e + lam * ((lo ** 2).sum() + (hi ** 2).sum())

    rng = np.random.default_rng(1)
    best, lengths = None, []
    for _ in range(RESTARTS):
        x = np.column_stack([rng.uniform(rx, BOX[0] - rx), rng.uniform(ry, BOX[1] - ry)]).ravel()
        for lam in (0.01, 0.1, 1, 10, 100, 1000, 10000):
            x = minimize(energy, x, args=(lam,), method="L-BFGS-B", options={"maxiter": 400}).x
        p, dist, overlap = parts(x)
        inside = (p[:, 0] - rx >= -1).all() and (p[:, 1] - ry >= -1).all() and (p[:, 0] + rx <= BOX[0] + 1).all() and (p[:, 1] + ry <= BOX[1] + 1).all()
        if overlap.max() > 1.0 or not inside:
            continue
        length = float((w * dist).sum())
        lengths.append(length)
        if best is None or length < best[0]:
            best = (length, p.copy())
    if best is None:
        raise SystemExit("no feasible layout found; enlarge BOX")
    length, p = best
    OUT.write_text(json.dumps({
        "objective": "sum of (sqrt(links) x centre distance)", "totalWeightedLength": round(length), "restarts": RESTARTS, "feasible": len(lengths),
        "worstFeasible": round(max(lengths)), "box": list(BOX), "gap": GAP,
        "positions": {names[i]: [round(float(p[i, 0]), 1), round(float(p[i, 1]), 1)] for i in range(n)},
    }, indent=1) + "\n")
    print(f"best total weighted length {length:,.0f} (worst feasible restart {max(lengths):,.0f}, {len(lengths)}/{RESTARTS} feasible)")


if __name__ == "__main__":
    main()
