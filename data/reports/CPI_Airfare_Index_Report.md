# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-08 10:49:57  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-08  
**Net Airfare Price Movement:** +5.19%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 19 | Rs. 9,413.37 | Rs. 9,343.75 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 19 | Rs. 8,961.63 | Rs. 8,945.51 | 95.20 | 95.40 | **95.93** | -4.07% |
| 2026-09-26 | 19 | Rs. 9,180.00 | Rs. 9,138.30 | 97.52 | 97.60 | **97.90** | -2.10% |
| 2026-09-27 | 19 | Rs. 11,436.95 | Rs. 11,603.67 | 121.50 | 115.96 | **117.94** | +17.94% |
| 2026-09-28 | 19 | Rs. 9,632.47 | Rs. 9,691.72 | 102.33 | 101.49 | **102.77** | +2.77% |
| 2026-10-01 | 19 | Rs. 9,222.42 | Rs. 9,232.02 | 97.97 | 98.06 | **98.97** | -1.03% |
| 2026-10-02 | 19 | Rs. 10,335.89 | Rs. 10,380.25 | 109.80 | 107.73 | **108.77** | +8.77% |
| 2026-10-03 | 19 | Rs. 12,189.37 | Rs. 12,370.07 | 129.48 | 124.98 | **127.49** | +27.49% |
| 2026-10-04 | 19 | Rs. 11,432.05 | Rs. 11,565.91 | 121.44 | 118.54 | **120.57** | +20.57% |
| 2026-10-05 | 19 | Rs. 10,488.21 | Rs. 10,630.29 | 111.41 | 108.62 | **110.62** | +10.62% |
| 2026-10-06 | 19 | Rs. 9,546.05 | Rs. 9,545.02 | 101.41 | 101.31 | **102.17** | +2.17% |
| 2026-10-07 | 19 | Rs. 9,688.63 | Rs. 9,731.09 | 102.92 | 103.03 | **104.39** | +4.39% |
| 2026-10-08 | 19 | Rs. 9,796.89 | Rs. 9,821.86 | 104.07 | 104.02 | **105.19** | +5.19% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
