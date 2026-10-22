#!/usr/bin/env python3
"""Second source-led batch, kept separate from the fixed 30-event pilot."""

import json
from pathlib import Path

from build_direct_enrichment_pilot import date, person, work


ROOT = Path(__file__).resolve().parents[1]
CATALOG = {e["id"]: e for e in json.loads((ROOT / "data/collection/field-events-merged.json").read_text())["events"]}
OUT = ROOT / "data/collection/enrichment/batch-02-direct.json"


def b(year, claim, source, url, note=""):
    return date(year, claim, source, url, note=note)


def blank(note):
    return date(note=note)


ROWS = []


def add(event_id, aliases, conceptual, methodological, institutional, people, notes):
    ROWS.append({"eventId": event_id, "canonicalName": CATALOG[event_id]["name"], "aliases": aliases,
                 "dates": {"conceptual": conceptual, "methodological": methodological, "institutional": institutional},
                 "firstTermUse": None, "people": people, "notes": notes})


add("E25", ["minimax theorem", "strategic games", "Nash equilibrium"],
    b(1928, "Von Neumann's article gives the minimax theorem for strategic games.", "Mathematische Annalen record", "https://doi.org/10.1007/BF01448847"),
    b(1928, "The article applies minimax to two-person zero-sum games.", "Mathematische Annalen record", "https://doi.org/10.1007/BF01448847"),
    b(1944, "Theory of Games and Economic Behavior is a named field monograph.", "Open Library first-edition record", "https://openlibrary.org/books/OL186826M/Theory_of_Games_and_Economic_Behavior"),
    [person("John von Neumann", "originator", "1903–1957", "https://mathshistory.st-andrews.ac.uk/Biographies/Von_Neumann/", [work("Zur Theorie der Gesellschaftsspiele", 1928, "https://doi.org/10.1007/BF01448847", "Minimax framework")]),
     person("John Nash", "developer", "1928–2015", "https://mathshistory.st-andrews.ac.uk/Biographies/Nash/", [work("Equilibrium points in n-person games", 1950, "https://doi.org/10.1073/pnas.36.1.48", "Extends equilibrium beyond zero-sum games")])],
    "Borel's earlier game papers are priority precursors, not erased by the 1928 minimax anchor. Nash's 1950 contribution is a later generalization. The 1944 textbook is an institutional anchor, not the origin date.")

add("E30", ["schemes", "Spec of a ring", "Éléments de géométrie algébrique"],
    blank("Searched EGA I (1960), the 1958 ICM programme, and Grothendieck's Bourbaki seminars. An earlier publicly published scheme definition has not been isolated."),
    b(1960, "EGA I develops schemes as a working tool for algebraic geometry.", "Numdam original article record", "https://numdam.org/item/PMIHES_1960__4__5_0/"),
    b(1960, "EGA I is a named systematic treatise subtitled Le langage des schémas.", "Numdam original article record", "https://numdam.org/item/PMIHES_1960__4__5_0/"),
    [person("Alexander Grothendieck", "originator", "1928–2014", "https://mathshistory.st-andrews.ac.uk/Biographies/Grothendieck/", [work("Éléments de géométrie algébrique I: Le langage des schémas", 1960, "https://numdam.org/item/PMIHES_1960__4__5_0/", "Systematic scheme language")])],
    "1960 is the first checked systematic publication, not a claim that no earlier public scheme definition exists. Dieudonné's editorial collaboration is recorded in EGA's publication history, but a separate event-specific work record for him has not been checked here.")

