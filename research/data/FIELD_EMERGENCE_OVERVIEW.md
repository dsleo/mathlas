# How mathematical fields are born and merge

A plain-language overview of the whole project.
Written for reading on a phone.
Status as of 17 October 2026.

---

## 1. The question

Mathematics did not appear all at once.
New fields were born from old ones.
Group theory came out of solving polynomial equations.
Algebraic topology came from joining algebra and topology.

Sometimes a result falls only when techniques from distant fields are combined.
Green and Tao proved the primes contain long arithmetic progressions
by mixing combinatorics, Fourier analysis, ergodic ideas and number theory.

**The goal:** build a dated, sourced list of such events,
from antiquity to now,
and say honestly how complete the list is.

This is a sister project to Proofscape's proof-diversity work.
There we compare different proofs of the same theorem.
Here we ask how whole fields appeared and merged.

---

## 2. Why "find all of them" is hard

No master list exists.
So we cannot just check our list against the truth.

Our answer is to **measure completeness**, not claim it.
We run several independent ways of finding events,
then ask how many known events each way recovers
and how much the ways overlap.

---

## 3. What counts as an event

One event is one dated case where a field was born
or where fields were joined.

### The seven event types

- **Birth by abstraction.**
  A recurring pattern becomes an object of its own.
  Example: groups, from permuting roots of equations.
- **Birth by fusion.**
  A field is created by joining others.
  Example: algebraic topology.
- **Technique transfer.**
  A tool from field A settles a question in field B.
  Example: Furstenberg's ergodic proof of Szemerédi's theorem.
- **Dictionary or analogy.**
  A systematic correspondence is found and then used.
  Examples: Weil's analogy, the Langlands programme.
- **Reification.**
  A field's methods become a theory in their own right.
  Example: category theory.
- **Import from outside.**
  Physics, games or engineering supply the idea.
  Example: gauge theory and four-manifolds.
- **Split.**
  A sub-area becomes its own discipline.
  Example: computer science.

### The three dates

"When was it born?" has several answers.
So each event keeps three dates.

- **Conceptual.**
  The first object, definition or statement of the idea.
- **Methodological.**
  The first time the tool was used on purpose on the target.
- **Institutional.**
  The first named chapter, textbook, journal, chair or MSC code.

For group theory these dates are decades apart.
Merging them would make every "birth date" an argument.

---

## 4. The five ways of finding events

We call them channels.
Each fails in a different way, which is the point.

**A. History.**
Read histories of mathematics, prize citations and ICM sections.
Very reliable, but only as complete as historians were.

**B. Classification counts.**
Mathematics papers carry MSC codes (subject labels).
Count how often two labels appear on the same paper, decade by decade.
A pair that suddenly takes off may mark a new combination.
Good from about 1970 on. Blind before.

**C. Citations.**
Flag papers that cite unusual pairs of fields.
A known method, but it needs a decade to confirm,
so it dates known events better than it finds new ones.

**D. Reading by an AI model.**
Have a model read abstracts and introductions
for cross-field technique use.
Broad and cheap, but every output must be checked.

**E. Formal and community sources.**
Lean's Mathlib dependencies, MathOverflow threads, expert blogs.
Not started.

---

## 5. How we measure completeness

We build **seed sets**: events we trust, written down in advance.
Then we measure how many each channel recovers.

**Seed set A (77 events).**
Picked from my own knowledge.
Risk: it leans toward famous cases.

**Seed set B (42 events).**
Picked by a rule, not by taste.
Take every Fields Medal (1936–2026) and Abel Prize (2003–2026) citation.
Keep it if the cited work combines or imports across at least two
MSC sections or creates a new area.
This lets us test recall on events I did not choose.

Later we also compare channels with each other.
If two independent channels find mostly the same events,
the total is probably close to what they found.
If they find different ones, many are still missing.
That is the capture–recapture idea.

---

## 6. How the numbers work (channel B)

**MSC.**
The Mathematics Subject Classification.
63 top-level sections, about 500 three-character classes.
Example: 37A is ergodic theory, 11B is sequences and sets in number theory.

**The raw measurement.**
For a pair of classes, count papers carrying both.
Do it per window (5 or 10 years).
Divide by the number of papers in the window.

