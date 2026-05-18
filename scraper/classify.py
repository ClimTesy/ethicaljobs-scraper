# scraper/classify.py
from .config import SECTOR_KEYWORDS

def classify_sector(text: str) -> str | None:
    t = text.lower()
    for sector, keywords in SECTOR_KEYWORDS.items():
        if any(k in t for k in keywords):
            return sector
    return None
