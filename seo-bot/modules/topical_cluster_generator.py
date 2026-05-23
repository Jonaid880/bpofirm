"""
Module 3 — Topical Cluster Generator
====================================

For each seed keyword:
  * Ask Claude for: pillar topic, 6-10 supporting cluster topics, semantic
    entities to mention, search intent, and a 5-bullet article outline that is
    AEO-friendly (direct-answer first paragraph + FAQ block).
  * Persist a CSV summary + one markdown brief per article.

Output:
  data/clusters_<ts>.csv
  data/briefs/<slug>.md
"""
from __future__ import annotations

import json
import re
from typing import Dict, List

from config.settings import settings, DATA_DIR
from utils.csv_writer import write_csv
from utils.llm_client import ask
from utils.logger import get_logger

log = get_logger("clusters")

PROMPT = """You are a senior SEO strategist for the Australian security industry.

For the seed keyword: "{kw}"

Return STRICT JSON with this shape:
{{
  "pillar": "...",
  "search_intent": "informational | commercial | transactional | navigational",
  "supporting_clusters": ["cluster topic 1", "cluster topic 2", ...],
  "semantic_entities": ["entity 1", "entity 2", ...],
  "people_also_ask": ["question 1?", "question 2?", ...],
  "article_brief": {{
    "title": "AEO-optimised H1",
    "meta_description": "150-160 chars",
    "direct_answer": "40-60 word direct answer for AI Overviews",
    "outline": ["H2 section 1", "H2 section 2", ...],
    "faq": [{{"q":"...","a":"..."}}, ...],
    "schema_types": ["Article","FAQPage", "..."]
  }}
}}

Audience: Australian businesses (commercial, retail, construction). Localise
where useful (Sydney, Melbourne, etc). Reference ASIAL / AS/NZS 2201 when
relevant. Output JSON only — no preamble.
"""


def _slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s[:80]


def _generate(kw: str) -> Dict:
    raw = ask(PROMPT.format(kw=kw), max_tokens=2500)
    # Defensive JSON extraction — Claude occasionally wraps in ```json
    raw = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        log.warning(f"JSON parse failed for {kw}; storing raw")
        return {"pillar": kw, "raw": raw}


def _write_brief(kw: str, data: Dict) -> str:
    slug = _slug(kw)
    path = DATA_DIR / "briefs" / f"{slug}.md"
    brief = data.get("article_brief", {})
    md = [
        f"# {brief.get('title', kw)}",
        "",
        f"**Seed keyword:** {kw}",
        f"**Search intent:** {data.get('search_intent','')}",
        f"**Pillar:** {data.get('pillar','')}",
        "",
        "## Meta description",
        brief.get("meta_description", ""),
        "",
        "## Direct answer (for AI Overviews)",
        brief.get("direct_answer", ""),
        "",
        "## Outline",
    ]
    for h2 in brief.get("outline", []):
        md.append(f"- {h2}")
    md += ["", "## FAQ"]
    for f in brief.get("faq", []):
        md.append(f"**Q: {f.get('q','')}**  \nA: {f.get('a','')}\n")
    md += ["", "## Supporting cluster topics"]
    for c in data.get("supporting_clusters", []):
        md.append(f"- {c}")
    md += ["", "## Semantic entities to mention"]
    for e in data.get("semantic_entities", []):
        md.append(f"- {e}")
    md += ["", "## People Also Ask"]
    for q in data.get("people_also_ask", []):
        md.append(f"- {q}")
    md += ["", "## Schema types", ", ".join(brief.get("schema_types", []))]
    path.write_text("\n".join(md), encoding="utf-8")
    return str(path)


def run() -> str:
    rows: List[Dict] = []
    for kw in settings.seed_keywords:
        log.info(f"Cluster: {kw}")
        data = _generate(kw)
        brief_path = _write_brief(kw, data)
        rows.append({
            "seed_keyword": kw,
            "pillar": data.get("pillar", ""),
            "intent": data.get("search_intent", ""),
            "n_clusters": len(data.get("supporting_clusters", [])),
            "n_entities": len(data.get("semantic_entities", [])),
            "n_faq": len(data.get("article_brief", {}).get("faq", [])),
            "brief_path": brief_path,
        })
    path = write_csv("clusters", rows,
                     fieldnames=["seed_keyword", "pillar", "intent",
                                 "n_clusters", "n_entities", "n_faq", "brief_path"])
    log.info(f"Generated {len(rows)} cluster briefs -> {path}")
    return str(path)


if __name__ == "__main__":
    run()
