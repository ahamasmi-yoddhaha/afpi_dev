# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-01 10:22:09  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-01  
**Net Airfare Price Movement:** +0.75%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 68 | Rs. 9,507.53 | Rs. 9,505.38 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 68 | Rs. 9,248.97 | Rs. 9,263.15 | 97.28 | 97.15 | **97.30** | -2.70% |
| 2026-09-26 | 68 | Rs. 9,502.07 | Rs. 9,432.58 | 99.95 | 99.37 | **98.99** | -1.01% |
| 2026-09-27 | 68 | Rs. 11,567.68 | Rs. 11,623.35 | 121.67 | 116.71 | **117.49** | +17.49% |
| 2026-09-28 | 68 | Rs. 9,552.74 | Rs. 9,571.84 | 100.48 | 100.13 | **100.58** | +0.58% |
| 2026-09-29 | 68 | Rs. 9,323.21 | Rs. 9,334.51 | 98.07 | 98.04 | **98.41** | -1.59% |
| 2026-09-30 | 68 | Rs. 9,695.94 | Rs. 9,709.17 | 101.99 | 101.23 | **101.71** | +1.71% |
| 2026-10-01 | 68 | Rs. 9,581.16 | Rs. 9,585.40 | 100.79 | 100.37 | **100.75** | +0.75% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
