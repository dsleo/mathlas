"""Identity and relationship rules for the public Field Emergence Map.

The source catalogue keeps separate provenance records. The map presents one
event per historical development, while retaining every source ID and useful
milestone. Shared catalogue roots are reviewed: a later proof of an earlier
conjecture remains a separate event and gets a directed connection.
"""

import copy
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from field_map_taxonomy import map_lane


# Same development entered by different collection passes. The first PID is
# stable and remains the public URL; the others redirect to it.
SAME_EVENT = {
    "P395": "P011",  # Poincare's Analysis situs to group-valued homology
    "P354": "P004",  # Euler to the consolidation of graph theory
    "P359": "P012",  # Hilbert's ideals to Noether's rings
    "P202": "P035",  # Gromov's symplectic topology
    "P293": "P036",  # conjecture, Moonshine module, and Borcherds's proof
    "P298": "P049",  # Hairer's regularity structures
    "P302": "P082",  # Scholze's perfectoid spaces and tilting
    "P365": "P199",  # ergodic hypothesis to rigorous ergodic theory
    "P255": "P069",  # Quillen's 1973 higher algebraic K-theory
    "P329": "P079",  # the 2006 measure-rigidity/QUE development, with Littlewood milestones
}

# Shared source roots, but different historical events: statement/problem then
# proof/solution. These are directed links, not duplicate records.
SEQUELS = {
    ("P023", "P259"): "Weil conjectures to Deligne's proof",
    ("P040", "P295"): "Modularity conjecture to Wiles's proof",
    ("P050", "P300"): "Discrepancy problem to Tao's solution",
    ("P480", "P241"): "Incidence-algebra method to Rota's combinatorial theory",
}

