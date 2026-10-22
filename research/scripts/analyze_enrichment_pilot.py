#!/usr/bin/env python3
"""Validate two independent enrichment passes and summarize the 30-event pilot.

Usage: python3 scripts/analyze_enrichment_pilot.py

Reads data/collection/enrichment/pilot/{A,B}{1,2,3}.json when present. A pass
must be written without access to the other pass. This script never promotes a
date to a published field or assigns a final evidence grade: linked records
still need to be checked against the claim they are meant to support.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "data/collection/enrichment/pilot"
DATE_KEYS = ("conceptual", "methodological", "institutional")
ROLES = {"originator", "developer", "systematiser", "popularizer"}
PRECISIONS = {"year", "range", "decade", "unknown"}
CONFIDENCES = {"high", "medium", "low"}
KINDS = {"primary", "secondary", "database"}
RECORD_HOSTS = (
    "crossref.org", "doi.org", "zbmath.org", "openlibrary.org",
    "archive.org", "arxiv.org", "mathscinet.ams.org",
)


def valid_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_record_url(value: object) -> bool:
    if not valid_url(value):
        return False
    host = urlparse(value).hostname or ""
    return any(host == suffix or host.endswith("." + suffix) for suffix in RECORD_HOSTS)


def valid_work_record(work: dict) -> bool:
    doi = work.get("doi")
    return valid_url(work.get("url")) or (isinstance(doi, str) and (valid_url(doi) or doi.startswith("10.")))


def valid_evidence(item: object) -> bool:
    return (isinstance(item, dict)
            and all(isinstance(item.get(k), str) and item[k].strip() for k in ("claim", "source"))
            and valid_url(item.get("url")) and item.get("kind") in KINDS)


def date_interval(date: dict) -> tuple[int, int] | None:
    start = date.get("start")
    end = date.get("end")
    if type(start) is not int:
        return None
    if end is None:
        end = start + 9 if date.get("precision") == "decade" else start
    if type(end) is not int or end < start:
        return None
    return start, end


def evidence_present(date: dict) -> bool:
    evidence = date.get("evidence", [])
    return date_interval(date) is not None and isinstance(evidence, list) and any(valid_evidence(item) for item in evidence)


def date_comparison(a: dict, b: dict) -> str:
    ai, bi = date_interval(a), date_interval(b)
    if not (evidence_present(a) and evidence_present(b) and ai and bi):
        return "not_comparable"
    if ai[1] - ai[0] > 10 or bi[1] - bi[0] > 10:
        return "broad_range"
    gap = max(ai[0] - bi[1], bi[0] - ai[1], 0)
    return "agree_within_3_years" if gap <= 3 else "disagree"


def validate_date(date: object, label: str, issues: list[str]) -> None:
    if not isinstance(date, dict):
        issues.append(f"{label}: missing date object")
        return
    if date.get("precision") not in PRECISIONS:
        issues.append(f"{label}: invalid precision")
    if date.get("confidence") not in CONFIDENCES:
        issues.append(f"{label}: invalid confidence")
    if not isinstance(date.get("note", ""), str):
        issues.append(f"{label}: note must be text")
    evidence = date.get("evidence")
    if not isinstance(evidence, list):
        issues.append(f"{label}: evidence must be a list")
        evidence = []
    for i, item in enumerate(evidence):
        if not isinstance(item, dict):
            issues.append(f"{label}: evidence {i} is not an object")
            continue
        if not all(isinstance(item.get(k), str) and item[k].strip() for k in ("claim", "source")):
            issues.append(f"{label}: evidence {i} needs claim and source")
        if not valid_url(item.get("url")):
            issues.append(f"{label}: evidence {i} needs a source URL")
        if item.get("kind") not in KINDS:
            issues.append(f"{label}: evidence {i} has invalid kind")
    interval = date_interval(date)
    if date.get("start") is not None and interval is None:
        issues.append(f"{label}: invalid start/end year")
    if interval and not any(valid_evidence(item) for item in evidence):
        issues.append(f"{label}: dated claim has no valid evidence")
    if interval is None and (date.get("precision") != "unknown" or not date.get("note")):
        issues.append(f"{label}: empty date needs unknown precision and a search note")


def validate_entry(entry: object, pid: str, pass_name: str, issues: list[str]) -> None:
    label = f"{pass_name}/{pid}"
    if not isinstance(entry, dict):
        issues.append(f"{label}: entry is not an object")
        return
    if entry.get("pid") != pid:
        issues.append(f"{label}: pid mismatch")
    if not isinstance(entry.get("canonicalName"), str) or not entry["canonicalName"].strip():
        issues.append(f"{label}: missing canonicalName")
    if not isinstance(entry.get("aliases"), list) or not all(isinstance(x, str) for x in entry["aliases"]):
        issues.append(f"{label}: aliases must be a list of strings")
    dates = entry.get("dates")
    if not isinstance(dates, dict):
        issues.append(f"{label}: missing dates")
        dates = {}
    for key in DATE_KEYS:
        validate_date(dates.get(key), f"{label}/{key}", issues)
    first_term = entry.get("firstTermUse")
    if first_term is not None:
        if not isinstance(first_term, dict) or not isinstance(first_term.get("term"), str) or type(first_term.get("year")) is not int or not first_term.get("source"):
            issues.append(f"{label}: firstTermUse needs term, year, and source")
    people = entry.get("people")
    if not isinstance(people, list):
        issues.append(f"{label}: people must be a list")
        people = []
    if len(people) > 6:
        issues.append(f"{label}: more than six people")
    for i, person in enumerate(people):
        if not isinstance(person, dict):
            issues.append(f"{label}: person {i} is not an object")
            continue
        if not isinstance(person.get("name"), str) or not person["name"].strip():
            issues.append(f"{label}: person {i} needs a name")
        if person.get("role") not in ROLES:
            issues.append(f"{label}: person {i} has invalid role")
        if not valid_url(person.get("url")):
            issues.append(f"{label}: person {i} needs a source URL")
        if not person.get("lifespan"):
            issues.append(f"{label}: person {i} needs a lifespan or explicit unknown value")
        works = person.get("works")
        if not isinstance(works, list) or not 1 <= len(works) <= 3:
            issues.append(f"{label}: person {i} needs one to three works")
            continue
        for j, work in enumerate(works):
            if not isinstance(work, dict) or not valid_work_record(work):
                issues.append(f"{label}: person {i} work {j} needs a record URL")
            elif not work.get("citation") or type(work.get("year")) is not int or not work.get("whyItMatters", work.get("why")):
                issues.append(f"{label}: person {i} work {j} needs citation, year, and relevance")


def main() -> int:
    manifest = json.loads((PILOT / "manifest.json").read_text())
    expected = {row["pid"]: row for row in manifest["events"]}
    passes: dict[str, dict[str, dict]] = {"A": {}, "B": {}}
    issues: list[str] = []
    missing_files: list[str] = []
    for pass_name in passes:
        for batch in (1, 2, 3):
            path = PILOT / f"{pass_name}{batch}.json"
            if not path.exists():
                missing_files.append(path.name)
                continue
            try:
                entries = json.loads(path.read_text())
            except (OSError, json.JSONDecodeError) as exc:
                issues.append(f"{path.name}: cannot parse JSON ({exc})")
                continue
            if not isinstance(entries, list):
                issues.append(f"{path.name}: expected a JSON list")
                continue
            batch_expected = {pid for pid, row in expected.items() if row["batch"] == batch}
            seen: set[str] = set()
            for entry in entries:
                pid = entry.get("pid") if isinstance(entry, dict) else None
                if pid not in batch_expected or pid in seen:
                    issues.append(f"{path.name}: unexpected or duplicate pid {pid!r}")
                    continue
                seen.add(pid)
                validate_entry(entry, pid, pass_name, issues)
                passes[pass_name][pid] = entry

    comparisons = Counter()
    coverage = {name: Counter() for name in passes}
    rows = []
    for pid, manifest_row in expected.items():
        date_rows = {}
        for key in DATE_KEYS:
            dates = {}
            for pass_name, entries in passes.items():
                date = entries.get(pid, {}).get("dates", {}).get(key, {})
                found = evidence_present(date)
                if found:
                    coverage[pass_name][key] += 1
                dates[pass_name] = {
                    "start": date.get("start"),
                    "end": date.get("end"),
                    "evidenced": found,
                    "recordLinked": found and any(is_record_url(ev.get("url")) for ev in date.get("evidence", []) if isinstance(ev, dict)),
                }
            a = passes["A"].get(pid, {}).get("dates", {}).get(key, {})
            b = passes["B"].get(pid, {}).get("dates", {}).get(key, {})
            comparison = date_comparison(a, b)
            comparisons[key, comparison] += 1
            date_rows[key] = {"passes": dates, "comparison": comparison}
        rows.append({"pid": pid, "eventId": manifest_row["eventId"], "name": manifest_row["name"], "dates": date_rows})

    comparison_counts = {
        key: {status: comparisons[key, status] for status in (
            "agree_within_3_years", "disagree", "broad_range", "not_comparable"
        )}
        for key in DATE_KEYS
    }
    missing_entries = {
        name: sorted(set(expected) - set(entries)) for name, entries in passes.items()
    }
    summary = {
        "status": "complete" if not missing_files and not issues and not any(missing_entries.values()) else "incomplete",
        "sampleSize": len(expected),
        "missingPassFiles": missing_files,
        "missingEntries": missing_entries,
        "passEntries": {name: len(entries) for name, entries in passes.items()},
        "evidencedDatesByPass": {name: dict(counts) for name, counts in coverage.items()},
        "comparisonsByDate": comparison_counts,
        "validationIssues": issues,
        "events": rows,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if issues else 2 if summary["status"] == "incomplete" else 0


if __name__ == "__main__":
    raise SystemExit(main())
