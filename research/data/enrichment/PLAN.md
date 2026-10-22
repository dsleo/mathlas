# Enrichment: remaining work, split into dispatchable items (2026-10-18)

**Rules for every item:** Haiku or Sonnet only (never Opus). Never put a personal email in an API request. Each item owns its output files; no two items write the same file. Nobody commits; Item 9 does that. Pass and fail are measured by `python3 -I scripts/validate_field_milestones.py <files>` (strict) and `scripts/validate_milestones.py` (light).

**State now:** 157 events have directly checked milestones (other session: `pilot/milestones1-3.json`, `scale/milestones41-52.json`, `batch-02-direct.json`). 400 events have source-first records (`scale/A_batch01-40.json`, normalised copies in `sourcefirst/A_NN.json`), unadjudicated. Strict validator on those 400: 0 structural problems left except the ones below.

| # | Item | Model | Input | Output (owned) | Done when |
|---|------|-------|-------|----------------|-----------|
| 1 | **Repair works lists** | Haiku, 4 agents of 10 files each | `sourcefirst/A_NN.json` events with strict errors "Invalid work citation" (83), "Expected 1–3 works; found 0" (82), "found 4" (6) | edits only the `works` fields in the same file | strict validator shows 0 work errors; no work added without a Crossref/zbMATH/Open Library/arXiv/archive.org record |
| 2 | **Fill empty notes and 10 bad people/URLs** | Haiku, 1 agent | the 10 events with empty notes and the 10 people with no biography URL (list from validator output) | same files | those errors are gone; URLs only from pages whose title names the person |
| 3 | **Thin events** | Sonnet, 3 agents (18 events each) | `sourcefirst/worklists.json` key `thin` (53 events with fewer than 4 milestones or fewer than 2 people with works) | `sourcefirst/thin_NN.json` (full replacement records) | each event has at least 4 milestones where history supports them, 2 or more people with works; gaps explained in notes |
| 4 | **Missing first statements** | Sonnet, 1 agent | `worklists.json` key `noFirstStatement` (16 events) | `sourcefirst/firststmt.json` | each event has a sourced first_statement or a note naming where it was searched |
| 5 | **Missing naming and institution anchors** | Haiku, 3 agents | the 102 events with no naming, consolidation or institution milestone (`sourcefirst/worklists.json`, key `noNaming`) | `sourcefirst/naming_NN.json` | a dated naming/institution/consolidation milestone with a record, or a note that none was found |
| 6 | **Disputed and unverified years** | Sonnet, 2 agents | notes fields with "unverified", "disputed", "vs" in `sourcefirst/A_NN.json`; also the Q5 "fifty years" claim and the arXiv 2507.12926 reference (did not resolve) | `sourcefirst/disputes.json` (per item: verdict, source, confidence) | each item resolved or marked unresolved with the search done |
| 7 | **Scripted year check of every cited work** | no model (script) | all works in `A_NN.json` and in the 157 direct records | `sourcefirst/work-check.json` | every work has status matched, mismatched or unreachable; mismatches handed to Item 6 |
| 8 | **Independent second pass for agreement statistics** | Sonnet, blind, 4 agents | a random 40-event sample (seed fixed), event name and summary only, never the first-pass output | `sourcefirst/second_NN.json` | agreement within 3 years computed per role against the first pass; grade A given only to agreeing items |
| 9 | **Merge, review page, commit** | one owner (main session) | all outputs above plus the 157 direct records | merged `milestones` file, rebuilt review page (aliases searchable), commit by explicit paths | page lists 557 events with a tier label (direct, source-first, second-passed); app-source edits from other sessions left alone |
| 10 | **Human audit** | you | the review page | audit marks | a 10% random sample checked; disagreements fed back to Items 3–6 |

**Order:** 1, 2, 7 first (they unblock a clean validator). Then 3, 4, 5, 6 in parallel (disjoint files). Then 8 (needs 3–6 finished so the comparison is against final text). Then 9, then 10.

**Dependencies:** 6 uses 7's mismatches. 8 uses 3–6. 9 uses everything. Items 1 and 2 touch the same files as 3 and 4, so run 1 and 2 before them or merge by event id.

**Known weaknesses to keep in mind:** Haiku records are thinner than Sonnet's. Wikipedia and MacTutor give history, not priority. Many naming years are missing. Nothing here yet gets grade A; that needs Item 8.


## Status after items 1-10 (2026-10-19)

Done: items 1-8 and the follow-ups (restore dropped people, review year mismatches, apply dispute fixes, fill gaps). Merged records are in `sourcefirst/merged/M_NN.json` (source of truth for the 400 source-first events); the explorer reads them. Strict validator: 0 errors on all 400.

Still open: your audit (item 10); 60 unresolved dispute or mismatch items; 16 events without a naming, consolidation or institution milestone; 19 low-confidence first statements; about 47 dropped people not restored; second-pass disagreements beyond 3 years listed in `second_blind/agreement.json`; no grade A date yet; a Sonnet re-pass of the thinnest Haiku records, if wanted.
