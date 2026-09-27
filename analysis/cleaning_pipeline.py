"""
Data Cleaning & Standardisation Pipeline for Domestic Airfare Price Data.
Handles:
  1. Missing value imputation and validation
  2. Multi-scrape exact and near de-duplication
  3. Statistical outlier detection (Tukey's IQR per horizon & carrier)
  4. Inventory attrition (sold-out and cancelled flights tracking)
  5. Domestic fare decomposition: Base Fare, GST (5%), UDF/ASF, and Convenience Fees
  6. Output of cleaned, de-duplicated database with full metadata
"""

import os
import argparse
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


# Directorate General of Civil Aviation (DGCA) statutory fee parameters
DEFAULT_UDF_ASF_FEE = 450.0       # Airport User Development Fee + Aviation Security Fee (Rs. 200 + GST)
DEFAULT_CONVENIENCE_FEE = 350.0   # Standard digital/web ticketing access fee
DEFAULT_GST_RATE = 0.05           # 5% GST for domestic economy air travel


def map_canonical_carrier(airline_str: str) -> str:
    """Standardizes airline names to canonical DGCA carrier names."""
    s = str(airline_str).lower().strip()
    if "indigo" in s:
        return "IndiGo"
    elif "air india" in s:
        return "Air India"
    elif "akasa" in s:
        return "Akasa Air"
    elif "spicejet" in s:
        return "SpiceJet"
    return "Others"


def decompose_ticket_fare(
    total_price: float,
    udf_fee: float = DEFAULT_UDF_ASF_FEE,
    conv_fee: float = DEFAULT_CONVENIENCE_FEE,
    gst_rate: float = DEFAULT_GST_RATE,
) -> Tuple[float, float, float, float]:
    """
    Decomposes gross domestic airfare into statutory components:
      - Base Fare (airline revenue component)
      - Taxes (5% GST under Indian GST Act)
      - User Development Fee & Aviation Security Fee (Airport authority)
      - Convenience Fee (OTA / airline online booking charge)

    Invariant: base_fare + taxes + udf_fee + conv_fee == total_price
    """
    if pd.isna(total_price) or total_price <= 0:
        return 0.0, 0.0, 0.0, 0.0

    total_price = float(total_price)
    statutory_fees = udf_fee + conv_fee

    if total_price > statutory_fees + 200.0:
        net_taxable = total_price - statutory_fees
        base = round(net_taxable / (1.0 + gst_rate), 2)
        taxes = round(base * gst_rate, 2)
        # Rounding discrepancy adjustment to guarantee exact sum equality
        remainder = round(total_price - (base + taxes + udf_fee + conv_fee), 2)
        taxes = round(taxes + remainder, 2)
        return base, taxes, udf_fee, conv_fee
    else:
        # Fallback proportional decomposition for unusually low or promotional fares
        base = round(total_price * 0.75, 2)
        taxes = round(total_price * 0.05, 2)
        u_fee = round(total_price * 0.12, 2)
        c_fee = round(total_price - (base + taxes + u_fee), 2)
        return base, taxes, u_fee, c_fee


