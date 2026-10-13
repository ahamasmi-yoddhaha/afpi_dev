# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-13 10:54:02  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-13  
**Net Airfare Price Movement:** -1.74%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 5 | Rs. 9,864.00 | Rs. 9,684.43 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 5 | Rs. 9,007.40 | Rs. 8,975.64 | 91.32 | 91.69 | **93.12** | -6.88% |
| 2026-09-26 | 5 | Rs. 9,071.80 | Rs. 9,213.57 | 91.97 | 92.29 | **95.43** | -4.57% |
| 2026-09-27 | 5 | Rs. 11,839.00 | Rs. 11,676.57 | 120.02 | 119.37 | **119.53** | +19.53% |
| 2026-09-28 | 5 | Rs. 9,572.50 | Rs. 9,780.04 | 97.05 | 97.48 | **101.73** | +1.73% |
| 2026-10-01 | 5 | Rs. 8,859.80 | Rs. 8,876.86 | 89.82 | 90.29 | **92.42** | -7.58% |
| 2026-10-02 | 5 | Rs. 10,095.40 | Rs. 10,151.71 | 102.35 | 102.06 | **104.48** | +4.48% |
| 2026-10-03 | 5 | Rs. 9,054.80 | Rs. 8,992.57 | 91.79 | 92.30 | **93.64** | -6.36% |
| 2026-10-04 | 5 | Rs. 10,031.20 | Rs. 10,169.29 | 101.69 | 101.92 | **105.52** | +5.52% |
| 2026-10-05 | 5 | Rs. 9,580.20 | Rs. 9,552.64 | 97.11 | 97.43 | **99.31** | -0.69% |
| 2026-10-06 | 5 | Rs. 9,291.20 | Rs. 9,225.50 | 94.18 | 94.72 | **96.13** | -3.87% |
| 2026-10-07 | 5 | Rs. 9,517.40 | Rs. 9,513.29 | 96.47 | 97.04 | **99.14** | -0.86% |
| 2026-10-08 | 5 | Rs. 10,102.00 | Rs. 10,416.36 | 102.39 | 102.07 | **107.44** | +7.44% |
| 2026-10-09 | 5 | Rs. 11,636.60 | Rs. 11,697.29 | 117.95 | 116.91 | **120.07** | +20.07% |
| 2026-10-10 | 5 | Rs. 13,502.00 | Rs. 13,957.57 | 136.85 | 135.19 | **142.38** | +42.38% |
| 2026-10-11 | 5 | Rs. 12,061.00 | Rs. 12,267.57 | 122.25 | 121.89 | **126.73** | +26.73% |
| 2026-10-13 | 5 | Rs. 9,427.00 | Rs. 9,409.64 | 95.55 | 96.08 | **98.26** | -1.74% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
