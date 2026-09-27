"""
Step 3 Main Runner: CPI Airfare Price Index Calculator & Report Generator.
Computes economic price indices (Jevons, Dutot, DGCA Weighted),
generates charts, and produces an academic-ready CPI summary report.
"""

import os
import argparse
import pandas as pd
from datetime import datetime

from analysis.cpi_index import (
    calculate_daily_cpi_indices,
    calculate_carrier_breakdown,
)
from analysis.visualizer import (
    plot_daily_cpi_trend,
    plot_carrier_comparison,
)


def generate_markdown_report(
    daily_df: pd.DataFrame,
    carrier_df: pd.DataFrame,
    output_path: str = "data/reports/CPI_Airfare_Index_Report.md",
) -> str:
    """Creates a comprehensive Markdown analysis report for project documentation."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    base_date = daily_df["observation_date"].iloc[0] if not daily_df.empty else "N/A"
    latest_date = daily_df["observation_date"].iloc[-1] if not daily_df.empty else "N/A"
    latest_inflation = daily_df["inflation_from_base_pct"].iloc[-1] if not daily_df.empty else 0.0

    report = f"""# Real-Time Airfare Price Index: DEL (Delhi) → HYD (Hyderabad) (CPI Augmentation)
## Empirical Research Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Base Observation Date ($t_0$):** {base_date}  
**Latest Observation Date ($t$):** {latest_date}  
**Net Airfare Price Movement:** {latest_inflation:+.2f}%  

---

### 1. Executive Summary
Traditional Consumer Price Index (CPI) methodology collects airfare rates infrequently from static offline booking counters. This project constructs a real-time, high-frequency Airfare Price Index specifically targeting the high-density domestic trunk corridor between **Delhi (DEL) and Hyderabad (HYD)**, utilizing automated web scraping across advance-purchase horizons ($t+1, t+7, t+15, t+30$) to augment official CPI metrics with true market dynamics.

---

### 2. Inter-Temporal Daily Price Indices (Base = 100.0)
The table below tracks day-over-day price evolution across observation dates:

