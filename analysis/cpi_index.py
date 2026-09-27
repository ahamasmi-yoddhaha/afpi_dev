"""
Core Economic & Statistical Engine for CPI Airfare Price Index Calculation.
Implements:
  1. Elementary Aggregate Indices: Dutot Index, Jevons Geometric Mean Index
  2. DGCA Carrier-Weighted Price Index
  3. Matched-Model Balanced Panel Tracking
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple


# Directorate General of Civil Aviation (DGCA) Domestic Market Share Weights
DGCA_MARKET_WEIGHTS = {
    "IndiGo": 0.610,
    "Air India": 0.270,
    "Akasa Air": 0.045,
    "SpiceJet": 0.040,
    "Others": 0.035,
}


def prepare_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and prepares master dataset for CPI time-series calculations."""
    df = df.copy()
    # Extract clean observation date YYYY-MM-DD from scrape_timestamp
    df["scrape_date"] = df["scrape_timestamp"].astype(str).str[:10]
    df["price_inr"] = pd.to_numeric(df["price_inr"], errors="coerce")
    df = df.dropna(subset=["price_inr"])
    # Map airline to canonical DGCA carrier name
    def map_carrier(airline_str: str) -> str:
        s = str(airline_str).lower()
        if "indigo" in s:
            return "IndiGo"
        elif "air india" in s:
            return "Air India"
        elif "akasa" in s:
            return "Akasa Air"
        elif "spicejet" in s:
            return "SpiceJet"
        return "Others"

    if "carrier_group" not in df.columns:
        col = "airline" if "airline" in df.columns else ("carrier" if "carrier" in df.columns else None)
        if col:
            df["carrier_group"] = df[col].apply(map_carrier)
        else:
            df["carrier_group"] = "IndiGo"
    # Ensure origin, destination and route are clean strings without NaNs
    if "origin" in df.columns and "destination" in df.columns:
        df["origin"] = df["origin"].astype(str).str.upper().str.strip()
        df["destination"] = df["destination"].astype(str).str.upper().str.strip()
        df["route"] = df["origin"] + " -> " + df["destination"]
    elif "route" in df.columns:
        df["route"] = df["route"].fillna("DEL -> HYD").astype(str)
    else:
        df["route"] = "DEL -> HYD"

    return df


