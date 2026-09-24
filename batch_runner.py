"""
Batch Runner for Daily DGCA Route Basket Extraction.
Orchestrates scraping across representative city-pairs and advance-purchase windows
(T+1, T+7, T+15, T+30, T+45), persists to SQLite, and updates CSV datasets.
"""

import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from config import (
    DGCA_ROUTE_BASKET,
    ADVANCE_PURCHASE_WINDOWS,
    DATA_DIR,
    LOGS_DIR,
)
from scraper_engine import EthicalScraperEngine
import database

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "scraper_daemon.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("BatchRunner")

def run_basket_scraping(test_mode: bool = False, headless: bool = True) -> dict:
    """Executes scraping for the DGCA route basket and advance windows.
    
    Args:
        test_mode: If True, runs a reduced basket (1 route x 2 windows) for quick validation.
        headless: Whether to run the browser in headless mode.
        
    Returns:
        Summary metrics dictionary of the batch run.
    """
    start_time = datetime.now()
    today = datetime.now().date()
    today_str = today.strftime("%Y-%m-%d")

    # Select routes and windows based on mode
    if test_mode:
        routes = [DGCA_ROUTE_BASKET[0]]  # DEL-BOM only
        windows = ADVANCE_PURCHASE_WINDOWS[:2]  # T+1 and T+7
        logger.info("Running in TEST MODE (1 Route x 2 Windows)")
    else:
        routes = DGCA_ROUTE_BASKET
        windows = ADVANCE_PURCHASE_WINDOWS
        logger.info(f"Running FULL BASKET ({len(routes)} Routes x {len(windows)} Windows = {len(routes) * len(windows)} queries)")

    total_tasks = len(routes) * len(windows)
    current_task = 0
    total_quotes_found = 0
    total_quotes_inserted = 0

    engine = EthicalScraperEngine(headless=headless)
    batch_results = []

    try:
        for r in routes:
            orig = r["origin"]
            dest = r["destination"]
            route_name = r["name"]

            for w in windows:
                current_task += 1
                w_label = w["label"]
                lead_days = w["lead_days"]
                travel_date = (today + timedelta(days=lead_days)).strftime("%Y-%m-%d")

                logger.info(f"\n[{current_task}/{total_tasks}] Processing {route_name} ({orig}->{dest}) for {w_label} ({travel_date})...")

                quotes = engine.scrape_sector_window(
                    origin=orig,
                    destination=dest,
                    travel_date_str=travel_date,
                    window_label=w_label,
                    lead_days=lead_days,
                )

                if quotes:
                    inserted = database.insert_quotes(quotes)
                    total_quotes_found += len(quotes)
                    total_quotes_inserted += inserted
                    batch_results.extend(quotes)
                    logger.info(f"-> Found {len(quotes)} quotes ({inserted} new unique saved to SQLite).")
                else:
                    logger.warning(f"-> 0 quotes extracted for {orig}->{dest} on {travel_date}.")

    finally:
        engine.close()

    duration_secs = (datetime.now() - start_time).total_seconds()

    # Export daily and master CSV files
    daily_csv = DATA_DIR / f"raw_quotes_{today.strftime('%Y%m%d')}.csv"
    master_csv = DATA_DIR / "master_airfare_dataset.csv"
    
    database.export_to_csv(str(daily_csv), booking_date=today_str)
    database.export_to_csv(str(master_csv))

    summary = {
        "run_date": today_str,
        "duration_seconds": round(duration_secs, 1),
        "total_queries": total_tasks,
        "quotes_found": total_quotes_found,
        "quotes_new_inserted": total_quotes_inserted,
        "daily_csv": str(daily_csv),
        "master_csv": str(master_csv),
    }

    # Print Pretty Run Report
    print("\n" + "=" * 70)
    print("         AIRFARE PRICE INDEX (APIx) - EXTRACTION REPORT")
    print("=" * 70)
    print(f"Run Date             : {summary['run_date']}")
    print(f"Elapsed Time         : {summary['duration_seconds']} seconds")
    print(f"Queries Executed     : {summary['total_queries']}")
    print(f"Total Quotes Found   : {summary['quotes_found']}")
    print(f"New Unique Inserted  : {summary['quotes_new_inserted']}")
    print(f"Daily CSV Saved      : {summary['daily_csv']}")
    print(f"Master CSV Updated   : {summary['master_csv']}")
    
    db_stats = database.get_stats()
    print("\nWarehouse Lifetime Stats:")
    print(f"  * Total Quotes in Warehouse: {db_stats['total_quotes']}")
    print(f"  * Unique Sectors Covered    : {db_stats['unique_sectors']}")
    print(f"  * Booking Days Recorded    : {db_stats['booking_dates']}")
    print("  * Carrier Distribution     :")
    for carrier, count in sorted(db_stats['carrier_breakdown'].items(), key=lambda x: x[1], reverse=True):
        print(f"      - {carrier:<20}: {count} quotes")
    print("=" * 70 + "\n")

    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DGCA Basket Batch Airfare Extraction")
    parser.add_argument("--test", action="store_true", help="Run in test mode (1 route x 2 windows)")
    parser.add_argument("--visible", action="store_true", help="Run browser visibly")
    args = parser.parse_args()

    run_basket_scraping(test_mode=args.test, headless=not args.visible)
