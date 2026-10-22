"""List first-statement and first-application milestones backed only by search pages."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "public/field-emergence-explorer.html"
OUTPUT = ROOT / "data/collection/field-map-evidence-review.json"
SEARCH_PREFIXES = (
    "https://openlibrary.org/search",
    "https://zbmath.org/?q=",
    "https://mathscinet.ams.org/mathscinet/search",
)


def main():
    page = PAGE.read_text()
    events = json.loads(page.split("const D=", 1)[1].split(";\nconst REDIRECTS=", 1)[0])
    review = []
    for event in events:
        for milestone in event["ms"]:
            if milestone["r"] not in {"first_statement", "first_application"}:
                continue
            urls = [source.get("u") or "" for source in milestone["ev"]]
            if urls and all(url.startswith(SEARCH_PREFIXES) for url in urls):
                review.append({
                    "pid": event["pid"],
                    "event": event["name"],
                    "role": milestone["r"],
                    "year": milestone["y"],
                    "milestone": milestone["l"],
                    "searchUrls": urls,
                })
    report = {
        "method": "Priority milestones whose every linked source is a search or query page; review the actual publication before treating the date as independently checked.",
        "count": len(review),
        "milestones": review,
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(review)} priority milestones need publication-level evidence")


if __name__ == "__main__":
    main()
