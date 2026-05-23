# SecurityBlogs.com.au — AI SEO Automation Bot

Modular AI-driven SEO, GEO (Generative Engine Optimisation) and AEO (Answer
Engine Optimisation) automation system for the Australian security industry
(CCTV monitoring, alarm response, AI surveillance, construction security,
retail security, monitoring centres).

Built to:

1. Increase citations in **ChatGPT, Gemini, Claude, Perplexity, Google AI
   Overviews**.
2. Build **topical authority** with pillar + cluster content.
3. Automate **off-page SEO** research (backlinks, outreach, digital PR).
4. Build **entity authority** (schema.org, knowledge-graph signals).
5. Improve **semantic SEO** coverage.
6. Generate **scalable authority signals** (citable stats, reports).

---

## Modules

| # | Module | What it does | Output |
|---|--------|--------------|--------|
| 1 | `ai_citation_tracker`     | Queries Perplexity / Google AI Overview / Bing Copilot for target prompts, extracts cited URLs and competitors. | `data/citations_*.csv` |
| 2 | `competitor_analyzer`     | Crawls competitor sitemaps, classifies topical coverage, finds content gaps vs. your site. | `data/competitor_gap_*.csv` |
| 3 | `topical_cluster_generator` | Uses Claude to expand seed keywords into pillar + cluster + AI-friendly article briefs. | `data/clusters_*.csv` + `data/briefs/*.md` |
| 4 | `entity_seo_builder`      | Generates Organization, LocalBusiness, Person (author) and Service schema. Builds entity relationship map. | `data/schema/*.json` |
| 5 | `guest_post_outreach`     | Finds niche-relevant sites via search operators, drafts personalised pitch emails. | `data/outreach_*.csv` + `data/emails/*.txt` |
| 6 | `digital_pr_generator`    | Generates statistics-page concepts, AI-citable research topics, PR angles. | `data/pr_ideas_*.csv` |
| 7 | `brand_mention_monitor`   | Tracks brand + competitor mentions across the web, flags unlinked mentions. | `data/mentions_*.csv` |
| 8 | `ai_overview_monitor`     | Monitors which of your URLs appear in Google AI Overviews / Perplexity for tracked queries. | `data/ai_overview_*.csv` |

## Publishers

| Target | Mode | File |
|--------|------|------|
| WordPress (your site) | **Auto-publish** via REST API | `publishers/wordpress.py` |
| Medium                | Draft export (Medium API deprecated) | `publishers/medium_draft.py` |
| LinkedIn / X / Reddit / Facebook | Draft queue for human approval (ToS-safe) | `publishers/social_drafts.py` |

---

## Quick start

```bash
cd seo-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # then fill in API keys
python run.py list         # see all available modules
python run.py citations    # run AI citation tracker
python run.py all          # run full daily workflow
```

See [SETUP.md](SETUP.md) for full installation, API key sourcing, scheduling
(cron / GitHub Actions) and publishing setup.

---

## Architecture

```
seo-bot/
├── config/           # settings + seed keywords + competitor list
├── utils/            # llm client, http, csv writer, logger
├── modules/          # the 8 SEO automation modules
├── publishers/       # WordPress + draft exporters
├── workflows/        # daily / weekly orchestration
├── templates/        # email + schema templates
├── data/             # CSV exports and generated artefacts (gitignored)
└── run.py            # CLI entry point
```

Every module:
- Reads config from `config/settings.py` (loaded from `.env`).
- Writes timestamped CSVs to `data/`.
- Is importable AND runnable standalone: `python -m modules.ai_citation_tracker`.
- Logs to `data/seo-bot.log`.

---

## Cost / API notes

The system is **designed to degrade gracefully**. Modules will run with
free / scraped sources if paid APIs are missing, and upgrade automatically
when keys are provided:

| Capability       | Free path           | Paid upgrade            |
|------------------|---------------------|-------------------------|
| SERP scraping    | DuckDuckGo HTML     | SerpAPI / DataForSEO    |
| LLM rewriting    | Claude API (cheap)  | n/a (already cheap)     |
| Backlink data    | Common Crawl index  | Ahrefs / Majestic API   |
| Mention tracking | Google news RSS     | Mention.com / Brand24   |
| Perplexity citations | Public web UI scrape | Perplexity API     |

Minimum viable: only `ANTHROPIC_API_KEY` is required.
