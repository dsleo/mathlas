#!/usr/bin/env python3
"""Per-field time series behind the 'map moves through time' mode.

A field is one of the lanes already used by the connection map (field_map_taxonomy.LANES).
An event belongs to the lane of its output field ('cl'). Island size is the cumulative number
of events in the lane; a lane emerges in the year of its first event. Positions come from scripts/layout_field_film.py. Cross-lane links come
from each event's stated input fields, mapped to lanes with the same classifier.
"""

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from field_map_taxonomy import LANES, map_lane  # noqa: E402

SRC = ROOT / "data/events.json"
OUT = ROOT / "data/field-film.json"
STOPS = [-2000, -1000, -500, 0, 500, 1000, 1300, 1500, 1600, 1700, 1750, 1800, 1850, 1900, 1925, 1950, 1975, 2000, 2025]
LINK_TYPES = {"birth-by-fusion": "fusion", "technique-transfer": "transfer", "dictionary-analogy": "analogy", "birth-by-abstraction": "abstraction", "reification": "reification", "split": "split"}


def load_events():
    return json.loads(SRC.read_text())


def lane_of_label(label):
    lane = map_lane({"to": [label], "name": ""})
    return lane


FAMILY = {
    "Number theory": 0, "Algebra": 1, "Group & representation theory": 1, "Category & homological algebra": 1,
    "Geometry": 2, "Differential geometry": 2, "Algebraic geometry": 2, "Topology": 3, "Algebraic topology": 3,
    "Analysis": 4, "Functional & harmonic analysis": 4, "Complex analysis": 4, "Approximation theory": 4, "Differential equations": 4,
    "Functional equations": 4, "Fluid mechanics": 4, "Solid mechanics": 4, "Dynamics": 4,
    "Probability": 5, "Statistics & decision theory": 5, "Game theory & economics": 5,
    "Logic & foundations": 6, "Computer science": 6, "Algorithms & complexity": 6, "Information & cryptography": 6,
    "Combinatorics": 7, "Graph theory": 7,
}
TYPES = [("technique-transfer", "Technique transfer", "#25805a"), ("birth-by-fusion", "Birth by fusion", "#9a7410"), ("birth-by-abstraction", "Birth by abstraction", "#b8532f"),
         ("import-from-outside", "Import from outside", "#b33f78"), ("dictionary-analogy", "Dictionary, analogy", "#2b6fb3"), ("reification", "Reification", "#7a4fb3"), ("split", "Split", "#4f7c82")]
LINK_TO_TYPE = {"transfer": 0, "fusion": 1, "abstraction": 2, "analogy": 4, "reification": 5, "split": 6}
TYPE_ALIAS = {"field-emergence": "birth-by-abstraction", "field-combination": "birth-by-fusion"}
LAYOUT = ROOT / "data/field-film-layout.json"  # written by scripts/layout_field_film.py
PAGE = ROOT / "public/index.html"
RUNTIME = ROOT / "public/data/field-film-runtime.json"

# the island styles of the proof map (its terrain generator knows five) and the lanes they suit
PROOF_FAMILY = {}
for _fam, _lanes in {
    "analytic": ["Analysis", "Approximation theory", "Functional & harmonic analysis", "Complex analysis", "Differential equations", "Functional equations", "Fluid mechanics", "Solid mechanics",
                 "Dynamics", "Mathematical physics", "Numerical analysis", "Applied mathematics", "Optimization & control", "Astronomy & trigonometry", "Geophysics & geodesy"],
    "algebraic": ["Number theory", "Algebra", "Group & representation theory", "Category & homological algebra", "Algebraic geometry"],
    "geometric": ["Geometry", "Differential geometry", "Topology", "Algebraic topology"],
    "discrete": ["Combinatorics", "Graph theory", "Probability", "Statistics & decision theory", "Game theory & economics"],
    "logic": ["Logic & foundations", "Computer science", "Algorithms & complexity", "Information & cryptography"],
}.items():
    for _name in _lanes:
        PROOF_FAMILY[_name] = _fam


