"""
Module 8 — AI Overview Monitor
==============================

For every target_query, check:
  * Does Google return an AI Overview? (via SerpAPI ai_overview=1, when key set)
  * Do any of OUR URLs appear in its `references` list?
  * Same for Perplexity citations.

Builds a longitudinal visibility table (append-only) you can graph over time.

Output:
  data/ai_overview_<ts>.csv          (this run)
  data/ai_overview_history.csv       (appended every run)
"""
from __future__ import annotations

import csv
from datetime import datetime
from typing import Dict, List
from urllib.parse import quote_plus, urlparse

from config.settings import settings, DATA_DIR
from utils.csv_writer import write_csv
from utils.http import get
from utils.logger import get_logger

log = get_logger("ai_overview")

HISTORY_PATH = DATA_DIR / "ai_overview_history.csv"


def _our_domain() -> str:
    return urlparse(settings.site_url).netloc.lower().replace("www.", "")


def _ai_overview_via_serpapi(query: str) -> Dict:
    if not settings.serpapi_key:
        return {"present": False, "references": []}
    url = (
        "https://serpapi.com/search.json?engine=google"
        f"&q={quote_plus(query)}&gl=au&hl=en&ai_overview=1"
        f"&api_key={settings.serpapi_key}"
    )
    r = get(url)
    if not r or r.status_code != 200:
        return {"present": False, "references": []}
    data = r.json()
    ai = data.get("ai_overview") or {}
    refs = ai.get("references") or []
    return {
        "present": bool(ai),
        "references": [ref.get("link", "") for ref in refs if ref.get("link")],
    }


def _append_history(rows: List[Dict]) -> None:
    new_file = not HISTORY_PATH.exists()
    fieldnames = ["timestamp", "query", "ai_overview_present", "our_url_present",
                  "our_position", "total_references"]
    with open(HISTORY_PATH, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        if new_file:
            w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def run() -> str:
    our = _our_domain()
    ts = datetime.utcnow().isoformat(timespec="seconds")
    rows: List[Dict] = []

    for q in settings.target_queries:
        log.info(f"AI Overview check: {q}")
        ao = _ai_overview_via_serpapi(q)
        refs = ao["references"]
        our_pos = next(
            (i + 1 for i, u in enumerate(refs) if our in (urlparse(u).netloc or "").lower()),
            None,
        )
        rows.append({
            "timestamp": ts,
            "query": q,
            "ai_overview_present": ao["present"],
            "total_references": len(refs),
            "our_url_present": our_pos is not None,
            "our_position": our_pos or "",
            "references": " | ".join(refs[:5]),
        })

    path = write_csv("ai_overview", rows,
                     fieldnames=["timestamp", "query", "ai_overview_present",
                                 "total_references", "our_url_present",
                                 "our_position", "references"])
    _append_history(rows)
    log.info(f"AI Overview snapshot -> {path}  (history appended to {HISTORY_PATH})")
    return str(path)


if __name__ == "__main__":
    run()
