"""
WordPress REST API publisher.

Auth: Application Passwords (WP Admin -> Users -> Profile -> Application
Passwords). Posts default to `draft` so a human approves before publish.

Usage:
    from publishers.wordpress import publish_markdown
    publish_markdown(path="data/briefs/cctv-monitoring-sydney.md", status="draft")
"""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path
from typing import Optional

import requests

from config.settings import settings
from utils.logger import get_logger

log = get_logger("wp")


def _auth_header() -> dict:
    if not (settings.wp_user and settings.wp_app_password):
        raise RuntimeError("WORDPRESS_USER / WORDPRESS_APP_PASSWORD missing in .env")
    token = base64.b64encode(
        f"{settings.wp_user}:{settings.wp_app_password}".encode()
    ).decode()
    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}


def _markdown_to_html(md: str) -> str:
    """Very small md->html converter for headings, lists, paragraphs, bold."""
    html_lines = []
    in_list = False
    for line in md.splitlines():
        s = line.rstrip()
        if not s:
            if in_list:
                html_lines.append("</ul>"); in_list = False
            html_lines.append("")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            if in_list:
                html_lines.append("</ul>"); in_list = False
            lvl = len(m.group(1))
            html_lines.append(f"<h{lvl}>{m.group(2)}</h{lvl}>")
            continue
        if s.startswith("- "):
            if not in_list:
                html_lines.append("<ul>"); in_list = True
            html_lines.append(f"<li>{s[2:]}</li>")
            continue
        if in_list:
            html_lines.append("</ul>"); in_list = False
        # bold
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        html_lines.append(f"<p>{s}</p>")
    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)


def _extract_title(md: str, fallback: str) -> str:
    for line in md.splitlines():
        m = re.match(r"^#\s+(.*)$", line.strip())
        if m:
            return m.group(1).strip()
    return fallback


def publish_markdown(path: str, *, status: str = "draft", categories: Optional[list[int]] = None) -> dict:
    p = Path(path)
    md = p.read_text(encoding="utf-8")
    title = _extract_title(md, fallback=p.stem.replace("-", " ").title())
    html = _markdown_to_html(md)

    if not settings.wp_url:
        raise RuntimeError("WORDPRESS_URL missing in .env")

    endpoint = settings.wp_url.rstrip("/") + "/wp-json/wp/v2/posts"
    payload = {"title": title, "content": html, "status": status}
    if categories:
        payload["categories"] = categories

    r = requests.post(endpoint, headers=_auth_header(), data=json.dumps(payload), timeout=30)
    if r.status_code >= 400:
        log.error(f"WP error {r.status_code}: {r.text[:500]}")
        r.raise_for_status()
    data = r.json()
    log.info(f"Posted '{title}' as {status} -> {data.get('link')}")
    return data
