"""
Main Runner: Real-Time Airfare Price Scraper for CPI Augmentation.
Scrapes domestic flight prices (default: DEL -> HYD) across advance-purchase horizons:
t+1, t+7, t+15, and t+30 days.

Outputs:
  - JSON file: data/raw_json/flight_prices_<ORIGIN>_<DEST>_<TIMESTAMP>.json
  - CSV file:  data/processed_csv/flight_prices_<ORIGIN>_<DEST>_<TIMESTAMP>.csv
"""

import os
import sys
import time
import argparse
from datetime import datetime

from scrapers.base_scraper import get_target_horizons
from scrapers.flight_scraper import FlightScraper
from utils.exporter import save_to_json, convert_json_to_csv, print_summary_table


def main():
    parser = argparse.ArgumentParser(
        description="Scrape flight prices for CPI Index (Step 1: DEL -> HYD across horizons)."
    )
    parser.add_argument("--origin", type=str, default="DEL", help="Origin airport code (default: DEL)")
    parser.add_argument("--dest", type=str, default="HYD", help="Destination airport code (default: HYD)")
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default: True)",
    )
    parser.add_argument(
        "--no-headless",
        dest="headless",
        action="store_false",
        help="Run browser with visible UI (for debugging)",
    )
    args = parser.parse_args()

    origin = args.origin.upper()
    destination = args.dest.upper()

    print("=" * 68)
    print(" REAL-TIME AIRFARE PRICE SCRAPER (CPI AUGMENTATION)")
    print("=" * 68)
    print(f"[*] Route:          {origin} -> {destination}")
    print(f"[*] Base Date (t):  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Target Lead:    t+1, t+7, t+15, t+30")
    print("=" * 68 + "\n")

    # 1. Compute target horizon dates
    horizons = get_target_horizons()
    print("[*] Scheduled Travel Horizons:")
    for h in horizons:
        print(f"    - {h['horizon']:<5} (in {h['horizon_days']:<2} days): {h['iso_date']} ({h['day_name']})")
    print()

    scraper = FlightScraper(headless=args.headless)
    all_flight_records = []

    # 2. Scrape each horizon sequentially with jitter
    for idx, h in enumerate(horizons):
        horizon_label = h["horizon"]
        horizon_days = h["horizon_days"]
        travel_date_iso = h["iso_date"]

        records = scraper.scrape_route_date(
            origin=origin,
            destination=destination,
            travel_date_iso=travel_date_iso,
            horizon_label=horizon_label,
            horizon_days=horizon_days,
        )

        all_flight_records.extend(records)

        # Politeness delay between horizons
        if idx < len(horizons) - 1:
            print("[*] Waiting 3 seconds before next horizon request...")
            time.sleep(3)

    print(f"\n[+] Total flight records collected: {len(all_flight_records)}")

    if not all_flight_records:
        print("[!] No records scraped. Please check network connectivity or try running with --no-headless.")
        return

    # 3. Export to JSON
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = save_to_json(
        records=all_flight_records,
        origin=origin,
        destination=destination,
        output_dir="data/raw_json",
        timestamp_str=timestamp_str,
    )
    print(f"[+] Saved structured JSON: {os.path.abspath(json_path)}")

    # 4. Convert to CSV
    csv_path, df = convert_json_to_csv(
        json_filepath=json_path,
        output_dir="data/processed_csv",
    )
    print(f"[+] Saved tabular CSV:     {os.path.abspath(csv_path)}")

    # 5. Display price index summary table
    print_summary_table(df)

    # 6. Auto-sync CPI Index & Dashboard
    try:
        import subprocess
        print("[*] Auto-updating CPI price indices and dashboard data...")
        subprocess.run([sys.executable, "calculate_index.py"], check=True)
        print("[+] Dashboard data successfully updated.")
    except Exception as e:
        print(f"[!] Note: Could not auto-run calculate_index.py: {e}")


if __name__ == "__main__":
    main()
