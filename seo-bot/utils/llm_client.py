"""
Thin wrapper around Anthropic's Claude API.

Centralised so every module uses the same client, the same defaults, and the
same prompt-caching strategy. Swap models via .env (LLM_MODEL / LLM_FAST_MODEL).
"""
from __future__ import annotations

from typing import Optional

from anthropic import Anthropic

from config.settings import settings
from utils.logger import get_logger

log = get_logger("llm")

_client: Optional[Anthropic] = None


def client() -> Anthropic:
    global _client
    if _client is None:
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY missing. Copy .env.example -> .env and fill it in.")
        _client = Anthropic(api_key=settings.anthropic_api_key)
    return _client


def ask(prompt: str, *, system: str = "", fast: bool = False, max_tokens: int = 2048) -> str:
    """One-shot completion. Returns the text content."""
    model = settings.llm_fast_model if fast else settings.llm_model
    log.info(f"LLM call model={model} prompt_chars={len(prompt)}")
    msg = client().messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system or "You are an expert SEO and GEO/AEO strategist for the Australian security industry.",
        messages=[{"role": "user", "content": prompt}],
    )
    parts = [b.text for b in msg.content if getattr(b, "type", None) == "text"]
    return "\n".join(parts).strip()
