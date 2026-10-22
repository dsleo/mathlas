#!/usr/bin/env python3
"""Check every pending event's bibliographic leads without assigning historical dates.

This is a deliberately conservative bulk pass. It confirms the identity and
publication metadata of cached leads, and searches for one additional OpenAlex
lead when the existing packet has none. A match remains a candidate: neither
historical priority nor the milestone role can be inferred from metadata.
"""

import concurrent.futures
import datetime as dt
import json
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/collection/enrichment'
OUTPUT = BASE / 'bulk-source-audit.json'
REVIEW_QUEUE = BASE / 'bulk-review-queue.json'
USER_AGENT = 'proofscape-field-emergence-metadata-audit/1.0'
HEADERS = {'User-Agent': USER_AGENT, 'Accept': 'application/json'}
NS = {'a': 'http://www.w3.org/2005/Atom'}


def clean(text):
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', text.casefold())).strip()


def similar(a, b):
    return SequenceMatcher(None, clean(a), clean(b)).ratio()


def fetch_json(url):
    for attempt in range(3):
        try:
            response = requests.get(url, headers=HEADERS, timeout=20)
            if response.status_code in (429, 500, 502, 503, 504):
                time.sleep(1.5 * (attempt + 1))
                continue
            response.raise_for_status()
            return response.json(), None
        except Exception as exc:
            if attempt == 2:
                return None, str(exc)[:160]
            time.sleep(.4 * (attempt + 1))
    return None, 'retry limit'


def crossref(url):
    doi = urllib.parse.unquote(url.split('doi.org/', 1)[1])
    record, error = fetch_json('https://api.crossref.org/works/' + urllib.parse.quote(doi, safe='/'))
    if error:
        return None, error
    work = record['message']
    dates = []
    for field in ('published-online', 'published-print', 'published', 'issued'):
        value = work.get(field, {}).get('date-parts', [])
        if value and value[0]:
            dates.append({'field': field, 'year': value[0][0]})
    return {'title': (work.get('title') or [''])[0], 'yearRecords': dates,
            'authors': [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in work.get('author', [])[:8]],
            'abstractAvailable': bool(work.get('abstract')), 'recordUrl': 'https://doi.org/' + doi}, None


def arxiv(url):
    identifier = url.split('/abs/', 1)[1]
    response = requests.get('https://export.arxiv.org/api/query', params={'id_list': identifier},
                            headers={'User-Agent': USER_AGENT}, timeout=20)
    response.raise_for_status()
    tree = ET.fromstring(response.text)
    entry = tree.find('a:entry', NS)
    if entry is None:
        return None, 'no arXiv entry'
    title = ' '.join((entry.findtext('a:title', default='', namespaces=NS)).split())
    published = entry.findtext('a:published', default='', namespaces=NS)
    authors = [author.findtext('a:name', default='', namespaces=NS)
               for author in entry.findall('a:author', NS)]
    return {'title': title, 'yearRecords': [{'field': 'first_public_submission', 'year': int(published[:4])}] if published else [],
            'authors': authors[:8], 'abstractAvailable': bool(entry.findtext('a:summary', default='', namespaces=NS)),
            'recordUrl': 'https://arxiv.org/abs/' + identifier}, None


def check_candidate(candidate):
    url = candidate['url']
    try:
        if 'doi.org/' in url:
            metadata, error = crossref(url)
        elif 'arxiv.org/abs/' in url:
            metadata, error = arxiv(url)
        else:
            metadata, error = None, 'metadata service not implemented for URL'
    except Exception as exc:
        metadata, error = None, str(exc)[:160]
    result = {'candidate': candidate, 'record': metadata, 'error': error, 'candidateOnly': True,
              'historicalRoleChecked': False, 'priorityChecked': False}
    if metadata:
        title_score = similar(candidate['title'], metadata['title'])
        years = {d['year'] for d in metadata['yearRecords']}
        result['identityCheck'] = {'titleSimilarity': round(title_score, 3),
                                   'yearMatches': candidate['year'] in years,
                                   'status': 'metadata_match' if title_score >= .82 and candidate['year'] in years else 'metadata_review'}
    return result


