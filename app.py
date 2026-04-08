import streamlit as st
import pandas as pd
from PIL import Image

# ─── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VaR Analysis — Master 1 Finance",
    page_icon="📊",
    layout="centered",
)

# ─── Title & description ───────────────────────────────────────────────────────
st.title("📊 Value at Risk (VaR) — Portfolio Analysis")
st.markdown("""
**Master 1 Finance — IAE Metz | April 2026**
**Noah MARTINS DE PINA, Evrim ACER, Lenny MOUKAH, Syphax BOUARABA**

This dashboard presents the results of our Value at Risk (VaR) analysis
on a diversified portfolio of stocks.
We computed VaR using three different methods at a **95% confidence level**
over a **1-day horizon**, then compared their results.
""")

st.divider()

# ─── Section 1: Stock prices ──────────────────────────────────────────────────
st.header("1. Historical Stock Prices")
st.markdown("Evolution of each stock's price over the observation period.")
st.image(Image.open("DATA/chart_01_prices.png"), use_container_width=True)

st.divider()

# ─── Section 2: Portfolio returns ─────────────────────────────────────────────
st.header("2. Daily Portfolio Returns")
st.markdown("Daily percentage returns of the portfolio (equal-weighted).")
st.image(Image.open("DATA/chart_02_portfolio_returns.png"), use_container_width=True)

st.divider()

# ─── Section 3: Return distribution & VaR threshold ──────────────────────────
st.header("3. Return Distribution & VaR Threshold")
st.markdown(
    "Histogram of daily returns with the Historical VaR threshold marked at the 5th percentile."
)
st.image(Image.open("DATA/chart_03_histogram_var.png"), use_container_width=True)

st.divider()

# ─── Section 4: VaR results table ─────────────────────────────────────────────
st.header("4. VaR Results by Method")
st.markdown("Summary of VaR estimates computed with each method.")

df = pd.read_csv("DATA/var_results.csv")

# Make the table easier to read
df_display = df[["Method", "VaR_percent", "Confidence", "Horizon"]].copy()
df_display["VaR_percent"] = df_display["VaR_percent"].map(lambda x: f"{x:.4f}%")
df_display.columns = ["Method", "VaR (%)", "Confidence Level", "Horizon"]

st.dataframe(df_display, use_container_width=True, hide_index=True)

st.divider()

# ─── Section 5: Method comparison chart ───────────────────────────────────────
st.header("5. Comparison of VaR Methods")
st.markdown("Visual comparison of the three VaR estimates.")
st.image(Image.open("DATA/chart_04_var_comparison.png"), use_container_width=True)

st.divider()

# ─── Section 6: Conclusion ────────────────────────────────────────────────────
st.header("6. Conclusion")
st.markdown("""
All three methods give consistent results, which confirms the reliability of our analysis:

- **Historical VaR ≈ 1.65%** — based on observed past returns (no distributional assumption).
- **Parametric VaR ≈ 1.87%** — assumes returns follow a normal distribution.
- **Monte Carlo VaR ≈ 1.86%** — simulates thousands of random scenarios.

**Interpretation:** With 95% confidence, the portfolio should not lose more than
approximately **1.65% to 1.87%** of its value in a single trading day.

The Parametric and Monte Carlo methods are slightly more conservative than
the Historical method. This is a common result: the normal distribution
assumption tends to produce slightly higher VaR estimates.

> **Key takeaway:** VaR is a useful risk measure, but it does not capture
> extreme tail events (black swans). It should be used alongside other
> risk metrics such as Expected Shortfall (CVaR).
""")

st.divider()
st.caption("Master 1 Finance — IAE Metz | VaR Project | 2026")
