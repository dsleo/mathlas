#!/usr/bin/env python3
"""Direct reconciliation of the final fixed pilot ten into sourced milestones."""

import json
from pathlib import Path

from build_pilot_milestones2 import m

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/collection/enrichment/pilot"
A = {x["pid"]: x for x in json.loads((BASE / "A3.json").read_text())}
B = {x["pid"]: x for x in json.loads((BASE / "B3.json").read_text())}
D = {x["pid"]: x for x in json.loads((BASE / "direct-research.json").read_text())["events"]}
IDS = {x["pid"]: x["eventId"] for x in json.loads((BASE / "manifest.json").read_text())["events"]}


def ev(pid, date, index=0, source="A"):
    row = {"A": A, "B": B, "D": D}[source][pid]
    item = row["dates"][date]["evidence"][index]
    return {key: item[key] for key in ("claim", "source", "url", "kind")}


spec = {
 "P006": {
  "phases": ["permutations of roots", "Galois groups", "abstract groups"],
  "milestones": [
   m("precursor",1772,"Lagrange studies permutations of roots","J.-L. Lagrange, Réflexions sur la résolution algébrique des équations (1770–72)",[],"Permutations are used to analyse solvability before groups become independent objects.",[ev("P006","conceptual",0,"D")],confidence="low",note="The memoir appeared in parts associated with 1770–72; this is a precursor, not an abstract-group publication.",phase="permutations of roots"),
   m("first_statement",1846,"Galois's group memoir appears in print","É. Galois, Mémoire sur les conditions de résolubilité des équations par radicaux, published by Liouville (1846)",["Evariste Galois"],"The public memoir gives a group criterion for solvability by radicals.",[ev("P006","conceptual")],phase="Galois groups"),
   m("first_application",1846,"Galois criterion applied to polynomial solvability","É. Galois, Mémoire sur les conditions de résolubilité des équations par radicaux, published by Liouville (1846)",["Evariste Galois"],"The printed criterion targets the solvability of polynomial equations.",[ev("P006","methodological")],note="The same memoir truly plays both first-statement and first-application roles.",phase="Galois groups"),
   m("key_development",1854,"Cayley abstracts group multiplication","A. Cayley, On the theory of groups, as depending on the symbolic equation θⁿ=1 (1854)",["Arthur Cayley"],"A group is treated as an abstract multiplication structure.",[ev("P006","institutional")],phase="abstract groups"),
   m("naming",1854,"Theory of groups appears in Cayley's title","A. Cayley, On the theory of groups, as depending on the symbolic equation θⁿ=1 (1854)",["Arthur Cayley"],"The published title supplies a named-field anchor.",[ev("P006","institutional")],note="The Cayley paper plays both abstraction and naming roles.",phase="abstract groups")],
  "note":"The 1770/72 Lagrange precursor, 1830 Galois manuscript, 1846 print and 1854 Cayley abstraction are different stages. The unpublished 1830 manuscript does not set a public date."
 },
 "P018": {
  "milestones": [
   m("precursor",1943,"Szele's tournament argument","T. Szele, Kombinatorische Untersuchungen über den gerichteten vollständigen Graphen (1943)",["Tibor Szele"],"A prior random-choice existence argument anticipates the later combinatorial method.",[ev("P018","conceptual")],confidence="low"),
   m("first_statement",1947,"Erdős's graph existence proof","P. Erdős, Some remarks on the theory of graphs, Bull. AMS 53 (1947)",["Paul Erdos"],"A published paper makes the random-construction method explicit for graph existence.",[ev("P018","conceptual",0,"D")],note="The paper both presents and uses the method."),
   m("first_application",1947,"Random graphs give Ramsey bounds","P. Erdős, Some remarks on the theory of graphs, Bull. AMS 53 (1947)",["Paul Erdos"],"A random graph argument proves a Ramsey-type existence bound.",[ev("P018","methodological")],note="The same paper truly plays both first-statement and first-application roles."),
   m("consolidation",1974,"Probabilistic Methods in Combinatorics","P. Erdős and J. Spencer, Probabilistic Methods in Combinatorics (1974)",["Paul Erdos","Joel Spencer"],"A named monograph consolidates the method.",[ev("P018","institutional")])],
  "note":"Szele 1943 is retained as a priority precursor; the 1947 Erdős paper is the checked graph-theoretic anchor. Rényi's 1969 lecture title may be an earlier naming anchor than the 1974 book and needs a record-level comparison."
 },
 "P048": {
  "phases": ["graphs", "matroids"],
  "milestones": [
   m("precursor",2010,"Huh posts a graph log-concavity preprint","J. Huh, Milnor numbers of projective hypersurfaces and the chromatic polynomial of graphs, arXiv:1008.4749 (2010)",["June Huh"],"The preprint uses geometry to establish graph chromatic-polynomial log-concavity.",[ev("P048","conceptual",1)],phase="graphs"),
   m("key_development",2012,"Huh–Katz matroid coefficients","J. Huh and E. Katz, Log-concavity of characteristic polynomials and the Bergman fan of matroids (2012)",["June Huh","Eric Katz"],"Geometric methods reach characteristic-polynomial coefficients for representable matroids.",[ev("P048","methodological",0,"D")],phase="matroids"),
   m("first_statement",2015,"Hodge theory for combinatorial geometries posted","K. Adiprasito, J. Huh and E. Katz, Hodge theory for combinatorial geometries, arXiv:1511.02888 (2015)",["Karim Adiprasito","June Huh","Eric Katz"],"The public preprint states the general matroid Hodge-theoretic construction.",[ev("P048","methodological",1)],note="The preprint both states the framework and applies it to log-concavity.",phase="matroids"),
   m("first_application",2015,"Hodge theory proves matroid log-concavity","K. Adiprasito, J. Huh and E. Katz, Hodge theory for combinatorial geometries, arXiv:1511.02888 (2015)",["Karim Adiprasito","June Huh","Eric Katz"],"The construction settles log-concavity questions for general matroids.",[ev("P048","methodological",1)],note="The same preprint truly plays both first-statement and first-application roles; journal publication followed in 2018.",phase="matroids")],
  "note":"The 2010 graph preprint, 2012 representable-matroid result, 2015 general-matroid preprint and 2018 journal issue are distinct stages or editions. The general result uses the public 2015 date, not its 2018 journal date. No clear named institution has been established."
 },
 "P447": {
  "milestones": [
   m("first_statement",1829,"Lobachevsky's geometry appears in print","N. Lobachevsky, Kazan Messenger account of non-Euclidean geometry (1829)",["Nikolai Lobachevsky"],"A published account develops geometry without Euclid's parallel postulate.",[ev("P447","conceptual")],confidence="low"),
   m("key_development",1832,"Bolyai's independent Appendix","J. Bolyai, Appendix scientiam spatii absolute veram exhibens (1832)",["Janos Bolyai"],"An independent public construction extends the non-Euclidean programme.",[{
       "claim":"Bolyai's Appendix appeared in 1832","source":"MacTutor","url":"https://mathshistory.st-andrews.ac.uk/Biographies/Bolyai/","kind":"history_page"}],confidence="low"),
   m("naming",1837,"Lobachevsky titles his work Géométrie imaginaire","N. Lobachevsky, Géométrie imaginaire, J. reine angew. Math. 17 (1837)",["Nikolai Lobachevsky"],"A published title names the alternative geometry, though not with the later non-Euclidean term.",[ev("P447","institutional")],confidence="low"),
   m("first_application",1868,"Beltrami models the alternative geometry","E. Beltrami, Saggio di interpretazione della geometria non-euclidea (1868)",["Eugenio Beltrami"],"A model addresses the consistency and interpretation of non-Euclidean geometry.",[ev("P447","methodological")])],
  "note":"Gauss's private thinking is not a public date. Lobachevsky's 1829 and Bolyai's 1832 publications are kept separately. The 1837 title uses 'imaginary geometry'; first appearance of the exact later term 'non-Euclidean' needs its own title search."
 },
 "P300": {
  "milestones": [
   m("precursor",2010,"Polymath5 publicly explores discrepancy","T. Gowers, Erdős discrepancy problem as a forthcoming Polymath project (2010)",["Timothy Gowers"],"A public research discussion develops directions that precede Tao's proof.",[ev("P300","conceptual")],confidence="low"),
   m("precursor",2014,"SAT resolves a finite discrepancy case","B. Konev and A. Lisitsa, A SAT attack on the Erdős discrepancy conjecture (2014)",["Boris Konev","Alexei Lisitsa"],"A finite computational result precedes the general theorem.",[ev("P300","institutional")]),
   m("first_statement",2015,"Tao posts the full discrepancy proof","T. Tao, The Erdős discrepancy problem, arXiv:1509.05363 (2015)",["Terence Tao"],"The public preprint states and proves the unbounded-discrepancy result.",[ev("P300","conceptual",0,"D")],note="The same preprint both states the theorem and uses multiplicative methods."),
   m("first_application",2015,"Multiplicative-function method closes the problem","T. Tao, The Erdős discrepancy problem, arXiv:1509.05363 (2015)",["Terence Tao"],"Multiplicative and Fourier-analytic tools solve the target discrepancy problem.",[ev("P300","methodological",0,"D")],note="The same preprint truly plays both first-statement and first-application roles.")],
  "note":"The 2010 blog and 2014 SAT result are precursors, not complete proofs. The 2015 public preprint precedes the 2016 journal publication. No field institution is claimed from the 2014 SAT title."
 },
 "P505": {
  "milestones": [
   m("first_statement",1982,"LLL reduction appears in print","A. K. Lenstra, H. W. Lenstra and L. Lovász, Factoring polynomials with rational coefficients (1982)",["Arjen K. Lenstra","Hendrik W. Lenstra Jr.","Laszlo Lovasz"],"The published paper introduces lattice basis reduction.",[ev("P505","conceptual")],note="The same paper introduces and applies LLL."),
   m("first_application",1982,"LLL factors rational polynomials","A. K. Lenstra, H. W. Lenstra and L. Lovász, Factoring polynomials with rational coefficients (1982)",["Arjen K. Lenstra","Hendrik W. Lenstra Jr.","Laszlo Lovasz"],"The new reduction method is used on polynomial factorization.",[ev("P505","methodological")],note="The same paper truly plays both first-statement and first-application roles."),
   m("key_development",1983,"Fixed-dimension integer programming","H. W. Lenstra, Integer programming with a fixed number of variables (1983)",["Hendrik W. Lenstra Jr."],"Lattice methods enter a further algorithmic target.",[ev("P505","methodological",1)]),
   m("naming",1986,"Lattice basis reduction in a later title","C.-P. Schnorr, A more efficient algorithm for lattice basis reduction (1986)",[],"The method's name appears in a later paper title.",[ev("P505","institutional",0,"B")],confidence="low")],
  "note":"The 1986 title is a checked later naming anchor, not asserted as the first title ever. The 1982 paper is the conceptual and methodological anchor."
 },
 "P151": {
  "milestones": [
   m("precursor",1684,"Leibniz publishes differential notation","G. W. Leibniz, Nova methodus pro maximis et minimis, Acta Eruditorum (1684)",["Gottfried Wilhelm Leibniz"],"Differential calculus and terminology precede the explicit isochrone equation.",[ev("P151","conceptual")],confidence="low"),
   m("first_statement",1690,"Bernoulli states an isochrone differential equation","J. Bernoulli, Acta Eruditorum isochrone paper (1690)",["Jacob Bernoulli"],"A published mechanics problem is expressed by a differential equation.",[ev("P151","conceptual",0,"B")],note="The same paper states and solves the target equation."),
   m("first_application",1690,"Bernoulli solves the isochrone problem","J. Bernoulli, Acta Eruditorum isochrone paper (1690)",["Jacob Bernoulli"],"The equation is purposefully used to find the curve.",[ev("P151","methodological")],note="The same paper truly plays both first-statement and first-application roles."),
   m("consolidation",1707,"Manfredi's treatise on differential equations","G. Manfredi, De constructione aequationum differentialium primi gradus (1707)",[],"A titled book-length treatment consolidates first-order equations.",[ev("P151","institutional")],confidence="low")],
  "note":"Leibniz's 1684 differential vocabulary and Bernoulli's 1690 mechanics application are distinct. The 1693 Leibniz paper remains a later application in the direct ledger; it is not the first target use here."
 },
 "P526": {
  "phases": ["totally positive Grassmannian", "ASEP", "KP solitons"],
  "milestones": [
   m("precursor",2005,"Williams counts positive Grassmann cells","L. K. Williams, Enumeration of totally positive Grassmann cells (2005)",["Lauren K. Williams"],"A combinatorial study precedes Postnikov's network framework.",[ev("P526","methodological",1)],phase="totally positive Grassmannian"),
   m("first_statement",2006,"Postnikov posts Grassmannian network theory","A. Postnikov, Total positivity, Grassmannians, and networks, arXiv:math/0609764 (2006)",["Alexander Postnikov"],"A public preprint connects total positivity, Grassmannians and networks.",[ev("P526","conceptual")],phase="totally positive Grassmannian"),
   m("first_application",2006,"ASEP tableaux linked to Grassmannian combinatorics","S. Corteel and L. K. Williams, Tableaux combinatorics for the asymmetric exclusion process, arXiv:math/0602109 (2006)",["Sylvie Corteel","Lauren K. Williams"],"A public preprint applies the combinatorial structure to an exclusion process.",[ev("P526","methodological",0,"D")],phase="ASEP"),
   m("key_development",2013,"KP solitons from the real Grassmannian","Y. Kodama and L. K. Williams, Combinatorics of KP solitons from the real Grassmannian (2013)",["Yuji Kodama","Lauren K. Williams"],"The positive Grassmannian links to another integrable-systems target.",[ev("P526","methodological",0,"B")],phase="KP solitons")],
  "note":"Williams 2005, Postnikov 2006, Corteel–Williams 2006 and Kodama–Williams 2013 concern related but distinct transfers. A general first named institution for this combined event is unverified."
 },
 "P401": {
  "milestones": [
   m("precursor",1893,"Weber develops an abstract field framework","H. Weber, Die allgemeinen Grundlagen der Galois'schen Gleichungstheorie (1893)",["Heinrich Weber"],"An earlier field abstraction precedes Steinitz's systematic theory.",[ev("P408","conceptual",0,"D")],confidence="low"),
   m("first_statement",1910,"Steinitz publishes Algebraische Theorie der Körper","E. Steinitz, Algebraische Theorie der Körper, J. reine angew. Math. 137 (1910)",["Ernst Steinitz"],"The paper gives a systematic abstract theory of fields.",[ev("P401","conceptual")],note="The same paper states and applies the abstract theory."),
   m("first_application",1910,"Steinitz proves field-structure results","E. Steinitz, Algebraische Theorie der Körper, J. reine angew. Math. 137 (1910)",["Ernst Steinitz"],"The abstract framework yields algebraic-closure and extension results.",[ev("P401","methodological")],note="The same paper truly plays both first-statement and first-application roles."),
   m("naming",1910,"Algebraic theory of fields named in title","E. Steinitz, Algebraische Theorie der Körper, J. reine angew. Math. 137 (1910)",["Ernst Steinitz"],"The paper title provides a reproducible named anchor.",[ev("P401","institutional")],note="The same paper plays both naming and first-statement roles.")],
  "note":"This narrower Steinitz event overlaps P408 but is kept separate: Weber is a precursor here, while P408 spans the wider ring-and-field programme."
 },
 "P019": {
  "milestones": [
   m("precursor",1942,"Natural isomorphisms in group theory","S. Eilenberg and S. Mac Lane, Natural isomorphisms in group theory, PNAS 28 (1942)",["Samuel Eilenberg","Saunders Mac Lane"],"Naturality appears before the full category framework.",[ev("P019","conceptual")]),
   m("first_statement",1945,"General theory of natural equivalences","S. Eilenberg and S. Mac Lane, General theory of natural equivalences, Trans. AMS 58 (1945)",["Samuel Eilenberg","Saunders Mac Lane"],"The published paper introduces categories and functors as a general theory.",[ev("P019","conceptual",1)],note="The same paper states and uses categories."),
   m("first_application",1945,"Categories organize natural equivalences","S. Eilenberg and S. Mac Lane, General theory of natural equivalences, Trans. AMS 58 (1945)",["Samuel Eilenberg","Saunders Mac Lane"],"The formalism is used to express natural equivalence across algebraic constructions.",[ev("P019","methodological",0,"D")],note="The same paper truly plays both first-statement and first-application roles."),
   m("naming",1948,"Categories in a paper title","S. Mac Lane, Groups, categories and duality, PNAS 34 (1948)",["Saunders Mac Lane"],"A published title explicitly names categories.",[ev("P019","institutional",0,"B")])],
  "note":"The 1942 natural-isomorphism paper is a conceptual precursor; the 1945 paper publicly defines categories. The 1948 title precedes later category textbooks and is the checked naming anchor here."
 }
}


