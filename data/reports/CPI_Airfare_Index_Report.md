# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-11 10:13:59  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-11  
**Net Airfare Price Movement:** +26.88%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 12 | Rs. 9,417.33 | Rs. 9,323.64 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 12 | Rs. 8,911.75 | Rs. 8,867.96 | 94.63 | 94.89 | **95.36** | -4.64% |
| 2026-09-26 | 12 | Rs. 9,135.50 | Rs. 9,159.29 | 97.01 | 97.21 | **98.38** | -1.62% |
| 2026-09-27 | 12 | Rs. 11,287.83 | Rs. 11,497.71 | 119.86 | 115.28 | **117.66** | +17.66% |
| 2026-09-28 | 12 | Rs. 9,334.17 | Rs. 9,347.64 | 99.11 | 99.37 | **100.48** | +0.48% |
| 2026-10-01 | 12 | Rs. 8,921.25 | Rs. 8,940.39 | 94.73 | 95.02 | **96.16** | -3.84% |
| 2026-10-02 | 12 | Rs. 9,432.92 | Rs. 9,390.32 | 100.17 | 99.98 | **100.42** | +0.42% |
| 2026-10-03 | 12 | Rs. 12,795.58 | Rs. 13,276.82 | 135.88 | 129.23 | **134.77** | +34.77% |
| 2026-10-04 | 12 | Rs. 12,234.33 | Rs. 12,682.71 | 129.91 | 125.81 | **131.33** | +31.33% |
| 2026-10-05 | 12 | Rs. 10,397.33 | Rs. 10,675.93 | 110.40 | 106.52 | **109.74** | +9.74% |
| 2026-10-06 | 12 | Rs. 9,116.33 | Rs. 9,079.14 | 96.80 | 97.11 | **98.01** | -1.99% |
| 2026-10-07 | 12 | Rs. 9,478.67 | Rs. 9,476.64 | 100.64 | 100.99 | **102.30** | +2.30% |
| 2026-10-08 | 12 | Rs. 9,702.00 | Rs. 9,746.86 | 103.02 | 102.88 | **104.63** | +4.63% |
| 2026-10-09 | 12 | Rs. 10,293.75 | Rs. 10,241.32 | 109.30 | 108.37 | **109.21** | +9.21% |
| 2026-10-10 | 12 | Rs. 11,434.83 | Rs. 11,531.00 | 121.42 | 119.44 | **121.69** | +21.69% |
| 2026-10-11 | 12 | Rs. 11,817.50 | Rs. 12,219.29 | 125.49 | 121.55 | **126.88** | +26.88% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
