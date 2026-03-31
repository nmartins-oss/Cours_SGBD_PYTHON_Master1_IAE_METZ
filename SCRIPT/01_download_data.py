# =============================================================================
# SCRIPT 01 — DOWNLOAD DATA FROM YAHOO FINANCE
# =============================================================================
# Purpose: Download historical daily stock prices for our portfolio
#          using the yfinance library. Save the data to the DATA/ folder.
#
# Library used: yfinance (Yahoo Finance API wrapper)
# Output:       DATA/prices.csv — daily closing prices for all stocks
# =============================================================================

import yfinance as yf
import pandas as pd
import os

# -----------------------------------------------------------------------------
# STEP 1 — Define our portfolio
# -----------------------------------------------------------------------------
# We chose 5 large-cap US stocks from 5 different sectors.
# This gives us a simple but realistic diversified portfolio.

TICKERS = [
    "AAPL",   # Apple — Technology
    "JPM",    # JPMorgan Chase — Finance
    "JNJ",    # Johnson & Johnson — Healthcare
    "XOM",    # ExxonMobil — Energy
    "WMT",    # Walmart — Consumer Staples
]

# -----------------------------------------------------------------------------
# STEP 2 — Define the date range
# -----------------------------------------------------------------------------
# We use 5 years of daily data (2019 to 2024).
# This gives us approximately 1250 trading days — enough for statistics.

START_DATE = "2019-01-01"
END_DATE   = "2024-12-31"

# -----------------------------------------------------------------------------
# STEP 3 — Download data from Yahoo Finance
# -----------------------------------------------------------------------------
print("Downloading data from Yahoo Finance...")
print(f"Tickers : {TICKERS}")
print(f"Period  : {START_DATE} to {END_DATE}")
print()

# yf.download returns a DataFrame with multi-level columns.
# auto_adjust=True corrects prices for splits and dividends automatically.
raw_data = yf.download(
    tickers    = TICKERS,
    start      = START_DATE,
    end        = END_DATE,
    auto_adjust= True,   # Adjusts for splits and dividends
    progress   = True    # Shows a progress bar
)

# -----------------------------------------------------------------------------
# STEP 4 — Keep only the "Close" prices
# -----------------------------------------------------------------------------
# We only need the daily closing price for each stock.
# After auto_adjust=True, "Close" already reflects dividend-adjusted prices.

prices = raw_data["Close"]

print()
print("Data downloaded successfully!")
print(f"Shape: {prices.shape[0]} rows (trading days) x {prices.shape[1]} columns (stocks)")
print()
print("First 5 rows:")
print(prices.head())

# -----------------------------------------------------------------------------
# STEP 5 — Save to CSV in the DATA/ folder
# -----------------------------------------------------------------------------
# Build the output path relative to this script's location.
script_dir  = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)          # one level up = project root
data_dir    = os.path.join(project_dir, "DATA")

os.makedirs(data_dir, exist_ok=True)               # create DATA/ if it doesn't exist

output_path = os.path.join(data_dir, "prices.csv")
prices.to_csv(output_path)

print(f"\nData saved to: {output_path}")
print("Script 01 complete.")
