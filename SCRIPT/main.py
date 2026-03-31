# =============================================================================
# MAIN SCRIPT — RUN THE ENTIRE PROJECT IN ORDER
# =============================================================================
# Purpose: This script runs all the project scripts in the correct order.
#          You can run this single file to execute the complete analysis.
#
# Order of execution:
#   1. Download data from Yahoo Finance
#   2. Inspect and clean the data
#   3. Compute daily returns
#   4. Build the equally weighted portfolio
#   5. Calculate VaR (Historical, Parametric, Monte Carlo)
#   6. Generate visualizations
#
# How to run:
#   Open a terminal in the SCRIPT/ folder and type:
#   python main.py
# =============================================================================

import subprocess
import sys
import os

# Get the directory where this script is located (the SCRIPT/ folder)
script_dir = os.path.dirname(os.path.abspath(__file__))

# List of scripts to run, in order
SCRIPTS = [
    "01_download_data.py",
    "02_inspect_data.py",
    "03_compute_returns.py",
    "04_portfolio.py",
    "05_var_calculation.py",
    "06_visualizations.py",
]

print("=" * 65)
print("  VaR ANALYSIS PROJECT — MASTER 1 FINANCE")
print("  Running all scripts in order...")
print("=" * 65)
print()

for i, script_name in enumerate(SCRIPTS, start=1):
    script_path = os.path.join(script_dir, script_name)

    print(f"[{i}/{len(SCRIPTS)}] Running: {script_name}")
    print("-" * 65)

    # Run each script using the same Python interpreter that runs this file.
    # If any script fails, we stop and report the error.
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=False   # show output directly in the terminal
    )

    if result.returncode != 0:
        print()
        print(f"ERROR: Script {script_name} failed with return code {result.returncode}")
        print("Please check the error message above and fix the issue.")
        sys.exit(1)

    print()

print("=" * 65)
print("  ALL SCRIPTS COMPLETED SUCCESSFULLY")
print()
print("  Output files are located in the DATA/ folder:")
print("    - prices.csv              : raw downloaded prices")
print("    - prices_clean.csv        : cleaned prices")
print("    - returns.csv             : individual stock daily returns")
print("    - portfolio_returns.csv   : portfolio daily returns")
print("    - var_results.csv         : VaR results (all 3 methods)")
print("    - chart_01_prices.png     : stock price evolution")
print("    - chart_02_portfolio_returns.png : portfolio returns over time")
print("    - chart_03_histogram_var.png     : histogram with VaR lines")
print("    - chart_04_var_comparison.png    : bar chart comparing VaR methods")
print("=" * 65)
