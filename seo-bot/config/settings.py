"""
Centralised settings loaded from environment variables and keywords.yaml.

Single source of truth — every module imports `settings` from here so that
adding a new env var or seed keyword is a one-file change.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "briefs").mkdir(exist_ok=True)
(DATA_DIR / "schema").mkdir(exist_ok=True)
(DATA_DIR / "emails").mkdir(exist_ok=True)
(DATA_DIR / "social_drafts").mkdir(exist_ok=True)
(DATA_DIR / "medium_drafts").mkdir(exist_ok=True)


def _env(key: str, default: str = "") -> str:
    return os.getenv(key, default) or default


def _env_list(key: str, default: str = "") -> List[str]:
    raw = _env(key, default)
    return [x.strip() for x in raw.split(",") if x.strip()]


@dataclass
class Settings:
    # LLM
    anthropic_api_key: str = field(default_factory=lambda: _env("ANTHROPIC_API_KEY"))
    llm_model: str = field(default_factory=lambda: _env("LLM_MODEL", "claude-opus-4-7"))
    llm_fast_model: str = field(default_factory=lambda: _env("LLM_FAST_MODEL", "claude-haiku-4-5-20251001"))

    # Site
    site_url: str = field(default_factory=lambda: _env("SITE_URL", "https://securityblogs.com.au"))
    site_name: str = field(default_factory=lambda: _env("SITE_NAME", "SecurityBlogs"))
    brand_names: List[str] = field(default_factory=lambda: _env_list("BRAND_NAMES", "SecurityBlogs"))
    country: str = field(default_factory=lambda: _env("COUNTRY", "AU"))

    # SERP / data providers
    serpapi_key: str = field(default_factory=lambda: _env("SERPAPI_KEY"))
    dataforseo_login: str = field(default_factory=lambda: _env("DATAFORSEO_LOGIN"))
    dataforseo_password: str = field(default_factory=lambda: _env("DATAFORSEO_PASSWORD"))
    perplexity_api_key: str = field(default_factory=lambda: _env("PERPLEXITY_API_KEY"))
    ahrefs_api_key: str = field(default_factory=lambda: _env("AHREFS_API_KEY"))

    # WordPress
    wp_url: str = field(default_factory=lambda: _env("WORDPRESS_URL"))
    wp_user: str = field(default_factory=lambda: _env("WORDPRESS_USER"))
    wp_app_password: str = field(default_factory=lambda: _env("WORDPRESS_APP_PASSWORD"))

    # Scheduling
    buffer_token: str = field(default_factory=lambda: _env("BUFFER_ACCESS_TOKEN"))
    hootsuite_token: str = field(default_factory=lambda: _env("HOOTSUITE_ACCESS_TOKEN"))

    # Seeds loaded from YAML
    seed_keywords: List[str] = field(default_factory=list)
    competitors: List[str] = field(default_factory=list)
    target_queries: List[str] = field(default_factory=list)
    service_areas: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        kw_path = ROOT / "config" / "keywords.yaml"
        if kw_path.exists():
            with open(kw_path, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            self.seed_keywords = data.get("seed_keywords", [])
            self.competitors = data.get("competitors", [])
            self.target_queries = data.get("target_queries", [])
            self.service_areas = data.get("service_areas", [])


settings = Settings()