**Why it needs care.**
- Most pairs have tiny counts in early decades.
  Tiny counts jump around by luck.
- Papers carry only a few codes,
  so a pair can rise a lot and still be below "independent chance".
- With about 140,000 class pairs,
  some will look dramatic by accident.

---

## 7. The detector

It answers one question:
for a pair of classes, did papers carrying both
become far more common than chance suggests,
and in which window?

How it works, in plain words:

- **Expected count.**
  Work out how many papers should carry both codes
  if the two classes were unrelated, given how big each is.
- **Change-point test.**
  Look for the first window where the count jumps
  well above the pair's own recent level,
  stays high in the next window,
  and is unlikely to be noise.
  That window is the onset.
- **Size-matched null.**
  Compare each pair with other pairs of similar size and growth.
  Small pairs naturally jump more, so this keeps the test fair.
- **False-discovery control.**
  A standard correction (Benjamini–Hochberg)
  keeps false flags to about 5% of what we report.
- **Tested by simulation.**
  The agent generated fake data with and without planted take-offs.

What the simulation showed:
- On pure noise the new rule flags 0–3% of pairs.
  My first simple rule flagged 25–85%.
- A 5-fold take-off is found about 55–90% of the time
  from about 10 expected papers upward.
- A 2-fold rise is almost never found.

So the detector is strict and calibrated,
but it only sees big, clear take-offs.

---

## 8. Where the data comes from

**zbMATH Open API.**
Exact publication year.
About 0.4 queries a second, with timeouts under load.
Good for targeted pairs, too slow for the full matrix.

**MaRDI SPARQL endpoint.**
Holds 4.5 million zbMATH documents with full MSC lists.
Returns every class pair for a year in a few minutes.
Catch: it has the **review year**, not the publication year.
Review lags publication by 0 to 11 years,
so onsets look late.
We use the API to calibrate that lag.

**OpenAlex.**
A free key is needed for real use.
The sign-up link goes to an email address,
and the one offered is probably not a mailbox you control.
Its math categories are also coarse (five subfields).
Parked for now.

**The full zbMATH graph dump (1.6 GB).**
Not downloaded, by your decision.

---

## 9. What has been done

**Design.**
Event types, three dates, five channels, completeness method.

**Seed sets.**
- A: 77 events, with sources.
  Citations were checked against Crossref, Open Library and arXiv.
  A few were corrected.
  Classical primary works were not looked up one by one.
- B: 42 events, with sources and the prize record each came from.

**Reading of prior work.**
Nine works read at abstract level.
No study found that builds dated pair-emergence curves
or a sourced catalogue of field marriages.
That is "none found here", not "none exists".
Google Scholar and the history literature are still to search.

**First test of channel B.**
35 section pairs, nine windows, 578 counts.

**Event-to-class map.**
Each of the 119 events mapped to MSC class pairs,
with the decade the pair should take off.
Rated by how visible it should be:
7 high, 47 medium, 32 low, 33 none.
(None means before MSC, or inside a single class.)

**Detector built and simulated.**

**Class-level run (finished).**
Full class-pair matrix by review year, 1970 to 2024,
from the SPARQL endpoint, and exact-year API counts for the event pairs.
The detector flags 54 of 24,000 pairs and none of the 86 gradable seed events.
As a ranking it shows modest signal
(8% of events in the top 1% of size-matched pairs, against 3% by chance).
Review year trails publication by about 2 years.
Details: `FIELD_EMERGENCE_CLASSLEVEL.md`.

**Independent AI check of the event-to-class pairs.**
A blind second pass agreed on at least one exact pair
for 84 of 91 gradable events.

**Three history harvests (channel A).**
MacTutor topics, ICM and prize records, Quanta and expert blogs:
240 candidates, each checked by two independent AI passes.
141 accepted by both, 32 contested, 46 rejected, 6 were seed events.
Details: `FIELD_EMERGENCE_CANDIDATES.md`.

**Coverage estimates for four periods.**
Two blind harvests per period, matched and verified:
513 verified events in total,
an estimated 526 to 741 at the granularity of standard sources.
Before 1850: 113 found, about 128 estimated.
1850 to 1930: 98 found, about 104.
1930 to 1990: 179 found, about 172 (probably higher).
1990 to 2026: 123 found, about 122 (probably higher).
The seed events are only 11% to 42% of what the sources record.
Details: `FIELD_EMERGENCE_COVERAGE.md`.

