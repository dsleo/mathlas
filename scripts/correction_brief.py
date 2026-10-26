#!/usr/bin/env python3
"""Write the ready-made brief for applying an accepted correction (for a person or an AI agent).

    python3 scripts/correction_brief.py --issue 12      # fetches the issue with the gh CLI
    GITHUB_EVENT_PATH=event.json python3 scripts/correction_brief.py    # inside the workflow

The brief holds what was reported, the current record of the milestone it concerns, and the procedure in AGENTS.md.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from record_correction import parse  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def fmt_year(y):
    return "" if y is None else f"{abs(y)} BCE" if y < 0 else str(y)


def ms_key(m):
    return (fmt_year(m.get("y")) + " " + m["l"]).strip()


def brief(issue):
    f = parse(issue.get("body"))
    events = {e["pid"]: e for e in json.loads((ROOT / "data/events.json").read_text())}
    e = events.get(f.get("event", ""))
    if e is None:
        return f"Correction #{issue['number']}: no event with id {f.get('event')!r} in data/events.json; check the issue by hand."
    match = [m for m in e.get("ms") or [] if ms_key(m) == f.get("milestone")]
    record = {"pid": e["pid"], "name": e["name"], "type": e["type"], "from": e["from"], "to": e["to"], "why": e.get("why"),
              "milestones": [{k: m.get(k) for k in ("r", "y", "ye", "l", "w", "d", "c", "n", "ev")} for m in (match or e.get("ms") or [])]}
    lines = [
        f"## Apply accepted correction #{issue['number']}",
        "",
        f"Reported by @{issue['user']['login']} ({issue['html_url']}); the maintainer has accepted it for investigation.",
        "",
        f"- **Event:** `{e['pid']}` {e['name']}",
        f"- **Milestone:** {f.get('milestone') or '(whole event)'}",
        f"- **Kind:** {f.get('kind', '')}",
        f"- **Proposed:** {f.get('summary', '')}",
        f"- **Source offered:** {f.get('source') or 'none'}",
        f"- **Page:** {f.get('page') or 'n/a'}",
        "",
        "### Current record" + ("" if match else " (milestone not matched; the whole event is shown)"),
        "```json", json.dumps(record, ensure_ascii=False, indent=1), "```",
        "",
        "### What to do",
        "Follow `AGENTS.md` (\"Applying an accepted correction\"): check the proposal against the source, edit `data/events.json` under the milestone rules, run verification and publish the margin note only after the correction is supported and applied. If the source does not support it, explain why here and leave the public record unchanged.",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue", type=int)
    args = ap.parse_args()
    if args.issue:
        issue = json.loads(subprocess.check_output(["gh", "api", f"repos/dsleo/mathlas/issues/{args.issue}"]))
    else:
        issue = json.load(open(os.environ["GITHUB_EVENT_PATH"]))["issue"]
    print(brief(issue))


if __name__ == "__main__":
    main()
