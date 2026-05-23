"""
Module 4 — Entity SEO Builder
=============================

Generates:
  * Organization + LocalBusiness schema (one JSON-LD per service area)
  * Service schema for each seed_keyword
  * Person schema scaffolding for authors
  * sameAs entity relationship map (Wikipedia / Wikidata / Crunchbase / LinkedIn)
  * A CSV of high-value citation opportunities (Wikipedia stubs, industry
    directories, ASIAL member listings, news outlets).

Output:
  data/schema/organization.json
  data/schema/localbusiness_<city>.json
  data/schema/service_<slug>.json
  data/entity_citation_opportunities_<ts>.csv
"""
from __future__ import annotations

import json
import re
from typing import Dict, List

import yaml

from config.settings import settings, DATA_DIR, ROOT
from utils.csv_writer import write_csv
from utils.llm_client import ask
from utils.logger import get_logger

log = get_logger("entities")


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:80]


def _load_yaml() -> Dict:
    with open(ROOT / "config" / "keywords.yaml", "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _organization_schema(org: Dict) -> Dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": org.get("legal_name", settings.site_name),
        "url": settings.site_url,
        "logo": f"{settings.site_url.rstrip('/')}/logo.png",
        "foundingDate": org.get("founding_date", ""),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": org.get("address", {}).get("street", ""),
            "addressLocality": org.get("address", {}).get("locality", ""),
            "addressRegion": org.get("address", {}).get("region", ""),
            "postalCode": org.get("address", {}).get("postcode", ""),
            "addressCountry": org.get("address", {}).get("country", "AU"),
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": org.get("contact", {}).get("phone", ""),
            "email": org.get("contact", {}).get("email", ""),
            "contactType": "customer service",
            "areaServed": "AU",
        },
        "sameAs": org.get("same_as", []),
    }


def _localbusiness_schema(city: str, org: Dict) -> Dict:
    return {
        "@context": "https://schema.org",
        "@type": "SecurityService",
        "name": f"{org.get('legal_name', settings.site_name)} — {city}",
        "url": f"{settings.site_url.rstrip('/')}/{_slug(city)}",
        "areaServed": {"@type": "City", "name": city, "addressCountry": "AU"},
        "priceRange": "$$",
        "telephone": org.get("contact", {}).get("phone", ""),
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city,
            "addressCountry": "AU",
        },
        "parentOrganization": {"@type": "Organization", "name": org.get("legal_name")},
    }


def _service_schema(kw: str) -> Dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": kw.title(),
        "provider": {"@type": "Organization", "name": settings.site_name, "url": settings.site_url},
        "areaServed": {"@type": "Country", "name": "Australia"},
        "audience": {"@type": "BusinessAudience", "name": "Commercial, retail, construction"},
    }


def _citation_opportunities(industry_auths: List[str]) -> List[Dict]:
    """Ask Claude to enumerate citation/listing opportunities for entity authority."""
    prompt = (
        "List 25 specific high-trust Australian websites where a Sydney-based "
        "security services company should be listed or cited to build entity "
        "authority for Google's knowledge graph and AI engines. Include the "
        "URL, the listing type (directory / news / association / wiki / "
        "regulator), and a 1-sentence pitch on why it matters.\n\n"
        f"Already aware of: {', '.join(industry_auths)}\n\n"
        "Output as a markdown table with columns: url | type | pitch"
    )
    text = ask(prompt, fast=True, max_tokens=2500)
    rows: List[Dict] = []
    for line in text.splitlines():
        if "|" not in line or line.strip().startswith("|-") or "url" in line.lower():
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) >= 3 and parts[0].startswith("http"):
            rows.append({"url": parts[0], "type": parts[1], "pitch": parts[2]})
    return rows


def run() -> Dict[str, str]:
    cfg = _load_yaml()
    entities = cfg.get("entities", {})
    org = entities.get("organization", {})

    schema_dir = DATA_DIR / "schema"

    # Organization
    org_schema = _organization_schema(org)
    (schema_dir / "organization.json").write_text(
        json.dumps(org_schema, indent=2), encoding="utf-8"
    )

    # LocalBusiness per city
    for city in settings.service_areas:
        path = schema_dir / f"localbusiness_{_slug(city)}.json"
        path.write_text(json.dumps(_localbusiness_schema(city, org), indent=2), encoding="utf-8")

    # Service per seed keyword
    for kw in settings.seed_keywords:
        path = schema_dir / f"service_{_slug(kw)}.json"
        path.write_text(json.dumps(_service_schema(kw), indent=2), encoding="utf-8")

    # Citation opportunities
    auths = entities.get("industry_authorities", [])
    opps = _citation_opportunities(auths)
    csv_path = write_csv("entity_citation_opportunities", opps,
                         fieldnames=["url", "type", "pitch"])

    log.info(f"Schema written to {schema_dir}; {len(opps)} citation opportunities -> {csv_path}")
    return {"schema_dir": str(schema_dir), "opportunities": str(csv_path)}


if __name__ == "__main__":
    run()
