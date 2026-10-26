# Milestone research status

The committed source catalogue, `data/events.json`, currently contains **553 events**:
**192** are marked `direct` and **361** are marked `source-first`. Together they
have **3,077 milestones** and **4,759 evidence entries**. Each milestone has at
least one evidence entry. These counts describe the present repository; they
are not a claim that every historical priority or source has had an independent
second review.

`python3 scripts/validate_events.py` checks IDs, milestone roles and evidence,
dated ordering, derived and displayed dates, and reciprocal event links. It
checks internal consistency, not whether a source proves the historical claim.
The rules are in [MILESTONE_SCHEMA.md](MILESTONE_SCHEMA.md).

`coverage.json` is a **historical research ledger** from an earlier catalogue
snapshot: it reports 563 records and a 163/400 researched/candidate split. It
is retained for provenance and must not be treated as a current coverage count.
The per-batch research files and original audit scripts referenced by older
status reports are absent from this checkout; see [research/README.md](../README.md).

The [cross-check summary](crosscheck/README.md) is likewise a preserved report
from a 2026-10-20 independent pass. Its listed disagreements are useful
research leads, but the underlying packet files are not committed here, so
the headline corroboration totals cannot be reproduced from this checkout.
Candidate records and title/year matches do not establish historical firstness.

Review batches A1, A2, B1, B2 and C (`review/`) and round 2 (`R2-*.md`) gave the highest-ranked events a direct review (round 2 promoted 8 more); the ranked worklist is `coverage_report.md`, and `crosscheck/ADJUDICATION.md` and `REVERIFY.md` record the cross-check leads and their independent re-check. Next research work: review the listed disagreements against primary and
bibliographic sources, adjudicate priority and milestone roles, then make a
fresh independent pass over the current 553-event catalogue. Record the new
pass and its source packets in this repository before publishing new agreement
statistics.
