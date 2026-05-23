"""
Dev.to publisher (official API).

Requires DEVTO_API_KEY in .env (https://dev.to/settings/extensions -> API Keys).

Posts as a draft by default; pass status='publish' to publish immediately.
We always set canonical_url back to your live article on securityblogs.com.au
so Dev.to amplifies your reach WITHOUT competing in Google.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import requests

from config.settings import settings
from utils.logger import get_logger

log = get_logger("devto")
DEVTO_API_KEY = os.getenv("DEVTO_API_KEY", "")


def _front_matter(md: str) -> tuple[str, str]:
    """Strip leading H1 to use as title; return (title, body_md)."""
    for line in md.splitlines():
        m = re.match(r"^#\s+(.*)$", line.strip())
        if m:
            title = m.group(1).strip()
            body = re.sub(r"^#\s+.*\n?", "", md, count=1)
            return title, body
    return Path("untitled").stem.title(), md


def publish(brief_path: str, *, status: str = "draft",
            canonical_url: str | None = None, tags: list[str] | None = None) -> dict:
    if not DEVTO_API_KEY:
        raise RuntimeError("DEVTO_API_KEY missing in .env")
    md = Path(brief_path).read_text(encoding="utf-8")
    title, body = _front_matter(md)
    payload = {
        "article": {
            "title": title,
            "body_markdown": body,
            "published": status == "publish",
            "canonical_url": canonical_url or settings.site_url.rstrip("/") + "/" +
                             re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-"),
            "tags": tags or ["security", "cybersecurity", "australia", "cctv"],
        }
    }
    r = requests.post(
        "https://dev.to/api/articles",
        headers={"api-key": DEVTO_API_KEY, "Content-Type": "application/json"},
        json=payload, timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    log.info(f"Dev.to: {title} -> {data.get('url')}")
    return data
