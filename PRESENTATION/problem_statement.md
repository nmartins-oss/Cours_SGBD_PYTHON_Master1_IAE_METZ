# Problem Statement
## Value at Risk Analysis on a US Equity Portfolio
### Master 1 Finance — IAE Metz — Academic Group Project
### Noah MARTINS DE PINA, Evrim ACER, Lenny MOUKAH, Syphax BOUARABA

---

## Context

Financial institutions and investors are constantly exposed to market risk — the risk that the value of an asset or portfolio will decline due to changes in market conditions. Measuring and managing this risk is a central concern in modern finance.

One of the most widely used tools for quantifying market risk is the **Value at Risk (VaR)**. Since the 1990s, VaR has become a standard metric in risk management, required under international regulatory frameworks such as **Basel III**. It provides a simple and intuitive answer to the question: *"How much can I lose, and how likely is that?"*

---

## Research Question

**How can we estimate the daily market risk of a diversified US equity portfolio, and how do different VaR estimation methods compare in their results and underlying assumptions?**

---

## Objectives

This project aims to:

1. Build a simple, equally weighted portfolio of US stocks from five different sectors.
2. Download and process real historical market data using Python and the Yahoo Finance API.
3. Compute the **1-day Value at Risk at 95% confidence** using three different methods:
   - The **Historical method**, which makes no distributional assumption.
   - The **Parametric method**, which assumes returns follow a normal distribution.
   - The **Monte Carlo simulation method**, which generates random scenarios.
4. Compare the results of the three methods and discuss their respective assumptions and limitations.
5. Draw practical conclusions about the risk profile of the portfolio.

---

## Methodology

We work with daily closing prices downloaded from Yahoo Finance for the period **January 2019 to December 2024**, covering approximately 1,500 trading days. Daily percentage returns are computed for each stock, and an equally weighted portfolio return series is constructed.

The three VaR methods are applied to this portfolio return series:

- **Historical VaR:** The 5th percentile of observed historical returns.
- **Parametric VaR:** Computed as μ − 1.645σ, where μ is the mean daily return and σ is the daily standard deviation.
- **Monte Carlo VaR:** The 5th percentile of 100,000 simulated returns drawn from a normal distribution calibrated on historical data.

---

## Scope and Limitations

This project focuses on **market risk only**, within a simplified academic framework. It does not account for:
- Liquidity risk or transaction costs
- Credit risk or counterparty risk
- The limitations of the normality assumption (fat tails, skewness)
- Dynamic correlations between assets

These limitations are acknowledged and constitute potential directions for further study.

---

## Expected Contribution

By the end of this project, we aim to demonstrate that different VaR methods produce different risk estimates, and that the choice of method matters. We also aim to show that Python is a practical and accessible tool for quantitative finance analysis, even at an academic level.

---

*Master 1 Finance — IAE Metz — Academic Group Project*
