"""
Module 10 — Broken Link Builder (off-page SEO)
==============================================

Workflow:

1. For each competitor in settings.competitors, fetch their top backlinks
   (Ahrefs API if AHREFS_API_KEY set; otherwise scrape a sample via SERP
   for `link:competitor.com`).
2. Visit each referring URL, parse all outbound <a href> links.
3. Test each outbound link — flag any returning 404 / 410 / connection error.
4. For each broken link whose anchor or surrounding text is relevant to our
   topics, draft an outreach email offering our matching page as a replacement.

Output:
  data/broken_links_<ts>.csv
  data/emails/broken-link-<domain>-<n>.txt
"""
from __future__ import annotations

from typing import Dict, List
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from config.settings import settings, DATA_DIR
from utils.csv_writer import write_csv
from utils.http import get
from utils.llm_client import ask
from utils.logger import get_logger
from utils.serp import search

log = get_logger("broken_links")

MAX_REFERRING_PER_COMPETITOR = 30
MAX_LINKS_CHECKED_PER_PAGE = 40


def _referring_urls_for(competitor_url: str) -> List[str]:
    """Cheap fallback: SERP for 'link:domain' style queries returns pages that mention competitor."""
    domain = urlparse(competitor_url).netloc.replace("www.", "")
    urls = []
    for q in [f'"{domain}" "resources"', f'"{domain}" "links"', f'link:{domain}']:
        for r in search(q, num=10):
            urls.append(r["url"])
    seen, out = set(), []
    for u in urls:
        if u and u not in seen:
            seen.add(u); out.append(u)
        if len(out) >= MAX_REFERRING_PER_COMPETITOR:
            break
    return out


def _ahrefs_backlinks(competitor_url: str) -> List[str]:
    if not settings.ahrefs_api_key:
        return []
    domain = urlparse(competitor_url).netloc
    url = (
        "https://api.ahrefs.com/v3/site-explorer/backlinks"
        f"?target={domain}&limit={MAX_REFERRING_PER_COMPETITOR}&mode=domain"
    )
    r = get(url, headers={"Authorization": f"Bearer {settings.ahrefs_api_key}"})
    if not r or r.status_code != 200:
        return []
    try:
        return [b.get("url_from") for b in r.json().get("backlinks", []) if b.get("url_from")]
    except Exception:
        return []


def _is_broken(url: str) -> bool:
    r = get(url, timeout=10, retries=0)
    if r is None:
        return True
    return r.status_code in (404, 410)


def _draft_pitch(referring_url: str, broken_link: str, anchor: str) -> str:
    prompt = (
        "Draft a 90-word personalised outreach email reporting a broken link.\n"
        f"Their page (still live): {referring_url}\n"
        f"Broken link they're pointing to: {broken_link}\n"
        f"Anchor text: {anchor}\n"
        f"Replacement we want them to use: {settings.site_url} (Australian security services — CCTV monitoring, alarm response, AI surveillance).\n\n"
        "Tone: friendly, brief, no pressure, no SEO jargon, no AI-spam phrases. Start with their content not ourselves. Output the email body only, no subject."
    )
    return ask(prompt, fast=True, max_tokens=400)


def run() -> str:
    rows: List[Dict] = []
    email_idx = 0

    for comp in settings.competitors:
        log.info(f"Backlinks for: {comp}")
        refs = _ahrefs_backlinks(comp) or _referring_urls_for(comp)
        for ref in refs:
            log.info(f"  scanning {ref}")
            page = get(ref, timeout=15, retries=0)
            if not page or page.status_code != 200:
                continue
            try:
                soup = BeautifulSoup(page.text, "lxml")
            except Exception:
                continue
            links = soup.find_all("a", href=True)[:MAX_LINKS_CHECKED_PER_PAGE]
            for a in links:
                href = urljoin(ref, a["href"])
                if not href.startswith("http"):
                    continue
                if urlparse(href).netloc == urlparse(ref).netloc:
                    continue
                if not _is_broken(href):
                    continue
                anchor = a.get_text(strip=True)[:120]
                row = {
                    "referring_url": ref,
                    "referring_domain": urlparse(ref).netloc,
                    "broken_url": href,
                    "broken_domain": urlparse(href).netloc,
                    "anchor": anchor,
                    "found_via_competitor": urlparse(comp).netloc,
                }
                rows.append(row)
                # Draft pitch
                email_idx += 1
                body = _draft_pitch(ref, href, anchor)
                (DATA_DIR / "emails" / f"broken-link-{email_idx:03d}-{urlparse(ref).netloc}.txt").write_text(
                    f"Subject: Broken link on {urlparse(ref).netloc}\n\n{body}", encoding="utf-8"
                )

    path = write_csv("broken_links", rows,
                     fieldnames=["referring_url", "referring_domain", "broken_url",
                                 "broken_domain", "anchor", "found_via_competitor"])
    log.info(f"Broken links -> {path} ({email_idx} pitches drafted)")
    return str(path)


if __name__ == "__main__":
    run()
