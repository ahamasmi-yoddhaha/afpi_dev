# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-03 09:21:41  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-03  
**Net Airfare Price Movement:** +20.64%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 67 | Rs. 9,503.51 | Rs. 9,499.49 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 67 | Rs. 9,260.30 | Rs. 9,270.97 | 97.44 | 97.31 | **97.45** | -2.55% |
| 2026-09-26 | 67 | Rs. 9,517.18 | Rs. 9,441.06 | 100.14 | 99.56 | **99.16** | -0.84% |
| 2026-09-27 | 67 | Rs. 11,415.43 | Rs. 11,478.57 | 120.12 | 115.64 | **116.45** | +16.45% |
| 2026-09-28 | 67 | Rs. 9,546.19 | Rs. 9,565.02 | 100.45 | 100.09 | **100.53** | +0.53% |
| 2026-10-01 | 67 | Rs. 9,478.84 | Rs. 9,493.63 | 99.74 | 99.62 | **100.02** | +0.02% |
| 2026-10-02 | 67 | Rs. 10,155.64 | Rs. 10,153.30 | 106.86 | 105.82 | **106.06** | +6.06% |
| 2026-10-03 | 67 | Rs. 11,764.21 | Rs. 11,793.84 | 123.79 | 120.11 | **120.64** | +20.64% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
