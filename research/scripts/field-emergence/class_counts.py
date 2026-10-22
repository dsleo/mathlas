#!/usr/bin/env python3
"""Document counts for (MSC class pair, year window) without the zbMATH dump.

Two routes, both resumable through a jsonl cache (one line per answer):

  api     zbMATH Open REST API (api.zbmath.org/v1/document/_search), exact
          publication year (py:), any-position MSC match (cc:). Slow (0.4-25 s
          per query), 502s above ~4 concurrent. One query per (pair, window).
  sparql  MaRDI portal SPARQL endpoint (query.portal.mardi4nfdi.de/sparql),
          which mirrors zbMATH Open (4.54M documents, full MSC lists). It has
          NO publication year: the only date is P28 "publication date", which
          is the zbMATH review/entry date (0-11 years after publication, see the
          report). Counts are therefore by REVIEW YEAR. One query per pair
          returns every year in the span; a "matrix" call returns every class
          pair for one year (about 80 s, 5 MB, ~18k pairs for 1995).

Classes are MSC prefixes of length 2 or 3 ("37", "37A"); pairs are "37A:11B".

Examples (run from the repo root):
  python3 scripts/field-emergence/class_counts.py query --route api \
      --pairs 37A:11B,05C:60K --windows 1990-1999,2000-2009
  python3 scripts/field-emergence/class_counts.py query --route sparql \
      --pairs 37A:11B --windows 1990-1999
  python3 scripts/field-emergence/class_counts.py matrix --years 1990-1999

Politeness: at most 4 workers (default 2 for sparql, which answers 429 with a
Retry-After header, honoured here). Results go to stdout as jsonl as well.
"""
import argparse, json, os, re, subprocess, sys, tempfile, threading, time, urllib.parse
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "class_counts_cache.jsonl")
MATRIX = os.path.join(HERE, "class_matrix_review_year.jsonl")
API = "https://api.zbmath.org/v1/document/_search"
SPARQL = "https://query.portal.mardi4nfdi.de/sparql"
PFX = "PREFIX wdt: <https://portal.mardi4nfdi.de/prop/direct/>\n"
LOCK = threading.Lock()


def curl(args, retries=6):
    """Run curl, return (http_code, body). Honours Retry-After on 429; retries 5xx/timeouts."""
    for k in range(retries):
        with tempfile.TemporaryDirectory() as td:
            body, hdr = os.path.join(td, "b"), os.path.join(td, "h")
            p = subprocess.run(["curl", "-s", "-o", body, "-D", hdr, "-w", "%{http_code}"] + args,
                               capture_output=True, text=True)
            code = int(p.stdout.strip() or 0)
            text = open(body, errors="replace").read() if os.path.exists(body) else ""
            if code == 429:
                m = re.search(r"(?i)retry-after:\s*(\d+)", open(hdr).read() if os.path.exists(hdr) else "")
                time.sleep(int(m.group(1)) + 2 if m else 20)
                continue
            if code == 0 or code >= 500:
                time.sleep(5 * (k + 1))
                continue
            return code, text
    return None, ""


# ---------------------------------------------------------------- cache
def load(path):
    d = {}
    if os.path.exists(path):
        for l in open(path):
            try:
                r = json.loads(l)
            except ValueError:
                continue
            d[r["k"]] = r
    return d


def put(path, rec):
    with LOCK:
        with open(path, "a") as f:
            f.write(json.dumps(rec) + "\n")


# ---------------------------------------------------------------- api route
def api_count(a, b, w):
    w = f"{w[0]}-{w[1]}"
    q = f"cc:{a} cc:{b} py:{w}" if a != b else f"cc:{a} py:{w}"
    code, text = curl(["--max-time", "120", f"{API}?page=0&results_per_page=1&search_string=" + urllib.parse.quote(q)])
    try:
        st = json.loads(text)["status"]
    except Exception:
        return None
    if st.get("nr_total_results") is not None:
        return st["nr_total_results"]
    if st.get("status_code") == 404 and "No results" in json.dumps(st):
        return 0
    return None


# ---------------------------------------------------------------- sparql route
def sparql(query, timeout=400):
    with tempfile.NamedTemporaryFile("w", suffix=".rq", delete=False) as f:
        f.write(query)
    try:
        code, text = curl(["--max-time", str(timeout), "-H", "Accept: application/sparql-results+json",
                           "--data-urlencode", f"query@{f.name}", SPARQL])
    finally:
        os.unlink(f.name)
    if code != 200:
        return None
    try:
        return json.loads(text)["results"]["bindings"]
    except Exception:
        return None


def date_filter(var, y0, y1):
    return (f'FILTER({var} >= "{y0}-01-01T00:00:00Z"^^<http://www.w3.org/2001/XMLSchema#dateTime> && '
            f'{var} < "{y1 + 1}-01-01T00:00:00Z"^^<http://www.w3.org/2001/XMLSchema#dateTime>)')


def sparql_pair_years(a, b, y0, y1):
    """{year: count} of documents carrying both classes, by review year, for y0..y1."""
    m2 = "" if a == b else f'?s wdt:P226 ?m2 . FILTER(STRSTARTS(?m2,"{b}"))'
    q = (PFX + "SELECT ?y (COUNT(*) AS ?n) WHERE { SELECT DISTINCT ?s ?y WHERE {\n"
         f'?s wdt:P28 ?d . {date_filter("?d", y0, y1)}\n'
         f'?s wdt:P226 ?m1 . FILTER(STRSTARTS(?m1,"{a}"))\n{m2}\nBIND(YEAR(?d) AS ?y) }}}} GROUP BY ?y')
    rows = sparql(q)
    if rows is None:
        return None
    return {int(r["y"]["value"]): int(r["n"]["value"]) for r in rows}


