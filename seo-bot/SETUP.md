# Setup Guide

## 1. Install

```bash
cd seo-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium       # only needed for ai_citation_tracker scraping path
```

## 2. Configure

```bash
cp .env.example .env
```

Open `.env` and fill in keys. **Minimum required**: `ANTHROPIC_API_KEY`.

### Where to get each key

| Variable | Where | Required? |
|----------|-------|-----------|
| `ANTHROPIC_API_KEY` | https://console.anthropic.com | **Yes** |
| `SERPAPI_KEY` | https://serpapi.com (free 100/mo) | Optional |
| `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` | https://dataforseo.com | Optional |
| `PERPLEXITY_API_KEY` | https://docs.perplexity.ai | Optional |
| `AHREFS_API_KEY` | https://ahrefs.com/api | Optional |
| `WORDPRESS_URL` | e.g. `https://securityblogs.com.au` | For publishing |
| `WORDPRESS_USER` | WP username | For publishing |
| `WORDPRESS_APP_PASSWORD` | WP → Users → Profile → Application Passwords | For publishing |

## 3. Set your targets

Edit `config/keywords.yaml`:

```yaml
seed_keywords:
  - cctv monitoring australia
  - alarm response sydney
  ...
competitors:
  - https://example-competitor.com.au
  ...
target_queries:        # what you want to rank for in AI engines
  - "best cctv monitoring service in australia"
  ...
```

## 4. Run

### One-off module run
```bash
python run.py citations              # AI citation tracker
python run.py competitors            # Competitor analyzer
python run.py clusters               # Topical cluster generator
python run.py entities               # Entity SEO builder
python run.py outreach               # Guest post outreach
python run.py pr                     # Digital PR generator
python run.py mentions               # Brand mention monitor
python run.py overviews              # AI Overview monitor
```

### Workflows
```bash
python run.py daily                  # citations + mentions + overviews
python run.py weekly                 # competitors + clusters + outreach + pr + entities
python run.py all                    # everything
```

### Publish a generated article
```bash
python run.py publish data/briefs/cctv-monitoring-sydney.md --status draft
```

## 5. Schedule (cron)

```cron
# Daily at 06:00
0 6 * * * cd /opt/seo-bot && /opt/seo-bot/.venv/bin/python run.py daily >> data/cron.log 2>&1
# Weekly Mon 07:00
0 7 * * 1 cd /opt/seo-bot && /opt/seo-bot/.venv/bin/python run.py weekly >> data/cron.log 2>&1
```

## 6. Schedule (GitHub Actions)

A starter workflow lives at `.github/workflows/seo-bot.yml` (committed
separately if you opt in). Add secrets in repo Settings → Secrets and
variables → Actions matching your `.env` keys.

## 7. Output locations

- CSV exports → `data/*.csv`
- Generated article briefs → `data/briefs/*.md`
- Generated schema → `data/schema/*.json`
- Outreach email drafts → `data/emails/*.txt`
- Logs → `data/seo-bot.log`

## 8. Publishing notes

- **WordPress**: fully automated via REST API + Application Passwords. Posts
  are created as `draft` by default. Change with `--status publish`.
- **LinkedIn / X / Reddit / Facebook**: drafts are written to
  `data/social_drafts/*.md`. Auto-posting violates each platform's ToS for
  unattended bots. Recommended: pipe drafts to **Buffer** or **Hootsuite**
  via their APIs (stubs included in `publishers/social_drafts.py`).
- **Medium**: API was deprecated in 2023. Drafts exported to
  `data/medium_drafts/*.md` for paste-in.

## 9. Troubleshooting

- *"ANTHROPIC_API_KEY missing"* — copy `.env.example` to `.env` and fill it in.
- *Playwright errors* — run `playwright install chromium`.
- *WordPress 401* — generate an **Application Password** (not your login
  password) at WP Admin → Users → Profile.
- *SerpAPI 429* — you've exhausted the free tier; the module falls back to
  DuckDuckGo HTML automatically.