def for_event_candidate(candidate, shared_result):
    """Re-evaluate identity for this citation when several events share one URL."""
    result = {**shared_result, 'candidate': candidate}
    metadata = result.get('record')
    if metadata:
        score = similar(candidate['title'], metadata['title'])
        years = {item['year'] for item in metadata['yearRecords']}
        result['identityCheck'] = {'titleSimilarity': round(score, 3),
                                   'yearMatches': candidate['year'] in years,
                                   'status': 'metadata_match' if score >= .82 and candidate['year'] in years else 'metadata_review'}
    return result


def search_lead(name):
    query = urllib.parse.urlencode({'search': name, 'per-page': 1})
    result, error = fetch_json('https://api.openalex.org/works?' + query)
    if error:
        return {'candidateOnly': True, 'error': error}
    items = result.get('results') or []
    if not items:
        return {'candidateOnly': True, 'status': 'no_result'}
    item = items[0]
    title = item.get('display_name') or ''
    return {'candidateOnly': True, 'status': 'search_lead_only',
            'title': title, 'year': item.get('publication_year'),
            'url': (item.get('primary_location') or {}).get('landing_page_url') or item.get('doi') or item.get('id'),
            'titleSimilarityToEvent': round(similar(name, title), 3),
            'historicalRoleChecked': False, 'priorityChecked': False}


def fallback_lead(name):
    query = urllib.parse.urlencode({'query.bibliographic': name, 'rows': 1})
    result, error = fetch_json('https://api.crossref.org/works?' + query)
    if error:
        return {'candidateOnly': True, 'status': 'search_error', 'error': error,
                'historicalRoleChecked': False, 'priorityChecked': False}
    items = result.get('message', {}).get('items') or []
    if not items:
        return {'candidateOnly': True, 'status': 'no_result',
                'historicalRoleChecked': False, 'priorityChecked': False}
    item = items[0]
    title = (item.get('title') or [''])[0]
    year = (item.get('published', {}).get('date-parts') or [[None]])[0][0]
    return {'candidateOnly': True, 'status': 'search_lead_only', 'source': 'Crossref fallback',
            'title': title, 'year': year, 'url': item.get('URL'),
            'titleSimilarityToEvent': round(similar(name, title), 3),
            'historicalRoleChecked': False, 'priorityChecked': False}


def write_review_queue(audit):
    queue = []
    for event in audit['events']:
        confirmed = [h for h in event['cachedLeadChecks']
                     if h.get('identityCheck', {}).get('status') == 'metadata_match']
        fresh = event['additionalSearch']
        similarity = (fresh or {}).get('titleSimilarityToEvent', 0)
        if confirmed:
            tier = 'read_confirmed_records'
        elif similarity >= .75:
            tier = 'check_new_title_lead'
        else:
            tier = 'targeted_primary_or_history_search'
        queue.append({'eventId': event['eventId'], 'pid': event['pid'],
                      'canonicalName': event['canonicalName'], 'reviewTier': tier,
                      'confirmedRecordCount': len(confirmed),
                      'newLeadTitleSimilarity': similarity if fresh else None,
                      'historicalRolesOpen': True})
    queue.sort(key=lambda x: (rank_for_tier(x['reviewTier']), -x['confirmedRecordCount'],
                              -(x['newLeadTitleSimilarity'] or 0), x['pid']))
    REVIEW_QUEUE.write_text(json.dumps({'totalEvents': len(queue), 'events': queue},
                                       ensure_ascii=False, indent=2) + '\n')


def rank_for_tier(tier):
    return {'read_confirmed_records': 1, 'check_new_title_lead': 2,
            'targeted_primary_or_history_search': 3}[tier]


