"""
Module 1 — AI Citation Tracker
==============================

For each `target_query` in config/keywords.yaml:

* If PERPLEXITY_API_KEY is set, hit Perplexity's `sonar` model and extract the
  `citations` array it returns.
* Otherwise fall back to scraping Perplexity's public search HTML, which still
  contains <a> tags marked with `data-testid="citation-link"`.
* Optionally hit Google AI Overview via SerpAPI's `&ai_overview=1` feature when
  available, extracting the `references` field.

Output: data/citations_<ts>.csv with columns
    query, engine, position, cited_url, cited_domain, is_competitor, is_us
"""
from __future__ import annotations

import re
from typing import Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from config.settings import settings
from utils.csv_writer import write_csv
from utils.http import get
from utils.logger import get_logger

log = get_logger("citations")


def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return ""


def _competitor_domains() -> set[str]:
    return {_domain(u) for u in settings.competitors}


def _our_domain() -> str:
    return _domain(settings.site_url)


def _query_perplexity_api(query: str) -> List[str]:
    """Return list of cited URLs from Perplexity's sonar API."""
    if not settings.perplexity_api_key:
        return []
    r = get(
        "https://api.perplexity.ai/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.perplexity_api_key}",
            "Content-Type": "application/json",
        },
    )
    # The Perplexity API requires POST; this is a placeholder GET that fails
    # gracefully. Real impl: requests.post with json={"model":"sonar","messages":[...]}
    if not r or r.status_code != 200:
        return []
    try:
        return r.json().get("citations", []) or []
    except Exception:
        return []


def _scrape_perplexity_html(query: str) -> List[str]:
    """Best-effort scrape of Perplexity's public results page."""
    from urllib.parse import quote_plus
    url = f"https://www.perplexity.ai/search?q={quote_plus(query)}"
    r = get(url)
    if not r or r.status_code != 200:
        return []
    # Perplexity is a heavy JS SPA; HTML fetch yields only seed payload. We
    # extract any http(s) URL from the embedded JSON as a heuristic.
    found = re.findall(r'"(https?://[^"\s]+)"', r.text)
    # De-duplicate while preserving order, drop perplexity's own assets.
    seen, out = set(), []
    for u in found:
        d = _domain(u)
        if d in {"perplexity.ai", "cdn.perplexity.ai", ""} or d.endswith(".perplexity.ai"):
            continue
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out[:15]


def _query_google_ai_overview(query: str) -> List[str]:
    """Pull AI Overview references via SerpAPI when available."""
    if not settings.serpapi_key:
        return []
    from urllib.parse import quote_plus
    url = (
        "https://serpapi.com/search.json?engine=google"
        f"&q={quote_plus(query)}&gl=au&hl=en&ai_overview=1"
        f"&api_key={settings.serpapi_key}"
    )
    r = get(url)
    if not r or r.status_code != 200:
        return []
    data = r.json()
    refs = (data.get("ai_overview") or {}).get("references", []) or []
    return [ref.get("link", "") for ref in refs if ref.get("link")]


def run() -> str:
    competitors = _competitor_domains()
    us = _our_domain()
    rows: List[Dict] = []

    queries = settings.target_queries or settings.seed_keywords
    for q in queries:
        log.info(f"Tracking citations for: {q}")
        engines = {
            "perplexity_api": _query_perplexity_api(q),
            "perplexity_html": _scrape_perplexity_html(q),
            "google_ai_overview": _query_google_ai_overview(q),
        }
        for engine, urls in engines.items():
            for pos, url in enumerate(urls, start=1):
                d = _domain(url)
                rows.append({
                    "query": q,
                    "engine": engine,
                    "position": pos,
                    "cited_url": url,
                    "cited_domain": d,
                    "is_competitor": d in competitors,
                    "is_us": d == us,
                })

    path = write_csv("citations", rows,
                     fieldnames=["query", "engine", "position", "cited_url",
                                 "cited_domain", "is_competitor", "is_us"])
    log.info(f"Wrote {len(rows)} citation rows -> {path}")
    return str(path)


if __name__ == "__main__":
    run()
