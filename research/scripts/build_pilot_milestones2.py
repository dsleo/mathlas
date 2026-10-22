#!/usr/bin/env python3
"""Directly reconcile the second fixed pilot ten into dated, sourced stages.

The original A/B/direct ledgers remain research inputs. This file makes the
stage choices explicit so disputed dates and ancient source gaps remain visible.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/collection/enrichment/pilot"
A = {x["pid"]: x for x in json.loads((BASE / "A2.json").read_text())}
B = {x["pid"]: x for x in json.loads((BASE / "B2.json").read_text())}
D = {x["pid"]: x for x in json.loads((BASE / "direct-research.json").read_text())["events"]}
IDS = {x["pid"]: x["eventId"] for x in json.loads((BASE / "manifest.json").read_text())["events"]}


def ev(pid, date, index=0, source="A"):
    row = {"A": A, "B": B, "D": D}[source][pid]
    item = row["dates"][date]["evidence"][index]
    return {key: item[key] for key in ("claim", "source", "url", "kind")}


def m(role, year, label, work, people, description, evidence, *, end=None, precision="year", confidence="medium", note=None, phase=None):
    out = {"role": role, "year": year, "precision": "range" if end is not None else precision,
           "label": label, "work": work, "people": people, "description": description,
           "evidence": evidence, "confidence": confidence}
    if end is not None:
        out["endYear"] = end
    if note:
        out["note"] = note
    if phase:
        out["phase"] = phase
    return out


spec = {
 "P108": {
  "phases": ["general large deviations", "Markov-process applications"],
  "milestones": [
   m("precursor", 1938, "Cramér's rare-event theorem", "H. Cramér, Sur un nouveau théorème-limite de la théorie des probabilités (1938)", ["Harald Cramer"], "Earlier probability result, narrower than the later general theory.", [ev("P108","conceptual",2)], confidence="low", phase="general large deviations"),
   m("first_statement",1966,"Varadhan's general asymptotic framework","S. R. S. Varadhan, Asymptotic probabilities and differential equations, CPAM 19 (1966)",["S. R. Srinivasa Varadhan"],"A public paper formulates the general large-deviation approach used here.",[ev("P108","conceptual")],phase="general large deviations"),
   m("first_application",1975,"Donsker–Varadhan apply variational asymptotics to Markov processes","M. D. Donsker and S. R. S. Varadhan, Asymptotic evaluation of certain Markov process expectations for large time I (1975)",["Monroe D. Donsker","S. R. Srinivasa Varadhan"],"The framework is deliberately applied to a Markov-process target.",[ev("P108","methodological")],phase="Markov-process applications"),
   m("consolidation",1984,"Varadhan's large-deviations lecture monograph","S. R. S. Varadhan, Large Deviations and Applications (1984)",["S. R. Srinivasa Varadhan"],"A named book-length treatment consolidates the theory.",[{
       "claim":"Published CBMS-NSF lecture monograph, 1984","source":"zbMATH Open","url":"https://zbmath.org/?q=an:0549.60023","kind":"bibliographic_record"}],phase="general large deviations")],
  "note": "The 1956 title-use claim in pass A is not promoted: it names a generic phrase, not clearly this general theory. Lanford's 1973 statistical-mechanics route and the 1975 Donsker–Varadhan target are separate possible methodological anchors."
 },
 "P086": {
  "milestones": [
   m("precursor",1982,"Yao connects computational hardness and pseudorandomness","A. C. Yao, Theory and application of trapdoor functions, FOCS (1982)",[],"A precursor supplies a computational route to pseudorandomness.",[ev("P086","conceptual")]),
   m("precursor",1982,"Blum–Micali pseudorandom bits","M. Blum and S. Micali, How to generate cryptographically strong sequences of pseudo random bits, FOCS (1982)",[],"A second precursor constructs pseudorandom sequences under hardness assumptions.",[ev("P086","conceptual",1)]),
   m("first_statement",1988,"Nisan–Wigderson formulate hardness versus randomness","N. Nisan and A. Wigderson, Hardness vs. randomness, FOCS (1988)",["Noam Nisan","Avi Wigderson"],"The published conference paper states the named tradeoff.",[ev("P086","methodological")],note="This paper both states the framework and applies it; see the adjacent milestone."),
   m("first_application",1988,"Nisan–Wigderson use hard functions for derandomization","N. Nisan and A. Wigderson, Hardness vs. randomness, FOCS (1988)",["Noam Nisan","Avi Wigderson"],"The construction targets randomized computation.",[ev("P086","methodological")],note="The same paper truly plays both first-statement and first-application roles."),
   m("naming",1988,"The phrase appears in a paper title","N. Nisan and A. Wigderson, Hardness vs. randomness, FOCS (1988)",["Noam Nisan","Avi Wigderson"],"The published title provides a reproducible naming anchor.",[ev("P086","institutional")],note="The same paper both names and develops the subject; it is deliberately recorded under both roles.")],
  "note":"The 1982 cryptographic papers are precursors, not a claim that the later named derandomization framework already existed."
 },
 "P329": {
  "phases": ["measure rigidity", "Littlewood and arithmetic QUE"],
  "milestones": [
   m("precursor",1967,"Furstenberg's disjointness and Diophantine problem","H. Furstenberg, Disjointness in ergodic theory, minimal sets, and a problem in Diophantine approximation (1967)",["Hillel Furstenberg"],"Ergodic ideas enter the Diophantine context before the 2006 transfer.",[ev("P329","conceptual")],phase="measure rigidity"),
   m("first_statement",2006,"Measure rigidity attacks Littlewood exceptions","M. Einsiedler, A. Katok and E. Lindenstrauss, Invariant measures and the set of exceptions to Littlewood's conjecture (2006)",["Manfred Einsiedler","Anatole Katok","Elon Lindenstrauss"],"The public paper formulates the measure-rigidity transfer relevant to this event.",[ev("P329","methodological")],note="This paper states and applies the transfer; see adjacent target milestone.",phase="Littlewood and arithmetic QUE"),
   m("first_application",2006,"Exceptional set for Littlewood's conjecture","M. Einsiedler, A. Katok and E. Lindenstrauss, Invariant measures and the set of exceptions to Littlewood's conjecture (2006)",["Manfred Einsiedler","Anatole Katok","Elon Lindenstrauss"],"Measure rigidity is used on the Littlewood exceptional set.",[ev("P329","methodological")],note="The same paper truly plays both first-statement and first-application roles.",phase="Littlewood and arithmetic QUE"),
   m("key_development",2006,"Lindenstrauss proves arithmetic QUE case","E. Lindenstrauss, Invariant measures and arithmetic quantum unique ergodicity (2006)",["Elon Lindenstrauss"],"A companion arithmetic application extends the transfer.",[ev("P329","methodological",1)],phase="Littlewood and arithmetic QUE"),
   m("naming",2007,"Measure rigidity and p-adic Littlewood in a title","M. Einsiedler and D. Kleinbock, Measure rigidity and p-adic Littlewood-type problems (2007)",["Manfred Einsiedler"],"The title explicitly names the transfer being tracked.",[ev("P329","institutional")],confidence="low",phase="Littlewood and arithmetic QUE")],
  "note":"Passes A and B date the Furstenberg precursor to 1967; the direct pass starts the specific 2006 event there. These are separate stages, not conflicting birth dates. The 2007 naming citation still needs a catalogue-level title check."
 },
 "P186": {
  "milestones": [
   m("precursor",-2000,"Old Babylonian tablet procedures","Old Babylonian mathematical tablets (individual dates unverified)",[],"Tablet problems use area and volume procedures later described as quadratic or cubic.",[ev("P186","conceptual",0,"B")],end=-1600,confidence="low",note="The cited history dates a broad period, not a specific tablet or publication."),
   m("key_development",1935,"Neugebauer publishes cuneiform mathematical texts","O. Neugebauer, Mathematische Keilschrift-Texte (1935)",["Otto Neugebauer"],"A modern edition makes the relevant tablets accessible as research texts.",[ev("P186","institutional",1,"B")],confidence="low"),
   m("naming",1937,"Gandz names Babylonian quadratic equations","S. Gandz, The origin and development of the quadratic equations in Babylonian, Greek and early Arabic algebra (1937)",[],"The modern article title explicitly names the studied procedure.",[ev("P186","institutional",0,"B")],confidence="low")],
  "note":"No precise original publication date or named ancient author has been established. Searches in MacTutor and the cited modern tablet editions provide a period only; conceptual and methodological derived dates stay empty. Modern naming is not an ancient institutional date."
 },
 "P119": {
  "milestones": [
   m("precursor",None,"Archimedes' statics treatises, undated","Archimedes, On the Equilibrium of Planes and On Floating Bodies",["Archimedes of Syracuse"],"The ancient treatises combine mechanical questions with geometric arguments.",[ev("P119","conceptual",0,"B")],precision="unknown",confidence="low",note="MacTutor gives a lifespan but no defensible composition or publication year; searched MacTutor and Open Library."),
   m("key_development",1586,"Stevin's published statics treatise","S. Stevin, De Beghinselen der Weeghconst (1586)",[],"A documented early modern development of the statics tradition.",[ev("P119","institutional",0,"B")],confidence="low"),
   m("consolidation",1897,"Heath publishes English Archimedes edition","T. L. Heath, The Works of Archimedes (1897)",["Archimedes of Syracuse"],"The edition consolidates access to the ancient statics corpus.",[ev("P119","conceptual",1,"B")],confidence="low",note="This dates the modern edition, not Archimedes' original treatise.")],
  "note":"A lifespan bound (287–212 BCE) is not a publication date. Both ancient derived dates remain empty. Stevin's 1586 treatise is not claimed to be the first statics book; medieval traditions were not exhausted."
 },
 "P408": {
  "phases": ["abstract field", "abstract ring"],
  "milestones": [
   m("precursor",1871,"Dedekind's field and ideal language","R. Dedekind, supplement to Dirichlet's Vorlesungen über Zahlentheorie (1871)",["Richard Dedekind"],"A field and ideal vocabulary precedes explicit axiomatic treatments.",[ev("P408","conceptual",1)],phase="abstract field"),
   m("first_statement",1893,"Weber's abstract field framework","H. Weber, Die allgemeinen Grundlagen der Galois'schen Gleichungstheorie (1893)",["Heinrich Weber"],"A checked published paper develops the abstract field framework.",[ev("P408","conceptual",0,"D")],phase="abstract field"),
   m("key_development",1910,"Steinitz's algebraic theory of fields","E. Steinitz, Algebraische Theorie der Körper (1910)",["Ernst Steinitz"],"Systematic field concepts extend the abstract programme.",[ev("P408","methodological")],phase="abstract field"),
   m("first_application",1921,"Noether applies abstract ring theory to ideals","E. Noether, Idealtheorie in Ringbereichen (1921)",["Emmy Noether"],"The abstract ring viewpoint is used to solve ideal-theoretic problems.",[ev("P408","methodological",0,"D")],phase="abstract ring"),
   m("consolidation",1930,"Moderne Algebra synthesizes the subject","B. L. van der Waerden, Moderne Algebra I (1930)",["Bartel van der Waerden"],"The textbook brings the abstract ring and field programme into a named course of study.",[ev("P408","institutional")])],
  "note":"The event bundles fields and rings: Dedekind 1871, Weber 1893, Steinitz 1910 and Noether 1921 mark distinct claims. The 1930 textbook is consolidation rather than origin."
 },
 "P179": {
  "milestones": [
   m("first_statement",1710,"Arbuthnot states a chance argument","J. Arbuthnot, An argument for Divine Providence, Philosophical Transactions (1710)",["John Arbuthnot"],"The public paper frames an unusually persistent birth-sex ratio as unlikely by chance.",[ev("P179","conceptual")],note="This paper both states and applies the argument; see adjacent milestone."),
   m("first_application",1710,"Coin-toss calculation on christening data","J. Arbuthnot, An argument for Divine Providence, Philosophical Transactions (1710)",["John Arbuthnot"],"The chance calculation is applied to annual London christening counts.",[ev("P179","methodological")],note="The same paper truly plays both first-statement and first-application roles."),
   m("consolidation",1925,"Fisher's significance-testing textbook","R. A. Fisher, Statistical Methods for Research Workers (1925)",["Ronald A. Fisher"],"The much later textbook consolidates significance testing as a method.",[ev("P179","institutional")],confidence="low")],
  "note":"Fisher 1925 is an institutional anchor for significance testing generally, not a direct continuation of Arbuthnot's providential interpretation; some pass-B sources suggest earlier named treatments."
 },
 "P021": {
  "milestones": [
   m("first_statement",1946,"Leray publishes the sheaf idea","J. Leray, L'anneau d'homologie d'une représentation, C. R. Acad. Sci. Paris 222 (1946)",["Jean Leray"],"The published note supplies an early public sheaf formulation.",[ev("P021","conceptual")],note="The same note also applies the tool to homology; see adjacent milestone."),
   m("first_application",1946,"Leray uses sheaves in homology","J. Leray, L'anneau d'homologie d'une représentation, C. R. Acad. Sci. Paris 222 (1946)",["Jean Leray"],"Sheaves are used on a representation's homological problem.",[ev("P021","methodological",0,"D")],note="The same paper truly plays both first-statement and first-application roles."),
   m("institution",1950,"Cartan's seminar covers sheaves","H. Cartan, Séminaire Henri Cartan, 1950–51: cohomologie, suites spectrales, faisceaux",["Henri Cartan"],"The named lecture series brings sheaves into sustained teaching.",[ev("P021","institutional")],end=1951,confidence="low"),
   m("key_development",1955,"Serre applies coherent sheaves to algebraic geometry","J.-P. Serre, Faisceaux algébriques cohérents, Ann. Math. 61 (1955)",["Jean-Pierre Serre"],"Coherent sheaves become a central algebraic-geometric tool.",[ev("P021","methodological",1)],confidence="medium")],
  "note":"Pass A uses Cartan 1953 and pass B Serre 1955 for the first application to later target areas. Leray's 1946 note already uses the tool for homology, so that earlier target is retained separately."
 },
 "P288": {
  "milestones": [
   m("first_statement",1959,"Iwasawa publishes the cyclotomic-tower framework","K. Iwasawa, On the Theory of Cyclotomic Fields, Ann. Math. (1959)",["Kenkichi Iwasawa"],"A public paper states the arithmetic tower framework.",[ev("P288","conceptual",0,"D")],note="The same paper states and applies the framework; see adjacent milestone."),
   m("first_application",1959,"Class groups in cyclotomic towers","K. Iwasawa, On the Theory of Cyclotomic Fields, Ann. Math. (1959)",["Kenkichi Iwasawa"],"The framework is used to study class-group growth.",[ev("P288","methodological",0,"D")],note="The same paper truly plays both first-statement and first-application roles."),
   m("key_development",1973,"Iwasawa extends the Z-l tower theory","K. Iwasawa, On Z-l-extensions of algebraic number fields, Ann. Math. 98 (1973)",["Kenkichi Iwasawa"],"A later paper develops the arithmetic theory.",[ev("P288","methodological",1)]),
   m("naming",1977,"Iwasawa theory appears in a paper title","J. Coates, p-adic L-functions and Iwasawa theory (1977)",[],"The named title provides a reproducible institutional anchor.",[ev("P288","institutional")],confidence="low")],
  "note":"The 1956 Seattle lecture is not the public-paper date. The 1977 naming citation is a zbMATH record that the automated Crossref checker cannot yet resolve."
 },
 "P405": {
  "milestones": [
   m("first_statement",1920,"Łukasiewicz publishes three-valued logic","J. Łukasiewicz, O logice trójwartościowej, Ruch Filozoficzny 5 (1920)",["Jan Lukasiewicz"],"A public note formulates the three-valued system.",[ev("P405","conceptual",0,"D")],note="The same paper states, applies and names this particular system; see adjacent milestones."),
   m("first_application",1920,"Three values applied to future contingents","J. Łukasiewicz, O logice trójwartościowej, Ruch Filozoficzny 5 (1920)",["Jan Lukasiewicz"],"The extra truth value addresses future-contingent propositions.",[ev("P405","methodological",0,"D")],note="The same paper truly plays both first-statement and first-application roles."),
   m("naming",1920,"Three-valued logic named in the title","J. Łukasiewicz, O logice trójwartościowej, Ruch Filozoficzny 5 (1920)",["Jan Lukasiewicz"],"The title explicitly names three-valued logic, a narrower term than all many-valued logics.",[ev("P405","institutional",0,"D")],note="The same paper plays both naming and first-statement roles; the term here names the three-valued phase."),
   m("key_development",1921,"Post generalizes to finitely many values","E. Post, Introduction to a general theory of elementary propositions, Amer. J. Math. 43 (1921)",["Emil Post"],"Finite many-valued truth-table systems extend the initial example.",[ev("P405","methodological")]),
   m("consolidation",1952,"Many-valued logics monograph","J. B. Rosser and A. R. Turquette, Many-valued Logics (1952)",[],"A book-length treatment consolidates the named wider field.",[ev("P405","institutional")],confidence="low")],
  "note":"Three-valued logic (1920) is a phase within many-valued logic. A broader first use of the phrase many-valued logic may differ from the 1920 narrow title; the 1952 monograph is a secure later naming anchor."
 }
}


def main():
    rows = []
    for pid in [x["pid"] for x in json.loads((BASE / "pilot2.json").read_text())]:
        a = A[pid]
        item = spec[pid]
        rows.append({"pid": pid, "eventId": IDS[pid], "canonicalName": a["canonicalName"],
                     "aliases": a["aliases"], "phases": item.get("phases", []),
                     "milestones": sorted(item["milestones"], key=lambda v: v["year"] if v["year"] is not None else 9999),
                     "people": a["people"][:6], "notes": item["note"]})
    target = BASE / "milestones2.json"
    target.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {len(rows)} events and {sum(len(x['milestones']) for x in rows)} milestones to {target}")


if __name__ == "__main__":
    main()
