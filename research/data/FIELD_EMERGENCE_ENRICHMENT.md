# Completing the event records: dates, people and works (strategy, 2026-10-18)

## Goal

For every event in `field-events-merged.json`, fill:
- the three dates (conceptual, methodological, institutional), each with evidence;
- the key people (originators, developers, systematisers) and their major works on this topic;
- aliases and search terms, so the page can find an event by the word a reader uses.

Nothing may be filled without a source. A blank with a note ("searched X, found nothing") is better than a guess.

## Principles

1. **Evidence over recall.** Every date and every person comes with a source (a bibliographic record, a history page or a database), not only the model's memory.
2. **Two independent passes.** A strong model and a second model research each event separately, without seeing each other. Agreement is the quality signal.
3. **Bibliographic records first.** Crossref, zbMATH Open, Open Library and archive.org give publication years that can be checked. History pages (MacTutor, Wikipedia, SEP) are second.
4. **Machine-checkable anchors.** The year a field's name first appears in a paper title (zbMATH, Crossref) and the year a classification code first exists give reproducible dates for the institutional date.
5. **Precision is recorded.** A date is a year, a range or a decade, never more exact than the evidence.
6. **Disputes are kept, not resolved.** If priority is contested, store both dates (private versus public) with the reason.

## What each date means, and where evidence comes from

- **Conceptual.** The earliest public statement of the idea. Use the publication date, not the date read or presented. Earlier private letters go in the note. Evidence: the primary paper or book in a bibliographic record.
- **Methodological.** The first time the tool was used on purpose on a target problem. Evidence: the paper that does it, found through histories and citation trails.
- **Institutional.** The first textbook or monograph, journal, named lecture series or ICM section, chair, or classification code for the field. Evidence: earliest title use (zbMATH and Crossref), MSC and Mathematical Reviews classification editions, ICM programmes, library catalogues.

## People and works

Per event, up to six people with a role (originator, developer, systematiser, popularizer), lifespan, a MacTutor or Wikipedia page, and one to three works relevant to this event only. A work counts only if it exists in a bibliographic record. A later pass can rank works by citation counts.

## Process

1. **Pilot.** 30 events across all periods and sources, researched by two independent passes (Opus and Sonnet), to measure how often the dates agree and how often evidence exists.
2. **Reconcile.** Agreement within a few years on the same evidence: accept. Disagreement: send to a third pass focused on the disputed date.
3. **Score.** Each date gets a grade: A (two passes agree, and a bibliographic record confirms), B (one source with a record), C (history page only), D (memory only, not shown as a date).
4. **Human audit.** A random 10% for you to check on the review page.
5. **Scale.** Run on all 557 events in batches of ten, with the same two passes.
6. **Publish.** The review page shows each date with its grade and source, the people and their works, and the aliases in search.

## Pilot status (2026-10-17)

The exact 30-event sample and three batches are preserved in
[`enrichment/pilot/`](enrichment/pilot/README.md). The six initial Opus/Sonnet
agents stopped on a session rate limit before writing complete outputs. At the
user's request, Codex then researched all 30 directly as a single source-led
pass. The [direct research ledger](enrichment/pilot/direct-research.json) and
[coverage report](enrichment/pilot/direct-report.md) are now present. This pass
has no independent agreement rate or A grades. The existing 557-event catalogue
has not been overwritten or published with these pilot fields. The
[pilot review page](../../public/field-emergence-pilot.html) shows the 30
researched events with source links and visible gaps.

## Direct scale-out (2026-10-17)

Codex directly researched ten further, non-pilot events in
[`batch-02-direct.json`](enrichment/batch-02-direct.json), preserving the pilot
denominator. The [combined review page](../../public/field-emergence-reviewed.html)
now displays 40 researched events. The other 517 remain pending; their existing
catalogue dates have not been promoted to evidenced dates. The
[batch-2 report](enrichment/batch-02-report.md) records the coverage and the
public-preprint versus journal-date distinctions.

## Milestone update (2026-10-18)

The current event format is [`MILESTONE_SCHEMA.md`](enrichment/MILESTONE_SCHEMA.md). Each event carries zero to eight ordered, evidenced milestones; zero marks an explicit source gap. Conceptual, methodological and institutional dates are derived from milestone roles; private letters and unpublished notes can only be precursors. The older flat schema below remains a description of the initial research ledgers, not the intended final catalogue format.

The [current status](enrichment/STATUS.md) is 147 events with cited milestones and 410 still without adjudicated milestones. Those 147 records contain 464 milestones; the [milestone preview](../../public/field-emergence-milestones.html) lists all 557 entries and visibly distinguishes researched records from open source gaps. A [bulk source audit](enrichment/BULK_SOURCE_AUDIT.md) has now run over all 410 pending entries, checking cached bibliographic metadata and obtaining new search leads, while keeping all historical dates open until their roles and priority are verified. The old 40-event page still shows the earlier flat research. The three pilot milestone batches, separate second direct batch and scale batches 42–52 have direct source checking, including publication-year distinctions and unresolved firstness questions. No A-grade two-pass agreement has been inferred from direct work.

## Original flat schema (per event)

- `canonicalName`, `aliases`
- `dates.conceptual | methodological | institutional`: `start`, `end`, `precision`, `confidence`, `evidence[]` (claim, source, url, kind), `note`
- `firstTermUse`: term, year, source
- `people[]`: name, role, lifespan, url, `works[]` (citation, year, doi or url, why it matters)
- `notes`: disputes and gaps

## Source-first strategy (2026-10-18)

Open-ended research per event is the expensive path. For the events still without milestones (batches 01-40), research now starts from reference pages, and bibliographic checks are spent only where a year matters.

1. **Reference pages first (no model).** `scripts/fetch_wikipedia_leads.py` stores the top three English Wikipedia articles per event (intro text, years). `scripts/fetch_mactutor_topics.py` stores the text of all MacTutor history topic pages. Princeton Companion is not online and is not used. SEP and nLab are added by agents when relevant.
2. **History-source entry (Sonnet/Haiku).** An agent reads the matched Wikipedia and MacTutor pages (plus MacTutor biographies of key people) and extracts stages, people, aliases and works, citing the page. Uncertain "firsts" stay open.
3. **Verified milestone.** Only first_statement, first_application and naming years are checked against Crossref, zbMATH, Open Library or arXiv, upgrading the evidence to bibliographic_record.
4. **Uncovered events.** Events with no usable page, or whose pages disagree, go to the full evidence-first research used for the pilot (Sonnet only, no Opus).
5. **Audit.** 10% sample for human check; milestone-level second pass by a different model before publication.

Pilot and batches 41-52 were completed by another session with direct source-led research (`pilot/milestones1-3.json`, `scale/milestones41-52.json`).