# Reviewed continuation or application of a named subject. These are shown as
# context, because a shared name alone does not document direct influence.
NAMED_BRANCHES = {
    ("P000", "P178"): "quadrature and areas",
    ("P000", "P194"): "Archimedean volume methods",
    ("P001", "P122"): "algebra in the Islamic mathematical tradition",
    ("P003", "P018"): "probabilistic methods in combinatorics",
    ("P005", "P053"): "analytic number theory and the zeta function",
    ("P011", "P263"): "homotopy methods and spectral sequences",
    ("P011", "E36"): "topological methods in combinatorics",
    ("P010", "P358"): "geometry through continuous transformation groups",
    ("P020", "E50"): "arithmetic progressions",
    ("P027", "P079"): "homogeneous dynamics and measure rigidity",
    ("P026", "P307"): "Langlands programme / local Langlands",
    ("P029", "P510"): "random matrix statistics",
    ("P032", "P485"): "noncommutative geometry",
    ("P033", "P341"): "four-manifold gauge theory",
    ("P037", "P294"): "moduli spaces of curves",
    ("P007", "P046"): "Fourier methods in sphere packing",
    ("P336", "P049"): "singular stochastic PDE methods",
    ("P056", "P348"): "o-minimality",
    ("P059", "P350"): "analytic methods for additive number theory",
    ("P062", "P491"): "three-manifold topology",
    ("P070", "P492"): "geometric invariant theory and stability",
    ("P071", "P337"): "Calabi-Yau geometry",
    ("P082", "P542"): "perfectoid geometry",
    ("P084", "P503"): "wavelets and sparse signal representation",
    ("P091", "P325"): "geometry of groups and nonpositive curvature",
    ("P092", "P082"): "non-archimedean analytic geometry",
    ("P093", "P549"): "rational points and Diophantine geometry",
    ("P094", "P476"): "sieve methods in number theory",
    ("P097", "P238"): "Morse theory and Floer homology",
    ("P098", "P524"): "microlocal and spectral analysis",
    ("P110", "P151"): "graphing motion and mathematical dynamics",
    ("P119", "P133"): "mathematical statics and mechanics",
    ("P445", "P430"): "vibrating strings and spectral methods",
    ("P120", "P453"): "Euler characteristic and map colouring",
    ("P111", "P196"): "Indian place-value numerals",
    ("P112", "P191"): "projective geometry",
    ("P116", "P117"): "binomial coefficients in probability",
    ("P121", "P158"): "trigonometry in the Islamic mathematical tradition",
    ("P123", "P114"): "Diophantine problems and Fermat",
    ("P124", "P009"): "algebraic number theory",
    ("P127", "P121"): "spherical astronomy and trigonometry",
    ("P130", "P132"): "probability and least squares",
    ("P132", "P376"): "least squares and statistical inference",
    ("P131", "P266"): "Bayesian inference",
    ("P133", "P151"): "mechanics and differential equations",
    ("P136", "P125"): "geometric study of cubic equations",
    ("P137", "P124"): "congruences and the Chinese remainder theorem",
    ("P138", "P006"): "polynomial equations and group theory",
    ("P139", "P191"): "geometric representation and coordinates",
    ("P140", "P138"): "symbolic algebra and equations",
    ("P141", "P121"): "sine and spherical trigonometry",
    ("P149", "P173"): "polynomial equation solving in China",
    ("P145", "P066"): "algebraic logic",
    ("P146", "P002"): "precursors to differential calculus",
    ("P152", "P376"): "probability and statistical inference",
    ("P153", "P166"): "Jacobi's theta-function work",
    ("P156", "P195"): "incommensurability and the theory of proportion",
    ("P158", "P198"): "trigonometry as an independent subject",
    ("P163", "P142"): "infinite series",
    ("P134", "P164"): "arithmetic books of Euclid's Elements",
    ("P165", "P133"): "planetary motion and Newtonian mechanics",
    ("P168", "P130"): "demography and probability",
    ("P170", "P118"): "curves and differential geometry",
    ("P172", "P448"): "the parallel postulate and non-Euclidean geometry",
    ("P176", "P459"): "Greek astronomy and chord tables",
    ("P177", "P122"): "al-Karaji's polynomial and binomial work",
    ("P180", "P373"): "foundations of analysis",
    ("P182", "P356"): "Abelian integrals and Riemann surfaces",
    ("P184", "P127"): "Greek mathematical astronomy",
    ("P185", "P150"): "De Moivre and complex trigonometry",
    ("P189", "P127"): "spherical trigonometry and astronomy",
    ("P192", "P429"): "determinants and matrix algebra",
    ("P193", "P460"): "trigonometry and complex algebra",
    ("P194", "P002"): "infinitesimal volumes and calculus",
    ("P197", "P195"): "ratios and the theory of proportion",
    ("P195", "P134"): "Eudoxus's proportion theory in Euclid",
    ("P198", "P193"): "trigonometry applied to algebra",
    ("P270", "P205"): "numerical methods for differential equations",
    ("P220", "P266"): "Monte Carlo methods",
    ("P230", "P546"): "type theory and foundations",
    ("P261", "P075"): "deformation theory and quantization",
    ("P232", "P262"): "formal languages and verification",
    ("P238", "P490"): "Floer homology",
    ("P238", "P543"): "Floer homology",
    ("P239", "P262"): "finite automata and verification",
    ("P257", "P461"): "model theory and nonstandard analysis",
    ("P257", "P038"): "model theory in Diophantine geometry",
    ("P264", "P343"): "tableaux and representation theory",
    ("P282", "P055"): "Riemann-Roch theorem",
    ("P290", "P470"): "Sobolev methods for partial regularity",
    ("P289", "E30"): "modern algebraic geometry",
    ("P294", "P321"): "Weil-Petersson volumes and topological recursion",
    ("P296", "Q22"): "distance-set geometry",
    ("P307", "P542"): "local Langlands",
    ("P301", "P077"): "motivic homotopy and the norm-residue problem",
    ("P221", "P315"): "computational complexity and geometric complexity theory",
    ("P212", "P303"): "cohomology theories in arithmetic geometry",
    ("P238", "P101"): "virtual cycles in Floer theory",
    ("P325", "P491"): "special cube complexes and virtual Haken",
    ("P363", "P440"): "metric spaces and dimension",
    ("P373", "P387"): "real-number foundations of geometry",
    ("P382", "P358"): "abstract and continuous groups",
    ("P390", "P525"): "Ramsey theory",
    ("P390", "P074"): "Ramsey theory in Banach spaces",
    ("P389", "P418"): "p-adic local methods and the Hasse principle",
    ("P392", "P033"): "gauge theory",
    ("P398", "P439"): "transcendence of pi",
    ("P405", "P227"): "many-valued and fuzzy logic",
    ("P397", "P011"): "Betti numbers",
    ("P435", "P437"): "measure theory and normal numbers",
    ("P012", "P408"): "commutative algebra and abstract rings",
    ("P411", "P391"): "group representations",
    ("P417", "P266"): "subjective probability and Bayesian inference",
    ("P444", "P128"): "complex analysis and the fundamental theorem of algebra",
    ("P450", "P011"): "topology from geometry of position",
    ("P419", "P384"): "characters and finite-group representations",
    ("P452", "P421"): "knot tabulation and knot theory",
    ("P459", "P189"): "spherical trigonometry",
    ("P465", "P069"): "Bott periodicity and K-theory",
    ("P469", "P102"): "singular integrals and Hardy spaces",
    ("P488", "P547"): "equivariant homotopy methods",
    ("P475", "P524"): "spectral theory and quantum chaos",
    ("P482", "P313"): "semidefinite methods and approximation",
    ("P499", "P348"): "Hodge theory",
    ("P514", "P107"): "homogeneous dynamics",
    ("P514", "P079"): "homogeneous dynamics and measure rigidity",
    ("P369", "P108"): "Markov processes and large deviations",
    ("P381", "P095"): "axiomatic set theory and forcing",
    ("P199", "P100"): "statistical mechanics and rigorous dynamics",
    ("P199", "P108"): "statistical mechanics and probability",
    ("P493", "P101"): "enumerative geometry and virtual cycles",
    ("P221", "P478"): "the mathematical study of algorithms",
    ("P478", "P479"): "algorithm analysis and analytic combinatorics",
    ("P496", "P495"): "soliton equations and finite-gap integration",
    ("P520", "P271"): "Brownian paths and stochastic calculus",
    ("P438", "Q62"): "Diophantine approximation and irrationality",
    ("P438", "P398"): "Liouville's transcendence work",
    ("P009", "P537"): "class groups in algebraic number theory",
    ("P517", "P338"): "contact topology",
    ("P523", "P300"): "distinct discrepancy problems",
    ("P548", "P527"): "quantum-field amplitudes",
    ("P350", "B33"): "Kakeya methods",
    ("E30", "P317"): "schemes and derived algebraic geometry",
    ("E32", "P531"): "Hilbert's tenth problem",
    ("E33", "P272"): "Atiyah-Singer index theorem",
    ("P453", "P063"): "four-colour problem",
    ("P464", "P279"): "characteristic classes",
    ("P510", "P339"): "Tracy-Widom distributions",
}

