"""
Exporter utility: handles structured JSON output and CSV transformation.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Tuple
import pandas as pd


def save_to_json(
    records: List[Dict[str, Any]],
    origin: str,
    destination: str,
    output_dir: str = "data/raw_json",
    timestamp_str: str = None,
) -> str:
    """
    Saves scraped flight records with metadata into a formatted JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    if timestamp_str is None:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"flight_prices_{origin}_{destination}_{timestamp_str}.json"
    filepath = os.path.join(output_dir, filename)

    payload = {
        "metadata": {
            "origin": origin,
            "destination": destination,
            "scrape_time": datetime.now().isoformat(),
            "total_records": len(records),
            "horizons": list(set(r.get("horizon") for r in records if "horizon" in r)),
        },
        "flights": records,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    return filepath


def convert_json_to_csv(
    json_filepath: str,
    output_dir: str = "data/processed_csv",
) -> Tuple[str, pd.DataFrame]:
    """
    Reads a scraped flight JSON file, flattens flight records into a tabular format,
    and writes out a standardized CSV file for price index calculations.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(json_filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    flights = data.get("flights", [])
    if not flights:
        df = pd.DataFrame(columns=[
            "scrape_timestamp", "horizon", "horizon_days", "travel_date",
            "origin", "destination", "airline", "flight_number",
            "departure_time", "arrival_time", "duration_mins", "stops",
            "price_inr", "source_portal"
        ])
    else:
        df = pd.DataFrame(flights)

        # Standardize column types
        if "price_inr" in df.columns:
            df["price_inr"] = pd.to_numeric(df["price_inr"], errors="coerce")
        if "duration_mins" in df.columns:
            df["duration_mins"] = pd.to_numeric(df["duration_mins"], errors="coerce")
        if "stops" in df.columns:
            df["stops"] = pd.to_numeric(df["stops"], errors="coerce").fillna(0).astype(int)

        # Ensure consistent column ordering
        expected_cols = [
            "scrape_timestamp", "horizon", "horizon_days", "travel_date",
            "origin", "destination", "airline", "flight_number",
            "departure_time", "arrival_time", "duration_mins", "stops",
            "price_inr", "source_portal"
        ]
        existing_cols = [c for c in expected_cols if c in df.columns]
        extra_cols = [c for c in df.columns if c not in expected_cols]
        df = df[existing_cols + extra_cols]

        # Sort logically: by horizon days then price
        sort_by = [c for c in ["horizon_days", "price_inr"] if c in df.columns]
        if sort_by:
            df = df.sort_values(by=sort_by).reset_index(drop=True)

    # Derive CSV filename from JSON filename
    base_name = os.path.splitext(os.path.basename(json_filepath))[0]
    csv_filename = f"{base_name}.csv"
    csv_filepath = os.path.join(output_dir, csv_filename)

    df.to_csv(csv_filepath, index=False, encoding="utf-8")
    # Also save a copy as latest.csv for easy access
    origin_val = df['origin'].iloc[0] if not df.empty and 'origin' in df.columns else 'route'
    dest_val = df['destination'].iloc[0] if not df.empty and 'destination' in df.columns else 'latest'
    latest_csv_filepath = os.path.join(output_dir, f"flight_prices_{origin_val}_{dest_val}_latest.csv")
    df.to_csv(latest_csv_filepath, index=False, encoding="utf-8")

    # Append to cumulative master dataset for multi-day time-series analysis
    append_to_master_csv(df, origin=origin_val, destination=dest_val)

    return csv_filepath, df


def append_to_master_csv(df: pd.DataFrame, origin: str, destination: str, master_path: str = "data/master_flight_prices.csv") -> str:
    """
    Appends newly scraped flight records to a single cumulative master CSV file.
    This master file collects daily data across days (Day 1, Day 2... Day 7) for CPI analysis.
    """
    if df.empty:
        return master_path

    os.makedirs(os.path.dirname(master_path), exist_ok=True)
    df = df.copy()
    if "origin" in df.columns and "destination" in df.columns:
        df["origin"] = df["origin"].astype(str).str.upper().str.strip()
        df["destination"] = df["destination"].astype(str).str.upper().str.strip()
        df["route"] = df["origin"] + " -> " + df["destination"]

    if os.path.exists(master_path):
        master_df = pd.read_csv(master_path)
        combined_df = pd.concat([master_df, df], ignore_index=True)
        # Drop duplicates based on key attributes to avoid accidental re-scrapes
        subset_cols = [c for c in ["scrape_timestamp", "travel_date", "airline", "departure_time", "price_inr"] if c in combined_df.columns]
        if subset_cols:
            combined_df = combined_df.drop_duplicates(subset=subset_cols)
    else:
        combined_df = df.copy()

    combined_df.to_csv(master_path, index=False, encoding="utf-8")
    return master_path


def print_summary_table(df: pd.DataFrame):
    """
    Prints a concise price summary per horizon to visualize the airfare index trends.
    """
    if df.empty or "price_inr" not in df.columns:
        print("[!] No records to summarize.")
        return

    print("\n" + "=" * 68)
    origin_name = df["origin"].iloc[0] if "origin" in df.columns and not df.empty else "DEL"
    dest_name = df["destination"].iloc[0] if "destination" in df.columns and not df.empty else "HYD"
    print(f" AIRFARE SUMMARY BY HORIZON ({origin_name} -> {dest_name})")
    print("=" * 68)
    
    summary = df.groupby(["horizon", "horizon_days"]).agg(
        total_flights=("price_inr", "count"),
        min_price=("price_inr", "min"),
        avg_price=("price_inr", "mean"),
        max_price=("price_inr", "max"),
    ).reset_index()

    summary = summary.sort_values(by="horizon_days")

    print(f"{'Horizon':<10} {'Days':<6} {'Flights':<10} {'Min (INR)':<14} {'Avg (INR)':<14} {'Max (INR)':<14}")
    print("-" * 68)
    for _, row in summary.iterrows():
        print(
            f"{row['horizon']:<10} {int(row['horizon_days']):<6} {int(row['total_flights']):<10} "
            f"Rs. {row['min_price']:<10.0f} Rs. {row['avg_price']:<10.1f} Rs. {row['max_price']:<10.0f}"
        )
    print("=" * 68 + "\n")
