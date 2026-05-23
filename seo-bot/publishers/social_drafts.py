"""
Social-post draft generator.

Why drafts (not auto-post)?
  LinkedIn, X/Twitter, Reddit, Facebook all forbid unattended automation for
  posting on behalf of users — accounts get suspended and posts get flagged
  as spam, hurting SEO/brand. Recommended pattern is:

    LLM -> draft file -> human approves -> Buffer/Hootsuite schedules

Buffer & Hootsuite both expose APIs designed for this and stay ToS-compliant.
Stubs for both are at the bottom of this file.

Usage:
    from publishers.social_drafts import draft_from_brief
    draft_from_brief("data/briefs/cctv-monitoring-sydney.md")
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import requests

from config.settings import settings, DATA_DIR
from utils.llm_client import ask
from utils.logger import get_logger

log = get_logger("social")

PLATFORMS = ["linkedin", "twitter", "reddit", "facebook"]


def draft_from_brief(brief_path: str) -> dict:
    md = Path(brief_path).read_text(encoding="utf-8")
    title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), Path(brief_path).stem)

    prompt = (
        f"Article: {title}\nSource brief:\n\n{md[:3000]}\n\n"
        "Write four social posts promoting this article. Return STRICT JSON:\n"
        "{\n"
        '  "linkedin": "1100-1300 char professional post, no hashtags spam, 3 line-break paragraphs",\n'
        '  "twitter": "260 chars max, 1-2 relevant hashtags",\n'
        '  "reddit": {"subreddit_suggestions":["r/sysadmin","r/AusBusiness"],"title":"...","body":"..."},\n'
        '  "facebook": "150-220 char conversational post"\n'
        "}\n"
        "Audience: Australian SMB & enterprise security buyers. JSON only."
    )
    raw = ask(prompt, fast=True, max_tokens=1500)
    raw = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"raw": raw}

    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]
    out_path = DATA_DIR / "social_drafts" / f"{slug}.md"
    lines = [f"# Social drafts: {title}", "", f"Source: `{brief_path}`", ""]
    for plat in PLATFORMS:
        lines += [f"## {plat.title()}", "```", json.dumps(data.get(plat, ""), indent=2), "```", ""]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    log.info(f"Social drafts -> {out_path}")
    return {"path": str(out_path), "data": data}


# -------------------- Buffer scheduling (ToS-safe) --------------------

def buffer_add_to_queue(platform_profile_id: str, text: str, link: str | None = None) -> dict:
    """Push a post to Buffer's queue. Requires BUFFER_ACCESS_TOKEN."""
    if not settings.buffer_token:
        raise RuntimeError("BUFFER_ACCESS_TOKEN missing")
    payload = {"text": text, "profile_ids[]": platform_profile_id}
    if link:
        payload["media[link]"] = link
    r = requests.post(
        f"https://api.bufferapp.com/1/updates/create.json?access_token={settings.buffer_token}",
        data=payload, timeout=20,
    )
    r.raise_for_status()
    return r.json()


# -------------------- Hootsuite (alternative) --------------------

def hootsuite_schedule(profile_ids: list[str], text: str, scheduled_send_time: str) -> dict:
    """Schedule a message via Hootsuite. scheduled_send_time must be ISO-8601 UTC."""
    if not settings.hootsuite_token:
        raise RuntimeError("HOOTSUITE_ACCESS_TOKEN missing")
    body = {"text": text, "socialProfileIds": profile_ids,
            "scheduledSendTime": scheduled_send_time}
    r = requests.post(
        "https://platform.hootsuite.com/v1/messages",
        headers={"Authorization": f"Bearer {settings.hootsuite_token}",
                 "Content-Type": "application/json"},
        json=body, timeout=20,
    )
    r.raise_for_status()
    return r.json()
