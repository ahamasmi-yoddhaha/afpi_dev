"""
Flight Scraper Module using Playwright for Indian Domestic Routes.
Extracts airline, flight times, duration, stops, and real-time INR prices.
"""

import re
import time
import unicodedata
from datetime import datetime
from typing import List, Dict, Any
from playwright.sync_api import sync_playwright


def parse_duration_to_minutes(duration_str: str) -> int:
    """Converts duration string like '2 hr 30 min' or '55 min' to integer minutes."""
    hours = 0
    minutes = 0
    hr_match = re.search(r"(\d+)\s*hr", duration_str)
    min_match = re.search(r"(\d+)\s*min", duration_str)
    if hr_match:
        hours = int(hr_match.group(1))
    if min_match:
        minutes = int(min_match.group(1))
    return hours * 60 + minutes


def parse_stops(stops_str: str) -> int:
    """Parses stops string like 'Nonstop' or '1 stop' to an integer."""
    if "nonstop" in stops_str.lower():
        return 0
    match = re.search(r"(\d+)", stops_str)
    return int(match.group(1)) if match else 0


def clean_text(text: str) -> str:
    """Normalizes Unicode characters (e.g., narrow non-breaking spaces \u202f)."""
    normalized = unicodedata.normalize("NFKD", text)
    return normalized.replace("\u202f", " ").replace("\xa0", " ").strip()


class FlightScraper:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def scrape_route_date(
        self,
        origin: str,
        destination: str,
        travel_date_iso: str,
        horizon_label: str,
        horizon_days: int,
    ) -> List[Dict[str, Any]]:
        """
        Scrapes one-way flight prices and flight details for a given origin,
        destination, and date (YYYY-MM-DD).
        """
        url = (
            f"https://www.google.com/travel/flights?q="
            f"Flights%20to%20{destination}%20from%20{origin}%20on%20{travel_date_iso}%20one%20way"
            f"&hl=en&gl=IN&curr=INR"
        )
        print(f"[*] Scraping {origin} -> {destination} for {travel_date_iso} ({horizon_label})...")

        flights: List[Dict[str, Any]] = []

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ],
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                locale="en-IN",
                extra_http_headers={"Accept-Language": "en-IN,en;q=0.9"},
            )
            page = context.new_page()

            try:
                try:
                    page.goto(url, timeout=40000, wait_until="domcontentloaded")
                except Exception as nav_e:
                    print(f"[*] Initial navigation notice: {nav_e}")

                page.wait_for_timeout(2000)

                # Dismiss Google consent modal if presented in cloud / international IP environments
                for btn_text in ["Accept all", "I agree", "Agree", "Tout accepter", "Alle akzeptieren"]:
                    try:
                        btn = page.locator(f"button:has-text('{btn_text}')")
                        if btn.count() > 0 and btn.first.is_visible():
                            btn.first.click()
                            page.wait_for_timeout(2000)
                            break
                    except Exception:
                        pass

                try:
                    page.wait_for_load_state("networkidle", timeout=12000)
                except Exception:
                    pass

                page.wait_for_timeout(3000)
                body_text = page.inner_text("body")

                # Pattern matching flight blocks with flexible currency symbols (₹, Rs, INR)
                pattern = re.compile(
                    r"(\d{1,2}:\d{2}\s*(?:AM|PM))\s*[–\-]\s*(\d{1,2}:\d{2}\s*(?:AM|PM)(?:\+\d)?)\s*\n"
                    r"([A-Za-z0-9\s]+?)\s*\n"
                    r"(\d+\s*hr(?:\s*\d+\s*min)?|\d+\s*min)\s*\n"
                    r"(?:[A-Z]{3}[–\-][A-Z]{3})\s*\n"
                    r"(Nonstop|\d+\s*stop(?:s)?)\s*\n"
                    r"(?:.*?\n)*?"
                    r"(?:₹|Rs\.?|INR)\s*([\d,]+)",
                    re.MULTILINE,
                )

                matches = pattern.findall(body_text)
                scrape_time = datetime.now().isoformat()

                for m in matches:
                    dep_time, arr_time, airline, duration_str, stops_str, price_str = m
                    dep_clean = clean_text(dep_time)
                    arr_clean = clean_text(arr_time)
                    airline_clean = clean_text(airline)
                    duration_clean = clean_text(duration_str)
                    stops_clean = clean_text(stops_str)
                    price_val = float(price_str.replace(",", ""))

                    flights.append({
                        "scrape_timestamp": scrape_time,
                        "horizon": horizon_label,
                        "horizon_days": horizon_days,
                        "travel_date": travel_date_iso,
                        "origin": origin.upper(),
                        "destination": destination.upper(),
                        "airline": airline_clean,
                        "departure_time": dep_clean,
                        "arrival_time": arr_clean,
                        "duration": duration_clean,
                        "duration_mins": parse_duration_to_minutes(duration_clean),
                        "stops": parse_stops(stops_clean),
                        "price_inr": price_val,
                        "source_portal": "GoogleFlights-Aggregator",
                    })

                print(f"[+] Found {len(flights)} flights for horizon {horizon_label} ({travel_date_iso}).")
            except Exception as e:
                print(f"[!] Error while scraping {travel_date_iso}: {e}")
            finally:
                browser.close()

        return flights
