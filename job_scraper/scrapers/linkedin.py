"""Scraper for LinkedIn job listings using Playwright.

LinkedIn aggressively blocks scrapers. This uses the public jobs search
(no login required) which is rate-limited but works for moderate usage.
For heavier use, provide LINKEDIN_EMAIL/LINKEDIN_PASSWORD in .env.
"""
import asyncio
import os
from playwright.async_api import async_playwright, TimeoutError as PWTimeout
from ..models import Job


BASE_URL = "https://www.linkedin.com"


async def _login(page, email: str, password: str) -> bool:
    try:
        await page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded", timeout=20000)
        await page.fill('#username', email)
        await page.fill('#password', password)
        await page.click('[type=submit]')
        await page.wait_for_timeout(3000)
        return "feed" in page.url or "jobs" in page.url
    except Exception:
        return False


async def _scrape_async(query: str, location: str, max_jobs: int = 25) -> list[Job]:
    jobs = []
    email = os.getenv("LINKEDIN_EMAIL", "")
    password = os.getenv("LINKEDIN_PASSWORD", "")

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

        if email and password:
            await _login(page, email, password)

        # Use the public jobs search (works without login)
        search_url = (
            f"{BASE_URL}/jobs/search/?keywords={query.replace(' ', '%20')}"
            f"&location={location.replace(' ', '%20')}&sortBy=DD&f_TPR=r86400"
        )
        try:
            await page.goto(search_url, wait_until="domcontentloaded", timeout=25000)
            await page.wait_for_timeout(3000)
        except PWTimeout:
            await browser.close()
            return []

        collected = 0
        prev_count = 0
        while collected < max_jobs:
            cards = await page.query_selector_all('.jobs-search__results-list li, .base-card')
            if not cards:
                break

            for card in cards[prev_count:]:
                if collected >= max_jobs:
                    break
                try:
                    await card.click()
                    await page.wait_for_timeout(1500)

                    title_el = await page.query_selector('.job-details-jobs-unified-top-card__job-title')
                    company_el = await page.query_selector('.job-details-jobs-unified-top-card__company-name')
                    location_el = await page.query_selector('.job-details-jobs-unified-top-card__bullet')
                    desc_el = await page.query_selector('.jobs-description-content__text')
                    salary_el = await page.query_selector('.job-details-jobs-unified-top-card__job-insight span')

                    title = (await title_el.inner_text()).strip() if title_el else "Unknown"
                    company = (await company_el.inner_text()).strip() if company_el else "Unknown"
                    loc = (await location_el.inner_text()).strip() if location_el else location
                    desc = (await desc_el.inner_text()).strip() if desc_el else ""
                    salary = (await salary_el.inner_text()).strip() if salary_el else None
                    job_url = page.url

                    jobs.append(Job(
                        title=title,
                        company=company,
                        location=loc,
                        description=desc[:4000],
                        url=job_url,
                        source="LinkedIn",
                        salary=salary,
                    ))
                    collected += 1
                except Exception:
                    continue

            prev_count = len(cards)
            # Scroll to load more
            try:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                new_cards = await page.query_selector_all('.jobs-search__results-list li, .base-card')
                if len(new_cards) == prev_count:
                    break
            except Exception:
                break

        await browser.close()
    return jobs


def scrape(query: str = "Product Manager", location: str = "Remote", max_jobs: int = 25) -> list[Job]:
    return asyncio.run(_scrape_async(query, location, max_jobs))
