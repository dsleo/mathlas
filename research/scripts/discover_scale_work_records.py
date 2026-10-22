#!/usr/bin/env python3
"""Collect Crossref candidates for staged field-event works, without promoting them to evidence.

The inherited catalogue citations are search strings, not verified records. This
script records publisher metadata and conservative title/year matching so that
event-specific research can inspect candidates before creating milestones.
"""

import argparse
import json
import re
import time
import unicodedata
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/collection/enrichment/scale"
ENDPOINT = "https://api.crossref.org/works"


def tokens(value):
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return set(re.findall(r"[a-z]{4,}|\d{4}", value))


def years_in(value):
    return {int(y) for y in re.findall(r"(?<!\d)(?:1[5-9]\d{2}|20\d{2})(?!\d)", value)}


def candidate_score(citation, record):
    title = (record.get("title") or [""])[0]
    title_words = tokens(title)
    citation_words = tokens(citation)
    overlap = len(title_words & citation_words) / len(title_words) if title_words else 0
    date = record.get("published") or record.get("issued") or {}
    try:
        year = int(date["date-parts"][0][0])
    except (KeyError, IndexError, TypeError, ValueError):
        year = None
    cited_years = years_in(citation)
    year_match = year in cited_years if cited_years else None
    return {
        "title": title,
        "year": year,
        "doi": record.get("DOI"),
        "url": record.get("URL"),
        "type": record.get("type"),
        "titleOverlap": round(overlap, 3),
        "yearMatch": year_match,
        "candidateOnly": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-batch", type=int, default=1)
    parser.add_argument("--end-batch", type=int, default=52)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--max-new", type=int, default=0, help="Stop after this many new queries (0 = all)")
    args = parser.parse_args()
    inputs = [BASE / f"batch{i:02d}.json" for i in range(args.start_batch, args.end_batch + 1)]
    catalogue = {row["id"]: row for row in json.loads((ROOT / "data/collection/field-events-merged.json").read_text())["events"]}
    ids = [event["eventId"] for path in inputs for event in json.loads(path.read_text())]
    cache_path = BASE / "work-search-cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    arxiv_path = BASE / "arxiv-records.json"
    if arxiv_path.exists():
        for row in json.loads(arxiv_path.read_text())["rows"]:
            if not row.get("title") or not row.get("published"):
                continue
            for match in row["citations"]:
                citation = match["citation"]
                record = {"title": row["title"], "year": int(row["published"][:4]),
                          "doi": None, "url": row["url"], "type": "arxiv_preprint",
                          "titleOverlap": round(len(tokens(row["title"]) & tokens(citation)) / max(1, len(tokens(row["title"]))), 3),
                          "yearMatch": int(row["published"][:4]) in years_in(citation) if years_in(citation) else None,
                          "candidateOnly": True, "source": "arxiv_explicit_id"}
                cache[citation] = {"status": "searched", "candidates": [record]}
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n")
    citations = list(dict.fromkeys(work for eid in ids for work in catalogue[eid].get("works", [])))
    session = requests.Session()
    session.headers["User-Agent"] = "Proofscape historical field research (bibliographic candidate lookup)"
    new = 0
    for citation in citations:
        if citation in cache and cache[citation]["status"] == "searched":
            continue
        for attempt in range(4):
            try:
                response = session.get(ENDPOINT, params={"query.bibliographic": citation, "rows": 3,
                                                          "select": "DOI,title,published,issued,URL,type"}, timeout=25)
                if response.status_code == 429:
                    time.sleep(min(30, 3 * 2 ** attempt))
                    continue
                response.raise_for_status()
                records = response.json()["message"]["items"]
                candidates = [candidate_score(citation, record) for record in records]
                cache[citation] = {"status": "searched", "candidates": candidates}
                break
            except (requests.RequestException, ValueError, KeyError) as exc:
                if attempt == 3:
                    cache[citation] = {"status": "unavailable", "error": str(exc)[:200], "candidates": []}
                else:
                    time.sleep(min(30, 3 * 2 ** attempt))
        else:
            cache[citation] = {"status": "unavailable", "error": "Crossref rate-limited after retries", "candidates": []}
        new += 1
        if new % 25 == 0:
            cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n")
            print(f"searched {new} new citations; {len(cache)} cached", flush=True)
        if args.max_new and new >= args.max_new:
            break
        time.sleep(args.delay)
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n")
    rows = []
    for eid in ids:
        event = catalogue[eid]
        rows.append({"eventId": eid, "name": event["name"], "catalogueDatesUnverified": event.get("dates"),
                     "works": [{"citation": work, **cache.get(work, {"status": "not_searched", "candidates": []})}
                               for work in event.get("works", [])]})
    output = BASE / "work-search.json"
    output.write_text(json.dumps({"method": "Crossref query.bibliographic candidates; no historical claim verified",
                                  "events": rows}, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"events": len(rows), "uniqueCitations": len(citations), "cached": len(cache),
                      "newQueries": new, "output": str(output.relative_to(ROOT))}), flush=True)


if __name__ == "__main__":
    main()
