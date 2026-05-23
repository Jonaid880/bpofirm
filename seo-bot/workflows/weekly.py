"""
Weekly workflow — expensive, low-frequency strategic work.

Runs:
  * Competitor Analyzer
  * Topical Cluster Generator
  * Entity SEO Builder
  * Guest Post Outreach
  * Digital PR Generator
"""
from modules import (
    competitor_analyzer,
    topical_cluster_generator,
    entity_seo_builder,
    guest_post_outreach,
    digital_pr_generator,
    citation_builder,
    broken_link_builder,
)
from utils.logger import get_logger

log = get_logger("weekly")


def run() -> None:
    log.info("=== WEEKLY WORKFLOW START ===")
    for mod in (competitor_analyzer, topical_cluster_generator, entity_seo_builder,
                guest_post_outreach, digital_pr_generator,
                citation_builder, broken_link_builder):
        try:
            mod.run()
        except Exception as e:
            log.exception(f"Module {mod.__name__} failed: {e}")
    log.info("=== WEEKLY WORKFLOW END ===")


if __name__ == "__main__":
    run()
