"""
Module 7 — Brand Mention Monitor
================================

For every brand alias in settings.brand_names AND every competitor domain,
query:

1. Google News RSS (free, no key) — returns recent news articles.
2. SERP for the brand name (via utils.serp) — returns top web pages mentioning it.

Then for each result, fetch the page and check whether it links to our site.
Unlinked mentions are flagged as link-reclamation opportunities.

Output: data/mentions_<ts>.csv
"""
from __future__ import annotations

from typing import Dict, List
from urllib.parse import quote_plus, urlparse

import feedparser
from bs4 import BeautifulSoup

from config.settings import settings
from utils.csv_writer import write_csv
from utils.http import get
from utils.logger import get_logger
from utils.serp import search

log = get_logger("mentions")


def _our_domain() -> str:
    return urlparse(settings.site_url).netloc.lower().replace("www.", "")


def _google_news(query: str) -> List[Dict]:
    url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-AU&gl=AU&ceid=AU:en"
    feed = feedparser.parse(url)
    return [
        {"source": "google_news", "title": e.get("title", ""), "url": e.get("link", ""),
         "published": e.get("published", "")}
        for e in feed.entries[:20]
    ]


def _has_link_to_us(page_url: str) -> bool:
    r = get(page_url)
    if not r or r.status_code != 200:
        return False
    soup = BeautifulSoup(r.text, "lxml")
    our = _our_domain()
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if our in href:
            return True
    return False


def run() -> str:
    rows: List[Dict] = []
    targets: List[str] = list(settings.brand_names)
    targets += [urlparse(c).netloc for c in settings.competitors]

    for target in targets:
        is_us = target in settings.brand_names
        log.info(f"Monitoring: {target} (is_us={is_us})")

        # Google News
        for item in _google_news(target):
            rows.append({
                "subject": target,
                "is_us": is_us,
                "source": "google_news",
                "title": item["title"],
                "url": item["url"],
                "published": item["published"],
                "links_to_us": _has_link_to_us(item["url"]) if is_us else False,
                "unlinked_mention": (is_us and not _has_link_to_us(item["url"])),
            })

        # Web SERP
        for r in search(f'"{target}"', num=10):
            rows.append({
                "subject": target,
                "is_us": is_us,
                "source": "web_serp",
                "title": r["title"],
                "url": r["url"],
                "published": "",
                "links_to_us": _has_link_to_us(r["url"]) if is_us else False,
                "unlinked_mention": (is_us and not _has_link_to_us(r["url"])),
            })

    path = write_csv("mentions", rows,
                     fieldnames=["subject", "is_us", "source", "title", "url",
                                 "published", "links_to_us", "unlinked_mention"])
    log.info(f"Mentions -> {path}")
    return str(path)


if __name__ == "__main__":
    run()
