# =============================================================================
# SCRIPT 06 — VISUALIZATIONS
# =============================================================================
# Purpose: Create clear, academic charts for the presentation.
#          Each chart is saved as a PNG file in the DATA/ folder.
#
# Charts produced:
#   1. Stock price evolution (normalized to 100)
#   2. Portfolio daily returns over time
#   3. Histogram of portfolio returns + VaR lines
#   4. Bar chart comparing the three VaR methods
#
# Input:  DATA/prices_clean.csv, DATA/portfolio_returns.csv, DATA/var_results.csv
# Output: DATA/chart_01_prices.png
#         DATA/chart_02_portfolio_returns.png
#         DATA/chart_03_histogram_var.png
#         DATA/chart_04_var_comparison.png
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# -----------------------------------------------------------------------------
# Setup paths
# -----------------------------------------------------------------------------
script_dir  = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir    = os.path.join(project_dir, "DATA")

# Load the data
prices           = pd.read_csv(os.path.join(data_dir, "prices_clean.csv"),
                                index_col=0, parse_dates=True)
portfolio_returns = pd.read_csv(os.path.join(data_dir, "portfolio_returns.csv"),
                                 index_col=0, parse_dates=True).squeeze()
var_results       = pd.read_csv(os.path.join(data_dir, "var_results.csv"))

# Extract VaR values by method name (as negative numbers for loss representation)
var_hist  = var_results.loc[var_results["Method"] == "Historical",  "VaR_decimal"].values[0]
var_param = var_results.loc[var_results["Method"] == "Parametric",  "VaR_decimal"].values[0]
var_mc    = var_results.loc[var_results["Method"] == "Monte Carlo", "VaR_decimal"].values[0]

print("Data loaded. Generating charts...")

# Use a clean academic style
plt.style.use("seaborn-v0_8-whitegrid")
COLORS = ["#2196F3", "#FF5722", "#4CAF50", "#FF9800", "#9C27B0"]

# =============================================================================
# CHART 1 — Normalized stock price evolution
# =============================================================================
# We normalize prices to 100 at the start so all stocks can be compared
# on the same scale, regardless of their actual price.

fig, ax = plt.subplots(figsize=(12, 6))

for i, ticker in enumerate(prices.columns):
    # Normalize: divide by the first price, multiply by 100
    normalized = prices[ticker] / prices[ticker].iloc[0] * 100
    ax.plot(normalized.index, normalized, label=ticker, color=COLORS[i], linewidth=1.5)

ax.axhline(y=100, color="black", linestyle="--", linewidth=0.8, alpha=0.5,
           label="Starting value (100)")
ax.set_title("Stock Price Evolution (Normalized to 100 at Start)", fontsize=14, fontweight="bold")
ax.set_xlabel("Date", fontsize=11)
ax.set_ylabel("Indexed Price (Base = 100)", fontsize=11)
ax.legend(loc="upper left", fontsize=10)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f"))

plt.tight_layout()
chart1_path = os.path.join(data_dir, "chart_01_prices.png")
plt.savefig(chart1_path, dpi=150)
plt.close()
print(f"Chart 1 saved: {chart1_path}")

# =============================================================================
# CHART 2 — Portfolio daily returns over time
# =============================================================================
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(portfolio_returns.index, portfolio_returns * 100,
        color="#2196F3", linewidth=0.8, alpha=0.9, label="Daily Return")
ax.axhline(y=0, color="black", linewidth=0.8)

# Mark the VaR threshold (Historical) as a horizontal dashed line
ax.axhline(y=var_hist * 100, color="red", linewidth=1.2, linestyle="--",
           label=f"Historical VaR 95% = {abs(var_hist)*100:.2f}%")

ax.set_title("Portfolio Daily Returns Over Time", fontsize=14, fontweight="bold")
ax.set_xlabel("Date", fontsize=11)
ax.set_ylabel("Daily Return (%)", fontsize=11)
ax.legend(fontsize=10)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))