def recover():
    audit = json.loads(OUTPUT.read_text())
    failed = [e for e in audit['events'] if e['additionalSearch'] and e['additionalSearch'].get('error')]
    print(f'Recovering {len(failed)} failed fresh-lead searches with Crossref', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(lambda e: fallback_lead(e['canonicalName']), failed))
    for event, result in zip(failed, results):
        event['additionalSearch'] = result
    for event in audit['events']:
        for hit in event['cachedLeadChecks']:
            if hit['error'] and 'doi.org/' in hit['candidate']['url']:
                hit.update(check_candidate(hit['candidate']))
    audit['counts']['metadataMatches'] = sum(h.get('identityCheck', {}).get('status') == 'metadata_match'
                                             for e in audit['events'] for h in e['cachedLeadChecks'])
    audit['counts']['metadataReviewOrError'] = audit['counts']['cachedLeadsChecked'] - audit['counts']['metadataMatches']
    audit['counts']['additionalSearchLeads'] = sum(e['additionalSearch'].get('status') == 'search_lead_only'
                                                 for e in audit['events'] if e['additionalSearch'])
    audit['counts']['additionalSearchErrors'] = sum(bool(e['additionalSearch'].get('error'))
                                                  for e in audit['events'] if e['additionalSearch'])
    audit['generatedAtUtc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    OUTPUT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
    write_review_queue(audit)
    print(json.dumps(audit['counts']), flush=True)


def main():
    coverage = json.loads((BASE / 'coverage.json').read_text())
    pending = [e for e in coverage['events'] if e['researchStatus'] != 'researched']
    if not pending:
        raise ValueError('No pending events in the coverage ledger')
    candidates = {c['url']: c for event in pending for c in event['sourceCandidates']}
    print(f'Checking {len(pending)} events, {len(candidates)} unique cached leads, '
          f'{sum(not e["sourceCandidates"] for e in pending)} lead-free searches', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        checked = dict(zip(candidates, pool.map(check_candidate, candidates.values())))
    lead_free = [e for e in pending if not e['sourceCandidates']]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        searched = dict(zip((e['eventId'] for e in lead_free),
                            pool.map(lambda e: search_lead(e['canonicalName']), lead_free)))
    rows = []
    for event in pending:
        hits = [for_event_candidate(c, checked[c['url']]) for c in event['sourceCandidates']]
        rows.append({'eventId': event['eventId'], 'pid': event['pid'],
                     'canonicalName': event['canonicalName'],
                     'cachedLeadChecks': hits,
                     'additionalSearch': searched.get(event['eventId']),
                     'milestoneAdjudication': 'open',
                     'note': 'Bulk metadata pass only. A historical role/date needs a source-content and priority review.'})
    counts = {'eventsChecked': len(rows), 'cachedLeadsChecked': sum(len(x['cachedLeadChecks']) for x in rows),
              'metadataMatches': sum(h.get('identityCheck', {}).get('status') == 'metadata_match' for x in rows for h in x['cachedLeadChecks']),
              'metadataReviewOrError': sum(h.get('identityCheck', {}).get('status') != 'metadata_match' for x in rows for h in x['cachedLeadChecks']),
              'additionalSearches': len(lead_free),
              'additionalSearchLeads': sum(x['additionalSearch'].get('status') == 'search_lead_only' for x in rows if x['additionalSearch']),
              'milestonesPromoted': 0}
    OUTPUT.write_text(json.dumps({'generatedAtUtc': dt.datetime.now(dt.timezone.utc).isoformat(),
                                  'method': 'Bulk bibliographic metadata and discovery audit; candidate-only results',
                                  'counts': counts, 'events': rows}, ensure_ascii=False, indent=2) + '\n')
    write_review_queue({'events': rows})
    print(json.dumps(counts), flush=True)


if __name__ == '__main__':
    if '--recover' in sys.argv:
        recover()
    else:
        main()
