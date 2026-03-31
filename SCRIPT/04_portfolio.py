# =============================================================================
# SCRIPT 04 — BUILD THE EQUALLY WEIGHTED PORTFOLIO
# =============================================================================
# Purpose: Combine individual stock returns into a single portfolio return
#          series, using equal weights (20% per stock).
#
# Equal weighting is the simplest assumption: we invest the same amount
# in each stock, so each stock contributes equally to the portfolio.
#
# Formula: Portfolio Return(t) = sum of [weight_i * return_i(t)]
#          With 5 stocks: weight = 1/5 = 0.20 for each stock
#
# Input:   DATA/returns.csv
# Output:  DATA/portfolio_returns.csv — daily portfolio returns
# =============================================================================

import pandas as pd
import os

# -----------------------------------------------------------------------------
# STEP 1 — Load the individual stock returns
# -----------------------------------------------------------------------------
script_dir  = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir    = os.path.join(project_dir, "DATA")

returns = pd.read_csv(
    os.path.join(data_dir, "returns.csv"),
    index_col  = 0,
    parse_dates= True
)

print("Individual stock returns loaded.")
print(f"Stocks in portfolio: {list(returns.columns)}")
print()

# -----------------------------------------------------------------------------
# STEP 2 — Define portfolio weights
# -----------------------------------------------------------------------------
n_stocks = len(returns.columns)
weights  = [1 / n_stocks] * n_stocks    # equal weight for each stock

print("Portfolio weights (equally weighted):")
for ticker, w in zip(returns.columns, weights):
    print(f"  {ticker}: {w:.0%}")
print()

# -----------------------------------------------------------------------------
# STEP 3 — Calculate portfolio daily returns
# -----------------------------------------------------------------------------
# Multiply each stock's return by its weight, then sum across all stocks.
# This gives one portfolio return per trading day.

portfolio_returns = (returns * weights).sum(axis=1)
portfolio_returns.name = "Portfolio"   # give it a clear name

print(f"Portfolio returns computed: {len(portfolio_returns)} observations")
print()

# -----------------------------------------------------------------------------
# STEP 4 — Display portfolio statistics
# -----------------------------------------------------------------------------
print("=" * 60)
print("PORTFOLIO DAILY RETURN STATISTICS")
print("=" * 60)
stats = portfolio_returns.describe()
print(stats.round(4))
print()

mean_r = portfolio_returns.mean()
std_r  = portfolio_returns.std()

print(f"Average daily return : {mean_r:.4f}  ({mean_r*100:.2f}%)")
print(f"Daily volatility     : {std_r:.4f}   ({std_r*100:.2f}%)")
print(f"Worst day            : {portfolio_returns.min():.4f}  ({portfolio_returns.min()*100:.2f}%)")
print(f"Best day             : {portfolio_returns.max():.4f}   ({portfolio_returns.max()*100:.2f}%)")
print()

# -----------------------------------------------------------------------------
# STEP 5 — Save portfolio returns to CSV
# -----------------------------------------------------------------------------
output_path = os.path.join(data_dir, "portfolio_returns.csv")
portfolio_returns.to_csv(output_path, header=True)

print(f"Portfolio returns saved to: {output_path}")
print("Script 04 complete.")
