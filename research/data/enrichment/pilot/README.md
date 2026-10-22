# Field emergence enrichment pilot

This directory preserves the exact 30-event sample selected on 2026-10-17 for
the two-pass pilot. `manifest.json` maps the temporary `P###` identifiers to
stable IDs in `field-events-merged.json`. The sample has 9 events before 1850,
6 from 1850–1929, 9 from 1930–1989, and 6 from 1990 onward. It includes
Boolean algebra, non-Euclidean geometry, and the Langlands programme. It spans
seven source families, but source families were not evenly sampled.

`pilot1.json` through `pilot3.json` are the original inputs sent to three Opus
and three Sonnet agents. They include the catalogue's current dates and works,
which may be inaccurate and can anchor both passes. The `blind-pilot*.json`
files keep the same events and context while omitting those existing claims.
Use the blind inputs for fresh independent passes. Keep the A and B results in
separate files (`A1.json` to `A3.json`, `B1.json` to `B3.json`); neither pass
should read the other's files before both are complete.

The first agent run hit a Claude session rate limit on 2026-10-17. The user
then requested direct work without waiting. `direct-research.json` is the
resulting source-linked ledger for all 30 events; `direct-report.md` gives
coverage and major corrections. `scripts/build_direct_enrichment_pilot.py`
recreates and validates it. The six A/B pass files were subsequently written,
along with `three-way-comparison.json`. Those flat dates are research inputs,
not a final verdict on a field's single birth date.

The current format is [`MILESTONE_SCHEMA.md`](../MILESTONE_SCHEMA.md): three
to eight dated stages per event, with the old three dates derived by role.
All three fixed pilot batches now have completed milestone outputs:
`milestones1.json`, `milestones2.json`, and `milestones3.json`. Their direct
audits are the corresponding `milestonesN-review.md` files. Scale batches
should use `milestonesN.json` as output names. Staged `scale/batchNN.json`
files are research inputs, not completed outputs.
The separate second direct batch now has ten completed records in
[`../second/milestones1.json`](../second/milestones1.json), audited in
[`../second/milestones1-review.md`](../second/milestones1-review.md). It does
not alter the fixed 30-event pilot denominator.

From the repository root, validate and build a preview of all completed
milestone outputs with:

```sh
python3 scripts/validate_field_milestones.py --output data/collection/enrichment/milestone-audit.json
python3 scripts/verify_field_works.py
python3 scripts/build_field_milestone_review.py
```

The metadata checker distinguishes verified records, unavailable services,
title comparisons needing review, and works with no direct record link. Its
result does not prove that the work supports the historical interpretation.
The [milestone preview](../../../../public/field-emergence-milestones.html)
contains completed, schema-valid batches only. The earlier direct-pass pages
remain available while the milestone sample is incomplete.

`scripts/build_field_emergence_pilot_review.py` creates the read-only
[`pilot review page`](../../../../public/field-emergence-pilot.html) and its
public JSON companion. It shows all three dates, including blank-date search
notes, plus aliases, linked sources, people, works, and priority notes. The
page covers only the 30 researched pilot events.
The later [combined review page](../../../../public/field-emergence-reviewed.html)
adds a separate second batch of ten without changing this fixed pilot sample.

For each event, produce `pid`, `canonicalName`, `aliases`, `dates`,
`firstTermUse`, `people`, and `notes`. Each of the three dates needs `start`,
`end`, `precision` (`year`, `range`, `decade`, or `unknown`), `confidence`,
`evidence` (each with `claim`, `source`, `url`, and `kind`), and `note`. Leave
`start` empty with `precision: "unknown"` and a note listing searches when
evidence is absent. Conceptual means the earliest **publicly published**
statement; methodological means the first purposeful application to a target
problem; institutional means the first named textbook, journal, lecture
series, ICM section, chair, classification code, or paper title. Publication
year governs even if presentation or private correspondence came earlier.

Every person needs an independent biographical source, a role, a lifespan when
known, and one to three works relevant to this event with bibliographic record
links. Preserve priority disputes in `notes`; do not turn private letters into
public dates. Bibliographic records from Crossref, zbMATH, Open Library, and
archive.org are preferred for dates and works. History pages can support a
date when no record is found; unsupported recollection cannot.

After both passes are complete, run:

```sh
python3 scripts/analyze_enrichment_pilot.py > pilot-analysis.json
```

The analyzer checks basic schema and source links, counts evidenced dates,
compares date intervals within three years, and lists disagreements. Its
`recordLinked` flag means only that a link points to a bibliographic service;
it does **not** verify that the linked record supports the exact claim. Check
that manually before assigning A/B/C grades or publishing dates. Resolve
disagreements with a third pass focused on that one date. Report agreement
among dates with two evidenced passes and evidence coverage over all 30 events
for each date type; do not treat missing pairs as disagreements.
