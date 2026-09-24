"""
Ethical Web Scraping Engine for Airline Portals and Aggregators.
Handles JavaScript-rendered DOMs, stealth overrides, polite rate limiting,
exponential backoff retries, and structured quote extraction.
"""

import logging
import random
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import SCRAPER_SETTINGS, USER_AGENTS, TARGET_CARRIERS

logger = logging.getLogger("ScraperEngine")

class EthicalScraperEngine:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
        self._init_driver()

    def _init_driver(self):
        """Initializes ChromeDriver with anti-bot evasion and stealth scripts."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass

        ua = random.choice(USER_AGENTS)
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument(f"--user-agent={ua}")

        if self.headless:
            options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.navigator.chrome = { runtime: {} };
            """
        })

    def _polite_delay(self):
        """Applies randomized rate-limiting delay between requests to be polite."""
        min_d = SCRAPER_SETTINGS["min_polite_delay"]
        max_d = SCRAPER_SETTINGS["max_polite_delay"]
        delay = random.uniform(min_d, max_d)
        logger.info(f"Ethical rate-limit delay: sleeping for {delay:.2f}s...")
        time.sleep(delay)

    def scrape_sector_window(
        self,
        origin: str,
        destination: str,
        travel_date_str: str,
        window_label: str,
        lead_days: int
    ) -> list[dict]:
        """Scrapes flight quotes for a specific sector and advance-purchase window.
        
        Args:
            origin: 3-letter IATA (e.g. DEL)
            destination: 3-letter IATA (e.g. BOM)
            travel_date_str: Date string YYYY-MM-DD
            window_label: Advance window tag (e.g. T+1, T+7, T+15)
            lead_days: Number of days between booking and travel
            
        Returns:
            List of parsed and normalized airfare quote dictionaries.
        """
        search_url = f"https://www.google.com/travel/flights?q=Flights%20to%20{destination}%20from%20{origin}%20on%20{travel_date_str}%20oneway"
        sector = f"{origin.upper()}-{destination.upper()}"
        booking_date = datetime.now().strftime("%Y-%m-%d")
        scrape_time = datetime.now().isoformat()

        max_retries = SCRAPER_SETTINGS["max_retries"]
        backoff = SCRAPER_SETTINGS["backoff_factor"]

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"[{sector} | {window_label}] Requesting {search_url} (Attempt {attempt}/{max_retries})")
                self.driver.get(search_url)

                # Wait for initial results to settle
                time.sleep(SCRAPER_SETTINGS["page_settle_delay"])

                # Smooth auto-scrolling to trigger lazy-loaded cards
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
                time.sleep(1.5)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)

                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                cards = soup.find_all("li", class_=lambda c: c and "pIav2d" in str(c))

                quotes = []
                for card in cards:
                    link_div = card.find("div", class_="JMc5Xc")
                    if not link_div or not link_div.get("aria-label"):
                        continue

                    label = link_div["aria-label"].replace("\u202f", " ").replace("\xa0", " ")

                    # 1. Price
                    price_m = re.search(r"From\s+([\d,]+)\s+Indian rupees", label, re.IGNORECASE)
                    if not price_m:
                        continue
                    fare_val = float(price_m.group(1).replace(",", ""))

                    # 2. Airline & Stops
                    flight_m = re.search(r"(\d+\s*stop[s]?|Nonstop)\s+flight\s+with\s+([^.]+)\.", label, re.IGNORECASE)
                    stops_str = flight_m.group(1).strip() if flight_m else "Nonstop"
                    raw_carrier = flight_m.group(2).strip() if flight_m else "Unknown Airline"

                    # Normalize airline name against target carriers
                    carrier = raw_carrier
                    for target in TARGET_CARRIERS:
                        if target.lower() in raw_carrier.lower():
                            carrier = target
                            break

                    # 3. Departure & Arrival Times & Airports
                    leaves_m = re.search(
                        r"Leaves\s+(.+?)\s+at\s+(\d{1,2}:\d{2}\s*[APMapm]{2})\s+on\s+(.+?)\s+and arrives at\s+(.+?)\s+at\s+(\d{1,2}:\d{2}\s*[APMapm]{2})\s+on\s+(.+?)\.",
                        label,
                        re.IGNORECASE,
                    )
                    dep_time = leaves_m.group(2).strip() if leaves_m else "N/A"
                    arr_time = leaves_m.group(5).strip() if leaves_m else "N/A"

                    # 4. Duration calculation
                    dur_m = re.search(r"Total duration\s+([^.]+)\.", label, re.IGNORECASE)
                    dur_str = dur_m.group(1).strip() if dur_m else "N/A"
                    dur_mins = 0
                    if dur_str != "N/A":
                        hr_m = re.search(r"(\d+)\s*hr", dur_str)
                        min_m = re.search(r"(\d+)\s*min", dur_str)
                        dur_mins = (int(hr_m.group(1)) * 60 if hr_m else 0) + (int(min_m.group(1)) if min_m else 0)

                    # Stops count
                    stops_count = 0
                    if "stop" in stops_str.lower() and "nonstop" not in stops_str.lower():
                        sc_m = re.search(r"(\d+)", stops_str)
                        stops_count = int(sc_m.group(1)) if sc_m else 1

                    quote_record = {
                        "scrape_timestamp": scrape_time,
                        "booking_date": booking_date,
                        "travel_date": travel_date_str,
                        "advance_window": window_label,
                        "lead_time_days": lead_days,
                        "origin": origin.upper(),
                        "destination": destination.upper(),
                        "sector": sector,
                        "carrier": carrier,
                        "departure_time": dep_time,
                        "arrival_time": arr_time,
                        "duration_mins": dur_mins,
                        "duration_str": dur_str,
                        "stops": stops_str,
                        "stops_count": stops_count,
                        "fare_class": "Economy",
                        "total_fare": fare_val,
                        "source_portal": "Aggregator/GoogleFlights",
                    }
                    quotes.append(quote_record)

                logger.info(f"[{sector} | {window_label}] Extracted {len(quotes)} valid quotes.")
                self._polite_delay()
                return quotes

            except Exception as e:
                logger.warning(f"Error scraping {sector} window {window_label} on attempt {attempt}: {e}")
                if attempt < max_retries:
                    sleep_time = (backoff ** attempt) + random.uniform(1, 3)
                    logger.info(f"Backing off for {sleep_time:.2f}s before retry...")
                    time.sleep(sleep_time)
                    self._init_driver()  # Refresh driver session on error
                else:
                    logger.error(f"Failed to scrape {sector} window {window_label} after {max_retries} attempts.")
                    self._polite_delay()
                    return []

        return []

    def close(self):
        """Safely terminates the browser session."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