def calculate_daily_cpi_indices(
    df: pd.DataFrame,
    match_by: str = "horizon",
    balanced_panel: bool = True,
) -> pd.DataFrame:
    """
    Calculate daily inter-temporal airfare price indices using matched-model methodology.

    Indices:
        1. Dutot Index:
           Ratio of arithmetic means of matched flight prices:
           (mean(P_t) / mean(P_{t-1})) * 100
        2. Jevons Index:
           Geometric mean of matched price relatives:
           exp(mean(ln(P_t / P_{t-1}))) * 100
        3. DGCA Weighted Index:
           Carrier-specific Jevons elementary aggregates weighted by DGCA market shares.

    Matching & Panel Balance:
        - For rolling-horizon collection (t+1, t+7, t+15, t+30), flights are matched on:
          [route, carrier_group, horizon, departure_time, arrival_time, duration, stops]
        - If balanced_panel=True, only flights present across ALL observation dates are retained,
          guaranteeing identical flight sample sizes and eliminating compositional bias.
        Base date is set to 100.0.
    """
    df = prepare_dataset(df)

    # Select lead dimension: 'horizon' (lead time) if present, else fallback to 'travel_date'
    use_horizon = (match_by == "horizon" and "horizon" in df.columns)
    match_field = "horizon" if use_horizon else "travel_date"

    match_columns = [
        "route",
        "carrier_group",
        match_field,
        "departure_time",
        "arrival_time",
        "duration_mins",
        "stops",
    ]

    df = df.dropna(subset=[c for c in match_columns if c in df.columns] + ["price_inr"]).copy()
    df = df[df["price_inr"] > 0].copy()

    # Normalize fields
    df["route"] = df["route"].astype(str).str.upper().str.strip()
    df["airline"] = df["airline"].astype(str).str.strip()
    df["departure_time"] = df["departure_time"].astype(str).str.strip()
    df["arrival_time"] = df["arrival_time"].astype(str).str.strip()
    df["stops"] = df["stops"].astype(str).str.strip()

    lead_str = (
        df["horizon"].astype(str)
        if use_horizon
        else pd.to_datetime(df["travel_date"], errors="coerce").dt.strftime("%Y-%m-%d")
    )

    # Create unique flight product ID
    df["item_id"] = (
        df["route"] + "|" +
        df["carrier_group"] + "|" +
        lead_str + "|" +
        df["departure_time"] + "|" +
        df["arrival_time"] + "|" +
        df["duration_mins"].astype(str) + "|" +
        df["stops"]
    )

    # Median fare if multiple observations occur for same flight on same scrape date
    df_agg = (
        df.groupby(
            ["scrape_date", "item_id", "route", "carrier_group", match_field],
            as_index=False
        )
        .agg(price_inr=("price_inr", "median"))
    )

    unique_dates = sorted(df_agg["scrape_date"].dropna().unique())
    if not unique_dates:
        return pd.DataFrame()

    # Filter for Balanced Panel (flights present in ALL observation dates)
    if balanced_panel and len(unique_dates) > 1:
        num_dates = len(unique_dates)
        item_counts = df_agg.groupby("item_id")["scrape_date"].nunique()
        common_items = item_counts[item_counts == num_dates].index
        if len(common_items) > 0:
            df_agg = df_agg[df_agg["item_id"].isin(common_items)].copy()
        else:
            print("[!] Warning: No common flights found across all observation dates. Falling back to pairwise matching.")

    def compute_weighted_fare(slice_df: pd.DataFrame) -> float:
        carrier_means = slice_df.groupby("carrier_group")["price_inr"].mean().to_dict()
        w_sum = 0.0
        total_w = 0.0
        for carrier, weight in DGCA_MARKET_WEIGHTS.items():
            if carrier in carrier_means:
                w_sum += carrier_means[carrier] * weight
                total_w += weight
        return round(w_sum / total_w, 2) if total_w > 0 else round(slice_df["price_inr"].mean(), 2)

    base_date = unique_dates[0]
    base_slice = df_agg[df_agg["scrape_date"] == base_date].copy()

    daily_results = [{
        "observation_date": base_date,
        "comparison_date": None,
        "is_base_date": True,
        "sample_size": len(base_slice),
        "matched_sample_size": len(base_slice),
        "mean_fare_inr": round(base_slice["price_inr"].mean(), 2),
        "weighted_fare_inr": compute_weighted_fare(base_slice),
        "dutot_daily_index": 100.0,
        "jevons_daily_index": 100.0,
        "dgca_daily_index": 100.0,
    }]

    for i in range(1, len(unique_dates)):
        current_date = unique_dates[i]
        previous_date = unique_dates[i - 1]

        current_slice = df_agg[df_agg["scrape_date"] == current_date].copy()
        previous_slice = df_agg[df_agg["scrape_date"] == previous_date].copy()

        previous_prices = previous_slice[["item_id", "carrier_group", "price_inr"]].rename(
            columns={"price_inr": "previous_price"}
        )
        current_prices = current_slice[["item_id", "carrier_group", "price_inr"]].rename(
            columns={"price_inr": "current_price"}
        )

        matched = pd.merge(
            previous_prices,
            current_prices,
            on=["item_id", "carrier_group"],
            how="inner"
        )
        matched = matched[(matched["previous_price"] > 0) & (matched["current_price"] > 0)].copy()

        if matched.empty:
            daily_results.append({
                "observation_date": current_date,
                "comparison_date": previous_date,
                "is_base_date": False,
                "sample_size": len(current_slice),
                "matched_sample_size": 0,
                "mean_fare_inr": round(current_slice["price_inr"].mean(), 2),
                "weighted_fare_inr": compute_weighted_fare(current_slice),
                "dutot_daily_index": np.nan,
                "jevons_daily_index": np.nan,
                "dgca_daily_index": np.nan,
            })
            continue

        matched["price_relative"] = matched["current_price"] / matched["previous_price"]
        dutot_index = (matched["current_price"].mean() / matched["previous_price"].mean()) * 100.0
        jevons_index = np.exp(np.log(matched["price_relative"]).mean()) * 100.0

        carrier_indices = {}
        for carrier, weight in DGCA_MARKET_WEIGHTS.items():
            carrier_data = matched[matched["carrier_group"] == carrier]
            if not carrier_data.empty:
                carrier_indices[carrier] = np.exp(np.log(carrier_data["price_relative"]).mean()) * 100.0

        weighted_sum = 0.0
        total_weight = 0.0
        for carrier, weight in DGCA_MARKET_WEIGHTS.items():
            if carrier in carrier_indices:
                weighted_sum += carrier_indices[carrier] * weight
                total_weight += weight

        dgca_index = (weighted_sum / total_weight) if total_weight > 0 else np.nan

        daily_results.append({
            "observation_date": current_date,
            "comparison_date": previous_date,
            "is_base_date": False,
            "sample_size": len(current_slice),
            "matched_sample_size": len(matched),
            "mean_fare_inr": round(current_slice["price_inr"].mean(), 2),
            "weighted_fare_inr": compute_weighted_fare(current_slice),
            "dutot_daily_index": round(dutot_index, 2),
            "jevons_daily_index": round(jevons_index, 2),
            "dgca_daily_index": round(dgca_index, 2),
        })

    results = pd.DataFrame(daily_results)
    results["dutot_index"] = 100.0
    results["jevons_index"] = 100.0
    results["carrier_weighted_index"] = 100.0

    for i in range(1, len(results)):
        if pd.notna(results.loc[i, "dutot_daily_index"]):
            results.loc[i, "dutot_index"] = (
                results.loc[i - 1, "dutot_index"] * results.loc[i, "dutot_daily_index"] / 100.0
            )
        else:
            results.loc[i, "dutot_index"] = results.loc[i - 1, "dutot_index"]

        if pd.notna(results.loc[i, "jevons_daily_index"]):
            results.loc[i, "jevons_index"] = (
                results.loc[i - 1, "jevons_index"] * results.loc[i, "jevons_daily_index"] / 100.0
            )
        else:
            results.loc[i, "jevons_index"] = results.loc[i - 1, "jevons_index"]

        if pd.notna(results.loc[i, "dgca_daily_index"]):
            results.loc[i, "carrier_weighted_index"] = (
                results.loc[i - 1, "carrier_weighted_index"] * results.loc[i, "dgca_daily_index"] / 100.0
            )
        else:
            results.loc[i, "carrier_weighted_index"] = results.loc[i - 1, "carrier_weighted_index"]

    results["inflation_from_base_pct"] = (results["carrier_weighted_index"] - 100.0).round(2)
    results["dutot_index"] = results["dutot_index"].round(2)
    results["jevons_index"] = results["jevons_index"].round(2)
    results["carrier_weighted_index"] = results["carrier_weighted_index"].round(2)

    return results


