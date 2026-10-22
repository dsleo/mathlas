#!/usr/bin/env python3
"""Collect Crossref candidate records for the enrichment pilot's existing works.

The catalogue's citations are unverified leads. Crossref search ranking is not
proof of a match, so output is for reconciliation only and must not be shown
as accepted evidence or shared with the independent research passes.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "data/collection/enrichment/pilot"
OUT = PILOT / "reconciliation-candidates.json"
HEADERS = {"User-Agent": "Proofscape-enrichment-pilot/0.1 (bibliographic research)"}


def crossref(query: str) -> list[dict]:
    params = urllib.parse.urlencode({
        "query.bibliographic": query,
        "rows": 3,
        "select": "DOI,title,author,published,issued,URL",
    })
    request = urllib.request.Request("https://api.crossref.org/works?" + params, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                items = json.load(response)["message"]["items"]
            break
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 502, 503) or attempt == 2:
                raise
            time.sleep(2 ** (attempt + 1))
    records = []
    for item in items:
        date_parts = item.get("published", item.get("issued", {})).get("date-parts", [[]])
        records.append({
            "title": (item.get("title") or [""])[0],
            "year": date_parts[0][0] if date_parts and date_parts[0] else None,
            "authors": [" ".join(filter(None, (a.get("given"), a.get("family")))) for a in item.get("author", [])][:6],
            "doi": item.get("DOI"),
            "url": item.get("URL"),
        })
    return records


def main() -> None:
    manifest = json.loads((PILOT / "manifest.json").read_text())
    events = {e["id"]: e for e in json.loads((ROOT / "data/collection/field-events-merged.json").read_text())["events"]}
    if OUT.exists():
        output = json.loads(OUT.read_text())
    else:
        output = {"retrievedAt": datetime.now(timezone.utc).isoformat(), "source": "Crossref REST API", "status": "candidates_unverified", "events": {}}
    for row in manifest["events"]:
        event_id = row["eventId"]
        existing = output["events"].setdefault(event_id, {"name": row["name"], "queries": []})
        searched = {item["citation"] for item in existing["queries"]}
        for citation in dict.fromkeys(events[event_id].get("works", [])):
            if citation in searched:
                continue
            try:
                records = crossref(citation)
                result = {"citation": citation, "candidates": records}
            except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
                result = {"citation": citation, "candidates": [], "error": str(exc)}
            existing["queries"].append(result)
            OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
            time.sleep(1)
    print(f"Saved candidate records for {len(output['events'])} pilot events to {OUT}")


if __name__ == "__main__":
    main()
