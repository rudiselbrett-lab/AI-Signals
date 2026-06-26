from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Job:
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    salary: Optional[str] = None
    job_type: Optional[str] = None  # full-time, contract, etc.
    posted_date: Optional[str] = None
    fit_score: Optional[float] = None
    fit_reasoning: Optional[str] = None
    fit_highlights: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "url": self.url,
            "source": self.source,
            "salary": self.salary,
            "job_type": self.job_type,
            "posted_date": self.posted_date,
            "fit_score": self.fit_score,
            "fit_reasoning": self.fit_reasoning,
            "fit_highlights": self.fit_highlights,
            "description_preview": self.description[:300] + "..." if len(self.description) > 300 else self.description,
        }
