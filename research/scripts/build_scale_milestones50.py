#!/usr/bin/env python3
"""Direct source-led milestones for the ten-event 2011–2020 scale batch."""

import json
from pathlib import Path

from build_pilot_milestones2 import m

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/collection/enrichment/scale"


def b(claim, url, source="arXiv"):
    return {"claim": claim, "source": source, "url": url, "kind": "bibliographic_record"}


def p(name, role, profile, title, year, url, why):
    return {"name": name, "role": role, "lifespan": None, "biographyUrl": profile,
            "works": [{"citation": title, "year": year, "url": url, "whyItMatters": why}]}


spec = {
 "E57/WC52/QC63": {
  "aliases": ["regularity structures", "singular stochastic PDEs", "Phi-four three", "KPZ equation"],
  "milestones": [
   m("precursor", 2011, "Pathwise KPZ solution", "M. Hairer, Solving the KPZ equation, arXiv:1109.6811 (2011)", ["Martin Hairer"], "A pathwise solution theory for KPZ precedes the general regularity-structure framework.", [b("First public preprint posted September 2011", "https://arxiv.org/abs/1109.6811")]),
   m("first_statement", 2013, "Regularity structures introduced", "M. Hairer, A theory of regularity structures, arXiv:1303.5113 (2013)", ["Martin Hairer"], "The preprint defines models and a calculus for singular stochastic PDEs.", [b("First public preprint posted March 2013", "https://arxiv.org/abs/1303.5113")], note="The same paper states and applies the framework."),
   m("first_application", 2013, "Phi-four three dynamics constructed", "M. Hairer, A theory of regularity structures, arXiv:1303.5113 (2013)", ["Martin Hairer"], "The paper uses regularity structures to construct the stochastic quantization process for the three-dimensional Phi-four model.", [b("The abstract explicitly names the Phi-four-three application", "https://arxiv.org/abs/1303.5113")], note="The same work truly plays both first-statement and first-application roles."),
   m("consolidation", 2020, "Rough-path course incorporates regularity structures", "P. K. Friz and M. Hairer, A Course on Rough Paths, second edition, Springer (2020)", ["Martin Hairer"], "A systematic second-edition text includes an introduction to regularity structures.", [b("Publisher records the 2020 second edition", "https://doi.org/10.1007/978-3-030-41556-3", "Springer / Crossref")])],
  "people": [p("Martin Hairer", "originator", "https://www.epfl.ch/labs/propde/prof-martin-hairer/", "A theory of regularity structures", 2013, "https://arxiv.org/abs/1303.5113", "Defines the framework and constructs its first major SPDE application")],
  "notes": "The 2011 KPZ work is a precursor, not a 2011 publication of the general regularity-structures theory. The Inventiones 2014 journal date follows the public 2013 preprint."
 },
 "B16/QC26/WC25": {
  "aliases": ["perfectoid spaces", "tilting equivalence", "almost purity", "p-adic Hodge theory"],
  "milestones": [
   m("first_statement", 2011, "Perfectoid spaces and tilting introduced", "P. Scholze, Perfectoid spaces, arXiv:1111.4914 (2011)", ["Peter Scholze"], "The preprint defines perfectoid rings and spaces and their characteristic-changing tilting operation.", [b("First public preprint posted November 2011", "https://arxiv.org/abs/1111.4914")], note="The same work defines and applies the theory."),
   m("first_application", 2011, "Tilting applied to weight-monodromy cases", "P. Scholze, Perfectoid spaces, arXiv:1111.4914 (2011)", ["Peter Scholze"], "The paper deduces cases of the weight-monodromy conjecture by reduction to equal characteristic.", [b("The abstract states the target application", "https://arxiv.org/abs/1111.4914")], note="The same work truly plays both first-statement and first-application roles."),
   m("key_development", 2012, "Perfectoid spaces used in rigid-analytic p-adic Hodge theory", "P. Scholze, p-adic Hodge theory for rigid-analytic varieties, arXiv:1205.3463 (2012)", ["Peter Scholze"], "A comparison theorem for rigid-analytic varieties explicitly relies on perfectoid spaces.", [b("First public preprint posted May 2012", "https://arxiv.org/abs/1205.3463")]),
   m("consolidation", 2013, "Perfectoid-space survey", "P. Scholze, Perfectoid Spaces: A survey, arXiv:1303.5948 (2013)", ["Peter Scholze"], "The survey organizes the new theory, applications and open problems.", [b("Public survey preprint posted March 2013", "https://arxiv.org/abs/1303.5948")])],
  "people": [p("Peter Scholze", "originator", "https://www.uni-bonn.de/de/forschung-lehre/forschungsprofil/transdisziplinaere-forschungsbereiche/modelling/mitgliederverzeichnis/peter-scholze", "Perfectoid spaces", 2011, "https://arxiv.org/abs/1111.4914", "Introduces tilting and applies it to weight-monodromy")],
  "notes": "The public arXiv posting is 2011, preceding the 2012 journal issue. The catalogue's 2020 institutional date has no checked field-naming institution and is not promoted."
 },
 "Q45": {
  "aliases": ["MIP*=RE", "entangled provers", "Connes embedding problem", "quantum multiprover interactive proofs"],
  "milestones": [
   m("precursor", 2012, "Entangled-prover NEXP lower bound", "T. Ito and T. Vidick, A multi-prover interactive proof for NEXP sound against entangled provers, arXiv:1207.0550 (2012)", [], "A lower bound for MIP* predates the equality with recursively enumerable languages.", [b("Public preprint posted July 2012", "https://arxiv.org/abs/1207.0550")]),
   m("key_development", 2019, "NEEXP lower bound for MIP*", "A. Natarajan and J. Wright, NEEXP in MIP*, arXiv:1904.05870 (2019)", [], "The stronger lower bound is part of the proof trajectory toward MIP*=RE.", [b("Public preprint posted April 2019", "https://arxiv.org/abs/1904.05870")]),
   m("first_statement", 2020, "MIP*=RE theorem posted", "Z. Ji, A. Natarajan, T. Vidick, J. Wright and H. Yuen, MIP*=RE, arXiv:2001.04383 (2020)", ["Zhengfeng Ji", "Anand Natarajan", "Thomas Vidick", "John Wright", "Henry Yuen"], "The preprint states the equality of entangled multiprover proofs and recursively enumerable languages.", [b("First public preprint posted January 2020", "https://arxiv.org/abs/2001.04383")], note="The same paper proves the theorem and its consequences."),
   m("first_application", 2020, "Halting problem reduced to nonlocal-game value", "Z. Ji et al., MIP*=RE, arXiv:2001.04383 (2020)", ["Zhengfeng Ji", "Anand Natarajan", "Thomas Vidick", "John Wright", "Henry Yuen"], "The theorem yields undecidability of entangled game value and a negative answer to Connes embedding.", [b("The abstract explicitly states both consequences", "https://arxiv.org/abs/2001.04383")], note="The same work truly plays both first-statement and first-application roles.")],
  "people": [p("Thomas Vidick", "developer", "https://iqim.caltech.edu/profile/thomas-vidick/", "MIP*=RE", 2020, "https://arxiv.org/abs/2001.04383", "Co-proves the theorem linking quantum games and computability")],
  "notes": "The inherited conceptual range 2011–13 describes antecedents, not the 2020 theorem. These precursors are separate milestones. This event overlaps Q46's quantum-game history but has a different target theorem."
 },
 "Q63": {
  "aliases": ["arc spaces and Rogers-Ramanujan identities", "Hilbert-Poincare series of arc spaces", "partitions from singularities"],
  "milestones": [
   m("first_statement", 2011, "Arc-space/partition correspondence posted", "C. Bruschek, H. Mourtada and J. Schepers, Arc Spaces and Rogers-Ramanujan Identities, arXiv:1101.4950 (2011)", ["Clemens Bruschek", "Hussein Mourtada", "Jan Schepers"], "The paper links Hilbert-Poincare series of arc spaces to partition generating functions.", [b("Public preprint posted January 2011", "https://arxiv.org/abs/1101.4950")], note="The same work states and applies the connection."),
   m("first_application", 2011, "Double-point arc space yields Rogers-Ramanujan identity", "C. Bruschek, H. Mourtada and J. Schepers, Arc Spaces and Rogers-Ramanujan Identities, DMTCS Proceedings AO (2011)", ["Clemens Bruschek", "Hussein Mourtada", "Jan Schepers"], "The 2011 proceeding applies the arc-space series of a double point to integer partitions without equal or consecutive parts.", [b("Published 2011 proceeding and abstract identify the double-point application", "https://doi.org/10.46298/dmtcs.2904", "DMTCS / Crossref")], note="This is a published version of the founding preprint and documents the same first application."),
   m("key_development", 2020, "Differential-ideal Groebner bases extend the partition connection", "P. Afsharijoo and H. Mourtada, Partition identities and application to infinite dimensional Groebner basis and viceversa, arXiv:2006.09147 (2020)", ["Hussein Mourtada"], "A later paper relates differential-ideal Groebner bases to Rogers-Ramanujan-type partition identities.", [b("Public preprint posted June 2020", "https://arxiv.org/abs/2006.09147")])],
  "people": [p("Hussein Mourtada", "originator", "https://webusers.imj-prg.fr/~hussein.mourtada/english.html", "Arc Spaces and Rogers-Ramanujan Identities", 2011, "https://doi.org/10.46298/dmtcs.2904", "Co-links arc spaces of singularities and partition identities")],
  "notes": "The inherited Craig–van Ittersum–Ono 2024 citation concerns partitions detecting primes, not this arc-space construction; it is not included as a development. The 2011 preprint and proceeding are the same project, not independent priority claims."
 },
 "B35": {
  "aliases": ["virtual fundamental cycles", "implicit atlases", "pseudo-holomorphic curve moduli", "algebraic VFC package"],
  "milestones": [
   m("precursor", 1996, "Intrinsic normal cone and virtual class", "K. Behrend and B. Fantechi, The intrinsic normal cone, arXiv:alg-geom/9601010 (1996)", [], "An earlier algebraic construction of virtual classes provides a distinct foundation.", [b("First public preprint posted January 1996", "https://arxiv.org/abs/alg-geom/9601010")]),
   m("first_statement", 2013, "Pardon introduces implicit-atlas VFC package", "J. Pardon, An algebraic approach to virtual fundamental cycles on moduli spaces of pseudo-holomorphic curves, arXiv:1309.2370 (2013)", ["John Pardon"], "The preprint presents an algebraic, sheaf-theoretic virtual-cycle construction using implicit atlases.", [b("First public preprint posted September 2013", "https://arxiv.org/abs/1309.2370")], note="The same paper states and applies this particular construction."),
   m("first_application", 2013, "Implicit-atlas package applied to symplectic invariants", "J. Pardon, An algebraic approach to virtual fundamental cycles on moduli spaces of pseudo-holomorphic curves, arXiv:1309.2370 (2013)", ["John Pardon"], "The paper gives definitions of Gromov–Witten invariants and Hamiltonian Floer homology and an S1-localization calculation.", [b("The abstract explicitly names these applications", "https://arxiv.org/abs/1309.2370")], note="The same work truly plays both first-statement and first-application roles.")],
  "people": [p("John Pardon", "originator", "https://scgp.stonybrook.edu/people/faculty/bios/john-pardon", "An algebraic approach to virtual fundamental cycles on moduli spaces of pseudo-holomorphic curves", 2013, "https://arxiv.org/abs/1309.2370", "Develops and applies implicit atlases")],
  "notes": "The inherited 2012 date is earlier than the checked 2013 public preprint and is not used. The event name's 'homotopical algebra' is broader than the paper's own description, which emphasizes algebraic/sheaf-theoretic implicit atlases."
 },
 "WC54": {
  "aliases": ["paracontrolled distributions", "singular SPDEs", "controlled rough paths", "paradifferential calculus"],
  "milestones": [
   m("precursor", 2003, "Controlled rough paths", "M. Gubinelli, Controlling Rough Paths, arXiv:math/0306433 (2003)", ["Massimiliano Gubinelli"], "Controlled rough paths supply one of the ingredients later adapted to singular PDEs.", [b("Public preprint posted June 2003", "https://arxiv.org/abs/math/0306433")]),
   m("first_statement", 2012, "Paracontrolled distributions introduced", "M. Gubinelli, P. Imkeller and N. Perkowski, Paracontrolled distributions and singular PDEs, arXiv:1210.2684 (2012)", ["Massimiliano Gubinelli", "Peter Imkeller", "Nicolas Perkowski"], "The paper combines paradifferential calculus with controlled rough paths for singular PDEs.", [b("First public preprint posted October 2012", "https://arxiv.org/abs/1210.2684")], note="The same paper introduces and applies the approach."),
   m("first_application", 2012, "Paracontrolled method applied to model SPDEs", "M. Gubinelli, P. Imkeller and N. Perkowski, Paracontrolled distributions and singular PDEs, arXiv:1210.2684 (2012)", ["Massimiliano Gubinelli", "Peter Imkeller", "Nicolas Perkowski"], "The authors treat fractional-Brownian, Burgers-type and parabolic-Anderson model problems.", [b("The abstract explicitly lists the model problems", "https://arxiv.org/abs/1210.2684")], note="The same work truly plays both first-statement and first-application roles.")],
  "people": [p("Massimiliano Gubinelli", "originator", "https://www.maths.ox.ac.uk/people/massimiliano.gubinelli", "Paracontrolled distributions and singular PDEs", 2012, "https://arxiv.org/abs/1210.2684", "Co-introduces and applies the method")],
  "notes": "The Forum of Mathematics, Pi publication is 2015; the same work was publicly available in 2012."
 },
 "WC62/QC20": {
  "phases": ["Ramanujan graphs", "interlacing families"],
  "aliases": ["Ramanujan graphs of every degree", "interlacing polynomials", "2-lifts", "spectral expanders"],
  "milestones": [
   m("precursor", 1988, "Classical Ramanujan graph constructions", "A. Lubotzky, R. Phillips and P. Sarnak, Ramanujan graphs, Combinatorica 8 (1988)", [], "Explicit constructions cover special degrees before the all-degree interlacing result.", [b("Publisher record dates the classical paper to 1988", "https://doi.org/10.1007/BF02126799", "Springer / Crossref")], phase="Ramanujan graphs"),
   m("first_statement", 2013, "Interlacing families for all-degree Ramanujan graphs", "A. Marcus, D. A. Spielman and N. Srivastava, Interlacing Families I: Bipartite Ramanujan Graphs of All Degrees, arXiv:1304.4132 (2013)", ["Adam Marcus", "Daniel A. Spielman", "Nikhil Srivastava"], "The public preprint introduces interlacing-polynomial existence arguments and states all-degree bipartite Ramanujan graph families.", [b("First public preprint posted April 2013", "https://arxiv.org/abs/1304.4132")], note="The same paper introduces and applies this interlacing method.", phase="interlacing families"),
   m("first_application", 2013, "Interlacing applied to graph 2-lifts", "A. Marcus, D. A. Spielman and N. Srivastava, Interlacing Families I: Bipartite Ramanujan Graphs of All Degrees, arXiv:1304.4132 (2013)", ["Adam Marcus", "Daniel A. Spielman", "Nikhil Srivastava"], "The method proves existence of good 2-lifts and infinite bipartite Ramanujan families in every degree above two.", [b("The abstract states the 2-lift target", "https://arxiv.org/abs/1304.4132")], note="The same work truly plays both first-statement and first-application roles.", phase="interlacing families")],
  "people": [p("Daniel A. Spielman", "developer", "https://cs.yale.edu/homes/spielman/", "Interlacing Families I: Bipartite Ramanujan Graphs of All Degrees", 2013, "https://arxiv.org/abs/1304.4132", "Co-develops interlacing families for all-degree expanders")],
  "notes": "This catalogue event bundles the 1988 graph notion and 2013 interlacing method. The 1988 paper is retained as a phase precursor, so derived dates describe the new transfer rather than the birth of Ramanujan graphs."
 },
 "QC12": {
  "aliases": ["Kadison-Singer problem", "mixed characteristic polynomials", "paving conjecture", "interlacing families II"],
  "milestones": [
   m("precursor", 1959, "Kadison–Singer problem posed", "R. V. Kadison and I. M. Singer, Extensions of Pure States, American Journal of Mathematics 81 (1959)", [], "The original operator-algebra problem predates its interlacing-polynomial solution.", [b("Publisher record dates the original article to 1959", "https://doi.org/10.2307/2372748", "JSTOR / Crossref")]),
   m("precursor", 2013, "Interlacing families I establishes method", "A. Marcus, D. A. Spielman and N. Srivastava, Interlacing Families I, arXiv:1304.4132 (2013)", ["Adam Marcus", "Daniel A. Spielman", "Nikhil Srivastava"], "An April preprint develops the interlacing method for Ramanujan graphs before the Kadison–Singer transfer.", [b("First public preprint posted April 2013", "https://arxiv.org/abs/1304.4132")]),
   m("first_statement", 2013, "Kadison–Singer solution posted", "A. Marcus, D. A. Spielman and N. Srivastava, Interlacing Families II: Mixed Characteristic Polynomials and the Kadison-Singer Problem, arXiv:1306.3969 (2013)", ["Adam Marcus", "Daniel A. Spielman", "Nikhil Srivastava"], "The public preprint states a positive solution through interlacing and mixed characteristic polynomials.", [b("First public preprint posted June 2013", "https://arxiv.org/abs/1306.3969")], note="The same paper states and applies the method."),
   m("first_application", 2013, "Mixed characteristic polynomials prove paving bounds", "A. Marcus, D. A. Spielman and N. Srivastava, Interlacing Families II: Mixed Characteristic Polynomials and the Kadison-Singer Problem, arXiv:1306.3969 (2013)", ["Adam Marcus", "Daniel A. Spielman", "Nikhil Srivastava"], "The method proves Weaver's KS2 and explicit paving consequences implying Kadison–Singer.", [b("The abstract identifies these target conjectures", "https://arxiv.org/abs/1306.3969")], note="The same work truly plays both first-statement and first-application roles.")],
  "people": [p("Daniel A. Spielman", "developer", "https://cs.yale.edu/homes/spielman/", "Interlacing Families II: Mixed Characteristic Polynomials and the Kadison-Singer Problem", 2013, "https://arxiv.org/abs/1306.3969", "Co-applies interlacing to Kadison–Singer")],
  "notes": "The original 1959 question and the 2013 interlacing proof are different stages. The 2015 Annals publication follows the public June 2013 preprint."
 },
 "Q25": {
  "aliases": ["Liouville quantum gravity", "Brownian map equivalence", "quantum Loewner evolution", "QLE metric"],
  "milestones": [
   m("precursor", 1999, "Schramm's LERW/UST scaling-limit work posted", "O. Schramm, Scaling limits of loop-erased random walks and uniform spanning trees, arXiv:math/9904022 (1999)", [], "SLE-related scaling-limit methods precede the later random-surface metric construction.", [b("Public preprint posted April 1999", "https://arxiv.org/abs/math/9904022")]),
   m("first_statement", 2015, "QLE metric on Liouville quantum gravity proposed", "J. Miller and S. Sheffield, Liouville quantum gravity and the Brownian map I: The QLE(8/3,0) metric, arXiv:1507.00719 (2015)", ["Jason Miller", "Scott Sheffield"], "The first series paper constructs a metric on a dense subset of the Liouville quantum gravity sphere.", [b("First public preprint posted July 2015", "https://arxiv.org/abs/1507.00719")]),
   m("first_application", 2016, "LQG metric identified with the Brownian map", "J. Miller and S. Sheffield, Liouville quantum gravity and the Brownian map II: geodesics and continuity of the embedding, arXiv:1605.03563 (2016)", ["Jason Miller", "Scott Sheffield"], "The QLE metric is extended continuously to the sphere and its metric-measure law is identified with the Brownian map.", [b("First public preprint posted May 2016; abstract states the identification", "https://arxiv.org/abs/1605.03563")])],
  "people": [p("Scott Sheffield", "developer", "https://math.mit.edu/~sheffield/", "Liouville quantum gravity and the Brownian map II: geodesics and continuity of the embedding", 2016, "https://arxiv.org/abs/1605.03563", "Co-proves the LQG/Brownian-map metric identification")],
  "notes": "The 2015 part I paper does not yet establish the full law equivalence; part II does so in 2016. This record concerns that specific metric bridge, not the first definition of LQG or SLE."
 },
 "QC24": {
  "phases": ["Bourgain–Guth restriction method", "decoupling and Vinogradov"],
  "aliases": ["l2 decoupling", "Bourgain-Demeter decoupling", "Vinogradov mean value theorem", "multilinear restriction"],
  "milestones": [
   m("precursor", 2010, "Bourgain–Guth multilinear restriction argument", "J. Bourgain and L. Guth, Bounds on oscillatory integral operators based on multilinear estimates, arXiv:1012.3760 (2010)", ["Jean Bourgain", "Larry Guth"], "Multilinear estimates improve restriction bounds and connect to curved Kakeya problems.", [b("Public preprint posted December 2010", "https://arxiv.org/abs/1012.3760")], phase="Bourgain–Guth restriction method"),
   m("first_statement", 2014, "Sharp l2 decoupling proved", "J. Bourgain and C. Demeter, The proof of the l2 Decoupling Conjecture, arXiv:1403.5335 (2014)", ["Jean Bourgain", "Ciprian Demeter"], "The public paper proves the decoupling conjecture for positive-curvature hypersurfaces and cones.", [b("First public preprint posted March 2014", "https://arxiv.org/abs/1403.5335")], phase="decoupling and Vinogradov"),
   m("first_application", 2015, "Decoupling proves Vinogradov mean-value conjecture", "J. Bourgain, C. Demeter and L. Guth, Proof of the main conjecture in Vinogradov's mean value theorem for degrees higher than three, arXiv:1512.01565 (2015)", ["Jean Bourgain", "Ciprian Demeter", "Larry Guth"], "A sharp decoupling inequality for curves yields the main conjecture in Vinogradov's mean-value theorem for degrees above three.", [b("First public preprint posted December 2015; abstract identifies the method", "https://arxiv.org/abs/1512.01565")], phase="decoupling and Vinogradov"),
   m("consolidation", 2016, "Decoupling study guide", "J. Bourgain and C. Demeter, A study guide for the l2 Decoupling Theorem, arXiv:1604.06032 (2016)", ["Jean Bourgain", "Ciprian Demeter"], "A self-contained proof organizes the decoupling theorem for readers.", [b("Public guide posted April 2016", "https://arxiv.org/abs/1604.06032")], phase="decoupling and Vinogradov")],
  "people": [p("Ciprian Demeter", "developer", "https://math.indiana.edu/about/faculty/demeter-ciprian.html", "The proof of the l2 Decoupling Conjecture", 2014, "https://arxiv.org/abs/1403.5335", "Co-proves sharp decoupling, later applied to Vinogradov")],
  "notes": "The event bundles the 2010 Bourgain–Guth restriction method, 2014 Bourgain–Demeter decoupling, and 2015 Vinogradov application. The 2016 Annals date is later than the public 2015 preprint."
 }
}


def main():
    staged = json.loads((BASE / "batch50.json").read_text())
    rows = []
    for source in staged:
        item = spec[source["eventId"]]
        rows.append({"pid": source["pid"], "eventId": source["eventId"], "canonicalName": source["name"],
                     "aliases": item["aliases"], "phases": item.get("phases", []),
                     "milestones": sorted(item["milestones"], key=lambda entry: entry["year"]),
                     "people": item["people"], "notes": item["notes"]})
    target = BASE / "milestones50.json"
    target.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {len(rows)} events and {sum(len(row['milestones']) for row in rows)} milestones")


if __name__ == "__main__":
    main()