---

## 10. What we have learned so far

- **The signal is real.**
  In the first test, eight of eleven pairs rose
  in the decade of, or just after, the matching events.
  Examples: number theory × dynamics after Furstenberg,
  manifolds × quantum theory after Donaldson,
  nonassociative rings × quantum theory in the 1980s–90s.
- **A simple detector does not work.**
  My first rule fired for 10 of 21 event tests
  but also for 17 of 56 control transitions.
  Not significant.
- **Coarse labels hide events.**
  SLE and the polynomial method leave no mark
  at two-digit level.
- **Class-level counts are tiny.**
  For ergodic theory × sequences and sets (37A × 11B),
  zbMATH shows 1, 2, 7 and 91 papers in the 1970s through 2000s.
  Thin evidence for 1970s–80s events.
- **Blind before about 1970.**
  Sections that did not exist earlier show zero papers.
  Even Kolmogorov–Sinai entropy (1958) is invisible.
  Early events must come from history (channel A).
- **The detector cannot yet be graded.**
  On 35 section pairs it flagged none of the seed events
  and none of 10 controls.
  That says the false-positive control works,
  not that recall is good or bad.
  The class-level run is the real test.

---

## 11. Honest limits

- Event types, field choices and dates are my judgements.
  A citation check shows a work exists.
  It does not show the work supports the claim.
- Seed set A leans famous.
  Seed set B is the fairer test.
- Review-year lag blurs onsets by up to a decade.
- MSC labels were assigned later for old papers,
  and the scheme itself changed.
  A jump around 2000 can be a relabelling.
- Prize entries for 2025–26 come from Wikipedia only.
- Only big take-offs are detectable.

---

## 12. What comes next

1. You audit the 14-event random sample from the accepted candidates.
2. Re-verify before 1850 with a second, stronger pass.
3. Resolve the 32 contested candidates.
4. Merge verified events into one catalogue with the seed sets.
5. Add the time-axis view to the map.

---

## 13. Open decisions

- **Who checks candidates?**
  Every claimed event needs two independent checks
  before it enters the catalogue.
  Default plan: two independent AI passes
  plus you checking a random 10%.
- **Shared checkout.**
  Another session has uncommitted edits to the app source
  in the same folder.
  I stage only my own files.
  A separate worktree would avoid any clash.
- **Branch.**
  Everything is on `feat/field-emergence`.
  Nothing has been pushed.

---

## 14. Where things are

All paths are under `data/collection/` unless noted.

**Design and notes**
- `FIELD_EMERGENCE_STUDY.md` – the strategy
- `FIELD_EMERGENCE_PHASE0.md` – prior work
- `FIELD_EMERGENCE_SPIKE.md` – first channel B test
- `FIELD_EMERGENCE_DETECTOR.md` – detector method and simulation
- `FIELD_EMERGENCE_OVERVIEW.md` – this file

**Data**
- `field-events-seed.json` – set A, 77 events
- `field-events-seed-b.json` – set B, 42 events
- `event-msc-map.json` – events mapped to class pairs
- `msc2020-classes.json` – class codes and titles
- `channel-b-spike.json` – first test series

**Code** (under `scripts/field-emergence/`)
- `detect.py` – the detector
- `class_counts.py` – counts via API or SPARQL
- `analyze_class_level.py` – grades the class-level run
- `zbmath_counts.py`, `analyze_spike.py` – first test

---

## 15. Glossary

- **MSC.** Mathematics Subject Classification, the label scheme.
- **Section.** Two-digit MSC code, such as 37.
- **Class.** Three-character MSC code, such as 37A.
- **Window.** A block of years, 5 or 10.
- **Lift.** Observed pair count divided by the count expected
  if the two classes were unrelated.
- **Onset.** The first window where a pair clearly takes off.
- **Review year.** The year zbMATH reviewed a paper.
  It trails the publication year.
- **Recall.** The share of known events a method recovers.
- **Capture–recapture.** Estimating a total from how much
  two independent searches overlap.
- **False discovery rate.** The share of reported findings
  that are flukes.
- **Null.** A model of "nothing special is happening",
  used to judge what counts as surprising.
