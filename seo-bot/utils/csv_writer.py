"""CSV export helper with timestamped filenames."""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from config import settings  # noqa: F401  (ensures DATA_DIR is created)
from config.settings import DATA_DIR


def write_csv(prefix: str, rows: Sequence[Mapping[str, object]], fieldnames: Iterable[str] | None = None) -> Path:
    """
    Write rows to data/<prefix>_YYYYMMDD-HHMMSS.csv and return the path.

    `fieldnames` is inferred from the first row if not provided.
    """
    if not rows:
        # Still emit an empty file so downstream jobs see "ran but no data".
        fieldnames = list(fieldnames or [])
    else:
        fieldnames = list(fieldnames or rows[0].keys())

    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    path = DATA_DIR / f"{prefix}_{ts}.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path
