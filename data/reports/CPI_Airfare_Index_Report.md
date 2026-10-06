# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-06 10:38:20  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-06  
**Net Airfare Price Movement:** +5.21%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 57 | Rs. 9,398.70 | Rs. 9,380.00 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 57 | Rs. 9,117.77 | Rs. 9,120.49 | 97.01 | 96.92 | **97.13** | -2.87% |
| 2026-09-26 | 57 | Rs. 9,230.65 | Rs. 9,222.06 | 98.21 | 98.31 | **98.42** | -1.58% |
| 2026-09-27 | 57 | Rs. 11,464.88 | Rs. 11,509.65 | 121.98 | 117.41 | **118.00** | +18.00% |
| 2026-09-28 | 57 | Rs. 9,572.95 | Rs. 9,585.88 | 101.85 | 101.36 | **101.69** | +1.69% |
| 2026-10-01 | 57 | Rs. 9,466.84 | Rs. 9,480.20 | 100.72 | 100.49 | **100.87** | +0.87% |
| 2026-10-02 | 57 | Rs. 10,178.30 | Rs. 10,183.13 | 108.30 | 106.98 | **107.26** | +7.26% |
| 2026-10-03 | 57 | Rs. 11,915.60 | Rs. 11,950.84 | 126.78 | 122.51 | **123.13** | +23.13% |
| 2026-10-04 | 57 | Rs. 11,161.58 | Rs. 11,184.67 | 118.76 | 116.21 | **116.71** | +16.71% |
| 2026-10-05 | 57 | Rs. 10,207.47 | Rs. 10,232.37 | 108.60 | 106.90 | **107.43** | +7.43% |
| 2026-10-06 | 57 | Rs. 9,875.11 | Rs. 9,889.46 | 105.06 | 104.68 | **105.21** | +5.21% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