# One mathematical symbol per event, in the vocabulary of the proof map's method marks: a keyword in the
# event's name or product first, otherwise the symbol of its field.
LANE_GLYPH = {
    "Astronomy & trigonometry": "sin", "Number theory": "\u2124", "Algebraic geometry": "Spec", "Geometry": "\u25b1", "Differential geometry": "\u2207",
    "Topology": "\u03c0\u2081", "Algebraic topology": "H", "Algebra": "\u27e8a\u27e9", "Group & representation theory": "G", "Category & homological algebra": "\u2243",
    "Analysis": "\u222b", "Approximation theory": "\u223c", "Functional & harmonic analysis": "\u2131", "Complex analysis": "\u2102", "Differential equations": "y\u2032",
    "Functional equations": "f\u2218f", "Fluid mechanics": "\u0394", "Solid mechanics": "\u03b5", "Probability": "\u2119", "Statistics & decision theory": "\u03c3",
    "Combinatorics": "#", "Graph theory": "\u21dd", "Logic & foundations": "\u2200", "Computer science": "\u03bb", "Algorithms & complexity": "O", "Numerical analysis": "\u2248",
    "Game theory & economics": "max", "Dynamics": "\u21ba", "Mathematical physics": "\u0127", "Geophysics & geodesy": "\u03c6", "Optimization & control": "\u03b4",
    "Information & cryptography": "\u2295", "Applied mathematics": "\u2248", "Other fields": "\u2022",
}
KEYWORD_GLYPH = [
    ("fourier", "\u2131"), ("wavelet", "\u03c8"), ("galois", "Gal"), ("ergodic", "\u21ba"), ("zeta", "\u03b6"), ("l-function", "\u03b6"), ("prime number", "\u03b6"),
    ("elliptic curve", "E"), ("modular form", "\u2261"), ("modular arithmetic", "\u2261"), ("congruence", "\u2261"), ("homolog", "H"), ("cohomolog", "H"), ("k-theory", "K"),
    ("topos", "\u2243"), ("categor", "\u2243"), ("functor", "\u2243"), ("sheaf", "\U0001d4d5"), ("scheme", "Spec"), ("lie ", "\U0001d524"), ("representation", "\u03c1"),
    ("fundamental group", "\u03c0\u2081"), ("homotop", "\u03c0\u2081"), ("morse", "\u2207"), ("differential form", "d\u03c9"), ("riemann", "\u03ba"), ("curvature", "\u03ba"),
    ("manifold", "M"), ("gauge", "A"), ("measure", "\u03c3"), ("lebesgue", "\u03c3"), ("martingale", "\u2119"), ("brownian", "\u2119"), ("probab", "\u2119"), ("random", "\u2119"),
    ("entropy", "H(X)"), ("information", "H(X)"), ("ramsey", "#"), ("generating function", "x\u207f"), ("graph", "\u21dd"), ("complexity", "O"), ("algorithm", "\u03bb"),
    ("computab", "\u03bb"), ("turing", "\u03bb"), ("set theory", "\u2135"), ("cardinal", "\u2135"), ("continuum", "\u2135"), ("axiom of choice", "AC"), ("incompleteness", "\u22a2"),
    ("proof theory", "\u22a2"), ("model theory", "\u22a8"), ("heat", "\u0394"), ("laplace", "\u0394"), ("navier", "\u0394"), ("fluid", "\u0394"), ("wave", "\u2202"),
    ("variational", "\u03b4"), ("calculus of variations", "\u03b4"), ("linear programming", "min"), ("convex", "\u2264"), ("fixed point", "f\u2218f"), ("chaos", "\u21ba"),
    ("dynamical", "\u21ba"), ("quantum", "\u0127"), ("relativity", "\u0127"), ("lattice", "\u2124\u00b2"), ("geometry of numbers", "\u2124\u00b2"), ("coding", "\u2295"),
    ("cryptograph", "\u2295"), ("fractal", "dim"), ("finite element", "\u2248"), ("numerical", "\u2248"), ("regression", "\u03c3"), ("statistic", "\u03c3"),
    ("sphere packing", "E\u2088"), ("index theorem", "ind"), ("calabi", "c\u2081"), ("mirror symmetry", "\u21c4"), ("moduli", "\U0001d4dc"), ("langlands", "L"), ("automorphic", "L"),
    ("dictionary", "\u2194"), ("forcing", "\u22a9"), ("diophantine", "\u2124[x]"), ("weil conjecture", "\u03b6"), ("quantum group", "U\u1d68"), ("deformation", "\u22c6"),
    ("d-module", "\U0001d49f"), ("building", "\u25b3"), ("moonshine", "j"), ("poisson", "{,}"), ("invariant theory", "\u27e8a\u27e9"), ("primes", "\u03c0(x)"), ("prime", "\u03c0(x)"),
    ("progression", "AP"), ("sieve", "\u03c0(x)"), ("symplectic", "\u03c9"), ("hodge", "H"), ("hyperbolic", "\u210d"), ("knot", "\u224d"), ("tropical", "max"),
    ("differential equation", "y\u2032"), ("calculus", "\u222b"), ("integral", "\u222b"), ("group", "G"), ("ring", "\u27e8a\u27e9"), ("ideal", "\u27e8a\u27e9"),
]


