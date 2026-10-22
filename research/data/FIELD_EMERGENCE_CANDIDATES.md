# Candidate events from three history harvests (2026-10-17)

## What was done

Three agents read different sources and proposed events not already in the seed sets:
- MacTutor history topics: 80 candidates, mostly before 1990
- ICM and prize records: 80 candidates
- Quanta Magazine, Tao and Gowers blogs: 80 candidates, 2000 to 2026

Each of the 240 candidates was then checked twice, independently:
- pass 1 by Sonnet agents
- pass 2 by Opus agents, which formed a judgement before reading the proposer's sources

Verifiers checked: is it a real field birth or combination, are type, fields and dates right, do the cited works exist (Crossref, arXiv, Open Library, search), is it a duplicate.

## Result

- **Accepted by both passes: 141** new events.
- **Contested (one accepts, one rejects): 32.**
- **Rejected by both: 46.**
- **Rediscovered a seed event: 6** (same event as a seed, found by accident because harvesters were told to skip seeds).
- **Tally across passes:** 140 accepted by both before duplicate merging, 49 rejected by both, 33 contested before merging.

Accepted by source: ICM and prizes 60, MacTutor 42, Quanta and blogs 36, plus 3 found in two lists.

## What the verifiers kept finding wrong

- Single-field results presented as combinations.
- Physics-internal items (not mathematical).
- Prize and ICM pages as evidence: they confirm who did the work, not the bridge.
- Wrong or truncated citations and wrong years (examples: Lindemann 1882 not 1880, Macaulay 1913 not 1915).
- Fields too coarse ("Geometry", "Analysis").
- Dates that were a first statement or reprint, not first use.

About a third of the proposals were not real events, which is why two passes are needed.

## Capture–recapture does not work on this design

The idea was to estimate how many events exist from how much the lists overlap. Run on these lists it gives nonsense (anything from about 900 to over 4,000), and the numbers are not reported as estimates, because:

1. Harvesters were told to skip events already in the seed sets, so overlap with the seeds is zero by construction.
2. The harvests cover different eras by design (MacTutor mostly before 1990, Quanta after 2000).
3. Overlap between harvests is small partly because the harvesters read different sources, not only because many events remain.

A valid estimate needs two harvests of the same scope (same era and fields), run blind to each other and to the seeds, with overlap measured afterwards.

What can be said: 141 events beyond the 119 seeds were found and accepted after reading a modest number of sources, so the unseen population is large.

## Files

- `field-events-candidates.json`: all 240 candidates with status, corrections and both verdicts
- `FIELD_EMERGENCE_AUDIT.md`: 14 randomly drawn accepted events for human audit
