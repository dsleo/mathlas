#!/usr/bin/env python3
"""Direct source-led milestone research for the seven-event final scale batch."""

import json
from pathlib import Path

from build_pilot_milestones2 import m

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/collection/enrichment/scale"


def bib(claim, url, source="arXiv"):
    return {"claim": claim, "source": source, "url": url, "kind": "bibliographic_record"}


def person(name, role, biography, citation, year, url, why, lifespan=None):
    return {"name": name, "role": role, "lifespan": lifespan, "biographyUrl": biography,
            "works": [{"citation": citation, "year": year, "url": url, "whyItMatters": why}]}


spec = {
 "Q1": {
  "aliases": ["distributed algorithms and descriptive combinatorics", "measurable graph coloring", "Borel coloring", "LOCAL model"],
  "milestones": [
   m("precursor",2016,"Measurable Lovász local lemma","A. Bernshteyn, Measurable versions of the Lovász Local Lemma and measurable graph colorings, arXiv:1604.07349 (2016)",["Anton Bernshteyn"],"Measurable coloring tools precede the explicit distributed-algorithm transfer.",[bib("Public precursor preprint posted in 2016","https://arxiv.org/abs/1604.07349")]),
   m("first_statement",2020,"Distributed-to-descriptive transfer stated","A. Bernshteyn, Distributed Algorithms, the Lovász Local Lemma, and Descriptive Combinatorics, arXiv:2004.04905 (2020)",["Anton Bernshteyn"],"The public paper states that efficient finite-graph local algorithms can yield well-behaved Borel-graph colorings.",[bib("Public preprint posted in April 2020","https://arxiv.org/abs/2004.04905")],note="The same paper states and applies the transfer."),
   m("first_application",2020,"Randomized local algorithms yield measurable colorings","A. Bernshteyn, Distributed Algorithms, the Lovász Local Lemma, and Descriptive Combinatorics, arXiv:2004.04905 (2020)",["Anton Bernshteyn"],"The paper applies randomized LOCAL algorithms to measurable and Baire-measurable coloring problems.",[bib("The abstract explicitly states the measurable-coloring application","https://arxiv.org/abs/2004.04905")],note="The same paper truly plays both first-statement and first-application roles."),
   m("key_development",2021,"Homomorphism graphs link descriptive and distributed methods","S. Brandt et al., On Homomorphism Graphs, arXiv:2111.03683 (2021)",[],"A later paper adapts descriptive-combinatorial methods to the distributed LOCAL model.",[bib("Public preprint posted in November 2021","https://arxiv.org/abs/2111.03683")])],
  "people": [person("Anton Bernshteyn","originator","https://bahtoh-math.github.io/","Distributed Algorithms, the Lovász Local Lemma, and Descriptive Combinatorics",2020,"https://arxiv.org/abs/2004.04905","States and applies the transfer")],
  "notes":"The inherited citation 'Rozhon et al., ITCS 2022' was too vague to assign a work record. arXiv:2111.03683 is On Homomorphism Graphs, a related later development, not Bernshteyn's founding transfer. No dedicated named institution was verified."
 },
 "Q10": {
  "aliases": ["Hodge atoms", "cubic fourfold irrationality", "quantum multiplication", "mirror symmetry and birational invariants"],
  "milestones": [
   m("precursor",2023,"Iritani's quantum-cohomology blowup theorem","H. Iritani, Quantum cohomology of blowups, arXiv:2307.13555 (2023)",[],"The later Hodge-atoms paper explicitly says its blowup behavior accords with this theorem.",[bib("Public preprint posted in July 2023","https://arxiv.org/abs/2307.13555")],note="This work concerns blowups, not a cubic-fourfold irrationality proof."),
   m("first_statement",2025,"Hodge atoms and cubic-fourfold result posted","L. Katzarkov, M. Kontsevich, T. Pantev and T. Y. Yu, Birational Invariants from Hodge Structures and Quantum Multiplication, arXiv:2508.05105 (2025)",["Ludmil Katzarkov","Maxim Kontsevich","Tony Pantev","Tony Yue Yu"],"The public preprint introduces Hodge atoms and states irrationality for very general cubic fourfolds.",[bib("Version 1 was public in August 2025 and contains this claim","https://arxiv.org/abs/2508.05105")],note="The same preprint states the framework and applies it; the claim is for very general cubic fourfolds."),
   m("first_application",2025,"Hodge atoms obstruct rationality","L. Katzarkov, M. Kontsevich, T. Pantev and T. Y. Yu, Birational Invariants from Hodge Structures and Quantum Multiplication, arXiv:2508.05105 (2025)",["Ludmil Katzarkov","Maxim Kontsevich","Tony Pantev","Tony Yue Yu"],"The authors apply the new invariants to prove that a very general cubic fourfold is not rational.",[bib("Version 1 was public in August 2025","https://arxiv.org/abs/2508.05105"),{"claim":"Version 1 explicitly states and proves the very-general-cubic-fourfold result","source":"Original preprint, version 1","url":"https://arxiv.org/html/2508.05105v1","kind":"primary_text"}],note="The same preprint truly plays both first-statement and first-application roles.")],
  "people": [
   person("Ludmil Katzarkov","originator","https://scholarship.miami.edu/esploro/profile/ludmil_katzarkov","Birational Invariants from Hodge Structures and Quantum Multiplication",2025,"https://arxiv.org/abs/2508.05105","Introduces and applies Hodge atoms"),
   person("Maxim Kontsevich","originator","https://www.ihes.fr/en/professeur/maxim-kontsevich-2/","Birational Invariants from Hodge Structures and Quantum Multiplication",2025,"https://arxiv.org/abs/2508.05105","Co-develops the birational invariant"),
   person("Tony Pantev","originator","https://www2.math.upenn.edu/~tpantev/","Birational Invariants from Hodge Structures and Quantum Multiplication",2025,"https://arxiv.org/abs/2508.05105","Co-develops the birational invariant"),
   person("Tony Yue Yu","originator","https://www.pma.caltech.edu/people/tony-yue-yu","Birational Invariants from Hodge Structures and Quantum Multiplication",2025,"https://arxiv.org/abs/2508.05105","Co-develops the Hodge-atom framework")],
  "notes":"The source claims irrationality only for a very general complex cubic fourfold, not every cubic fourfold. The catalogue's 2019 conceptual date had no checked work and is not promoted. Iritani's 2023 work is a precursor to blowup behavior, not the proof itself."
 },
 "Q22": {
  "aliases": ["integral distance sets", "integer distance sets", "Erdős–Anning theorem", "determinant method"],
  "milestones": [
   m("precursor",1945,"Anning–Erdős integral distances","N. H. Anning and P. Erdős, Integral distances, Bull. AMS 51 (1945)",[],"A classical paper establishes an earlier structural restriction on infinite integral-distance sets.",[bib("Published 1945 Bulletin article","https://doi.org/10.1090/S0002-9904-1945-08407-9","AMS / Crossref")]),
   m("first_statement",2024,"Greenfeld–Iliopoulou–Peluse post structural theorem","R. Greenfeld, M. Iliopoulou and S. Peluse, On integer distance sets, arXiv:2401.10821 (2024)",["Rachel Greenfeld","Marina Iliopoulou","Sarah Peluse"],"The public preprint states that nearly all points of a planar integer-distance set lie on a line or circle.",[bib("Public preprint posted in January 2024","https://arxiv.org/abs/2401.10821")],note="The same paper states and proves the target structural result."),
   m("first_application",2024,"Determinant method applied to integer-distance structure","R. Greenfeld, M. Iliopoulou and S. Peluse, On integer distance sets, arXiv:2401.10821 (2024)",["Rachel Greenfeld","Marina Iliopoulou","Sarah Peluse"],"The authors use the determinant method to cover lifted points by curves and derive structural and diameter bounds.",[bib("Public preprint posted in January 2024","https://arxiv.org/abs/2401.10821"),{"claim":"Section 1.4 explicitly uses the determinant method to cover lifted points by algebraic curves","source":"Original paper, section 1.4","url":"https://arxiv.org/html/2401.10821","kind":"primary_text"}],note="The same paper truly plays both first-statement and first-application roles.")],
  "people": [
   person("Rachel Greenfeld","originator","https://www.math.ias.edu/~rgreenfeld/","On integer distance sets",2024,"https://arxiv.org/abs/2401.10821","Proves the structural theorem"),
   person("Marina Iliopoulou","originator","https://research.birmingham.ac.uk/en/persons/marina-iliopoulou/","On integer distance sets",2024,"https://arxiv.org/abs/2401.10821","Proves the structural theorem"),
   person("Sarah Peluse","originator","https://www.web.stanford.edu/~speluse/","On integer distance sets",2024,"https://arxiv.org/abs/2401.10821","Proves the structural theorem")],
  "notes":"The determinant-method step is stated explicitly in section 1.4 of the original paper. Anning–Erdős 1945 is a precursor, not the new structural theorem."
 },
 "Q38": {
  "phases": ["knot invariants", "Kazhdan–Lusztig polynomials"],
  "aliases": ["machine learning guided mathematics", "AI mathematical intuition", "knot signature and cusp geometry", "Kazhdan–Lusztig combinatorial invariance"],
  "milestones": [
   m("first_statement",2021,"Nature paper sets out machine-learning-guided discovery","A. Davies et al., Advancing mathematics by guiding human intuition with AI, Nature 600 (2021)",["Marc Lackenby","Geordie Williamson"],"A public article describes a workflow that uses learned patterns and attribution to guide mathematical conjectures.",[bib("Published Nature research article in December 2021","https://doi.org/10.1038/s41586-021-04086-x","Nature / Crossref")]),
   m("first_application",2021,"Knot signature–cusp relation proved","A. Davies, A. Juhász, M. Lackenby and N. Tomašev, The signature and cusp geometry of hyperbolic knots, arXiv:2111.15323 (2021)",["Marc Lackenby"],"A machine-learning-discovered relation leads to a proved knot-theoretic inequality.",[bib("Public preprint posted in November 2021","https://arxiv.org/abs/2111.15323")],phase="knot invariants"),
   m("key_development",2021,"Kazhdan–Lusztig candidate formula","C. Blundell et al., Towards combinatorial invariance for Kazhdan–Lusztig polynomials, arXiv:2111.15161 (2021)",["Geordie Williamson"],"The companion paper proposes a Bruhat-graph formula relevant to combinatorial invariance.",[bib("Public preprint posted in November 2021","https://arxiv.org/abs/2111.15161")],phase="Kazhdan–Lusztig polynomials")],
  "people": [
   person("Marc Lackenby","developer","https://www.maths.ox.ac.uk/people/marc.lackenby","The signature and cusp geometry of hyperbolic knots",2021,"https://arxiv.org/abs/2111.15323","Proves the knot application"),
   person("Geordie Williamson","developer","https://profiles.sydney.edu.au/g.williamson","Towards combinatorial invariance for Kazhdan–Lusztig polynomials",2021,"https://arxiv.org/abs/2111.15161","Develops the representation-theory application")],
  "notes":"The catalogue's 2019 date has no checked public work for this particular paired application and is not promoted. The companion preprints were posted in November 2021, just before the Nature article in December; within-year ordering matters for any claim of a single first publication."
 },
 "Q62": {
  "aliases": ["irrationality of L(2, chi minus 3)", "arithmetic holonomy", "Apéry-style irrationality", "zeta and Dirichlet L values"],
  "milestones": [
   m("precursor",1979,"Apéry's published irrationality account","R. Apéry, Irrationalité de ζ(2) et ζ(3), Astérisque 61 (1979)",[],"A prior irrationality proof supplies the historical comparison.",[bib("Published article in Astérisque 61, pages 11–13","https://numdam.org/book-part/AST_1979__61__11_0/","Numdam")],note="The 1978 lecture is not substituted for the 1979 publication year."),
   m("first_statement",2024,"Calegari–Dimitrov–Tang post L-value independence","F. Calegari, V. Dimitrov and Y. Tang, The linear independence of 1, ζ(2), and L(2,χ−3), arXiv:2408.15403 (2024)",["Frank Calegari","Vesselin Dimitrov","Yunqing Tang"],"The public preprint states the linear-independence and irrationality theorem.",[bib("Public preprint posted in August 2024","https://arxiv.org/abs/2408.15403")],note="The same work states and applies its arithmetic-holonomy method."),
   m("first_application",2024,"Arithmetic holonomy proves L-value irrationality","F. Calegari, V. Dimitrov and Y. Tang, The linear independence of 1, ζ(2), and L(2,χ−3), arXiv:2408.15403 (2024)",["Frank Calegari","Vesselin Dimitrov","Yunqing Tang"],"The authors apply arithmetic holonomy bounds to Zagier's construction to prove irrationality.",[bib("The abstract identifies the method and target value","https://arxiv.org/abs/2408.15403")],note="The same paper truly plays both first-statement and first-application roles.")],
  "people": [
   person("Frank Calegari","originator","https://math.uchicago.edu/~fcale/","The linear independence of 1, ζ(2), and L(2,χ−3)",2024,"https://arxiv.org/abs/2408.15403","Co-proves the L-value result"),
   person("Yunqing Tang","originator","https://math.berkeley.edu/people/faculty/yunqing-tang","The linear independence of 1, ζ(2), and L(2,χ−3)",2024,"https://arxiv.org/abs/2408.15403","Co-proves the L-value result"),
   person("Vesselin Dimitrov","originator","https://www.pma.caltech.edu/people/vesselin-dimitrov","The linear independence of 1, ζ(2), and L(2,χ−3)",2024,"https://arxiv.org/abs/2408.15403","Co-proves the L-value result")],
  "notes":"The inherited summary said 'analytic continuation of power series', but the checked paper's abstract instead identifies an arithmetic holonomy bound applied to Zagier's construction. The event description should be corrected during catalogue integration."
 },
 "Q68": {
  "aliases": ["AlphaTensor", "reinforcement learning for matrix multiplication", "tensor decomposition game", "matrix multiplication algorithms"],
  "milestones": [
   m("precursor",1969,"Strassen's faster matrix multiplication","V. Strassen, Gaussian elimination is not optimal, Numer. Math. 13 (1969)",[],"A classical faster algorithm is the benchmark later surpassed for particular small matrices.",[bib("Published 1969 Numerische Mathematik article","https://doi.org/10.1007/BF02165411","Springer / Crossref")]),
   m("first_statement",2022,"AlphaTensor research article","A. Fawzi et al., Discovering faster matrix multiplication algorithms with reinforcement learning, Nature 610 (2022)",["Alhussein Fawzi"],"The published paper describes a reinforcement-learning game for exact matrix-multiplication tensor decompositions.",[bib("Nature article published 5 October 2022","https://doi.org/10.1038/s41586-022-05172-4","Nature / Crossref")],note="The same article introduces and applies AlphaTensor."),
   m("first_application",2022,"AlphaTensor finds improved multiplication algorithms","A. Fawzi et al., Discovering faster matrix multiplication algorithms with reinforcement learning, Nature 610 (2022)",["Alhussein Fawzi"],"The agent finds exact decompositions, including a 4×4 mod-2 algorithm using 47 multiplications.",[bib("The article reports the 4×4 finite-field result","https://doi.org/10.1038/s41586-022-05172-4","Nature / Crossref")],note="The same paper truly plays both first-statement and first-application roles."),
   m("key_development",2022,"Kauers–Moosbauer improve a mod-2 record","M. Kauers and J. Moosbauer, The FBHHRBNRSSSHK-Algorithm for Multiplication in Z₂^{5×5} Is Still Not the End of the Story, arXiv:2210.04045 (2022)",[],"An independent search rapidly improves a finite-field multiplication record.",[bib("Public preprint posted in October 2022","https://arxiv.org/abs/2210.04045")])],
  "people": [person("Alhussein Fawzi","originator","https://www.fawzi.ai/","Discovering faster matrix multiplication algorithms with reinforcement learning",2022,"https://doi.org/10.1038/s41586-022-05172-4","Leads the published AlphaTensor method")],
  "notes":"AlphaTensor concerns discovery of exact algorithms; the result is not a general improvement to the asymptotic matrix-multiplication exponent. Fawzi's personal research page identifies his role and links the work."
 },
 "B33": {
  "aliases": ["three-dimensional Kakeya conjecture", "Kakeya sets in R3", "Wang–Zahl Kakeya theorem"],
  "milestones": [
   m("precursor",2024,"Wang–Zahl prove a partial 3D Kakeya dimension result","H. Wang and J. Zahl, The Assouad dimension of Kakeya sets in R³, arXiv:2401.12337 (2024)",["Hong Wang","Joshua Zahl"],"The precursor establishes full Assouad dimension and special Hausdorff-dimension cases.",[bib("Public preprint posted in January 2024","https://arxiv.org/abs/2401.12337")]),
   m("first_statement",2025,"Three-dimensional Kakeya theorem posted","H. Wang and J. Zahl, Volume estimates for unions of convex sets, and the Kakeya set conjecture in three dimensions, arXiv:2502.17655 (2025)",["Hong Wang","Joshua Zahl"],"The public preprint states the Hausdorff-dimension-three result.",[bib("Public preprint posted 24 February 2025","https://arxiv.org/abs/2502.17655")],note="The same preprint states and proves the target result."),
   m("first_application",2025,"Volume estimates applied to Kakeya sets","H. Wang and J. Zahl, Volume estimates for unions of convex sets, and the Kakeya set conjecture in three dimensions, arXiv:2502.17655 (2025)",["Hong Wang","Joshua Zahl"],"Multi-scale volume estimates for convex-set unions close the three-dimensional Kakeya target.",[bib("The paper title and abstract identify the volume-estimate application","https://arxiv.org/abs/2502.17655")],note="The same paper truly plays both first-statement and first-application roles."),
   m("key_development",2026,"Streamlined proof with Guth","L. Guth, H. Wang and J. Zahl, A streamlined proof of the Kakeya set conjecture in R³, arXiv:2601.14411 (2026)",["Hong Wang","Joshua Zahl"],"A later public preprint gives a streamlined proof of the theorem.",[bib("Public preprint posted in January 2026","https://arxiv.org/abs/2601.14411")])],
  "people": [
   person("Hong Wang","originator","https://www.ihes.fr/en/hong-wang-ihes/","Volume estimates for unions of convex sets, and the Kakeya set conjecture in three dimensions",2025,"https://arxiv.org/abs/2502.17655","Co-proves the three-dimensional theorem"),
   person("Joshua Zahl","originator","https://www.math.ubc.ca/user/2684","Volume estimates for unions of convex sets, and the Kakeya set conjecture in three dimensions",2025,"https://arxiv.org/abs/2502.17655","Co-proves the three-dimensional theorem")],
  "notes":"The 2024 paper proves weaker or special dimension claims; it is not the full 2025 result. The 2026 streamlined proof is a later development. No textbook or named field institution is claimed."
 }
}


def main():
    staged = json.loads((BASE / "batch52.json").read_text())
    rows = []
    for event in staged:
        item = spec[event["eventId"]]
        rows.append({"eventId": event["eventId"], "canonicalName": event["name"],
                     "aliases": item["aliases"], "phases": item.get("phases", []),
                     "milestones": sorted(item["milestones"], key=lambda v: v["year"]),
                     "people": item["people"], "notes": item["notes"]})
    target = BASE / "milestones52.json"
    target.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {len(rows)} events and {sum(len(e['milestones']) for e in rows)} milestones to {target}")


if __name__ == "__main__":
    main()
