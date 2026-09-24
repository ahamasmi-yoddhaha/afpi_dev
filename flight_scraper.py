import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver(headless: bool = True) -> webdriver.Chrome:
    """Configures and returns a Chrome WebDriver with anti-detection flags."""
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
    
    if headless:
        options.add_argument("--headless=new")
        
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
    })
    return driver

def scrape_flights(origin: str, destination: str, date_str: str, headless: bool = True) -> list[dict]:
    """Scrapes flight data for a given route and date.
    
    Args:
        origin: 3-letter IATA code or city name (e.g. DEL)
        destination: 3-letter IATA code or city name (e.g. BOM)
        date_str: Flight date in YYYY-MM-DD format (e.g. 2026-09-26)
        headless: Whether to run Chrome in headless mode
    """
    search_url = f"https://www.google.com/travel/flights?q=Flights%20to%20{destination}%20from%20{origin}%20on%20{date_str}%20oneway"
    print(f"\n[1/4] Launching search for {origin} -> {destination} on {date_str}...")
    print(f"      URL: {search_url}")

    driver = create_driver(headless=headless)
    flights = []

    try:
        if not headless:
            print("      [Mode] VISIBLE BROWSER: Chrome window is open on your screen.")
            print("      Observe Google Flights loading the route and date...")

        driver.get(search_url)
        # Allow dynamic cards and prices to settle
        time.sleep(5)

        # Smooth scrolling to show the user how elements load
        print("      Scrolling through flight results...")
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight / 3, behavior: 'smooth'});")
        time.sleep(2)
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight * 2 / 3, behavior: 'smooth'});")
        time.sleep(2)
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(2)

        if not headless:
            print("      Keeping browser open for 3 seconds so you can view the rendered cards...")
            time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Google Flights cards are list items with class pIav2d
        cards = soup.find_all('li', class_=lambda c: c and 'pIav2d' in str(c))
        print(f"[2/4] Found {len(cards)} raw flight cards on page.")

        for card in cards:
            link_div = card.find('div', class_='JMc5Xc')
            if not link_div or not link_div.get('aria-label'):
                continue

            label = link_div['aria-label'].replace('\u202f', ' ').replace('\xa0', ' ')

            # 1. Price
            price_m = re.search(r'From\s+([\d,]+)\s+Indian rupees', label, re.IGNORECASE)
            price_val = int(price_m.group(1).replace(',', '')) if price_m else None

            # 2. Stops and Airline
            flight_m = re.search(r'(\d+\s*stop[s]?|Nonstop)\s+flight\s+with\s+([^.]+)\.', label, re.IGNORECASE)
            stops = flight_m.group(1).strip() if flight_m else "Nonstop"
            airline = flight_m.group(2).strip() if flight_m else "Unknown Airline"

            # 3. Departure & Arrival Times & Airports
            leaves_m = re.search(r'Leaves\s+(.+?)\s+at\s+(\d{1,2}:\d{2}\s*[APMapm]{2})\s+on\s+(.+?)\s+and arrives at\s+(.+?)\s+at\s+(\d{1,2}:\d{2}\s*[APMapm]{2})\s+on\s+(.+?)\.', label, re.IGNORECASE)
            
            # 4. Total Duration
            dur_m = re.search(r'Total duration\s+([^.]+)\.', label, re.IGNORECASE)
            duration = dur_m.group(1).strip() if dur_m else "N/A"

            if price_val and leaves_m:
                flight_record = {
                    "airline": airline,
                    "source": origin.upper(),
                    "source_airport": leaves_m.group(1).strip(),
                    "departure_time": leaves_m.group(2).strip(),
                    "departure_date": leaves_m.group(3).strip(),
                    "destination": destination.upper(),
                    "destination_airport": leaves_m.group(4).strip(),
                    "arrival_time": leaves_m.group(5).strip(),
                    "arrival_date": leaves_m.group(6).strip(),
                    "duration": duration,
                    "stops": stops,
                    "price_inr": price_val,
                    "search_date": date_str
                }
                flights.append(flight_record)

        print(f"[3/4] Successfully parsed {len(flights)} validated flight records.")

    finally:
        driver.quit()

    return flights

def save_results(flights: list[dict], csv_path: str = "flights_data.csv", json_path: str = "flights_data.json"):
    """Saves parsed flights to both CSV and JSON formats."""
    if not flights:
        print("No flight records to save.")
        return

    # 1. Save CSV
    keys = list(flights[0].keys())
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(flights)
    print(f"[4/4] Saved {len(flights)} rows to CSV: {csv_path}")

    # 2. Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(flights, f, indent=2, ensure_ascii=False)
    print(f"      Saved JSON backup: {json_path}")

def print_summary(flights: list[dict]):
    """Prints a neat analytical summary table of the scraped flights."""
    if not flights:
        return

    prices = [f['price_inr'] for f in flights if f.get('price_inr')]
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    avg_price = int(sum(prices) / len(prices)) if prices else 0

    airlines = {}
    for f in flights:
        a = f['airline']
        airlines[a] = airlines.get(a, 0) + 1

    print("\n" + "=" * 65)
    print("                AIR FARE SCRAPING SUMMARY")
    print("=" * 65)
    print(f"Total Flights Found : {len(flights)}")
    print(f"Lowest Fare         : INR {min_price:,}")
    print(f"Average Fare        : INR {avg_price:,}")
    print(f"Highest Fare        : INR {max_price:,}")
    print("\nAirlines Breakdown:")
    for a, count in sorted(airlines.items(), key=lambda x: x[1], reverse=True):
        print(f"  * {a:20}: {count} flights")
    
    print("\nSample Flight Records (Top 3):")
    print("-" * 65)
    for i, f in enumerate(flights[:3], 1):
        print(f"[{i}] {f['airline']} | {f['source']} ({f['departure_time']}) -> {f['destination']} ({f['arrival_time']}) | {f['duration']} | {f['stops']} | INR {f['price_inr']:,}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    # Default to 2 days ahead if no date provided
    default_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser(description="Air Fare Prediction (AFP) Flight Scraper")
    parser.add_argument("--origin", default="DEL", help="Origin airport code (default: DEL)")
    parser.add_argument("--destination", default="BOM", help="Destination airport code (default: BOM)")
    parser.add_argument("--date", default=default_date, help=f"Flight date YYYY-MM-DD (default: {default_date})")
    parser.add_argument("--csv", default="flights_data.csv", help="Output CSV filepath")
    parser.add_argument("--json", default="flights_data.json", help="Output JSON filepath")
    parser.add_argument("--visible", action="store_true", help="Run browser visibly instead of headless")

    args = parser.parse_args()

    results = scrape_flights(
        origin=args.origin,
        destination=args.destination,
        date_str=args.date,
        headless=not args.visible
    )

    save_results(results, csv_path=args.csv, json_path=args.json)
    print_summary(results)
