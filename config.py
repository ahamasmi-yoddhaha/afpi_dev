"""
Configuration module for the Airfare Scraping and Price Index Engine (APIx).
Defines DGCA representative route basket, advance purchase windows,
ethical rate-limiting safeguards, and target carrier specifications.
"""

from pathlib import Path

# --- BASE DIRECTORIES ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
DB_PATH = DATA_DIR / "airfare_warehouse.db"

# --- DGCA REPRESENTATIVE BASKET OF CITY-PAIRS ---
# Selected based on Directorate General of Civil Aviation (DGCA) domestic passenger traffic data
DGCA_ROUTE_BASKET = [
    {"origin": "DEL", "destination": "BOM", "name": "Delhi - Mumbai"},
    {"origin": "DEL", "destination": "BLR", "name": "Delhi - Bengaluru"},
    {"origin": "BOM", "destination": "BLR", "name": "Mumbai - Bengaluru"},
    {"origin": "DEL", "destination": "CCU", "name": "Delhi - Kolkata"},
    {"origin": "BLR", "destination": "HYD", "name": "Bengaluru - Hyderabad"},
    {"origin": "MAA", "destination": "DEL", "name": "Chennai - Delhi"},
]

# --- ADVANCE-PURCHASE WINDOWS ---
# As specified in the problem statement: T+1, T+7, T+15, T+30, T+45 days
ADVANCE_PURCHASE_WINDOWS = [
    {"label": "T+1", "lead_days": 1},
    {"label": "T+7", "lead_days": 7},
    {"label": "T+15", "lead_days": 15},
    {"label": "T+30", "lead_days": 30},
    {"label": "T+45", "lead_days": 45},
]

# --- TARGET INDIAN CARRIERS ---
TARGET_CARRIERS = [
    "IndiGo",
    "Air India",
    "Air India Express",
    "Akasa Air",
    "SpiceJet",
]

# --- ETHICAL SCRAPING & RATE-LIMITING SAFEGUARDS ---
SCRAPER_SETTINGS = {
    "min_polite_delay": 4.0,       # Minimum delay between queries in seconds
    "max_polite_delay": 8.0,       # Maximum delay between queries (jitter)
    "page_settle_delay": 5.0,      # Wait time for dynamic AJAX cards to render
    "max_retries": 3,              # Exponential backoff retry attempts
    "backoff_factor": 2.0,         # Multiplier for exponential backoff
    "request_timeout": 30,         # Selenium wait timeout
    "daily_run_time": "02:00",     # 02:00 AM IST (low traffic hours)
}

# --- REALISTIC USER-AGENT ROTATION POOL ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
]
