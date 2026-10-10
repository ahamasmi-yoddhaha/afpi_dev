# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-10 10:03:48  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-10  
**Net Airfare Price Movement:** +22.62%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 13 | Rs. 9,447.46 | Rs. 9,376.56 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 13 | Rs. 8,901.15 | Rs. 8,862.14 | 94.22 | 94.46 | **94.75** | -5.25% |
| 2026-09-26 | 13 | Rs. 9,107.69 | Rs. 9,120.89 | 96.41 | 96.59 | **97.41** | -2.59% |
| 2026-09-27 | 13 | Rs. 11,277.46 | Rs. 11,449.89 | 119.37 | 115.15 | **117.11** | +17.11% |
| 2026-09-28 | 13 | Rs. 9,293.12 | Rs. 9,294.57 | 98.36 | 98.58 | **99.33** | -0.67% |
| 2026-10-01 | 13 | Rs. 8,950.31 | Rs. 8,973.18 | 94.73 | 94.99 | **95.96** | -4.04% |
| 2026-10-02 | 13 | Rs. 9,799.85 | Rs. 9,851.71 | 103.72 | 102.87 | **103.96** | +3.96% |
| 2026-10-03 | 13 | Rs. 12,659.54 | Rs. 13,028.18 | 133.99 | 127.84 | **131.98** | +31.98% |
| 2026-10-04 | 13 | Rs. 11,997.69 | Rs. 12,315.00 | 126.98 | 122.95 | **126.66** | +26.66% |
| 2026-10-05 | 13 | Rs. 10,401.31 | Rs. 10,634.42 | 110.08 | 106.52 | **109.10** | +9.10% |
| 2026-10-06 | 13 | Rs. 9,177.69 | Rs. 9,161.31 | 97.13 | 97.41 | **98.15** | -1.85% |
| 2026-10-07 | 13 | Rs. 9,644.15 | Rs. 9,681.87 | 102.07 | 102.24 | **103.57** | +3.57% |
| 2026-10-08 | 13 | Rs. 9,759.46 | Rs. 9,810.52 | 103.29 | 103.15 | **104.59** | +4.59% |
| 2026-10-09 | 13 | Rs. 10,807.38 | Rs. 10,885.99 | 114.39 | 112.34 | **113.92** | +13.92% |
| 2026-10-10 | 13 | Rs. 11,576.77 | Rs. 11,690.70 | 122.53 | 120.60 | **122.62** | +22.62% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
