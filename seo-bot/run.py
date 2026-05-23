#!/usr/bin/env python3
"""
CLI entry point.

Examples
--------
    python run.py list
    python run.py citations
    python run.py daily
    python run.py weekly
    python run.py all
    python run.py publish data/briefs/cctv-monitoring-australia.md --status draft
    python run.py social data/briefs/cctv-monitoring-australia.md
"""
from __future__ import annotations

import argparse
import sys
from typing import Callable, Dict

from utils.logger import get_logger

log = get_logger("run")


def _module_runners() -> Dict[str, Callable]:
    from modules import (
        ai_citation_tracker, competitor_analyzer, topical_cluster_generator,
        entity_seo_builder, guest_post_outreach, digital_pr_generator,
        brand_mention_monitor, ai_overview_monitor,
    )
    from workflows import daily, weekly
    return {
        "citations":   ai_citation_tracker.run,
        "competitors": competitor_analyzer.run,
        "clusters":    topical_cluster_generator.run,
        "entities":    entity_seo_builder.run,
        "outreach":    guest_post_outreach.run,
        "pr":          digital_pr_generator.run,
        "mentions":    brand_mention_monitor.run,
        "overviews":   ai_overview_monitor.run,
        "daily":       daily.run,
        "weekly":      weekly.run,
        "all":         lambda: (daily.run(), weekly.run()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(prog="seo-bot")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="List available commands")
    for cmd in ("citations", "competitors", "clusters", "entities", "outreach",
                "pr", "mentions", "overviews", "daily", "weekly", "all"):
        sub.add_parser(cmd, help=f"Run the '{cmd}' module/workflow")

    pub = sub.add_parser("publish", help="Publish a brief to WordPress")
    pub.add_argument("path")
    pub.add_argument("--status", default="draft", choices=["draft", "publish", "pending", "private"])

    soc = sub.add_parser("social", help="Generate social drafts from a brief")
    soc.add_argument("path")

    med = sub.add_parser("medium", help="Export brief as Medium import file")
    med.add_argument("path")

    args = parser.parse_args()

    if args.cmd == "list":
        for k in _module_runners():
            print(f"  - {k}")
        print("  - publish <brief_path> [--status draft|publish]")
        print("  - social  <brief_path>")
        print("  - medium  <brief_path>")
        return 0

    if args.cmd == "publish":
        from publishers.wordpress import publish_markdown
        result = publish_markdown(args.path, status=args.status)
        print(result.get("link") or result)
        return 0

    if args.cmd == "social":
        from publishers.social_drafts import draft_from_brief
        draft_from_brief(args.path)
        return 0

    if args.cmd == "medium":
        from publishers.medium_draft import export
        export(args.path)
        return 0

    runners = _module_runners()
    fn = runners.get(args.cmd)
    if not fn:
        parser.print_help()
        return 1
    fn()
    return 0


if __name__ == "__main__":
    sys.exit(main())
