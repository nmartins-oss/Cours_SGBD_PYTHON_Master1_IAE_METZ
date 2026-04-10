# Value at Risk (VaR) Analysis — US Equity Portfolio
### Master 1 Finance — Academic Group Project — IAE Metz 2026
### Noah MARTINS DE PINA, Evrim ACER, Lenny MOUKAH, Syphax BOUARABA

> **Presentation date: April 10, 2026**

---

## Project Objective

This project computes and compares three methods of Value at Risk (VaR) for a diversified US equity portfolio.

**VaR answers one key question:** *What is the maximum daily loss we can expect, with 95% confidence?*

We compare three approaches:
- **Historical VaR** — based directly on past returns
- **Parametric VaR** — based on the assumption of normality
- **Monte Carlo VaR** — based on simulated random scenarios

---

## Portfolio

| Ticker | Company | Sector |
|--------|---------|--------|
| AAPL | Apple | Technology |
| JPM | JPMorgan Chase | Finance |
| JNJ | Johnson & Johnson | Healthcare |
| XOM | ExxonMobil | Energy |
| WMT | Walmart | Consumer Staples |

- **Weighting:** Equal weight (20% per stock)
- **Horizon:** 1 day
- **Confidence level:** 95%
- **Period:** January 2019 – December 2024

---

## Data Source

All data is downloaded automatically from **Yahoo Finance** using the `yfinance` Python library.  
No manual file download is required. The script handles everything.

---

## Project Structure

```
project/
│
├── DATA/                          # Generated data files and charts
│   ├── prices.csv
│   ├── prices_clean.csv
│   ├── returns.csv
│   ├── portfolio_returns.csv
│   ├── var_results.csv
│   ├── chart_01_prices.png
│   ├── chart_02_portfolio_returns.png
│   ├── chart_03_histogram_var.png
│   └── chart_04_var_comparison.png
│
├── SCRIPT/                        # Python scripts
│   ├── 01_download_data.py        # Download prices from Yahoo Finance
│   ├── 02_inspect_data.py         # Inspect and clean the data
│   ├── 03_compute_returns.py      # Compute daily returns
│   ├── 04_portfolio.py            # Build equally weighted portfolio
│   ├── 05_var_calculation.py      # Calculate VaR (3 methods)
│   ├── 06_visualizations.py       # Generate charts
│   └── main.py                    # Run everything in one command
│
├── PRESENTATION/                  # Slides and presentation material
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Installation

Make sure Python 3.9 or higher is installed on your machine.

Install the required libraries by running this command in your terminal:

```bash
pip install -r requirements.txt
```

---

## How to Run

### Option 1 — Run everything at once (recommended)

```bash
cd SCRIPT
python main.py
```

### Option 2 — Run scripts one by one

```bash
cd SCRIPT
python 01_download_data.py
python 02_inspect_data.py
python 03_compute_returns.py
python 04_portfolio.py
python 05_var_calculation.py
python 06_visualizations.py
```

All output files (CSV and PNG) will be saved in the `DATA/` folder.

---

## Method Descriptions

### Historical VaR
Uses the actual distribution of past returns. Takes the 5th percentile of all observed daily returns. No mathematical assumption is required — it is purely data-driven.

### Parametric VaR (Variance-Covariance)
Assumes that portfolio returns follow a normal distribution. Uses the mean and standard deviation of historical returns combined with the z-score of 1.645 (for 95% confidence).

**Formula:** VaR = μ − 1.645 × σ

### Monte Carlo VaR
Simulates 100,000 random daily returns drawn from a normal distribution with the same mean and standard deviation as historical data. The 5th percentile of the simulated distribution is taken as the VaR.

---

## Limitations

- VaR does not indicate *how large* losses can be beyond the threshold.
- Historical VaR is backward-looking and depends on the chosen time period.
- Parametric and Monte Carlo VaR assume normality; financial returns often have fatter tails.
- The model does not account for liquidity risk or transaction costs.
- Correlations between stocks are assumed to be stable over time.

---

## Python Libraries Used

| Library | Version | Purpose |
|---------|---------|---------|
| yfinance | ≥ 0.2.30 | Yahoo Finance data download |
| pandas | ≥ 2.0.0 | Data manipulation |
| numpy | ≥ 1.24.0 | Numerical calculations |
| matplotlib | ≥ 3.7.0 | Visualizations |
| scipy | ≥ 1.11.0 | Statistical functions |

---

*Master 1 Finance — Academic Project — IAE Metz*
