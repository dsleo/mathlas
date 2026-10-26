# Independent re-check of the 24 "fixed" cross-check rows (2026-10-26)

Scope: the `fixed` rows of `ADJUDICATION.md` and the matching changes to `data/events.json` in commits 4632aaf and e19ddf9 (compared against c474a1e). Nothing in `data/events.json` or any generated file was edited. This note only reports.

Method: each cited work was re-looked up from scratch (Crossref API for DOIs, arXiv, J-STAGE, CiNii, Internet Archive scans and catalogue metadata, MacTutor, Euler Archive, Wikipedia as a secondary check). Role and confidence were judged against `MILESTONE_SCHEMA.md` (publication year governs, private or unpublished work is a precursor, a milestone needs a source). Derived dates were recomputed from the milestone list by the schema rule for all 22 events involved; they all match the stored `derived` and `shown` values. Link distances were checked for P250 (E25 = 1928, d = -2 became -7, E25 side +7) and P004 (all six distances dropped by exactly 5). Milestone lists are in year order for every edited event.

Note: `ADJUDICATION.md` is not in this worktree's checkout (it lives on later commits, read from fe2501a).

## Summary table

Verdicts: confirmed / wrong (what is right) / uncertain. Row numbers refer to `ADJUDICATION.md`.

| # | pid | Milestone (as recorded) | Verdict | Evidence checked | Proposed JSON edit |
|---|-----|-------------------------|---------|------------------|--------------------|
| 1 | P012 | 1868 precursor, Gordan finiteness for binary forms | confirmed. Crelle 69 (1868), pp. 323-354, DOI title matches; precursor is right (a finite-basis result for invariants, not the public start of commutative algebra). | https://api.crossref.org/works/10.1515/crll.1868.69.323 | none |
| 2 | P052 | 1974 key_development, Knuth, Computer Science and its Relation to Mathematics | confirmed. AMM 81(4), April 1974, pp. 323-343. key_development rather than consolidation is correct for an essay. | https://api.crossref.org/works/10.1080/00029890.1974.11993556 | none |
| 3 | P055 | 1961 key_development, Atiyah-Hirzebruch, Vector bundles and homogeneous spaces | confirmed. Proc. Sympos. Pure Math. 3, AMS, 1961, pp. 7-38 (Crossref has no volume field; the volume is the series number 3 in the DOI path pspum/003). | https://api.crossref.org/works/10.1090/pspum/003/0139181 | none |
| 4 | P058 | 2021 key_development, Fargues-Scholze | confirmed with a caveat. arXiv:2102.13459, v1 26 Feb 2021 (now v4, Nov 2024); abstract says it develops "the geometric Langlands program on the Fargues-Fontaine curve", which supports filing it under geometric Langlands. Preprint year is disclosed in the note; medium confidence is right. | https://arxiv.org/abs/2102.13459 | none |
| 5 | P063 | 2017 key_development, formal proof of Kepler | confirmed. Forum Math. Pi 5 (2017), online 29 May 2017, e2; authors Hales et al. | https://api.crossref.org/works/10.1017/fmp.2017.1 | none |
| 6 | P095 | 1974 first_application, Shelah on Whitehead; 1980 kept as key_development | confirmed. Israel J. Math. 18(3), Sept 1974, pp. 243-256; the 1980 paper is Israel J. Math. 35(4), pp. 257-285 ("Whitehead groups may not be free even assuming CH, II"), DOI bf02760652 matches. Derived methodological date 1980 to 1974 is consistent (earliest first_application). The 1974 paper is the standard citation for the independence result (V=L implies Whitehead groups free; MA + not-CH gives a non-free one; stated from standard accounts, the paper text was not read here); the record's medium confidence and the caveat that forcing was not read in the text are appropriate. | https://api.crossref.org/works/10.1007/bf02757281 ; https://api.crossref.org/works/10.1007/bf02760652 | none |
| 7 | P200 | 1931 precursor, Goedel's incompleteness paper | confirmed. Monatsh. Math. Phys. 38, pp. 173-198, issued Dec 1931. Precursor is defensible: it defines primitive recursive functions but is not the Church-Turing statement the event is about. | https://api.crossref.org/works/10.1007/bf01700692 | none |
| 8 | P285 | 1981 consolidation, Smale handbook survey | confirmed. Chapter 8, Handbook of Mathematical Economics vol. 1, North-Holland, 1981, pp. 331-370. A survey chapter is a consolidation under the schema; derived institutional date stays 1973 (naming comes first). | https://api.crossref.org/works/10.1016/s1573-4382(81)01012-6 | none |
| 9 | P354 into P004 | 1930 key_development, Kuratowski | confirmed. Fund. Math. 15 (1930), pp. 271-283, "Sur le probleme des courbes gauches en Topologie". | https://api.crossref.org/works/10.4064/fm-15-1-271-283 | none |
| 9b | P004 | merge of the 1736 and 1741 Euler first statements into one 1741 first_statement; map and conceptual date 1736 to 1741 | confirmed. Euler Archive E53: Commentarii Acad. Sci. Petropolitanae 8, pp. 128-140, "Published Date 1741, Written Date 1735". Publication year governs, the 1735 precursor remains, derived conceptual 1741, and the six link distances were reduced by exactly 5 (e.g. P181 1845 - 1741 = 104). Wikipedia and MacTutor "1736" is the volume title and presentation date. | https://scholarlycommons.pacific.edu/euler-works/53/ | none |
| 12 | P449 | precursor, Brunelleschi perspective, 1413-1425 range | confirmed. MacTutor gives about 1413; Wikipedia (Brunelleschi, Perspective) says experiments 1415-1420, demonstration about 1420, and application "around 1425". No primary source; a range with a precursor role and medium confidence is right. (The record's note attributes 1425 to Wikipedia and about 1420 to Smarthistory; the Smarthistory page returned 403 here, but the Wikipedia perspective article gives both 1420 and 1425, so the note's spread holds.) | https://mathshistory.st-andrews.ac.uk/HistTopics/Art/ ; https://en.wikipedia.org/wiki/Perspective_(graphical) | none |
| 17 | P118 | 1731 precursor, Clairaut on double-curvature curves | confirmed. MacTutor: research on double-curvature curves completed 1729, and its page links the title page "Recherches sur les courbes a double courbure (1731)". Dating by publication (1731) with the 1729 completion in the label note is right. | https://mathshistory.st-andrews.ac.uk/Biographies/Clairaut/ | none |
| 18 | P118 | 1784 key_development, Monge, memoire sur les deblais et remblais | wrong in two places (details in the Monge section below): the print year 1784 is correct and now settled from the volume's own title page, so confidence should be raised from low; and the cited BnF bibliography does not mention curvature at all, so the evidence claim "notes it establishes the curves of curvature" is unsupported by the URL given. | https://archive.org/details/histoiredelacad81hist ; https://www.bnf.fr/sites/default/files/2019-12/Des%20tas%20de%20sables%20aux%20pixels_bibliographie.pdf ; https://en.wikipedia.org/wiki/Gaspard_Monge | see "Edit A" |
| 20 | P129 | 1530-1550 range key_development, Yuktibhasa | confirmed. Wikipedia: composed about 1530; MacTutor Jyesthadeva: written 1501 in one place and about 1550 in another; MacTutor Madhava: about 1550 (the cited page does say this). Range with medium confidence is right. Derived methodological stays null because the schema counts only first_application; the `shown` fallback 1550 to 1530 uses the range start and is consistent. Optional tidy-up: the note says "MacTutor's Jyesthadeva biography" while the evidence cites the Madhava page; either add the Jyesthadeva URL or reword (no change of date). | https://en.wikipedia.org/wiki/Yuktibh%C4%81%E1%B9%A3%C4%81 ; https://mathshistory.st-andrews.ac.uk/Biographies/Jyesthadeva/ ; https://mathshistory.st-andrews.ac.uk/Biographies/Madhava/ | none required (optional ev addition, see "Edit C") |
| 21 | P132 | 1823 key_development, Gauss Theoria combinationis, low confidence | confirmed on the year, but the two open points are settled and the confidence and note should be updated (details in the Gauss section below): print year 1823; the minimum-variance (optimality) theorem is in Pars prior, arts. 19-21, not Pars posterior. | https://archive.org/details/bub_gb_ZQ8OAAAAQAAJ ; https://archive.org/details/werke00gausgoog ; https://gtfp.cs.rhul.ac.uk/pulskamp/Gauss/Gauss.html | see "Edit B" |
| 22 | P135 | 1811-1815 range key_development, revised second edition | confirmed. Internet Archive metadata for vol. 1: "Paris, Ve Courcier", date 1811; Wikipedia: enlarged second edition of vol. 1 in 1811, vol. 2 revised by Lagrange but published posthumously 1815. Methodological fallback 1834 to 1811 is consistent (earliest key_development). (Publisher is "Ve Courcier", i.e. widow Courcier; the record writes "Courcier". Cosmetic.) | https://archive.org/metadata/mcaniqueanalyt01lagr ; https://en.wikipedia.org/wiki/M%C3%A9canique_analytique | none |
| 27 | P185 | 1738 key_development, De Moivre normal approximation | confirmed. Latin pamphlet "Approximatio ad summam terminorum binomii (a+b)^n in seriem expansi", 12 Nov 1733, privately circulated, 7 pages; English version in The Doctrine of Chances, 2nd ed., London (Woodfall), 1738, pp. 235-243. Dating by the 1738 publication is consistent with the schema (the 1733 pamphlet is private). | https://en.wikipedia.org/wiki/Abraham_de_Moivre | none |
| 30 | P234 | 1943 key_development, On rings of operators IV | confirmed. Ann. Math. 44(4), Oct 1943, pp. 716-808. | https://api.crossref.org/works/10.2307/1969107 | none |
| 31 | P250 | 1935 first_statement, Sprague (map year 1930 to 1935, confidence low to medium) | confirmed, with a caveat. J-STAGE: Tohoku Math. J. (1st ser.) 41, pp. 438-444, "Published: 1935" (volume 41 listed as 1935). Wikipedia and the JFM/Zbl references cite it as 1936, which is the review year or the 1935-36 volume span; the publisher's own record says 1935, so 1935 stands. The map year and the E25 link distance change are arithmetically consistent (E25 = 1928, so -2 becomes -7 and the reverse link +7). The catalogue seed range for this event already started at 1935. | https://www.jstage.jst.go.jp/article/tmj1911/41/0/41_0_438/_article | none |
| 32 | P250 | Grundy 1939 folded into the Sprague milestone as an independent rediscovery | confirmed. Eureka 2 (1939), pp. 6-8 (Wikipedia reference; reprinted Eureka 27, 1964, pp. 9-11). Only secondary sources, as the note already says. | https://en.wikipedia.org/wiki/Sprague%E2%80%93Grundy_theorem | none |
| 33 | P253 | 1975 key_development, Collins CAD | confirmed. LNCS 33, Springer, 1975, pp. 134-183 (2nd GI Conference, Kaiserslautern, May 1975). | https://api.crossref.org/works/10.1007/3-540-07407-4_17 | none |
| 34 | P260 | 1975 precursor, Kasparov K-homology | confirmed. Math. USSR Izv. 9(4), 1975, pp. 751-792, "Topological invariants of elliptic operators. I: K-homology". Precursor (not first_statement) is right since the bivariant KK-groups appear in 1979-1980. | https://api.crossref.org/works/10.1070/im1975v009n04abeh001497 | none |
| 35 | P267 | 1949 precursor, von Neumann Illinois lectures | confirmed. Burks' editor's introduction: "Five lectures delivered at the University of Illinois in December, 1949"; published only as Part I of the 1966 book. Precursor is right (unpublished lectures). | https://archive.org/details/theoryofselfrepr00vonn_0 | none |
| 36 | P272 | 1983 key_development, Getzler | confirmed. Comm. Math. Phys. 92(2), June 1983, pp. 163-178. | https://api.crossref.org/works/10.1007/bf01210843 | none |
| 37 | P370 | 1928 key_development, Hilbert-Ackermann, low confidence | confirmed. CiNii: "Grundzuge der theoretischen Logik", Springer, datePublished 1928, with bibliography and index. Low confidence is right because relevance to the programme is from secondary accounts; key_development rather than consolidation is the safer role. | https://ci.nii.ac.jp/ncid/BA01700588?l=en | none |

