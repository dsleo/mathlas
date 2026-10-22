# Field emergence enrichment status

As of 18 October 2026, the [milestone review](../../../public/field-emergence-milestones.html) covers all **557 catalogue entries**. Of these, **157** have directly checked, cited milestone lists with **489 milestones**: the 30 fixed pilot events, ten separate direct-batch events, and scale batches 41–52. The other **400** have no adjudicated milestones or derived dates. Of those, 191 have bibliographic leads awaiting interpretation and 209 still need a stronger source search. They are staged in **40 compact [review packets](queue/)**. Catalogue coverage must not be read as 557 researched histories.

The [coverage ledger](coverage.json) distinguishes researched records, candidate leads and source-search gaps. Candidate titles and inherited catalogue dates are unverified context, never promoted automatically to historical milestones. The [milestone schema](MILESTONE_SCHEMA.md) derives conceptual, methodological and institutional dates only from eligible, cited roles. An absent source or unresolved priority leaves the date blank. A-grade evidence still requires an independent agreeing pass; the direct records currently support B or C at best.

The [validator report](milestone-audit.json) covers 16 files and 157 records with **zero errors and 24 intentional warnings** where no defensible first public statement is assigned. The [work check](work-verification.json) inventories **883** milestone and person-work citations: 707 directly verified by title/year, 21 verified via a matching person-work entry, 23 flagged for title review despite year agreement, 104 links outside the metadata checker's supported services, nine titles without a confirmed year, and 19 milestone works without a direct record URL. The source-audit files beside each scale batch explain dated primary-document and publisher exceptions. Bibliographic identity is not proof of historical firstness.

Direct audits for [batch 41](scale/batch41-source-audit.md), [batch 42](scale/batch42-source-audit.md), [batch 43](scale/batch43-source-audit.md), [batch 44](scale/batch44-source-audit.md), [batch 45](scale/batch45-source-audit.md), [batch 46](scale/batch46-source-audit.md), [batch 47](scale/batch47-source-audit.md), [batch 48](scale/batch48-source-audit.md), and [batch 49](scale/batch49-source-audit.md) record key priority checks and remaining gaps. The [pilot agreement report](pilot/milestone-pilot-report.md) describes the earlier flat-date comparison; its result cannot be transferred to the milestone records.

The scalable workflow is to read one compact packet, verify source identity and contents, assign only supported roles, audit person and work links, then rebuild the coverage and review page. A Crossref/arXiv lookup already triaged 1,063 unique inherited citations: 317 strong and 20 plausible Crossref matches, 96 explicit arXiv IDs, and no close match for 643. A further [bulk audit](BULK_SOURCE_AUDIT.md) ran on **the then-410 pending events at once**: 309/309 cached lead appearances matched source title/year metadata, and all 210 previously lead-free events received a fresh top search result. That audit snapshot and the [prioritized review queue](bulk-review-queue.json) group 200 events with confirmed records, 29 with plausible new title leads, and 181 requiring targeted primary or history searches. All these findings remain candidates only. The remaining work is source-content reading, historical-role and priority adjudication, and an independent second pass for grade A and a new agreement statistic. Do not claim full historical enrichment until those steps finish.

Run from the repository root after another completed batch:

```sh
python3 scripts/validate_field_milestones.py --output data/collection/enrichment/milestone-audit.json
python3 scripts/verify_field_works.py
python3 scripts/build_field_milestone_review.py
```

No milestone-data commit has been made. Unrelated app-source edits in the shared checkout are outside this work.

## Update 2026-10-20

The 400 events counted as pending above already carry source-first milestone records (`sourcefirst/merged`, shown as the `source-first` tier in the explorer); "pending" here means not yet at the directly-checked bar. An independent pass over all 400 is in [`crosscheck/`](crosscheck/README.md): 525 of 565 dated milestones corroborate the source-first years; 40 differ and are listed in `crosscheck/summary.json`. Coverage now counts 563 events (557 catalogue entries plus the six focused additions FM1-FM6), of which 163 are directly checked.
