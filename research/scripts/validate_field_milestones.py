#!/usr/bin/env python3
"""Validate completed milestone batches and derive legacy dates without guessing.

Only files named milestones*.json are outputs. The scale/batch*.json files are
research inputs and must never be interpreted as completed enrichment records.
"""

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/collection/enrichment"
ROLES = {"precursor", "first_statement", "first_application", "key_development", "consolidation", "naming", "institution", "recognition"}
PRECISIONS = {"year", "range", "decade", "unknown"}
KINDS = {"bibliographic_record", "history_page", "primary_text"}
PEOPLE_ROLES = {"originator", "developer", "systematiser", "popularizer"}
CONFIDENCES = {"high", "medium", "low"}
DERIVED = {"conceptual": {"first_statement"}, "methodological": {"first_application"}, "institutional": {"naming", "consolidation", "institution"}}


def issue(issues, level, path, location, message):
    issues.append({"level": level, "file": str(path.relative_to(ROOT)), "location": location, "message": message})


def valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme == "https" and bool(parsed.netloc)
    except (TypeError, ValueError):
        return False


def expected_ids(path):
    name = path.stem
    try:
        batch = int(name.replace("milestones", ""))
    except ValueError:
        return None
    if path.parent.name == "pilot":
        manifest = json.loads((BASE / "pilot/manifest.json").read_text())
        return {r["eventId"] for r in manifest["events"] if r["batch"] == batch}
    if path.parent.name == "scale":
        stage = BASE / "scale" / f"batch{batch:02d}.json"
        return {r["eventId"] for r in json.loads(stage.read_text())} if stage.exists() else None
    if path.parent.name == "second":
        second = json.loads((BASE / "batch-02-direct.json").read_text())["events"]
        return {r["eventId"] for r in second} if batch == 1 else None
    return None


def derived_dates(row):
    """Return the earliest eligible milestone per old date, retaining precision.

    An unknown year never sets a date. Equal earliest-year milestones are all
    referenced, since naming and a book can coincide without being duplicates.
    """
    dates = {}
    for field, roles in DERIVED.items():
        eligible = [(i, m) for i, m in enumerate(row["milestones"]) if m.get("role") in roles and isinstance(m.get("year"), int)]
        if not eligible:
            dates[field] = None
            continue
        first = min(m["year"] for _, m in eligible)
        ties = [(i, m) for i, m in eligible if m["year"] == first]
        evidence = [source for _, milestone in ties for source in milestone.get("evidence", [])]
        # The current milestone ledger is a direct research pass. A linked
        # record can justify B, while a history page alone justifies C. A
        # grade needs independently reconciled research and is never inferred
        # from the number of links on one milestone.
        grade = "B" if any(source.get("kind") == "bibliographic_record" for source in evidence) else "C" if any(source.get("kind") in {"history_page", "primary_text"} for source in evidence) else None
        dates[field] = {"start": first, "end": max(m.get("endYear") or first for _, m in ties),
                        "precision": "range" if any(m.get("precision") == "range" for _, m in ties) else ties[0][1]["precision"],
                        "milestoneIndices": [i for i, _ in ties], "roles": [m["role"] for _, m in ties], "grade": grade}
    return dates