def sparql_matrix_year(y):
    """{ 'A|B': n } for every 3-character class pair (A<B) whose documents have review year y, plus
    'A|A' for single-class totals."""
    inner = lambda v, m, d: (f'{{ SELECT DISTINCT ?s ?{v} WHERE {{ ?s wdt:P28 ?{d} . {date_filter("?" + d, y, y)} '
                             f'?s wdt:P226 ?{m} . BIND(SUBSTR(?{m},1,3) AS ?{v}) }} }}')
    q = (PFX + "SELECT ?a ?b (COUNT(*) AS ?n) WHERE {\n" + inner("a", "m", "d") + "\n" + inner("b", "m2", "d2") +
         "\nFILTER(?a <= ?b) } GROUP BY ?a ?b")
    rows = sparql(q, timeout=600)
    if rows is None:
        return None
    return {f'{r["a"]["value"]}|{r["b"]["value"]}': int(r["n"]["value"]) for r in rows}


def matrix_cmd(args):
    done = load(MATRIX)
    y0, y1 = map(int, args.years.split("-"))
    todo = [y for y in range(y0, y1 + 1) if f"y{y}" not in done]
    print(f"{len(todo)} years to fetch", file=sys.stderr)

    def one(y):
        t = time.time()
        m = sparql_matrix_year(y)
        if m is None:
            print(f"year {y}: failed", file=sys.stderr)
            return
        put(MATRIX, {"k": f"y{y}", "year": y, "route": "sparql-review-year", "pairs": m})
        print(f"year {y}: {len(m)} pairs, {time.time() - t:.0f}s", file=sys.stderr)

    with ThreadPoolExecutor(min(args.workers, 4)) as ex:
        list(ex.map(one, todo))


# ---------------------------------------------------------------- query command
def parse_windows(s):
    out = []
    for w in s.split(","):
        a, b = map(int, w.split("-"))
        out.append((a, b))
    return out


def query_cmd(args):
    pairs = sorted({tuple(sorted(p.split(":"))) for p in args.pairs.split(",")})
    wins = parse_windows(args.windows)
    cache = load(CACHE)
    matrix = load(MATRIX)
    results = []

    def cached(a, b, w):
        return cache.get(f"{args.route}|{a}|{b}|{w[0]}-{w[1]}")

    def from_matrix(a, b, w):
        # only for 3-character classes; needs every year of the window in the matrix
        if len(a) != 3 or len(b) != 3 or any(f"y{y}" not in matrix for y in range(w[0], w[1] + 1)):
            return None
        return sum(matrix[f"y{y}"]["pairs"].get(f"{a}|{b}", 0) for y in range(w[0], w[1] + 1))

    def emit(a, b, w, n, src):
        rec = {"k": f"{args.route}|{a}|{b}|{w[0]}-{w[1]}", "route": args.route, "a": a, "b": b,
               "window": f"{w[0]}-{w[1]}", "n": n}
        if src != "cache":
            put(CACHE, rec)
        results.append({**rec, "src": src})

    if args.route == "api":
        jobs = []
        for a, b in pairs:
            for w in wins:
                c = cached(a, b, w)
                if c and c["n"] is not None:
                    emit(a, b, w, c["n"], "cache")
                else:
                    jobs.append((a, b, w))

        def one(j):
            n = api_count(*j)
            if n is not None:
                emit(*j[:2], j[2], n, "api")
        with ThreadPoolExecutor(min(args.workers, 4)) as ex:
            list(ex.map(one, jobs))
    else:
        jobs = []
        for a, b in pairs:
            need = []
            for w in wins:
                c = cached(a, b, w)
                n = c["n"] if c else from_matrix(a, b, w)
                if n is not None:
                    emit(a, b, w, n, "cache" if c else "matrix")
                else:
                    need.append(w)
            if need:
                jobs.append((a, b, need))

        def one(j):
            a, b, need = j
            # one query per pair covering the whole span of the missing windows
            y0, y1 = min(w[0] for w in need), max(w[1] for w in need)
            yc = sparql_pair_years(a, b, y0, y1)
            if yc is None:
                print(f"{a}:{b} failed", file=sys.stderr)
                return
            for w in need:
                emit(a, b, w, sum(n for y, n in yc.items() if w[0] <= y <= w[1]), "sparql")
        with ThreadPoolExecutor(min(args.workers, 4)) as ex:
            list(ex.map(one, jobs))

    for r in sorted(results, key=lambda r: (r["a"], r["b"], r["window"])):
        print(json.dumps(r))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("query")
    q.add_argument("--pairs", required=True, help="comma list like 37A:11B,05C:60K (2 or 3 characters each)")
    q.add_argument("--windows", required=True, help="comma list like 1990-1999,2000-2009")
    q.add_argument("--route", choices=["api", "sparql"], default="api")
    q.add_argument("--workers", type=int, default=2)
    m = sub.add_parser("matrix")
    m.add_argument("--years", required=True, help="e.g. 1990-1999 (review years, SPARQL route)")
    m.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    (query_cmd if a.cmd == "query" else matrix_cmd)(a)
