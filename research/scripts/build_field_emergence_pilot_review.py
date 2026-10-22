#!/usr/bin/env python3
"""Build a self-contained, read-only review page from the sourced pilot ledger."""

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/collection/enrichment/pilot/direct-research.json"
TARGET = ROOT / "public/field-emergence-pilot.html"
TARGET_JSON = ROOT / "public/field-emergence-pilot.json"
BATCH2 = ROOT / "data/collection/enrichment/batch-02-direct.json"
REVIEW = ROOT / "public/field-emergence-reviewed.html"
REVIEW_JSON = ROOT / "public/field-emergence-reviewed.json"
FIELDS = (("conceptual", "Conceptual"), ("methodological", "Methodological"), ("institutional", "Institutional"))


def h(value):
    return html.escape(str(value), quote=True)


def link(url, label):
    assert url.startswith("https://")
    return f'<a href="{h(url)}" target="_blank" rel="noopener noreferrer">{h(label)} ↗</a>'


def date_cell(key, label, item):
    d = item["dates"][key]
    year = f'{d["start"]}' if d["start"] is not None else "Open"
    grade = d["grade"] or "—"
    parts = [f'<section class="date-cell"><div class="date-top"><h4>{h(label)}</h4><span class="grade">{h(grade)}</span></div><div class="year">{year}</div>']
    if d["evidence"]:
        parts.append('<ul class="sources">')
        for source in d["evidence"]:
            parts.append(f'<li>{h(source["claim"])} <span class="source-name">{link(source["url"], source["source"])}</span></li>')
        parts.append('</ul>')
    if d["note"]:
        parts.append(f'<p class="date-note">{h(d["note"])}</p>')
    parts.append('</section>')
    return "".join(parts)


def people_section(item):
    if not item["people"]:
        return '<p class="empty">No sourced person assigned. The record explains why.</p>'
    out = ['<div class="people-grid">']
    for person in item["people"]:
        life = f' · {h(person["lifespan"])}' if person["lifespan"] else ""
        out.append(f'<section class="person"><h5>{link(person["biographyUrl"], person["name"])}</h5><p class="role">{h(person["role"])}{life}</p><ul>')
        for work in person["works"]:
            out.append(f'<li>{link(work["url"], work["citation"])} <span class="work-year">{h(work["year"])}</span><small>{h(work["whyItMatters"])}</small></li>')
        out.append('</ul></section>')
    out.append('</div>')
    return "".join(out)


def event_section(item):
    key = item.get("pid", item["eventId"])
    search = " ".join([key, item["eventId"], item["canonicalName"], *item["aliases"], *(person["name"] for person in item["people"])]).casefold()
    dates = item["dates"]
    missing = [key for key, _ in FIELDS if dates[key]["start"] is None]
    date_summary = " · ".join(f'{label[:1]} {dates[key]["start"] or "—"}' for key, label in FIELDS)
    out = [f'<details class="event" id="{h(key)}" data-search="{h(search)}" data-missing="{h(" ".join(missing))}">',
           '<summary><span class="event-index">', h(key), '</span><span class="event-name">', h(item["canonicalName"]), '</span><span class="event-years">', h(date_summary), '</span><span class="chevron" aria-hidden="true">⌄</span></summary>',
           '<div class="event-body"><p class="event-id">Catalogue ID ', h(item["eventId"]), '</p>',
           '<div class="aliases"><span>Search aliases</span> ', h(" · ".join(item["aliases"])), '</div>',
           '<div class="date-grid">']
    out.extend(date_cell(key, label, item) for key, label in FIELDS)
    out.append('</div><h3>People &amp; works</h3>')
    out.append(people_section(item))
    if item["firstTermUse"]:
        first = item["firstTermUse"]
        out.append(f'<p class="term">Earliest checked title use: <strong>{h(first["term"])}</strong> ({h(first["year"])}). {link(first["url"], first["status"])}</p>')
    out.extend(['<h3>Research note</h3><p class="research-note">', h(item["notes"]), '</p></div></details>'])
    return "".join(out)


def write_page(events, target, ledger_name, intro):
    counts = {key: sum(e["dates"][key]["start"] is not None for e in events) for key, _ in FIELDS}
    cards = "\n".join(event_section(e) for e in events)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Field emergence · {len(events)} directly reviewed events</title>
