#!/usr/bin/env python3
"""Summarize publisher-record search coverage without claiming historical priority."""

import json
from collections import Counter
from pathlib import Path

from discover_scale_work_records import tokens

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/collection/enrichment/scale"


def main():
    data = json.loads((BASE / "work-search.json").read_text())
    rows = []
    for event in data["events"]:
        counts = Counter()
        for work in event["works"]:
            if work["status"] != "searched":
                counts[work["status"]] += 1
                continue
            candidates = work["candidates"]
            explicit = [c for c in candidates if c.get("source") == "arxiv_explicit_id"]
            if explicit:
                candidate = explicit[0]
                # A journal citation may carry a later year than its arXiv
                # posting; call this a difference, not a contradiction.
                category = ("explicit_id_year_difference" if candidate["yearMatch"] is False else
                            "explicit_id_title_not_in_citation" if candidate["titleOverlap"] < .6 else "explicit_id_record")
                counts[category] += 1
                continue
            # Short generic titles such as "Eudoxus" can otherwise look like
            # exact matches to an unrelated reference entry.
            plausible = [c for c in candidates if len(tokens(c["title"])) >= 3 and c["titleOverlap"] >= .75 and c["yearMatch"] is not False]
            strong = [c for c in plausible if c["titleOverlap"] >= .8 and c["yearMatch"] is True]
            counts["strong_candidate" if strong else "plausible_candidate" if plausible else "no_close_candidate"] += 1
        rows.append({"eventId": event["eventId"], "name": event["name"], "citations": len(event["works"]),
                     "counts": dict(counts)})
    totals = Counter()
    for row in rows:
        totals.update(row["counts"])
    report = {"warning": "A matching catalogue title and year does not establish the work's role or historical priority.",
              "events": len(rows), "citations": sum(r["citations"] for r in rows), "citationResults": dict(totals),
              "eventsWithStrongCandidate": sum(r["counts"].get("strong_candidate", 0) > 0 for r in rows),
              "eventsWithoutAnyRecordCandidate": sum(not (r["counts"].get("strong_candidate", 0) or r["counts"].get("plausible_candidate", 0) or any(key.startswith("explicit_id_") for key in r["counts"])) for r in rows),
              "rows": rows}
    (BASE / "work-search-summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
