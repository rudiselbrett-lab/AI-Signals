"""Scraper for Hacker News 'Who is Hiring?' monthly threads via Algolia API."""
import httpx
from datetime import datetime
from ..models import Job


HN_ALGOLIA = "https://hn.algolia.com/api/v1"


def _get_latest_who_is_hiring_id() -> int | None:
    """Find the most recent 'Ask HN: Who is hiring?' post."""
    resp = httpx.get(
        f"{HN_ALGOLIA}/search",
        params={
            "query": "Ask HN: Who is hiring?",
            "tags": "story,ask_hn",
            "hitsPerPage": 5,
        },
        timeout=15,
    )
    resp.raise_for_status()
    hits = resp.json().get("hits", [])
    for hit in hits:
        title = hit.get("title", "")
        if "who is hiring" in title.lower() and str(datetime.now().year) in title:
            return int(hit["objectID"])
    # Fall back to first result
    if hits:
        return int(hits[0]["objectID"])
    return None


def _fetch_comments(story_id: int) -> list[dict]:
    """Fetch all top-level comments from a HN story."""
    comments = []
    page = 0
    while True:
        resp = httpx.get(
            f"{HN_ALGOLIA}/search",
            params={
                "tags": f"comment,story_{story_id}",
                "hitsPerPage": 100,
                "page": page,
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        hits = data.get("hits", [])
        if not hits:
            break
        comments.extend(hits)
        if len(comments) >= data.get("nbHits", 0):
            break
        page += 1
    return comments


def _parse_comment_to_job(comment: dict) -> Job | None:
    text = comment.get("comment_text", "") or ""
    if not text or len(text) < 100:
        return None

    # Strip HTML tags for cleaner text
    import re
    clean = re.sub(r"<[^>]+>", " ", text).strip()

    # First line usually has company | role | location
    first_line = clean.split("\n")[0][:200]
    parts = [p.strip() for p in first_line.split("|")]

    company = parts[0] if parts else "Unknown"
    title = parts[1] if len(parts) > 1 else "Product Manager"
    location = parts[2] if len(parts) > 2 else "Remote"

    story_id = comment.get("story_id") or comment.get("parent_id")
    url = f"https://news.ycombinator.com/item?id={comment['objectID']}"

    return Job(
        title=title,
        company=company,
        location=location,
        description=clean[:4000],
        url=url,
        source="Hacker News",
        posted_date=comment.get("created_at", "")[:10],
    )


def scrape(keywords: list[str] | None = None) -> list[Job]:
    """Return jobs from the current HN Who is Hiring thread."""
    story_id = _get_latest_who_is_hiring_id()
    if not story_id:
        return []

    comments = _fetch_comments(story_id)
    jobs = []
    for comment in comments:
        job = _parse_comment_to_job(comment)
        if job is None:
            continue
        text_lower = (job.description + job.title).lower()
        # Filter to PM-relevant posts unless no keywords given
        if keywords:
            if not any(kw.lower() in text_lower for kw in keywords):
                continue
        jobs.append(job)

    return jobs
