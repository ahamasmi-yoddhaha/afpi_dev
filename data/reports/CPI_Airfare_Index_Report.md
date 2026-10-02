# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-02 13:25:14  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-02  
**Net Airfare Price Movement:** +6.64%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 68 | Rs. 9,493.56 | Rs. 9,492.17 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 68 | Rs. 9,253.15 | Rs. 9,267.09 | 97.47 | 97.34 | **97.48** | -2.52% |
| 2026-09-26 | 68 | Rs. 9,509.50 | Rs. 9,439.60 | 100.17 | 99.59 | **99.21** | -0.79% |
| 2026-09-27 | 68 | Rs. 11,391.03 | Rs. 11,456.38 | 119.99 | 115.55 | **116.36** | +16.36% |
| 2026-09-28 | 68 | Rs. 9,557.54 | Rs. 9,576.37 | 100.67 | 100.32 | **100.73** | +0.73% |
| 2026-10-01 | 68 | Rs. 9,584.37 | Rs. 9,596.49 | 100.96 | 100.56 | **100.90** | +0.90% |
| 2026-10-02 | 68 | Rs. 10,215.16 | Rs. 10,209.08 | 107.60 | 106.48 | **106.64** | +6.64% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