| Observation Date | Sample Size | Mean Fare (INR) | Weighted Fare (INR) | Dutot Index | Jevons Index | DGCA Weighted Index | Inflation vs Base |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for _, r in daily_df.iterrows():
        w_fare = r.get("weighted_fare_inr", r.get("mean_fare_inr", 0.0))
        report += (
            f"| {r['observation_date']} | {r['sample_size']} | Rs. {r['mean_fare_inr']:,.2f} | "
            f"Rs. {w_fare:,.2f} | {r['dutot_index']:.2f} | {r['jevons_index']:.2f} | "
            f"**{r['carrier_weighted_index']:.2f}** | {r['inflation_from_base_pct']:+.2f}% |\n"
        )

    report += """
> **Methodology Notes:**
> - **Dutot Index**: Ratio of arithmetic mean prices ($\bar{P}_t / \bar{P}_0 \times 100$).
> - **Jevons Index**: Geometric mean of price relatives, recommended by the UN & IMF for unweighted elementary aggregates.
> - **DGCA Weighted Index**: Weighted by official Directorate General of Civil Aviation domestic market share (IndiGo ~61%, Air India ~27%, Akasa ~4.5%, SpiceJet ~4%).

---

### 3. Visualizations
The generated graphical plots are saved in `data/plots/`:
1. **Daily CPI Trend**: `data/plots/daily_cpi_airfare_trend.png`
2. **Carrier Price Comparison**: `data/plots/carrier_price_comparison.png`
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Calculate CPI Airfare Price Index from Master Dataset")
    parser.add_argument(
        "--data",
        type=str,
        default="data/master_flight_prices.csv",
        help="Path to master flight prices CSV (default: data/master_flight_prices.csv)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.data):
        print(f"[!] Master dataset not found at {args.data}.")
        print("[!] Please run at least one scrape first: python run_scraper.py")
        return

    print("=" * 70)
    print(" STEP 3: AIRFARE PRICE INDEX (CPI AUGMENTATION) CALCULATION")
    print("=" * 70)
    print(f"[*] Reading dataset from: {args.data}")

    raw_df = pd.read_csv(args.data)
    # Strictly filter for DEL -> HYD route
    raw_df = raw_df[(raw_df["origin"].astype(str).str.upper() == "DEL") & (raw_df["destination"].astype(str).str.upper() == "HYD")].copy()
    print(f"[+] Loaded {len(raw_df)} raw DEL -> HYD flight observations.")

    # 0. Execute Pre-Analysis Data Cleaning & Decomposition Pipeline
    print("\n[*] Executing Data Cleaning, De-duplication & Fare Decomposition Pipeline...")
    from analysis.cleaning_pipeline import clean_airfare_pipeline, generate_cleaning_audit_report
    clean_df, audit_metrics = clean_airfare_pipeline(raw_df)

    clean_csv = "data/cleaned_flight_prices.csv"
    audit_report = "data/reports/Data_Cleaning_Audit_Report.md"
    clean_df.to_csv(clean_csv, index=False, encoding="utf-8")
    generate_cleaning_audit_report(audit_metrics, clean_df, audit_report)

    print(f"[+] Duplicates Removed:          {audit_metrics['duplicates_removed']} records")
    print(f"[+] Cleaned Flight Observations: {len(clean_df)} records")
    print(f"[+] Statistical Outliers Flagged:{audit_metrics['outliers_flagged']}")
    print(f"[+] Balanced Panel Flights:      {audit_metrics['balanced_panel_count']} flights per date")
    fd = audit_metrics['fare_decomposition_averages']
    print(f"[+] Fare Decomposition:          Base: Rs.{fd['mean_base_fare']:,.0f} ({fd['base_fare_percentage']}%) | Taxes: Rs.{fd['mean_taxes']:,.0f} ({fd['taxes_percentage']}%) | Fees: Rs.{fd['mean_udf_fee']+fd['mean_convenience_fee']:,.0f}")
    print(f"[+] Saved Cleaned Airfare DB:    {clean_csv}")
    print(f"[+] Saved Cleaning Audit Report: {audit_report}")

    # 1. Compute Daily Inter-Temporal CPI Indices
    print("\n[*] Computing Daily CPI Indices (Dutot, Jevons, DGCA Weighted)...")
    daily_df = calculate_daily_cpi_indices(clean_df, balanced_panel=True)

    # 2. Carrier Breakdown
    carrier_df = calculate_carrier_breakdown(clean_df)

    # 3. Save processed summaries to CSV
    os.makedirs("data/reports", exist_ok=True)
    daily_csv = "data/reports/cpi_daily_index_summary.csv"
    daily_df.to_csv(daily_csv, index=False, encoding="utf-8")
    print(f"[+] Saved Daily Index Summary:   {daily_csv}")

    # 4. Generate Visual Charts
    print("\n[*] Generating high-resolution publication charts...")
    p1 = plot_daily_cpi_trend(daily_df, output_dir="data/plots")
    p2 = plot_carrier_comparison(carrier_df, output_dir="data/plots")
    print(f"[+] Saved: {p1}")
    print(f"[+] Saved: {p2}")

    # 5. Generate Dedicated DEL -> HYD Dashboard Data
    import json
    from analysis.cpi_index import build_dashboard_data
    dashboard_payload = build_dashboard_data(clean_df)
    dashboard_payload["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dashboard_json_path = "data/dashboard_data.json"
    with open(dashboard_json_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_payload, f, indent=2)
    print(f"[+] Saved DEL -> HYD Dashboard JSON: {dashboard_json_path}")

    dashboard_js_path = "data/dashboard_data.js"
    with open(dashboard_js_path, "w", encoding="utf-8") as f:
        f.write("window.DASHBOARD_DATA = " + json.dumps(dashboard_payload, indent=2) + ";\n")
    print(f"[+] Saved Dashboard JS Data:      {dashboard_js_path}")

    # 6. Generate Project Report
    report_file = generate_markdown_report(daily_df, carrier_df)
    print(f"[+] Generated Academic Report:   {report_file}")

    # 7. Print Terminal Summary Tables
    print("\n" + "=" * 70)
    print(" DAILY INTER-TEMPORAL AIRFARE PRICE INDEX (CPI SUB-INDEX)")
    print("=" * 70)
    print(f"{'Date':<12} {'Flights':<9} {'Mean (INR)':<13} {'Dutot':<10} {'Jevons':<10} {'Weighted':<10} {'Change':<8}")
    print("-" * 70)
    for _, r in daily_df.iterrows():
        print(
            f"{r['observation_date']:<12} {r['sample_size']:<9} Rs. {r['mean_fare_inr']:<9.0f} "
            f"{r['dutot_index']:<10.2f} {r['jevons_index']:<10.2f} {r['carrier_weighted_index']:<10.2f} {r['inflation_from_base_pct']:+5.2f}%"
        )
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
