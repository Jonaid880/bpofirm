# GitHub Actions setup

The workflow at `.github/workflows/seo-bot.yml` runs the bot automatically:

| Trigger | Cron (UTC) | Local (Sydney) | Command |
|---------|-----------|-----------------|---------|
| Daily   | `0 6 * * *`     | 16:00 AEST / 17:00 AEDT | `python run.py daily` |
| Weekly  | `0 19 * * 1`    | Tue 05:00 AEST / 06:00 AEDT | `python run.py weekly` |
| Manual  | `workflow_dispatch` | any time, you pick command | any of the 12 |

## 1. Add the only required secret

GitHub → repo Settings → Secrets and variables → **Actions** → **New repository secret**:

| Name | Value |
|------|-------|
| `ANTHROPIC_API_KEY` | from https://console.anthropic.com |

That's the minimum. With only this secret set, the bot runs every module that doesn't need external paid APIs.

## 2. Add optional secrets (in priority order)

| Secret | What it unlocks | Cost |
|--------|-----------------|------|
| `SERPAPI_KEY` | Google AI Overview tracking; SERPs without scraping | Free 100/mo |
| `WORDPRESS_URL`, `WORDPRESS_USER`, `WORDPRESS_APP_PASSWORD` | Auto-publishing to your WP site | Free |
| `DEVTO_API_KEY` | Auto-publish to Dev.to (canonical -> WP) | Free |
| `HASHNODE_API_KEY`, `HASHNODE_PUBLICATION_ID` | Auto-publish to Hashnode | Free |
| `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_AUTHOR_URN` | LinkedIn UGC posts | Free |
| `GOOGLE_PLACES_API_KEY`, `GOOGLE_PLACE_ID` | Google review monitoring + reply drafts | Free up to limits |
| `AHREFS_API_KEY` | Real backlink data (vs SERP-scrape fallback) | ~US$129/mo |
| `PERPLEXITY_API_KEY` | Higher-fidelity AI citation tracking | Pay-as-you-go |
| `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` | Bulk SERP data | Pay-as-you-go |

Add each via the same Settings → Secrets and variables → Actions page.

## 3. Add repository variables (non-secret config)

Settings → Secrets and variables → Actions → **Variables** tab:

| Variable | Default | Override if |
|----------|---------|-------------|
| `SITE_URL` | `https://securityblogs.com.au` | you change domain |
| `SITE_NAME` | `SecurityBlogs` | rebrand |
| `BRAND_NAMES` | `SecurityBlogs,Security Blogs Australia` | add aliases |
| `PRODUCTREVIEW_SLUG` | (empty) | set to your ProductReview.com.au slug to enable review pulls |
| `TRUSTPILOT_DOMAIN` | (empty) | set to `securityblogs.com.au` to enable Trustpilot |

## 4. Trigger your first run

GitHub → **Actions** tab → **seo-bot** workflow → **Run workflow** button → choose a command (try `daily` first) → **Run workflow**.

After ~2–5 min, the run completes. Click into it → bottom of page → **Artifacts** → download `seo-bot-output-<run-id>.zip` to inspect every CSV, brief, schema file and email draft.

## 5. (Optional) Persist outputs in the repo

If you'd rather browse historical runs directly on GitHub instead of downloading ZIPs:

1. Create an empty branch named `seo-bot-data`:
   ```bash
   git checkout --orphan seo-bot-data
   git rm -rf .
   git commit --allow-empty -m "init"
   git push -u origin seo-bot-data
   ```
2. Uncomment the `commit-artifacts:` job at the bottom of `.github/workflows/seo-bot.yml`.
3. Change the top-level `permissions:` block to `contents: write`.

Every scheduled run will then commit its `data/` folder to that branch.

## 6. Cost expectation

- Anthropic spend per **daily** run: ~US$0.05–0.20 (haiku for most calls)
- Anthropic spend per **weekly** run: ~US$0.50–2.00 (opus for cluster + PR generation)
- GitHub Actions: free for public repos; 2,000 free minutes/month on free private repos (this workflow uses ~3 min/day + ~10 min/week = ~130 min/month)

## 7. Troubleshooting

- **Workflow doesn't appear in Actions tab** → the workflow file must be merged to the **default branch** for the schedule to fire. PRs can trigger via `workflow_dispatch`.
- **"ANTHROPIC_API_KEY missing"** → secret name typo (must be exactly `ANTHROPIC_API_KEY`) or you added it as an Environment secret instead of a Repository secret.
- **All runs upload empty artifacts** → check the run log; usually a missing secret causing every module to skip.
- **You want notifications** → add a Slack/Discord webhook step at the end of the job.
