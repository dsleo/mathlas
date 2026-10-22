#!/usr/bin/env python3
"""Record an accepted correction (a closed issue labelled `accepted`) in public/data/corrections.json.

Reads the GitHub issue event from the file named by GITHUB_EVENT_PATH. The issue body comes from the issue form
(`### Heading` sections). Everything in it is untrusted: fields are validated and length-capped here, and the page escapes them.
Prints the issue number when an entry was added, and nothing when the issue is not an accepted correction.
"""
import json
import os
import re
import sys
from pathlib import Path

OUT = Path(os.environ.get("CORRECTIONS", Path(__file__).resolve().parents[1] / "public/data/corrections.json"))
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


def main():
    event = json.load(open(os.environ["GITHUB_EVENT_PATH"]))
    issue = event["issue"]
    labels = {l["name"] for l in issue.get("labels", [])}
    if "accepted" not in labels or "correction" not in labels or issue.get("state_reason") != "completed":
        return
    f = parse(issue.get("body"))
    if not re.fullmatch(r"[A-Za-z0-9_-]+", f.get("event", "")):
        sys.exit("issue has no valid event id")
    if f.get("page") and not f["page"].startswith("https://"):
        f.pop("page")
    entries = json.loads(OUT.read_text()) if OUT.exists() else []
    if any(e["issue"] == issue["number"] for e in entries):
        return
    entries.append({**f, "issue": issue["number"], "url": issue["html_url"], "by": issue["user"]["login"], "date": (issue.get("closed_at") or "")[:10]})
    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=1) + "\n")
    print(issue["number"])


if __name__ == "__main__":
    main()
