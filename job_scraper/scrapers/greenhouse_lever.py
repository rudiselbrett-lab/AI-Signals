"""
Scraper for Greenhouse and Lever ATS job boards via their public APIs.

These are the job board backends used by hundreds of companies.
No auth required — they expose public JSON endpoints.
"""
import httpx
from ..models import Job


# Well-known companies using Greenhouse (add more as needed)
GREENHOUSE_COMPANIES = [
    "airbnb", "stripe", "notion", "figma", "linear", "vercel",
    "openai", "anthropic", "databricks", "ramp", "brex", "plaid",
    "airtable", "rippling", "retool", "scale-ai", "anyscale",
    "lattice", "deel", "remote", "mercury", "loom", "superhuman",
]

# Well-known companies using Lever
LEVER_COMPANIES = [
    "netflix", "shopify", "twilio", "hashicorp", "fastly",
    "cloudflare", "carta", "cockroachdb", "fivetran", "dbt-labs",
    "snyk", "postman", "amplitude", "segment", "mixpanel",
]


def _fetch_greenhouse(company: str, keywords: list[str]) -> list[Job]:
    url = f"https://api.greenhouse.io/v1/boards/{company}/jobs?content=true"
    try:
        resp = httpx.get(url, timeout=10)
        resp.raise_for_status()
        jobs_data = resp.json().get("jobs", [])
    except Exception:
        return []

    jobs = []
    for j in jobs_data:
        title = j.get("title", "")
        if keywords and not any(kw.lower() in title.lower() for kw in keywords):
            continue
        location_obj = j.get("location", {})
        loc = location_obj.get("name", "Unknown") if isinstance(location_obj, dict) else str(location_obj)
        desc_html = j.get("content", "")
        import re
        desc = re.sub(r"<[^>]+>", " ", desc_html).strip()[:4000]
        jobs.append(Job(
            title=title,
            company=company.replace("-", " ").title(),
            location=loc,
            description=desc,
            url=j.get("absolute_url", f"https://boards.greenhouse.io/{company}"),
            source="Greenhouse",
            posted_date=j.get("updated_at", "")[:10],
        ))
    return jobs


def _fetch_lever(company: str, keywords: list[str]) -> list[Job]:
    url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    try:
        resp = httpx.get(url, timeout=10)
        resp.raise_for_status()
        postings = resp.json()
    except Exception:
        return []

    jobs = []
    for p in postings:
        title = p.get("text", "")
        if keywords and not any(kw.lower() in title.lower() for kw in keywords):
            continue
        categories = p.get("categories", {})
        loc = categories.get("location", "Unknown")
        # Lever nests description in lists
        desc_parts = []
        for section in p.get("descriptionBody", {}).get("content", []):
            if isinstance(section, dict):
                for item in section.get("content", []):
                    if isinstance(item, dict) and item.get("type") == "text":
                        desc_parts.append(item.get("text", ""))
        desc = " ".join(desc_parts)[:4000] or p.get("description", "")[:4000]
        jobs.append(Job(
            title=title,
            company=company.replace("-", " ").title(),
            location=loc,
            description=desc,
            url=p.get("hostedUrl", f"https://jobs.lever.co/{company}"),
            source="Lever",
            posted_date=str(p.get("createdAt", ""))[:10],
        ))
    return jobs


def scrape(keywords: list[str] | None = None) -> list[Job]:
    kw = keywords or ["product manager", "PM", "product lead"]
    jobs = []
    for company in GREENHOUSE_COMPANIES:
        jobs.extend(_fetch_greenhouse(company, kw))
    for company in LEVER_COMPANIES:
        jobs.extend(_fetch_lever(company, kw))
    return jobs