add("E32", ["Hilbert's tenth problem", "DPRM theorem", "Diophantine undecidability"],
    b(1970, "Matiyasevich published the result that enumerable sets are Diophantine.", "Math-Net.Ru original article record", "https://www.mathnet.ru/dan35274"),
    b(1970, "The result completes the Diophantine representation needed for the negative solution.", "Math-Net.Ru original article record", "https://www.mathnet.ru/dan35274", note="Davis, Putnam, and Robinson's 1961 exponential-Diophantine reduction is a necessary precursor."),
    blank("Searched Math-Net.Ru and Annals records for the 1961/1970 papers. Neither is a first named textbook, journal, lecture series, or classification anchor for this bridge."),
    [person("Yuri Matiyasevich", "originator", "born 1947", "https://mathshistory.st-andrews.ac.uk/Biographies/Matiyasevich/", [work("The Diophantineness of enumerable sets", 1970, "https://www.mathnet.ru/dan35274", "Completes the unsolvability proof")]),
     person("Julia Robinson", "developer", "1919–1985", "https://mathshistory.st-andrews.ac.uk/Biographies/Robinson_Julia/", [work("The decision problem for exponential Diophantine equations", 1961, "https://doi.org/10.2307/1970289", "Joint precursor with Davis and Putnam")])],
    "The 1961 Davis–Putnam–Robinson paper is retained as a precursor; it did not yet settle Hilbert's tenth problem. The original 1970 Russian article, rather than a later English translation, dates the completed result.")

add("E33", ["index theorem", "elliptic operator index", "topological index"],
    b(1963, "Atiyah and Singer announced the index theorem for elliptic operators on compact manifolds.", "AMS original article record", "https://doi.org/10.1090/S0002-9904-1963-10957-X"),
    b(1963, "The published note computes an analytic index from topological data.", "AMS original article record", "https://doi.org/10.1090/S0002-9904-1963-10957-X"),
    blank("Searched the AMS 1963 announcement and Annals 1968 proof series; neither establishes the first textbook, named lecture series, or field classification."),
    [person("Michael Atiyah", "originator", "1929–2019", "https://mathshistory.st-andrews.ac.uk/Biographies/Atiyah/", [work("The index of elliptic operators on compact manifolds", 1963, "https://doi.org/10.1090/S0002-9904-1963-10957-X", "Published theorem announcement")]),
     person("Isadore Singer", "originator", "1924–2021", "https://mathshistory.st-andrews.ac.uk/Biographies/Singer/", [work("The index of elliptic operators. I", 1968, "https://doi.org/10.2307/1970715", "Full proof series")])],
    "The 1963 announcement is public; the detailed Annals proof appeared in 1968. Gelfand's 1960 problem statement is a precursor, not the theorem's public proof.")

add("E36", ["topological combinatorics", "Kneser graphs", "neighborhood complex"],
    b(1978, "Lovász published a homotopy-theoretic solution of Kneser's conjecture.", "Elsevier original article record", "https://doi.org/10.1016/0097-3165(78)90022-5"),
    b(1978, "The paper uses graph-neighborhood topology to prove a chromatic-number bound.", "Elsevier original article record", "https://doi.org/10.1016/0097-3165(78)90022-5"),
    blank("Searched the 1978 Lovász record and later topological-combinatorics book references; earliest named institutional anchor not verified."),
    [person("László Lovász", "originator", "born 1948", "https://mathshistory.st-andrews.ac.uk/Biographies/Lovasz/", [work("Kneser's conjecture, chromatic number, and homotopy", 1978, "https://doi.org/10.1016/0097-3165(78)90022-5", "Topological proof of the graph-coloring conjecture")])],
    "Kneser formulated the conjecture in 1955; the topological transfer in this event is the 1978 published proof.")

add("E42", ["Jones polynomial", "knot invariant from operator algebras", "braid representations"],
    b(1985, "Jones published a polynomial knot invariant derived from von Neumann algebras.", "AMS original article record", "https://doi.org/10.1090/S0273-0979-1985-15304-2"),
    b(1985, "The paper uses operator-algebra and braid constructions to distinguish knots.", "AMS original article record", "https://doi.org/10.1090/S0273-0979-1985-15304-2"),
    blank("Searched the 1985 AMS paper and 1987 follow-up; the first named textbook or classification for this cross-field connection is not verified."),
    [person("Vaughan Jones", "originator", "1952–2020", "https://en.wikipedia.org/wiki/Vaughan_Jones", [work("A polynomial invariant for knots via von Neumann algebras", 1985, "https://doi.org/10.1090/S0273-0979-1985-15304-2", "Original knot polynomial from operator algebras")])],
    "Jones's 1984 discovery predates the January 1985 publication; the date field follows the public paper. Witten's 1989 field-theoretic interpretation is a later development, not the origin.")