# Related records for which the catalogue supports comparison but not a
# directed dependency (including work in separate mathematical traditions).
RELATED_PEERS = {
    ("P002", "P129"): "infinite-series approaches to calculus",
    ("P003", "P183"): "early writing on games of chance",
    ("P015", "P391"): "group representations and quantum mechanics",
    ("P116", "P155"): "binomial-coefficient triangles",
    ("P147", "P192"): "determinants in separate traditions",
    ("P148", "P154"): "finite-difference methods",
    ("P175", "P187"): "early Indian combinatorics",
    ("E25", "P250"): "distinct branches of game theory",
}

# Similar titles and dates, but one is a genuine specialization of the other.
DISTINCT_SUBFIELDS = {
    frozenset(("E25", "P250")),  # strategic games versus combinatorial games
    frozenset(("P134", "P164")),  # whole Elements versus its arithmetic books
    frozenset(("P246", "P540")),  # CFT versus Liouville CFT construction
}

# One publication can introduce more than one mathematical development.
DISTINCT_SHARED_WORKS = {
    frozenset(("P013", "P360")),  # Volterra functionals and functional analysis
    frozenset(("P322", "P341")),  # Seiberg-Witten theory and its invariants
    frozenset(("P356", "P415")),  # Riemann surfaces and Dirichlet's principle
    frozenset(("P398", "P438")),  # Liouville's method and later transcendence proofs
}

