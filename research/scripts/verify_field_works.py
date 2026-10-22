#!/usr/bin/env python3
"""Check milestone person-work citations against publisher/repository metadata.

This checks the *existence and recorded year* of cited works, not whether a
paper supports the historical claim made about it. Missing metadata and HTTP
failures remain unverified rather than becoming false negatives.
"""

import argparse
import html
import json
import re
import time
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/collection/enrichment"
USER_AGENT = "Proofscape field-emergence metadata audit (research use)"


def key_for(url):
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = unquote(parsed.path).strip("/")
    if host in {"doi.org", "dx.doi.org"}:
        return "crossref", path.lower()
    if host.endswith("arxiv.org") and path.startswith("abs/"):
        return "arxiv", path[4:]
    if host.endswith("openlibrary.org"):
        match = re.search(r"/(works|books)/(OL\d+[WM])", "/" + path)
        if match:
            return "openlibrary", match.group(2)
    if host.endswith("archive.org") and path.startswith("details/"):
        return "archive", path.split("/")[1]
    if host.endswith("numdam.org") and (path.startswith("item/") or path.startswith("book-part/")):
        return "numdam", url
    if host == "api.zbmath.org" and re.fullmatch(r"v1/document/\d+", path):
        return "zbmath", path.rsplit("/", 1)[-1]
    if host.endswith("henripoincarepapers.univ-nantes.fr") and "bibkey=" in parsed.query:
        return "poincare_bibliography", url
    return "unsupported", url


def year_from_date_parts(value):
    try:
        return int(value["date-parts"][0][0])
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def year_from_string(value):
    match = re.search(r"(?<!\d)(?:1[4-9]\d{2}|20\d{2})(?!\d)", str(value or ""))
    return int(match.group()) if match else None


def title_check(citation, record_title):
    """Flag obvious wrong targets; a match is only a heuristic, not proof."""
    def words(value):
        value = unicodedata.normalize("NFKD", html.unescape(value or ""))
        value = "".join(c for c in value if not unicodedata.combining(c))
        return set(re.findall(r"[a-z0-9]{3,}", value.casefold()))
    cited, recorded = words(citation), words(record_title)
    if not recorded:
        return "unavailable"
    return "plausible" if len(cited & recorded) / len(recorded) >= 0.55 else "review"


