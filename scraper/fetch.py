# scraper/fetch.py
import requests
from bs4 import BeautifulSoup
from .config import ETHICALJOBS_BASE, CATEGORIES

def get_page(url: str) -> BeautifulSoup:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def iter_category_jobs():
    for path in CATEGORIES:
        page = 1
        while True:
            url = f"{ETHICALJOBS_BASE}{path}&page={page}"
            print("DEBUG: Fetching URL:", url)

            try:
                soup = get_page(url)
            except Exception as e:
                print("DEBUG: Failed to fetch page:", url, e)
                break

            cards = soup.select("a[href*='/job/'], a[href*='/jobs/']")
            print("DEBUG: Found", len(cards), "job links on page", page)

            if not cards:
                break

            for a in cards:
                href = a.get("href")
                if not href:
                    continue

                if href.startswith("/"):
                    job_url = ETHICALJOBS_BASE + href
                else:
                    job_url = href

                job_url = job_url.split("?")[0]
                yield job_url

            page += 1
