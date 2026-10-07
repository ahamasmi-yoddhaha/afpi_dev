# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-07 10:29:05  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-07  
**Net Airfare Price Movement:** +2.72%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 56 | Rs. 9,408.91 | Rs. 9,387.25 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 56 | Rs. 9,123.91 | Rs. 9,123.01 | 96.97 | 96.88 | **97.08** | -2.92% |
| 2026-09-26 | 56 | Rs. 9,234.86 | Rs. 9,223.31 | 98.15 | 98.25 | **98.35** | -1.65% |
| 2026-09-27 | 56 | Rs. 11,434.73 | Rs. 11,481.24 | 121.53 | 116.91 | **117.50** | +17.50% |
| 2026-09-28 | 56 | Rs. 9,582.52 | Rs. 9,597.83 | 101.84 | 101.34 | **101.72** | +1.72% |
| 2026-10-01 | 56 | Rs. 9,478.27 | Rs. 9,487.15 | 100.73 | 100.50 | **100.87** | +0.87% |
| 2026-10-02 | 56 | Rs. 10,200.55 | Rs. 10,208.42 | 108.41 | 107.09 | **107.41** | +7.41% |
| 2026-10-03 | 56 | Rs. 11,964.84 | Rs. 12,012.99 | 127.17 | 122.89 | **123.66** | +23.66% |
| 2026-10-04 | 56 | Rs. 11,169.43 | Rs. 11,201.36 | 118.71 | 116.13 | **116.74** | +16.74% |
| 2026-10-05 | 56 | Rs. 10,230.25 | Rs. 10,264.01 | 108.73 | 107.02 | **107.63** | +7.63% |
| 2026-10-06 | 56 | Rs. 9,891.95 | Rs. 9,899.74 | 105.13 | 104.76 | **105.25** | +5.25% |
| 2026-10-07 | 56 | Rs. 9,605.71 | Rs. 9,615.84 | 102.09 | 102.13 | **102.72** | +2.72% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
