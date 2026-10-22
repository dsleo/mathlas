# Catalogue-wide work-record search (18 October 2026)

The 52 staged scale batches contain **517 events** and **1,076 inherited citation entries** representing **1,063 unique citation strings**. [`work-search.json`](work-search.json) preserves up to three Crossref search candidates per citation. [`arxiv-records.json`](arxiv-records.json) records the identity and first posting date of every explicit arXiv ID encountered. [`work-search-summary.json`](work-search-summary.json) gives event-level search coverage.

The candidate triage is:

| Result | Citation entries | Meaning |
| --- | ---: | --- |
| Strong Crossref candidate | 317 | A returned title overlaps strongly and its publisher year matches the inherited citation year. Still requires event-level interpretation. |
| Plausible Crossref candidate | 20 | A close title, but the cited year was absent or less certain. |
| Explicit arXiv ID, aligned metadata | 22 | The identifier resolved and citation text/year broadly agrees. |
| Explicit arXiv ID, title absent from shorthand citation | 35 | The identifier resolved; the inherited citation contains little or no title to compare. |
| Explicit arXiv ID, cited year differs from first posting | 39 | The identifier resolved, but the inherited year differs. This may be a journal year rather than an error and needs inspection. |
| No close candidate | 643 | Crossref's top three did not supply a defensible title/year match. This includes ancient or lost works and vague shorthand citations. |

**250 of the 517 scale events have no close work-record candidate in these searches.** This is a search-coverage measure, not a verdict that no historical evidence exists. Ancient works may need surviving-edition catalogues and history sources; other entries need title expansion, zbMATH, Open Library, archive.org, or direct archive searches. A verified bibliographic record confirms the work's identity and date, not its role as the first public statement or first application.

The search exposed a concrete inherited-reference error in batch 51: `arXiv:1709.05032` is not Slofstra's non-closure paper. The [source audit](batch51-source-audit.md) identifies the relevant Slofstra record as `arXiv:1703.08618`. Similar mismatches should be corrected only after opening the original record, not by promoting the highest-scoring search candidate.