plt.tight_layout()
chart2_path = os.path.join(data_dir, "chart_02_portfolio_returns.png")
plt.savefig(chart2_path, dpi=150)
plt.close()
print(f"Chart 2 saved: {chart2_path}")

# =============================================================================
# CHART 3 — Histogram of portfolio returns + VaR lines
# =============================================================================
fig, ax = plt.subplots(figsize=(12, 6))

# Draw the histogram
ax.hist(portfolio_returns * 100, bins=60, color="#90CAF9", edgecolor="white",
        alpha=0.85, label="Historical daily returns")

# Overlay a normal curve for comparison
x_range = np.linspace(portfolio_returns.min() * 100, portfolio_returns.max() * 100, 300)
mu_pct   = portfolio_returns.mean() * 100
std_pct  = portfolio_returns.std()  * 100
from scipy.stats import norm
normal_curve = norm.pdf(x_range, mu_pct, std_pct)
# Scale the curve to match histogram height
n_obs    = len(portfolio_returns)
bin_width = (portfolio_returns.max() - portfolio_returns.min()) * 100 / 60
ax.plot(x_range, normal_curve * n_obs * bin_width,
        color="#1565C0", linewidth=2, linestyle="-", label="Normal distribution fit")

# Draw VaR vertical lines
ax.axvline(x=var_hist  * 100, color="red",    linewidth=2, linestyle="-",
           label=f"Historical VaR = -{abs(var_hist)*100:.2f}%")
ax.axvline(x=var_param * 100, color="orange", linewidth=2, linestyle="--",
           label=f"Parametric VaR = -{abs(var_param)*100:.2f}%")
ax.axvline(x=var_mc    * 100, color="green",  linewidth=2, linestyle=":",
           label=f"Monte Carlo VaR = -{abs(var_mc)*100:.2f}%")

# Shade the left tail (worst 5%)
tail_threshold = var_hist * 100
ax.fill_betweenx([0, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 50],
                  portfolio_returns.min() * 100, tail_threshold,
                  alpha=0.15, color="red", label="5% tail (worst days)")

ax.set_title("Histogram of Portfolio Daily Returns with VaR Thresholds (95%)",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Daily Return (%)", fontsize=11)
ax.set_ylabel("Frequency (number of days)", fontsize=11)
ax.legend(fontsize=9, loc="upper left")

plt.tight_layout()
chart3_path = os.path.join(data_dir, "chart_03_histogram_var.png")
plt.savefig(chart3_path, dpi=150)
plt.close()
print(f"Chart 3 saved: {chart3_path}")

# =============================================================================
# CHART 4 — Bar chart comparing the three VaR methods
# =============================================================================
fig, ax = plt.subplots(figsize=(8, 5))

methods = ["Historical", "Parametric", "Monte Carlo"]
var_pct  = [abs(var_hist)*100, abs(var_param)*100, abs(var_mc)*100]
bar_colors = ["#EF5350", "#FFA726", "#66BB6A"]

bars = ax.bar(methods, var_pct, color=bar_colors, edgecolor="white",
              width=0.5, alpha=0.9)

# Add value labels on top of each bar
for bar, value in zip(bars, var_pct):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.02,
            f"{value:.2f}%",
            ha="center", va="bottom", fontsize=12, fontweight="bold")

ax.set_title("Comparison of 1-Day VaR at 95% Confidence Level",
             fontsize=14, fontweight="bold")
ax.set_ylabel("VaR — Maximum Expected Daily Loss (%)", fontsize=11)
ax.set_ylim(0, max(var_pct) * 1.3)
ax.set_xlabel("Method", fontsize=11)

plt.tight_layout()
chart4_path = os.path.join(data_dir, "chart_04_var_comparison.png")
plt.savefig(chart4_path, dpi=150)
plt.close()
print(f"Chart 4 saved: {chart4_path}")

print()
print("All charts generated successfully.")
print("Script 06 complete.")
