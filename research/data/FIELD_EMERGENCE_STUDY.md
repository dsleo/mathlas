# Study design: how mathematical fields are born and married

## Question

When and how did new fields of mathematics emerge from older ones (group theory from the solution of polynomial equations), and when did a result fall to a combination of techniques from distant fields (ergodic theory and Fourier analysis in additive combinatorics)? Goal: a dated, sourced, searchable inventory of such events, from antiquity to now, with an honest estimate of how complete it is.

"Find all" is not checkable directly, because no list of all events exists. The strategy is therefore built around **estimating coverage**, not asserting it.

## 1. Fix what an event is (before collecting anything)

| Type | Meaning | Example |
| --- | --- | --- |
| **Birth by abstraction** | A recurring pattern in one field is made an object of its own | polynomial resolvents → permutation groups → abstract groups |
| **Birth by fusion** | A field is created by joining two others | algebraic topology, algebraic geometry, analytic number theory |
| **Technique transfer** | A tool from field A settles a question native to field B | Furstenberg's ergodic proof of Szemerédi's theorem |
| **Dictionary / analogy** | A systematic correspondence between fields is found, then exploited | Weil's number field / function field / Riemann surface analogy; Langlands |
| **Reification** | A field's methods become a theory in their own right | category theory out of algebraic topology |
| **Import from outside** | A question or tool enters from physics, CS, or logic | gauge theory → 4-manifolds; entropy → additive combinatorics |
| **Split / disciplinarization** | A sub-area stops talking to its parent | |

Each event stores **three separate dates**, never one: *conceptual* (first object or definition), *methodological* (first tool used on purpose), *institutional* (named chapter, code, journal, chair, textbook). Group theory's three dates are decades apart; collapsing them is how "when was X born" arguments never end.

Granularity: nodes are the existing `technique-vocabulary.json` families and groups, so events render on the World map. Where the vocabulary is too coarse (it has 5 families and 8 `fields`), map to MSC 2020 two-digit sections.

## 2. Five discovery channels with independent failure modes

No channel is trusted alone. Each finds events the others miss.

**A. Historiography (high precision, recall limited by what historians chose to write about).**
Systematic pass over the secondary literature, extracting every stated "origin", "fusion" or "unexpected connection". Starting set, from memory and to be verified: Bourbaki's *Éléments d'histoire*, Dieudonné's *Panorama* and *History of Algebraic and Differential Topology*, Kolmogorov–Yushkevich's *Mathematics of the 19th Century*, Kline, Gray, Corry (*Modern Algebra and the Rise of Mathematical Structures*), Wussing (abstract group concept), Hawkins (Lie groups), Kleiner, Krömer (category theory), Mac Lane (*Form and Function*), Weil's 1940 letter to Simone Weil. Add ICM plenary and section lists (the section structure of the ICM is itself a dated institutional record), Fields/Abel/Shaw citations, and Quanta/Notices features for the last 20 years.

**B. Classification co-occurrence (high recall for 1931–now, blind before).**
zbMATH Open carries MSC codes per paper under CC-BY-SA 4.0, covers the *Jahrbuch über die Fortschritte der Mathematik* (1868–1942) in the same database, and a Zenodo dump includes each paper's MSC and the MSCs of its references ([API paper](https://arxiv.org/pdf/2106.04664), [JFM in zbMATH Open](https://ems.press/journals/mag/articles/3718587)). Signal: pairs of MSC sections whose co-occurrence rises from near zero to sustained, measured against a degree-preserving null; then the same on *reference* MSCs (what a paper cites vs where it lives). Birth shows up as a pair that acquires its own code or journal. Caveat: codes on old material are assigned retroactively by later editors, and MSC revisions (2000, 2010, 2020) must be mapped.

