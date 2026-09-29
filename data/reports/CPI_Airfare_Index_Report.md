# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-09-29 09:29:05  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-09-29  
**Net Airfare Price Movement:** -2.13%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 73 | Rs. 9,546.56 | Rs. 9,544.90 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 73 | Rs. 9,227.18 | Rs. 9,257.78 | 96.65 | 96.61 | **96.90** | -3.10% |
| 2026-09-26 | 73 | Rs. 9,468.63 | Rs. 9,429.39 | 99.18 | 98.73 | **98.62** | -1.38% |
| 2026-09-27 | 73 | Rs. 11,440.08 | Rs. 11,503.04 | 119.83 | 115.17 | **116.04** | +16.04% |
| 2026-09-28 | 73 | Rs. 9,520.33 | Rs. 9,546.85 | 99.72 | 99.49 | **99.98** | -0.02% |
| 2026-09-29 | 73 | Rs. 9,282.33 | Rs. 9,318.92 | 97.23 | 97.30 | **97.87** | -2.13% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
