# scraper/sheets.py
import gspread
from google.oauth2.service_account import Credentials
from .config import GOOGLE_SHEET_NAME, SECTOR_TABS

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_client(service_account_json_path: str):
    # DEBUG: Show where the file is and what it contains
    print("DEBUG: Attempting to load JSON from:", service_account_json_path)

    try:
        with open(service_account_json_path, "r") as f:
            raw = f.read()
        print("DEBUG: First 200 chars of file:", raw[:200])
    except Exception as e:
        print("DEBUG: Failed to read file:", e)
        raise

    # Now let Google load it normally
    creds = Credentials.from_service_account_file(service_account_json_path, scopes=SCOPES)
    return gspread.authorize(creds)

def get_sheet(client, sector_key: str):
    sh = client.open(GOOGLE_SHEET_NAME)
    tab_name = SECTOR_TABS[sector_key]
    return sh.worksheet(tab_name)

def existing_job_ids(ws) -> set:
    try:
        col = ws.col_values(1)  # assuming job_id is column A
        return set(col[1:])     # skip header
    except Exception:
        return set()

def append_jobs(ws, rows: list[dict]):
    if not rows:
        return
    # ensure header
    header = [
        "job_id", "title", "organisation", "category", "location",
        "salary", "posted_date", "closing_date", "url",
        "description_raw", "experience_extracted", "sector_tag", "scraped_at"
    ]
    if not ws.get_all_values():
        ws.append_row(header)
    values = [
        [
            r["job_id"], r["title"], r["organisation"], r["category"], r["location"],
            r["salary"], r["posted_date"], r["closing_date"], r["url"],
            r["description_raw"], r["experience_extracted"], r["sector_tag"], r["scraped_at"]
        ]
        for r in rows
    ]
    ws.append_rows(values, value_input_option="RAW")
