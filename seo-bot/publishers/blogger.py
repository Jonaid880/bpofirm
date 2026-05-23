"""
Blogger publisher (Google API v3).

Requires:
  BLOGGER_OAUTH_TOKEN  short-lived OAuth access token (scope: blogger)
  BLOGGER_BLOG_ID      numeric blog id from your Blogger dashboard URL

Tip: use google-auth + refresh-token in production; for now this expects a
fresh access token in the env (run `gcloud auth application-default
print-access-token` or rotate via your OAuth client).
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import requests

from config.settings import settings
from utils.logger import get_logger

log = get_logger("blogger")
TOKEN = os.getenv("BLOGGER_OAUTH_TOKEN", "")
BLOG_ID = os.getenv("BLOGGER_BLOG_ID", "")


def _md_to_html(md: str) -> str:
    # Minimal markdown -> html; for richer output share publishers/wordpress.py
    from publishers.wordpress import _markdown_to_html as conv
    return conv(md)


def publish(brief_path: str, *, draft: bool = True) -> dict:
    if not (TOKEN and BLOG_ID):
        raise RuntimeError("BLOGGER_OAUTH_TOKEN or BLOGGER_BLOG_ID missing")
    md = Path(brief_path).read_text(encoding="utf-8")
    title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")),
                 Path(brief_path).stem.title())
    body = re.sub(r"^#\s+.*\n?", "", md, count=1)
    html = _md_to_html(body)

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/?isDraft={'true' if draft else 'false'}"
    payload = {"kind": "blogger#post", "title": title, "content": html,
               "labels": ["security", "australia", "cctv", "alarm-monitoring"]}
    r = requests.post(url, headers={"Authorization": f"Bearer {TOKEN}",
                                    "Content-Type": "application/json"},
                      json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    log.info(f"Blogger: {title} -> {data.get('url')}")
    return data
