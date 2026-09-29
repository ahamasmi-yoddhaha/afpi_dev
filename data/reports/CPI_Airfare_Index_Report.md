# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-09-28 16:57:07  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-09-28  
**Net Airfare Price Movement:** +0.43%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 78 | Rs. 9,531.74 | Rs. 9,535.80 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 78 | Rs. 9,224.81 | Rs. 9,266.36 | 96.78 | 96.75 | **97.08** | -2.92% |
| 2026-09-26 | 78 | Rs. 9,436.58 | Rs. 9,425.10 | 99.01 | 98.58 | **98.66** | -1.34% |
| 2026-09-27 | 78 | Rs. 11,371.04 | Rs. 11,452.53 | 119.30 | 114.79 | **115.80** | +15.80% |
| 2026-09-28 | 78 | Rs. 9,558.72 | Rs. 9,578.87 | 100.29 | 100.04 | **100.43** | +0.43% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