def fetch(session, kind, key):
    if kind == "crossref":
        url = "https://api.crossref.org/works/" + key
    elif kind == "arxiv":
        url = "https://export.arxiv.org/api/query"
    elif kind == "openlibrary":
        url = "https://openlibrary.org/" + ("works" if key.endswith("W") else "books") + "/" + key + ".json"
    elif kind == "archive":
        url = "https://archive.org/metadata/" + key
    elif kind == "zbmath":
        url = "https://api.zbmath.org/v1/document/" + key
    elif kind in {"numdam", "poincare_bibliography"}:
        url = key
    else:
        return {"status": "unsupported", "source": kind}
    try:
        response = session.get(url, params={"id_list": key} if kind == "arxiv" else None, timeout=20)
        if response.status_code == 404:
            return {"status": "not_found", "source": kind, "url": response.url}
        if kind == "arxiv" and response.status_code in (429, 500, 502, 503, 504):
            # The export API commonly rate-limits bulk audits; the public abs
            # page carries the original submission date in citation_date.
            page = session.get("https://arxiv.org/abs/" + key, timeout=20)
            if page.ok:
                metas = dict(re.findall(r'<meta name="(citation_[^"]+)" content="([^"]*)"', page.text))
                title = html.unescape(metas.get("citation_title", ""))
                year = year_from_string(metas.get("citation_date"))
                if title and year:
                    return {"status": "found", "source": "arxiv_abs_html", "title": title,
                            "years": [year], "url": page.url}
        if response.status_code in (429, 500, 502, 503, 504):
            return {"status": "unavailable", "source": kind, "httpStatus": response.status_code}
        response.raise_for_status()
        if kind == "numdam":
            metas = dict(re.findall(r'<meta name="(citation_[^"]+)" content="([^"]*)"', response.text))
            cite = re.search(r'<pre[^>]*id="how-to-cite-div"[^>]*>(.*?)</pre>', response.text, re.S)
            title = re.search(r'<title[^>]*>(.*?)</title>', response.text, re.S | re.I)
            year = year_from_string(metas.get("citation_publication_date") or (cite.group(1) if cite else ""))
            recorded_title = metas.get("citation_title") or (title.group(1) if title else "")
            recorded_title = " ".join(html.unescape(re.sub(r"<[^>]+>", "", recorded_title)).split())
            return {"status": "found" if recorded_title else "unavailable", "source": kind,
                    "title": recorded_title, "years": [year] if year else [], "url": response.url}
        if kind == "zbmath":
            result = response.json().get("result") or {}
            title = result.get("title") or {}
            recorded_title = title.get("title", "") if isinstance(title, dict) else str(title)
            year = year_from_string(result.get("year"))
            return {"status": "found" if recorded_title else "unavailable", "source": kind,
                    "title": recorded_title, "years": [year] if year else [], "url": response.url}
        if kind == "poincare_bibliography":
            title = re.search(r'Titre article\s*:\s*</td>\s*<td>([^<]+)', response.text)
            year = re.search(r'Année\s*:\s*</td>\s*<td>(\d{4})', response.text)
            return {"status": "found" if title else "unavailable", "source": kind,
                    "title": html.unescape(title.group(1)) if title else "",
                    "years": [int(year.group(1))] if year else [], "url": response.url}
        if kind == "crossref":
            m = response.json()["message"]
            years = {year_from_date_parts(m.get(k)) for k in ("published", "published-print", "published-online", "issued")}
            issue = m.get("journal-issue") or {}
            years.update(year_from_date_parts(issue.get(k)) for k in ("published-print", "published-online"))
            return {"status": "found", "source": kind, "title": (m.get("title") or [""])[0],
                    "years": sorted(y for y in years if y), "url": response.url}
        if kind == "arxiv":
            atom = {"a": "http://www.w3.org/2005/Atom"}
            entry = ET.fromstring(response.content).find("a:entry", atom)
            if entry is None:
                return {"status": "not_found", "source": kind, "url": response.url}
            title = " ".join((entry.findtext("a:title", "", atom)).split())
            published = entry.findtext("a:published", "", atom)
            return {"status": "found", "source": kind, "title": title,
                    "years": [int(published[:4])] if published[:4].isdigit() else [], "url": response.url}
        if kind == "openlibrary":
            m = response.json()
            date = m.get("publish_date") or m.get("first_publish_date")
            year = year_from_string(date)
            return {"status": "found", "source": kind, "title": m.get("title", ""),
                    "years": [year] if year else [], "url": response.url,
                    "note": "Open Library work records often omit the original publication year" if not year else None}
        m = response.json()
        meta = m.get("metadata", {})
        date = meta.get("date") or meta.get("year")
        year = year_from_string(date)
        return {"status": "found", "source": kind, "title": meta.get("title", ""),
                "years": [year] if year else [], "url": response.url,
                "note": "Archive item date can describe an edition or upload"}
    except (requests.RequestException, ValueError, ET.ParseError, KeyError, TypeError) as exc:
        return {"status": "unavailable", "source": kind, "error": str(exc)[:160]}


