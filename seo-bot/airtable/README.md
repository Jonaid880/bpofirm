# Airtable Import — StateGuard SEO Command Centre

Four CSVs ready to paste/import into the matching tabs of your **StateGuard SEO Command Centre** Airtable base.

## Files

| File | Goes into Airtable tab | Rows |
|------|------------------------|------|
| `ai_visibility.csv`    | **AI Visibility**     | 52 questions |
| `content_calendar.csv` | **Content Calendar**  | 30 blog briefs |
| `link_opportunities.csv` | **Link Opportunities** | 36 platforms |
| `keywords.csv`         | **Keywords**          | 50 geo-grained queries |

## Two ways to import each file

### Option A — Paste into existing grid (fastest)
1. Open the target Airtable tab.
2. Open the CSV in a spreadsheet app (Excel, Google Sheets) → select all → copy.
3. In Airtable, click the empty row at the bottom of the grid → Cmd/Ctrl+V.
4. Airtable matches columns by name (rename my CSV headers if your table uses different field names).

### Option B — Add or import → CSV file
1. In Airtable, click the **+** next to your tabs → **Add or import** → **CSV file**.
2. Drop the CSV → confirm field-mapping (Airtable auto-detects most).
3. **Important**: pick "Add to existing table" → choose the right tab (e.g. AI Visibility). Do not let Airtable create a new tab.

## Column matching

If your tab field names differ slightly from my CSV headers, rename the CSV column to match the Airtable field name *before* you paste/import. Airtable matches by exact field-name string.

### AI Visibility — my CSV columns
`Question | ChatGPT Citation | Gemini Citation | Perplexity Citation | StateGuard Citation | Competitor Cited | Opportunity Identified | Review Date`

The four "Citation" columns are checkboxes — I've set them all to `false` because the bot hasn't run citation tracking yet. After running `python run.py citations` they'll auto-update.

### Content Calendar — my CSV columns
`Title | Target Query | Intent | Word Count | Direct Answer | Schema Types | Status | Publish To | Priority | Due Date | Cluster Pillar`

If your tab uses `Publish Date` instead of `Due Date`, rename. If you have an `Assignee` column, leave it blank and assign in Airtable.

### Link Opportunities — my CSV columns
`Platform/Site | Type | URL | Priority | Action | Status | DA/DR Est | Notes`

### Keywords — my CSV columns
`Keyword | State | Suburb/Precinct | Intent | AI Overview Likelihood | Service Line | Priority | Notes`

## Recommended import order

1. **Keywords** first — feeds everything else.
2. **AI Visibility** next — uses the keywords.
3. **Content Calendar** next — blog briefs tied to AI Visibility opportunities.
4. **Link Opportunities** last — distribution plan once content exists.

## Want auto-sync instead of CSV paste?

The bot can push directly into your Airtable on every workflow run — no more CSV imports. To enable:

1. Get an Airtable Personal Access Token: https://airtable.com/create/tokens
   - Scopes needed: `data.records:read`, `data.records:write`, `schema.bases:read`
   - Add your base to the token's access list.
2. Find your Base ID: open the base → `Help` → `API documentation` → the URL shows `https://airtable.com/appXXXXXXXXXXXXX/...` — `appXXXXXXXXXXXXX` is the base ID.
3. Add to GitHub Secrets:
   - `AIRTABLE_TOKEN` = the personal access token
   - `AIRTABLE_BASE_ID` = the `app...` string
4. Run `python run.py airtable-sync` once to wire field mappings; thereafter every workflow run auto-pushes.

The sync module lives at `seo-bot/publishers/airtable_sync.py`.

## What changes after the bot runs against StateGuard

Once you set `SITE_URL=https://stateguard.com.au` in `.env`/GitHub Secrets and run:

- `python run.py citations` → populates the 4 Citation columns in **AI Visibility** with real true/false
- `python run.py competitors` → populates **Competitors** tab + updates `Competitor Cited` column
- `python run.py clusters` → generates briefs that map to **Content Calendar** rows
- `python run.py biz-citations` → updates **Link Opportunities** with real existence-check status
- `python run.py mentions` → backfills new mentions as **Link Opportunities** P3 rows
- `python run.py haro` → adds drafted journalist pitches as **Link Opportunities** rows with `Type=Journalist Pitch`
