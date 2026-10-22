#!/usr/bin/env python3
"""Write the manually checked, source-linked direct pilot research ledger.

This is a single researcher pass. It deliberately makes no inter-model agreement
claim and leaves dates empty where the stated definition has not been evidenced.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "data/collection/enrichment/pilot"
MANIFEST = json.loads((PILOT / "manifest.json").read_text())


def ev(claim, source, url, kind="bibliographic_record"):
    return {"claim": claim, "source": source, "url": url, "kind": kind}


def date(year=None, claim=None, source=None, url=None, kind="bibliographic_record", note=""):
    if year is None:
        return {"start": None, "end": None, "precision": "unknown", "confidence": "none", "grade": None, "evidence": [], "note": note}
    return {"start": year, "end": year, "precision": "year", "confidence": "medium" if kind == "bibliographic_record" else "low", "grade": "B" if kind == "bibliographic_record" else "C", "evidence": [ev(claim, source, url, kind)], "note": note}


def work(title, year, url, why):
    return {"citation": title, "year": year, "url": url, "whyItMatters": why}


def person(name, role, lifespan, bio, works):
    return {"name": name, "role": role, "lifespan": lifespan, "biographyUrl": bio, "works": works}


D = {}


def add(pid, aliases, conceptual, methodological, institutional, people, notes, first_term_use=None):
    D[pid] = {"aliases": aliases, "dates": {"conceptual": conceptual, "methodological": methodological, "institutional": institutional}, "firstTermUse": first_term_use, "people": people, "notes": notes}


# Batch 1. The links below are to the original publication or a catalogue of it,
# rather than search-result matches. A work's date is not silently a field date.
add("P367", ["qualitative dynamics", "celestial mechanics", "three-body problem"],
    date(1881, "Poincaré's first Sur les courbes paper was published in 1881.", "Numdam journal record", "https://www.numdam.org/item/JMPA_1881_3_7__375_0/"),
    date(1890, "The published three-body memoir applies qualitative dynamics to celestial mechanics.", "Henri Poincaré Papers bibliographic record", "https://henripoincarepapers.univ-nantes.fr/en/bibliohp/ajax.php?bibkey=hp1890am"),
    date(1927, "Birkhoff's textbook is titled Dynamical Systems.", "AMS book record", "https://doi.org/10.1090/coll/009"),
    [person("Henri Poincaré", "originator", "1854–1912", "https://mathshistory.st-andrews.ac.uk/Biographies/Poincare/", [work("Sur les courbes définies par une équation différentielle", 1881, "https://www.numdam.org/item/JMPA_1881_3_7__375_0/", "Qualitative study of differential-equation curves")]), person("George David Birkhoff", "systematiser", "1884–1944", "https://mathshistory.st-andrews.ac.uk/Biographies/Birkhoff/", [work("Dynamical Systems", 1927, "https://doi.org/10.1090/coll/009", "Named textbook")])],
    "The 1881 conceptual paper is not yet the three-body application; Poincaré's 1890 memoir is the checked target-problem anchor.")

add("P363", ["metric space", "abstract distance", "espace métrique"],
    date(1906, "Fréchet's 1906 thesis gives the abstract-space framework used for metric spaces.", "Crossref original article record", "https://doi.org/10.1007/BF03018603", note="A 1905 note on écart is a precursor; whether it satisfies the full metric axioms needs checking."),
    date(1906, "Fréchet's work applies abstract distance to functional calculus.", "Crossref original article record", "https://doi.org/10.1007/BF03018603"),
    date(note="Searched Crossref for Fréchet 1906, Hausdorff 1914 and Fréchet 1928 books; no checked earliest title that names metric spaces."),
    [person("Maurice Fréchet", "originator", "1878–1973", "https://mathshistory.st-andrews.ac.uk/Biographies/Frechet/", [work("Sur quelques points du calcul fonctionnel", 1906, "https://doi.org/10.1007/BF03018603", "Abstract-distance framework")])],
    "Do not infer that the term metric space appeared in the 1906 title.")

add("P026", ["Langlands program", "Langlands correspondence", "automorphic–Galois reciprocity"],
    date(1970, "The published account Problems in the theory of automorphic forms appeared in 1970.", "Springer book chapter record", "https://doi.org/10.1007/BFb0079065", note="The January 1967 Weil letter circulated privately; IAS identifies 1970 as the first published account."),
    date(1970, "Jacquet and Langlands use the programme's ideas for GL(2).", "Springer book record", "https://doi.org/10.1007/BFb0058988"),
    date(note="Searched Crossref/IAS for earliest textbook or paper title explicitly naming the Langlands programme; the 1970 publications do not name the programme in their titles."),
    [person("Robert Langlands", "originator", "born 1936", "https://www.ias.edu/scholars/langlands", [work("Problems in the theory of automorphic forms", 1970, "https://doi.org/10.1007/BFb0079065", "First published account")]), person("Hervé Jacquet", "developer", "born 1939", "https://en.wikipedia.org/wiki/Herv%C3%A9_Jacquet", [work("Automorphic Forms on GL(2)", 1970, "https://doi.org/10.1007/BFb0058988", "Early target case")])],
    "1967 private-letter priority is preserved separately: https://publications.ias.edu/book/export/html/43. It cannot be the conceptual publication date. IAS publication history: https://publications.ias.edu/rpl/problems.")

add("P232", ["formal grammars", "Chomsky hierarchy", "generative grammar"],
    date(1956, "Chomsky compares formal models for language in a 1956 publication.", "IEEE original article record", "https://doi.org/10.1109/TIT.1956.1056813"),
    date(1956, "The paper purposely tests grammar models against language description.", "IEEE original article record", "https://doi.org/10.1109/TIT.1956.1056813"),
    date(note="Searched Crossref for formal-language textbook and journal titles; no checked earliest institutional anchor."),
    [person("Noam Chomsky", "originator", "born 1928", "https://en.wikipedia.org/wiki/Noam_Chomsky", [work("Three models for the description of language", 1956, "https://doi.org/10.1109/TIT.1956.1056813", "Formal grammar classes applied to language")])],
    "The 1956 journal date, rather than the date of any talk, governs the entry.")

add("P406", ["Fuchsian equations", "regular singular point", "Frobenius series"],
    date(1866, "Fuchs published the theory of variable-coefficient linear differential equations in 1866.", "De Gruyter original article record", "https://doi.org/10.1515/crll.1866.66.121"),
    date(1873, "Frobenius deliberately integrates linear ODEs by power series.", "De Gruyter original article record", "https://doi.org/10.1515/crll.1873.76.214"),
    date(note="Searched the 1866 Fuchs and 1873 Frobenius article records; neither establishes a first named textbook, journal, lecture series, or title for the field."),
    [person("Lazarus Fuchs", "originator", "1833–1902", "https://mathshistory.st-andrews.ac.uk/Biographies/Fuchs/", [work("Zur Theorie der linearen Differentialgleichungen mit veränderlichen Coefficienten", 1866, "https://doi.org/10.1515/crll.1866.66.121", "Regular singular equations")]), person("Ferdinand Georg Frobenius", "developer", "1849–1917", "https://mathshistory.st-andrews.ac.uk/Biographies/Frobenius/", [work("Ueber die Integration der linearen Differentialgleichungen durch Reihen", 1873, "https://doi.org/10.1515/crll.1873.76.214", "Series solution method")])],
    "The name Frobenius method postdates the 1866 Fuchs precursor; the two dates describe different contributions.")

add("P159", ["Cotes formula", "complex logarithms", "Logometria"],
    date(1714, "Cotes published Logometria in Philosophical Transactions in 1714.", "Royal Society original article record", "https://doi.org/10.1098/rstl.1714.0002"),
    date(1714, "Logometria uses logarithmic measures for circular angles.", "Royal Society original article record", "https://doi.org/10.1098/rstl.1714.0002"),
    date(note="Searched the Royal Society 1714 article and Open Library's 1722 Harmonia Mensurarum edition; neither identifies a separately named field institution."),
    [person("Roger Cotes", "originator", "1682–1716", "https://mathshistory.st-andrews.ac.uk/Biographies/Cotes/", [work("Logometria", 1714, "https://doi.org/10.1098/rstl.1714.0002", "Published logarithm/angle result")])],
    "Harmonia Mensurarum was published posthumously in 1722 (https://openlibrary.org/books/OL19111135M/Harmonia_mensurarum), not 1714.")

add("P134", ["Elements", "Euclidean geometry", "axiomatic geometry"],
    date(note="Searched Open Library editions and MacTutor Euclid history. The original Greek composition has no verifiable publication year; circa 300 BCE is a historical estimate, not a bibliographic publication date."),
    date(note="Searched MacTutor Euclid biography and Open Library editions; no datable first purposeful use separate from the treatise."),
    date(note="Searched Open Library's Elements records; an ancient school adoption or first named institution cannot be dated to a publication year."),
    [person("Euclid", "systematiser", None, "https://mathshistory.st-andrews.ac.uk/Biographies/Euclid/", [work("Elements (original composition undated; first printed edition)", 1482, "https://openlibrary.org/books/OL25760900M/Preclarissimus_liber_elementorum_Euclidis_perspicacissimi_in_artem_geometrie_incipit_qua_m_foeliciss", "Surviving bibliographic anchor for the treatise, not its ancient origin")])],
    "Historical estimate around 300 BCE: https://mathshistory.st-andrews.ac.uk/Extras/Valdivia_aspects_maths/. Do not substitute the 1482 edition date for ancient emergence.")

add("P066", ["algebra of logic", "Boolean algebra", "Stone duality", "Stone representation theorem"],
    date(1847, "Boole's Mathematical Analysis of Logic was published in 1847.", "Open Library edition record", "https://openlibrary.org/works/OL2630394W/The_mathematical_analysis_of_logic"),
    date(1847, "Boole applies algebraic calculation to logic in the 1847 book.", "Open Library edition record", "https://openlibrary.org/works/OL2630394W/The_mathematical_analysis_of_logic"),
    date(note="Searched the 1847 Boole and 1936 Stone records; neither title literally names 'Boolean algebra' as a field, and no first named textbook/title has been established for the merged subject."),
    [person("George Boole", "originator", "1815–1864", "https://mathshistory.st-andrews.ac.uk/Biographies/Boole/", [work("The Mathematical Analysis of Logic", 1847, "https://openlibrary.org/works/OL2630394W/The_mathematical_analysis_of_logic", "Introduces algebraic logic")]), person("Marshall Harvey Stone", "developer", "1903–1989", "https://mathshistory.st-andrews.ac.uk/Biographies/Stone/", [work("The theory of representations for Boolean algebras", 1936, "https://doi.org/10.1090/S0002-9947-1936-1501865-8", "Topological representation phase")])],
    "This merged event covers two phases, 1847 Boole and 1936 Stone. They are not competing priority dates.")

add("P057", ["Langlands over function fields", "Drinfeld modules", "shtukas", "global Langlands correspondence"],
    date(1974, "Drinfeld's elliptic modules paper appeared in 1974.", "Crossref original article record", "https://doi.org/10.1070/SM1974V023N04ABEH001731", note="1974 is the geometric-tool precursor, not the proof of the correspondence."),
    date(1983, "Drinfeld applied the geometric machinery to two-dimensional representations over a finite field.", "Annals article record", "https://doi.org/10.2307/2374382"),
    date(note="Searched Drinfeld 1974/1983 and Lafforgue 2002 records; none establishes the first named textbook, journal, lecture series or title 'function-field Langlands'."),
    [person("Vladimir Drinfeld", "originator", "born 1954", "https://en.wikipedia.org/wiki/Vladimir_Drinfeld", [work("Elliptic modules", 1974, "https://doi.org/10.1070/SM1974V023N04ABEH001731", "Geometric objects"), work("Two-dimensional l-adic representations of the fundamental group of a curve over a finite field", 1983, "https://doi.org/10.2307/2374382", "Rank-two correspondence")]), person("Laurent Lafforgue", "developer", "born 1966", "https://en.wikipedia.org/wiki/Laurent_Lafforgue", [work("Chtoucas de Drinfeld et correspondance de Langlands", 2002, "https://doi.org/10.1007/s002220100174", "General GL(n) breakthrough")])],
    "The 2002 Lafforgue extension is kept as a later milestone, not backdated into the original emergence.")

add("P533", ["elliptic curve murmurations", "Frobenius-trace murmurations", "rank patterns"],
    date(2022, "The public arXiv record first appeared on 21 April 2022.", "arXiv preprint record", "https://arxiv.org/abs/2204.10140"),
    date(2022, "The preprint applies data-scientific classification to elliptic-curve ranks.", "arXiv preprint record", "https://arxiv.org/abs/2204.10140"),
    date(2022, "The public preprint title Murmurations of elliptic curves names the phenomenon.", "arXiv preprint record", "https://arxiv.org/abs/2204.10140", note="The journal version appeared in 2024."),
    [person("Yang-Hui He", "originator", "born 1975", "https://en.wikipedia.org/wiki/Yang-Hui_He", [work("Murmurations of elliptic curves", 2022, "https://arxiv.org/abs/2204.10140", "First public preprint and data analysis")])],
    "The catalogue's 2020 date is unsupported by the checked 2022 preprint. The 2024 journal date should not displace the earlier public arXiv date.")

# Batch 2.
add("P108", ["large deviation principle", "Donsker–Varadhan theory", "rare-event asymptotics"],
    date(1966, "Varadhan's paper on asymptotic probabilities was published in 1966.", "Wiley original article record", "https://doi.org/10.1002/CPA.3160190303"),
    date(1975, "Donsker and Varadhan apply asymptotic evaluation to long-time Markov process expectations.", "Wiley original article record", "https://doi.org/10.1002/CPA.3160280102"),
    date(note="Searched the 1966 and 1975 article records and AMS Large Deviations books; no checked first textbook or title naming this probability field."),
    [person("S. R. S. Varadhan", "originator", "born 1940", "https://en.wikipedia.org/wiki/S._R._S._Varadhan", [work("Asymptotic probabilities and differential equations", 1966, "https://doi.org/10.1002/CPA.3160190303", "Early large-deviation analysis")]), person("Monroe D. Donsker", "developer", "1924–1991", "https://en.wikipedia.org/wiki/Monroe_D._Donsker", [work("Asymptotic evaluation of certain Markov process expectations for large time, I", 1975, "https://doi.org/10.1002/CPA.3160280102", "Markov-process application")])],
    "1966 and 1975 are different stages; the 1975 article supplies the explicit target-problem evidence.")

add("P086", ["derandomization", "hardness versus randomness", "Nisan–Wigderson generator"],
    date(1988, "The FOCS paper Hardness vs. randomness was published in 1988.", "IEEE conference record", "https://doi.org/10.1109/SFCS.1988.21916", note="The journal version followed in 1994."),
    date(1988, "The paper constructs a pseudorandom generator from a hard function.", "IEEE conference record", "https://doi.org/10.1109/SFCS.1988.21916"),
    date(1988, "The paper title names Hardness vs. randomness.", "IEEE conference record", "https://doi.org/10.1109/SFCS.1988.21916"),
    [person("Noam Nisan", "originator", "born 1961", "https://en.wikipedia.org/wiki/Noam_Nisan", [work("Hardness vs. randomness", 1988, "https://doi.org/10.1109/SFCS.1988.21916", "Explicit hardness-to-randomness reduction")]), person("Avi Wigderson", "originator", "born 1956", "https://en.wikipedia.org/wiki/Avi_Wigderson", [work("Hardness vs randomness", 1994, "https://doi.org/10.1016/S0022-0000(05)80043-1", "Expanded journal account")])],
    "The catalogue's 1994 date is the journal issue, not the first public publication. The paper notes a 1988 conference presentation; the 1988 proceedings record independently confirms publication.")

add("P329", ["measure rigidity", "Littlewood conjecture exceptions", "higher-rank dynamics"],
    date(2006, "The Annals article connecting invariant measures to Littlewood exceptions is dated 2006.", "Annals original article record", "https://doi.org/10.4007/annals.2006.164.513"),
    date(2006, "Its abstract applies measure classification to prove dimension zero for the exceptional set.", "Annals original article record", "https://doi.org/10.4007/annals.2006.164.513"),
    date(note="Searched Annals and Crossref for a first named textbook, journal, lecture series, or title for the combined field; no earlier institutional anchor checked."),
    [person("Manfred Einsiedler", "developer", None, "https://en.wikipedia.org/wiki/Manfred_Einsiedler", [work("Invariant measures and the set of exceptions to Littlewood’s conjecture", 2006, "https://doi.org/10.4007/annals.2006.164.513", "Measure rigidity applied to Littlewood")]), person("Anatole Katok", "developer", "1944–2018", "https://en.wikipedia.org/wiki/Anatole_Katok", [work("Invariant measures and the set of exceptions to Littlewood’s conjecture", 2006, "https://doi.org/10.4007/annals.2006.164.513", "Joint theorem")]), person("Elon Lindenstrauss", "developer", "born 1970", "https://en.wikipedia.org/wiki/Elon_Lindenstrauss", [work("Invariant measures and the set of exceptions to Littlewood’s conjecture", 2006, "https://doi.org/10.4007/annals.2006.164.513", "Joint theorem")])],
    "The catalogue's 1996 date has not been supported by a record for this specific Littlewood application.")

add("P186", ["Old Babylonian algebra", "BM 85200 + VAT 6599", "cellar problems"],
    date(note="Searched MacTutor Babylonian mathematics, Schøyen MS 3048 and publications on BM 85200+VAT 6599. The surviving tablets are dated only by broad archaeological periods; no public publication year is recoverable."),
    date(note="Searched the BM 85200+VAT 6599 tablet analysis and MacTutor account; a first purposeful application of the method cannot be ordered across undated tablets."),
    date(note="Searched museum tablet descriptions and bibliographies; no ancient named textbook, chair, lecture series, or classification anchor found."),
    [],
    "Evidence of cubic problem-solving: https://mathshistory.st-andrews.ac.uk/HistTopics/Babylonian_mathematics/ and object record https://www.schoyencollection.com/mathematics-collection/9-3-algebra/cubic-equations-table-ms-3048. Anonymous scribes cannot be assigned named-person entries. Catalogue -1900 is not a publication date.")

add("P119", ["Archimedean statics", "law of the lever", "On the Equilibrium of Planes"],
    date(note="Searched MacTutor Archimedes biography and On the Equilibrium of Planes extract plus Open Library editions; no dated original publication of the ancient treatise."),
    date(note="Searched the extant Equilibrium of Planes text and Archimedes biography; applications to balance are described but not independently datable."),
    date(note="Searched Archimedes treatise catalogues; no first institutional naming date established in antiquity."),
    [person("Archimedes", "originator", "c. 287–212 BCE", "https://mathshistory.st-andrews.ac.uk/Biographies/Archimedes/", [work("On the Equilibrium of Planes (in The Works of Archimedes)", 1897, "https://openlibrary.org/works/OL5681640W/The_works_of_Archimedes", "Primary treatise surviving in a modern bibliographic edition")])],
    "MacTutor original-text extract: https://mathshistory.st-andrews.ac.uk/Extras/Archimedes_on_statics/. The catalogue's +212 is his death year, not an emergence publication date.")

add("P408", ["abstract ring", "abstract field", "Körper", "ideal theory"],
    date(1893, "Weber's paper supplies a checked abstract-field/Galois framework in 1893.", "Springer original article record", "https://doi.org/10.1007/BF01446451", note="The ring half emerged separately: Fraenkel 1915 and Noether 1921. This single date is a field-theory anchor, not a date for both structures."),
    date(1921, "Noether applies abstract commutative ring ideas to ideal theory.", "Springer original article record", "https://doi.org/10.1007/BF01464225"),
    date(note="Searched Weber 1893, Fraenkel 1915, Noether 1921 and van der Waerden's 1930 Moderne Algebra. The event merges rings and fields; no single first institutional anchor for both has been established."),
    [person("Heinrich Weber", "developer", "1842–1913", "https://mathshistory.st-andrews.ac.uk/Biographies/Weber/", [work("Die allgemeinen Grundlagen der Galois'schen Gleichungstheorie", 1893, "https://doi.org/10.1007/BF01446451", "Abstract field setting")]), person("Emmy Noether", "systematiser", "1882–1935", "https://mathshistory.st-andrews.ac.uk/Biographies/Noether_Emmy/", [work("Idealtheorie in Ringbereichen", 1921, "https://doi.org/10.1007/BF01464225", "Unified commutative ideal theory")])],
    "Dedekind's 1871 ideal work is a precursor (https://plato.stanford.edu/entries/dedekind-foundations/), not yet a modern abstract-ring axiomatisation. Fraenkel's 1915 explicit ring paper: https://doi.org/10.1515/crll.1915.145.139. MacTutor history: https://mathshistory.st-andrews.ac.uk/HistTopics/Ring_theory/.")

add("P179", ["Arbuthnot test", "sign test", "sex-ratio hypothesis test"],
    date(1710, "Arbuthnot's argument was published in Philosophical Transactions in 1710.", "Royal Society original article record", "https://doi.org/10.1098/rstl.1710.0011"),
    date(1710, "The article tests the London birth-sex counts against equal likelihood.", "Royal Society original article record", "https://doi.org/10.1098/rstl.1710.0011"),
    date(note="Searched the Royal Society paper and later bibliographies; no first named textbook, journal, lecture series, or title for significance testing established in 1710."),
    [person("John Arbuthnot", "originator", "1667–1735", "https://en.wikipedia.org/wiki/John_Arbuthnot", [work("An argument for divine providence taken from the constant regularity observed in the births of both sexes", 1710, "https://doi.org/10.1098/rstl.1710.0011", "Binomial-tail style inference on birth records")])],
    "The Royal Society archive distinguishes the 1710 published article from an April 1711 manuscript copy: https://makingscience.royalsociety.org/items/el_a_54/paper-an-argument-for-divine-providence-taken-from-the-constant-regularity-observed-in-the-birth-of-bothe-sexes-by-john-arbuthnot.")

add("P021", ["faisceaux", "sheaves", "coherent sheaves"],
    date(1946, "Leray's Comptes rendus note introduced faisceaux in 1946.", "MathSciNet bibliographic record", "https://mathscinet.ams.org/mathscinet-getitem?mr=8%2C49d", note="The 1945 captivity-course paper is a precursor, but a full-text search found no 'faisceau' there. The 1946 original scan is https://ncatlab.org/nlab/files/Leray-0.pdf."),
    date(1946, "Leray uses sheaves for the homology of a representation in the same published note that introduces them.", "MathSciNet bibliographic record", "https://mathscinet.ams.org/mathscinet-getitem?mr=8%2C49d", note="Serre's 1955 FAC paper is a later application to algebraic geometry, not the first purposeful use of sheaves."),
    date(note="Searched Leray 1945 and Serre's 1955 Faisceaux algébriques cohérents title; a named 1955 article exists, but earlier sheaf-title use has not been ruled out."),
    [person("Jean Leray", "originator", "1906–1998", "https://mathshistory.st-andrews.ac.uk/Biographies/Leray/", [work("L'anneau d'homologie d'une représentation", 1946, "https://mathscinet.ams.org/mathscinet-getitem?mr=8%2C49d", "Introduces sheaves for cohomology of maps")]), person("Jean-Pierre Serre", "developer", "born 1926", "https://mathshistory.st-andrews.ac.uk/Biographies/Serre/", [work("Faisceaux algébriques cohérents", 1955, "https://doi.org/10.2307/1969915", "Sheaf method in algebraic geometry")])],
    "Leray's 1945 paper was based on captivity lectures but did not yet name faisceaux. The 1946 note is cited in Numdam (https://www.numdam.org/item/BSMF_1954__82__97_0/) with linked MathSciNet and zbMATH records. The 1946 date, not the 27 May submission/presentation notation, governs. Historical analysis: https://math.mit.edu/~hrm/papers/ss.pdf.")

add("P288", ["cyclotomic Iwasawa theory", "Z_p-extensions", "Iwasawa invariants"],
    date(1959, "Iwasawa's On the Theory of Cyclotomic Fields was published in 1959.", "Annals original article record", "https://doi.org/10.2307/1970328"),
    date(1959, "The paper studies class-group growth in cyclotomic towers.", "Annals original article record", "https://doi.org/10.2307/1970328"),
    date(note="Searched Annals and AMS histories of Iwasawa theory; the 1959 title says cyclotomic fields, not 'Iwasawa theory', and no first named textbook/title anchor is checked."),
    [person("Kenkichi Iwasawa", "originator", "1917–1998", "https://mathshistory.st-andrews.ac.uk/Biographies/Iwasawa/", [work("On the Theory of Cyclotomic Fields", 1959, "https://doi.org/10.2307/1970328", "Cyclotomic tower and class-group framework")])],
    "AMS survey confirms a late-1950s series, so 1959 is a checked anchor rather than a proven first: https://doi.org/10.1090/surv/280.")

add("P405", ["three-valued logic", "Łukasiewicz logic", "many-valued logic", "Post logic"],
    date(1920, "Łukasiewicz's O logice trójwartościowej was printed in Ruch Filozoficzny in 1920.", "Digitized original journal issue", "https://kpbc.umk.pl/Content/247342/PDF/EOD_OPEN_006_12_nr_09.pdf"),
    date(1920, "The publication develops a third truth value to address future contingents.", "Stanford Encyclopedia of Philosophy", "https://plato.stanford.edu/entries/lukasiewicz/", "history_page"),
    date(1920, "The article title names three-valued logic.", "Digitized original journal issue", "https://kpbc.umk.pl/Content/247342/PDF/EOD_OPEN_006_12_nr_09.pdf", note="This names three-valued logic, not necessarily the entire later family of many-valued logics."),
    [person("Jan Łukasiewicz", "originator", "1878–1956", "https://plato.stanford.edu/entries/lukasiewicz/", [work("O logice trójwartościowej", 1920, "https://kpbc.umk.pl/Content/247342/PDF/EOD_OPEN_006_12_nr_09.pdf", "First printed three-valued account")]), person("Emil Post", "developer", "1897–1954", "https://mathshistory.st-andrews.ac.uk/Biographies/Post/", [work("Introduction to a General Theory of Elementary Propositions", 1921, "https://doi.org/10.2307/2370324", "General finite-valued propositional systems")])],
    "Łukasiewicz's 1917 discovery and 1918 lecture are not the publication date; SEP identifies the 1920 print account.")

# Batch 3.
add("P006", ["Galois theory", "permutation groups", "resolvents", "abstract group theory"],
    date(1772, "The 1770-volume first sections of Lagrange's Réflexions were printed in 1772.", "EMS Press historical bibliography", "https://ems.press/content/book-chapter-files/20478?nt=1", "history_page", note="The academy volume is labelled 1770; its first part was printed in 1772 and continuation in 1773. A direct original-volume catalogue record is still needed."),
    date(1772, "Lagrange used permutations of roots to analyse solvability of polynomial equations.", "EMS Press historical analysis", "https://ems.press/content/book-chapter-files/20478?nt=1", "history_page"),
    date(1854, "Cayley's paper title names the theory of groups.", "Taylor & Francis original article record", "https://doi.org/10.1080/14786445408647421"),
    [person("Joseph-Louis Lagrange", "originator", "1736–1813", "https://mathshistory.st-andrews.ac.uk/Biographies/Lagrange/", [work("Oeuvres de Lagrange (collected edition including Réflexions)", 1867, "https://openlibrary.org/books/OL23322801M/Oeuvres.", "Bibliographic record of collected work; original 1772 print still needs a direct record")]), person("Arthur Cayley", "systematiser", "1821–1895", "https://mathshistory.st-andrews.ac.uk/Biographies/Cayley/", [work("On the theory of groups, as depending on the symbolic equation θⁿ=1", 1854, "https://doi.org/10.1080/14786445408647421", "Named abstract-group paper")])],
    "Do not confuse academy volume year 1770 with publication year 1772, or Galois's 1831 submitted memoir with its 1846 publication. The 1854 paper names groups but does not prove it is the first institutional anchor for the entire later field.")

add("P018", ["probabilistic method", "Erdős random construction", "random graphs"],
    date(1947, "Erdős's graph paper appeared in the Bulletin in 1947.", "AMS original article record", "https://doi.org/10.1090/S0002-9904-1947-08785-1"),
    date(1947, "The paper uses existence through a random graph argument for a combinatorial bound.", "AMS original article record", "https://doi.org/10.1090/S0002-9904-1947-08785-1"),
    date(note="Searched AMS 1947 record, Erdős–Rényi 1959, and Alon–Spencer textbook records; a 1992 first edition record for The Probabilistic Method has not been checked."),
    [person("Paul Erdős", "originator", "1913–1996", "https://mathshistory.st-andrews.ac.uk/Biographies/Erdos/", [work("Some remarks on the theory of graphs", 1947, "https://doi.org/10.1090/S0002-9904-1947-08785-1", "Random graph existence proof")])],
    "The method predates the literal phrase 'probabilistic method'; 1947 is a publication anchor for the named event, not a claim that all randomized combinatorics began then.")

add("P048", ["matroid Hodge theory", "log-concavity", "Bergman fan", "chromatic polynomial"],
    date(2012, "Huh's chromatic-polynomial and Huh–Katz matroid papers appeared in 2012.", "AMS original article record", "https://doi.org/10.1090/S0894-0347-2012-00731-0"),
    date(2012, "Huh and Katz apply geometric methods to log-concavity of matroid characteristic polynomials.", "Springer original article record", "https://doi.org/10.1007/s00208-011-0777-6"),
    date(note="Searched Huh 2012, Huh–Katz 2012, and Adiprasito–Huh–Katz 2018. The 2018 article title names Hodge theory for combinatorial geometries, but its status as the first such title is unverified."),
    [person("June Huh", "originator", "born 1983", "https://en.wikipedia.org/wiki/June_Huh", [work("Milnor numbers of projective hypersurfaces and the chromatic polynomial of graphs", 2012, "https://doi.org/10.1090/S0894-0347-2012-00731-0", "Chromatic log-concavity"), work("Hodge theory for combinatorial geometries", 2018, "https://doi.org/10.4007/annals.2018.188.2.1", "Full matroid Hodge theory")]), person("Eric Katz", "developer", None, "https://people.math.osu.edu/katz.60/", [work("Log-concavity of characteristic polynomials and the Bergman fan of matroids", 2012, "https://doi.org/10.1007/s00208-011-0777-6", "Geometric matroid application")])],
    "The 2018 Annals paper was received in 2015; neither date replaces the 2012 publications for the first checked conceptual/application stage.")

add("P447", ["hyperbolic geometry", "parallel postulate", "Bolyai–Lobachevsky geometry"],
    date(1829, "Lobachevsky's first account of non-Euclidean geometry appeared in the Kazan Messenger in 1829.", "MacTutor biography", "https://mathshistory.st-andrews.ac.uk/Biographies/Lobachevsky/", "history_page", note="First original bibliographic record not found in Crossref/Open Library; see Bolyai's independent publication dispute in disputedDates."),
    date(1829, "Lobachevsky's publication works through a geometry denying the parallel postulate.", "MacTutor history", "https://mathshistory.st-andrews.ac.uk/HistTopics/Non-Euclidean_geometry/", "history_page"),
    date(note="Searched Lobachevsky Kazan Messenger, Bolyai Appendix, and early non-Euclidean geometry histories; no checked earliest named textbook or chair distinct from original treatises."),
    [person("Nikolai Lobachevsky", "originator", "1792–1856", "https://mathshistory.st-andrews.ac.uk/Biographies/Lobachevsky/", [work("Geometrische Untersuchungen zur Theorie der Parallellinien", 1840, "https://openlibrary.org/works/OL38541616W/Geometrische_Untersuchungen_zur_Theorie_der_Parallellinien", "Later catalogued exposition; first 1829 account has history-source evidence only")]), person("János Bolyai", "originator", "1802–1860", "https://mathshistory.st-andrews.ac.uk/Biographies/Bolyai/", [work("Appendix to Tentamen", 1832, "https://openlibrary.org/works/OL17311426W/Tentamen_juventutem_studiosam_in_elementa_matheseos_purae_elementaris_ac_sublimioris_methodo_intuiti", "Independent published construction included in the 1832 edition")])],
    "Gauss's 1817 private correspondence is a precursor, not a published date. MacTutor says a Bolyai reprint was sent to Gauss by June 1831, while the Hungarian Academy dates the Tentamen edition to 1832; preserve both.")
D["P447"]["disputedDates"] = [
    {"year": 1831, "claim": "Bolyai's Appendix had been printed in time for a June 1831 reprint to Gauss.", "url": "https://mathshistory.st-andrews.ac.uk/Biographies/Bolyai/", "reason": "early separate printing or advance copy"},
    {"year": 1832, "claim": "The Hungarian Academy dates the Tentamen edition containing the Appendix to 1832.", "url": "https://mta200.hu/kincseink/bolyai-janos-appendix-106388", "reason": "bound-edition publication date"},
]

add("P300", ["Erdős discrepancy problem", "Polymath5", "multiplicative discrepancy"],
    date(2015, "Tao released the full proof as a public preprint on 17 September 2015.", "arXiv preprint record", "https://arxiv.org/abs/1509.05363", note="The conjecture itself is much older; this date marks the proof technique in the event summary."),
    date(2015, "The proof uses Polymath5 reductions and multiplicative-function methods to settle discrepancy.", "arXiv preprint record", "https://arxiv.org/abs/1509.05363"),
    date(note="Searched Tao's 2015 arXiv and 2016 Discrete Analysis records; the problem name predates this solution, and no first title use has been established."),
    [person("Terence Tao", "developer", "born 1975", "https://en.wikipedia.org/wiki/Terence_Tao", [work("The Erdős discrepancy problem", 2015, "https://arxiv.org/abs/1509.05363", "Proof using multiplicative functions")])],
    "2010 is associated with Polymath5's earlier work, not a verified public statement of Tao's final method. Journal version: https://doi.org/10.19086/da.609. The SAT c=2 result is separate: https://doi.org/10.1007/978-3-319-09284-3_17.")

add("P505", ["LLL algorithm", "lattice basis reduction", "Lenstra–Lenstra–Lovász algorithm"],
    date(1982, "Factoring polynomials with rational coefficients appeared in 1982.", "Springer original article record", "https://doi.org/10.1007/BF01457454"),
    date(1982, "The paper introduces lattice basis reduction to factor rational polynomials.", "Springer original article record", "https://doi.org/10.1007/BF01457454"),
    date(note="Searched the 1982 paper and Crossref for first named LLL textbook or paper title; the original title does not itself name lattice basis reduction."),
    [person("Arjen K. Lenstra", "originator", "born 1956", "https://en.wikipedia.org/wiki/Arjen_Lenstra", [work("Factoring polynomials with rational coefficients", 1982, "https://doi.org/10.1007/BF01457454", "Lattice-reduction algorithm")]), person("Hendrik W. Lenstra", "originator", "born 1949", "https://en.wikipedia.org/wiki/Hendrik_Lenstra", [work("Factoring polynomials with rational coefficients", 1982, "https://doi.org/10.1007/BF01457454", "Joint algorithm")]), person("László Lovász", "originator", "born 1948", "https://en.wikipedia.org/wiki/L%C3%A1szl%C3%B3_Lov%C3%A1sz", [work("Factoring polynomials with rational coefficients", 1982, "https://doi.org/10.1007/BF01457454", "Joint algorithm")])],
    "No earlier presentation date is substituted for the 1982 journal publication.")

add("P151", ["ordinary differential equations", "fluxional equations", "separation of variables", "Bernoulli equation"],
    date(1693, "Leibniz's Supplementum geometriae practicae was published in Acta Eruditorum in 1693.", "Museo Galileo bibliographic catalogue", "https://opac.museogalileo.it/imss/resource?dcnr=6&uri=177222&v=l", note="Newton's 1671 manuscript was not published until 1736; earlier published calculus applications may still predate 1693."),
    date(1693, "Leibniz's 1693 paper deliberately uses series to address transcendental problems.", "Museo Galileo bibliographic catalogue", "https://opac.museogalileo.it/imss/resource?dcnr=6&uri=177222&v=l"),
    date(note="Searched Newton's Methodus Fluxionum editions and Leibniz/Bernoulli Acta references; first named textbook/title of differential equations not checked."),
    [person("Gottfried Wilhelm Leibniz", "developer", "1646–1716", "https://mathshistory.st-andrews.ac.uk/Biographies/Leibniz/", [work("Supplementum geometriae practicae sese ad problemata transcendentia extendens ope nova methodi generalissima per series infinita", 1693, "https://opac.museogalileo.it/imss/resource?dcnr=6&uri=177222&v=l", "Published series method for transcendental problems")]), person("Isaac Newton", "originator", "1642–1727", "https://mathshistory.st-andrews.ac.uk/Biographies/Newton/", [work("The Method of Fluxions and Infinite Series", 1736, "https://openlibrary.org/books/OL7105241M/The_method_of_fluxions_and_infinite_series", "1671 manuscript finally published in 1736")])],
    "The original catalogue date 1671 is a manuscript date, not a public publication date. A historical discussion of the 1693 differential-equation use is at https://schoolbag.info/mathematics/history/35.html; 1693 is the first directly catalogued candidate found here, not proven global priority.")

add("P526", ["totally nonnegative Grassmannian", "positive Grassmannian", "permutation tableaux", "KP solitons"],
    date(2005, "Williams's paper on totally positive Grassmann cells was published in 2005.", "Elsevier original article record", "https://www.sciencedirect.com/science/article/pii/S0001870804000544", note="This is a checked Grassmannian-combinatorics anchor; Lusztig's 1994 flag-variety work is a precursor."),
    date(2006, "Corteel and Williams's public preprint connects Grassmannian-derived tableaux to exclusion-process probabilities.", "arXiv preprint record", "https://arxiv.org/abs/math/0602109", note="Kodama–Williams connected the same geometry to KP solitons in a 2011 public preprint."),
    date(note="Searched Williams 2005, Postnikov 2006, Corteel–Williams 2006 and Kodama–Williams 2011 titles; no single first institutional title naming this three-way hub."),
    [person("Lauren Williams", "developer", None, "https://math.berkeley.edu/~williams/", [work("Enumeration of totally positive Grassmann cells", 2005, "https://www.sciencedirect.com/science/article/pii/S0001870804000544", "Cell-counting combinatorics"), work("Tableaux combinatorics for the asymmetric exclusion process", 2006, "https://arxiv.org/abs/math/0602109", "Probability connection"), work("KP solitons and total positivity for the Grassmannian", 2011, "https://arxiv.org/abs/1106.0023", "Integrable-systems connection")]), person("Alexander Postnikov", "originator", None, "https://math.mit.edu/~apost/", [work("Total positivity, Grassmannians, and networks", 2006, "https://arxiv.org/abs/math/0609764", "Positive-Grassmannian network model")])],
    "The event merges connections made in 2005, 2006 and 2011. It cannot honestly have a single 1994 emergence for all three.")

add("P401", ["abstract field", "field extensions", "Steinitz field theory"],
    date(1910, "Steinitz's Algebraische Theorie der Körper appeared in 1910.", "De Gruyter original article record", "https://doi.org/10.1515/CRLL.1910.137.167"),
    date(1910, "The paper systematically studies abstract fields and extensions.", "De Gruyter original article record", "https://doi.org/10.1515/CRLL.1910.137.167"),
    date(note="Searched Steinitz 1910 and Weber 1893 field/Galois titles. Steinitz's title names algebraic field theory, but earlier institutional title use has not been ruled out."),
    [person("Ernst Steinitz", "systematiser", "1871–1928", "https://mathshistory.st-andrews.ac.uk/Biographies/Steinitz/", [work("Algebraische Theorie der Körper", 1910, "https://doi.org/10.1515/CRLL.1910.137.167", "Systematic abstract field theory")])],
    "Weber's 1893 abstract Galois framework is an earlier related publication (https://doi.org/10.1007/BF01446451); 1910 marks Steinitz's systematic treatment, not all field theory's birth.")

add("P019", ["categories", "functors", "natural transformations", "natural equivalences"],
    date(1945, "Eilenberg and Mac Lane's General theory of natural equivalences was published in 1945.", "AMS original article record", "https://doi.org/10.1090/S0002-9947-1945-0013131-6", note="Their 1942 paper addresses natural isomorphisms but does not yet give general category theory."),
    date(1945, "The paper introduces categories and functors to study natural equivalences.", "AMS original article record", "https://doi.org/10.1090/S0002-9947-1945-0013131-6"),
    date(note="Searched 1945 Eilenberg–Mac Lane and Mac Lane's 1971 Categories for the Working Mathematician. The 1971 book names the subject but has not been shown to be the first named textbook or title."),
    [person("Samuel Eilenberg", "originator", "1913–1998", "https://mathshistory.st-andrews.ac.uk/Biographies/Eilenberg/", [work("General theory of natural equivalences", 1945, "https://doi.org/10.1090/S0002-9947-1945-0013131-6", "Introduces category/functor framework")]), person("Saunders Mac Lane", "originator", "1909–2005", "https://mathshistory.st-andrews.ac.uk/Biographies/MacLane/", [work("General theory of natural equivalences", 1945, "https://doi.org/10.1090/S0002-9947-1945-0013131-6", "Joint founding paper"), work("Categories for the Working Mathematician", 1971, "https://doi.org/10.1007/978-1-4612-9839-7", "Named systematic textbook")])],
    "The 1942 Natural Isomorphisms in Group Theory article is a precursor: https://pubmed.ncbi.nlm.nih.gov/16588584/. Publication, not presentation, fixes the 1945 category date.")

D["P086"]["firstTermUse"] = {"term": "Hardness vs. randomness", "year": 1988, "url": "https://doi.org/10.1109/SFCS.1988.21916", "status": "earliest_checked_title; broader priority search pending"}
D["P405"]["firstTermUse"] = {"term": "O logice trójwartościowej (on three-valued logic)", "year": 1920, "url": "https://kpbc.umk.pl/Content/247342/PDF/EOD_OPEN_006_12_nr_09.pdf", "status": "earliest_checked_title; broader priority search pending"}
D["P533"]["firstTermUse"] = {"term": "Murmurations of elliptic curves", "year": 2022, "url": "https://arxiv.org/abs/2204.10140", "status": "earliest_checked_title; broader priority search pending"}


def main():
    assert len(D) == len(MANIFEST["events"]) == 30
    rows = []
    for meta in MANIFEST["events"]:
        row = {"pid": meta["pid"], "eventId": meta["eventId"], "canonicalName": meta["name"], **D[meta["pid"]]}
        rows.append(row)
    assert len({r["pid"] for r in rows}) == 30
    for row in rows:
        assert row["aliases"] and len(row["people"]) <= 6
        for field in ("conceptual", "methodological", "institutional"):
            d = row["dates"][field]
            if d["start"] is None:
                assert d["end"] is None and d["grade"] is None and d["note"]
            else:
                assert d["start"] == d["end"] and d["grade"] in ("B", "C") and d["evidence"]
                assert all(x["url"].startswith("https://") and x["claim"] for x in d["evidence"])
        for p in row["people"]:
            assert p["role"] in ("originator", "developer", "systematiser", "popularizer")
            assert p["biographyUrl"].startswith("https://") and 1 <= len(p["works"]) <= 3
            assert all(w["citation"] and w["url"].startswith("https://") for w in p["works"])
    output = {"method": "single direct research pass", "researchedAt": "2026-10-17", "gradePolicy": "B = one checked bibliographic record; C = history source only; A requires a second independent pass and is unavailable here", "events": rows}
    target = PILOT / "direct-research.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    counts = {field: {grade: sum(r["dates"][field]["grade"] == grade for r in rows) for grade in ("B", "C", None)} for field in ("conceptual", "methodological", "institutional")}
    n_people = sum(len(r["people"]) for r in rows)
    n_works = sum(len(p["works"]) for r in rows for p in r["people"])
    report = f"""# Direct research pilot: 30 field-emergence events

