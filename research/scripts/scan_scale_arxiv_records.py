#!/usr/bin/env python3
"""Resolve explicit arXiv IDs in inherited scale citations to original records."""

import json
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/collection/enrichment/scale"
CATALOGUE = {e["id"]: e for e in json.loads((ROOT / "data/collection/field-events-merged.json").read_text())["events"]}
ARXIV_ID = re.compile(r"(?:arXiv\s*:\s*|arxiv\.org/abs/)?((?:\d{4}\.\d{4,5}|(?:math|cs|hep-th|hep-ph|quant-ph)/\d{7})(?:v\d+)?)", re.I)
NS = {"a": "http://www.w3.org/2005/Atom"}


def main():
    ids = [e["eventId"] for n in range(1, 53) for e in json.loads((BASE / f"batch{n:02d}.json").read_text())]
    citations = {}
    for eid in ids:
        for citation in CATALOGUE[eid].get("works", []):
            match = ARXIV_ID.search(citation)
            if match:
                citations.setdefault(match.group(1), []).append({"eventId": eid, "citation": citation})
    session = requests.Session()
    session.headers["User-Agent"] = "Proofscape field-emergence bibliographic research"
    records = {}
    for i in range(0, len(citations), 25):
        batch = list(citations)[i:i + 25]
        try:
            response = session.get("https://export.arxiv.org/api/query", params={"id_list": ",".join(batch), "max_results": len(batch)}, timeout=45)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            for entry in root.findall("a:entry", NS):
                url = entry.findtext("a:id", "", NS)
                key = re.sub(r"v\d+$", "", url.split("/abs/", 1)[-1])
                records[key] = {"title": " ".join(entry.findtext("a:title", "", NS).split()),
                                "authors": [a.findtext("a:name", "", NS) for a in entry.findall("a:author", NS)],
                                "published": entry.findtext("a:published", "", NS), "url": url}
        except (requests.RequestException, ET.ParseError) as exc:
            for key in batch:
                records[key] = {"error": str(exc)[:200]}
        time.sleep(1)
    rows = []
    for key, matches in citations.items():
        row = {"arxivId": key, "citations": matches, **records.get(re.sub(r"v\d+$", "", key), {"error": "No matching API entry"})}
        rows.append(row)
    out = {"note": "Explicit-ID lookup verifies arXiv metadata, not the event's historical claim.",
           "uniqueIds": len(citations), "resolved": sum("title" in r for r in rows), "rows": rows}
    (BASE / "arxiv-records.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}))


if __name__ == "__main__":
    main()
