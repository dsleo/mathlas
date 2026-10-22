You are researching ten mathematical field-emergence events. Work from the
assigned `blind-pilotN.json` input only. Read section 3 of
`data/collection/FIELD_EMERGENCE_OVERVIEW.md` and the strategy in
`data/collection/FIELD_EMERGENCE_ENRICHMENT.md`. Do not read the original
`pilotN.json`, `control-anchors.md`, `reconciliation-candidates.json`, or any
other pass output. Existing catalogue dates and works are unverified.

For each event, return one JSON object with `pid`, `canonicalName`, `aliases`,
`dates`, `firstTermUse`, `people`, and `notes`. `dates` must contain
`conceptual`, `methodological`, and `institutional`. Each date is an object
with `start` (integer year or null), `end` (integer or null), `precision`
(`year`, `range`, `decade`, `unknown`), `confidence` (`high`, `medium`, `low`),
`evidence` (a list), and `note` (text). Every evidence item has `claim`,
`source`, `url`, and `kind` (`primary`, `secondary`, or `database`).

- Conceptual: earliest **published public** statement of the event's idea.
  Use publication date, not presentation date. Record earlier private letters
  and priority disputes in the note.
- Methodological: first purposeful use of the relevant tool on a target
  problem. Cite the work that actually performs the use.
- Institutional: earliest named textbook/monograph, journal, lecture series,
  ICM section, chair, classification code, or paper title. For a term search,
  state the corpus searched and phrase the result as the earliest indexed
  title found, not an absolute claim of first use.

If a date cannot be evidenced, set `start` and `end` to null,
`precision` to `unknown`, `evidence` to an empty list, and write in `note`
which sources and terms you searched. Do not create a date from memory.

For `firstTermUse`, give `term`, `year`, and a direct source link only when the
title record supports it; otherwise use null. For `people`, include no more
than six mathematicians, each with `name`, `role` (`originator`, `developer`,
`systematiser`, `popularizer`), `lifespan` (or `unknown`), a biography `url`,
and one to three works. Each work needs `citation`, integer `year`, a DOI or
record `url`, and `whyItMatters` tied to this event. Omit a person if the
required source and work record cannot be found. Keep contested claims in
`notes` without resolving them by guess.

Use bibliographic records such as Crossref, zbMATH Open, Open Library,
archive.org, publisher catalogues, and journals for works and publication
dates; use MacTutor, SEP, and similarly sourced histories for context. Check
that each linked record actually matches the author, title, and year. Ancient
works may have no modern bibliographic record: keep precise ancient dates
empty if necessary and explain the evidence gap. Do not quote more than a
short phrase from any source.

Write a valid JSON list to the assigned output file, with one item for every
assigned `pid`. Work only in your output file. Report counts of evidenced
conceptual, methodological, and institutional dates on completion.
