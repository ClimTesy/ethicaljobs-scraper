# scraper/experience.py
import re

NUMERIC_PATTERNS = [
    r"(\d+)\s*\+?\s*(years|yrs)",
    r"at least\s+(\d+)\s*(years|yrs)?",
    r"minimum of\s+(\d+)\s*(years|yrs)?",
    r"(\d+)\s*(years|yrs)\s*(experience|exp)",
]

def extract_experience(text: str) -> str:
    t = text.lower()
    for pattern in NUMERIC_PATTERNS:
        m = re.search(pattern, t)
        if m:
            return f"{m.group(1)} years"
    if "demonstrated experience" in t or "proven experience" in t or "extensive experience" in t:
        return "qualitative only"
    return ""