NAME_OVERRIDES = {
    "P036": "Monstrous moonshine",
    # Keep the whole Elements distinct from its arithmetic sub-books.
    "P134": "Euclid's Elements: axiomatic geometry",
    "P164": "Euclid's Elements VII–IX: deductive arithmetic",
}

# This source-first record dates a proof event to the earlier conjecture. Keep
# the earlier milestones as context, but date the event to the published proof.
REFOCUS = {"P259": (1974, "Deligne's proof")}

# Every visible tag has been reviewed as a name for the whole entry. Other
# source aliases remain in searchTerms, where related concepts are useful.
VISIBLE_ALIASES = json.loads((Path(__file__).resolve().parents[1] / "data/collection/field-map-visible-aliases.json").read_text())


def norm(value):
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = value.casefold().replace("programme", "program").replace("–", "-")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def source_ids(value):
    return set(re.findall(r"[A-Z]+\d+", value or ""))


def unique_terms(terms, title=""):
    """Keep one visible spelling per term; retain raw terms for search."""
    seen = {norm(title)}
    result = []
    for term in terms:
        key = norm(term)
        if key and key not in seen:
            result.append(term)
            seen.add(key)
    return result


def display_aliases(pid, terms, title):
    """Use the reviewed display list; broad source terms stay searchable."""
    shown = VISIBLE_ALIASES.get(pid, [])
    available = {norm(term) for term in terms}
    if any(norm(term) not in available for term in shown):
        raise ValueError(f"Visible alias missing from source terms: {pid}")
    if len({norm(term) for term in shown}) != len(shown) or norm(title) in {norm(term) for term in shown}:
        raise ValueError(f"Redundant visible alias: {pid}")
    return shown


def _milestone_key(m):
    role, year = m.get("r"), m.get("y")
    if role in {"first_statement", "first_application", "naming", "consolidation", "institution"}:
        return role, year
    return role, year, norm(m.get("l"))


def merge_events(events):
    by_id = {e["pid"]: copy.deepcopy(e) for e in events}
    grouped = defaultdict(list)
    for event in events:
        grouped[SAME_EVENT.get(event["pid"], event["pid"])].append(event["pid"])
    result = []
    for primary, members in grouped.items():
        main = by_id[primary]
        main["sourceIds"] = sorted(set().union(*(source_ids(by_id[p]["id"]) for p in members)))
        main["mergedPids"] = sorted(p for p in members if p != primary)
        search = list(main.get("aliases") or [])
        milestones = {_milestone_key(m): m for m in main["ms"]}
        people = {norm(p["name"]): p for p in main["people"]}
        for pid in members:
            if pid == primary:
                continue
            extra = by_id[pid]
            search.extend([extra["name"], *(extra.get("aliases") or [])])
            for m in extra["ms"]:
                key = _milestone_key(m)
                if key not in milestones:
                    main["ms"].append(m)
                    milestones[key] = m
                else:
                    existing = milestones[key]
                    urls = {x.get("u") for x in existing.get("ev") or []}
                    existing["ev"].extend(x for x in m.get("ev") or [] if x.get("u") not in urls)
            for p in extra["people"]:
                key = norm(p["name"])
                if key not in people:
                    main["people"].append(p)
                    people[key] = p
                else:
                    present = {w.get("u") or norm(w.get("c")) for w in people[key]["works"]}
                    people[key]["works"].extend(w for w in p["works"] if (w.get("u") or norm(w.get("c"))) not in present)
            main["phases"] = unique_terms([*main["phases"], *extra["phases"]])
            if extra["tier"] == "direct" and main["tier"] != "direct":
                main["tier"] = "direct"
            if extra["y"] is not None and (main["y"] is None or extra["y"] < main["y"]):
                main["y"] = extra["y"]
                main["approx"] = extra["approx"]
        main["name"] = NAME_OVERRIDES.get(primary, main["name"])
        main["searchTerms"] = unique_terms(search, main["name"])
        main["aliases"] = display_aliases(primary, search, main["name"])
        main["ms"].sort(key=lambda m: (m.get("y") is None, m.get("y") or 0))
        result.append(main)
    return result


