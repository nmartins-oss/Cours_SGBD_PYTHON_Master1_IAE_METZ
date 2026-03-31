# =============================================================================
# SCRIPT 03 — COMPUTE DAILY RETURNS
# =============================================================================
# Purpose: Calculate the daily percentage return for each stock.
#          Daily returns are the building block of all VaR calculations.
#
# Formula: return(t) = [Price(t) - Price(t-1)] / Price(t-1)
#          Or equivalently using logarithms: log(Price(t) / Price(t-1))
#
# We use simple percentage returns (not log returns) for simplicity.
# For a 1-day horizon, both methods give very similar results.
#
# Input:   DATA/prices_clean.csv
# Output:  DATA/returns.csv — daily returns for each stock
# =============================================================================

import pandas as pd
import os

# -----------------------------------------------------------------------------
# STEP 1 — Load the clean price data
# -----------------------------------------------------------------------------
script_dir  = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir    = os.path.join(project_dir, "DATA")

prices = pd.read_csv(
    os.path.join(data_dir, "prices_clean.csv"),
    index_col  = 0,
    parse_dates= True
)

print("Price data loaded.")
print(f"Stocks: {list(prices.columns)}")
print()

# -----------------------------------------------------------------------------
# STEP 2 — Compute daily percentage returns
# -----------------------------------------------------------------------------
# pct_change() computes (Price_today - Price_yesterday) / Price_yesterday
# The first row will be NaN because there is no previous day — we drop it.

returns = prices.pct_change()   # daily percentage changes
returns = returns.dropna()      # remove the first row which is NaN

print(f"Returns computed: {returns.shape[0]} daily observations")
print()

# -----------------------------------------------------------------------------
# STEP 3 — Display basic statistics on returns
# -----------------------------------------------------------------------------
print("=" * 60)
print("DESCRIPTIVE STATISTICS ON DAILY RETURNS")
print("=" * 60)
print(returns.describe().round(4))
print()

# Highlight the minimum and maximum return for each stock
print("=" * 60)
print("WORST DAY (minimum return) per stock:")
print("=" * 60)
print(returns.min().round(4))
print()

print("=" * 60)
print("BEST DAY (maximum return) per stock:")
print("=" * 60)
print(returns.max().round(4))
print()

# -----------------------------------------------------------------------------
# STEP 4 — Save the returns to CSV
# -----------------------------------------------------------------------------
output_path = os.path.join(data_dir, "returns.csv")
returns.to_csv(output_path)

print(f"Returns saved to: {output_path}")
print("Script 03 complete.")
