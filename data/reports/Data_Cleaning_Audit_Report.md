# Airfare Database Data Cleaning & Standardisation Audit Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Observation Dates:** 2026-09-24, 2026-09-25, 2026-09-26, 2026-09-27, 2026-09-28, 2026-10-01, 2026-10-02, 2026-10-03, 2026-10-04, 2026-10-05, 2026-10-06, 2026-10-07, 2026-10-08, 2026-10-09  
**Pipeline Execution:** Completed Successfully  

---

### 1. Ingestion, Filtering & De-duplication Summary

| Metric | Count | Percentage |
| :--- | :--- | :--- |
| **Raw Scraped Observations** | **1,924** | 100.0% |
| **Invalid / Missing Values Handled** | 0 | 0.0% |
| **Duplicate Scrapes Removed** | 528 | 27.4% |
| **Cleaned & De-duplicated Records** | **1,396** | **72.6%** |
| **Statistical Outliers Flagged** | 92 | 6.6% |
| **Strictly Balanced Panel Flights (All Dates)** | **18 per date** | — |

---

### 2. Statutory Domestic Fare Decomposition (DGCA & MoCA Framework)

In accordance with Indian Ministry of Civil Aviation (MoCA) and DGCA tariff guidelines, gross airfares are decomposed into:
1. **Base Airfare**: The core airline ticket tariff subject to dynamic yield management.
2. **Goods & Services Tax (GST)**: Statutory 5% GST levied on domestic economy tickets under the CGST Act.
3. **Airport User Development Fee (UDF) & Aviation Security Fee (ASF)**: Statutory fee (Rs. 450.00).
4. **Convenience Charges**: Standard digital web booking platform charges (Rs. 350.00).

| Component | Average Value (INR) | Share of Total Airfare |
| :--- | :--- | :--- |
| **Base Fare** | **Rs. 8,916.10** | **87.7%** |
| **Taxes (GST 5%)** | Rs. 445.81 | 4.4% |
| **Airport UDF & ASF Fee** | Rs. 450.00 | 4.4% |
| **Convenience / Web Fee** | Rs. 350.00 | 3.4% |
| **Total Gross Airfare** | **Rs. 10,161.91** | **100.0%** |

---

### 3. Inventory Attrition & Sold-Out Analysis

The table below tracks flight service attrition (depleted seats / cancelled flights) across consecutive scraping dates:

| Transition Period | Active Flights Day $t$ | Sold Out / Cancelled by Day $t+1$ | New Flights Added Day $t+1$ | Common Retained |
| :--- | :---: | :---: | :---: | :---: |
| 2026-09-24 &rarr; 2026-09-25 | 114 | 24 | 25 | 90 |
| 2026-09-25 &rarr; 2026-09-26 | 115 | 8 | 11 | 107 |
| 2026-09-26 &rarr; 2026-09-27 | 118 | 9 | 13 | 109 |
| 2026-09-27 &rarr; 2026-09-28 | 122 | 15 | 15 | 107 |
| 2026-09-28 &rarr; 2026-10-01 | 122 | 25 | 4 | 97 |
| 2026-10-01 &rarr; 2026-10-02 | 101 | 5 | 2 | 96 |
| 2026-10-02 &rarr; 2026-10-03 | 98 | 2 | 3 | 96 |
| 2026-10-03 &rarr; 2026-10-04 | 99 | 3 | 5 | 96 |
| 2026-10-04 &rarr; 2026-10-05 | 101 | 4 | 3 | 97 |
| 2026-10-05 &rarr; 2026-10-06 | 100 | 9 | 9 | 91 |
| 2026-10-06 &rarr; 2026-10-07 | 100 | 6 | 7 | 94 |
| 2026-10-07 &rarr; 2026-10-08 | 101 | 56 | 8 | 45 |
| 2026-10-08 &rarr; 2026-10-09 | 53 | 6 | 5 | 47 |

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
