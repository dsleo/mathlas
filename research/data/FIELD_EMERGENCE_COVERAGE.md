# How complete is the list? Coverage estimates by period (2026-10-17)

## Design

For each of four periods, two harvests ran blind to each other, to the seed sets and to the earlier harvests, on different source families:
- **Wikipedia** only
- **A second family:** MacTutor biographies and the Stanford Encyclopedia of Philosophy for the three periods before 1990; Quanta Magazine, Tao's and Gowers's blogs and the nLab for 1990 to 2026

An AI agent matched the same event across the two lists and the seed events dated in that period. A separate pass judged each item: real and in scope, real but out of scope, or not an event.

## Results

- **Before 1850:** 113 verified events. Wikipedia 75, second family 89, overlap 52. Estimated total about **128** (95% interval about 116 to 140). Lower bound from singletons and doubletons: 158. The 12 seed events are 11% of the verified set; the harvests found 11 of them.
- **1850 to 1930:** 98 verified events. Wikipedia 70, second family 70, overlap 47. Estimated total about **104** (94 to 114). Lower bound 124. The 25 seeds are 26% of the verified set; the harvests found 20 of them.
- **1930 to 1990:** 179 verified events (accepted by both a Sonnet and an Opus pass). Wikipedia 106, second family 106, overlap 65. Estimated total about **172** (156 to 188). Lower bound 268. The 75 seeds are 42% of the verified set; the harvests found 43 of them. Estimates built on the seeds are higher, about 225.
- **1990 to 2026:** 123 verified events (accepted by both passes). Wikipedia 75, second family 59, overlap 36. Estimated total about **122** (105 to 139). Lower bound 191. The 47 seeds are 38% of the verified set; the harvests found 22 of them (47%).

Across the four periods: 513 verified events (events dated near a boundary can appear in two periods), against an estimated 526 to 741 at this granularity.

## How to read this

- The numbers estimate how many field births and combinations the **standard narratives and sources** record, at the granularity those sources use. Events that historians rarely discuss are not counted, and neither are events split or merged differently.
- **The estimates are probably too low.** Both harvests in a period retell the same historiography, and many entries were written from the agents' memory rather than from the pages, so the two lists agree more than independent searches would. The lower bound and the seed-based estimates, which are higher in the 20th century, suggest the true totals are above the two-list figures.
- **The harvests miss technical and recent events.** For 1990 to 2026 they found under half of the seed events, which come from prize citations. General sources are weak on modern, specialised results.
- **Verification quality varies.** 1930 to 1990 and 1990 to 2026 were judged twice (Sonnet, then Opus with a bibliographic check of every main work); the stricter rule kept 214 of 255 and 135 of 210 items. 1850 to 1930 had one Opus pass and before 1850 one Sonnet pass.
- **Not human-checked** apart from the 14-event audit sample, which awaits review.

## The result that matters

The seed sets, chosen from knowledge and prizes, are only a small share of what the sources record: 11% before 1850, 26% in 1850 to 1930, 42% in 1930 to 1990 and 38% since 1990. Recall measured only against the seed sets would have overstated completeness.

## Files

- `field-events-verified.json`: the 513 verified events with sources, list membership, corrections and verifier notes, and the clusters that only one pass accepted
- `field-events-1850-1930.json`: the first period on its own
