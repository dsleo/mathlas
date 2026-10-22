# Mathlas

**An atlas of mathematics through time.** Each island is a field of mathematics. It appears at the first recorded event in that field and grows with every event after it, from 2000 BCE to 2025. Live at https://dsleo.github.io/mathlas/.

The map starts at the present day. Press the gear (bottom right) for search, the time-lapse, themes, the event-type legend and credits. Drag the time rail to watch the fields emerge. Click an island for its events, an event for its card, and double-click the card for the full "core sample" (every dated milestone with its evidence).

## What is on the map

| | |
|---|---|
| **553 events** | dated, typed episodes in which a mathematical idea, field or technique appears or changes |
| **33 islands** | fields (the lanes of Proofscape's connection map), from Algebra and Geometry to Information & cryptography |
| **3,002 milestones** | the dated steps inside the events, with **4,433 cited pieces of evidence** |
| **1,180 people** | named in the events; **40 landmark mathematicians** stand as statues (37 with a portrait) |
| **624 links** | between fields, each tied to the event that created it |
| **Time span** | 2000 BCE to 2025 |

### The seven kinds of event

Every event is one of seven types. The type says *how* mathematics changed, and each has its own birth animation on the map.

| Type | Events | What happens | Examples |
|---|---:|---|---|
| **Technique transfer** | 203 | A method built in one field solves problems in another. Drawn as a **bridge** between islands. | Archimedes' mechanical method for areas and volumes (physics to geometry); Perfectoid spaces and tilting (Scholze); Public-key cryptography |
| **Birth by fusion** | 101 | Two fields combine and a new one is born at the join. | Functional analysis; Combinatorial group theory; the four colour problem (Kempe and Heawood) |
| **Birth by abstraction** | 91 | A pattern is lifted out of concrete problems and becomes a field of its own. | Graph theory from the Königsberg bridges; Algebraic topology (Betti numbers to homology groups); Group theory from polynomial equations |
| **Import from outside** | 84 | A field takes in a problem or structure from physics, economics or computing. | Probability from games of chance; Newton's *Principia*; Game theory; Shor's algorithm |
| **Dictionary, analogy** | 49 | A precise correspondence is found between two fields. | Weil's dictionary; The Langlands programme; Monstrous moonshine |
| **Reification** | 18 | An operation or construction is turned into an object that can itself be studied. | Axiomatic set theory (Zermelo); Elementary topos theory; Arithmetization of analysis |
| **Split** | 7 | A subfield separates and becomes independent. | Computer science separates from mathematics; Computational complexity; Al-Tusi makes trigonometry independent of astronomy |

(Six early "field emergence" records are counted with birth by abstraction and one "field combination" with birth by fusion.)

### Reading the map

- **Island size** is the cumulative number of events in the field; **position** keeps strongly linked fields close (see below).
- **Bridges** between islands are technique transfers (thicker means more of them). **Dotted and dashed chords** are the other kinds of link, coloured by type.
- **Large symbols** mark each island's main events (155 in all, never two the same on one island). The rest are dots with names that appear as you zoom in.
- **Statues** are landmark mathematicians, shown with a portrait where a reusable one exists. The same person can stand on several islands.

## Methodology

**1. The catalogue of events.** The 553 events come from the field-emergence catalogue built for [Proofscape](https://github.com/dsleo/proofscape): a hand-seeded list of moments when a field, a technique or a bridge between fields came into being, extended batch by batch. Each event records its type, the fields it draws from, the field it produces, and a short account of what happened. It is a curated selection, not an exhaustive census of mathematics.

**2. Dated milestones with evidence.** An event is not a single date. It is an ordered list of milestones, each with a role (precursor, first statement, first application, key development, consolidation, naming, institution, recognition), a year, and cited evidence. A milestone needs evidence, and publication year governs the date, not the year of a talk. Years come from bibliographic records (Crossref, zbMATH, Open Library, archive.org, arXiv) where they exist, and from history pages (MacTutor, Wikipedia) otherwise. Private letters and unpublished notes are precursors, never the start. An event sits on the map at its first public statement, derived by rule from its milestones.

**3. Two tiers of checking.** 161 events are *directly checked*: each milestone was read against its source and audited. The other 392 are *source-first*: milestones assembled from cited sources but not yet held to that bar. Where a caveat remains it is shown behind an "i" icon on the milestone; confidence grades and bookkeeping notes stay in the data and are not shown.

**4. Fields.** Each event belongs to the field it *produces*. The 33 fields are the lanes of Proofscape's connection map. A field's island appears in the year of its first event.

**5. Growth.** Island area follows the cumulative event count, with each event fading in over about ten years so that growth is smooth when you scrub.

**6. Placement.** Islands are laid out by minimising total link length, where each pair of fields counts with the square root of the number of links between them, subject to islands never overlapping at their final size (L-BFGS on a penalty function, 24 random restarts, `scripts/layout_field_film.py`). So fields that exchange more techniques sit closer, and no one pair dominates.

**7. Links.** A link is drawn between two fields for every event that takes input from one and produces output in the other, using the same classifier that assigns events to fields.

**8. Terrain.** Each island is drawn once, at its final size, with the terrain generator of Proofscape's proof map (contours, rivers, forests, mountains) and scaled as the field grows.

**9. Symbols and landmarks.** An island shows `1 + 1.05 sqrt(n)` main events (at most nine), chosen by how much the record says about them (milestones, named people, direct checking). Symbols are curated per event (`GLYPH_OVERRIDE`) and unique within an island. A mathematician becomes a landmark when they are the primary person (first listed, originator or systematiser) in at least three events; they stand on each island where that holds, at most four per island. These choices are scored, not curated by a historian, so they are the least settled part of the map.

**10. Portraits.** Fetched from Wikimedia Commons and kept only under public-domain, CC0, CC BY or CC BY-SA licences, with author and source recorded and shown under the © button. Where no reusable portrait exists (for example Eudoxus, for whom no likeness survives) the statue keeps a plain bust.

### Limits

- Selection bias: the catalogue favours what is well documented in English-language and Western sources, although it includes Babylonian, Greek, Chinese, Indian and Islamic work.
- Event types are an editorial classification, and many events could fairly carry two.
- Dates are the first public statement, which is often later than when an idea was first used, and may be earlier than its acceptance.
- Source-first events have not been independently verified milestone by milestone.

The raw research behind the events (catalogues, milestone research per event, validation scripts) is archived in [`research/`](research/).

### Corrections

Every event card (and its core sample) has a pencil (✎) at the top right that opens a pre-filled GitHub issue (event, milestone, the page you were on, and a short form: what needs fixing, what it should say, a source). A GitHub account is needed. To accept one, add the label `accepted` and close the issue as completed: a workflow then opens a pull request that records it in `public/data/corrections.json`. The pull request body carries a ready-made brief (what was reported, the current record, the source offered): ask an AI agent to "apply the brief in this pull request" (it follows [`AGENTS.md`](AGENTS.md)) or edit `data/events.json` by hand, rebuild, and merge. Accepted corrections show in the margin of the milestone, credited to the contributor.

## Licence

CC0 1.0 for the code and our own data; portraits, fonts and source-derived text keep their own terms (see `NOTICE.md`).

## Build

The committed `public/` is the built site. To regenerate it:

```bash
npm install
npm run build          # data/events.json -> public/
npm run layout         # optional: recompute island positions (needs numpy, scipy)
npm run portraits      # optional: fetch missing portraits from Wikimedia Commons
npm run serve          # http://localhost:5174
```

- `data/events.json` holds the 553 events (embedded JSON).
- `scripts/build_field_film.py` assigns events to fields, picks main events, symbols and landmarks, and writes the page from `scripts/film_template.html`.
- `scripts/build_film_art.mjs` draws each island with the terrain generator in `src/`.

Deep links: `#e=<event id>`, `#p=<person>` or `#f=<field>`, plus `&core` (open the core sample) and `&t=<year>`.
