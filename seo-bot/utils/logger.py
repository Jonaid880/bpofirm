"""Lightweight project-wide logger."""
import logging
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "seo-bot.log"
LOG_PATH.parent.mkdir(exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger that writes to both stdout and data/seo-bot.log."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    fh = logging.FileHandler(LOG_PATH)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger
