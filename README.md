# Real-Time Airfare Scraping & Price Index Engine (APIx)

An end-to-end software platform designed to automatically web-scrape airfare data from major Indian carriers (**IndiGo, Air India, Air India Express, Akasa Air, SpiceJet**), clean and normalize price quotes, and store structured datasets for constructing the **Real-time Airfare Price Index (APIx)**.

---

## 1. System Architecture

```text
afp_scraping/
├── config.py             # DGCA route basket, T+N advance windows, ethical rate-limits
├── scraper_engine.py     # Selenium stealth engine with anti-bot evasion & backoff retries
├── database.py           # SQLite warehouse (airfare_warehouse.db) with de-duplication
├── batch_runner.py       # Full basket orchestrator (6 routes x 5 advance windows = 30 queries)
├── scheduler.py          # Daily scheduled daemon with cron and interval modes
├── flight_scraper.py     # Interactive single-route CLI scraper
├── data/
│   ├── airfare_warehouse.db       # Primary SQLite ACID data warehouse
│   ├── master_airfare_dataset.csv # Cumulative deduplicated CSV dataset
│   └── raw_quotes_YYYYMMDD.csv    # Daily timestamped partition
└── logs/
    └── scraper_daemon.log         # Complete execution and audit logs
```

---

## 2. Key Specifications Implemented

### A. DGCA Representative City-Pair Basket
Selected based on Directorate General of Civil Aviation (DGCA) passenger traffic data:
- **DEL-BOM** (Delhi – Mumbai: #1 busiest domestic corridor)
- **DEL-BLR** (Delhi – Bengaluru)
- **BOM-BLR** (Mumbai – Bengaluru)
- **DEL-CCU** (Delhi – Kolkata)
- **BLR-HYD** (Bengaluru – Hyderabad)
- **MAA-DEL** (Chennai – Delhi)

### B. Advance-Purchase Windows
As required by the economic index model:
- **T+1**: 1 day ahead (last-minute fare dynamics)
- **T+7**: 7 days ahead (short-term booking window)
- **T+15**: 15 days ahead (medium-term booking window)
- **T+30**: 30 days ahead (standard advance booking)
- **T+45**: 45 days ahead (early-bird benchmark)

### C. Carrier Coverage
- **IndiGo**
- **Air India**
- **Air India Express**
- **Akasa Air**
- **SpiceJet**

### D. Ethical Scraping & Anti-Bot Safeguards
- **Randomized Polite Jitter**: Sleeps 4.0 to 8.0 seconds between queries to avoid server stress.
- **Stealth Overrides**: Removes `navigator.webdriver` and injects realistic browser fingerprints.
- **Exponential Backoff**: Up to 3 automatic retries with exponential backoff on network failures.
- **Session Management**: Automatically recycles ChromeDriver instances upon unhandled errors.

---

## 3. How to Run

### 1. Test Mode (Quick verification: 1 Route x 2 Windows)
```powershell
.\.venv\Scripts\python.exe scheduler.py --test
```

### 2. Immediate Full Basket Run (All 6 Routes x 5 Windows = 30 Queries)
```powershell
.\.venv\Scripts\python.exe scheduler.py --now
```

### 3. Continuous Daily Scheduled Daemon (Default: Runs at 02:00 AM IST)
```powershell
.\.venv\Scripts\python.exe scheduler.py --daily-at 02:00
```

### 4. Periodic Interval Mode (e.g., Every 12 Hours or Every 30 Minutes)
```powershell
# Run every 12 hours
.\.venv\Scripts\python.exe scheduler.py --interval-hours 12

# Run every 30 minutes (for testing/demonstration)
.\.venv\Scripts\python.exe scheduler.py --interval-mins 30
```

### 5. Single Route Interactive Scraper
```powershell
# Headless run
.\.venv\Scripts\python.exe flight_scraper.py --origin DEL --destination BOM --date 2026-10-05

# Visible browser run (pops up Chrome on desktop)
.\.venv\Scripts\python.exe flight_scraper.py --origin DEL --destination BOM --date 2026-10-05 --visible
```

---

## 4. Database Schema (`data/airfare_warehouse.db`)

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Auto-increment primary key |
| `scrape_timestamp` | TEXT | ISO timestamp when the quote was extracted |
| `booking_date` | TEXT | Booking date (`YYYY-MM-DD`) |
| `travel_date` | TEXT | Departure date (`YYYY-MM-DD`) |
| `advance_window` | TEXT | Advance window (`T+1`, `T+7`, `T+15`, `T+30`, `T+45`) |
| `lead_time_days` | INTEGER | Days between booking and travel date (1, 7, 15, 30, 45) |
| `origin` | TEXT | 3-letter IATA code (`DEL`) |
| `destination` | TEXT | 3-letter IATA code (`BOM`) |
| `sector` | TEXT | Standard sector code (`DEL-BOM`) |
| `carrier` | TEXT | Airline (*IndiGo*, *Air India*, *Akasa Air*, etc.) |
| `departure_time` | TEXT | Departure time string (`5:00 AM`) |
| `arrival_time` | TEXT | Arrival time string (`7:20 AM`) |
| `duration_mins` | INTEGER | Flight duration in minutes (`140`) |
| `duration_str` | TEXT | Raw duration string (`2 hr 20 min`) |
| `stops` | TEXT | Stop description (`Nonstop`, `1 stop`) |
| `stops_count` | INTEGER | Stop count integer (`0`, `1`) |
| `fare_class` | TEXT | Fare tier (`Economy`) |
| `total_fare` | REAL | Total price in INR (`6314.0`) |
| `source_portal` | TEXT | Data extraction source |
