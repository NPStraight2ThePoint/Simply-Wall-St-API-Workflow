# Simply-Wall-St-API-Workflow

## Overview
This repository demonstrates the creation of a data pipeline that retrieves financial data from the **Simply Wall St API**, processes, cleans, and stores the data in a PostgreSQL database and applies financial analysis.

The project is built using:
- **Python**
- **PostgreSQL**
- **Pandas**
- **Excel**
- **Simply Wall St API**

## How It Works

# Python API Queries
   * All Exchanges(130+) & Company counts(150K+)
   * All Tickers under all Exchanges(150K+)
   * Company Info (Sector(s), Market, MarketCap, Status) for all Tickers/Exchanges
   * Insider Transactions for all Tickers/Exchanges
   * Financial Indicators for all Tickers/Exchanges (130+)
   * Members for all Tickers/Exchanges
   * Owners for all Tickers/Exchanges
  
   # General ETL Process

   * API->Batch Queries->JSON->DataFrame->Flattening/Cleansing->CSV
   * Merge/Transform CSV's->Joined CSV (API2SQL ETL Column Mapping)
   * Create SQL Temp Table->Copy CSV to SQL Temp Table->INSERT to Clean SQL Table -> On Conflict/Constraint handling->DROP Temp Table

   # Data QA
   * Data Integrity Validation -> Retry Queries -> Expected State achieved

   # Financial Analysis   
   * Export clean data -> Stock Attribution Analysis -> Final Watchlist

   # Visualisation
   * Power BI Visualisation


## Final SQL Tables

1.Exchanges & Company_Counts
| index_date | exchange  | company_count |
|------------|-----------|---------------|
| 8/02/2025  | DB        | 17469         |
| 8/02/2025  | OTCPK     | 15599         |
| 8/02/2025  | LSE       | 8725          |
| 8/02/2025  | BATS-CHIXE| 6822          |
| 8/02/2025  | BSE       | 4940          |
| 8/02/2025  | TSE       | 4563          |
| 8/02/2025  | XTRA      | 3677          |
| 8/02/2025  | SZSE      | 3532          |

2.List of Tickers
| exchange | name                     | ticker | id                                     | classification_status | market_cap_usd   |
|----------|--------------------------|--------|----------------------------------------|-----------------------|------------------|
| ASX      | Ansell                   | ANN    | 25ece3b4-                              | ACTIVE                | 3174886131       |
| ASX      | Advance ZincTek          | ANO    | 5a642809-                              | ACTIVE                | 30014488.19      |
| ASX      | Anatara Lifesciences     | ANR    | 9f371156-                              | ACTIVE                | 7549833.144      |
| ASX      | Anax Metals              | ANX    | 06a27ec2-                              | ACTIVE                | 6057025.543      |
| ASX      | ANZ Group Holdings       | ANZ    | 213a0983-                              | ACTIVE                | 57863985237      |
| ...      | ...                      | ...    | ...                                    | ...                   | ...              |

3. Company Info
   
| id       | date       | exchange | ticker | name                        | market_cap | primary_industry       | secondary        | tertiary              | country   | iso2 |
|----------|------------|----------|--------|-----------------------------|------------|------------------------|------------------|-----------------------|-----------|------|
| 70e51eb9 | 19/02/2025 | ASX      | 14D    | 1414 Degrees                | 4.35M      | Capital Goods          | Electrical       | Components & Equip    | Australia | AU   |
| 867e8678 | 19/02/2025 | ASX      | 1AD    | AdAlta                      | 6.42M      | Pharma & Biotech       | Biotechs         | Biotechnology         | Australia | AU   |
| ab60d5fb | 19/02/2025 | ASX      | 1AE    | Aurora Energy Metals        | 6.03M      | Materials              | Metals & Mining  | Diversified Metals    | Australia | AU   |
| 1794b0ff | 19/02/2025 | ASX      | 1AG    | Alterra                     | 2.80M      | Food & Beverage        | Food             | Agricultural Products | Australia | AU   |
| c6c4adb8 | 19/02/2025 | ASX      | 1AI    | Algorae Pharma              | 6.44M      | Pharma & Biotech       | Biotechs         | Biotechnology         | Australia | AU   |
| ac5900dd | 19/02/2025 | ASX      | 1CG    | One Click Group             | 8.99M      | Commercial Services    | Prof. Services   | Research & Consulting | Australia | AU   |
| 24c54267 | 19/02/2025 | ASX      | 1GOV   | Vaneck 1-5Y Aus Gov Bond ETF| 0          | Financials             | Capital Markets  | Asset Mgmt & Custody  | Australia | AU   |


4. Insider Transactions
   
