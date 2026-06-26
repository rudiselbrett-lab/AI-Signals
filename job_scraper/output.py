"""Rich terminal output and JSON export for job results."""
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from .models import Job

console = Console()


def print_results(jobs: list[Job], threshold: float = 8.0) -> None:
    if not jobs:
        console.print(f"\n[yellow]No jobs found scoring {threshold}+ out of 10.[/yellow]")
        return

    console.print(f"\n[bold green]Found {len(jobs)} jobs scoring {threshold}+/10[/bold green]\n")

    for i, job in enumerate(jobs, 1):
        score = job.fit_score or 0
        color = "green" if score >= 9 else "cyan" if score >= 8 else "yellow"

        header = Text()
        header.append(f"#{i} ", style="dim")
        header.append(f"[{score:.0f}/10] ", style=f"bold {color}")
        header.append(f"{job.title}", style="bold white")
        header.append(f" at {job.company}", style="white")
        header.append(f"  [{job.source}]", style="dim")

        body = Text()
        body.append(f"Location: {job.location}\n", style="dim")
        if job.salary:
            body.append(f"Salary: {job.salary}\n", style="dim")
        body.append(f"\n{job.fit_reasoning}\n", style="white")
        if job.fit_highlights:
            body.append("\nHighlights:\n", style="bold")
            for h in job.fit_highlights:
                body.append(f"  • {h}\n", style="cyan")
        body.append(f"\n{job.url}", style="blue underline")

        console.print(Panel(body, title=header, border_style=color, expand=False))
        console.print()


def export_json(jobs: list[Job], output_dir: str = ".") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path(output_dir) / f"jobs_{ts}.json"
    data = [j.to_dict() for j in jobs]
    path.write_text(json.dumps(data, indent=2))
    return str(path)


def export_markdown(jobs: list[Job], output_dir: str = ".") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path(output_dir) / f"jobs_{ts}.md"
    lines = [f"# Job Matches — {datetime.now().strftime('%B %d, %Y')}\n"]
    for i, job in enumerate(jobs, 1):
        score = job.fit_score or 0
        lines.append(f"## {i}. [{job.title} at {job.company}]({job.url})")
        lines.append(f"**Score:** {score:.0f}/10 | **Location:** {job.location} | **Source:** {job.source}")
        if job.salary:
            lines.append(f"**Salary:** {job.salary}")
        lines.append(f"\n{job.fit_reasoning}\n")
        if job.fit_highlights:
            lines.append("**Highlights:**")
            for h in job.fit_highlights:
                lines.append(f"- {h}")
        lines.append("")
    path.write_text("\n".join(lines))
    return str(path)
