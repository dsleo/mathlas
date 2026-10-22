"""Apply reviewed publication links to the field map's priority evidence queue.

The URLs below point to a source publication, publisher record, institutional
archive, or an author's publication list. Keep each claim narrow enough to be
supported by that page; this pass verifies publication dates, not priority.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCEFIRST = ROOT / "data/collection/enrichment/sourcefirst/merged"
PILOT = ROOT / "data/collection/enrichment/pilot"


REPLACEMENTS = {
    "P021": ("Leray publishes the sheaf idea", "Leray's 1946 published note defines a faisceau and applies it to homology.", "Leray, Comptes rendus 222 (1946), digitized note", "https://ncatlab.org/nlab/files/Leray-0.pdf", "primary_text"),
    "P032": ("Differential geometry on C*-algebras", "Connes's C*-algèbres et géométrie différentielle is dated 1980 in the IHES archive.", "IHES archives, Connes M/80/04", "https://archives.ihes.fr/document/M_80_04.pdf", "primary_text"),
    "P054": ("Eilenberg and Mac Lane define homology of groups through extensions", "Group Extensions and Homology appears in Annals of Mathematics 43 (1942), pp. 757–831.", "Annals of Mathematics/JSTOR article record", "https://www.jstor.org/stable/1968966", "bibliographic_record"),
    "P076": ("Conformal dynamical systems", "Sullivan lists Conformal Dynamical Systems in Geometric Dynamics, LNM 1007 (1983), pp. 725–752.", "Dennis Sullivan, publications list", "https://www.math.stonybrook.edu/~dennis/publications/", "author_bibliography"),
    "P209": ("Dantzig's public statement of the simplex method", "The 1951 Cowles volume lists Dantzig's chapter on maximization at pp. 339–347 and a separate simplex-method application chapter.", "Cowles Foundation, Activity Analysis contents", "https://cowles.yale.edu/research/cfm-13-activity-analysis-production-and-allocation", "publisher_record"),
    "P232": ("Chomsky and Miller, Finite state languages", "The article appeared in Information and Control 1(2), May 1958, pp. 91–112.", "Elsevier, Information and Control article", "https://www.sciencedirect.com/science/article/pii/S0019995858900822", "publisher_record"),
    "P267": ("Von Neumann's self-reproducing automaton in a cellular space", "The edited Theory of Self-Reproducing Automata was published by University of Illinois Press in 1966.", "National Diet Library catalogue", "https://ndlsearch.ndl.go.jp/books/R100000002-I000006369183", "library_catalogue"),
    "P273": ("Frey's link between elliptic curves and Diophantine equations", "The university library catalogue records Frey's 40-page Links between stable elliptic curves and certain diophantine equations in 1986.", "Karlsruhe Institute of Technology library", "https://katalog.bibliothek.kit.edu/bib/591708", "library_catalogue"),
    "P361": ("Riesz's geometry of function spaces", "The historical bibliography identifies Riesz's paper in Comptes rendus 144 (1907), pp. 1409–1411.", "Revue d'histoire des mathématiques, Numdam", "https://numdam.org/articles/10.24033/rhm.57/", "historical_bibliography"),
    "P363": ("Abstract distance applied to functionals and compactness in function spaces", "Fréchet's Sur quelques points du calcul fonctionnel appeared in Rendiconti del Circolo Matematico di Palermo 22 (1906), pp. 1–72.", "Springer, Fréchet original article", "https://link.springer.com/article/10.1007/BF03018603", "publisher_record"),
    "P369": ("Markov's statistical study of Eugene Onegin", "The original Onegin statistical study appeared in the Imperial Academy bulletin 7(3) (1913), pp. 153–162.", "Math-Net.Ru digitized original", "https://www.mathnet.ru/eng/im6612", "primary_text"),
    "P384": ("Representations of finite groups by linear substitutions", "ETH's archive digitizes Frobenius's original paper; the AMS historical account dates the representation-theory development to 1897.", "ETH Library digitization and AMS history", "https://www.e-rara.ch/doi/10.3931/e-rara-18879", "primary_text"),
    "P400": ("Russell's paradox in The Principles of Mathematics", "The 1903 original text discusses the contradiction in Chapter X.", "Russell, The Principles of Mathematics, digitized text", "https://people.umass.edu/klement/pom/pom.html", "primary_text"),
    "P441": ("Fatou's note on rational substitutions", "Fatou's bibliography records Sur les substitutions rationnelles in Comptes rendus, 1917.", "Michèle Audin, University of Strasbourg, Fatou bibliography", "https://audin.pages.math.unistra.fr/histoire/biblioFatou.pdf", "historical_bibliography"),
    "P451": ("Riesz on continuity and abstract set theory", "Riesz's contribution appears in the printed proceedings of the 1908 Rome congress, issued in 1909.", "International Mathematical Union, ICM 1908 proceedings", "https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1908.2/ICM1908.2.ocr.pdf", "primary_text"),
    "P540": ("Multiplicative chaos", "The journal's own table of contents records Kahane's Sur le chaos multiplicatif in volume 9(2), December 1985, pp. 105–150.", "Annales des sciences mathématiques du Québec", "https://www.labmath.uqam.ca/~annales/english/volumes/09-2.html", "publisher_record"),
}


def update_row(row):
    replacement = REPLACEMENTS.get(row.get("pid"))
    if replacement:
        label, claim, source, url, kind = replacement
        matches = [m for m in row.get("milestones", []) if m.get("label") == label]
        if len(matches) != 1:
            raise ValueError(f"Expected one milestone for {row['pid']}: {label}")
        schema_kind = kind if kind in {"bibliographic_record", "history_page", "primary_text"} else "bibliographic_record"
        matches[0]["evidence"] = [{"claim": claim, "source": source, "url": url, "kind": schema_kind}]
    if row.get("pid") == "P537":
        for milestone in row["milestones"]:
            if milestone["year"] == 1984 and milestone["label"] == "Cohen-Lenstra heuristics on class groups":
                milestone["role"] = "precursor"
                milestone["evidence"] = [{"claim": "Cohen and Lenstra's class-group heuristics appeared in 1984; this predates the Sawin–Wood moment theorem.", "source": "Cohen and Lenstra, Springer chapter DOI", "url": "https://doi.org/10.1007/BFb0099440", "kind": "bibliographic_record"}]
            elif milestone["year"] == 2019:
                milestone["role"] = "precursor"
            elif milestone["year"] == 2022:
                milestone["role"] = "first_statement"
                milestone["evidence"] = [{"claim": "Sawin and Wood state the moment problem and their general existence and uniqueness theorem in the 2022 preprint.", "source": "Sawin and Wood, original paper", "url": "https://arxiv.org/abs/2210.06279", "kind": "primary_text"}]
        note = "The 1984 Cohen–Lenstra heuristics are a precursor; the Sawin–Wood moment theorem was first stated in 2022."
        if note not in (row.get("notes") or ""):
            row["notes"] = (row.get("notes") or "").rstrip() + " " + note


def main():
    found = set()
    for path in sorted(SOURCEFIRST.glob("M_*.json")) + sorted(PILOT.glob("milestones*.json")):
        rows = json.loads(path.read_text())
        selected = [row for row in rows if row.get("pid") in REPLACEMENTS or row.get("pid") == "P537"]
        if not selected:
            continue
        for row in selected:
            if row["pid"] in found:
                raise ValueError(f"Duplicate curated record: {row['pid']}")
            found.add(row["pid"])
            update_row(row)
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n")
    expected = set(REPLACEMENTS) | {"P537"}
    if found != expected:
        raise ValueError(f"Missing curated records: {sorted(expected - found)}")
    print(f"Updated {len(found)} priority milestone records")


if __name__ == "__main__":
    main()