| ticker | exchange | date       | type  | owner                 | owner_type  | description                       | trade_min   | trade_max | shares | price_min | price_max | value  | pct_shares | pct_change | insider | filing_date  |
|--------|----------|------------|-------|-----------------------|-------------|-----------------------------------|------------|------------|--------|-----------|-----------|--------|------------|------------|---------|--------------|
| 1AD    | ASX      | 19/02/2025 | BUY   | Stuart Morris         | INDIVIDUAL  | Derivative Exercise & Retained    | 2024-06-03 | 2024-06-03 | 59.90M | 0.029999  | 0.029999  | 1.80M  | 10.06%     | 159.58%    | FALSE   | 2024-06-02   |
| 1AG    | ASX      | 19/02/2025 | BUY   | Sandon Capital Inv.   | COMPANY     | Private Acquisition               | 2023-03-28 | 2024-02-27 | 3.51M  | 0.012000  | 0.012000  | 42.13K | 0.40%      | 2.62%      | FALSE   | 2024-02-27   |
| 1AG    | ASX      | 19/02/2025 | BUY   | Sandon Capital Pty    | COMPANY     | Private Acquisition               | 2023-03-28 | 2024-02-27 | 1.18M  | 0.012000  | 0.012000  | 14.16K | 0.14%      | 1.34%      | FALSE   | 2024-02-27   |
| 1CG    | ASX      | 19/02/2025 | BUY   | Winton Willesee       | INDIVIDUAL  | Open Market Acquisition           | 2024-05-31 | 2024-05-31 | 1.33M  | 0.008957  | 0.008957  | 11.88K | 0.17%      | 19.87%     | TRUE    | 2024-06-04   |
| 1CG    | ASX      | 19/02/2025 | BUY   | Russell Baskerville   | INDIVIDUAL  | Open Market Acquisition           | 2024-06-04 | 2024-06-04 | 1.00M  | 0.010000  | 0.010000  | 10.00K | 0.13%      | 3.34%      | TRUE    | 2024-06-10   |
| 1CG    | ASX      | 19/02/2025 | BUY   | Mark Waller           | INDIVIDUAL  | Open Market Acquisition           | 2024-06-04 | 2024-06-07 | 2.00M  | 0.009144  | 0.009144  | 18.29K | 0.26%      | 3.11%      | TRUE    | 2024-06-10   |
| 1CG    | ASX      | 19/02/2025 | BUY   | Winton Willesee       | INDIVIDUAL  | Open Market Derivative Acquisition| 2024-06-07 | 2024-06-07 | 509.48K| 0.030000  | 0.030000  | 0      | -          | -          | TRUE    | 2024-06-14   |
| 1MC    | ASX      | 19/02/2025 | BUY   | Allan Charles Buckler | INDIVIDUAL  | Open Market Acquisition           | 2024-10-15 | 2024-10-18 | 1.10M  | 0.029999  | 0.029999  | 32.99K | 0.36%      | 3.21%      | TRUE    | 2024-10-21   |

5. Financial Indicators

| Ticker | Exchange | Date       | Dividends_CoveredByFCF  | ... | Future_ExpectedRevenueGrowthAboveMarket | ... | Health_STLiabilitiesCover                 | ... | Past_HighQualityPastEarnings | ... | Value_1YearReturnInLineOrAboveIndustry |
|--------|---------|------------|-------------------------|-----|------------------------------------------|-----|-------------------------------------------|-----|------------------------------|-----|----------------------------------------|
| A1N    | ASX     | 19/02/2025 | No FCF for dividends    | ... | 5.7% < Market (6%)                      | ... | Assets(A$98.7M) > Liabilities(A$81.7M)   | ... | Unprofitable                  | ... | Underperformed Media (-21%)           |
| A2B    | ASX     | 19/02/2025 | No FCF for dividends    | ... | Insufficient Data                       | ... | Assets(A$142.3M) > Liabilities(A$110.3M) | ... | High Non-Cash Earnings        | ... | Outperformed Transportation (-16.3%)  |
| A2M    | ASX     | 19/02/2025 | 47% payout, covered     | ... | 7.1% > Market (6%)                      | ... | Assets(NZ$1.4B) > Liabilities(NZ$473.9M) | ... | High-Quality Earnings         | ... | Outperformed Food (8.8%)              |
| AAI    | ASX     | 19/02/2025 | No notable dividend     | ... | 2.2% < Market (6%)                      | ... | Assets($4.9B) > Liabilities($3.4B)      | ... | One-off $341M loss            | ... | Insufficient Data                     |

   
📥 **[Sample Dataset/All Indicators](link_to_csv_or_repo)**


### 2. Data Validity Checks / SQL Procedures

This step ensures the quality of the data:
- **Check for duplicate or null rows.**
- **Verify the expected number of tickers** retrieved by reconciling `CompanyCount` vs actual total tickers.

### 3. 'Stock' Attribution Analysis

This step includes:
- Quering data from the PostgreSQL database and store it in a formulated Excel spreadsheet.
- Display stock rankings based on stock attributions.
- Filter and sort data based on stock rankings and sectors.


## Stock Attribution Analysis



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