def audit_file(path):
    issues = []
    try:
        rows = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        issue(issues, "error", path, "$", f"Cannot read JSON: {exc}")
        return [], issues
    if not isinstance(rows, list):
        issue(issues, "error", path, "$", "Batch output must be a JSON list")
        return [], issues
    expected = expected_ids(path)
    found = [r.get("eventId") for r in rows if isinstance(r, dict)]
    if expected is not None and set(found) != expected:
        issue(issues, "error", path, "$", f"Event IDs differ from input: missing {sorted(expected - set(found))}; extra {sorted(set(found) - expected)}")
    if len(found) != len(set(found)):
        issue(issues, "error", path, "$", "Duplicate eventId")
    derived = []
    for row_number, row in enumerate(rows):
        loc = f"[{row_number}]"
        if not isinstance(row, dict):
            issue(issues, "error", path, loc, "Event is not an object")
            continue
        for key in ("eventId", "canonicalName", "aliases", "milestones", "people", "notes"):
            if key not in row:
                issue(issues, "error", path, loc, f"Missing {key}")
        for key in ("eventId", "canonicalName", "notes"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                issue(issues, "error", path, loc, f"{key} must be nonempty text")
        aliases = row.get("aliases")
        if not isinstance(aliases, list) or any(not isinstance(a, str) or not a.strip() for a in aliases):
            issue(issues, "error", path, loc, "aliases must be a list of nonempty names")
        milestones = row.get("milestones")
        if not isinstance(milestones, list):
            issue(issues, "error", path, loc, "milestones must be a list")
            continue
        if not 0 <= len(milestones) <= 8:
            issue(issues, "error", path, loc, f"Expected 0–8 milestones; found {len(milestones)}")
        if not milestones and (not isinstance(row.get("searchedSources"), list) or
                               not row["searchedSources"] or
                               any(not isinstance(source, str) or not source.strip() for source in row["searchedSources"])):
            issue(issues, "error", path, loc, "No milestones requires a nonempty searchedSources list")
        phases = row.get("phases") or []
        if not isinstance(phases, list):
            issue(issues, "error", path, loc, "phases must be a list")
            phases = []
        elif any(not isinstance(phase, str) or not phase.strip() for phase in phases):
            issue(issues, "error", path, loc, "phases must contain nonempty names")
        seen_years = []
        seen_undated = False
        work_roles = {}
        for i, m in enumerate(milestones):
            where = f"{loc}.milestones[{i}]"
            if not isinstance(m, dict):
                issue(issues, "error", path, where, "Milestone is not an object")
                continue
            role, year, precision = m.get("role"), m.get("year"), m.get("precision")
            if role not in ROLES:
                issue(issues, "error", path, where, f"Invalid role: {role}")
            if precision not in PRECISIONS:
                issue(issues, "error", path, where, f"Invalid precision: {precision}")
            if m.get("confidence") not in CONFIDENCES:
                issue(issues, "error", path, where, f"Invalid confidence: {m.get('confidence')}")
            if m.get("work") is not None and not isinstance(m["work"], str):
                issue(issues, "error", path, where, "work must be text or null")
            if year is None:
                seen_undated = True
                if precision != "unknown":
                    issue(issues, "error", path, where, "Null year requires unknown precision")
                if role != "precursor" and not m.get("note"):
                    issue(issues, "error", path, where, "Undated non-precursor needs a search note")
            elif type(year) is not int:
                issue(issues, "error", path, where, "year must be an integer or null")
            else:
                if seen_undated:
                    issue(issues, "error", path, where, "Dated milestone follows an undated one")
                if seen_years and year < seen_years[-1]:
                    issue(issues, "error", path, where, "Milestones are not ordered by year")
                seen_years.append(year)
                if precision == "unknown":
                    issue(issues, "error", path, where, "Known year cannot have unknown precision")
            end = m.get("endYear")
            if end is not None and (type(end) is not int or type(year) is not int or end < year):
                issue(issues, "error", path, where, "Invalid endYear")
            if precision == "range" and end is None:
                issue(issues, "error", path, where, "Range precision needs endYear")
            if m.get("phase") and m["phase"] not in phases:
                issue(issues, "error", path, where, "phase is not listed in event phases")
            for key in ("label", "description"):
                if not isinstance(m.get(key), str) or not m[key].strip():
                    issue(issues, "error", path, where, f"Missing {key}")
            if not isinstance(m.get("people"), list):
                issue(issues, "error", path, where, "people must be a list")
            evidence = m.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                issue(issues, "error", path, where, "Milestone needs evidence")
            else:
                for j, e in enumerate(evidence):
                    if not isinstance(e, dict) or not e.get("claim") or not e.get("source") or e.get("kind") not in KINDS or not valid_url(e.get("url")):
                        issue(issues, "error", path, f"{where}.evidence[{j}]", "Invalid evidence claim, source, kind, or URL")
            work = m.get("work")
            if work:
                previous = work_roles.setdefault(work.casefold().strip(), [])
                if previous and role not in previous and "both" not in (m.get("note") or "").casefold():
                    issue(issues, "warning", path, where, "Same work appears under different roles; explain dual role in note")
                previous.append(role)
        if milestones and not any(m.get("role") == "first_statement" for m in milestones if isinstance(m, dict)):
            issue(issues, "warning", path, loc, "No first_statement milestone; explain source gap in notes")
        persons = row.get("people")
        if not isinstance(persons, list):
            issue(issues, "error", path, loc, "people must be a list")
            persons = []
        if len(persons) > 6:
            issue(issues, "error", path, loc, f"More than six people: {len(persons)}")
        for j, p in enumerate(persons):
            where = f"{loc}.people[{j}]"
            if not isinstance(p, dict) or not p.get("name") or p.get("role") not in PEOPLE_ROLES or not valid_url(p.get("biographyUrl")):
                issue(issues, "error", path, where, "Invalid person name, role, or biography URL")
                continue
            works = p.get("works")
            if not isinstance(works, list) or not 1 <= len(works) <= 3:
                issue(issues, "error", path, where, f"Expected 1–3 works; found {len(works) if isinstance(works, list) else 'non-list'}")
                continue
            for k, w in enumerate(works):
                if not isinstance(w, dict) or not w.get("citation") or not isinstance(w.get("year"), int) or not valid_url(w.get("url")) or not w.get("whyItMatters"):
                    issue(issues, "error", path, f"{where}.works[{k}]", "Invalid work citation, year, URL, or relevance")
        derived.append({"eventId": row.get("eventId"), "pid": row.get("pid"), "dates": derived_dates(row)})
    return derived, issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, help="Completed milestones*.json files; defaults to all existing pilot and scale outputs")
    parser.add_argument("--output", type=Path, help="Write JSON audit to this path")
    args = parser.parse_args()
    paths = args.paths or sorted((BASE / "pilot").glob("milestones*.json")) + sorted((BASE / "second").glob("milestones*.json")) + sorted((BASE / "scale").glob("milestones*.json"))
    all_derived, all_issues = [], []
    for path in paths:
        dates, issues = audit_file(path.resolve())
        all_derived.extend(dates)
        all_issues.extend(issues)
    result = {"files": [str(p.resolve().relative_to(ROOT)) for p in paths], "events": len(all_derived), "issueCounts": dict(Counter(i["level"] for i in all_issues)), "issues": all_issues, "derivedDates": all_derived}
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"files": len(paths), "events": len(all_derived), "issueCounts": result["issueCounts"]}))
    for i in all_issues:
        print(f'{i["level"].upper()}: {i["file"]} {i["location"]}: {i["message"]}')
    if result["issueCounts"].get("error"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
