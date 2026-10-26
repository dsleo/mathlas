#!/usr/bin/env python3
"""Stage a correction for review, then publish its note after verification.

With no arguments, read the accepted GitHub issue from GITHUB_EVENT_PATH and
write a repository review proposal. The issue body is untrusted: only known
fields are retained, whitespace is normalized, and lengths are capped.

After checking the offered source and applying a supported change to
data/events.json, a maintainer records the review with `verify` and adds the
public margin note with `publish`. An issue label alone never publishes a claim.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = Path(os.environ.get("PROPOSALS_DIR", ROOT / "research/corrections/proposals"))
OUT = Path(os.environ.get("CORRECTIONS", ROOT / "public/data/corrections.json"))
FIELDS = {"Event": "event", "Milestone": "milestone", "Page": "page", "What needs fixing": "kind", "What it should say": "summary", "Source": "source"}
CAPS = {"event": 40, "milestone": 200, "page": 300, "kind": 40, "summary": 600, "source": 300}


def parse(body):
    out = {}
    for head, text in re.findall(r"^### (.+?)\s*\n+(.*?)(?=^### |\Z)", body or "", re.S | re.M):
        key = FIELDS.get(head.strip())
        text = text.strip()
        if key and text != "_No response_":
            out[key] = re.sub(r"\s+", " ", text)[:CAPS[key]]
    return out


def proposal_path(number):
    return PROPOSALS / f"{number}.json"


def load_proposal(number):
    path = proposal_path(number)
    if not path.exists():
        sys.exit(f"No repository review proposal for correction #{number}")
    return json.loads(path.read_text())


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=1) + "\n")


def propose():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        sys.exit("GITHUB_EVENT_PATH is required to stage an issue")
    issue = json.loads(Path(event_path).read_text())["issue"]
    labels = {label.get("name") for label in issue.get("labels", [])}
    if "accepted" not in labels or "correction" not in labels or issue.get("state_reason") != "completed":
        return
    fields = parse(issue.get("body"))
    if not re.fullmatch(r"[A-Za-z0-9_-]+", fields.get("event", "")):
        sys.exit("issue has no valid event id")
    if fields.get("page") and not fields["page"].startswith("https://"):
        fields.pop("page")
    number = issue["number"]
    path = proposal_path(number)
    if path.exists():
        return
    proposal = {
        "issue": number,
        "url": issue["html_url"],
        "by": issue["user"]["login"],
        "date": (issue.get("closed_at") or "")[:10],
        "status": "accepted_for_review",
        "report": fields,
        "review": None,
    }
    write_json(path, proposal)
    print(number)


def verify(number, reviewer, source_checked, application):
    proposal = load_proposal(number)
    if proposal.get("status") == "verified_and_applied":
        sys.exit(f"Correction #{number} is already verified")
    if proposal.get("status") != "accepted_for_review":
        sys.exit(f"Correction #{number} is not awaiting review")
    for name, value in (("reviewer", reviewer), ("source checked", source_checked), ("applied change", application)):
        if not value.strip():
            sys.exit(f"A {name} is required to verify the correction")
    event_id = proposal.get("report", {}).get("event")
    events = json.loads((ROOT / "data/events.json").read_text())
    if not any(event.get("pid") == event_id for event in events):
        sys.exit(f"Event {event_id!r} does not exist in data/events.json")
    proposal["status"] = "verified_and_applied"
    proposal["review"] = {
        "reviewer": reviewer.strip()[:100],
        "sourceChecked": source_checked.strip()[:600],
        "application": application.strip()[:600],
    }
    write_json(proposal_path(number), proposal)
    print(f"Verified correction #{number}")


def publish(number):
    proposal = load_proposal(number)
    review = proposal.get("review")
    if proposal.get("status") != "verified_and_applied" or not isinstance(review, dict) or not all(review.get(key) for key in ("reviewer", "sourceChecked", "application")):
        sys.exit(f"Correction #{number} must be verified and applied before publication")
    entries = json.loads(OUT.read_text()) if OUT.exists() else []
    if any(entry.get("issue") == number for entry in entries):
        return
    entry = {
        **proposal["report"],
        "summary": review["application"],
        "source": review["sourceChecked"],
        **{key: proposal[key] for key in ("issue", "url", "by", "date")},
    }
    entries.append(entry)
    write_json(OUT, entries)
    print(f"Published margin note for correction #{number}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command")
    verify_parser = subcommands.add_parser("verify", help="record source review and applied data change")
    verify_parser.add_argument("--issue", type=int, required=True)
    verify_parser.add_argument("--reviewer", required=True)
    verify_parser.add_argument("--source-checked", required=True)
    verify_parser.add_argument("--application", required=True)
    publish_parser = subcommands.add_parser("publish", help="publish a verified correction as a margin note")
    publish_parser.add_argument("--issue", type=int, required=True)
    args = parser.parse_args()
    if args.command == "verify":
        verify(args.issue, args.reviewer, args.source_checked, args.application)
    elif args.command == "publish":
        publish(args.issue)
    else:
        propose()


if __name__ == "__main__":
    main()
