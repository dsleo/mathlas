# Milestone schema for field events

Replaces the three single dates (conceptual, methodological, institutional) with a short, ordered list of dated milestones, each with a role and evidence. The three old dates are then derived by rule, so older views still work.

## Why

The pilot showed that two careful passes disagree about a "birth date" mostly because an event spans several phases (group theory: Lagrange 1770, Galois 1830/1846, Cayley 1854; Boolean algebra: Boole 1847, Stone 1936). A single date forces a choice. A list of roles does not.

## Per event

- `pid` / `eventId`, `canonicalName`, `aliases`
- `phases` (optional): short labels when the event bundles stages, for example `["Boole's algebra of logic", "Stone duality"]`
- `milestones`: 0 to 8 items, ordered by year (see below). Zero is valid when research has not established a dated event; record the searches and gap in `notes` / `searchedSources`.
- `people`: up to 6 key mathematicians, each `{name, role, lifespan, biographyUrl, works: [{citation, year, url, whyItMatters}]}` with works relevant to this event
- `notes`: disputes and gaps

## Milestone

```
{
  "role": one of the roles below,
  "phase": optional phase label,
  "year": start year (negative for BCE) or null,
  "endYear": optional end of a range,
  "precision": "year" | "range" | "decade" | "unknown",
  "label": short name of the milestone, for example "Galois' memoir published",
  "work": "author, title, venue, year" or null,
  "people": ["names"],
  "description": one sentence in your own words,
  "evidence": [{"claim", "source", "url", "kind": "bibliographic_record" | "history_page" | "primary_text" | "primary_publication" | "primary_archive"}],
  "confidence": "high" | "medium" | "low",
  "note": optional
}
```

## Roles (controlled vocabulary)

- `precursor`: an earlier idea, private work or unpublished result that is not the public start (a note, not a date to rank)
- `first_statement`: the earliest public statement of the idea (publication year governs, not the date a talk was given)
- `first_application`: the first purposeful use of the idea or tool on a target problem
- `key_development`: a result or extension that made the idea matter (for example a proof of a main theorem)
- `consolidation`: the first systematic treatment: a textbook, monograph, survey or course
- `naming`: the first use of the field's name in a title, or the term's coinage
- `institution`: a journal, chair, lecture series, ICM section or classification code that names the field
- `recognition`: a prize or conference that marks acceptance (optional)

## Rules

1. No milestone without evidence. A milestone with unknown year is allowed only for a precursor or when the note says what was searched.
2. One milestone per distinct thing: do not repeat the same paper under two roles unless it truly plays both (a note says so).
3. Private versus public: private letters and unpublished notes are `precursor` milestones.
4. Prefer bibliographic records (Crossref, zbMATH, Open Library, archive.org, arXiv) for years; use history pages when no record exists.
5. At least one `first_statement` and, when the field is in the MSC era, a `naming` or `institution` milestone should be attempted; if not found, say so in the notes.
6. A search result is a **candidate**, not evidence that a milestone or priority claim is true. Keep candidate works outside `milestones`; promote one only after checking its identity, year, event relevance and the specific role it supports.
7. Catalogue dates are research leads only. A zero-milestone record has no derived dates and must say which sources were searched. Do not create extra milestones to reach a quota.

## Derived dates (so older views keep working)

- conceptual = earliest `first_statement`; if none, null
- methodological = earliest `first_application`; if none, null
- institutional = earliest of `naming`, `consolidation` and `institution`
- `precursor` and `recognition` never set a derived date.

The source catalogue uses `shown.conceptual.y` and `y` for the map date. When
there is no dated first statement, these may fall back to the earliest dated
milestone, including a precursor. Such a map date is an approximate navigation
aid, not a verified public start: `derived.conceptual` remains null,
`approx` must be true, and the displayed basis must say that no first
statement was found. This distinction is especially important for ancient
records whose surviving evidence gives a broad period rather than a precise
publication date.
