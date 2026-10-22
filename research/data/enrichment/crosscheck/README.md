# Independent cross-check of the source-first records (2026-10-20)

`milestones53.json` to `milestones87.json` hold an independent bibliographic pass over 400 events (Crossref, arXiv, MacTutor, Wikipedia, SEP), run in 35 packets. They are **not** in `scale/`, so they do not feed the coverage ledger or the explorer: each has about 1.4 milestones against 5.9 in the matching source-first record, and promoting them would have replaced richer records with thinner ones.

Use: [`summary.json`](summary.json) compares every dated milestone with the source-first record of the same event. 525 of 565 dated milestones (93%) fall within one year of a source-first year, so the source-first years are independently corroborated. The 40 others are listed with their evidence URLs; each is either a new fact or a conflict to adjudicate. Eight milestones are undated; 40 events came back with no milestone (no verifiable source reachable).

Caveats: most evidence is a Crossref/arXiv record (title, author, year), not the paper text; Wikipedia/MacTutor-only items are medium or low confidence. The agents also reported inherited-citation errors (e.g. Turing 1937 not 1936 in Crossref, Euler's Konigsberg paper published 1741, Ruffini 1809, Argand 1806) that are worth checking against the catalogue.
