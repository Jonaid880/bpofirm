"""
Multi-platform fan-out publisher.

Given one markdown brief, publishes to every platform with credentials
configured. WordPress is treated as the canonical home — every other
platform sets canonical_url back to the WordPress URL, so:
  * Google attributes ranking to securityblogs.com.au (no duplicate-content
    penalty),
  * referral traffic + brand entity signals come back to you,
  * the LLMs (which index Dev.to, Hashnode, LinkedIn) see your content
    multiple times across high-DR domains -> better AI citation odds.

Usage:
    python run.py fanout data/briefs/cctv-monitoring-sydney.md
"""
from __future__ import annotations

import importlib
from typing import Dict

from utils.logger import get_logger

log = get_logger("fanout")

PLATFORMS = {
    "wordpress":  "publishers.wordpress",
    "devto":      "publishers.devto",
    "hashnode":   "publishers.hashnode",
    "linkedin":   "publishers.linkedin_articles",
    "ghost":      "publishers.ghost",
    "blogger":    "publishers.blogger",
    "medium":     "publishers.medium_draft",
    "social":     "publishers.social_drafts",
}


def fanout(brief_path: str, *, status: str = "draft") -> Dict[str, str]:
    """Publish to every platform whose creds are configured. Returns {platform: status}."""
    results: Dict[str, str] = {}

    # 1. WordPress first — gets the canonical URL
    canonical = None
    try:
        wp = importlib.import_module("publishers.wordpress")
        res = wp.publish_markdown(brief_path, status=status)
        canonical = res.get("link")
        results["wordpress"] = f"OK -> {canonical}"
    except Exception as e:
        results["wordpress"] = f"SKIP: {e}"

    # 2. Then everyone else, each pointing canonical back at WP
    for name, mod_path in PLATFORMS.items():
        if name == "wordpress":
            continue
        try:
            mod = importlib.import_module(mod_path)
            if name == "medium":
                mod.export(brief_path); results[name] = "OK (draft file)"
            elif name == "social":
                mod.draft_from_brief(brief_path); results[name] = "OK (draft file)"
            elif name == "blogger":
                mod.publish(brief_path, draft=(status == "draft")); results[name] = "OK"
            else:
                mod.publish(brief_path, canonical_url=canonical); results[name] = "OK"
        except Exception as e:
            results[name] = f"SKIP: {e}"

    for k, v in results.items():
        log.info(f"  {k}: {v}")
    return results