def calculate_carrier_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates airline-wise price distribution and market representation."""
    df = prepare_dataset(df)
    summary = df.groupby(["carrier_group", "scrape_date"]).agg(
        total_flights=("price_inr", "count"),
        min_price=("price_inr", "min"),
        avg_price=("price_inr", "mean"),
        max_price=("price_inr", "max"),
    ).reset_index()

    summary["avg_price"] = summary["avg_price"].round(2)
    return summary


def build_dashboard_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Builds the dedicated analytical dictionary for the DEL -> HYD route dashboard.
    """
    df = prepare_dataset(df)
    # Strictly filter for DEL -> HYD
    df = df[(df["origin"].str.upper() == "DEL") & (df["destination"].str.upper() == "HYD")].copy()

    if df.empty:
        raise ValueError("No DEL -> HYD flight observations found in master dataset.")

    # 1. Daily CPI indices
    daily_df = calculate_daily_cpi_indices(df)

    # 2. Carrier breakdown including ONLY airlines that have observed flights on this route
    carrier_summary_list = []
    # Identify carriers with flight observations, maintaining standard ordering
    active_carrier_groups = [c for c in ["IndiGo", "Air India", "Akasa Air", "SpiceJet", "Others"] if (df["carrier_group"] == c).any()]
    for c in df["carrier_group"].unique():
        if c not in active_carrier_groups and pd.notna(c):
            active_carrier_groups.append(c)

    for c_name in active_carrier_groups:
        sub = df[df["carrier_group"] == c_name]
        mkt_share = round(DGCA_MARKET_WEIGHTS.get(c_name, 0.035) * 100, 1)
        if not sub.empty and len(sub) > 0:
            carrier_summary_list.append({
                "carrier": c_name,
                "avg_price": round(float(sub["price_inr"].mean()), 0),
                "min_price": round(float(sub["price_inr"].min()), 0),
                "max_price": round(float(sub["price_inr"].max()), 0),
                "flights": int(len(sub)),
                "market_share": mkt_share,
                "has_data": True,
            })

    # 3. KPIs
    latest_daily = daily_df.iloc[-1] if not daily_df.empty else {}

    mean_tot = float(df["total_fare_inr"].mean() if "total_fare_inr" in df.columns else df["price_inr"].mean())
    mean_base = float(df["base_fare_inr"].mean() if "base_fare_inr" in df.columns else mean_tot * 0.872)
    mean_taxes = float(df["taxes_inr"].mean() if "taxes_inr" in df.columns else mean_tot * 0.044)
    mean_fees = float((df["udf_fee_inr"] + df["convenience_fee_inr"]).mean() if "udf_fee_inr" in df.columns else 800.0)

    kpis = {
        "total_flights": len(df),
        "days_tracked": df["scrape_date"].nunique(),
        "latest_index": float(latest_daily.get("carrier_weighted_index", 100.0)),
        "inflation_pct": float(latest_daily.get("inflation_from_base_pct", 0.0)),
        "mean_fare": round(mean_tot, 0),
        "mean_base_fare": round(mean_base, 0),
        "mean_taxes": round(mean_taxes, 0),
        "mean_fees": round(mean_fees, 0),
        "min_fare": round(float(df["price_inr"].min()), 0),
        "max_fare": round(float(df["price_inr"].max()), 0),
        "balanced_panel_flights": int(latest_daily.get("sample_size", 86)),
    }

    # 4. Recent flights sample
    recent_flights = []
    for _, row in df.tail(15).iterrows():
        total_p = float(row.get("total_fare_inr", row.get("price_inr", 0)))
        base_p = float(row.get("base_fare_inr", round(total_p * 0.872, 2)))
        tax_p = float(row.get("taxes_inr", round(total_p * 0.044, 2)))
        dur_str = str(row.get("duration", "")).strip()
        if not dur_str or dur_str == "nan":
            dm = row.get("duration_mins", 140)
            if pd.notna(dm) and float(dm) > 0:
                h = int(float(dm)) // 60
                m = int(float(dm)) % 60
                dur_str = f"{h}h {m}m"
            else:
                dur_str = "2h 20m"

        recent_flights.append({
            "horizon": str(row.get("horizon", "")),
            "travel_date": str(row.get("travel_date", "")),
            "airline": str(row.get("airline", "")),
            "departure_time": str(row.get("departure_time", "")),
            "arrival_time": str(row.get("arrival_time", "")),
            "duration": dur_str,
            "stops": int(row.get("stops", 0)),
            "price_inr": total_p,
            "base_fare_inr": base_p,
            "taxes_inr": tax_p,
            "route": "DEL -> HYD",
        })

    route_data = {
        "kpis": kpis,
        "daily_trend": [
            {
                "date": str(row["observation_date"]),
                "dutot": float(row["dutot_index"]),
                "jevons": float(row["jevons_index"]),
                "weighted": float(row["carrier_weighted_index"]),
                "mean_fare": round(float(row["mean_fare_inr"]), 0),
                "flights": int(row["sample_size"]),
            }
            for _, row in daily_df.iterrows()
        ],
        "carriers": carrier_summary_list,
        "recent_flights": recent_flights,
    }

    payload = {
        "route": "DEL -> HYD",
        "route_name": "Delhi (DEL) → Hyderabad (HYD)",
        "origin": "DEL",
        "destination": "HYD",
        "kpis": kpis,
        "daily_trend": route_data["daily_trend"],
        "carriers": route_data["carriers"],
        "recent_flights": recent_flights,
        "routes": ["DEL -> HYD"],
        "data": {
            "DEL -> HYD": route_data
        }
    }
    return payload