LANE_POOL = {
    "Astronomy & trigonometry": ["sin", "\u2220", "\u2299", "\u2609", "cos", "\u25cb", "tan"],
    "Applied mathematics": ["\u2248", "\u2207\u00b2", "\u03a3", "\u0394t", "\u221d"],
    "Game theory & economics": ["\u2264", "f\u2218f", "O", "\u03a0", "u(x)"],
    "Numerical analysis": ["\u2248", "\u03b4", "h", "O(h)"],
    "Fluid mechanics": ["\u0394", "\u2202\u209c", "v", "\u2207\u00b7"],
    "Number theory": ["\u2124", "p", "\u2261", "\u211a", "gcd", "\u03c0(x)", "\u230ax\u230b", "\u03c6(n)", "\u03bc(n)", "\u2124/n"],
    "Algebra": ["\u27e8a\u27e9", "\u2297", "F[x]", "det", "Aut", "\u211a", "\u2295", "\u2245", "ker", "\u2124[i]", "\U0001d53d\u2090"],
    "Algebraic geometry": ["Spec", "V(f)", "\U0001d4aa", "\u2297", "Proj", "\u2119\u207f", "\u03a9", "Pic", "\u2102\u2119\u00b9"],
    "Geometry": ["\u25b1", "\u2220", "\u03ba", "\u22a5", "dim", "\u25b3", "\u2225", "\u03c0", "\u25cb", "\u221a2"],
    "Differential geometry": ["\u2207", "\u03ba", "M", "d\u03c9", "Ric"],
    "Topology": ["\u03c0\u2081", "\u03c7", "\U0001d54a\u00b9", "\u2202M", "X", "\u222a", "\u2245", "\u2282\u2282", "\u228d", "\u2205"],
    "Algebraic topology": ["H", "\u03c0\u2081", "\u03c7", "\u222a", "Ext"],
    "Group & representation theory": ["G", "\u03c1", "\U0001d524", "Z(G)", "\u22ca", "|G|"],
    "Category & homological algebra": ["\u2243", "Hom", "\u2297", "Ext", "\u22a3"],
    "Analysis": ["\u222b", "lim", "\u03a3", "sup", "\u03b5", "\u221e", "\u03a0", "e\u02e3", "\u221a", "\u2202\u0305", "\u2113\u00b9"],
    "Functional & harmonic analysis": ["\u2131", "\u2016\u00b7\u2016", "\u03c8", "L\u00b2", "\u22a5"],
    "Complex analysis": ["\u2102", "\u222e", "z", "f\u2032", "Res"],
    "Differential equations": ["y\u2032", "\u0394", "\u2202", "\u2207\u00b2"],
    "Probability": ["\u2119", "\U0001d53c", "\u03c3", "Var", "\u03bc"],
    "Statistics & decision theory": ["\u03c3", "x\u0304", "p", "\u03c7\u00b2"],
    "Combinatorics": ["#", "n!", "C(n,k)", "\u03a3", "R"],
    "Graph theory": ["\u21dd", "K\u2085", "\u03c7(G)", "V,E"],
    "Logic & foundations": ["\u2200", "\u22a2", "\u22a8", "\u2135", "\u00ac", "\u2203"],
    "Computer science": ["\u03bb", "\u2192", "\u27e6\u27e7", "\u22a5"],
    "Algorithms & complexity": ["O", "P", "NP", "n\u00b2"],
    "Dynamics": ["\u21ba", "f\u2218f", "\u03bb", "\u03a6"],
    "Mathematical physics": ["\u0127", "H", "\u03c8", "\u0124"],
    "Optimization & control": ["\u03b4", "min", "\u2207f", "\u03bb"],
    "Information & cryptography": ["\u2295", "mod", "p", "H(X)"],
}
EXTRA_POOL = {
    "Combinatorics": ["\u2308x\u2309", "K\u2099", "\u220f", "(n k)", "\u2294", "\u03c3\u2099", "\u2205"],
    "Logic & foundations": ["\u22a5", "\u2208", "\u2205", "\u22a4", "\U0001d4ab(A)", "\u2227", "\u2228"],
    "Group & representation theory": ["Aut", "\u22b2", "S\u2099", "SO(3)", "SL\u2082", "Gal", "\u2124/n"],
    "Probability": ["P(A)", "N(0,1)", "\u03a9", "\u03bc(A)", "\u03c4", "\u2131\u209c"],
    "Differential geometry": ["TM", "g\u1d62\u2c7c", "exp", "K", "\u03c9", "\u2225\u00b7\u2225"],
    "Algebraic topology": ["H\u207f", "\u03c0\u2099", "\u03a9", "\u2202", "\u2297"],
    "Complex analysis": ["\u03b6", "\u210d", "e\u2071\u1dff", "\u221e", "\u2202\u0305"],
    "Functional & harmonic analysis": ["\u2113\u00b2", "\u2329\u00b7,\u00b7\u232a", "\u03b4", "\u03a3", "\u222b"],
    "Differential equations": ["\u03c6\u209c", "\u2202\u209c", "\u222b\u222b", "\u03bb", "u(x,t)"],
    "Number theory": ["\u2135", "\u03a3", "p\u1d4f", "\u2124\u209a"],
    "Statistics & decision theory": ["\u03bc", "\u03b2", "\u0398", "\U0001d53c"],
    "Algorithms & complexity": ["\u03a9", "\u0398", "log n", "2\u207f"],
}
GENERIC = {"group", "ring", "field", "graph", "measure", "function", "calculus", "integral", "statistic", "random", "numerical", "algorithm", "fluid", "wave", "heat"}