def main():
    rows = []
    for pid in [x["pid"] for x in json.loads((BASE / "pilot3.json").read_text())]:
        a, item = A[pid], spec[pid]
        people = json.loads(json.dumps(a["people"][:6]))
        if pid == "P447":
            # Archive links identify later scanned editions, not the original printing.
            for person in people:
                for work in person["works"]:
                    if work["url"] == "https://archive.org/details/geometrischeunt00loba":
                        work["year"] = 1887
                        work["citation"] = "Lobachevsky, Geometrische Untersuchungen zur Theorie der Parallellinien (1887 reprint of 1840 work)"
                    elif work["url"] == "https://archive.org/details/ioannisbolyaide00blgoog":
                        work["year"] = 1902
                        work["citation"] = "Bolyai, Appendix scientiam spatii absolute veram exhibens (1902 edition of 1832 work)"
        rows.append({"pid": pid, "eventId": IDS[pid], "canonicalName": a["canonicalName"],
                     "aliases": a["aliases"], "phases": item.get("phases", []),
                     "milestones": sorted(item["milestones"], key=lambda v: v["year"] if v["year"] is not None else 9999),
                     "people": people, "notes": item["note"]})
    target = BASE / "milestones3.json"
    target.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {len(rows)} events and {sum(len(x['milestones']) for x in rows)} milestones to {target}")


if __name__ == "__main__":
    main()
