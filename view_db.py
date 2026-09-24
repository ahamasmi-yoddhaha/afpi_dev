"""
Utility script to inspect the SQLite schema, statistics, and records in airfare_warehouse.db.
Usage:
    python view_db.py                 # Displays schema, stats, and sample rows
    python view_db.py --limit 20      # Displays top 20 rows
    python view_db.py --query "SQL"   # Runs custom SQL query
"""

import argparse
import sqlite3
import pandas as pd
from config import DB_PATH

def inspect_database(limit: int = 5, custom_query: str = None):
    conn = sqlite3.connect(DB_PATH)
    
    if custom_query:
        print(f"\n--- EXECUTING CUSTOM QUERY: {custom_query} ---")
        df = pd.read_sql_query(custom_query, conn)
        print(df.to_string(index=False))
        conn.close()
        return

    print("=" * 75)
    print(f"      DATABASE INSPECTION: {DB_PATH.name}")
    print("=" * 75)

    # 1. TABLE SCHEMA
    print("\n[1] TABLE SCHEMA (raw_airfare_quotes):")
    schema_df = pd.read_sql_query("PRAGMA table_info(raw_airfare_quotes);", conn)
    print(schema_df[['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk']].to_string(index=False))

    # 2. INDEXES
    print("\n[2] INDEXES:")
    indexes_df = pd.read_sql_query("PRAGMA index_list(raw_airfare_quotes);", conn)
    print(indexes_df[['seq', 'name', 'unique']].to_string(index=False))

    # 3. SUMMARY METRICS
    print("\n[3] WAREHOUSE METRICS:")
    total = conn.execute("SELECT COUNT(*) FROM raw_airfare_quotes;").fetchone()[0]
    dates = conn.execute("SELECT COUNT(DISTINCT booking_date) FROM raw_airfare_quotes;").fetchone()[0]
    print(f"  * Total Quotes Stored : {total}")
    print(f"  * Booking Days Logged : {dates}")

    # Carrier Breakdown
    carrier_df = pd.read_sql_query("""
        SELECT 
            carrier, 
            COUNT(*) AS total_flights,
            MIN(total_fare) AS min_fare,
            ROUND(AVG(total_fare), 2) AS avg_fare,
            MAX(total_fare) AS max_fare
        FROM raw_airfare_quotes
        GROUP BY carrier
        ORDER BY total_flights DESC;
    """, conn)
    print("\n  Carrier Breakdown & Price Summary (INR):")
    print(carrier_df.to_string(index=False))

    # Advance Window Breakdown
    window_df = pd.read_sql_query("""
        SELECT 
            advance_window, 
            lead_time_days,
            COUNT(*) AS quotes_count,
            ROUND(AVG(total_fare), 2) AS avg_fare
        FROM raw_airfare_quotes
        GROUP BY advance_window, lead_time_days
        ORDER BY lead_time_days ASC;
    """, conn)
    print("\n  Advance Window Breakdown:")
    print(window_df.to_string(index=False))

    # 4. SAMPLE RECORDS
    print(f"\n[4] SAMPLE RECORDS (Top {limit}):")
    cols = ['sector', 'carrier', 'advance_window', 'departure_time', 'arrival_time', 'duration_str', 'stops', 'total_fare']
    sample_df = pd.read_sql_query(f"SELECT {', '.join(cols)} FROM raw_airfare_quotes LIMIT {limit};", conn)
    print(sample_df.to_string(index=False))
    print("=" * 75 + "\n")

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect airfare_warehouse.db")
    parser.add_argument("--limit", type=int, default=5, help="Number of sample records to show (default: 5)")
    parser.add_argument("--query", type=str, default=None, help="Execute a custom SQL query")
    args = parser.parse_args()

    inspect_database(limit=args.limit, custom_query=args.query)
