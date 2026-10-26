#!/usr/bin/env python3
"""Generate readable, stable reference pages from the curated event catalogue.

The atlas remains the source of truth. These pages are a second presentation of
the same records, with ordinary links that work without JavaScript or an SVG map.
"""

from __future__ import annotations

import csv
import html
import io
import json
import re
import shutil
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_field_film import clean_milestone  # noqa: E402

SOURCE = ROOT / "data/events.json"
DEST = ROOT / "public/reference"
PORTRAITS = ROOT / "public/data/portraits.json"
MIN_PERSON_EVENTS = 3  # people with fewer events (or no portrait) stay unlinked: thin pages add noise


def escape(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def safe_link(url: object, label: object) -> str:
    """Only source and biography HTTP(S) URLs become clickable links."""
    raw = str(url or "").strip()
    parsed = urlsplit(raw)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return escape(label)
    return f'<a href="{escape(raw)}" rel="noopener noreferrer" target="_blank">{escape(label)}</a>'


def slug(text: str) -> str:
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", folded.lower()))


def year(value: object) -> str:
    if value is None:
        return "Date unknown"
    number = int(value)
    return f"{abs(number):,} BCE" if number < 0 else str(number)


def event_year(event: dict) -> str:
    return ("≈ " if event.get("approx") else "") + year(event.get("y"))


def years(item: dict) -> str:
    first, last = item.get("y"), item.get("ye")
    if first is None:
        return "Date unknown"
    if last is None or last == first:
        return year(first)
    return f"{year(first)}–{year(last)}"


def sort_year(event: dict) -> tuple[int, str]:
    return int(event.get("y") or 0), event["name"].casefold()


def page(title: str, description: str, body: str, *, css: str) -> str:
    # A relative canonical is intentionally omitted: GitHub Pages may be hosted
    # under either a repository prefix or a custom domain.
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{escape(description[:260])}">
<title>{escape(title)} · Mathlas</title>
<link rel="stylesheet" href="{escape(css)}">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
{body}
</body>
</html>
"""


def header(crumbs: list[tuple[str, str]], home: str) -> str:
    links = [f'<a href="{escape(path)}">{escape(label)}</a>' for label, path in crumbs]
    separator = ' <span aria-hidden="true">/</span> '
    nav = f'<nav aria-label="Breadcrumb">{separator.join(links)}</nav>' if links else ""
    return f"""<header class="site-header"><div class="header-inner">
<a class="brand" href="{escape(home)}">Mathlas <span>Reference</span></a>
{nav}
</div></header>"""


def event_href(pid: str, prefix: str) -> str:
    return f"{prefix}events/{quote(pid, safe='')}/"


def field_href(field: str, prefix: str, field_slugs: dict[str, str]) -> str:
    return f"{prefix}fields/{field_slugs[field]}/"


def map_href(event: dict | None = None, field: str | None = None, *, prefix: str) -> str:
    if event:
        return f"{prefix}index.html#e={quote(event['pid'], safe='')}&core&t={int(event['y'])}"
    if field:
        return f"{prefix}index.html#f={quote(field, safe='')}&t=2025"
    return f"{prefix}index.html"


def event_listing(event: dict, href: str) -> str:
    description = event.get("why") or ""
    terms = " ".join([event["name"], description, *event.get("aliases", []), *event.get("searchTerms", []), *(p.get("name") or "" for p in event.get("people") or [])])
    return f"""<li class="event-row" data-pid="{escape(event['pid'])}" data-y="{int(event.get('y') or 0)}" data-tier="{escape(event.get('tier'))}" data-search="{escape(terms)}"><span class="event-year">{escape(event_year(event))}</span>
<div><a class="event-name" href="{escape(href)}">{escape(event['name'])}</a>
<p>{escape(description)}</p></div></li>"""


def relation_group(event: dict, key: str, title: str, by_pid: dict[str, dict]) -> str:
    relations = event.get("rel", {}).get(key, [])
    if not relations:
        return ""
    rows = []
    for rel in relations:
        other = by_pid.get(rel.get("p"))
        if not other:
            continue
        detail = rel.get("f") or "Curated connection"
        rows.append(f"""<li><a href="../{escape(other['pid'])}/">{escape(other['name'])}</a>
<span class="year">{escape(event_year(other))}</span><small>{escape(detail)}</small></li>""")
    if not rows:
        return ""
    return f'<section class="relation-group"><h3>{escape(title)}</h3><ul>{"".join(rows)}</ul></section>'


def milestone(item: dict) -> str:
    item = clean_milestone(item)
    evidence = []
    for source in item.get("ev") or []:
        claim, name = source.get("c") or "", source.get("s") or "Source"
        cited = safe_link(source.get("u"), name)
        evidence.append(f'<li>{escape(claim)} <span class="source">{cited}</span></li>')
    source_block = f'<details><summary>Evidence ({len(evidence)})</summary><ul>{"".join(evidence)}</ul></details>' if evidence else ""
    work = f'<p class="work">{escape(item["w"])}</p>' if item.get("w") else ""
    description = f'<p>{escape(item["d"])}</p>' if item.get("d") else ""
    note = f'<details class="caveat"><summary>Dating or attribution note</summary><p>{escape(item["n"])}</p></details>' if item.get("n") else ""
    role = (item.get("r") or "").replace("_", " ")
    return f"""<li class="milestone"><div class="milestone-date">{escape(years(item))}</div>
<div><h3>{escape(item.get('l'))}</h3><p class="eyebrow">{escape(role)}</p>
{work}{description}{note}{source_block}</div></li>"""


def search_text(event: dict) -> str:
    """Everything a reader might search for: milestones, works, evidence sources, people."""
    parts = [event["name"], event.get("why"), *event.get("aliases", []), *event.get("searchTerms", [])]
    for m in event.get("ms") or []:
        parts += [m.get("l"), m.get("d"), m.get("w"), *(e.get("s") for e in m.get("ev") or [])]
    for p in event.get("people") or []:
        parts += [p.get("name"), *(w.get("c") for w in p.get("works") or [])]
    return " ".join(str(x) for x in parts if x)


def events_csv(events: list[dict]) -> str:
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(["pid", "name", "year", "approximate", "field", "type", "review", "milestones", "people", "path"])
    for e in sorted(events, key=sort_year):
        w.writerow([e["pid"], e["name"], e.get("y"), e.get("approx"), e["cl"], e.get("type"), e.get("tier"), len(e.get("ms") or []),
                    "; ".join(p.get("name") or "" for p in e.get("people") or []), f"events/{e['pid']}/"])
    return out.getvalue()


def cite_block(event: dict) -> str:
    people = ", ".join(p["name"] for p in event.get("people") or [] if p.get("role") == "originator")
    text = f"Mathlas. “{event['name']}.” Mathlas Reference, {event['pid']}"
    return f"""<section class="cite" aria-labelledby="cite-title"><h2 id="cite-title">Cite this page</h2>
<p class="section-intro">Stable identifier <code>{escape(event['pid'])}</code>; the record can change as sources are reviewed, so cite the date you accessed it.</p>
<p class="cite-text" data-title="{escape(text)}">{escape(text)}.</p>{f'<p class="section-intro">Originator(s): {escape(people)}.</p>' if people else ''}</section>"""


def person_page(name: str, info: dict, by_pid: dict[str, dict], people_slugs: dict[str, str], field_slugs: dict[str, str]) -> str:
    portrait = info.get("portrait")
    img = (f'<img class="portrait" src="../../../{escape(portrait["file"])}" alt="" width="120" height="120">'
           f'<p class="section-intro">Portrait: {escape(portrait.get("author") or "unknown")}, {escape(portrait["license"])}, {safe_link(portrait.get("source"), "Wikimedia Commons")}.</p>') if portrait else ""
    life = f'<p class="eyebrow">{escape(info["life"])}</p>' if info.get("life") else '<p class="eyebrow">Person</p>'
    bio = f'<p class="map-link"><a href="{escape(info["url"])}" rel="noopener noreferrer" target="_blank">Biography <span aria-hidden="true">↗</span></a></p>' if str(info.get("url") or "").startswith("http") else ""
    rows = []
    for pid, role in sorted(info["events"], key=lambda x: sort_year(by_pid[x[0]])):
        e = by_pid[pid]
        rows.append(f'<li class="event-row"><span class="event-year">{escape(event_year(e))}</span><div><a class="event-name" href="../../events/{escape(pid)}/">{escape(e["name"])}</a><p>{escape(role.replace("_", " "))} · {escape(e["cl"])}</p></div></li>')
    body = header([("All topics", "../../"), ("People", "../")], "../../../index.html")
    body += f"""<main id="content" class="layout">{life}<h1>{escape(name)}</h1>{img}{bio}
<section><h2>Events ({len(rows)})</h2><ol class="event-list">{''.join(rows)}</ol></section></main>
<footer><a href="../">All people</a> · <a href="../../">Browse the reference</a></footer>"""
    return page(name, f"{name}: {len(rows)} events in the Mathlas catalogue.", body, css="../../style.css")


def people_index(linked: dict[str, dict], people_slugs: dict[str, str]) -> str:
    rows = "".join(f'<li><a href="{people_slugs[n]}/">{escape(n)}</a> <span class="year">{len(i["events"])} events</span></li>' for n, i in sorted(linked.items(), key=lambda x: x[0].casefold()))
    body = header([("All topics", "../")], "../../index.html")
    body += f"""<main id="content" class="layout"><p class="eyebrow">{len(linked)} people</p><h1>People</h1>
<p class="lede">People credited in at least {MIN_PERSON_EVENTS} catalogue events, or with a licensed portrait.</p><ul class="people">{rows}</ul></main>"""
    return page("People", "People in the Mathlas catalogue.", body, css="../style.css")


def collect_people(events: list[dict]) -> tuple[dict[str, dict], dict[str, str]]:
    portraits = json.loads(PORTRAITS.read_text(encoding="utf-8")) if PORTRAITS.exists() else {}
    info: dict[str, dict] = {}
    for e in events:
        for p in e.get("people") or []:
            i = info.setdefault(p["name"], {"events": [], "life": p.get("life"), "url": p.get("url")})
            i["events"].append((e["pid"], p.get("role") or ""))
            i["life"] = i["life"] or p.get("life")
            i["url"] = i["url"] or p.get("url")
    linked = {}
    for n, i in info.items():
        i["portrait"] = portraits.get(n)
        if len(i["events"]) >= MIN_PERSON_EVENTS or i["portrait"]:
            linked[n] = i
    slugs = {n: slug(n) for n in linked}
    if len(set(slugs.values())) != len(slugs):
        raise ValueError("Person slug collision")
    return linked, slugs


def person(item: dict, people_slugs: dict[str, str] | None = None) -> str:
    name = safe_link(item.get("url"), item.get("name"))
    if people_slugs and item.get("name") in people_slugs:
        name = f'<a href="../../people/{people_slugs[item["name"]]}/">{escape(item["name"])}</a>' + (f' <a class="bio" href="{escape(item["url"])}" rel="noopener noreferrer" target="_blank" aria-label="Biography of {escape(item["name"])}">↗</a>' if str(item.get("url") or "").startswith("http") else "")
    role = (item.get("role") or "").replace("_", " ")
    extra = f' <span class="year">{escape(item["life"])}</span>' if item.get("life") else ""
    return f'<li>{name}{extra}<small>{escape(role)}</small></li>'


def event_page(event: dict, by_pid: dict[str, dict], field_slugs: dict[str, str], people_slugs: dict[str, str]) -> str:
    field = event["cl"]
    intro = event.get("why") or ""
    alias = ", ".join(event.get("aliases") or [])
    aliases = f'<p class="aliases">Also known as: {escape(alias)}</p>' if alias else ""
    milestones = sorted(event.get("ms") or [], key=lambda x: (x.get("y") is None, x.get("y") or 0))
    milestone_html = "".join(milestone(item) for item in milestones)
    people = "".join(person(item, people_slugs) for item in event.get("people") or [])
    relations = "".join([
        relation_group(event, "b", "Earlier connections", by_pid),
        relation_group(event, "a", "Later connections", by_pid),
        relation_group(event, "s", "Companion ideas", by_pid),
    ])
    if not relations:
        relations = '<p class="quiet">No curated connections are recorded yet.</p>'
    body = header([("All topics", "../../"), (field, f"../../fields/{field_slugs[field]}/")], "../../../index.html")
    body += f"""<main id="content" class="layout">
<p class="eyebrow">{escape(event_year(event))} · {escape(field)}</p>
<h1>{escape(event['name'])}</h1>
<p class="lede">{escape(intro)}</p>{aliases}
{'<p class="approx-note">≈ marks an approximate map placement; a dated first statement is not established for this event.</p>' if event.get('approx') else ''}
<p class="map-link"><a href="{escape(map_href(event, prefix='../../../'))}">Locate this event on the map <span aria-hidden="true">↗</span></a></p>
<div class="content-grid"><article>
<section aria-labelledby="timeline-title"><h2 id="timeline-title">Historical record</h2>
<p class="section-intro">These milestones show distinct stages of the idea. Dates and priority claims can be uncertain; consult the evidence and notes for each stage.</p>
<ol class="milestones">{milestone_html}</ol></section>
</article><aside>
<section aria-labelledby="connections-title"><h2 id="connections-title">Connections</h2>
<p class="section-intro">Curated links between catalogue events. Their descriptions are editorial pointers, not independent proof of historical influence.</p>
{relations}</section>
<section aria-labelledby="people-title"><h2 id="people-title">People</h2>
<ul class="people">{people}</ul></section>
{cite_block(event)}
</aside></div></main>
<footer><a href="../../">Browse all fields and events</a> · <a href="../../../index.html">Explore the map</a></footer>
<script>document.querySelectorAll('.cite-text').forEach(function(p){{p.textContent=p.dataset.title+', '+location.href+'.'}})</script>"""
    return page(event["name"], intro or event["name"], body, css="../../style.css")


def field_page(field: str, events: list[dict], field_slugs: dict[str, str]) -> str:
    ordered = sorted(events, key=sort_year)
    intro = f"A curated selection of {len(events)} recorded events in {field}. The dates describe these selected records, not the origin or size of the field."
    rows = "".join(event_listing(event, f"../../events/{event['pid']}/") for event in ordered)
    body = header([("All topics", "../../")], "../../../index.html")
    body += f"""<main id="content" class="layout">
<p class="eyebrow">Field · {len(events)} selected events</p>
<h1>{escape(field)}</h1><p class="lede">{escape(intro)}</p>
{'<p class="approx-note">≈ marks an approximate map placement where a dated first statement is not established.</p>' if any(e.get('approx') for e in events) else ''}
<p class="map-link"><a href="{escape(map_href(field=field, prefix='../../../'))}">Locate this field on the map <span aria-hidden="true">↗</span></a></p>
<section aria-labelledby="events-title"><h2 id="events-title">Events in this field</h2>
<ol class="event-list">{rows}</ol></section></main>
<footer><a href="../../">Browse all fields and events</a> · <a href="../../../index.html">Explore the map</a></footer>"""
    return page(field, intro, body, css="../../style.css")


def index_page(by_field: dict[str, list[dict]], field_slugs: dict[str, str]) -> str:
    sections = []
    for field in sorted(by_field, key=str.casefold):
        events = sorted(by_field[field], key=sort_year)
        rows = "".join(event_listing(event, f"events/{event['pid']}/") for event in events)
        sections.append(f"""<section class="field-section" data-search="{escape(field)}" aria-labelledby="field-{field_slugs[field]}">
<h2 id="field-{field_slugs[field]}"><a href="fields/{field_slugs[field]}/">{escape(field)}</a> <span>{len(events)} events</span></h2>
<ol class="event-list">{rows}</ol></section>""")
    body = header([], "../index.html")
    body += f"""<main id="content" class="layout index-layout">
<p class="eyebrow">An atlas of mathematical ideas</p><h1>Browse the reference</h1>
<p class="lede">Read selected events by field, follow their connections, and inspect the sources behind each milestone. The map is another way into the same catalogue.</p>
<p class="approx-note">≈ marks an approximate map placement where a dated first statement is not established.</p>
<form role="search" id="reference-search" autocomplete="off"><label for="query">Search events, milestones, sources and people</label>
<input id="query" type="search" placeholder="Try group theory or Emmy Noether" aria-describedby="search-help">
<div class="filters"><label>Period <select id="period"><option value="">Any</option><option value="-99999,1500">Before 1500</option><option value="1500,1799">1500–1799</option><option value="1800,1899">1800–1899</option><option value="1900,99999">1900 on</option></select></label>
<label>Review <select id="tier"><option value="">Any</option><option value="direct">Direct review</option><option value="source-first">Source-first</option></select></label></div>
<p id="search-help">Filters the list below, including text inside milestones and sources. Every field and event link works without JavaScript. <a href="people/">People</a> · <a href="events.csv" download>Download all events (CSV)</a></p></form>
<p id="search-status" role="status" aria-live="polite"></p>
<div class="field-jump" aria-label="Jump to a field">{''.join(f'<a href="#field-{field_slugs[field]}">{escape(field)}</a>' for field in sorted(by_field, key=str.casefold))}</div>
<div id="fields">{''.join(sections)}</div></main>
<footer><a href="../index.html">Explore the map</a></footer>
<script src="search.js" defer></script>"""
    return page("Reference", "Browse fields, events, people, milestones, and sources in the Mathlas catalogue.", body, css="style.css")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    events = json.loads(SOURCE.read_text(encoding="utf-8"))
    by_pid = {event["pid"]: event for event in events}
    if len(by_pid) != len(events):
        raise ValueError("Duplicate event pid in source")
    by_field: dict[str, list[dict]] = defaultdict(list)
    for event in events:
        by_field[event["cl"]].append(event)
    field_slugs = {field: slug(field) for field in by_field}
    if len(set(field_slugs.values())) != len(field_slugs):
        raise ValueError("Field slug collision")

    # Event and field pages are generated entirely from the source catalogue.
    # Remove retired pages so old IDs cannot linger after an event is deleted.
    for section in ("events", "fields"):
        if (DEST / section).exists():
            shutil.rmtree(DEST / section)
    write(DEST / "index.html", index_page(by_field, field_slugs))
    for field, field_events in by_field.items():
        write(DEST / "fields" / field_slugs[field] / "index.html", field_page(field, field_events, field_slugs))
    linked, people_slugs = collect_people(events)
    if (DEST / "people").exists():
        shutil.rmtree(DEST / "people")
    for event in events:
        write(DEST / "events" / event["pid"] / "index.html", event_page(event, by_pid, field_slugs, people_slugs))
    for name, info in linked.items():
        write(DEST / "people" / people_slugs[name] / "index.html", person_page(name, info, by_pid, people_slugs, field_slugs))
    write(DEST / "people" / "index.html", people_index(linked, people_slugs))
    write(DEST / "events.csv", events_csv(events))
    write(DEST / "search-index.json", json.dumps({e["pid"]: search_text(e) for e in events}, ensure_ascii=False, separators=(",", ":")))
    print(f"Generated {len(events)} event pages, {len(by_field)} field pages and {len(linked)} people pages in {DEST}")


if __name__ == "__main__":
    main()
