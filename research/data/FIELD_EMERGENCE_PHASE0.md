# Phase 0: what prior work exists (reading notes, 2026-10-16)

Scope and limits. This is reading at abstract and metadata level (arXiv abstract pages and publisher pages, summarised by a tool), not a close reading of full papers. Only the leads found in two search rounds were read. Google Scholar, MathSciNet and the history-of-mathematics monographs were not searched. Treat "not found" as "not found here".

## Leads read

| Work | What it does | Data | Use for us |
| --- | --- | --- | --- |
| Salnikov, Cassese, Lambiotte, Jones, *Co-occurrence simplicial complexes in mathematics* ([arXiv:1803.04410](https://arxiv.org/abs/1803.04410)) | Concepts that co-occur in an article form simplices; "holes" between distant concepts close when they are finally combined in one paper | Word-level concepts from mathematical articles (corpus and size not stated on the abstract page) | The hole-closing idea is a concept-level analogue of a "marriage" event. Words, not MSC, and no dated catalogue |
| *Network analysis of Zentralblatt MATH data* ([arXiv:1409.1726](https://arxiv.org/abs/1409.1726), Scientometrics 102 (2015)) | Two-mode networks works x authors/journals/keywords/MSC, analysed in Pajek | zbMATH 1990-2010 | Confirms MSC-based networks over zbMATH are feasible. Descriptive; the abstract reports no MSC-pair time series or emergence analysis |
| *Evolutionary events in a mathematical sciences research collaboration network* ([arXiv:1203.5158](https://arxiv.org/abs/1203.5158)) | Sliding windows on the collaboration network; two major shifts; pure and applied subnetworks diverge | Mathematical Reviews subset 1985-2009 | Collaboration structure, not topic structure. Not a detector of new fields |
| *A structural signature of topic popularity in mathematical collaboration networks* ([arXiv:2506.22946](https://arxiv.org/abs/2506.22946)) | Popular topics are modular, niche topics core-periphery | arXiv metadata, 121,391 papers 2020-2025, 1,938 algorithmically found topics | The topic list could be a finer unit than two-digit MSC for recent years. Not about emergence |
| Lin, Evans, Wu, *New directions in science emerge from disconnection and discord* ([arXiv:2103.03398](https://arxiv.org/abs/2103.03398)) | Atypical combinations are about twice as likely to disrupt; disruption scores take a decade or more to converge | Not named on the abstract page | Supports channel C. The decade-long latency means atypicality is a retrospective tool for dating, not an early detector |
| Uzzi et al. 2013 and follow-ups (Bornmann et al. validation) | Z-score of journal-pair co-citation against a shuffled null | Web of Science | Reusable null-model recipe (implemented in Novelpy). One variant tracks expert judgement, another does not |
| *Same Problem, Different Field* ([arXiv:2609.07595](https://arxiv.org/abs/2609.07595), JCDL 2026) | LLM "computational fingerprints" find the same computation in different fields; 109-paper benchmark, 18 method families | Computational/applied papers | Template for channel D (find technique twins across MSC sections). Not tested on proofs; code and benchmark are public |
| *The Network Structure of Mathlib* ([arXiv:2604.24797](https://arxiv.org/abs/2604.24797)) | Static multilayer graph of 308,129 declarations and 7,563 modules; 50.9% of coupling crosses namespaces | Mathlib | Shows cross-area dependency is real and large. The abstract describes no time dimension, so dating needs git history, which we would extract ourselves |
| Interdisciplinary emergence with BERTopic ([Humanit. Soc. Sci. Commun. 2024](https://www.nature.com/articles/s41599-024-03044-y)) | Network analysis plus topic modelling for emergence | not read (publisher redirect) | Unknown; retry |

Also seen only in search snippets, not read: the PLOS ONE paper on applied mathematics as an interdisciplinary hub (PNAS corpus 1999-2013).

## Verdict on the "gap" claim

No work found here builds dated MSC-pair emergence curves or a curated, sourced catalogue of field births and marriages. Neighbours exist for each ingredient (MSC networks, atypicality indices, concept co-occurrence, technique-twin retrieval, Mathlib structure). The accurate statement is "no direct precedent found at abstract level", not "none exists". It should not be asserted in a write-up until Google Scholar, MathSciNet and the history-of-mathematics literature have been searched.

## What this changes in the design

1. **Channel C is retrospective.** With convergence times of a decade or more, use it to date and rank known marriages, not to find new ones early.
2. **Unit of analysis.** Two-digit MSC is coarse; for post-2020 arXiv, algorithmic topics (as in 2506.22946) are a finer unit. For before 1990 only MSC (retro-assigned) is available.
3. **Data route.** Existing zbMATH network studies used the database directly, so the pipeline is not novel; the contribution is the dated pair-emergence layer and the sourced event catalogue.
4. **Reuse.** Novelpy for the atypicality null; the technique-fingerprint prompt from 2609.07595 for channel D; Mathlib git history for formal-era dating.
