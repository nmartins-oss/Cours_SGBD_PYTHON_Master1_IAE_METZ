# =============================================================================
# SCRIPT 05 — VALUE AT RISK (VaR) CALCULATION
# =============================================================================
# Purpose: Compute the 1-day VaR at 95% confidence using three methods:
#
#   1. HISTORICAL VaR
#      Uses the actual past returns directly.
#      The 95% VaR = the 5th percentile of historical returns.
#      No mathematical assumption needed — purely data-driven.
#
#   2. PARAMETRIC VaR (also called Variance-Covariance method)
#      Assumes returns follow a normal distribution.
#      Uses the mean and standard deviation of past returns.
#      Formula: VaR = mean - z * std
#      Where z = 1.645 for 95% confidence (from the normal distribution table).
#
#   3. MONTE CARLO VaR
#      Simulates 100,000 random daily returns using the same mean and std.
#      Then takes the 5th percentile of these simulated returns.
#      More flexible than parametric, but similar here since we assume normality.
#
# Confidence level: 95%  →  we look at the 5th percentile (worst 5% of days)
# Horizon: 1 day
#
# Input:   DATA/portfolio_returns.csv
# Output:  Prints VaR results to the screen + saves DATA/var_results.csv
# =============================================================================

import pandas as pd
import numpy as np
import os

# For reproducibility: fixing the random seed means Monte Carlo
# gives the same result every time the script is run.
np.random.seed(42)

# -----------------------------------------------------------------------------
# STEP 1 — Load portfolio returns
# -----------------------------------------------------------------------------
script_dir  = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir    = os.path.join(project_dir, "DATA")

portfolio_returns_df = pd.read_csv(
    os.path.join(data_dir, "portfolio_returns.csv")
)

print("Preview of portfolio_returns.csv:")
print(portfolio_returns_df.head())
print("\nColumns:")
print(portfolio_returns_df.columns)

# Keep only the last column, which should contain the numeric portfolio returns
portfolio_returns = pd.to_numeric(
    portfolio_returns_df.iloc[:, -1],
    errors="coerce"
).dropna()   # convert single-column DataFrame to a Series

print("Portfolio returns loaded.")
print(f"Number of observations: {len(portfolio_returns)}")
print()

# -----------------------------------------------------------------------------
# STEP 2 — Set parameters
# -----------------------------------------------------------------------------
CONFIDENCE_LEVEL = 0.95             # 95% confidence
ALPHA            = 1 - CONFIDENCE_LEVEL   # 5% tail
N_SIMULATIONS    = 100_000          # number of Monte Carlo simulations

# -----------------------------------------------------------------------------
# STEP 3 — HISTORICAL VaR
# -----------------------------------------------------------------------------
# Sort all past daily returns from worst to best.
# The 5th percentile is the threshold below which only 5% of days fall.
# This is our historical VaR: the loss we would have exceeded only 5% of days.

historical_var = portfolio_returns.quantile(ALPHA)

print("=" * 60)
print("METHOD 1 — HISTORICAL VaR")
print("=" * 60)
print(f"The 5th percentile of historical returns: {historical_var:.4f}")
print(f"Historical VaR (95%): {abs(historical_var)*100:.2f}%")
print(f"Interpretation: On a typical day, we do not expect to lose more")
print(f"than {abs(historical_var)*100:.2f}% of portfolio value with 95% confidence.")
print()

# -----------------------------------------------------------------------------
# STEP 4 — PARAMETRIC VaR
# -----------------------------------------------------------------------------
# This method assumes returns are normally distributed.
# We compute the mean (mu) and standard deviation (sigma) of the return series.
# Then use the z-score for 95% confidence: z = 1.645

mu    = portfolio_returns.mean()   # average daily return
sigma = portfolio_returns.std()    # daily volatility (standard deviation)

z_score = 1.645    # z-score for 95% one-tailed confidence interval
                   # Meaning: only 5% of a normal distribution is below -1.645 std

parametric_var = mu - z_score * sigma

print("=" * 60)
print("METHOD 2 — PARAMETRIC VaR")
print("=" * 60)
print(f"Mean daily return (mu)   : {mu:.6f}")
print(f"Daily std deviation (sigma): {sigma:.6f}")
print(f"Z-score at 95%           : {z_score}")
print(f"Parametric VaR           : {parametric_var:.4f}")
print(f"Parametric VaR (95%): {abs(parametric_var)*100:.2f}%")
print(f"Interpretation: Assuming normally distributed returns, we do not")
print(f"expect to lose more than {abs(parametric_var)*100:.2f}% in one day, 95% of the time.")
print()

# -----------------------------------------------------------------------------
# STEP 5 — MONTE CARLO VaR
# -----------------------------------------------------------------------------
# We simulate 100,000 random daily returns drawn from a normal distribution
# with the same mean and standard deviation as our historical data.
# Then we take the 5th percentile of these simulated returns.

simulated_returns = np.random.normal(loc=mu, scale=sigma, size=N_SIMULATIONS)
monte_carlo_var   = np.percentile(simulated_returns, ALPHA * 100)

print("=" * 60)
print("METHOD 3 — MONTE CARLO VaR")
print("=" * 60)
print(f"Number of simulations : {N_SIMULATIONS:,}")
print(f"Monte Carlo VaR       : {monte_carlo_var:.4f}")
print(f"Monte Carlo VaR (95%): {abs(monte_carlo_var)*100:.2f}%")
print(f"Interpretation: Based on {N_SIMULATIONS:,} simulated scenarios, we do not")
print(f"expect to lose more than {abs(monte_carlo_var)*100:.2f}% in one day, 95% of the time.")
print()

# -----------------------------------------------------------------------------
# STEP 6 — Compare all three methods
# -----------------------------------------------------------------------------
print("=" * 60)
print("COMPARISON OF ALL THREE VaR METHODS")
print("=" * 60)
print(f"{'Method':<20} {'VaR (decimal)':<18} {'VaR (%)':<10}")
print("-" * 50)
print(f"{'Historical':<20} {historical_var:<18.6f} {abs(historical_var)*100:.4f}%")
print(f"{'Parametric':<20} {parametric_var:<18.6f} {abs(parametric_var)*100:.4f}%")
print(f"{'Monte Carlo':<20} {monte_carlo_var:<18.6f} {abs(monte_carlo_var)*100:.4f}%")
print()

# Note on differences:
# - If Historical VaR > Parametric VaR → actual returns have fatter tails than normal
# - If they are close → returns behave roughly normally
# - Monte Carlo with normal assumption should be close to Parametric

# -----------------------------------------------------------------------------
# STEP 7 — Save results
# -----------------------------------------------------------------------------
results = pd.DataFrame({
    "Method"        : ["Historical", "Parametric", "Monte Carlo"],
    "VaR_decimal"   : [historical_var, parametric_var, monte_carlo_var],
    "VaR_percent"   : [abs(historical_var)*100, abs(parametric_var)*100, abs(monte_carlo_var)*100],
    "Confidence"    : ["95%", "95%", "95%"],
    "Horizon"       : ["1 day", "1 day", "1 day"]
})

output_path = os.path.join(data_dir, "var_results.csv")
results.to_csv(output_path, index=False)

print(f"VaR results saved to: {output_path}")
print("Script 05 complete.")
