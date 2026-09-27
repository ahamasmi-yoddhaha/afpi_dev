"""
Automated Daily Scheduler for Airfare Price Index Scraping.
Runs daily at a scheduled time (or every 24 hours) for a set number of days (e.g., 7 days).
Appends all collected data into a central master CSV for CPI analysis.
"""

import time
import argparse
import subprocess
import sys
from datetime import datetime, timedelta


def run_scraping_job(origin: str, dest: str) -> bool:
    """Executes the run_scraper.py script as a subprocess."""
    print("\n" + "=" * 68)
    print(f"[*] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TRIGGERING SCHEDULED SCRAPE: {origin} -> {dest}")
    print("=" * 68)

    cmd = [sys.executable, "run_scraper.py", "--origin", origin, "--dest", dest, "--headless"]
    try:
        result = subprocess.run(cmd, check=True)
        print(f"[+] Scraping job completed successfully at {datetime.now().strftime('%H:%M:%S')}.")

        # Automatically calculate price indices and sync frontend dashboard
        print(f"[*] [{datetime.now().strftime('%H:%M:%S')}] Auto-syncing CPI Price Index and Dashboard...")
        calc_cmd = [sys.executable, "calculate_index.py"]
        subprocess.run(calc_cmd, check=True)
        print(f"[+] Dashboard data successfully synced at {datetime.now().strftime('%H:%M:%S')}.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Scraping job failed with return code {e.returncode}.")
        return False
    except Exception as e:
        print(f"[!] Unexpected error during scrape execution: {e}")
        return False


def start_scheduler(origin: str, dest: str, run_time: str, total_days: int, run_now: bool):
    """
    Schedules and executes the scraper daily.
    
    :param origin: Origin airport code (e.g., DEL)
    :param dest: Destination airport code (e.g., HYD)
    :param run_time: Daily execution time in 'HH:MM' (24-hour format), e.g. '09:00'
    :param total_days: Number of days to run (e.g. 7). Set to 0 for indefinite runs.
    :param run_now: If True, executes once immediately before waiting for next scheduled time.
    """
    print("=" * 68)
    print(" AUTOMATED AIRFARE PRICE INDEX SCHEDULER")
    print("=" * 68)
    print(f"[*] Route:            {origin} -> {dest}")
    print(f"[*] Daily Run Time:   {run_time} (IST)")
    print(f"[*] Duration:         {total_days} days" if total_days > 0 else "[*] Duration:         Indefinite (continuous)")
    print(f"[*] Master Dataset:   data/master_flight_prices.csv")
    print("=" * 68)

    completed_runs = 0

    # Optional immediate first run
    if run_now:
        print("\n[*] Starting initial run immediately...")
        success = run_scraping_job(origin, dest)
        if success:
            completed_runs += 1
            print(f"[+] Day 1 / {total_days} complete.")
            if total_days > 0 and completed_runs >= total_days:
                print("\n[+] All scheduled days completed!")
                return

    target_hour, target_minute = map(int, run_time.split(":"))

    while True:
        if total_days > 0 and completed_runs >= total_days:
            print(f"\n[+] Finished all {total_days} daily scraping runs.")
            print("[+] Your cumulative dataset is ready at: data/master_flight_prices.csv")
            break

        now = datetime.now()
        next_run = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

        # If today's target time has already passed, schedule for tomorrow
        if next_run <= now:
            next_run += timedelta(days=1)

        wait_seconds = (next_run - now).total_seconds()
        hours, remainder = divmod(int(wait_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)

        print(f"\n[*] Next scheduled scrape: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[*] Sleeping for {hours}h {minutes}m {seconds}s... (Press Ctrl+C to stop)")

        try:
            time.sleep(wait_seconds)
            # Wake up and run
            success = run_scraping_job(origin, dest)
            if success:
                completed_runs += 1
                if total_days > 0:
                    print(f"[+] Progress: {completed_runs}/{total_days} daily scrapes completed.")
        except KeyboardInterrupt:
            print("\n[!] Scheduler stopped by user.")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Daily Flight Price Scheduler")
    parser.add_argument("--origin", type=str, default="DEL", help="Origin airport (default: DEL)")
    parser.add_argument("--dest", type=str, default="HYD", help="Destination airport (default: HYD)")
    parser.add_argument("--time", type=str, default="09:00", help="Daily time in 24-hr format HH:MM (default: 09:00)")
    parser.add_argument("--days", type=int, default=7, help="Number of days to run (default: 7, 0 for infinite)")
    parser.add_argument(
        "--run-now",
        action="store_true",
        default=True,
        help="Run once immediately on startup, then wait for daily scheduled time (default: True)"
    )

    args = parser.parse_args()
    start_scheduler(
        origin=args.origin.upper(),
        dest=args.dest.upper(),
        run_time=args.time,
        total_days=args.days,
        run_now=args.run_now,
    )