def refocus_solution(event):
    if event["pid"] not in REFOCUS:
        return False
    year, marker = REFOCUS[event["pid"]]
    proof = [m for m in event["ms"] if m.get("y") == year and marker.casefold() in (m.get("l") or "").casefold()]
    if len(proof) != 1:
        raise ValueError(f"Expected one dated proof milestone for {event['pid']}")
    for m in event["ms"]:
        if m.get("y") is not None and m["y"] < year and m["r"] != "precursor":
            m["r"] = "precursor"
    proof[0]["r"] = "first_statement"
    return True


def audit_shared_roots(events):
    """Fail the build if a new shared source ID has no identity decision."""
    roots = defaultdict(list)
    for e in events:
        for root in source_ids(e["id"]):
            roots[root].append(e["pid"])
    reviewed = {frozenset((child, parent)) for child, parent in SAME_EVENT.items()}
    reviewed |= {frozenset(pair) for pair in SEQUELS}
    unknown = [(root, pids) for root, pids in roots.items() if len(pids) > 1 and frozenset(pids) not in reviewed]
    if unknown:
        raise ValueError(f"Unreviewed shared catalogue IDs: {unknown}")


def audit_near_duplicates(events):
    """Catch same-period title containment even when catalogue IDs differ."""
    reviewed = {frozenset((child, parent)) for child, parent in SAME_EVENT.items()}
    reviewed |= {frozenset(pair) for pair in SEQUELS}
    reviewed |= DISTINCT_SUBFIELDS
    unknown = []
    for i, a in enumerate(events):
        for b in events[i + 1:]:
            if a["y"] is None or b["y"] is None or abs(a["y"] - b["y"]) > 3:
                continue
            left, right = set(norm(a["name"]).split()), set(norm(b["name"]).split())
            left -= {"the", "and", "of", "from", "with", "for", "in", "to", "on", "its", "a", "an", "by", "via"}
            right -= {"the", "and", "of", "from", "with", "for", "in", "to", "on", "its", "a", "an", "by", "via"}
            if min(len(left), len(right)) >= 2 and (left <= right or right <= left):
                if frozenset((a["pid"], b["pid"])) not in reviewed:
                    unknown.append((a["pid"], b["pid"], a["name"], b["name"]))
    if unknown:
        raise ValueError(f"Unreviewed same-period name overlaps: {unknown}")


def audit_shared_first_statements(events):
    """Check pairs that claim the same first public work for distinct events."""
    works = defaultdict(set)
    for event in events:
        for milestone in event["ms"]:
            if milestone.get("r") == "first_statement" and milestone.get("w") and milestone.get("y") is not None:
                key = (milestone["y"], norm(milestone["w"]))
                if len(key[1]) >= 20:
                    works[key].add(event["pid"])
    unknown = []
    for (year, work), pids in works.items():
        if len(pids) > 1 and frozenset(pids) not in DISTINCT_SHARED_WORKS:
            unknown.append((year, work, sorted(pids)))
    if unknown:
        raise ValueError(f"Unreviewed shared first-statement works: {unknown}")


def audit_visible_aliases(events):
    """Ensure the reviewed list is current and no visible tag is duplicated."""
    by_id = {event["pid"]: event for event in events}
    missing = set(VISIBLE_ALIASES) - set(by_id)
    if missing:
        raise ValueError(f"Visible aliases assigned to missing events: {sorted(missing)}")
    labels = defaultdict(list)
    for event in events:
        for alias in event["aliases"]:
            labels[norm(alias)].append(event["pid"])
    repeated = {alias: pids for alias, pids in labels.items() if len(pids) > 1}
    if repeated:
        raise ValueError(f"Visible aliases repeated across events: {repeated}")


def _tokens(text):
    stop = {"the", "and", "of", "from", "with", "for", "in", "to", "on", "its", "a", "an", "by", "via", "theory", "method", "methods", "geometric", "algebraic", "analytic", "number", "fields", "field", "geometry", "analysis", "topology", "physics", "program", "programs", "spaces", "structures", "functions", "groups", "representations", "curves", "conjecture", "problem", "higher", "abstract", "random", "computer", "computational", "algorithmic", "topological"}
    return set(norm(text).split()) - stop