def glyph_candidates(event):
    """Glyphs for an event, best first: keyword matches by score (name x3, product/aliases/phases x2, summary and fields x1,
    generic words discounted), then its field's pool in an order that depends on the event's id."""
    name = (event.get("name") or "").lower() + " "
    mid = " ".join([event.get("product") or "", *(event.get("aliases") or []), *(event.get("phases") or [])]).lower() + " "
    low = " ".join([event.get("why") or "", *(event.get("from") or []), *(event.get("to") or [])]).lower() + " "
    scores = {}
    for order, (key, glyph) in enumerate(KEYWORD_GLYPH):
        hit = lambda text: re.search(r"(?<![a-z])" + re.escape(key), text) is not None  # word start: "ring" must not match "Sherrington"
        weight = max((3 if hit(name) else 0), (2 if hit(mid) else 0), (1 if hit(low) else 0))
        if weight:
            if key in GENERIC:
                weight *= 0.4
            scores[glyph] = scores.get(glyph, 0) + weight - order * 1e-6
    out = [g for g, v in sorted(scores.items(), key=lambda kv: -kv[1]) if v >= 0.8]
    pool = list(LANE_POOL.get(event["cl"], [])) + [g for g in EXTRA_POOL.get(event["cl"], []) if g not in LANE_POOL.get(event["cl"], [])]
    if pool:
        k = sum(ord(c) * (i + 1) for i, c in enumerate(event["pid"])) % len(pool)
        pool = pool[k:] + pool[:k]
    for g in pool + [LANE_GLYPH.get(event["cl"], "\u2022")]:
        if g not in out:
            out.append(g)
    return out


def importance(event):
    """How much the record says about an event: milestones, people, and a bonus for a directly checked record."""
    return len(event.get("ms") or []) + 0.5 * len(event.get("people") or []) + (2 if event.get("tier") == "direct" else 0)