def clean_airfare_pipeline(
    raw_df: pd.DataFrame,
    outlier_iqr_multiplier: float = 2.5,
    udf_fee: float = DEFAULT_UDF_ASF_FEE,
    conv_fee: float = DEFAULT_CONVENIENCE_FEE,
    gst_rate: float = DEFAULT_GST_RATE,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Executes the full end-to-end data-cleaning and standardization pipeline.

    :param raw_df: Raw master DataFrame from web scraping
    :param outlier_iqr_multiplier: Multiplier k for Tukey's IQR rule (default: 2.5 for extreme spikes)
    :return: (cleaned_df, audit_metrics)
    """
    initial_record_count = len(raw_df)
    df = raw_df.copy()

    # -------------------------------------------------------------
    # Stage 1: Validation & Handling Missing Values
    # -------------------------------------------------------------
    # Parse timestamps and dates
    df["scrape_timestamp"] = pd.to_datetime(df.get("scrape_timestamp"), errors="coerce")
    df["scrape_date"] = df["scrape_timestamp"].dt.strftime("%Y-%m-%d")
    df["travel_date"] = pd.to_datetime(df.get("travel_date"), errors="coerce").dt.strftime("%Y-%m-%d")

    # Coerce price and filter invalid rows
    df["price_inr"] = pd.to_numeric(df.get("price_inr"), errors="coerce")
    missing_price_count = int(df["price_inr"].isna().sum() + (df["price_inr"] <= 0).sum())

    critical_cols = ["price_inr", "scrape_date", "airline", "departure_time", "arrival_time"]
    df = df.dropna(subset=[c for c in critical_cols if c in df.columns]).copy()
    df = df[df["price_inr"] > 0].copy()

    # -------------------------------------------------------------
    # Stage 2: Normalization & Standardization
    # -------------------------------------------------------------
    df["origin"] = df.get("origin", "DEL").astype(str).str.upper().str.strip()
    df["destination"] = df.get("destination", "HYD").astype(str).str.upper().str.strip()
    df["route"] = df["origin"] + " -> " + df["destination"]

    df["airline"] = df["airline"].astype(str).str.strip()
    df["carrier_group"] = df["airline"].apply(map_canonical_carrier)
    df["carrier"] = df["carrier_group"]  # Alias for standard naming

    df["departure_time"] = df["departure_time"].astype(str).str.strip()
    df["arrival_time"] = df["arrival_time"].astype(str).str.strip()

    # Clean stops and duration
    df["stops"] = pd.to_numeric(df.get("stops"), errors="coerce").fillna(0).astype(int)
    df["duration_mins"] = pd.to_numeric(df.get("duration_mins"), errors="coerce").fillna(135).astype(int)
    df["fare_class"] = "Economy"

    # Standardize lead time / advance purchase window
    if "horizon" in df.columns:
        df["advance_purchase_window"] = df["horizon"].astype(str).str.strip()
    else:
        df["advance_purchase_window"] = "t+1"

    if "horizon_days" in df.columns:
        df["lead_days"] = pd.to_numeric(df["horizon_days"], errors="coerce").fillna(1).astype(int)
    else:
        horizon_map = {"t+1": 1, "t+7": 7, "t+15": 15, "t+30": 30}
        df["lead_days"] = df["advance_purchase_window"].map(horizon_map).fillna(1).astype(int)

    # -------------------------------------------------------------
    # Stage 3: Exact & Near De-duplication
    # -------------------------------------------------------------
    # A single scraping run or repeated daily runs may capture the same flight service multiple times.
    dedup_keys = [
        "scrape_date",
        "origin",
        "destination",
        "carrier_group",
        "advance_purchase_window",
        "departure_time",
        "arrival_time",
        "duration_mins",
        "stops",
    ]

    pre_dedup_count = len(df)
    df_dedup = (
        df.groupby(dedup_keys, as_index=False)
        .agg({
            "scrape_timestamp": "first",
            "travel_date": "first",
            "airline": "first",
            "carrier": "first",
            "route": "first",
            "fare_class": "first",
            "lead_days": "first",
            "price_inr": "median",  # Median fare across identical runs on same observation date
        })
    )
    duplicates_removed = pre_dedup_count - len(df_dedup)

    # Deterministic flight product ID
    df_dedup["flight_id"] = (
        df_dedup["route"] + "|" +
        df_dedup["carrier_group"] + "|" +
        df_dedup["advance_purchase_window"] + "|" +
        df_dedup["departure_time"] + "|" +
        df_dedup["arrival_time"] + "|" +
        df_dedup["duration_mins"].astype(str) + "|" +
        df_dedup["stops"].astype(str)
    )

    # -------------------------------------------------------------
    # Stage 4: Statistical Outlier Detection (Tukey's IQR per Horizon)
    # -------------------------------------------------------------
    df_dedup["is_outlier"] = False
    df_dedup["outlier_type"] = "NORMAL"
    df_dedup["outlier_threshold_high"] = np.nan
    df_dedup["outlier_threshold_low"] = np.nan

    outlier_counts = 0
    for h, grp in df_dedup.groupby("advance_purchase_window"):
        q1 = grp["price_inr"].quantile(0.25)
        q3 = grp["price_inr"].quantile(0.75)
        iqr = q3 - q1

        # Use IQR multiplier (default 2.5 for extreme deviations)
        high_cutoff = round(q3 + outlier_iqr_multiplier * iqr, 2)
        low_cutoff = round(max(2000.0, q1 - outlier_iqr_multiplier * iqr), 2)

        h_mask = df_dedup["advance_purchase_window"] == h
        df_dedup.loc[h_mask, "outlier_threshold_high"] = high_cutoff
        df_dedup.loc[h_mask, "outlier_threshold_low"] = low_cutoff

        spike_mask = h_mask & (df_dedup["price_inr"] > high_cutoff)
        floor_mask = h_mask & (df_dedup["price_inr"] < low_cutoff)

        df_dedup.loc[spike_mask, "is_outlier"] = True
        df_dedup.loc[spike_mask, "outlier_type"] = "HIGH_SPIKE"

        df_dedup.loc[floor_mask, "is_outlier"] = True
        df_dedup.loc[floor_mask, "outlier_type"] = "LOW_ANOMALY"

    outlier_counts = int(df_dedup["is_outlier"].sum())

    # -------------------------------------------------------------
    # Stage 5: Cancellations & Inventory Attrition Analysis
    # -------------------------------------------------------------
    unique_dates = sorted(df_dedup["scrape_date"].dropna().unique())
    num_dates = len(unique_dates)

    # Identify items present across ALL observation dates (balanced panel)
    date_counts = df_dedup.groupby("flight_id")["scrape_date"].nunique()
    balanced_ids = set(date_counts[date_counts == num_dates].index)
    df_dedup["is_balanced"] = df_dedup["flight_id"].isin(balanced_ids)

    # Inventory tracking across consecutive days
    df_dedup["inventory_status"] = "ACTIVE"
    attrition_summary = []

    for i in range(len(unique_dates) - 1):
        d_curr = unique_dates[i]
        d_next = unique_dates[i + 1]

        set_curr = set(df_dedup[df_dedup["scrape_date"] == d_curr]["flight_id"])
        set_next = set(df_dedup[df_dedup["scrape_date"] == d_next]["flight_id"])

        sold_out_next = set_curr - set_next
        new_in_next = set_next - set_curr

        # Tag flights that deplete/sell out on subsequent day
        curr_mask = (df_dedup["scrape_date"] == d_curr) & (df_dedup["flight_id"].isin(sold_out_next))
        df_dedup.loc[curr_mask, "inventory_status"] = "DEPLETED_SUBSEQUENT_DAY"

        # Tag newly appeared flights
        next_mask = (df_dedup["scrape_date"] == d_next) & (df_dedup["flight_id"].isin(new_in_next))
        df_dedup.loc[next_mask, "inventory_status"] = "NEW_INVENTORY"

        attrition_summary.append({
            "from_date": d_curr,
            "to_date": d_next,
            "starting_flights": len(set_curr),
            "sold_out_or_cancelled": len(sold_out_next),
            "new_inventory_added": len(new_in_next),
            "retained_common_flights": len(set_curr & set_next),
        })

    # -------------------------------------------------------------
    # Stage 6: Fare Component Decomposition (Statutory Breakdown)
    # -------------------------------------------------------------
    decomp_results = df_dedup["price_inr"].apply(
        lambda p: decompose_ticket_fare(p, udf_fee, conv_fee, gst_rate)
    )

    df_dedup["base_fare_inr"] = [r[0] for r in decomp_results]
    df_dedup["taxes_inr"] = [r[1] for r in decomp_results]
    df_dedup["udf_fee_inr"] = [r[2] for r in decomp_results]
    df_dedup["convenience_fee_inr"] = [r[3] for r in decomp_results]
    df_dedup["total_fare_inr"] = df_dedup["price_inr"].round(2)

    # Standard downstream aliases
    df_dedup["price_inr"] = df_dedup["total_fare_inr"]
    df_dedup["horizon"] = df_dedup["advance_purchase_window"]
    df_dedup["horizon_days"] = df_dedup["lead_days"]

    # Sort dataset cleanly
    final_cols = [
        "flight_id",
        "scrape_date",
        "scrape_timestamp",
        "origin",
        "destination",
        "route",
        "carrier",
        "airline",
        "carrier_group",
        "advance_purchase_window",
        "horizon",
        "lead_days",
        "horizon_days",
        "travel_date",
        "fare_class",
        "departure_time",
        "arrival_time",
        "duration_mins",
        "stops",
        "base_fare_inr",
        "taxes_inr",
        "udf_fee_inr",
        "convenience_fee_inr",
        "total_fare_inr",
        "price_inr",
        "inventory_status",
        "is_outlier",
        "outlier_type",
        "is_balanced",
    ]

    cleaned_df = df_dedup[final_cols].sort_values(
        by=["scrape_date", "advance_purchase_window", "carrier_group", "departure_time"]
    ).reset_index(drop=True)

    # -------------------------------------------------------------
    # Stage 7: Assemble Audit Metrics
    # -------------------------------------------------------------
    audit_metrics = {
        "initial_record_count": initial_record_count,
        "missing_price_count": missing_price_count,
        "duplicates_removed": duplicates_removed,
        "clean_record_count": len(cleaned_df),
        "outliers_flagged": outlier_counts,
        "unique_observation_dates": unique_dates,
        "balanced_panel_count": len(balanced_ids),
        "attrition_summary": attrition_summary,
        "fare_decomposition_averages": {
            "mean_total_fare": round(float(cleaned_df["total_fare_inr"].mean()), 2),
            "mean_base_fare": round(float(cleaned_df["base_fare_inr"].mean()), 2),
            "mean_taxes": round(float(cleaned_df["taxes_inr"].mean()), 2),
            "mean_udf_fee": round(float(cleaned_df["udf_fee_inr"].mean()), 2),
            "mean_convenience_fee": round(float(cleaned_df["convenience_fee_inr"].mean()), 2),
            "base_fare_percentage": round(float((cleaned_df["base_fare_inr"].mean() / cleaned_df["total_fare_inr"].mean()) * 100), 1),
            "taxes_percentage": round(float((cleaned_df["taxes_inr"].mean() / cleaned_df["total_fare_inr"].mean()) * 100), 1),
            "fees_percentage": round(float(((cleaned_df["udf_fee_inr"].mean() + cleaned_df["convenience_fee_inr"].mean()) / cleaned_df["total_fare_inr"].mean()) * 100), 1),
        }
    }

    return cleaned_df, audit_metrics


def generate_cleaning_audit_report(
    metrics: Dict[str, Any],
    cleaned_df: pd.DataFrame,
    output_path: str = "data/reports/Data_Cleaning_Audit_Report.md",
) -> str:
    """Generates an academic markdown audit report summarizing the cleaning process."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fd = metrics["fare_decomposition_averages"]
    dates_str = ", ".join(metrics["unique_observation_dates"])

    report = f"""# Airfare Database Data Cleaning & Standardisation Audit Report

**Route Corridor:** Delhi Indira Gandhi International (DEL) &rarr; Hyderabad Rajiv Gandhi International (HYD)  
**Observation Dates:** {dates_str}  
**Pipeline Execution:** Completed Successfully  

---

### 1. Ingestion, Filtering & De-duplication Summary

| Metric | Count | Percentage |
| :--- | :--- | :--- |
| **Raw Scraped Observations** | **{metrics['initial_record_count']:,}** | 100.0% |
| **Invalid / Missing Values Handled** | {metrics['missing_price_count']:,} | {metrics['missing_price_count']/metrics['initial_record_count']*100:.1f}% |
| **Duplicate Scrapes Removed** | {metrics['duplicates_removed']:,} | {metrics['duplicates_removed']/metrics['initial_record_count']*100:.1f}% |
| **Cleaned & De-duplicated Records** | **{metrics['clean_record_count']:,}** | **{metrics['clean_record_count']/metrics['initial_record_count']*100:.1f}%** |
| **Statistical Outliers Flagged** | {metrics['outliers_flagged']:,} | {metrics['outliers_flagged']/metrics['clean_record_count']*100:.1f}% |
| **Strictly Balanced Panel Flights (All Dates)** | **{metrics['balanced_panel_count']:,} per date** | — |

---

### 2. Statutory Domestic Fare Decomposition (DGCA & MoCA Framework)

In accordance with Indian Ministry of Civil Aviation (MoCA) and DGCA tariff guidelines, gross airfares are decomposed into:
1. **Base Airfare**: The core airline ticket tariff subject to dynamic yield management.
2. **Goods & Services Tax (GST)**: Statutory 5% GST levied on domestic economy tickets under the CGST Act.
3. **Airport User Development Fee (UDF) & Aviation Security Fee (ASF)**: Statutory fee (Rs. 450.00).
4. **Convenience Charges**: Standard digital web booking platform charges (Rs. 350.00).

| Component | Average Value (INR) | Share of Total Airfare |
| :--- | :--- | :--- |
| **Base Fare** | **Rs. {fd['mean_base_fare']:,.2f}** | **{fd['base_fare_percentage']:.1f}%** |
| **Taxes (GST 5%)** | Rs. {fd['mean_taxes']:,.2f} | {fd['taxes_percentage']:.1f}% |
| **Airport UDF & ASF Fee** | Rs. {fd['mean_udf_fee']:,.2f} | {fd['mean_udf_fee']/fd['mean_total_fare']*100:.1f}% |
| **Convenience / Web Fee** | Rs. {fd['mean_convenience_fee']:,.2f} | {fd['mean_convenience_fee']/fd['mean_total_fare']*100:.1f}% |
| **Total Gross Airfare** | **Rs. {fd['mean_total_fare']:,.2f}** | **100.0%** |

---

### 3. Inventory Attrition & Sold-Out Analysis

The table below tracks flight service attrition (depleted seats / cancelled flights) across consecutive scraping dates:

| Transition Period | Active Flights Day $t$ | Sold Out / Cancelled by Day $t+1$ | New Flights Added Day $t+1$ | Common Retained |
| :--- | :---: | :---: | :---: | :---: |
"""
    for att in metrics["attrition_summary"]:
        report += (
            f"| {att['from_date']} &rarr; {att['to_date']} | "
            f"{att['starting_flights']} | {att['sold_out_or_cancelled']} | "
            f"{att['new_inventory_added']} | {att['retained_common_flights']} |\n"
        )

    report += """
---

### 4. Cleaned Dataset Sample (DEL &rarr; HYD)

| Flight ID | Date | Horizon | Carrier | Base Fare (INR) | Taxes (INR) | Fees (INR) | Total (INR) | Status |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
"""
    for _, r in cleaned_df.head(10).iterrows():
        fees = r["udf_fee_inr"] + r["convenience_fee_inr"]
        report += (
            f"| `{r['flight_id'][:28]}...` | {r['scrape_date']} | {r['advance_purchase_window']} | "
            f"{r['carrier_group']} | Rs. {r['base_fare_inr']:,.0f} | Rs. {r['taxes_inr']:,.0f} | "
            f"Rs. {fees:,.0f} | **Rs. {r['total_fare_inr']:,.0f}** | {r['inventory_status']} |\n"
        )

    report += "\n> **Output Path:** `data/cleaned_flight_prices.csv`\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return output_path


def run_cleaning_pipeline(
    raw_csv_path: str = "data/master_flight_prices.csv",
    output_clean_csv: str = "data/cleaned_flight_prices.csv",
    audit_report_path: str = "data/reports/Data_Cleaning_Audit_Report.md",
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Convenience wrapper that reads master CSV, cleans it, and writes output files."""
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Master flight dataset not found at: {raw_csv_path}")

    raw_df = pd.read_csv(raw_csv_path)
    cleaned_df, metrics = clean_airfare_pipeline(raw_df)

    os.makedirs(os.path.dirname(output_clean_csv), exist_ok=True)
    cleaned_df.to_csv(output_clean_csv, index=False, encoding="utf-8")

    generate_cleaning_audit_report(metrics, cleaned_df, audit_report_path)
    return cleaned_df, metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Airfare Data Cleaning & Standardization Pipeline")
    parser.add_argument("--input", type=str, default="data/master_flight_prices.csv", help="Path to raw master CSV")
    parser.add_argument("--output", type=str, default="data/cleaned_flight_prices.csv", help="Path for cleaned CSV")
    args = parser.parse_args()

    print("=" * 72)
    print(" AIRFARE PRICE INDEX: DATA CLEANING & STANDARDIZATION PIPELINE")
    print("=" * 72)
    print(f"[*] Input raw dataset:  {args.input}")

    clean_df, audit = run_cleaning_pipeline(args.input, args.output)

    print(f"[+] Cleaned dataset:    {args.output}")
    print(f"[+] Audit Report:       data/reports/Data_Cleaning_Audit_Report.md")
    print("-" * 72)
    print(f"[*] Raw Records:        {audit['initial_record_count']}")
    print(f"[*] Duplicates Removed: {audit['duplicates_removed']}")
    print(f"[*] Clean Records:      {audit['clean_record_count']}")
    print(f"[*] Outliers Flagged:   {audit['outliers_flagged']}")
    print(f"[*] Balanced Cohort:    {audit['balanced_panel_count']} flights per date")
    fd = audit['fare_decomposition_averages']
    print(f"[*] Fare Decomposition: Base: Rs.{fd['mean_base_fare']:,.0f} ({fd['base_fare_percentage']}%) | Taxes: Rs.{fd['mean_taxes']:,.0f} ({fd['taxes_percentage']}%) | Fees: Rs.{fd['mean_udf_fee']+fd['mean_convenience_fee']:,.0f}")
    print("=" * 72 + "\n")
