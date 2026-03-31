# =============================================================================
# SCRIPT 02 — INSPECT AND CLEAN THE DATA
# =============================================================================
# Purpose: Load the downloaded price data, check its quality, and handle
#          any missing values. This is a standard step in any data project.
#
# Input:   DATA/prices.csv
# Output:  DATA/prices_clean.csv — cleaned price data ready for analysis
# =============================================================================

import pandas as pd
import os

# -----------------------------------------------------------------------------
# STEP 1 — Load the data
# -----------------------------------------------------------------------------
script_dir  = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir    = os.path.join(project_dir, "DATA")

input_path  = os.path.join(data_dir, "prices.csv")

print("Loading price data...")
prices = pd.read_csv(input_path, index_col=0, parse_dates=True)

print(f"Data loaded: {prices.shape[0]} rows x {prices.shape[1]} columns")
print()

# -----------------------------------------------------------------------------
# STEP 2 — Display basic information
# -----------------------------------------------------------------------------
print("=" * 60)
print("BASIC INFORMATION")
print("=" * 60)
print(prices.info())
print()

print("=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)
print(prices.head())
print()

print("=" * 60)
print("LAST 5 ROWS")
print("=" * 60)
print(prices.tail())
print()

print("=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)
print(prices.describe().round(2))
print()

# -----------------------------------------------------------------------------
# STEP 3 — Check for missing values
# -----------------------------------------------------------------------------
print("=" * 60)
print("MISSING VALUES PER STOCK")
print("=" * 60)
missing = prices.isnull().sum()
print(missing)
print()

if missing.sum() == 0:
    print("No missing values found. The data is clean.")
else:
    print(f"Total missing values: {missing.sum()}")
    print("Filling missing values using forward fill (ffill)...")
    # Forward fill: replace NaN with the last known price.
    # This is a standard method for financial time series.
    prices = prices.ffill()

    # If there are still NaN at the very start, use backward fill.
    prices = prices.bfill()

    remaining = prices.isnull().sum().sum()
    print(f"Missing values after cleaning: {remaining}")

print()

# -----------------------------------------------------------------------------
# STEP 4 — Check the date range and number of observations
# -----------------------------------------------------------------------------
print("=" * 60)
print("DATE RANGE INFORMATION")
print("=" * 60)
print(f"Start date  : {prices.index.min().date()}")
print(f"End date    : {prices.index.max().date()}")
print(f"Total days  : {len(prices)} trading days")
print()

# -----------------------------------------------------------------------------
# STEP 5 — Save the clean data
# -----------------------------------------------------------------------------
output_path = os.path.join(data_dir, "prices_clean.csv")
prices.to_csv(output_path)

print(f"Clean data saved to: {output_path}")
print("Script 02 complete.")