# Curated symbols for the main events whose scored glyph was generic or misleading; unique within each island.
GLYPH_OVERRIDE = {
    "P000": "π", "P113": "ℙ²", "P134": "△", "P449": "∞",
    "P049": "ξ", "P089": "σᵢσⱼ", "P116": "(n k)", "P183": "P(A)", "P540": "Z",
    "P138": "x⁵", "P192": "det", "P379": "V(f)", "P458": "i",
    "P100": "∂f", "P386": "𝒟", "P403": "∫K", "P443": "E(k)", "P460": "eⁱˣ",
    "P453": "χ(G)", "P477": "λ₂", "Q1": "χ_B",
    "P016": "ζ", "P057": "𝔽q", "P082": "ℚₚ", "P126": "Dy²", "P385": "Gᵃᵇ",
    "P013": "‖·‖", "P217": "Ψ", "P251": "μ", "P528": "cos",
    "P170": "κ", "P355": "gᵢⱼ", "P371": "dω", "P413": "M",
    "P188": "Δφ", "P204": "sech", "P406": "xʳ", "P412": "ρ", "P496": "[L,A]",
    "P161": "℘", "P356": "ℂ", "P407": "ℂⁿ", "P415": "Δu",
    "P136": "x³", "P182": "∫ω", "P212": "Hét", "P256": "IH", "P289": "an", "P486": "tmf",
    "P263": "Eᵣ", "P260": "KK", "P322": "HF", "P363": "d(x,y)", "P383": "deg f", "P488": "θⱼ",
    "P066": "∧∨", "P262": "□", "P357": "ℵ₀", "P373": "ℝ", "P374": "S(n)", "P381": "∈", "P531": "ℤ",
    "P246": "Vir", "P332": "B(m,n)", "P382": "G", "P409": "w=1", "P420": "⟨X|R⟩", "P425": "|G|",
    "P064": "ed≡1", "P253": "GB", "P268": "△", "P507": "|ψ⟩",
    "P061": "Rμν", "P133": "F=ma", "P240": "ℂℙ³", "P454": "∂L",
    "P214": "Λ", "P224": "V(x)", "P367": "ẋ",
    "P221": "P", "P226": "K(x)", "P232": "Σ*", "P323": "NP",
    "P347": "[[n,k]]", "P278": "s→t", "P402": "δS", "P462": "u(t)",
    "P229": "Ω", "P261": "Def", "P538": "Sym",
    "P131": "P(A|B)", "P132": "Σr²", "P266": "θ", "P375": "r", "P456": "≻",
    "P119": "ρgh", "P284": "LP", "P416": "N′",
    "P149": "x₀", "P205": "h", "P220": "π≈",
    "P176": "60", "P459": "crd",
    "E25": "u(x)", "P215": "x*", "P509": "PPAD",
    "P470": "ε", "P558": "ρ", "P559": "Tₙ", "P561": "σε", "P562": "f(f)",
}


def assign_glyphs(events):
    """Main events (the few that carry an island's name on the map) get a symbol no other main event of the same
    field uses; every other event keeps its best symbol for its card but is drawn as a dot and a name."""
    import math
    by_field = defaultdict(list)
    for e in events:
        by_field[e["cl"]].append(e)
    out = {}
    for field, evs in by_field.items():
        evs.sort(key=lambda e: (-importance(e), e["pid"]))
        k = max(1, min(9, round(1 + 1.05 * math.sqrt(len(evs)))))
        used, mains = set(), []
        for rank, e in enumerate(evs):
            cands = glyph_candidates(e)
            words = {w for w in re.findall(r"[a-z]{4,}", unicodedata.normalize("NFKD", e.get("name") or "").encode("ascii", "ignore").decode().lower())}
            twin = any(len(words & w) >= 2 and len(words & w) / len(words | w) >= 0.4 for w in mains)  # near-duplicate title of a main event
            if len(mains) < k and not twin:
                mains.append(words)
                g = next((c for c in cands if c not in used), cands[0])
                g = GLYPH_OVERRIDE.get(e["pid"], g)
                used.add(g)
                out[e["pid"]] = (g, 1)
            else:
                out[e["pid"]] = (cands[0], 0)
    return out


def initials(event):
    people = event.get("people") or []
    name = people[0].get("name", "") if people and people[0] else ""
    parts = [x for x in name.split() if not re.match(r"^(de|der|des|du|van|von|la|le|el)$", x, re.I)]
    return "".join(x[0] for x in parts[:2]).upper()


