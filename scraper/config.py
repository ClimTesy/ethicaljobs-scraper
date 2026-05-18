# scraper/config.py

ETHICALJOBS_BASE = "https://www.ethicaljobs.com.au"

CATEGORIES = [
    "/jobs?categories=health-care-medical",
    "/jobs?categories=international-development",
    "/jobs?categories=project-management",
    "/jobs?categories=community-development",
    "/jobs?categories=policy-research",
    "/jobs?categories=consulting-strategy",
    "/jobs?categories=education-training",
    "/jobs?categories=environment-conservation",
    "/jobs?categories=information-communication-technology",
]


GOOGLE_SHEET_NAME = "EthicalJobs Sector Dataset"

SECTOR_TABS = {
    "health": "Health",
    "health_data": "Health Data / Health Information / Digital Health",
    "int_dev": "International Development",
    "prog_mgmt": "Program Management",
    "mel": "Monitoring & Evaluation (MEL / MERL / MEAL)",
    "prog_effect": "Program Effectiveness / Quality / Performance",
    "agriculture": "Agriculture / Food Systems / Rural Development",
}

# simple keyword rules (can be refined)
SECTOR_KEYWORDS = {
    "health_data": [
        "health information", "health data", "digital health", "his", "dhis2",
        "emr", "ehr", "health informatics", "data quality", "health surveillance",
        "public health intelligence"
    ],
    "mel": [
        "mel", "merl", "meal", "monitoring and evaluation",
        "monitoring, evaluation", "results framework", "performance monitoring"
    ],
    "prog_effect": [
        "program quality", "program effectiveness", "program performance",
        "quality assurance"
    ],
    "prog_mgmt": [
        "program manager", "programme manager", "project manager",
        "project coordinator", "program officer", "portfolio manager"
    ],
    "int_dev": [
        "international development", "dfat", "indo-pacific", "pacific",
        "development program", "aid program", "capacity building"
    ],
    "agriculture": [
        "agriculture", "food systems", "rural development",
        "livelihoods", "value chain"
    ],
    "health": [
        "public health", "health promotion", "health systems",
        "clinical governance", "health system strengthening"
    ],
}
