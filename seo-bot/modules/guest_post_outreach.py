"""
Module 5 — Guest Post Outreach Engine
=====================================

1. Runs Google search-operator queries to surface niche-relevant sites that
   accept guest posts (e.g. `intitle:"write for us" security`).
2. For each prospect, asks Claude for: relevance score 0-10, suggested 3
   guest-post topics, and a 90-word personalised pitch email.
3. Exports a CSV ready for a CRM (Pipedrive / HubSpot) + one .txt email
   draft per prospect.

Output:
  data/outreach_<ts>.csv
  data/emails/<domain>.txt
"""
from __future__ import annotations

import re
from typing import Dict, List
from urllib.parse import urlparse

from config.settings import settings, DATA_DIR
from utils.csv_writer import write_csv
from utils.llm_client import ask
from utils.logger import get_logger
from utils.serp import search

log = get_logger("outreach")

OPERATORS = [
    'intitle:"write for us" security',
    'intitle:"guest post" security australia',
    'inurl:"write-for-us" cctv',
    '"contribute" "security industry" site:.au',
    '"submit a guest post" surveillance',
    '"become a contributor" security',
    'security blog "guest author" site:.au',
    'construction safety "guest post"',
    'retail loss prevention "write for us"',
]


def _prospects() -> List[Dict]:
    seen = set()
    out: List[Dict] = []
    for op in OPERATORS:
        for r in search(op, num=10):
            domain = urlparse(r["url"]).netloc.lower()
            if domain in seen or not domain:
                continue
            seen.add(domain)
            out.append({"domain": domain, "url": r["url"],
                        "title": r["title"], "snippet": r["snippet"], "operator": op})
    return out


def _enrich(prospect: Dict) -> Dict:
    prompt = (
        "You are a digital PR strategist for an Australian security services company "
        f"({settings.site_url}, focus: CCTV monitoring, alarm response, AI "
        "surveillance, construction/retail security).\n\n"
        "Evaluate this guest-post prospect:\n"
        f"- Domain: {prospect['domain']}\n"
        f"- Title: {prospect['title']}\n"
        f"- Snippet: {prospect['snippet']}\n\n"
        "Return STRICT JSON:\n"
        "{\n"
        '  "relevance_score": 0-10,\n'
        '  "rationale": "1 sentence",\n'
        '  "topic_ideas": ["topic 1","topic 2","topic 3"],\n'
        '  "pitch_email": "90-word personalised email body, no subject line"\n'
        "}"
    )
    import json
    raw = ask(prompt, fast=True, max_tokens=900)
    raw = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"relevance_score": 0, "rationale": "", "topic_ideas": [], "pitch_email": raw}


def run() -> str:
    rows: List[Dict] = []
    for p in _prospects():
        log.info(f"Prospect: {p['domain']}")
        enr = _enrich(p)
        rows.append({
            "domain": p["domain"],
            "url": p["url"],
            "relevance_score": enr.get("relevance_score"),
            "rationale": enr.get("rationale"),
            "topic_1": (enr.get("topic_ideas") or [""])[0],
            "topic_2": (enr.get("topic_ideas") or ["", ""])[1] if len(enr.get("topic_ideas", [])) > 1 else "",
            "topic_3": (enr.get("topic_ideas") or ["", "", ""])[2] if len(enr.get("topic_ideas", [])) > 2 else "",
            "operator": p["operator"],
        })
        # Email draft file
        (DATA_DIR / "emails" / f"{p['domain']}.txt").write_text(
            "Subject: Guest contribution idea for " + p["domain"] + "\n\n" +
            (enr.get("pitch_email") or ""),
            encoding="utf-8",
        )

    rows.sort(key=lambda r: (r.get("relevance_score") or 0), reverse=True)
    path = write_csv("outreach", rows,
                     fieldnames=["domain", "url", "relevance_score", "rationale",
                                 "topic_1", "topic_2", "topic_3", "operator"])
    log.info(f"Outreach sheet -> {path}")
    return str(path)


if __name__ == "__main__":
    run()
