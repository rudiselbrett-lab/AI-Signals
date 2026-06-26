#!/usr/bin/env python3
"""
AI-Signals Job Scraper
Finds jobs you're a good fit for (score 8+/10) using Claude AI.

Usage:
  python main.py [--sources hn,greenhouse,indeed,linkedin] [--threshold 8] [--export]
"""
import argparse
import os
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

load_dotenv()
console = Console()

PROFILE_PATH = Path(__file__).parent / "profile.yaml"


def load_profile() -> str:
    if not PROFILE_PATH.exists():
        console.print("[red]profile.yaml not found. Copy profile.yaml and fill in your details.[/red]")
        sys.exit(1)
    data = yaml.safe_load(PROFILE_PATH.read_text())
    candidate = data.get("candidate", {})
    lines = [
        f"Name: {candidate.get('name', 'N/A')}",
        f"Title: {candidate.get('title', 'N/A')}",
        f"Years of experience: {candidate.get('years_of_experience', 'N/A')}",
        f"\nSummary:\n{candidate.get('summary', '').strip()}",
        f"\nSkills: {', '.join(candidate.get('skills', []))}",
        f"\nPreferred industries: {', '.join(candidate.get('preferred_industries', []))}",
        f"Preferred locations: {', '.join(candidate.get('preferred_locations', []))}",
        f"Company size preference: {', '.join(candidate.get('preferred_company_size', []))}",
        f"\nDeal breakers: {', '.join(candidate.get('deal_breakers', []))}",
        f"\nAdditional context:\n{candidate.get('additional_context', '').strip()}",
    ]
    return "\n".join(lines)


def parse_args():
    parser = argparse.ArgumentParser(description="AI-powered PM job finder")
    parser.add_argument(
        "--sources",
        default="hn,greenhouse",
        help="Comma-separated sources: hn, greenhouse, indeed, linkedin (default: hn,greenhouse)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=float(os.getenv("FIT_SCORE_THRESHOLD", "8")),
        help="Minimum fit score to include (default: 8)",
    )
    parser.add_argument(
        "--query",
        default="Product Manager",
        help="Search query for Indeed/LinkedIn (default: 'Product Manager')",
    )
    parser.add_argument(
        "--location",
        default="Remote",
        help="Location for Indeed/LinkedIn (default: Remote)",
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export results to JSON and Markdown files",
    )
    parser.add_argument(
        "--max-jobs",
        type=int,
        default=50,
        help="Max jobs to fetch per source (default: 50)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    sources = [s.strip().lower() for s in args.sources.split(",")]

    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]ANTHROPIC_API_KEY not set. Add it to your .env file.[/red]")
        sys.exit(1)

    profile_text = load_profile()
    console.print(f"[bold]AI-Signals Job Scraper[/bold] — threshold: {args.threshold}/10\n")
    console.print(f"Sources: {', '.join(sources)}")
    console.print(f"Query: {args.query} | Location: {args.location}\n")

    all_jobs = []

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:

        if "hn" in sources:
            task = progress.add_task("Scraping Hacker News Who's Hiring...", total=None)
            from job_scraper.scrapers import hn
            pm_keywords = ["product manager", "PM", "product lead", "head of product", "product owner"]
            jobs = hn.scrape(keywords=pm_keywords)
            all_jobs.extend(jobs)
            progress.update(task, description=f"HN: found {len(jobs)} PM posts")
            progress.stop_task(task)

        if "greenhouse" in sources or "lever" in sources:
            task = progress.add_task("Scraping Greenhouse & Lever job boards...", total=None)
            from job_scraper.scrapers import greenhouse_lever
            jobs = greenhouse_lever.scrape()
            all_jobs.extend(jobs)
            progress.update(task, description=f"Greenhouse/Lever: found {len(jobs)} jobs")
            progress.stop_task(task)

        if "indeed" in sources:
            task = progress.add_task(f"Scraping Indeed for '{args.query}'...", total=None)
            from job_scraper.scrapers import indeed
            jobs = indeed.scrape(query=args.query, location=args.location, max_pages=3)
            all_jobs.extend(jobs)
            progress.update(task, description=f"Indeed: found {len(jobs)} jobs")
            progress.stop_task(task)

        if "linkedin" in sources:
            task = progress.add_task(f"Scraping LinkedIn for '{args.query}'...", total=None)
            from job_scraper.scrapers import linkedin
            jobs = linkedin.scrape(query=args.query, location=args.location, max_jobs=args.max_jobs)
            all_jobs.extend(jobs)
            progress.update(task, description=f"LinkedIn: found {len(jobs)} jobs")
            progress.stop_task(task)

        # Deduplicate by URL
        seen_urls = set()
        unique_jobs = []
        for job in all_jobs:
            if job.url not in seen_urls:
                seen_urls.add(job.url)
                unique_jobs.append(job)

        console.print(f"\n[bold]Total unique jobs found:[/bold] {len(unique_jobs)}")

        if not unique_jobs:
            console.print("[yellow]No jobs found. Try different sources or check your network.[/yellow]")
            return

        # Score with Claude
        score_task = progress.add_task(
            f"Scoring {len(unique_jobs)} jobs with Claude AI...", total=len(unique_jobs)
        )
        from job_scraper.scorer import score_job
        scored = []
        for job in unique_jobs:
            try:
                scored.append(score_job(job, profile_text))
            except Exception as e:
                console.print(f"[dim red]Scoring error for {job.title} at {job.company}: {e}[/dim red]")
                job.fit_score = 0
                scored.append(job)
            progress.advance(score_task)

        matches = sorted(
            [j for j in scored if (j.fit_score or 0) >= args.threshold],
            key=lambda j: j.fit_score or 0,
            reverse=True,
        )

    from job_scraper.output import print_results, export_json, export_markdown
    print_results(matches, threshold=args.threshold)

    if args.export and matches:
        json_path = export_json(matches)
        md_path = export_markdown(matches)
        console.print(f"[dim]Exported: {json_path}[/dim]")
        console.print(f"[dim]Exported: {md_path}[/dim]")


if __name__ == "__main__":
    main()