def _field_name(text):
    """Remove explanatory parentheses from a catalogue field label."""
    return norm(re.sub(r"\([^)]*\)", "", text or ""))


def _output_concepts(event):
    """Fields explicitly named as a result or at the start of an event title."""
    product = event.get("product") or ""
    parts = [product, *re.split(r"\s*[;/]\s*|\s+and\s+", product)]
    concepts = {_field_name(part): 3 for part in parts if _field_name(part)}
    title = re.split(r"[:(]", event["name"], maxsplit=1)[0]
    prefix = re.split(r"\s+(?:from|and|via)\s+", title, maxsplit=1)[0]
    if len(_field_name(prefix).split()) >= 2:
        concepts[_field_name(prefix)] = max(concepts.get(_field_name(prefix), 0), 2)
    for field in set(concepts) | {_field_name(x) for x in event["from"]}:
        if field and (_field_name(title) == field or _field_name(title).startswith(field + " from ") or _field_name(title).startswith(field + " and ")):
            concepts[field] = max(concepts.get(field, 0), 2)
    return concepts


def build_relations(events):
    """Link field flows, named descendants, and reviewed problem-to-proof pairs."""
    freq = Counter(x for e in events for x in set(map(norm, e["from"] + e["to"])))
    token_freq = Counter(t for e in events for t in _tokens(e["name"]))
    rare_fields = lambda fs: {norm(x): x for x in fs if freq[norm(x)] <= 8}
    by_id = {e["pid"]: e for e in events}
    for e in events:
        e["rel"] = {"b": [], "a": [], "s": []}
        e["cl"] = map_lane(e)
    edges = {}

    def add(a, b, kind, label):
        if a == b or a not in by_id or b not in by_id:
            return
        A, B = by_id[a], by_id[b]
        if A["y"] is None or B["y"] is None:
            return
        delta = B["y"] - A["y"]
        if kind == "same":
            A["rel"]["s"].append({"p": b, "f": label, "d": delta, "t": kind})
            B["rel"]["s"].append({"p": a, "f": label, "d": -delta, "t": kind})
        else:
            A["rel"]["a"].append({"p": b, "f": label, "d": delta, "t": kind})
            B["rel"]["b"].append({"p": a, "f": label, "d": delta, "t": kind})
        edges[(a, b)] = kind

    for A in events:
        for B in events:
            if A is B or A["y"] is None or B["y"] is None:
                continue
            delta = B["y"] - A["y"]
            feed = set(rare_fields(A["to"])) & set(rare_fields(B["from"]))
            if feed and 0 < delta <= 80:
                field = sorted(feed)[0]
                if (A["pid"], B["pid"]) not in edges:
                    add(A["pid"], B["pid"], "feeds", rare_fields(B["from"])[field])
            product = norm(A.get("product"))
            if product and len(product.split()) >= 2 and 0 < delta <= 100 and (A["pid"], B["pid"]) not in edges:
                target = norm(re.split(r"[:(]", B["name"], maxsplit=1)[0])
                if product == target or product in set(map(norm, B["from"])):
                    add(A["pid"], B["pid"], "feeds", A["product"])
            if A["pid"] < B["pid"] and set(rare_fields(A["from"])) & set(rare_fields(B["from"])) and set(rare_fields(A["to"])) & set(rare_fields(B["to"])):
                field = sorted(set(rare_fields(A["to"])) & set(rare_fields(B["to"])))[0]
                if (A["pid"], B["pid"]) not in edges:
                    add(A["pid"], B["pid"], "same", rare_fields(B["to"])[field])

    # A rare named concept can seed a more specific descendant even when one
    # catalogue pass called its output "Number theory" and another "Geometry".
    for A in events:
        for B in events:
            if A is B or A["y"] is None or B["y"] is None:
                continue
            delta = B["y"] - A["y"]
            if not 0 < delta <= 100 or (A["pid"], B["pid"]) in edges:
                continue
            source_name = re.split(r"[:(]", A["name"], maxsplit=1)[0]
            target_name = re.split(r"[:(]", B["name"], maxsplit=1)[0]
            target_fields = " ".join(B["from"] + B["to"])
            source_terms = _tokens(source_name)
            common = source_terms & (_tokens(target_name) | _tokens(target_fields))
            distinctive = {t for t in common if len(t) >= 6 and token_freq[t] <= 12}
            proper_names = {t for t in distinctive if re.search(rf"\S+\s+{re.escape(t.capitalize())}\b", source_name) and re.search(rf"\b{re.escape(t.capitalize())}\b", target_name + " " + target_fields)}
            rare_subject = {t for t in distinctive if token_freq[t] <= 3 and len(t) >= 7 and norm(source_name).endswith(t)}
            if (len(source_terms) >= 2 and len(distinctive) >= 2) or (len(source_terms) == 1 and proper_names) or rare_subject:
                label = ", ".join(sorted(distinctive)[:2])
                add(A["pid"], B["pid"], "feeds", label)

    for (a, b), label in SEQUELS.items():
        if (a, b) not in edges:
            add(a, b, "feeds", label)

    for (a, b), label in NAMED_BRANCHES.items():
        if (a, b) not in edges:
            same_year = a in by_id and b in by_id and by_id[a]["y"] == by_id[b]["y"]
            add(a, b, "same" if same_year else "named", label)

    for (a, b), label in RELATED_PEERS.items():
        if (a, b) not in edges and (b, a) not in edges:
            add(a, b, "same", label)

    focused_path = Path(__file__).resolve().parents[1] / "data/collection/field-map-focused-additions.json"
    for addition in json.loads(focused_path.read_text())["entries"]:
        for link in addition["links"]:
            a, b = link["from"], link["to"]
            if a not in by_id or b not in by_id or not link["evidence"].startswith("https://"):
                raise ValueError(f"Invalid focused map link: {a} -> {b}")
            if by_id[a]["y"] >= by_id[b]["y"]:
                raise ValueError(f"Focused map link is not forward in time: {a} -> {b}")
            if (a, b) not in edges:
                add(a, b, link["kind"], link["label"])

    # A catalogue pass may call the same field "Commutative algebra" in one
    # product and "commutative algebra (ideals)" in a later input. Attach the
    # earliest explicit source for each distinctive input field. These are
    # context links, not claims that one particular paper caused the other.
    input_freq = Counter(_field_name(field) for e in events for field in set(e["from"]))
    outputs = {e["pid"]: _output_concepts(e) for e in events}
    for B in events:
        for raw_field in B["from"]:
            field = _field_name(raw_field)
            if not field or input_freq[field] > 16 or (len(field.split()) < 2 and (len(field) < 7 or input_freq[field] > 8)):
                continue
            candidates = []
            for A in events:
                if A is B or A["y"] is None or B["y"] is None or not 0 < B["y"] - A["y"] <= 500:
                    continue
                score = outputs[A["pid"]].get(field, 0)
                if score:
                    candidates.append((-score, A["y"], A["pid"]))
            if candidates:
                _, _, source = min(candidates)
                if (source, B["pid"]) not in edges:
                    add(source, B["pid"], "context", raw_field)

    # Broad foundation labels would make a hairball if joined to every later
    # use. Give each explicit foundation one earliest catalogue successor.
    for source, field in (("P001", "algebra"), ("P003", "probability")):
        A = by_id[source]
        followers = sorted(
            (B for B in events if B["y"] is not None and B["y"] > A["y"]
             and field in {_field_name(x) for x in B["from"]}),
            key=lambda B: (B["y"], B["pid"]),
        )
        if followers and (source, followers[0]["pid"]) not in edges:
            add(source, followers[0]["pid"], "context", field)

    for e in events:
        for k in "bas":
            e["rel"][k] = sorted(e["rel"][k], key=lambda r: (r["t"] in {"context", "named"}, abs(r["d"])))
    return sorted((a, b, kind) for (a, b), kind in edges.items())
