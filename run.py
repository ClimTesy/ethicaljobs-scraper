# run.py
from scraper.fetch import iter_category_jobs
from scraper.parse import parse_job
from scraper.classify import classify_sector
from scraper.experience import extract_experience
from scraper.sheets import get_client, get_sheet, existing_job_ids, append_jobs

SERVICE_ACCOUNT_JSON = "service_account.json"  # path in repo or secret mount

def main():
    client = get_client(SERVICE_ACCOUNT_JSON)

    sector_buffers: dict[str, list[dict]] = {}

    seen_urls = set()
    for url in iter_category_jobs():
        if url in seen_urls:
            continue
        seen_urls.add(url)

        job = parse_job(url)
        sector = classify_sector(job["description_raw"] + " " + job["title"])
        if not sector:
            continue

        job["experience_extracted"] = extract_experience(job["description_raw"])
        job["sector_tag"] = sector

        sector_buffers.setdefault(sector, []).append(job)

    for sector_key, jobs in sector_buffers.items():
        ws = get_sheet(client, sector_key)
        existing = existing_job_ids(ws)
        new_rows = [j for j in jobs if j["job_id"] not in existing]
        append_jobs(ws, new_rows)

if __name__ == "__main__":
    main()
