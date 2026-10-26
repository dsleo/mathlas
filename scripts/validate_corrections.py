#!/usr/bin/env python3
"""Reject public margin notes without a verified and applied review proposal."""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public/data/corrections.json"
PROPOSALS = ROOT / "research/corrections/proposals"


def main():
    notes = json.loads(PUBLIC.read_text())
    errors = []
    if not isinstance(notes, list):
        errors.append("public/data/corrections.json must be a list")
        notes = []
    seen = set()
    for note in notes:
        if not isinstance(note, dict) or type(note.get("issue")) is not int:
            errors.append("public correction has no integer issue number")
            continue
        number = note["issue"]
        if number in seen:
            errors.append(f"duplicate public correction #{number}")
        seen.add(number)
        path = PROPOSALS / f"{number}.json"
        if not path.exists():
            errors.append(f"public correction #{number} has no review proposal")
            continue
        proposal = json.loads(path.read_text())
        review = proposal.get("review")
        if proposal.get("status") != "verified_and_applied" or not isinstance(review, dict) or not all(
            isinstance(review.get(key), str) and review[key].strip()
            for key in ("reviewer", "sourceChecked", "application")
        ):
            errors.append(f"public correction #{number} is not verified and applied")
        if proposal.get("issue") != number:
            errors.append(f"public correction #{number} does not match its proposal number")
        if proposal.get("report", {}).get("event") != note.get("event"):
            errors.append(f"public correction #{number} does not match its proposal event")
        if isinstance(review, dict) and (note.get("summary") != review.get("application") or note.get("source") != review.get("sourceChecked")):
            errors.append(f"public correction #{number} does not match its verified resolution")
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"{len(errors)} correction validation error(s)", file=sys.stderr)
        return 1
    print(f"Validated {len(notes)} published correction(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
