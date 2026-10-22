# Milestone pilot batch 1: direct audit

Ten completed events, now with 67 ordered milestones. The structural validator reports no errors. This review distinguishes source-supported chronology from the remaining interpretation questions; it is not an independent model pass.

## Disputed dates

| Event | Audit finding | Remaining question |
| --- | --- | --- |
| P367, dynamical systems | [Poincaré's bibliography](https://henripoincarepapers.univ-nantes.fr/bibliohp/?a=on&action=go&yr=1880) records a **published 1880 note** in *Comptes rendus* 90, 673–675. The longer 1881 memoir and the [1890 three-body application](https://henripoincarepapers.univ-nantes.fr/bibliohp/ajax.php?bibkey=hp1890am) are separate milestones. | The submitted and withdrawn 1880 memoir must not be mistaken for the published note. |
| P363, metric spaces | The 1905 *écart* note is listed in zbMATH; a [historical analysis of its text](https://papyrus.bib.umontreal.ca/jspui/bitstream/1866/4759/2/Belanger_Mathieu_2010_these.pdf) quotes an abstract distance-like definition. The [1906 thesis](https://doi.org/10.1007/BF03018603) is a separate systematic development and application. | Whether the 1905 definition satisfies the later metric axioms exactly remains open. The milestone claims an abstract *écart*, not a modern metric-space axiomatisation. |
| P026, number-field Langlands | The 1967 private Weil letter is a precursor. Public statement and Jacquet–Langlands application have [1970 publication records](https://doi.org/10.1007/bfb0058988). Tunnell's [1981 octahedral Artin case](https://doi.org/10.1090/S0273-0979-1981-14936-3) is now a distinct later milestone. | The 1970 versus 1981 methodological disagreement is about which target problem counts as the programme's first application, rather than the existence of either publication. |
| P057, function-field Langlands | Drinfeld's [1974 elliptic modules](https://www.mathnet.ru/eng/sm3735) provide an early function-field and GL(2) connection. The [1977 published proof](https://doi.org/10.1007/BF01079470) and [1983 full treatment](https://doi.org/10.2307/2374382) remain separate. | The 1974 statement is about the machinery and a partial link, not the 1977 full correspondence proof. |
| P533, murmurations | The [2019 machine-learning preprint](https://arxiv.org/abs/1911.02008) is a first application in the wider ML-on-curves phase. A different [2020 preprint](https://arxiv.org/abs/2010.01213) is a precursor. The [2022 murmuration preprint](https://arxiv.org/abs/2204.10140) is the first statement of the named pattern; its journal appearance was 2024. | The 2019 methodological date describes the broad tool phase, not a claim that murmurations had been discovered by then. |

Boolean algebra now records Boole's 1847 book as both a public statement and a purposeful algebraic application to logic. Stone's [1934 topological application](https://doi.org/10.1073/pnas.20.3.197) and [1936 representation theorem](https://doi.org/10.1090/s0002-9947-1936-1501865-8) are separate milestones. The 1880 Peirce title was removed from the `naming` role because *algebra of logic* is not the name *Boolean algebra*; Sheffer's 1913 title carries the checked naming claim.

Euclid's `c. 300 BCE` is a historical estimate with `decade` precision. No ancient publication record has been found, and the review page must never render it as an exact year. The 1482 printed edition is a later transmission milestone, not an origin date.

## Work-record audit

`scripts/verify_field_works.py` checks cited URLs against Crossref, arXiv, Open Library, archive.org, Numdam, and the Henri Poincaré Papers bibliography. It reports metadata existence and recorded year, not whether a paper proves the associated historical claim. It also inventories milestone works that have no direct bibliographic URL. zbMATH's API timed out during this pass, so those records remain unverified rather than being counted as absent.

The three person-work title flags are metadata wording differences: Crossref's long Latin title for Cotes's *Logometria*, Open Library's Latin incipit for the 1482 *Elements*, and the expanded subtitle of Boole's *Laws of Thought*. Their years match. The earlier Poincaré 1890 DOI pointed only to a section titled “Introduction”; it has been replaced with the bibliography record for the complete memoir.
