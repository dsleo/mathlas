#!/usr/bin/env python3
"""Build a searchable preview of researched events and explicit open gaps."""

import html
import json
import unicodedata
from pathlib import Path

from validate_field_milestones import BASE, ROOT
from build_field_coverage import main as build_coverage


TARGET = ROOT / "public/field-emergence-milestones.html"
TARGET_JSON = ROOT / "public/field-emergence-milestones.json"
DATE_NAMES = (("conceptual", "First statement"), ("methodological", "First application"), ("institutional", "Naming / consolidation"))
ROLE_NAMES = {"precursor": "Precursor", "first_statement": "First statement", "first_application": "First application", "key_development": "Key development", "consolidation": "Consolidation", "naming": "Naming", "institution": "Institution", "recognition": "Recognition"}


def h(value):
    return html.escape(str(value), quote=True)


def fold(value):
    value = unicodedata.normalize("NFKD", value.casefold())
    return "".join(c for c in value if not unicodedata.combining(c))


def link(url, label):
    return f'<a href="{h(url)}" target="_blank" rel="noopener noreferrer">{h(label)}</a>'


def year_label(year, precision="year", end=None):
    if year is None:
        return "Undated"
    def n(value):
        return f"{abs(value)} BCE" if value < 0 else str(value)
    if precision == "range" and end is not None:
        return f"{n(year)}–{n(end)}"
    if precision == "decade":
        return f"c. {n(year)}"
    return n(year)


def milestone_card(m):
    date = year_label(m.get("year"), m.get("precision"), m.get("endYear"))
    sources = "".join(f'<li>{link(e["url"], e["source"])}<span>{h(e["claim"])}</span></li>' for e in m["evidence"])
    phase = f'<span class="phase">{h(m["phase"])}</span>' if m.get("phase") else ""
    work = f'<p class="work">{h(m["work"])}</p>' if m.get("work") else ""
    note = f'<p class="milestone-note">{h(m["note"])}</p>' if m.get("note") else ""
    return f'''<li class="milestone"><div class="timeline-date">{h(date)}</div><div class="timeline-content"><div class="milestone-meta"><span class="role role-{h(m['role'])}">{h(ROLE_NAMES[m['role']])}</span>{phase}<span class="confidence">{h(m['confidence'])} confidence</span></div><h4>{h(m['label'])}</h4><p>{h(m['description'])}</p>{work}<details class="evidence"><summary>{len(m['evidence'])} linked source{'s' if len(m['evidence']) != 1 else ''}</summary><ul>{sources}</ul>{note}</details></div></li>'''


def person_card(p):
    works = "".join(f'<li>{link(w["url"], w["citation"])} <span class="work-date">{h(w["year"])}</span><small>{h(w["whyItMatters"])}</small></li>' for w in p["works"])
    life = f' · {h(p["lifespan"])}' if p.get("lifespan") else ""
    return f'<section class="person"><h4>{link(p["biographyUrl"], p["name"])}</h4><p>{h(p["role"])}{life}</p><ul>{works}</ul></section>'


def event_card(row):
    dates = row["derivedDates"]
    def date_badge(key, label):
        date = dates[key]
        shown = year_label(date["start"], date["precision"], date["end"]) if date else "Open"
        grade = f' · grade {h(date["grade"])}' if date and date.get("grade") else ""
        return f'<span><b>{h(label)}</b> {h(shown)}{grade}</span>'
    badges = "".join(date_badge(key, label) for key, label in DATE_NAMES)
    search = fold(" ".join([row.get("pid") or "", row["eventId"], row["canonicalName"], *row["aliases"], *row.get("searchTerms", []), *(p["name"] for p in row["people"])]))
    aliases = " · ".join(row["aliases"]) or "None recorded"
    milestones = "".join(milestone_card(m) for m in row["milestones"])
    people = "".join(person_card(p) for p in row["people"])
    researched = row["researchStatus"] == "researched"
    status = f"{len(row['milestones'])} milestones" if researched else ("Candidates to review" if row["sourceCandidates"] else "Source search needed")
    if researched:
        detail = f'<ol class="timeline">{milestones}</ol><details class="people"><summary>People and cited works · {len(row["people"])}</summary><div class="people-grid">{people}</div></details>'
    else:
        leads = ''.join(f'<li>{link(c["url"], c["title"])} · {h(c["year"])}<small>Matched inherited citation: {h(c["inheritedCitation"])}</small></li>' for c in row["sourceCandidates"])
        lead_section = f'<details class="leads"><summary>Bibliographic search leads · {len(row["sourceCandidates"])}</summary><p>These records are candidates only. Their relevance, historical role and priority have not been checked.</p><ul>{leads}</ul></details>' if leads else ''
        searches = '; '.join(row.get('searchedSources', []))
        detail = f'<p class="pending">No source-adjudicated milestones yet. The three dates remain open.</p>{lead_section}<p class="searched"><b>Searched:</b> {h(searches)}</p>'
    return f'''<details class="event" id="{h(row.get('pid') or row['eventId'])}" data-search="{h(search)}" data-status="{h(row['researchStatus'])}"><summary><span class="pid">{h(row.get('pid') or row['eventId'])}</span><span class="event-title">{h(row['canonicalName'])}</span><span class="event-count">{h(status)}</span><span class="toggle" aria-hidden="true">⌄</span></summary><div class="event-body"><p class="event-id">Catalogue ID {h(row['eventId'])}</p><div class="derived">{badges}</div><p class="aliases"><b>Search aliases</b> {h(aliases)}</p>{detail}<details class="notes"><summary>Research notes and unresolved questions</summary><p>{h(row['notes'])}</p></details></div></details>'''