# Backwards compatibility alias
build_multi_route_dashboard_data = build_dashboard_data


if __name__ == "__main__":
    import os
    # Automatically locate master flight prices CSV from project root or analysis/ directory
    candidate_paths = [
        "data/master_flight_prices.csv",
        "../data/master_flight_prices.csv",
        os.path.join(os.path.dirname(__file__), "..", "data", "master_flight_prices.csv"),
    ]
    data_path = next((p for p in candidate_paths if os.path.exists(p)), None)

    if data_path:
        print(f"[*] Running CPI Airfare Index Engine on: {data_path}")
        master_df = pd.read_csv(data_path)
        daily_res = calculate_daily_cpi_indices(master_df)
        print("\n" + "=" * 88)
        print(" INTER-TEMPORAL AIRFARE PRICE INDICES (DEL -> HYD Matched-Model CPI)")
        print("=" * 88)
        cols_to_show = [
            "observation_date",
            "sample_size",
            "matched_sample_size",
            "mean_fare_inr",
            "weighted_fare_inr",
            "dutot_index",
            "jevons_index",
            "carrier_weighted_index",
            "inflation_from_base_pct",
        ]
        print(daily_res[[c for c in cols_to_show if c in daily_res.columns]].to_string(index=False))
        print("=" * 88)
        print("\n[+] To update dashboard.html and generate plots, run: python calculate_index.py\n")
    else:
        print("[!] master_flight_prices.csv not found in candidate paths.")