add("E49", ["SLE", "stochastic Loewner evolution", "Schramm–Loewner evolution"],
    b(1999, "Schramm's public preprint describes Brownian-driven Loewner scaling limits.", "arXiv preprint record", "https://arxiv.org/abs/math/9904022", note="The journal version appeared in 2000."),
    b(1999, "The preprint applies the construction to loop-erased random walk and uniform spanning trees.", "arXiv preprint record", "https://arxiv.org/abs/math/9904022"),
    blank("Searched the 1999 arXiv and 2000 Israel Journal record; earliest explicitly named SLE textbook or section not checked."),
    [person("Oded Schramm", "originator", "1961–2008", "https://en.wikipedia.org/wiki/Oded_Schramm", [work("Scaling limits of loop-erased random walks and uniform spanning trees", 2000, "https://doi.org/10.1007/BF02803524", "Published journal form of the 1999 SLE preprint")])],
    "This entry treats an arXiv posting as a public bibliographic preprint. If the catalogue requires peer-reviewed publication only, use the 2000 journal date instead; both dates and the reason are preserved here.")

add("E50", ["Green–Tao theorem", "arithmetic progressions in primes", "relative Szemerédi theorem"],
    b(2004, "Green and Tao publicly posted the theorem that primes contain arbitrarily long progressions.", "arXiv preprint record", "https://arxiv.org/abs/math/0404188", note="The journal article appeared in 2008."),
    b(2004, "The preprint applies a transference principle and sieve majorant to the primes.", "arXiv preprint record", "https://arxiv.org/abs/math/0404188"),
    blank("Searched the 2004 arXiv and 2008 Annals records; no first named textbook, lecture series, or classification for this particular bridge established."),
    [person("Ben Green", "originator", "born 1977", "https://en.wikipedia.org/wiki/Ben_Green_(mathematician)", [work("The primes contain arbitrarily long arithmetic progressions", 2008, "https://doi.org/10.4007/annals.2008.167.481", "Published theorem proof")]),
     person("Terence Tao", "originator", "born 1975", "https://mathshistory.st-andrews.ac.uk/Biographies/Tao/", [work("The primes contain arbitrarily long arithmetic progressions", 2008, "https://doi.org/10.4007/annals.2008.167.481", "Transference and sieve proof")])],
    "The public 2004 preprint, not the 2008 journal publication, is used for first public statement; the later journal work remains linked for both authors.")

add("E51", ["polynomial method", "finite-field Kakeya", "polynomial partitioning"],
    blank("Searched Dvir's 2008 Kakeya preprint and Guth–Katz's 2010 distances preprint. The broad polynomial method predates these breakthroughs; an earliest public general formulation is not established."),
    b(2008, "Dvir's preprint applies low-degree polynomials to the finite-field Kakeya problem.", "arXiv preprint record", "https://arxiv.org/abs/0803.2336", note="Guth and Katz apply polynomial partitioning to distinct distances in a separate 2010 public preprint, journal 2015."),
    blank("Searched the Dvir 2009 and Guth–Katz 2015 journal records; earliest named field textbook or title-use anchor not verified."),
    [person("Zeev Dvir", "developer", None, "https://www.cs.princeton.edu/~zdvir/", [work("On the size of Kakeya sets in finite fields", 2009, "https://doi.org/10.1090/S0894-0347-08-00607-3", "Polynomial proof of finite-field Kakeya")]),
     person("Larry Guth", "developer", None, "https://en.wikipedia.org/wiki/Larry_Guth", [work("On the Erdős distinct distances problem in the plane", 2015, "https://doi.org/10.4007/annals.2015.181.1.2", "Polynomial partitioning for distance bounds")])],
    "These are two different targets under a broad catalogue label. Their public preprint years are 2008 and 2010 respectively; neither should be promoted to the origin of the entire polynomial method. Birth years were not verified in the consulted biographies and are left blank.")

