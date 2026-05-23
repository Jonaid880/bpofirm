"""
Module 6 — Digital PR Generator
===============================

Generates ideas that journalists, bloggers and AI engines will cite:
  * Statistics-page concepts (e.g. "Australian retail shrinkage stats 2026")
  * AI-citable research topic ideas (original survey / dataset angles)
  * PR angles tied to news cycles (legislation, ASIAL events)
  * Linkable asset concepts (calculators, ROI tools, checklists)

Output: data/pr_ideas_<ts>.csv
"""
from __future__ import annotations

import json
import re
from typing import Dict, List

from config.settings import settings
from utils.csv_writer import write_csv
from utils.llm_client import ask
from utils.logger import get_logger

log = get_logger("pr")

PROMPT = """You are a digital PR strategist for an Australian security services
brand ({site}) covering: CCTV monitoring, alarm response, AI surveillance,
construction security, retail security, monitoring centres.

Generate 20 high-value digital-PR ideas designed to:
- Earn .au news mentions and journalist links
- Be cited by ChatGPT / Perplexity / Google AI Overviews (need original data
  or a definitive answer)
- Build entity authority

Return STRICT JSON array. Each item:
{{
  "title": "...",
  "type": "statistics-page | original-research | calculator | report | survey | data-viz | trend-analysis",
  "ai_citability_score": 1-10,
  "outreach_targets": ["publication 1","publication 2","publication 3"],
  "data_source": "where the data comes from",
  "hook": "1 sentence why this gets picked up",
  "linkable_asset": "what physical page lives at securityblogs.com.au"
}}

JSON only — no preamble.
"""


def run() -> str:
    raw = ask(PROMPT.format(site=settings.site_url), max_tokens=4000)
    raw = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        ideas: List[Dict] = json.loads(raw)
    except json.JSONDecodeError:
        log.warning("Could not parse JSON; writing single 'raw' row.")
        ideas = [{"title": "RAW", "hook": raw[:500]}]

    path = write_csv("pr_ideas", ideas,
                     fieldnames=["title", "type", "ai_citability_score",
                                 "outreach_targets", "data_source", "hook", "linkable_asset"])
    log.info(f"PR ideas -> {path}")
    return str(path)


if __name__ == "__main__":
    run()
