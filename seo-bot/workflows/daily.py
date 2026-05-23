"""
Daily workflow — cheap, high-frequency monitoring.

Runs:
  * AI Citation Tracker
  * Brand Mention Monitor
  * AI Overview Monitor
"""
from modules import ai_citation_tracker, brand_mention_monitor, ai_overview_monitor
from utils.logger import get_logger

log = get_logger("daily")


def run() -> None:
    log.info("=== DAILY WORKFLOW START ===")
    for mod in (ai_citation_tracker, brand_mention_monitor, ai_overview_monitor):
        try:
            mod.run()
        except Exception as e:
            log.exception(f"Module {mod.__name__} failed: {e}")
    log.info("=== DAILY WORKFLOW END ===")


if __name__ == "__main__":
    run()
