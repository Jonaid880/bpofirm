"""
Airtable sync — push bot outputs into the StateGuard SEO Command Centre base.

Requires:
  AIRTABLE_TOKEN     Personal Access Token from https://airtable.com/create/tokens
                     (scopes: data.records:read + data.records:write + schema.bases:read)
  AIRTABLE_BASE_ID   The 'appXXXXXXXXXXXXX' string from your base URL

Maps which CSV/dataset goes into which Airtable tab via TABLE_MAP. Edit there
if your tab names differ.

Usage (CLI):
    python run.py airtable-sync                # sync all
    python -c "from publishers.airtable_sync import sync_table; sync_table('AI Visibility', 'seo-bot/airtable/ai_visibility.csv')"
"""
from __future__ import annotations

import csv
import os
import time
from pathlib import Path
from typing import Dict, List

import requests

from config.settings import settings, ROOT
from utils.logger import get_logger

log = get_logger("airtable")

TOKEN = os.getenv("AIRTABLE_TOKEN", "")
BASE = os.getenv("AIRTABLE_BASE_ID", "")
API = "https://api.airtable.com/v0"

# Which CSV feeds which Airtable tab.
# We address tables by TABLE ID, not name. Names can mismatch invisibly
# (emoji prefix, trailing whitespace, rename) and Airtable returns 404 for
# any miss. Table IDs are immutable — find them in the URL of the table
# view: https://airtable.com/{baseId}/{tableId}/{viewId}.
TABLE_MAP: Dict[str, Path] = {
    "tblj8ImoiXXOjc2Xm":  ROOT / "airtable" / "ai_visibility.csv",  # AI Visibility
    # Add more table IDs to re-enable other tabs, e.g.:
    # "tblXXXXXXXXXXXXXX": ROOT / "airtable" / "content_calendar.csv",
}

# Fields that should be coerced from CSV string to checkbox / number / date.
CHECKBOX_FIELDS = {"ChatGPT Citation", "Gemini Citation",
                   "Perplexity Citation", "StateGuard Citation"}
NUMBER_FIELDS   = {"Word Count"}


def _headers() -> dict:
    if not (TOKEN and BASE):
        raise RuntimeError("AIRTABLE_TOKEN or AIRTABLE_BASE_ID missing. See seo-bot/airtable/README.md.")
    return {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


def _coerce(field: str, value: str):
    if value == "":
        return None
    if field in CHECKBOX_FIELDS:
        return value.strip().lower() in {"true", "yes", "1", "checked"}
    if field in NUMBER_FIELDS:
        try:
            return int(value)
        except ValueError:
            return None
    return value


def _existing_records(table: str, key_field: str) -> Dict[str, str]:
    """Return {key_value: record_id} for the table — used for upsert."""
    out: Dict[str, str] = {}
    url = f"{API}/{BASE}/{requests.utils.quote(table)}"
    offset = None
    while True:
        params = {"pageSize": 100}
        if offset:
            params["offset"] = offset
        r = requests.get(url, headers=_headers(), params=params, timeout=20)
        if r.status_code == 404:
            log.warning(f"Table '{table}' not found in base — skipping.")
            return {}
        r.raise_for_status()
        data = r.json()
        for rec in data.get("records", []):
            k = rec.get("fields", {}).get(key_field)
            if k:
                out[str(k)] = rec["id"]
        offset = data.get("offset")
        if not offset:
            break
    return out


def sync_table(table: str, csv_path: Path) -> Dict[str, int]:
    """Upsert all rows from csv_path into the named Airtable table.

    Upsert key is the first column of the CSV (Question / Title / Platform/Site /
    Keyword) — change `KEY_BY_TABLE` below if your schema uses something else.
    """
    KEY_BY_TABLE = {
        "tblj8ImoiXXOjc2Xm": "Question",       # AI Visibility
        # Add table-id -> upsert key entries here if re-enabling other tabs.
    }
    key_field = KEY_BY_TABLE.get(table, "")
    if not key_field:
        raise ValueError(f"No upsert key configured for table {table}")

    if not csv_path.exists():
        log.warning(f"CSV missing: {csv_path}")
        return {"created": 0, "updated": 0, "skipped": 0}

    existing = _existing_records(table, key_field)
    with open(csv_path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    created = updated = skipped = 0
    url = f"{API}/{BASE}/{requests.utils.quote(table)}"

    # Airtable allows up to 10 records per PATCH/POST.
    for i in range(0, len(rows), 10):
        batch = rows[i:i+10]
        to_create, to_update = [], []
        for row in batch:
            fields = {k: _coerce(k, v) for k, v in row.items() if v != ""}
            fields = {k: v for k, v in fields.items() if v is not None}
            key_val = str(row.get(key_field, "")).strip()
            if not key_val:
                skipped += 1
                continue
            rec_id = existing.get(key_val)
            if rec_id:
                to_update.append({"id": rec_id, "fields": fields})
            else:
                to_create.append({"fields": fields})

        if to_create:
            r = requests.post(url, headers=_headers(),
                              json={"records": to_create, "typecast": True}, timeout=30)
            if r.status_code >= 400:
                log.error(f"Create failed: {r.status_code} {r.text[:200]}")
            else:
                created += len(to_create)
        if to_update:
            r = requests.patch(url, headers=_headers(),
                               json={"records": to_update, "typecast": True}, timeout=30)
            if r.status_code >= 400:
                log.error(f"Update failed: {r.status_code} {r.text[:200]}")
            else:
                updated += len(to_update)
        time.sleep(0.25)   # respect Airtable 5 req/sec/base limit

    log.info(f"{table}: created={created} updated={updated} skipped={skipped}")
    return {"created": created, "updated": updated, "skipped": skipped}


def sync_all() -> Dict[str, Dict[str, int]]:
    results: Dict[str, Dict[str, int]] = {}
    for table, csv_path in TABLE_MAP.items():
        try:
            results[table] = sync_table(table, csv_path)
        except Exception as e:
            log.exception(f"Sync of {table} failed: {e}")
            results[table] = {"error": str(e)}
    return results


if __name__ == "__main__":
    sync_all()
