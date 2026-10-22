# Mathlas

An atlas of mathematics through time. Each island is a field; it appears at its first recorded event and grows with every event after it. Bridges are technique transfers; dotted chords are the other links between fields. Zoom in for the events, the landmark mathematicians and their portraits.

Open `public/index.html` through any static server (`npm run serve`, then http://localhost:5174). Press the gear for search, the time-lapse, themes and event types.

## Licence

CC0 1.0 for the code and our own data; portraits, fonts and source-derived text keep their own terms (see `NOTICE.md`).

## Build

The committed `public/` is the built site. To regenerate it:

```bash
npm install
npm run build          # data/source/field-emergence-explorer.html -> public/
npm run layout         # optional: recompute island positions (needs numpy, scipy)
npm run portraits      # optional: fetch missing portraits from Wikimedia Commons
```

- `data/source/field-emergence-explorer.html` holds the 553 recorded events (embedded JSON). It comes from the Proofscape field-emergence work.
- `scripts/build_field_film.py` assigns events to fields, picks main events and symbols (`GLYPH_OVERRIDE`) and landmark mathematicians, and writes the page from `scripts/film_template.html`.
- `scripts/build_film_art.mjs` draws each island with the terrain generator in `src/` (shared with Proofscape's proof map).
- Portraits are reused only under public-domain, CC0, CC BY or CC BY-SA licences, with the author and source in `public/data/portraits.json` and shown under the © button.

## Deep links

`#e=<event id>`, `#p=<person>` or `#f=<field>`, plus `&core` (open the core sample) and `&t=<year>`.
