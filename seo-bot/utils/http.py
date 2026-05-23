"""Polite HTTP helpers used by crawlers and scrapers."""
from __future__ import annotations

import time
from typing import Optional

import requests
from requests import Response

UA = (
    "Mozilla/5.0 (compatible; SecurityBlogs-SEO-Bot/1.0; "
    "+https://securityblogs.com.au/bot)"
)
DEFAULT_TIMEOUT = 20


def get(url: str, *, headers: Optional[dict] = None, timeout: int = DEFAULT_TIMEOUT,
        retries: int = 2, backoff: float = 1.5) -> Optional[Response]:
    """GET with retry + UA. Returns None on permanent failure."""
    merged = {"User-Agent": UA, "Accept-Language": "en-AU,en;q=0.9"}
    if headers:
        merged.update(headers)
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, headers=merged, timeout=timeout, allow_redirects=True)
            if r.status_code < 500:
                return r
        except requests.RequestException:
            pass
        time.sleep(backoff ** attempt)
    return None
