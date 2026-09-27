"""
Visualization Module for CPI Airfare Price Index.
Generates publication-quality charts for project reports and presentations.
"""

import os
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend safe for scripts
import matplotlib.pyplot as plt
import pandas as pd




def plot_daily_cpi_trend(daily_df: pd.DataFrame, output_dir: str = "data/plots") -> str:
    """
    Plots the inter-temporal CPI Airfare Index trend across observation days.
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "daily_cpi_airfare_trend.png")

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

    dates = daily_df["observation_date"].tolist()
    dutot = daily_df["dutot_index"].tolist()
    jevons = daily_df["jevons_index"].tolist()
    weighted = daily_df["carrier_weighted_index"].tolist()

    ax.plot(dates, dutot, marker="o", linewidth=2, label="Dutot Index (Arithmetic Mean)")
    ax.plot(dates, jevons, marker="^", linewidth=2, label="Jevons Index (Geometric Mean)")
    ax.plot(dates, weighted, marker="s", linewidth=2.5, color="#2ca02c", label="DGCA Carrier-Weighted Index")

    # Baseline 100 line
    ax.axhline(100.0, color="gray", linestyle=":", linewidth=1.5, label="Base Period (100.0)")

    ax.set_title("Inter-Temporal Real-Time Airfare Price Index (CPI Sub-Index)", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Observation Date (t)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_ylabel("Price Index (Base Day = 100.0)", fontsize=11, fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="best", framealpha=0.9)

    fig.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()
    return filepath


def plot_carrier_comparison(carrier_df: pd.DataFrame, output_dir: str = "data/plots") -> str:
    """
    Plots airline price comparison only for airlines that have flights on the route.
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "carrier_price_comparison.png")

    # Aggregate by carrier and filter out zero-flight / zero-price carriers
    summary = carrier_df.groupby("carrier_group").agg(
        avg_price=("avg_price", "mean"),
        total_flights=("total_flights", "sum")
    ).reset_index()

    summary = summary[(summary["avg_price"] > 0) & (summary["total_flights"] > 0)].sort_values(by="total_flights", ascending=False)

    if summary.empty:
        summary = carrier_df.groupby("carrier_group")["avg_price"].mean().reset_index()

    carrier_names = summary["carrier_group"].tolist()
    avg_prices = summary["avg_price"].tolist()

    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    color_palette = {
        "IndiGo": "#2563eb",
        "Air India": "#dc2626",
        "Akasa Air": "#ea580c",
        "SpiceJet": "#9333ea",
        "Others": "#0284c7"
    }
    colors = [color_palette.get(c, "#2563eb") for c in carrier_names]
    bars = ax.bar(carrier_names, avg_prices, color=colors, width=0.45, edgecolor="#cbd5e1")

    ax.set_title("Average Domestic Airfare by Active Airline Carrier (DEL -> HYD)", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Airline Carrier", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_ylabel("Mean Airfare (INR)", fontsize=11, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Bar annotations
    for bar, p in zip(bars, avg_prices):
        if p > 0:
            ax.annotate(f"Rs. {p:,.0f}", xy=(bar.get_x() + bar.get_width() / 2, p),
                        xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")

    fig.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()
    return filepath

