"""
Medium drafts.

Medium's public posting API was deprecated in 2023. Until they reopen it, this
just writes a paste-ready markdown file with the correct Medium-flavoured
heading style; you import via Medium's 'Import a story' tool.
"""
from __future__ import annotations

import re
from pathlib import Path

from config.settings import DATA_DIR
from utils.logger import get_logger

log = get_logger("medium")


def export(brief_path: str) -> str:
    md = Path(brief_path).read_text(encoding="utf-8")
    slug = re.sub(r"[^a-z0-9]+", "-", Path(brief_path).stem.lower()).strip("-")[:60]
    out = DATA_DIR / "medium_drafts" / f"{slug}.md"
    out.write_text(md, encoding="utf-8")
    log.info(f"Medium draft -> {out} (import via medium.com -> ... -> Import a story)")
    return str(out)
