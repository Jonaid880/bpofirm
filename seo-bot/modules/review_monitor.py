"""
Module 12 — Review Monitor + Reply Drafter (off-page SEO)
=========================================================

Pulls recent reviews from:
  * Google Business Profile (via Places Details API if GOOGLE_PLACES_API_KEY
    and GOOGLE_PLACE_ID set)
  * ProductReview.com.au (scrape of the public business page)
  * Trustpilot (scrape of the public business page)

For each new review, drafts an owner reply in Australian English. Drafts are
written to disk for human approval — auto-replying is fine on Google
(allowed) but the human should always glance, so we never auto-post.

Output:
  data/reviews_<ts>.csv
  data/emails/review-reply-<source>-<id>.txt
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Dict, List

from bs4 import BeautifulSoup

from config.settings import settings, DATA_DIR
from utils.csv_writer import write_csv
from utils.http import get
from utils.llm_client import ask
from utils.logger import get_logger

log = get_logger("reviews")

import os
GOOGLE_PLACES_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")
GOOGLE_PLACE_ID = os.getenv("GOOGLE_PLACE_ID", "")
PRODUCTREVIEW_SLUG = os.getenv("PRODUCTREVIEW_SLUG", "")        # e.g. "securityblogs"
TRUSTPILOT_DOMAIN = os.getenv("TRUSTPILOT_DOMAIN", "")          # e.g. "securityblogs.com.au"


def _google_reviews() -> List[Dict]:
    if not (GOOGLE_PLACES_KEY and GOOGLE_PLACE_ID):
        return []
    url = (
        "https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={GOOGLE_PLACE_ID}&fields=reviews,rating,user_ratings_total"
        f"&key={GOOGLE_PLACES_KEY}"
    )
    r = get(url)
    if not r or r.status_code != 200:
        return []
    try:
        revs = r.json().get("result", {}).get("reviews", [])
    except Exception:
        return []
    return [{
        "source": "google",
        "id": f"g-{rv.get('time')}",
        "rating": rv.get("rating"),
        "author": rv.get("author_name"),
        "text": rv.get("text", ""),
        "url": rv.get("author_url", ""),
        "ts": datetime.utcfromtimestamp(rv.get("time", 0)).isoformat() if rv.get("time") else "",
    } for rv in revs]


def _productreview() -> List[Dict]:
    if not PRODUCTREVIEW_SLUG:
        return []
    url = f"https://www.productreview.com.au/listings/{PRODUCTREVIEW_SLUG}"
    r = get(url)
    if not r or r.status_code != 200:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    out = []
    for card in soup.select("[itemprop='review']")[:20]:
        rating = card.select_one("[itemprop='ratingValue']")
        author = card.select_one("[itemprop='author']")
        body = card.select_one("[itemprop='reviewBody']")
        out.append({
            "source": "productreview",
            "id": f"pr-{hash(body.get_text()[:80]) if body else ''}",
            "rating": rating.get_text(strip=True) if rating else "",
            "author": author.get_text(strip=True) if author else "",
            "text": body.get_text(strip=True) if body else "",
            "url": url,
            "ts": "",
        })
    return out


def _trustpilot() -> List[Dict]:
    if not TRUSTPILOT_DOMAIN:
        return []
    url = f"https://www.trustpilot.com/review/{TRUSTPILOT_DOMAIN}"
    r = get(url)
    if not r or r.status_code != 200:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    out = []
    # Trustpilot embeds reviews in JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "{}")
        except Exception:
            continue
        revs = []
        if isinstance(data, dict) and "review" in data:
            revs = data["review"] if isinstance(data["review"], list) else [data["review"]]
        for rv in revs[:20]:
            out.append({
                "source": "trustpilot",
                "id": f"tp-{hash(rv.get('reviewBody','')[:80])}",
                "rating": (rv.get("reviewRating") or {}).get("ratingValue"),
                "author": (rv.get("author") or {}).get("name", ""),
                "text": rv.get("reviewBody", ""),
                "url": url,
                "ts": rv.get("datePublished", ""),
            })
    return out


def _draft_reply(rev: Dict) -> str:
    rating = float(rev.get("rating") or 0)
    tone = "warmly thank them, name one specific thing they mentioned" if rating >= 4 \
           else "apologise sincerely, offer a direct contact channel (no defensiveness), invite offline conversation"
    prompt = (
        "Draft an owner reply to this customer review. Australian English, max 60 "
        "words, no marketing fluff, no AI-spam phrases, no 'we value your "
        f"feedback'. Tone: {tone}. Sign off with 'The team at {settings.site_name}'.\n\n"
        f"Rating: {rev.get('rating')}\nAuthor: {rev.get('author')}\nReview: {rev.get('text')}"
    )
    return ask(prompt, fast=True, max_tokens=250)


def run() -> str:
    reviews = _google_reviews() + _productreview() + _trustpilot()
    log.info(f"Pulled {len(reviews)} reviews")
    rows: List[Dict] = []
    for rv in reviews:
        draft = _draft_reply(rv) if rv.get("text") else ""
        draft_path = ""
        if draft:
            p = DATA_DIR / "emails" / f"review-reply-{rv['source']}-{re.sub(r'[^a-zA-Z0-9-]', '_', str(rv['id']))[:40]}.txt"
            p.write_text(f"Reply to {rv['author']} ({rv['rating']}★):\n\n{draft}", encoding="utf-8")
            draft_path = str(p)
        rows.append({
            "source": rv["source"],
            "id": rv["id"],
            "rating": rv["rating"],
            "author": rv["author"],
            "text": rv["text"][:500],
            "url": rv["url"],
            "ts": rv["ts"],
            "draft_path": draft_path,
        })
    path = write_csv("reviews", rows,
                     fieldnames=["source", "id", "rating", "author", "text",
                                 "url", "ts", "draft_path"])
    log.info(f"Reviews -> {path}")
    return str(path)


if __name__ == "__main__":
    run()
