"""
Base Scraper module providing date calculation, headers, and standardization.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any


def get_target_horizons(base_date: datetime = None) -> List[Dict[str, Any]]:
    """
    Computes the target horizons: t+1, t+7, t+15, and t+30 from the base date.
    
    Returns a list of dicts with horizon labels, day offsets, and formatted date strings.
    """
    if base_date is None:
        base_date = datetime.now()

    horizons = [
        {"horizon": "t+1", "days": 1},
        {"horizon": "t+7", "days": 7},
        {"horizon": "t+15", "days": 15},
        {"horizon": "t+30", "days": 30},
    ]

    target_dates = []
    for h in horizons:
        target_date = base_date + timedelta(days=h["days"])
        target_dates.append({
            "horizon": h["horizon"],
            "horizon_days": h["days"],
            "date_obj": target_date,
            "iso_date": target_date.strftime("%Y-%m-%d"),
            "display_date": target_date.strftime("%d/%m/%Y"),
            "emt_date": target_date.strftime("%d/%m/%Y"),  # DD/MM/YYYY for EaseMyTrip
            "day_name": target_date.strftime("%A"),
        })

    return target_dates


def get_default_headers() -> Dict[str, str]:
    """
    Returns standard HTTP headers to mimic modern desktop browser requests.
    """
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }
