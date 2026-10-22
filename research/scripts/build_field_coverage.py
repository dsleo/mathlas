#!/usr/bin/env python3
"""Cover every event without promoting search hits into historical milestones.

Completed milestone batches remain authoritative. Unresearched events are
explicitly open, with cached bibliographic candidates and compact review packets.
All outputs are deterministic from the catalogue, source cache, and completed
milestone files; no network or model calls occur here.
"""

import json
import re
from collections import Counter
from pathlib import Path

from discover_scale_work_records import tokens
from validate_field_milestones import BASE, ROOT, audit_file, derived_dates

CATALOGUE = ROOT / 'data/collection/field-events-merged.json'
SEARCH = BASE / 'scale/work-search.json'
SCALE = BASE / 'scale'
QUEUE = BASE / 'queue'
OUTPUT = BASE / 'coverage.json'
FOCUSED = ROOT / 'data/collection/field-map-focused-additions.json'


def batch_paths():
    return (sorted((BASE / 'pilot').glob('milestones*.json')) +
            sorted((BASE / 'second').glob('milestones*.json')) +
            sorted(SCALE.glob('milestones*.json')))


def completed_records():
    rows = {}
    for path in batch_paths():
        _, issues = audit_file(path.resolve())
        errors = [issue for issue in issues if issue['level'] == 'error']
        if errors:
            raise ValueError(f'{path}: {len(errors)} schema errors')
        for row in json.loads(path.read_text()):
            eid = row['eventId']
            if eid in rows:
                raise ValueError(f'Duplicate completed event: {eid}')
            rows[eid] = {**row, 'derivedDates': derived_dates(row),
                         'batchFile': str(path.relative_to(ROOT)),
                         'researchStatus': 'researched', 'sourceCandidates': [],
                         'searchTerms': []}
    return rows


def candidate_tier(candidate):
    if candidate.get('source') == 'arxiv_explicit_id':
        return 'explicit_arxiv_id'
    title = candidate.get('title') or ''
    if len(tokens(title)) >= 3 and candidate.get('yearMatch') is True and candidate.get('titleOverlap', 0) >= .8:
        return 'strong_title_year'
    if len(tokens(title)) >= 3 and candidate.get('yearMatch') is not False and candidate.get('titleOverlap', 0) >= .75:
        return 'plausible_title'
    return None


def title_prefix_in_citation(title, citation):
    """Short inherited titles often omit a subtitle; require a 4-word prefix."""
    def words(value):
        return re.findall(r'[a-z0-9]+', value.casefold())
    title_words, cited_words = words(title), words(citation)
    if len(title_words) < 5:
        return False
    prefix = title_words[:4]
    if sum(len(word) >= 5 for word in prefix) < 2:
        return False
    return any(cited_words[i:i + 4] == prefix for i in range(len(cited_words) - 3))


def candidates_for(source_row):
    candidates = []
    seen = set()
    for work in source_row.get('works', []):
        for candidate in work.get('candidates', []):
            tier = candidate_tier(candidate)
            if not tier and candidate.get('yearMatch') is True and title_prefix_in_citation(candidate.get('title') or '', work['citation']):
                tier = 'title_prefix_year'
            url = candidate.get('url') or ''
            if not tier or not url or url in seen or not candidate.get('year') or not candidate.get('title'):
                continue
            if url.startswith('http://arxiv.org/'):
                url = re.sub(r'v\d+$', '', url.replace('http://', 'https://'))
            if url in seen:
                continue
            seen.add(url)
            candidates.append({'title': candidate['title'], 'year': candidate['year'], 'url': url,
                               'inheritedCitation': work['citation'], 'matchTier': tier,
                               'candidateOnly': True})
    rank = {'explicit_arxiv_id': 0, 'strong_title_year': 1, 'title_prefix_year': 2, 'plausible_title': 3}
    candidates.sort(key=lambda c: (rank[c['matchTier']], c['year'], c['title']))
    return candidates[:3]


def pending_record(event, source_row, pid):
    aliases = list(dict.fromkeys(a.get('name', '').strip() for a in event.get('also', [])
                                 if isinstance(a, dict) and a.get('name', '').strip() and a['name'].strip() != event['name']))
    works = source_row.get('works', [])
    searched = [f'Crossref bibliographic search for {len(works)} inherited citation(s)']
    if any('arxiv:' in w['citation'].casefold() for w in works):
        searched.append('Explicit arXiv IDs in inherited citations')
    candidates = candidates_for(source_row)
    return {'pid': pid, 'eventId': event['id'], 'canonicalName': event['name'],
            'aliases': aliases, 'searchTerms': [*event.get('from', []), *event.get('to', [])],
            'phases': [], 'milestones': [], 'people': [],
            'notes': 'Automated bibliographic lookup only; historical roles and priority have not been adjudicated. Catalogue dates remain unverified.',
            'searchedSources': searched, 'sourceCandidates': candidates,
            'researchStatus': 'candidate_review' if candidates else 'source_search_needed',
            'derivedDates': {'conceptual': None, 'methodological': None, 'institutional': None},
            'catalogueDatesUnverified': event.get('dates')}


def compact_task(record):
    return {'eventId': record['eventId'], 'pid': record['pid'], 'name': record['canonicalName'],
            'summary': record.get('catalogueSummary'), 'catalogueDatesUnverified': record['catalogueDatesUnverified'],
            'inheritedWorks': record['inheritedWorks'], 'candidates': record['sourceCandidates'],
            'task': 'Check record identity and contents; decide whether each supports a specific milestone role, or leave it open. Do not infer priority from search rank.'}


def main():
    catalogue = json.loads(CATALOGUE.read_text())['events']
    if len(catalogue) != 557 or len({event['id'] for event in catalogue}) != 557:
        raise ValueError('Expected 557 unique catalogue events')
    sources = {row['eventId']: row for row in json.loads(SEARCH.read_text())['events']}
    staged = {row['eventId']: (row['pid'], batch)
              for batch in range(1, 53)
              for row in json.loads((SCALE / f'batch{batch:02d}.json').read_text())}
    completed = completed_records()
    catalog_ids = {event['id'] for event in catalogue}
    if set(completed) - catalog_ids or set(staged) - catalog_ids:
        raise ValueError('Completed or staged event absent from catalogue')
    if set(staged) | set(completed) != catalog_ids:
        raise ValueError('Catalogue events missing from both staging and completed research')
    rows = []
    for event in catalogue:
        eid = event['id']
        if eid in completed:
            row = completed[eid]
        else:
            source = sources.get(eid)
            if source is None or eid not in staged:
                raise ValueError(f'Missing source-search or staged input for {eid}')
            row = pending_record(event, source, staged[eid][0])
            row['catalogueSummary'] = event.get('why', '')
            row['inheritedWorks'] = [w['citation'] for w in source.get('works', [])]
        rows.append(row)
    focused = json.loads(FOCUSED.read_text())['entries']
    used_pids = {row.get('pid') or row['eventId'] for row in rows}
    for addition in focused:
        event, record = addition['catalogue'], addition['record']
        if event['id'] in catalog_ids or record['eventId'] != event['id'] or record['pid'] in used_pids:
            raise ValueError(f"Duplicate or mismatched focused event: {event['id']}")
        if record['researchStatus'] != 'researched' or not record['milestones']:
            raise ValueError(f"Focused event needs researched milestones: {event['id']}")
        for milestone in record['milestones']:
            if not milestone.get('evidence') or any(not source.get('url', '').startswith('https://') for source in milestone['evidence']):
                raise ValueError(f"Focused milestone needs linked evidence: {event['id']}")
        catalog_ids.add(event['id'])
        used_pids.add(record['pid'])
        rows.append(record)
    counts = Counter(row['researchStatus'] for row in rows)
    report = {'method': 'Completed milestones plus explicitly unadjudicated bibliographic candidates; no pending catalogue dates promoted',
              'totalEvents': len(rows), 'statusCounts': dict(counts), 'events': rows}
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    QUEUE.mkdir(exist_ok=True)
    packets = 0
    for batch in range(1, 53):
        pending = [row for row in rows if row['eventId'] in {event['eventId'] for event in json.loads((SCALE / f'batch{batch:02d}.json').read_text())}
                   and row['researchStatus'] != 'researched']
        target = QUEUE / f'batch{batch:02d}.json'
        if pending:
            target.write_text(json.dumps({'batch': batch, 'events': [compact_task(row) for row in pending]}, ensure_ascii=False, separators=(',', ':')) + '\n')
            packets += 1
        elif target.exists():
            target.unlink()
    print(json.dumps({'totalEvents': len(rows), 'statusCounts': dict(counts), 'reviewPackets': packets}))


if __name__ == '__main__':
    main()