**C. Citation-novelty indices (flags the individual marriage paper).**
Uzzi-style atypical-combination scores (z-score of observed vs shuffled co-citation of journal pairs, tail of the paper's distribution) and Rao–Stirling diversity, computed over MSC instead of journals ([Uzzi et al.; Novelpy implementation](https://arxiv.org/pdf/2211.10346)). Validation is mixed: one score tracks expert judgment, another does not, so use the validated variant and treat output as a *candidate list*, not a finding.

**D. LLM extraction over abstracts and introductions (broad, cheap, needs verification).**
For papers surviving B or C: extract `{result, target field, tools and their source fields, claimed novelty, supporting quote}`. Cue phrases ("using methods from", "a new connection between", "surprisingly") raise recall before the model sees anything. Output feeds the same `borrowsFrom` schema the route tags already use. This also searches arXiv, whose cross-list tags give a free second classification from 1991.

**E. Formal and community structure (new, machine-readable).**
Mathlib's import graph is a dated dependency network between areas, with git history ([The Network Structure of Mathlib](https://arxiv.org/abs/2604.24797)); Lean blueprints (PFR, FLT) state which areas a proof imports. MathOverflow "unexpected applications of X to Y" threads, Tao's and Gowers's blogs, and nLab "relation to" sections are expert-curated leads.

## 3. Completeness: how "all" becomes a number

1. **Seed set.** Hand-build ~60 events I know independently (Galois/groups, Weil conjectures, Atiyah–Singer, Jones polynomial, moonshine, Furstenberg, Green–Tao, Perelman, Wiles, Hairer, Mirzakhani, Huh, PFR...). Report each channel's **recall on the seeds**.
2. **Capture–recapture.** Overlap between channels' independent finds (Lincoln–Petersen / Chao) gives an estimate of the total and an interval. Report "N found, estimated M exist".
3. **Precision audit.** Random sample of each channel's output is verified by two reviewers, as the route tags already are.
4. **Era table.** Report coverage per era, since channel B is blind before 1868 and weak before 1931; for earlier periods the claim is only "what historiography records".

## 4. Verification and evidence rules (reuse the repo's)

Candidate → needs a primary source or a named secondary source with a locator. Separate `source-extracted` from `assistant-reconstruction`, keep the two-reviewer agreement field, flag `near-duplicate` and `not-an-event` (a field *using* a tool is not a marriage unless the tool was new to it or the result was out of its former reach). Precedence is recorded as an interval ("not before Xs, not after Y"), never a false point date.

## 5. How it connects to what exists

- Every route in the course-results catalog whose `borrowsFrom` differs from the theorem's home field is already a technique-transfer event, a free pilot of ~hundreds of rows. The strict rival-pair bridges on the World map are the within-catalog subset.
- Proofs of one theorem by distant fields (four proofs of Szemerédi) are the cleanest marriage evidence there is; the catalog is a *source* of events, not just a display.

## 6. Prior work to read first (found by search, not yet read)

- [Co-occurrence simplicial complexes in mathematics](https://arxiv.org/pdf/1803.04410): arXiv concept co-occurrence, "holes" between distant areas.
- [Network analysis of Zentralblatt MATH data](https://ar5iv.labs.arxiv.org/html/1409.1726) and [Mathematical Reviews collaboration network 1985–2009](https://arxiv.org/pdf/1203.5158).
- [Structural signature of topic popularity in mathematical collaboration networks](https://arxiv.org/pdf/2506.22946).
- [Interdisciplinarity of applied mathematics](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0137424) (PNAS corpus).
- [Same Problem, Different Field](https://arxiv.org/pdf/2609.07595): technique fingerprints across fields (2026 preprint).
- Not found by search, so *no claim either way*: a study of MSC-pair emergence over time, or a curated list of marriages. Treat as an open gap only after a proper review (Phase 0).

## Phases

0. **Literature review (1–2 weeks):** the six bullets above plus history-of-mathematics sources; decide what to reuse. Outcome: confirm or kill the "gap" claim.
1. **Schema and seeds:** event schema, 60 seeds, ontology mapping to MSC.
2. **Channel B on 1931–now:** cheapest large-scale signal; sets the candidate list for D.
3. **Channels A and E in parallel,** merge, capture–recapture.
4. **Verification pass and map layer:** a time axis on the World view (islands appearing, bridges dated).

## Status (2026-10-16)

| Piece | File | State |
| --- | --- | --- |
| Seed set A (77 events, from the author's knowledge) | [field-events-seed.json](field-events-seed.json) | Committed; citations mostly checked |
| Seed set B (42 events, derived by rule from Fields and Abel citations) | [field-events-seed-b.json](field-events-seed-b.json) | Independent of A; citations partly checked. Use B to grade recall |
| Phase 0 reading notes | [FIELD_EMERGENCE_PHASE0.md](FIELD_EMERGENCE_PHASE0.md) | Abstract-level; no direct precedent found |
| Channel B spike | [FIELD_EMERGENCE_SPIKE.md](FIELD_EMERGENCE_SPIKE.md) | Curves show the expected take-offs after 1970; no validated detector yet; blind before about 1970 |
