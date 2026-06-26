"""Score job fit using Claude AI."""
import json
import os
import anthropic
from .models import Job


_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


SCORING_PROMPT = """\
You are a career coach evaluating how well a candidate fits a job posting.

## Candidate Profile
{profile}

## Job Posting
Title: {title}
Company: {company}
Location: {location}
{salary_line}
Description:
{description}

## Task
Score how well this candidate fits this job on a scale of 1-10:
- 10: Perfect fit — all skills match, ideal industry, great level
- 8-9: Strong fit — most skills match, minor gaps
- 6-7: Decent fit — some relevant skills, worth applying
- 4-5: Weak fit — significant skill or role mismatch
- 1-3: Poor fit — wrong role, industry, or level entirely

Respond with ONLY valid JSON in this exact format:
{{
  "score": <number 1-10>,
  "reasoning": "<2-3 sentence summary of why this score>",
  "highlights": ["<strength 1>", "<strength 2>", "<gap or concern>"]
}}
"""


def score_job(job: Job, profile_text: str) -> Job:
    """Score a job against the candidate profile and return updated Job."""
    salary_line = f"Salary: {job.salary}" if job.salary else ""
    prompt = SCORING_PROMPT.format(
        profile=profile_text,
        title=job.title,
        company=job.company,
        location=job.location,
        salary_line=salary_line,
        description=job.description[:3000],
    )

    client = _get_client()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",  # fast + cheap for bulk scoring
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()

    # Extract JSON even if there's surrounding text
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start >= 0 and end > start:
        raw = raw[start:end]

    result = json.loads(raw)
    job.fit_score = float(result.get("score", 0))
    job.fit_reasoning = result.get("reasoning", "")
    job.fit_highlights = result.get("highlights", [])
    return job


def score_jobs(jobs: list[Job], profile_text: str, threshold: float = 8.0) -> list[Job]:
    """Score all jobs and return those meeting the threshold, sorted by score."""
    scored = []
    for job in jobs:
        try:
            scored.append(score_job(job, profile_text))
        except Exception as e:
            job.fit_score = 0
            job.fit_reasoning = f"Scoring failed: {e}"
            scored.append(job)

    return sorted(
        [j for j in scored if (j.fit_score or 0) >= threshold],
        key=lambda j: j.fit_score or 0,
        reverse=True,
    )
