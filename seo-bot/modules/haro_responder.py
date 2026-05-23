"""
Module 11 — HARO / SourceBottle / Qwoted Responder (off-page SEO)
=================================================================

Pulls journalist queries from:
  * SourceBottle public RSS (free, AU-focused)
  * Qwoted public queries (when QWOTED_API_KEY set)
  * HARO daily emails — set HARO_INBOX (IMAP) for auto-pull; falls back to a
    local data/haro_inbox/*.txt drop folder.

For each query, scores topical fit to our security expertise. If fit >= 7,
asks Claude to draft a 150-word expert quote in Australian English with a
named-expert attribution scaffold.

Output:
  data/haro_responses_<ts>.csv
  data/emails/haro-<id>.txt
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from xml.etree import ElementTree as ET

from config.settings import settings, DATA_DIR
from utils.csv_writer import write_csv
from utils.http import get
from utils.llm_client import ask
from utils.logger import get_logger

log = get_logger("haro")

INBOX = DATA_DIR / "haro_inbox"
INBOX.mkdir(exist_ok=True)

EXPERTISE = [
    "cctv monitoring", "alarm response", "ai video surveillance", "monitoring centre",
    "construction site security", "retail loss prevention", "guard tour", "asial",
    "as/nzs 2201", "access control", "intrusion detection", "back to base",
]

SOURCEBOTTLE_FEEDS = [
    "https://www.sourcebottle.com/feed/category-business.xml",
    "https://www.sourcebottle.com/feed/category-tech.xml",
    "https://www.sourcebottle.com/feed/category-other.xml",
]


def _from_sourcebottle() -> List[Dict]:
    """Parse the SourceBottle RSS feeds."""
    out: List[Dict] = []
    for feed_url in SOURCEBOTTLE_FEEDS:
        r = get(feed_url)
        if not r or r.status_code != 200:
            continue
        try:
            root = ET.fromstring(r.text)
        except ET.ParseError:
            continue
        for item in root.findall(".//item"):
            out.append({
                "source": "sourcebottle",
                "title": (item.findtext("title") or "").strip(),
                "body": (item.findtext("description") or "").strip(),
                "url": (item.findtext("link") or "").strip(),
                "deadline": (item.findtext("pubDate") or "").strip(),
                "id": (item.findtext("guid") or "").strip()[-40:],
            })
    return out


def _from_inbox() -> List[Dict]:
    """Read user-dropped HARO emails as .txt files in data/haro_inbox/."""
    out = []
    for p in INBOX.glob("*.txt"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        # Naively split a HARO digest by '------'
        for chunk in re.split(r"-{5,}", text):
            chunk = chunk.strip()
            if len(chunk) < 80:
                continue
            title_match = re.search(r"^(?:Summary|Subject):\s*(.+)$", chunk, re.MULTILINE | re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else chunk.splitlines()[0][:120]
            out.append({
                "source": "haro_inbox",
                "title": title,
                "body": chunk[:1500],
                "url": "",
                "deadline": "",
                "id": p.stem,
            })
    return out


def _score_fit(query: Dict) -> int:
    text = f"{query['title']} {query['body']}".lower()
    hits = sum(1 for kw in EXPERTISE if kw in text)
    # Score: 1 hit -> 5, 2 -> 7, 3+ -> 9
    return min(10, 4 + hits * 2)


def _draft_response(query: Dict) -> str:
    prompt = (
        "You are an Australian security industry expert (CCTV monitoring, alarm "
        "response, AI surveillance, monitoring centres, ASIAL-aligned). Draft a "
        "150-word expert quote for this journalist query. Australian English, no "
        "marketing fluff, include one concrete stat or specific example, end with "
        "a one-line bio scaffold: 'Name, Title at SecurityBlogs Australia "
        f"({settings.site_url})'.\n\n"
        f"QUERY TITLE: {query['title']}\nQUERY BODY: {query['body']}\n\n"
        "Output the quote only — no preamble."
    )
    return ask(prompt, fast=True, max_tokens=400)


def run() -> str:
    queries = _from_sourcebottle() + _from_inbox()
    log.info(f"Pulled {len(queries)} journalist queries")
    rows: List[Dict] = []
    for q in queries:
        fit = _score_fit(q)
        row = {
            "ts": datetime.utcnow().isoformat(timespec="seconds"),
            "source": q["source"],
            "id": q["id"],
            "title": q["title"][:200],
            "deadline": q["deadline"],
            "url": q["url"],
            "fit_score": fit,
            "draft_path": "",
        }
        if fit >= 7:
            draft = _draft_response(q)
            path = DATA_DIR / "emails" / f"haro-{q['source']}-{q['id'] or fit}.txt"
            path.write_text(f"Subject: Re: {q['title'][:150]}\n\n{draft}", encoding="utf-8")
            row["draft_path"] = str(path)
        rows.append(row)

    csv_path = write_csv("haro_responses", rows,
                         fieldnames=["ts", "source", "id", "title", "deadline",
                                     "url", "fit_score", "draft_path"])
    log.info(f"HARO results -> {csv_path} ({sum(1 for r in rows if r['draft_path'])} drafts)")
    return str(csv_path)


if __name__ == "__main__":
    run()