def arrange(film, events_raw, placed):
    """Place every event inside its island by sub-topic: events that came from another field sit on the side
    facing that field; internal developments group by subject theme. Then relax so symbols never overlap.
    Coordinates are in the island's own unit frame (the page multiplies by the island radius)."""
    import math
    centre = {k: v for k, v in placed["positions"].items()}
    raw = {e["pid"]: e for e in events_raw}
    out = {}
    by_field = defaultdict(list)
    for e in film["events"]:
        by_field[e["field"]].append(e)
    for field, evs in by_field.items():
        evs.sort(key=lambda e: (e["year"], e["pid"]))
        n = len(evs)
        cx, cy = centre[field]
        pref, groups = [], defaultdict(list)
        for k, e in enumerate(evs):
            src = {lane_of_label(l) for l in raw[e["pid"]]["from"]} - {field, "Other fields"}
            src = [x for x in src if x in centre]
            if src:
                vx = sum(centre[x][0] - cx for x in src); vy = sum(centre[x][1] - cy for x in src)
                ang = math.atan2(vy, vx)
                key = ("from", round(ang, 1))
            else:
                th = glyph_candidates(raw[e["pid"]])[0]
                ang = (sum(ord(c) for c in th) % 360) / 180 * math.pi
                key = ("glyph", th)
            groups[key].append(k)
            pref.append(ang)
        rho = [0.0] * n
        for members in groups.values():
            for j, k in enumerate(members):
                rho[k] = 0.18 + 0.62 * (j + 0.5) / len(members)
        pos = [[math.cos(pref[k]) * rho[k], math.sin(pref[k]) * rho[k]] for k in range(n)]
        want = [p[:] for p in pos]
        area = math.pi * 0.82 ** 2
        dmin = math.sqrt(2 * area / (math.sqrt(3) * max(n, 1))) * 0.9
        nmain = sum(1 for e in evs if e.get("main"))
        dmain = math.sqrt(2 * area / (math.sqrt(3) * max(nmain, 1))) * 0.92  # the symbols are drawn large, so they spread out
        for step in range(400):
            t = 1 - step / 400
            force = [[0.0, 0.0] for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    dx, dy = pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]
                    d = math.hypot(dx, dy) or 1e-4
                    need = dmain if (evs[i].get("main") and evs[j].get("main")) else dmin
                    if d < need:
                        push = (need - d) * 0.5
                        force[i][0] += dx / d * push; force[i][1] += dy / d * push
                        force[j][0] -= dx / d * push; force[j][1] -= dy / d * push
            for i in range(n):
                force[i][0] += (want[i][0] - pos[i][0]) * 0.06
                force[i][1] += (want[i][1] - pos[i][1]) * 0.06
                pos[i][0] += force[i][0] * 0.6 * t + force[i][0] * 0.1
                pos[i][1] += force[i][1] * 0.6 * t + force[i][1] * 0.1
                r = math.hypot(pos[i][0], pos[i][1])
                lim = 0.62 if evs[i].get("main") else 0.84
                if r > lim:
                    pos[i][0] *= lim / r; pos[i][1] *= lim / r
        for e, p in zip(evs, pos):
            out[e["pid"]] = [round(p[0] * 1.18, 3), round(p[1] * 0.88, 3)]
    return out
TEMPLATE = ROOT / "scripts/film_template.html"


DETAILS = ROOT / "public/data/field-film-events.json"


CAVEAT = re.compile(r"infer|not (?:been )?(?:read|checked|verified)|editorial|characterisation|rests on|naming candidate|not a priority claim", re.I)
DATEY = re.compile(r"\b(?:years?|dates?|dated|crossref|open library|reprint|translation|submission|edition|venue|zbmath|publication|original)\b", re.I)


def clean_milestone(m):
    """UI copy: drop confidence grades and date-bookkeeping notes; keep only caveats about the claim itself (shown behind an info icon)."""
    m = {k: v for k, v in m.items() if k != "c"}
    note = m.get("n")
    if note and not (CAVEAT.search(note) and not DATEY.search(note)):
        m["n"] = None
    return m


def write_details(events):
    """Milestones, sources and people for the drawer and the core-sample view; fetched on first use."""
    out = {}
    for e in events:
        out[e["pid"]] = {"why": e.get("why"), "ms": [clean_milestone(m) for m in e.get("ms") or []], "people": e.get("people") or [], "grade": e.get("grade") or {}}
    DETAILS.parent.mkdir(parents=True, exist_ok=True)
    DETAILS.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print(f"wrote {DETAILS.relative_to(ROOT)} ({DETAILS.stat().st_size // 1024} KB)")


