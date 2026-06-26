# AI-Signals Job Scraper

Finds Product Manager jobs you're a strong fit for (score 8+/10) using Claude AI.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Configure credentials
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Edit your profile
nano profile.yaml   # fill in your real background, skills, preferences
```

## Usage

```bash
# Quick run — scrapes HN Who's Hiring + Greenhouse/Lever (no browser needed)
python main.py

# Include Indeed and LinkedIn (uses Playwright browser)
python main.py --sources hn,greenhouse,indeed,linkedin

# Custom query/location for Indeed & LinkedIn
python main.py --sources indeed,linkedin --query "Senior Product Manager" --location "San Francisco"

# Lower the threshold (show 7+ instead of 8+)
python main.py --threshold 7

# Export matches to JSON + Markdown files
python main.py --export

# All options
python main.py --sources hn,greenhouse,indeed,linkedin --threshold 8 --query "PM" --location "Remote" --export
```

## Sources

| Source | Auth needed | Notes |
|--------|-------------|-------|
| Hacker News | No | Monthly "Who's Hiring" thread via Algolia API |
| Greenhouse / Lever | No | Public ATS boards for 40+ top tech companies |
| Indeed | No | Uses Playwright headless browser |
| LinkedIn | Optional | Works without login; add credentials to `.env` for more results |

## How scoring works

Each job is sent to Claude (Haiku — fast & cheap) along with your `profile.yaml`.
Claude returns a 1-10 fit score, a 2-3 sentence reasoning, and key highlights/gaps.
Only jobs scoring **8 or above** are shown.

## Customizing your profile

Edit `profile.yaml` to reflect your actual background:
- `skills` — list your real skills
- `preferred_industries` — what you want to work on
- `deal_breakers` — what to avoid
- `additional_context` — free-text notes for the scorer

## Adding more companies

In `job_scraper/scrapers/greenhouse_lever.py`, add company slugs to:
- `GREENHOUSE_COMPANIES` — find the slug in `boards.greenhouse.io/<slug>`
- `LEVER_COMPANIES` — find the slug in `jobs.lever.co/<slug>`
