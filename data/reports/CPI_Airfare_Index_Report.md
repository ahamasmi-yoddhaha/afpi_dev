# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-09 10:48:36  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-09  
**Net Airfare Price Movement:** +15.70%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 18 | Rs. 9,368.06 | Rs. 9,279.93 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 18 | Rs. 8,917.50 | Rs. 8,890.80 | 95.19 | 95.40 | **96.01** | -3.99% |
| 2026-09-26 | 18 | Rs. 9,202.56 | Rs. 9,159.06 | 98.24 | 98.30 | **98.78** | -1.22% |
| 2026-09-27 | 18 | Rs. 10,767.33 | Rs. 10,833.00 | 114.94 | 111.64 | **112.94** | +12.94% |
| 2026-09-28 | 18 | Rs. 9,242.33 | Rs. 9,237.24 | 98.66 | 98.86 | **99.73** | -0.27% |
| 2026-10-01 | 18 | Rs. 9,224.00 | Rs. 9,235.28 | 98.46 | 98.53 | **99.60** | -0.40% |
| 2026-10-02 | 18 | Rs. 10,413.89 | Rs. 10,479.22 | 111.17 | 108.98 | **110.37** | +10.37% |
| 2026-10-03 | 18 | Rs. 12,370.33 | Rs. 12,610.90 | 132.05 | 127.48 | **130.85** | +30.85% |
| 2026-10-04 | 18 | Rs. 11,522.56 | Rs. 11,692.62 | 123.01 | 119.93 | **122.51** | +22.51% |
| 2026-10-05 | 18 | Rs. 10,520.11 | Rs. 10,688.64 | 112.31 | 109.29 | **111.69** | +11.69% |
| 2026-10-06 | 18 | Rs. 9,580.17 | Rs. 9,585.35 | 102.28 | 102.14 | **103.24** | +3.24% |
| 2026-10-07 | 18 | Rs. 9,704.44 | Rs. 9,755.98 | 103.61 | 103.68 | **105.31** | +5.31% |
| 2026-10-08 | 18 | Rs. 9,805.56 | Rs. 9,835.74 | 104.68 | 104.59 | **105.99** | +5.99% |
| 2026-10-09 | 18 | Rs. 10,851.33 | Rs. 10,895.56 | 115.85 | 114.20 | **115.70** | +15.70% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
