import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Load data from the Excel file / 3-Year Adjusted closes from Yahoo Finance API
df = pd.read_excel("ASX Pricing 20.xlsx", index_col=0, parse_dates=True)

# Calculate daily returns
returns = df.pct_change().dropna()

# Expected returns dictionary (analyst targets)
expected_returns_dict = {
    "ALD": 0.171, "CKF": 0.1844, "CSL": 0.214, "CUV": 1.4612, "DTL": 0.1088,
    "FLT": 0.1512, "HLO": 0.4166, "IFM": 0.33, "ING": 0.0654, "JIN": 0.0973,
    "LAU": 0.418, "MXI": 0.328, "NGI": 0.493, "NHF": 0.0793, "NIC": 0.394,
    "SIQ": 0.221, "SXE": 0.387, "TWR": 0.1507, "VEE": 0.8804, "WGX": 0.4837
}

# Align expected returns with df.columns
expected_returns_series = pd.Series(expected_returns_dict)
expected_returns = expected_returns_series.reindex(df.columns, fill_value=np.nan).to_numpy()

# Covariance matrix from historical data
cov_matrix = returns.cov()

# Number of assets
num_assets = len(expected_returns)

# Initial weights (equal allocation)
init_weights = np.ones(num_assets) / num_assets

# Constraints: sum of weights = 1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# Bounds: each weight must be between 2% and 10%
bounds = [(0.02, 0.10) for _ in range(num_assets)]

# Sharpe Ratio (negative because we minimize)
def neg_sharpe(w, exp_ret, cov_matrix):
    port_return = np.dot(w, exp_ret)
    port_volatility = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
    return -port_return / port_volatility

# Optimization to maximize Sharpe ratio

result = minimize(neg_sharpe, init_weights, args=(expected_returns, cov_matrix),
                  method='SLSQP', bounds=bounds, constraints=constraints)

# Optimized weights
optimal_weights = result.x

# Display optimized portfolio weights
print("Optimized Portfolio Weights:")
for ticker, weight in zip(df.columns, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

# Define sector mapping
sector_mapping = {
    "IFM": "Software", "JIN": "Consumer Services", "DTL": "Software", "VEE": "Capital Goods",
    "SIQ": "Commercial Services", "HLO": "Consumer Services", "CUV": "Pharmaceuticals & Biotech",
    "CKF": "Consumer Services", "FLT": "Consumer Services", "ALD": "Energy", "TWR": "Insurance",
    "NHF": "Insurance", "NIC": "Materials", "WGX": "Materials", "CSL": "Pharmaceuticals & Biotech",
    "ING": "Food, Beverage & Tobacco", "LAU": "Transportation", "MXI": "Capital Goods",
    "SXE": "Capital Goods", "NGI": "Diversified Financials"
}

# Create portfolio DataFrame
portfolio_df = pd.DataFrame({"Stock": df.columns, "Weight": optimal_weights})
portfolio_df["Sector"] = portfolio_df["Stock"].map(sector_mapping)

# Aggregate sector weights
sector_df = portfolio_df.groupby("Sector")["Weight"].sum().reset_index()

# Save to CSV for Power BI
portfolio_df.to_csv("optimized_portfolio.csv", index=False)
sector_df.to_csv("sector_exposure.csv", index=False)

print(portfolio_df)
print(sector_df)
print("✅ Data saved: optimized_portfolio.csv & sector_exposure.csv")
