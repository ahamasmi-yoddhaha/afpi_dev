# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-02 09:58:54  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-02  
**Net Airfare Price Movement:** +6.97%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 66 | Rs. 9,513.76 | Rs. 9,507.57 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 66 | Rs. 9,264.32 | Rs. 9,271.87 | 97.38 | 97.25 | **97.37** | -2.63% |
| 2026-09-26 | 66 | Rs. 9,525.09 | Rs. 9,442.67 | 100.12 | 99.54 | **99.07** | -0.93% |
| 2026-09-27 | 66 | Rs. 11,403.98 | Rs. 11,465.99 | 119.87 | 115.39 | **116.17** | +16.17% |
| 2026-09-28 | 66 | Rs. 9,576.89 | Rs. 9,595.47 | 100.67 | 100.32 | **100.75** | +0.75% |
| 2026-09-29 | 66 | Rs. 9,340.00 | Rs. 9,342.07 | 98.18 | 98.15 | **98.44** | -1.56% |
| 2026-09-30 | 66 | Rs. 9,724.03 | Rs. 9,746.78 | 102.22 | 101.45 | **102.01** | +2.01% |
| 2026-10-01 | 66 | Rs. 9,605.77 | Rs. 9,609.74 | 100.97 | 100.56 | **100.95** | +0.95% |
| 2026-10-02 | 66 | Rs. 10,249.45 | Rs. 10,249.69 | 107.73 | 106.61 | **106.97** | +6.97% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
