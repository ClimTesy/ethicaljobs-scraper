# scraper/fetch.py
import requests
from bs4 import BeautifulSoup
from .config import ETHICALJOBS_BASE, CATEGORIES

def get_page(url: str) -> BeautifulSoup:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def iter_category_jobs():
    for path in CATEGORIES:
        page = 1
        while True:
            url = f"{ETHICALJOBS_BASE}{path}?page={page}"
            soup = get_page(url)
            cards = soup.select("a[href*='/jobs/']")
            if not cards:
                break
            for a in cards:
                job_url = a.get("href")
                if job_url and "/jobs/" in job_url:
                    yield ETHICALJOBS_BASE + job_url.split("?")[0]
            page += 1