Count: 25 items checked (24 fixed rows, plus the P004 merge counted separately as 9b). 22 confirmed (2 with a caveat noted but no edit), 2 need an edit (P118 Monge, P132 Gauss), 1 optional tidy-up (P129 evidence note). 0 uncertain.

## Monge, Sur la theorie des deblais et des remblais: print year settled

Question: Histoire de l'Academie royale des sciences, annee 1781, printed 1781 or 1784?

Answer: 1784, high confidence.

- The OCR of the Internet Archive scan of the volume (https://archive.org/download/histoiredelacad81hist/histoiredelacad81hist_djvu.txt) has the title page: "ANNEE M.DCCLXXXI. Avec les Memoires de Mathematique et de Physique, pour la meme Annee, tires des Registres de cette Academie. A Paris, de l'Imprimerie royale. M.DCCLXXXIV." The table of contents lists "Memoire sur la Theorie des Deblais et des Remblais. Par M. Monge" followed by the next item at page 705, consistent with pp. 666-704.
- The Internet Archive catalogue record for the same volume (https://archive.org/metadata/histoiredelacad81hist) has `volume: 1781`, `year: 1784`. The 1784 volume of the series carries `year: 1787`, so the three-year lag is systematic.
- The BnF bibliography confirms the title and pages 666-704 (volume year 1781) but does not give the print year, and it does not mention curvature.
- The curvature claim itself is supported by the printed volume: around pp. 689-690 of the memoir Monge shows that the intersections of the surface with the developable surfaces made by the normals are "les lignes de moindre courbure" and "les lignes de plus grande courbure". Wikipedia (Gaspard Monge, quoting Rouse Ball's account) says the memoir "establishes in connection with it his capital discovery of the curves of curvature of a surface".

Edit A (P118, milestone year 1784, role key_development, label starting "Monge's memoir on the theory of deblais"): replace the three fields `c`, `n`, `ev` of that milestone with:

```json
"c": "high",
"n": "Presented to the Academy on 28 March 1781. The volume of the Histoire de l'Académie royale des sciences for the year 1781 has the imprint 'De l'Imprimerie royale, M.DCCLXXXIV' on its title page (Internet Archive scan, also catalogued there as year 1784), so the publication year is 1784. The lines of greatest and least curvature appear in the memoir (printed volume, about pp. 689-690).",
"ev": [
 {"c": "Title page of the volume for the year 1781 reads 'Paris, de l'Imprimerie royale, M.DCCLXXXIV'; the table of contents lists the Monge memoir; the memoir defines the lines of greatest and least curvature", "s": "Internet Archive, Histoire de l'Académie royale des sciences, année 1781 (printed 1784)", "u": "https://archive.org/details/histoiredelacad81hist", "k": "bibliographic_record"},
 {"c": "Gives the memoir at Mém. de l'Académie 1781, pp. 666-704", "s": "BnF, Des tas de sable aux pixels (bibliography)", "u": "https://www.bnf.fr/sites/default/files/2019-12/Des%20tas%20de%20sables%20aux%20pixels_bibliographie.pdf", "k": "bibliographic_record"},
 {"c": "Says the memoir establishes, in connection with the earthwork problem, the curves of curvature of a surface", "s": "Wikipedia, Gaspard Monge", "u": "https://en.wikipedia.org/wiki/Gaspard_Monge", "k": "history_page"}
]
```

The milestone's `y` (1784), `w` and `d` stay as they are. No derived date changes (key_development does not set one).

## Gauss, Theoria combinationis observationum erroribus minimis obnoxiae: print year and which part

Print year: 1823, medium confidence.

- Gauss's Werke vol. 4 (https://archive.org/download/werke00gausgoog/werke00gausgoog_djvu.txt) reproduces the headings of both parts with the original imprint: Pars prior "Societati regiae scientiarum exhibita 1821 Febr. 15 [OCR: 16]. Commentationes societatis regiae scientiarum Gottingensis recentiores. Vol. v. Gottingae MDCCCXXIII" and Pars posterior "exhibita 1823 Febr. 2. ... Vol. v. Gottingae MDCCCXXIII". The OCR of the first date line reads "MDCCCXXIN", so the print year rests on the clear second heading, on the editors' consistent reproduction, and on the next item.
- A separate edition, "Gottingae, apud Henricum Dieterich", is catalogued by the Internet Archive (Ghent copy, https://archive.org/details/bub_gb_ZQ8OAAAAQAAJ) with date 1823; its title page shows Dieterich and the year, and its text contains both parts with the same exhibition dates (Pars prior 15 Feb 1821, Pars posterior 2 Feb 1823). The Gauss Werke supplement in vol. 6 of the Commentationes carries "MDCCCXXVIII", so vol. 5 and 6 are five years apart, consistent with 1823.
- Pars posterior was read on 2 Feb 1823, so the volume cannot be earlier than 1823. Gauss's own notice of Pars posterior in the Gottingische gelehrte Anzeigen is dated 24 Feb 1823 (Pulskamp bibliography).
- I could not locate a library catalogue record of volume 5 alone (the Internet Archive search returned volumes of the series for other years only; HathiTrust returned 403). So the print year rests on the Werke imprint and the 1823 separate edition rather than a catalogue entry for the volume. Confidence is medium rather than high for that reason.
- One caveat for dating: Gauss published a notice of Pars prior in the Gottingische gelehrte Anzeigen on 26 Feb 1821 (Werke 4, pp. 95-100). That notice is a short public announcement of the content, but the work itself (the theorem and its proof) was printed only in 1823. Publication year of the work governs, so 1823 stays.

Which part states the minimum-variance result: Pars prior.

- Pars prior has arts. 1-22 (vol. 5, pp. 33-62). The introduction to the section (arts. 17-18) states the aim ("methodum quadratorum minimorum exhibere combinationem ex omnibus optimam, non quidem proxime, sed absolute, quaecunque fuerit lex probabilitatis errorum"), art. 19 sets up the linear model, art. 20 is the "Problema" ("among all systems of coefficients ... for which the combination equals the unknown x plus a constant, find the one with minimum sum of squares of the coefficients", the Gauss-Markov optimality problem; solution and "Q.E.I." in the same article), and art. 21 concludes that the most suitable determination is the least-squares one with weight 1/[aa]. These are Werke 4, pp. ~21-25 (vol. 5 about pp. 56-60).
- Pars posterior (arts. 23-39, pp. 63-90) continues with elimination, weights, correction of the weights and the estimation of the mean error from the residuals; it does not contain the optimality theorem.
- The existing milestone is therefore correctly dated and correctly spans Pars prior and Pars posterior; only the note ("Which part holds each result was not checked") is now answerable.

Edit B (P132, milestone year 1823, label "Gauss's Theoria combinationis observationum erroribus minimis obnoxiae"): replace `c`, `n` and `ev`:

```json
"c": "medium",
"n": "Pars prior (arts. 1-22) was presented 15 Feb 1821 and Pars posterior (arts. 23 ff.) 2 Feb 1823; both appear in volume 5 of the Commentationes recentiores, whose headings in Gauss's Werke 4 read 'Gottingae MDCCCXXIII', and a separate Dieterich edition is dated 1823, so the work was printed in 1823 (Gauss's own notice of Pars prior appeared in the Göttingische gelehrte Anzeigen on 26 Feb 1821). The minimum-variance result (among linear combinations without constant term, least squares has the smallest mean error) is in Pars prior, arts. 19-21 (the problem of art. 20); Pars posterior treats weights, elimination and the estimate of the mean error. A library record of volume 5 alone was not found.",
"ev": [
 {"c": "Bibliography of Gauss's least-squares writings: Pars prior (vol. 5, pp. 33-62, 15 Feb 1821) and Pars posterior (vol. 5, pp. 63-90, 2 Feb 1823); the dates given are those of the papers, not a print year", "s": "Pulskamp, Gauss bibliography (Royal Holloway)", "u": "https://gtfp.cs.rhul.ac.uk/pulskamp/Gauss/Gauss.html", "k": "bibliographic_record"},
 {"c": "Headings of both parts read 'Commentationes societatis regiae scientiarum Gottingensis recentiores. Vol. v. Gottingae MDCCCXXIII'; art. 20 poses and solves the minimum problem, art. 21 concludes that least squares is the most suitable combination", "s": "Gauss, Werke vol. 4 (1873), Internet Archive scan", "u": "https://archive.org/details/werke00gausgoog", "k": "primary_text"},
 {"c": "Separate Göttingen edition by Dieterich, dated 1823, containing Pars prior and Pars posterior", "s": "Internet Archive, Theoria combinationis observationum erroribus minimis obnoxiae (Dieterich, 1823)", "u": "https://archive.org/details/bub_gb_ZQ8OAAAAQAAJ", "k": "bibliographic_record"}
]
```

Optional, not required by the data rules: the label could be shortened or the `d` sentence refined to say "among linear combinations with the least mean error", since the current wording ("independent of the normal law assumed in his 1809 derivation") is accurate. No derived date changes.

## Edit C (optional, P129, milestone range 1530-1550, "Yuktibhasa gives derivations")

The note cites "MacTutor's Jyesthadeva biography", but the evidence list cites only the Madhava biography (which does say "around 1550"). To match, append to its `ev`:

```json
{"c": "Says the Yuktibhasa was written in 1501 in one passage and in about 1550 in another, so no single date is reliable", "s": "MacTutor, Jyesthadeva", "u": "https://mathshistory.st-andrews.ac.uk/Biographies/Jyesthadeva/", "k": "history_page"}
```

## Items needing an edit

1. P118, Monge 1784 key_development: raise `c` to high, rewrite `n`, replace `ev` (the BnF page does not support the curvature claim). Edit A.
2. P132, Gauss 1823 key_development: raise `c` to medium, rewrite `n` (print year and which part now settled), add evidence. Edit B.
3. P129, Yuktibhasa range (optional): add the Jyesthadeva MacTutor evidence entry so the note and the evidence agree. Edit C.

No fixed row has a wrong year, journal, volume, role or derived date. All Crossref DOIs resolve to the cited title, journal, volume and year.
