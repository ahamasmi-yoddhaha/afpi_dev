"""
Database module for persistent storage, de-duplication, and indexing
of raw airfare price quotes in SQLite.
"""

import sqlite3
import pandas as pd
from datetime import datetime
from config import DB_PATH

def get_connection():
    """Returns a connection to the SQLite warehouse database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode = WAL;")  # Fast concurrent writes
    return conn

def init_db():
    """Initializes the SQLite database schema and analytical indexes."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_airfare_quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scrape_timestamp TEXT NOT NULL,
                booking_date TEXT NOT NULL,
                travel_date TEXT NOT NULL,
                advance_window TEXT NOT NULL,
                lead_time_days INTEGER NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                sector TEXT NOT NULL,
                carrier TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                duration_mins INTEGER,
                duration_str TEXT,
                stops TEXT,
                stops_count INTEGER,
                fare_class TEXT DEFAULT 'Economy',
                total_fare REAL NOT NULL,
                source_portal TEXT DEFAULT 'Aggregator/Multi-Source',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(booking_date, travel_date, sector, carrier, departure_time, total_fare)
            );
        """)

        # Performance and analytical querying indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sector_travel ON raw_airfare_quotes (sector, travel_date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_window_lead ON raw_airfare_quotes (advance_window, lead_time_days);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_booking_carrier ON raw_airfare_quotes (booking_date, carrier);")
        conn.commit()

def insert_quotes(quotes: list[dict]) -> int:
    """Inserts a batch of flight quotes with automatic de-duplication.
    
    Returns:
        Number of new records inserted.
    """
    if not quotes:
        return 0

    init_db()
    inserted_count = 0

    query = """
        INSERT OR IGNORE INTO raw_airfare_quotes (
            scrape_timestamp, booking_date, travel_date, advance_window, lead_time_days,
            origin, destination, sector, carrier, departure_time, arrival_time,
            duration_mins, duration_str, stops, stops_count, fare_class, total_fare, source_portal
        ) VALUES (
            :scrape_timestamp, :booking_date, :travel_date, :advance_window, :lead_time_days,
            :origin, :destination, :sector, :carrier, :departure_time, :arrival_time,
            :duration_mins, :duration_str, :stops, :stops_count, :fare_class, :total_fare, :source_portal
        );
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany(query, quotes)
        inserted_count = cursor.rowcount
        conn.commit()

    return inserted_count

def export_to_csv(output_csv_path: str, booking_date: str = None) -> int:
    """Exports data from SQLite to a CSV file.
    
    If booking_date is provided (YYYY-MM-DD), exports records for that day only.
    Otherwise exports the entire database.
    """
    with get_connection() as conn:
        if booking_date:
            df = pd.read_sql_query(
                "SELECT * FROM raw_airfare_quotes WHERE booking_date = ? ORDER BY sector, advance_window, total_fare ASC",
                conn,
                params=(booking_date,)
            )
        else:
            df = pd.read_sql_query(
                "SELECT * FROM raw_airfare_quotes ORDER BY booking_date DESC, sector, advance_window ASC",
                conn
            )
            
    df.to_csv(output_csv_path, index=False, encoding='utf-8')
    return len(df)

def get_stats() -> dict:
    """Returns database summary statistics."""
    init_db()
    with get_connection() as conn:
        total_quotes = conn.execute("SELECT COUNT(*) FROM raw_airfare_quotes;").fetchone()[0]
        sectors = conn.execute("SELECT COUNT(DISTINCT sector) FROM raw_airfare_quotes;").fetchone()[0]
        dates = conn.execute("SELECT COUNT(DISTINCT booking_date) FROM raw_airfare_quotes;").fetchone()[0]
        carriers = conn.execute("SELECT carrier, COUNT(*) FROM raw_airfare_quotes GROUP BY carrier;").fetchall()

    return {
        "total_quotes": total_quotes,
        "unique_sectors": sectors,
        "booking_dates": dates,
        "carrier_breakdown": dict(carriers),
    }

if __name__ == "__main__":
    init_db()
    print("Database initialized at:", DB_PATH)
    print("Current Stats:", get_stats())
