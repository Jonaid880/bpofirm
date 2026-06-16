"""
Live state check.

Prints a snapshot of:
  * Which secrets / config are configured
  * Which CSV / brief / schema outputs exist and how fresh they are
  * Which modules have been run + when
  * What's blocking the bot from running cleanly

Run with:  python run.py status
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

from config.settings import settings, DATA_DIR


# (env-var-name, label, required?)
ENV_KEYS: List[Tuple[str, str, bool]] = [
    ("ANTHROPIC_API_KEY",       "Anthropic (LLM)",              True),
    ("WORDPRESS_URL",           "WordPress URL",                False),
    ("WORDPRESS_USER",          "WordPress user",               False),
    ("WORDPRESS_APP_PASSWORD",  "WordPress app password",       False),
    ("SERPAPI_KEY",             "SerpAPI",                      False),
    ("PERPLEXITY_API_KEY",      "Perplexity",                   False),
    ("AHREFS_API_KEY",          "Ahrefs",                       False),
    ("DEVTO_API_KEY",           "Dev.to",                       False),
    ("HASHNODE_API_KEY",        "Hashnode",                     False),
    ("LINKEDIN_ACCESS_TOKEN",   "LinkedIn",                     False),
    ("GHOST_ADMIN_API_KEY",     "Ghost",                        False),
    ("BLOGGER_OAUTH_TOKEN",     "Blogger",                      False),
    ("GOOGLE_PLACES_API_KEY",   "Google Places (reviews)",      False),
]

MODULE_OUTPUTS = {
    "ai_citation_tracker":     "citations_",
    "competitor_analyzer":     "competitor_gap_",
    "topical_cluster_generator": "clusters_",
    "entity_seo_builder":      "entity_citation_opportunities_",
    "guest_post_outreach":     "outreach_",
    "digital_pr_generator":    "pr_ideas_",
    "brand_mention_monitor":   "mentions_",
    "ai_overview_monitor":     "ai_overview_",
    "citation_builder":        "citation_submission_queue_",
    "broken_link_builder":     "broken_links_",
    "haro_responder":          "haro_responses_",
    "review_monitor":          "reviews_",
}


def _latest(prefix: str) -> Path | None:
    matches = sorted(DATA_DIR.glob(f"{prefix}*.csv"))
    return matches[-1] if matches else None


def _age(path: Path) -> str:
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    delta = datetime.now(timezone.utc) - mtime
    if delta.days >= 1:
        return f"{delta.days}d ago"
    h = delta.seconds // 3600
    if h >= 1:
        return f"{h}h ago"
    return f"{max(1, delta.seconds // 60)}m ago"


def _row(symbol: str, label: str, detail: str = "") -> str:
    return f"  {symbol} {label:<32}{detail}"


def run() -> str:
    out: List[str] = []
    out.append("=" * 70)
    out.append(f"  SEO Bot status — {settings.site_url}")
    out.append("=" * 70)

    # ----- Config -----
    out.append("\n[ Config ]")
    out.append(_row("•", "Seed keywords",      str(len(settings.seed_keywords))))
    out.append(_row("•", "Competitors",         str(len(settings.competitors))))
    out.append(_row("•", "Target queries",      str(len(settings.target_queries))))
    out.append(_row("•", "Service areas",       str(len(settings.service_areas))))

    # ----- Secrets / API keys -----
    out.append("\n[ Credentials ]")
    missing_required = []
    for env_var, label, required in ENV_KEYS:
        present = bool(os.getenv(env_var))
        if required and not present:
            missing_required.append(env_var)
        sym = "✓" if present else ("✗" if required else "·")
        tag = " (required)" if required else ""
        out.append(_row(sym, label, ("set" if present else "missing") + tag))

    # ----- Module run freshness -----
    out.append("\n[ Module runs ]")
    for mod, prefix in MODULE_OUTPUTS.items():
        latest = _latest(prefix)
        if latest:
            out.append(_row("✓", mod, f"last: {_age(latest)}  ({latest.name})"))
        else:
            out.append(_row("·", mod, "never run"))

    # ----- Output counts -----
    briefs = list((DATA_DIR / "briefs").glob("*.md"))
    schema = list((DATA_DIR / "schema").glob("*.json"))
    emails = list((DATA_DIR / "emails").glob("*.txt"))
    socials = list((DATA_DIR / "social_drafts").glob("*.md"))

    out.append("\n[ Generated assets ]")
    out.append(_row("•", "Article briefs (data/briefs/)",     str(len(briefs))))
    out.append(_row("•", "Schema files (data/schema/)",       str(len(schema))))
    out.append(_row("•", "Email drafts (data/emails/)",       str(len(emails))))
    out.append(_row("•", "Social drafts (data/social_drafts/)", str(len(socials))))

    # ----- Verdict -----
    out.append("\n[ Verdict ]")
    if missing_required:
        out.append(f"  ⚠ Cannot run — missing: {', '.join(missing_required)}")
        out.append("    Add to .env (local) or GitHub Secrets (Actions).")
    else:
        out.append("  ✓ Bot is configured to run.")
        if not briefs:
            out.append("    Suggested next: python run.py weekly")
        elif not list(DATA_DIR.glob("citations_*.csv")):
            out.append("    Suggested next: python run.py daily")
        else:
            out.append("    Suggested next: python run.py fanout data/briefs/<file>.md")

    out.append("=" * 70)
    text = "\n".join(out)
    print(text)
    return text


if __name__ == "__main__":
    run()
