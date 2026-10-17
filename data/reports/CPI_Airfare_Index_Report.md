# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** 2026-10-17 07:58:27  
**Base Observation Date ($t_0$):** 2026-09-24  
**Latest Observation Date ($t$):** 2026-10-17  
**Net Airfare Price Movement:** -5.31%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | 114 | Rs. 9,499.74 | Rs. 9,466.31 | 100.00 | 100.00 | **100.00** | +0.00% |
| 2026-09-25 | 115 | Rs. 9,417.41 | Rs. 9,399.27 | 96.82 | 96.80 | **97.05** | -2.95% |
| 2026-09-26 | 118 | Rs. 9,518.02 | Rs. 9,511.16 | 98.38 | 97.90 | **98.18** | -1.82% |
| 2026-09-27 | 122 | Rs. 10,737.52 | Rs. 10,683.14 | 112.51 | 108.89 | **109.03** | +9.03% |
| 2026-09-28 | 122 | Rs. 9,544.30 | Rs. 9,476.88 | 98.79 | 98.44 | **98.13** | -1.87% |
| 2026-10-01 | 101 | Rs. 9,671.68 | Rs. 9,644.96 | 96.76 | 96.97 | **96.94** | -3.06% |
| 2026-10-02 | 98 | Rs. 10,298.14 | Rs. 10,238.21 | 104.20 | 103.70 | **103.14** | +3.14% |
| 2026-10-03 | 99 | Rs. 11,585.56 | Rs. 11,589.50 | 117.13 | 114.58 | **114.51** | +14.51% |
| 2026-10-04 | 101 | Rs. 11,067.74 | Rs. 11,107.31 | 111.99 | 110.26 | **110.41** | +10.41% |
| 2026-10-05 | 100 | Rs. 10,173.53 | Rs. 10,142.59 | 103.96 | 103.39 | **103.24** | +3.24% |
| 2026-10-06 | 100 | Rs. 10,275.69 | Rs. 10,305.13 | 103.60 | 103.28 | **103.47** | +3.47% |
| 2026-10-07 | 101 | Rs. 10,145.12 | Rs. 10,040.45 | 102.09 | 101.98 | **101.37** | +1.37% |
| 2026-10-08 | 53 | Rs. 10,237.34 | Rs. 11,470.33 | 96.49 | 98.05 | **97.22** | -2.78% |
| 2026-10-09 | 52 | Rs. 10,759.94 | Rs. 11,388.61 | 101.75 | 102.82 | **98.99** | -1.01% |
| 2026-10-10 | 59 | Rs. 12,296.44 | Rs. 12,329.55 | 115.61 | 116.74 | **103.94** | +3.94% |
| 2026-10-11 | 53 | Rs. 11,938.60 | Rs. 11,763.03 | 112.26 | 112.53 | **100.02** | +0.02% |
| 2026-10-13 | 26 | Rs. 11,050.54 | Rs. 12,444.89 | 100.16 | 99.62 | **93.76** | -6.24% |
| 2026-10-14 | 27 | Rs. 9,618.89 | Rs. 10,558.13 | 100.16 | 99.62 | **93.76** | -6.24% |
| 2026-10-15 | 26 | Rs. 12,534.23 | Rs. 14,600.58 | 100.16 | 99.62 | **93.76** | -6.24% |
| 2026-10-16 | 54 | Rs. 11,794.96 | Rs. 12,237.58 | 115.68 | 112.55 | **91.34** | -8.66% |
| 2026-10-17 | 54 | Rs. 11,743.37 | Rs. 13,001.72 | 112.22 | 111.28 | **94.69** | -5.31% |

> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($ar{P}_t / ar{P}_0 	imes 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
