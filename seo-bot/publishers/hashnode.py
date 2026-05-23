"""
Hashnode publisher (GraphQL API).

Requires:
  HASHNODE_API_KEY  (https://hashnode.com/settings/developer)
  HASHNODE_PUBLICATION_ID  (from your blog's dashboard URL)

Sets canonicalUrl back to your live securityblogs.com.au article.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import requests

from config.settings import settings
from utils.logger import get_logger

log = get_logger("hashnode")
API_KEY = os.getenv("HASHNODE_API_KEY", "")
PUB_ID = os.getenv("HASHNODE_PUBLICATION_ID", "")

GQL = """
mutation PublishPost($input: PublishPostInput!) {
  publishPost(input: $input) { post { id slug url } }
}
"""


def publish(brief_path: str, *, canonical_url: str | None = None) -> dict:
    if not (API_KEY and PUB_ID):
        raise RuntimeError("HASHNODE_API_KEY or HASHNODE_PUBLICATION_ID missing")
    md = Path(brief_path).read_text(encoding="utf-8")
    title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")),
                 Path(brief_path).stem.title())
    body = re.sub(r"^#\s+.*\n?", "", md, count=1)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]

    variables = {
        "input": {
            "title": title,
            "publicationId": PUB_ID,
            "contentMarkdown": body,
            "slug": slug,
            "originalArticleURL": canonical_url or
                                  f"{settings.site_url.rstrip('/')}/{slug}",
            "tags": [{"slug": "security", "name": "Security"},
                     {"slug": "australia", "name": "Australia"}],
        }
    }
    r = requests.post(
        "https://gql.hashnode.com/",
        headers={"Authorization": API_KEY, "Content-Type": "application/json"},
        json={"query": GQL, "variables": variables}, timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    url = (((data.get("data") or {}).get("publishPost") or {}).get("post") or {}).get("url")
    log.info(f"Hashnode: {title} -> {url}")
    return data
