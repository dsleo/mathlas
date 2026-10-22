#!/usr/bin/env python3
"""Direct source-led reconciliation of the ten contemporary batch-51 events."""

import json
from pathlib import Path

from build_pilot_milestones2 import m

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/collection/enrichment/scale"


def bib(claim, url, source="arXiv"):
    return {"claim": claim, "source": source, "url": url, "kind": "bibliographic_record"}


def history(claim, url, source):
    return {"claim": claim, "source": source, "url": url, "kind": "history_page"}


def person(name, role, profile, citation, year, url, relevance):
    return {"name": name, "role": role, "lifespan": None, "biographyUrl": profile,
            "works": [{"citation": citation, "year": year, "url": url, "whyItMatters": relevance}]}


spec = {
 "Q33": {
  "phases": ["higher-form symmetries", "non-invertible symmetries"],
  "aliases": ["generalized global symmetries", "higher-form symmetry", "categorical symmetry", "non-invertible symmetry"],
  "milestones": [
   m("first_statement", 2014, "Higher-form symmetries defined", "D. Gaiotto et al., Generalized Global Symmetries, arXiv:1412.5148 (2014)", ["Davide Gaiotto", "Anton Kapustin", "Nathan Seiberg", "Brian Willett"], "The paper defines q-form global symmetries using extended charged operators.", [bib("First public version posted in December 2014", "https://arxiv.org/abs/1412.5148")], phase="higher-form symmetries"),
   m("key_development", 2021, "Non-invertible topological operators extend the framework", "B. Heidenreich et al., Non-Invertible Global Symmetries and Completeness of the Spectrum, arXiv:2104.07036 (2021)", [], "Non-invertible operators are used to connect charge completeness and absence of global symmetries.", [bib("First public version posted in April 2021; abstract states the extension", "https://arxiv.org/abs/2104.07036")], phase="non-invertible symmetries"),
   m("first_application", 2022, "Non-invertible symmetries applied to QED and QCD", "Y. Choi, H. T. Lam and S.-H. Shao, Non-invertible Global Symmetries in the Standard Model, arXiv:2205.05086 (2022)", ["Yichul Choi", "Ho Tat Lam", "Shu-Heng Shao"], "The paper applies non-invertible operators to QED and QCD selection rules and reframes the neutral-pion decay coupling.", [bib("First public version posted in May 2022; abstract specifies QED, QCD and pion coupling", "https://arxiv.org/abs/2205.05086")], phase="non-invertible symmetries")],
  "people": [person("Davide Gaiotto", "originator", "https://perimeterinstitute.ca/people/davide-gaiotto", "Generalized Global Symmetries", 2014, "https://arxiv.org/abs/1412.5148", "Co-introduces q-form symmetries")],
  "notes": "The event spans distinct higher-form and non-invertible phases. The 2022 paper is a documented physical application, not a proven first application of all generalized symmetries. No named field institution was verified."
 },
 "Q4": {
  "aliases": ["fractal uncertainty principle", "FUP", "spectral gaps without pressure", "quantum chaos"],
  "milestones": [
   m("first_statement", 2015, "Fractal uncertainty principle named in spectral-gap work", "S. Dyatlov and J. Zahl, Spectral gaps, additive energy, and a fractal uncertainty principle, arXiv:1504.06589 (2015)", ["Semyon Dyatlov", "Joshua Zahl"], "The public paper introduces a fractal uncertainty principle in its spectral-gap argument.", [bib("First public version posted in April 2015", "https://arxiv.org/abs/1504.06589")], note="The same paper states and applies the principle."),
   m("first_application", 2015, "Fractal uncertainty used for hyperbolic spectral gaps", "S. Dyatlov and J. Zahl, Spectral gaps, additive energy, and a fractal uncertainty principle, arXiv:1504.06589 (2015)", ["Semyon Dyatlov", "Joshua Zahl"], "The method yields an essential spectral gap for convex co-compact hyperbolic manifolds under the paper's dimension conditions.", [bib("Abstract explicitly identifies the spectral-gap application", "https://arxiv.org/abs/1504.06589")], note="The same paper truly plays both first-statement and first-application roles."),
   m("key_development", 2016, "Spectral gaps without the pressure condition", "J. Bourgain and S. Dyatlov, Spectral gaps without the pressure condition, arXiv:1612.09040 (2016)", ["Jean Bourgain", "Semyon Dyatlov"], "A stronger fractal uncertainty result gives gaps for all convex co-compact hyperbolic surfaces.", [bib("First public version posted in December 2016; abstract names fractal uncertainty as the new ingredient", "https://arxiv.org/abs/1612.09040")]),
   m("consolidation", 2019, "Survey of fractal uncertainty and quantum chaos", "S. Dyatlov, An introduction to fractal uncertainty principle, arXiv:1903.02599 (2019)", ["Semyon Dyatlov"], "The survey systematically presents the principle and its quantum-chaos applications.", [bib("Public survey preprint posted in March 2019", "https://arxiv.org/abs/1903.02599")])],
  "people": [person("Semyon Dyatlov", "originator", "https://math.mit.edu/directory/profile.html?pid=1581", "Spectral gaps, additive energy, and a fractal uncertainty principle", 2015, "https://arxiv.org/abs/1504.06589", "Co-introduces and applies the principle")],
  "notes": "The 2015 Dyatlov–Zahl paper is earlier than the inherited 2016 Bourgain–Dyatlov citation. The later paper proves a broader surface result."
 },
 "QC22/WC67": {
  "aliases": ["cap set problem", "cap sets in F3n", "slice rank", "polynomial method for cap sets"],
  "milestones": [
   m("precursor", 2016, "Croot–Lev–Pach polynomial method", "E. Croot, V. Lev and P. Pach, Progression-free sets in Z_4^n are exponentially small, arXiv:1605.01506 (2016)", [], "The precursor applies a polynomial argument to progression-free sets in a different group.", [bib("First public version posted 5 May 2016", "https://arxiv.org/abs/1605.01506")]),
   m("first_statement", 2016, "Exponential cap-set bound posted", "J. S. Ellenberg and D. Gijswijt, On large subsets of F_q^n with no three-term arithmetic progression, arXiv:1605.09223 (2016)", ["Jordan S. Ellenberg", "Dion Gijswijt"], "The note states an exponential bound, including the F3 cap-set problem.", [bib("First public version posted 30 May 2016", "https://arxiv.org/abs/1605.09223")], note="The same note states and applies the transferred method."),
   m("first_application", 2016, "Polynomial method applied to cap sets", "J. S. Ellenberg and D. Gijswijt, On large subsets of F_q^n with no three-term arithmetic progression, arXiv:1605.09223 (2016)", ["Jordan S. Ellenberg", "Dion Gijswijt"], "The authors explicitly use the Croot–Lev–Pach method to bound cap sets.", [bib("The abstract names the method and target problem", "https://arxiv.org/abs/1605.09223")], note="The same work truly plays both first-statement and first-application roles.")],
  "people": [person("Jordan S. Ellenberg", "developer", "https://people.math.wisc.edu/~ellenber/", "On large subsets of F_q^n with no three-term arithmetic progression", 2016, "https://arxiv.org/abs/1605.09223", "Co-applies the polynomial method to cap sets")],
  "notes": "The Croot–Lev–Pach paper is a method precursor for a different ambient group; the cap-set result is the later Ellenberg–Gijswijt note. No independent field institution is asserted."
 },
 "WC28/QC70": {
  "aliases": ["prisms", "prismatic site", "integral p-adic Hodge theory", "A-infinity cohomology"],
  "milestones": [
   m("precursor", 2015, "Integral p-adic Hodge theory announced", "B. Bhatt, M. Morrow and P. Scholze, Integral p-adic Hodge theory—announcement, arXiv:1507.08129 (2015)", [], "The announcement sketches an interpolating cohomology theory before prisms were defined.", [bib("Public announcement posted July 2015", "https://arxiv.org/abs/1507.08129")]),
   m("first_statement", 2019, "Prisms and prismatic site introduced", "B. Bhatt and P. Scholze, Prisms and Prismatic Cohomology, arXiv:1905.08229 (2019)", ["Bhargav Bhatt", "Peter Scholze"], "The preprint defines prisms and attaches the prismatic site to p-adic formal schemes.", [bib("First public version posted May 2019", "https://arxiv.org/abs/1905.08229")], note="The same paper defines the theory and proves applications."),
   m("first_application", 2019, "Prismatic cohomology proves comparison results", "B. Bhatt and P. Scholze, Prisms and Prismatic Cohomology, arXiv:1905.08229 (2019)", ["Bhargav Bhatt", "Peter Scholze"], "The paper applies the theory to almost purity, q-de Rham cohomology and p-adic Tate-twist vanishing.", [bib("The abstract lists these applications", "https://arxiv.org/abs/1905.08229")], note="The same work truly plays both first-statement and first-application roles.")],
  "people": [person("Bhargav Bhatt", "originator", "https://websites.umich.edu/~bhattb/", "Prisms and Prismatic Cohomology", 2019, "https://arxiv.org/abs/1905.08229", "Co-introduces and applies prismatic cohomology")],
  "notes": "The 2015 announcement and 2016 full integral-Hodge paper are precursors, not the first use of 'prismatic'. The Annals 2022 issue publishes the already public 2019 work; it is not counted as a separate conceptual milestone."
 },
 "Q46": {
  "aliases": ["linear system games", "Tsirelson problem", "quantum correlations not closed", "nonlocal game undecidability"],
  "milestones": [
   m("first_statement", 2016, "Solution-group embedding and game undecidability", "W. Slofstra, Tsirelson's problem and an embedding theorem for groups arising from non-local games, arXiv:1606.03140 (2016)", ["William Slofstra"], "The paper embeds finitely presented groups into solution groups and states undecidability for perfect commuting-operator strategies.", [bib("First public version posted June 2016", "https://arxiv.org/abs/1606.03140")], note="The same paper develops and applies the embedding theorem."),
   m("first_application", 2016, "Group embedding applied to nonlocal games", "W. Slofstra, Tsirelson's problem and an embedding theorem for groups arising from non-local games, arXiv:1606.03140 (2016)", ["William Slofstra"], "The solution-group construction gives nonlocal games separating commuting and tensor-product strategies.", [bib("The abstract states this application", "https://arxiv.org/abs/1606.03140")], note="The same work truly plays both first-statement and first-application roles."),
   m("key_development", 2017, "Quantum correlation set shown non-closed", "W. Slofstra, The set of quantum correlations is not closed, arXiv:1703.08618 (2017)", ["William Slofstra"], "A linear-system game separates a limit of finite-dimensional strategies from any finite-dimensional perfect strategy.", [bib("First public version posted March 2017", "https://arxiv.org/abs/1703.08618")]),
   m("key_development", 2020, "MIP*=RE gives stronger undecidability", "Z. Ji et al., MIP*=RE, arXiv:2001.04383 (2020)", [], "The result reduces the halting problem to deciding the entangled value of a nonlocal game.", [bib("First public version posted January 2020", "https://arxiv.org/abs/2001.04383")])],
  "people": [person("William Slofstra", "originator", "https://uwaterloo.ca/pure-mathematics/contacts/william-slofstra", "Tsirelson's problem and an embedding theorem for groups arising from non-local games", 2016, "https://arxiv.org/abs/1606.03140", "Transfers solution-group embedding to nonlocal games")],
  "notes": "The inherited arXiv:1709.05032 points to a different paper by Dykema, Paulsen and Prakash. Slofstra's non-closure paper is arXiv:1703.08618. The 2017 paper's later version adds finite-dimensional undecidability; do not backdate that particular statement to version 1 without checking it."
 },
 "QC78/WC95": {
  "aliases": ["NTK", "infinite-width neural networks", "kernel gradient descent", "lazy training"],
  "milestones": [
   m("first_statement", 2018, "Neural tangent kernel defined", "A. Jacot, F. Gabriel and C. Hongler, Neural Tangent Kernel: Convergence and Generalization in Neural Networks, arXiv:1806.07572 (2018)", ["Arthur Jacot", "Franck Gabriel", "Clément Hongler"], "The preprint defines the NTK for neural-network training.", [bib("First public version posted June 2018", "https://arxiv.org/abs/1806.07572")], note="The same paper defines and uses the kernel."),
   m("first_application", 2018, "NTK used to analyze training and generalization", "A. Jacot, F. Gabriel and C. Hongler, Neural Tangent Kernel: Convergence and Generalization in Neural Networks, arXiv:1806.07572 (2018)", ["Arthur Jacot", "Franck Gabriel", "Clément Hongler"], "The authors describe infinite-width gradient descent through kernel dynamics and analyze convergence.", [bib("The abstract explicitly describes training dynamics", "https://arxiv.org/abs/1806.07572")], note="The same work truly plays both first-statement and first-application roles."),
   m("key_development", 2019, "NTK spectra analyzed", "G. Yang and H. Salman, A Fine-Grained Spectral Perspective on Neural Networks, arXiv:1907.10599 (2019)", [], "Spectral analysis of the NTK studies learning bias and generalization across architectures.", [bib("Public preprint posted July 2019", "https://arxiv.org/abs/1907.10599")])],
  "people": [person("Clément Hongler", "originator", "https://www.epfl.ch/labs/csft/clement-hongler/", "Neural Tangent Kernel: Convergence and Generalization in Neural Networks", 2018, "https://arxiv.org/abs/1806.07572", "Co-introduces the NTK and its training analysis")],
  "notes": "This record covers the neural tangent kernel, not the entire mean-field theory of neural networks. The inherited summary conflates related but distinct infinite-width regimes."
 },
 "WC65": {
  "aliases": ["Lorentzian polynomials", "strong Mason conjecture", "log-concavity in matroids", "M-convex functions"],
  "milestones": [
   m("precursor", 2015, "Matroid Hodge theory proves log-concavity", "K. Adiprasito, J. Huh and E. Katz, Hodge Theory for Combinatorial Geometries, arXiv:1511.02888 (2015)", ["June Huh"], "The earlier matroid Hodge theorem motivates later Lorentzian-polynomial methods.", [bib("First public version posted November 2015", "https://arxiv.org/abs/1511.02888")]),
   m("first_statement", 2019, "Lorentzian polynomial class developed", "P. Brändén and J. Huh, Lorentzian polynomials, arXiv:1902.03719 (2019)", ["Petter Brändén", "June Huh"], "The preprint defines the class and connects it to matroids and M-convex sets.", [bib("First public version posted February 2019", "https://arxiv.org/abs/1902.03719")], note="The same paper defines the class and proves major applications."),
   m("first_application", 2019, "Lorentzian method proves strongest Mason conjecture", "P. Brändén and J. Huh, Lorentzian polynomials, arXiv:1902.03719 (2019)", ["Petter Brändén", "June Huh"], "The paper applies Lorentzian-polynomial theory to the homogenized matroid Tutte polynomial and strongest Mason conjecture.", [bib("The abstract explicitly states these applications", "https://arxiv.org/abs/1902.03719")], note="The same work truly plays both first-statement and first-application roles.")],
  "people": [person("Petter Brändén", "originator", "https://www.kth.se/profile/pbranden/", "Lorentzian polynomials", 2019, "https://arxiv.org/abs/1902.03719", "Co-develops the Lorentzian-polynomial framework")],
  "notes": "The checked founding preprint was posted in 2019. The catalogue's 2018 start was not promoted without a matching public record; the 2020 Annals issue is a later publication of the same work."
 },
 "QC99": {
  "aliases": ["o-minimal Hodge theory", "definable period maps", "algebraicity of Hodge loci", "Ax-Schanuel for Hodge structures"],
  "milestones": [
   m("precursor", 2017, "Ax–Schanuel for Hodge variations", "B. Bakker and J. Tsimerman, The Ax-Schanuel conjecture for variations of Hodge structures, arXiv:1712.05088 (2017)", ["Benjamin Bakker", "Jacob Tsimerman"], "A related period-map transcendence theorem predates the tame-topology paper.", [bib("First public version posted December 2017", "https://arxiv.org/abs/1712.05088")]),
   m("first_statement", 2018, "Arithmetic quotients shown o-minimally definable", "B. Bakker, B. Klingler and J. Tsimerman, Tame topology of arithmetic quotients and algebraicity of Hodge loci, arXiv:1810.04801 (2018)", ["Benjamin Bakker", "Bruno Klingler", "Jacob Tsimerman"], "The paper develops the tame-topology framework for arithmetic quotients and period maps.", [bib("First public version posted October 2018", "https://arxiv.org/abs/1810.04801")], note="The same paper states the framework and applies it."),
   m("first_application", 2018, "Definability applied to Hodge loci", "B. Bakker, B. Klingler and J. Tsimerman, Tame topology of arithmetic quotients and algebraicity of Hodge loci, arXiv:1810.04801 (2018)", ["Benjamin Bakker", "Bruno Klingler", "Jacob Tsimerman"], "The authors derive algebraicity statements for Hodge loci using o-minimal definability.", [bib("The abstract names the Hodge-locus application", "https://arxiv.org/abs/1810.04801")], note="The same work truly plays both first-statement and first-application roles.")],
  "people": [person("Benjamin Bakker", "developer", "https://benjamin-bakker.github.io/", "Tame topology of arithmetic quotients and algebraicity of Hodge loci", 2018, "https://arxiv.org/abs/1810.04801", "Co-develops and applies o-minimal Hodge methods")],
  "notes": "The event summary mixes the 2017 Ax–Schanuel theorem with the 2018 tame-topology work. The former is retained as a related precursor, not asserted to be an o-minimal application."
 },
 "Q13": {
  "aliases": ["Lorentzian optimal transport", "synthetic timelike Ricci curvature", "Lorentzian length spaces", "nonsmooth spacetime curvature"],
  "milestones": [
   m("precursor", 2018, "Transport entropy characterizes smooth strong energy condition", "R. J. McCann, Displacement convexity of Boltzmann's entropy characterizes the strong energy condition from general relativity, arXiv:1808.01536 (2018)", [], "A smooth-spacetime transport characterization precedes the synthetic extension.", [bib("First public version posted August 2018", "https://arxiv.org/abs/1808.01536")]),
   m("first_statement", 2020, "Synthetic timelike Ricci bounds formulated", "F. Cavalletti and A. Mondino, Optimal transport in Lorentzian synthetic spaces, synthetic timelike Ricci curvature lower bounds and applications, arXiv:2004.08934 (2020)", ["Fabio Cavalletti", "Andrea Mondino"], "The preprint defines timelike Ricci lower bounds using transport in Lorentzian synthetic spaces.", [bib("First public version posted April 2020", "https://arxiv.org/abs/2004.08934")], note="The same paper formulates and applies synthetic curvature bounds."),
   m("first_application", 2020, "Synthetic curvature applied to Lorentzian comparison", "F. Cavalletti and A. Mondino, Optimal transport in Lorentzian synthetic spaces, synthetic timelike Ricci curvature lower bounds and applications, arXiv:2004.08934 (2020)", ["Fabio Cavalletti", "Andrea Mondino"], "The paper uses the new transport bounds for geometric comparison applications in Lorentzian length spaces.", [bib("The paper's title and abstract identify applications", "https://arxiv.org/abs/2004.08934")], note="The same work truly plays both first-statement and first-application roles."),
   m("key_development", 2025, "Synthetic null hypersurfaces studied", "F. Cavalletti, A. Mondino and E. Manini, On the geometry of synthetic null hypersurfaces, arXiv:2506.04934 (2025)", [], "The later paper develops geometry of null hypersurfaces in the synthetic setting.", [bib("First public version posted June 2025", "https://arxiv.org/abs/2506.04934")])],
  "people": [person("Fabio Cavalletti", "originator", "https://www.unimi.it/it/ugov/person/fabio-cavalletti", "Optimal transport in Lorentzian synthetic spaces, synthetic timelike Ricci curvature lower bounds and applications", 2020, "https://arxiv.org/abs/2004.08934", "Co-formulates and applies synthetic timelike Ricci bounds")],
  "notes": "The catalogue's claim that the cited 2025 null-hypersurface paper reproves Hawking–Penrose singularity theorems is unsupported by that citation and is not repeated here. A separate source is needed for the singularity-theorem part of the event name."
 },
 "Q40": {
  "aliases": ["condensed sets", "condensed abelian groups", "solid completion", "liquid vector spaces"],
  "milestones": [
   m("first_statement", 2019, "Condensed abelian groups publicly described", None, ["Dustin Clausen", "Peter Scholze"], "A public institute seminar abstract describes condensed abelian groups and solid completion as joint work.", [history("The MPIM seminar record dated September 2019 contains the public abstract", "https://www.mpim-bonn.mpg.de/node/9765", "Max Planck Institute for Mathematics")], note="This seminar abstract is a public statement, but the first publication date of the original course notes remains to be independently pinned down."),
   m("institution", 2019, "Named Bonn course on condensed mathematics", None, ["Dustin Clausen", "Peter Scholze"], "Bonn lists a summer-term course and notes with the field name.", [history("Scholze's official lecture-notes index identifies the course as SS 19", "https://www.math.uni-bonn.de/people/scholze/Notes.html?language=en", "University of Bonn")], note="The currently hosted PDF is a 2026 update and is not used to date the original document."),
   m("first_application", 2020, "Condensed vector spaces used for functional-analysis theorem", None, ["Dustin Clausen", "Peter Scholze"], "The liquid-vector-space theorem is presented as a key application of condensed mathematics to functional analysis.", [{"claim": "Scholze's public note sets out the liquid-vector-space theorem and its application", "source": "Scholze, original research note", "url": "https://xenaproject.wordpress.com/2020/12/05/liquid-tensor-experiment/", "kind": "primary_text"}], note="This records a documented application, not a proven first application of every condensed construction. The 2020 note has no checked bibliographic record, so the work field remains empty.")],
  "people": [person("Peter Scholze", "originator", "https://www.uni-bonn.de/de/forschung-lehre/forschungsprofil/transdisziplinaere-forschungsbereiche/modelling/mitgliederverzeichnis/peter-scholze", "Lectures on Condensed Mathematics (updated citable edition)", 2026, "https://arxiv.org/abs/2605.03658", "Presents the joint Clausen–Scholze framework; this work entry refers specifically to the 2026 edition")],
  "notes": "The 2019 course and public seminar are independently documented, but the currently citable arXiv edition of the lecture notes is from 2026. The original 2019 notes' publication date remains uncertain. The 2020 public liquid-tensor note is an application rather than a firstness proof."
 }
}


def main():
    staged = json.loads((BASE / "batch51.json").read_text())
    rows = []
    for source in staged:
        item = spec[source["eventId"]]
        rows.append({"pid": source["pid"], "eventId": source["eventId"], "canonicalName": source["name"],
                     "aliases": item["aliases"], "phases": item.get("phases", []),
                     "milestones": sorted(item["milestones"], key=lambda entry: entry["year"]),
                     "people": item["people"], "notes": item["notes"]})
    target = BASE / "milestones51.json"
    target.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {len(rows)} events and {sum(len(row['milestones']) for row in rows)} milestones")


if __name__ == "__main__":
    main()