def works_in(path):
    try:
        rows = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        return [], {"file": str(path), "error": str(exc)}
    works = []
    for row in rows:
        for person in row.get("people", []):
            for work in person.get("works", []):
                works.append({"file": str(path.relative_to(ROOT)), "eventId": row.get("eventId"),
                              "itemType": "person_work", "person": person.get("name"), "citation": work.get("citation"),
                              "claimedYear": work.get("year"), "citedUrl": work.get("url")})
        for index, milestone in enumerate(row.get("milestones", [])):
            if not milestone.get("work"):
                continue
            evidence = milestone.get("evidence") or []
            source = next((e for e in evidence if e.get("kind") == "bibliographic_record"), None)
            if source is None:
                source = next((e for e in evidence if e.get("kind") == "primary_text"), None)
            works.append({"file": str(path.relative_to(ROOT)), "eventId": row.get("eventId"),
                          "itemType": "milestone_work", "milestoneIndex": index,
                          "milestoneRole": milestone.get("role"), "citation": milestone["work"],
                          "claimedYear": milestone.get("year"), "endYear": milestone.get("endYear"),
                          "precision": milestone.get("precision"),
                          "citedUrl": source.get("url") if source else None})
    return works, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, help="Completed milestones*.json outputs")
    parser.add_argument("--output", type=Path, default=BASE / "work-verification.json")
    parser.add_argument("--cache", type=Path, default=BASE / "work-metadata-cache.json")
    parser.add_argument("--refresh", action="store_true", help="Refresh cached metadata")
    args = parser.parse_args()
    paths = [p.resolve() for p in (args.paths or sorted((BASE / "pilot").glob("milestones*.json")) + sorted((BASE / "second").glob("milestones*.json")) + sorted((BASE / "scale").glob("milestones*.json")))]
    works, file_errors = [], []
    for path in paths:
        items, error = works_in(path.resolve())
        works.extend(items)
        if error:
            file_errors.append(error)
    cache = json.loads(args.cache.read_text()) if args.cache.exists() else {}
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    for item in works:
        if not item.get("citedUrl"):
            item.update({"result": "no_work_record_url", "recordTitle": None, "recordYears": [],
                         "recordUrl": None, "recordNote": "Milestone evidence lacks a direct work record", "titleCheck": "unavailable"})
            continue
        kind, key = key_for(item.get("citedUrl") or "")
        cache_key = kind + ":" + key
        if args.refresh or cache_key not in cache or cache[cache_key]["status"] == "unavailable":
            cache[cache_key] = fetch(session, kind, key)
            if kind != "unsupported":
                time.sleep(0.12)
        meta = cache[cache_key]
        years = meta.get("years", [])
        title_status = title_check(item.get("citation"), meta.get("title"))
        year_ok = item["claimedYear"] in years or (item.get("precision") == "range" and item.get("endYear") is not None and any(item["claimedYear"] <= y <= item["endYear"] for y in years))
        if meta["status"] != "found":
            result = meta["status"]
        elif not years:
            result = "title_found_year_unconfirmed"
        elif title_status == "review":
            result = "year_verified_title_review" if year_ok else "year_and_title_review"
        elif year_ok:
            result = "verified"
        else:
            result = "year_mismatch"
        item.update({"result": result, "recordTitle": meta.get("title"), "recordYears": years,
                     "recordUrl": meta.get("url"), "recordNote": meta.get("note"), "titleCheck": title_status})
    verified_person_records = {(key_for(w["citedUrl"]), w["claimedYear"]) for w in works
                               if w["itemType"] == "person_work" and w["result"] == "verified"}
    for item in works:
        if (item["itemType"] == "milestone_work" and item["result"] == "year_verified_title_review"
                and (key_for(item["citedUrl"]), item["claimedYear"]) in verified_person_records):
            item["result"] = "verified_via_person_work"
    args.cache.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n")
    report = {"files": [str(p.relative_to(ROOT)) for p in paths], "works": len(works),
              "resultCounts": dict(Counter(w["result"] for w in works)),
              "resultCountsByType": {kind: dict(Counter(w["result"] for w in works if w["itemType"] == kind)) for kind in ("person_work", "milestone_work")},
              "fileErrors": file_errors, "citations": works}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"files": len(paths), "works": len(works), "resultCountsByType": report["resultCountsByType"],
                      "fileErrors": len(file_errors)}))
    for w in works:
        if w["result"] not in {"verified", "verified_via_person_work", "title_found_year_unconfirmed"}:
            label = w.get("person") or f'milestone {w.get("milestoneIndex")}'
            print(f'{w["result"]}: {w["eventId"]} {label}: {w["claimedYear"]} {w["citedUrl"]} (record years {w["recordYears"]})')
    if file_errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
