"""
LinkedIn Articles publisher (official Marketing Developer Platform API).

Requires LINKEDIN_ACCESS_TOKEN with `w_member_social` scope and the
member URN (LINKEDIN_AUTHOR_URN, e.g. 'urn:li:person:abc123').

Notes:
  * LinkedIn's Articles endpoint requires app review approval. Without it,
    we fall back to creating a UGC text post with the article link — still
    valuable for referral traffic and brand entity signals.
  * For the full Article publishing path, see
    https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/ugc-post-api
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import requests

from config.settings import settings
from utils.logger import get_logger

log = get_logger("linkedin")
TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
AUTHOR = os.getenv("LINKEDIN_AUTHOR_URN", "")


def _ugc_share(title: str, summary: str, link: str) -> dict:
    body = {
        "author": AUTHOR,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": f"{title}\n\n{summary}"},
                "shareMediaCategory": "ARTICLE",
                "media": [{
                    "status": "READY",
                    "description": {"text": summary[:200]},
                    "originalUrl": link,
                    "title": {"text": title[:200]},
                }],
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    r = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        json=body, timeout=30,
    )
    r.raise_for_status()
    return r.json()


def publish(brief_path: str, *, canonical_url: str | None = None) -> dict:
    if not (TOKEN and AUTHOR):
        raise RuntimeError("LINKEDIN_ACCESS_TOKEN or LINKEDIN_AUTHOR_URN missing")
    md = Path(brief_path).read_text(encoding="utf-8")
    title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")),
                 Path(brief_path).stem.title())
    # Use 'Direct answer' or 'Meta description' block as summary if present.
    m = re.search(r"## Meta description\s*\n(.+?)\n", md, re.DOTALL)
    summary = (m.group(1).strip() if m else md[:280]).replace("\n", " ")
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]
    link = canonical_url or f"{settings.site_url.rstrip('/')}/{slug}"
    res = _ugc_share(title, summary, link)
    log.info(f"LinkedIn: {title} -> id={res.get('id')}")
    return res
