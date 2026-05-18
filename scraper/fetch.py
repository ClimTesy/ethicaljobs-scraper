def iter_category_jobs():
    for path in CATEGORIES:
        page = 1
        while True:
            url = f"{ETHICALJOBS_BASE}{path}?page={page}"
            soup = get_page(url)

            # Updated selector for new EthicalJobs HTML
            cards = soup.select("a[href*='/job/'], a[href*='/jobs/']")
            if not cards:
                break

            for a in cards:
                href = a.get("href")
                if not href:
                    continue

                # Normalize relative URLs
                if href.startswith("/"):
                    job_url = ETHICALJOBS_BASE + href
                else:
                    job_url = href

                job_url = job_url.split("?")[0]
                yield job_url

            page += 1
