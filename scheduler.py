"""
Scheduled Daily Extraction Daemon.
Provides an automated scheduler capable of running daily extraction cycles
at configured times (e.g., 02:00 AM IST) or regular intervals, with heartbeat logging
and clean process management.
"""

import argparse
import logging
import sys
import time
from datetime import datetime
import schedule
from config import SCRAPER_SETTINGS, LOGS_DIR
from batch_runner import run_basket_scraping

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "scraper_daemon.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("SchedulerDaemon")

def scheduled_job():
    """Wrapper function executed on each scheduled trigger."""
    logger.info("==================================================")
    logger.info("TRIGGERED SCHEDULED DAILY AIRFARE EXTRACTION CYCLE")
    logger.info("==================================================")
    try:
        run_basket_scraping(test_mode=False, headless=True)
    except Exception as e:
        logger.error(f"Scheduled extraction encountered an unhandled exception: {e}", exc_info=True)

def main():
    parser = argparse.ArgumentParser(description="Airfare Price Index (APIx) Scheduled Extraction Daemon")
    parser.add_argument("--now", action="store_true", help="Run immediate full basket extraction and exit")
    parser.add_argument("--test", action="store_true", help="Run immediate test extraction (1 route x 2 windows) and exit")
    parser.add_argument("--daily-at", default=SCRAPER_SETTINGS.get("daily_run_time", "02:00"), help="Schedule daily run at HH:MM (24-hr format, e.g. 02:00)")
    parser.add_argument("--interval-hours", type=int, default=None, help="Run every N hours")
    parser.add_argument("--interval-mins", type=int, default=None, help="Run every N minutes (useful for live testing)")
    parser.add_argument("--visible", action="store_true", help="Run with visible browser window")

    args = parser.parse_args()

    # Immediate one-off runs
    if args.test:
        logger.info("Executing immediate test extraction...")
        run_basket_scraping(test_mode=True, headless=not args.visible)
        return

    if args.now:
        logger.info("Executing immediate full basket extraction...")
        run_basket_scraping(test_mode=False, headless=not args.visible)
        return

    # Scheduling Mode
    logger.info("==================================================")
    logger.info("   AIRFARE SCRAPING ENGINE - SCHEDULER DAEMON     ")
    logger.info("==================================================")

    if args.interval_mins:
        schedule.every(args.interval_mins).minutes.do(scheduled_job)
        logger.info(f"Scheduler mode: Running every {args.interval_mins} minute(s).")
    elif args.interval_hours:
        schedule.every(args.interval_hours).hours.do(scheduled_job)
        logger.info(f"Scheduler mode: Running every {args.interval_hours} hour(s).")
    else:
        schedule.every().day.at(args.daily_at).do(scheduled_job)
        logger.info(f"Scheduler mode: Configured for daily extraction at {args.daily_at} IST.")

    # Calculate and log next run
    next_run = schedule.next_run()
    logger.info(f"Next scheduled extraction cycle: {next_run}")
    logger.info("Daemon is active and waiting. Press Ctrl+C to terminate.\n")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Daemon termination requested by user. Shutting down cleanly.")

if __name__ == "__main__":
    main()