add("E52", ["sum-product and expansion", "SL2 expander graphs", "growth in finite groups"],
    b(2008, "Bourgain and Gamburd published expansion bounds for Cayley graphs of SL2(Fp).", "Annals original article record", "https://doi.org/10.4007/annals.2008.167.625", note="The article was received in 2005 and appeared in the 2008 journal volume; a prior public preprint date needs checking."),
    b(2008, "The article deliberately combines finite-field growth estimates with spectral expansion.", "Annals original article record", "https://doi.org/10.4007/annals.2008.167.625"),
    blank("Searched the 2004 sum-product and 2008 Annals expansion records; no first named textbook, journal, lecture series, or classification for the bridge established."),
    [person("Jean Bourgain", "originator", "1954–2018", "https://mathshistory.st-andrews.ac.uk/Biographies/Bourgain/", [work("Uniform expansion bounds for Cayley graphs of SL2(Fp)", 2008, "https://doi.org/10.4007/annals.2008.167.625", "Expansion theorem")]),
     person("Alex Gamburd", "developer", None, "https://en.wikipedia.org/wiki/Alexander_Gamburd", [work("Uniform expansion bounds for Cayley graphs of SL2(Fp)", 2008, "https://doi.org/10.4007/annals.2008.167.625", "Coauthor of expansion theorem")])],
    "Bourgain–Katz–Tao's 2003 public sum-product preprint (https://arxiv.org/abs/math/0301343) is a tool precursor, not yet this group-expansion result. Helfgott's 2008 group-growth paper (https://doi.org/10.4007/annals.2008.167.601) is another precursor. Gamburd's birth year was not verified and is blank.")


def main():
    assert len(ROWS) == len({r["eventId"] for r in ROWS}) == 10
    pilot_ids = {r["eventId"] for r in json.loads((ROOT / "data/collection/enrichment/pilot/direct-research.json").read_text())["events"]}
    assert not pilot_ids.intersection(r["eventId"] for r in ROWS)
    for row in ROWS:
        assert row["eventId"] in CATALOG and row["aliases"] and len(row["people"]) <= 6
        for d in row["dates"].values():
            assert (d["start"] is None and d["note"] and not d["evidence"]) or (d["start"] is not None and d["grade"] == "B" and d["evidence"])
        for p in row["people"]:
            assert p["role"] in ("originator", "developer", "systematiser", "popularizer") and 1 <= len(p["works"]) <= 3
    OUT.write_text(json.dumps({"method": "single direct research pass", "researchedAt": "2026-10-17", "events": ROWS}, ensure_ascii=False, indent=2) + "\n")
    coverage = {field: sum(r["dates"][field]["start"] is not None for r in ROWS) for field in ("conceptual", "methodological", "institutional")}
    (OUT.parent / "batch-02-report.md").write_text(f"# Direct enrichment batch 2\n\nTen additional, non-pilot events were researched in one source-led pass. Coverage: conceptual {coverage['conceptual']}/10, methodological {coverage['methodological']}/10, institutional {coverage['institutional']}/10. The 30-event pilot figures remain separate. Public preprints are treated as public bibliographic records; journal dates are retained in notes where they differ. No independent agreement or A grade is claimed.\n\nE30 and E51 conceptual dates remain empty because the first public statement of those broad ideas was not established. E51 and E52 also retain missing living-person birth years rather than guessing. No batch-2 data is merged into the unverified 557-event catalogue.\n")
    print(OUT)


if __name__ == "__main__":
    main()
