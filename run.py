from scraper.fetch import iter_category_jobs
from scraper.parse import parse_job
from scraper.classify import classify_sector
from scraper.experience import extract_experience
from scraper.sheets import get_client, get_sheet, existing_job_ids, append_jobs

SERVICE_ACCOUNT_JSON = "service_account.json"

def main():
    client = get_client(SERVICE_ACCOUNT_JSON)

    sector_buffers: dict[str, list[dict]] = {}

    seen_urls = set()
    print("DEBUG: Starting job iteration")
    for url in iter_category_jobs():
        print("DEBUG: Found job URL:", url)

        if url in seen_urls:
            print("DEBUG: Skipping duplicate URL:", url)
            continue
        seen_urls.add(url)

        job = parse_job(url)
        print("DEBUG: Parsed job:", job.get("job_id"), job.get("title"))

        sector = classify_sector(job["description_raw"] + " " + job["title"])
        print("DEBUG: Classified sector:", sector)

        if not sector:
            print("DEBUG: No sector — skipping job")
            continue

        job["experience_extracted"] = extract_experience(job["description_raw"])
        job["sector_tag"] = sector

        sector_buffers.setdefault(sector, []).append(job)

    print("DEBUG: Sector buffers:", {k: len(v) for k, v in sector_buffers.items()})

    for sector_key, jobs in sector_buffers.items():
        print(f"DEBUG: Processing sector '{sector_key}' with {len(jobs)} jobs")

        ws = get_sheet(client, sector_key)
        existing = existing_job_ids(ws)
        print("DEBUG: Existing job IDs:", len(existing))

        new_rows = [j for j in jobs if j["job_id"] not in existing]
        print("DEBUG: New rows to append:", len(new_rows))

        append_jobs(ws, new_rows)

if __name__ == "__main__":
    main()
