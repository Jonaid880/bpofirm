"""
Ghost publisher (Admin API).

Requires:
  GHOST_ADMIN_URL     e.g. https://blog.example.com
  GHOST_ADMIN_API_KEY format 'id:secret' from Ghost Admin -> Integrations
"""
from __future__ import annotations

import os
import re
import time
from pathlib import Path

import requests
# `jwt` (PyJWT) is imported lazily inside _token() so this publisher can be
# loaded even when PyJWT/cryptography aren't installed — users who don't use
# Ghost shouldn't need to install crypto deps.

from config.settings import settings
from utils.logger import get_logger

log = get_logger("ghost")
GHOST_URL = os.getenv("GHOST_ADMIN_URL", "")
GHOST_KEY = os.getenv("GHOST_ADMIN_API_KEY", "")


def _token() -> str:
    import jwt   # PyJWT
    if ":" not in GHOST_KEY:
        raise RuntimeError("GHOST_ADMIN_API_KEY must be in 'id:secret' format")
    kid, secret = GHOST_KEY.split(":", 1)
    iat = int(time.time())
    payload = {"iat": iat, "exp": iat + 5 * 60, "aud": "/admin/"}
    return jwt.encode(payload, bytes.fromhex(secret), algorithm="HS256",
                      headers={"kid": kid, "alg": "HS256", "typ": "JWT"})


def publish(brief_path: str, *, status: str = "draft",
            canonical_url: str | None = None) -> dict:
    if not (GHOST_URL and GHOST_KEY):
        raise RuntimeError("GHOST_ADMIN_URL or GHOST_ADMIN_API_KEY missing")
    md = Path(brief_path).read_text(encoding="utf-8")
    title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")),
                 Path(brief_path).stem.title())
    body = re.sub(r"^#\s+.*\n?", "", md, count=1)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]

    url = GHOST_URL.rstrip("/") + "/ghost/api/admin/posts/?source=html"
    payload = {"posts": [{
        "title": title,
        "html": body,
        "status": status,            # 'draft' | 'published' | 'scheduled'
        "canonical_url": canonical_url or f"{settings.site_url.rstrip('/')}/{slug}",
        "tags": [{"name": "security"}, {"name": "australia"}],
    }]}
    r = requests.post(url, headers={"Authorization": f"Ghost {_token()}",
                                    "Content-Type": "application/json"},
                      json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    log.info(f"Ghost: {title} -> status={status}")
    return data
