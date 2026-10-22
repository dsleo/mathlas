# Channel B spike: MSC pair counts over time (2026-10-16)

## What was run

zbMATH Open's public search API (`api.zbmath.org/v1/document/_search`, count = `nr_total_results`) was queried for the number of documents classified in each of 35 two-digit MSC section pairs (25 chosen from the seed events, 10 random controls drawn from the same sections) in nine windows: 1931-49, then decades 1950-59 to 2010-19, and 2020-24. 578 counts in total. Code and raw counts are in [`scripts/field-emergence`](../../scripts/field-emergence); the derived series are in [`channel-b-spike.json`](channel-b-spike.json).

Per-10k frequency below = documents carrying both sections per 10,000 documents of the window.

## What the curves show

| Pair (seed events) | 1960s | 1970s | 1980s | 1990s | 2000s | 2010s | 2020-24 | Reading |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 x 37 number theory x dynamics (E38 1977, E50, B13) | 0.3 | 0.2 | 2.4 | 4.7 | 11.0 | 12.1 | 16.2 | Take-off in the 1980s after Furstenberg; second surge in the 2000s with Green-Tao |
| 05 x 37 combinatorics x dynamics (E50) | 0.0 | 0.1 | 0.5 | 0.8 | 3.2 | 6.1 | 6.5 | Surge in the 2000s |
| 57 x 81 manifolds x quantum theory (E41 1983) | 0.1 | 0.3 | 2.8 | 9.8 | 5.1 | 7.2 | 9.0 | Take-off in the 1980s, peak 1990s (Seiberg-Witten 1994) |
| 17 x 81 nonassociative rings x quantum theory (E44, B06) | 0.2 | 1.5 | 13.6 | 58.0 | 22.6 | 20.4 | 19.0 | Strong 1980s-90s wave (quantum groups, vertex algebras) |
| 14 x 81 algebraic geometry x quantum theory (E47 1991) | 0.1 | 0.5 | 2.6 | 10.7 | 11.7 | 22.1 | 25.1 | Steady growth from the 1980s, steeper after mirror symmetry |
| 05 x 14 combinatorics x algebraic geometry (E51, E56) | 0.1 | 0.5 | 1.4 | 2.9 | 4.9 | 10.5 | 19.6 | Accelerating after 2000; no visible step at 2008 or 2012 |
| 05 x 55 combinatorics x algebraic topology (E36 1978) | 0.1 | 1.2 | 1.4 | 1.1 | 1.7 | 3.4 | 6.0 | Step in the 1970s, second wave in the 2010s |
| 05 x 68 combinatorics x computer science (E73 1976) | 0.6 | 26.1 | 47.8 | 56.8 | 75.6 | 108.2 | 80.0 | Step in the 1970s |
| 11 x 22 number theory x Lie groups (E34 Langlands) | 1.5 | 5.8 | 11.3 | 9.8 | 9.0 | 11.4 | 12.1 | Step in the 1970s after the 1967-70 programme |
| 60 x 81 probability x quantum theory (E49 SLE 2000) | 0.4 | 2.8 | 18.9 | 15.5 | 9.9 | 12.3 | 17.9 | No signal at the SLE date |
| 37 x 94 dynamics x information (B17 1958) | 0.0 | 0.6 | 1.3 | 4.5 | 10.3 | 7.2 | 6.3 | Nothing before 1970 |

## Verdict

1. **Descriptive signal is real.** Eight of the eleven pairs above step up in the decade of, or shortly after, the seed events that name them (11x37, 05x37, 57x81, 17x81, 14x81, 05x55, 05x68, 11x22). Section-pair curves are a usable visual and a sensible first screen.
2. **A simple detector is not validated.** The statistic I tried (window-to-window jump in lift of at least 1.5) fired for 10 of 21 event-pair tests but also for 17 of 56 control transitions (30%). That difference is not significant, and the statistic is dominated by small-count noise in sparse early windows. A second statistic, the first window with at least 20 co-classified documents, falls in the 1970s-80s for both event pairs and controls. Neither separates events from background. Treat the curves as description, not detection.
3. **Two-digit sections are too coarse for some events.** SLE (E49) and the polynomial method (E51) leave no mark at section level; they would need class-level codes such as 60K35 or 52C. The next spike should query three-character classes (the API accepts `cc:37A`).
4. **Blind before about 1970.** Sections that did not exist in earlier MSC editions (37, 94) show zero documents in the 1950s-60s even for Kolmogorov-Sinai entropy (B17, 1958). Retroactive classification is partial in zbMATH Open. Anything before 1970 has to come from historiography (channel A) or the JFM-era records, not MSC counts.
5. **Retro-classification and MSC revisions confound birth dates.** A new section is itself an institutional marker (section 37 appears in the 2000 edition); a rise in a pair around 2000 can be a relabelling.

## What would make this a detector

- Class-level codes with documents counted per class, not per section.
- A null that matches pair size and growth (for example resampling documents within window, or comparing against the 20 closest pairs by marginal counts) and a Poisson or negative-binomial change-point test on per-10k frequency, not a lift ratio.
- The full 1,953-pair matrix, so that "what is surprising" is ranked against every pair rather than 35. The API was slow and sometimes returned 502s under concurrency; the zbMATH Open knowledge graph dump (about 1.6 GB on Zenodo, record 21497976) would make this offline work. It was not downloaded.

## Reproducing

`scripts/field-emergence/zbmath_counts.py` fills `zbmath_counts.jsonl` (resumable); `analyze_spike.py` reads that file and a metadata file written by the first script and writes `channel_b_spike.json`. Both use `curl` because Python's bundled certificate store rejected the API's certificate chain in this environment.
