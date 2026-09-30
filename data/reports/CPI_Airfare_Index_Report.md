# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-09-30 09:55:21  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-09-30  
**Net Airfare Price Movement:** +1.55%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 70 | Rs. 9,509.76 | Rs. 9,510.76 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 70 | Rs. 9,249.43 | Rs. 9,269.20 | 97.26 | 97.14 | **97.31** | -2.69% |
| 2026-09-26 | 70 | Rs. 9,496.66 | Rs. 9,438.72 | 99.86 | 99.31 | **99.00** | -1.00% |
| 2026-09-27 | 70 | Rs. 11,494.61 | Rs. 11,551.32 | 120.87 | 116.00 | **116.76** | +16.76% |
| 2026-09-28 | 70 | Rs. 9,541.38 | Rs. 9,562.46 | 100.33 | 99.99 | **100.42** | +0.42% |
| 2026-09-29 | 70 | Rs. 9,309.03 | Rs. 9,329.73 | 97.88 | 97.86 | **98.28** | -1.72% |
| 2026-09-30 | 70 | Rs. 9,691.14 | Rs. 9,697.38 | 101.90 | 101.17 | **101.55** | +1.55% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
