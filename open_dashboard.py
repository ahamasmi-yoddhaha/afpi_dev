"""
Opens the interactive Airfare Price Index Dashboard in your default web browser.
Automatically verifies if new scraped flight data exists in master_flight_prices.csv
and synchronizes dashboard data before opening.
"""

import os
import sys
import argparse
import subprocess
import webbrowser


def sync_dashboard_if_needed(force: bool = False):
    """Ensures dashboard data is synchronized with the latest master CSV."""
    master_csv = "data/master_flight_prices.csv"
    data_js = "data/dashboard_data.js"
    data_json = "data/dashboard_data.json"

    needs_sync = force
    if not os.path.exists(data_js) or not os.path.exists(data_json):
        needs_sync = True
    elif os.path.exists(master_csv):
        csv_mtime = os.path.getmtime(master_csv)
        js_mtime = os.path.getmtime(data_js)
        code_mtime = max(
            os.path.getmtime("calculate_index.py") if os.path.exists("calculate_index.py") else 0,
            os.path.getmtime("analysis/cpi_index.py") if os.path.exists("analysis/cpi_index.py") else 0,
        )
        if csv_mtime > js_mtime or code_mtime > js_mtime:
            needs_sync = True

    if needs_sync:
        print("[*] Synchronizing dashboard with latest scraped flights...")
        try:
            py_bin = ["py", "-3.13"] if os.system("py -3.13 -c \"import pandas\" >nul 2>&1") == 0 else [sys.executable]
            subprocess.run(py_bin + ["calculate_index.py"], check=True)
            print("[+] Dashboard data successfully synchronized.")
        except Exception as e:
            print(f"[!] Warning: Auto-sync encountered error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Open Airfare CPI Dashboard")
    parser.add_argument("--sync", "--refresh", action="store_true", help="Force recalculate indices and sync dashboard")
    args = parser.parse_args()

    sync_dashboard_if_needed(force=args.sync)

    dashboard_path = os.path.abspath("dashboard.html")
    if not os.path.exists(dashboard_path):
        print(f"[!] dashboard.html not found at {dashboard_path}")
        return

    url = f"file:///{dashboard_path.replace(os.sep, '/')}"
    print(f"[*] Opening Airfare CPI Dashboard: {url}")
    webbrowser.open(url)


if __name__ == "__main__":
    main()
