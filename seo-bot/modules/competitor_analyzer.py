"""
Module 2 — Competitor Analyzer
==============================

1. Pulls each competitor's sitemap.xml (and /sitemap_index.xml).
2. Extracts URL paths and uses Claude to classify each into a topical bucket
   (cctv-monitoring, alarm-response, ai-surveillance, etc.).
3. Crosses against our own sitemap (settings.site_url + /sitemap.xml) to
   find topics where competitors have N pages and we have 0 or few.
4. (Optional) Pulls top backlinks per competitor when AHREFS_API_KEY is set.

Output:
  data/competitor_pages_<ts>.csv
  data/competitor_gap_<ts>.csv
"""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from config.settings import settings
from utils.csv_writer import write_csv
from utils.http import get
from utils.llm_client import ask
from utils.logger import get_logger

log = get_logger("competitors")

TOPIC_BUCKETS = [
    "cctv-monitoring", "alarm-response", "ai-surveillance",
    "construction-security", "retail-security", "monitoring-centre",
    "access-control", "mobile-patrols", "guarding", "compliance-asial",
    "case-study", "pricing", "other",
]


def _fetch_sitemap_urls(base: str) -> List[str]:
    """Return all <loc> URLs from base/sitemap.xml (recursing into sitemap indexes)."""
    candidates = [base.rstrip("/") + p for p in ["/sitemap.xml", "/sitemap_index.xml"]]
    urls: List[str] = []
    for sm in candidates:
        r = get(sm)
        if not r or r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, "xml")
        locs = [loc.get_text(strip=True) for loc in soup.find_all("loc")]
        # If it's a sitemap index, recurse one level.
        for loc in locs:
            if loc.endswith(".xml"):
                r2 = get(loc)
                if r2 and r2.status_code == 200:
                    inner = BeautifulSoup(r2.text, "xml")
                    urls.extend(l.get_text(strip=True) for l in inner.find_all("loc"))
            else:
                urls.append(loc)
        if urls:
            break
    return urls


def _classify_batch(urls: List[str]) -> Dict[str, str]:
    """Ask Claude to classify a batch of URLs into TOPIC_BUCKETS."""
    if not urls:
        return {}
    sample = urls[:80]                 # cap per call to keep cost predictable
    prompt = (
        "Classify each URL below into exactly one bucket from this list:\n"
        f"{', '.join(TOPIC_BUCKETS)}\n\n"
        "Return one line per URL in the form: URL ||| bucket\n\n"
        + "\n".join(sample)
    )
    text = ask(prompt, fast=True, max_tokens=4000)
    mapping: Dict[str, str] = {}
    for line in text.splitlines():
        if "|||" not in line:
            continue
        url, bucket = [p.strip() for p in line.split("|||", 1)]
        if bucket not in TOPIC_BUCKETS:
            bucket = "other"
        mapping[url] = bucket
    return mapping


def _backlinks_via_ahrefs(domain: str) -> List[Dict]:
    """Pull top-50 backlinks for a domain via Ahrefs API (if key set)."""
    if not settings.ahrefs_api_key:
        return []
    url = (
        "https://api.ahrefs.com/v3/site-explorer/backlinks"
        f"?target={domain}&limit=50&mode=domain"
    )
    r = get(url, headers={"Authorization": f"Bearer {settings.ahrefs_api_key}"})
    if not r or r.status_code != 200:
        return []
    try:
        return r.json().get("backlinks", [])
    except Exception:
        return []


def run() -> Dict[str, str]:
    page_rows: List[Dict] = []
    coverage: Dict[str, Counter] = defaultdict(Counter)

    # Classify our site first
    our_urls = _fetch_sitemap_urls(settings.site_url)
    log.info(f"Our site: {len(our_urls)} URLs")
    our_map = _classify_batch(our_urls)
    for u, b in our_map.items():
        coverage["__us__"][b] += 1
        page_rows.append({"site": settings.site_url, "url": u, "bucket": b})

    # Classify each competitor
    for comp in settings.competitors:
        comp_urls = _fetch_sitemap_urls(comp)
        log.info(f"{comp}: {len(comp_urls)} URLs")
        cmap = _classify_batch(comp_urls)
        for u, b in cmap.items():
            coverage[comp][b] += 1
            page_rows.append({"site": comp, "url": u, "bucket": b})

    # Build gap table
    gap_rows: List[Dict] = []
    for bucket in TOPIC_BUCKETS:
        our_n = coverage["__us__"].get(bucket, 0)
        for comp in settings.competitors:
            their_n = coverage[comp].get(bucket, 0)
            if their_n > our_n:
                gap_rows.append({
                    "bucket": bucket,
                    "competitor": comp,
                    "competitor_pages": their_n,
                    "our_pages": our_n,
                    "gap": their_n - our_n,
                })
    gap_rows.sort(key=lambda r: r["gap"], reverse=True)

    p1 = write_csv("competitor_pages", page_rows, fieldnames=["site", "url", "bucket"])
    p2 = write_csv("competitor_gap", gap_rows,
                   fieldnames=["bucket", "competitor", "competitor_pages", "our_pages", "gap"])

    # Optional backlinks pass
    bl_rows: List[Dict] = []
    for comp in settings.competitors:
        domain = urlparse(comp).netloc
        for bl in _backlinks_via_ahrefs(domain):
            bl_rows.append({
                "competitor": domain,
                "referring_url": bl.get("url_from"),
                "anchor": bl.get("anchor"),
                "dr": bl.get("domain_rating"),
            })
    if bl_rows:
        write_csv("competitor_backlinks", bl_rows,
                  fieldnames=["competitor", "referring_url", "anchor", "dr"])

    log.info(f"Pages -> {p1}\nGap   -> {p2}")
    return {"pages": str(p1), "gap": str(p2)}


if __name__ == "__main__":
    run()
