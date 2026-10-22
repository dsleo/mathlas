# Class-level run: what the numbers say (2026-10-17)

Channel B at three-character MSC class level, graded against the seed events.

## What was run

- **Data.** Class-pair counts for every review year 1970 to 2024, from the MaRDI SPARQL mirror of zbMATH Open (query route, no dump downloaded). 24k class pairs with at least 30 documents, 728 classes, eleven 5-year windows.
- **Detector.** `scripts/field-emergence/detect.py` with its default settings. No threshold was tuned on the seed events.
- **Grading.** 119 seed events (sets A and B), each mapped to class pairs by two independent passes (a first mapper and a blind AI pass). Pairs from either pass count; a stricter score uses only pairs both passes proposed. An event is a "hit" if one of its pairs is flagged (q at most 0.05) with an onset in the expected decade or the next.

## Results

- **Detector flags:** 54 of 24k pairs (q at most 0.05).
- **Seed events recovered:** 0 of 86 gradable events were flagged with a correct onset. One pair was flagged late. Using only pairs both passes agreed on: 0 of 80.
- **Closest miss:** mirror symmetry (14J x 81T), q about 0.06 on the earlier partial run.
- **Ranking test (no thresholds).** Rank each event's best pair among pairs of similar size by the detector's raw evidence:
  - top 1%: 8.1% of events observed, 2.9% expected by chance
  - top 5%: 20.9% observed, 13.9% by chance
  - top 10%: 36.0% observed, 26.3% by chance
  - top 20%: 53.5% observed, 47.2% by chance
  This is real but modest enrichment, about 3 times chance at the top 1%.
- **What the 54 flagged pairs are.** Mostly numerical analysis and computational geometry (for example 51N x 65D, 26D x 65D), and general "00" classes. Not the field combinations in our seed sets.

## Reading

1. **The detector is strict and calibrated, and it does not find the known events.** The simulation predicted this: seed pairs rise 1.2 to 2 times per decade, and the detector needs about 3 to 5 times at 10 or more expected documents.
2. **Channel B alone is a weak finder of field combinations at class level.** As a ranking it carries some signal, enough to prioritise reading, not enough to discover.
3. **Role in the pipeline.** Use channel B to rank and date known candidates, and to point the reading channel at the top-ranked pairs. Discovery has to come from history and reading (channels A and D).

## Calibration facts

- **Review-year lag.** Comparing yearly publication counts (API) with review-year counts (SPARQL) for 14 high-visibility pairs: about 2 years pooled (0 to 3 per pair). Totals differ by about 7%, SPARQL lower. So 5-year windows by review year are acceptable.
- **Class-pair agreement between independent AI mappers.** Of 91 gradable events, 84 share at least one exact class pair (16 identical, 68 partial) and 7 differ. Agreement is probably inflated because both used the same 219-class title file.
- **Counts are thin.** For example 37A x 11B has 1, 2, 7 and 91 documents in the 1970s to 2000s.

## Limits

- Review-year counts, not publication-year.
- MSC codes for old papers were assigned later; the scheme changed (class 37 appears only in the 2000 edition).
- The detector looks for take-offs from an established baseline, so a new pair that is rare then common is the best case, an old pair with a gradual rise the worst.
- Seed pairs are my and an AI's readings of event summaries, not observed classifications.

## Files

- `class-level-results.json` : summary, 54 flagged pairs, per-event grades
- `event-msc-map-consensus.json` : pairs per event from both passes
- `llm-pair-check/` : the blind pass outputs
- `scripts/field-emergence/class_counts.py`, `analyze_class_level.py`