ART = ROOT / "public/data/field-film-art.json"


NOT_MATHEMATICIANS = {"Roshdi Rashed"}


def landmarks(events_raw, film):
    """Mathematicians who are *primary* in at least three events (the first person listed, or an originator or systematiser;
    a name that merely appears among the developers does not count) stand as statues on every island where they are primary
    in an event, at most four statues per island, spaced round the shore."""
    import math
    from collections import defaultdict
    names = [f["id"] for f in film["fields"]]
    primary = defaultdict(list)
    credited = defaultdict(int)
    info = {}
    for e in events_raw:
        for k, person in enumerate(e.get("people") or []):
            name = person.get("name")
            if not name or name in NOT_MATHEMATICIANS:
                continue
            credited[name] += 1
            info.setdefault(name, person)
            if k == 0 or person.get("role") in ("originator", "systematiser"):
                primary[name].append(e)
    ranked = sorted(((n, v) for n, v in primary.items() if len(v) >= 3), key=lambda kv: -len(kv[1]))
    per_island = defaultdict(list)
    out = []
    for name, evs in ranked:
        by_home = defaultdict(list)
        for e in evs:
            by_home[e["cl"]].append(e)
        for home, mine in by_home.items():
            if len(per_island[home]) >= 4:
                continue
            per_island[home].append(len(out))
            mine = sorted(mine, key=lambda e: e["y"])
            out.append({"name": name, "life": info[name].get("life"), "url": info[name].get("url"), "f": names.index(home), "e": [e["pid"] for e in mine],
                        "all": [e["pid"] for e in sorted(evs, key=lambda e: e["y"])], "credited": credited[name], "y": mine[0]["y"]})
    for home, members in per_island.items():
        for k, idx in enumerate(sorted(members, key=lambda i: out[i]["y"])):
            angle = (1 + 2 * k) * math.pi / (2 * len(members)) + math.pi * 0.35 + (sum(ord(c) for c in home) % 7) * 0.2
            out[idx]["x"], out[idx]["z"] = round(math.cos(angle) * 1.18 * 0.8, 3), round(math.sin(angle) * 0.88 * 0.8, 3)
    return out


def write_page(film):
    names = [f["id"] for f in film["fields"]]
    tindex = {t[0]: i for i, t in enumerate(TYPES)}
    placed = json.loads(LAYOUT.read_text())
    data = {
        "world": placed["box"],
        "types": [{"id": t[0], "name": t[1], "color": t[2]} for t in TYPES],
        "fields": [{"id": f["id"], "x": f["x"], "y": f["y"], "n": f["events"], "fam": PROOF_FAMILY[f["id"]], "first": f["firstYear"]} for f in film["fields"]],
        "events": [{"p": e["pid"], "y": e["year"], "a": e["approx"], "t": tindex[TYPE_ALIAS.get(e["type"], e["type"])], "f": names.index(e["field"]), "n": e["name"], "g": e["glyph"], "m": e["main"], "w": e["weight"], "s": e["from"], "i": e["initials"], "c": e["cid"], "x": e["x"], "z": e["z"]} for e in film["events"]],
        "links": [{"a": names.index(l["from"]), "b": names.index(l["to"]), "y": l["year"], "t": LINK_TO_TYPE.get(l["type"], 2)} for l in film["links"] if l["from"] in names and l["to"] in names],
        "ships": [{"y": s["year"], "t": names.index(s["to"])} for s in film["ships"] if s["to"] in names],
        "people": film["people"],
        "searchPeople": film["searchPeople"],
    }
    RUNTIME.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    html = TEMPLATE.read_text()
    PAGE.write_text(html)
    fonts = ROOT / "public/fonts"
    fonts.mkdir(exist_ok=True)
    katex = ROOT / "node_modules/katex/dist/fonts"  # real Computer Modern, with true italics and blackboard bold
    for out_name, src_name in {"lm-main-regular": "Main-Regular", "lm-main-italic": "Main-Italic", "lm-main-bold": "Main-Bold", "lm-main-bolditalic": "Main-BoldItalic",
                               "lm-sans-regular": "SansSerif-Regular", "lm-sans-italic": "SansSerif-Italic", "lm-sans-bold": "SansSerif-Bold",
                               "lm-ams": "AMS-Regular", "lm-fraktur": "Fraktur-Regular", "lm-caligraphic": "Caligraphic-Regular", "lm-math-italic": "Math-Italic"}.items():
        (fonts / f"{out_name}.woff2").write_bytes((katex / f"KaTeX_{src_name}.woff2").read_bytes())
    print(f"wrote {RUNTIME.relative_to(ROOT)} ({RUNTIME.stat().st_size//1024} KB)")
    print(f"wrote {PAGE.relative_to(ROOT)} ({len(html)//1024} KB)")


