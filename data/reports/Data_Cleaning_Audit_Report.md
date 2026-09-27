# Airfare Database Data Cleaning & Standardisation Audit Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Observation Dates:** 2026-09-24, 2026-09-25, 2026-09-26, 2026-09-27  
**Pipeline Execution:** Completed Successfully  

---

### 1. Ingestion, Filtering & De-duplication Summary

| Metric | Count | Percentage |
| :--- | :--- | :--- |
| **Raw Scraped Observations** | **893** | 100.0% |
| **Invalid / Missing Values Handled** | 0 | 0.0% |
| **Duplicate Scrapes Removed** | 424 | 47.5% |
| **Cleaned & De-duplicated Records** | **469** | **52.5%** |
| **Statistical Outliers Flagged** | 35 | 7.5% |
| **Strictly Balanced Panel Flights (All Dates)** | **82 per date** | — |

---

### 2. Statutory Domestic Fare Decomposition (DGCA & MoCA Framework)

In accordance with Indian Ministry of Civil Aviation (MoCA) and DGCA tariff guidelines, gross airfares are decomposed into:
1. **Base Airfare**: The core airline ticket tariff subject to dynamic yield management.
2. **Goods & Services Tax (GST)**: Statutory 5% GST levied on domestic economy tickets under the CGST Act.
3. **Airport User Development Fee (UDF) & Aviation Security Fee (ASF)**: Statutory fee (Rs. 450.00).
4. **Convenience Charges**: Standard digital web booking platform charges (Rs. 350.00).

| Component | Average Value (INR) | Share of Total Airfare |
| :--- | :--- | :--- |
| **Base Fare** | **Rs. 8,577.27** | **87.5%** |
| **Taxes (GST 5%)** | Rs. 428.86 | 4.4% |
| **Airport UDF & ASF Fee** | Rs. 450.00 | 4.6% |
| **Convenience / Web Fee** | Rs. 350.00 | 3.6% |
| **Total Gross Airfare** | **Rs. 9,806.13** | **100.0%** |

---

### 3. Inventory Attrition & Sold-Out Analysis

The table below tracks flight service attrition (depleted seats / cancelled flights) across consecutive scraping dates:

| Transition Period | Active Flights Day $t$ | Sold Out / Cancelled by Day $t+1$ | New Flights Added Day $t+1$ | Common Retained |
| :--- | :---: | :---: | :---: | :---: |
| 2026-09-24 &rarr; 2026-09-25 | 114 | 24 | 25 | 90 |
| 2026-09-25 &rarr; 2026-09-26 | 115 | 8 | 11 | 107 |
| 2026-09-26 &rarr; 2026-09-27 | 118 | 9 | 13 | 109 |

---

### 4. Cleaned Dataset Sample (DEL &rarr; HYD)

| Flight ID | Date | Horizon | Carrier | Base Fare (INR) | Taxes (INR) | Fees (INR) | Total (INR) | Status |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| `DEL -> HYD|Air India|t+1|10:...` | 2026-09-24 | t+1 | Air India | Rs. 7,534 | Rs. 377 | Rs. 800 | **Rs. 8,711** | ACTIVE |
| `DEL -> HYD|Air India|t+1|10:...` | 2026-09-24 | t+1 | Air India | Rs. 7,645 | Rs. 382 | Rs. 800 | **Rs. 8,827** | ACTIVE |
| `DEL -> HYD|Air India|t+1|11:...` | 2026-09-24 | t+1 | Air India | Rs. 7,534 | Rs. 377 | Rs. 800 | **Rs. 8,711** | ACTIVE |
| `DEL -> HYD|Air India|t+1|12:...` | 2026-09-24 | t+1 | Air India | Rs. 7,645 | Rs. 382 | Rs. 800 | **Rs. 8,827** | ACTIVE |
| `DEL -> HYD|Air India|t+1|2:0...` | 2026-09-24 | t+1 | Air India | Rs. 7,534 | Rs. 377 | Rs. 800 | **Rs. 8,711** | ACTIVE |
| `DEL -> HYD|Air India|t+1|2:3...` | 2026-09-24 | t+1 | Air India | Rs. 8,394 | Rs. 420 | Rs. 800 | **Rs. 9,614** | ACTIVE |
| `DEL -> HYD|Air India|t+1|6:0...` | 2026-09-24 | t+1 | Air India | Rs. 11,705 | Rs. 585 | Rs. 800 | **Rs. 13,090** | ACTIVE |
| `DEL -> HYD|Air India|t+1|6:0...` | 2026-09-24 | t+1 | Air India | Rs. 8,090 | Rs. 404 | Rs. 800 | **Rs. 9,294** | ACTIVE |
| `DEL -> HYD|Air India|t+1|7:3...` | 2026-09-24 | t+1 | Air India | Rs. 8,094 | Rs. 405 | Rs. 800 | **Rs. 9,299** | ACTIVE |
| `DEL -> HYD|Air India|t+1|8:3...` | 2026-09-24 | t+1 | Air India | Rs. 7,645 | Rs. 382 | Rs. 800 | **Rs. 8,827** | ACTIVE |

> **Output Path:** `data/cleaned_flight_prices.csv`
