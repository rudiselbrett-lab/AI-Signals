"""Scraper for Indeed job listings using Playwright."""
import asyncio
import re
from playwright.async_api import async_playwright, TimeoutError as PWTimeout
from ..models import Job


BASE_URL = "https://www.indeed.com"


async def _scrape_async(query: str, location: str, max_pages: int = 3) -> list[Job]:
    jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )
        page = await ctx.new_page()

        for pg in range(max_pages):
            start = pg * 10
            url = (
                f"{BASE_URL}/jobs?q={query.replace(' ', '+')}"
                f"&l={location.replace(' ', '+')}&start={start}&sort=date"
            )
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                await page.wait_for_timeout(2000)
            except PWTimeout:
                break

            cards = await page.query_selector_all('[data-jk]')
            if not cards:
                break

            for card in cards:
                try:
                    title_el = await card.query_selector('h2 span')
                    company_el = await card.query_selector('[data-testid="company-name"]')
                    location_el = await card.query_selector('[data-testid="text-location"]')
                    salary_el = await card.query_selector('[data-testid="attribute_snippet_testid"]')
                    jk = await card.get_attribute("data-jk") or ""

                    title = (await title_el.inner_text()) if title_el else "Unknown"
                    company = (await company_el.inner_text()) if company_el else "Unknown"
                    loc = (await location_el.inner_text()) if location_el else "Unknown"
                    salary = (await salary_el.inner_text()) if salary_el else None
                    job_url = f"{BASE_URL}/viewjob?jk={jk}"

                    # Fetch description from job detail page
                    detail = await ctx.new_page()
                    desc = ""
                    try:
                        await detail.goto(job_url, wait_until="domcontentloaded", timeout=15000)
                        desc_el = await detail.query_selector('#jobDescriptionText')
                        if desc_el:
                            desc = await desc_el.inner_text()
                    except Exception:
                        pass
                    finally:
                        await detail.close()

                    jobs.append(Job(
                        title=title.strip(),
                        company=company.strip(),
                        location=loc.strip(),
                        description=desc[:4000],
                        url=job_url,
                        source="Indeed",
                        salary=salary,
                    ))
                except Exception:
                    continue

        await browser.close()
    return jobs


def scrape(query: str = "Product Manager", location: str = "Remote", max_pages: int = 3) -> list[Job]:
    return asyncio.run(_scrape_async(query, location, max_pages))
