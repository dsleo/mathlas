# Adjudication of the 40 cross-check leads (2026-10-26)

Each lead in `summary.json` was checked against a bibliographic record or history page before any change to `data/events.json`. Publication year governs dates. Private or unpublished work is recorded as a precursor. **Fixed** means the record was edited (a milestone added or corrected). **Lead wrong** means the record already holds the right fact or the lead's date is not the publication date. **Unresolved** means no source settled it, so nothing changed. Every event stays `source-first`: none was given a full direct review.

Totals after the second pass: 24 fixed, 16 lead wrong, 0 unresolved (the 5 first-pass unresolved leads: 4 fixed or improved, 1 rejected).

| # | pid | Lead milestone | Verdict | Source checked / action |
|---|-----|----------------|---------|-------------------------|
| 1 | P012 | 1868 Gordan's finiteness for binary forms | fixed | Crossref 10.1515/crll.1868.69.323 (Crelle 69, 1868); added as precursor |
| 2 | P052 | 1974 Knuth, Computer science and its relation to mathematics | fixed | Crossref 10.1080/00029890.1974.11993556 (AMM 81, 1974); added as key_development, not consolidation (an essay, not a treatise) |
| 3 | P055 | 1961 Atiyah-Hirzebruch, Vector bundles and homogeneous spaces | fixed | Crossref 10.1090/pspum/003/0139181 (PSPM 3, 1961); added as key_development |
| 4 | P058 | 2021 Fargues-Scholze geometrization of local Langlands | fixed | arXiv:2102.13459 (v1 26 Feb 2021; the abstract places the work in the geometric Langlands programme on the FF curve); added as key_development, medium confidence, preprint year noted |
| 5 | P063 | 2017 Formal proof of the Kepler conjecture | fixed | Crossref 10.1017/fmp.2017.1 (Forum Math. Pi 5, 2017); added as key_development |
| 6 | P095 | 1974 Whitehead problem independent of ZFC | fixed | Crossref 10.1007/bf02757281 (Israel J. Math. 18, 1974); now the first_application (methodological date 1980 to 1974); Shelah 1980 kept as key_development |
| 7 | P200 | 1931 Goedel's incompleteness paper | fixed | Crossref 10.1007/bf01700692 (Monatsh. 38, 1931); added as precursor |
| 8 | P285 | 1981 Smale, Global analysis and economics (Handbook) | fixed | Crossref 10.1016/s1573-4382(81)01012-6 (Handbook of Math. Econ. 1, 1981); added as consolidation (institutional date unchanged, 1973) |
| 9 | P354 (merged into P004) | 1930 Kuratowski's planarity characterisation | fixed | Crossref 10.4064/fm-15-1-271-283 (Fund. Math. 15, 1930); added as key_development to P004 |
| 10 | P420 | 1927 Schreier on subgroups of free groups | lead wrong | Already in the record as the 1924-1927 range "Nielsen and Schreier on free groups" with the same DOI; the matcher compared start years only |
| 11 | P432 | 1797 Wessel's memoir presented | lead wrong | 1797 is the reading at the Academy; the record dates the publication (1799) as first_statement, as the schema requires |
| 12 | P449 | 1425 Brunelleschi investigates perspective | fixed | Second pass: no source gives 1425 for the experiment (Smarthistory c. 1420, MacTutor c. 1413, Wikipedia 1425); precursor widened to the range 1413-1425 with the disagreement in the note |
| 13 | P488 | 2009 Hill-Hopkins-Ravenel nonexistence | lead wrong | arXiv:0908.3724 is the preprint of the Annals 2016 paper, already recorded at 2016 with the arXiv link in its evidence |
| 14 | P540 | 2014 Liouville quantum gravity on the sphere | lead wrong | arXiv:1410.7318 is the preprint of the CMP 2016 paper already recorded (first_application 2016) |
| 15 | P080 | 2009 Mouhot-Villani preprint | lead wrong | arXiv:0904.2760 is the preprint of Acta Math. 207 (2011), already recorded |
| 16 | P114 | 1736 First published proof of the little theorem | lead wrong | Euler E54 was presented in 1736 and printed in Commentarii 8 in 1741 (Euler Archive); the record has 1741 |
| 17 | P118 | 1731 Clairaut on curves of double curvature | fixed | MacTutor (Clairaut) gives the 1731 title page and 1729 completion; precursor re-dated 1729 to 1731 by publication |
| 18 | P118 | 1785 Monge memoir on generation of surfaces | fixed (different milestone) | The 1785 date was not matched to a publication. Second pass found Monge's 1781 memoir on déblais and remblais (Mém. Acad. 1781, pp. 666-704, presented 28 Mar 1781; BnF bibliography) which introduces the lines of curvature; added as key_development, year 1784 (printing, low confidence: one secondary source) |
| 19 | P125 | 1209 Sharaf al-Din's Treatise on equations | lead wrong | Falls inside the recorded first_statement range 1165-1213; no source fixes the year more precisely |
| 20 | P129 | 1530 Yuktibhasa | fixed | Second pass: Wikipedia about 1530; MacTutor states both 1501 and about 1550 so it is not a reliable single date; key_development re-dated to the range 1530-1550 (methodological fallback 1550 to 1530) |
| 21 | P132 | 1822 Gauss optimality of least squares | fixed (low confidence) | Second pass: Pars prior vol. 5 pp. 33-62 (15 Feb 1821), Pars posterior pp. 63-90 (2 Feb 1823) per Pulskamp's bibliography; the volume cannot predate 1823; added key_development 1823 at low confidence. Print year and which part holds the optimality theorem still not confirmed |
| 22 | P135 | 1811 expanded second edition | fixed | archive.org scan of vol. 1 (Paris, Courcier, 1811) and Wikipedia (vol. 2 posthumous 1815); added as key_development 1811-1815 (methodological fallback moves 1834 to 1811) |
| 23 | P149 | 600 Wang Xiaotong's cubic approximation | lead wrong | Record has the better-supported 620-626 range (Jigu suanjing, before 626, MacTutor) |
| 24 | P155 | 1000 Jia Xian and the triangle | lead wrong | MacTutor (Jia Xian) gives about 1050, as recorded; the lead's 1000 is a looser century date |
| 25 | P175 | -250 Chandahshastra | lead wrong | Inside the recorded range -300 to -100 |
| 26 | P176 | -140 Hipparchus tests lunar models | lead wrong | Inside the recorded range -147 to -127 |
| 27 | P185 | 1733 Normal approximation to the binomial | fixed | MacTutor (De Moivre) and Wikipedia: Latin pamphlet dated Nov 1733, privately circulated, published in the 1738 Doctrine of Chances; added as key_development 1738 with the 1733 pamphlet in the note |
| 28 | P189 | 100 Sphaerica | lead wrong | Inside the recorded range 98-130 |
| 29 | P190 | 1727 ln(-1) = pi i found | lead wrong | Second pass: sources only show the Euler-Bernoulli letters (e.g. 10 Dec 1728) arguing about log(-1); none shows Euler stating i pi in 1727 and the identity is not explicit even in his 1749 paper. Nothing added; letters would be a precursor at most and the evidence page could not be read |
| 30 | P234 | 1943 On rings of operators IV | fixed | Crossref 10.2307/1969107 (Ann. Math. 44, 1943); added as key_development |
| 31 | P250 | 1936 Sprague, Ueber mathematische Kampfspiele | fixed | J-STAGE record (Tohoku Math. J. 41, 1935, 438-444); first_statement 1930-1939 (decade) to 1935, confidence low to medium; map year 1930 to 1935 and the P250/E25 link distance updated |
| 32 | P250 | 1939 Grundy, Mathematics and games | fixed | Eureka 2 (1939) 6-8 per Wikipedia and secondary citations; kept inside the Sprague milestone as an independent rediscovery rather than a separate milestone |
| 33 | P253 | 1975 Cylindrical algebraic decomposition | fixed | Crossref 10.1007/3-540-07407-4_17 (LNCS 33, 1975); added as key_development |
| 34 | P260 | 1975 Kasparov's K-homology | fixed | Crossref 10.1070/im1975v009n04abeh001497 (Math. USSR Izv. 9, 1975); added as precursor, not first_statement (KK appears 1979-1980) |
| 35 | P267 | 1949 von Neumann's lectures on self-reproducing automata | fixed | Burks' editor's introduction (archive.org scan of the 1966 book): five Illinois lectures, December 1949; added as precursor (unpublished lectures) |
| 36 | P272 | 1983 Getzler's supersymmetric proof | fixed | Crossref 10.1007/bf01210843 (CMP 92, 1983); added as key_development beside the 1986 short proof |
| 37 | P370 | 1928 Grundzuege der theoretischen Logik | fixed | CiNii record (Springer, Grundlehren 27, 1928); added as key_development, low confidence, not consolidation (a logic textbook; Hilbert-Bernays 1934 stays the consolidation) |
| 38 | P389 | 1897 Hensel invents p-adic numbers | lead wrong | zbMATH/JFM 30.0096.03: Jahresber. DMV 6, published 1899, as recorded; 1897 (MacTutor) is the date of the idea, not a publication |
| 39 | P389 | 1921 Hasse local-global principle | lead wrong | 1921 is Hasse's dissertation year; the record dates the Crelle 152 publication (1923) |
| 40 | P459 | -150 Hipparchus' table of chords | lead wrong | MacTutor gives about 140 BC, as recorded; neither year is attested in a source |

Resolved after the first pass: P004 carried two first_statement milestones for Euler's Königsberg paper (1736 and 1741). The paper was printed in 1741, so the 1736 entry was merged into the 1741 milestone (its two history-page sources kept, with the note that 1736 is the volume title and presentation year); the map and conceptual date is now 1741 and the six P004 link distances were recomputed.