<style>
:root{{color-scheme:light;--paper:#f5f0e6;--ink:#302a23;--muted:#665b4e;--line:#cfc3b4;--amber:#8a581e;--wash:#fffaf1}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 ui-sans-serif,Helvetica,sans-serif}}a{{color:#754713;text-decoration-color:#ba9564;text-underline-offset:3px}}a:hover{{color:#4f2e0b}}a:focus-visible,summary:focus-visible,input:focus-visible,select:focus-visible{{outline:2px solid #9a5a13;outline-offset:3px}}
.wrap{{width:min(1160px,calc(100% - 48px));margin:auto}}header{{border-bottom:1px solid var(--line);padding:34px 0 30px}}.eyebrow{{text-transform:uppercase;color:var(--amber);font-size:11px;font-weight:800;letter-spacing:.16em;margin:0 0 14px}}h1{{font:400 clamp(38px,5vw,64px)/1.05 Georgia,CMU,serif;letter-spacing:-.045em;margin:0;max-width:850px}}.intro{{max-width:760px;color:var(--muted);margin:17px 0 0}}.intro strong{{color:var(--ink)}}
.metrics{{display:flex;flex-wrap:wrap;gap:0;margin:32px 0 0;border-top:1px solid var(--line)}}.metric{{min-width:165px;padding:16px 28px 4px 0;margin-right:30px}}.metric strong{{display:block;font:400 30px Georgia,CMU,serif;line-height:1.1}}.metric span{{font-size:12px;color:var(--muted)}}
main{{padding:26px 0 80px}}.toolbar{{display:flex;gap:12px;align-items:end;flex-wrap:wrap;margin-bottom:14px}}label{{display:grid;gap:5px;font-size:11px;text-transform:uppercase;font-weight:800;letter-spacing:.1em;color:var(--muted)}}input,select{{height:43px;padding:0 12px;border:1px solid #a99a88;background:#fffaf3;color:var(--ink);font:14px ui-sans-serif,Helvetica,sans-serif}}input{{width:min(460px,calc(100vw - 48px))}}select{{min-width:195px}}.showing{{color:var(--muted);font-size:12px;margin:0 0 14px}}
.event{{border-top:1px solid var(--line)}}.event:last-child{{border-bottom:1px solid var(--line)}}summary{{display:grid;grid-template-columns:48px minmax(0,1fr) auto 20px;gap:15px;align-items:baseline;padding:21px 4px;cursor:pointer;list-style:none}}summary::-webkit-details-marker{{display:none}}summary:hover .event-name{{color:var(--amber)}}.event-index{{color:var(--amber);font-size:11px;font-weight:800;letter-spacing:.1em}}.event-name{{font:400 clamp(20px,2.4vw,28px)/1.2 Georgia,CMU,serif;letter-spacing:-.02em}}.event-years{{color:var(--muted);white-space:nowrap;font-size:12px}}.chevron{{font-size:20px;color:var(--amber);transition:transform .2s}}details[open] .chevron{{transform:rotate(180deg)}}.event-body{{padding:0 0 28px 63px}}.event-id{{margin:0 0 8px;color:var(--muted);font-size:11px}}.aliases{{font-size:13px;color:var(--muted);margin-bottom:21px}}.aliases span{{font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--amber);margin-right:8px}}
.date-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}.date-cell{{padding:18px 20px 20px 0;min-width:0}}.date-cell + .date-cell{{border-left:1px solid var(--line);padding-left:20px}}.date-top{{display:flex;justify-content:space-between;align-items:center;gap:10px}}h4{{margin:0;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);font-size:11px}}.grade{{border:1px solid #b79767;color:var(--amber);padding:1px 6px;font-size:10px;font-weight:800}}.year{{font:400 32px Georgia,CMU,serif;margin:6px 0 12px}}.sources{{padding-left:16px;margin:0;font-size:12px}}.sources li+li{{margin-top:6px}}.source-name{{display:block;margin-top:3px}}.date-note{{font-size:12px;color:var(--muted);margin:11px 0 0}}h3{{font:400 19px Georgia,CMU,serif;margin:25px 0 8px}}.people-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 30px}}.person{{border-top:1px solid #e0d7ca;padding-top:11px}}h5{{font-size:14px;margin:0}}.role{{font-size:12px;color:var(--muted);margin:1px 0 9px}}.person ul{{padding-left:18px;margin:0;font-size:12px}}.person li+li{{margin-top:8px}}.person small{{display:block;color:var(--muted);font-size:11px}}.work-year{{color:var(--muted)}}.research-note,.term,.empty{{font-size:12px;color:var(--muted);max-width:850px;margin:0;overflow-wrap:anywhere}}.term{{margin-top:18px}}.empty-state{{padding:38px 0;color:var(--muted)}}footer{{border-top:1px solid var(--line);padding:19px 0 35px;font-size:12px;color:var(--muted)}}
@media(max-width:760px){{.wrap{{width:min(100% - 30px,1160px)}}summary{{grid-template-columns:35px 1fr 18px;gap:8px}}.event-years{{grid-column:2;grid-row:2}}.chevron{{grid-column:3;grid-row:1}}.event-body{{padding-left:43px}}.date-grid{{grid-template-columns:1fr}}.date-cell{{padding:15px 0}}.date-cell + .date-cell{{border-left:0;border-top:1px solid var(--line);padding-left:0}}.people-grid{{grid-template-columns:1fr}}.metrics{{gap:0}}.metric{{min-width:130px;margin-right:10px}}}}
</style></head><body>
<header><div class="wrap"><p class="eyebrow">Proofscape · research ledger</p><h1>When did a field emerge?</h1><p class="intro">{h(intro)} Each date has a linked record or a visible search note. These are direct research passes: grades B and C indicate evidence type; independent agreement and A grades are not available.</p><div class="metrics"><div class="metric"><strong>{counts['conceptual']}/{len(events)}</strong><span>conceptual dates evidenced</span></div><div class="metric"><strong>{counts['methodological']}/{len(events)}</strong><span>method dates evidenced</span></div><div class="metric"><strong>{counts['institutional']}/{len(events)}</strong><span>institutional dates evidenced</span></div></div></div></header>
<main class="wrap"><div class="toolbar"><label>Find an event or alias<input id="search" type="search" placeholder="Try Stone duality, categorification, Langlands…" autocomplete="off"></label><label>Date to inspect<select id="filter"><option value="">All reviewed events</option><option value="conceptual">Conceptual date missing</option><option value="methodological">Method date missing</option><option value="institutional">Institutional date missing</option></select></label></div><p class="showing" id="showing" aria-live="polite">Showing {len(events)} events</p><div id="events">{cards}</div><p class="empty-state" id="empty" hidden>No reviewed events match these filters.</p></main>
<footer><div class="wrap">Research snapshot: 17 October 2026. B = linked bibliographic or archival record; C = history source only. A missing date means the evidence has not established a defensible year. <a href="{h(ledger_name)}">Source ledger</a></div></footer>
<script>const events=[...document.querySelectorAll('.event')],search=document.querySelector('#search'),filter=document.querySelector('#filter'),count=document.querySelector('#showing'),empty=document.querySelector('#empty');function update(){{const q=search.value.trim().toLocaleLowerCase().split(/\\s+/).filter(Boolean),f=filter.value;let n=0;for(const item of events){{const ok=q.every(t=>item.dataset.search.includes(t))&&(!f||item.dataset.missing.split(' ').includes(f));item.hidden=!ok;if(ok)n++}}count.textContent=`Showing ${{n}} of ${{events.length}} reviewed events`;empty.hidden=n!==0}}search.addEventListener('input',update);filter.addEventListener('change',update);if(location.hash){{const target=document.querySelector(location.hash);if(target?.matches('.event'))target.open=true}}</script>
</body></html>'''
    target.write_text(page)


def main():
    pilot = json.loads(SOURCE.read_text())
    batch2 = json.loads(BATCH2.read_text())
    assert len(pilot["events"]) == 30 and len(batch2["events"]) == 10
    events = pilot["events"] + batch2["events"]
    assert len({e["eventId"] for e in events}) == 40
    write_page(pilot["events"], TARGET, TARGET_JSON.name, "A source-led review of 30 pilot events from a catalogue of 557.")
    TARGET_JSON.write_text(SOURCE.read_text())
    write_page(events, REVIEW, REVIEW_JSON.name, "A source-led review of 40 events from a catalogue of 557. The remaining 517 have not yet received this direct evidence pass.")
    REVIEW_JSON.write_text(json.dumps({"method": "two consecutive direct research batches; no independent comparison", "events": events}, ensure_ascii=False, indent=2) + "\n")
    print(TARGET)
    print(REVIEW)


if __name__ == "__main__":
    main()
