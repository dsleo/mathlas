#!/usr/bin/env python3
"""Curate the ten source-led direct events into the milestone schema.

The source ledger supplies identities, aliases, biographies and baseline works.
Additional stages below use separately checked publication records. Unknown
origin dates remain unknown; no catalogue date is promoted by default.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/collection/enrichment/batch-02-direct.json"
TARGET = ROOT / "data/collection/enrichment/second/milestones1.json"


def e(claim, source, url, kind="bibliographic_record"):
    return {"claim": claim, "source": source, "url": url, "kind": kind}


def m(role, year, label, description, work, people, evidence, *, phase=None, confidence="medium", note=None):
    item = {"role": role, "year": year, "precision": "year" if year is not None else "unknown",
            "label": label, "work": work, "people": people, "description": description,
            "evidence": evidence if isinstance(evidence, list) else [evidence], "confidence": confidence}
    if phase:
        item["phase"] = phase
    if note:
        item["note"] = note
    return item


def extra(person, citation, year, url, why):
    person["works"].append({"citation": citation, "year": year, "url": url, "whyItMatters": why})


def build():
    base = {r["eventId"]: r for r in json.loads(SOURCE.read_text())["events"]}
    rows = []

    x = base["E25"]
    mini = "J. von Neumann, Zur Theorie der Gesellschaftsspiele, Math. Ann. 100 (1928)"
    mini_ev = e("Published minimax article in 1928", "Mathematische Annalen / Crossref", "https://doi.org/10.1007/BF01448847")
    book_ev = e("First edition of the named book, 1944", "Open Library", "https://openlibrary.org/books/OL186826M/Theory_of_Games_and_Economic_Behavior")
    x["milestones"] = [
        m("first_statement", 1928, "Von Neumann formulates minimax games", "The article gives a mathematical framework for two-person zero-sum games.", mini, ["John von Neumann"], mini_ev, confidence="high", note="This publication truly makes the statement and applies its minimax method; see the adjacent milestone for the second role."),
        m("first_application", 1928, "Minimax applied to strategic games", "Von Neumann uses the minimax principle on the target class of strategic games.", mini, ["John von Neumann"], mini_ev, confidence="high", note="The same article truly plays both first-statement and first-application roles."),
        m("consolidation", 1944, "Theory of Games and Economic Behavior", "Von Neumann and Morgenstern establish a named book-length treatment of game theory.", "J. von Neumann and O. Morgenstern, Theory of Games and Economic Behavior (1944)", ["John von Neumann"], book_ev, confidence="high"),
        m("key_development", 1950, "Nash's n-person equilibrium", "Nash extends strategic equilibrium beyond two-person zero-sum games.", "J. Nash, Equilibrium points in n-person games, PNAS 36 (1950)", ["John Nash"], e("Published n-person equilibrium paper, 1950", "PNAS / Crossref", "https://doi.org/10.1073/pnas.36.1.48"), confidence="high"),
    ]
    extra(x["people"][0], "Theory of Games and Economic Behavior (with Oskar Morgenstern)", 1944, book_ev["url"], "Named systematic book")
    x["notes"] += " Borel's earlier game papers remain a priority precursor, but no particular one was dated here without a checked publication record."
    rows.append(x)

    x = base["E30"]
    ega1 = "A. Grothendieck, Éléments de géométrie algébrique I: Le langage des schémas, Publ. Math. IHÉS 4 (1960)"
    ega_ev = e("EGA I published in 1960 with the language of schemes", "Numdam / IHÉS", "https://numdam.org/item/PMIHES_1960__4__5_0/")
    x["phases"] = ["Scheme language", "Scheme geometry"]
    x["milestones"] = [
        m("first_statement", 1960, "EGA I states the scheme language", "The first checked public systematic definition of schemes appears in EGA I.", ega1, ["Alexander Grothendieck"], ega_ev, phase="Scheme language", confidence="medium", note="Earlier 1958 lectures and notes may contain the definition; their publication timing has not been established. EGA I truly plays both statement and consolidation roles."),
        m("consolidation", 1960, "EGA I consolidates the language", "The book-length treatment makes schemes the working language of algebraic geometry.", ega1, ["Alexander Grothendieck"], ega_ev, phase="Scheme language", confidence="high", note="This publication truly serves both as the first checked statement and systematic consolidation."),
        m("first_application", 1961, "EGA II applies schemes to morphisms", "The second installment develops global classes of morphisms using the scheme framework.", "A. Grothendieck, EGA II: Étude globale élémentaire de quelques classes de morphismes, Publ. Math. IHÉS 8 (1961)", ["Alexander Grothendieck"], e("EGA II published 28 December 1961", "Numdam / IHÉS", "https://numdam.org/item/PMIHES_1961__8__5_0/"), phase="Scheme geometry", confidence="high", note="EGA I already uses examples, but EGA II is the first separate checked target-problem development; the prior flat direct pass put methodological at 1960."),
    ]
    extra(x["people"][0], "Éléments de géométrie algébrique II: Étude globale élémentaire de quelques classes de morphismes", 1961, "https://numdam.org/item/PMIHES_1961__8__5_0/", "Early application of schemes to morphisms")
    x["notes"] += " Conceptual 1960 means first checked public definition, not proof that no earlier printed exposition exists. Methodological 1960 versus 1961 remains an interpretation question."
    rows.append(x)

    x = base["E32"]
    dpr = "M. Davis, H. Putnam and J. Robinson, The decision problem for exponential Diophantine equations, Ann. Math. 74 (1961)"
    dpr_ev = e("1961 reduction to exponential Diophantine equations", "Annals of Mathematics / JSTOR", "https://doi.org/10.2307/1970289")
    mat = "Yu. Matiyasevich, The Diophantineness of enumerable sets, Dokl. Akad. Nauk SSSR 191 (1970)"
    mat_ev = e("Original Russian article published in 1970", "Math-Net.Ru", "https://www.mathnet.ru/dan35274")
    x["milestones"] = [
        m("precursor", 1961, "Davis–Putnam–Robinson reduction", "The reduction makes the missing exponential-Diophantine step decisive but does not yet solve Hilbert's tenth problem.", dpr, ["Julia Robinson"], dpr_ev, confidence="high"),
        m("first_statement", 1970, "Matiyasevich closes Hilbert's tenth problem", "The article establishes the Diophantineness result needed for the negative solution.", mat, ["Yuri Matiyasevich"], mat_ev, confidence="high", note="The paper truly states the result and applies logic to the target decision problem."),
        m("first_application", 1970, "Undecidability follows for Hilbert's tenth", "The Diophantine representation is used to finish the algorithmic unsolvability argument.", mat, ["Yuri Matiyasevich"], mat_ev, confidence="high", note="The same paper truly plays both statement and purposeful-application roles."),
        m("key_development", 1972, "Detailed account of Diophantine sets", "Matiyasevich gives a fuller account of the result and the logic behind it.", "Yu. Matiyasevich, Diophantine sets, Russian Math. Surveys 27 (1972)", ["Yuri Matiyasevich"], e("Detailed survey published in 1972", "Math-Net.Ru / journal record", "https://www.mathnet.ru/eng/rm5112"), confidence="medium"),
    ]
    extra(x["people"][0], "Diophantine sets", 1972, "https://www.mathnet.ru/eng/rm5112", "Fuller account of the result")
    rows.append(x)

    x = base["E33"]
    ati = "M. Atiyah and I. Singer, The index of elliptic operators on compact manifolds, Bull. AMS 69 (1963)"
    ati_ev = e("Published theorem announcement in 1963", "AMS / Crossref", "https://doi.org/10.1090/S0002-9904-1963-10957-X")
    x["milestones"] = [
        m("precursor", 1960, "Gel'fand poses the index problem", "Gel'fand asks for topological information about the index of elliptic operators.", None, ["Israel Gel'fand"], e("Gel'fand's 1960 index question", "Atiyah's historical account", "https://celebratio.org/Atiyah_MF/article/40/", "history_page"), confidence="medium"),
        m("first_statement", 1963, "Atiyah–Singer theorem announced", "Atiyah and Singer publish the equality of analytic and topological indices.", ati, ["Michael Atiyah", "Isadore Singer"], ati_ev, confidence="high", note="The announcement truly gives both the theorem statement and its index application."),
        m("first_application", 1963, "Topological index computes analytic index", "The index formula is applied to elliptic operators on compact manifolds.", ati, ["Michael Atiyah", "Isadore Singer"], ati_ev, confidence="high", note="The same published announcement truly plays both statement and application roles."),
        m("key_development", 1968, "Detailed proof in the Annals", "The first paper in the index-operator series gives the detailed K-theoretic proof.", "M. Atiyah and I. Singer, The index of elliptic operators I, Ann. Math. 87 (1968)", ["Michael Atiyah", "Isadore Singer"], e("Annals paper published in 1968", "Annals / JSTOR", "https://doi.org/10.2307/1970715"), confidence="high"),
    ]
    rows.append(x)

    x = base["E36"]
    lov = "L. Lovász, Kneser's conjecture, chromatic number, and homotopy, JCTA 25 (1978)"
    lov_ev = e("1978 published proof using homotopy", "Journal of Combinatorial Theory / Crossref", "https://doi.org/10.1016/0097-3165(78)90022-5")
    x["milestones"] = [
        m("precursor", 1955, "Kneser states the coloring conjecture", "The combinatorial problem predates its topological solution.", None, ["Martin Kneser"], e("Kneser's 1955 Aufgabe 360 is cited in later mathematical literature", "Kneser problem bibliography", "https://www.math.unam.mx/~urrutia/online_papers/knesser.pdf", "history_page"), confidence="medium", note="Some catalogues list the problem in a 1956 issue; check the original issue before treating this as an exact publication anchor."),
        m("first_statement", 1978, "Lovász proves Kneser's conjecture", "The paper states the graph-coloring result through a topological argument.", lov, ["László Lovász"], lov_ev, confidence="high", note="This paper truly states the result and applies topology to the combinatorial target."),
        m("first_application", 1978, "Homotopy used on Kneser graphs", "Lovász applies the topology of a graph complex to the chromatic-number problem.", lov, ["László Lovász"], lov_ev, confidence="high", note="The same paper truly plays both statement and first-application roles."),
        m("key_development", 1978, "Bárány's short topological proof", "A different short proof follows using Borsuk–Ulam ideas.", "I. Bárány, A short proof of Kneser's conjecture, JCTA 25 (1978)", ["Imre Bárány"], e("Short proof in JCTA 25, 1978", "Journal of Combinatorial Theory / Crossref", "https://doi.org/10.1016/0097-3165(78)90023-7"), confidence="medium"),
    ]
    rows.append(x)

    x = base["E42"]
    jon = "V. Jones, A polynomial invariant for knots via von Neumann algebras, Bull. AMS 12 (1985)"
    jon_ev = e("Published 1985 knot-invariant article", "AMS / Crossref", "https://doi.org/10.1090/S0273-0979-1985-15304-2")
    x["milestones"] = [
        m("first_statement", 1985, "Jones polynomial published", "Jones announces a polynomial knot invariant arising from von Neumann algebra methods.", jon, ["Vaughan Jones"], jon_ev, confidence="high", note="The discovery is often dated 1984, but the checked public paper is 1985. It truly makes both statement and application."),
        m("first_application", 1985, "Operator algebras applied to knots", "The published construction deliberately transfers algebraic operator methods to knot theory.", jon, ["Vaughan Jones"], jon_ev, confidence="high", note="The same paper truly plays both statement and purposeful-application roles."),
        m("key_development", 1987, "Braid-group and link-polynomial extension", "Jones develops Hecke-algebra representations and a two-variable link invariant.", "V. Jones, Hecke algebra representations of braid groups and link polynomials, Ann. Math. 126 (1987)", ["Vaughan Jones"], e("Annals article, volume 126 (1987), pages 335–388", "Annals of Mathematics", "https://annals.math.princeton.edu/1987/126-2/p05"), confidence="high"),
    ]
    extra(x["people"][0], "Hecke algebra representations of braid groups and link polynomials", 1987, "https://doi.org/10.2307/1971403", "Extends the operator-algebraic knot invariant")
    rows.append(x)

    x = base["E49"]
    sle = "O. Schramm, Scaling limits of loop-erased random walks and uniform spanning trees, arXiv:math/9904022 (1999)"
    sle_ev = e("Public preprint submitted in 1999", "arXiv", "https://arxiv.org/abs/math/9904022")
    x["milestones"] = [
        m("first_statement", 1999, "Schramm proposes stochastic Loewner evolution", "The public preprint identifies a conformally invariant scaling-limit framework.", sle, ["Oded Schramm"], sle_ev, confidence="high", note="The 2000 journal publication is the same work; the public 1999 posting governs."),
        m("first_application", 1999, "Scaling limits targeted at LERW and UST", "The construction is directed at loop-erased walks and uniform spanning trees.", sle, ["Oded Schramm"], sle_ev, confidence="high", note="The same preprint truly plays both first-statement and purposeful-application roles."),
        m("key_development", 2001, "LERW and UST conformal invariance proved", "Lawler, Schramm and Werner identify the LERW scaling limit with SLE(2).", "G. Lawler, O. Schramm and W. Werner, Conformal invariance of planar loop-erased random walks and uniform spanning trees, arXiv:math/0112234 (2001)", ["Oded Schramm"], e("Public preprint submitted in 2001", "arXiv", "https://arxiv.org/abs/math/0112234"), confidence="high"),
    ]
    extra(x["people"][0], "Scaling limits of loop-erased random walks and uniform spanning trees (preprint)", 1999, sle_ev["url"], "First public SLE formulation")
    extra(x["people"][0], "Conformal invariance of planar loop-erased random walks and uniform spanning trees (with Lawler and Werner)", 2001, "https://arxiv.org/abs/math/0112234", "Proof of a predicted scaling limit")
    rows.append(x)

    x = base["E50"]
    gt = "B. Green and T. Tao, The primes contain arbitrarily long arithmetic progressions, arXiv:math/0404188 (2004)"
    gt_ev = e("Public preprint submitted in 2004", "arXiv", "https://arxiv.org/abs/math/0404188")
    x["milestones"] = [
        m("precursor", 2003, "Green proves Roth's theorem in the primes", "Green's three-term progression result is a precursor to arbitrary lengths.", "B. Green, Roth's theorem in the primes, arXiv:math/0302311 (2003)", ["Ben Green"], e("Public preprint submitted in 2003", "arXiv", "https://arxiv.org/abs/math/0302311"), confidence="high"),
        m("first_statement", 2004, "Green–Tao theorem made public", "The preprint states that primes contain arbitrarily long arithmetic progressions.", gt, ["Ben Green", "Terence Tao"], gt_ev, confidence="high", note="The preprint truly states the theorem and applies a relative Szemerédi method; its journal form appeared in 2008."),
        m("first_application", 2004, "Transference method applied to primes", "The proof uses a pseudorandom majorant and relative combinatorial method on the primes.", gt, ["Ben Green", "Terence Tao"], gt_ev, confidence="high", note="The same preprint truly plays both statement and purposeful-application roles."),
    ]
    extra(x["people"][0], "Roth's theorem in the primes", 2003, "https://arxiv.org/abs/math/0302311", "Immediate three-term precursor")
    rows.append(x)

    x = base["E51"]
    x["phases"] = ["Finite-field Kakeya", "Polynomial partitioning"]
    x["milestones"] = [
        m("first_application", 2008, "Dvir applies polynomials to finite-field Kakeya", "A low-degree polynomial argument proves the finite-field Kakeya bound.", "Z. Dvir, On the size of Kakeya sets in finite fields, arXiv:0803.2336 (2008)", ["Zeev Dvir"], e("Public preprint submitted in March 2008", "arXiv", "https://arxiv.org/abs/0803.2336"), phase="Finite-field Kakeya", confidence="high"),
        m("key_development", 2010, "Guth–Katz polynomial partitioning", "A different polynomial technique attacks the Erdős distinct-distance problem.", "L. Guth and N. H. Katz, On the Erdős distinct distances problem in the plane, arXiv:1011.4105 (2010)", ["Larry Guth"], e("Public preprint submitted in November 2010", "arXiv", "https://arxiv.org/abs/1011.4105"), phase="Polynomial partitioning", confidence="high"),
        m("consolidation", 2016, "Guth's Polynomial Methods in Combinatorics", "The AMS lecture-series volume gives a named systematic treatment of several polynomial methods.", "L. Guth, Polynomial Methods in Combinatorics, University Lecture Series 64 (2016)", ["Larry Guth"], e("AMS named lecture-series book, 2016", "AMS book record", "https://doi.org/10.1090/ulect/064"), confidence="high"),
    ]
    extra(x["people"][0], "On the size of Kakeya sets in finite fields (preprint)", 2008, "https://arxiv.org/abs/0803.2336", "Public application before the 2009 journal version")
    extra(x["people"][1], "On the Erdős distinct distances problem in the plane (with Nets Hawk Katz)", 2010, "https://arxiv.org/abs/1011.4105", "Polynomial partitioning application")
    extra(x["people"][1], "Polynomial Methods in Combinatorics", 2016, "https://doi.org/10.1090/ulect/064", "Named systematic treatment")
    x["notes"] += " The broad polynomial method predates Dvir; no defensible first public statement of the entire method has been isolated, so conceptual stays open. The 2016 book is a consolidation anchor, not an origin."
    rows.append(x)

    x = base["E52"]
    bg = "J. Bourgain and A. Gamburd, Uniform expansion bounds for Cayley graphs of SL₂(Fp), Ann. Math. 167 (2008)"
    bg_ev = e("Annals article, volume 167 (2008), pages 625–642", "Annals of Mathematics / Crossref", "https://doi.org/10.4007/annals.2008.167.625")
    x["phases"] = ["Finite-field sum-product tools", "Expansion in groups"]
    x["milestones"] = [
        m("precursor", 2003, "Finite-field sum-product preprint", "Bourgain, Katz and Tao establish a tool later used in expansion arguments.", "J. Bourgain, N. Katz and T. Tao, A sum-product estimate in finite fields and applications, arXiv:math/0301343 (2003)", ["Jean Bourgain"], e("Public preprint submitted in 2003", "arXiv", "https://arxiv.org/abs/math/0301343"), phase="Finite-field sum-product tools", confidence="high"),
        m("first_statement", 2008, "Bourgain–Gamburd expansion theorem", "The paper establishes uniform expansion bounds for Cayley graphs of SL₂(Fp).", bg, ["Jean Bourgain", "Alex Gamburd"], bg_ev, phase="Expansion in groups", confidence="high", note="The publication truly states the theorem and applies additive-combinatorial growth tools to group expansion. A possible earlier public preprint remains unverified."),
        m("first_application", 2008, "Growth tools applied to SL₂ expansion", "The proof deliberately transfers sum-product and group-growth estimates to expander graphs.", bg, ["Jean Bourgain", "Alex Gamburd"], bg_ev, phase="Expansion in groups", confidence="high", note="The same article truly plays both first-statement and purposeful-application roles."),
    ]
    extra(x["people"][0], "A sum-product estimate in finite fields and applications (with Katz and Tao)", 2003, "https://arxiv.org/abs/math/0301343", "Precursor tool for expansion")
    rows.append(x)

    assert len(rows) == 10 and len({r["eventId"] for r in rows}) == 10
    output = [{"eventId": r["eventId"], "canonicalName": r["canonicalName"], "aliases": r["aliases"],
               "phases": r.get("phases", []), "milestones": r["milestones"], "people": r["people"], "notes": r["notes"]}
              for r in rows]
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {len(output)} events and {sum(len(r['milestones']) for r in output)} milestones to {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
