# Real-Time Airfare Price Index: DEL → HYD (CPI Augmentation)

A specialized empirical research framework that collects, aggregates, and calculates real-time domestic airfare price indices for the high-density trunk route **Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)** across advance booking lead times ($t+1, t+7, t+15, t+30$) to augment official Consumer Price Index (CPI) metrics.

---

## Systematic Workflow Architecture

```
┌────────────────────────────────────────────────────────┐
│  Automated Daily Scheduler (09:00 AM IST)              │
│  scheduler.py  /  run_daily.bat                        │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  Step 1: Real-Time Web Scraper (run_scraper.py)        │
│  - Scrapes DEL -> HYD on Google Flights                │
│  - Captures t+1, t+7, t+15, t+30 advance horizons      │
│  - Saves data/raw_json/ and data/processed_csv/        │
│  - Appends to cumulative data/master_flight_prices.csv │
└───────────────────────────┬────────────────────────────┘
                            │ (Auto-Chained)
                            ▼
┌────────────────────────────────────────────────────────┐
│  Step 2: Data Cleaning & Decomposition Pipeline        │
│  - Multi-scrape exact & near de-duplication            │
│  - Statistical outlier detection (Tukey's IQR)         │
│  - Inventory attrition & sold-out flights tracking     │
│  - Statutory fare decomposition: Base, GST, UDF, Fees  │
│  - Produces data/cleaned_flight_prices.csv             │
│  - Produces data/reports/Data_Cleaning_Audit_Report.md │
└───────────────────────────┬────────────────────────────┘
                            │ (Auto-Chained)
                            ▼
┌────────────────────────────────────────────────────────┐
│  Step 3: Economic Index Engine (calculate_index.py)    │
│  - Computes UN/IMF Jevons, Dutot, DGCA Weighted Indices│
│  - Enforces Balanced Panel (constant-quality basket)   │
│  - Generates publication charts (data/plots/*.png)     │
│  - Generates Academic Report (data/reports/*.md)       │
│  - Exports fresh data/dashboard_data.js & .json        │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  Step 4: Interactive Dashboard (dashboard.html)        │
│  - Focused Light-Theme UI for DEL -> HYD corridor      │
│  - 3 Core KPIs: Latest CPI, Average Fare, Panel Cohort │
│  - Airline carrier tariff comparison (all 5 carriers)  │
│  - Inter-temporal CPI price trend with line hover      │
└────────────────────────────────────────────────────────┘
```

---

## 1. Running the Scraper Manually

To execute an immediate scrape of DEL &rarr; HYD flights and automatically sync the dashboard:

```powershell
python run_scraper.py
```
*(Runs in headless browser mode by default. To watch the browser live during debugging, add `--no-headless`).*

---

## 2. Automated Daily Scheduler

The scheduler is scheduled for **09:00 AM IST daily**. It runs the scraper across all horizons and automatically chains `calculate_index.py` to refresh the dashboard immediately upon completion.

### Method A: Terminal Background Scheduler
```powershell
python scheduler.py --days 7 --time 09:00
```
*(Will execute an immediate run upon launch, then wait for 09:00 AM every subsequent day).*

### Method B: Windows Task Scheduler (Recommended for background runs)
Open PowerShell in this project folder and run:
```powershell
$batchPath = (Get-Item ".\run_daily.bat").FullName
schtasks /create /tn "AirfareDailyScraper" /tr "`"$batchPath`"" /sc daily /st 09:00 /f
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Set-ScheduledTask -TaskName "AirfareDailyScraper" -Settings $settings
```

---

## 3. Opening the Interactive Dashboard

To open the dashboard in your default web browser:
```powershell
python open_dashboard.py
```
*(Automatically verifies whether fresh flights have been collected since the last calculation and auto-syncs before opening).*

To force recalculation and open:
```powershell
python open_dashboard.py --sync
```

---

## 4. Manual Index & Report Generation

If you only want to re-run the statistical engine and generate updated charts without scraping:

```powershell
python calculate_index.py
```

### Outputs Produced:
1. **Interactive Frontend Feed**:
   - `data/dashboard_data.js` (zero-CORS local viewing)
   - `data/dashboard_data.json`
2. **High-Resolution Publication Plots** (in `data/plots/`):
   - `daily_cpi_airfare_trend.png` (Inter-temporal Dutot, Jevons, DGCA Weighted)
   - `carrier_price_comparison.png` (Airline breakdown)
3. **Academic Research Report**:
   - `data/reports/CPI_Airfare_Index_Report.md`
4. **Summary Tables**:
   - `data/reports/cpi_daily_index_summary.csv`