This is one source-led pass by Codex, replacing the interrupted Opus/Sonnet run at the user's request. It is **not** an independent two-pass comparison. Agreement rates and A grades are therefore unavailable. Date grades here mean B (a checked bibliographic/archival record) or C (history evidence only); blank means no date is displayed, with searches documented in the event record.

| Date | Evidenced / 30 | B | C | Blank |
| --- | ---: | ---: | ---: | ---: |
| Conceptual | {30-counts['conceptual'][None]} | {counts['conceptual']['B']} | {counts['conceptual']['C']} | {counts['conceptual'][None]} |
| Methodological | {30-counts['methodological'][None]} | {counts['methodological']['B']} | {counts['methodological']['C']} | {counts['methodological'][None]} |
| Institutional | {30-counts['institutional'][None]} | {counts['institutional']['B']} | {counts['institutional']['C']} | {counts['institutional'][None]} |

The ledger has {n_people} sourced person entries and {n_works} work links across 30 events, plus aliases and event-specific notes. These counts describe the **pilot only**; the remaining catalogue events have not been researched in this pass. A B grade confirms a matching record and date, not exhaustive proof that no earlier publication exists. Institutional dates are especially conservative for that reason.

Key corrections to the existing catalogue:

- **Langlands (P026):** 1967 is the private Weil letter; the first checked published account is 1970. The private date remains in the note.
- **Sheaf theory (P021):** the 1945 captivity-course paper is a precursor. Leray's first `faisceau` announcement was published in 1946; the 1945 text was checked for that term and did not contain it.
- **Non-Euclidean geometry (P447):** Gauss's 1817 work was private. Lobachevsky's 1829 publication gets C until a direct record is located; Bolyai's 1831 separate printing and 1832 bound edition are both retained with reasons.
- **Hardness versus randomness (P086):** the 1988 proceedings paper predates the 1994 journal article.
- **Cotes (P159):** `Logometria` was published in 1714; `Harmonia Mensurarum` is a later 1722 edition.
- **Ancient works (P134, P186, P119):** original publication years are not recoverable. Their proposed point dates are withheld rather than converted from a death date or archaeological estimate.

The main open research is the earliest *institutional* naming for {counts['institutional'][None]} events, followed by exact first-use priority for broad merged events and source records for the oldest works. The ledger keeps these gaps visible. A [pilot-only review page](../../../../public/field-emergence-pilot.html) displays the 30 researched records; the other 527 catalogue events are not presented as reviewed.
"""
    (PILOT / "direct-report.md").write_text(report)
    print(target)


if __name__ == "__main__":
    main()
