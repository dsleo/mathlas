#!/usr/bin/env python3
"""Fetch a portrait for each landmark mathematician from Wikipedia/Wikimedia Commons, keeping only images whose licence
allows reuse (public domain, CC0, CC BY, CC BY-SA) and recording the author and licence for credit.

Writes public/portraits/<slug>.jpg (240 px thumbnails) and public/data/portraits.json. Needs network access.
"""

import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILM = ROOT / "data/field-film.json"
OUT_DIR = ROOT / "public/portraits"
OUT_JSON = ROOT / "public/data/portraits.json"
UA = "Mathlas/0.1 (https://github.com/dsleo/mathlas; portrait lookup for a research map)"
OK_LICENSE = re.compile(r"^(public domain|pd[- ]|cc0|cc[- ]by|cc[- ]by[- ]sa)", re.I)
# a few names where the plain name is not the Wikipedia title
TITLES = {"Maxim Kontsevich": "Maxim Kontsevich", "Pierre de Fermat": "Pierre de Fermat", "Abraham de Moivre": "Abraham de Moivre"}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def api(host, params):
    return json.loads(get(f"https://{host}/w/api.php?" + urllib.parse.urlencode({**params, "format": "json"})))


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()).strip("-")


def strip_tags(text):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text or "")).strip()


# names whose Wikipedia page image is unusable: pick a Commons file by hand (licence still checked)
FILES = {"John von Neumann": "John von Neumann.jpg", "Mikhail Gromov": "Mikhael Gromov.jpg"}  # Menelaus: the only Commons image is a helmeted warrior, likely the Spartan king, so no portrait


def main():
    names = sorted({p["name"] for p in json.loads(FILM.read_text())["people"]})
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    existing = json.loads(OUT_JSON.read_text()) if OUT_JSON.exists() else {}
    result = dict(existing)
    for name in names:
        if name in result:
            continue
        try:
            if name in FILES:
                filename = FILES[name]
                c = api("commons.wikimedia.org", {"action": "query", "titles": "File:" + filename, "prop": "imageinfo", "iiprop": "extmetadata|url", "iiurlwidth": 240,
                                                  "iiextmetadatafilter": "LicenseShortName|Artist|Credit|LicenseUrl|AttributionRequired"})
                thumb = next(iter(c["query"]["pages"].values()))["imageinfo"][0]["thumburl"]
            else:
                q = api("en.wikipedia.org", {"action": "query", "redirects": 1, "titles": TITLES.get(name, name), "prop": "pageimages", "piprop": "thumbnail|name", "pithumbsize": 240})
                page = next(iter(q["query"]["pages"].values()))
                thumb, filename = page.get("thumbnail", {}).get("source"), page.get("pageimage")
                if not thumb or not filename:
                    print(f"{name}: no image"); result[name] = None; continue
                c = api("commons.wikimedia.org", {"action": "query", "titles": "File:" + filename, "prop": "imageinfo", "iiprop": "extmetadata|url",
                                                  "iiextmetadatafilter": "LicenseShortName|Artist|Credit|LicenseUrl|AttributionRequired"})
            info = next(iter(c["query"]["pages"].values())).get("imageinfo", [{}])[0]
            meta = info.get("extmetadata", {})
            lic = strip_tags(meta.get("LicenseShortName", {}).get("value"))
            if not OK_LICENSE.match(lic):
                print(f"{name}: licence '{lic}' not reusable, skipped"); result[name] = None; continue
            (OUT_DIR / f"{slug(name)}.jpg").write_bytes(get(thumb))
            result[name] = {"file": f"portraits/{slug(name)}.jpg", "license": lic, "author": strip_tags(meta.get("Artist", {}).get("value"))[:160],
                            "source": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(filename.replace(" ", "_")), "licenseUrl": meta.get("LicenseUrl", {}).get("value")}
            print(f"{name}: {lic}")
        except Exception as error:  # a missing portrait is fine; the page falls back to a bust
            print(f"{name}: {error}"); result[name] = None
        time.sleep(0.3)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n")
    print(sum(1 for v in result.values() if v), "of", len(result), "portraits kept")


if __name__ == "__main__":
    main()
