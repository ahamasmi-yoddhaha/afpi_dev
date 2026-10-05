# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-05 10:44:52  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-05  
**Net Airfare Price Movement:** +6.81%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 64 | Rs. 9,479.47 | Rs. 9,470.48 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 64 | Rs. 9,258.80 | Rs. 9,264.70 | 97.67 | 97.54 | **97.67** | -2.33% |
| 2026-09-26 | 64 | Rs. 9,547.98 | Rs. 9,458.56 | 100.72 | 100.12 | **99.62** | -0.38% |
| 2026-09-27 | 64 | Rs. 11,262.30 | Rs. 11,318.14 | 118.80 | 114.75 | **115.49** | +15.49% |
| 2026-09-28 | 64 | Rs. 9,561.84 | Rs. 9,580.90 | 100.86 | 100.51 | **100.94** | +0.94% |
| 2026-10-01 | 64 | Rs. 9,495.12 | Rs. 9,505.62 | 100.15 | 100.05 | **100.42** | +0.42% |
| 2026-10-02 | 64 | Rs. 10,193.66 | Rs. 10,193.89 | 107.52 | 106.47 | **106.72** | +6.72% |
| 2026-10-03 | 64 | Rs. 11,764.61 | Rs. 11,799.53 | 124.09 | 120.40 | **120.99** | +20.99% |
| 2026-10-04 | 64 | Rs. 11,035.55 | Rs. 11,058.23 | 116.40 | 114.25 | **114.72** | +14.72% |
| 2026-10-05 | 64 | Rs. 10,217.44 | Rs. 10,233.14 | 107.77 | 106.39 | **106.81** | +6.81% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
