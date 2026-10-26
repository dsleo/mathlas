#!/usr/bin/env python3
"""Publish the curated event connections used by the atlas reading views."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/events.json"
TARGET = ROOT / "public/data/genealogy.json"


def main():
    events = json.loads(SOURCE.read_text())
    known = {event["pid"] for event in events}
    graph = {}
    for event in events:
        groups = {}
        for direction in ("b", "a", "s"):
            # Keep the editor's order and wording, while never publishing a dead link.
            links = [
                {key: link[key] for key in ("p", "f", "t") if key in link}
                for link in (event.get("rel") or {}).get(direction, [])
                if link.get("p") in known and link.get("p") != event["pid"]
            ]
            if links:
                groups[direction] = links
        if groups:
            graph[event["pid"]] = groups
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote {TARGET.relative_to(ROOT)} ({TARGET.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
