# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-04 10:00:16  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-04  
**Net Airfare Price Movement:** +16.16%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 65 | Rs. 9,477.48 | Rs. 9,467.17 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 65 | Rs. 9,252.88 | Rs. 9,256.43 | 97.63 | 97.49 | **97.62** | -2.38% |
| 2026-09-26 | 65 | Rs. 9,537.62 | Rs. 9,449.06 | 100.64 | 100.01 | **99.55** | -0.45% |
| 2026-09-27 | 65 | Rs. 11,437.89 | Rs. 11,500.19 | 120.68 | 116.06 | **116.89** | +16.89% |
| 2026-09-28 | 65 | Rs. 9,570.51 | Rs. 9,589.21 | 100.98 | 100.61 | **101.08** | +1.08% |
| 2026-10-01 | 65 | Rs. 9,485.57 | Rs. 9,493.44 | 100.08 | 99.95 | **100.33** | +0.33% |
| 2026-10-02 | 65 | Rs. 10,173.35 | Rs. 10,173.10 | 107.33 | 106.26 | **106.55** | +6.55% |
| 2026-10-03 | 65 | Rs. 11,818.09 | Rs. 11,856.55 | 124.69 | 120.94 | **121.62** | +21.62% |
| 2026-10-04 | 65 | Rs. 11,214.63 | Rs. 11,247.11 | 118.32 | 115.56 | **116.16** | +16.16% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
