# Field emergence: how the inventory was built (2026-10-19)

The same text, with live numbers, is in the explorer page's "How this was built" panel (`public/field-emergence-explorer.html`).

## 1. The question

When and how were mathematical fields born or merged? A "field event" is a birth by abstraction (group theory from polynomial solving), a birth by fusion, a technique transfer (Green–Tao style), a dictionary or analogy, a reification, an import from outside mathematics, or a split. The inventory records each event with dated milestones, the people behind it, their works, and a source for every claim. It also estimates how complete it is.

## 2. What an entry contains

- **Type, source fields, target fields**, a one-line reason it was listed (catalogue text, not verified).
- **Milestones** (3 to 8, ordered by year). Each has a role, year, label, work, people, a sentence of description, evidence links, and a confidence.
- **Roles:** precursor, first_statement (earliest public statement; publication year governs, never a talk or private letter), first_application, key_development, consolidation (first textbook or survey), naming (first title using the field's name), institution (journal, chair, classification code), recognition.
- **Two displayed dates** (changed 2026-10-19). The headline is *idea first stated* = earliest first_statement. The second, *took hold*, is the earliest later milestone: first application, key development, naming, textbook or institution. It is shown as "same period" when under five years after the idea. The three schema dates (conceptual, methodological, institutional) are still stored in the data by rule, but the first-applied and named dates coincide with the idea date in a third to two fifths of events and are not reproducible enough to headline: on the blind sample the idea date agreed within three years in 83% of cases, the took-hold date in 51%, the naming date in 44%. A missing source leaves a date blank; fallbacks are marked "≈".
- **People** (up to 6) with role (originator, developer, systematiser, popularizer), a biography link, and 1 to 3 works each, every work with a year and a URL.

## 3. Pipeline

1. **Strategy and seeds.** Two hand-built seed sets (77 and 42 events) with sourced citations, every citation checked by search. They are a calibration set, not the target list.
2. **Five discovery channels were designed:** history sources (A), classification counts (B), citation novelty (C), reading by language models (D), formal libraries (E). A and B were built. C and D were not. E (Mathlib) was dropped.
3. **Channel B (zbMATH classification counts).** A change-point detector on counts of papers per pair of MSC classes flagged 54 of about 24,000 pairs and recovered none of the 86 gradable seed events. Its only use is ranking and dating, not discovery.
4. **Channel A (history harvests).** Three harvests read MacTutor history topics, ICM and prize records, and Quanta and expert blogs: 240 candidates. Each candidate was checked twice by independent passes. Both accepted 141, the passes split on 32, both rejected 46, and 6 turned out to be seed events. About a third of proposals were not real events, which is why two passes are needed.
5. **Completeness estimate.** For four periods (before 1850, 1850–1930, 1930–1990, 1990–2026) two blind harvests (Wikipedia, and MacTutor/Stanford Encyclopedia or Quanta/blogs) were matched against each other. This gave 513 verified events and an estimated 526 to 741 at this granularity. The estimate is probably low, because both harvests retell the same historiography.
6. **Merge.** The seeds and verified harvests were de-duplicated into 557 entries.
7. **Enrichment with milestones.** Every event gets a milestone list instead of one "birth date", because careful sources disagree on a single date when an event spans several stages (group theory: Lagrange 1770, Galois 1830/1846, Cayley 1854).
   - **157 events were checked directly**, one by one, by a separate research session (a 30-event pilot, then batches).
   - **400 events were built source-first**: an agent reads the Wikipedia and MacTutor pages, extracts stages, people and works, then confirms the year of each work behind a first statement, first application or naming in Crossref, zbMATH, Open Library, arXiv or archive.org, and upgrades the evidence from "history page" to "bibliographic record". Uncertain "firsts" stay open with a note.
8. **Verification passes** (all on the 400): a strict schema validator (0 errors); a scripted check of 3,708 cited works against bibliographic metadata; a review of every flagged year mismatch; a re-research of every flagged or disputed claim; repair of invalid or unverifiable works; an attempt to restore people who lost their works; targeted searches for missing naming, institution and first-statement milestones.
9. **Independent second pass.** A random, fixed sample of 40 events was researched again blind (event name and a short summary only, no sight of the first pass) and compared.
10. **Human audit.** The explorer has "Looks right / Looks wrong / Not sure" for every entry and a 56-event audit sample.

### Chronology and connection rules (added 2026-10-19)

- Nothing that builds on an idea can precede its first statement. A naming, textbook, institution, application, development or recognition milestone dated before the earliest first statement is reclassified as a precursor (`scripts/chronology.py`).
- Displayed dates may fall back, and say so: "first applied" falls back to the earliest later key development; with no first statement the earliest dated milestone is shown as the idea date. A fallback is marked with "≈" and a basis line.
- Connected events are strict and directional: an earlier event's result field must be a later event's input field, the field name must be distinctive (in at most 8 events), and the gap at most 80 years; or two events share both a source and a result field. The connection map draws these links.

## 4. Results so far

| Measure | Value |
|---|---|
| Events | 557 (157 checked directly, 400 source-first) |
| Milestones | 2,835 (489 direct, 2,346 source-first) |
| People | 1,902 (312 direct, 1,590 source-first) |
| Evidence items | 4,243: 2,417 bibliographic records, 1,795 history pages, 31 primary texts |
| Strict validator on the 400 | 0 errors |
| Works checked by script | 3,708: 1,728 verified, 973 not checkable by the script, 395 without a record URL, 74 year mismatches (most are reprints), the rest need title review |
| Flagged claims reviewed | 186 verdicts: 81 confirmed, 48 corrected, 57 unresolved; a further fix pass settled 71 of 131 items and left 60 unresolved |
| Mismatch review | 74 cases: 44 reprint or edition differences, 3 wrong years, 7 reviews mistaken for the book, 20 unresolved |
| Blind second pass | 40 events. Idea date agrees within 3 years in 30 of 36 comparable cases; the took-hold date in 20 of 39; the separate naming and consolidation date in only 14 of 32 |
| People restored | 25 of 72 who had been dropped for lack of a checkable work |

## 5. Evidence levels

- **Checked directly:** milestones read and checked one by one.
- **Source-first, unadjudicated:** built from reference pages with years checked in bibliographic records. Priority is not independently confirmed.
- **Catalogue only:** nothing on this tier is shown as a verified date.
- **Grades** on directly checked dates: A needs an independent pass that agrees, B one bibliographic record, C a history page only, D memory only (not shown as a date). No date is graded A yet.

## 6. Limits to keep in mind

- The inventory is what standard sources record, at the granularity those sources use. It is not every possible field event.
- Wikipedia and MacTutor shape which stories get told. They give history, not proof of priority.
- A year in a bibliographic record can be a reprint, translation or review. The method keeps the original publication year for first statements and first applications.
- Older material (before about 1868) is poorly covered by zbMATH, and ancient and medieval works often survive only as editions. Many of these "firsts" stay open.
- Batches 17 to 40 were written by the smallest model and are thinner than the earlier Sonnet batches (in a first comparison, 3.3 milestones and 2.2 people per event against 6.9 and 4.4); a stricter brief and later gap-filling narrowed but did not close that difference.
- The agreement between two passes is high for the first statement, moderate for first application, and low for naming dates, because "naming" and "textbook" are definition-dependent.
- Language models wrote the summaries and extracted claims; they were constrained to sourced evidence, but the human audit is the final check.

## 7. Where things are

- Data: `data/collection/field-events-merged.json` (catalogue), `data/collection/enrichment/` (records, worklists, verdicts), `public/field-emergence-explorer.html` (the explorer).
- Schema: `data/collection/enrichment/MILESTONE_SCHEMA.md`. Plan and status: `PLAN.md`, `STATUS.md`.
- Scripts: `scripts/validate_field_milestones.py`, `verify_field_works.py`, `merge_sourcefirst.py`, `merge_gaps.py`, `build_field_explorer.py`.
