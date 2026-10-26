#!/usr/bin/env python3
"""Check the source catalogue before generating the public atlas.

The rules for milestone roles and derived dates live in
research/enrichment/MILESTONE_SCHEMA.md. Display dates may fall back to a
different milestone when no dated first statement is known; those dates must
be visibly approximate and must not be stored as a derived conceptual date.
"""

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/events.json"
ROLES = {
    "precursor",
    "first_statement",
    "first_application",
    "key_development",
    "consolidation",
    "naming",
    "institution",
    "recognition",
}
DERIVED_ROLES = {
    "conceptual": {"first_statement"},
    "methodological": {"first_application"},
    "institutional": {"naming", "consolidation", "institution"},
}
PRECISIONS = {"year", "range", "decade", "unknown"}
CONFIDENCES = {"high", "medium", "low"}
EVIDENCE_KINDS = {"bibliographic_record", "history_page", "primary_text", "primary_publication", "primary_archive"}
LINK_KINDS = {"feeds", "named", "context", "same"}


def is_year(value):
    return type(value) is int  # bool is an int subclass in Python


def earliest(milestones, roles):
    return min((m["y"] for m in milestones if isinstance(m, dict) and m.get("r") in roles and is_year(m.get("y"))), default=None)


def validate(events):
    errors = []

    def fail(where, message):
        errors.append(f"{where}: {message}")

    if not isinstance(events, list):
        return ["data/events.json: expected a list of events"]

    by_pid = {}
    by_id = {}
    for pos, event in enumerate(events):
        where = f"event #{pos + 1}"
        if not isinstance(event, dict):
            fail(where, "expected an object")
            continue
        pid = event.get("pid")
        event_id = event.get("id")
        if not isinstance(pid, str) or not pid.strip():
            fail(where, "missing pid")
        elif pid in by_pid:
            fail(where, f"duplicate pid {pid} (also at event #{by_pid[pid][0] + 1})")
        else:
            by_pid[pid] = (pos, event)
        if not isinstance(event_id, str) or not event_id.strip():
            fail(where, "missing id")
        elif event_id in by_id:
            fail(where, f"duplicate id {event_id} (also at event #{by_id[event_id] + 1})")
        else:
            by_id[event_id] = pos
        if not isinstance(event.get("name"), str) or not event["name"].strip():
            fail(where, "missing event name")

    for pos, event in enumerate(events):
        if not isinstance(event, dict):
            continue
        where = event.get("pid") or f"event #{pos + 1}"
        milestones = event.get("ms")
        if not isinstance(milestones, list):
            fail(where, "ms must be a list")
            continue
        previous_year = None
        for number, milestone in enumerate(milestones, 1):
            place = f"{where} milestone #{number}"
            if not isinstance(milestone, dict):
                fail(place, "expected an object")
                continue
            role = milestone.get("r")
            year = milestone.get("y")
            end_year = milestone.get("ye")
            if role not in ROLES:
                fail(place, f"unknown role {role!r}")
            if not isinstance(milestone.get("l"), str) or not milestone["l"].strip():
                fail(place, "missing label")
            if year is not None and not is_year(year):
                fail(place, "year must be an integer or null")
            if end_year is not None and not is_year(end_year):
                fail(place, "end year must be an integer or null")
            if is_year(year) and is_year(end_year) and end_year < year:
                fail(place, "end year precedes start year")
            if is_year(year):
                if previous_year is not None and year < previous_year:
                    fail(place, "milestones are not in year order")
                previous_year = year
            precision = milestone.get("p")
            if precision not in PRECISIONS:
                fail(place, f"unknown precision {precision!r}")
            elif (precision == "unknown") != (year is None):
                fail(place, "unknown precision and null year must occur together")
            if year is None and role != "precursor" and not milestone.get("n"):
                fail(place, "an undated non-precursor needs a note about the research gap")
            if milestone.get("c") not in CONFIDENCES:
                fail(place, f"unknown confidence {milestone.get('c')!r}")
            evidence = milestone.get("ev")
            if not isinstance(evidence, list) or not evidence:
                fail(place, "at least one evidence item is required")
            else:
                for evidence_number, item in enumerate(evidence, 1):
                    source_place = f"{place} evidence #{evidence_number}"
                    if not isinstance(item, dict):
                        fail(source_place, "expected an object")
                        continue
                    for key in ("c", "s", "u"):
                        if not isinstance(item.get(key), str) or not item[key].strip():
                            fail(source_place, f"missing {key}")
                    if item.get("k") not in EVIDENCE_KINDS:
                        fail(source_place, f"unknown kind {item.get('k')!r}")

        derived = event.get("derived")
        shown = event.get("shown")
        if not isinstance(derived, dict) or not isinstance(shown, dict):
            fail(where, "derived and shown date objects are required")
            continue
        expected = {field: earliest(milestones, roles) for field, roles in DERIVED_ROLES.items()}
        for field, expected_year in expected.items():
            if derived.get(field) != expected_year:
                fail(where, f"derived.{field} is {derived.get(field)!r}; milestone roles imply {expected_year!r}")
            shown_field = shown.get(field)
            if not isinstance(shown_field, dict):
                fail(where, f"shown.{field} must be an object")
                continue
            shown_year = shown_field.get("y")
            if shown_year is not None and not is_year(shown_year):
                fail(where, f"shown.{field}.y must be an integer or null")
            if field == "institutional" and shown_year != expected_year:
                fail(where, "shown.institutional must equal the derived institutional date")

        conceptual = expected["conceptual"]
        displayed = shown.get("conceptual", {}).get("y") if isinstance(shown.get("conceptual"), dict) else None
        fallback = conceptual is None
        fallback_year = earliest(milestones, ROLES)
        if fallback:
            if displayed != fallback_year:
                fail(where, f"conceptual fallback is {displayed!r}; earliest dated milestone is {fallback_year!r}")
            if fallback_year is not None and not event.get("approx"):
                fail(where, "conceptual fallback must be marked approx=true")
            basis = shown.get("conceptual", {}).get("basis", "")
            if "no first statement found" not in basis:
                fail(where, "conceptual fallback basis must explain the missing first statement")
        else:
            if displayed != conceptual:
                fail(where, "shown.conceptual must equal the derived conceptual date")
            if event.get("approx"):
                fail(where, "a dated first statement must not be marked as a fallback")
        if event.get("y") != displayed:
            fail(where, "map year y must equal shown.conceptual.y")

        first_application = expected["methodological"]
        shown_method = shown.get("methodological", {}).get("y") if isinstance(shown.get("methodological"), dict) else None
        if first_application is not None and shown_method != first_application:
            fail(where, "shown.methodological must equal the first application date when one is known")
        if first_application is None and shown_method != earliest(milestones, {"key_development"}):
            fail(where, "methodological fallback must be the earliest dated key development")

        if conceptual is not None:
            for number, milestone in enumerate(milestones, 1):
                if not isinstance(milestone, dict):
                    continue
                year = milestone.get("y")
                if milestone.get("r") not in {"precursor", "first_statement"} and is_year(year) and year < conceptual:
                    fail(f"{where} milestone #{number}", "a later role predates the first statement; review its role")

        took = event.get("took")
        if not isinstance(took, dict):
            fail(where, "took must be an object")
        elif took.get("y") is not None and not any(
            m.get("y") == took.get("y") and m.get("r") == took.get("role") and m.get("l") == took.get("label")
            for m in milestones if isinstance(m, dict)
        ):
            fail(where, "took must refer to an existing milestone")

        relations = event.get("rel")
        if not isinstance(relations, dict) or set(relations) != {"b", "a", "s"}:
            fail(where, "rel must contain b, a and s lists")
            continue
        for direction, reverse in (("b", "a"), ("a", "b"), ("s", "s")):
            links = relations.get(direction)
            if not isinstance(links, list):
                fail(where, f"rel.{direction} must be a list")
                continue
            targets = Counter()
            for link in links:
                place = f"{where} rel.{direction}"
                if not isinstance(link, dict):
                    fail(place, "expected an object")
                    continue
                target = link.get("p")
                if not isinstance(target, str):
                    fail(place, "target p must be an event id string")
                    continue
                targets[target] += 1
                if target not in by_pid:
                    fail(place, f"unknown target {target!r}")
                    continue
                if target == event.get("pid"):
                    fail(place, "self-link")
                kind = link.get("t")
                if kind not in LINK_KINDS or (direction == "s") != (kind == "same"):
                    fail(place, f"invalid relationship kind {kind!r}")
                if not isinstance(link.get("f"), str) or not link["f"].strip():
                    fail(place, "missing connection description")
                if not is_year(link.get("d")):
                    fail(place, "distance d must be an integer")
                target_event = by_pid[target][1]
                target_relations = target_event.get("rel")
                reverse_links = target_relations.get(reverse, []) if isinstance(target_relations, dict) else []
                if not isinstance(reverse_links, list):
                    reverse_links = []
                matching = [other for other in reverse_links if isinstance(other, dict) and other.get("p") == event.get("pid")]
                if len(matching) != 1:
                    fail(place, f"expected one reciprocal rel.{reverse} link at {target}")
                elif any(matching[0].get(key) != link.get(key) for key in ("f", "t")) or matching[0].get("d") != (-link.get("d") if direction == "s" and is_year(link.get("d")) else link.get("d")):
                    fail(place, f"reciprocal link at {target} has different description, kind, or distance")
                source_year = event.get("y")
                target_year = target_event.get("y")
                if is_year(source_year) and is_year(target_year) and is_year(link.get("d")):
                    expected_distance = (source_year - target_year) if direction == "b" else (target_year - source_year)
                    if direction == "s":
                        expected_distance = target_year - source_year
                    if link["d"] != expected_distance:
                        fail(place, f"distance d is {link['d']}; map years imply {expected_distance}")
                    if direction in {"b", "a"} and expected_distance < 0:
                        fail(place, "before/after link reverses map chronology")
            for target, count in targets.items():
                if count > 1:
                    fail(f"{where} rel.{direction}", f"duplicate target {target!r}")

    return errors


def main():
    try:
        events = json.loads(SOURCE.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read {SOURCE}: {exc}", file=sys.stderr)
        return 1
    errors = validate(events)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"{len(errors)} validation error(s)", file=sys.stderr)
        return 1
    print(f"Validated {len(events)} events and {sum(len(e['ms']) for e in events)} milestones")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