def main():
    build_coverage()
    coverage = json.loads((BASE / "coverage.json").read_text())
    rows = coverage["events"]
    TARGET_JSON.write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n")
    cards = "\n".join(event_card(row) for row in rows)
    count = len(rows)
    researched = coverage["statusCounts"]["researched"]
    candidate = coverage["statusCounts"].get("candidate_review", 0)
    search_needed = coverage["statusCounts"].get("source_search_needed", 0)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Field emergence · milestone review</title>
<style>
:root{{color-scheme:light;--paper:#f5f0e6;--ink:#302a23;--muted:#685e52;--line:#cfc3b4;--amber:#8a581e;--surface:#fffaf1;--soft:#eae0d0}}*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 ui-sans-serif,Helvetica,sans-serif}}a{{color:#754713;text-underline-offset:3px}}a:focus-visible,summary:focus-visible,input:focus-visible{{outline:2px solid var(--amber);outline-offset:3px}}.wrap{{width:min(1160px,calc(100% - 40px));margin:auto}}header{{padding:40px 0 31px;border-bottom:1px solid var(--line)}}.eyebrow{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:var(--amber);margin:0 0 13px}}h1{{font:400 clamp(38px,5vw,62px)/1.06 Georgia,serif;letter-spacing:-.04em;margin:0}}.intro{{max-width:760px;color:var(--muted);margin:15px 0 0}}.progress{{margin:23px 0 0;color:var(--ink);font-size:13px}}.progress strong{{font:400 25px Georgia,serif;margin-right:8px}}main{{padding:27px 0 90px}}.tools{{display:flex;gap:15px;align-items:end;flex-wrap:wrap;margin-bottom:20px}}label{{display:grid;gap:5px;text-transform:uppercase;letter-spacing:.08em;font-size:11px;font-weight:800;color:var(--muted)}}input{{height:44px;width:min(480px,calc(100vw - 40px));padding:0 13px;border:1px solid #a99a88;background:var(--surface);color:var(--ink);font:14px ui-sans-serif,Helvetica,sans-serif}}.shown{{font-size:12px;color:var(--muted);padding-bottom:11px}}.event{{border-top:1px solid var(--line)}}.event:last-of-type{{border-bottom:1px solid var(--line)}}.event>summary{{display:grid;grid-template-columns:55px minmax(0,1fr) 105px 20px;gap:15px;align-items:baseline;padding:19px 4px;cursor:pointer;list-style:none}}summary::-webkit-details-marker{{display:none}}.pid{{color:var(--amber);font-size:11px;font-weight:800}}.event-title{{font:400 clamp(19px,2.3vw,27px)/1.25 Georgia,serif}}.event-count{{color:var(--muted);font-size:12px;white-space:nowrap}}.toggle{{font-size:20px;color:var(--amber);transition:transform .2s}}.event[open] .toggle{{transform:rotate(180deg)}}.event-body{{padding:0 0 34px 74px}}.event-id{{font-size:11px;color:var(--muted);margin:0 0 12px}}.derived{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:15px}}.derived span{{border:1px solid var(--line);padding:5px 10px;background:var(--surface);font-size:12px}}.derived b{{font-size:10px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin-right:5px}}.aliases{{font-size:12px;color:var(--muted);margin:0 0 24px}}.aliases b{{text-transform:uppercase;letter-spacing:.07em;font-size:10px;color:var(--amber);margin-right:8px}}.timeline{{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}}.milestone{{display:grid;grid-template-columns:105px minmax(0,1fr);border-bottom:1px solid var(--line)}}.timeline-date{{padding:17px 12px 17px 0;font:400 20px Georgia,serif;color:var(--amber);white-space:nowrap}}.timeline-content{{border-left:1px solid var(--line);padding:17px 0 20px 19px}}.milestone-meta{{display:flex;align-items:center;flex-wrap:wrap;gap:6px;font-size:10px;text-transform:uppercase;letter-spacing:.06em;font-weight:800}}.role{{background:#dfcfb9;color:#553616;padding:2px 6px}}.role-precursor{{background:#e4e0d7;color:#635b50}}.phase{{color:var(--amber)}}.confidence{{margin-left:auto;color:var(--muted);font-weight:600}}.timeline h4{{font:400 20px/1.2 Georgia,serif;margin:8px 0 5px}}.timeline p{{font-size:13px;margin:0;max-width:750px}}.timeline .work{{font-style:italic;color:var(--muted);margin-top:7px;font-size:12px}}.evidence{{margin-top:8px;font-size:12px}}.evidence>summary,.people>summary,.notes>summary{{cursor:pointer;color:var(--amber);font-weight:700}}.evidence ul{{margin:8px 0;padding-left:18px}}.evidence li+li{{margin-top:6px}}.evidence li span{{display:block;color:var(--muted)}}.milestone-note{{color:var(--muted);font-size:12px!important;margin-top:8px!important}}.people,.notes{{border-bottom:1px solid var(--line);padding:15px 0}}.people-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px 35px;margin-top:18px}}.person{{border-top:1px solid var(--soft);padding-top:9px}}.person h4{{font-size:14px;margin:0}}.person p{{font-size:12px;color:var(--muted);margin:2px 0 8px}}.person ul{{padding-left:17px;margin:0;font-size:12px}}.person li+li{{margin-top:7px}}.person small{{display:block;color:var(--muted)}}.work-date{{color:var(--muted)}}.notes p{{max-width:780px;color:var(--muted);font-size:12px;overflow-wrap:anywhere}}.empty{{color:var(--muted)}}footer{{border-top:1px solid var(--line);padding:20px 0 35px;font-size:12px;color:var(--muted)}}
@media(max-width:720px){{.event>summary{{grid-template-columns:40px 1fr 16px;gap:8px}}.event-count{{grid-column:2;grid-row:2}}.toggle{{grid-column:3;grid-row:1}}.event-body{{padding-left:0}}.milestone{{grid-template-columns:78px minmax(0,1fr)}}.timeline-date{{font-size:16px}}.timeline-content{{padding-left:13px}}.people-grid{{grid-template-columns:1fr}}.confidence{{margin-left:0}}}}
</style></head><body><header><div class="wrap"><p class="eyebrow">Proofscape · evidence ledger</p><h1>The emergence of a field</h1><p class="intro">Each event is a sequence of public statements, applications, developments and named institutions. Private work appears as a precursor. The three summary dates are derived from the milestones; open dates stay open. Grade B has a linked bibliographic record; grade C uses a history page or primary text only. Grade A requires independent agreement and is not inferred from this direct pass.</p><p class="progress"><strong>{count} / 557</strong> events have completed milestone records</p></div></header><main class="wrap"><div class="tools"><label>Find an event, person or alias<input type="search" id="search" placeholder="Try Stone duality, Langlands, metric space…" autocomplete="off"></label><span class="shown" id="shown" aria-live="polite">Showing {count} events</span></div><div id="events">{cards}</div><p class="empty" id="empty" hidden>No completed milestones match this search.</p></main><footer><div class="wrap">This preview contains completed, schema-valid batches only. <a href="field-emergence-milestones.json">Download the milestone ledger</a>. <a href="field-emergence-reviewed.html">Open the earlier direct-pass review</a>.</div></footer><script>const cards=[...document.querySelectorAll('.event')],input=document.querySelector('#search'),shown=document.querySelector('#shown'),empty=document.querySelector('#empty');function fold(s){{return s.toLocaleLowerCase().normalize('NFKD').replace(/[\\u0300-\\u036f]/g,'')}}function update(){{const words=fold(input.value.trim()).split(/\\s+/).filter(Boolean);let n=0;for(const c of cards){{const ok=words.every(w=>c.dataset.search.includes(w));c.hidden=!ok;if(ok)n++}}shown.textContent=`Showing ${{n}} of ${{cards.length}} events`;empty.hidden=n!==0}}input.addEventListener('input',update);if(location.hash){{const id=decodeURIComponent(location.hash.slice(1));const target=document.getElementById(id);if(target?.matches('.event'))target.open=true}}</script></body></html>'''
    page = page.replace(f'{count} / 557</strong> events have completed milestone records', f'{researched} / {count}</strong> events have researched milestones · {candidate} have search leads · {search_needed} need further source search')
    page = page.replace('This preview contains completed, schema-valid batches only.', 'This preview lists the whole catalogue. Search leads are unverified and do not create historical dates.')
    page = page.replace('No completed milestones match this search.', 'No events match this search.')
    page = page.replace('</style></head>', '.pending{background:#fff4dc;border-left:3px solid var(--amber);padding:12px 15px;font-size:13px}.leads,.searched{font-size:12px;color:var(--muted)}.leads>summary{cursor:pointer;color:var(--amber);font-weight:700}.leads ul{padding-left:20px}.leads li{margin:8px 0}.leads small{display:block}.searched{margin-top:15px}</style></head>')
    TARGET.write_text(page)
    print(f"Built {TARGET.relative_to(ROOT)} with {count} events")


if __name__ == "__main__":
    main()