def main():
    events = load_events()
    write_details(events)
    by_field = defaultdict(list)
    for e in events:
        by_field[e["cl"]].append(e["y"])
    fields = []
    for lane in LANES:
        years = sorted(by_field.get(lane, []))
        if not years:
            continue
        fields.append({
            "id": lane, "events": len(years), "firstYear": years[0],
            "sizes": {str(stop): sum(1 for y in years if y <= stop) for stop in STOPS},
        })
    fields.sort(key=lambda f: f["firstYear"])
    links, ships, splits = [], [], []
    for e in events:
        kind = e["type"]
        target = e["cl"]
        if kind == "import-from-outside":
            ships.append({"pid": e["pid"], "year": e["y"], "to": target, "cargo": e["from"][:3], "name": e["name"]})
            continue
        sources = {lane_of_label(label) for label in e["from"]} - {target, "Other fields"}
        for src in sorted(sources):
            row = {"pid": e["pid"], "year": e["y"], "type": LINK_TYPES.get(kind, kind), "from": src, "to": target, "name": e["name"]}
            (splits if kind == "split" else links).append(row)
    GL = assign_glyphs(events)
    names_idx = {f["id"]: i for i, f in enumerate(fields)}
    events_out = [{"pid": e["pid"], "year": e["y"], "approx": e.get("approx", False), "type": e["type"], "field": e["cl"], "name": e["name"], "tier": e["tier"], "glyph": GL[e["pid"]][0], "main": GL[e["pid"]][1], "weight": round(importance(e), 1), "from": sorted({names_idx[lane_of_label(l)] for l in e["from"] if lane_of_label(l) in names_idx and lane_of_label(l) != e["cl"]}), "initials": initials(e), "cid": e["id"]} for e in events]
    placed = json.loads(LAYOUT.read_text())
    for f in fields:
        f["x"], f["y"] = placed["positions"][f["id"]]
    film = {"method": __doc__.strip(), "stops": STOPS, "fields": fields, "links": links, "ships": ships, "splits": splits, "events": events_out}
    spots = arrange(film, events, placed)
    for e in events_out:
        e["x"], e["z"] = spots[e["pid"]]
    film["box"] = placed["box"]
    film["people"] = landmarks(events, film)
    people_index = defaultdict(set)
    for event in events:
        for person in event.get("people") or []:
            name = person.get("name")
            if name:
                people_index[name].add(event["pid"])
    year_by_pid = {event["pid"]: event["year"] for event in events_out}
    film["searchPeople"] = [
        {"n": name, "p": sorted(pids, key=year_by_pid.__getitem__)}
        for name, pids in sorted(people_index.items())
    ]
    OUT.write_text(json.dumps(film, ensure_ascii=False, indent=1) + "\n")
    (ROOT / "data/field-film-families.json").write_text(json.dumps(PROOF_FAMILY, indent=1) + "\n")
    import subprocess
    subprocess.run(["node", str(ROOT / "scripts/build_film_art.mjs")], check=True, cwd=ROOT)
    write_page(film)
    print(f"{len(fields)} fields, {len(links)} links, {len(ships)} ships, {len(splits)} split links, {len(events_out)} events")
    print(Counter(l["type"] for l in links))
    for f in fields:
        print(f"{f['firstYear']:>6} {f['id']:<34} {f['events']:>3}  1800:{f['sizes']['1800']:>3} 1900:{f['sizes']['1900']:>3} 2025:{f['sizes']['2025']:>3}")


if __name__ == "__main__":
    main()
