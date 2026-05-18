# scraper/parse.py
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup
import requests

def job_id_from_url(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()

def parse_job(url: str) -> dict:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    title = (soup.select_one("h1") or {}).get_text(strip=True) if soup.select_one("h1") else ""
    org = (soup.select_one("[class*='org'], .job-org") or {}).get_text(strip=True) if soup.select_one("[class*='org'], .job-org") else ""
    location = (soup.select_one("[class*='location'], .job-location") or {}).get_text(strip=True) if soup.select_one("[class*='location'], .job-location") else ""
    category = (soup.select_one("[class*='category'], .job-category") or {}).get_text(strip=True) if soup.select_one("[class*='category'], .job-category") else ""
    salary = (soup.select_one("[class*='salary']") or {}).get_text(strip=True) if soup.select_one("[class*='salary']") else ""

    # crude: full text for experience + sector classification
    description_raw = soup.get_text(" ", strip=True)

    return {
        "job_id": job_id_from_url(url),
        "title": title,
        "organisation": org,
        "category": category,
        "location": location,
        "salary": salary,
        "posted_date": "",      # can be refined if visible
        "closing_date": "",     # can be refined if visible
        "url": url,
        "description_raw": description_raw,
        "scraped_at": datetime.utcnow().isoformat(timespec="seconds"),
    }
