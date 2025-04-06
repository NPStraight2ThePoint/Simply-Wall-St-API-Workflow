# 📈 Data Pipeline - Summary

## 🚀 Overview
This repository demonstrates the creation of a data pipeline that retrieves financial data from the **Simply Wall St API**, processes/cleans and stores the data in a PostgreSQL database. It then performs Financial analysis based on 5 stock attributions (Value,Future,Past,Dividend,Health) and outputs a stock ranking list based on the attributions.
A Sharpe Ratio optimisation is then applied for the final 'Winners' to derive optimal weights.
Final results are being visualised in Power BI .

The project is built using:
- **Python**
- **PostgreSQL**
- **Pandas/Scipy/Numpy**
- **Excel**
- **Simply Wall St API**
- **Power BI**

## 🔹 Workflow Overview

### 1. ETL Process

* **Extract**  
  - **API** Connection & data fetch.  
  - Optimized **batch queries** for large datasets.  
  - **Error handling** (Exponential backoff, incremental batch retries) to streamline the process.  

* **Transform**  
  - JSON → DataFrame → Flattened DataFrame → CSV.  
  - Merge/Transform CSVs → Joined CSV (**API2SQL ETL Mapping**).  

* **Load (SQL Database Storage)**  
  - Insert data into **temporary tables**.  
  - Conflict/Constraint handling.  
  - Remove **nulls, duplicates, and invalid entries**.  
  - Flag **out-of-tolerance** data.  
  - Validate **expected vs actual** data → Retry ETL if needed.  
  - Validate expected state and load to formal tables.  
    📥 **[SQL Procedures](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Script%20Framework/SQL%20Procedures)**
    
### 2. Financial Analysis   
  
  - Query structured data from PostgreSQL DB and store it in formulated Excel spreadsheet.
  - Apply stock attribution analysis based on 5 factors :
     * Value (DCF Fair Value, PE vs Industry, Fair PE, Analyst Targets)
     * Future (Earnings growth forecast, Revenue growth forecast, Future ROE)
     * Past (Quality earnings, Profit Margin Growth, Earnings Trend, Growth , Earnings vs Industry)
     * Health (Assets vs ST/LT Liabilities,D/E Ratio, Operating CF Debt coverage, EBIT Interest coverage)
     * Dividend (Dividend Stability, Dividend Growth, Yield vs Industry vs Market, Payout Ratio, CF Coverage)
  - Stock filtering based on attribution Rankings, Sectors, Market Caps, Expected Returns,Volatility & Sharpe Ratio.
  - Sharpe Ratio Maximise via Numpy/Scipy for optimal weight allocation 📥 **[Script Framework](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Script%20Framework/Sharpe_Ratio%20Maximise.py)**

### 3. Power BI Visualization
- **Holdings Report**.
- **Sector Exposure**.
   
## Data
* All Exchanges(130+) & Company counts(150K+)
  📥 **[Script Framework](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Script%20Framework/Exchanges_Counts.py)**
* All Tickers under all Exchanges(150K+)
* Company Info (Sector(s), Market, MarketCap, Status) for all Tickers/Exchanges
* Insider Transactions for all Tickers/Exchanges
* Financial Indicators for all Tickers/Exchanges (130+)
  📥 **[Script Framework](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Script%20Framework/Financial%20Indicators.py)**
  📥 **[List of all Indicators](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/raw/Simply-Wall-St-API-Pipeline/Data/Simply_Statements_Data.xlsx)**
* Members for all Tickers/Exchanges
* Owners for all Tickers/Exchanges

---

## 🌍 Visualizing the Process
To better understand the pipeline, here are visual representations:

### 📝 ETL Workflow
![ETL Workflow](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/1st.png)
![ETL Workflow2](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/2nd.png)
![ETL Workflow4](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/3.png)

---



## Project Information

**Created by:** Nicholas Papadimitris  
**Timestamp:** 2025-02-09 10:26 (UTC)  
**Unique ID:** [Simply-Wall-St-API-Workflow-2025-02-09 10:26]


## Future Updates & Feedback  
This project is continuously evolving, and I plan to add more features and updates in the future.  

By sharing this work, I aim to show how to streamline your data workflow(s) and tranform them into useful insights. I'm open to feedback on its value, and if you’re interested in optimizing your workflows or improving your data processing, feel free to reach out. I'm more than happy to elaborate on any aspect of the project if you need more details!

**Author:** Nicholas Papadimitris  
📧 **Email:** nicholas.papadimitris@gmail.com  
💼 **LinkedIn:** [Nicholas Papadimitris](https://www.linkedin.com/in/nicholas-papadimitris/)

## Similar Projects Coming Soon  
I'm working on additional projects related to financial data pipelines, analytics, and investing insights. Stay tuned for more releases! 🚀  

## Disclaimer
API is still in beta, which means things are subject to change. Specs could be updated, limits might be introduced, paywalls added, or even certain features removed .
